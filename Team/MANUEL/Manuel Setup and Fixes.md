---
tags:
  - manuel
  - setup
updated: 2026-10-26
---

# Manuel Setup and Fixes

Part of [[Manuel Home]]. How Manuel's PC is set up, and problems that were fixed (so nobody has to search again).

## Setup (2026-10-26)
- Windows 10, Roblox Studio, 2-step verification on, joined the game with Team Create.
- **Claude ↔ Studio:** Roblox's MCP server is built into Studio ([docs](https://create.roblox.com/docs/studio/mcp)).
  - In Studio: Assistant > … > Manage MCP Servers > **Enable Studio as MCP server** = ON (green dot).
  - In Claude Code: `claude mcp add --scope user Roblox_Studio -- cmd.exe /c %LOCALAPPDATA%\Roblox\mcp.bat`, then reload VS Code. (Remove: `claude mcp remove Roblox_Studio -s user`.)
- **This vault:** cloned with GitHub Desktop to `Documents\GitHub\ROBOLOX`. Uploading changes: GitHub Desktop > **Push origin**.

## Fixes
- **Studio: "We could not open the place … Failed to fetch place info."** Roblox wasn't down and the PC was fine; Studio's login was stuck. Fix: click your name (top right) > **Log Out**, then log back in.
- **Obsidian Git: "Git is not ready".** Git for Windows isn't installed (GitHub Desktop only has its own hidden copy). Fix: install Git from **git-scm.com** (default options), then restart Obsidian.
- **Claude Code: "Settings file failed to parse".** `settings.json` had been wiped blank (a save got cut off). Restored from the backup file; the broken copy was kept.

## Studio basics (learned 2026-10-26)
- Camera: W/A/S/D move, E up, Q down, hold right mouse button to look, mouse wheel = zoom, Shift = slower.
- **Explorer** = everything in the game; **Workspace** = what you see in 3D; **Properties** = the details of what's selected.
- **Part** = a basic building block. Move tool = Ctrl+2. Play = F5, Stop = Shift+F5.

---

**Related:** [[Manuel Home]] · [[MANUEL]]
