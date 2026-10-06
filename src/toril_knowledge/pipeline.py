from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openai import OpenAI


HEADING_RE = re.compile(r"^(#{1,6})[ ]+(.+?)[ ]*$")
PAGE_RE = re.compile(r"<!--[ ]*(?:page|pdf_page)[ ]*[:#]?[ ]*([0-9]+)[ ]*-->", re.I)

SYSTEM_PROMPT = """You extract auditable facts from sourcebook text.
Return JSON only with top-level keys entities, claims, relationships, and events.
Do not invent missing information. Prefer explicit claims over inference.
Keep evidence snippets short. Preserve canonical names and aliases.
Economic details matter: keep production, trade goods, prices, routes, seasonality,
labor, taxes, guilds, resources, infrastructure, shipping, credit, currencies,
and dependencies whenever the source states them.
"""

EXTRACTION_PROMPT = """Extract structured knowledge from this source section.

Entity fields: name, type, aliases, attributes.
Claim fields: subject, predicate, object, qualifiers, evidence, confidence.
Relationship fields: source, relation, target, evidence.
Event fields: name, date, location, participants, cause, consequence, evidence.

Only emit information supported by the source.

book_id: {book_id}
chunk_id: {chunk_id}
heading: {heading}
pages: {pages}

SOURCE
---
{text}
---
"""


@dataclass(slots=True)
class Section:
    heading: str
    text: str
    page_start: int | None = None
    page_end: int | None = None
    line_start: int | None = None
    line_end: int | None = None


@dataclass(slots=True)
class Chunk:
    chunk_id: str
    book_id: str
    source_path: str
    heading: str
    text: str
    page_start: int | None = None
    page_end: int | None = None
    line_start: int | None = None
    line_end: int | None = None


def parse_markdown(path: str | Path) -> list[Section]:
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    stack: list[str] = []
    body: list[str] = []
    sections: list[Section] = []
    page_start: int | None = None
    page_end: int | None = None
    heading_line: int | None = None
    body_start_line: int | None = None
    last_line: int | None = None

    def flush() -> None:
        nonlocal body, page_start, page_end, body_start_line, last_line
        text = "\n".join(body).strip()
        if text:
            heading = " > ".join(stack) if stack else "(preamble)"
            start_line = heading_line if stack and heading_line is not None else body_start_line
            sections.append(
                Section(
                    heading,
                    text,
                    page_start,
                    page_end,
                    start_line,
                    last_line,
                )
            )
        body = []
        page_start = None
        page_end = None
        body_start_line = None
        last_line = None

    for line_number, line in enumerate(lines, start=1):
        page_match = PAGE_RE.search(line)
        if page_match:
            page = int(page_match.group(1))
            if page_start is None:
                page_start = page
            page_end = page
            if body_start_line is None:
                body_start_line = line_number
            last_line = line_number
            body.append(line)
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            flush()
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            stack[:] = stack[: level - 1]
            while len(stack) < level - 1:
                stack.append("(untitled)")
            stack.append(title)
            heading_line = line_number
            continue

        if body_start_line is None and line.strip():
            body_start_line = line_number
        if line.strip():
            last_line = line_number
        body.append(line)

    flush()
    return sections


