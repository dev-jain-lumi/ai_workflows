---
name: move-story
description: "Move one or many DNAQ stories to a new parent feature, optionally updating epic when explicitly provided."
argument-hint: "Mode, source, target, story keys"
model: "GPT-5.4 (copilot)"
---

Move Jira stories using rules in [.github/skills/move-story/SKILL.md](../skills/move-story/SKILL.md).

Input mode (choose one):

- Feature mode (bulk not-done):
  - source feature: ${input:Source feature key}
  - source epic (optional): ${input:Source epic key}
  - target feature: ${input:Target feature key}
  - target epic (optional): ${input:Target epic key}
  - scope: move all not-done stories

- Story-key mode (single or bulk):
  - story key(s): ${input:Story key or comma-separated keys}
  - target feature: ${input:Target feature key}
  - target epic (optional): ${input:Target epic key}

Notes:
- In story-key mode, you do not need to provide the current/source feature or current/source epic.
- The workflow fetches the existing story and reads the current values before replacing them.

Execution requirements:

1. Never add Jira comments.
2. NEVER EVER create a new story in this workflow.
3. This workflow only fetches existing stories and replaces existing feature relationships with the provided values.
4. In feature mode, fetch candidate stories once, then exclude Done status category.
5. For each moved story:
- if target epic is explicitly provided and different, set parent epic to target epic
- set `parent_feature_key__customfield_12445` to `https://luminus.atlassian.net/browse/<target-feature-key>`
- remove the current Parent/Child feature relation
- add the new `Parent/Child` relation with `inwardIssue=<feature>` and `outwardIssue=<story>`
6. If a referenced story does not exist, fail it. Do not create a replacement, placeholder, probe, or test issue.
7. Avoid duplicate links.
8. Read and update only the fields needed for reassignment.
9. Return per-story status and clear summary counts.

Return format:

1. Summary: candidates, moved, skipped done, failed, partial cleanup required
2. Per-story rows: story key, move status, notes
