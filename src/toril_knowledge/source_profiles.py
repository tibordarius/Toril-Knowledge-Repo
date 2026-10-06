from __future__ import annotations

from typing import Any


NARRATIVE_SOURCE_TYPES = {"novel"}

NARRATIVE_SOURCE_INSTRUCTIONS = """
NARRATIVE SOURCE MODE
- Distinguish narrator-described observations from dialogue, thoughts, hearsay, rumor, metaphor and speculation.
- Dialogue, belief, memory and reported claims must remain perspective-bearing records with the speaker/viewpoint identified when available.
- Do not promote a character's statement or thought into an objective world fact unless the narration independently establishes it.
- Concrete actions, locations, objects and directly narrated observations may be explicit, but keep them bounded to the depicted scene/time when appropriate.
- Literary metaphor, simile, hyperbole and figurative language are not literal world facts.
- Do not infer population-scale, economic, political or ecological system properties from a single anecdote or scene.
- Preserve chronology, viewpoint and uncertainty. A novel is evidence about depicted events and perspectives, not a setting encyclopedia.
"""

MAGAZINE_SOURCE_INSTRUCTIONS = """
MAGAZINE SOURCE MODE
- Preserve article authorship/presentation context when available.
- Distinguish setting statements from rules advice, adventure hooks, letters, fiction and editorial material.
- Do not silently treat speculative or optional article content as universal world state.
"""


def source_profile_limits(
    source_type: str | None,
    *,
    domain_top_k: int,
    system_top_k: int,
    inference_top_k: int,
) -> dict[str, int]:
    source_type = (source_type or "sourcebook").casefold()
    if source_type == "novel":
        return {
            "domain_top_k": min(domain_top_k, 8),
            "system_top_k": min(system_top_k, 2),
            "inference_top_k": min(inference_top_k, 2),
        }
    if source_type == "magazine":
        return {
            "domain_top_k": min(domain_top_k, 8),
            "system_top_k": min(system_top_k, 4),
            "inference_top_k": min(inference_top_k, 2),
        }
    return {
        "domain_top_k": domain_top_k,
        "system_top_k": system_top_k,
        "inference_top_k": inference_top_k,
    }


def source_instructions(meta: dict[str, Any], classification_kind: str | None = None) -> str:
    source_type = (meta.get("source_type") or "sourcebook").casefold()

    if source_type == "errata" or classification_kind == "errata":
        return (
            "\n\nERRATA MODE\n"
            "Treat this text as a correction overlay. Use record_type=correction where appropriate. "
            "Capture the target page/section, corrected field or wording, previous value when stated, "
            "and replacement value in attributes. Do not promote corrected mechanics into unrelated lore."
        )

    if source_type == "novel":
        return "\n\n" + NARRATIVE_SOURCE_INSTRUCTIONS.strip()

    if source_type == "magazine":
        return "\n\n" + MAGAZINE_SOURCE_INSTRUCTIONS.strip()

    return ""
