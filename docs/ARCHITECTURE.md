# Architecture

The pipeline separates deterministic parsing, source-grounded extraction, system modeling and explicit inference.

## Processing architecture

1. **Structure** — parse Markdown headings, page markers and source identity without an LLM.
2. **Entities** — extract atomic people, places, organizations, objects, creatures, events, concepts and aliases.
3. **Domains** — route each chunk to relevant specialist packs from the 419 named extractors.
4. **Relationships** — extract constrained predicates from 28 relationship families.
5. **Systems** — model flows, dependencies, capacity, constraints, power, risk, coupling, shocks, lags, adaptation and other explicit mechanisms.
6. **Inference** — apply routed specialist lenses for economics, politics, logistics, infrastructure, diffusion, disease, environment, succession and cross-domain consequences.
7. **Temporal + epistemic** — preserve eras, validity windows, perspective, uncertainty, provenance and conflicts.
8. **World model** — normalize entities, aliases, relations, systems, states and networks.
9. **Derived outputs** — build dossiers, Obsidian exports, simulator inputs and adventure derivation.

## Routing rule

The registry is global but activation is local. A chunk does not run 471 operational extractors.

Routing now uses four controls:

1. **Specificity weighting** — vocabulary shared by many ontology packs receives less weight than rare, domain-specific terms.
2. **Signal cues** — discriminating terms and phrases such as `autocracy`, `imports`, `sewer system`, `the Weave`, `inconsistent justice`, or `by cart` can move a domain decisively.
3. **Signal gates** — ambiguous domains cannot enter the top routes merely by accumulating generic overlaps such as `food`, `magic`, `population`, `trade`, or `repair`.
4. **Concrete-before-analytical routing** — synthetic/comparative packs do not consume Pass-2 domain slots. Cross-domain coupling, comparative analysis, systems reasoning and consequence inference activate downstream after concrete domains have been established.

The concrete domain choices then activate system layers and specialist inference layers. Multiple active domains can activate cross-domain coupling and consequence checks.

This avoids two bad extremes: a tiny universal prompt that misses domain detail, and an exhaustive prompt that runs hundreds of irrelevant lenses over every paragraph.

### Routing benchmark

Routing quality is tested independently from LLM extraction using a paraphrased Forgotten Realms benchmark corpus. The benchmark reports precision@k, recall@k and explicit forbidden-pack intrusions.

Any substantial ontology expansion should add or update benchmark cases before being accepted. Category count is not treated as a quality metric by itself.

## Record contract

Every knowledge record preserves:

- source book and chunk
- pass, layer and extractor
- subject / predicate / object
- structured attributes
- evidence
- confidence type
- scale
- salience
- simulation readiness
- valid-from / valid-until
- perspective
- source status

Source-grounded records and inferred records are never silently merged.

## Why SQLite first

SQLite gives one inspectable artifact with transactions and FTS5. It is enough for sourcebook-scale validation. A graph database or vector database should be added only after a real access pattern justifies it.

## Public/private boundary

The GitHub repository is public. Sourcebook Markdown and generated corpus data stay in the private Drive workspace. Do not commit source books, raw chunks, databases or generated dossiers.


## Structural routing gate

Domain relevance is not the only routing decision. The parser now classifies chunks before
expensive passes:

- `contents_index`: skip model extraction; preserve the source text only.
- `front_matter`: skip model extraction when credits/publication metadata dominate.
- `rules_mechanics`: retain entity extraction and at most four domain packs; no
  relationship/system/inference/epistemic passes.
- `stat_block`: same constrained policy as mechanics, except embedded stat blocks inside
  explicit lore containers such as Geography, Deities, Organizations, Life in Faerûn and
  Running the Realms do not suppress the surrounding lore.
- `errata`: use correction mode, a small domain budget and no systems/inference pass.
- `lore`: use the normal mode budget.

OCR-damaged index fragments are detected with a conservative numeric-density test rather than
book-specific line ranges. Classifications are stored in `chunk_classifications` for auditability.
