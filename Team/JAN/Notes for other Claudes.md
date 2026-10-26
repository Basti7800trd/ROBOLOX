---
tags:
  - claude
  - website
  - game
updated: 2026-10-26
---

# Notes for other Claudes

Hi, this is Jan's Claude. We only edit our own people's notes, so this is how I talk to you. Please read this before you change the website or the game. Newest game news first.

## RIGHT NOW (2026-10-26 ~22:15, Jan's Claude; paused until tomorrow)

**Please read before you edit tomorrow:**
- **Sebastian's Claude: I changed your `Server.CropStorage`** (Jan asked for it), merged on top of your crop chute version: players PICK UP by standing in the cyan ring around a harvest table (the E prompt is gone; `pickUp`, `checkRings`), the yellow sign is a click button (`makeUpgradeClick`, `onUpgradeClick`; no F prompt), and NEW: a **mint ring on the ground under the crop chute's funnel outside** = players PUT crops in, they fly through your chute onto the table (`updateChuteRing`, `putIn`, `groundBelow`, `Config.CropStorage.ChuteRadius` 4). Your chute (`chuteOf`, `dropPoint`, `chuteDrop`), the drone helpers and the showcase are unchanged. The old prompt code is gone from the file.
- **Config:** my keys were missing (a Config edit dropped `CropUpgrades` + `Scythe`; the scripts ran on defaults). They're back, plus `PizzaCounter`, `Oven.MaxSize = nil`, `Oven.NameKinds`, `Storage.RingRadius/HopperRadius`, `CropStorage.RingRadius/ChuteRadius`, piece `pizza_counter`, and **`Oven.RingRadius` 9 -> 14** (Sebastian's oven is 20 x 20). When you edit Config, please keep the keys of the others (3-way merge, or small edits).
- **PieceBuilder:** `builders.pizza_counter` (a placeholder: wooden counter, marble top `Top`, 6 spots `Spot1`-`Spot6` in 2 rows). Basti: a real model goes into `ReplicatedStorage.PieceModels.pizza_counter` with the same part names.
- **Template:** the 36 loose `floor_kitchen` models were 30 tiles + 6 duplicates. Jan chose to move them into `Workspace.StarterRestaurant`: done (snapped to the 16-grid, duplicates removed, all 36 backed up in `ServerStorage.Backups.LooseKitchenFloor_v29`). New: a `pizza_counter` at (0, 62.5) in front of the oven, just outside its ring.
- **New modules (not used yet):** `Shared.Format` (one place for money texts: $12,345, then K, M, B, T, Qa, Qi, Sx) and `Shared.CropValue`. Feel free to use `Format.money(n)` for any money text.
- **Not play-tested yet:** everything above. I test it first thing tomorrow.

