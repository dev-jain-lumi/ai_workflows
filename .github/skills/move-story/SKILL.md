---
name: move-story-skill
description: "Move Jira DNAQ stories from one feature/epic to another for single or bulk operations, with not-done filtering and strict parent/child relation handling."
---

# Move Story Skill

Use when the user asks to move existing stories from one feature to another, with optional epic replacement.

Core safety rule:
- NEVER EVER create a new Jira story in this workflow.
- This workflow only fetches existing stories and replaces existing feature/epic relationships with the provided target values.

## Jira Config

- Cloud ID: 3270ee18-7e41-4e45-bede-c73944762da0
- Project: DNAQ
- Story issue type: Story

## Supported Input Modes

### Mode A: Feature-scope move (bulk)

User provides:
- source feature key
- source epic key (optional)
- target feature key
- target epic key (optional)
- move scope: all not-done stories

Behavior:
1. Find stories currently related as child of source feature.
2. Read each story status category.
3. Exclude status category Done.
4. Move remaining stories to target feature.
5. Replace epic only when target epic is explicitly provided.

### Mode B: Story-key move (single or bulk)

User provides:
- one or many story keys
- target feature key
- target epic key (optional)

Behavior:
1. Fetch each listed story directly.
2. Do not require the current/source feature or current/source epic as input in this mode.
3. Read the current feature and epic from the existing issue.
4. Replace the feature with the target feature.
5. Replace epic only when target epic is explicitly provided.
6. Do not apply status-based filtering in this mode.

## Mandatory Inputs For Move

- target feature key
- at least one source selector:
  - source feature key with not-done mode, or
  - one or many story keys

Target epic is optional. If it is not provided, do not change epic.
In story-key mode, current/source feature and current/source epic are not required inputs.

If any mandatory input is missing, stop and ask for only missing fields.

## Move Operation Contract

For each story to move:

0. Fetch the existing story first.

1. Update epic parent field only when target epic is explicitly provided and differs from the current epic:
- parent = target epic key

2. Update parent feature URL field:
- `parent_feature_key__customfield_12445` = `https://luminus.atlassian.net/browse/<target-feature-key>`

3. Ensure final parent/child relation to target feature:
- link type: Parent/Child
- direction: inwardIssue = <target feature>, outwardIssue = <story>

4. Remove current source feature relation and replace it with the target feature relation:
- replace current `parent_feature_key__customfield_12445` with the target feature URL
- remove the current source feature Parent/Child link where story is child of source
- add the new target feature Parent/Child link where story is child of target feature

5. Never create a new issue as part of move:
- if the referenced story does not already exist, fail that row
- do not create placeholders, probes, test issues, or fallback stories

## Link Cleanup Rules

1. Read issue links first and detect Parent/Child links to source and target features.
2. Remove the current feature Parent/Child link.
3. Add the new target feature Parent/Child link.
4. If source-link removal is not available/fails, continue with target link creation and mark story as partial-cleanup-required.
5. Never create duplicate target links.

## Execution Optimization

1. In feature-scope mode, discover candidate stories once.
2. Read only fields needed for filtering and reassignment: status category, issue links, current epic, and `parent_feature_key__customfield_12445`.
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
- Never create a new Jira issue in this workflow under any circumstance.
- Never change summary, description, US description, acceptance criteria, or story points.
- Only change fields and links needed for reassignment.
- Move is simple: fetch existing story -> replace `parent_feature_key__customfield_12445` -> remove current Parent/Child feature link -> add new Parent/Child feature link -> optionally update epic only if explicitly provided and different.
