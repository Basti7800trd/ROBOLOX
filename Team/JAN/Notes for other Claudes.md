---
tags:
  - claude
  - website
  - game
updated: 2026-10-26
---

# Notes for other Claudes

Hi, this is Jan's Claude. We only edit our own people's notes, so this is how I talk to you. Please read this before you change the website or the game. Newest game news first.

## NEW CORE LOOP (2026-10-26, Jan's design; being built right now)

Jan: "instead of the order system we now want a gambling system that brings seeds and you have a farm where you place the seeds and when they are done you can harvest the result, just put it inside a big oven where all ingredients go in, the more is in it the bigger it is and the longer the pizza name is, 15 s to cook ... customers don't want a specified pizza but just want anything ... my friend builds storage and gambling for seeds". Jan's choices: dough + sauce + cheese are FREE (every pizza has them), the farm grows the toppings; the PC ordering, garage, prep table and small oven are REMOVED. Seeds live in the hotbar (one slot per seed kind, like his screenshot of the reference game).

**The loop:** seeds -> plant on a farm bed -> it grows (and regrows after each harvest) -> harvest = a basket in your hands -> storage (fridges/freezers) or straight into the big oven -> the big oven cooks (15 s from the first topping; more can go in until it's done) -> the pizza lands on the shelf in front of the oven -> carry it to ANY waiting customer -> they pay the pizza's value (+ tip).

**Who builds what:**
- **Jan's Claude:**
  - New modules: `Server.Farm` (beds, plants, seeds as hotbar Tools), `Server.BigOven`, `Shared.Pizza` (name, value, size, model), `StarterPlayerScripts.FarmClient` (seed picker fallback).
  - Changed modules: Customers (any pizza), Drones (3 jobs: harvest, carry, serve), Quests (new tutorial), Config, Carry, Main.
  - Stations: the PC, the prep table and the small oven come out.
- **Manuel's Claude (gambling):** please make the slot machine give SEEDS. Call `require(ServerScriptService.Server.Farm).giveSeeds(player, cropId, amount)`, with crop ids = the topping ids in `Config.Ingredients` (pepperoni, ham, tomato, pineapple, mushroom, pepper, onion, olive, chicken, bacon, corn, basil, gold). Farm saves the seeds and makes/updates the hotbar Tool. The fancy coloured hotbar (rarity colours + BAG button like Jan's screenshot) is yours if you want it: each seed Tool has the attributes `Crop`, `Count` and `Rarity`.
- **Sebastian's Claude (storage):**
  - Harvest baskets are Carry items of kind `"box"` (`{ kind = "box", ingredient, amount }`), so your fridges'/freezers' "Store box" prompt takes them as they are.
  - I added `Stations.takeStock(plot, ingredient, amount)` (it takes fridge food first through your `takeFresh`). The big oven and the carry drones use it.
  - If you add a "Take" action to the storage, hand the player `{ kind = "box", ingredient, amount }`: the big oven accepts that.
  - Until then, the big oven has a stand-in prompt "Add from storage".
- **Template (Workspace.StarterRestaurant, whoever owns it):** after the switch the game skips `manager_desk`, `garage`, `prep_table`, `oven`, `cutting_board` and the old docks (`dock_order`, `dock_topping`, `dock_oven`, `dock_cut`). Please delete those models.
  - New pieces you can place: `big_oven` (10 x 9 x 7, the middle of the kitchen), `farm_bed` (8 x 1.4 x 8, in the yard), `dock_harvest`.
  - Until they're in the template, the game adds them by itself when a player joins: the oven in the kitchen middle, 4 beds where the garage was, and the harvest dock at (-48, 25). If a spot is blocked, the piece goes into the player's backpack.
- **ClientMain:** the PC view (`Views.pc`, Manuel's mystery cards) and the prep view (`Views.prep`) can't open any more because the server never sends "pc" / "prep". I left them in place so I don't collide with your edits. Delete them whenever it suits you.

## Game: no more cutting (2026-10-26, Jan asked for it)

- **Vegetables and fruit arrive already cut.** Tomato, pineapple, mushroom, pepper, onion and olive boxes hold 8 ready portions (`Config.Ingredients[...].box = 8`, no `cut` field any more). One stock item = one pizza's worth, for every ingredient.
- **There is no "tomato_cut" any more.** The fridge stock uses the plain ids (`plot.stock.tomato`). `Stations.stockKey(t)` still exists but just returns `t`. Old saves: SaveService turns "tomato_cut" into "tomato" when it loads.
- **Gone:** the cutting board (`cutting_board` piece, station `"cut"`, CUTTING BOARD menu), the cutting drones (`dock_cut`, `Config.DroneTasks.cut`), the tutorial step "Cut a tomato", the quest "Cut N vegetables", `Config.Timers.Cut`, `Config.Kitchen.LowCut` / `CutTarget`. 5 drone types now: order, carry, topping, oven, serve.
- **Manuel's Claude:** I didn't touch the slot machine, Recipes, the PC, the garage or Deliveries. If your slot machine ever gives ingredients, put them in with `Stations.storeBox(plot, ingredient, amount)` (that's how boxes get into the fridge). The drone boards now show 5 docks instead of 6. Three pictures aren't needed any more: `drone.cut`, `station.cut`, `stat.veggiesCut` (marked in 2_IMAGE_PROMPTS).
- **Whoever edits `Workspace.StarterRestaurant`** (the starter restaurant template on Plot 1): it still has a `cutting_board` and a `dock_cut` model. The game skips them now because they're not in `Config.Pieces`. Please delete them, or put a `counter` where the cutting board was. I left the template alone so I wouldn't get in your way.
- Details: [[Roblox Changelog]] (24). Every script I changed has a line in PART 1 of the Studio notebook.

## World landmarks (done 2026-10-26, outside the plots)

Jan asked me to continue the landscape. Now in `Workspace.Landscape.Landmarks`, all plain parts, far outside the lobby, roads and plots (radius 372+):
- a windmill on its hill
- a farm (barn, farmhouse, silo, wheat and tomato fields, hay bales)
- a bridge over the stream and a dock on the lake
- 8 lamps along the country path
- fences, 23 flower patches and 3 hot-air balloons

The tools are in `ServerStorage.WorldTools` (`WorldSpots` + `FarmBuilder`, `WaterBuilder`, `CountryBuilder`). Run one again in Edit mode to rebuild its group; it only replaces what it made itself. The windmill sails and the balloons move through small Scripts with RunContext Client. No game script changed, so nothing in your areas is affected. Details: [[Roblox Changelog]] (25).

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
