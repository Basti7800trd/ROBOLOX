# Automate Your Pizza Restaurant: Beta Plan

Part of [[Roblox Home]] -> 3 Game. The design of the beta, from the user's words and popups 3 + 4 (2026-10-25, [[Roblox Changelog]] (5)). Numbers marked "proposal" are Claude's first guesses; the user's numbers always win.

## The game
- **Name:** "Automate Your Pizza Restaurant". Published 2026-10-25 17:24 UTC by the user (account Jan_smt), user-owned. GameId `10772980656`, PlaceId `95557580235525`. Private: only the owner + Edit collaborators can open it. The friends were added via Collaborate.
- **The user's words:** "it should be a tycoon like game but very customizable with an ui where you place which chairs etc ... a pizza restaurant that you automate by buying drones and building stuff you have to do everything on your own at the beginning, buy groceries and serve customers etc, later on you are able to automate everything and make more money, deliver pizzas etc."
- "it should be multiplayer with a clean lobby and a bunch of plots for other players by the way a middle with a leaderboard and it should not be like a normal tycoon but something where you can actually decide and do stuff on your own, place buildings etc customize looks"

## Decisions (popups 3 + 4, 2026-10-25)
| Topic | Decision |
|---|---|
| Building | **Starter restaurant, every piece editable**: walls, doors, floors, chairs, ovens... can be moved, repainted, removed or added. Extra buildings outside (drone pad, garage, ...). |
| Pizza making | **Several manual steps** (see the loop below). |
| Groceries | **Walk to the market** in the middle of the lobby, buy a crate, carry it to your fridge. |
| Looks | **All of it:** colors + materials, floor + wall patterns, lights + music, a restaurant name sign. |
| Seating rule (user) | "customers are not happy and will leave if the chair is not standing in front of a table or something". |
| Patience | Customers **leave without paying** when their patience runs out; tips for fast service. |
| Leaderboard | **Total money earned** (all time), in the middle of the lobby. |
| Automation | **All 4 drones**: chef, waiter, grocery, delivery. |
| Pacing (user) | "everything should be possible to automate but with long steps in between so 1h each and the longer you play the more and faster it can become". |
| Testing | Claude may start/stop Studio playtests itself to catch errors. |
| Tools (user) | "use the mcp at all times unless i allow you to use powershell from now on". |

