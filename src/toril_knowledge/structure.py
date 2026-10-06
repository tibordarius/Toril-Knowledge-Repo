from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChunkClassification:
    kind: str
    confidence: float
    reasons: tuple[str, ...]


SPACE_RE = re.compile(r"\s+")
NONWORD_RE = re.compile(r"[^a-z0-9 ]+")

CONTENTS_RE = re.compile(r"\b(?:table of contents|contents|index)\b", re.I)
ERRATA_RE = re.compile(r"\b(?:errata|rules corrections?|official corrections?)\b", re.I)
INDEX_NUMBER_RE = re.compile(r"\b\d{1,3}\b")
INDEX_WORD_RE = re.compile(r"\b[A-Za-z]{3,}\b")
FRONT_HEADING_RE = re.compile(
    r"\b(?:credits?|editors?|designers?|cartographers?|illustrators?|isbn|copyright|printing)\b",
    re.I,
)
RULE_HEADING_RE = re.compile(
    r"\b(?:characters?|character options?|classes?|prestige classes?|feats?|skills?|"
    r"spell descriptions?|domain spells?|equipment|weapons?|armor|monster levels?|"
    r"what you need to play|converting core d d)\b",
    re.I,
)

LORE_CONTAINER_RE = re.compile(
    r"\b(?:life in faerun|life in faerûn|geography|deities|organizations?|"
    r"running the realms)\b",
    re.I,
)

FRONT_TEXT_CUES = (
    "isbn",
    "wizards of the coast",
    "all rights reserved",
    "printed in",
    "first printing",
    "editor",
    "designer",
    "cartographer",
    "illustrator",
)

RULE_TEXT_PATTERNS = (
    re.compile(r"\bprerequisite\b", re.I),
    re.compile(r"\bbenefit\b", re.I),
    re.compile(r"\bsaving throw\b", re.I),
    re.compile(r"\bspell resistance\b", re.I),
    re.compile(r"\bcaster level\b", re.I),
    re.compile(r"\bclass skills?\b", re.I),
    re.compile(r"\bskill points?\b", re.I),
    re.compile(r"\bbase attack\b", re.I),
    re.compile(r"\bhit die\b", re.I),
    re.compile(r"\bcomponents?\s*:", re.I),
    re.compile(r"\bduration\s*:", re.I),
    re.compile(r"\brange\s*:", re.I),
)

STAT_BLOCK_PATTERNS = (
    re.compile(r"\bstr\b.{0,80}\bdex\b.{0,80}\bcon\b.{0,80}\bint\b.{0,80}\bwis\b.{0,80}\bcha\b", re.I | re.S),
    re.compile(r"\b(?:ac|armor class)\s*[: ]\s*\d+", re.I),
    re.compile(r"\b(?:hp|hit points?)\s*[: ]\s*\d+", re.I),
    re.compile(r"\b(?:fort|ref|will)\s*[+\-]?\s*\d+", re.I),
    re.compile(r"\b(?:cr|challenge rating)\s*[: ]\s*\d+", re.I),
    re.compile(r"\binitiative\s*[: ]\s*[+\-]?\d+", re.I),
)


def _normalized(value: str) -> str:
    value = NONWORD_RE.sub(" ", value.casefold())
    return SPACE_RE.sub(" ", value).strip()


def classify_chunk(heading: str, text: str) -> ChunkClassification:
    heading_norm = _normalized(heading)
    text_norm = _normalized(text[:12000])
    reasons: list[str] = []

    if CONTENTS_RE.search(heading_norm):
        reasons.append("contents/index heading")
        return ChunkClassification("contents_index", 0.99, tuple(reasons))

    # OCR often truncates INDEX to INDE.
    if heading_norm == "inde" or heading_norm.startswith("inde index"):
        reasons.append("OCR index heading")
        return ChunkClassification("contents_index", 0.98, tuple(reasons))

    page_number_count = len(INDEX_NUMBER_RE.findall(text[:12000]))
    word_count = len(INDEX_WORD_RE.findall(text[:12000]))
    index_density = page_number_count / max(1, page_number_count + word_count)
    if page_number_count >= 100 and index_density >= 0.55:
        reasons.append(
            f"index-like numeric density ({page_number_count} page-number tokens, {index_density:.2f})"
        )
        return ChunkClassification("contents_index", 0.97, tuple(reasons))

    if ERRATA_RE.search(heading_norm) or (
        "errata" in text_norm[:800] and "correction" in text_norm[:1200]
    ):
        reasons.append("embedded errata/correction section")
        return ChunkClassification("errata", 0.98, tuple(reasons))

    front_hits = sum(cue in text_norm for cue in FRONT_TEXT_CUES)
    if FRONT_HEADING_RE.search(heading_norm):
        front_hits += 2
        reasons.append("front-matter heading")
    if heading_norm.startswith("preamble"):
        front_hits += 1
        reasons.append("preamble")
    if front_hits >= 3:
        reasons.append(f"{front_hits} front-matter cues")
        return ChunkClassification("front_matter", min(0.99, 0.72 + front_hits * 0.05), tuple(reasons))

    stat_hits = sum(bool(pattern.search(text[:12000])) for pattern in STAT_BLOCK_PATTERNS)
    if stat_hits >= 3 and not LORE_CONTAINER_RE.search(heading_norm):
        reasons.append(f"{stat_hits} stat-block patterns")
        return ChunkClassification("stat_block", min(0.98, 0.72 + stat_hits * 0.05), tuple(reasons))
    if stat_hits >= 3:
        reasons.append("embedded stat block inside lore container")

    rule_hits = sum(bool(pattern.search(text[:12000])) for pattern in RULE_TEXT_PATTERNS)
    if RULE_HEADING_RE.search(heading_norm):
        rule_hits += 2
        reasons.append("rules/mechanics heading")
    if rule_hits >= 3:
        reasons.append(f"{rule_hits} rules/mechanics cues")
        return ChunkClassification("rules_mechanics", min(0.96, 0.68 + rule_hits * 0.04), tuple(reasons))

    return ChunkClassification("lore", 0.65, ("no structural suppression cues",))


def routing_limits(
    classification: ChunkClassification,
    *,
    domain_top_k: int,
    system_top_k: int,
    inference_top_k: int,
) -> dict[str, int | bool]:
    if classification.kind in {"front_matter", "contents_index"}:
        return {
            "domain_top_k": 0,
            "system_top_k": 0,
            "inference_top_k": 0,
            "skip_entity": True,
            "skip_relationship": True,
            "skip_epistemic": True,
        }

    if classification.kind in {"rules_mechanics", "stat_block"}:
        return {
            "domain_top_k": min(domain_top_k, 4),
            "system_top_k": 0,
            "inference_top_k": 0,
            "skip_entity": False,
            "skip_relationship": True,
            "skip_epistemic": True,
        }

    if classification.kind == "errata":
        return {
            "domain_top_k": min(domain_top_k, 4),
            "system_top_k": 0,
            "inference_top_k": 0,
            "skip_entity": False,
            "skip_relationship": True,
            "skip_epistemic": False,
        }

    return {
        "domain_top_k": domain_top_k,
        "system_top_k": system_top_k,
        "inference_top_k": inference_top_k,
        "skip_entity": False,
        "skip_relationship": False,
        "skip_epistemic": False,
    }
