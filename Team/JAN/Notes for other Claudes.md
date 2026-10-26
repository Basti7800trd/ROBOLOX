---
tags:
  - claude
  - website
updated: 2026-10-26
---

# Notes for other Claudes

Hi, this is Jan's Claude. We only edit our own people's notes, so this is how I talk to you. Please read this before you change the website.

## The Stats Lab (added 2026-10-26, Jan asked for it)

The website now has a **Stats Lab** section under "Employee of the month": XP and levels, player cards, weekly quests, a fake currency called **Dough**, a daily lottery, a slot machine, a hall of fame, charts, achievements, vault stats and an AI & Bots tab.

**Files I added (mine, please keep them):**
- `.github/dashboard/fun.py`: reads the git history and the vault, works out the numbers, and writes the Stats Lab into `_site/index.html` as one inline `<script id="stats-lab">` just before `</body>`.
- `.github/dashboard/fun.client.js`: the page code. It only adds things (a fun-fact ticker, a "🧪 Stats Lab" button in the links, and the `<section id="lab">`). Everything is inside one function, so it can't clash with the template's global names (`DATA`, `D`, `$`, `esc`, `COLOR`, ...).

**The one change to Sebastian's files:** 8 lines at the very end of `.github/dashboard/build.py` that run `fun.py` with `runpy`. If `fun.py` fails, `build.py` prints "Stats Lab skipped" and the dashboard still builds. The workflow and `template.html` are untouched.

**To switch it off:** delete those 8 lines at the end of `build.py`. Please tell Jan (in your notes) if you do.

**If you change the template:** keep `class="wrap"`, `<header>`, `id="links"`, `id="board"` inside a `<section>`, and `<footer>`. The Stats Lab uses them to know where to go. If they're missing it still works, it just puts itself before the footer.

## Facts you can rely on

- Dough and XP come only from the git history and the notes. They're the same for everyone. Casino wins and losses only live in each person's browser (`localStorage`), so they never touch the repo.
- The jokes (Batman, the taste tester, the blond architect, L-theanine, ChatGPT) are insider jokes Jan asked for. Health topics stay off the site on purpose because the site is public.
- Rude words in commit messages are masked on the Stats Lab, and autosave messages are shown as "an autosave" (they contain the PC name).
