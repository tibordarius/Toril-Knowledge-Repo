from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from .ontology import keywords_for_pack, packs


@dataclass(frozen=True, slots=True)
class Route:
    pack_id: str
    title: str
    score: float
    matches: tuple[str, ...]


TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z'-]{2,}")


def route_text(
    heading: str,
    text: str,
    *,
    layer: str = "domain",
    top_k: int = 8,
    minimum_score: float = 1.0,
) -> list[Route]:
    heading_tokens = _tokens(heading)
    text_tokens = _tokens(text)
    routes: list[Route] = []

    for pack in packs(layer):
        keywords = keywords_for_pack(pack)
        heading_hits = sorted(keywords.intersection(heading_tokens))
        body_hits = sorted(keywords.intersection(text_tokens))
        score = (3.0 * len(heading_hits)) + len(body_hits)

        category_words = _tokens(pack.title)
        score += 2.0 * len(category_words.intersection(heading_tokens))
        score += 0.5 * len(category_words.intersection(text_tokens))

        if score >= minimum_score:
            routes.append(
                Route(pack.id, pack.title, score, tuple((heading_hits + body_hits)[:24]))
            )

    routes.sort(key=lambda route: (-route.score, route.pack_id))
    return routes[:top_k]


def route_relationship_families(
    heading: str,
    text: str,
    selected_pack_ids: Iterable[str],
) -> list[str]:
    combined = " ".join([heading, text]).casefold()
    selected = " ".join(selected_pack_ids).casefold()
    families: set[str] = {"structural", "spatial", "temporal"}

    mapping = {
        "political": ("government", "politic", "administr", "monarch", "aristocrat", "governance"),
        "diplomatic": ("diplomat", "geopolit", "international", "treaty", "imperial"),
        "economic": ("economic", "commercial", "mercantile", "financial", "market", "trade", "labor"),
        "resource": ("resource", "agricultur", "extractive", "commodity", "scarcity", "ecological"),
        "military": ("martial", "military", "naval", "siege", "army", "warfare", "security"),
        "criminal": ("illicit", "criminal", "smuggl", "piracy", "underworld", "black_market"),
        "social": ("sociolog", "anthropolog", "kinship", "class", "household", "demograph"),
        "religious": ("religious", "theolog", "divine", "clerical", "cultic", "sacred"),
        "magical": ("arcane", "magical", "occult", "wizard", "sorcer", "thaumaturg", "planar"),
        "information": ("information", "knowledge", "communication", "intelligence", "espionage"),
    }

    haystack = combined + " " + selected
    for family, cues in mapping.items():
        if any(cue in haystack for cue in cues):
            families.add(family)
    return sorted(families)


SYSTEM_CORE = (
    "causal_relationship_layers",
    "dependency_layer",
    "constraint_layer",
    "risk_layer",
    "temporal_state_layer",
)

SYSTEM_BY_DOMAIN = {
    "economic_and_commercial_domains": (
        "flow_layers", "capacity_layer", "bottleneck_and_chokepoint_layer",
        "substitution_layer", "competition_layer", "incentive_layer", "network_layer",
    ),
    "governmental_and_political_domains": (
        "power_layer", "pressure_layer", "incentive_layer", "conflict_layer",
        "cooperation_layer", "resilience_layer", "network_layer",
    ),
    "legal_and_juridical_domains": (
        "power_layer", "constraint_layer", "conflict_layer", "cooperation_layer",
    ),
    "diplomatic_and_geopolitical_domains": (
        "power_layer", "pressure_layer", "conflict_layer", "cooperation_layer",
        "capability_layer", "network_layer",
    ),
    "martial_and_military_domains": (
        "capability_layer", "capacity_layer", "flow_layers", "constraint_layer",
        "vulnerability_layer", "resilience_layer", "bottleneck_and_chokepoint_layer",
    ),
    "security_and_intelligence_domains": (
        "capability_layer", "vulnerability_layer", "risk_layer", "network_layer",
    ),
    "illicit_and_criminal_domains": (
        "network_layer", "incentive_layer", "competition_layer", "conflict_layer",
        "flow_layers", "risk_layer",
    ),
    "sociological_and_anthropological_domains": (
        "pressure_layer", "incentive_layer", "power_layer", "change_layer", "trend_layer",
    ),
    "religious_theological_and_divine_domains": (
        "power_layer", "network_layer", "conflict_layer", "cooperation_layer",
        "pressure_layer",
    ),
    "arcane_magical_and_occult_domains": (
        "dependency_layer", "capability_layer", "constraint_layer",
        "vulnerability_layer", "risk_layer", "flow_layers",
    ),
    "geographic_and_spatial_domains": (
        "constraint_layer", "bottleneck_and_chokepoint_layer", "network_layer",
    ),
    "biological_and_ecological_domains": (
        "dependency_layer", "flow_layers", "pressure_layer", "vulnerability_layer",
        "resilience_layer", "threshold_layer", "cascade_layer",
    ),
    "wilderness_and_survival_domains": (
        "constraint_layer", "risk_layer", "vulnerability_layer", "resilience_layer",
    ),
    "urban_and_settlement_domains": (
        "capacity_layer", "pressure_layer", "bottleneck_and_chokepoint_layer",
        "vulnerability_layer", "resilience_layer", "network_layer",
    ),
    "maritime_domains": (
        "flow_layers", "capacity_layer", "bottleneck_and_chokepoint_layer",
        "constraint_layer", "risk_layer", "network_layer",
    ),
    "technological_and_scientific_domains": (
        "capability_layer", "capacity_layer", "constraint_layer", "substitution_layer",
        "change_layer", "trend_layer",
    ),
    "information_knowledge_and_communication_domains": (
        "flow_layers", "network_layer", "power_layer", "vulnerability_layer",
    ),
    "historical_domains": (
        "causal_relationship_layers", "change_layer", "trend_layer", "temporal_state_layer",
    ),
    "adventure_and_gameable_content_domains": (
        "risk_layer", "opportunity_layer", "conflict_layer", "vulnerability_layer",
    ),
}


