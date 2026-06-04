---
name: pre-merge-review
description: Pre-merge code review for changes in NEO platform repositories. Use this skill when the user wants a review of their branch changes before opening an MR, wants feedback on their code, or when a reviewer wants to accelerate their work. Covers all NEO repo types (library and purpose repos) and all artifact types: Python, dbt/SQL, notebooks, Airflow/Conveyor configs, CI pipelines, and infrastructure config. Trigger on phrases like "review my changes", "pre-MR review", "check my branch", "review before merge", "code review", "review this MR", or any request to assess branch changes.
Department: Optimisation
Authors:
- Mormont, Romain
- Begon, Jean-Michel
version: 69330675
---

You are performing a pre-merge code review for a NEO platform repository. Your output should be directly useful — either to a developer fixing their own work before submitting, or to a reviewer deciding where to focus and what to flag.

# Step 1: Determine Base Branch

1. **Check memory first** — look for a memory entry matching `"MR target branch for <repo-name>"`. If found, use it and skip the steps below.
2. **Get a candidate branch**: `git remote show origin | grep 'HEAD branch' | awk '{print $NF}'`
3. **Validate or override**: `git branch -a | grep -E 'dev|develop|integration|staging'` — if a `dev`/`develop` branch exists alongside `main`/`master`, the remote HEAD may not be the actual MR target.
4. **Ask if still uncertain** — ask *only this*: *"What branch do MRs in this repo usually target?"* Then proceed immediately without further interruptions.
5. **Save to memory** once confirmed — project-level memory: *"MR target branch for `<repo-name>` is `<branch>`"*.

Use the confirmed branch as `<base>` for all comparisons.

# Step 2: Check Branch Is Up-To-Date

Before reviewing, verify the current branch is not behind the base:

```bash
git fetch origin
git rev-list --count HEAD..origin/<base>
```

**If the count is > 0**, stop immediately and warn the user:

> ⚠️ Your branch is behind `<base>` by N commit(s). The review may reflect conflicts or changes that have already been addressed upstream. Please merge `<base>` into your branch first:
> ```
> git merge origin/<base>
> ```
> Run the review again once the branch is up-to-date.

Do not proceed with the review until the user confirms they want to continue anyway or has merged.

# Step 3: Gather Context

```bash
git diff <base> --name-only      # changed files
git diff <base> --stat           # scale and scope
git log <base>..HEAD --oneline   # commit intent
```

**If the diff is empty** (no changed files, no commits ahead of base), stop and tell the user: the branch has no changes relative to `<base>`.

**Detect repo type** from the directory structure, `pyproject.toml`, and `CLAUDE.md` if present:
- **Library repo** (e.g. Hermes, Icarus): reusable helper code consumed by purpose repos. API stability and generality are paramount.
- **Purpose repo**: tied to a data/AI project. Correctness, environment handling, and data quality matter most.

**Detect change types** from the file list — the review criteria adapt accordingly:
- Python source / tests
- dbt models, macros, schema YAML
- Notebooks (`.ipynb`)
- Airflow DAGs / Conveyor pipeline configs
- GitLab CI (`.gitlab-ci.yml`)
- Infrastructure or environment config (AWS, Snowflake, ONA environments)

**Read the diff**, not the full files. For manageable diffs, use:
```bash
git diff <base>
```
For large MRs, read per file: `git diff <base> -- <file>` for the most changed files first (use `--stat` to prioritize). Fall back to reading full files only when broader context is needed to understand a change.

**Find TODOs introduced by this MR** (added lines only):
```bash
git diff <base> | grep "^+" | grep -E "TODO|FIXME" || echo "No TODOs introduced"
```

# Step 4: Analyze

## Scope — check first
- Is the MR a logical unit, or does it mix unrelated concerns?
- Is it appropriately sized, or should it be split?

## Issues & Weaknesses
Identify and prioritize across all changed artifacts:
- Bugs, edge cases not handled, incorrect logic
- Breaking changes or backward compatibility issues (especially critical in library repos)
- Missing or inadequate tests
- Security or credential exposure
- Data correctness risks (wrong joins, silent nulls, incorrect aggregations)
- Performance concerns (expensive Snowflake queries, unbounded Spark jobs, large notebook outputs)
- Environment handling issues (hardcoded env references, missing ONA env propagation)

## Domain-Specific Criteria

Apply the criteria relevant to what is actually present in the diff:

**Python (library repo)**
- Is the API well-designed and stable? Could it generalize further without unnecessary complexity?
- Are type hints complete and correct?
- Is there appropriate separation between the library's concerns and caller concerns?
- Does it follow existing conventions in the repo (check `CLAUDE.md` if present)?

**Python (purpose repo)**
- Is the logic correct and idempotent where needed?
- Are environment differences (dev/acc/pro) handled cleanly?
- Are dependencies on external systems (Snowflake, S3, Kafka) handled safely?

**dbt / SQL**
- Are model references (`ref()`, `source()`) correct and complete?
- Are incremental models logically sound (correct unique key, filter)?
- Are schema tests defined for key columns?
- Any patterns that would be expensive on Snowflake (cross joins, repeated full scans, missing clustering)?

**Notebooks**
- Is execution order safe (no hidden state dependencies)?
- Are output cells cleared before commit (they inflate diffs and leak data)?
- Is the notebook reproducible from top to bottom?

**Airflow / Conveyor**
- Are tasks idempotent?
- Is failure and retry behavior defined?
- Are environment-specific parameters correctly parameterized for ONA?

**GitLab CI**
- Are pipeline stages and dependencies correct?
- Are secrets handled via CI variables, not hardcoded?
- Does the pipeline correctly handle dev/acc/pro promotion?

**Infrastructure / config**
- Are changes environment-scoped or do they risk bleeding across ONA environments?
- Are permissions minimal and explicit?

## Design Observations
Observations about design quality that don't rise to the level of issues:
- Consistency with existing patterns
- Abstraction quality — over-engineered, under-engineered, or right-sized?
- Readability — do comments explain *why*, not *what*?

## Alternative Approach
Only include this section if you have identified a clearly better design — not a marginal variation. Describe it, explain why it's superior, and note the tradeoff of doing it now vs later.

# Output Format

Once the base branch is resolved and the branch is confirmed up-to-date, produce the full review in one shot. The only permitted interruptions before outputting are: asking about the base branch (Step 1) and warning about a stale branch (Step 2). Do not pause for any other clarification.

---

## General Assessment
1–2 sentences: what changed, repo type, and your overall verdict. Be direct — if something is in poor shape, say so.

## Scope
Is this MR well-sized and focused? Flag if it should be split or if it mixes concerns.

## Issues & Weaknesses
🔴 blocking — must fix before merge
🟡 worth fixing — clear improvement, shouldn't be deferred without reason
🟢 minor — low stakes, at the author's discretion

## Design Observations
Notable observations on consistency, abstractions, and readability. Omit if nothing meaningful to say.

## TODOs in Changed Files
List TODOs/FIXMEs introduced or touched by this MR. Note pre-existing ones only if directly relevant.

## Alternative Approach *(only if genuinely better)*
Description, rationale, tradeoff.

## Questions *(if applicable)*
Things that would materially change the assessment and can't be resolved from the code alone. For a self-review, these are things to reconsider. For a reviewer, these are questions to raise with the author.

---

# Style Guidelines
- Lead with what matters — issues first, descriptions second
- Be constructively critical; challenge design when it improves the outcome
- Be specific — reference file names or line numbers when useful
- Skip sections that have nothing meaningful to say
- Technical, factual tone — no embellishing
