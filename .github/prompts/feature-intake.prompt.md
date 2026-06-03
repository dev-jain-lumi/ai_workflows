---
name: feature-intake
description: "Use when: start feature intake, new feature, PI prep intake, create feature page for epic"
---

Answer the questions below, then I will extract the content, produce user story material, and create the Confluence feature page as a draft under your Epic.

Answer only what you know — leave anything blank that is not decided yet.

---

**1. Input source**
- [ ] I have a Jira Epic key → provide: `LUMI-_____`
- [ ] I have a Confluence Epic page URL or page ID → provide: ___
- [ ] I'm sharing notes / transcript / brief in this chat (paste below)

**2. Feature name** (short, used in page title)

**3. Header fields**
- Intake priority (High / Medium / Low):
- High-level estimate (HLE) if known:
- Solution architect:
- Tech lead:
- Dedicated team:
- Target final review date:

**4. Scope**
- What problem does this feature solve, and for whom?
- What is explicitly IN scope?
- What is explicitly OUT of scope?

**5. Requirements**
List the most important requirements to implement (ordered by priority):

**6. Technical design**
- Key components / technologies involved:
- Any data flows or integrations to describe?
- Should I generate a PlantUML architecture diagram? (yes / no)

**7. User stories — what you already have**
List any stories or capabilities in mind. I will structure them into a story map with AC and HLE.

**8. Cost / OPEX**
- Expected AWS cost impact (delta)?
- Any new licenses needed?

**9. Interfaces with other applications**
Name any systems this feature will read from or write to (only if known):

**10. SMI impact**
Any impact on Infra, Security, or Workload Automation teams? (yes / no / unknown)

**11. Other release trains**
Does this feature affect any other RT? (yes / no — if yes, which?)

**12. GDPR**
Does this feature involve personal or sensitive data? (yes / no)

**13. References**
- Teams folder or document links:
- Meeting recording or transcript link:
- Any other references:

---

Once you've answered, I will:
1. Summarize my understanding back to you for confirmation
2. Flag any gaps in the must-have sections (0, 1, 3, 4, 5)
3. Produce user story material in story-map format
4. Generate a Rovo instruction file (`Knowledge/project/<initiative>/<jira-key>.rovo.md`) — feed it to Rovo in Confluence and Rovo will create the draft page under your Epic
