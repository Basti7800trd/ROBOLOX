---
tags:
  - dashboard
updated: 2026-10-26
---

# Dashboard

> [!info] Updated automatically on every push · last update 26 Oct 2026, 18:20 (Vienna) · 76 changes so far
> Don't edit this note by hand — it gets overwritten. Change [[Todo]] instead.

## Kitchen status

**11%** done — 1 of 9 tasks served

`███░░░░░░░░░░░░░░░░░░░░░░░░░░░`

Open **7** · In the oven **0** · Blocked **1** · Served **1**

## Order rail

### ⛔ Blocked (1)

- ⚠️ **Starter restaurant is empty (2026-10-26, between 18:07 and ~18:10):** `Workspace.StarterRestaurant` only holds `SlotMachinePreview` + `FarmPreview`; walls, floors, big oven, tables, farm beds, harvest table are gone, 5 loose `floor_kitchen` models lie directly in Workspace. New players get an EMPTY restaurant until it's back — don't publish. Not written down by anyone; Sebastian's Claude did not delete it. Working near it then: Manuel's Claude (farm upgrades), Jan's Claude (pizza counter / harvest table rings), Laser_Gaming0214. Whoever did it: check your undo history. Otherwise restore via Studio **File → Version History** (a version from before 18:07). Details in the team notebook (PART 1) — [[JAN]], [[MANUEL]], [[SEBASTIAN]]

### 📝 Open (7)

- Tell Jan what changed in `Server.Farm` (signposts facing the middle path, 3 × 3 crop fields, demo hook) and in `builders.farm_bed`, see — [[SEBASTIAN]]
- Check the farm still fits the extended restaurant (first row of fields + its path right behind the building) — [[SEBASTIAN]]
- Decide with Jan: should the oven take crops from the harvest table, and should the drone jobs use the new crop drone? — [[SEBASTIAN]]
- Decide: is the fridge/freezer spoilage still used with the new harvest-basket loop? — [[SEBASTIAN]]
- Find free sounds for rain and thunder (`Sounds.ids.weather_rain`, `thunder`) — [[SEBASTIAN]]
- Before publishing: move or hide the test plot's yellow highlight (plot 1, TestBuildPizzaHut) — [[SEBASTIAN]]
- Let players buy better weather chances with Robux (see) — [[SEBASTIAN]], [[SEBASTIAN]]

### ✅ Served (1)

- ~~Move the team notebook from Claude Docs to this vault~~ — [[SEBASTIAN]]

## Kitchen crew

| | Tasks served | In the oven | Blocked | Own checklist |
| --- | --- | --- | --- | --- |
| [[JAN]] | 0 / 1 | 0 | 1 | — |
| [[MANUEL]] | 0 / 1 | 0 | 1 | — |
| [[SEBASTIAN]] | 1 / 9 | 0 | 1 | `░░░░░░░░░░` 0/16 |

## Employee of the month

*Extremely scientific.*

| | Who | Title | Points | Tasks | Boxes | Commits | Lines |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 🥇 | **Jan** | Head pizzaiolo | **334** | 0 | 0 | 22 | 1471 |
| 🥈 | **Manuel** | Sous-chef | **310** | 0 | 0 | 27 | 642 |
| 🥉 | **Sebastian** | Dishwasher | **207** | 1 | 0 | 12 | 4104 |
| 4 | **Claude** | Delivery drone | **11** | 0 | 0 | 1 | 12 |

> [!quote] Night oven: Sebastian
> most commits between 23:00 and 05:00

> [!quote] Keyboard smasher: Sebastian
> most lines changed (capped in points, sorry)

> [!quote] Poet laureate: Sebastian
> commit message: “I made shit”

> [!note]- How points work
> Finished task in [[Todo]] **50** · ticked box on your own page **15** · commit **10** + 1 per 10 lines changed (max 20 per commit, so spamming “AYOOOO” doesn't win). Settings files and this note don't count.

## Order log

| When | Who | What | Lines |
| --- | --- | --- | ---: |
| 26 Oct 18:20 | Sebastian | Todo: starter restaurant is empty (who/when/how to restore) | +1 −0 |
| 26 Oct 18:15 | Manuel | Manuel Changelog: farm upgrades (4 beds, sign, 2nd floor) | +16 −0 |
| 26 Oct 18:04 | Jan | vault backup: 2026-10-26 17:04:48 | +13 −1 |
| 26 Oct 18:01 | Jan | vault backup: 2026-10-26 17:01:33 | +8 −0 |
| 26 Oct 17:52 | Jan | vault backup: 2026-10-26 16:52:55 | +15 −0 |
| 26 Oct 17:45 | Manuel | Manuel: 32 seed pictures in the game (changelog + checklist) | +7 −0 |
| 26 Oct 17:45 | Manuel | vault backup: 2026-10-26 17:45:03 | +32 −32 |
| 26 Oct 17:20 | Manuel | Manuel Changelog: slot results appear together | +6 −0 |
| 26 Oct 17:15 | Manuel | Manuel Changelog: slot machine double size, no odds board | +6 −0 |
| 26 Oct 17:06 | Sebastian | Sebastian Changelog + Game overview/Todo: weather, farm, harvest table, crop drone, sign, bigger plots | +119 −3 |
| 26 Oct 16:47 | Manuel | Manuel Changelog: slot machine back to full size, shorter lever | +7 −0 |
| 26 Oct 16:40 | Manuel | Manuel Changelog: slot machine smaller | +6 −0 |
| 26 Oct 16:27 | Manuel | Manuel Changelog: slot machine visible in Edit mode | +8 −0 |
| 26 Oct 16:27 | Jan | vault backup: 2026-10-26 15:27:32 | +46 −12 |
| 26 Oct 16:16 | Manuel | vault backup: 2026-10-26 16:16:20 | +7 −0 |

---

**Related:** [[Home]] · [[Todo]] · [[Team]]
