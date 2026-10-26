# Next To-Dos

Part of [[Roblox Home]]. What comes next for "Automate Your Pizza Restaurant", in order. Written 2026-10-25 when the user paused the work ([[Roblox Changelog]] (13)); the friends work in Studio in the meantime. Claude ticks items off and adds new ones.

## 0. First thing when Claude is back (every time)
1. Pull the team repo, then read PART 1 of the shared team notebook in Studio (`ServerStorage.TeamGuide.0_TEAM_NOTEBOOK`, newest on top) and the friends' notes in this vault: `Team/MANUEL/` (Manuel Changelog first) and `Team/SEBASTIAN.md`. Then the top of [[Roblox Changelog]].
2. The friends may have changed scripts. Compare every Studio script with the disk copy in `D:\HAVIL\-Roblox\PizzaRestaurant\src\` (sizes + checksums: the table at the end of Changelog (27)). Copy their changes to disk BEFORE editing anything (Playbook 4, 2026-10-26: the helper + checksum method). Someone may be editing right now: list the sizes twice, 45 s apart.
3. Run a quick play test (0 errors?) to check the friends' changes didn't break anything.
4. After every change of mine: the changelog entry here, a PART 1 line in the Studio notebook when the game changed, and [[Notes for other Claudes]] when the other Claudes need to know. Everything in English.

## 1. Next
- [x] **The new core loop** (done, [[Roblox Changelog]] (26)): seeds -> farm -> storage plate -> big oven -> any customer, 3 drones, new tutorial. Play-tested with DevTools, 0 errors.
- [x] **Bigger restaurant, the oven's ring, the hopper, the carry board** (done, [[Roblox Changelog]] (27)). Play-tested with DevTools, 0 errors.
- [ ] **Jan's playtest of the new loop** with real clicks (Plant, Harvest, Unlock farm bed, the storage plate, the oven's ring, Take pizza, the carry board) -> popups G-I in [[Playtest Questions]].
- [x] **Decided (Jan, 2026-10-26):** pepperoni, ham, chicken, bacon and gold become rare seeds on the slot machine. Asked Manuel's Claude in [[Notes for other Claudes]] + PART 1 (the slot machine is theirs). Open: Manuel's Claude adds them to `Config.Slot.Items`.
- [ ] **Manu + Basti:** the real 3D models (oven, beds, plate, hopper wall, carry board); Sebastian also the general design + UI (Jan, 2026-10-26). Keep the part names the code needs (oven `Shelf`/`Spot1-4`/`Mouth`/`Chimney`, plate `Plate`, bed `Soil`).
- [ ] Unlock prices and the sizes are first guesses (`Config.Farm.UnlockPrice` 250 x `UnlockPriceMul` 1.35, `Config.Storage.Capacity` 40, `TakeAmount` 12, `Config.Carry.BackCapacity` 12, `Config.Oven.RingRadius` 9): Jan's numbers win.
- [x] **Team repo: clone (done, [[Roblox Changelog]] (19))** to `C:\Users\schmu\Documents\GitHub\ROBOLOX`. JanPrompting stays signed in on this PC (Changelog (18)).
- [ ] **Team repo: Obsidian Git plugin (set up with PowerShell, [[Roblox Changelog]] (21); Jan reloads Obsidian with Ctrl+R and says "reloaded"):** open `C:\Users\schmu\Documents\GitHub\ROBOLOX` as a vault, install and enable the Git plugin (Vinzent03), The commit identity is set in GitHub Desktop (File → Options → Author: JanPrompting, Jan's Gmail). The plugin runs commit-and-sync every 1 minute, with `.obsidian` excluded from automatic commits. Then Claude copies our notes into `Team/JAN/` and links them from `Team/JAN.md`.
- [ ] **The user's playtest** of the big update -> popups A-D in [[Playtest Questions]].
- [ ] **Real saving test:** the user turns on File > Experience Settings > Security > "Enable Studio Access to API Services" (their switch). Then Claude tests leave + join, offline earnings and the 3 boards with real DataStores.
- [ ] **Phone test:** Roblox's Device Simulator through the Studio MCP skill `rbx-device-simulator-lua`. Fix what doesn't fit.
- [ ] **Sign heights:** do the station signs and customer bubbles show above them (playtest question)? If not, flip `SIGN_ANCHOR` / `STATUS_ANCHOR` in `Server.Stations`.
- [x] **No more cutting** (done, [[Roblox Changelog]] (24)). Open: someone deletes the `cutting_board` + `dock_cut` models from `Workspace.StarterRestaurant` (asked in PART 1; not ours to edit while they work on it).
- [ ] **Phone check of the landmarks** (Device Simulator near the farm and the lobby: FPS ok with ~1,100 new parts?). Optional: nicer white flower patches.
- [x] **World landmarks** (done 2026-10-26, [[Roblox Changelog]] (25); the old plan below is kept for the record):
  - Put `WorldSpots` (disk: `src\ServerStorage\WorldTools\WorldSpots.luau`) into `ServerStorage.WorldTools`.
  - Then add a windmill on its hill, the farm (barn, silo, fields, hay bales), a bridge, a dock, 3 hot-air balloons, lamps, fences and flower patches.
  - The Creator Store search was poor: spam re-uploads, deleted accounts, fake "Roblox" names. Build the landmarks from parts in the game's own style, or with Roblox's generators. No random uploads.

## 2. Team
- [ ] Popup: who does what (images, models, UI, testing) + the weekend rhythm.
- [ ] The friends swap in ChatGPT images (`2_BILDER_PROMPTS` -> `Shared.UIAssets`) and real models (`ReplicatedStorage.PieceModels`).
- [ ] Multiplayer test with the friends in one server: everyone gets their own restaurant, and customers go to the right one.

## 3. Later
- [ ] Build mode extras: paint, floor / wall patterns, restaurant name sign (the rest of M3).
- [ ] M6: delivery area + delivery drone.
- [ ] [[Before Publish Checklist]], then the user presses Publish.
- [ ] Read the community plugin `roblox-dev` (the user's decision), write the Roblox Basics note, make the team decisions (group or user-owned, ages, task list).
- [ ] Before any Rojo / Git setup: remove the 3 old German TeamGuide files from `src\ServerStorage\TeamGuide\` (`1_LIES_MICH`, `2_BILDER_PROMPTS`, `3_CHANGELOG`), and `src\ServerScriptService\Server\Deliveries.luau` (gone from the game since (26)); needs a shell, so ask the user first.
- [x] A shared cloud doc outside Roblox: the team made one (2026-10-26, Changelog (15)); Jan's tab comes from `Jan Notepad.html`.
- [ ] Next time Studio is open: one line at the top of the notebook's PART 1 pointing to the team doc (Jan's tab = Jan + Claude), and "his" -> "Jan's" in the notebook (no guessed pronouns).
