from __future__ import annotations

import csv
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


NOVEL_RE = re.compile(r"^(\d{4})-(?:\d{2}|xx)\s+-", re.I)
EDITION_RE = re.compile(r"\b(1e|2e|3e|3\.5e|4e|5e)\b", re.I)
PRODUCT_CODE_RE = re.compile(r"\((\d{4,6})\s*(1e|2e|3e|3\.5e|4e|5e)\)", re.I)
DUP_SUFFIX_RE = re.compile(r"(?:\s+copy(?:[_ ]?\d+)?|\s*\(\d+\)|_\d+)$", re.I)
NONALNUM_RE = re.compile(r"[^a-z0-9]+")
WHITESPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True, slots=True)
class SourceInventoryRecord:
    role: str
    path: str
    filename: str
    source_key: str
    product_code: str | None
    source_type: str
    edition: str | None
    publication_year: int | None
    sha256: str
    size_bytes: int
    canonical: bool
    duplicate_status: str
    duplicate_of: str | None
    paired_path: str | None
    pair_method: str | None


def _strip_duplicate_suffix(value: str) -> str:
    current = value.strip()
    while True:
        updated = DUP_SUFFIX_RE.sub("", current).strip()
        if updated == current:
            return updated
        current = updated


def normalize_source_title(value: str) -> str:
    stem = Path(value).stem.strip()
    stem = _strip_duplicate_suffix(stem)
    stem = re.sub(r"^d_d_4_0_eng_campaign_settings_", "", stem, flags=re.I)
    stem = stem.replace("_", " ").replace("’", "'").replace("‘", "'").replace(chr(96), "'")
    stem = NONALNUM_RE.sub(" ", stem.casefold())
    return WHITESPACE_RE.sub(" ", stem).strip()


def product_code(value: str) -> str | None:
    match = PRODUCT_CODE_RE.search(Path(value).stem)
    if not match:
        return None
    return f"{match.group(1)}-{match.group(2).casefold()}"


def infer_source_type(value: str) -> str:
    name = Path(value).stem
    lowered = name.casefold()
    if "errata" in lowered:
        return "errata"
    if NOVEL_RE.match(name):
        return "novel"
    if "dragon magazine" in lowered or "dungeon magazine" in lowered:
        return "magazine"
    if "campaign setting" in lowered:
        return "campaign_setting"
    if "player's guide" in lowered or "players guide" in lowered:
        return "player_guide"
    if any(token in lowered for token in ("adventure", "module")):
        return "adventure"
    return "sourcebook"


def infer_edition(value: str) -> str | None:
    name = Path(value).stem
    match = EDITION_RE.search(name)
    if match:
        return match.group(1).casefold()
    if name.casefold().startswith("d_d_4_0_"):
        return "4e"
    return None


def infer_publication_year(value: str) -> int | None:
    match = NOVEL_RE.match(Path(value).name)
    return int(match.group(1)) if match else None


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _rank_candidate(path: Path) -> tuple[int, int, str]:
    lowered = path.as_posix().casefold()
    penalty = 0
    if "copy" in lowered:
        penalty += 10
    if re.search(r"\(\d+\)(?=\.[^.]+$)", lowered):
        penalty += 8
    if re.search(r"_\d+(?=\.[^.]+$)", lowered):
        penalty += 6
    if "__macosx" in lowered:
        penalty += 50
    if "missing" in lowered or "unreleased" in lowered:
        penalty += 20
    return penalty, len(path.as_posix()), path.as_posix().casefold()


def _pick_canonical(paths: Iterable[Path]) -> Path:
    return min(paths, key=_rank_candidate)


