# Sourcebook Profiles

These profiles describe how the current test corpus should be handled. They do not reproduce sourcebook content.

## Forgotten Realms Campaign Setting Box Set (1e)

- Heavy OCR noise and irregular headings.
- Broad world-description material mixed with maps, lists and reference entries.
- Strong historical value for older temporal states.
- Use aggressive structural QA and conservative entity normalization.
- Do not compare statements directly with later editions without time/edition context.

## Forgotten Realms Campaign Setting (3e)

- Very dense corpus with many Markdown headings.
- Particularly valuable for regional stat blocks, settlement/region descriptions, government, religion, imports/exports, labor, agriculture, industry, travel, trade, coinage, magic in society, engineering, ships and geography.
- Route regional entries broadly: economic + governmental + demographic + religious + geographic + urban + military/illicit when supported.
- Excellent baseline for simulator-oriented extraction.

## Forgotten Realms Campaign Setting Errata

- Register as source_type=errata.
- Treat as correction overlays against the 3e Campaign Setting.
- Do not turn changed game statistics or corrected wording into independent world-state claims.
- Preserve target page/section and old/new wording where available.

## Forgotten Realms Campaign Guide (4e)

- Strong region/gazetteer coverage, post-Spellplague temporal state, cosmology, pantheon and threats.
- Expect geographic, political, magical, divine, factional, historical and adventure routing.
- Lore-check text should be treated as source assertions with an attached presentation context, not as a different canon tier.

## Forgotten Realms Player's Guide (4e)

- Mixes player mechanics with regional/background material.
- Mechanics-heavy sections should not trigger expensive world-system inference.
- Background and regional sections can contain dense urban, cultural, demographic, economic and geographic lore.

## Neverwinter Campaign Setting (4e)

- Strong faction structure with explicit history/goals/relationships/encounter material.
- Gazetteer is dense in neighborhoods, sites, hazards, factions, ruins, infrastructure and adventure hooks.
- Faction chapters should strongly route organizational, political, social, military, illicit, religious/magical and adventure packs as appropriate.
- Encounter/stat-block sections should be downweighted for world-system extraction unless the surrounding prose establishes persistent setting facts.

## General corpus rules

- Preserve OCR text as source evidence; normalization belongs in a separate layer.
- Keep mechanics facts distinguishable from world facts.
- Track edition and setting date.
- Keep rumors, beliefs and narrator claims as perspective-bearing records.
- Never erase a conflicting older claim merely because a newer edition exists.
