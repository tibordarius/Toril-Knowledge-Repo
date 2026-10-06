# Google Drive layout

The private workspace is named **Toril Knowledge Pipeline**.

- 00_Inbox_MD — newly converted Markdown awaiting validation
- 01_Sources — accepted source Markdown, treated as immutable
- 02_Runs — extraction databases, JSONL, logs and run manifests
- 03_Reviewed — human-reviewed dossiers and resolved conflicts
- 04_Exports — Obsidian packs, simulator inputs and downstream exports
- 99_Archive — superseded runs and retired source versions

Recommended rule: moving a source from Inbox to Sources means it passed structural validation and becomes the provenance anchor for all later runs.
