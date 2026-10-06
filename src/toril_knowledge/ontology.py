from __future__ import annotations

import json
import re
from dataclasses import dataclass
from importlib.resources import files
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Extractor:
    id: str
    name: str
    category: str
    category_id: str
    layer: str
    focus: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ExtractorPack:
    id: str
    title: str
    layer: str
    extractors: tuple[Extractor, ...]


def load_registry() -> dict:
    resource = files("toril_knowledge.data").joinpath("domain_registry.json")
    return json.loads(resource.read_text(encoding="utf-8"))


def extractors(registry: dict | None = None) -> list[Extractor]:
    registry = registry or load_registry()
    return [
        Extractor(
            id=item["id"],
            name=item["name"],
            category=item["category"],
            category_id=item["category_id"],
            layer=item["layer"],
            focus=tuple(item.get("focus", [])),
        )
        for item in registry["extractors"]
    ]


def packs(layer: str | None = None, registry: dict | None = None) -> list[ExtractorPack]:
    registry = registry or load_registry()
    grouped: dict[tuple[str, str], list[Extractor]] = {}
    titles: dict[str, str] = {}
    for ex in extractors(registry):
        if layer and ex.layer != layer:
            continue
        key = (ex.category_id, ex.layer)
        grouped.setdefault(key, []).append(ex)
        titles[ex.category_id] = ex.category
    return [
        ExtractorPack(pack_id, titles[pack_id], pack_layer, tuple(items))
        for (pack_id, pack_layer), items in grouped.items()
    ]


def relationship_families(registry: dict | None = None) -> dict[str, tuple[str, ...]]:
    registry = registry or load_registry()
    return {
        name: tuple(relations)
        for name, relations in registry.get("relationship_families", {}).items()
    }


def keywords_for_pack(pack: ExtractorPack) -> set[str]:
    words: set[str] = set()
    for ex in pack.extractors:
        words.update(_terms(ex.name))
        for focus in ex.focus:
            words.update(_terms(focus))
    words.difference_update(
        {
            "extractor", "information", "system", "systems", "relationships",
            "relationship", "other", "general", "likely", "different",
            "individual", "regional", "world", "social",
        }
    )
    return words


def _terms(value: str) -> Iterable[str]:
    for token in re.findall(r"[a-zA-Z][a-zA-Z'-]{2,}", value.casefold()):
        if len(token) >= 4:
            yield token


def prompt_block(pack: ExtractorPack) -> str:
    lines = [f"PACK: {pack.title}"]
    for ex in pack.extractors:
        focus = ", ".join(ex.focus) if ex.focus else ex.name
        lines.append(f"- {ex.name}: {focus}")
    return "\n".join(lines)
