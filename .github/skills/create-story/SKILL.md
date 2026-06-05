---
name: create-story
description: "Create Jira DNAQ stories from user context (single or bulk), enforce quality rules, apply default fields, create correct child-of feature link direction, and append created results to a tracking CSV."
---

# Create Story Skill

Use this skill when the user asks to create one or more stories from free text or CSV input.

## Jira Config

- Cloud ID: `3270ee18-7e41-4e45-bede-c73944762da0`
- Project: `DNAQ`
- Default issue type: `Story`
- Master defaults source: `Knowledge/product-context/stories/dnaq-story-master.csv`
- Created-story log: `Knowledge/product-context/stories/dnaq-story-created.csv`

## Required Behavior

1. Never add Jira comments while creating or linking stories.
2. For feature relation, story must be child of feature:
- Use `Parent/Child` link type.
- Use direction: `inwardIssue = <feature key>`, `outwardIssue = <story key>`.
3. Do not create duplicate links:
- Read current `issuelinks` first.
- Create link only if the exact child-of relation is missing.
4. After each create, fetch created issue data and append one row to `dnaq-story-created.csv`.
5. Support both single-story and bulk-story creation from:
- Plain text context
- CSV content/path provided by user

## Column Contract

The master CSV contains story-specific columns only:

- `story_ref`
- `summary`
- `parent_epic_key__parent`
- `parent_feature_key__customfield_12445`
- `parent_feature_link_key__issue_link_is_child_of`
- `us_description__customfield_10513`
- `acceptance_criteria__customfield_10536`

All other Jira fields are taken from defaults in this skill unless explicitly overridden by user input.

Per-story required columns (no global default):

- `parent_epic_key__parent`
- `parent_feature_key__customfield_12445`
- `parent_feature_link_key__issue_link_is_child_of`
- `summary`
- `us_description__customfield_10513`

## Default Field Values (DNAQ stories)

Unless explicitly overridden by user or row input, prepopulate with:

- `project_key`: `DNAQ`
- `issue_type`: `Story`
- `priority`: `Medium`
- `reporter`: `Devashish Jain`
- `reporter__account_id`: `712020:f645d120-98c0-4029-84c3-01f4405dfce9`
- `business_owner__customfield_10512`: `Devashish Jain`
- `business_owner__customfield_10512__account_id`: `712020:f645d120-98c0-4029-84c3-01f4405dfce9`
- `lead_solution_designer__customfield_10515`: `Jan Floren`
- `lead_solution_designer__customfield_10515__account_id`: `5e8ed38071d2150b82f49de2`
- `dedicated_team__customfield_10803`: `DNA DataViz Platform`
- `dedicated_team__customfield_10803__option_id`: `11911`
- `story_points__customfield_10105`: `2`

Do not default these values globally; they must come from each story input:

- `parent_epic_key__parent`
- `parent_feature_key__customfield_12445`
- `parent_feature_link_key__issue_link_is_child_of`
- `summary`
- `us_description__customfield_10513`

`acceptance_criteria__customfield_10536` is optional. If missing, create the story without it.

## Quality Rules For Generated Content

### `summary`

1. Use action-oriented phrasing.
2. Keep concise and specific.
3. Do not include implementation noise.

### `us_description__customfield_10513`

1. Structure as: `Original context: ... As a <role>, I want <goal>, so that <value>.`
2. Tie back to user-provided context.
3. Ensure role, goal, and value are explicit.

### `acceptance_criteria__customfield_10536`

1. Outcome-based and testable.
2. One clear completion statement minimum.
3. Avoid vague words like "improve" without measurable intent.

## Jira API Mapping Rules

Before create, validate per story that epic, feature, feature-link direction key, summary, and US description are present. If any is missing, fail that row with a clear error and continue bulk processing.

1. Create issue first with core fields and compatible types.
2. If `customfield_10513` requires ADF, update it via edit call in ADF format.
3. If `acceptance_criteria__customfield_10536` is provided and requires ADF, update it via edit call in ADF format.
4. For `customfield_12445` (Parent Feature URL field), set value as:
- `https://luminus.atlassian.net/browse/<feature-key>`
5. Enforce Parent/Child issue link direction as mandatory (feature -> story child relation).

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

## Completion Output

At the end, provide a concise creation report:

1. Total requested
2. Total created
3. Total failed
4. Created keys list
5. Location of updated created log CSV
