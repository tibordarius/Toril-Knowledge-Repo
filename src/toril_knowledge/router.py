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
        "causal": ("cause", "causal", "trigger", "result", "consequence", "feedback", "cascade"),
        "dependency": ("depend", "reliance", "requires", "critical", "scarcity", "substitut"),
        "legal": ("legal", "law", "jurid", "court", "regulat", "license", "jurisdiction"),
        "power": ("power", "authority", "legitim", "influence", "coerc", "veto", "mobiliz"),
        "capability": ("capability", "capacity", "reach", "readiness", "mobiliz", "project"),
        "flow": ("flow", "trade", "route", "migration", "shipping", "supply", "distribution"),
        "logistical": ("logistic", "supply", "warehouse", "transport", "provision", "resupply", "route"),
        "infrastructure": ("infrastructure", "road", "bridge", "port", "canal", "sewer", "aqueduct", "grid"),
        "ecological": ("ecolog", "habitat", "predat", "species", "migration", "pollinat", "biodivers"),
        "technological": ("technolog", "engineer", "manufactur", "mechanical", "innovation", "diffusion"),
        "epistemic": ("evidence", "claim", "belief", "uncertain", "corrobor", "contradict", "source"),
        "provenance": ("source", "record", "archive", "author", "edition", "errata", "citation"),
        "cultural": ("culture", "language", "custom", "festival", "ritual", "symbol", "identity"),
        "biological": ("disease", "health", "medicine", "poison", "immune", "infection", "patholog"),
        "interaction": ("coupling", "spillover", "externality", "interact", "cross-domain", "mediates"),
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

SYSTEM_ENRICHMENTS_BY_DOMAIN = {
    "economic_and_commercial_domains": (
        "cross_domain_coupling_layer", "externality_layer", "distributional_effect_layer",
        "shock_propagation_layer", "lag_delay_layer", "equilibrium_layer", "volatility_layer",
    ),
    "governmental_and_political_domains": (
        "institutional_friction_layer", "path_dependency_layer", "distributional_effect_layer",
        "cross_domain_coupling_layer", "lag_delay_layer", "leverage_point_layer",
    ),
    "legal_and_juridical_domains": (
        "institutional_friction_layer", "lag_delay_layer", "path_dependency_layer",
    ),
    "diplomatic_and_geopolitical_domains": (
        "shock_propagation_layer", "cross_domain_coupling_layer", "path_dependency_layer",
        "leverage_point_layer",
    ),
    "martial_and_military_domains": (
        "shock_propagation_layer", "lag_delay_layer", "cross_domain_coupling_layer",
    ),
    "security_and_intelligence_domains": (
        "shock_propagation_layer", "institutional_friction_layer", "lag_delay_layer",
    ),
    "illicit_and_criminal_domains": (
        "cross_domain_coupling_layer", "externality_layer", "shock_propagation_layer",
    ),
    "sociological_and_anthropological_domains": (
        "distributional_effect_layer", "adaptation_layer", "path_dependency_layer",
        "cross_domain_coupling_layer",
    ),
    "religious_theological_and_divine_domains": (
        "cross_domain_coupling_layer", "path_dependency_layer", "adaptation_layer",
    ),
    "arcane_magical_and_occult_domains": (
        "cross_domain_coupling_layer", "externality_layer", "shock_propagation_layer",
    ),
    "geological_hydrological_and_climatological_domains": (
        "shock_propagation_layer", "adaptation_layer", "cross_domain_coupling_layer",
    ),
    "biological_and_ecological_domains": (
        "adaptation_layer", "externality_layer", "shock_propagation_layer",
        "cross_domain_coupling_layer",
    ),
    "urban_and_settlement_domains": (
        "institutional_friction_layer", "externality_layer", "distributional_effect_layer",
        "cross_domain_coupling_layer",
    ),
    "maritime_domains": (
        "shock_propagation_layer", "lag_delay_layer", "cross_domain_coupling_layer",
    ),
    "technological_and_scientific_domains": (
        "path_dependency_layer", "adaptation_layer", "externality_layer",
        "cross_domain_coupling_layer",
    ),
    "information_knowledge_and_communication_domains": (
        "lag_delay_layer", "path_dependency_layer", "cross_domain_coupling_layer",
    ),
    "historical_domains": (
        "path_dependency_layer", "lag_delay_layer", "shock_propagation_layer",
    ),
    "cross_domain_geographic_and_synthetic_domains": (
        "cross_domain_coupling_layer", "shock_propagation_layer", "path_dependency_layer",
        "leverage_point_layer", "externality_layer",
    ),
    "material_environment_and_mobility_domains": (
        "cross_domain_coupling_layer", "shock_propagation_layer", "adaptation_layer",
        "externality_layer", "lag_delay_layer",
    ),
    "cognitive_philosophical_and_symbolic_domains": (
        "path_dependency_layer", "adaptation_layer", "cross_domain_coupling_layer",
    ),
    "scientific_and_historical_specialty_domains": (
        "path_dependency_layer", "lag_delay_layer", "shock_propagation_layer",
    ),
    "systems_and_comparative_analytical_domains": (
        "cross_domain_coupling_layer", "shock_propagation_layer", "lag_delay_layer",
        "adaptation_layer", "path_dependency_layer", "externality_layer",
        "tradeoff_layer", "distributional_effect_layer", "institutional_friction_layer",
        "equilibrium_layer", "volatility_layer", "leverage_point_layer",
    ),
}


