from __future__ import annotations

import math
import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable

from .ontology import keywords_for_pack, packs


@dataclass(frozen=True, slots=True)
class Route:
    pack_id: str
    title: str
    score: float
    matches: tuple[str, ...]


TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z'-]{2,}")
SPACE_RE = re.compile(r"[^a-z0-9]+")

# Words that occur across many domains and should almost never route a pack by themselves.
LOW_SIGNAL_TERMS = {
    "area", "areas", "book", "books", "city", "control", "different", "food",
    "general", "government", "individual", "information", "life", "magic",
    "magical", "market", "markets", "people", "place", "places", "population",
    "power", "rare", "region", "regional", "repair", "resources", "social",
    "system", "systems", "trade", "travel", "uses", "world",
}

# These packs are analytical overlays. They should not compete one-for-one with concrete
# domains during first-pass routing; they become eligible after concrete domains are clear.
ANALYTICAL_DOMAIN_IDS = {
    "cross_domain_geographic_and_synthetic_domains",
    "systems_and_comparative_analytical_domains",
}

# Hand-curated discriminators. These are intentionally compact: the registry still supplies
# broad vocabulary, while these terms/phrases carry enough signal to change ranking.
DOMAIN_RULES: dict[str, dict[str, object]] = {
    "economic_and_commercial_domains": {
        "strong": {
            "imports", "exports", "mercantilism", "merchant", "merchants", "coinage",
            "currency", "tariff", "tariffs", "tax", "taxes", "wages", "prices",
            "credit", "banking", "guild", "guilds", "commodities", "commerce",
        },
        "phrases": (
            "imports ", "exports ", "trade route", "merchant house", "market price",
            "coin and commerce", "tax revenue", "commercial activity",
        ),
    },
    "governmental_and_political_domains": {
        "strong": {
            "autocracy", "council", "councils", "ruler", "rulers", "governance",
            "administration", "officials", "lord", "king", "queen", "regent",
            "succession", "sovereignty", "policies", "edict", "edicts",
        },
        "phrases": (
            "ruled by", "governed by", "lord protector", "ruling class",
            "public opinion", "city administrators", "law and state",
        ),
    },
    "sociological_and_anthropological_domains": {
        "strong": {
            "slaves", "slavery", "class", "classes", "caste", "kinship", "household",
            "households", "ethnicity", "diaspora", "refugees", "status", "station",
        },
        "phrases": (
            "social class", "ruling class", "population consists", "population comprises",
            "family structure", "class and station",
        ),
    },
    "urban_and_settlement_domains": {
        "strong": {
            "ward", "wards", "district", "districts", "neighborhood", "neighborhoods",
            "sewers", "streets", "housing", "slums", "plaza", "square", "gate",
            "gates", "municipal", "cityscape",
        },
        "phrases": (
            "city ward", "city district", "urban district", "sewer system",
            "city walls", "neighborhood", "settlement pattern",
        ),
    },
    "maritime_domains": {
        "strong": {
            "harbor", "harbour", "port", "ports", "ship", "ships", "shipping", "fleet",
            "naval", "sailors", "dock", "docks", "anchorage", "piracy", "pirates",
            "strait", "coastwise",
        },
        "phrases": (
            "shipping lane", "naval harbor", "sea route", "port city", "merchant ship",
            "maritime trade", "river port",
        ),
    },
    "material_environment_and_mobility_domains": {
        "strong": {
            "transport", "road", "roads", "bridge", "bridges", "canal", "aqueduct",
            "infrastructure", "waterworks", "waste", "sanitation", "energy", "land-use",
            "mobility", "caravan", "caravans",
        },
        "phrases": (
            "road network", "transport network", "water system", "waste system",
            "land use", "food system", "travel time",
        ),
    },
    "arcane_magical_and_occult_domains": {
        "strong": {
            "weave", "wizard", "wizards", "sorcerer", "sorcerers", "spell", "spells",
            "portal", "portals", "ritual", "rituals", "necromancy", "necromantic",
            "enchantment", "reagents", "spellplague", "teleportation", "arcane",
        },
        "phrases": (
            "the weave", "magical energy", "spell casting", "arcane magic",
            "magic item", "dread ring", "high magic",
        ),
    },
    "religious_theological_and_divine_domains": {
        "strong": {
            "deity", "deities", "temple", "temples", "clergy", "priest", "priests",
            "church", "faith", "worship", "cult", "cults", "pilgrimage", "heresy",
            "divine", "holy",
        },
        "phrases": (
            "worship of", "church of", "temple of", "holy day", "divine magic",
            "religious order",
        ),
    },
    "martial_and_military_domains": {
        "strong": {
            "army", "armies", "soldier", "soldiers", "mercenary", "mercenaries",
            "garrison", "siege", "fortress", "fortification", "battle", "warfare",
            "troops", "militia", "regiment", "patrols", "blockade",
        },
        "phrases": (
            "military force", "standing army", "hired soldiers", "fighting force",
            "military ranks", "war party",
        ),
    },
    "security_and_intelligence_domains": {
        "strong": {
            "spy", "spies", "espionage", "agents", "operative", "operatives",
            "surveillance", "intelligence", "informants", "counterintelligence",
            "secrets", "security",
        },
        "phrases": (
            "secret agents", "intelligence network", "trade information",
            "operating inside", "high-ranking operative",
        ),
    },
    "illicit_and_criminal_domains": {
        "strong": {
            "smuggling", "smugglers", "blackmail", "bribery", "bribes", "racket",
            "thieves", "gang", "gangs", "underworld", "contraband", "assassin",
            "assassins", "pirates", "safehouse", "safehouses",
        },
        "phrases": (
            "slave trade", "black market", "criminal network", "thieves guild",
            "protection racket", "secretive cult",
        ),
    },
    "information_knowledge_and_communication_domains": {
        "strong": {
            "records", "archive", "archives", "literacy", "scholar", "scholars",
            "library", "libraries", "rumor", "rumors", "message", "messages",
            "knowledge", "censorship", "printing",
        },
        "phrases": (
            "spread information", "trade secrets", "written records",
            "public knowledge", "information network",
        ),
    },
    "historical_domains": {
        "strong": {
            "history", "historical", "founded", "founding", "century", "centuries",
            "era", "eras", "dynasty", "ancient", "formerly", "recently",
        },
        "phrases": (
            "recent history", "years ago", "in the year", "first era", "second era",
        ),
    },
    "geographic_and_spatial_domains": {
        "strong": {
            "north", "south", "east", "west", "border", "borders", "valley", "mountain",
            "mountains", "river", "rivers", "coast", "coastal", "island", "islands",
            "forest", "desert", "plain", "plains",
        },
        "phrases": (
            "north of", "south of", "east of", "west of", "along the coast",
            "trade corridor", "river valley",
        ),
    },
    "biological_and_ecological_domains": {
        "strong": {
            "habitat", "species", "predator", "predators", "prey", "ecosystem",
            "ecology", "flora", "fauna", "migration", "biodiversity", "pollution",
        },
        "phrases": (
            "food web", "natural habitat", "ecological pressure", "species population",
        ),
    },
    "mundane_everyday_life_domains": {
        "strong": {
            "meals", "clothing", "lodging", "inn", "inns", "tavern", "taverns",
            "household", "households", "chores", "rent", "cook", "cooking",
            "furnishings", "daily",
        },
        "phrases": (
            "daily life", "everyday life", "household goods", "room and board",
            "food and lodging",
        ),
    },
    "adventure_and_gameable_content_domains": {
        "strong": {
            "adventurers", "heroes", "encounter", "encounters", "quest", "quests",
            "treasure", "rumor", "rumors", "hook", "hooks", "characters",
        },
        "phrases": (
            "adventure hook", "the characters", "the heroes", "theme tie-in",
            "possible adventure",
        ),
    },
}