## Redesign decisions after the first look (2026-10-25, popups 6-8, [[Roblox Changelog]] (8))
- **User:** "the layout is first of all too small the players need some space between bases and the design looks bad, did you put the kitchen in an extra room yet? then there should be a drone spawnpoint where you can buy 1 dron for x amount of money or upgrade all their speed capacity and battery they go back to their spawn if they dont have battery left and move like smart AIs".
- **Plots:** 128x128 (was 96) with ~55 studs of greenery, paths and fences between neighbours.
- **Restaurant:** 2x bigger, 64x64. **Style: cozy Italian pizzeria** (brick outside, red-white awnings, big PIZZERIA sign; wood + cream inside, checkered tablecloths, warm lamps; white-tiled steel kitchen) **plus a big garden around the building** (entrance area etc.), "so the plot is not just the building".
- **Everything looked bad** (lobby + map, outside, inside + furniture, HUD) -> all of it gets redone.
- **Furniture:** "you always have to order seats etc and later place them where you want ... out of a backpack ... highly customizable yet simple". Bought in a **Shop tab of the build menu** -> goes into the **backpack** -> placed with the mouse.
- **Chunks:** "you dont buy chunks your chunks are where you can place stuff" = the plot is a grid of squares you place on; no land buying.
- **Drones:** "1 drone is for 1 task you can buy them in their areas ... 1 area where you can have max 5 working at a time and they autonomate 1 task". **6 drone areas:** ordering (PC), carrying (garage -> fridge), cutting, toppings (prep table), oven, serving. Max 5 drones per area. Drones fly back to their area's dock to recharge when the battery is empty, and move like smart AIs.
- **Drone prices:** the user: "a lot like 1k 10k 500k 2m smth like that" -> first drone per area: ordering $1K, carrying $10K, cutting $100K, toppings $500K, oven $2M, serving $5M; each extra drone in the same area x2 (Claude's fill-in, changeable). (An earlier popup said "$500 first drone"; the later answer wins.)
- **Upgrades** (apply to ALL drones): speed, capacity, battery; 10 levels each, $250 doubling (speed +15 %, capacity +1, battery +20 % per level).
- Handoffs between drones (Claude's design): topping drone puts raw pizzas on the prep table shelf -> oven drone bakes and puts them on the serving hatch -> waiter drone serves the customer who ordered it.

## Changes after the start (2026-10-25, [[Roblox Changelog]] (6))
- **No market.** The user: "remove the shop and use a pc for like a manager room where you can order the stuff you put on the pizzas for now and it will get thrown into your garage where you can put it in the kitchen". Built: a manager office with a desk + PC (order screen), single-ingredient boxes ($10 each), delivery after 15 s into a **garage** next to the restaurant (boxes bounce in), pick up -> fridge. The lobby middle only has the spawn + leaderboard now.
- **Style reference:** the Roblox game "Automate a Restaurant" (user: "higher focus on design and style mechanic how it works but for our game"). Taken over: orange plank floors with dark gaps, pink walls with blue stone trim, chunky rounded HUD buttons with icons, big green money bottom-left, bold white text with dark outlines. Seen there too (ideas, not decided): rarity labels on ingredients ("Rare 1 in 175"), a leaderboard with SERVER / RECIPES / ALL TIME tabs, Rewards / Index / Saves buttons, a friend boost. The user will show more references another time.
- **Real restaurant layout** (user: "the kitchen is supposed to be a seperate room ... take inspiration of real restaurant layouts", Changelog (7)): dining room in front; a separate tiled kitchen behind it with a kitchen door + serving hatch (the "pass"); the office off the kitchen; a back door from the kitchen to the garage (deliveries come in the back, like real restaurants). Later automation idea: chef drone puts pizzas on the pass, waiter drone serves from there.
- **Status:** milestones 1 + 2 built and tested (see the Changelog); the crates/market sections below are history.

## The manual loop (before any drone)
1. ~~Market~~ -> **manager PC**: order single-ingredient boxes; they land in the garage after 15 s. Carry one box at a time.
2. **Fridge** in your restaurant: "Store box" puts the ingredients into your stock.
3. **Cutting board:** vegetables and fruit must be cut before use (user: "cutting vegetables and opening them from the crate").
4. **Prep table:** dough -> sauce -> cheese -> the toppings THIS customer ordered (user: "one customer wants hawaii pizza and you need to put the ingedients they want on it"). You carry the raw pizza.
5. **Oven:** bake timer; take it out in time or it burns (proposal).
6. **Serve:** carry it to the customer at their table. The right pizza = price + tip for speed. A wrong pizza = proposal: half price, no tip.

## Customers
- Walk in from the street side of your plot and look for a free chair that **stands in front of a table**. None = unhappy bubble, they leave.
- Sit, order a pizza from the menu (an order ticket over their head + a list in the kitchen), patience bar.
- Served in time: eat, pay, leave. Patience gone: leave without paying.

## Menu (proposal)
| Pizza | Ingredients | Price (proposal) |
|---|---|---|
| Margherita | dough, sauce, cheese, tomato (cut) | $15 |
| Pepperoni | dough, sauce, cheese, pepperoni | $18 |
| Hawaii | dough, sauce, cheese, ham, pineapple (cut) | $20 |
| Veggie | dough, sauce, cheese, mushroom (cut), pepper (cut) | $20 |

## Market crates (proposal)
- **Basics** $30: 5 dough, 5 sauce, 5 cheese.
- **Veggies** $20: 3 tomatoes, 3 mushrooms, 3 peppers (each cut = 2 portions).
- **Meat + Fruit** $25: 4 pepperoni, 4 ham, 3 pineapples (each cut = 2 portions).

## Other numbers (proposals)
- Start cash $100. Patience 90 s. Bake 12 s, burns 20 s after it's done. A new customer about every 20 s while a valid free seat exists. Tip up to +50 % for speed.
- **Automation pacing:** price each next drone / automation step so it takes about **1 hour of play** to afford (user). Upgrades make drones faster over time.

## Lobby + plots
- A clean lobby: spawn in the middle, the **leaderboard** (total money earned) and the **market** there.
- Plots around it (proposal: 6 per server), one per player, assigned on join; the owner's name on a sign.
- Each plot: a starter restaurant made of pieces + free land for extra buildings.

## Milestones
Status 2026-10-25 after [[Roblox Changelog]] (12): M1, M2, M4, M5 built + tested by Claude in Studio; M3 built without paint / patterns / name sign; M6 not started. Extra (from the research): stars, recipe ladder, special customers, tutorial + endless quests, 3 global boards, landscape + day/night, UI with 90 image slots. Not tested yet: real DataStore saving, phones, several players.
1. **M1 Lobby + plots + starter restaurant:** map, plot assignment, cash, leaderstats, leaderboard board. ✅
2. **M2 Manual loop:** ~~market crates~~ PC orders + garage boxes, carrying, fridge stock, cutting board, prep table (topping UI), oven, customers (seating rule, orders, patience, tips). ✅
3. **M3 Build mode:** catalog UI, place / move / rotate / sell on a grid, paint (colors + materials), floor + wall patterns, lights + music, name sign. ✅ shop + place / move / turn / store; ⬜ paint, patterns, name sign.
4. **M4 Saving:** cash, total earned, the restaurant layout, stock, unlocks; global leaderboard. ✅ (Studio test mode only)
5. **M5 Drones:** grocery, chef, waiter, each ~1 h apart, plus upgrades. ✅ 6 drone areas (order, carry, cut, topping, oven, serve) + 3 upgrades.
6. **M6 Delivery:** delivery area + delivery drone. ⬜

## Tech plan (Claude)
- **Server decides everything** (money, stock, orders, payments); clients only send requests (RemoteEvents) and show things.
- Players and drones use the SAME station actions (take stock, cut, prep, bake, serve), so automation plugs into the manual loop.
- **Pieces are data** (a catalog in a shared ModuleScript); each piece's look comes from `ReplicatedStorage.PieceModels.<id>` if a friend made a model, else from a simple placeholder built from parts. So the art friends can swap models without touching code.
- UI is built in code for the beta; it moves to Studio-made UI when the UI friend takes over.
- Saving: Claude's own small DataStore module; ProfileStore (a community library) only with the user's yes.
- Source files are kept on disk too (`D:\HAVIL\-Roblox\PizzaRestaurant\src\`) for backups and later Git.
- All Studio work goes through the Studio MCP (user's rule). Roblox's own skills via the MCP `skill` tool: `rbx-debug`, `rbx-device-simulator-lua` (phone UI tests), `rbx-docs-search`, `rbx-perf-profiling`, `rbx-scene-analysis`, `rbx-unit-test`, `rbx-create-skill`.

## Later / ideas
- The user: "maybe ill switch to a self made garden instead of a shop later we will see": grow your own ingredients instead of the market.
- Restaurant likes / visits between players.
- After the start: **split the tasks in the team** (popup).

## Playtest questions (for M1 + M2, ask in popups after the test)
- Did you get your own plot with your name on it?
- Could you buy a crate at the market and carry it home?
- Did opening the crate fill your fridge?
- Did cutting work?
- Could you put the right toppings on the pizza?
- Did the oven bake it (and burn it when you waited too long)?
- Did customers only sit on chairs in front of tables, and leave when there was none?
- Did serving pay you, with a tip when you were fast?
- Is the money on the leaderboard?