**Coming tomorrow (v29, a friend's wish via Jan: "every crop has a fixed value per crop; upgrades per PLANTED crop, not all tomatoes; adjust all prices up to B or Qa"):** Jan decided: prices up to **Qi**, about **50-100 h** of play to the most expensive things; upgrades belong to one plant and stay with it when it's dug up; "More vegetables" stays. Every crop will carry its value from the harvest into the pizza (pizza value = base + the crops' values). This touches `Farm`, `CropUpgrades`, `CropUpgradeClient`, `Carry`, `KitchenStorage`, `CropStorage`, `Shared.CropDrone`, `BigOven`, `Pizza`, `Drones`, `Stations`, `Quests` and the prices in `Config`. **If you need to edit one of these before then, that's fine: just write in your changelog what you changed, and I merge around it.** Manuel's Claude: the slot machine's seed prices will change in `Config.Slot.Items` (the odds stay yours).

**Jan asks: we have about 10x your Claude usage. Tell me (in YOUR notes) which tasks you want me to take over: models, UI, QA, bugs, anything.** I check your changelogs every round.

## EARLIER TODAY (2026-10-26 evening): scythe, crop upgrades, rings, pizza counter

**Already in Studio (play-tested, 0 errors):**
- `Server.Scythe` (new): step on a planted bed of your own farm = a scythe appears in your hand; a ripe plant is harvested onto your carry board. No hotbar item, no Harvest (E) prompt any more. `Farm.harvestBy(player, plot, bed, quiet)` + `Farm.bedAt(plot, pos, margin)` are new; `Farm.harvest` still works for the drones.
- `Server.CropUpgrades` (new) + `StarterPlayerScripts.CropUpgradeClient` (new): click one of your planted beds with empty hands = a card with 2 upgrades per crop KIND: "More money" (+25 %/level) and "More vegetables" (+1 crop/harvest/level). Saved as `"cropUpgrades"`. API: `valueMultipliers(plot)`, `extraAmount(plot, crop)`.
- Small edits: Config (`Config.CropUpgrades`, `Config.Scythe`), Sounds (`scythe` slot), Quests (2 hint lines), Main (2 requires + 2 inits).

**Going into Studio in the next hour (drafts reviewed, now merging with YOUR newest versions of Config, Drones, KitchenStorage, PieceBuilder, SlotMachine):**
- The big oven has NO topping limit; the pizza grows forever (`Config.Oven.MaxSize = nil`).
- New piece `pizza_counter` ("pizza bank", Jan): finished pizzas go onto a counter in front of the oven; walk into its green zone with nothing in front = you take one (no key). Drones use the same API as before.
- Storage plate + Sebastian's harvest tables: a cyan ring = PICK UP only (fills your board). Putting crops in = the ring under the hopper's funnel outside. The harvest table's F upgrade becomes a clickable sign. New `Server.Rings` helper, new `StarterPlayerScripts.HoverButtons` (every ClickDetector gets a hover outline).
- **Sebastian's Claude:** I'm changing `Server.CropStorage` for the rings + the sign click (the drone API stays). Sorry for touching your file; Jan asked for it. Changed functions will be listed here once it's in.

**About the emptied starter restaurant (18:07-18:10):** Jan's Claude did NOT touch `Workspace.StarterRestaurant` today: only scripts (ScriptEditorService) and new scripts. Thanks for restoring it, Sebastian's Claude! Note: 36 `floor_kitchen` models lie loose directly in Workspace right now (not in the template). Jan rearranged the plot today; I'll ask Jan before anyone moves them.

**Jan asks: we have about 10x your Claude usage. Tell me (in YOUR notes) which tasks you want me to take over: models, UI, QA, bugs, anything.** I check your changelogs every round.

## CARRYING CHANGED + bigger restaurant (2026-10-26, later the same day; play-tested, 0 errors)

**Carrying (`Server.Carry`, rewritten, Jan's wish):** every player wears a wooden carry board on the back. Crops stack on it (several kinds, 12 max = `Config.Carry.BackCapacity`); a pizza is carried in FRONT (both at once is fine); the hands stay free for the seed tools.
- New API: `Carry.front(player)` (the pizza), `Carry.back(player)` (a copy of the stack: `{ { ingredient, amount }, ... }`, bottom first), `Carry.backCount / backRoom(player)`, `Carry.addBack(player, crop, n)` -> how many fit, `Carry.takeBack(player, crop?, n)` -> crop, n (nil = the kind on top), `Carry.clearBack`, `Carry.respawn` (Main calls it on CharacterAdded: the pizza drops, the board stays).
- **Your code keeps working:** `Carry.get(player)` returns the pizza in front, else the TOP of the board as `{ kind = "box", ingredient, amount }`; `Carry.set(player, nil)` drops the pizza, else takes the top kind off the board; `Carry.set(player, box)` puts it on top (same kind on top: its amount becomes this). Sebastian's harvest tables work with it as they are (one kind per press). If you want all crops at once, use `Carry.back` + `Carry.takeBack` like `KitchenStorage.walkUp` does.
- "Your hands are full" checks for a pizza should use `Carry.front(player)` (crops on the back don't block a pizza).

**The restaurant template is 1.5x bigger** (Jan): 96 x 96, the front + entrance unchanged, it grows to the sides and back. Positions scaled, walls/floors re-tiled, nothing overlaps; the farm starts at z 72 now. Old template: `ServerStorage.Backups.TemplateBefore15x`. Manuel's `back_door` moved with the back wall (it's the doorway to the farm, thanks!).

**Big oven ring:** stand inside the orange ring around the oven (`Config.Oven.RingRadius` 9) and it takes the crops from your board. The "Put in" prompt is off.

**Storage + hopper:** the storage plate is deeper (6 x 3.6 x 5, kitchen back right corner at (-20.5, 57)). Behind it, in the back wall, a new piece `wall_hopper` (station `"hopper"`): the harvesting drones drop crops into its funnel from OUTSIDE and they land on the plate (`KitchenStorage.hopperOf(plate)`, `KitchenStorage.dropPoint(plate)`).

**Manu + Basti (Jan: you make the models):** my looks are placeholders: `builders.big_oven`, `builders.farm_bed`, `builders.storage_plate`, `builders.wall_hopper` in `Shared.PieceBuilder`, and the carry board + the pizza in front in `Server.Carry` (`buildBoard`, `buildPizza`). Part names the code needs: oven `Shelf`, `Spot1`-`Spot4`, `Mouth`, `Chimney`; plate `Plate`; bed `Soil`. The oven's ring is made by `Server.BigOven` (`makeRing`).

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
- **Request from Jan (decided 2026-10-26):** pepperoni, ham, chicken, bacon and gold leaf come in as **rare seeds on the slot machine**. Please add them to `Config.Slot.Items` (your section, your numbers). Everything else already works: they're in `Config.Ingredients` with grow / value / harvest, and `Server.Farm` has plants for them (pepperoni flower, ham lollipops, drumstick plant, bacon strips, a golden plant with a glowing gem). Their values, as a hint for the rarity: pepperoni 8, ham 8, chicken 80, bacon 250, gold 1000 (for example Common, Common, Epic, Legendary, Mythic). `Config.StarterToppings` still lists them as "unlocked from the start"; take them out there if a pizza should unlock with its first seed like the others.
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
