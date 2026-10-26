# Team Workflow

Part of [[Roblox Home]]. How the 3 of us work together. **Draft:** the parts marked "proposal" get decided with the user in the team popup ([[Setup Plan]] step 5). After that this note is the rulebook. The friends' own guide + shared log is in the game: `ServerStorage.TeamGuide` (`0_TEAM_NOTEBOOK`, `1_READ_ME`, `2_IMAGE_PROMPTS`, English).

## Who
- **The user (team lead):** design, decisions, testing, every final button. Claude (on the user's PC) writes all scripts.
- **Friend 1, Friend 2:** complete beginners; they may not use Claude, so their guides must stand on their own (English, since 2026-10-25). Names + jobs: to be filled in.
- **Proposal (brief §5):** friend 1 = building / map; friend 2 = UI, art and models (ChatGPT + Blender) + test lead; everyone tests.

## Weekend rhythm (proposal)
- **Saturday:** start from the [[Session Handover]] box -> ONE weekend goal -> build.
- **Sunday:** team playtest -> [[Playtest Questions]] in popups -> notes -> refresh the handover box.
- **Between weekends:** nothing unless the user asks.
- Checklist: [[Weekend Session Checklist]].

## Working in the same place (proposal; facts from the brief, re-check before the guide)
- **Collaborate** button: right side of Studio's top bar (✔ 2026-10-25). In a user-owned game only the owner's Roblox **friends** can get Edit access; in a group game, Edit comes from group roles. A user-owned game can be moved to a group later ([[UEFN to Roblox]] §9).
- Team Create saves the place to the cloud every 4 minutes (✔ 2026-10-25), with Script History per script and the place's Version History in Creator Hub.
- **Scripts:** only Claude (through the user's Studio) edits scripts, so live edits and Claude's work never overwrite each other. The friends don't touch scripts.
- Try new things in your own test place first.
- Name and group your work (Models and Folders in the Explorer).
- Never delete other people's work without asking.
- No free Toolbox models unless their scripts were checked (they can hide backdoors).
- No Robux spending unless all 3 agree.

## Accounts (proposal)
- 2-step verification on every account.
- Everyone friends with each other on Roblox.
- Roblox's **age check** (ID or facial age estimation) for all 3, the owner included, before working together; the ages must fit (table in [[UEFN to Roblox]] §8, ✔ 2026-10-25).

## Talking + tasks (open)
- A team channel on the user's Discord server.
- One simple task list: Discord forum posts, Trello or GitHub Projects (decided in the team popup).

## Already made for the friends (UEFN session, 2026-10-25)
`Claude + Codex/Roblox Friends Starter.md` in the UEFN vault: a 1,986-character text each friend pastes into their own Claude chat (free account works), so their Claude teaches them Studio step by step, in their own language. Its team rules match the ones above.

## The shared team notebook (2026-10-25, [[Roblox Changelog]] (14))
- In the game: `ServerStorage.TeamGuide.0_TEAM_NOTEBOOK`. Team Create saves it to the cloud, so all 3 (and Claude) read and write the same text.
- **PART 1 = what changed, newest on top.** Everyone adds 1-3 lines after each work session: `[YYYY-MM-DD] [name]: what changed + what isn't finished`.
- Claude reads PART 1 first after every pause.

## The team repo (2026-10-26, [[Roblox Changelog]] (16))
- **Combined storage = the GitHub repo** https://github.com/Basti7800trd/ROBOLOX (the team's Obsidian vault: JAN, MANUEL, SEBASTIAN; start note Home.md). It replaces the Claude Doc below, which Claude can't reach.
- Claude commits to it through the Obsidian Git plugin once the user has cloned it with GitHub Desktop (Changelog (17)). Pushes go out right away (the user's choice), following the repo's rules.
- Until then, the Jan notepad (`D:\HAVIL\-Roblox\Jan Notepad.html`) is the source text for the user's page.

## The old Claude Doc (superseded 2026-10-26, [[Roblox Changelog]] (15))
- A shared Claude Doc with one notepad tab per person: https://claude.ai/artifact/W8i2QUtJgt91kmZxpCCdWN. The friends write their changes in their own tabs.
- **The Jan tab** = everything Jan + Claude did, step by step (newest on top), plus everything from this vault. Claude keeps it in `D:\HAVIL\-Roblox\Jan Notepad.html`; after every change the user clicks **Copy everything**, opens the Jan tab, presses Ctrl+A, Ctrl+V.
- Claude can't open the doc (it was made in another Claude organization), so at the start of a session the user tells Claude what the friends wrote.
