# Extensive World-Model Pipeline

This repository treats sourcebooks as evidence for a computable world model, not as documents to summarize.

## Core design

The ontology contains 419 named specialist extractors from the working taxonomy, plus operational layers for temporal state, networks, spatial/economic/demographic/political/military/ecological/urban/adventure inference, normalization, scale, certainty, perspective, salience and simulation readiness.

The important efficiency rule is that the registry is **available globally but activated locally**. A chunk does not run every specialist. Deterministic lexical routing first selects relevant domain packs; those domain choices then activate appropriate system and inference layers.

## Nine passes

0. **Structure** — parse Markdown, capture source identity, edition, setting date, provenance and structural quality.
1. **Entities** — people, places, organizations, factions, institutions, objects, creatures, events, concepts, titles and aliases.
2. **Domains** — routed specialist extraction across economics, government, law, diplomacy, military affairs, crime, society, culture, religion, magic, geography, ecology, wilderness, urbanism, maritime affairs, technology, information, history, mundane life and adventure material.
3. **Relationships** — typed structural, political, diplomatic, economic, resource, military, criminal, social, religious, magical, spatial, temporal and information relationships.
4. **Systems** — flows, dependencies, pressures, incentives, power, capabilities, capacities, constraints, vulnerability, resilience, bottlenecks, substitution, competition, conflict, cooperation, feedback, thresholds, cascades, cross-domain coupling, shocks, lags, adaptation, path dependency, externalities, trade-offs, distributional effects, institutional friction, equilibrium/disequilibrium, volatility, leverage points, opportunities and risks.
5. **Inference** — explicitly labeled deductions such as likely industries, trade dependencies, trade networks, supply-chain weak points, fiscal pressure, institutional capacity, diplomatic leverage, logistical reach, infrastructure gaps, technology and knowledge diffusion, magical economy effects, religious influence, migration, disease spread, environmental pressure, resource depletion, maritime structure, criminal networks, succession risk, cross-domain consequences, lore gaps and adventure opportunities.
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

The registry currently includes 28 relationship families:

- structural, political, diplomatic, economic, resource, military and criminal
- social, religious, magical, spatial, temporal and information
- causal, dependency, legal, power, capability and flow
- logistical, infrastructure, ecological and technological
- epistemic, provenance, cultural, biological and cross-domain interaction

Relationship predicates are constrained by family during extraction to reduce synonym drift. The additional families are deliberately more explicit than generic `related_to` edges: they distinguish authority from influence, dependence from trade, capacity from actual action, evidence from belief, and physical flow from ownership.

## Routing

Routing happens in three stages:

1. **Concrete domain routing** uses specificity-weighted vocabulary, curated discriminators and phrase cues. Generic vocabulary is heavily downweighted, and ambiguous packs can be signal-gated.
2. **System routing** is derived mainly from the selected concrete domains. Economic material activates flows/capacity/bottlenecks; political material activates power/pressure/incentives; military material activates capability/logistics/vulnerability; urban material activates capacity/pressure/resilience. Cross-domain coupling activates when multiple concrete domains are present.
3. **Inference routing** combines lexical evidence with the established domains and system context.

Synthetic and comparative analytical packs are deliberately excluded from first-pass domain competition. Their functions belong downstream, where they cannot crowd concrete economic, political, urban, maritime, religious, magical or other source domains out of the limited routing budget.

This is cheaper and usually more accurate than asking one universal prompt to remember hundreds of concerns.

### Benchmark before ontology growth

The repository includes a paraphrased Forgotten Realms routing benchmark based on representative 1e, 3e and 4e source patterns. It tracks precision@k, recall@k and forbidden-route regressions.

Run:

```bash
toril benchmark-routing tests/fixtures/routing_benchmarks.json
```

New categories should be justified by missed source phenomena and accompanied by routing benchmark cases. More ontology entries are not automatically better if they reduce route precision.

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


## Expanded specialist domains

The 2026-10-06.2 registry adds five additional specialist packs rather than duplicating existing broad domains:

1. **Cross-domain geographic and synthetic domains** — geoeconomic, geostrategic, geocultural, geolinguistic, georeligious, geodemographic, ethnolinguistic, biogeographical, geophysical, geochemical and geotechnical.
2. **Material, environmental and mobility domains** — nature, environmental systems, resources, transport, travel, energy, land use, food systems, health, hazards, material culture, monster ecology, infrastructure systems, water systems and waste systems.
3. **Cognitive, philosophical and symbolic domains** — cognitive, philosophical, symbolic, sociolinguistic, folkloric, mythological, iconographic, rhetorical, narrative and hermeneutical.
4. **Scientific and historical specialty domains** — pathological, pharmacological, toxicological, paleontological, paleoclimatological, archaeozoological, archaeobotanical, numismatic, paleographic, codicological, sigillographic and epigraphic.
5. **Systems and comparative analytical domains** — systemic, structural, functional, comparative, network-analytic, causal-comparative, institutional-comparative, spatial-analytic, temporal-analytic, distributional, complexity and diffusion.

These remain specialist lenses. A source chunk only activates them when routing evidence supports them.

## Cross-domain coupling

The world model now has explicit operational layers for phenomena that sit between ordinary domain extractors:

- cross-domain coupling
- shock propagation
- lag and delay
- adaptation
- path dependency
- externalities
- trade-offs
- distributional effects
- institutional friction
- equilibrium and disequilibrium
- volatility
- leverage points

This matters because many useful consequences are not contained inside a single domain. A drought can become an agricultural shock, then a trade shock, then a fiscal problem, then an urban political problem. Those transitions are modeled as separate records instead of being compressed into one vague inference.

## Specialist inference expansion

The inference router now supports dedicated lenses for geoeconomics, trade networks, supply chains, fiscal systems, institutions, law, diplomacy, logistics, infrastructure, technological diffusion, knowledge diffusion, magical economy, religious influence, cultural diffusion, migration, disease, environment, resource depletion, maritime systems, security, criminal networks, succession and cross-domain consequences.

Inference remains downstream of explicit extraction. It must not overwrite source-grounded records and must carry reasoning, assumptions and uncertainty.
