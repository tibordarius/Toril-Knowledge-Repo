from toril_knowledge.source_profiles import source_instructions, source_profile_limits


def test_novel_profile_reduces_system_and_inference_budgets():
    limits = source_profile_limits(
        "novel",
        domain_top_k=12,
        system_top_k=8,
        inference_top_k=6,
    )
    assert limits == {
        "domain_top_k": 8,
        "system_top_k": 2,
        "inference_top_k": 2,
    }


def test_sourcebook_profile_keeps_requested_budgets():
    limits = source_profile_limits(
        "campaign_setting",
        domain_top_k=12,
        system_top_k=8,
        inference_top_k=6,
    )
    assert limits == {
        "domain_top_k": 12,
        "system_top_k": 8,
        "inference_top_k": 6,
    }


def test_narrative_instructions_preserve_perspective():
    instructions = source_instructions({"source_type": "novel"}, "lore")
    assert "dialogue" in instructions.casefold()
    assert "perspective" in instructions.casefold()
    assert "objective world fact" in instructions.casefold()


def test_embedded_errata_overrides_other_source_profiles():
    instructions = source_instructions({"source_type": "novel"}, "errata")
    assert "ERRATA MODE" in instructions
