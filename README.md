# Toril Knowledge Repo

Schema-first extraction pipeline for turning Markdown sourcebooks into an auditable Toril knowledge layer.

The operating rule is: **extract once, preserve provenance, synthesize later**.

## Data boundary

This repository is public. It contains code, schemas, prompts, tests, and documentation only.

Book Markdown, extracted text, SQLite databases, generated dossiers, and other corpus material stay in the private Google Drive workspace. They are deliberately excluded from Git.

## Pipeline

```text
Markdown source
  -> deterministic structure + provenance
  -> semantic chunks
  -> entity pass
  -> routed specialist domain packs
  -> typed relationship pass
  -> system pass: flows / dependencies / power / capacity / constraints / risk
  -> explicit inference pass
  -> temporal + epistemic validation
  -> normalized world model
  -> dossiers / Obsidian / simulator inputs / adventure derivation
```

The extensive ontology currently contains **419 named specialist extractors**, operational
meta/inference layers, and 28 typed relationship families. The full registry is available
to every book, but only relevant packs are activated per chunk.

The first implementation is intentionally conservative: no vector database, no graph database, and no large-context summarization loop. SQLite is enough to validate the extraction contract and provenance model before adding more infrastructure.

## Quick start

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate

pip install -e ".[dev]"

set OPENAI_API_KEY=...
set TORIL_LLM_MODEL=...
```

Then:

```bash
toril --db data/toril.db ingest "path/to/book.md" --book-id frcs-3e
toril --db data/toril.db search "Waterdeep trade harbor"
toril --db data/toril.db route --book-id frcs-3e --limit 20
toril --db data/toril.db extract-world --book-id frcs-3e --mode deep
toril --db data/toril.db dossier "Waterdeep" --out exports/waterdeep.md
```

See `docs/ARCHITECTURE.md` and `docs/DRIVE_LAYOUT.md`.

## Current scope

The pipeline preserves book, chunk, heading, and page provenance for extracted facts. Economic details are explicitly requested because generic lore summarization tends to discard production, trade, prices, routes, seasonality, labor, taxation, guilds, infrastructure, shipping, credit, currencies, and dependencies.

Next additions should focus on conflict review, cross-book entity resolution, hybrid lexical/vector retrieval, run manifests, cost accounting, and calibration of the new cross-domain coupling and specialist inference layers against real sourcebooks.


## Extensive extraction

See [docs/EXTENSIVE_PIPELINE.md](docs/EXTENSIVE_PIPELINE.md) for the nine-pass world-model
architecture and [docs/SOURCE_PROFILES.md](docs/SOURCE_PROFILES.md) for the current
Forgotten Realms sourcebook handling rules.

Use `deep` as the normal high-quality corpus mode. Use `exhaustive` only on selected
high-value sections; running every possible lens over every mechanics table is expensive
and usually worse than routing.


## Routing quality

Domain routing is benchmarked separately from extraction. The router uses specificity-weighted
terms, curated high-signal phrases, and signal gates for ambiguous domains. Synthetic/comparative
packs do not compete with concrete source domains; cross-domain analysis is activated later by
system and inference routing.

Run the benchmark with:

```bash
toril benchmark-routing tests/fixtures/routing_benchmarks.json
```

The public benchmark corpus is paraphrased from representative Forgotten Realms source patterns.
Do not add large numbers of ontology categories without re-running this benchmark and adding
regression cases for the new routing behavior.
