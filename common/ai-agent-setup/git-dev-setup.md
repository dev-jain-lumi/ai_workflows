# Git & Dev Environment Setup

## Remotes

This repo pushes to two remotes:

| Remote | URL | Purpose |
|---|---|---|
| `origin` | `https://github.com/dev-jain-lumi/ai_workflows.git` | GitHub (primary, VS Code connected) |
| `gitlab` | `https://gitlab.com/Devashish.Jain1/dataviz_private.git` | GitLab (Gitpod source) |

---

## Keeping GitHub and GitLab in Sync (Push Mirror)

Set up a **GitLab push mirror to GitHub** — every push to GitLab auto-replicates to GitHub. No manual double-push needed.

**One-time setup in GitLab:**

1. GitLab project → **Settings → Repository → Mirroring repositories**
2. Click **Add new**
3. Git repository URL: `https://github.com/dev-jain-lumi/ai_workflows.git`
4. Mirror direction: **Push**
5. Authentication: use a GitHub Personal Access Token (PAT) with `repo` scope
   - Generate at: https://github.com/settings/tokens
6. Click **Mirror repository**

Once set, every `git push gitlab main` will also update GitHub within ~1 minute.

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
# Commit and push (local Windows)
git add -A
git commit -m "your message"
git push gitlab main   # mirror handles GitHub sync

# Push to both manually (if mirror not set up)
git push origin main
git push gitlab main

# Check remotes
git remote -v

# Roll back last commit (keeps changes staged)
git reset --soft HEAD~1

# Roll back and discard changes
git revert <commit-hash>
```
