---
aliases:
  - Manuel
tags:
  - team
  - person
updated: 2026-10-26
role: menus and menu pictures
---

# MANUEL

Menus and menu pictures. My Claude (Claude Code in VS Code on my PC) works in Studio through Roblox's official Studio MCP and writes everything it changes here and in PART 1 of the team notebook (ServerStorage > TeamGuide > 0\_TEAM\_NOTEBOOK).

## My tasks

See **Backlinks** in the right sidebar, or [[Todo]].

- Pictures: swap the 90 emoji icons for ChatGPT images. Prompts: ServerStorage > TeamGuide > 2\_IMAGE\_PROMPTS. **Done: 1 / 90** (hud.recipes).
- Open question: one look for all pictures. My blue book is glossy with a dark-navy outline; the STYLE text in 2\_IMAGE\_PROMPTS says dark-brown outline.

## Rules I work with

- [[JAN]] said I may paste image IDs into `ReplicatedStorage > Shared > UIAssets`. Other script changes only when I ask for them, and each one gets a line in PART 1 so Jan's Claude can copy it into its backup.
- Pictures are always made by me in ChatGPT, never by Claude.
- Only Jan publishes; no Robux spending without the team.

## Log (newest on top)

### 2026-10-26: what changed in the game
All changes play-tested in Studio (0 errors) and written in PART 1 of the team notebook. Undo any of them: right-click the script > View Script History.

1. **Clickable drone upgrade boards** (`Server.Drones`): every dock has a board with 4 tiles you click in the world (ClickDetectors, mouse + touch): **Speed**, **Carry Amount**, **Battery Size** (for all drones) and **Drone Amount** (one more drone for that dock). Each tile shows now > next and the price (green = you can pay, brown = not yet, gold = MAX). Copied from the look of "Automate a Restaurant". The "Drones" prompt and panel still work.
2. **Customers wait for the tutorial** (`Server.Quests` + `Server.Customers`): no customers until the first pizza is baked; the first one comes ~3 s after "Bake the pizza". The "Make a pizza" hint now says "Make a Margherita at the prep table 🥖🥫🧀🍅". Players past the tutorial get customers as before.
3. **BUILD moved to the hotbar** (`StarterPack.Build` + `BuildClient`): a "Build" tool in slot 1. Key 1 / click = open build mode, again = close; X or opening another panel puts it away.
4. **Left buttons cut down** (`ClientMain`): OPEN/CLOSED, HOME, DRONES, STATS and BUILD are hidden (not deleted). Only **RECIPES** is left, centred on the left side.
5. **Always open** (`Server.Plots`): the restaurant opens by itself (no OPEN/CLOSED button any more); the tutorial step "Open the restaurant" finishes by itself.
6. **First picture**: the RECIPES button is my blue book (`rbxassetid://87000022272572` in UIAssets.HUD.recipes).

Heads-up for [[SEBASTIAN]]'s test list: the phone check "All 6 left buttons" is now just RECIPES + the Build tool in the hotbar.

### 2026-10-26: setup
- 2-step verification on, Roblox Studio installed, joined the game with Team Create.
- Claude connected to Studio with Roblox's built-in MCP server ([docs](https://create.roblox.com/docs/studio/mcp)).
- "Failed to fetch place info" in Studio → fixed by logging out and back in.
- Obsidian Git plugin says "Git is not ready": Git for Windows isn't installed (GitHub Desktop has its own hidden copy). Fix: install Git from git-scm.com.
