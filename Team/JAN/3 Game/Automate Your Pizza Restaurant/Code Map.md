# Code Map: Automate Your Pizza Restaurant

Part of [[Roblox Home]] -> 3 Game. Where everything lives in the Studio place (state after [[Roblox Changelog]] (12), 2026-10-25). Claude wrote every script through the Studio MCP. Design: [[Beta Plan]]. The team's version (English, for beginners) is in Studio: `ServerStorage.TeamGuide.0_TEAM_NOTEBOOK` PART 4 and `1_READ_ME`.

**Disk copy:** every script is also in `D:\HAVIL\-Roblox\PizzaRestaurant\src\` with Rojo-style paths (`ServerScriptService\Server\*.luau`, `ReplicatedStorage\Shared\*.luau`, `StarterPlayer\StarterPlayerScripts\*.client.luau`, `ServerScriptService\*.server.luau`, `ServerStorage\...`). Studio = disk, byte for byte, at the end of (12). Older versions: `D:\HAVIL\-Roblox\PizzaRestaurant\backup\before-11\` and `ServerStorage.Backups.UI_v1`.

## The new core loop (2026-10-26, [[Roblox Changelog]] (26)): newest first, the tables below are older
| Where | What |
|---|---|
| `Server.Farm` | Farm beds behind the restaurant (`Config.Farm.BedSpots`: rows of 2 beds, a lane, 2 beds), plants that grow and regrow, Plant / Harvest / Remove plant, the seed picker remote `FarmAction`, the locked beds + "Unlock farm bed" (`refreshLocked`), saving `"farm"`. Seeds = Manuel's slot machine (`SlotMachine.getSeeds/takeSeed/giveSeed`). Sebastian added the 3 x 3 plant fields, signposts and a demo. |
| `Server.KitchenStorage` | The storage plate (`storage_plate`, station `"plate"`): crops lie on it; walk up = put down / pick up; API `platesOf, count, space, put, take, total`; saving `"storage"`. |
| `Server.BigOven` | The big oven (`big_oven`, station `"bigoven"`): toppings in, 15 s countdown, the pizza on its shelf, the upgrade board, saving `"oven"`. |
| `Shared.Pizza` | A pizza's name, value, size, item and 3D model. |
| `StarterPlayerScripts.FarmClient` | The seed picker, tap a bed with a seed in hand, the spinning ready cubes. |
| `Server.Drones` | 3 jobs: harvest (farm -> plate), carry (plate -> oven), serve (shelf -> customers); `Drones.ensureDocks` (SaveService `"docks"`). |
| `Server.CropStorage` | Sebastian's harvest tables (the drones and the oven use them after the plate). |
| `Server.Weather` | Sebastian's weather: `Workspace.CropGrowth` makes the plants grow faster. |
| `Server.SlotMachine` + `StarterPlayerScripts.Inventory` | Manuel's seed slot machine and the own hotbar + BAG. |
| Gone | PC, garage, `Server.Deliveries`, prep table, small oven: `ServerStorage.Backups.BeforeNewLoop` + `OldKitchenTemplate`. |
| DevTools (Studio only) | `Loop:Invoke(player, step)`, `Seeds`, `Ripe`, `Fill`, `ServeAll`, `Quest`, `Rejoin`, `Weather`, `CropDemo`. |

## Rules of the code
- **The server decides everything** (money, stock, orders, payments, quests). Clients only send requests through `ReplicatedStorage.Remotes` and show things.
- **All numbers are in one file:** `ReplicatedStorage.Shared.Config`. Change numbers there, not in the scripts.
- **Pieces are data.** Every wall, chair, oven, drone dock... is a piece from `Config.Pieces`, built by `PieceBuilder`. A friend's real model goes into `ReplicatedStorage.PieceModels` named like the piece id (front = -Z, bottom at y 0) and replaces the placeholder. No code change.
- **Every picture is a slot** in `Shared.UIAssets` (90 slots). Empty `image` = the emoji shows. Paste `rbxassetid://...` = the picture shows everywhere.
- **Every sound is a slot** in `Shared.Sounds` (empty = silent).
- Modules talk through hooks, not require loops: `Plots.onPieceAdded / onPieceRemoved / onAssigned / onReleased`, `Economy.onStat`, `SaveService.register(key, { save, load })`.

