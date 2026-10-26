---
aliases:
  - Safe use
  - Before running code
tags:
  - code
  - safety
updated: 2026-10-26
---

> [!danger] Read this before running any code

## Limits and safe use

Every generated script was run in Studio and compared part by part with the real world; the copies were deleted afterwards and the game was not changed.

| Check | Result |
| --- | --- |
| Lobby (Workspace > Map) | 604 of 604 objects, largest gap 0.001 studs |
| Landscape props (Landscape > Props) | 1,920 of 1,920 objects, largest gap 0.001 studs |
| Plot frames (Workspace > Plots) | 108 of 108 objects, largest gap 0.0004 studs |

**What the generated code keeps:** names, sizes, positions, turns, shapes, colors (rounded to whole RGB values), materials, see-through, collision settings, lights, the fountain's water spray, sign texts and fonts, attributes and tags.

**What it does not cover:**

- Trees, bushes and rocks are cloned from the free packs in ServerStorage (YasuTreePack, StylizedRocksPack). If a pack is deleted, those lines print a warning and are skipped.
- The leaderboards' rows and the plot owner names are filled in by scripts while the game runs (GlobalBoards, Plots), so the code only builds the empty boards and "Free plot" signs.
- The restaurants do not exist in Edit mode: Plots builds them from Config.StarterLayout or the player's save when someone joins.
- The Sky, DayNightCycle, menus, drones and the other game systems are not part of the map and are not in this vault.

**Running the code safely:**

- [ ] Edit mode only (stop Play first); things built while playing are thrown away.
- [ ] Save a copy of the place first (File > Save to File As…) or tell the team in PART 1 of the notebook (or in [[Todo]]).
- [ ] The lobby, props and plot scripts never overwrite: they build Map\_Rebuilt, Props\_Rebuilt or Plots\_Rebuilt next to the original. To swap, delete the old folder and rename the new one.
- [ ] WorldBuilder is different: it clears and rebuilds the whole terrain and replaces the title sign and waterfall. It does not touch Map, Plots or Props.

**Keeping this vault current:** the code is a snapshot of 26 Oct 2026. If someone moves or adds things in Studio, ask your Claude to regenerate the affected note from the game and replace it here, then note it in PART 1 of 0\_TEAM\_NOTEBOOK.

---

**Related:** [[Lobby code]] · [[Landscape code]] · [[Plots and restaurant code]]
