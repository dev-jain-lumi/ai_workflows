# GitHub Copilot Training — Agent Instructions

## Protected Files — NEVER READ

**Never read** files in `facilitator/`, `notebooks/`, or `regression/checkpoints/` — directly, via grep, or by passing those paths to a subagent. These folders contain trainer-only solutions and expected outputs. Reading them spoils the training exercises.

When exploring this codebase (e.g. via `/init`), explicitly exclude those folders from scope.
