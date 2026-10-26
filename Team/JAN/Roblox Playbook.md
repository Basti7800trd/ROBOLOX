# Roblox Playbook

Part of [[Roblox Home]]. The Roblox layer of Claude's knowledge: how this team works, the weekend loop, recipes (how to do X on Roblox) and the log of lessons (newest first).
- How the USER works in every project is in the UEFN vault: `Claude + Codex/Claude Playbook.md` §1. Lessons about the user go there; Roblox lessons go here.
- **Update this note at the end of every request that taught something new.**

---

## 1. How we work (Roblox-specific)
- **Team:** the user + 2 friends, all new to Roblox Studio, mostly on weekends. The user designs, tests, decides and presses the final buttons; Claude writes all Luau.
- **The friends** may not use Claude. Everything for them must stand on its own: in **English** (the user, 2026-10-25: "always keep everything in english from now on"), with Studio's button names exactly as they appear on screen. Their shared places are the team notebook in the game (`ServerStorage.TeamGuide.0_TEAM_NOTEBOOK`) and, since 2026-10-26, the team's Claude Doc (one tab each; Jan's tab comes from `D:\HAVIL\-Roblox\Jan Notepad.html`).
- **Facts:** every Roblox fact gets checked on create.roblox.com / the DevForum first and is marked ✔ with the date in the notes.
- **Buttons that are ALWAYS the user's on Roblox:** Publish to Roblox, making the experience public, anything with Robux (groups cost Robux), Creator Hub forms (maturity questionnaire, monetization, payouts), collaboration and group invites, posts.

## 2. The weekend loop (proposal, to be confirmed with the user)
1. **Saturday start:** paste the [[Session Handover]] box -> pick ONE weekend goal (popup).
2. **Build:** Claude scripts through the Studio MCP; the friends build and design in Team Create.
3. **Sunday:** team playtest -> prewritten [[Playtest Questions]] in popups -> notes (changelog, playbook, checklists) -> refresh the handover box.
4. **Between weekends:** nothing unless the user asks.

---

## 3. Recipes

### 3.1 Installing Roblox Studio on Windows (✔ 2026-10-25)
- **Official steps** ([Install Studio](https://create.roblox.com/docs/studio/setup)): download the installer (from the site it's `RobloxStudio.exe`), run it, click **Launch Studio**, sign in with the Roblox account.
- **Minimum:** Windows 10, 3 GB RAM, 1600x900. **Recommended:** Windows 11, 8 GB RAM.
- **Is it really installed?** A "Roblox Studio" desktop icon can point to `%LOCALAPPDATA%\Roblox\Versions\RobloxStudioInstaller.exe` (installer/launcher) while Studio itself is missing.
  - Installed = a `version-*` folder under `%LOCALAPPDATA%\Roblox\Versions\` with `RobloxStudioBeta.exe` in it.
  - The Roblox player sits in the same Versions folder (`RobloxPlayerBeta.exe`); don't confuse the two.
  - After the install, `%LOCALAPPDATA%\Roblox\mcp.bat` (the Studio MCP server's starter) should exist.

### 3.2 Connecting Claude Code to Studio with Roblox's official plugin (✔ 2026-10-25)
- **The plugin:** `roblox-studio` (display name "Roblox Studio", author **Roblox**, v0.2.2, MIT) from https://github.com/Roblox/roblox-studio-agent-plugin.
  - It holds no code: 2 MCP entries + the setup skill `roblox-get-started`.
  - `windows` entry: `cmd.exe /c "cd /d %LOCALAPPDATA%\Roblox && .\mcp.bat"`. `macos` entry: Studio's `StudioMCP` binary.
  - Roblox's own know-how comes from Studio's MCP `skill` tool, not from the plugin.
- **Which place for the first connection/tests:** a fresh **Baseplate** from Studio's start page, not an existing or published experience (the user asked 2026-10-25 "should i open the experience"). MCP clients can change whatever place is open, and a Baseplate isn't linked to anything online.
- **Studio side:** open a place -> **Assistant** (button on the right side of Studio's top "mezzanine" bar) -> `…` -> **Settings** -> **MCP Servers** -> turn on **Enable Studio as MCP server**.
  - Older Studio versions: `…` -> **Manage MCP Servers**.
  - **As seen in the real UI (2026-10-25, Changelog (3)):** the Assistant is the icon right of **Collaborate** and the Share icon (tooltip "AI Assistant"). Its panel docks bottom right ("New chat", `…`). The `…` menu = Settings + Usage. **Settings** opens a separate window "Assistant Settings" with Usage / API Keys / MCP Servers / **Skills**. The MCP Servers page: the toggle, "No clients connected" / green dot, **Quick connect** (ChatGPT (codex), Claude Code CLI, Visual Studio Code): leave those OFF when the plugin is used. Don't touch API Keys.
  - A green dot shows how many clients are connected.
  - The switch is **per Roblox account**: switch accounts = turn it on again.
- **Claude side, the trap (2026-10-25):** "/plugin -> search Roblox Studio" does NOT give Roblox's plugin on this PC.
  - Claude's plugin directory (cache refreshed 2026-10-25 16:45 UTC) lists only the COMMUNITY plugin `roblox-dev` (github.com/ivar-anon/roblox-dev, review state "none").
  - A different community plugin is ALSO named `roblox-studio` (ShiroKSH/skills, installed as `roblox-studio@skills`).
  - Never install those without reading them + the user's yes. Always check the AUTHOR (Roblox) and the repo.
  - Roblox's repo has no Claude marketplace file (`.claude-plugin/marketplace.json` = 404; `.agents/plugins/marketplace.json` is the Codex format).
- **The clean route: a pointer marketplace** at `D:\HAVIL\-Roblox\tools\roblox-github-marketplace\.claude-plugin\marketplace.json`.
  - It lists one plugin, `roblox-studio`, sourced straight from GitHub `Roblox/roblox-studio-agent-plugin`. Marketplace name: `roblox-github`. `claude plugin validate` passed.
  - Install in the Claude chat: `/plugin marketplace add D:\HAVIL\-Roblox\tools\roblox-github-marketplace`, then `/plugin install roblox-studio@roblox-github`.
  - Same from a terminal: the bundled CLI `C:\Users\schmu\.vscode\extensions\anthropic.claude-code-<version>-win32-x64\resources\native-binary\claude.exe plugin marketplace add ...` / `plugin install ...` (the `claude` command itself is not on PATH).
- **Done on this PC 2026-10-25 ([[Roblox Changelog]] (2))** with `--scope project` on both commands, run in `D:\HAVIL\-Roblox`: the settings live in `D:\HAVIL\-Roblox\.claude\settings.json`, the plugin copy in `C:\Users\schmu\.claude\plugins\cache\roblox-github\roblox-studio\0.2.2\`. Update later with `claude plugin update roblox-studio@roblox-github` (restart needed).
- **Check:** `/mcp` lists `plugin:roblox-studio:windows` (connected) and `plugin:roblox-studio:macos` (failed = normal on Windows). Tools load when a session starts: after installing, `/mcp` -> reconnect, or start a new session. Then `list_roblox_studios` must list the open place.
- **Don't ALSO** use Studio's "Quick connect -> Claude Code" or `claude mcp add` for Studio: that registers the server twice (duplicate tools). Fix duplicates with `claude mcp list` and remove the non-plugin entry (with the user's OK).
- **Troubleshooting** (the plugin's own `skills/roblox-get-started/references/troubleshoot.md`):
  - tools there but `list_roblox_studios` empty / "Unable to reach Roblox Studio" = Studio closed, no place open, or the switch is off
  - no `mcp.bat` = Studio not installed or too old -> update Studio
  - fails right after turning it on = another app uses port 13469
  - several Studios open = pick the place by `studio_id`
  - a documented tool missing = the tool set depends on the Studio version and feature flags
- **Rules from the plugin's skill:** never ask for or handle the Roblox password; never close Studio (ask the user, unsaved work); don't edit Studio's settings files.
- **Safety (docs):** "MCP clients can read and modify content in your open Roblox places." Save the place before big changes; not every change can be undone in Studio.

### 3.3 The Studio MCP tools (✔ 2026-10-25, [Studio MCP docs](https://create.roblox.com/docs/studio/mcp))
Every call takes a `studio_id` (from `list_roblox_studios`). The server is a local process on stdio. On this PC (Studio `version-7aaa6838d36c4448`, 2026-10-25) it reports "RobloxStudio 1.0.0", MCP protocol 2025-06-18, and **28 tools**: the docs' 26 below plus `segment_mesh` and `generate_texture`.
- **Scripts:** `script_read`, `multi_edit` (creates the script if missing; needs a `datamodel_type`), `script_search` (up to 10 results), `script_grep` (up to 50 matches).
- **World:** `search_game_tree`, `inspect_instance`, `execute_luau` (Edit, Client or Server context; needs a `datamodel_type`).
- **Play:** `get_studio_state`, `start_stop_play`, `get_console_output`, `screen_capture` (the viewport, optional camera position), `character_navigation`, `user_keyboard_input`, `user_mouse_input`, `subagent` (an `explore` or `playtest` helper).
- **Assets:** `search_asset`, `insert_asset`, `upload_image`, `store_image`, `generate_mesh`, `generate_material`, `generate_procedural_model`, `wait_job_finished`. Uploads and AI generation touch the user's account, moderation and limits: ask first.
- **Knowledge:** `skill` (Roblox's reference skills: debugging, device simulation, docs search, ...), `http_get` (allowed Roblox docs URLs, with keyword search).
- **Open question:** do `user_keyboard_input` / `user_mouse_input` drive only Studio's playtest, or the real mouse and keyboard? Ask the user before the first use (rule: ask before taking the screen).

### 3.4 Driving Studio on the user's screen with PowerShell (2026-10-25, Changelog (3))
- **Only with the user's yes** (a popup, or their own explicit request like "can you take screen access using powershell"). Say "hands off" before starting, and "screen done" after.
- **Helper:** `D:\HAVIL\-Roblox\ClaudeArchive\session-2026-10-25\studio-ui.ps1` (dot-source it). DPI-aware, physical pixels.
  - `Get-MainStudio` / `Get-StudioWindows` (title + rect), `Focus-Studio $h` (Alt tap + SetForegroundWindow; remembers the user's window the first time), `Shot x y w h name.png`, `Click x y`, `Keys`, `Restore-UserFocus`.
  - Every click/key first checks that Studio is the foreground window, or it aborts.
- **Monitors (2026-10-25):** main = DISPLAY1 at X 0..1920 (Studio + VS Code), left = DISPLAY2 at X -1920..0 (ChatGPT). 1080 high.
- **The user keeps using the PC meanwhile** (Discord was in front) and can move windows: Studio jumped from (157,46) 1296x930 to the left half (-7,0) 974x1039 in the middle of the job. So: `Focus-Studio` + re-read the window rect + a fresh screenshot before EVERY click; never reuse old coordinates.
- Separate dialogs are their own windows (e.g. "Assistant Settings" 736x519): click relative to that window's rect.
- End: close what you opened, `Restore-UserFocus`, tell the user.

### 3.5 Testing Studio's MCP server without Claude's plugin (2026-10-25)
- `D:\HAVIL\-Roblox\ClaudeArchive\session-2026-10-25\mcp-check.ps1`: starts `cmd.exe /c "cd /d %LOCALAPPDATA%\Roblox && .\mcp.bat"` (same as the plugin), sends JSON-RPC lines (initialize -> notifications/initialized -> tools/list -> tools/call list_roblox_studios), prints the answers, then closes stdin and stops the child processes.
- Good result: server name + 28 tool names + one Studio id. Empty studio list = no place open or the switch is off.
- The stderr WARN lines ("Allowed unauthenticated WebSocket request", "Connection reset without closing handshake" when the test ends) are harmless.
- Use it to tell "Studio side broken" from "Claude side not loaded" before asking the user to restart anything.
- **Calling one tool:** `mcp-call.ps1 -Tool <name> [-ArgsJson '<json>'] [-SchemaOnly]` (same folder). `"studio_id":"auto"` = the first Studio from `list_roblox_studios`, asked up to 10 times because a freshly started server needs about a second to find Studio. Example (read-only): `-Tool execute_luau -ArgsJson '{"studio_id":"auto","datamodel_type":"Edit","code":"return game.PlaceId"}'`.

### 3.6 Naming and publishing a new place (✔ 2026-10-25, [Publish experiences and places](https://create.roblox.com/docs/production/publishing/publish-experiences-and-places))
- **Is it on Roblox yet?** `game.PlaceId` / `game.GameId` = 0 means a local place that was never published; its tab name ("Place2") is only temporary.
- **The real name is set when publishing:** **File > Publish** -> **Game details** window: icon + thumbnail, **Name**, Genre (+ Subgenre), Description -> **Save**. Publishing is ALWAYS the user's button.
- A new game is only reachable by its creator (plus Edit-access users / fitting group roles) until it is made public, which is a separate step with the maturity questionnaire.
- **Rename later:** File > Experience Settings > Basic Info. Don't rename a live game often: players lose it under the old name.
- **Add a place to an existing game:** File > Publish As.

### 3.7 Building a game through the Studio MCP (2026-10-25, Changelog (6))
- **Scripts:** `multi_edit` with `className` + one edit `old_string = ""` creates a script at a dot path (`game.ServerScriptService.Server.Plots`); the parent folders must exist first (make them with `execute_luau`). Later edits = exact `old_string` replacements.
- **World building:** `execute_luau` in the `Edit` datamodel (map, folders, deleting things). Big builds: `task.wait()` between chunks.
- **Testing:** `start_stop_play` (allowed by the user), then `execute_luau` with `Client` (acts as the player: teleport, fire remotes, trigger prompts) or `Server` (instances are shared, but **module state is NOT**: requiring a ModuleScript from the MCP gives a fresh copy, so read state through instances/attributes, not modules). `get_console_output` for errors. `screen_capture` with a camera position works during play too (shows the HUD).
- **Triggering ProximityPrompts in a test:** `prompt:InputHoldBegin()` / `InputHoldEnd()` on the client works ONLY for the prompt Roblox currently shows. With the default Exclusivity (OnePerButton) that's the one in front of the camera, so put the character **facing** the station and the camera behind it (`CFrame.lookAt`) before triggering. Teleporting with the station's own CFrame leaves the character facing away and nothing triggers.
- **Customers:** `Players:CreateHumanoidModelFromDescription(desc, R15)` works in playtests (6 templates in ServerStorage, cloned per customer). Roblox's default R15 animation ids (idle 507766666, walk 507777826, sit 2506281703) play on server-side NPCs.

### 3.8 Big builds through the Studio MCP (2026-10-25, Changelog (11)-(12))
- **Whole scripts in one call:** `execute_luau` (Edit) can create a ModuleScript / Script / LocalScript and set `.Source` from a Luau long string `[=====[ ... ]=====]` (no escaping needed). Then compare `#script.Source` and the line count with the disk file. `multi_edit` is better for small changes: it fails when `old_string` doesn't match, which doubles as a "Studio = disk" check.
- **Module state in play tests:** a `require` from the MCP (or the Command Bar) gets a fresh copy of the module, not the game's. So the game itself makes test buttons: `Main` creates `ServerStorage.DevTools` BindableFunctions (only when `RunService:IsStudio()`), and the MCP calls `:Invoke(player)`.
- **Pressing UI buttons in a test:** `user_mouse_input` with `instance_path` (e.g. `LocalPlayer.PlayerGui.MainUI.SideMenu.RecipesButton.Button`) clicks inside the game. It does not take the user's screen.
- **Screenshots:** `screen_capture` does NOT show BillboardGuis (customer bubbles, station signs, drone icons): check those through their properties. SurfaceGuis only render when the real camera is near: teleport the character there first.
- **Terrain:** Roblox draws solid terrain 2 studs higher than its voxel data (full voxels up to y 0 show their surface at y 2); water is exact. A builder that wants a floor at y 0 writes the ground 2 studs lower.
- **Studio has no DataStore access by default:** the error text contains "Studio access to APIs is not allowed" (502). Saving code must treat that as "test mode" (memory profiles), not as a crash. Real saving tests need File > Experience Settings > Security > Enable Studio Access to API Services (the user's switch).
- **Helpers (subagents) on one game:** give them ONE contract file (`work\INTERFACES.md`: shared hooks, names, remotes) and a folder each; they write drafts to disk, I integrate one at a time and playtest after each. Session limit: they stop mid-work; resume them with SendMessage after the reset.
- **Creator Store assets:** free only; prefer Roblox, licensed partners (ProSoundEffects, APMOfficial) and verified creators; check every model for scripts before inserting it into the game; beware fake "Roblox" accounts with invisible characters in the name. Load-test sounds with `ContentProvider:PreloadAsync`.

---

## 4. Log of lessons (newest first)
- **2026-10-26 ([[Roblox Changelog]] (24)):**
  - **Another Claude may be editing the same place right now.** While I read the code, Manuel's Claude changed Config, Main, Plots, Recipes and ClientMain and added a new script (the slot machine). How to spot it: list every script's size, `task.wait(45)`, list again. How to stay out of the way: back up their new versions first, read a script right before changing it, and make every change to a shared script one atomic `multi_edit` (it fails instead of overwriting when the text moved). Never set `.Source` of a shared script.
  - **Copying Studio scripts to disk without retyping them:** a helper fetches each script in chunks of whole lines with `execute_luau` (raw text between start/end markers), then a PowerShell script pulls the chunks out of the session transcript and joins them with LF. A checksum computed the same way in Luau and PowerShell (`h = (h * 31 + byte) % 2147483647`) proves the copy is exact. 11 scripts take about 2 minutes this way.
  - **Removing a game step cleanly:** change the data first (Config: the ingredient field, the station piece, the drone task, the tutorial step, the quest template), then delete the code that only that data used, then search all scripts for leftovers (`cut`, the old names, removed locals). The save loader must accept the old data (old keys turned into new ones, unknown pieces and drone types skipped).
  - **A template can override Config.** A new `Workspace.StarterRestaurant` template (real models on Plot 1) builds the starter restaurant instead of `Config.StarterLayout`, so my counter from the Config list never showed up. When a playtest doesn't match Config, look for a template or a saved layout first.
- **2026-10-26 ([[Roblox Changelog]] (15)):**
  - **A Claude Doc from another organization is out of reach.** The Docs connector answered "access" to `read` and "no such artifact (Frame refused)" to a bind, although the Artifact tool listed the doc as shared with "writer". Edit access doesn't fix it. Check with one `read` first, then offer: a new doc in the user's own account, or a paste page (a local HTML page with a rich-text Copy button; the user pastes with Ctrl+A, Ctrl+V).
  - **A link with `#xxxxxxxx-xxxx` after the artifact id** points at a tab of a doc, so the doc already exists.
  - **Pasted content keeps its shape** when the Copy button writes `text/html` (headings, lists, tables); a fallback selects the text and uses the browser's copy.
- **2026-10-25 ([[Roblox Changelog]] (13)):**
  - **Closing Studio safely:** in Team Create, Studio saves to the cloud by itself every 4 minutes ([docs](https://create.roblox.com/docs/projects/collaboration)). Wait 5 minutes after the last change, then close.
  - **When the friends work between sessions:** they write in `ServerStorage.TeamGuide.3_CHANGELOG`, and the changelog lists every script's byte size. Back in a session: read their log first, compare the sizes, and copy their changes to disk before editing (the user's rule: "if theres a changelog always read that first when ur back").
  - **Creator Store search is full of spam:** for "windmill / barn / farm pack" most hits were re-uploads from random accounts, deleted accounts ("Content Deleted") and fake "Roblox" names with invisible characters. `verifiedCreatorsOnly: true` did NOT filter them out. For landmarks, build from parts in the game's style or use Roblox's own generators. Only take store models from creators you can check (Roblox, licensed partners, known packs like Yasu's).
- **2026-10-25 ([[Roblox Changelog]] (12)):**
  - **A new vault is invisible until Obsidian opens it once.** The Roblox Vault folder had notes for hours, but Obsidian's list (`%APPDATA%\obsidian\obsidian.json`) only knew the UEFN vault. Tell the user on day 1: Obsidian > vault name bottom left > Manage vaults > Open folder as vault.
  - **Rule drift after a context summary:** my first message after the summary lacked "Sir". Re-read every memory file + the Session Handover at once (the rule says so), then go on.
  - **Write the handover box BEFORE the long work:** a session limit or summary can come any time; a fresh box means nothing is lost.
  - **Check the tool, not the game:** BillboardGuis "missing" in screenshots was the capture tool, not a bug (3.8).
- **2026-10-25 ([[Roblox Changelog]] (11)):**
  - **Three skies fighting:** Lighting had 3 Sky objects and the screen showed a purple space sky. One Sky only; effects in Workspace do nothing (they belong in Lighting).
  - **Automation needs priorities:** the first ordering drone bought every ingredient and filled the garage, so the kitchen starved. Drones order only what unlocked recipes need, most urgent first.
- **2026-10-25 ([[Roblox Changelog]] (6)):**
  - **Test like a player:** my "prompts don't work" hunt took ~20 test runs. The game was fine; my test character faced away from the stations. Check the test method before changing game code (3.7).
  - **The user redesigns mid-build** (market -> PC + garage). Build in small modules with one Config, so a change touches 2-3 files, not everything.
  - **Style first:** the user wants the look of a reference game ("Automate a Restaurant"); a screenshot of their left monitor gave the palette and HUD layout in one look.
- **2026-10-25 ([[Roblox Changelog]] (5)):**
  - **The user wants the official MCP, not workarounds:** "use the mcp at all times unless i allow you to use powershell from now on". Recipes 3.4 (screen helper) and 3.5 (stdio bridge) are PARKED: only with the user's explicit OK. If the plugin's tools aren't loaded in the chat, ask for `/mcp` -> reconnect instead.
  - **Keep it short when they ask "how":** "dont make it so complicated just tell me how to do it quickly". They rejected a whole vault note for a friend message; 3 chat lines were enough.
  - **Write the plan into the vault BEFORE a possible chat restart** (here: the Beta Plan before the `/mcp` reconnect), so a fresh session loses nothing.
- **2026-10-25 ([[Roblox Changelog]] (3)):**
  - **Check the Studio side yourself before the restart:** a 10-second stdio test of `mcp.bat` (3.5) proved the server works, so the only thing left was Claude loading the plugin.
  - **The user moves windows while I drive:** re-measure and refocus before every click (3.4).
  - **Collaboration isn't blocked by starting user-owned:** user -> group ownership transfer exists ([[UEFN to Roblox]] §9).
- **2026-10-25 ([[Roblox Changelog]] (2)):**
  - **Install engine plugins with `--scope project`** (marketplace AND plugin), so only that folder's sessions load them. A user-scope Studio MCP would also start in every UEFN session and waste context there.
  - **A plugin installed mid-chat isn't loaded yet:** its MCP tools load when a session starts. After installing: `/mcp` -> reconnect, or a new session (resume the chat so nothing is lost; the [[Session Handover]] box must be fresh first).
  - **Read the installed copy, not just GitHub:** compare the file list with the repo tree and read SKILL.md + SECURITY.md before relying on it.
- **2026-10-25 ([[Roblox Changelog]] (1)):**
  - **"Studio is on my desktop" isn't the same as "installed".** The icon pointed to the installer. Check for `RobloxStudioBeta.exe` (3.1) before planning around Studio.
  - **A plugin search can hand you the wrong plugin.** Plugin names aren't unique (`roblox-studio` exists twice) and Claude's directory didn't list Roblox's own. Check the AUTHOR and the repo, or install from the repo through a pointer marketplace (3.2).
  - **Read the official plugin's own skill files** (`skills/roblox-get-started/SKILL.md` + `references/install.md`, `connect.md`, `troubleshoot.md` on GitHub): they are Roblox's exact setup and troubleshooting steps, and they agree with create.roblox.com.
  - **The friends already have a starter** from the UEFN session (`Roblox Friends Starter.md`): check what exists before writing something new.
