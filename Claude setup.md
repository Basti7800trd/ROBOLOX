---
aliases:
  - Claude guide
tags:
  - setup
  - claude
updated: 2026-10-26
---

# Claude setup

How to let **your own Claude** read and edit this vault. Pick one way. Your Claude follows the rules in `CLAUDE.md` automatically.

## 0. Before anything (once)

1. Make a GitHub account if you don't have one.
2. Tell Basti or Jan your GitHub username. They invite you to the **RoboloxPizzaGang** organization (organization page → **People** → **Invite member**).
3. Accept the invite (email or github.com/notifications).

Without step 2–3 your Claude can read the repo (while it's public) but **can't save changes**.

## A. Claude in the browser / app (easiest, no install)

1. Open **claude.ai/code** (or "Code" in the Claude app).
2. Connect GitHub when it asks, and allow access to **RoboloxPizzaGang/ROBOLOX**.
   - If ROBOLOX doesn't show up: an organization owner opens the organization → **Settings** → **GitHub Apps** → **Claude** → Configure → adds ROBOLOX under *Repository access*.
3. Start a session on the ROBOLOX repo and tell Claude what to do, e.g. *"Add a task for MANUEL to Todo"*.
4. Claude commits and pushes. Your Obsidian picks it up on the next pull (Obsidian Git does this automatically).

## B. Claude Code on your computer

1. Do the vault setup from `README.md` first (clone with GitHub Desktop, open in Obsidian).
2. Install Claude Code: see docs.claude.com → Claude Code → *Getting started*.
3. Open a terminal **in the vault folder** and run `claude`.
4. Ask for what you need. It reads `CLAUDE.md`, pulls, edits, commits and pushes with your GitHub login.

## C. Claude desktop app with your folder

1. Clone the vault (see `README.md`).
2. In the Claude desktop app, add the vault folder to the chat.
3. Claude edits the files there. **Obsidian Git** then commits and pushes them within 10 minutes (or run *Obsidian Git: Commit and sync* yourself).

## Problems

| Problem | Fix |
| --- | --- |
| Claude says "permission denied" / 403 when pushing | You're not in the organization yet → step 0 |
| Repo not in Claude's list | An owner adds ROBOLOX to the Claude GitHub app (A.2) |
| "Merge conflict" | Someone edited the same lines. Ask Claude: *"pull and resolve the conflict, keep both changes"* |
| Changes don't appear in Obsidian | Ctrl/Cmd+P → *Obsidian Git: Pull* |

---

**Related:** [[Home]] · [[Team]]
