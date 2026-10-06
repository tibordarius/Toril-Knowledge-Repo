from toril_knowledge.ontology import load_registry, packs, relationship_families
from toril_knowledge.router import (
    route_inference_from_domains,
    route_relationship_families,
    route_system_from_domains,
    route_text,
)


def test_registry_is_extensive():
    registry = load_registry()
    assert registry["named_extractor_count"] >= 419
    assert registry["operational_extractor_count"] >= registry["named_extractor_count"]
    assert len(packs("domain")) >= 29
    assert len(packs("system")) >= 35
    assert len(packs("inference")) >= 30
    assert len(relationship_families()) >= 28


def test_regional_stat_block_routes_broadly():
    routes = route_text(
        "Calimshan",
        "Population 5,339,520. Government autocracy. Imports food and slaves. "
        "Exports armor, books, gems, jewelry, ships, silk, spices, weapons and wine. "
        "Most people rely upon mercantilism for their livelihood.",
        top_k=10,
    )
    ids = {route.pack_id for route in routes}
    assert "economic_and_commercial_domains" in ids
    assert "governmental_and_political_domains" in ids
    assert "sociological_and_anthropological_domains" in ids


def test_city_routes_to_urban_domain():
    routes = route_text(
        "Waterdeep",
        "The city has wards, sewers, wealthy merchants, caravans, docks, taverns, "
        "markets, neighborhoods, guilds, walls and roads.",
        top_k=10,
    )
    assert any(route.pack_id == "urban_and_settlement_domains" for route in routes)


def test_relationship_router_activates_trade_and_magic():
    families = route_relationship_families(
        "Port city",
        "Merchants trade by ship while a wizard guild maintains portals.",
        ["economic_and_commercial_domains", "arcane_magical_and_occult_domains"],
    )
    assert "economic" in families
    assert "magical" in families
    assert "structural" in families


def test_system_and_inference_are_derived_from_domains():
    domains = [
        "economic_and_commercial_domains",
        "urban_and_settlement_domains",
        "governmental_and_political_domains",
    ]
    systems = route_system_from_domains(domains, top_k=12)
    assert "flow_layers" in systems
    assert "capacity_layer" in systems
    assert "power_layer" in systems

    inferences = route_inference_from_domains(domains, top_k=12)
    assert "economic_inference_layer" in inferences
    assert "urban_inference_layer" in inferences
    assert "political_inference_layer" in inferences


def test_expanded_specialist_domains_are_registered():
    registry = load_registry()
    names = {item["name"] for item in registry["extractors"]}
    for expected in {
        "geoeconomic", "geostrategic", "geocultural", "geolinguistic",
        "georeligious", "geodemographic", "nature", "environmental",
        "energy", "land-use", "food-system", "health", "material-culture",
        "cognitive", "philosophical", "symbolic", "pathological",
        "pharmacological", "toxicological", "systemic", "comparative",
        "complexity", "diffusion",
    }:
        assert expected in names


def test_relationship_model_has_mechanism_specific_families():
    families = relationship_families()
    for family in {
        "causal", "dependency", "legal", "power", "capability", "flow",
        "logistical", "infrastructure", "ecological", "technological",
        "epistemic", "provenance", "cultural", "biological", "interaction",
    }:
        assert family in families

    assert "critically_depends_on" in families["dependency"]
    assert "has_jurisdiction_over" in families["legal"]
    assert "flows_to" in families["flow"]
    assert "sourced_from" in families["provenance"]
    assert "couples_with" in families["interaction"]


def test_relationship_router_activates_new_mechanism_families():
    families = route_relationship_families(
        "Contaminated trade corridor",
        "A licensed port depends on an aqueduct and warehouse route. "
        "Pollution harms habitat while engineers maintain the bridge. "
        "Records contradict an older source about the legal jurisdiction.",
        [
            "economic_and_commercial_domains",
            "legal_and_juridical_domains",
            "biological_and_ecological_domains",
            "technological_and_scientific_domains",
        ],
    )
    for expected in {
        "dependency", "legal", "flow", "logistical", "infrastructure",
        "ecological", "technological", "epistemic", "provenance",
    }:
        assert expected in families


def test_cross_domain_system_layers_activate_for_multi_domain_chunks():
    domains = [
        "economic_and_commercial_domains",
        "governmental_and_political_domains",
        "material_environment_and_mobility_domains",
    ]
    systems = route_system_from_domains(domains, top_k=20)
    assert "cross_domain_coupling_layer" in systems
    assert "shock_propagation_layer" in systems
    assert "externality_layer" in systems
    assert "distributional_effect_layer" in systems


def test_specialist_inference_layers_are_routed():
    domains = [
        "economic_and_commercial_domains",
        "maritime_domains",
        "cross_domain_geographic_and_synthetic_domains",
    ]
    inferences = route_inference_from_domains(domains, top_k=24)
    assert "geoeconomic_inference_layer" in inferences
    assert "trade_network_inference_layer" in inferences
    assert "maritime_inference_layer" in inferences
    assert "logistics_inference_layer" in inferences
    assert "cross_domain_consequence_inference_layer" in inferences