def route_system_from_domains(selected_pack_ids: Iterable[str], top_k: int = 10) -> list[str]:
    selected = list(selected_pack_ids)
    scores: dict[str, float] = {pack_id: 1.0 for pack_id in SYSTEM_CORE}
    for domain_id in selected:
        for rank, system_id in enumerate(SYSTEM_BY_DOMAIN.get(domain_id, ())):
            scores[system_id] = scores.get(system_id, 0.0) + max(1.0, 4.0 - rank * 0.35)
        for rank, system_id in enumerate(SYSTEM_ENRICHMENTS_BY_DOMAIN.get(domain_id, ())):
            scores[system_id] = scores.get(system_id, 0.0) + max(0.75, 2.75 - rank * 0.25)

    if len(set(selected)) >= 2:
        scores["cross_domain_coupling_layer"] = scores.get("cross_domain_coupling_layer", 0.0) + 3.0
        scores["shock_propagation_layer"] = scores.get("shock_propagation_layer", 0.0) + 1.25
        scores["distributional_effect_layer"] = scores.get("distributional_effect_layer", 0.0) + 0.75

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

INFERENCE_ENRICHMENTS_BY_DOMAIN = {
    "economic_and_commercial_domains": (
        "trade_network_inference_layer", "supply_chain_inference_layer",
        "fiscal_inference_layer", "geoeconomic_inference_layer",
    ),
    "governmental_and_political_domains": (
        "institutional_inference_layer", "succession_inference_layer",
        "legal_inference_layer", "cross_domain_consequence_inference_layer",
    ),
    "legal_and_juridical_domains": (
        "legal_inference_layer", "institutional_inference_layer",
    ),
    "diplomatic_and_geopolitical_domains": (
        "diplomatic_inference_layer", "geoeconomic_inference_layer",
        "succession_inference_layer", "cross_domain_consequence_inference_layer",
    ),
    "martial_and_military_domains": (
        "logistics_inference_layer", "security_inference_layer",
        "cross_domain_consequence_inference_layer",
    ),
    "security_and_intelligence_domains": (
        "security_inference_layer", "criminal_network_inference_layer",
        "knowledge_diffusion_inference_layer",
    ),
    "illicit_and_criminal_domains": (
        "criminal_network_inference_layer", "trade_network_inference_layer",
        "security_inference_layer", "cross_domain_consequence_inference_layer",
    ),
    "sociological_and_anthropological_domains": (
        "migration_inference_layer", "cultural_diffusion_inference_layer",
        "cross_domain_consequence_inference_layer",
    ),
    "cultural_and_symbolic_domains": (
        "cultural_diffusion_inference_layer", "knowledge_diffusion_inference_layer",
    ),
    "religious_theological_and_divine_domains": (
        "religious_influence_inference_layer", "cultural_diffusion_inference_layer",
        "cross_domain_consequence_inference_layer",
    ),
    "arcane_magical_and_occult_domains": (
        "magical_economy_inference_layer", "technological_diffusion_inference_layer",
        "cross_domain_consequence_inference_layer",
    ),
    "geographic_and_spatial_domains": (
        "trade_network_inference_layer", "logistics_inference_layer",
        "infrastructure_inference_layer",
    ),
    "geological_hydrological_and_climatological_domains": (
        "environmental_inference_layer", "resource_depletion_inference_layer",
        "infrastructure_inference_layer", "cross_domain_consequence_inference_layer",
    ),
    "biological_and_ecological_domains": (
        "environmental_inference_layer", "disease_inference_layer",
        "resource_depletion_inference_layer", "cross_domain_consequence_inference_layer",
    ),
    "wilderness_and_survival_domains": (
        "environmental_inference_layer", "logistics_inference_layer",
    ),
    "urban_and_settlement_domains": (
        "infrastructure_inference_layer", "migration_inference_layer",
        "disease_inference_layer", "cross_domain_consequence_inference_layer",
    ),
    "maritime_domains": (
        "maritime_inference_layer", "trade_network_inference_layer",
        "logistics_inference_layer", "security_inference_layer",
    ),
    "technological_and_scientific_domains": (
        "technological_diffusion_inference_layer", "infrastructure_inference_layer",
        "disease_inference_layer",
    ),
    "information_knowledge_and_communication_domains": (
        "knowledge_diffusion_inference_layer", "institutional_inference_layer",
    ),
    "historical_domains": (
        "institutional_inference_layer", "succession_inference_layer",
        "cross_domain_consequence_inference_layer",
    ),
    "mundane_everyday_life_domains": (
        "supply_chain_inference_layer", "migration_inference_layer",
        "cultural_diffusion_inference_layer",
    ),
    "adventure_and_gameable_content_domains": (
        "cross_domain_consequence_inference_layer", "security_inference_layer",
        "criminal_network_inference_layer",
    ),
    "cross_domain_geographic_and_synthetic_domains": (
        "geoeconomic_inference_layer", "trade_network_inference_layer",
        "migration_inference_layer", "diplomatic_inference_layer",
        "cross_domain_consequence_inference_layer",
    ),
    "material_environment_and_mobility_domains": (
        "logistics_inference_layer", "infrastructure_inference_layer",
        "environmental_inference_layer", "resource_depletion_inference_layer",
        "disease_inference_layer", "cross_domain_consequence_inference_layer",
    ),
    "cognitive_philosophical_and_symbolic_domains": (
        "cultural_diffusion_inference_layer", "knowledge_diffusion_inference_layer",
        "institutional_inference_layer",
    ),
    "scientific_and_historical_specialty_domains": (
        "disease_inference_layer", "knowledge_diffusion_inference_layer",
        "resource_depletion_inference_layer",
    ),
    "systems_and_comparative_analytical_domains": (
        "cross_domain_consequence_inference_layer", "institutional_inference_layer",
        "trade_network_inference_layer", "supply_chain_inference_layer",
        "geoeconomic_inference_layer",
    ),
}


