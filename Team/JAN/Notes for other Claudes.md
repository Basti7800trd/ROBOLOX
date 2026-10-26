---
tags:
  - claude
  - website
  - game
updated: 2026-10-26
---

# Notes for other Claudes

Hi, this is Jan's Claude. We only edit our own people's notes, so this is how I talk to you. Please read this before you change the website or the game. Newest game news first.

## NEW CORE LOOP (2026-10-26, Jan's design; LIVE in Studio, play-tested, 0 errors)

Jan: "instead of the order system we now want a gambling system that brings seeds and you have a farm ... put it inside a big oven where all ingredients go in, the more is in it the bigger it is and the longer the pizza name is, 15 s to cook ... customers don't want a specified pizza but just want anything". Later: "**basti will do the 3d models and general design ui etc**, just make sure to build the functions" (Jan's Claude = the functions, Sebastian = 3D models, design, UI), and the storage = "**a plate in the top right corner of my kitchen** (seen from the entrance) that the vegetables lay on, and you pick them up just by walking up to them".

**The loop:** slot machine seed -> plant it on a farm bed -> it grows (and regrows after every harvest) -> Harvest = a basket in your hands -> walk up to the **storage plate** in the kitchen (basket goes on it; walk up with empty hands = take 6 of the most valuable crop) -> the **big oven** (Put in E / Add from storage G; 15 s from the first topping, more can go in until it's done) -> the pizza lands on the oven's shelf (Take pizza F) -> ANY waiting customer -> they pay the pizza's value + tip. Drones: harvest (farm -> plate), carry (plate -> oven), serve (shelf -> customers).

**APIs you can use** (all server modules in `ServerScriptService.Server`):
- `Farm`: `seeds(player)`, `giveSeeds(player, crop, n, quiet)` (goes through `SlotMachine.giveSeed`), `plant(plot, bed, crop)`, `readyBeds(plot)`, `harvest(plot, bed)` -> crop, amount, `hoverPoint(bed)`, `debugReady(player)`.
- `KitchenStorage` (the plate, piece `storage_plate`, station `"plate"`): `platesOf(plot)`, `count(piece)`, `space(piece)`, `put(piece, crop, n)` -> how many fit, `take(piece, crop?, n)` -> crop, n (crop nil = the most valuable), `total(plot)`.
- `BigOven` (piece `big_oven`, station `"bigoven"`): `of(plot)`, `room(oven)`, `put(plot, oven, crop, n)`, `addFromStorage(plot, oven)`, `readyCount(oven)`, `takePizza(plot, oven)`, `returnPizza(plot, oven, pizza)`, `insideCount(oven)`.
- `Shared.Pizza`: `name(toppings)`, `value(toppings, level)`, `make(toppings, level)`, `model(pizza)`.
- Studio tests: `ServerStorage.DevTools.Loop:Invoke(player, "plant" / "ripe" / "harvest" / "store" / "oven" / "serve" / "drones" / "state")`, plus `Seeds` and `Ripe`.

**For Sebastian's Claude:**
- I saw your edits in `Server.Farm` (3 x 3 plant fields, signposts, the demo). I kept all of them and only added the **unlocking** of locked beds on top (`refreshLocked`, `lockedSoon`, the section "more beds: unlock the next row of the farm"). Please keep those hooks when you edit Farm again (one `lockedSoon(plot)` call at the end of `onPieceAdded` and `onPieceRemoved`, one in `loadFarm`).
- The 3D models are yours (Jan's words): `builders.big_oven`, `builders.farm_bed`, `builders.storage_plate` in `Shared.PieceBuilder` are simple placeholders. The code only needs: the oven parts named `Shelf`, `Spot1`..`Spot4`, `Mouth`, `Chimney` (all optional); the plate part named `Plate` (the crops lie on it); the bed part named `Soil`.
- The drones and the oven take crops from the **plate first, then your harvest tables** (`CropStorage` API: tablesOf / count / space / put / take), then the fridges. Your harvest table stands in the middle lane behind farm row 3; move it wherever you like.
- Template: I added `big_oven` (0, 14), `storage_plate` (-12.5, 25.5), 4 `farm_bed`s (row 1 at z 40), `dock_harvest` (40, 40, rot 90), moved the 2 trees at (±20, 48) to (±46, 64), and moved the old models (garage, PC desk, prep table, small oven, cutting board, old docks) to `ServerStorage.Backups.OldKitchenTemplate`. The folder `FarmPreview` shows the locked rows in Edit mode only; delete it whenever you like.

**For Manuel's Claude:**
- The farm uses your seeds only: `SlotMachine.getSeeds / takeSeed / giveSeed`, the held seed = the Tool's `SeedId`. New players get 4 tomato seeds once (through `giveSeed`). Your 24 new crops work on the farm, in the oven and with the drones (they all have grow / value / harvest).
- Pepperoni, ham, chicken, bacon and gold are not on the slot machine, so nobody can get them right now. Jan hasn't decided yet how they come in.
- ClientMain's PC view and prep view can't open any more (the server never sends "pc" / "prep"). They're yours to delete.

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
