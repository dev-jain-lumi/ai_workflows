# Reference: Agent prompt that produces the target dashboard

This is the prompt that reliably generates a dashboard close to `dashboard_mockup.html`.
Do not share with participants — they discover this through iteration.

---

## The prompt

> I have actual CET output in `regression/actual/` and reference checkpoints in `regression/checkpoints/`.
> Each pair of files (e.g. `actual_summer.csv` and `checkpoint_summer.csv`) shares the same columns:
> `startDate`, `startTime`, `order`, `cetStartDate`, `cetStarttime`, plus others.
>
> Build a self-contained `dashboard.html` (no server, no npm, no build step — vanilla HTML/CSS/JS only).
> Embed the CSV data inline using fetch or hardcoded JS arrays parsed from the files.
>
> The dashboard should have three sections — winter, summer, october — each containing:
>
> **1. A summary card** showing:
>    - Number of rows where `cetStarttime` differs between actual and checkpoint
>    - Green background if 0 mismatches, red if any
>
> **2. A line chart** (using Chart.js from CDN) where:
>    - X-axis = delivery hour index (0–23 or 0–47)
>    - Y-axis = cetStarttime as decimal hours (e.g. "01:00:00" → 1.0)
>    - Two lines: actual (blue) and checkpoint (green)
>    - In summer, the two lines should be visibly offset by 1.0 across all rows
>    - In winter, the lines should overlap exactly
>
> **3. A detail table** showing startDate, startTime, order, actual cetStarttime, checkpoint cetStarttime:
>    - Rows where actual ≠ checkpoint: red background
>    - The october row where order=B and startTime=02:00:00: yellow background with a tooltip
>      "DST fall-back order B — clock already in CET, no conversion needed"

---

## Why this prompt works

- **Explicit file paths** — agent knows exactly where to read from
- **Column names named** — no guessing the schema
- **Chart.js from CDN** — avoids npm/build, agent knows this library well
- **Y-axis as decimal hours** — tells the agent how to convert time strings for charting
- **Specific colours and conditions** — red/green/yellow with exact conditions
- **Tooltip text given** — the order B explanation is domain knowledge the agent doesn't have

## What participants typically discover through iteration

1. First attempt: usually tables only, no charts
2. Second prompt: charts added but y-axis wrong (strings not numbers)
3. Third prompt: summer offset visible but order B not highlighted
4. Fourth prompt: order B highlighted but tooltip missing or wrong

The progression from 1→4 is the exercise. Each gap teaches something about prompt specificity.
