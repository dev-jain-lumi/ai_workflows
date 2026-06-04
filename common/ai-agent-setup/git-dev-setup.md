# Git & Dev Environment Setup

## Remotes

This repo pushes to two remotes:

| Remote | URL | Purpose |
|---|---|---|
| `origin` | `https://github.com/dev-jain-lumi/ai_workflows.git` | GitHub (primary, VS Code connected) |
| `gitlab` | `https://gitlab.com/Devashish.Jain1/dataviz_private.git` | GitLab (Gitpod source) |

---

## Keeping GitHub and GitLab in Sync

GitLab is the **primary remote** (Gitpod source). GitHub is a **manual backup** — push to it occasionally, not on every commit.

```powershell
# Day-to-day: push to GitLab only
git push gitlab main

# Backup to GitHub when needed (e.g. end of week, before major changes)
git push origin main
```

---

## Dev Environment

**Gitpod** (browser-based VS Code):

- Open: `https://gitpod.io/#https://gitlab.com/Devashish.Jain1/dataviz_private`
- Config file: `.gitpod.yml` at repo root
- Gitpod auto-installs extensions defined in `.gitpod.yml` on workspace start
- Workspaces auto-stop after 30 min idle; **pin** in Gitpod dashboard to preserve state
- Always commit and push before closing — uncommitted changes are lost when a workspace is deleted

**Local (Windows, VS Code):**

- Path: `C:\Users\JAIND\OneDrive - Luminus\Devashish All\AI_Workflows`
- Remotes already configured (see above)
- Push to both remotes: `git push origin main && git push gitlab main`
- Or rely on GitLab mirror once configured (push to `gitlab` only)

---

## Branching Convention

Working directly on `main` — this is a private solo repo. Rollback via `git revert <commit>` if needed.

---

## Quick Reference

```powershell
# Day-to-day push (GitLab — primary)
git add -A
git commit -m "your message"
git push gitlab main

# Backup push to GitHub (manual, as needed)
git push origin main

# Check remotes
git remote -v

# Roll back last commit (keeps changes staged)
git reset --soft HEAD~1

# Roll back and discard changes
git revert <commit-hash>
```
