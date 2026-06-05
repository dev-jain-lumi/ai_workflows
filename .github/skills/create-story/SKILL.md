---
name: create-story
description: "Create DNAQ Jira stories from free text or CSV using standard field mappings, defaults, and linking rules."
---

# Create Story Skill

Use this skill when the user asks to create one or more DNAQ Jira stories from free text or CSV input.

## Jira Configuration

- Cloud ID: `3270ee18-7e41-4e45-bede-c73944762da0`
- Project key: `DNAQ`
- Default issue type: `Story`
- Master CSV: `Knowledge/product-context/stories/dnaq-story-master.csv`
- Created-story log: `Knowledge/product-context/stories/dnaq-story-created.csv`

## Core Rules

1. Never add Jira comments during story creation or linking.
2. Never assign stories by default. Leave assignee fields blank unless explicitly provided.
3. Create the Jira issue first with the minimum payload, then update additional fields.
4. Link each story as a child of its feature using `Parent/Child`.
5. Do not create duplicate feature links.
6. Continue bulk processing even if individual rows fail.
7. After each successful create, append one row to the created-story log.
8. Do not overwrite existing created-log history.

## Input Modes

Support both:

- Single story from plain text
- Bulk stories from:
  - Plain text blocks
  - CSV content
  - CSV file path

For bulk plain text, split stories by headings, numbered items, or clear topic boundaries.

## Field Alias Convention

CSV columns use readable workflow aliases. Jira API calls must use Jira system field names.

| Alias | Meaning | Jira system field |
|---|---|---|
| `parent_epic_key__parent` | Epic parent key | `parent` |
| `parent_feature_key__customfield_12445` | Parent Feature URL field | `customfield_12445` |
| `parent_feature_link_key__issue_link_is_child_of` | Feature key used for Parent/Child issue link | Not a field |
| `us_description__customfield_10513` | User Story Description | `customfield_10513` |
| `acceptance_criteria__customfield_10536` | Acceptance Criteria | `customfield_10536` |
| `business_owner__customfield_10512` | Business Owner | `customfield_10512` |
| `lead_solution_designer__customfield_10515` | Lead Solution Designer | `customfield_10515` |
| `dedicated_team__customfield_10803` | Dedicated Team | `customfield_10803` |
| `story_points__customfield_10105` | Story Points | `customfield_10105` |

## Required Per-Story Fields

Each story must have:

- `summary`
- `parent_epic_key__parent`
- `parent_feature_key__customfield_12445`
- `parent_feature_link_key__issue_link_is_child_of`
- `us_description__customfield_10513`

Optional:

- `acceptance_criteria__customfield_10536`

If a required field is missing, fail only that row with a clear error and continue processing the rest.

## Default DNAQ Story Values

Use these unless explicitly overridden by user input or row input.

| Field | Default |
|---|---|
| `project_key` | `DNAQ` |
| `issue_type` | `Story` |
| `priority` | `Medium` |
| `reporter` | `Devashish Jain` |
| `reporter__account_id` | `712020:f645d120-98c0-4029-84c3-01f4405dfce9` |
| `business_owner__customfield_10512` | `Devashish Jain` |
| `business_owner__customfield_10512__account_id` | `712020:f645d120-98c0-4029-84c3-01f4405dfce9` |
| `lead_solution_designer__customfield_10515` | `Jan Floren` |
| `lead_solution_designer__customfield_10515__account_id` | `5e8ed38071d2150b82f49de2` |
| `dedicated_team__customfield_10803` | `DNA DataViz Platform` |
| `dedicated_team__customfield_10803__option_id` | `11911` |
| `story_points__customfield_10105` | `2` |

Assignee defaults:

- `assignee`: blank
- `assignee__account_id`: blank

## Content Quality Rules

### Summary

- Use action-oriented phrasing.
- Keep it concise and specific.
- Avoid implementation noise unless implementation is the actual story value.

### User Story Description

Field: `us_description__customfield_10513`

Use this structure:

```text
Original context: <one sentence from the supplied topic/context>.

As a <role>, I want <goal>, so that <business value>.