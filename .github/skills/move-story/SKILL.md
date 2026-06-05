---
name: move-story-skill
description: "Move Jira DNAQ stories from one feature/epic to another for single or bulk operations, with not-done filtering and strict parent/child relation handling."
---

# Move Story Skill

Use when the user asks to move existing stories from source feature/epic to target feature/epic.

## Jira Config

- Cloud ID: 3270ee18-7e41-4e45-bede-c73944762da0
- Project: DNAQ
- Story issue type: Story

## Supported Input Modes

### Mode A: Feature-scope move (bulk)

User provides:
- source feature key
- source epic key (optional but recommended)
- target feature key
- target epic key
- move scope: all not-done stories

Behavior:
1. Find stories currently related as child of source feature.
2. Read each story status category.
3. Exclude status category Done.
4. Move remaining stories to target feature/epic.

### Mode B: Story-key move (single or bulk)

User provides:
- one or many story keys
- target feature key
- target epic key

Behavior:
1. Move each listed story directly.
2. Do not apply status-based filtering in this mode.

## Mandatory Inputs For Move

- target feature key
- target epic key
- at least one source selector:
  - source feature key with not-done mode, or
  - one or many story keys

If any mandatory input is missing, stop and ask for only missing fields.

## Move Operation Contract

For each story to move:

1. Update epic parent field:
- parent = target epic key

2. Update parent feature URL field:
- customfield_12445 = https://luminus.atlassian.net/browse/<target-feature-key>

3. Ensure final parent/child relation to target feature:
- link type: Parent/Child
- direction: inwardIssue = <target feature>, outwardIssue = <story>

4. Remove old source relation/value:
- replace old epic with target epic
- replace old customfield_12445 with target feature URL
- remove source feature Parent/Child link where story is child of source

## Link Cleanup Rules

1. Read issue links first and detect Parent/Child links to source and target features.
2. If source link exists, attempt delete by issue link id using Jira REST via mcp_atlassian-mcp_fetch.
3. If delete is not available/fails, continue with target link creation and mark story as partial-cleanup-required.
4. Never create duplicate target links.

## Execution Optimization

1. In feature-scope mode, discover candidate stories once.
2. Read only fields needed for filtering and reassignment: status category, issue links, parent epic, and parent feature field.
3. Only write fields that actually change.
4. Return one consolidated result summary instead of interleaving extra verification steps.

## JQL Guidance

For feature-scope discovery, prefer JQL similar to:
- issue in linkedIssues("<source-feature-key>", "is the parent of") AND issuetype = Story

If linkedIssues function behavior is limited in site config, use fallback:
1. Search project stories by recent window and check issuelinks in issue payload.
2. Keep only stories with Parent/Child link where inwardIssue/outwardIssue implies child-of source feature.

## Status Filter Rule

In feature-scope mode:
- Keep only stories where statusCategory != Done.

## Output Format

Return:
1. Summary
- total candidates
- moved
- skipped done
- failed
- partial cleanup required

2. Per-story result rows
- story_key
- from_feature
- to_feature
- from_epic
- to_epic
- status_category
- move_status (moved | skipped_done | failed | partial_cleanup_required)
- notes

## Safety Rules

- Never add comments.
- Never change summary, description, US description, acceptance criteria, or story points.
- Only change fields and links needed for reassignment.
