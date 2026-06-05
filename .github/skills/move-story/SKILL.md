---
name: move-story
description: "Skill: move an existing DNAQ story to a target epic and feature using a strict, repeatable Jira MCP sequence."
---

# Move Story Skill

Use this skill when the user asks to move an existing story to a different epic and feature.

## Jira Config

- Cloud ID: `3270ee18-7e41-4e45-bede-c73944762da0`
- Story project: `DNAQ`
- Link type for feature relation: `Parent/Child`

## Required Inputs Per Request

1. `story_key` (example: `DNAQ-823`)
2. `target_epic_key__parent` (example: `LUMI-10671`)
3. `target_feature_key__customfield_12445` (example: `LUMI-10670`)

If any input is missing, fail with a clear validation error and do not perform partial updates.

## Scope Guardrail

Only these parameters may be changed:

1. `parent` (epic parent field)
2. `customfield_12445` (Parent Feature URL field)
3. `Parent/Child` issue link for feature-child relation

Do not update summary, description, assignee, priority, story points, labels, status, comments, or any other fields.

## Jira Field and Link Mapping

1. Epic parent field:
- Workflow alias: `target_epic_key__parent`
- Jira field: `parent`

2. Parent feature field:
- Workflow alias: `target_feature_key__customfield_12445`
- Jira field: `customfield_12445`
- Value format: `https://luminus.atlassian.net/browse/<feature-key>`

3. Feature child relation:
- Link type: `Parent/Child`
- Direction: `inwardIssue = <target feature key>`, `outwardIssue = <story key>`

## Explicit Tool Sequence (Mandatory)

Use this exact sequence and do not substitute alternate orchestration paths:

1. `mcp_atlassian-mcp_getJiraIssue`
- Read current `parent`, `customfield_12445`, and `issuelinks`.
- Validate story exists and capture pre-change state.

2. `mcp_atlassian-mcp_editJiraIssue`
- Update only:
  - `parent.key = <target_epic_key__parent>`
  - `customfield_12445 = https://luminus.atlassian.net/browse/<target_feature_key__customfield_12445>`

3. `mcp_atlassian-mcp_createIssueLink`
- Ensure `Parent/Child` relation to target feature exists using:
  - `inwardIssue = <target feature key>`
  - `outwardIssue = <story key>`

4. `mcp_atlassian-mcp_getJiraIssue`
- Re-read `parent`, `customfield_12445`, and `issuelinks` to verify the move result.

## Link Replacement Behavior

Current MCP tools available in this workflow can create links but may not delete old links directly.

1. Always create or ensure the target `Parent/Child` link.
2. If an old feature `Parent/Child` link remains, report it explicitly as residual state.
3. Do not attempt unsupported delete workarounds.

## Connection and Tool Transparency (Mandatory)

Every execution response must explicitly include:

1. Connection used:
- Atlassian MCP cloudId: `3270ee18-7e41-4e45-bede-c73944762da0`

2. Exact tool calls used, in order.

3. Exact fields and link directions touched.

4. Pre vs post values for:
- `parent`
- `customfield_12445`
- feature `Parent/Child` links

## Completion Output

Return a concise report with:

1. `story_key`
2. `target_epic_key`
3. `target_feature_key`
4. `move_status` (`moved`, `partially_moved`, or `failed`)
5. `connections_used`
6. `tools_used_in_order`
7. `changed_parameters_only`
8. `residual_links` (if any)
9. `story_url`
