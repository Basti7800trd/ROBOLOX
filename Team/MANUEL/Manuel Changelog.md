---
tags:
  - manuel
  - changelog
updated: 2026-10-26
---

# Manuel Changelog

Part of [[Manuel Home]]. Everything Manuel's Claude changed in the game, **newest on top**. Every change was play-tested in Studio (0 errors) and has a line in PART 1 of the team notebook. Undo any script change: right-click the script > View Script History.

## 2026-10-26

### Our own hotbar + bag
- **Manuel** (2 screenshots from another game): "img1 is the hotbar, img2 is the opened bag, but dont add 'sprays, potions, cleanse, tools'".
- **New:** `StarterPlayerScripts.Inventory` (LocalScript). Roblox's own backpack is switched off.
  - **Hotbar** (bottom middle, kept clear of the money + goal bar): a blue **BAG** button + **10 slots** on a dark brown bar, numbered 1–9 and 0. Slot 1 = Build, then the seeds in the order you got them. Slot colour = rarity (white Common, green Uncommon, blue Rare, purple Epic, …; other tools light blue), a red badge with the count (from 2), a gold outline on the item you hold. Keys 1–0 or a click = hold / put away.
  - **Bag** (the BAG button, X closes it): tabs **All** and **Seeds** only, "BACKPACK" + item counter, a tan grid with every item (also the ones that don't fit in the hotbar), and a taped info card on the right: "PICK AN ITEM" → hover = preview, click = keep it on the card; picture, name, rarity, "You have N", **EQUIP / UNEQUIP**.
  - Works with any Tool, so Jan's garden tools show up too (picture = the Tool's TextureId, otherwise its first letter). Shrinks on small screens.
- **Fixes on the way:** the olive emoji 🫒 is invisible in Roblox (it showed as an empty slot) → 🟢 in `UIAssets` and `Config`, until there's a picture. Moving the mouse to EQUIP used to switch the card to another item → click now keeps the item on the card.
- **Test:** 12 items (Build, 8 seed types, 3 test tools): hotbar showed the first 10 with colours + badges, the bag showed all 12; key 3 = Pepper Seed held; EQUIP = Basil Seed held. 0 errors.

### Test tools: speed slider + infinite money (Studio only)
- **Manuel:** "add a slide bar on the side so i can move faster while testing, also give me infinite money".
- **New (both switch themselves off outside Studio, `RunService:IsStudio()`, so real players never get them):**
  - `ServerScriptService.DevTestTools` (Script): keeps every player's Cash at **$1,000,000,000,000** (tops it up every second when it drops below $100B). "Earned" isn't touched, so the leaderboards stay honest.
  - `StarterPlayerScripts.DevSpeed` (LocalScript): a **SPEED** slider on the right side of the screen, 16 (normal) to 150. Drag the knob or click the bar; the speed stays after respawning.
- To test without the money: select DevTestTools in Explorer > Properties > untick **Enabled**.
- **Test:** slider dragged to 109 → walk speed 109; money $1T. 0 errors.