def semantic_chunks(
    sections: list[Section],
    book_id: str,
    source_path: str,
    max_chars: int = 14000,
    min_chars: int = 2500,
    overlap: int = 700,
) -> list[Chunk]:
    chunks: list[Chunk] = []
    pending: list[Section] = []
    pending_size = 0

    def make_chunk(
        heading: str,
        text: str,
        start: int | None,
        end: int | None,
        line_start: int | None,
        line_end: int | None,
    ) -> None:
        digest = hashlib.sha256((book_id + "\\x00" + heading + "\\x00" + text).encode("utf-8")).hexdigest()[:20]
        chunks.append(
            Chunk(
                digest, book_id, source_path, heading, text,
                start, end, line_start, line_end
            )
        )

    def emit(group: list[Section]) -> None:
        if not group:
            return
        heading = group[0].heading if len(group) == 1 else group[0].heading + " ... " + group[-1].heading
        text = "\\n\\n".join("## " + s.heading + "\\n" + s.text for s in group)
        starts = [s.page_start for s in group if s.page_start is not None]
        ends = [s.page_end for s in group if s.page_end is not None]
        line_starts = [s.line_start for s in group if s.line_start is not None]
        line_ends = [s.line_end for s in group if s.line_end is not None]
        make_chunk(
            heading,
            text,
            min(starts) if starts else None,
            max(ends) if ends else None,
            min(line_starts) if line_starts else None,
            max(line_ends) if line_ends else None,
        )

    for section in sections:
        if len(section.text) > max_chars:
            emit(pending)
            pending = []
            pending_size = 0
            step = max(1, max_chars - overlap)
            for index, start in enumerate(range(0, len(section.text), step), 1):
                piece = section.text[start : start + max_chars]
                make_chunk(
                    section.heading + " [part " + str(index) + "]",
                    piece,
                    section.page_start,
                    section.page_end,
                    section.line_start,
                    section.line_end,
                )
            continue

        if pending and pending_size + len(section.text) > max_chars:
            emit(pending)
            pending = []
            pending_size = 0

        pending.append(section)
        pending_size += len(section.text)

        if pending_size >= min_chars:
            emit(pending)
            pending = []
            pending_size = 0

    emit(pending)
    return chunks


def normalize(value: str) -> str:
    value = re.sub(r"[^\\w\\s'-]", "", value.casefold().strip())
    return re.sub(r"\\s+", " ", value)


