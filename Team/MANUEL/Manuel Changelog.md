---
tags:
  - manuel
  - changelog
updated: 2026-10-26
---

# Manuel Changelog

Part of [[Manuel Home]]. Everything Manuel's Claude changed in the game, **newest on top**. Every change was play-tested in Studio (0 errors) and has a line in PART 1 of the team notebook. Undo any script change: right-click the script > View Script History.

## 2026-10-26

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
