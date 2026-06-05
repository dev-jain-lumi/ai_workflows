---
name: move-story
description: "Prompt: move an existing DNAQ story to a target epic and feature while changing only parent and feature-link parameters."
argument-hint: "Story key, target feature key, target epic key"
---

Move a Jira story by following the strict workflow in [.github/skills/move-story/SKILL.md](../skills/move-story/SKILL.md).

Inputs (required):

- Story key: ${input:Story key (example DNAQ-823)}
- Target feature key: ${input:Target feature key (example LUMI-10670)}
- Target epic key: ${input:Target epic key (example LUMI-10671)}

Execution requirements:

1. Validate all three inputs before making changes.
2. Change only these parameters:
- `parent`
- `customfield_12445`
- feature `Parent/Child` link direction (`inwardIssue=<feature>`, `outwardIssue=<story>`)
3. Do not modify any other issue fields.
4. Use the exact tool sequence defined in the skill.
5. Always include explicit connection and tool transparency in the result.

Return format:

1. `story_key`
2. `target_epic_key`
3. `target_feature_key`
4. `move_status`
5. `connections_used`
6. `tools_used_in_order`
7. `changed_parameters_only`
8. `residual_links` (if old feature links remain)
9. `story_url`
