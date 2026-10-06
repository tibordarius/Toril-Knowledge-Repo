# Toril Knowledge Repo

Schema-first extraction pipeline for turning Markdown sourcebooks into an auditable Toril knowledge layer.

The operating rule is: **extract once, preserve provenance, synthesize later**.

## Data boundary

This repository is public. It contains code, schemas, prompts, tests, and documentation only.

Book Markdown, extracted text, SQLite databases, generated dossiers, and other corpus material stay in the private Google Drive workspace. They are deliberately excluded from Git.

## Pipeline

```text
Markdown book
  -> deterministic structure parsing
  -> semantic chunks
  -> LLM extraction
       - entities
       - claims
       - relationships
       - events
  -> SQLite fact layer + FTS
  -> dossiers / review / exports
```

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
toril --db data/toril.db extract --book-id frcs-3e
toril --db data/toril.db dossier "Waterdeep" --out exports/waterdeep.md
```

See `docs/ARCHITECTURE.md` and `docs/DRIVE_LAYOUT.md`.

## Current scope

The pipeline preserves book, chunk, heading, and page provenance for extracted facts. Economic details are explicitly requested because generic lore summarization tends to discard production, trade, prices, routes, seasonality, labor, taxation, guilds, infrastructure, shipping, credit, currencies, and dependencies.

Next additions should be conflict review, cross-book entity resolution, hybrid lexical/vector retrieval, run manifests and cost accounting, and specialist extractors for economics, politics, history, geography, and adventure material.
