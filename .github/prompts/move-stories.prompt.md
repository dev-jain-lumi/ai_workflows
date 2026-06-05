---
name: move-stories
description: "Move one or many DNAQ stories from source feature/epic to target feature/epic, including mode to move all not-done stories from a feature."
argument-hint: "Mode, source, target, story keys"
agent: "move-story"
model: "GPT-5.4 (copilot)"
---

Move Jira stories using rules in [.github/skills/move-story/SKILL.md](../skills/move-story/SKILL.md).

Input mode (choose one):

- Feature mode (bulk not-done):
  - source feature: ${input:Source feature key}
  - source epic (optional): ${input:Source epic key}
  - target feature: ${input:Target feature key}
  - target epic: ${input:Target epic key}
  - scope: move all not-done stories

- Story-key mode (single or bulk):
  - story key(s): ${input:Story key or comma-separated keys}
  - target feature: ${input:Target feature key}
  - target epic: ${input:Target epic key}

Execution requirements:

1. Never add Jira comments.
2. In feature mode, fetch stories that are child of source feature and exclude Done status category.
3. For each moved story:
- set parent epic to target epic
- set parent feature field to target feature URL
- ensure Parent/Child relation is target feature -> story child
- remove old source relation/value where possible
4. Avoid duplicate links.
5. Return per-story status and clear summary counts.

Return format:

1. Summary: candidates, moved, skipped done, failed, partial cleanup required
2. Per-story rows: story key, move status, notes
