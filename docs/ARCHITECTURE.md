# Architecture

The pipeline separates deterministic work from probabilistic work.

1. Parse Markdown headings and page markers without an LLM.
2. Chunk on semantic boundaries.
3. Extract atomic entities, claims, relationships and events.
4. Persist everything with source book, chunk, heading and page provenance.
5. Retrieve with SQLite FTS before adding embeddings.
6. Build dossiers from the fact layer instead of rereading whole books.
7. Review conflicts before promoting claims to canonical knowledge.

## Why SQLite first

SQLite gives one inspectable artifact with transactions and FTS5. It is enough for sourcebook-scale validation. A graph database or vector database should be added only after a real access pattern justifies it.

## Public/private boundary

The GitHub repository is public. Sourcebook Markdown and generated corpus data stay in the private Drive workspace. Do not commit source books, raw chunks, databases, or generated dossiers.
