---
aliases:
  - Overview
  - Game design
tags:
  - game
  - overview
  - map
updated: 2026-10-26
---

# Game overview

**Tags:** #game #overview #map · **Updated:** 26 Oct 2026

## The game right now

Automate Your Pizza Restaurant is a multiplayer restaurant tycoon in complete beta: you make pizzas by hand, then buy drones that take over each kitchen step until the restaurant runs itself. It is published privately; only [[JAN]] publishes updates.

### The pizza loop (by hand)

1. **Order** ingredient boxes on the office PC (most cost $10 for 4–5 items). Start money is $100.
2. After **15 s**, boxes land in the garage (max 18). Carry them to a **fridge** (60 items) or **freezer** (30 items).
3. **Cut** vegetables (tomato, pineapple, mushroom, pepper, onion, olives): 1 vegetable = 2 portions, 1.5 s per cut.
4. **Prep table:** add the toppings for the ordered pizza.
5. **Oven:** bakes in **12 s**; take it out within **20 s** or it burns.
6. **Serve** the customer who ordered it: price + a speed tip. A wrong pizza pays half, no tip.

### Customers and stars

- Customers come only while the restaurant is OPEN: one every 20 s at first, max 12 at once.
- They sit only on a chair in front of a table, wait 90 s (ring goes green → yellow → red), eat 8 s, pay and leave. Too slow = they leave without paying.
- **Stars (1–5)** = average of the last 30 visits, scored on the right pizza, speed and a cozy table (2 decorations within 12 studs). New restaurants start at 2.0. At 5 stars customers come every 8 s and tip up to +100%.
- **Special customers:** VIP (from 3 stars, pays 3×), Food Critic (+0.3 stars for 10 min), Birthday Kid (biggest tip), Grumpy (less patience, bonus if served fast).

### Recipe book

Starting pizzas: Margherita $15, Pepperoni $18, Hawaii $20, Veggie $20.

| Pizza | Sells for | Unlock cost | Stars needed |
| --- | --- | --- | --- |
| BBQ Chicken | $40 | $750 | 2 |
| Capricciosa | $60 | $2,500 | 2.5 |
| Diavola | $90 | $8,000 | 3 |
| Garden | $150 | $25,000 | 3.5 |
| Meat Lovers | $250 | $80,000 | 4 |
| Supreme | $400 | $250,000 | 4.5 |
| Golden Pizza | $1,000 | $1,000,000 | 4.8 |

### Build mode and drones

- **BUILD:** SHOP (buy into the backpack) → BACKPACK (place on a grid; a green or red preview shows if it fits) → EDIT (turn, move, store). The starter backpack is empty, so seats must be bought first.
- **Drones:** 6 areas, max 5 drones each; each extra drone in an area costs 2× the one before. First drone prices: Ordering $1K, Carrying $10K, Cutting $100K, Toppings $500K, Oven $2M, Serving $5M.
- **Drone upgrades** (all drones): Speed +15%, Capacity +1 item, Battery +20%; 10 levels each, $250 for level 1, doubling each level. Drones fly over walls when blocked and go home to charge.

### Progression, saving and menus

- **Tutorial:** 11 steps from the first order to the first drone ($400 rewards + $150 for the drone), then one endless quest at a time.
- **Saving:** everything, every 2 min and on leave, with a session lock. Offline: drones earn 25% of the last visit's income per minute, up to 2 h.
- **Menus:** 6 buttons on the left (OPEN, HOME, RECIPES, BUILD, DRONES, STATS), a counting money display, stars, a next-goal bar, a quest pill with CLAIM, a guide beam, flying coins.

### Weather, farm and crops (added 26 Oct 2026, details in [[Sebastian Changelog]])

- **Weather** (new roll every 20 min): ☀️ sunny 59 %, 🌧️ rain 30 % (crops +20 %), ⛈️ thunderstorm 10 % (crops +100 %), 🌈 rainbow 1 % (unicorns fly, customers pay ×5, crops ×10, confetti piles worth $1 each). Rain and storms darken the sky and show rain and lightning; a small badge in the top left shows the current event.
- **Farm look:** fields are wooden planters with planting rows; one seed grows a whole 3 × 3 field of that crop (one crop per field). Each field's signpost faces the middle path; dirt paths with loose boards run down the middle and between the rows.
- **Harvest table** (Garden, $250): crops brought by players or drones lie on it in stacks. Holds 25, +5 per upgrade (first upgrade $2K), max 75.
- **Crop drone:** a robot drone model with a basket that shows the crops it carries (`Shared.CropDrone`; a paste-ready copy in `ServerStorage.Models`). It isn't part of the drone jobs yet.
- **Storage room:** a dry room (carrying drones, door into the delivery shed) and a cooling chamber with fridges (60, food goes bad after 10 min) and freezers (30, nothing goes bad).
- **Restaurant sign:** every restaurant's entrance says "Luigi's Pizza Shed", Italian trattoria style with a chef mascot.

### Not done yet

- All 90 menu pictures are still emojis (prompts in 2\_IMAGE\_PROMPTS) — [[MANUEL]]'s area, with the menus.
- Furniture, oven and drones are still built from simple parts; only trees and bushes are real models.
- Untested: phones, several players in one server, real saving.
- Planned: landmarks (windmill, farm, bridge, dock, hot-air balloons), paint and patterns in build mode, a delivery drone.

## World layout

The lobby is at the world center (0, 0); the 6 plots sit 235 studs out, one every 60°, each turned so its gate faces the lobby. Everything inside radius 350 is flat at y = 0; the hills, lake and mountains start outside it.

![[world-layout.svg]]
*World layout, top-down: lobby + 6 plots.*

Plot centers (x, z): Plot1 (117.5, 203.5), Plot2 (235, 0), Plot3 (117.5, −203.5), Plot4 (−117.5, −203.5), Plot5 (−235, 0), Plot6 (−117.5, 203.5).

| Object | Where (x, z) | Notes |
| --- | --- | --- |
| Fountain | 0, 0 | 22-stud basin with a bowl and spout |
| Spawn (LobbySpawn) | 0, 26 | 14-stud red disc; players spawn facing the fountain |
| Top Earners board | 0, −44 | All-time money, top 10 of all servers |
| Pizzas per Minute board | −40, −40 | Best 5-minute peak |
| Fastest Pizza This Week board | 40, −40 | Resets every Monday |
| Plaza, road, sidewalk | 0, 0 | Flat discs: plaza 128, road 172, sidewalk 184 studs wide |
| Lobby decoration | around the plaza | 44 lamp posts, 30 trees, 4 benches, 4 flower beds, 6 paths to the plots |
| Title sign | 5, −111 | Floats about 50 studs up, 92 studs wide |
| Plots 1–6 | see above | 128 × 256 (twice as long to the back since 26 Oct: `Base` + `BaseBack`), hedges, a stone gate and a name sign; plot 1 is named TestBuildPizzaHut in Studio |
| Harvest table showcase | 34, 16 | On the plaza facing the fountain; crop drones fill and empty it forever (`Workspace.CropShowcase`) |
| Waterfall and lake | 0, 599 | Part of the WorldBuilder landscape |
| Trees, bushes, rocks | x −886 to 865, z −869 to 839 | 370 pack models + 70 loose rocks in Landscape > Props |

---

**Related:** [[Home]] · [[Code]] · [[Todo]]
