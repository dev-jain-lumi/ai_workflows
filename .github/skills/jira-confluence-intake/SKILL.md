---
name: jira-confluence-intake
description: "Use when: jira intake, feature intake, PI prep, create feature page, feature Confluence page, user story breakdown, story map, feature brief, meeting to feature, transcript to feature, epic intake"
---

# Feature Intake Skill

Converts an Epic or a user brief into a structured Confluence feature page and user story material for PI prep.

## Atlassian Config

- **Cloud ID**: `3270ee18-7e41-4e45-bede-c73944762da0` (luminus.atlassian.net)
- **Space**: `AIML` (RT Data & Analytics)
- **Feature Template page**: `3209527465` — read this page to get the exact section structure before creating any new page
- **New page location**: child of the Epic's Confluence page (ask user for Epic Confluence page URL or page ID if not provided)
- **Title format**: `LUMI-<key>: <feature name> feature intake for PI prep`

## Input Modes

### Mode A — Epic-driven

User provides a Jira Epic key (e.g. `LUMI-12345`):

1. Read the Jira Epic: summary, description, acceptance criteria, linked issues, components, labels
2. Ask user: "Do you also have a Confluence page for this Epic?" — if yes, read it for additional context
3. Proceed to [Content Extraction](#content-extraction)

### Mode B — Brief-driven

User provides meeting notes, transcript, or free-form brief in chat:

1. Acknowledge and summarize the input back in 3–5 bullet points to confirm understanding
2. Ask any clarifying questions needed for sections 0–4 of the template before proceeding
3. Proceed to [Content Extraction](#content-extraction)

---

## Content Extraction

**Only populate sections where you have real information. Leave a section out entirely rather than filling it with placeholder text or restating what was already said in another section.**

Map input to template sections. For each section, state explicitly what is confirmed vs. assumed.

### Header Metadata

| Field | Source |
|-------|--------|
| Status | always `New` |
| Intake Prio | from user input |
| HLE | extract from input or leave blank |
| Feature Link | Jira feature key if available |
| Epic Link | Jira Epic key |
| Sol. Arch | from user input |
| Tech lead | from user input |
| Final Review Date | from user input |
| Dedicated Team | from user input |

### Section Rules

| # | Section | Populate when… |
|---|---------|----------------|
| 0 | **Scope & Context** (must) | always — problem, for whom, why now, in-scope vs out-of-scope list |
| 1 | **Requirements to implement** (must) | always — ordered by importance; no duplicating scope narrative |
| 2 | **Demo Scenarios** | only if concrete end-to-end scenarios are clear from input |
| 3 | **Technical design** (must) | always — key components and data flows; add PlantUML block if architecture discussed (see below) |
| 4 | **Story mapping & Estimations** (must) | always — story map + assumptions used in HLE |
| 5 | **Cost (OPEX) Impact** (must) | always — even if answer is "no delta identified" |
| 6 | **Interfaces with other Applications** | only if specific integration points are known |
| 7 | **SMI Impact** | only if Infra / Security / WA teams are explicitly affected |
| 8 | **Impact on other Release Trains** | only if another RT is named |
| 9 | **GDPR Compliancy** | only if personal or sensitive data is involved |
| 10 | **References & Links** | always — Jira link + any Teams/meeting links provided |

---

## User Story Material (Section 4)

Do NOT create Jira stories. Produce a story map the user can use to create stories manually:

```
Epic: LUMI-<key>

Capability: <area>
  Story 1: As a <role>, I want <goal> so that <value>
    - AC: [ ] ...
    - HLE: S / M / L / XL
    - Dependencies: ...
```

Group by capability area. Flag stories with external dependencies or needing architecture sign-off.

---

## Architecture Diagram (Section 3 or 6)

When architecture or integration flows are discussed, generate a PlantUML code block following [AGENTS.md PlantUML Standards](../../../AGENTS.md#plantuml-standards). Embed the raw code on the Confluence page inside a `<pre><code>` block — the user will convert it to a diagram manually.

```plantuml
@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam defaultFontName "Work Sans"
skinparam defaultFontSize 13
skinparam ArrowColor #4F9E30
skinparam ArrowThickness 1
skinparam Rectangle {
  BackgroundColor #3D7A25
  BorderColor #2C591B
  FontColor #FFFFFF
  RoundCorner 6
}
' components here
@enduml
```

Rules: clean routing, no crossing lines, split into overview + detail if dense.

---

## Output: Rovo Instruction File

Do not create the Confluence page directly. Instead, generate a Rovo-ready instruction file and save it to:

`Knowledge/project/<initiative>/<jira-key>.rovo.md`

The file must be fully self-contained — Rovo needs zero extra context to act on it.

### File structure

```
# Rovo: Create Feature Page

## What to do
Create a new Confluence page as a **draft** (do not publish).
- Space: AIML (RT Data & Analytics)
- Parent page: <Epic Confluence page URL or ID>
- Title: LUMI-<key>: <feature name> feature intake for PI prep
- Template reference: https://luminus.atlassian.net/wiki/spaces/AIML/pages/3209527465 — mirror its section structure exactly

After creating the draft, add the new page URL as a remote link on Jira Epic <LUMI-key>.

---

## Page content

### Header

| Field | Value |
|-------|-------|
| Status | New |
| Intake Prio | <value or blank> |
| HLE | <value or blank> |
| Feature Link | <value or blank> |
| Epic Link | <LUMI-key> |
| Sol. Arch | <value or blank> |
| Tech lead | <value or blank> |
| Final Review Date | <value or blank> |
| Dedicated Team | <value or blank> |

### 0. Scope & Context
<content — only if available>

### 1. Requirements to implement
<content — only if available>

### 3. Technical design
<content — only if available>

**PlantUML diagram** (embed as a code block — user will render manually):
```plantuml
<diagram code here>
```

### 4. Story mapping & Estimations
<story map content>

Assumptions:
- ...

### 5. Cost (OPEX) Impact
<content or "No delta identified">

### 10. References & Links
- Jira: <link>
- <other links>

---
## Notes for Rovo
- Omit any section heading that has no content above
- Do not add placeholder text or filler
- PlantUML blocks: paste as plain code block, do not render as image
```

### What to tell the user

After saving the file, share the path and say:
> "Feed `Knowledge/project/<initiative>/<jira-key>.rovo.md` to Rovo in Confluence. Rovo will create the draft page and link it back to the Jira Epic."

---

## Local Reference Capture

Also save in `Knowledge/project/<initiative>/`:

| File | Content |
|------|---------|
| `<jira-key>.source.md` | canonical brief used as input |
| `<jira-key>.notes.md` | open questions, decisions, assumptions flagged during intake |

Append any new actions to [MASTER_TODO.csv](../../../MASTER_TODO.csv).

---

## Quality Gate Before Closing

- [ ] Sections 0, 1, 3, 4, 5 have real content (marked "must")
- [ ] Scope explicitly split into in-scope / out-of-scope
- [ ] Every story has an owner or is flagged as unowned
- [ ] At least one assumption stated in section 4
- [ ] Rovo instruction file saved and path shared with user
- [ ] PlantUML code included if architecture was discussed
