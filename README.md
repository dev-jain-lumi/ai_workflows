# Management Copilot OS

Professional managerial AI workflow system for turning messy management inputs into structured decisions, roadmaps, risks, actions, and executive-ready artifacts.

## Core Principle

Context -> Workflow -> Artifact -> Decision or Action Log -> Review

## Quick Start

1. Capture raw notes in BACKLOG.md.
2. Run a workflow from Workflows/ using COMMANDS.md prompts.
3. Save outputs under Artifacts/ using Templates/.
4. Run checks in Evals/ before sharing upward.
5. Track decisions and follow-up checkpoints.

## Repository Map

- AGENTS.md: AI behavior, routing, quality gates.
- MANAGEMENT_PRINCIPLES.md: leadership and decision principles.
- OPERATING_MODEL.md: demand-to-delivery operating loop.
- STRATEGIC_CONTEXT.md: business priorities and constraints.
- BACKLOG.md: messy inbox.
- COMMANDS.md: reusable trigger prompts.
- Workflows/: repeatable managerial flows.
- Templates/: standard output formats.
- Artifacts/: generated outputs and logs.
- Knowledge/: stable context for the assistant.
- Evals/: acceptance checks.

## Artifact Lifecycle

Draft -> Review -> Approved -> Superseded -> Archived

## Authoring Pattern

Knowledge sources live in `Knowledge/` (YAML, CSV, Markdown). Outputs in `Artifacts/` are generated from those sources. Never edit outputs directly — always update the source first, then regenerate.

| Source format | Used for |
|---|---|
| YAML / TOML | structured config, process definitions |
| CSV | planning data, roadmaps, to-do tracking |
| Markdown | narrative notes, briefs, decisions |
| PlantUML (`.puml`) | architecture and flow diagrams |

Generated outputs: HTML (shareable), CSV (exchange), Markdown (stakeholder-facing).

## Quarto Presentation Flow

Quarto source and includes for AI-assisted coding training live in:

- AI_Luminus/presentations/ai-assisted-coding/vscode_agents_concepts.qmd
- AI_Luminus/presentations/ai-assisted-coding/github-copilot-training/

Local render commands:

```bash
quarto render AI_Luminus/presentations/ai-assisted-coding/vscode_agents_concepts.qmd --to revealjs
python3 -m http.server 8000
```

Open in browser:

- http://127.0.0.1:8000/AI_Luminus/presentations/ai-assisted-coding/vscode_agents_concepts.html
