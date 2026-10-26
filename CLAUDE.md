# Rules for Claude in this vault

This folder is the team's Obsidian vault for the Roblox game **Automate Your Pizza Restaurant** (team: JAN, MANUEL, SEBASTIAN). It is a git repo shared by three people and their Claudes.

- **Pull before editing, commit + push right after** (`git pull --rebase`, then `git add -A && git commit -m "<what changed>" && git push`). Keep commits small so merges stay easy.
- **Plain Obsidian markdown only.** Use `[[Note name]]` links, YAML properties at the top (`tags`, `updated`), and tags like `#open`. Set `updated:` to today's date when you change a note.
- **Don't rename or move notes** unless asked — other notes link to them by name.
- **Todo format:** `- [ ] Task — [[OWNER]] #open` (statuses: `#open`, `#doing`, `#blocked`, `#done`; tick the box when done).
- **Personal pages** (`Team/JAN.md` etc.) belong to that person: only edit someone else's page if they ask.
- **Code notes are snapshots of Roblox Studio.** Studio is the source of truth. When regenerating code from the game, replace the whole code block and update the note's `updated:` property.
- **Never run code from these notes in Studio** without the person confirming, and follow `Code/Limits and safe use.md`.
- Everything in English.
