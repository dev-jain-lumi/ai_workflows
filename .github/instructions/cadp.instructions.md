---
applyTo: "AI_Luminus/how-to-CADP/**"
description: "Use when working in the how-to-CADP folder: building CADPs, generating dbt models, writing Soda contracts, updating CADP process docs, or answering questions about the NEO data product workflow."
---

# CADP (Consumer-Aligned Data Product) — Agent Instructions

## What is a CADP?

A **CADP** is a consumer-facing, governed data product built from upstream SADPs (Source-Aligned Data Products) and exposed via controlled metadata, access, and publication flows on the NEO platform.

Key distinction: **SADP = source-aligned input; CADP = consumer-aligned output.**

## Authoritative References (read before generating artifacts)

- [cadp-process.yaml](../AI_Luminus/how-to-CADP/docs/cadp-process.yaml) — canonical 15-step process (steps 0–14), tool responsibilities per step
- [Process-Tool Flow.csv](../AI_Luminus/how-to-CADP/docs/Process-Tool%20Flow%20v2.csv) — matrix view of steps × tools
- [cadp-checklist.yaml](../AI_Luminus/how-to-CADP/checklists/cadp-checklist.yaml) — gating checklist (before-setup, before-build, during-build, before-publish, publish-and-operate)
- [cadp-tooling-architecture.puml](../AI_Luminus/how-to-CADP/docs/cadp-tooling-architecture.puml) — tooling architecture diagram (PlantUML)
- [fact_example.sql](../AI_Luminus/how-to-CADP/examples/dbt/fact_example.sql) — canonical dbt fact model pattern

## Process Summary (Steps 0–14)

| Step | Name | Key Gate |
|------|------|----------|
| 0 | Onboard with NEO Platform | Active LIAM roles, Snowflake login, GitLab SSO |
| 1 | Request / Join a Purpose | Approved PBAC roles, Purpose-specific schemas accessible |
| 2 | Onboard with GitLab | Repo conventions understood, MR/branching aligned |
| 3 | Set Up IDE (Ona / VS Code) | SQL + dbt commands work locally |
| 4 | Discover Upstream Data Products | Upstream grain, cadence, ownership confirmed in Portal |
| 5 | Request Upstream Access | Data agreements approved, read permissions verified |
| 6 | Inspect Upstream Content | Source assessment: grain, keys, quality, join feasibility |
| 7 | Define CADP Design | Blueprint: grain, facts, dims, keys, naming, tests, publish intent |
| 8 | Build Transformation Logic | Working DEV models with passing dbt tests in P_{PURPOSE} |
| 9 | Validate CADP Output | All dbt tests + Soda contracts pass; reconciliation confirmed |
| 10 | Register in DPM | Public schema `purpose__data_id` provisioned |
| 11 | Deploy Pipeline | Merged to main; CI/CD validates and deploys |
| 12 | Run Scheduled Refresh | Event-triggered on upstream SADP; monitoring active |
| 13 | Publish (WAP) | Zero-copy clone to public schema only after Soda contracts pass |
| 14 | Register and Expose | Discoverable in Portal with full metadata and PBAC access path |

## Toolchain Roles

| Tool | Role |
|------|------|
| Data Product Portal | Discovery, access requests, consumer exposure |
| Data Product Manager (DPM) | Product registration, public schema provisioning, PBAC |
| Snowflake | Storage: DEV in `P_{PURPOSE}`, published in `purpose__data_id` |
| Ona / VS Code | IDE: SQL exploration, dbt development |
| GitLab | Source control, MR reviews, branching conventions |
| Vulcan | Runtime config, publish behavior, WAP configuration |
| GitLab CI/CD | Pipeline deployment and automation |
| Conveyor / Airflow | Scheduling, triggering, monitoring, backfills |
| dbt | Transformation layers: `stg_`, `int_`, `fct_`, `dim_` |
| Soda | Data quality contracts; gate for WAP publish step |

## Critical Conventions

- **dbt naming**: `stg_` (staging) → `int_` (intermediate) → `fct_` (facts) → `dim_` (dimensions)
- **Business keys**: reuse from SADPs — never create new keys in CADPs
- **Schema pattern**: dev writes to `P_{PURPOSE}` (private); published output in `purpose__data_id` (public)
- **WAP pattern**: Write → Audit (Soda) → Publish (atomic zero-copy clone). Failed Soda contracts **block** publication.
- **Grain first**: always define "one row represents X" before building; grain duplicates must be explicitly explained
- **Access via PBAC**: never bypass data agreements; access flows through DPM-governed roles

## Documentation Conventions

- All narrative notes: Markdown
- Process/step data: YAML (as in `cadp-process.yaml`) or CSV
- Diagrams: PlantUML (`.puml`); follow the green palette in [AGENTS.md](../AGENTS.md#plantuml-standards)
- Checklists: YAML
- Examples: SQL in `examples/dbt/`

## When Adding or Updating Docs

### Update flow — always follow this order

```
cadp-process.yaml          ← edit HERE first (canonical source)
        │
        ├─▶ cadp-process.toml          update [meta] + any changed [[steps]] blocks
        │         │
        │         └─▶ cadp-process-guide.html   paste the updated TOML into the
        │                                        <script type="text/toml"> block
        │
        ├─▶ Process-Tool Flow enhanced.csv       re-derive only when step content changes
        │   (+ sibling .meta.yaml stays unchanged unless columns change)
        │
        └─▶ cadp-tooling-architecture.puml / .mmd   update only when tool relationships change
```

Rules:
- Never edit the TOML or HTML first — always start from the YAML.
- The CSV is a matrix view; it only needs updating when step text or tool columns change.
- The `.puml` / `.mmd` diagrams are architecture-level views; they are not step-by-step docs and rarely change.
- `cadp-checklist.yaml` is a gating checklist and is maintained independently.

### Other doc conventions

- Add new examples under `examples/<tool>/`
- Do not duplicate step content across files; link instead
