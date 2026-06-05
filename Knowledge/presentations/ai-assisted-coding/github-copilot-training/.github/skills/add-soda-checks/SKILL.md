---
description: Generate Soda data quality checks for a data pipeline output. Use when asked to add quality checks, a SODA scan, or data validation to a pipeline.
---

You are helping add Soda data quality checks to a data pipeline.

## Step 1 — Understand the schema

Read the pipeline's loader or transform file to identify:
- Required columns and their types
- Columns with constrained values (enums, flags)
- Numeric columns where negatives may or may not be valid
- Any timestamp or date columns that are computed (not passed through)

Ask the user to point you to the relevant file if it is not obvious.

## Step 2 — Generate the YAML

Create or update the SODA checks YAML file (typically `soda_checks/<name>.yml`).

The YAML will be loaded programmatically via `soda-core-duckdb` using `scan.add_sodacl_yaml_str()`. Use this format — these are the check types that work reliably:

```yaml
checks for <dataset_name>:
  # Why this check matters: <one line explaining the business rule>
  - missing_count(column_name) = 0:
      name: Human-readable check name

  - invalid_count(column_name) = 0:
      valid values: [VALUE1, VALUE2]
      name: Human-readable check name

  - invalid_count(column_name) = 0:
      valid regex: "^\\d+\\.?\\d*$"
      name: Human-readable check name
```

> **Note**: the `order` column must be renamed to `curve_order` before scanning — `order` is a reserved SQL word in DuckDB. Use `curve_order` as the column name in the YAML.

Rules:
- Add a comment above each check explaining **why** the rule exists, not just what it checks
- Use `warn: when > 0` instead of `fail: when > 0` for non-blocking issues
- Before generating, ask: "Are there any domain rules I should know? For example: which numeric columns allow negative values? Which columns are computed by the pipeline rather than passed through from the source?"

## Step 3 — Identify what SODA catches vs. what it doesn't

After generating the checks, explicitly state:
- Which data quality issues this YAML would surface
- Which issues it would **not** catch (e.g. a value that is present but wrong — that requires a regression test, not a SODA check)

## Step 4 — Show the run command

```bash
soda scan -d <datasource> -c soda_checks/<name>.yml
```

## Discussion prompt

> "SODA catches what is missing or structurally wrong. A regression runner catches what is present but incorrect.
> Which kind of bug would each tool catch in this pipeline?"