@lru_cache(maxsize=8)
def _pack_statistics(layer: str) -> tuple[int, dict[str, int]]:
    selected = packs(layer)
    document_frequency: dict[str, int] = {}
    for pack in selected:
        for keyword in keywords_for_pack(pack):
            document_frequency[keyword] = document_frequency.get(keyword, 0) + 1
    return len(selected), document_frequency


def _idf(term: str, layer: str) -> float:
    pack_count, df = _pack_statistics(layer)
    frequency = df.get(term, 0)
    # Rare terms are much more useful for routing than words present in half the ontology.
    return math.log2((pack_count + 1.0) / (frequency + 1.0)) + 0.25


def _normalized_text(value: str) -> str:
    return " " + SPACE_RE.sub(" ", value.casefold()).strip() + " "


def _route_score(pack, heading: str, text: str, layer: str) -> tuple[float, list[str], int]:
    heading_tokens = _tokens(heading)
    text_tokens = _tokens(text)
    heading_norm = _normalized_text(heading)
    text_norm = _normalized_text(text)
    keywords = keywords_for_pack(pack)
    rules = DOMAIN_RULES.get(pack.id, {}) if layer == "domain" else {}
    strong = set(rules.get("strong", set()))
    phrases = tuple(rules.get("phrases", ()))

    score = 0.0
    matches: list[str] = []
    high_signal = 0

    for token in sorted(keywords.intersection(heading_tokens)):
        weight = _idf(token, layer) * 2.6
        if token in LOW_SIGNAL_TERMS:
            weight *= 0.18
        if token in strong:
            weight += 3.0
            high_signal += 1
        score += weight
        matches.append("h:" + token)

    for token in sorted(keywords.intersection(text_tokens)):
        weight = _idf(token, layer) * 0.9
        if token in LOW_SIGNAL_TERMS:
            weight *= 0.15
        if token in strong:
            weight += 2.2
            high_signal += 1
        score += weight
        matches.append(token)

    # Curated discriminators can repair gaps in the generated ontology vocabulary.
    keyword_matches = keywords.intersection(heading_tokens | text_tokens)
    for token in sorted(strong.difference(keyword_matches)):
        if token in heading_tokens:
            score += 5.5
            high_signal += 1
            matches.append("h:!" + token)
        elif token in text_tokens:
            score += 3.5
            high_signal += 1
            matches.append("!" + token)

    category_words = _tokens(pack.title).difference(LOW_SIGNAL_TERMS)
    for token in category_words.intersection(heading_tokens):
        score += _idf(token, layer) * 1.75
        high_signal += 1

    for phrase in phrases:
        normalized_phrase = " " + SPACE_RE.sub(" ", phrase.casefold()).strip() + " "
        if normalized_phrase in heading_norm:
            score += 7.0
            high_signal += 2
            matches.append("h:"" + phrase + """)
        elif normalized_phrase in text_norm:
            score += 4.5
            high_signal += 2
            matches.append(""" + phrase + """)

    return score, matches[:24], high_signal


