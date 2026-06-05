---
name: create-story
description: "Skill: internal create-story rules and field mappings for the DNAQ Jira story creation workflow."
---

# Create Story Skill

Use this skill when the user asks to create one or more stories from free text or CSV input.

## Jira Config

- Cloud ID: `3270ee18-7e41-4e45-bede-c73944762da0`
- Project: `DNAQ`
- Default issue type: `Story`
- Master defaults source: `Knowledge/product-context/stories/dnaq-story-master.csv`
- Created-story log: `Knowledge/product-context/stories/dnaq-story-created.csv`

## Field Naming Convention

- Columns in CSV/user input use workflow aliases such as `parent_feature_key__customfield_12445` for readability.
- Jira API calls must use the real Jira system field name, for example `customfield_12445`.
- `parent_epic_key__parent`: human meaning = epic parent key; system name = `parent`
- `parent_feature_key__customfield_12445`: human meaning = Parent Feature URL field; system name = `customfield_12445`
- `parent_feature_link_key__issue_link_is_child_of`: human meaning = create Parent/Child link with feature as parent; system name = not a field, this is an issue-link instruction
- `us_description__customfield_10513`: human meaning = User Story Description; system name = `customfield_10513`
- `acceptance_criteria__customfield_10536`: human meaning = Acceptance Criteria; system name = `customfield_10536`

## Required Behavior

1. Never add Jira comments while creating or linking stories.
2. For feature relation, story must be child of feature:
- Use `Parent/Child` link type.
- Use direction: `inwardIssue = <feature key>`, `outwardIssue = <story key>`.
3. Do not create duplicate links:
- Read current `issuelinks` first.
- Create link only if the exact child-of relation is missing.
4. Do not assign the story to anyone by default:
- Leave `assignee` and `assignee__account_id` blank unless the user explicitly provides an assignee.
5. After each create, fetch created issue data and append one row to `dnaq-story-created.csv`.
6. Support both single-story and bulk-story creation from:
- Plain text context
- CSV content/path provided by user

## Column Contract

The master CSV contains story-specific columns only:

- `story_ref`
- `summary`
- `parent_epic_key__parent` - human meaning: epic parent key; system name: `parent`
- `parent_feature_key__customfield_12445` - human meaning: Parent Feature URL field; system name: `customfield_12445`
- `parent_feature_link_key__issue_link_is_child_of` - human meaning: create Parent/Child link with feature as parent; system name: not a field, this is an issue-link instruction
- `us_description__customfield_10513` - human meaning: User Story Description; system name: `customfield_10513`
- `acceptance_criteria__customfield_10536` - human meaning: Acceptance Criteria; system name: `customfield_10536`

All other Jira fields are taken from defaults in this skill unless explicitly overridden by user input.

Per-story required columns (no global default):

- `parent_epic_key__parent` - human meaning: epic parent key; system name: `parent`
- `parent_feature_key__customfield_12445` - human meaning: Parent Feature URL field; system name: `customfield_12445`
- `parent_feature_link_key__issue_link_is_child_of` - human meaning: create Parent/Child link with feature as parent; system name: not a field, this is an issue-link instruction
- `summary`
- `us_description__customfield_10513` - human meaning: User Story Description; system name: `customfield_10513`

`acceptance_criteria__customfield_10536` is optional. Human meaning: Acceptance Criteria. System name: `customfield_10536`.

## Default Field Values (DNAQ stories)

Unless explicitly overridden by user or row input, prepopulate with:

- `project_key`: `DNAQ`
- `issue_type`: `Story`
- `priority`: `Medium`
- `reporter`: `Devashish Jain`
- `reporter__account_id`: `712020:f645d120-98c0-4029-84c3-01f4405dfce9`
- `business_owner__customfield_10512`: `Devashish Jain` - human meaning: Business Owner; system name: `customfield_10512`
- `business_owner__customfield_10512__account_id`: `712020:f645d120-98c0-4029-84c3-01f4405dfce9`
- `lead_solution_designer__customfield_10515`: `Jan Floren` - human meaning: Lead Solution Designer; system name: `customfield_10515`
- `lead_solution_designer__customfield_10515__account_id`: `5e8ed38071d2150b82f49de2`
- `dedicated_team__customfield_10803`: `DNA DataViz Platform` - human meaning: Dedicated Team; system name: `customfield_10803`
- `dedicated_team__customfield_10803__option_id`: `11911`
- `story_points__customfield_10105`: `2` - human meaning: Story Points; system name: `customfield_10105`

