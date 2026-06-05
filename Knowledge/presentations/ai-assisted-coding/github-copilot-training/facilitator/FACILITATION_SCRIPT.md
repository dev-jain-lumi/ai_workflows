# FACILITATION_SCRIPT.md

Exact words for key moments. Use these or adapt — the arc matters more than the wording.

---

## Opening (09:00)

> "We have a market data pipeline that ingests hourly forward power curves.
> Last year we added a `cetStarttime` column — delivery time normalised to fixed CET,
> so downstream systems don't have to deal with DST offsets.
> The Python implementation passed all our tests. It shipped.
> Nine months later, a summer regression found 29,211 rows wrong.
> The column was being populated — but it was just copying `startTime` directly.
> In winter, CET equals local time, so the copy looked correct. In June it was off
> by an hour on every single row.
>
> Today you're going to find that bug, write the tests that would have caught it,
> and build the checks that protect every column we add after this one."

---

## M1 — before participants start (~09:05)

> "Open `curve_pipeline/curve_loader.py` in Copilot Chat. Ask it to explain
> what each function does. Then fill in M1_EXPLORE.ipynb. You have 20 minutes.
> Don't look at `cet_converter.py` yet."

At the 15-minute mark, prompt:
> "Find me the test that would pass even if `cetStarttime` just copied
> `startTime` directly. That test exists in `test_curve_loader.py` already.
> Which one is it, and why does it pass with the bug?"

Expected answer: all of them — `test_curve_loader.py` uses winter data only.

---

## M2 — the bug reveal (~09:45)

After participants run the summer regression and see the mismatch count:

> "75 mismatches in the training data — same pattern as the 29,211 in production.
> All in the `cetStarttime` column. All summer records.
> The pattern: Python said 00:00:00. the reference output said 23:00:00 the day before.
> What's the difference? One hour. CEST is UTC+2. CET is UTC+1.
> Python copied the local time. the reference output converts to fixed CET."

After the summer fix:
> "Summer is now clean. Run the fall-back checkpoint."

After seeing 4 mismatches on fall-back (29 before fix → 4 after summer fix; only order B rows remain):
> "Now we're looking at October. Four rows. Same date. What do they have in common?"
Wait for someone to find order B.

> "Oct 25 is the fall-back night. The clock goes 02:00→ 02:00.
> Who can tell me what's special about order B at 02:00?"
Wait for someone to answer.

> "The DST fall-back night. The clock goes 02:00 → 02:00.
> Order A is the first 02:00 — in CEST. Order B is the second — already in CET.
> If you subtract 1 hour from order B, you get 01:00. That's wrong."

---

## M4 — before writing tests (~11:15)

> "The checkpoint that missed the bug was from February. CET equals local time
> in winter — the copy-through matched every row. Zero mismatches. Shipped.
>
> Today you write the test that would have caught it. Before writing a single
> line of implementation, you'll have a test for winter, a test for summer,
> and a test for DST fall-back order B.
>
> That order matters. The summer test is the litmus test. If your implementation
> passes summer, you've done the one thing the original checkpoint couldn't."

After Copilot generates the tests:
> "Find the test that would still pass if I put the copy-through bug back in.
> There should be exactly one: the winter test. If there are more, you're missing
> a test."

---

## M5 — before the SODA section (~13:00, 30 min)

> "You have a working validator. Now you add the last line of defence before a curve
> is published: data quality checks that catch structural problems — missing values,
> wrong types, non-numeric quotes.
>
> The regression runner checks that `cetStarttime` has the right value.
> SODA checks that it's present at all. You need both.
>
> The question to keep in mind: would a SODA check have caught the copy-through bug?
> Think about what the bug actually produces before you answer."

---

## M6 — before the vibe coding session (~13:45, 45 min)

> "Every module so far has had a spec: a test file, a stub, a precise prompt.
> M6 has none of that.
>
> You'll give Copilot a goal and let it build. Your job is to review what it
> produces and verify it's correct — not just that it looks correct.
> Those are different things."

After participants open the dashboard in a browser:

> "Before you ask it to improve anything: is the data right?
> Did it read the CSVs, or did it invent plausible-looking values?
> An agent that builds confidently from wrong data is more dangerous than one
> that says it doesn't know."

---

## Closing (15:50)

> "One thing to take back to your team: every reference checkpoint you use for
> regression needs at least one record from each CET regime. Winter, summer,
> DST fall-back with order B.
>
> If your checkpoint doesn't cover all three, it can't catch all three failure modes."
