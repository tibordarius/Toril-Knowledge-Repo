from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import uuid
from typing import Any, Iterable

from openai import OpenAI

from .ontology import ExtractorPack, packs, prompt_block, relationship_families
from .router import (
    Route,
    route_inference_from_domains,
    route_relationship_families,
    route_system_from_domains,
    route_text,
)


MODE_CONFIG = {
    "lean": {"domain_top_k": 4, "system_top_k": 0, "inference_top_k": 0, "max_pass": 3},
    "standard": {"domain_top_k": 8, "system_top_k": 4, "inference_top_k": 0, "max_pass": 4},
    "deep": {"domain_top_k": 12, "system_top_k": 8, "inference_top_k": 6, "max_pass": 7},
    "exhaustive": {"domain_top_k": 99, "system_top_k": 99, "inference_top_k": 99, "max_pass": 7},
}

RECORD_TYPES = {
    "entity", "attribute", "claim", "relation", "event", "quantity", "state",
    "flow", "dependency", "constraint", "capacity", "pressure", "incentive",
    "power", "vulnerability", "resilience", "risk", "opportunity", "trend",
    "inference", "gap", "perspective", "conflict", "correction",
}

BASE_SYSTEM = """You build an auditable world model from sourcebook text.
Return JSON only: {"records": [...]}.

Every record must contain:
record_type, subject, predicate, object, attributes, evidence,
confidence_type, scale, salience, simulation_readiness,
valid_from, valid_until, perspective, source_status.

Rules:
- Preserve source wording in names, titles, dates, quantities, institutions and terminology.
- Never silently reconcile different editions, eras, narrators, rumors or perspectives.
- For source-grounded passes, do not invent missing facts.
- evidence must be a short support fragment.
- source_status is "explicit" or "strong_implication" unless this is an inference pass.
- Use null when a field is unknown.
- Separate a fact from its interpretation.
- Prefer several atomic records over one overloaded record.
- If source_type is errata, emit correction records for the target material instead of
  treating corrected game text as independent world-state lore.
"""

ENTITY_PROMPT = """PASS 1: ENTITY AND ATTRIBUTE EXTRACTION

Extract people, places, settlements, regions, organizations, factions, institutions,
objects, artifacts, documents, creatures, species, events, concepts, titles and aliases.
Also capture explicit numeric/statistical attributes and obvious entity-to-entity relations.
Do not infer systems yet.
"""

RELATIONSHIP_PROMPT = """PASS 3: RELATIONSHIP EXTRACTION

Extract typed relationships only when the source supports them.
Allowed relationship families and predicates:
{relations}

Do not create relations merely because they would be plausible.
"""

TEMPORAL_EPISTEMIC_PROMPT = """PASS 6-7: TEMPORAL AND EPISTEMIC MODEL

Extract time-bounded states, changes, eras, recurrence, trends, source perspective,
rumor/uncertainty, contradictory claims within this chunk, and statements whose truth
is explicitly limited to a time, faction, narrator or location.

Do not compare against other books here. Cross-book conflict detection happens later.
"""

INFERENCE_RULES = """This is an inference pass. You may derive new records, but each inference must:
- use source_status="inferred";
- explain the reasoning in attributes.reasoning;
- state assumptions in attributes.assumptions;
- identify uncertainty;
- never overwrite explicit lore;
- distinguish "likely", "possible", and "required by the evidence".
"""


