from toril_knowledge.ontology import load_registry, packs, relationship_families
from toril_knowledge.router import (
    route_inference_from_domains,
    route_relationship_families,
    route_system_from_domains,
    route_text,
)


def test_registry_is_extensive():
    registry = load_registry()
    assert registry["named_extractor_count"] >= 350
    assert registry["operational_extractor_count"] >= registry["named_extractor_count"]
    assert len(packs("domain")) >= 20
    assert len(packs("system")) >= 20
    assert len(packs("inference")) >= 10
    assert len(relationship_families()) >= 10


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
