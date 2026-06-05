---
name: create-story
description: "Prompt: execute the DNAQ create-story workflow from context text or CSV and write created results to the created-story log CSV."
argument-hint: "Single context or bulk context/CSV"
---

Create Jira story items using the rules in [.github/skills/create-story/SKILL.md](../skills/create-story/SKILL.md).

Input (pick one):

- Single story context: ${input:Story context text}
- Bulk story context text: ${input:Multiple stories text block}
- CSV path or CSV content: ${input:CSV path or pasted CSV content}

Execution requirements:

1. Use default DNAQ values unless explicitly overridden by user/row.
2. Per story, require these inputs (no global fallback):
- `parent_epic_key__parent`
- `parent_feature_key__customfield_12445` (and link key)
- `summary`
- `us_description__customfield_10513`
If any is missing for a row, return a row-level error and continue bulk processing.
3. `acceptance_criteria__customfield_10536` is optional.
4. If story points are missing, default `story_points__customfield_10105` to `2`.
5. Keep assignee blank unless the user explicitly provides one.
6. Never add Jira comments.
7. Ensure feature relation is child-of (mandatory):
- `Parent/Child` link with `inwardIssue=<feature>` and `outwardIssue=<story>`.
8. Use the faster execution path in bulk mode:
- read the source once
- create with minimal payload first
- only edit when ADF fields are needed
- append created-log rows in one batch write
9. For each created story:
- Fetch created issue data.
- Append to `Knowledge/product-context/stories/dnaq-story-created.csv`.
10. In bulk mode, process independently per row and continue on failures.
11. Enforce the simple tool path only:
- Follow the explicit sequence from the skill without reordering or substitution.
- Use Jira MCP tools for Jira operations.
- Use direct file edit tooling (for example apply_patch) to append `Knowledge/product-context/stories/dnaq-story-created.csv`.
- Do not use terminal scripting for CSV appends.
- Do not switch to alternate workflows or helper-agent logic when the explicit sequence is available.

Return format:

1. Summary counts: requested, created, failed
2. Table/list per story: `story_ref`, `created_issue_key` (or error), `url`
3. Confirm CSV append target updated: `Knowledge/product-context/stories/dnaq-story-created.csv`