## The place
| Where | What |
|---|---|
| `Workspace.Map` | The lobby: `Plaza` + rings, `Fountain`, `Road` + `RoadLines`, `Sidewalk`, `LobbySpawn`, `Decor` (benches, lamps, trees) and the 3 boards: `Leaderboard` (attribute `Board = "earned"`, middle), `LeaderboardSpeed` (`pizzasPerMinute`, left), `LeaderboardFastest` (`fastestPizza`, right). |
| `Workspace.Plots.Plot1..6` | One per player around the lobby. Each: `Base`, `Sign` (owner name + "⭐ 2.0" pill), folders `Pieces` (the restaurant), `Customers`, `Decor`. Boxes, drones and shelves are made at runtime. |
| `Workspace.Landscape` | `Props` (440 stylized trees, bushes, rocks from the free packs; attribute `AutoProp`; no collision), `TitleSign`, `Waterfall`. The terrain itself comes from WorldBuilder. `Workspace.Baseplate` is hidden, not deleted. |
| `Lighting` | Sky, Atmosphere, `PizzaColor` / `PizzaBloom` / `PizzaSunRays` / `PizzaDepthOfField` (the old Bloom + SunRays are off). Old values: `ServerStorage.OldLighting.BeforeWorldBuilder`. |
| `ReplicatedStorage.Remotes` | Made by `Net`: Notify, OpenStation, StationAction, StationData, GoHome, ToggleOpen, BuildAction, BuildData, DroneAction, DroneData, Effect, QuestAction, RecipeAction. |
| `ReplicatedStorage.PieceModels` | Real models for pieces (now: `tree`, `bush` from Yasu's pack). |
| `ServerStorage` | `TeamGuide` (`0_TEAM_NOTEBOOK` = the team's shared log + whole story, `1_READ_ME`, `2_IMAGE_PROMPTS`; all English, comment-only ModuleScripts), `WorldTools.WorldBuilder`, `YasuTreePack` + `StylizedRocksPack` (the free asset packs), `OldLighting`, `OldDecor`, `Backups`. In Studio play tests only: `DevTools`. |

## Server (`ServerScriptService`)
| Script | What it does |
|---|---|
| `Main` (Script) | Starts every module in order, player join (save load -> plot -> apply save) and leave (save -> boards -> free the plot), OPEN + HOME buttons, the hint line (player attribute `Hint`), play time, the Studio-only `DevTools`. |
| `DayNightCycle` (Script) | 20-minute days with short blue nights, warm sunrise/sunset, lamps brighter at night, day/night/waterfall sound loops. Numbers: `Config.DayNight`. |
| `Server.Net` | The remotes + `Net.notify(player, text, kind)` + `Net.effect(player, "coins" / "sound" / "celebrate", data)`. |
| `Server.Economy` | leaderstats `Cash` + `Earned`; `spend`, `earn`, `refund`; all stats (`stat`, `statMin`, `onStat` hooks). |
| `Server.Carry` | The ONE item in a player's hands (box or pizza) + the model in front of them. |
| `Server.Plots` | Plot owners, `assign(player, savedLayout)` (builds the saved restaurant, or the starter one), placing pieces, the seating rule, stock + fridge capacity, `home(player)`. |
| `Server.Stations` | Kitchen machines: PC (order panel), fridge, prep table, oven (bake/burn), trash, shelves; the signs + "needs ..." bubbles over them. No cutting board since [[Roblox Changelog]] (24): vegetables arrive already cut. |
| `Server.SlotMachine` | Made by Manuel's Claude (2026-10-26): the topping slot machine in every yard; toppings are unlocked there instead of buying recipes. See Manuel's notes. |
| `Server.Deliveries` | Orders from the PC (players + ordering drones) -> boxes land in the garage after `Config.Timers.Delivery`. |
| `Server.Customers` | NPC customers: walk in, sit at a table, order (patience ring), eat, pay + tip, leave; special customers (VIP, Food Critic, Birthday Kid, Grumpy); tutorial orders. |
| `Server.Rating` | Stars 1-5 (average of the last 30 visits): more stars = more customers + bigger tips. |
| `Server.Recipes` | The Recipe Book: which pizzas a restaurant sells; unlocks cost money + stars. |
| `Server.Build` | The build shop (buy into the backpack), placing from the backpack, turn / move / store. Rules shared with the client in `Shared.Placement`. |
| `Server.Drones` | 5 drone areas (order, carry, topping, oven, serve; the cutting drones went in (24)), up to 5 drones each, upgrades (speed, capacity, battery), dibs so two drones never grab the same thing, jobs by priority. |
| `Server.Quests` | The 10-step tutorial (ends with the first drone; "Cut a tomato" went in (24)) and endless quests sized to the player's pace. |
| `Server.SaveService` | DataStore saving: one key per player (`PizzaProfiles_v1`, `Player_<UserId>`), session lock, autosave every 2 min, save on leave + shutdown, offline drone earnings. Studio without API access = test profiles (nothing kept after Stop). |
| `Server.GlobalBoards` | The data for the 3 boards across all servers (OrderedDataStores; the weekly board resets Monday 00:00 UTC). |
| `Server.Leaderboard` | Draws every Map model with the attribute `Board`: top 10, medals, "Be the first! 🍕", weekly countdown. |

## Client (`StarterPlayer.StarterPlayerScripts`)
| Script | What it does |
|---|---|
| `ClientMain` | The whole screen: 6 big buttons (OPEN, HOME, RECIPES, BUILD, DRONES, STATS), money + stars + next-goal bar, quest pill with CLAIM, guide beam, all panels (PC, prep table, Recipe Book, drone dock, drones list, stats), messages, flying coins, celebrations. Phone / tablet / PC layouts. |
| `BuildClient` | Build mode: shop as one scroll list with 3D previews, backpack, the green/red ghost, turn / move / store, big touch buttons on phones. |

## Shared (`ReplicatedStorage.Shared`)
| Module | What it holds |
|---|---|
| `Config` | Every number: `StartCash`, `Timers`, `Pay`, `Rating`, `SpecialCustomers`, `Ingredients`, `Menu`, `DroneTasks` / `DroneUpgrades` / `DroneBase`, `Quests`, `Kitchen`, `DayNight`, `Save`, `Pieces`, `StarterLayout`. |
| `PieceBuilder` | Builds a piece's model (placeholder parts in the cozy Italian style, or the friend model from `PieceModels`). |
| `Placement` | Placing rules (grid, inside the plot, no overlap), used by server and client. |
| `UIKit` | The UI style: colours, fonts, chunky buttons, panels, bars, messages. |
| `UIAssets` | The 90 picture slots (image id or emoji). |
| `Sounds` | Sound name -> audio id; `Sounds.play(name, part or position)`. |

## Tools (Edit mode only, never in a running game)
- **World:** `require(game.ServerStorage.WorldTools.WorldBuilder)()` in the Command Bar rebuilds the terrain (deletes and rebuilds it; props stay). Roblox draws solid terrain 2 studs higher than its voxels; the builder already corrects that.
- **Landmarks ([[Roblox Changelog]] (25)):** `local S = require(game.ServerStorage.WorldTools.WorldSpots)`, then `require(game.ServerStorage.WorldTools.FarmBuilder)(S, workspace.Landscape.Landmarks)` (same for `WaterBuilder`, `CountryBuilder`) rebuilds that group. Each builder only replaces its own models. Use `require(module:Clone())` from the Command Bar to get a fresh copy after editing a builder. The windmill sails (`SpinSails`) and the balloons (`Float`) are Scripts with RunContext Client: they move on each player's device, so the server does nothing.
- **Test buttons (play tests in Studio):** in the Command Bar, Server view: `game.ServerStorage.DevTools.Fill:Invoke(player)` (fridge full), `ServeAll` (perfect pizza to every waiting customer), `Rejoin` (leave + join = saving test), `Quest` with "finish" / "restart" / "skip" / "new".
- **Helper drafts + READMEs:** `D:\HAVIL\-Roblox\PizzaRestaurant\work\{save,customers,kitchen,ui,quests,world}\`, contract `work\INTERFACES.md`. `work\world\WorldSpots.luau` = spots for landmarks (windmill, barn, bridge, dock, balloons, lamps, fences, flowers) to fill with Creator Store models.
