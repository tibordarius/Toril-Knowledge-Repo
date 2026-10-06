# Google Drive layout

The private workspace is named **Toril Knowledge Pipeline**.

```text
Toril Knowledge Pipeline/
├── 00_Inbox_MD/
├── 01_Sources/
├── 02_Runs/
│   ├── DB/
│   ├── JSONL/
│   ├── Logs/
│   └── Manifests/
├── 03_Reviewed/
│   ├── Entities/
│   └── Conflicts/
├── 04_Exports/
│   ├── Obsidian/
│   └── Simulator/
├── 05_Ontology/
│   ├── Domain_Registry/
│   ├── Relationship_Types/
│   ├── Prompts/
│   ├── QA/
│   └── Source_Profiles/
├── 06_World_Model/
│   ├── Entities/
│   ├── Relations/
│   ├── Systems/
│   ├── Temporal/
│   ├── Inferences/
│   ├── Conflicts/
│   └── Simulation_Inputs/
└── 99_Archive/
```

## Folder contract

- **00_Inbox_MD** — newly converted Markdown awaiting structural validation.
- **01_Sources** — accepted source Markdown. Once promoted here, treat the exact file/version as immutable provenance.
- **02_Runs** — transient extraction databases, JSONL, logs, manifests and audit data.
- **03_Reviewed** — human-reviewed entities, conflict decisions and promoted material.
- **04_Exports** — downstream Obsidian packs and simulator-ready exports.
- **05_Ontology** — domain registry, typed relationships, prompt versions, QA rules and source profiles.
- **06_World_Model** — normalized knowledge after review/validation: entities, relations, systems, temporal states, explicit inferences and unresolved conflicts.
- **99_Archive** — superseded source versions, retired runs and obsolete exports.

## Promotion path

```text
00_Inbox_MD
    -> validation
01_Sources
    -> extraction
02_Runs
    -> QA / reconciliation
03_Reviewed
    -> normalization
06_World_Model
    -> downstream generation
04_Exports
```

Do not promote raw LLM output straight into the world model. Inference must remain distinguishable from explicit lore, and edition/time conflicts must remain visible until resolved or intentionally represented as separate temporal states.
