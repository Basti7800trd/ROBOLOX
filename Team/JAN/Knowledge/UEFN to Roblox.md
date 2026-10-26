# UEFN to Roblox

Part of [[Roblox Home]]. What the user knows from Fortnite UEFN -> what it's called and how it works on Roblox. Started as a copy of the Starter Brief §3 + §4 (written by the UEFN session, 2026-10-25), corrected here as we learn.
- ✔ = checked on create.roblox.com / the DevForum / Roblox's GitHub, with the date. Everything else is knowledge as of mid-2026: **check it before telling the user it's a fact.**
- Corrections go to the "Corrections" list at the bottom AND into the table row.

## The table
| UEFN (what the user knows) | Roblox |
|---|---|
| UEFN editor | **Roblox Studio** (free, Windows/Mac). Built-in AI **Assistant** (button on the right side of Studio's top bar ✔ 2026-10-25). |
| Island / project, island code | **Experience** (a "universe" with 1+ **places**). No codes; players find it through its page, link, search and recommendations. |
| Creator Portal | **Creator Hub** (create.roblox.com): Creations, the experience dashboard, analytics, monetization, and the questionnaire. |
| Verse | **Luau** (Roblox's Lua; optional types with `--!strict`). Three script types: **Script** (server), **LocalScript** (the player's device), **ModuleScript** (shared code, `require`). |
| Devices (button, trigger volume, HUD message, movement modulator, audio player, ...) | No devices: everything is **Instances** (Parts, Models, Folders, ...) plus scripts. Equivalents: **ProximityPrompt** = button; `Touched` / zone checks = volume; **Sound** = audio player; **Humanoid.WalkSpeed** = movement modulator; **BillboardGui / SurfaceGui** = text props and billboards; **TweenService** = moving props; **Lighting.ClockTime** = day/night. |
| `@editable` device fields | **Attributes** on instances (editable in the Properties panel) or a settings ModuleScript. |
| `weak_map(session, ...)` session globals | Plain tables inside a ModuleScript: one copy per server (server scripts) or per player device (LocalScripts). |
| Persistable save data | **DataStoreService** (per-player keys, limits/throttling). Use a proven library such as **ProfileStore** (session locking) from day 1. |
| Spawning props from Verse | `Clone()` models kept in ServerStorage / ReplicatedStorage. |
| UMG widgets / Verse UI | **ScreenGui** in StarterGui, designed in Studio and driven by LocalScripts. Size in **Scale** (%) so it fits phones. HUD-scale trouble -> UIScale / UIAspectRatioConstraint. |
| V-Bucks in-island offers | **Developer Products** (consumables; the server's `MarketplaceService.ProcessReceipt` must SAVE the purchase before it returns `PurchaseGranted`, and must handle the same receipt twice), **Game Passes** (permanent perks), Subscriptions, **Premium Payouts** (Robux for Premium players' playtime). |
| PaidRandomItem + odds text + RestrictPaidRandomItems | ✔ (brief, 2026-10-25) **Paid random items policy:** list EVERY outcome with numeric odds that sum to exactly 100 %, behind a button labelled "Info"/"Details" (a bare (i) isn't enough). It also covers items bought with a currency that was bought with Robux. Per-player rules via **PolicyService** (e.g. `IsPaidItemTradingAllowed` ✔, `ArePaidRandomItemsRestricted`). |
| IARC questionnaire / age ratings | **Maturity & Compliance Questionnaire** in Creator Hub -> content maturity label (Minimal / Mild / Moderate / Restricted). |
| Lore revision control, Check In | **Team Create** saves the place to the cloud every 4 minutes ✔ (brief), plus **Script History** per script ✔ (brief) and place **Version History** in Creator Hub. Real versioning: Git + Script Sync. |
| Launch Session / Push Changes | **Play** (F5), Play Here, Run. Test tab -> **Clients and Servers** = several players simulated on one PC. Collaborative testing with the team. Claude can start/stop a playtest itself through the Studio MCP (`start_stop_play` ✔ 2026-10-25). |
| Private version -> release -> Epic review | **Publish to Roblox** goes live at once for NEW servers. Updates have no review queue, but each uploaded image/mesh/audio is moderated. Old servers keep the old version until you **migrate/restart servers**. |
| Thumbnail pre-check, Discover | Icon + thumbnails in Creator Hub. Discovery = Roblox recommendations driven by engagement, retention and monetization. Thumbnail experiments exist (verify the current tool). |
| Epic IP flags | Roblox asset moderation + DMCA. Same rule: no famous look-alikes. |
| Claude skills / tools for the engine | ✔ 2026-10-25 **Roblox's OFFICIAL Claude plugin** `roblox-studio` ([Roblox/roblox-studio-agent-plugin](https://github.com/Roblox/roblox-studio-agent-plugin), made by Roblox). It holds only configuration + the setup skill `roblox-get-started` and starts Studio's built-in MCP server (`%LOCALAPPDATA%\Roblox\mcp.bat`); `/mcp` shows `plugin:roblox-studio:windows` (the macOS entry failing is normal). **Install correction:** it is NOT in Claude's plugin directory (only the community `roblox-dev` is) -> install from GitHub through a pointer marketplace ([[Roblox Playbook]] 3.2). Studio's **`skill` tool** serves Roblox's own reference skills. Community packs: read first, the user's yes first. |
| unreal-mcp + editor Python console | ✔ 2026-10-25 **Studio's built-in MCP server**: Assistant -> `…` -> Settings -> MCP Servers -> **Enable Studio as MCP server** (older Studio: `…` -> Manage MCP Servers). Green dot = connected clients. Per Roblox account. Tools: see [[Roblox Playbook]] 3.3 (`execute_luau` = the Python-console equivalent). Plus Studio's **Command Bar** (runs Luau) and plugins. |
| Verse files on disk that Claude edits | ✔ (brief) **Script Sync** (built into Studio): mirrors scripts to text files, both ways, with a conflict dialog; good for an external editor and Git. Or **Rojo** (third-party; the whole project as files). Also: the Studio MCP edits scripts directly (`script_read`, `multi_edit` ✔ 2026-10-25). |
| Devices replicate only within 150 m | **StreamingEnabled**: far-away parts aren't on the player's device. Scripts use `WaitForChild`; important models can be made persistent. |
| Text props hold 16 letters | TextLabels in BillboardGui / SurfaceGui: no letter limit. |
| Niagara VFX | ParticleEmitter, Beam, Trail (with Attachments). |
| Animated meshes / AnimSequences | Animator + Studio's Animation Editor. **Animations must be owned by the experience owner** (the group in a group game), or they don't play. |
| Music flagged by Epic | Roblox's licensed music library in the Creator Store. Own audio uploads have limits + moderation. |
| Blender -> FBX -> import pipeline | Studio **3D Importer** (FBX, OBJ; glTF in newer versions) -> MeshParts. Check the current triangle/texture limits. Roblox is **Y-up**; 1 stud ≈ 0.28 m. The Studio MCP can also generate meshes/materials (`generate_mesh`, `generate_material` ✔ 2026-10-25; ask first). |
| Fortnite's own HUD / ESC menu | Roblox CoreGui (player list, chat, menu) can be partly hidden with `StarterGui:SetCoreGuiEnabled`. |
| Analytics device + portal IDs | **AnalyticsService** (custom, economy and funnel events) + Creator Hub Analytics. |
| Leaderboard | `leaderstats` (built-in player list) + OrderedDataStore for global boards. |
| `before_upload.py` test switches | A Config ModuleScript + `RunService:IsStudio()` checks, so test buttons can NEVER run on live servers. |
| Event countdown from UTC epochs | The same idea: `os.time()` / `DateTime.now()` on the server. |
| Rejoin = same player object (the old speed bug) | On Roblox every join is a new Player object. Save on `PlayerRemoving` + `game:BindToClose`. |

## The big differences (brief §4; read before building anything)
1. **Players can cheat.** In Fortnite only the server runs Verse. On Roblox the player's device runs LocalScripts, and exploiters can change anything on their side. Money, purchases, damage, speed and egg rolls are decided and checked on the **server** only. RemoteEvents carry requests, never results.
2. **Saving can lose data** (DataStore limits, two servers writing the same player). Use ProfileStore (or whatever is current), save on leave + BindToClose, and turn on "Enable Studio Access to API Services" only for tests.
3. **Purchases:** ProcessReceipt grants and saves first, then confirms. Never trust the client to say "I bought it".
4. **Free models** from the Creator Store can hide backdoor scripts. Check every script inside, or use own / ChatGPT / Blender models.
5. **Asset ownership in team games:** animations (and some audio) must be uploaded by the group that owns the game.
6. **Mobile first:** big touch buttons, Scale sizes, and a phone test every weekend.
7. **Publishing is instant.** No Epic review, and no safety net either. Keep a separate test place and publish the real place only from a checked state.
8. ✔ 2026-10-25 ([Collaboration](https://create.roblox.com/docs/projects/collaboration)) **Collaboration rules:**
   - The **Collaborate** button is on the right side of Studio's top bar (opens Manage Collaborators). Team Create sessions also open from the Creator Dashboard ("Edit in Studio").
   - Working with other people needs an **age check** (verify your ID, or facial age estimation) by every collaborator AND the owner. Team Create alone needs none.
   - Compatible age groups by default: under 9 <-> under 13; 9-12 <-> under 16; 13-15 <-> 9-17; 16-17 <-> 13+; 18+ <-> 16+. Across groups: become trusted friends with every collaborator who already accessed the game, or get parental permission (an under-13 creator needs one of the two).
   - **User-owned** game: Edit access only for the owner's **Roblox friends** (Play access for anyone). **Group-owned**: Edit through group **roles** (the "Edit experiences" permission); single people can only get Play access there.
   - Live Scripting is on by default (scripts auto-save every 5 min, Ctrl+S saves, saves show in Script History). Drafts Mode is off by default (File > Experience Settings; everyone must leave the session for the change).
   - Inactive after more than 5 minutes without using Studio. Reverting is owner-only: turn collaboration off first, or auto-saves can overwrite the revert. Restored scripts land in the Workspace root.
   - Team Create autosaves to the cloud every 4 minutes.
9. ✔ 2026-10-25 ([Experience ownership transfer](https://create.roblox.com/docs/projects/experience-ownership-transfer), page updated 2026-06-15) **A user-owned experience can move to a group later:** Creations -> Configure -> Settings -> Initiate ownership transfer -> pick the group -> type the experience name -> Initiate transfer.
   - Needs: a verified email, publish rights in the target group, and private ModuleScripts / InsertService assets uploaded to the group first.
   - When the group accepts, the experience becomes private and all its servers close. Pending transfers can be cancelled.

## Corrections (newest first)
- **2026-10-25 (3):** collaboration rules re-checked on the docs (full age table, Drafts Mode off by default, reverting is owner-only). NEW: user -> group ownership transfer exists (§9), so starting user-owned is not a dead end. The Studio MCP offers 28 tools on this PC (2 more than the docs list).
- **2026-10-25:** the official plugin is not found by "/plugin -> search Roblox Studio" on this PC (Claude's directory lists only the community `roblox-dev`; a 2nd community plugin is also named `roblox-studio`). Install route: [[Roblox Playbook]] 3.2. The MCP switch moved from `…` -> Manage MCP Servers to `…` -> Settings -> MCP Servers in newer Studio.

Sources checked 2026-10-25: [Install Studio](https://create.roblox.com/docs/studio/setup), [Studio MCP server](https://create.roblox.com/docs/studio/mcp), [Assistant guide](https://create.roblox.com/docs/assistant/guide), [Roblox/roblox-studio-agent-plugin](https://github.com/Roblox/roblox-studio-agent-plugin) (README, plugin.json, skills/roblox-get-started). Brief sources: see the Starter Brief's list.
