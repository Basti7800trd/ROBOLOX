---
tags:
  - sebastian
  - changelog
updated: 2026-10-26
---

# Sebastian Changelog

Part of [[SEBASTIAN]]. Everything Sebastian's Claude changed in the game, **newest on top**. Most changes were play-tested in Studio; where something was only checked in Edit mode, it says so. Undo any script change: right-click the script > View Script History.

Some changes touch scripts other people own (Jan's `Server.Farm`, the shared `Shared.PieceBuilder` / `Shared.Config`). Those are marked **⚠ touches Jan's code**.

## 2026-10-26

### Farm: wooden planters, 3 × 3 crop fields, signs facing the middle path, dirt paths
- **Sebastian:** "the signs are supposed to face the big path in the middle, make it so only a specific crop can be planted in one field, make the path more dirtlike … with planks (not like a normal floor)", then "instead of bricks, outside the fields make it planks and let the dirt inside look more dynamic".
- **Farm beds** (`builders.farm_bed` in `Shared.PieceBuilder`): a wooden garden planter, 2 rows of plank boards per side in different wood colours, a top board, dark corner posts, ivy on the front corners and a painted maiolica tile with lemons. Inside: 3 raised planting rows, dark furrows, clumps and pebbles. The part `Soil` is unchanged (same size, top still 1.15), so Jan's planting code works as before. The 4 starter beds in `Workspace.StarterRestaurant` were rebuilt.
- **One crop per field, shown as a whole field** (⚠ touches Jan's code, `Server.Farm` `buildPlant` / `scalePlant`): one seed now grows as **3 × 3** smaller plants of that crop in rows (`FIELD_GRID`, `FIELD_GAP`, `FIELD_SCALE`). A field already held only one crop until it's dug up, so nothing mixes. A full field is 60–90 parts (was 7–10); lower `FIELD_GRID` if it gets heavy.
- **Signposts** (⚠ touches Jan's code, `makeSign` / `placeSign` in `Server.Farm`): the crop sign is a wooden signpost instead of a floating billboard. Beds next to the middle path have it on that side, outer beds at their front corner nearest the middle; every board faces the middle path. Same card inside (crop + time left + bar, "✅ Ready!", "🌱 Plant a seed!").
- **Paths** (all 6 plots, `Plot > Decor`, parts `FarmPath` + `FarmPlank`): a dirt path down the middle lane (restaurant back wall to behind the last row) and dirt paths in every gap between the rows, with loose wooden boards across them (crooked, gaps between, different wood colours). They only use the existing gaps; no bed moved, so Jan's unlock order and saved farms are fine.
- **Demo** (`Config.Farm.DemoUntil` + `DemoCrops`, `demoPlant` in `Server.Farm`, ⚠ Jan's code): until that time a new owner's first 2 empty fields get tomatoes + pineapple for free, ready in seconds. Last run until 17:12; it switches itself off. `0` = off.
- **Test:** play test → tomato field (3 × 3) and pineapple field, both signs "✅ Ready!" facing the middle path, 0 errors.
- **Note:** a teammate extended the restaurant towards the farm meanwhile; the first row and its path may now sit very close to the building. Not checked yet (see [[Todo]]).

### Entrance sign: "Luigi's Pizza Shed"
- **Sebastian:** "make the sign more authentic, italian and rename it 'Pizza Shed'", then "make it luigi and put a supermario head in one corner".
- **Changed:** the entrance sign (`builders.entrance` in `Shared.PieceBuilder`): dark green painted board in a gold frame, Italian flag bands top and bottom, **"Luigi's"** + **"Pizza Shed"** in gold calligraphy (Fondamento), "FORNO A LEGNA · DAL 2026" underneath, a ❦ flourish, and a 3D **chef mascot** (white chef's hat, moustache, round nose) in the left corner.
- **Not Mario:** Nintendo's character would risk takedowns/moderation in a public game, so the chef is our own mascot.
- `Server.Plots` no longer writes the owner's name on the entrance (it always says "Luigi's"). The gate sign at the street still says "<name>'s Pizzeria".
- **Test:** checked in Edit mode (screenshot), not in a play test.

### Lobby showcase + spinning rotors + crop drone model saved
- **Sebastian:** "demonstrate the table again, now constantly flying in dropping and taking out crops with the new drone model, with spinning rotors and ingame showcase. remove the sample drone too but save the model".
- **Lobby showcase:** `Workspace.CropShowcase` (a harvest table on the plaza at about 34, 16, facing the fountain). Forever: 3 crop drones fill it ("FULL 25"), wait, carry everything away, repeat. Only for show (no prompts, no owner). Delete the folder to remove it. Code: `CropStorage.showcase`.
- **Rotors:** every rotor's blades hang on a `Motor6D` tagged `DroneRotor`; the new LocalScript `StarterPlayerScripts.DroneRotors` spins them on each player's screen (no network traffic).
- **Model to paste:** `ServerStorage.Models.CropDrone` (its `Basket` script keeps the basket matching the attributes). The sample in Workspace was removed.
- **Test:** play test → showcase looping, 12 rotors spinning, 0 errors.

### Crop drone model
- **Sebastian** (reference picture): "make a drone model … properties to collect, deliver and pick up crops (just pasteable model at first) whichever crop it picks up are supposed to be inside the basket".
- **New:** `ReplicatedStorage.Shared.CropDrone`: a white robot drone with a screen face (cyan "^ ^" eyes), yellow beacon, 4 rotor rings with yellow glow, 2 robot arms with glowing joints and claws, and a blue basket underneath. About 113 parts.
- **Properties (attributes):** `Capacity` (6), `CarryIngredient`, `CarryAmount`, `Task` (idle / collect / pickup / deliver). The crops it carries lie in the basket; while collecting / picking up, its right claw holds one more.
- **API:** `CropDrone.build(cf)`, `.collect` / `.pickUp(drone, crop, n)`, `.deliver(drone, n)`, `.space`, `.contents`, `.watch`, `.crop(ingredient, cf)`. With a harvest table: `CropStorage.dronePickUp(drone, table)`, `CropStorage.droneDeliver(drone, table)`.
- **Not done:** the game's real drone jobs (`Server.Drones`) don't use it yet.

### Harvest table (crop storage)
- **Sebastian** (reference picture): a placeable storage "where later the drones and player themselves can bring harvested crops … visibly shown in stacks … max limit … upgradeable", placed at the back of the plot, with a demo.
- **New piece `crop_table`** ("Harvest Table", Garden category, $250): blue bin with a light blue rim and a yellow sign "Storage Size · 12 / 25 · 25 > 30 · $2K" (red "FULL" when full). Crops lie on top in stacks by kind.
- **Code:** `ServerScriptService.Server.CropStorage`. Size 25, +5 per upgrade, max 75 (`Config.CropStorage`); first upgrade $2K, ×1.8 each. The level is saved per restaurant (`SaveService` key `cropStorage`); the crops on the table aren't.
- **Players:** E = put down the crop basket you carry (what doesn't fit stays in your hands) / take up to 5 of the kind it has most of. F = upgrade.
- **Starter restaurant:** one at plot (0, 80), in the back half.
- **Studio test:** `game.ServerStorage.DevTools.CropDemo:Invoke(player)`: drones fill it, a free upgrade to 30, fill again, empty it; only the table stays.
- **Not done:** the oven doesn't take crops from it yet.

### Weather events: rainbow + unicorns, confetti, event badge, test mode
- **Rainbow** (1 %, sunny is now 59 % so the chances add up to 100): customers pay **×5** (incl. tips), crops grow **×10**, a big rainbow in the sky and 6 winged unicorns with rainbow trails flying around each player. Message: "🌈 Rainbow! Unicorns are flying! Money x5, crops x10".
- **Confetti:** during a rainbow, confetti piles fall near every player (every 3 s, max 8 each, gone after 40 s). Walk into one = **$1** (the seed reward was removed again on request). Server-checked, can't be cheated.
- **Badge** (top left): only for events (rain, storm, rainbow), not normal sunny weather, e.g. "🌈 Rainbow 💰 x5 🌱 x10 • 20m".
- **Test mode:** `Config.Weather.TestFastUntil`: until that time the weather cycles sunny → rain → storm → rainbow every 10 s. Last set to 15:00, now expired. `0` = off.
- **Code:** `Config.Weather`, `Server.Weather`, `Server.Customers` (money ×5), `StarterPlayerScripts.WeatherClient`.

### Weather
- **Sebastian:** "60% sunny … 30% rain which boosts crop growth by 20% … 10% thunderstorm which boosts 100% … rolled every 20 minutes".
- **New:** `ServerScriptService.Server.Weather` + `StarterPlayerScripts.WeatherClient`, settings in `Config.Weather`. Every 20 min a roll (each server also rolls when it starts); a message when it changes.
- **Crops:** `Weather.growth()` or the Workspace attribute `CropGrowth` (1 / 1.2 / 2 / 10). Jan's farm already uses it.
- **Look:** `DayNightCycle` reads `Lighting.WeatherDim` and makes the sky darker and greyer (day and night); thick grey clouds. Rain falls around each player's camera, lightning flashes in storms.
- **Sounds:** `Sounds.ids.weather_rain` and `thunder` are empty (silent) until someone pastes ids.
- **Studio test:** `game.ServerStorage.DevTools.Weather:Invoke("storm")` (or "rain", "sunny", "rainbow").
- **Idea for later:** buy better weather chances with Robux, see [[SEBASTIAN#Ideas for later]].

### Plots twice as long (to the back)
- **Sebastian:** "double the plot size in length to the back".
- **Changed (all 6 plots):** a second grass part `BaseBack` behind each `Base` (now 128 × 256), side hedges longer, back hedge at the new end, the terrain there flattened. `Base` stays the plot centre, so all positions and saved layouts are unchanged.
- **Build limit:** `Placement.PlotBack = 189` (sides + front still 61); the build grid covers the new area.
- **Bug fix:** `BuildClient` and `ClientMain` found the player's plot by name ("Plot1"), which broke after plot 1 was renamed; they now use the `PlotIndex` attribute.

### Storage room: dry room + cooling chamber, fridges spoil food
- **Sebastian:** dry storage with the carrying drones and a connection to the delivery shed, a cooling department with fridges and freezers; food goes bad in fridges, not in freezers, but freezers hold less.
- **Layout:** a wall splits the room. Dry room: carrying drone dock, shelves, back door straight into the delivery shed (moved against the wall). Cooling chamber: white "cold" walls, tiled floor, 2 fridges + 2 freezers. A door from the kitchen into each room.
- **New piece `freezer`** ($600). Freezer holds 30, fridge 60 (`Config.FreezerCapacity`, `Config.FridgeCapacity`). Boxes go into the freezers first; fridge food goes bad after `Config.SpoilMinutes` (10), with a message to the owner. Pizzas use fridge food first. Signs: "🧊 count / cap 🤢 3m" and "❄️ count / cap".
- **Code:** `Server.Stations` (fridges + freezers part), `Server.Plots` (capacity), `Shared.PieceBuilder` (freezer, cold walls).
- **Note:** the team has since moved to Jan's harvest-basket loop; check if this storage logic is still used.

### Dining room ↔ kitchen wall: wide door, one big serving hatch, pickup counter
- **Sebastian** (screenshot): the door wider and on the right, the two hatches merged into one bigger one on the left, a counter behind it with a tip jar, a bell and Italian decoration.
- **New pieces:** `wall_door_wide` (6-wide opening), `wall_pass_wide` (16 wide, holds **8** pizzas, `shelfSlots` in `Config`), `pickup_counter` (wood + marble, pizza board, tip jar, bell, basil, olive oil, "GRAZIE!" sign; decoration only). `Server.Stations` reads the shelf size from the piece.
- **Note:** Sebastian's Claude first changed the street-side front wall by mistake; that was put back exactly as it was.

### Starter restaurant editable in Studio + test plot
- **Starter restaurant in Studio:** `Workspace.StarterRestaurant` = the real models of the starting restaurant (on plot 1). Edit, move, delete pieces in Studio and new owners get exactly that. When the server starts it moves to ServerStorage (never shows twice). Hide it in Studio: drag it into ServerStorage; show again: back into Workspace. `Config.StarterLayout` is only the fallback now.
- **Test plot:** plot 1 is renamed **TestBuildPizzaHut**, has a yellow `Highlight` and its gate sign says "TEST BUILD - PIZZA HUT" (the game writes the owner name there when someone gets it). The highlight is visible in the game too.

---

**Related:** [[SEBASTIAN]] · [[Game overview]] · [[Todo]]