def connect(path: str | Path) -> sqlite3.Connection:
    db = Path(path)
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS chunks (
          chunk_id TEXT PRIMARY KEY, book_id TEXT NOT NULL, source_path TEXT NOT NULL,
          heading TEXT NOT NULL, page_start INTEGER, page_end INTEGER,
          content TEXT NOT NULL, extracted_at TEXT
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
          chunk_id UNINDEXED, book_id UNINDEXED, heading, content
        );
        CREATE TABLE IF NOT EXISTS entities (
          id INTEGER PRIMARY KEY, chunk_id TEXT NOT NULL, name TEXT NOT NULL,
          normalized_name TEXT NOT NULL, type TEXT NOT NULL,
          aliases_json TEXT NOT NULL, attributes_json TEXT NOT NULL,
          UNIQUE(chunk_id, normalized_name, type)
        );
        CREATE TABLE IF NOT EXISTS claims (
          id INTEGER PRIMARY KEY, chunk_id TEXT NOT NULL, subject TEXT NOT NULL,
          predicate TEXT NOT NULL, object TEXT NOT NULL, qualifiers_json TEXT NOT NULL,
          evidence TEXT, confidence TEXT, claim_key TEXT NOT NULL,
          UNIQUE(chunk_id, claim_key)
        );
        CREATE TABLE IF NOT EXISTS relationships (
          id INTEGER PRIMARY KEY, chunk_id TEXT NOT NULL, source TEXT NOT NULL,
          relation TEXT NOT NULL, target TEXT NOT NULL, evidence TEXT,
          relation_key TEXT NOT NULL, UNIQUE(chunk_id, relation_key)
        );
        CREATE TABLE IF NOT EXISTS events (
          id INTEGER PRIMARY KEY, chunk_id TEXT NOT NULL, name TEXT NOT NULL,
          date_text TEXT, location TEXT, participants_json TEXT NOT NULL,
          cause TEXT, consequence TEXT, evidence TEXT
        );
        """
    )
    chunk_columns = {row[1] for row in conn.execute("PRAGMA table_info(chunks)")}
    if "line_start" not in chunk_columns:
        conn.execute("ALTER TABLE chunks ADD COLUMN line_start INTEGER")
    if "line_end" not in chunk_columns:
        conn.execute("ALTER TABLE chunks ADD COLUMN line_end INTEGER")
    conn.commit()
    install_world_model_schema(conn)
    return conn


def ingest(conn: sqlite3.Connection, chunks: list[Chunk]) -> int:
    for chunk in chunks:
        conn.execute(
            """INSERT INTO chunks
               (chunk_id, book_id, source_path, heading, page_start, page_end,
                content, extracted_at, line_start, line_end)
               VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?, ?)
               ON CONFLICT(chunk_id) DO UPDATE SET
               heading=excluded.heading,
               page_start=excluded.page_start,
               page_end=excluded.page_end,
               line_start=excluded.line_start,
               line_end=excluded.line_end,
               content=excluded.content""",
            (
                chunk.chunk_id,
                chunk.book_id,
                chunk.source_path,
                chunk.heading,
                chunk.page_start,
                chunk.page_end,
                chunk.text,
                chunk.line_start,
                chunk.line_end,
            ),
        )
        conn.execute("DELETE FROM chunks_fts WHERE chunk_id = ?", (chunk.chunk_id,))
        conn.execute(
            "INSERT INTO chunks_fts(chunk_id, book_id, heading, content) VALUES (?, ?, ?, ?)",
            (chunk.chunk_id, chunk.book_id, chunk.heading, chunk.text),
        )
    conn.commit()
    return len(chunks)


def clean_json(text: str) -> dict[str, Any]:
    fence = chr(96) * 3
    text = text.strip()
    if text.startswith(fence + "json"):
        text = text[len(fence + "json"):].lstrip()
    elif text.startswith(fence):
        text = text[len(fence):].lstrip()
    if text.endswith(fence):
        text = text[:-len(fence)].rstrip()
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("LLM output must be a JSON object")
    return data


def store_extraction(conn: sqlite3.Connection, chunk_id: str, data: dict[str, Any]) -> None:
    for entity in data.get("entities", []):
        name = str(entity.get("name", "")).strip()
        if name:
            conn.execute(
                "INSERT OR IGNORE INTO entities VALUES (NULL, ?, ?, ?, ?, ?, ?)",
                (
                    chunk_id,
                    name,
                    normalize(name),
                    str(entity.get("type", "other")),
                    json.dumps(entity.get("aliases", []), ensure_ascii=False),
                    json.dumps(entity.get("attributes", {}), ensure_ascii=False, sort_keys=True),
                ),
            )

    for claim in data.get("claims", []):
        subject = str(claim.get("subject", "")).strip()
        predicate = str(claim.get("predicate", "")).strip()
        obj = str(claim.get("object", "")).strip()
        if not (subject and predicate and obj):
            continue
        qualifiers = json.dumps(claim.get("qualifiers", {}), ensure_ascii=False, sort_keys=True)
        key_source = normalize(subject) + "\\x00" + predicate.casefold() + "\\x00" + normalize(obj) + "\\x00" + qualifiers
        key = hashlib.sha256(key_source.encode("utf-8")).hexdigest()
        conn.execute(
            "INSERT OR IGNORE INTO claims VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                chunk_id,
                subject,
                predicate,
                obj,
                qualifiers,
                str(claim.get("evidence", ""))[:320] or None,
                claim.get("confidence"),
                key,
            ),
        )

    for rel in data.get("relationships", []):
        source = str(rel.get("source", "")).strip()
        relation = str(rel.get("relation", "")).strip()
        target = str(rel.get("target", "")).strip()
        if not (source and relation and target):
            continue
        key = hashlib.sha256((normalize(source) + "\\x00" + relation.casefold() + "\\x00" + normalize(target)).encode("utf-8")).hexdigest()
        conn.execute(
            "INSERT OR IGNORE INTO relationships VALUES (NULL, ?, ?, ?, ?, ?, ?)",
            (chunk_id, source, relation, target, str(rel.get("evidence", ""))[:320] or None, key),
        )

    for event in data.get("events", []):
        name = str(event.get("name", "")).strip()
        if name:
            conn.execute(
                "INSERT INTO events VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    chunk_id,
                    name,
                    event.get("date"),
                    event.get("location"),
                    json.dumps(event.get("participants", []), ensure_ascii=False),
                    event.get("cause"),
                    event.get("consequence"),
                    str(event.get("evidence", ""))[:320] or None,
                ),
            )

    conn.execute("UPDATE chunks SET extracted_at = datetime('now') WHERE chunk_id = ?", (chunk_id,))
    conn.commit()


def extract_pending(
    conn: sqlite3.Connection,
    book_id: str | None = None,
    model: str | None = None,
    limit: int | None = None,
) -> int:
    selected_model = model or os.getenv("TORIL_LLM_MODEL")
    if not selected_model:
        raise RuntimeError("Set TORIL_LLM_MODEL or pass --model.")

    sql = "SELECT * FROM chunks WHERE extracted_at IS NULL"
    params: list[Any] = []
    if book_id:
        sql += " AND book_id = ?"
        params.append(book_id)
    sql += " ORDER BY rowid"
    if limit is not None:
        sql += " LIMIT ?"
        params.append(limit)

    rows = conn.execute(sql, params).fetchall()
    client = OpenAI()

    for row in rows:
        pages = "unknown"
        if row["page_start"] is not None:
            pages = str(row["page_start"])
            if row["page_end"] not in (None, row["page_start"]):
                pages += "-" + str(row["page_end"])

        prompt = EXTRACTION_PROMPT.format(
            book_id=row["book_id"],
            chunk_id=row["chunk_id"],
            heading=row["heading"],
            pages=pages,
            text=row["content"],
        )
        response = client.responses.create(
            model=selected_model,
            instructions=SYSTEM_PROMPT,
            input=prompt,
        )
        store_extraction(conn, row["chunk_id"], clean_json(response.output_text))

    return len(rows)


def search_chunks(conn: sqlite3.Connection, query: str, limit: int = 10) -> list[dict[str, Any]]:
    rows = conn.execute(
        """SELECT c.chunk_id, c.book_id, c.heading, c.page_start, c.page_end,
                  c.line_start, c.line_end,
                  snippet(chunks_fts, 3, '[', ']', ' ... ', 18) AS snippet
           FROM chunks_fts JOIN chunks c USING(chunk_id)
           WHERE chunks_fts MATCH ?
           ORDER BY bm25(chunks_fts)
           LIMIT ?""",
        (query, limit),
    ).fetchall()
    return [dict(row) for row in rows]


def entity_dossier(conn: sqlite3.Connection, name: str) -> dict[str, Any]:
    norm = normalize(name)
    mentions = conn.execute("SELECT * FROM entities WHERE normalized_name = ?", (norm,)).fetchall()
    claims = conn.execute(
        """SELECT claims.*, chunks.book_id, chunks.heading, chunks.page_start, chunks.page_end
           FROM claims JOIN chunks USING(chunk_id)
           WHERE lower(subject) = lower(?) OR lower(object) = lower(?)
           ORDER BY claims.id""",
        (name, name),
    ).fetchall()
    relationships = conn.execute(
        """SELECT relationships.*, chunks.book_id, chunks.heading, chunks.page_start, chunks.page_end
           FROM relationships JOIN chunks USING(chunk_id)
           WHERE lower(source) = lower(?) OR lower(target) = lower(?)
           ORDER BY relationships.id""",
        (name, name),
    ).fetchall()
    return {
        "entity": name,
        "mentions": [dict(row) for row in mentions],
        "claims": [dict(row) for row in claims],
        "relationships": [dict(row) for row in relationships],
    }


def write_dossier(data: dict[str, Any], output: str | Path) -> Path:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# " + data["entity"], "", "## Claims", ""]
    for claim in data["claims"]:
        pages = claim.get("page_start")
        if pages is not None and claim.get("page_end") not in (None, pages):
            pages = str(pages) + "-" + str(claim["page_end"])
        source = str(claim.get("book_id")) + " | " + str(claim.get("heading"))
        if pages is not None:
            source += " | p. " + str(pages)
        lines.append("- **" + claim["predicate"] + "**: " + claim["object"])
        lines.append("  Source: " + source)
    lines.extend(["", "## Relationships", ""])
    for rel in data["relationships"]:
        lines.append("- " + rel["source"] + " **" + rel["relation"] + "** " + rel["target"])
    path.write_text("\\n".join(lines) + "\\n", encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(prog="toril", description="Toril knowledge extraction pipeline")
    parser.add_argument("--db", default=os.getenv("TORIL_DB_PATH", "data/toril.db"))
    sub = parser.add_subparsers(dest="command", required=True)

    ingest_parser = sub.add_parser("ingest")
    ingest_parser.add_argument("markdown")
    ingest_parser.add_argument("--book-id")
    ingest_parser.add_argument("--max-chars", type=int, default=14000)
    ingest_parser.add_argument("--min-chars", type=int, default=2500)
    ingest_parser.add_argument("--overlap", type=int, default=700)
    ingest_parser.add_argument("--title")
    ingest_parser.add_argument("--edition")
    ingest_parser.add_argument("--publication-year", type=int)
    ingest_parser.add_argument("--setting-date")
    ingest_parser.add_argument("--source-type", default="sourcebook")
    ingest_parser.add_argument("--canon-tier", default="official")

    extract_parser = sub.add_parser("extract")
    extract_parser.add_argument("--book-id")
    extract_parser.add_argument("--model")
    extract_parser.add_argument("--limit", type=int)

    search_parser = sub.add_parser("search")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=10)

    dossier_parser = sub.add_parser("dossier")
    dossier_parser.add_argument("entity")
    dossier_parser.add_argument("--out")

    route_parser = sub.add_parser("route")
    route_parser.add_argument("--book-id", required=True)
    route_parser.add_argument("--limit", type=int)
    route_parser.add_argument("--domain-top-k", type=int, default=8)
    route_parser.add_argument("--system-top-k", type=int, default=6)
    route_parser.add_argument("--inference-top-k", type=int, default=6)

    world_parser = sub.add_parser("extract-world")
    world_parser.add_argument("--book-id", required=True)
    world_parser.add_argument("--model")
    world_parser.add_argument("--mode", choices=["lean", "standard", "deep", "exhaustive"], default="deep")
    world_parser.add_argument("--limit", type=int)

    args = parser.parse_args()
    conn = connect(args.db)

    if args.command == "ingest":
        path = Path(args.markdown)
        book_id = args.book_id or path.stem.lower().replace(" ", "-")
        sections = parse_markdown(path)
        chunks = semantic_chunks(
            sections,
            book_id,
            str(path),
            max_chars=args.max_chars,
            min_chars=args.min_chars,
            overlap=args.overlap,
        )
        chunk_count = ingest(conn, chunks)
        register_source(
            conn,
            book_id=book_id,
            title=args.title or path.stem,
            edition=args.edition,
            publication_year=args.publication_year,
            setting_date=args.setting_date,
            source_type=args.source_type,
            canon_tier=args.canon_tier,
            source_path=str(path),
            sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        )
        print(
            json.dumps(
                {
                    "book_id": book_id,
                    "sections": len(sections),
                    "chunks": chunk_count,
                    "edition": args.edition,
                    "setting_date": args.setting_date,
                },
                indent=2,
            )
        )
        return

    if args.command == "extract":
        print(json.dumps({"extracted_chunks": extract_pending(conn, args.book_id, args.model, args.limit)}, indent=2))
        return

    if args.command == "search":
        print(json.dumps(search_chunks(conn, args.query, args.limit), indent=2, ensure_ascii=False))
        return

    if args.command == "dossier":
        data = entity_dossier(conn, args.entity)
        if args.out:
            print(write_dossier(data, args.out))
        else:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    if args.command == "route":
        sql = "SELECT * FROM chunks WHERE book_id=? ORDER BY rowid"
        params: list[Any] = [args.book_id]
        if args.limit:
            sql += " LIMIT ?"
            params.append(args.limit)
        rows = conn.execute(sql, params).fetchall()
        planned = []
        for row in rows:
            routes = plan_chunk_routes(
                conn,
                row,
                domain_top_k=args.domain_top_k,
                system_top_k=args.system_top_k,
                inference_top_k=args.inference_top_k,
            )
            planned.append(
                {
                    "chunk_id": row["chunk_id"],
                    "heading": row["heading"],
                    "domain": [route.pack_id for route in routes["domain"]],
                    "system": [route.pack_id for route in routes["system"]],
                    "inference": [route.pack_id for route in routes["inference"]],
                }
            )
        print(json.dumps(planned, indent=2, ensure_ascii=False))
        return

    if args.command == "extract-world":
        result = run_world_model(
            conn,
            book_id=args.book_id,
            model=args.model,
            mode=args.mode,
            limit=args.limit,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return


if __name__ == "__main__":
    main()
