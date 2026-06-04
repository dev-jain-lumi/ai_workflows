# SETUP.md

## 1. Clone and install

```bash
git clone <repo-url> copilot-training-dc
cd copilot-training-dc
pip install -e ".[dev]"
```

If you don't have a `pyproject.toml` yet, install manually:
```bash
pip install pandas mcp requests
pip install pytest  # for running tests
```

---

## 2. Generate synthetic data

```bash
python data/generate_sample_data.py
```

This creates:
- `data/curve_with_issues.csv` — 7 rows with bad type, null quote, unknown order
- `data/curve_multi_quoted_date.csv` — 144 rows across two quoted dates

---

## 3. Add real data (facilitator only)

The following files are NOT in the repo. Add them before the session:

| File | Description |
|---|---|
| `data/curve_winter.csv` | 3 days × 24h, winter, order A only, no CET issues |
| `data/curve_summer.csv` | June delivery, CEST offset, CET columns wrong (29K mismatches) |
| `data/curve_october.csv` | Last Sunday October, order A + B, 6 mismatches after partial fix |
| `regression/checkpoints/checkpoint_winter.csv` | reference output, February — passes with copy-through bug |
| `regression/checkpoints/checkpoint_summer.csv` | reference output, June — 29,211 mismatches before fix |
| `regression/checkpoints/checkpoint_october.csv` | reference output, fall-back night — 6 mismatches after summer fix |

The checkpoint CSVs must have these columns (matching `_COMPARE_COLUMNS` in `regression_dc_fwd_power.py`):
```
quotedDate, startDate, startTime, order, quote, cetStartDate, cetStarttime
```

---

## 4. Verify setup

```bash
pytest tests/test_curve_loader.py -v
# → 16 tests, all green
```

---

## 5. Configure MCP (Module 6)

Start the MCP server:
```bash
python mcp_server/server.py
```

The `.vscode/mcp.json` file is pre-configured. Open VS Code in this folder —
Copilot Chat should show `curve-tools` and `airflow-tools` in the tool picker.

Set Airflow credentials as environment variables:
```bash
export AIRFLOW_BASE_URL=http://your-airflow:8080
export AIRFLOW_USER=your_user
export AIRFLOW_PASS=your_password
```

---

## 6. Set up git worktrees (Module 5)

Run from the repo root before the session:
```bash
git worktree add .worktrees/scenario-1 -b fix/cet-bug
git worktree add .worktrees/scenario-2 -b feat/order-b-validation
```

Participants open each worktree in a separate VS Code window.
