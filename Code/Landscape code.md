---
tags:
  - code
  - landscape
  - terrain
updated: 2026-10-26
studio_path: "Workspace > Landscape"
objects: 1920
---

> [!warning] Before running
> WorldBuilder clears and rebuilds the whole terrain. Read [[Limits and safe use]].

## Landscape code (terrain, title sign, waterfall, props)

The landscape comes from two sources: the WorldBuilder script (terrain, lighting, title sign, waterfall) and 1,920 placed props (trees, bushes, rocks) that no script builds.

| Part of the landscape | Built by | How to rebuild |
| --- | --- | --- |
| Terrain: hills, lake, stream, pond, plateau, river, farm fields, mountains | WorldBuilder | `require(game.ServerStorage.WorldTools.WorldBuilder)()` in the Command Bar (Edit mode) |
| Lighting, atmosphere, clouds, wind, post effects (not the Sky) | WorldBuilder | same call; set APPLY\_LIGHTING = false to skip |
| Title sign and waterfall (Landscape > TitleSign, Waterfall) | WorldBuilder | same call; it only replaces children marked WorldBuilder = true |
| 370 trees and bushes + 70 rocks (Landscape > Props) | placed by hand from the free packs | the props code below (paste the [[Lobby code#Shared helpers (paste these first, also for the landscape and plot code)|shared helpers]] first) |

WorldBuilder mentions a WorldSpots.luau that lists spots for store assets. It is not in the game, so the props code below is the only record of where each prop stands.

### WorldBuilder (ServerStorage > WorldTools > WorldBuilder, 1073 lines)

```lua
--[[
	WorldBuilder  ·  "Automate Your Pizza Restaurant"
	=============================================================================
	Builds the world AROUND the lobby and the 6 plots and gives the place a warm,
	happy cartoon look. It makes:
	  * Terrain ground instead of the flat Baseplate (top exactly at y = 0)
	  * Rolling hills, terraced sandstone hills, a ring of snowy mountains
	  * A lake with a sandy beach, a stream with a pond, a plateau with a cliff
	    and a river on top that falls into the lake (the waterfall)
	  * A country path (dirt) from the lake to a flat farm yard with fields
	  * Lighting, Atmosphere, Clouds, wind and post effects (NOT the Sky: the
	    skybox is chosen separately)
	  * A big floating title sign "AUTOMATE YOUR PIZZA RESTAURANT"
	  * A simple waterfall made of a few parts (optional)

	Trees, rocks, bushes, flowers, fences, lamps, the windmill, the farm buildings,
	the bridge and the dock are NOT built here: WorldSpots.luau lists their spots
	so Creator Store assets can be placed there (same seed = same spots).

	HOW TO RUN (Roblox Studio, EDIT mode, not while playing): this is a ModuleScript in
	ServerStorage.WorldTools. Type this into the Command Bar (View > Command Bar) and press Enter:
	    require(game.ServerStorage.WorldTools.WorldBuilder)()
	It takes a few seconds. The Output window shows the progress and a summary at the end.

	SAFE TO RUN AGAIN: it clears the terrain and rebuilds it (same result every
	time). In Workspace.Landscape it only replaces what it made itself (children
	with the attribute WorldBuilder = true); your asset clones stay.

	It never touches Workspace.Map, Workspace.Plots, the SpawnLocation or the Sky.
	Everything inside radius 350 around the lobby stays flat at y = 0.

	UEFN comparison: like running a script that sculpts your whole landscape and
	sets the "Day Sequence" in one go.
]]

--------------------------------------------------------------------------------
-- SETTINGS (safe to change)
--------------------------------------------------------------------------------
local CONFIG = {
	CHUNK_STUDS = 64, -- terrain is written in 64 x 64 stud columns (multiple of 4)
	YIELD_EVERY = 0.06, -- seconds of work before Studio gets a frame to breathe

	APPLY_LIGHTING = true, -- Lighting, Atmosphere, Clouds, wind and post effects
	USE_DEPTH_OF_FIELD = true, -- a soft blur on the far mountains only

	BASEPLATE_MODE = "hide", -- "hide" (invisible + no collision), "delete" or "keep"

	BUILD_TITLE_SIGN = true,
	SIGN_POSITION = Vector3.new(0, 46, -112), -- floats behind and above the leaderboard (outside its 30-stud ring)
	SIGN_SIZE = Vector2.new(80, 24), -- width, height in studs
	SIGN_LOOK_AT = Vector3.new(0, 8, 26), -- the sign turns to face this point (the spawn)

	BUILD_SIMPLE_WATERFALL = true, -- a few parts; delete Landscape.Waterfall if you place a store waterfall

	LOCK_PARTS = true, -- WorldBuilder parts can't be clicked by accident in Studio
	ALLOW_IN_PLAY_MODE = false, -- things built while playing are thrown away when you stop
}

local Workspace = game:GetService("Workspace")
local Lighting = game:GetService("Lighting")
local RunService = game:GetService("RunService")
local Terrain = Workspace.Terrain

--------------------------------------------------------------------------------
-- >>> SHARED WORLD SHAPE >>>
-- Keep this block IDENTICAL in WorldBuilder.luau and WorldSpots.luau: it says where the
-- hills, the water, the paths and the farm are, so the terrain and the spots always match.
--------------------------------------------------------------------------------
local SHAPE_VERSION = "pizza-world-1"
local SEED = 20261025 -- change it (in BOTH files) for a different, but repeatable, landscape

local FLAT_RADIUS = 350 -- inside this radius the ground is flat at y = 0 (lobby, roads, plots)
local WORLD_RADIUS = 1100 -- size of the terrain disc
local BOTTOM_Y = -24 -- lowest terrain layer (multiple of 4)
local WATER_LEVEL = -1.5 -- water surface of the lake, the stream and the pond

local noise = math.noise
local sqrt, abs, floor, min, max = math.sqrt, math.abs, math.floor, math.min, math.max
local PI = math.pi

local function lerp(a, b, t)
	return a + (b - a) * t
end

-- 0 when x <= e0, 1 when x >= e1, a soft S-curve in between (also works when e0 > e1)
local function smoothstep(e0, e1, x)
	local t = (x - e0) / (e1 - e0)
	if t <= 0 then
		return 0
	elseif t >= 1 then
		return 1
	end
	return t * t * (3 - 2 * t)
end

-- A point on the ground from an angle (degrees) and a distance from the lobby centre.
-- Same angles as the plots: 0 = +Z, 90 = +X (Plot1 = 30, Plot2 = 90, Plot3 = 150 ...).
local function polar(deg, dist)
	local a = math.rad(deg)
	return dist * math.sin(a), dist * math.cos(a)
end

-- smallest difference between two angles in radians (-pi .. pi)
local function angleDiff(a, b)
	return (a - b + PI) % (2 * PI) - PI
end

local shapeRandom = Random.new(SEED)
local NOISE_X = shapeRandom:NextNumber(10, 90)
local NOISE_Z = shapeRandom:NextNumber(10, 90)

-- smooth layered noise, about -0.5 .. 0.5
local function fbm(x, z, salt)
	return noise(x + NOISE_X, z + NOISE_Z, salt) * 0.57
		+ noise(x * 2.03 + NOISE_X, z * 2.03 + NOISE_Z, salt + 3.7) * 0.29
		+ noise(x * 4.11 + NOISE_X, z * 4.11 + NOISE_Z, salt + 7.3) * 0.14
end

-- A line through {x, z} points (stream, river, country path). margin = the farthest distance we ask for.
local function makeLine(points, margin)
	local line = { points = points, segs = {}, minX = math.huge, maxX = -math.huge, minZ = math.huge, maxZ = -math.huge }
	for i = 1, #points - 1 do
		local a, b = points[i], points[i + 1]
		local dx, dz = b[1] - a[1], b[2] - a[2]
		table.insert(line.segs, {
			ax = a[1],
			az = a[2],
			dx = dx,
			dz = dz,
			len2 = dx * dx + dz * dz,
			minX = min(a[1], b[1]) - margin,
			maxX = max(a[1], b[1]) + margin,
			minZ = min(a[2], b[2]) - margin,
			maxZ = max(a[2], b[2]) + margin,
		})
		line.minX = min(line.minX, a[1] - margin, b[1] - margin)
		line.maxX = max(line.maxX, a[1] + margin, b[1] + margin)
		line.minZ = min(line.minZ, a[2] - margin, b[2] - margin)
		line.maxZ = max(line.maxZ, a[2] + margin, b[2] + margin)
	end
	return line
end

-- distance from (x, z) to the line; math.huge when it is farther away than the line's margin
local function lineDistance(line, x, z)
	if x < line.minX or x > line.maxX or z < line.minZ or z > line.maxZ then
		return math.huge
	end
	local best = math.huge
	for _, s in line.segs do
		if x >= s.minX and x <= s.maxX and z >= s.minZ and z <= s.maxZ then
			local t = ((x - s.ax) * s.dx + (z - s.az) * s.dz) / s.len2
			if t < 0 then
				t = 0
			elseif t > 1 then
				t = 1
			end
			local px, pz = s.ax + s.dx * t - x, s.az + s.dz * t - z
			local d = px * px + pz * pz
			if d < best then
				best = d
			end
		end
	end
	return sqrt(best)
end

---- THE LAYOUT (studs; lobby centre = 0, 0, 0) ----

-- Lake between Plot6 (330 deg) and Plot1 (30 deg), behind the spawn, visible from the plots.
local LAKE = { x = 0, z = 525, r = 82, bottom = -14 }

-- Small pond behind Plot1; a stream runs from it into the lake.
local POND = { r = 22, bottom = -6 }
POND.x, POND.z = polar(32, 430)
local STREAM_HALF = 6 -- half width of the stream water
local STREAM = makeLine({
	{ 61, 482 },
	{ 100, 460 },
	{ 128, 432 },
	{ 149, 419 },
	{ 172, 408 },
	{ 200, 384 },
	{ POND.x - 6, POND.z + 4 },
}, 22)

-- Bridge over the stream (the country path crosses here)
local BRIDGE_X, BRIDGE_Z = 149, 419
local BRIDGE_HALF = 17 -- half of the bridge length
local BRIDGE_DX, BRIDGE_DZ -- unit direction along the bridge (across the stream)
do
	local sx, sz = 172 - 128, 408 - 432 -- direction of the stream at the bridge
	local len = sqrt(sx * sx + sz * sz)
	BRIDGE_DX, BRIDGE_DZ = -sz / len, sx / len
end
local BRIDGE_A = { BRIDGE_X - BRIDGE_DX * BRIDGE_HALF, BRIDGE_Z - BRIDGE_DZ * BRIDGE_HALF } -- lobby side
local BRIDGE_B = { BRIDGE_X + BRIDGE_DX * BRIDGE_HALF, BRIDGE_Z + BRIDGE_DZ * BRIDGE_HALF } -- far side

-- Dock on the lake beach (the lobby side), pointing into the lake
local DOCK_X, DOCK_Z = 10, 432

-- Farm between Plot2 (90 deg) and Plot3 (150 deg). Farm coordinates: u = right, v = towards the lobby.
local FARM_H = 1.5 -- the farm yard is flattened to this height
local FARM_X, FARM_Z = polar(120, 560)
local FARM_CF = CFrame.lookAt(Vector3.new(FARM_X, FARM_H, FARM_Z), Vector3.new(0, FARM_H, 0))
local FARM_RIGHT, FARM_FWD = FARM_CF.RightVector, FARM_CF.LookVector
local function farmXZ(u, v)
	return FARM_X + FARM_RIGHT.X * u + FARM_FWD.X * v, FARM_Z + FARM_RIGHT.Z * u + FARM_FWD.Z * v
end
local FARM_GATE_SIDE -- +1 or -1: the side of the farm where the country path arrives
do
	local ax, az = polar(110, 600)
	FARM_GATE_SIDE = ((ax - FARM_X) * FARM_RIGHT.X + (az - FARM_Z) * FARM_RIGHT.Z) >= 0 and 1 or -1
end
local WHEAT_FIELD = { u = -32 * FARM_GATE_SIDE, v = 18, hu = 25, hv = 25 } -- centre + half sizes
local TOMATO_FIELD = { u = 28 * FARM_GATE_SIDE, v = 13, hu = 21, hv = 18 }
local FARM_YARD = { u = 0, v = -38, hu = 54, hv = 24 }
local FARM_GATE_X, FARM_GATE_Z = farmXZ(70 * FARM_GATE_SIDE, -9)

-- Windmill on a small hill next to the farm
local MILL_X, MILL_Z = polar(138, 690)
local MILL_HILL_R = 85

-- Plateau with a cliff behind the lake. A river on top falls into the lake at x = 0 (the waterfall).
local CLIFF_BASE_R = 598 -- distance of the cliff foot straight behind the lake
local CLIFF_WIDTH = 10 -- the cliff rises over this many studs
local PLATEAU_H = 44
local RIVER_WL = 41.5 -- water level of the river on the plateau
local RIVER_HALF = 6
local RIVER = makeLine({ { 0, 598 }, { 6, 640 }, { -7, 680 }, { 3, 715 }, { 0, 742 } }, 22)
local SPRING = { x = 0, z = 742, r = 15 } -- little lake where the river starts

-- Country path: dock -> bridge -> along the meadow -> over the hills -> farm gate
local PATH = makeLine({
	{ DOCK_X, DOCK_Z },
	{ 48, 424 },
	{ 95, 410 },
	BRIDGE_A,
	BRIDGE_B,
	{ 190, 452 },
	{ 250, 470 },
	{ 340, 480 },
	{ 430, 470 },
	{ 515, 405 },
	{ 588, 252 },
	{ 624, 84 },
	{ 612, -88 },
	{ 566, -196 },
	{ FARM_GATE_X, FARM_GATE_Z },
}, 8)

-- Terraced sandstone hills between Plot4 (210 deg) and Plot5 (270 deg)
local TERRACE_ANGLE = math.rad(240)

-- Big snowy mountains: { angle, distance, height, radius }
local PEAKS = {}
for _, p in { { 215, 930, 300, 300 }, { 150, 960, 250, 250 }, { 275, 980, 270, 260 }, { 35, 1010, 220, 240 }, { 95, 1000, 210, 230 } } do
	local px, pz = polar(p[1], p[2])
	table.insert(PEAKS, { x = px, z = pz, height = p[3], radius = p[4], r2 = p[4] * p[4], salt = p[1] * 0.013 })
end

---- ZONES (what the ground is made of) ----
local ZONE_NATURAL, ZONE_FLAT, ZONE_SAND, ZONE_PATH, ZONE_FIELD, ZONE_TERRACE, ZONE_VOID = 0, 1, 2, 3, 4, 5, 6
local ZONE_NAMES = { [0] = "natural", "flat", "sand", "path", "field", "terrace", "void" }

local function inRect(u, v, rect)
	return abs(u - rect.u) <= rect.hu and abs(v - rect.v) <= rect.hv
end

-- 1 = inside the open meadow between the lobby and the lake (no hills there, so the plots see the lake)
local function meadowAmount(r, absTheta)
	return (1 - smoothstep(0.55, 0.78, absTheta)) * (1 - smoothstep(600, 700, r))
end

-- THE HEIGHT MAP. Returns: ground height (studs), zone, water level (or nil when there is no water).
local function sampleGround(x, z)
	local r = sqrt(x * x + z * z)
	if r < FLAT_RADIUS then
		return 0, ZONE_FLAT, nil
	end
	if r > WORLD_RADIUS then
		return BOTTOM_Y - 8, ZONE_VOID, nil
	end
	local theta = math.atan2(x, z) -- 0 = +Z, pi / 2 = +X (same as the plot angles)
	local absTheta = abs(theta)
	local zone = ZONE_NATURAL
	local sandy = false
	local wl = nil

	-- 1. rolling hills, taller further out
	local hillAmp = 8 + 26 * smoothstep(380, 820, r)
	local base = hillAmp * math.clamp(0.5 + fbm(x / 240, z / 240, 1.3) * 1.35, 0, 1.2)
	base += 16 * smoothstep(520, 860, r) * (noise(x / 650 + NOISE_X, z / 650 + NOISE_Z, 9.1) + 0.6)
	base *= smoothstep(FLAT_RADIUS, FLAT_RADIUS + 90, r) -- no hills right next to the plots
	base *= 1 - 0.93 * meadowAmount(r, absTheta) -- open meadow towards the lake

	-- 2. terraced sandstone hills (steps with steep sides)
	local tDiff = abs(angleDiff(theta, TERRACE_ANGLE))
	if tDiff < 0.42 and r > 420 and r < 840 then
		local mask = (1 - smoothstep(0.28, 0.42, tDiff)) * smoothstep(420, 480, r) * (1 - smoothstep(780, 840, r))
		local tall = base * (1 + 0.8 * mask)
		local steps = tall / 11
		local whole = floor(steps)
		base = lerp(tall, (whole + smoothstep(0.7, 1, steps - whole)) * 11, mask)
		if mask > 0.5 then
			zone = ZONE_TERRACE
		end
	end

	-- 3. mountains: a ring around the map edge plus a few big peaks
	local mountain = 0
	if r > 830 then
		local ringT = smoothstep(830, 1010, r)
		local ridge = noise((z / r) * 2.5 + 17.3, (x / r) * 2.5 + 5.9, 0.71) + 0.5
		local rough = 1 - abs(noise(x / 140 + NOISE_X, z / 140 + NOISE_Z, 2.2)) * 2
		mountain = ringT * (85 + 120 * ridge + 45 * rough) * (1 - 0.3 * smoothstep(1040, 1100, r))
	end
	for _, peak in PEAKS do
		local dx, dz = x - peak.x, z - peak.z
		local d2 = dx * dx + dz * dz
		if d2 < peak.r2 then
			local t = 1 - sqrt(d2) / peak.radius
			local bump = peak.height * t ^ 1.7 * (0.88 + 0.3 * noise(x / 90 + peak.salt, z / 90 - peak.salt, 4.4))
			if bump > mountain then
				mountain = bump
			end
		end
	end
	base += mountain

	-- 4. flat farm yard
	local fdx, fdz = x - FARM_X, z - FARM_Z
	local farmDist = sqrt(fdx * fdx + fdz * fdz)
	if farmDist < 165 then
		base = lerp(base, FARM_H, 1 - smoothstep(110, 165, farmDist))
	end

	-- 5. flat shores around the lake, the stream and the pond
	local ldx, ldz = x - LAKE.x, z - LAKE.z
	local lakeDist = sqrt(ldx * ldx + ldz * ldz)
	local shoreR = LAKE.r
	if lakeDist < LAKE.r + 45 then
		local nx, nz = ldx / (lakeDist + 0.001), ldz / (lakeDist + 0.001)
		shoreR = LAKE.r + 10 * noise(nx * 1.4 + 3.1, nz * 1.4 + 8.7, 6.6) * (1 - 0.8 * max(0, nz))
		base = lerp(base, 0.5, 1 - smoothstep(shoreR + 8, shoreR + 30, lakeDist))
	end
	local streamDist = lineDistance(STREAM, x, z)
	if streamDist < STREAM_HALF + 14 then
		base = lerp(base, 0.4, 1 - smoothstep(STREAM_HALF + 3, STREAM_HALF + 14, streamDist))
	end
	local pdx, pdz = x - POND.x, z - POND.z
	local pondDist = sqrt(pdx * pdx + pdz * pdz)
	if pondDist < POND.r + 30 then
		base = lerp(base, 0.5, 1 - smoothstep(POND.r + 6, POND.r + 30, pondDist))
	end

	-- 6. plateau with a cliff behind the lake, and the windmill hill
	local h = base
	local plateau = 1 - smoothstep(0.62, 0.8, absTheta)
	local cliffR = math.huge
	if plateau > 0 then
		local q = absTheta / 0.66
		cliffR = CLIFF_BASE_R + 46 * q * q
		h += PLATEAU_H * smoothstep(cliffR, cliffR + CLIFF_WIDTH, r) * plateau
	end
	local mdx, mdz = x - MILL_X, z - MILL_Z
	local millD2 = mdx * mdx + mdz * mdz
	if millD2 < MILL_HILL_R * MILL_HILL_R then
		local t = 1 - millD2 / (MILL_HILL_R * MILL_HILL_R)
		h += 22 * t * t
	end

	-- 7. river and spring on the plateau (the river falls over the cliff = the waterfall)
	if plateau > 0.5 and r > cliffR then
		local riverDist = lineDistance(RIVER, x, z)
		local sdx, sdz = x - SPRING.x, z - SPRING.z
		local springDist = sqrt(sdx * sdx + sdz * sdz)
		local onTop = smoothstep(cliffR + 6, cliffR + 12, r)
		if riverDist < RIVER_HALF + 14 then
			h = lerp(h, PLATEAU_H + 0.6, (1 - smoothstep(RIVER_HALF + 4, RIVER_HALF + 14, riverDist)) * onTop)
		end
		if springDist < SPRING.r + 14 then
			h = lerp(h, PLATEAU_H + 0.6, 1 - smoothstep(SPRING.r + 4, SPRING.r + 14, springDist))
		end
		if riverDist < RIVER_HALF and r > cliffR + 4 then
			local q = riverDist / RIVER_HALF
			h = min(h, RIVER_WL - 3.5 + 6 * q * q) -- the river bed (also cuts a notch into the cliff edge)
		end
		if springDist < SPRING.r then
			local q = springDist / SPRING.r
			h = min(h, RIVER_WL - 4.5 + 6 * q * q)
		end
		if (riverDist < RIVER_HALF + 2 and r > cliffR + CLIFF_WIDTH) or springDist < SPRING.r + 2 then
			wl = RIVER_WL
		end
		if (riverDist < RIVER_HALF + 3 and r > cliffR + CLIFF_WIDTH) or springDist < SPRING.r + 4 then
			sandy = true
		end
	end

	-- 8. dig the lake, the stream and the pond
	if lakeDist < shoreR + 4 then
		h = lerp(h, LAKE.bottom, smoothstep(shoreR + 4, shoreR - 22, lakeDist))
	end
	if streamDist < STREAM_HALF + 2 then
		h = lerp(h, -4.5, smoothstep(STREAM_HALF + 2, STREAM_HALF - 3, streamDist))
	end
	if pondDist < POND.r + 3 then
		h = lerp(h, POND.bottom, smoothstep(POND.r + 3, POND.r - 12, pondDist))
	end
	if lakeDist < shoreR + 6 or streamDist < STREAM_HALF + 4 or pondDist < POND.r + 5 then
		wl = WATER_LEVEL
	end
	if lakeDist < shoreR + 14 or streamDist < STREAM_HALF + 3 or pondDist < POND.r + 8 then
		sandy = true
	end

	-- 9. farm fields + farm yard, and the country path
	if farmDist < 140 then
		local u = fdx * FARM_RIGHT.X + fdz * FARM_RIGHT.Z
		local v = fdx * FARM_FWD.X + fdz * FARM_FWD.Z
		if inRect(u, v, WHEAT_FIELD) or inRect(u, v, TOMATO_FIELD) then
			zone = ZONE_FIELD
		elseif inRect(u, v, FARM_YARD) then
			zone = ZONE_PATH
		end
	end
	if lineDistance(PATH, x, z) < 3.6 + 0.9 * noise(x / 16, z / 16, 8.8) then
		zone = ZONE_PATH
	end
	if sandy then
		zone = ZONE_SAND
	end

	-- 10. the edge of the world slopes down
	if r > WORLD_RADIUS - 24 then
		h = lerp(h, BOTTOM_Y - 4, smoothstep(WORLD_RADIUS - 24, WORLD_RADIUS, r))
	end
	return h, zone, wl
end
--------------------------------------------------------------------------------
-- <<< END OF SHARED WORLD SHAPE <<<
--------------------------------------------------------------------------------

local M = Enum.Material
local AIR = M.Air
local clock = os.clock
local _ = ZONE_NAMES -- (used by WorldSpots; kept here so both copies stay identical)

local function rgb(r, g, b)
	return Color3.fromRGB(r, g, b)
end

local notes = {} -- things the integrator should know (printed again at the end)
local function note(text)
	table.insert(notes, text)
	print("[WorldBuilder] " .. text)
end

local lastBreath = clock()
-- Gives Studio a frame now and then so it doesn't freeze during the long build.
local function breathe()
	if clock() - lastBreath > CONFIG.YIELD_EVERY then
		task.wait()
		lastBreath = clock()
	end
end

--------------------------------------------------------------------------------
-- TERRAIN MATERIALS
--------------------------------------------------------------------------------
-- Picks the material for the top of a column (surface) and for deeper down (deep, shows on cliff sides).
-- slope = how steep the ground is (1 = 45 degrees).
local function chooseMaterials(h, zone, slope, x, z)
	if zone == ZONE_FLAT then
		-- LeafyGrass has no animated grass blades, so no blades poke through the plots, roads and plaza
		return M.LeafyGrass, M.Ground
	elseif zone == ZONE_SAND then
		if slope > 1.4 then
			return M.Rock, M.Rock
		end
		return M.Sand, M.Sand
	elseif zone == ZONE_FIELD then
		return M.Ground, M.Ground
	elseif zone == ZONE_PATH then
		if slope > 1 then
			return M.Rock, M.Rock
		end
		return M.Ground, M.Ground
	end
	local cliff = (zone == ZONE_TERRACE) and M.Sandstone or M.Rock
	local wobble = noise(x / 55, z / 55, 5.5) * 36 -- snow line and rock line are not perfectly straight
	if h > 182 + wobble then
		if slope < 1.7 then
			return M.Snow, M.Rock
		end
		return M.Rock, M.Rock
	end
	if slope > 1 then
		return cliff, cliff
	end
	if h > 118 + wobble then
		return M.Rock, M.Rock
	end
	if slope > 0.7 and h > 30 then
		return cliff, cliff
	end
	if noise(x / 70, z / 70, 12.3) > 0.28 then
		return M.LeafyGrass, M.Ground -- darker patches for colour variety
	end
	return M.Grass, M.Ground
end

--------------------------------------------------------------------------------
-- TERRAIN WRITER
--------------------------------------------------------------------------------
-- Roblox draws SOLID terrain 2 studs higher than the voxel data says (measured in Studio on 2026-10-25:
-- full voxels up to y = 0 show their surface at y = 2). Water is drawn exactly where the data says.
-- So the ground is written 2 studs lower, and the surface you see matches the height map (lobby at y = 0).
local SOLID_RENDER_OFFSET = 2
-- Writes the height map into the terrain, one 64 x 64 stud column of voxels (4 x 4 x 4 studs) at a time.
local function buildTerrain()
	local started = clock()
	Terrain:Clear()

	local C = CONFIG.CHUNK_STUDS
	local NV = floor(C / 4) -- voxels per chunk side
	local W = NV + 2 -- columns per side including a 1-column border (used for the slopes)
	local colH = table.create(W * W, 0)
	local colZone = table.create(W * W, 0)
	local colWater = table.create(W * W, false)
	local surfMat = table.create(NV * NV, AIR)
	local deepMat = table.create(NV * NV, AIR)

	-- all chunks that touch the world disc
	local reach = WORLD_RADIUS + 8
	local first = -math.ceil(reach / C) * C
	local chunks = {}
	for cx = first, -first - C, C do
		for cz = first, -first - C, C do
			local nx = math.clamp(0, cx, cx + C)
			local nz = math.clamp(0, cz, cz + C)
			if nx * nx + nz * nz <= reach * reach then
				table.insert(chunks, { cx, cz })
			end
		end
	end

	local useChannels = true -- WriteVoxelChannels can hold sand AND water in one voxel (nicer shores)
	local written, voxelCount = 0, 0
	local nextReport = 0.1

	for index, chunk in chunks do
		local cx, cz = chunk[1], chunk[2]

		-- 1. sample the height map for every column (plus the border ring)
		local maxTop = -math.huge
		for i = 0, NV + 1 do
			local x = cx + (i - 0.5) * 4
			for k = 0, NV + 1 do
				local z = cz + (k - 0.5) * 4
				local h, zone, wl = sampleGround(x, z)
				local id = i * W + k + 1
				colH[id] = h
				colZone[id] = zone
				colWater[id] = wl or false
				if i >= 1 and i <= NV and k >= 1 and k <= NV then
					local top = (wl and wl > h) and wl or h
					if top > maxTop then
						maxTop = top
					end
				end
			end
		end

		if maxTop > BOTTOM_Y then
			-- 2. materials per column, using the slope towards the 4 neighbours
			for i = 1, NV do
				for k = 1, NV do
					local id = i * W + k + 1
					local h = colH[id]
					local slope = max(abs(h - colH[id - W]), abs(h - colH[id + W]), abs(h - colH[id - 1]), abs(h - colH[id + 1])) * 0.25
					local surf, deep = chooseMaterials(h, colZone[id], slope, cx + (i - 0.5) * 4, cz + (k - 0.5) * 4)
					local ci = (i - 1) * NV + k
					surfMat[ci] = surf
					deepMat[ci] = deep
				end
			end

			-- 3. fill the voxel arrays [x][y][z]
			local yTop = math.ceil((maxTop + 1) / 4) * 4
			local ny = floor((yTop - BOTTOM_Y) / 4 + 0.5)
			local mats, occs, liqs = table.create(NV), table.create(NV), table.create(NV)
			for i = 1, NV do
				local mX, oX, lX = table.create(ny), table.create(ny), table.create(ny)
				mats[i], occs[i], liqs[i] = mX, oX, lX
				for j = 1, ny do
					local yb = BOTTOM_Y + (j - 1) * 4 -- bottom of this voxel layer
					local mY, oY, lY = table.create(NV), table.create(NV), table.create(NV)
					mX[j], oX[j], lX[j] = mY, oY, lY
					for k = 1, NV do
						local id = i * W + k + 1
						local depth = colH[id] - SOLID_RENDER_OFFSET - yb -- how far the ground surface is above the bottom of this voxel
						local solid = depth * 0.25
						if solid >= 1 then
							solid = 1
						elseif solid < 0.004 then
							solid = 0
						end
						local mat = AIR
						if solid > 0 then
							local ci = (i - 1) * NV + k
							if depth <= 8 then
								mat = surfMat[ci]
							else
								mat = deepMat[ci]
							end
						end
						local liquid = 0
						local wl = colWater[id]
						if wl and solid < 1 then
							liquid = (wl - yb) * 0.25
							if liquid > 1 then
								liquid = 1
							end
							if liquid <= solid then
								liquid = 0 -- the water would be hidden inside the ground
							end
						end
						mY[k] = mat
						oY[k] = solid
						lY[k] = liquid
					end
				end
			end

			-- 4. write the chunk
			local region = Region3.new(Vector3.new(cx, BOTTOM_Y, cz), Vector3.new(cx + C, yTop, cz + C)):ExpandToGrid(4)
			if useChannels then
				local ok, err = pcall(function()
					Terrain:WriteVoxelChannels(region, 4, { SolidMaterial = mats, SolidOccupancy = occs, LiquidOccupancy = liqs })
				end)
				if not ok then
					useChannels = false
					note("WriteVoxelChannels failed (" .. tostring(err) .. "). Using WriteVoxels instead (water edges a bit blockier).")
				end
			end
			if not useChannels then
				-- classic format: one material per voxel, water is the material Water
				for i = 1, NV do
					for j = 1, ny do
						local mY, oY, lY = mats[i][j], occs[i][j], liqs[i][j]
						for k = 1, NV do
							if oY[k] <= 0 and lY[k] > 0 then
								mY[k] = M.Water
								oY[k] = lY[k]
							end
						end
					end
				end
				Terrain:WriteVoxels(region, 4, mats, occs)
			end
			written += 1
			voxelCount += NV * NV * ny
		end

		breathe()
		if index / #chunks >= nextReport then
			print(string.format("[WorldBuilder] Terrain %d%%", floor(index / #chunks * 100 + 0.5)))
			nextReport += 0.1
		end
	end
	return written, voxelCount, clock() - started
end

--------------------------------------------------------------------------------
-- WATER AND GROUND COLOURS
--------------------------------------------------------------------------------
local function setupTerrainLook()
	Terrain.WaterColor = rgb(38, 176, 206) -- bright cartoon turquoise
	Terrain.WaterTransparency = 0.55
	Terrain.WaterReflectance = 0.45
	Terrain.WaterWaveSize = 0.12
	Terrain.WaterWaveSpeed = 14
	local colors = {
		[M.Grass] = rgb(104, 186, 76),
		[M.LeafyGrass] = rgb(116, 188, 74),
		[M.Sand] = rgb(240, 216, 158),
		[M.Rock] = rgb(150, 140, 134),
		[M.Snow] = rgb(248, 251, 255),
		[M.Ground] = rgb(150, 108, 72),
		[M.Sandstone] = rgb(222, 166, 112),
	}
	for material, color in colors do
		Terrain:SetMaterialColor(material, color)
	end
	-- Animated grass (Terrain.Decoration) is "Not Scriptable" on create.roblox.com; we try anyway.
	local ok = pcall(function()
		Terrain.Decoration = true
	end)
	if not ok then
		note("Animated grass: scripts can't switch it on. In Studio select Workspace > Terrain and tick 'Decoration' in Properties (only the hills use Grass; the lobby ring uses LeafyGrass on purpose).")
	end
end

--------------------------------------------------------------------------------
-- LIGHTING, ATMOSPHERE, CLOUDS, POST EFFECTS (the Sky is NOT touched)
--------------------------------------------------------------------------------
local OUR_EFFECTS = { PizzaColor = true, PizzaBloom = true, PizzaSunRays = true, PizzaDepthOfField = true }

-- Finds the effect with this name in Lighting (reuses it) or makes it.
local function effect(className, name)
	local obj = Lighting:FindFirstChild(name)
	if obj and not obj:IsA(className) then
		note("Lighting." .. name .. " is a " .. obj.ClassName .. ", not a " .. className .. ". A new one was added next to it.")
		obj = nil
	end
	if not obj then
		obj = Instance.new(className)
		obj.Name = name
		obj.Parent = Lighting
	end
	return obj
end

local function setupLighting()
	-- Realistic = modern shadows and lights ("Soft" is the flat retro look). Technology itself is not scriptable.
	local okStyle = pcall(function()
		Lighting.LightingStyle = Enum.LightingStyle.Realistic
	end)
	if not okStyle then
		note("Could not set Lighting.LightingStyle; set it to Realistic in the Properties window if you like.")
	end
	Lighting.ClockTime = 14.25 -- sunny afternoon (DayNightCycle takes over while playing)
	Lighting.GeographicLatitude = 41.9 -- Rome
	Lighting.Brightness = 2.8
	Lighting.Ambient = rgb(112, 104, 124) -- indoors / shade (must stay below OutdoorAmbient)
	Lighting.OutdoorAmbient = rgb(152, 142, 160) -- bright, slightly lilac shadows = cartoon look
	Lighting.ColorShift_Top = rgb(255, 238, 210) -- warm sunlight
	Lighting.EnvironmentDiffuseScale = 0.75
	Lighting.EnvironmentSpecularScale = 0.35
	Lighting.ExposureCompensation = 0.1
	Lighting.ShadowSoftness = 0.35
	Lighting.GlobalShadows = true

	-- Atmosphere: soft blue haze that makes the far mountains look far away
	local atmospheres = {}
	for _, child in Lighting:GetChildren() do
		if child:IsA("Atmosphere") then
			table.insert(atmospheres, child)
		end
	end
	local atmosphere = atmospheres[1]
	if not atmosphere then
		atmosphere = Instance.new("Atmosphere")
		atmosphere.Name = "PizzaAtmosphere"
		atmosphere.Parent = Lighting
	end
	if #atmospheres > 1 then
		note("Lighting has " .. #atmospheres .. " Atmosphere objects; only one should exist. Set up: Lighting." .. atmosphere.Name .. ". Delete the others.")
	end
	atmosphere.Density = 0.3
	atmosphere.Offset = 0.18
	atmosphere.Color = rgb(199, 224, 255)
	atmosphere.Decay = rgb(120, 168, 232)
	atmosphere.Glare = 0.35
	atmosphere.Haze = 1.1

	-- Clouds only render when they are a child of Terrain
	local clouds = Terrain:FindFirstChildOfClass("Clouds")
	if not clouds then
		clouds = Instance.new("Clouds")
		clouds.Name = "PizzaClouds"
		clouds.Parent = Terrain
	end
	clouds.Enabled = true
	clouds.Cover = 0.55
	clouds.Density = 0.42
	clouds.Color = rgb(255, 255, 255)

	-- a gentle breeze: moves the clouds and the animated grass
	Workspace.GlobalWind = Vector3.new(6, 0, -3)

	-- post effects (PizzaColor and PizzaBloom already exist in the place: they are reused)
	local color = effect("ColorCorrectionEffect", "PizzaColor")
	color.Enabled = true
	color.Brightness = 0.02
	color.Contrast = 0.08
	color.Saturation = 0.15
	color.TintColor = rgb(255, 249, 240)

	local bloom = effect("BloomEffect", "PizzaBloom")
	bloom.Enabled = true
	bloom.Intensity = 0.55
	bloom.Size = 26
	bloom.Threshold = 1.25 -- only very bright things glow (neon lamps, sun glints)

	local rays = effect("SunRaysEffect", "PizzaSunRays")
	rays.Enabled = true
	rays.Intensity = 0.06
	rays.Spread = 0.6

	local depth = effect("DepthOfFieldEffect", "PizzaDepthOfField")
	depth.Enabled = CONFIG.USE_DEPTH_OF_FIELD
	depth.FarIntensity = 0.12
	depth.FocusDistance = 80
	depth.InFocusRadius = 400 -- sharp up to about 480 studs: only the far mountains get soft
	depth.NearIntensity = 0

	-- other effects of the same kinds would stack on top of ours: switch them off (not deleted)
	for _, child in Lighting:GetChildren() do
		local sameKind = child:IsA("ColorCorrectionEffect") or child:IsA("BloomEffect") or child:IsA("SunRaysEffect") or child:IsA("DepthOfFieldEffect")
		if sameKind and not OUR_EFFECTS[child.Name] and child.Enabled then
			child.Enabled = false
			note("Switched off Lighting." .. child.Name .. " (" .. child.ClassName .. "), it would stack with the Pizza effects.")
		end
	end
end

--------------------------------------------------------------------------------
-- BASEPLATE
--------------------------------------------------------------------------------
local function handleBaseplate()
	local plate = Workspace:FindFirstChild("Baseplate")
	if not plate or not plate:IsA("BasePart") then
		note("No Workspace.Baseplate found (nothing to hide).")
		return
	end
	if CONFIG.BASEPLATE_MODE == "delete" then
		plate:Destroy()
		note("Deleted Workspace.Baseplate (the terrain is the ground now).")
	elseif CONFIG.BASEPLATE_MODE == "hide" then
		-- remember the old look once, so it can be restored by hand (see README)
		if plate:GetAttribute("WB_OldTransparency") == nil then
			plate:SetAttribute("WB_OldTransparency", plate.Transparency)
			plate:SetAttribute("WB_OldCanCollide", plate.CanCollide)
		end
		plate.Transparency = 1
		plate.CanCollide = false
		plate.CanTouch = false
		plate.CanQuery = false
		plate.CastShadow = false
		-- textures and decals stay visible on an invisible part, so hide them too
		for _, d in plate:GetDescendants() do
			if d:IsA("Decal") then -- Texture is a kind of Decal
				d.Transparency = 1
			end
		end
		note("Workspace.Baseplate is now invisible and has no collision (the terrain is the ground).")
	end
end

--------------------------------------------------------------------------------
-- PARTS (only the title sign and the simple waterfall)
--------------------------------------------------------------------------------
local partCount = 0
local WHITE = rgb(255, 255, 255)
local SIGN_RED = rgb(206, 48, 42)

local function part(parent, shape, size, cf, color, material, transparency)
	local p = Instance.new("Part")
	if shape then
		p.Shape = shape -- set the shape before the size
	end
	p.Size = size
	p.CFrame = cf
	p.Color = color
	p.Material = material or M.SmoothPlastic
	p.Transparency = transparency or 0
	p.Anchored = true
	p.CanCollide = false -- decor: players walk through
	p.CanTouch = false
	p.CanQuery = false
	p.CastShadow = false
	p.Locked = CONFIG.LOCK_PARTS
	p.Parent = parent
	partCount += 1
	return p
end

-- A simple cartoon waterfall where the river falls off the cliff into the lake.
local function buildWaterfall(parent)
	local m = Instance.new("Model")
	m.Name = "Waterfall"
	m:SetAttribute("WorldBuilder", true)
	local sheetZ = CLIFF_BASE_R - 3 -- the falling water hangs just in front of the cliff
	local top = RIVER_WL + 0.3
	local bottom = WATER_LEVEL - 1
	local height = top - bottom
	local blue = rgb(140, 210, 255)
	local foam = rgb(245, 252, 255)
	local sheet = part(m, nil, Vector3.new(12, height, 1.2), CFrame.new(0, bottom + height / 2, sheetZ), blue, M.SmoothPlastic, 0.15)
	sheet.Name = "Sheet"
	-- white streaks on the falling water
	for i, x in { -4.2, -1.5, 1.4, 4 } do
		local len = height * (0.95 - i * 0.09)
		part(m, nil, Vector3.new(0.9, len, 0.3), CFrame.new(x, top - len / 2, sheetZ - 0.75), foam, M.SmoothPlastic, 0.25)
	end
	-- the water pouring over the edge of the cliff, with a round lip
	local lipZ = CLIFF_BASE_R + CLIFF_WIDTH + 2
	part(m, nil, Vector3.new(12, 1, lipZ - sheetZ), CFrame.new(0, RIVER_WL, (lipZ + sheetZ) / 2), blue, M.SmoothPlastic, 0.15)
	part(m, Enum.PartType.Cylinder, Vector3.new(12, 2.6, 2.6), CFrame.new(0, RIVER_WL - 0.3, sheetZ), blue, M.SmoothPlastic, 0.1)
	-- foam where it lands: { x, size, distance in front }
	for _, f in { { -5, 5.5, 1.5 }, { -1.5, 7, 3 }, { 2.5, 6, 1 }, { 5.5, 4.5, 2.5 }, { 0.5, 5, 0.5 } } do
		part(m, Enum.PartType.Ball, Vector3.new(f[2], f[2], f[2]), CFrame.new(f[1], WATER_LEVEL + 0.3, sheetZ - f[3]), foam, M.SmoothPlastic, 0.1)
	end
	-- a spot for a water sound (DayNightCycle plays Sounds.ids.ambience_water here if it is set)
	local spot = Instance.new("Attachment")
	spot.Name = "WaterSoundSpot"
	spot.Position = Vector3.new(0, -height / 2 + 2, -2)
	spot.Parent = sheet
	m.Parent = parent
	return m
end

-- One side of the title sign (SurfaceGui).
local function addTitleGui(board, face)
	local gui = Instance.new("SurfaceGui")
	gui.Name = "TitleGui" .. face.Name
	gui.Face = face
	gui.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
	gui.PixelsPerStud = 14
	gui.LightInfluence = 0 -- always bright, also at night
	gui.MaxDistance = 2000
	gui.Parent = board

	local bg = Instance.new("Frame")
	bg.Name = "Bg"
	bg.Size = UDim2.fromScale(1, 1)
	bg.BackgroundColor3 = SIGN_RED
	bg.BorderSizePixel = 0
	bg.Parent = gui

	-- white checkered trim at the top and the bottom, like a pizzeria table cloth
	local squares = 20
	for row = 0, 1 do
		for i = 0, squares - 1 do
			if (i + row) % 2 == 0 then
				local square = Instance.new("Frame")
				square.BorderSizePixel = 0
				square.BackgroundColor3 = WHITE
				square.Size = UDim2.fromScale(1 / squares, 0.075)
				square.Position = UDim2.fromScale(i / squares, row == 0 and 0 or 0.925)
				square.Parent = bg
			end
		end
	end

	local function line(name, text, posY, height, width, color, strokeColor, strokeThickness)
		local label = Instance.new("TextLabel")
		label.Name = name
		label.AnchorPoint = Vector2.new(0.5, 0)
		label.Position = UDim2.fromScale(0.5, posY)
		label.Size = UDim2.fromScale(width, height)
		label.BackgroundTransparency = 1
		label.Font = Enum.Font.FredokaOne
		label.Text = text
		label.TextScaled = true
		label.TextColor3 = color
		label.Parent = bg
		local stroke = Instance.new("UIStroke")
		stroke.ApplyStrokeMode = Enum.ApplyStrokeMode.Contextual -- outline around the letters
		stroke.Color = strokeColor
		stroke.Thickness = strokeThickness
		stroke.Parent = label
	end
	line("Line1", "AUTOMATE YOUR", 0.11, 0.28, 0.8, WHITE, rgb(110, 24, 20), 4)
	line("Line2", "PIZZA RESTAURANT", 0.4, 0.46, 0.94, rgb(255, 214, 72), rgb(92, 34, 14), 6)
end

-- A cartoon pizza (a disc that shows on both sides).
local function buildPizza(parent, cf, d)
	local facing = CFrame.Angles(0, PI / 2, 0) -- cylinders lie along X; this turns them to face front/back
	part(parent, Enum.PartType.Cylinder, Vector3.new(2.2, d, d), cf * facing, rgb(226, 166, 84)) -- crust
	part(parent, Enum.PartType.Cylinder, Vector3.new(2.4, d * 0.88, d * 0.88), cf * facing, rgb(204, 52, 36)) -- tomato sauce
	part(parent, Enum.PartType.Cylinder, Vector3.new(2.6, d * 0.8, d * 0.8), cf * facing, rgb(255, 214, 96)) -- cheese
	for i = 0, 5 do -- pepperoni
		local a = i * PI / 3 + 0.3
		local rr = d * ((i % 2 == 0) and 0.24 or 0.3)
		part(parent, Enum.PartType.Cylinder, Vector3.new(2.8, d * 0.15, d * 0.15), cf * CFrame.new(math.cos(a) * rr, math.sin(a) * rr, 0) * facing, rgb(178, 36, 30))
	end
	for i = 0, 2 do -- basil leaves
		local a = i * 2 * PI / 3 + 1.2
		local rr = d * 0.12
		part(parent, nil, Vector3.new(d * 0.08, d * 0.05, 2.9), cf * CFrame.new(math.cos(a) * rr, math.sin(a) * rr, 0) * CFrame.Angles(0, 0, a), rgb(60, 150, 60))
	end
end

-- The big floating title sign. It turns towards the spawn and floats high, so it blocks no path.
local function buildTitleSign(parent)
	local m = Instance.new("Model")
	m.Name = "TitleSign"
	m:SetAttribute("WorldBuilder", true)
	local cf = CFrame.lookAt(CONFIG.SIGN_POSITION, CONFIG.SIGN_LOOK_AT)
	local w, h = CONFIG.SIGN_SIZE.X, CONFIG.SIGN_SIZE.Y
	part(m, nil, Vector3.new(w + 3, h + 3, 1.2), cf, WHITE).Name = "Frame"
	local board = part(m, nil, Vector3.new(w, h, 2), cf, SIGN_RED)
	board.Name = "Board"
	addTitleGui(board, Enum.NormalId.Front)
	addTitleGui(board, Enum.NormalId.Back)
	-- a pizza "sticker" on the top-left corner
	local pizza = Instance.new("Model")
	pizza.Name = "Pizza"
	buildPizza(pizza, cf * CFrame.new(-w / 2 - 2, h / 2 + 1, 0), 18)
	pizza.Parent = m
	m.Parent = parent
	return m
end

--------------------------------------------------------------------------------
-- MAIN
--------------------------------------------------------------------------------
local function main()
	if RunService:IsRunning() and not CONFIG.ALLOW_IN_PLAY_MODE then
		warn("[WorldBuilder] Please stop the playtest and run this in Edit mode (things built while playing are thrown away).")
		return
	end
	local started = clock()
	print(string.format("[WorldBuilder] Building %s (seed %d). Studio may feel slow for a moment...", SHAPE_VERSION, SEED))

	-- our folder: only what WorldBuilder made earlier is removed (asset clones placed by you stay)
	local landscape = Workspace:FindFirstChild("Landscape")
	if not landscape then
		landscape = Instance.new("Folder")
		landscape.Name = "Landscape"
		landscape.Parent = Workspace
	end
	for _, child in landscape:GetChildren() do
		if child:GetAttribute("WorldBuilder") == true then
			child:Destroy()
		end
	end
	landscape:SetAttribute("BuildComplete", false)

	if CONFIG.APPLY_LIGHTING then
		setupLighting()
	end
	setupTerrainLook()
	handleBaseplate()

	local chunks, voxels, terrainSeconds = buildTerrain()
	Terrain:SetAttribute("WorldShapeVersion", SHAPE_VERSION .. ":" .. SEED) -- WorldSpots checks this

	if CONFIG.BUILD_SIMPLE_WATERFALL then
		buildWaterfall(landscape)
	end
	if CONFIG.BUILD_TITLE_SIGN then
		buildTitleSign(landscape)
	end

	local seconds = clock() - started
	landscape:SetAttribute("BuildComplete", true)
	landscape:SetAttribute("BuildSeconds", floor(seconds * 10 + 0.5) / 10)
	landscape:SetAttribute("WorldShapeVersion", SHAPE_VERSION .. ":" .. SEED)

	print("[WorldBuilder] ------------------------------------------------------------")
	print(string.format("[WorldBuilder] DONE in %.1f s (terrain %.1f s): %d terrain chunks, %d voxels, %d parts.", seconds, terrainSeconds, chunks, voxels, partCount))
	print("[WorldBuilder] Next: require WorldSpots and place Creator Store assets at its spots (see README).")
	for _, text in notes do
		print("[WorldBuilder] NOTE: " .. text)
	end
	print("[WorldBuilder] ------------------------------------------------------------")
end

-- require(...) gives this function; calling it builds the world.
return function()
	local ok, err = xpcall(main, debug.traceback)
	if not ok then
		warn("[WorldBuilder] FAILED: " .. tostring(err))
	end
	return ok
end
```

### Props (Workspace > Landscape > Props)

Generated from the game on 26 Oct 2026 and tested in Studio: it rebuilds all 1,920 objects. Trees and bushes are cloned from ServerStorage > YasuTreePack with their size and turn; rocks are cloned from ServerStorage > StylizedRocksPack, and each line lists only what differs from the pack rock. If a Props folder exists, the copy is built as Props\_Rebuilt.

```lua
local S = {}

V[0]=new("Folder",workspace:FindFirstChild("Landscape") or new("Folder",workspace,{Name="Landscape"}),{Name="Props"})
V[0].Name=workspace.Landscape:FindFirstChild("Props") and "Props_Rebuilt" or "Props"
pack("Tree_04",V[0],cf(759.9,34.055,-321.259,0,-120.562,0),0.793202,"Tree_04")
pack("Tree_02",V[0],cf(729.235,27.099,-115.714,0,108.507,0),0.811998,"Tree_02")
pack("Tree_06",V[0],cf(-644.509,17.258,-53.802,0,-46.503,0),0.648637,"Tree_06")
pack("Tree_08",V[0],cf(-833.011,37.076,-92.828,0,-174.273,0),0.542899,"Tree_08")
pack("Tree_06",V[0],cf(-648.589,8.702,91.229,0,95.991,0),0.513963,"Tree_06")
pack("Tree_09",V[0],cf(-88.918,27.283,-758.206,0,3.612,0),1.105338,"Tree_09")
pack("Tree_16",V[0],cf(-300.991,64.699,610.787,0,12.195,0),0.797291,"Tree_16")
pack("Tree_18",V[0],cf(845.238,37.089,52.341,0,-110.153,0),0.791133,"Tree_18")
pack("Tree_07",V[0],cf(569.877,22.243,601.677,0,166.401,0),0.55391,"Tree_07")
pack("Tree_14",V[0],cf(-262.625,64.866,679.844,0,-99.731,0),1.045206,"Tree_14")
pack("Tree_02",V[0],cf(-277.215,35.258,-799.968,0,132.748,0),0.834413,"Tree_02")
pack("Tree_19",V[0],cf(543.415,37.908,616.364,0,64.949,0),0.382537,"Tree_19")
pack("Tree_06",V[0],cf(-659.579,35.725,420.388,0,19.554,0),0.604336,"Tree_06")
pack("Tree_12",V[0],cf(315.776,14.064,-457.947,0,-58.029,0),1.055428,"Tree_12")
pack("Tree_07",V[0],cf(-447.027,76.39,697.687,0,-27.418,0),0.616122,"Tree_07")
pack("Tree_03",V[0],cf(598.924,23.896,118.596,0,31.231,0),1.121646,"Tree_03")
pack("Tree_05",V[0],cf(-468.691,8.838,54.973,0,18.36,0),0.78379,"Tree_05")
pack("Tree_06",V[0],cf(561.528,31.619,-470.284,0,76.735,0),0.613796,"Tree_06")
pack("Tree_02",V[0],cf(684.499,18.838,-220.876,0,-127.881,0),0.794252,"Tree_02")
pack("Tree_02",V[0],cf(434.248,12.157,-10.57,0,116.237,0),0.698767,"Tree_02")
pack("Tree_17",V[0],cf(522.225,14.284,7.003,0,-49.082,0),0.995548,"Tree_17")
pack("Tree_18",V[0],cf(713.27,19.526,-49.198,0,-69.843,0),0.961479,"Tree_18")
pack("Tree_03",V[0],cf(-372.421,8.138,-91.378,0,162.198,0),0.76541,"Tree_03")
pack("Tree_09",V[0],cf(650.873,21.889,-337.345,0,60.929,0),0.809632,"Tree_09")
pack("Tree_03",V[0],cf(762.802,38.013,-238.173,0,-66.133,0),1.003883,"Tree_03")
pack("Tree_17",V[0],cf(143.1,50.667,-733.143,0,87.814,0),1.027722,"Tree_17")
pack("Tree_01",V[0],cf(740.637,30.588,-188.825,0,-176.876,0),0.967129,"Tree_01")
pack("Tree_06",V[0],cf(60.726,15.923,-533.18,0,-109.072,0),0.64839,"Tree_06")
pack("Tree_03",V[0],cf(-730.692,23.315,-68.546,0,-83.461,0),1.02028,"Tree_03")
pack("Tree_09",V[0],cf(-172.824,25.782,-597.445,0,-109.657,0),1.284995,"Tree_09")
pack("Tree_16",V[0],cf(636.037,14.452,-210.122,0,-171.458,0),0.959619,"Tree_16")
pack("Tree_19",V[0],cf(-477.615,2.828,-295.218,0,16.69,0),0.432969,"Tree_19")
pack("Tree_04",V[0],cf(-423.112,6.101,-364.616,0,117.374,0),0.864691,"Tree_04")
pack("Tree_09",V[0],cf(-37.524,20.104,-576.13,0,-114.041,0),1.208658,"Tree_09")
pack("Tree_06",V[0],cf(-684.445,30.675,327.669,0,108.661,0),0.847059,"Tree_06")
pack("Tree_06",V[0],cf(455.976,15.915,469.713,0,-92.882,0),0.875404,"Tree_06")
pack("Tree_06",V[0],cf(-430.68,18.003,-120.98,0,-125.269,0),0.677738,"Tree_06")
pack("Tree_02",V[0],cf(126.997,49.874,-703.385,0,-64.738,0),0.956843,"Tree_02")
pack("Tree_12",V[0],cf(-239.569,27.713,-528.658,0,-0.296,0),0.762166,"Tree_12")
pack("Tree_01",V[0],cf(789.082,31.842,282.21,0,-2.681,0),1.004886,"Tree_01")
pack("Tree_07",V[0],cf(-558.032,6.97,187.164,0,-28.428,0),0.540289,"Tree_07")
pack("Tree_03",V[0],cf(521.99,83.123,-710.941,0,-155.016,0),0.775761,"Tree_03")
pack("Tree_11",V[0],cf(-405.55,6.78,270.194,0,-37.705,0),0.47817,"Tree_11")
pack("Tree_12",V[0],cf(783.421,31.694,-87.269,0,43.124,0),1.168989,"Tree_12")
pack("Tree_15",V[0],cf(-485.864,13.623,-255.441,0,-87.54,0),0.429042,"Tree_15")
pack("Tree_18",V[0],cf(-120.43,8.715,-461.87,0,114.359,0),0.789157,"Tree_18")
pack("Tree_13",V[0],cf(380.574,10.221,110.177,0,-100.609,0),0.553026,"Tree_13")
pack("Tree_19",V[0],cf(-615.371,25.976,-106.985,0,5.346,0),0.415884,"Tree_19")
pack("Tree_19",V[0],cf(-462.096,6.892,155.577,0,-99.314,0),0.528605,"Tree_19")
pack("Tree_19",V[0],cf(489.924,15.65,225.584,0,-116.684,0),0.600148,"Tree_19")
pack("Tree_12",V[0],cf(208.004,45.681,-779.285,0,-62.762,0),1.082154,"Tree_12")
pack("Tree_02",V[0],cf(-7.668,17.215,-529.108,0,143.522,0),0.945891,"Tree_02")
pack("Tree_05",V[0],cf(-718.87,28.998,-470.169,0,136.863,0),0.636862,"Tree_05")
pack("Tree_12",V[0],cf(-708.964,21.3,-64.515,0,51.33,0),1.044861,"Tree_12")
pack("Tree_02",V[0],cf(780.946,27.755,309.465,0,-157.424,0),1.010671,"Tree_02")
pack("Tree_04",V[0],cf(-318.991,54.838,-697.576,0,81.064,0),0.73793,"Tree_04")
pack("Tree_14",V[0],cf(-420.045,50.651,-539.741,0,-91.488,0),1.237099,"Tree_14")
pack("Tree_15",V[0],cf(-640.13,25.176,-338.65,0,79.187,0),0.496357,"Tree_15")
pack("Tree_04",V[0],cf(305.011,5.285,-233.901,0,-168.439,0),0.727278,"Tree_04")
pack("Tree_14",V[0],cf(-554.237,38.571,576.308,0,115.566,0),0.78639,"Tree_14")
pack("Tree_07",V[0],cf(-456.446,15.586,-74.931,0,-59.755,0),0.68869,"Tree_07")
pack("Tree_19",V[0],cf(-204.317,23.833,-552.707,0,71.906,0),0.40329,"Tree_19")
pack("Tree_16",V[0],cf(98.545,38.343,-665.653,0,-146.972,0),0.954554,"Tree_16")
pack("Tree_14",V[0],cf(766.76,25.916,-67.948,0,-109.92,0),0.920482,"Tree_14")
pack("Tree_04",V[0],cf(-330.119,14.84,-407.626,0,20.975,0),0.844849,"Tree_04")
pack("Tree_05",V[0],cf(571.378,26.796,239.217,0,116.598,0),0.559501,"Tree_05")
pack("Tree_04",V[0],cf(336.833,11.458,-440.223,0,157.408,0),0.791826,"Tree_04")
pack("Tree_11",V[0],cf(163.13,40.679,-732.799,0,-93.272,0),0.428458,"Tree_11")
pack("Tree_01",V[0],cf(-574.662,37.708,-208.294,0,11.349,0),0.690559,"Tree_01")
pack("Tree_08",V[0],cf(816.245,28.119,222.14,0,81.17,0),0.524933,"Tree_08")
pack("Tree_05",V[0],cf(-355.18,7.926,-380.604,0,9.418,0),0.82616,"Tree_05")
pack("Tree_14",V[0],cf(26.03,45.214,-796.658,0,-175.94,0),1.023729,"Tree_14")
pack("Tree_07",V[0],cf(-312.249,13.874,-428.449,0,38.323,0),0.706348,"Tree_07")
pack("Tree_12",V[0],cf(-534.547,28.382,-101.974,0,155.518,0),0.958598,"Tree_12")
pack("Tree_19",V[0],cf(-21.502,10.633,-433.746,0,113.417,0),0.573467,"Tree_19")
pack("Tree_11",V[0],cf(-5.858,13.827,-508.259,0,-66.573,0),0.481866,"Tree_11")
pack("Tree_16",V[0],cf(544.445,55.24,-650.779,0,-162.107,0),0.890461,"Tree_16")
pack("Tree_05",V[0],cf(-561.841,10.905,20.877,0,132.588,0),0.658508,"Tree_05")
pack("Tree_04",V[0],cf(488.126,68.978,-669.821,0,8.917,0),0.574943,"Tree_04")
pack("Tree_13",V[0],cf(697.013,31.565,-352.896,0,104.926,0),0.631443,"Tree_13")
pack("Tree_10",V[0],cf(442.009,45.027,-514.488,0,-115.278,0),0.42788,"Tree_10")
pack("Tree_18",V[0],cf(-250.137,12.111,-354.907,0,-174.728,0),1.113239,"Tree_18")
pack("Tree_12",V[0],cf(452.951,17.817,103.73,0,-109.686,0),1.068807,"Tree_12")
pack("Tree_09",V[0],cf(114.955,21.733,-580.084,0,176.108,0),1.138347,"Tree_09")
pack("Tree_14",V[0],cf(799.552,42.096,-97.701,0,79.576,0),1.214723,"Tree_14")
pack("Tree_17",V[0],cf(90.995,55.68,-799.673,0,23.906,0),1.001027,"Tree_17")
pack("Tree_08",V[0],cf(-751.137,23.31,-65.557,0,78.971,0),0.628636,"Tree_08")
pack("Tree_09",V[0],cf(422.536,8.646,-144.951,0,74.639,0),0.887109,"Tree_09")
pack("Tree_17",V[0],cf(-421.984,10.383,406.139,0,100.732,0),0.755748,"Tree_17")
pack("Tree_01",V[0],cf(-53.972,78.203,826.332,0,-162.736,0),1.04661,"Tree_01")
pack("Tree_19",V[0],cf(-62.162,15.132,-576.713,0,-45.563,0),0.575293,"Tree_19")
pack("Tree_12",V[0],cf(687.479,24.52,-332.984,0,16.557,0),0.71371,"Tree_12")
pack("Tree_15",V[0],cf(380.683,5.084,-127.458,0,148.807,0),0.615609,"Tree_15")
pack("Tree_10",V[0],cf(-710.153,28.832,372.886,0,-63.765,0),0.422908,"Tree_10")
pack("Tree_03",V[0],cf(-635.193,8.918,114.613,0,-37.229,0),0.78347,"Tree_03")
pack("Tree_17",V[0],cf(518.356,16.801,250.108,0,-29.13,0),0.696913,"Tree_17")
pack("Tree_18",V[0],cf(-159.97,19.968,-578.86,0,-65.097,0),1.033894,"Tree_18")
pack("Tree_12",V[0],cf(-614.494,40.835,-188.815,0,-140.496,0),1.138606,"Tree_12")
pack("Tree_12",V[0],cf(-530.494,29.056,-247.425,0,168.29,0),1.075417,"Tree_12")
pack("Tree_11",V[0],cf(-667.075,27.582,317.886,0,89.197,0),0.552214,"Tree_11")
pack("Tree_06",V[0],cf(-633.592,35.866,405.997,0,6.029,0),0.550127,"Tree_06")
pack("Tree_18",V[0],cf(725.647,27.662,189.428,0,49.364,0),1.096775,"Tree_18")
pack("Tree_16",V[0],cf(-519.894,9.34,91.521,0,72.318,0),1.030447,"Tree_16")
pack("Tree_06",V[0],cf(153.963,17.427,-497.428,0,45.432,0),0.874161,"Tree_06")
pack("Tree_02",V[0],cf(33.424,35.828,-745.743,0,112.931,0),0.832031,"Tree_02")
pack("Tree_17",V[0],cf(378.682,17.993,-509.454,0,-31.005,0),0.816736,"Tree_17")
pack("Tree_19",V[0],cf(-141.188,17.947,-608.434,0,80.203,0),0.43941,"Tree_19")
pack("Tree_17",V[0],cf(-601.297,7.02,86.032,0,-106.76,0),0.669471,"Tree_17")
pack("Tree_07",V[0],cf(784.321,24.327,179.957,0,-142.402,0),0.68263,"Tree_07")
pack("Tree_08",V[0],cf(-443.639,10.391,243.233,0,-138.659,0),0.738336,"Tree_08")
pack("Tree_11",V[0],cf(-289.958,34.94,-755.63,0,12.027,0),0.41256,"Tree_11")
pack("Tree_15",V[0],cf(-261.758,61.006,752.968,0,-174.393,0),0.655662,"Tree_15")
pack("Tree_15",V[0],cf(-329.636,65.975,660.148,0,-131.45,0),0.460963,"Tree_15")
pack("Tree_15",V[0],cf(152.536,13.509,-468.999,0,136.307,0),0.62023,"Tree_15")
pack("Tree_15",V[0],cf(-200.046,20.507,-522.224,0,28.853,0),0.669418,"Tree_15")
pack("Tree_16",V[0],cf(384.93,106.555,-770.081,0,-134.22,0),0.712048,"Tree_16")
pack("Tree_11",V[0],cf(-727.952,23.959,-355.028,0,-47.241,0),0.439022,"Tree_11")
pack("Tree_19",V[0],cf(75.049,32.146,-678.516,0,-95.618,0),0.50613,"Tree_19")
pack("Tree_03",V[0],cf(-513.8,22.96,-99.521,0,-8.054,0),0.876818,"Tree_03")
pack("Tree_19",V[0],cf(-144.189,12.148,-514.205,0,130.403,0),0.536609,"Tree_19")
pack("Tree_15",V[0],cf(-273.26,56.446,718.973,0,72.492,0),0.432892,"Tree_15")
pack("Tree_18",V[0],cf(165.996,47.958,-762.713,0,98.909,0),1.022617,"Tree_18")
pack("Tree_16",V[0],cf(757.602,37.395,-266.094,0,-175.232,0),1.006914,"Tree_16")
pack("Tree_04",V[0],cf(398.491,13.709,301.874,0,-166.895,0),0.557608,"Tree_04")
pack("Tree_10",V[0],cf(-516.535,7.437,164.799,0,5.921,0),0.529512,"Tree_10")
pack("Tree_05",V[0],cf(791.945,44.815,-267.509,0,41.991,0),0.691222,"Tree_05")
pack("Tree_17",V[0],cf(463.283,16.788,293.946,0,-168.259,0),0.826021,"Tree_17")
pack("Tree_07",V[0],cf(-203.569,27.023,-765.625,0,45.742,0),0.546948,"Tree_07")
pack("Tree_06",V[0],cf(794.496,28.474,-51.36,0,-3.147,0),0.699145,"Tree_06")
pack("Tree_13",V[0],cf(736.149,20.472,-44.61,0,-58.575,0),0.627731,"Tree_13")
pack("Tree_14",V[0],cf(-31.174,14.044,-462.057,0,-53.238,0),1.107737,"Tree_14")
pack("Tree_02",V[0],cf(426.754,11.711,-96.172,0,-144.342,0),0.900113,"Tree_02")
pack("Tree_19",V[0],cf(431.323,47.57,572.961,0,-46.641,0),0.488521,"Tree_19")
pack("Tree_16",V[0],cf(704.221,22.605,-247.807,0,65.934,0),0.938322,"Tree_16")
pack("Tree_13",V[0],cf(-520.294,13.452,63.743,0,-67.747,0),0.758267,"Tree_13")
pack("Tree_14",V[0],cf(-608.172,39.181,-211.74,0,50.338,0),0.874547,"Tree_14")
pack("Tree_12",V[0],cf(626.808,14.773,-331.941,0,-64.866,0),0.793442,"Tree_12")
pack("Tree_13",V[0],cf(824.585,65,-268.809,0,-170.883,0),0.563165,"Tree_13")
pack("Tree_10",V[0],cf(454.407,29.924,-588.165,0,-140.817,0),0.48145,"Tree_10")
pack("Tree_05",V[0],cf(608.326,18.235,-362.458,0,120.944,0),0.639641,"Tree_05")
pack("Tree_13",V[0],cf(461.157,19.142,230.311,0,-154.745,0),0.704575,"Tree_13")
pack("Tree_03",V[0],cf(725.063,25.994,-74.443,0,95.264,0),0.764715,"Tree_03")
pack("Tree_07",V[0],cf(91.349,49.895,-819.39,0,41.554,0),0.47377,"Tree_07")
pack("Tree_10",V[0],cf(538.164,6.709,-51.583,0,-14.189,0),0.390615,"Tree_10")
pack("Tree_07",V[0],cf(-631.114,8.54,91.016,0,-21.529,0),0.507461,"Tree_07")
pack("Tree_01",V[0],cf(732.011,22.294,164.618,0,127.361,0),0.998732,"Tree_01")
pack("Tree_17",V[0],cf(475.779,13.34,399.533,0,-47.629,0),0.853042,"Tree_17")
pack("Tree_02",V[0],cf(666.331,20.053,-189.927,0,-38.898,0),0.926571,"Tree_02")
pack("Tree_03",V[0],cf(582.817,31.288,-445.736,0,-149.412,0),1.04182,"Tree_03")
pack("Tree_18",V[0],cf(484.101,23.555,145.479,0,123.096,0),1.127642,"Tree_18")
pack("Tree_15",V[0],cf(-381.498,6.764,-55.61,0,-75.695,0),0.631936,"Tree_15")
pack("Tree_19",V[0],cf(135.076,62.152,-842.618,0,18.255,0),0.541861,"Tree_19")
pack("Tree_08",V[0],cf(689.596,30.569,435.178,0,-162.029,0),0.63637,"Tree_08")
pack("Tree_02",V[0],cf(736.374,27.234,284.78,0,-161.741,0),0.760062,"Tree_02")
pack("Tree_06",V[0],cf(514.281,70.101,-683.645,0,-24.306,0),0.798967,"Tree_06")
pack("Tree_08",V[0],cf(-593.505,35.119,562.145,0,-61.323,0),0.519182,"Tree_08")
pack("Tree_07",V[0],cf(-743.464,27.47,3.106,0,-21.709,0),0.601858,"Tree_07")
pack("Tree_06",V[0],cf(552.831,14.226,528.467,0,-25.479,0),0.573547,"Tree_06")
pack("Tree_09",V[0],cf(420.66,14.009,98.55,0,16.567,0),0.975054,"Tree_09")
pack("Tree_08",V[0],cf(158.197,5.352,496.852,0,-136.501,0),0.697636,"Tree_08")
pack("Tree_06",V[0],cf(-740.801,42.291,-248.353,0,158.62,0),0.83781,"Tree_06")
pack("Tree_17",V[0],cf(534.068,23.272,205.886,0,128.505,0),1.093692,"Tree_17")
pack("Tree_18",V[0],cf(-735.407,28.17,-332.967,0,-29.722,0),0.697936,"Tree_18")
pack("Tree_19",V[0],cf(765.49,29.584,265.396,0,-27.47,0),0.435349,"Tree_19")
pack("Tree_18",V[0],cf(725.883,30.787,-324.608,0,73.1,0),0.940326,"Tree_18")
pack("Tree_17",V[0],cf(-316.766,49.135,-789.14,0,-93.141,0),1.022655,"Tree_17")
pack("Tree_02",V[0],cf(-662.401,36.691,-301.645,0,135.064,0),0.643875,"Tree_02")
pack("Tree_13",V[0],cf(711.59,35.346,-395.435,0,-41.559,0),0.527934,"Tree_13")
pack("Tree_12",V[0],cf(-505.933,9.37,104.199,0,172.069,0),1.14266,"Tree_12")
pack("Tree_18",V[0],cf(-539.942,11.009,165.499,0,-5.528,0),1.058457,"Tree_18")
pack("Tree_19",V[0],cf(-242.207,60.679,732.905,0,119.459,0),0.611407,"Tree_19")
pack("Tree_02",V[0],cf(699.563,23.987,-77.182,0,1.499,0),0.977519,"Tree_02")
pack("Tree_08",V[0],cf(628.978,12.736,-93.564,0,-73.319,0),0.56589,"Tree_08")
pack("Tree_07",V[0],cf(-786.632,25.131,-108.891,0,94.823,0),0.624811,"Tree_07")
pack("Tree_04",V[0],cf(-449.698,6.67,201.471,0,-37.918,0),0.539737,"Tree_04")
pack("Tree_14",V[0],cf(-608.22,12.692,16.122,0,144.422,0),0.946422,"Tree_14")
pack("Tree_05",V[0],cf(428.998,55.172,601.049,0,12.23,0),0.781001,"Tree_05")
pack("Tree_19",V[0],cf(-655.227,35.386,390.119,0,-135.84,0),0.532232,"Tree_19")
pack("Tree_05",V[0],cf(710.915,34.882,401.64,0,164.601,0),0.636094,"Tree_05")
pack("Tree_16",V[0],cf(-369.577,76.457,-807.414,0,149.067,0),0.790531,"Tree_16")
pack("Tree_16",V[0],cf(697.223,22.5,-180.843,0,-150.883,0),0.681449,"Tree_16")
pack("Tree_03",V[0],cf(724.95,26.014,-191.819,0,44.315,0),0.833809,"Tree_03")
pack("Tree_01",V[0],cf(795.31,27.705,217.136,0,35.259,0),0.812599,"Tree_01")
pack("Tree_09",V[0],cf(55.096,47.938,-762.954,0,67.75,0),0.968402,"Tree_09")
pack("Tree_04",V[0],cf(-457.115,17.276,-222.33,0,80.557,0),0.795479,"Tree_04")
pack("Tree_02",V[0],cf(-745.341,29.94,106.467,0,-0.018,0),0.73706,"Tree_02")
pack("Tree_01",V[0],cf(-476.985,24.827,-115.084,0,142.937,0),0.908328,"Tree_01")
pack("Tree_08",V[0],cf(-535.141,27.497,-120.935,0,82.039,0),0.753618,"Tree_08")
pack("Tree_01",V[0],cf(-273.793,66.781,626.36,0,121.38,0),1.039678,"Tree_01")
pack("Tree_10",V[0],cf(-81.117,6.348,-457.732,0,71.234,0),0.474296,"Tree_10")
pack("Tree_04",V[0],cf(-189.484,17.359,-499.719,0,-138.224,0),0.865215,"Tree_04")
pack("Tree_09",V[0],cf(-709.235,31.003,-374.051,0,-45.871,0),1.310456,"Tree_09")
pack("Tree_15",V[0],cf(-661.139,36.615,-318.981,0,93.71,0),0.553056,"Tree_15")
pack("Tree_15",V[0],cf(742.143,41.852,-436.374,0,15.372,0),0.497756,"Tree_15")
pack("Tree_13",V[0],cf(-193.728,73.549,684.965,0,-153.251,0),0.490342,"Tree_13")
pack("Tree_03",V[0],cf(424.378,10.89,-115.594,0,-67.599,0),0.897695,"Tree_03")
pack("Tree_02",V[0],cf(-337.289,68.406,614.854,0,-135.616,0),0.664607,"Tree_02")
pack("Tree_07",V[0],cf(-325.873,6.295,470.747,0,-19.026,0),0.677399,"Tree_07")
pack("Tree_13",V[0],cf(-19.785,45.278,-769.355,0,-12.076,0),0.802126,"Tree_13")
pack("Tree_15",V[0],cf(-331.078,4.51,307.68,0,-79.884,0),0.637598,"Tree_15")
pack("Tree_04",V[0],cf(-659.906,37.392,364.306,0,-11.259,0),0.768821,"Tree_04")
pack("Tree_09",V[0],cf(627.959,17.97,-153.325,0,149.717,0),1.134451,"Tree_09")
pack("Tree_09",V[0],cf(-147.746,10.82,-459.555,0,35.214,0),1.047095,"Tree_09")
pack("Tree_17",V[0],cf(-108.633,83.713,838.725,0,-62.915,0),0.681671,"Tree_17")
pack("Tree_01",V[0],cf(450.701,17.005,183.912,0,37.315,0),0.767994,"Tree_01")
pack("Tree_19",V[0],cf(-416.111,78.603,732.519,0,-113.495,0),0.593774,"Tree_19")
pack("Tree_01",V[0],cf(-431.663,12.526,278.42,0,-134.29,0),1.063593,"Tree_01")
pack("Tree_10",V[0],cf(192.702,12.339,-479.999,0,-84.304,0),0.612559,"Tree_10")
pack("Tree_18",V[0],cf(402.587,14.823,252.442,0,-135.055,0),0.807633,"Tree_18")
pack("Tree_06",V[0],cf(715.219,39.953,-469.732,0,-105.276,0),0.694259,"Tree_06")
pack("Tree_01",V[0],cf(-31.953,20.826,-717.841,0,114.668,0),0.811154,"Tree_01")
pack("Tree_18",V[0],cf(-297.005,64.928,718.659,0,48.335,0),0.96687,"Tree_18")
pack("Tree_11",V[0],cf(237.11,80.635,704.227,0,-55.299,0),0.452481,"Tree_11")
pack("Tree_13",V[0],cf(327.897,14.836,-416.723,0,-136.656,0),0.822071,"Tree_13")
pack("Tree_01",V[0],cf(784.344,36.062,-202.797,0,-116.007,0),0.837738,"Tree_01")
pack("Tree_01",V[0],cf(-516.716,29.013,-128.473,0,-3.645,0),0.976853,"Tree_01")
pack("Tree_07",V[0],cf(47.564,18.383,-612.506,0,144.829,0),0.68554,"Tree_07")
pack("Tree_16",V[0],cf(761.674,35.083,-282.031,0,-94.751,0),0.692356,"Tree_16")
pack("Tree_06",V[0],cf(-575.499,60.131,-444.076,0,-163.27,0),0.771051,"Tree_06")
pack("Tree_10",V[0],cf(9.93,11.916,-552.874,0,107.966,0),0.398744,"Tree_10")
pack("Tree_15",V[0],cf(-240.908,10.427,-401.559,0,-127.88,0),0.653166,"Tree_15")
pack("Tree_15",V[0],cf(435.135,10.597,385.965,0,-162.886,0),0.547376,"Tree_15")
pack("Tree_05",V[0],cf(546.469,22.66,227.378,0,170.686,0),0.65094,"Tree_05")
pack("Tree_03",V[0],cf(-417.664,11.758,458.954,0,-116.776,0),0.859578,"Tree_03")
pack("Tree_13",V[0],cf(0.525,84.728,810.154,0,124.018,0),0.622127,"Tree_13")
pack("Tree_15",V[0],cf(-701.3,20.903,14.697,0,-24.953,0),0.441619,"Tree_15")
pack("Tree_07",V[0],cf(-618.816,32.116,376.639,0,-83.154,0),0.563142,"Tree_07")
pack("Tree_11",V[0],cf(820.211,21.68,165.755,0,-123.991,0),0.383879,"Tree_11")
pack("Tree_17",V[0],cf(88.014,49.668,-748.37,0,-3.61,0),0.866306,"Tree_17")
pack("Tree_03",V[0],cf(-169.215,19.092,-566.073,0,-34.04,0),0.810523,"Tree_03")
pack("Tree_03",V[0],cf(-578.692,39.116,-177.308,0,58.69,0),0.853448,"Tree_03")
pack("Tree_08",V[0],cf(763.361,31.997,242.637,0,5.216,0),0.642106,"Tree_08")
pack("Tree_11",V[0],cf(71.758,7.843,-395.967,0,-160.441,0),0.506156,"Tree_11")
pack("Tree_15",V[0],cf(-655.026,36.016,-235.039,0,88.116,0),0.478271,"Tree_15")
pack("Tree_19",V[0],cf(-659.112,37.787,-167.161,0,82.845,0),0.400216,"Tree_19")
pack("Tree_17",V[0],cf(160.354,76.669,-865.099,0,-25.633,0),1.066765,"Tree_17")
pack("Tree_14",V[0],cf(-799.126,31.134,-98.198,0,-172.322,0),0.890589,"Tree_14")
pack("Tree_14",V[0],cf(831.649,33.811,185.992,0,2.938,0),1.088218,"Tree_14")
pack("Tree_08",V[0],cf(574.597,19.121,112.13,0,-88.882,0),0.685693,"Tree_08")
pack("Tree_16",V[0],cf(-402.94,8.547,449.673,0,104.619,0),0.844057,"Tree_16")
pack("Tree_08",V[0],cf(524.905,20.92,417.261,0,74.938,0),0.493588,"Tree_08")
pack("Tree_01",V[0],cf(-164.279,58.884,615.356,0,-124.46,0),0.94214,"Tree_01")
pack("Tree_16",V[0],cf(675.827,33.94,178.503,0,-55.575,0),1.092065,"Tree_16")
pack("Tree_06",V[0],cf(-175.529,76.034,836.339,0,51.562,0),0.648771,"Tree_06")
pack("Tree_16",V[0],cf(-619.719,40.43,-287.306,0,-172.466,0),1.030836,"Tree_16")
pack("Tree_12",V[0],cf(-731.867,24.926,91.728,0,15.395,0),1.062199,"Tree_12")
pack("Tree_09",V[0],cf(51.119,16.774,-472.92,0,83.867,0),0.956593,"Tree_09")
pack("Tree_04",V[0],cf(514.063,31.769,577.447,0,-136.47,0),0.775478,"Tree_04")
pack("Tree_08",V[0],cf(-64.823,21.863,-716.048,0,-1.104,0),0.487955,"Tree_08")
pack("Tree_16",V[0],cf(507.162,21.545,139.202,0,154.98,0),0.787631,"Tree_16")
pack("Tree_10",V[0],cf(280.548,4.035,-397.606,0,160.465,0),0.592416,"Tree_10")
pack("Tree_13",V[0],cf(-577.504,10.943,170.19,0,-27.349,0),0.525838,"Tree_13")
pack("Tree_19",V[0],cf(-524.153,9.648,263.421,0,-18.314,0),0.592806,"Tree_19")
pack("Tree_12",V[0],cf(208.564,76.47,734.117,0,-163.297,0),0.720587,"Tree_12")
pack("Tree_12",V[0],cf(-592.12,10.575,29.868,0,-147.291,0),1.023232,"Tree_12")
pack("Tree_19",V[0],cf(218.581,11.704,-510.138,0,127.503,0),0.513915,"Tree_19")
pack("Tree_09",V[0],cf(779.106,30.91,239.516,0,-124.371,0),0.850461,"Tree_09")
pack("Tree_06",V[0],cf(-600.066,36.452,-259.321,0,-104.646,0),0.548557,"Tree_06")
pack("Tree_18",V[0],cf(-265.373,30.608,-758.095,0,-121.413,0),1.136559,"Tree_18")
pack("Tree_17",V[0],cf(-619.513,13.299,58.06,0,45.316,0),1.093677,"Tree_17")
pack("Tree_13",V[0],cf(-692.52,17.883,113.913,0,28.912,0),0.838005,"Tree_13")
pack("Tree_08",V[0],cf(-440.204,72.617,669.201,0,106.001,0),0.741305,"Tree_08")
pack("Tree_01",V[0],cf(-520.475,57.461,628.438,0,98.121,0),0.688683,"Tree_01")
pack("Tree_18",V[0],cf(699.858,29.064,184.353,0,-37.539,0),0.792688,"Tree_18")
pack("Tree_16",V[0],cf(269.838,92.4,-869.491,0,-149.72,0),0.894818,"Tree_16")
pack("Tree_04",V[0],cf(-213.905,25.197,-802.817,0,-33.885,0),0.823484,"Tree_04")
pack("Tree_17",V[0],cf(-513.143,30.332,528.01,0,143.389,0),1.027654,"Tree_17")
pack("Tree_15",V[0],cf(558.497,20.011,199.422,0,-84.557,0),0.555482,"Tree_15")
pack("Tree_01",V[0],cf(-178.095,6.603,-413.782,0,164.14,0),0.6993,"Tree_01")
pack("Tree_01",V[0],cf(-51.111,36.744,-770.41,0,-160.167,0),1.087523,"Tree_01")
pack("Tree_14",V[0],cf(760.978,22.678,170.824,0,72.069,0),1.071382,"Tree_14")
pack("Tree_17",V[0],cf(-522.79,12.272,225.595,0,131.934,0),1.059596,"Tree_17")
pack("Tree_06",V[0],cf(-124.93,80.144,775.676,0,116.802,0),0.819684,"Tree_06")
pack("Tree_07",V[0],cf(-261.742,28.907,-797.241,0,38.737,0),0.620584,"Tree_07")
pack("Tree_18",V[0],cf(-492.553,22.639,-108.244,0,164.692,0),0.87423,"Tree_18")
pack("Tree_08",V[0],cf(-367.967,5.689,-388.49,0,20.728,0),0.549143,"Tree_08")
pack("Tree_04",V[0],cf(-307.552,10.719,-385.824,0,-20.905,0),0.558011,"Tree_04")
pack("Tree_15",V[0],cf(-281.503,12.191,-456.535,0,-8.048,0),0.422403,"Tree_15")
pack("Tree_09",V[0],cf(538.375,22.113,258.251,0,-22.143,0),1.004698,"Tree_09")
pack("Tree_19",V[0],cf(223.24,75.374,790.916,0,-76.323,0),0.596203,"Tree_19")
pack("Bush_03",V[0],cf(683.468,32.63,364.063,0,23.365,0),0.783686,"Bush_03")
pack("Bush_01",V[0],cf(244.322,33.288,-790.045,0,-46.939,0),0.471325,"Bush_01")
pack("Bush_03",V[0],cf(-393.306,19.394,-476.055,0,-117.434,0),0.636427,"Bush_03")
pack("Bush_02",V[0],cf(402.292,9.756,278.893,0,39.059,0),0.431681,"Bush_02")
pack("Bush_03",V[0],cf(442.018,29.927,533.013,0,-171.008,0),0.896466,"Bush_03")
pack("Bush_03",V[0],cf(-318.989,21.637,-536.599,0,177.098,0),0.837206,"Bush_03")
pack("Bush_01",V[0],cf(359.963,0.159,-177.327,0,-58.468,0),0.54413,"Bush_01")
pack("Bush_03",V[0],cf(-433.754,64.002,598.591,0,-131.543,0),0.702597,"Bush_03")
pack("Bush_02",V[0],cf(372.872,55.061,617.27,0,87.754,0),0.50503,"Bush_02")
pack("Bush_02",V[0],cf(-325.525,55.358,-663.347,0,-87.635,0),0.689708,"Bush_02")
pack("Bush_01",V[0],cf(285.402,1.896,-445.6,0,26.31,0),0.760492,"Bush_01")
pack("Bush_02",V[0],cf(-271.09,-0.699,294.732,0,94.908,0),0.588398,"Bush_02")
pack("Bush_03",V[0],cf(308.14,33.416,-716.044,0,90.042,0),0.758905,"Bush_03")
pack("Bush_02",V[0],cf(228.206,0.082,555.151,0,52.551,0),0.439337,"Bush_02")
pack("Bush_02",V[0],cf(560.826,52.084,-658.033,0,-63.811,0),0.732638,"Bush_02")
pack("Bush_02",V[0],cf(-684.614,21.354,-337.79,0,62.332,0),0.773363,"Bush_02")
pack("Bush_03",V[0],cf(-382.297,-0.262,-328.063,0,28.141,0),1.145221,"Bush_03")
pack("Bush_01",V[0],cf(269.359,-0.082,536.876,0,-155.079,0),0.572789,"Bush_01")
pack("Bush_01",V[0],cf(-273.667,25.245,-743.648,0,57.862,0),0.639659,"Bush_01")
pack("Bush_03",V[0],cf(500.576,38.729,-519.178,0,177.502,0),0.704729,"Bush_03")
pack("Bush_03",V[0],cf(-480.372,10.683,-453.571,0,4.175,0),0.76015,"Bush_03")
pack("Bush_03",V[0],cf(-615.681,32.752,-258.197,0,-23.176,0),1.174479,"Bush_03")
pack("Bush_01",V[0],cf(-134.161,22.129,-666.369,0,-8.593,0),0.615471,"Bush_01")
pack("Bush_03",V[0],cf(-369.59,1.089,471.824,0,-94.904,0),0.693039,"Bush_03")
pack("Bush_02",V[0],cf(-750.925,11.682,-125.642,0,-126.039,0),0.458153,"Bush_02")
pack("Bush_02",V[0],cf(740.076,20.865,-210.989,0,172.891,0),0.626155,"Bush_02")
pack("Bush_02",V[0],cf(437.905,31.468,-554.08,0,94.649,0),0.512575,"Bush_02")
pack("Bush_03",V[0],cf(779.219,16.416,20.84,0,161.843,0),0.669948,"Bush_03")
pack("Bush_01",V[0],cf(479.217,11.129,437.618,0,58.822,0),0.481519,"Bush_01")
pack("Bush_01",V[0],cf(570.543,12.49,-400.734,0,-20.28,0),0.720736,"Bush_01")
pack("Bush_01",V[0],cf(-429.839,43.004,523.442,0,-58.572,0),0.558408,"Bush_01")
pack("Bush_02",V[0],cf(-332.465,49.009,552.013,0,-144.326,0),0.581709,"Bush_02")
pack("Bush_02",V[0],cf(-602.418,16.682,280.996,0,43.622,0),0.429313,"Bush_02")
pack("Bush_03",V[0],cf(-229.713,19.398,-771.113,0,177.896,0),1.099449,"Bush_03")
pack("Bush_03",V[0],cf(-4.502,10.881,-703.556,0,-145.707,0),0.761637,"Bush_03")
pack("Bush_01",V[0],cf(-609.265,44.421,602.146,0,83.283,0),0.70019,"Bush_01")
pack("Bush_01",V[0],cf(-481.511,37.159,547.251,0,-103.519,0),0.585521,"Bush_01")
pack("Bush_03",V[0],cf(621.845,36.85,-489.05,0,-100.314,0),0.785932,"Bush_03")
pack("Bush_03",V[0],cf(-515.309,64.163,655.815,0,-85.842,0),0.767662,"Bush_03")
pack("Bush_02",V[0],cf(-281.726,-0.273,433.628,0,-8.472,0),0.636793,"Bush_02")
pack("Bush_01",V[0],cf(679.281,8.353,-54.389,0,160.075,0),0.706816,"Bush_01")
pack("Bush_03",V[0],cf(-497.826,3.895,243.408,0,22.063,0),1.013086,"Bush_03")
pack("Bush_03",V[0],cf(-669.037,33.228,-160.616,0,30.142,0),0.812916,"Bush_03")
pack("Bush_03",V[0],cf(461.357,9.034,320.224,0,119.662,0),1.042637,"Bush_03")
pack("Bush_01",V[0],cf(553.945,14.738,189.65,0,-73.275,0),0.73307,"Bush_01")
pack("Bush_03",V[0],cf(-646.078,41.895,538.184,0,-179.522,0),0.712913,"Bush_03")
pack("Bush_02",V[0],cf(331.691,80.685,687.254,0,123.977,0),0.691624,"Bush_02")
pack("Bush_01",V[0],cf(42.358,65.261,695.507,0,-76.245,0),0.580384,"Bush_01")
pack("Bush_01",V[0],cf(-350.227,60.083,589.953,0,173.418,0),0.438349,"Bush_01")
pack("Bush_03",V[0],cf(735.26,13.364,159.215,0,51.185,0),1.099283,"Bush_03")
pack("Bush_03",V[0],cf(729.625,23.609,-140.345,0,-27.273,0),1.047433,"Bush_03")
pack("Bush_02",V[0],cf(190.233,-0.112,563.554,0,85.742,0),0.605143,"Bush_02")
pack("Bush_03",V[0],cf(253.605,1.279,-360.042,0,118.288,0),1.142123,"Bush_03")
pack("Bush_01",V[0],cf(326.152,3.051,237.653,0,-38.518,0),0.616174,"Bush_01")
pack("Bush_02",V[0],cf(-309.604,39.517,-620.458,0,16.402,0),0.609671,"Bush_02")
pack("Bush_01",V[0],cf(-739.091,20.813,108.219,0,76.978,0),0.443255,"Bush_01")
pack("Bush_03",V[0],cf(-333.886,-0.212,327.665,0,138.983,0),0.993169,"Bush_03")
pack("Bush_01",V[0],cf(-805.778,10.617,244.391,0,-83.444,0),0.439063,"Bush_01")
pack("Bush_02",V[0],cf(-498.927,21.339,-217.539,0,178.165,0),0.700183,"Bush_02")
pack("Bush_01",V[0],cf(149.15,68.408,677.331,0,-106.266,0),0.745957,"Bush_01")
pack("Bush_01",V[0],cf(-183.672,19.589,-604.107,0,-128.757,0),0.734562,"Bush_01")
pack("Bush_03",V[0],cf(-240.944,16.815,-497.993,0,-147.206,0),0.951405,"Bush_03")
pack("Bush_01",V[0],cf(516.761,49.712,-656.277,0,-156.824,0),0.605306,"Bush_01")
pack("Bush_01",V[0],cf(-513.429,26.491,547.874,0,-48.932,0),0.470049,"Bush_01")
pack("Bush_02",V[0],cf(540.565,58.071,-683.131,0,116.717,0),0.700355,"Bush_02")
pack("Bush_01",V[0],cf(49.874,68.178,721.543,0,4.693,0),0.538655,"Bush_01")
pack("Bush_03",V[0],cf(-552.867,21.64,-310.449,0,121.076,0),0.91149,"Bush_03")
pack("Bush_02",V[0],cf(291.64,-0.012,-300.221,0,37.132,0),0.493215,"Bush_02")
pack("Bush_02",V[0],cf(257.943,1.24,-333.682,0,-86.666,0),0.604946,"Bush_02")
pack("Bush_03",V[0],cf(-664.714,30.874,382.552,0,-70.386,0),0.976118,"Bush_03")
pack("Bush_03",V[0],cf(-432.364,3.874,141.363,0,-138.335,0),0.844888,"Bush_03")
pack("Bush_02",V[0],cf(-693.432,3.642,148.94,0,86.154,0),0.755569,"Bush_02")
pack("Bush_02",V[0],cf(-240.468,4.046,-372.182,0,-27.93,0),0.442465,"Bush_02")
pack("Bush_03",V[0],cf(-393.72,3.791,252.195,0,-5.806,0),1.142635,"Bush_03")
pack("Bush_01",V[0],cf(-379.77,90.633,794.871,0,132.789,0),0.756766,"Bush_01")
pack("Bush_03",V[0],cf(-226.956,-0.195,385.72,0,-173.311,0),1.151731,"Bush_03")
pack("Bush_03",V[0],cf(-755.706,25.216,374.047,0,-16.072,0),0.931059,"Bush_03")
pack("Bush_01",V[0],cf(-689.497,22.283,-422.623,0,144.004,0),0.741823,"Bush_01")
pack("Bush_03",V[0],cf(723.503,27.988,414.75,0,65.538,0),1.15986,"Bush_03")
pack("Bush_03",V[0],cf(-459.728,67.522,649.11,0,175.612,0),0.788417,"Bush_03")
pack("Bush_02",V[0],cf(382.414,45.846,570.444,0,-86.096,0),0.571472,"Bush_02")
pack("Bush_02",V[0],cf(-456.286,4.222,241.187,0,174.821,0),0.757842,"Bush_02")
pack("Bush_01",V[0],cf(351.368,48.233,591.801,0,82.576,0),0.684202,"Bush_01")
pack("Bush_03",V[0],cf(-392.36,2.208,44.215,0,30.276,0),1.059579,"Bush_03")
pack("Bush_02",V[0],cf(-671.021,15.525,33.32,0,114.339,0),0.499057,"Bush_02")
pack("Bush_03",V[0],cf(-8.352,39.967,-815.701,0,143.285,0),1.150126,"Bush_03")
mesh("rbxassetid://118751307245812",V[0],{CFrame=cf(-316.212,50.888,-680.008,0,169.295,0),_attrs={["AutoProp"]=true},Size=Vector3.new(2.819,2.398,3.611),CanCollide=false,CanTouch=false,CanQuery=false})
pack("Bush_02",V[0],cf(484.153,7.306,-118.511,0,-5.292,0),0.561521,"Bush_02")
mesh("rbxassetid://105075619034361",V[0],{CFrame=cf(-583.25,14.286,217.293,0,-123.128,0),_attrs={["AutoProp"]=true},Size=Vector3.new(10.755,19.514,9.104),CanCollide=false,CanTouch=false,CanQuery=false})
pack("Bush_01",V[0],cf(-580.006,22.114,376.891,0,-4.931,0),0.460064,"Bush_01")
pack("Bush_03",V[0],cf(-535.838,10.867,-4.361,0,126.69,0),1.169652,"Bush_03")
pack("Bush_01",V[0],cf(463.879,12.851,133.261,0,-150.12,0),0.526736,"Bush_01")
mesh("rbxassetid://84686903386845",V[0],{CFrame=cf(13.757,24.937,-712.517,0,-110.803,0),_attrs={["AutoProp"]=true},Size=Vector3.new(28.996,25.87,24.204),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://129137061388220",V[0],{CFrame=cf(-377.459,66.302,-636.636,0,-106.981,0),_attrs={["AutoProp"]=true},Size=Vector3.new(6.734,11.675,4.348),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://129137061388220",V[0],{CFrame=cf(-521.309,15.015,383.989,0,-96.718,0),_attrs={["AutoProp"]=true},Size=Vector3.new(5.986,10.377,3.865),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://140209872891749",V[0],{CFrame=cf(590.721,43.945,633.487,0,138.543,0),_attrs={["AutoProp"]=true},Size=Vector3.new(7.625,5.466,8.686),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://84686903386845",V[0],{CFrame=cf(-374.488,9.247,169.615,0,-54.321,0),_attrs={["AutoProp"]=true},Size=Vector3.new(24.652,21.995,20.578),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://118751307245812",V[0],{CFrame=cf(-318.282,43.317,-620.897,0,-59.295,0),_attrs={["AutoProp"]=true},Size=Vector3.new(3.786,3.222,4.85),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://77567619963102",V[0],{CFrame=cf(-153.853,84.753,837.352,0,-88.503,0),_attrs={["AutoProp"]=true},Size=Vector3.new(21.74,27.729,21.869),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://128129862753053",V[0],{CFrame=cf(-274.283,3.754,-326.803,0,128.767,0),_attrs={["AutoProp"]=true},Size=Vector3.new(7.306,5.205,7.333),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://84686903386845",V[0],{CFrame=cf(215.511,8.955,-410.706,0,155.446,0),_attrs={["AutoProp"]=true},Size=Vector3.new(28.138,25.106,23.488),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://105075619034361",V[0],{CFrame=cf(-426.482,43.91,-527.64,0,-120.185,0),_attrs={["AutoProp"]=true},Size=Vector3.new(11.385,20.659,9.638),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://133711501968980",V[0],{CFrame=cf(-885.572,100.739,-266.127,0,140.435,0),_attrs={["AutoProp"]=true},Size=Vector3.new(3.066,5.568,3.218),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://105075619034361",V[0],{CFrame=cf(-311.542,7.389,-291.283,0,-124.886,0),_attrs={["AutoProp"]=true},Size=Vector3.new(9.953,18.06,8.425),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://77567619963102",V[0],{CFrame=cf(-212.308,12.88,-473.663,0,-90.462,0),_attrs={["AutoProp"]=true},Size=Vector3.new(8.2,10.459,8.249),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://82715674813797",V[0],{CFrame=cf(864.772,78.127,-50.954,0,-73.171,0),_attrs={["AutoProp"]=true},Size=Vector3.new(15.085,13.647,16.131),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://118751307245812",V[0],{CFrame=cf(-296.914,0.871,380.914,0,176.613,0),_attrs={["AutoProp"]=true},Size=Vector3.new(2.921,2.486,3.742),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://118751307245812",V[0],{CFrame=cf(417.491,39.029,-641.335,0,105.967,0),_attrs={["AutoProp"]=true},Size=Vector3.new(5.127,4.362,6.568),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://105075619034361",V[0],{CFrame=cf(-370.19,37.067,-550.736,0,22.068,0),_attrs={["AutoProp"]=true},Size=Vector3.new(11.464,20.802,9.704),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://128129862753053",V[0],{CFrame=cf(101.773,65.843,687.955,0,-74.259,0),_attrs={["AutoProp"]=true},Size=Vector3.new(8.555,6.095,8.587),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://77567619963102",V[0],{CFrame=cf(-744.864,30.485,-179.051,0,-141.173,0),_attrs={["AutoProp"]=true},Size=Vector3.new(21.97,28.022,22.1),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://118751307245812",V[0],{CFrame=cf(319.113,54.512,-765.262,0,-48.437,0),_attrs={["AutoProp"]=true},Size=Vector3.new(6.888,5.861,8.824),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://133711501968980",V[0],{CFrame=cf(756.747,22.205,-71.406,0,-34.05,0),_attrs={["AutoProp"]=true},Size=Vector3.new(3.491,6.34,3.664),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://87099845207275",V[0],{CFrame=cf(-779.26,47.905,58.92,0,99.967,0),_attrs={["AutoProp"]=true},Size=Vector3.new(48.881,19.87,35.996),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://87099845207275",V[0],{CFrame=cf(110.206,53.29,-805.585,0,76.048,0),_attrs={["AutoProp"]=true},Size=Vector3.new(37.554,15.266,27.655),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://87099845207275",V[0],{CFrame=cf(636.335,13.964,16.089,0,-146.54,0),_attrs={["AutoProp"]=true},Size=Vector3.new(28.878,11.739,21.266),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://105431839183241",V[0],{CFrame=cf(524.411,16.252,-441.176,0,-70.338,0),_attrs={["AutoProp"]=true},Size=Vector3.new(4.998,10.199,4.199),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://82715674813797",V[0],{CFrame=cf(-760.6,18.882,338.223,0,167.713,0),_attrs={["AutoProp"]=true},Size=Vector3.new(15.672,14.178,16.759),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://77567619963102",V[0],{CFrame=cf(20.705,26.26,-728.298,0,59.017,0),_attrs={["AutoProp"]=true},Size=Vector3.new(10.954,13.971,11.019),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://128129862753053",V[0],{CFrame=cf(-720.054,21.413,326.06,0,52.476,0),_attrs={["AutoProp"]=true},Size=Vector3.new(9.774,6.964,9.811),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://84686903386845",V[0],{CFrame=cf(-473.887,26.899,-153.62,0,-162.183,0),_attrs={["AutoProp"]=true},Size=Vector3.new(17.158,15.309,14.322),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://87099845207275",V[0],{CFrame=cf(465.546,34.181,-591.675,0,-85.197,0),_attrs={["AutoProp"]=true},Size=Vector3.new(52.551,21.362,38.699),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://129137061388220",V[0],{CFrame=cf(-478.681,109.665,729.112,0,12.516,0),_attrs={["AutoProp"]=true},Size=Vector3.new(9.644,16.718,6.226),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://118751307245812",V[0],{CFrame=cf(-323.917,50.604,557.177,0,80.02,0),_attrs={["AutoProp"]=true},Size=Vector3.new(4.089,3.479,5.239),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://133711501968980",V[0],{CFrame=cf(-779.033,28.11,-320.264,0,41.686,0),_attrs={["AutoProp"]=true},Size=Vector3.new(2.66,4.831,2.792),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://133711501968980",V[0],{CFrame=cf(267.662,2.091,456.858,0,-27.954,0),_attrs={["AutoProp"]=true},Size=Vector3.new(2.392,4.344,2.51),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://128129862753053",V[0],{CFrame=cf(-413.503,4.251,173.383,0,18.309,0),_attrs={["AutoProp"]=true},Size=Vector3.new(7.637,5.441,7.665),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://77567619963102",V[0],{CFrame=cf(625.456,15.415,28.783,0,-69.398,0),_attrs={["AutoProp"]=true},Size=Vector3.new(9.782,12.477,9.84),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://84686903386845",V[0],{CFrame=cf(-524.313,78.346,-526.012,0,-171.831,0),_attrs={["AutoProp"]=true},Size=Vector3.new(18.812,16.785,15.704),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://84686903386845",V[0],{CFrame=cf(-198.258,62.106,627.291,0,-131.939,0),_attrs={["AutoProp"]=true},Size=Vector3.new(21.628,19.297,18.054),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://82715674813797",V[0],{CFrame=cf(239.256,4.214,301.397,0,74.547,0),_attrs={["AutoProp"]=true},Size=Vector3.new(8.584,7.766,9.179),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://118751307245812",V[0],{CFrame=cf(-512.962,11.648,-313.861,0,178.429,0),_attrs={["AutoProp"]=true},Size=Vector3.new(3.283,2.793,4.205),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://128129862753053",V[0],{CFrame=cf(-713.538,26.283,364.278,0,-108.875,0),_attrs={["AutoProp"]=true},Size=Vector3.new(9.992,7.119,10.03),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://77567619963102",V[0],{CFrame=cf(-190.439,68.607,716.633,0,131.475,0),_attrs={["AutoProp"]=true},Size=Vector3.new(12.108,15.443,12.179),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://105431839183241",V[0],{CFrame=cf(801.042,34.614,-66.362,0,-45.014,0),_attrs={["AutoProp"]=true},Size=Vector3.new(8.258,16.852,6.938),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://133711501968980",V[0],{CFrame=cf(541.466,20.107,-457.046,0,-53.966,0),_attrs={["AutoProp"]=true},Size=Vector3.new(1.632,2.964,1.713),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://105431839183241",V[0],{CFrame=cf(193.785,43.746,-765.263,0,134.571,0),_attrs={["AutoProp"]=true},Size=Vector3.new(8.239,16.813,6.922),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://87099845207275",V[0],{CFrame=cf(-228.11,63.16,718.445,0,-137.804,0),_attrs={["AutoProp"]=true},Size=Vector3.new(40.601,16.504,29.899),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://105431839183241",V[0],{CFrame=cf(446.681,12.711,241.868,0,66.539,0),_attrs={["AutoProp"]=true},Size=Vector3.new(4.541,9.268,3.816),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://105075619034361",V[0],{CFrame=cf(-673.502,67.912,541.312,0,-172.237,0),_attrs={["AutoProp"]=true},Size=Vector3.new(13.003,23.594,11.007),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://77567619963102",V[0],{CFrame=cf(117.348,66.222,-853.018,0,65.774,0),_attrs={["AutoProp"]=true},Size=Vector3.new(13.007,16.591,13.084),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://133711501968980",V[0],{CFrame=cf(-210.148,65.542,813.128,0,-10.281,0),_attrs={["AutoProp"]=true},Size=Vector3.new(2.632,4.781,2.762),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://140209872891749",V[0],{CFrame=cf(-722.507,19.976,336.983,0,161.972,0),_attrs={["AutoProp"]=true},Size=Vector3.new(8.602,6.167,9.799),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://87099845207275",V[0],{CFrame=cf(30.18,12.633,-438.216,0,-118.31,0),_attrs={["AutoProp"]=true},Size=Vector3.new(27.778,11.292,20.456),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://84686903386845",V[0],{CFrame=cf(-778.806,32.35,-145.632,0,48.021,0),_attrs={["AutoProp"]=true},Size=Vector3.new(44.24,39.472,36.929),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://133711501968980",V[0],{CFrame=cf(753.56,113.698,-529.929,0,103.468,0),_attrs={["AutoProp"]=true},Size=Vector3.new(4.098,7.442,4.3),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://118751307245812",V[0],{CFrame=cf(-730.191,19.958,-394.659,0,157.47,0),_attrs={["AutoProp"]=true},Size=Vector3.new(4.407,3.75,5.645),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://140209872891749",V[0],{CFrame=cf(-678.083,27.03,-452.212,0,53.952,0),_attrs={["AutoProp"]=true},Size=Vector3.new(6.569,4.709,7.483),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://133711501968980",V[0],{CFrame=cf(-202.902,61.208,643.496,0,38.35,0),_attrs={["AutoProp"]=true},Size=Vector3.new(2.035,3.696,2.136),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://87099845207275",V[0],{CFrame=cf(-149.605,21.622,-705.91,0,155.783,0),_attrs={["AutoProp"]=true},Size=Vector3.new(20.882,8.489,15.378),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://84686903386845",V[0],{CFrame=cf(780.484,40.135,-183.964,0,162.072,0),_attrs={["AutoProp"]=true},Size=Vector3.new(27.936,24.925,23.319),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://128129862753053",V[0],{CFrame=cf(-704.34,32.054,391.417,0,-131.224,0),_attrs={["AutoProp"]=true},Size=Vector3.new(9.981,7.111,10.019),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://105431839183241",V[0],{CFrame=cf(109.055,53.604,-774.914,0,-44.78,0),_attrs={["AutoProp"]=true},Size=Vector3.new(7.863,16.047,6.607),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://84686903386845",V[0],{CFrame=cf(-395.96,8.227,-363.754,0,119.867,0),_attrs={["AutoProp"]=true},Size=Vector3.new(28.869,25.757,24.098),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://133711501968980",V[0],{CFrame=cf(360.817,9.129,300.338,0,-140.654,0),_attrs={["AutoProp"]=true},Size=Vector3.new(1.858,3.375,1.95),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://133711501968980",V[0],{CFrame=cf(-222.244,1.281,308.284,0,-142.563,0),_attrs={["AutoProp"]=true},Size=Vector3.new(2.125,3.858,2.229),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://140209872891749",V[0],{CFrame=cf(806.451,23.176,198.386,0,120.682,0),_attrs={["AutoProp"]=true},Size=Vector3.new(10.006,7.173,11.399),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://140209872891749",V[0],{CFrame=cf(462.838,83.887,669.54,0,60.738,0),_attrs={["AutoProp"]=true},Size=Vector3.new(11.08,7.943,12.621),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://140209872891749",V[0],{CFrame=cf(-541.132,3.038,114.202,0,-109.557,0),_attrs={["AutoProp"]=true},Size=Vector3.new(4.883,3.501,5.563),CanCollide=false,CanTouch=false,CanQuery=false})
mesh("rbxassetid://105075619034361",V[0],{CFrame=cf(408.891,100.068,718.602,0,87.13,0),_attrs={["AutoProp"]=true},Size=Vector3.new(21.025,38.15,17.797),CanCollide=false,CanTouch=false,CanQuery=false})
```

---

**Related:** [[Lobby code]] · [[Limits and safe use]]
