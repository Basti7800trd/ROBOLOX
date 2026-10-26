# Session Handover

Part of [[Roblox Home]]. To start a fresh Claude Code session that knows everything without re-reading the whole history: open VS Code in `D:\HAVIL\-Roblox\` (that folder also loads Claude's memory files), open the Claude tab and paste the box below. Claude refreshes this note at the end of every session (last: 2026-10-26, after changelog (21)).

```
Continue my ROBLOX project: my first Roblox game, with 2 friends, all 3 new to Roblox Studio; we work mostly on weekends. Phase 1 = how we start and work together, not the game yet. Working folder: D:\HAVIL\-Roblox\ . My Roblox Obsidian vault is your long-term memory: C:\Users\schmu\Documents\GitHub\ROBOLOX\Team\JAN\ (since 2026-10-26; the old Roblox Vault is an archive)

Read now, nothing else:
0. FIRST: my friends work in Studio between our sessions. Read PART 1 of our shared team notebook in Studio (ServerStorage.TeamGuide.0_TEAM_NOTEBOOK, newest on top). Then compare every Studio script with the disk copy (sizes in Roblox Changelog (13) + (14)) and copy their changes to disk before you edit anything. Also ask me what my friends changed in the team repo, https://github.com/Basti7800trd/ROBOLOX. Claude commits there through the Obsidian Git plugin once you have cloned it (Changelog (17)). JanPrompting is Jan's own collaborator account (Changelog (18)).
1. Roblox Home.md (all notes sorted) and the newest entries at the TOP of Roblox Changelog.md.
2. 1 Plan and To-Dos\Next To-Dos.md = what's next, in order.
Look up only when needed: Roblox Playbook.md (recipes + lessons), Knowledge\UEFN to Roblox.md, 2 Team\Team Workflow.md. My UEFN vault (C:\Users\schmu\Documents\Obsidian Vault) is read-only, except Claude + Codex\Claude Playbook.md (lessons about how I work).

Rules (also in your memory files):
- CORE RULE: start EVERY message to me with "Sir". If a message doesn't, you've lost track of my rules - re-read them.
- ONE to-do at a time, or ask me with AskUserQuestion popups (recommended option first). Explain Roblox simply; compare with UEFN when it helps.
- Never buy anything or click Robux buttons. Never publish, post or send anything for me (no Publish to Roblox, no invites, no Creator Hub forms): I press the final buttons. Discord only when I ask.
- Ask (popup) before you take my screen. 2 monitors, ChatGPT on the left one. Give focus back afterwards.
- Trust my numbers. Everything child-friendly. Max plan, but no waste.
- Roblox changes fast: check facts on create.roblox.com / the DevForum before you tell me.
- Tell me IMMEDIATELY when a tool (the Studio MCP!) is down.
- Use the Studio MCP (plugin:roblox-studio:windows) at all times; PowerShell only when I allow it. If the MCP tools aren't loaded, tell me to reconnect in /mcp.
- Community plugins / skill packs only after you've read them and I said yes. Roblox's OFFICIAL plugin comes from Roblox's GitHub (Roblox Playbook 3.2), not the "roblox-dev" community plugin.
- Everything in English (guides for my friends, Studio text, names, notes).
- After every finished request: changelog entry (next number is (22)), playbook lessons, checklists, and a new step in my Jan notepad (D:\HAVIL\-Roblox\Jan Notepad.html, newest step on top). Refresh this box at the end of the session.
- Only you touch Studio. Helpers (subagents) research or write drafts to disk (D:\HAVIL\-Roblox\PizzaRestaurant\work\), never Studio / PowerShell / Bash.

State (2026-10-25): setup done (1)-(4). GAME (5): "Automate Your Pizza Restaurant" (published privately once; Team Create, friends added via Collaborate; nothing new is live until I press Publish). Built + tested by Claude (6)-(12): lobby with 3 global boards (top earners, pizzas per minute, fastest pizza this week), 6 plots, 64x64 pizzeria, kitchen loop (PC -> garage boxes -> fridge -> cut -> prep -> oven -> customers), build mode, 6 drones, saving (DataStore + session lock + offline earnings), stars + recipe ladder + special customers, tutorial (11 steps) + endless quests, new UI with 90 image slots (emoji until a ChatGPT image id is pasted into Shared.UIAssets), terrain landscape + day/night + sounds. All scripts on disk: D:\HAVIL\-Roblox\PizzaRestaurant\src\ (= Studio). Every script: 3 Game\...\Code Map.md. Not tested yet: real DataStore saving (needs File > Experience Settings > Security > Enable Studio Access to API Services), phones, several players, billboard heights. (13) PAUSED so my friends can work. (14) Everything English; shared team notebook = ServerStorage.TeamGuide.0_TEAM_NOTEBOOK (+ 1_READ_ME, 2_IMAGE_PROMPTS). (15) The shared Claude Doc lives in another Claude organization, so Claude can't reach it. (16) The team's combined storage is the GitHub repo https://github.com/Basti7800trd/ROBOLOX, the GitHub connector failed to sign in, so the plan is the Obsidian Git plugin (approved, Changelog (17)). Pushes go out right away (Jan's choice). JanPrompting is Jan's own GitHub account and a collaborator on the repo (Changelog (18)). Keep its sign-in on this PC. (19) The repo is cloned to C:\Users\schmu\Documents\GitHub\ROBOLOX. The Obsidian Git plugin is set up (interval 1 minute; `.obsidian` excluded from automatic commits; Changelog (21)). Jan reloads Obsidian with Ctrl+R, then our notes go into Team/JAN/. Next: 1 Plan and To-Dos\Next To-Dos.md (my playtest with popups, real saving test, phone test, world landmarks, team popup).
```

**For Claude, when refreshing:** keep the box short (it costs tokens in every new session). Update the next changelog number, the State paragraph and the date above; details belong in the [[Roblox Changelog]] and the [[Setup Plan]], not here.