def route_system_from_domains(selected_pack_ids: Iterable[str], top_k: int = 10) -> list[str]:
    scores: dict[str, float] = {pack_id: 1.0 for pack_id in SYSTEM_CORE}
    for domain_id in selected_pack_ids:
        for rank, system_id in enumerate(SYSTEM_BY_DOMAIN.get(domain_id, ())):
            scores[system_id] = scores.get(system_id, 0.0) + max(1.0, 4.0 - rank * 0.35)
    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    return [pack_id for pack_id, _ in ordered[:top_k]]


INFERENCE_BY_DOMAIN = {
    "economic_and_commercial_domains": (
        "economic_inference_layer", "missing_information_layer", "plausibility_layer"
    ),
    "governmental_and_political_domains": (
        "political_inference_layer", "missing_information_layer", "plausibility_layer"
    ),
    "diplomatic_and_geopolitical_domains": (
        "political_inference_layer", "military_inference_layer", "plausibility_layer"
    ),
    "martial_and_military_domains": (
        "military_inference_layer", "spatial_inference_layer", "plausibility_layer"
    ),
    "sociological_and_anthropological_domains": (
        "demographic_inference_layer", "political_inference_layer"
    ),
    "biological_and_ecological_domains": (
        "ecological_inference_layer", "spatial_inference_layer"
    ),
    "geographic_and_spatial_domains": (
        "spatial_inference_layer", "ecological_inference_layer"
    ),
    "urban_and_settlement_domains": (
        "urban_inference_layer", "demographic_inference_layer", "economic_inference_layer"
    ),
    "maritime_domains": (
        "spatial_inference_layer", "economic_inference_layer", "military_inference_layer"
    ),
    "adventure_and_gameable_content_domains": (
        "adventure_inference_layer", "missing_information_layer"
    ),
    "illicit_and_criminal_domains": (
        "adventure_inference_layer", "political_inference_layer", "economic_inference_layer"
    ),
    "arcane_magical_and_occult_domains": (
        "missing_information_layer", "plausibility_layer", "adventure_inference_layer"
    ),
}


def route_inference_from_domains(
    selected_pack_ids: Iterable[str],
    lexical_routes: Iterable[Route] = (),
    top_k: int = 8,
) -> list[str]:
    scores: dict[str, float] = {}
    for route in lexical_routes:
        scores[route.pack_id] = scores.get(route.pack_id, 0.0) + route.score
    for domain_id in selected_pack_ids:
        for rank, inference_id in enumerate(INFERENCE_BY_DOMAIN.get(domain_id, ())):
            scores[inference_id] = scores.get(inference_id, 0.0) + max(1.0, 4.0 - rank * 0.5)
    for meta in ("certainty_layer", "salience_layer", "simulation_readiness_layer"):
        scores[meta] = scores.get(meta, 0.0) + 0.75
    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    return [pack_id for pack_id, _ in ordered[:top_k]]


def _tokens(value: str) -> set[str]:
    return {token.casefold() for token in TOKEN_RE.findall(value) if len(token) >= 4}
