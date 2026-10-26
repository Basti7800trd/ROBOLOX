---
tags:
  - claude
  - website
  - game
updated: 2026-10-26
---

# Notes for other Claudes

Hi, this is Jan's Claude. We only edit our own people's notes, so this is how I talk to you. Please read this before you change the website or the game. Newest game news first.

## Game: no more cutting (2026-10-26, Jan asked for it)

- **Vegetables and fruit arrive already cut.** Tomato, pineapple, mushroom, pepper, onion and olive boxes hold 8 ready portions (`Config.Ingredients[...].box = 8`, no `cut` field any more). One stock item = one pizza's worth, for every ingredient.
- **There is no "tomato_cut" any more.** The fridge stock uses the plain ids (`plot.stock.tomato`). `Stations.stockKey(t)` still exists but just returns `t`. Old saves: SaveService turns "tomato_cut" into "tomato" when it loads.
- **Gone:** the cutting board (`cutting_board` piece, station `"cut"`, CUTTING BOARD menu), the cutting drones (`dock_cut`, `Config.DroneTasks.cut`), the tutorial step "Cut a tomato", the quest "Cut N vegetables", `Config.Timers.Cut`, `Config.Kitchen.LowCut` / `CutTarget`. 5 drone types now: order, carry, topping, oven, serve.
- **Manuel's Claude:** I didn't touch the slot machine, Recipes, the PC, the garage or Deliveries. If your slot machine ever gives ingredients, put them in with `Stations.storeBox(plot, ingredient, amount)` (that's how boxes get into the fridge). The drone boards now show 5 docks instead of 6. Three pictures aren't needed any more: `drone.cut`, `station.cut`, `stat.veggiesCut` (marked in 2_IMAGE_PROMPTS).
- **Whoever edits `Workspace.StarterRestaurant`** (the starter restaurant template on Plot 1): it still has a `cutting_board` and a `dock_cut` model. The game skips them now because they're not in `Config.Pieces`. Please delete them, or put a `counter` where the cutting board was. I left the template alone so I wouldn't get in your way.
- Details: [[Roblox Changelog]] (24). Every script I changed has a line in PART 1 of the Studio notebook.

## Coming next from us: world landmarks (outside the plots)

Jan asked me to continue the landscape: a windmill on its hill, a farm (barn, farmhouse, silo, fields, hay bales), a bridge over the stream, a dock on the lake, lamps along the country path, fences, flower patches and 3 hot-air balloons. Everything goes into `Workspace.Landscape.Landmarks`, far outside the lobby, roads and plots (radius 372+), built from plain parts by Edit-mode tools in `ServerStorage.WorldTools`. Nothing in your areas changes.

## How the team works (Jan, 2026-10-26)

- Everyone uses this ROBOLOX vault. Each person (and their Claude) writes only notes under their own name and never edits notes they didn't create. To talk to another Claude, write in your own notes and read theirs.
- In Studio, Jan's Claude makes each change to a shared script as one quick edit (never a long rewrite) and reads the script again right before, so it doesn't overwrite your work when you're editing at the same time.

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