### The slot machine gives SEEDS (for Jan's garden)
- **Manuel:** "remove the ingredients, add seeds that i can plant in the garden jan is making right now … the player has to pull on the machine for seeds, plant those seeds in the garden, harvest the fruits and vegetables and make the pizza, u and me just should focus on the slot machine and the seeds now".
- **Manuel's choices:** non-plants (dough, sauce, cheese, meat, gold leaf) are Jan's part, skip them · seeds go into the **hotbar**, and into the **backpack** when the hotbar is full (Manuel sends a picture of the bag later) · the **PC stays until Jan's garden works**.
- **Seeds** (`Config.Slot.Items`, price = the seed's value):

| Seed | Rarity | oneIn | Price |
|---|---|---|---|
| Tomato | Common | 3 | $10 |
| Mushroom | Common | 4 | $12 |
| Pepper | Uncommon | 8 | $25 |
| Pineapple | Uncommon | 10 | $30 |
| Onion | Uncommon | 12 | $35 |
| Corn | Rare | 30 | $120 |
| Olives | Rare | 40 | $160 |
| Basil | Epic | 100 | $500 |

- **Changed:**
  - `Shared.Config`: `Config.Slot.Items` = the 8 plant seeds (with `price`); `Config.StarterToppings` now also has pepperoni, ham, chicken, bacon, gold (Jan's part, so they count as unlocked; a pizza unlocks once you've got the seeds of its plants).
  - `Server.SlotMachine`: every roll = **1 seed** (repeats add more). Each seed type is a **Tool** "Tomato Seed x3" (attributes `SeedId` + `Count`, held as a coloured seed packet with the plant's picture). Build stays slot 1; Roblox's backpack holds the tools after the 10 hotbar slots. The first seed of a plant still unlocks its topping, so the PC and recipes keep working. Results say "Tomato Seed" + "NEW!" or "+1 seed"; message "🌱 +N seeds"; celebration "New seed!". Odds board shows the seed names, prices and how many you have. Sign: "🎰 SEED SLOTS 🌱".
  - Seeds are saved (`"slot"` save) and come back after respawning.
  - **For Jan's garden:** `SlotMachine.getSeeds(player)`, `SlotMachine.takeSeed(player, id, n)`, `SlotMachine.giveSeed(player, id, n)`; the held seed = the equipped Tool's `SeedId`. Written in PART 1 of the team notebook for Jan's Claude.
- **Test:** 2 pulls → Build | Tomato Seed x4 | Onion Seed x1 | Mushroom Seed x1 | Corn Seed x2 (BBQ Chicken + Meat Lovers unlocked); same after respawn and after DevTools Rejoin. 0 errors.
- **Pictures needed (Manuel, ChatGPT):** 8 seed packets for the hotbar (Tomato, Mushroom, Pepper, Pineapple, Onion, Corn, Olive, Basil). Until then the hotbar shows the tool names as text.
- Jan is already building the garden side: a weather system ("Rain! Crops grow 20% faster") showed up in the test.

### Slot machine: 9 reels, opening from the middle
- **Manuel:** "make it 9 rolls, and it should start from the middle (roll amount 1 = the middle roll), and upgrade from the middle, (roll amount 2 = left from middle, roll amount 3 = right from middle) and so on".
- **Changed:** `Config.Slot.MaxRolls = 9` (so 9 reels and max 9 rolls). `Server.SlotMachine`: new `reelOf(k)` = which reel roll k uses: 1 → reel 5 (middle), 2 → 4, 3 → 6, 4 → 3, 5 → 7, 6 → 2, 7 → 8, 8 → 1, 9 → 9 (reels counted from the viewer's left). The covers and the results use it.
- The 9th roll costs $6.6M (×3 per roll).
- **Test:** 1 roll = only the middle reel open, 8 covers; 2 upgrades → reels 4, 5, 6 open; a 3-roll pull put the results above those 3. 0 errors.

### Slot machine: one reel per roll, locked reels covered
- **Manuel** (screenshot: grey covers over unused reels): "make the slots that r not used like that …, if i upgrade roll amount, 1 of the rolls unlocks".
- **Changed:** `Server.SlotMachine`
  - The drum has **8 reels** (= `Config.Slot.MaxRolls`), each one roll wide; the drum is now 17.6 studs long, and the caps, counter, lever and both boards moved out to make room (`DRUM_LEN`, `REELS`, `reelX`).
  - Every reel you haven't unlocked has a **grey cover** (a cylinder with two lighter rims) that doesn't turn. You start with reel 1 open (the viewer's left).
  - Buying **Roll Amount** opens the next reel: its cover grows a little and fades away, with a "pop" sound (`refresh` → `m.covers`). After loading a save, the right number of reels is open.
  - Each result now stands **above its own reel**.
- **Test:** new player = 1 open reel, 7 covers; 2 Roll Amount clicks ($1K + $3K) opened reels 2 and 3; a 3-roll pull put Pepperoni, Mushroom and Pineapple above reels 1-3. 0 errors.

### PC: locked toppings are mystery cards
- **Manuel:** "lock all the toppings in the computer, so that the player doesent know what toppings exist".
- **Changed:** `ClientMain` (`Views.pc.card` + `Views.pc.update`): a topping you haven't unlocked shows a **"?"** instead of its picture, **"???"** as name and price, the lock and "🎰 slot machine". Locked cards move to the end of the list; when one is unlocked it shows normally again. The "+" message now says "Unlock this topping at the 🎰 slot machine first" without the name.
- **Test:** a new player's PC shows Dough, Sauce, Cheese, Tomato, then only "?" cards. 0 errors.
- **Later the same day (Manuel: "remove the text 'slot machine' and the emoji"):** the "🎰 slot machine" line on mystery cards is gone; they only show "?", "???", "???" and the lock.
- **Still shows the toppings:** the slot machine's odds board and drum, and the Recipe Book (topping icons of locked pizzas).

### Topping slot machine (replaces buying recipes)
- **Manuel** (2 screenshots from another game): "remove the system how to unlock new toppings, i want a slot machine where u can unlock them, u need to pull a lever to spin, … u start with only 1 roll, and have to upgrade ur roll amount and luck boost …, give each item a rarity and a pull chance and also a custom price".
- **Manuel's choices:** a roll **only unlocks** (repeats give nothing) · pizzas unlock **by themselves** when all their toppings are unlocked · pulling is **free, no waiting** (one spin = 3 s) · new players start with the **Margherita** toppings (dough, sauce, cheese, tomato).
- **How it plays:** every restaurant has a slot machine in its yard (east side, facing the restaurant). Click the red lever ball (or the "Pull" prompt) → the drum spins → one result per roll on the counter: name, rarity, real chance, price, "NEW!" or "✔ have it". New toppings get a message + celebration (fanfare from Epic up). Next to it: a board with **Luck Boost** (green) and **Roll Amount** (blue), clicked like the drone boards, and an **ODDS** board with every topping (✅ = unlocked).
- **The toppings** (`Config.Slot.Items`; price = the PC box price):

| Topping | Rarity | oneIn | Price |
|---|---|---|---|
| Pepperoni | Common | 3 | $10 |
| Ham | Common | 3 | $12 |
| Mushroom | Common | 4 | $12 |
| Pineapple | Uncommon | 8 | $15 |
| Pepper | Uncommon | 10 | $15 |
| Onion | Uncommon | 12 | $18 |
| Corn | Rare | 30 | $25 |
| Olives | Rare | 40 | $30 |
| Chicken | Epic | 100 | $60 |
| Basil | Epic | 150 | $60 |
| Bacon | Legendary | 500 | $120 |
| Gold Leaf | Mythic | 2500 | $500 |

  The game shows the **real** chance, worked out from all of them (e.g. Pepperoni 1 in 4, Gold Leaf about 1 in 3.2K at luck x1.0).
- **Upgrades:** Luck Boost: 10 levels, each +10 % (x1.0 → x2.0); rarer tiers get more of it (chance × luck^tier). Price $500, ×2.2 per level. Roll Amount: 1 → 8 rolls; $1K for the 2nd, ×3 per roll.
- **Changed (in Studio):**
  - `Shared.Config`: new `Config.StarterToppings` + `Config.Slot` (rarities, items, upgrade numbers); box prices by rarity; `unlock`/`stars` in `Config.Menu` marked as not used; quest template `unlockRecipe` weight 0.
  - `Server.Recipes` rewritten: `plot.toppings` (unlocked toppings) → `plot.recipes` worked out from it; `Recipes.unlockTopping`; owner attributes `Recipes` + `Toppings`; old saves (a list of bought pizzas) are converted to their toppings, so nobody loses a pizza. `neededIngredients` = dough + unlocked toppings (what the PC sells and drones order).
  - **New** `Server.SlotMachine`: builds the machine per plot, the spin, results, upgrades, odds board; saved as `"slot"` = { luck, rolls }.
  - `Main`: requires + inits `SlotMachine`, registers the `"slot"` save.
  - `ClientMain`: the PC locks by topping ("🎰 slot machine"); the Recipe Book shows **Missing toppings** + "Spin the slot machine!" instead of stars / price / UNLOCK; the goal bar and red dot no longer point at recipes.
- **Test:** new player = only Margherita; real mouse clicks on the lever: Pepperoni (Common, 1 in 4, $10, NEW!) → the Pepperoni pizza joined the menu by itself; Roll Amount 1 → 5 and Luck x1.2 bought by clicking (right prices taken); a 5-roll pull showed 5 results with readable cards; Recipe Book showed the missing toppings; DevTools Rejoin kept toppings, pizzas, rolls and luck. 0 errors.
- **Good to know:** the drum and result icons use the ingredient pictures from UIAssets, so they change as soon as those pictures are added ([[Picture Checklist]]). Ordering drones now order every unlocked topping, also ones no pizza uses yet. The machine isn't in the tutorial yet.

### Clickable drone upgrade boards
- **Manuel** (with a screenshot from another tycoon): "there are drone upgrade buttons, i want it to work exactly like that, so u can upgrade the drone by just clicking that buttons".
- **Changed:** `ServerScriptService.Server.Drones`
  - `makeBoard` rewritten: a 7 x 5.6-stud board with a yellow frame on top of every dock sign. Title (e.g. "💻 Ordering Drones") and 4 tiles: **Speed** (blue), **Carry Amount** (green), **Battery Size** (light blue), **Drone Amount** (red). Each tile shows "now > next" (14 > 16, 1 > 2, 120s > 144s, 0 > 1 drones) and a price button: green = you can pay, brown = not yet, gold = MAX.
  - Each tile has an invisible click part with a **ClickDetector** (mouse and touch). Speed / Carry / Battery upgrade **all** drones; Drone Amount buys one more drone for that dock. Owner only, 0.25 s spam guard; an open dock panel refreshes too.
  - `updateBoard` rewritten for the tiles (refreshed every second). The old `upgradeLine` was removed. The "Drones" prompt and panel still work.
- **Test:** all 6 boards show the right numbers. Real mouse clicks: Speed 14 > 16 became 16 > 18 ($250 paid), Drone Amount bought the first ordering drone ($1K) and it started ordering.

### Customers only come after "Bake the pizza" in the tutorial
- **Manuel:** "make the customers come first, when i finished the tutorial (when the game says bake a pizza, and after that bring to customer)".
- **Changed:**
  - `Server.Quests`: new `updateCustomerHold` (runs every 0.5 s in `refresh`). During the tutorial steps order, carry, cut, open, make and bake (until the bake is done) it sets `plot.holdCustomers = true`. `onAssigned` holds customers until the quests know the step (safety: released after 60 s if the quests never start); `onReleased` clears it.
  - `Server.Customers` (`plotLoop`): no customers while `plot.holdCustomers` is set; the first one comes ~3 s after.
  - The "Make a pizza" hint without a customer now says **"Make a Margherita at the prep table 🥖🥫🧀🍅"** (before: "A customer is coming").
- Players past the tutorial get customers as before.
- **Test (DevTools Quest "finish"):** steps 1-6 had 0 customers; after "Bake the pizza" the first customer came in 2.6 s.

### BUILD moved to the hotbar (slot 1)
- **Manuel:** "remove the edit ui too, but place it in the hotbar on slot 1" (= the BUILD button).
- **Changed:**
  - New `StarterPack.Build`: a Tool without a handle that can't be dropped, in hotbar slot 1 for every player.
  - `BuildClient`: the BUILD button is hidden (`buildCell.Visible = false`). New "hotbar tool" part: key **1** / click = open build mode, again = close (stops placing / editing). X or opening another panel puts the tool away.
  - `ClientMain`: `HUD.buttonCount = 1`, so RECIPES sits alone in the middle on the left.
- **Notes:** the slot shows the word "Build" until it gets a picture (the tool's TextureId). The tutorial step "Buy and place an item" can't make the BUILD button pulse any more.

### Left buttons cut down + always open
- **Manuel:** "remove the ui closed, home, drones, stats and compact the remaining in the middle", then "b" (no open/close switch).
- **Changed:**
  - `StarterPlayerScripts.ClientMain`: OPEN/CLOSED, HOME, DRONES and STATS are **hidden**, not deleted, so the rest of the script still works. `HUD.buttonCount` + `Layout.apply` centre the buttons that are left. To bring one back: take it out of the hide list and raise `HUD.buttonCount`.
  - `Server.Plots` (`Plots.assign`): `plot.open = true` and the attribute `Open = true` when a player gets a plot. The tutorial step "Open the restaurant" finishes by itself.
- **Without the buttons:** drones are bought at the docks; HOME = walk back; the stats screen can't be opened.

### First picture: the Recipe Book
- **Manuel:** "replace the recipe book with the one i attached" (blue book with a gold compass star, made in ChatGPT).
- The .webp already had a see-through background → converted to a trimmed 512 x 512 PNG → uploaded through Studio → `rbxassetid://87000022272572` → `UIAssets.HUD.recipes`. Shows on the RECIPES button and as the Recipe Book's title icon.

### Joined the team notebook
- Read PART 1 and 1\_READ\_ME; added Manuel's first line to PART 1 (no game changes).

---

**Related:** [[Manuel Home]] · [[Picture Checklist]] · [[MANUEL]]