def route_text(
    heading: str,
    text: str,
    *,
    layer: str = "domain",
    top_k: int = 8,
    minimum_score: float = 1.5,
) -> list[Route]:
    scored: list[tuple[Route, int]] = []
    for pack in packs(layer):
        score, matches, high_signal = _route_score(pack, heading, text, layer)
        if score >= minimum_score:
            scored.append((Route(pack.id, pack.title, score, tuple(matches)), high_signal))

    if layer != "domain":
        scored.sort(key=lambda item: (-item[0].score, item[0].pack_id))
        return [route for route, _ in scored[:top_k]]

    concrete = [(route, signal) for route, signal in scored if route.pack_id not in ANALYTICAL_DOMAIN_IDS]
    analytical = [(route, signal) for route, signal in scored if route.pack_id in ANALYTICAL_DOMAIN_IDS]
    concrete.sort(key=lambda item: (-item[0].score, item[0].pack_id))

    # Analytical/synthetic packs only enter after the text clearly activates multiple
    # concrete domains. Their score is discounted so they enrich rather than crowd out.
    strong_concrete = [item for item in concrete if item[0].score >= 4.0 or item[1] >= 1]
    if len(strong_concrete) >= 2:
        discounted: list[tuple[Route, int]] = []
        for route, signal in analytical:
            adjusted = Route(route.pack_id, route.title, route.score * 0.45, route.matches)
            if adjusted.score >= minimum_score:
                discounted.append((adjusted, signal))
        concrete.extend(discounted)

    concrete.sort(key=lambda item: (-item[0].score, item[0].pack_id))
    return [route for route, _ in concrete[:top_k]]



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