## Quality Rules For Generated Content

### `summary`

1. Use action-oriented phrasing.
2. Keep concise and specific.
3. Do not include implementation noise.

### `us_description__customfield_10513`

Human meaning: User Story Description. System name: `customfield_10513`.

1. Structure as: `Original context: ... As a <role>, I want <goal>, so that <value>.`
2. Tie back to user-provided context.
3. Ensure role, goal, and value are explicit.

### `acceptance_criteria__customfield_10536`

Human meaning: Acceptance Criteria. System name: `customfield_10536`.

1. Outcome-based and testable.
2. One clear completion statement minimum.
3. Avoid vague words like "improve" without measurable intent.

## Jira API Mapping Rules

Before create, validate per story that epic, feature, feature-link direction key, summary, and US description are present. If any is missing, fail that row with a clear error and continue bulk processing.

Phase 1: create the issue with only the minimum creation payload.

1. Mandatory in phase 1:
- `project_key = DNAQ`
- `summary`
2. No other fields are required in phase 1. All remaining fields can be populated after the issue exists.

Phase 2: populate the remaining fields after create.

3. If `customfield_10513` requires ADF, update it via edit call in ADF format. Human meaning: User Story Description.
4. If `customfield_10536` is provided and requires ADF, update it via edit call in ADF format. Human meaning: Acceptance Criteria.
5. For `customfield_12445`, set value as below. Human meaning: Parent Feature URL field.
- `https://luminus.atlassian.net/browse/<feature-key>`
6. Enforce `Parent/Child` issue link direction as mandatory (feature -> story child relation). This link instruction comes from workflow alias `parent_feature_link_key__issue_link_is_child_of`, not from a Jira field.

## Execution Optimization

1. Read the source CSV or text input once per request.
2. Create issues with the minimal create payload first.
3. Only call issue edit when ADF fields are actually needed.
4. For bulk runs, accumulate created-log rows in memory and write them in one append batch.
5. Avoid extra verification reads when create/edit responses already provide the needed issue key and URL.

## Explicit Tool Sequence

The successful workflow uses the normal Atlassian MCP connection only. It does not depend on hidden hooks, private memory, or any extra connection outside the active Jira MCP session.

This sequence is mandatory for this workflow. Do not substitute alternative orchestration paths when these tools are available.

Use this exact order:

1. `mcp_atlassian-mcp_createJiraIssue`
2. `mcp_atlassian-mcp_editJiraIssue`
3. `mcp_atlassian-mcp_getJiraIssue` only when link verification is needed
4. `mcp_atlassian-mcp_createIssueLink`
5. Update `Knowledge/product-context/stories/dnaq-story-created.csv` using direct file-edit tooling (for example `apply_patch`)

Tooling guardrails:

1. Do not use terminal scripting to append or modify `Knowledge/product-context/stories/dnaq-story-created.csv`.
2. Do not replace this sequence with helper-agent-only logic or alternate workflows.
3. Keep Jira operations on Jira MCP tools and CSV writes on workspace file-edit tools.

If a backing agent is used, it must follow this skill and prompt only. No extra business rules should live only inside the agent.

## Bulk Mode Rules

1. Accept multi-story plain text blocks and split into stories by headings or numbered items.
2. Accept CSV rows and process each row independently.
3. Continue processing remaining rows if one row fails.
4. Return per-row status:
- `story_ref`
- `created_issue_key` or `error`
- `notes`

## Created Log Rules

After each successful create:

1. Fetch created issue details from Jira.
2. Append one row to `Knowledge/product-context/stories/dnaq-story-created.csv`.
3. Keep cumulative history; never overwrite existing rows.
4. Include source fields + runtime fields:
- `created_issue_key`
- `created_issue_url`
- `create_status`
- `created_at_utc`
5. Keep `assignee` and `assignee__account_id` blank unless explicitly set by the user.

## Completion Output

At the end, provide a concise creation report:

1. Total requested
2. Total created
3. Total failed
4. Created keys list
5. Location of updated created log CSV
