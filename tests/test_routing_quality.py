from pathlib import Path

from toril_knowledge.benchmark import evaluate_benchmarks, load_benchmarks
from toril_knowledge.ontology import load_registry
from toril_knowledge.router import route_text


FIXTURE = Path(__file__).parent / "fixtures" / "routing_benchmarks.json"


def test_extractor_ids_are_namespaced_and_unique():
    registry = load_registry()
    ids = [item["id"] for item in registry["extractors"]]
    assert len(ids) == len(set(ids))
    assert all(item_id.count(".") >= 2 for item_id in ids)
    assert all(item.get("legacy_id") for item in registry["extractors"])


def test_routing_benchmark_recall_and_noise():
    report = evaluate_benchmarks(load_benchmarks(FIXTURE))
    assert report["macro_recall_at_k"] >= 0.75
    assert report["macro_precision_at_k"] >= 0.45
    assert report["forbidden_hits"] == 0


def test_concrete_domains_beat_analytical_overlays():
    routes = route_text(
        "Regional Economy",
        "Merchants export grain and wine through a caravan network. The council taxes "
        "market sales and uses the revenue to maintain roads and bridges.",
        top_k=6,
    )
    ids = [route.pack_id for route in routes]
    assert "economic_and_commercial_domains" in ids[:3]
    if "systems_and_comparative_analytical_domains" in ids:
        assert ids.index("systems_and_comparative_analytical_domains") >= 3


def test_generic_magic_word_does_not_route_ecology():
    routes = route_text(
        "Magic in Society",
        "Wizards study spells through the Weave and merchants sell enchanted goods.",
        top_k=5,
    )
    ids = {route.pack_id for route in routes}
    assert "arcane_magical_and_occult_domains" in ids
    assert "biological_and_ecological_domains" not in ids


def test_mundane_repairs_do_not_route_maritime():
    routes = route_text(
        "Village Life",
        "Families cook meals, pay rent, repair tools and bring grain to a weekly market by cart.",
        top_k=5,
    )
    ids = {route.pack_id for route in routes}
    assert "mundane_everyday_life_domains" in ids
    assert "maritime_domains" not in ids