def route_inference_from_domains(
    selected_pack_ids: Iterable[str],
    lexical_routes: Iterable[Route] = (),
    top_k: int = 8,
) -> list[str]:
    selected = list(selected_pack_ids)
    scores: dict[str, float] = {}
    for route in lexical_routes:
        scores[route.pack_id] = scores.get(route.pack_id, 0.0) + route.score
    for domain_id in selected:
        for rank, inference_id in enumerate(INFERENCE_BY_DOMAIN.get(domain_id, ())):
            scores[inference_id] = scores.get(inference_id, 0.0) + max(1.0, 4.0 - rank * 0.5)
        for rank, inference_id in enumerate(INFERENCE_ENRICHMENTS_BY_DOMAIN.get(domain_id, ())):
            scores[inference_id] = scores.get(inference_id, 0.0) + max(0.75, 2.75 - rank * 0.3)

    if len(set(selected)) >= 2:
        scores["cross_domain_consequence_inference_layer"] = (
            scores.get("cross_domain_consequence_inference_layer", 0.0) + 3.0
        )

    for meta in ("certainty_layer", "salience_layer", "simulation_readiness_layer"):
        scores[meta] = scores.get(meta, 0.0) + 0.75
    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    return [pack_id for pack_id, _ in ordered[:top_k]]


def _tokens(value: str) -> set[str]:
    return {token.casefold() for token in TOKEN_RE.findall(value) if len(token) >= 4}
