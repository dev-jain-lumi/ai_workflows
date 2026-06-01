# Strategy And Roadmap Knowledge

Purpose:
- Keep roadmap source data in an AI-friendly location tied to product strategy.
- Preserve a CSV-first workflow so the file can be pasted into Excel anytime.

Files:
- `platform-owner-roadmap.source.csv`: working source of truth for roadmap editing.
- `platform-owner-roadmap.notes.md`: optional decisions, assumptions, and mapping notes.

Publishing flow:
1. Edit `platform-owner-roadmap.source.csv` in this folder.
2. When ready to share, copy the latest version to:
	- `Artifacts/platform-management/roadmaps/platform-owner-roadmap.output.csv`
3. Keep output CSV clean for business sharing; keep analysis notes in this Knowledge folder.

Why this split:
- Knowledge folder = stable context for AI and iterative authoring.
- Artifacts folder = outward-facing deliverables.
