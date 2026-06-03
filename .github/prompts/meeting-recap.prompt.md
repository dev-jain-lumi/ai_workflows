---
name: meeting-recap
description: "Use when: prepare for this meeting, meeting prep, convert meeting notes to actions, meeting recap, follow-up actions from meeting"
---

Follow [Workflows/meeting-prep-and-recap.md](../../Workflows/meeting-prep-and-recap.md).

Detect mode from context:

## Mode A — Before Meeting

Required inputs (ask if missing):
- meeting objective and desired outcome
- attendees and their roles
- agenda items

Steps:
1. Define the single desired outcome (decision, alignment, or unblock)
2. List decision points and sensitive topics
3. Draft 2–3 key questions per stakeholder role
4. State the ask and a fallback position
5. Flag risks if the meeting ends without the desired outcome

## Mode B — After Meeting (notes provided)

Required inputs (ask if missing):
- raw meeting notes or transcript
- attendees

Steps:
1. Extract decisions made (exact, unambiguous)
2. Convert each action item to: verb + deliverable + owner + due date
3. List open questions with an owner to resolve each
4. Capture new risks with a mitigation owner
5. Draft a follow-up message (3–5 sentences, decision + actions + next checkpoint)

Apply [Evals/actionability-check.md](../../Evals/actionability-check.md) before finalizing:
- every action has an owner and due date
- no vague verbs (e.g. "look into", "discuss further")
- blockers escalated clearly

Save output to `Artifacts/meeting-notes/YYYY-MM-DD-<topic>.md` using [Templates/meeting-recap.md](../../Templates/meeting-recap.md).
