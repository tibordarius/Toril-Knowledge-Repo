from toril_knowledge.structure import classify_chunk, routing_limits


def test_contents_and_index_are_skipped():
    for heading in ("Contents > Table of Contents", "INDEX", "INDE > Index"):
        classification = classify_chunk(heading, "Many entries and page references.")
        assert classification.kind == "contents_index"
        limits = routing_limits(
            classification,
            domain_top_k=12,
            system_top_k=8,
            inference_top_k=6,
        )
        assert limits["skip_entity"] is True
        assert limits["domain_top_k"] == 0


def test_front_matter_is_skipped():
    classification = classify_chunk(
        "Credits",
        "ISBN 1234. Wizards of the Coast. First printing. Editor and designer credits.",
    )
    assert classification.kind == "front_matter"


def test_rules_mechanics_keep_entities_but_drop_system_inference():
    classification = classify_chunk(
        "Spell Descriptions",
        "Components: V, S. Range: close. Duration: 1 round. Saving Throw: Will negates. "
        "Spell Resistance: yes.",
    )
    assert classification.kind == "rules_mechanics"
    limits = routing_limits(
        classification,
        domain_top_k=12,
        system_top_k=8,
        inference_top_k=6,
    )
    assert limits["domain_top_k"] == 4
    assert limits["system_top_k"] == 0
    assert limits["inference_top_k"] == 0
    assert limits["skip_entity"] is False
    assert limits["skip_relationship"] is True
    assert limits["skip_epistemic"] is True


def test_stat_block_detection():
    classification = classify_chunk(
        "Ancient Wyrm",
        "AC 31, hp 350, CR 22, Initiative +4. Str 31 Dex 10 Con 25 Int 20 Wis 21 Cha 24. "
        "Fort +18 Ref +11 Will +15.",
    )
    assert classification.kind == "stat_block"


def test_lore_keeps_full_budget():
    classification = classify_chunk(
        "Calimshan",
        "The realm exports silk and spices, is ruled by an autocrat, and its merchant houses "
        "compete for influence in the cities.",
    )
    assert classification.kind == "lore"
    limits = routing_limits(
        classification,
        domain_top_k=12,
        system_top_k=8,
        inference_top_k=6,
    )
    assert limits["domain_top_k"] == 12
    assert limits["system_top_k"] == 8
    assert limits["inference_top_k"] == 6
    assert limits["skip_entity"] is False