def build_source_inventory(root: str | Path) -> dict:
    root = Path(root)
    candidates = [
        path for path in root.rglob("*")
        if path.is_file() and path.suffix.casefold() in {".md", ".pdf"}
    ]

    metadata: dict[Path, dict] = {}
    for path in candidates:
        metadata[path] = {
            "source_key": normalize_source_title(path.name),
            "product_code": product_code(path.name),
            "source_type": infer_source_type(path.name),
            "edition": infer_edition(path.name),
            "publication_year": infer_publication_year(path.name),
            "sha256": file_sha256(path),
            "size_bytes": path.stat().st_size,
        }

    markdowns = [path for path in candidates if path.suffix.casefold() == ".md"]
    pdfs = [path for path in candidates if path.suffix.casefold() == ".pdf"]

    md_groups: dict[str, list[Path]] = {}
    pdf_groups: dict[str, list[Path]] = {}
    pdf_codes: dict[str, list[Path]] = {}
    for path in markdowns:
        md_groups.setdefault(metadata[path]["source_key"], []).append(path)
    for path in pdfs:
        pdf_groups.setdefault(metadata[path]["source_key"], []).append(path)
        code = metadata[path]["product_code"]
        if code:
            pdf_codes.setdefault(code, []).append(path)

    canonical_md = {key: _pick_canonical(paths) for key, paths in md_groups.items()}
    canonical_pdf = {key: _pick_canonical(paths) for key, paths in pdf_groups.items()}

    records: list[SourceInventoryRecord] = []
    exact_duplicate_groups = 0
    title_collision_groups = 0

    for key, paths in md_groups.items():
        hashes = {metadata[path]["sha256"] for path in paths}
        if len(paths) > 1:
            if len(hashes) == 1:
                exact_duplicate_groups += 1
            else:
                title_collision_groups += 1
        chosen = canonical_md[key]

        for path in paths:
            is_canonical = path == chosen
            if len(paths) == 1:
                duplicate_status = "unique"
                duplicate_of = None
            elif len(hashes) == 1:
                duplicate_status = "canonical" if is_canonical else "exact_duplicate"
                duplicate_of = None if is_canonical else chosen.as_posix()
            else:
                duplicate_status = "title_collision_review"
                duplicate_of = None

            pdf_matches = pdf_groups.get(key, [])
            pair_method = "title" if pdf_matches else None
            if not pdf_matches and metadata[path]["product_code"]:
                pdf_matches = pdf_codes.get(metadata[path]["product_code"], [])
                pair_method = "product_code" if pdf_matches else None
            paired = _pick_canonical(pdf_matches) if pdf_matches else None

            records.append(
                SourceInventoryRecord(
                    role="markdown",
                    path=path.as_posix(),
                    filename=path.name,
                    source_key=key,
                    product_code=metadata[path]["product_code"],
                    source_type=metadata[path]["source_type"],
                    edition=metadata[path]["edition"],
                    publication_year=metadata[path]["publication_year"],
                    sha256=metadata[path]["sha256"],
                    size_bytes=metadata[path]["size_bytes"],
                    canonical=is_canonical and duplicate_status != "title_collision_review",
                    duplicate_status=duplicate_status,
                    duplicate_of=duplicate_of,
                    paired_path=paired.as_posix() if paired else None,
                    pair_method=pair_method,
                )
            )

    for key, paths in pdf_groups.items():
        chosen = canonical_pdf[key]
        hashes = {metadata[path]["sha256"] for path in paths}
        for path in paths:
            is_canonical = path == chosen
            if len(paths) == 1:
                duplicate_status = "unique"
                duplicate_of = None
            elif len(hashes) == 1:
                duplicate_status = "canonical" if is_canonical else "exact_duplicate"
                duplicate_of = None if is_canonical else chosen.as_posix()
            else:
                duplicate_status = "title_collision_review"
                duplicate_of = None

            records.append(
                SourceInventoryRecord(
                    role="pdf",
                    path=path.as_posix(),
                    filename=path.name,
                    source_key=key,
                    product_code=metadata[path]["product_code"],
                    source_type=metadata[path]["source_type"],
                    edition=metadata[path]["edition"],
                    publication_year=metadata[path]["publication_year"],
                    sha256=metadata[path]["sha256"],
                    size_bytes=metadata[path]["size_bytes"],
                    canonical=is_canonical and duplicate_status != "title_collision_review",
                    duplicate_status=duplicate_status,
                    duplicate_of=duplicate_of,
                    paired_path=None,
                    pair_method=None,
                )
            )

    canonical_markdowns = [
        record for record in records if record.role == "markdown" and record.canonical
    ]
    paired_markdowns = [record for record in canonical_markdowns if record.paired_path]

    return {
        "root": root.as_posix(),
        "summary": {
            "markdown_files": len(markdowns),
            "pdf_files": len(pdfs),
            "canonical_markdowns": len(canonical_markdowns),
            "paired_canonical_markdowns": len(paired_markdowns),
            "unpaired_canonical_markdowns": len(canonical_markdowns) - len(paired_markdowns),
            "exact_duplicate_markdown_groups": exact_duplicate_groups,
            "title_collision_markdown_groups": title_collision_groups,
            "novel_markdowns": sum(
                1 for record in canonical_markdowns if record.source_type == "novel"
            ),
        },
        "records": [asdict(record) for record in records],
    }


def write_inventory(
    inventory: dict,
    json_path: str | Path,
    csv_path: str | Path | None = None,
) -> None:
    json_path = Path(json_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    if csv_path is None:
        return
    csv_path = Path(csv_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows = inventory["records"]
    fieldnames = list(rows[0].keys()) if rows else [
        "role", "path", "filename", "source_key", "product_code", "source_type",
        "edition", "publication_year", "sha256", "size_bytes", "canonical",
        "duplicate_status", "duplicate_of", "paired_path", "pair_method",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
