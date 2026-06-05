---
name: create-story
description: "Create one or many DNAQ Jira stories from context text or CSV, apply default field values, enforce story quality rules, and append created results to the created-story log CSV."
argument-hint: "Single context or bulk context/CSV"
model: "GPT-5.4 (copilot)"
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
5. Never add Jira comments.
6. Ensure feature relation is child-of (mandatory):
- `Parent/Child` link with `inwardIssue=<feature>` and `outwardIssue=<story>`.
7. For each created story:
- Fetch created issue data.
- Append to `Knowledge/product-context/stories/dnaq-story-created.csv`.
8. In bulk mode, process independently per row and continue on failures.

Return format:

1. Summary counts: requested, created, failed
2. Table/list per story: `story_ref`, `created_issue_key` (or error), `url`
3. Confirm CSV append target updated: `Knowledge/product-context/stories/dnaq-story-created.csv`