def install_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS source_catalog (
          book_id TEXT PRIMARY KEY,
          title TEXT,
          edition TEXT,
          publication_year INTEGER,
          setting_date TEXT,
          source_type TEXT,
          canon_tier TEXT,
          source_path TEXT,
          sha256 TEXT,
          notes TEXT,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS world_runs (
          run_id TEXT PRIMARY KEY,
          book_id TEXT,
          mode TEXT NOT NULL,
          model TEXT NOT NULL,
          status TEXT NOT NULL,
          started_at TEXT DEFAULT CURRENT_TIMESTAMP,
          completed_at TEXT,
          config_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS chunk_routes (
          chunk_id TEXT NOT NULL,
          layer TEXT NOT NULL,
          pack_id TEXT NOT NULL,
          score REAL NOT NULL,
          matches_json TEXT NOT NULL,
          active INTEGER NOT NULL DEFAULT 1,
          PRIMARY KEY (chunk_id, layer, pack_id)
        );

        CREATE TABLE IF NOT EXISTS knowledge_records (
          record_id TEXT PRIMARY KEY,
          run_id TEXT,
          chunk_id TEXT NOT NULL,
          book_id TEXT NOT NULL,
          pass_no INTEGER NOT NULL,
          layer TEXT NOT NULL,
          extractor_id TEXT,
          record_type TEXT NOT NULL,
          subject TEXT,
          predicate TEXT,
          object_json TEXT,
          attributes_json TEXT NOT NULL,
          evidence TEXT,
          confidence REAL,
          confidence_type TEXT,
          scale TEXT,
          salience TEXT,
          simulation_readiness TEXT,
          valid_from TEXT,
          valid_until TEXT,
          perspective TEXT,
          source_status TEXT NOT NULL,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_knowledge_subject
          ON knowledge_records(book_id, subject);
        CREATE INDEX IF NOT EXISTS idx_knowledge_chunk
          ON knowledge_records(chunk_id, pass_no);
        CREATE INDEX IF NOT EXISTS idx_knowledge_type
          ON knowledge_records(record_type, predicate);

        CREATE TABLE IF NOT EXISTS extraction_audit (
          id INTEGER PRIMARY KEY,
          run_id TEXT NOT NULL,
          chunk_id TEXT NOT NULL,
          pass_no INTEGER NOT NULL,
          pack_id TEXT,
          status TEXT NOT NULL,
          model TEXT NOT NULL,
          request_hash TEXT NOT NULL,
          input_tokens INTEGER,
          output_tokens INTEGER,
          error TEXT,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS entity_aliases (
          canonical_key TEXT NOT NULL,
          alias TEXT NOT NULL,
          normalized_alias TEXT NOT NULL,
          book_id TEXT NOT NULL,
          chunk_id TEXT,
          valid_from TEXT,
          valid_until TEXT,
          PRIMARY KEY (canonical_key, normalized_alias, book_id)
        );

        CREATE TABLE IF NOT EXISTS cross_source_conflicts (
          conflict_id TEXT PRIMARY KEY,
          subject TEXT NOT NULL,
          predicate TEXT NOT NULL,
          record_ids_json TEXT NOT NULL,
          conflict_type TEXT NOT NULL,
          resolution_status TEXT NOT NULL DEFAULT 'unresolved',
          resolution_note TEXT,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()


def register_source(
    conn: sqlite3.Connection,
    *,
    book_id: str,
    title: str | None = None,
    edition: str | None = None,
    publication_year: int | None = None,
    setting_date: str | None = None,
    source_type: str = "sourcebook",
    canon_tier: str = "official",
    source_path: str | None = None,
    sha256: str | None = None,
    notes: str | None = None,
) -> None:
    install_schema(conn)
    conn.execute(
        """INSERT INTO source_catalog
           (book_id, title, edition, publication_year, setting_date, source_type,
            canon_tier, source_path, sha256, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(book_id) DO UPDATE SET
             title=COALESCE(excluded.title, title),
             edition=COALESCE(excluded.edition, edition),
             publication_year=COALESCE(excluded.publication_year, publication_year),
             setting_date=COALESCE(excluded.setting_date, setting_date),
             source_type=COALESCE(excluded.source_type, source_type),
             canon_tier=COALESCE(excluded.canon_tier, canon_tier),
             source_path=COALESCE(excluded.source_path, source_path),
             sha256=COALESCE(excluded.sha256, sha256),
             notes=COALESCE(excluded.notes, notes)""",
        (
            book_id, title, edition, publication_year, setting_date, source_type,
            canon_tier, source_path, sha256, notes,
        ),
    )
    conn.commit()


def plan_chunk_routes(
    conn: sqlite3.Connection,
    chunk: sqlite3.Row,
    *,
    domain_top_k: int = 8,
    system_top_k: int = 4,
    inference_top_k: int = 4,
) -> dict[str, list[Route]]:
    install_schema(conn)

    domain_routes = route_text(
        chunk["heading"], chunk["content"], layer="domain", top_k=domain_top_k
    )
    domain_ids = [route.pack_id for route in domain_routes]

    system_ids = route_system_from_domains(domain_ids, top_k=system_top_k) if system_top_k else []
    system_pack_map = {pack.id: pack for pack in packs("system")}
    system_routes = [
        Route(pack_id, system_pack_map[pack_id].title, float(system_top_k - index), ("domain-derived",))
        for index, pack_id in enumerate(system_ids)
        if pack_id in system_pack_map
    ]

    lexical_inference = (
        route_text(chunk["heading"], chunk["content"], layer="inference", top_k=inference_top_k)
        if inference_top_k else []
    )
    inference_ids = (
        route_inference_from_domains(domain_ids, lexical_inference, top_k=inference_top_k)
        if inference_top_k else []
    )
    inference_pack_map = {pack.id: pack for pack in packs("inference")}
    inference_routes = [
        Route(pack_id, inference_pack_map[pack_id].title, float(inference_top_k - index), ("domain+lexical",))
        for index, pack_id in enumerate(inference_ids)
        if pack_id in inference_pack_map
    ]

    planned: dict[str, list[Route]] = {
        "domain": domain_routes,
        "system": system_routes,
        "inference": inference_routes,
    }

    for layer, routes in planned.items():
        for route in routes:
            conn.execute(
                """INSERT INTO chunk_routes(chunk_id, layer, pack_id, score, matches_json, active)
                   VALUES (?, ?, ?, ?, ?, 1)
                   ON CONFLICT(chunk_id, layer, pack_id) DO UPDATE SET
                     score=excluded.score, matches_json=excluded.matches_json, active=1""",
                (chunk["chunk_id"], layer, route.pack_id, route.score, json.dumps(route.matches)),
            )
    conn.commit()
    return planned


def run_world_model(
    conn: sqlite3.Connection,
    *,
    book_id: str,
    model: str | None = None,
    mode: str = "deep",
    limit: int | None = None,
) -> dict[str, Any]:
    install_schema(conn)
    if mode not in MODE_CONFIG:
        raise ValueError(f"Unknown mode {mode!r}; choose from {sorted(MODE_CONFIG)}")
    model = model or os.getenv("TORIL_LLM_MODEL")
    if not model:
        raise RuntimeError("Set TORIL_LLM_MODEL or pass --model.")

    config = MODE_CONFIG[mode]
    run_id = uuid.uuid4().hex
    conn.execute(
        "INSERT INTO world_runs(run_id, book_id, mode, model, status, config_json) VALUES (?, ?, ?, ?, 'running', ?)",
        (run_id, book_id, mode, model, json.dumps(config, sort_keys=True)),
    )
    conn.commit()

    sql = "SELECT * FROM chunks WHERE book_id=? ORDER BY rowid"
    params: list[Any] = [book_id]
    if limit:
        sql += " LIMIT ?"
        params.append(limit)
    rows = conn.execute(sql, params).fetchall()
    client = OpenAI()
    totals = {"chunks": len(rows), "calls": 0, "records": 0}

    try:
        for chunk in rows:
            routes = plan_chunk_routes(
                conn,
                chunk,
                domain_top_k=config["domain_top_k"],
                system_top_k=config["system_top_k"],
                inference_top_k=config["inference_top_k"],
            )

            totals["records"] += _call_and_store(
                client, conn, run_id, chunk, model, 1, "entity", "core_entities",
                ENTITY_PROMPT, inference=False,
            )
            totals["calls"] += 1

            domain_packs = _packs_by_id("domain", [route.pack_id for route in routes["domain"]])
            for group in _batched(domain_packs, 3 if mode != "exhaustive" else 2):
                block = "\n\n".join(prompt_block(pack) for pack in group)
                prompt = (
                    "PASS 2: SPECIALIST DOMAIN EXTRACTION\n\n"
                    "Use each specialist lens below. Emit only supported records; it is valid for a lens "
                    "to emit nothing.\n\n" + block
                )
                pack_id = "+".join(pack.id for pack in group)
                totals["records"] += _call_and_store(
                    client, conn, run_id, chunk, model, 2, "domain", pack_id, prompt, inference=False,
                )
                totals["calls"] += 1

            family_names = route_relationship_families(
                chunk["heading"], chunk["content"], [route.pack_id for route in routes["domain"]]
            )
            relations = relationship_families()
            relation_block = "\n".join(
                f"{name}: {', '.join(relations[name])}" for name in family_names if name in relations
            )
            totals["records"] += _call_and_store(
                client, conn, run_id, chunk, model, 3, "relationship", "+".join(family_names),
                RELATIONSHIP_PROMPT.format(relations=relation_block), inference=False,
            )
            totals["calls"] += 1

            if config["max_pass"] >= 4:
                system_packs = _packs_by_id("system", [route.pack_id for route in routes["system"]])
                for group in _batched(system_packs, 3):
                    block = "\n\n".join(prompt_block(pack) for pack in group)
                    prompt = (
                        "PASS 4: SYSTEM EXTRACTION\n\n"
                        "Extract flows, dependencies, pressures, incentives, power, capabilities, capacities, "
                        "constraints, vulnerabilities, resilience, bottlenecks, substitutions, competition, "
                        "cooperation, thresholds, risks and opportunities only where supported.\n\n" + block
                    )
                    pack_id = "+".join(pack.id for pack in group)
                    totals["records"] += _call_and_store(
                        client, conn, run_id, chunk, model, 4, "system", pack_id, prompt, inference=False,
                    )
                    totals["calls"] += 1

            if config["max_pass"] >= 5:
                inference_packs = _packs_by_id("inference", [route.pack_id for route in routes["inference"]])
                for group in _batched(inference_packs, 3):
                    block = "\n\n".join(prompt_block(pack) for pack in group)
                    prompt = (
                        "PASS 5: DERIVED INFERENCE\n\n" + INFERENCE_RULES + "\n\n"
                        "Apply these inference lenses:\n" + block
                    )
                    pack_id = "+".join(pack.id for pack in group)
                    totals["records"] += _call_and_store(
                        client, conn, run_id, chunk, model, 5, "inference", pack_id, prompt, inference=True,
                    )
                    totals["calls"] += 1

            if config["max_pass"] >= 7:
                totals["records"] += _call_and_store(
                    client, conn, run_id, chunk, model, 7, "epistemic", "temporal_epistemic",
                    TEMPORAL_EPISTEMIC_PROMPT, inference=False,
                )
                totals["calls"] += 1

        conn.execute(
            "UPDATE world_runs SET status='completed', completed_at=datetime('now') WHERE run_id=?",
            (run_id,),
        )
        conn.commit()
    except Exception:
        conn.execute(
            "UPDATE world_runs SET status='failed', completed_at=datetime('now') WHERE run_id=?",
            (run_id,),
        )
        conn.commit()
        raise

    return {"run_id": run_id, "mode": mode, **totals}


def _call_and_store(
    client: OpenAI,
    conn: sqlite3.Connection,
    run_id: str,
    chunk: sqlite3.Row,
    model: str,
    pass_no: int,
    layer: str,
    pack_id: str,
    task_prompt: str,
    *,
    inference: bool,
) -> int:
    source_meta = conn.execute(
        "SELECT * FROM source_catalog WHERE book_id=?", (chunk["book_id"],)
    ).fetchone()
    meta = dict(source_meta) if source_meta else {"book_id": chunk["book_id"]}
    source_instructions = ""
    if meta.get("source_type") == "errata":
        source_instructions = (
            "\n\nERRATA MODE\n"
            "Treat this text as a correction overlay. Use record_type=correction where appropriate. "
            "Capture the target page/section, corrected field or wording, previous value when stated, "
            "and replacement value in attributes. Do not promote corrected mechanics into unrelated lore."
        )

    prior_context = ""
    if inference:
        prior = conn.execute(
            """SELECT record_type, subject, predicate, object_json, attributes_json,
                      confidence_type, scale, source_status
               FROM knowledge_records
               WHERE run_id=? AND chunk_id=? AND pass_no<=4
               ORDER BY pass_no, rowid LIMIT 150""",
            (run_id, chunk["chunk_id"]),
        ).fetchall()
        if prior:
            prior_context = (
                "\n\nPRIOR EXPLICIT/SYSTEM RECORDS\n"
                + json.dumps([dict(row) for row in prior], ensure_ascii=False)
            )

    user_prompt = (
        task_prompt
        + source_instructions
        + prior_context
        + "\n\nSOURCE METADATA\n"
        + json.dumps(meta, ensure_ascii=False, default=str)
        + "\n\nCHUNK METADATA\n"
        + json.dumps(
            {
                "chunk_id": chunk["chunk_id"],
                "heading": chunk["heading"],
                "page_start": chunk["page_start"],
                "page_end": chunk["page_end"],
                "line_start": chunk["line_start"] if "line_start" in chunk.keys() else None,
                "line_end": chunk["line_end"] if "line_end" in chunk.keys() else None,
            },
            ensure_ascii=False,
        )
        + "\n\nSOURCE TEXT\n---\n"
        + chunk["content"]
        + "\n---"
    )
    request_hash = hashlib.sha256((BASE_SYSTEM + user_prompt).encode("utf-8")).hexdigest()
    try:
        response = client.responses.create(model=model, instructions=BASE_SYSTEM, input=user_prompt)
        data = _clean_json(response.output_text)
        count = _store_records(
            conn, run_id, chunk, pass_no, layer, pack_id, data.get("records", []), inference=inference
        )
        usage = getattr(response, "usage", None)
        input_tokens = getattr(usage, "input_tokens", None) if usage else None
        output_tokens = getattr(usage, "output_tokens", None) if usage else None
        conn.execute(
            """INSERT INTO extraction_audit
               (run_id, chunk_id, pass_no, pack_id, status, model, request_hash, input_tokens, output_tokens)
               VALUES (?, ?, ?, ?, 'ok', ?, ?, ?, ?)""",
            (
                run_id, chunk["chunk_id"], pass_no, pack_id, model, request_hash,
                input_tokens, output_tokens,
            ),
        )
        conn.commit()
        return count
    except Exception as exc:
        conn.execute(
            """INSERT INTO extraction_audit
               (run_id, chunk_id, pass_no, pack_id, status, model, request_hash, error)
               VALUES (?, ?, ?, ?, 'error', ?, ?, ?)""",
            (
                run_id, chunk["chunk_id"], pass_no, pack_id, model, request_hash,
                str(exc)[:1000],
            ),
        )
        conn.commit()
        raise


def _store_records(
    conn: sqlite3.Connection,
    run_id: str,
    chunk: sqlite3.Row,
    pass_no: int,
    layer: str,
    extractor_id: str,
    records: Iterable[dict[str, Any]],
    *,
    inference: bool,
) -> int:
    count = 0
    for item in records:
        if not isinstance(item, dict):
            continue
        record_type = str(item.get("record_type") or "claim").strip().lower()
        if record_type not in RECORD_TYPES:
            record_type = "claim"
        source_status = str(item.get("source_status") or ("inferred" if inference else "explicit"))
        if inference:
            source_status = "inferred"
        elif source_status == "inferred":
            source_status = "strong_implication"

        record_id = uuid.uuid4().hex
        conn.execute(
            """INSERT INTO knowledge_records
               (record_id, run_id, chunk_id, book_id, pass_no, layer, extractor_id,
                record_type, subject, predicate, object_json, attributes_json, evidence,
                confidence, confidence_type, scale, salience, simulation_readiness,
                valid_from, valid_until, perspective, source_status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                record_id, run_id, chunk["chunk_id"], chunk["book_id"], pass_no, layer,
                extractor_id, record_type, item.get("subject"), item.get("predicate"),
                json.dumps(item.get("object"), ensure_ascii=False),
                json.dumps(item.get("attributes") or {}, ensure_ascii=False, sort_keys=True),
                str(item.get("evidence") or "")[:500] or None,
                _float_or_none(item.get("confidence")),
                item.get("confidence_type"), item.get("scale"), item.get("salience"),
                item.get("simulation_readiness"), item.get("valid_from"),
                item.get("valid_until"), item.get("perspective"), source_status,
            ),
        )
        count += 1
    conn.commit()
    return count


def _packs_by_id(layer: str, ids: Iterable[str]) -> list[ExtractorPack]:
    wanted = set(ids)
    return [pack for pack in packs(layer) if pack.id in wanted]


def _batched(items: list[Any], size: int) -> Iterable[list[Any]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


def _clean_json(text: str) -> dict[str, Any]:
    fence = chr(96) * 3
    text = text.strip()
    if text.startswith(fence + "json"):
        text = text[len(fence + "json") :].lstrip()
    elif text.startswith(fence):
        text = text[len(fence) :].lstrip()
    if text.endswith(fence):
        text = text[: -len(fence)].rstrip()
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("LLM output must be a JSON object")
    return value


def _float_or_none(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return None
