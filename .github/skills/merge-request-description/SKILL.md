---
name: merge-request-description
description: Generate a GitLab MR description for the current branch. Use this skill when the user wants to write or generate an MR description, draft merge request content, create a GitLab MR template, or prepare the text to submit with their MR. Trigger on phrases like "generate MR description", "write the MR", "draft the merge request", "create MR description", "fill the MR template", or any request to produce GitLab MR content for the current branch.
Department: Optimisation
Authors:
- Mormont, Romain
- Begon, Jean-Michel
version: c39e99c9
---

You are generating a GitLab MR description for the current branch compared to `main`. The description will be read by reviewers — every word should help them understand the change faster. Do not produce filler, do not pad sections, and do not defer to other files for content that should be inline.

# Step 1: Gather Git Context

Determine the MR target branch using this decision sequence:

1. **Check memory first** — look for a saved entry about the MR target branch for this repository. If found, use it directly and skip the steps below.
2. **Auto-detect**: `git remote show origin | grep 'HEAD branch' | awk '{print $NF}'`
3. **Check for integration branches**: `git branch -a | grep -E 'dev|develop|integration|staging'`
4. **Ask the user if uncertain** — if a `dev`/`develop`/`integration` branch exists alongside `main`/`master`, the auto-detected HEAD may not be the actual MR target. Ask: *"What branch do MRs in this repo usually target? (e.g., `main`, `dev`)"*
5. **Save to memory** once confirmed — write a project-level memory: *"MR target branch for `<repo-name>` is `<branch>`"* so you don't need to ask again.

Use the confirmed branch (referred to as `<base>`) for all comparisons.

Run the following to understand what changed:
- `git diff <base> --name-only` — changed files
- `git diff <base> --stat` — scale and scope of changes
- `git log <base>..HEAD --oneline` — commit intent
- If `CHANGELOG.md` exists, read the relevant entry — use it as a source for the Changes section, but don't just point the reviewer there

Read enough of the changed source files to accurately summarize the change. Do not perform a full code review.

# Step 2: Calibrate Verbosity

**Match the description length to the size and complexity of the change.**

The **Summary** and **Checklist** are always present. The **Checklist** always appears last, after all other sections. Everything else is conditional:

- **Small/focused change** (single fix, minor refactor, config tweak): Summary + Checklist only. Skip all other sections unless one has something genuinely useful to say.
- **Medium change** (new feature, meaningful refactor): use the relevant optional sections. Omit any where you have nothing concrete to add.
- **Large/complex change**: use the full structure.

Never include a section just to fill the template. An absent section is better than a vague or generic one.

# Step 3: Generate the MR Description

Start with a **suggested title** on a single line before the body — the reviewer sees this first:

```
Title: <type>(<scope>): <short imperative description>
```
Use conventional commit style (e.g. `feat(upside): add KPI computer`, `fix(plotter): correct axis label`). Keep it under 72 characters.

Then produce the description body using the template below, selecting only the sections relevant for this MR.

---

## 🧩 Summary
One or two sentences: what does this MR do and why?

## 🎯 Motivation
*(include only if not already obvious from the Summary)*
Why is this change needed? Reference related issue(s) if applicable (e.g. Close #xxx). State the constraint, bug, or opportunity that motivated it.

## 🧠 Changes
What was changed and how. Write this inline — do not just say "see CHANGELOG.md". If the CHANGELOG entry is detailed, you may reference it for completeness, but the key points must appear here.

Note important design decisions, new abstractions, or dependency changes the reviewer should be aware of.

## 🧪 Testing
How the change was validated:
- Unit tests added or modified
- Manual testing steps performed
- Anything deliberately not tested and why

## 🧨 Risks / Impact
*(skip if minimal)*
What could break or requires extra reviewer attention: breaking API changes, migration impact, performance implications, or areas of non-obvious risk.

## 📋 Follow-Ups
*(skip if none)*
Deferred work, known limitations, or TODOs intentionally left for later.

## Checklist
*(author self-check before submitting)*
- [ ] the `CHANGELOG.md` is up-to-date and the version is reflected in the `pyproject.toml` (following semantic versioning);
- [ ] the MR is well formatted:
    * the MR is a logical unit, with reasonable size;
    * the title is descriptive and the template is filled;
    * a (bidirectional) link to the ticket is made;
- [ ] the code is correct and efficient (with proper tests added, clear responsibility, etc.);
- [ ] the code is clear
    * documented or self-documented;
    * typed;
    * following the conventions;
    * reasoning is made apparent when necessary in the code itself.

---

> Disclaimer: this message was automatically generated

---

# Step 4: Write to File

Save the rendered description to `MR_description.md` in the repository root and tell the user where to find it.
