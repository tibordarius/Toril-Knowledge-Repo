# Extensive World-Model Pipeline

This repository treats sourcebooks as evidence for a computable world model, not as documents to summarize.

## Core design

The ontology contains 359 named specialist extractors from the working taxonomy, plus operational layers for temporal state, networks, spatial/economic/demographic/political/military/ecological/urban/adventure inference, normalization, scale, certainty, perspective, salience and simulation readiness.

The important efficiency rule is that the registry is **available globally but activated locally**. A chunk does not run every specialist. Deterministic lexical routing first selects relevant domain packs; those domain choices then activate appropriate system and inference layers.

## Nine passes

0. **Structure** — parse Markdown, capture source identity, edition, setting date, provenance and structural quality.
1. **Entities** — people, places, organizations, factions, institutions, objects, creatures, events, concepts, titles and aliases.
2. **Domains** — routed specialist extraction across economics, government, law, diplomacy, military affairs, crime, society, culture, religion, magic, geography, ecology, wilderness, urbanism, maritime affairs, technology, information, history, mundane life and adventure material.
3. **Relationships** — typed structural, political, diplomatic, economic, resource, military, criminal, social, religious, magical, spatial, temporal and information relationships.
4. **Systems** — flows, dependencies, pressures, incentives, power, capabilities, capacities, constraints, vulnerability, resilience, bottlenecks, substitution, competition, conflict, cooperation, feedback, thresholds, cascades, opportunities and risks.
5. **Inference** — explicitly labeled deductions such as likely industries, trade dependencies, demographic pressures, political instability, military reach, ecological consequences, urban patterns, lore gaps and adventure opportunities.
6. **Temporal model** — valid-from/valid-until states, eras, change and trends.
7. **Epistemic validation** — explicit versus inferred claims, source perspective, uncertainty, contradictions, edition conflicts and missing information.
8. **World model** — normalized entities, aliases, relationships, flows, systems, pressures and states.
9. **Derived game world** — simulator inputs, faction behavior, trade/economic/political/demographic/war simulation and adventure hooks.

## Modes

| Mode | Intended use | Domain packs | System layers | Inference |
| --- | --- | ---: | ---: | --- |
| lean | indexing and first-pass triage | 4 | off | off |
| standard | ordinary lore extraction | 8 | 4 | off |
| deep | main Toril knowledge build | 12 | 8 | 6 |
| exhaustive | selected high-value sections | all routed packs | all routed layers | all routed layers |

Do not use exhaustive mode across an entire corpus by default. It is a microscope, not a lawnmower.

## Knowledge record

All specialist passes write to a common record layer. A record carries:

- source book and chunk
- pass and extractor
- record type
- subject / predicate / object
- structured attributes
- evidence
- confidence and confidence type
- scale
- salience
- simulation readiness
- valid-from / valid-until
- perspective
- source status: explicit, strong implication or inferred

This prevents inference from being mixed with canon and prevents one edition from silently overwriting another.

## Source identity and chronology

Every book should be registered with at least:

- book_id
- title
- edition
- publication year
- setting date or era when known
- source type
- canon tier
- SHA-256
- original source path

Different editions should normally coexist as temporal states. A 1e description and a 4e description are not automatically a contradiction.

Errata should be registered with source_type=errata and treated as correction evidence, not as ordinary setting lore.

## Relationship families

The registry currently includes 13 relationship families:

- structural
- political
- diplomatic
- economic
- resource
- military
- criminal
- social
- religious
- magical
- spatial
- temporal
- information

Relationship predicates are constrained by family during extraction to reduce synonym drift.

## Routing

Routing happens in three stages:

1. **Domain routing** uses heading and body vocabulary.
2. **System routing** is derived mainly from the selected domains. Economic material activates flows/capacity/bottlenecks; political material activates power/pressure/incentives; military material activates capability/logistics/vulnerability; urban material activates capacity/pressure/resilience.
3. **Inference routing** combines lexical evidence with domain-derived lenses.

This is cheaper and usually more accurate than asking one universal prompt to remember hundreds of concerns.

## Recommended Forgotten Realms workflow

For a new sourcebook:

```bash
toril ingest book.md \
  --book-id frcs-3e \
  --title "Forgotten Realms Campaign Setting" \
  --edition 3e \
  --publication-year 2001 \
  --setting-date "1372 DR"

toril route --book-id frcs-3e --limit 20

toril extract-world --book-id frcs-3e --mode deep
```

Inspect routing before paying for a complete deep run. If an entire book routes badly, fix the router or source profile first rather than compensating with a larger model.

## Promotion policy

Raw LLM output should move through:

```text
02_Runs
  -> QA
  -> 03_Reviewed
  -> 06_World_Model
  -> 04_Exports / Simulator
```

Only reviewed or sufficiently validated records should be treated as canonical world-model inputs.
