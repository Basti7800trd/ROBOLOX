---
tags:
  - code
  - plots
  - restaurant
updated: 2026-10-26
studio_path: "Workspace > Plots"
objects: 108
---

> [!warning] Before running
> Read [[Limits and safe use]]. Edit mode only.

## Plots and restaurant code

Each of the 6 plots has two parts: a fixed frame that always stands in the world, and the restaurant, which is built from code when a player joins and removed when they leave.

1. **Frame (always there):** Workspace > Plots > Plot1–6, each with a 128 × 128 Base, a name Sign, Decor (hedges, gate pillars, gate caps, entrance path) and empty Pieces and Customers folders. No script builds these, so the code below was generated from the game (tested in Studio: all 108 objects rebuilt exactly).
2. **Restaurant (built per player):** when a player joins, Plots.assign gives them the first free plot. It reads their saved layout, or Config.StarterLayout for a new player, and calls Plots.place for each entry.
3. **Each piece:** Plots.place asks PieceBuilder for the model (or the matching model in ReplicatedStorage > PieceModels), puts it at the plot's position plus the piece's x, z and turn, and stores it in the plot's Pieces folder.
4. **Build mode:** Placement checks every new spot. You can build up to 61 studs from the plot centre, floors snap to a 16-stud grid and everything else to half studs, and pieces of the same group can't overlap.

Plot coordinates are x and z in studs from the plot centre; negative z points towards the street (the lobby).

### Plot frames (Workspace > Plots)

Paste the [[Lobby code#Shared helpers (paste these first, also for the landscape and plot code)|shared helpers]] first. If a Plots folder exists, the copy is built as Plots\_Rebuilt.

```lua
local S = {}
S[1]={Size=Vector3.new(56,3.2,2),Color=rgb(62,138,58),Material=Enum.Material.Grass}
S[2]={Size=Vector3.new(2.6,10,2.6),Color=rgb(214,204,188),Material=Enum.Material.Slate}
S[3]={Size=Vector3.new(12,0.1,28),Color=rgb(214,200,176),Material=Enum.Material.Pavement}
S[4]={Size=Vector3.new(3.2,0.8,3.2),Color=rgb(180,170,155),Material=Enum.Material.Slate}
S[5]={Size=Vector3.new(2,3.2,124),Color=rgb(62,138,58),Material=Enum.Material.Grass}
S[6]={Size=Vector3.new(128,3.2,2),Color=rgb(62,138,58),Material=Enum.Material.Grass}
S[7]={Size=Vector3.new(128,0.4,128),Color=rgb(112,186,84),Material=Enum.Material.Grass}
S[8]={Size=Vector3.new(20,3,1.2),Color=rgb(206,62,50),Material=Enum.Material.SmoothPlastic}
S[9]={SizingMode=Enum.SurfaceGuiSizingMode.PixelsPerStud,PixelsPerStud=30}
S[10]={Size=UDim2.new(0.76,0,0.7,0),Position=UDim2.new(0.12,0,0,0),BackgroundTransparency=1,FontFace=Font.new("rbxasset://fonts/families/FredokaOne.json",Enum.FontWeight.Regular,Enum.FontStyle.Normal),TextColor3=rgb(255,255,255),TextScaled=true,TextWrapped=true}
V[0]=new("Folder",workspace,{Name="Plots"})
V[0].Name=workspace:FindFirstChild("Plots") and "Plots_Rebuilt" or "Plots"
V[1]=new("Model",V[0],{Name="Plot1",_attrs={["PlotIndex"]=1}})
V[2]=new("Folder",V[1],{Name="Decor"})
new("Part",V[2],{Name="Hedge",CFrame=cf(54.823,2,166.956,0,30,0)},S[1])
new("Part",V[2],{Name="GatePillar",CFrame=cf(93.794,5.2,144.456,0,30,0)},S[2])
new("Part",V[2],{Name="Hedge",CFrame=cf(117.177,2,130.956,0,30,0)},S[1])
new("Part",V[2],{Name="EntrancePath",CFrame=cf(92.5,0.45,160.215,0,30,0)},S[3])
new("Part",V[2],{Name="GateCap",CFrame=cf(78.206,10.6,153.456,0,30,0)},S[4])
new("Part",V[2],{Name="GateCap",CFrame=cf(93.794,10.6,144.456,0,30,0)},S[4])
new("Part",V[2],{Name="GatePillar",CFrame=cf(78.206,5.2,153.456,0,30,0)},S[2])
new("Part",V[2],{Name="Hedge",CFrame=cf(172.06,2,172.016,0,30,0)},S[5])
new("Part",V[2],{Name="Hedge",CFrame=cf(62.94,2,235.016,0,30,0)},S[5])
new("Part",V[2],{Name="Hedge",CFrame=cf(149,2,258.076,0,30,0)},S[6])
new("Part",V[1],{Name="Base",CFrame=cf(117.5,0.2,203.516,0,30,0)},S[7])
new("Folder",V[1],{Name="Pieces"})
new("Folder",V[1],{Name="Customers"})
V[3]=new("Part",V[1],{Name="Sign",CFrame=cf(86,9.4,148.956,0,30,0)},S[8])
V[4]=new("SurfaceGui",V[3],{Name="SignGui"},S[9])
new("TextLabel",V[4],{Name="Label",Text="Free plot"},S[10])
V[1].WorldPivot=cf(117.35,5.5,203.256,0,30,0)
V[1].PrimaryPart=V[1]:FindFirstChild("Base")
V[5]=new("Model",V[0],{Name="Plot2",_attrs={["PlotIndex"]=2}})
new("Folder",V[5],{Name="Pieces"})
V[6]=new("Folder",V[5],{Name="Decor"})
new("Part",V[6],{Name="GatePillar",CFrame=cf(172,5.2,-9,0,90,0)},S[2])
new("Part",V[6],{Name="EntrancePath",CFrame=cf(185,0.45,0,0,90,0)},S[3])
new("Part",V[6],{Name="GatePillar",CFrame=cf(172,5.2,9,0,90,0)},S[2])
new("Part",V[6],{Name="GateCap",CFrame=cf(172,10.6,-9,0,90,0)},S[4])
new("Part",V[6],{Name="Hedge",CFrame=cf(172,2,36,0,90,0)},S[1])
new("Part",V[6],{Name="Hedge",CFrame=cf(172,2,-36,0,90,0)},S[1])
new("Part",V[6],{Name="GateCap",CFrame=cf(172,10.6,9,0,90,0)},S[4])
new("Part",V[6],{Name="Hedge",CFrame=cf(235,2,-63,0,90,0)},S[5])
new("Part",V[6],{Name="Hedge",CFrame=cf(298,2,0,0,90,0)},S[6])
new("Part",V[6],{Name="Hedge",CFrame=cf(235,2,63,0,90,0)},S[5])
new("Folder",V[5],{Name="Customers"})
V[7]=new("Part",V[5],{Name="Sign",CFrame=cf(172,9.4,0,0,90,0)},S[8])
V[8]=new("SurfaceGui",V[7],{Name="SignGui"},S[9])
new("TextLabel",V[8],{Name="Label",Text="Free plot"},S[10])
new("Part",V[5],{Name="Base",CFrame=cf(235,0.2,0,0,90,0)},S[7])
V[5].WorldPivot=cf(234.7,5.5,0,0,90,0)
V[5].PrimaryPart=V[5]:FindFirstChild("Base")
V[9]=new("Model",V[0],{Name="Plot3",_attrs={["PlotIndex"]=3}})
new("Folder",V[9],{Name="Customers"})
new("Folder",V[9],{Name="Pieces"})
V[10]=new("Folder",V[9],{Name="Decor"})
new("Part",V[10],{Name="Hedge",CFrame=cf(149,2,-258.076,0,150,0)},S[6])
new("Part",V[10],{Name="EntrancePath",CFrame=cf(92.5,0.45,-160.215,0,150,0)},S[3])
new("Part",V[10],{Name="Hedge",CFrame=cf(117.177,2,-130.956,0,150,0)},S[1])
new("Part",V[10],{Name="Hedge",CFrame=cf(62.94,2,-235.016,0,150,0)},S[5])
new("Part",V[10],{Name="GateCap",CFrame=cf(78.206,10.6,-153.456,0,150,0)},S[4])
new("Part",V[10],{Name="GateCap",CFrame=cf(93.794,10.6,-144.456,0,150,0)},S[4])
new("Part",V[10],{Name="Hedge",CFrame=cf(172.06,2,-172.016,0,150,0)},S[5])
new("Part",V[10],{Name="GatePillar",CFrame=cf(78.206,5.2,-153.456,0,150,0)},S[2])
new("Part",V[10],{Name="GatePillar",CFrame=cf(93.794,5.2,-144.456,0,150,0)},S[2])
new("Part",V[10],{Name="Hedge",CFrame=cf(54.823,2,-166.956,0,150,0)},S[1])
V[11]=new("Part",V[9],{Name="Sign",CFrame=cf(86,9.4,-148.956,0,150,0)},S[8])
V[12]=new("SurfaceGui",V[11],{Name="SignGui"},S[9])
new("TextLabel",V[12],{Name="Label",Text="Free plot"},S[10])
new("Part",V[9],{Name="Base",CFrame=cf(117.5,0.2,-203.516,0,150,0)},S[7])
V[9].WorldPivot=cf(117.35,5.5,-203.256,0,150,0)
V[9].PrimaryPart=V[9]:FindFirstChild("Base")
V[13]=new("Model",V[0],{Name="Plot4",_attrs={["PlotIndex"]=4}})
new("Part",V[13],{Name="Base",CFrame=cf(-117.5,0.2,-203.516,0,-150,0)},S[7])
new("Folder",V[13],{Name="Pieces"})
new("Folder",V[13],{Name="Customers"})
V[14]=new("Folder",V[13],{Name="Decor"})
new("Part",V[14],{Name="Hedge",CFrame=cf(-54.823,2,-166.956,0,-150,0)},S[1])
new("Part",V[14],{Name="Hedge",CFrame=cf(-117.177,2,-130.956,0,-150,0)},S[1])
new("Part",V[14],{Name="Hedge",CFrame=cf(-62.94,2,-235.016,0,-150,0)},S[5])
new("Part",V[14],{Name="Hedge",CFrame=cf(-172.06,2,-172.016,0,-150,0)},S[5])
new("Part",V[14],{Name="GatePillar",CFrame=cf(-78.206,5.2,-153.456,0,-150,0)},S[2])
new("Part",V[14],{Name="EntrancePath",CFrame=cf(-92.5,0.45,-160.215,0,-150,0)},S[3])
new("Part",V[14],{Name="Hedge",CFrame=cf(-149,2,-258.076,0,-150,0)},S[6])
new("Part",V[14],{Name="GatePillar",CFrame=cf(-93.794,5.2,-144.456,0,-150,0)},S[2])
new("Part",V[14],{Name="GateCap",CFrame=cf(-78.206,10.6,-153.456,0,-150,0)},S[4])
new("Part",V[14],{Name="GateCap",CFrame=cf(-93.794,10.6,-144.456,0,-150,0)},S[4])
V[15]=new("Part",V[13],{Name="Sign",CFrame=cf(-86,9.4,-148.956,0,-150,0)},S[8])
V[16]=new("SurfaceGui",V[15],{Name="SignGui"},S[9])
new("TextLabel",V[16],{Name="Label",Text="Free plot"},S[10])
V[13].WorldPivot=cf(-117.35,5.5,-203.256,0,-150,0)
V[13].PrimaryPart=V[13]:FindFirstChild("Base")
V[17]=new("Model",V[0],{Name="Plot5",_attrs={["PlotIndex"]=5}})
new("Folder",V[17],{Name="Pieces"})
V[18]=new("Folder",V[17],{Name="Decor"})
new("Part",V[18],{Name="GateCap",CFrame=cf(-172,10.6,9,0,-90,0)},S[4])
new("Part",V[18],{Name="Hedge",CFrame=cf(-172,2,36,0,-90,0)},S[1])
new("Part",V[18],{Name="Hedge",CFrame=cf(-235,2,-63,0,-90,0)},S[5])
new("Part",V[18],{Name="GatePillar",CFrame=cf(-172,5.2,-9,0,-90,0)},S[2])
new("Part",V[18],{Name="Hedge",CFrame=cf(-172,2,-36,0,-90,0)},S[1])
new("Part",V[18],{Name="GatePillar",CFrame=cf(-172,5.2,9,0,-90,0)},S[2])
new("Part",V[18],{Name="EntrancePath",CFrame=cf(-185,0.45,0,0,-90,0)},S[3])
new("Part",V[18],{Name="Hedge",CFrame=cf(-235,2,63,0,-90,0)},S[5])
new("Part",V[18],{Name="Hedge",CFrame=cf(-298,2,0,0,-90,0)},S[6])
new("Part",V[18],{Name="GateCap",CFrame=cf(-172,10.6,-9,0,-90,0)},S[4])
new("Folder",V[17],{Name="Customers"})
V[19]=new("Part",V[17],{Name="Sign",CFrame=cf(-172,9.4,0,0,-90,0)},S[8])
V[20]=new("SurfaceGui",V[19],{Name="SignGui"},S[9])
new("TextLabel",V[20],{Name="Label",Text="Free plot"},S[10])
new("Part",V[17],{Name="Base",CFrame=cf(-235,0.2,0,0,-90,0)},S[7])
V[17].WorldPivot=cf(-234.7,5.5,0,0,-90,0)
V[17].PrimaryPart=V[17]:FindFirstChild("Base")
V[21]=new("Model",V[0],{Name="Plot6",_attrs={["PlotIndex"]=6}})
new("Folder",V[21],{Name="Pieces"})
new("Folder",V[21],{Name="Customers"})
V[22]=new("Folder",V[21],{Name="Decor"})
new("Part",V[22],{Name="GatePillar",CFrame=cf(-78.206,5.2,153.456,0,-30,0)},S[2])
new("Part",V[22],{Name="GateCap",CFrame=cf(-78.206,10.6,153.456,0,-30,0)},S[4])
new("Part",V[22],{Name="Hedge",CFrame=cf(-117.177,2,130.956,0,-30,0)},S[1])
new("Part",V[22],{Name="EntrancePath",CFrame=cf(-92.5,0.45,160.215,0,-30,0)},S[3])
new("Part",V[22],{Name="Hedge",CFrame=cf(-54.823,2,166.956,0,-30,0)},S[1])
new("Part",V[22],{Name="Hedge",CFrame=cf(-149,2,258.076,0,-30,0)},S[6])
new("Part",V[22],{Name="Hedge",CFrame=cf(-62.94,2,235.016,0,-30,0)},S[5])
new("Part",V[22],{Name="GatePillar",CFrame=cf(-93.794,5.2,144.456,0,-30,0)},S[2])
new("Part",V[22],{Name="GateCap",CFrame=cf(-93.794,10.6,144.456,0,-30,0)},S[4])
new("Part",V[22],{Name="Hedge",CFrame=cf(-172.06,2,172.016,0,-30,0)},S[5])
new("Part",V[21],{Name="Base",CFrame=cf(-117.5,0.2,203.516,0,-30,0)},S[7])
V[23]=new("Part",V[21],{Name="Sign",CFrame=cf(-86,9.4,148.956,0,-30,0)},S[8])
V[24]=new("SurfaceGui",V[23],{Name="SignGui"},S[9])
new("TextLabel",V[24],{Name="Label",Text="Free plot"},S[10])
V[21].WorldPivot=cf(-117.35,5.5,203.256,0,-30,0)
V[21].PrimaryPart=V[21]:FindFirstChild("Base")
```

### Plots (ServerScriptService > Server > Plots), 214 lines

Gives each player a plot, builds their restaurant piece by piece, and answers questions like "which table does this chair face?" and "how much fits in the fridges?".

```lua
-- Plots: who owns which plot, the pieces placed on it (walls, chairs, ovens...) and the restaurant's stock.
-- Positions on a plot use plot coordinates: x/z in studs from the plot centre, negative z = towards the street.
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Config = require(ReplicatedStorage.Shared.Config)
local PieceBuilder = require(ReplicatedStorage.Shared.PieceBuilder)

local Plots = {}
Plots.list = {}
local byPlayer = {}

-- Other modules hook in here instead of requiring each other.
Plots.onPieceAdded = {} -- fn(plot, piece)
Plots.onPieceRemoved = {} -- fn(plot, piece)
Plots.onAssigned = {} -- fn(plot)
Plots.onReleased = {} -- fn(plot), called while plot.owner is still set

function Plots.init()
	for _, model in workspace.Plots:GetChildren() do
		local index = model:GetAttribute("PlotIndex")
		local base = model:FindFirstChild("Base")
		if index and base then
			Plots.list[index] = {
				index = index,
				model = model,
				cf = base.CFrame * CFrame.new(0, -base.Size.Y / 2, 0), -- ground centre, -Z = towards the street
				owner = nil,
				pieces = {},
				nextUid = 1,
				stock = {},
				customers = {},
				open = false,
			}
		end
	end
end

function Plots.ofPlayer(player)
	return byPlayer[player]
end

local function setSign(plot, text)
	local sign = plot.model:FindFirstChild("Sign")
	local gui = sign and sign:FindFirstChild("SignGui")
	local label = gui and gui:FindFirstChild("Label")
	if label then
		label.Text = text
	end
end

-- The base CFrame of a piece in plot coordinates (floor pieces lie on the ground, the rest on the floor).
function Plots.localCF(id, x, z, rot)
	local def = Config.Pieces[id]
	local y = def.layer == "floor" and Config.GroundY or Config.FloorY
	return CFrame.new(x, y, z) * CFrame.Angles(0, math.rad(rot or 0), 0)
end

function Plots.toWorld(plot, localPos)
	return plot.cf * localPos
end

-- skins = { front, back } look for walls (see PieceBuilder)
function Plots.place(plot, id, x, z, rot, skins)
	local def = Config.Pieces[id]
	if not def then
		return nil
	end
	local localCF = Plots.localCF(id, x, z, rot)
	local model = PieceBuilder.build(id, { skins = skins })
	PieceBuilder.place(model, plot.cf * localCF)
	local uid = plot.nextUid
	plot.nextUid += 1
	model:SetAttribute("Uid", uid)
	model:SetAttribute("X", x)
	model:SetAttribute("Z", z)
	model:SetAttribute("Rot", rot or 0)
	if id == "entrance" and plot.owner then
		local ownerLabel = model:FindFirstChild("OwnerLabel", true)
		if ownerLabel then
			ownerLabel.Text = plot.owner.DisplayName .. "'s"
		end
	end
	model.Parent = plot.model.Pieces
	local piece = { uid = uid, id = id, def = def, plot = plot, x = x, z = z, rot = rot or 0, skins = skins, localCF = localCF, model = model }
	plot.pieces[uid] = piece
	for _, fn in Plots.onPieceAdded do
		fn(plot, piece)
	end
	return piece
end

function Plots.removePiece(plot, uid)
	local piece = plot.pieces[uid]
	if not piece then
		return
	end
	for _, fn in Plots.onPieceRemoved do
		fn(plot, piece)
	end
	plot.pieces[uid] = nil
	piece.model:Destroy()
end

function Plots.clearPieces(plot)
	for uid in plot.pieces do
		Plots.removePiece(plot, uid)
	end
end

-- Gives the player the first free plot and builds their restaurant: the saved layout (a list of
-- { id, x, z, rot, skins } from SaveService) or, without one, the starter restaurant.
-- Returns the plot or nil when all are taken (or the player left while it was being built).
function Plots.assign(player, layout)
	for i = 1, #Plots.list do
		local plot = Plots.list[i]
		if not plot.owner then
			plot.owner = player
			plot.open = false
			plot.stock = {}
			plot.nextUid = 1
			byPlayer[player] = plot
			player:SetAttribute("PlotIndex", i)
			player:SetAttribute("Open", false)
			setSign(plot, player.DisplayName .. "'s Pizzeria")
			plot.builtFromSave = type(layout) == "table" and #layout > 0
			for n, entry in if plot.builtFromSave then layout else Config.StarterLayout do
				if type(entry) == "table" and Config.Pieces[entry.id] and type(entry.x) == "number" and type(entry.z) == "number" then
					Plots.place(plot, entry.id, entry.x, entry.z, tonumber(entry.rot) or 0, if type(entry.skins) == "table" then entry.skins else nil)
				end
				if n % 15 == 0 then
					task.wait()
					if plot.owner ~= player then
						return nil -- the player left while the restaurant was being built
					end
				end
			end
			for _, fn in Plots.onAssigned do
				fn(plot)
			end
			return plot
		end
	end
	return nil
end

function Plots.release(player)
	local plot = byPlayer[player]
	if not plot then
		return
	end
	for _, fn in Plots.onReleased do
		fn(plot)
	end
	byPlayer[player] = nil
	plot.owner = nil
	plot.open = false
	Plots.clearPieces(plot)
	plot.stock = {}
	setSign(plot, "Free plot")
end

-- Puts the player in front of their restaurant door.
function Plots.home(player)
	local plot = byPlayer[player]
	local character = player.Character
	if plot and character and character:FindFirstChild("HumanoidRootPart") then
		character:PivotTo(plot.cf * CFrame.new(0, 4, -56) * CFrame.Angles(0, math.rad(180), 0))
	end
end

-- The table a chair faces, or nil. A point 2 studs in front of the chair must be on (or just next to) a table.
function Plots.tableFor(plot, chair)
	local probe = (chair.localCF * CFrame.new(0, 0, -2)).Position
	for _, p in plot.pieces do
		if p.def.isTable then
			local rel = p.localCF:PointToObjectSpace(probe)
			if math.abs(rel.X) <= p.def.size.X / 2 + 0.75 and math.abs(rel.Z) <= p.def.size.Z / 2 + 0.75 then
				return p
			end
		end
	end
	return nil
end

-- Free chairs that stand in front of a table.
function Plots.freeSeats(plot)
	local seats = {}
	for _, p in plot.pieces do
		if p.def.isChair and not p.occupant and Plots.tableFor(plot, p) then
			table.insert(seats, p)
		end
	end
	return seats
end

function Plots.stockCount(plot)
	local n = 0
	for _, v in plot.stock do
		n += v
	end
	return n
end

function Plots.capacity(plot)
	local fridges = 0
	for _, p in plot.pieces do
		if p.def.station == "fridge" then
			fridges += 1
		end
	end
	return fridges * Config.FridgeCapacity
end

return Plots
```

### Placement (ReplicatedStorage > Shared > Placement), 73 lines

The build-mode rules, shared by the green/red preview on the player's screen and the real check on the server.

```lua
-- Placement: the rules for placing pieces on a plot, shared by the client (green/red preview)
-- and the server (the real check). Positions are plot coordinates (x/z from the plot centre).
local Config = require(script.Parent.Config)

local Placement = {}

Placement.PlotHalf = 61 -- you can build up to this far from the plot centre (inside the hedges)
Placement.ChunkSize = 4 -- the grid lines shown while building

-- width and depth of a piece after turning it (rot in degrees: 0, 90, 180, 270)
function Placement.footprint(id, rot)
	local size = Config.Pieces[id].size
	if (rot or 0) % 180 == 90 then
		return size.Z, size.X
	end
	return size.X, size.Z
end

function Placement.normalRot(rot)
	rot = math.floor((rot or 0) / 90 + 0.5) * 90
	return rot % 360
end

-- Floors snap to the 16-stud floor grid; everything else to half studs.
function Placement.snap(id, x, z)
	local def = Config.Pieces[id]
	if def.layer == "floor" then
		return math.floor((x - 8) / 16 + 0.5) * 16 + 8, math.floor((z - 8) / 16 + 0.5) * 16 + 8
	end
	return math.floor(x * 2 + 0.5) / 2, math.floor(z * 2 + 0.5) / 2
end

-- floors only bump into floors; everything else bumps into walls and objects
local function group(id)
	return Config.Pieces[id].layer == "floor" and "floor" or "solid"
end

-- pieces = list of { uid, id, x, z, rot }. Returns true, or false + a reason.
function Placement.check(pieces, id, x, z, rot, ignoreUid)
	local def = Config.Pieces[id]
	if not def then
		return false, "Unknown item"
	end
	local w, d = Placement.footprint(id, rot)
	if math.abs(x) + w / 2 > Placement.PlotHalf or math.abs(z) + d / 2 > Placement.PlotHalf then
		return false, "Outside your plot"
	end
	local g = group(id)
	for _, p in pieces do
		if p.uid ~= ignoreUid and Config.Pieces[p.id] and group(p.id) == g then
			local pw, pd = Placement.footprint(p.id, p.rot)
			if math.abs(p.x - x) < (w + pw) / 2 - 0.05 and math.abs(p.z - z) < (d + pd) / 2 - 0.05 then
				return false, "Something is in the way"
			end
		end
	end
	return true
end

-- Reads the placed pieces of a plot model from the attributes Plots puts on every piece model.
function Placement.piecesOf(plotModel)
	local list = {}
	for _, m in plotModel.Pieces:GetChildren() do
		local uid = m:GetAttribute("Uid")
		if uid and Config.Pieces[m.Name] then
			table.insert(list, { uid = uid, id = m.Name, x = m:GetAttribute("X"), z = m:GetAttribute("Z"), rot = m:GetAttribute("Rot") or 0 })
		end
	end
	return list
end

return Placement
```

### PieceBuilder (ReplicatedStorage > Shared > PieceBuilder), 696 lines

Builds the 3D model of every piece from parts in the cozy Italian pizzeria style. A model in ReplicatedStorage > PieceModels with the same name as a piece id replaces the built one.

```lua
-- PieceBuilder: makes the 3D model of a placeable piece in the cozy Italian pizzeria style (2026-10-25).
-- If ReplicatedStorage.PieceModels has a Model named like the piece id (e.g. "chair"), that model is used
-- instead (made by the art friends, front = -Z). Walls have two looks ("skins"), one per side:
-- brick outside; dining (wood + cream), kitchen (white tiles), office, storage inside.
-- Parts with the attribute Paint are the ones players can recolour later.
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Config = require(script.Parent.Config)

local PieceBuilder = {}

local M = Enum.Material
local C = {
	brick = Color3.fromRGB(178, 88, 64),
	stone = Color3.fromRGB(222, 212, 192),
	cap = Color3.fromRGB(236, 226, 206),
	plaster = Color3.fromRGB(250, 236, 208),
	wainscot = Color3.fromRGB(142, 88, 52),
	darkwood = Color3.fromRGB(92, 56, 34),
	wood = Color3.fromRGB(176, 118, 72),
	honey = Color3.fromRGB(214, 152, 88),
	tile = Color3.fromRGB(244, 244, 240),
	tileBlue = Color3.fromRGB(150, 168, 190),
	steel = Color3.fromRGB(196, 201, 208),
	darksteel = Color3.fromRGB(120, 126, 134),
	shutter = Color3.fromRGB(58, 116, 72),
	red = Color3.fromRGB(204, 52, 44),
	white = Color3.fromRGB(250, 250, 246),
	leaf = Color3.fromRGB(70, 146, 58),
	leaf2 = Color3.fromRGB(92, 170, 70),
	glass = Color3.fromRGB(170, 215, 240),
	iron = Color3.fromRGB(48, 50, 54),
	terracotta = Color3.fromRGB(196, 108, 70),
	office = Color3.fromRGB(198, 214, 200),
	concrete = Color3.fromRGB(206, 204, 198),
	gold = Color3.fromRGB(232, 186, 70),
	warm = Color3.fromRGB(255, 214, 150),
	soil = Color3.fromRGB(96, 66, 42),
}
local FONT = Enum.Font.FredokaOne
local UP = CFrame.Angles(0, 0, math.rad(90)) -- turns a cylinder part upright

-- add a part; at = Vector3 (centre, y = 0 is the bottom of the piece) or a CFrame
local function add(model, size, at, color, material, props, paint)
	local p = Instance.new("Part")
	p.Anchored = true
	p.TopSurface = Enum.SurfaceType.Smooth
	p.BottomSurface = Enum.SurfaceType.Smooth
	p.Size = size
	p.CFrame = typeof(at) == "CFrame" and at or CFrame.new(at)
	p.Color = color
	p.Material = material or M.SmoothPlastic
	if props then
		for k, v in props do
			p[k] = v
		end
	end
	if paint then
		p:SetAttribute("Paint", paint == true and "main" or paint)
	end
	p.Parent = model
	return p
end

local NOCOLLIDE = { CanCollide = false }

local function cyl(model, height, diameter, pos, color, material, props, paint)
	local p = add(model, Vector3.new(height, diameter, diameter), CFrame.new(pos) * UP, color, material, props, paint)
	p.Shape = Enum.PartType.Cylinder
	return p
end

local function ball(model, d, pos, color, material)
	local p = add(model, Vector3.new(d, d, d), pos, color, material, NOCOLLIDE)
	p.Shape = Enum.PartType.Ball
	return p
end

local function label(part, face, text, color, ppS)
	local gui = Instance.new("SurfaceGui")
	gui.Face = face
	gui.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
	gui.PixelsPerStud = ppS or 40
	gui.LightInfluence = 0
	gui.Parent = part
	local l = Instance.new("TextLabel")
	l.Name = "Label"
	l.Size = UDim2.fromScale(1, 1)
	l.BackgroundTransparency = 1
	l.Text = text
	l.TextScaled = true
	l.Font = FONT
	l.TextColor3 = color
	l.Parent = gui
	return l, gui
end

local function light(part, range, brightness)
	local pl = Instance.new("PointLight")
	pl.Range = range or 14
	pl.Brightness = brightness or 0.9
	pl.Color = Color3.fromRGB(255, 210, 150)
	pl.Parent = part
end

---------------------------------------------------------------- walls
-- bands from the floor (0) to the top (12): { y0, y1, colour, material }
local SKINS = {
	brick = { { 0, 1.6, C.stone, M.Slate }, { 1.6, 12, C.brick, M.Brick } },
	dining = { { 0, 0.5, C.darkwood, M.Wood }, { 0.5, 3.6, C.wainscot, M.WoodPlanks }, { 3.6, 3.9, C.darkwood, M.Wood }, { 3.9, 12, C.plaster, M.Plaster } },
	kitchen = { { 0, 0.6, C.darksteel, M.Metal }, { 0.6, 12, C.tile, M.CeramicTiles } },
	office = { { 0, 0.6, C.darkwood, M.Wood }, { 0.6, 12, C.office, M.Plaster } },
	storage = { { 0, 12, C.concrete, M.Concrete } },
}
local MAIN_BAND = { brick = 2, dining = 4, kitchen = 2, office = 2, storage = 1 }

-- rects = { {x0, x1, y0, y1}, ... } in wall coordinates (x across the wall, y up)
local function wallBody(m, rects, width, skins)
	local front = skins and skins[1] or "dining"
	local back = skins and skins[2] or front
	for _, r in rects do
		local x0, x1, y0, y1 = r[1], r[2], r[3], r[4]
		local w = x1 - x0
		local cx = (x0 + x1) / 2
		add(m, Vector3.new(w, y1 - y0, 0.6), Vector3.new(cx, (y0 + y1) / 2, 0), C.cap)
		for _, side in { { -1, front, "front" }, { 1, back, "back" } } do
			local skin = SKINS[side[2]] or SKINS.dining
			for bi, band in skin do
				local b0, b1 = math.max(band[1], y0), math.min(band[2], y1)
				if b1 - b0 > 0.01 then
					add(m, Vector3.new(w, b1 - b0, 0.2), Vector3.new(cx, (b0 + b1) / 2, side[1] * 0.4), band[3], band[4], nil,
						bi == MAIN_BAND[side[2]] and side[3] or nil)
				end
			end
		end
	end
	add(m, Vector3.new(width, 0.5, 1.4), Vector3.new(0, 12.25, 0), C.cap, M.Slate)
end

-- which side (-1 front / 1 back) is the outside (brick), or nil for inner walls
local function outside(skins)
	if skins and skins[1] == "brick" then
		return -1
	elseif skins and skins[2] == "brick" then
		return 1
	end
	return nil
end

-- red / white striped awning sticking out of the wall on `side`, sloping down
local function awning(m, width, y, side)
	local n = math.max(2, math.floor(width / 1.25))
	local stripe = width / n
	for i = 0, n - 1 do
		local x = -width / 2 + stripe * (i + 0.5)
		add(m, Vector3.new(stripe, 0.15, 2.6), CFrame.new(x, y - 0.5, side * 1.65) * CFrame.Angles(math.rad(side * 25), 0, 0),
			(i % 2 == 0) and C.red or C.white, M.Fabric, NOCOLLIDE)
	end
	add(m, Vector3.new(width, 0.5, 0.1), Vector3.new(0, y - 1.35, side * 2.85), C.red, M.Fabric, NOCOLLIDE)
end

local FLOWERS = { C.red, Color3.fromRGB(255, 200, 60), C.white, Color3.fromRGB(230, 90, 160) }

local function flowerBox(m, width, y, side)
	add(m, Vector3.new(width, 0.7, 0.8), Vector3.new(0, y, side * 0.95), C.darkwood, M.Wood, NOCOLLIDE)
	local n = math.floor(width / 0.8)
	for i = 0, n - 1 do
		local x = -width / 2 + 0.4 + i * 0.8
		ball(m, 0.7, Vector3.new(x, y + 0.45, side * 0.95), C.leaf, M.Grass)
		ball(m, 0.5, Vector3.new(x, y + 0.75, side * 1.0), FLOWERS[(i % #FLOWERS) + 1])
	end
end

local function shutters(m, x0, x1, y0, y1, side)
	for _, x in { x0 - 0.75, x1 + 0.75 } do
		add(m, Vector3.new(1.4, y1 - y0, 0.15), Vector3.new(x, (y0 + y1) / 2, side * 0.6), C.shutter, M.Wood, NOCOLLIDE)
		for k = 1, 5 do
			add(m, Vector3.new(1.2, 0.08, 0.06), Vector3.new(x, y0 + k * (y1 - y0) / 6, side * 0.7), Color3.fromRGB(40, 86, 52), M.Wood, NOCOLLIDE)
		end
	end
end

local builders = {}

builders.wall = function(m, opts)
	wallBody(m, { { -4, 4, 0, 12 } }, 8, opts.skins)
end

builders.wall_window = function(m, opts)
	wallBody(m, { { -4, 4, 0, 3 }, { -4, 4, 9, 12 }, { -4, -2.6, 3, 9 }, { 2.6, 4, 3, 9 } }, 8, opts.skins)
	add(m, Vector3.new(5.2, 6, 0.15), Vector3.new(0, 6, 0), C.glass, M.Glass, { Transparency = 0.55 })
	add(m, Vector3.new(6, 0.35, 1.5), Vector3.new(0, 2.9, 0), C.cap, M.Slate)
	add(m, Vector3.new(5.4, 0.3, 1.2), Vector3.new(0, 9.1, 0), C.white, M.Wood)
	add(m, Vector3.new(0.25, 6, 1.1), Vector3.new(-2.65, 6, 0), C.white, M.Wood)
	add(m, Vector3.new(0.25, 6, 1.1), Vector3.new(2.65, 6, 0), C.white, M.Wood)
	add(m, Vector3.new(0.2, 6, 0.4), Vector3.new(0, 6, 0), C.white, M.Wood)
	add(m, Vector3.new(5.2, 0.2, 0.4), Vector3.new(0, 6.2, 0), C.white, M.Wood)
	local side = outside(opts.skins)
	if side then
		shutters(m, -2.6, 2.6, 3.1, 8.9, side)
		flowerBox(m, 5.2, 2.4, side)
		awning(m, 6.4, 10.4, side)
	end
end

builders.wall_door = function(m, opts)
	wallBody(m, { { -4, -2.2, 0, 12 }, { 2.2, 4, 0, 12 }, { -2.2, 2.2, 9, 12 } }, 8, opts.skins)
	add(m, Vector3.new(0.4, 9, 1.3), Vector3.new(-2.2, 4.5, 0), C.darkwood, M.Wood)
	add(m, Vector3.new(0.4, 9, 1.3), Vector3.new(2.2, 4.5, 0), C.darkwood, M.Wood)
	add(m, Vector3.new(4.8, 0.4, 1.3), Vector3.new(0, 9.1, 0), C.darkwood, M.Wood)
end

-- serving hatch ("the pass"): steel shelf + heat lamps between kitchen and dining room
builders.wall_pass = function(m, opts)
	wallBody(m, { { -4, 4, 0, 3.6 }, { -4, 4, 8.4, 12 }, { -4, -3, 3.6, 8.4 }, { 3, 4, 3.6, 8.4 } }, 8, opts.skins)
	add(m, Vector3.new(7, 0.3, 2.4), Vector3.new(0, 3.75, 0), C.steel, M.Metal)
	add(m, Vector3.new(6.2, 0.3, 0.8), Vector3.new(0, 8.2, 0), C.darksteel, M.Metal)
	for _, x in { -1.8, 0, 1.8 } do
		local lamp = add(m, Vector3.new(0.7, 0.25, 0.7), Vector3.new(x, 7.95, 0), Color3.fromRGB(255, 150, 60), M.Neon)
		if x == 0 then
			light(lamp, 8, 0.6)
		end
	end
	local bell = cyl(m, 0.4, 0.5, Vector3.new(2.6, 4.1, 0), C.gold, M.Metal)
	bell.Shape = Enum.PartType.Ball
	bell.Size = Vector3.new(0.5, 0.5, 0.5)
end

-- the big entrance: 10-wide opening, open glass doors, awning, lanterns and the PIZZERIA sign
builders.entrance = function(m, opts)
	wallBody(m, { { -8, -5, 0, 12 }, { 5, 8, 0, 12 }, { -5, 5, 9.5, 12 } }, 16, opts.skins)
	local side = outside(opts.skins) or -1
	local inside = -side
	add(m, Vector3.new(0.6, 9.5, 1.5), Vector3.new(-5, 4.75, 0), C.cap, M.Slate)
	add(m, Vector3.new(0.6, 9.5, 1.5), Vector3.new(5, 4.75, 0), C.cap, M.Slate)
	add(m, Vector3.new(10.6, 0.6, 1.5), Vector3.new(0, 9.5, 0), C.cap, M.Slate)
	for _, s in { -1, 1 } do
		-- open glass door leaves (no collision)
		local hinge = Vector3.new(s * 4.6, 4.6, inside * 0.3)
		add(m, Vector3.new(0.15, 9, 4.4), CFrame.new(hinge + Vector3.new(0, 0, inside * 2.2)), C.glass, M.Glass, { Transparency = 0.5, CanCollide = false })
		add(m, Vector3.new(0.25, 9.2, 0.25), CFrame.new(hinge + Vector3.new(0, 0, inside * 4.4)), C.darkwood, M.Wood, NOCOLLIDE)
		-- lanterns
		add(m, Vector3.new(0.3, 1.2, 0.6), Vector3.new(s * 6.5, 7, side * 0.75), C.iron, M.Metal, NOCOLLIDE)
		local lantern = add(m, Vector3.new(0.8, 1.2, 0.8), Vector3.new(s * 6.5, 6.6, side * 1.2), C.warm, M.Neon, NOCOLLIDE)
		light(lantern, 14, 0.8)
	end
	add(m, Vector3.new(6, 0.06, 3), Vector3.new(0, 0.03, side * 2), Color3.fromRGB(150, 40, 36), M.Fabric, NOCOLLIDE)
	awning(m, 12, 11.2, side)
	-- sign above the wall
	local board = add(m, Vector3.new(15, 3.6, 0.5), Vector3.new(0, 14.4, side * 0.2), C.cap, M.Slate)
	add(m, Vector3.new(15.6, 4.2, 0.4), Vector3.new(0, 14.4, -side * 0.15), C.red, M.SmoothPlastic)
	local face = side < 0 and Enum.NormalId.Front or Enum.NormalId.Back
	local gui = Instance.new("SurfaceGui")
	gui.Name = "SignGui"
	gui.Face = face
	gui.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
	gui.PixelsPerStud = 40
	gui.LightInfluence = 0
	gui.Parent = board
	local owner = Instance.new("TextLabel")
	owner.Name = "OwnerLabel"
	owner.Size = UDim2.fromScale(1, 0.32)
	owner.BackgroundTransparency = 1
	owner.Text = ""
	owner.TextScaled = true
	owner.Font = FONT
	owner.TextColor3 = Color3.fromRGB(60, 120, 70)
	owner.Parent = gui
	local title = Instance.new("TextLabel")
	title.Name = "Title"
	title.Position = UDim2.fromScale(0, 0.3)
	title.Size = UDim2.fromScale(1, 0.7)
	title.BackgroundTransparency = 1
	title.Text = "PIZZERIA"
	title.TextScaled = true
	title.Font = FONT
	title.TextColor3 = C.red
	title.Parent = gui
	for _, x in { -6.5, 6.5 } do
		add(m, Vector3.new(0.4, 2.2, 0.4), Vector3.new(x, 12.4, side * 0.2), C.iron, M.Metal, NOCOLLIDE)
	end
end

---------------------------------------------------------------- floors (16 x 16)
builders.floor_wood = function(m)
	add(m, Vector3.new(16, 0.12, 16), Vector3.new(0, 0.06, 0), C.darkwood)
	local shades = { Color3.fromRGB(206, 144, 82), C.honey, Color3.fromRGB(222, 162, 98) }
	for i = 0, 7 do
		add(m, Vector3.new(16, 0.08, 1.9), Vector3.new(0, 0.16, -7 + i * 2), shades[(i % 3) + 1], M.WoodPlanks, nil, true)
	end
end

builders.floor_kitchen = function(m)
	add(m, Vector3.new(16, 0.12, 16), Vector3.new(0, 0.06, 0), Color3.fromRGB(90, 96, 104))
	for ix = 0, 3 do
		for iz = 0, 3 do
			local lightTile = (ix + iz) % 2 == 0
			add(m, Vector3.new(3.92, 0.08, 3.92), Vector3.new(-6 + ix * 4, 0.16, -6 + iz * 4), lightTile and C.tile or C.tileBlue, M.CeramicTiles, nil, lightTile)
		end
	end
end

builders.floor_office = function(m)
	add(m, Vector3.new(16, 0.12, 16), Vector3.new(0, 0.06, 0), C.darkwood, M.Wood)
	add(m, Vector3.new(15.4, 0.08, 15.4), Vector3.new(0, 0.16, 0), Color3.fromRGB(122, 48, 50), M.Carpet, nil, true)
end

builders.floor_storage = function(m)
	add(m, Vector3.new(16, 0.2, 16), Vector3.new(0, 0.1, 0), Color3.fromRGB(176, 176, 172), M.Concrete, nil, true)
end

builders.floor_terrace = function(m)
	add(m, Vector3.new(16, 0.12, 16), Vector3.new(0, 0.06, 0), Color3.fromRGB(150, 140, 126))
	for ix = 0, 3 do
		for iz = 0, 3 do
			local shade = ((ix * 3 + iz) % 3 == 0) and Color3.fromRGB(214, 200, 176) or Color3.fromRGB(226, 214, 192)
			add(m, Vector3.new(3.85, 0.08, 3.85), Vector3.new(-6 + ix * 4, 0.16, -6 + iz * 4), shade, M.Slate, nil, true)
		end
	end
end

---------------------------------------------------------------- dining
local function checkeredTable(m, topY)
	add(m, Vector3.new(4, 0.2, 4), Vector3.new(0, topY - 0.1, 0), C.wood, M.Wood)
	for ix = 0, 3 do
		for iz = 0, 3 do
			local redSquare = (ix + iz) % 2 == 0
			add(m, Vector3.new(1, 0.06, 1), Vector3.new(-1.5 + ix, topY + 0.03, -1.5 + iz), redSquare and C.red or C.white, M.Fabric, nil, redSquare)
		end
	end
	for _, e in { { Vector3.new(4.1, 0.6, 0.06), Vector3.new(0, topY - 0.3, -2.03) }, { Vector3.new(4.1, 0.6, 0.06), Vector3.new(0, topY - 0.3, 2.03) },
		{ Vector3.new(0.06, 0.6, 4.1), Vector3.new(-2.03, topY - 0.3, 0) }, { Vector3.new(0.06, 0.6, 4.1), Vector3.new(2.03, topY - 0.3, 0) } } do
		add(m, e[1], e[2], C.red, M.Fabric, nil, true)
	end
	cyl(m, 0.5, 0.35, Vector3.new(0, topY + 0.3, 0), C.white)
	add(m, Vector3.new(0.12, 0.25, 0.12), Vector3.new(0, topY + 0.65, 0), Color3.fromRGB(255, 190, 80), M.Neon, NOCOLLIDE)
end

builders.table = function(m)
	add(m, Vector3.new(1.6, 0.2, 1.6), Vector3.new(0, 0.1, 0), C.iron, M.Metal)
	add(m, Vector3.new(0.4, 2.6, 0.4), Vector3.new(0, 1.4, 0), C.iron, M.Metal)
	checkeredTable(m, 2.95)
end

builders.umbrella_table = function(m)
	builders.table(m)
	add(m, Vector3.new(0.25, 6.2, 0.25), Vector3.new(0, 6, 0), C.white, M.Metal, NOCOLLIDE)
	local canopy = cyl(m, 0.3, 6.4, Vector3.new(0, 8.9, 0), C.red, M.Fabric, NOCOLLIDE, true)
	for i = 0, 3 do
		add(m, Vector3.new(6.2, 0.06, 0.5), CFrame.new(0, 9.08, 0) * CFrame.Angles(0, math.rad(i * 45), 0), C.white, M.Fabric, NOCOLLIDE)
	end
	ball(m, 0.5, Vector3.new(0, 9.3, 0), C.white)
	canopy.Name = "Canopy"
end

builders.chair = function(m)
	for _, x in { -0.75, 0.75 } do
		for _, z in { -0.75, 0.75 } do
			add(m, Vector3.new(0.2, 1.7, 0.2), Vector3.new(x, 0.85, z), C.darkwood, M.Wood)
		end
	end
	add(m, Vector3.new(1.9, 0.25, 1.9), Vector3.new(0, 1.8, 0), C.darkwood, M.Wood)
	add(m, Vector3.new(1.7, 0.2, 1.7), Vector3.new(0, 2.0, 0), C.red, M.Fabric, nil, true)
	for _, x in { -0.75, 0.75 } do
		add(m, Vector3.new(0.2, 2.2, 0.2), Vector3.new(x, 3.0, 0.8), C.darkwood, M.Wood)
	end
	add(m, Vector3.new(1.8, 0.35, 0.2), Vector3.new(0, 3.95, 0.8), C.darkwood, M.Wood)
	add(m, Vector3.new(1.6, 0.2, 0.15), Vector3.new(0, 3.1, 0.8), C.darkwood, M.Wood)
end

builders.host_stand = function(m)
	add(m, Vector3.new(2.2, 3.6, 1.4), Vector3.new(0, 1.8, 0), C.darkwood, M.Wood, nil, true)
	add(m, Vector3.new(2.4, 0.2, 1.6), CFrame.new(0, 3.75, 0) * CFrame.Angles(math.rad(-12), 0, 0), C.wood, M.Wood)
	add(m, Vector3.new(1.2, 0.12, 0.9), CFrame.new(0.2, 3.9, -0.1) * CFrame.Angles(math.rad(-12), 0, 0), C.red, M.Leather)
	add(m, Vector3.new(1.8, 0.12, 0.2), Vector3.new(0, 2.6, -0.72), C.gold, M.Metal)
end

---------------------------------------------------------------- kitchen
local function steelCounter(m)
	add(m, Vector3.new(4, 3.4, 3), Vector3.new(0, 1.7, 0), C.steel, M.Metal, nil, true)
	add(m, Vector3.new(4.2, 0.2, 3.2), Vector3.new(0, 3.5, 0), Color3.fromRGB(214, 218, 224), M.Metal)
	add(m, Vector3.new(0.06, 2.6, 0.05), Vector3.new(0, 1.7, -1.52), C.darksteel, M.Metal)
	for _, x in { -0.4, 0.4 } do
		add(m, Vector3.new(0.12, 0.6, 0.12), Vector3.new(x, 2.4, -1.6), C.darksteel, M.Metal)
	end
end

builders.counter = function(m)
	add(m, Vector3.new(4, 3.4, 3), Vector3.new(0, 1.7, 0), C.wood, M.Wood, nil, true)
	add(m, Vector3.new(4.2, 0.2, 3.2), Vector3.new(0, 3.5, 0), Color3.fromRGB(236, 236, 232), M.Marble)
end

builders.cutting_board = function(m)
	steelCounter(m)
	add(m, Vector3.new(2.8, 0.2, 1.8), Vector3.new(-0.3, 3.7, -0.1), Color3.fromRGB(222, 184, 135), M.Wood)
	add(m, Vector3.new(0.14, 0.05, 1.2), Vector3.new(1.45, 3.65, -0.2), Color3.fromRGB(210, 214, 220), M.Metal)
	add(m, Vector3.new(0.2, 0.14, 0.5), Vector3.new(1.45, 3.68, 0.6), C.darkwood, M.Wood)
	ball(m, 0.7, Vector3.new(-0.8, 4.15, -0.2), Color3.fromRGB(220, 50, 40))
	ball(m, 0.6, Vector3.new(0.1, 4.1, 0.2), Color3.fromRGB(60, 160, 60))
	cyl(m, 0.3, 0.6, Vector3.new(0.6, 3.95, -0.4), Color3.fromRGB(230, 220, 205))
end

builders.prep_table = function(m)
	steelCounter(m)
	add(m, Vector3.new(3, 0.15, 2), Vector3.new(-0.4, 3.68, -0.1), Color3.fromRGB(240, 240, 236), M.Marble)
	cyl(m, 0.15, 1.8, Vector3.new(-0.4, 3.82, -0.1), Color3.fromRGB(240, 215, 160))
	local bins = { Color3.fromRGB(200, 40, 30), Color3.fromRGB(255, 220, 90), Color3.fromRGB(60, 160, 60), Color3.fromRGB(240, 150, 150) }
	for i, col in bins do
		add(m, Vector3.new(0.8, 0.35, 0.6), Vector3.new(-1.6 + (i - 1) * 1.05, 3.78, 1.15), C.darksteel, M.Metal)
		add(m, Vector3.new(0.65, 0.1, 0.45), Vector3.new(-1.6 + (i - 1) * 1.05, 3.97, 1.15), col)
	end
end

-- wood-fired dome oven
builders.oven = function(m)
	add(m, Vector3.new(4, 2.4, 3), Vector3.new(0, 1.2, 0), C.stone, M.Slate, nil, true)
	add(m, Vector3.new(4.2, 0.4, 3.2), Vector3.new(0, 2.6, 0), C.cap, M.Slate)
	local dome = add(m, Vector3.new(3.2, 3.2, 3.2), Vector3.new(0, 2.9, 0.1), C.terracotta, M.Brick, nil, true)
	dome.Shape = Enum.PartType.Ball
	add(m, Vector3.new(1.7, 1.2, 0.5), Vector3.new(0, 3.3, -1.3), Color3.fromRGB(30, 20, 18))
	local fire = add(m, Vector3.new(1.3, 0.35, 0.3), Vector3.new(0, 2.95, -1.25), Color3.fromRGB(255, 130, 40), M.Neon)
	light(fire, 10, 1.2)
	add(m, Vector3.new(2.2, 0.25, 0.25), Vector3.new(0, 4.0, -1.45), C.cap, M.Slate)
	add(m, Vector3.new(2.6, 1.2, 0.25), Vector3.new(0, 1.0, -1.52), Color3.fromRGB(40, 30, 26))
	for i = 0, 2 do
		-- firewood logs lying along x
		local log = cyl(m, 2.2, 0.35, Vector3.new(0, 0.7 + i * 0.32, -1.5), Color3.fromRGB(120, 78, 46), M.Wood)
		log.CFrame = CFrame.new(0, 0.7 + i * 0.32, -1.5)
	end
	add(m, Vector3.new(0.7, 1.6, 0.7), Vector3.new(0, 4.9, 0.7), C.darksteel, M.Metal)
end

builders.fridge = function(m)
	add(m, Vector3.new(4, 7, 3), Vector3.new(0, 3.5, 0), C.steel, M.Metal, nil, true)
	add(m, Vector3.new(0.06, 6.4, 0.05), Vector3.new(0, 3.7, -1.52), C.darksteel)
	for _, x in { -0.35, 0.35 } do
		add(m, Vector3.new(0.2, 2.2, 0.25), Vector3.new(x, 4.2, -1.65), C.darksteel, M.Metal)
	end
	add(m, Vector3.new(3.6, 0.4, 0.05), Vector3.new(0, 6.65, -1.52), C.darksteel)
	add(m, Vector3.new(1.4, 0.5, 0.05), Vector3.new(-1, 6.05, -1.53), Color3.fromRGB(70, 170, 255), M.Neon)
end

builders.trash_bin = function(m)
	cyl(m, 2.6, 1.8, Vector3.new(0, 1.3, 0), C.steel, M.Metal, nil, true)
	cyl(m, 0.25, 1.9, Vector3.new(0, 2.7, 0), C.darksteel, M.Metal)
	add(m, Vector3.new(0.6, 0.15, 0.6), Vector3.new(0, 0.1, -1), C.darksteel, M.Metal)
end

builders.kitchen_shelf = function(m)
	for _, x in { -1.9, 1.9 } do
		add(m, Vector3.new(0.2, 7, 1.4), Vector3.new(x, 3.5, 0), C.steel, M.Metal)
	end
	local jars = { Color3.fromRGB(200, 40, 30), Color3.fromRGB(255, 220, 90), Color3.fromRGB(240, 215, 160), Color3.fromRGB(80, 160, 70), Color3.fromRGB(230, 230, 230) }
	for level = 0, 3 do
		local y = 0.4 + level * 2
		add(m, Vector3.new(3.8, 0.15, 1.4), Vector3.new(0, y, 0), C.steel, M.Metal, nil, level == 0)
		if level > 0 then
			for i = 0, 3 do
				cyl(m, 0.9, 0.7, Vector3.new(-1.3 + i * 0.85, y + 0.53, 0), jars[((level + i) % #jars) + 1], M.Glass)
			end
		end
	end
end

---------------------------------------------------------------- office
builders.manager_desk = function(m)
	add(m, Vector3.new(6, 0.4, 3), Vector3.new(0, 2.9, 0), C.wood, M.Wood, nil, true)
	add(m, Vector3.new(0.5, 2.7, 2.6), Vector3.new(-2.6, 1.35, 0), C.darkwood, M.Wood)
	add(m, Vector3.new(0.5, 2.7, 2.6), Vector3.new(2.6, 1.35, 0), C.darkwood, M.Wood)
	add(m, Vector3.new(4.6, 2.2, 0.15), Vector3.new(0, 1.6, 1.2), C.darkwood, M.Wood)
	add(m, Vector3.new(0.3, 0.6, 0.3), Vector3.new(0, 3.4, 0.6), Color3.fromRGB(60, 60, 70))
	add(m, Vector3.new(2.8, 1.8, 0.25), Vector3.new(0, 4.4, 0.6), Color3.fromRGB(45, 45, 55))
	local screen = add(m, Vector3.new(2.5, 1.5, 0.05), Vector3.new(0, 4.4, 0.46), Color3.fromRGB(70, 170, 255), M.Neon)
	label(screen, Enum.NormalId.Front, "📦 ORDERS", Color3.new(1, 1, 1), 60)
	add(m, Vector3.new(1.8, 0.1, 0.6), Vector3.new(0, 3.15, -0.5), Color3.fromRGB(80, 80, 90))
	add(m, Vector3.new(0.3, 0.9, 0.3), Vector3.new(2.3, 3.55, 0.6), C.iron, M.Metal)
	local shade = add(m, Vector3.new(0.9, 0.4, 0.6), Vector3.new(2.3, 4.1, 0.4), Color3.fromRGB(40, 120, 70), M.Glass)
	light(shade, 8, 0.5)
	add(m, Vector3.new(0.9, 0.2, 1.2), Vector3.new(-2, 3.2, -0.2), C.white)
end

builders.office_chair = function(m)
	cyl(m, 0.2, 1.6, Vector3.new(0, 0.1, 0), Color3.fromRGB(60, 60, 70))
	add(m, Vector3.new(0.3, 1.5, 0.3), Vector3.new(0, 0.95, 0), Color3.fromRGB(60, 60, 70))
	add(m, Vector3.new(2, 0.4, 2), Vector3.new(0, 1.9, 0), Color3.fromRGB(40, 40, 46), M.Leather, nil, true)
	add(m, Vector3.new(2, 2.4, 0.4), Vector3.new(0, 3.2, 0.8), Color3.fromRGB(40, 40, 46), M.Leather, nil, true)
end

builders.bookshelf = function(m)
	add(m, Vector3.new(4, 7, 0.2), Vector3.new(0, 3.5, 0.65), C.darkwood, M.Wood, nil, true)
	for _, x in { -1.9, 1.9 } do
		add(m, Vector3.new(0.2, 7, 1.4), Vector3.new(x, 3.5, 0), C.darkwood, M.Wood)
	end
	local books = { C.red, Color3.fromRGB(60, 110, 170), Color3.fromRGB(70, 140, 80), C.gold, Color3.fromRGB(120, 70, 140) }
	for level = 0, 3 do
		local y = 0.3 + level * 1.8
		add(m, Vector3.new(3.6, 0.15, 1.3), Vector3.new(0, y, 0), C.wood, M.Wood)
		for i = 0, 5 do
			add(m, Vector3.new(0.45, 1.2 + (i % 3) * 0.12, 1), Vector3.new(-1.4 + i * 0.55, y + 0.7, 0.05), books[((level * 2 + i) % #books) + 1])
		end
	end
end

---------------------------------------------------------------- decor
builders.plant = function(m)
	local pot = cyl(m, 1.4, 1.6, Vector3.new(0, 0.7, 0), C.terracotta, M.Brick, nil, true)
	pot.Name = "Pot"
	ball(m, 2, Vector3.new(0, 2.3, 0), C.leaf, M.Grass)
	ball(m, 1.5, Vector3.new(0.4, 3.2, 0.2), C.leaf2, M.Grass)
	ball(m, 1.2, Vector3.new(-0.5, 3.0, -0.3), C.leaf2, M.Grass)
end

builders.lamp = function(m)
	cyl(m, 0.3, 1.4, Vector3.new(0, 0.15, 0), C.darkwood)
	add(m, Vector3.new(0.3, 5.6, 0.3), Vector3.new(0, 3.1, 0), C.darkwood)
	local shade = add(m, Vector3.new(1.4, 1.2, 1.4), Vector3.new(0, 6.3, 0), C.warm, M.Neon, nil, true)
	light(shade, 16, 1.0)
end

builders.painting = function(m)
	add(m, Vector3.new(3.6, 2.8, 0.2), Vector3.new(0, 6, 0.05), C.gold, M.Wood, nil, true)
	add(m, Vector3.new(3.1, 2.3, 0.1), Vector3.new(0, 6, -0.07), Color3.fromRGB(140, 196, 236))
	add(m, Vector3.new(3.1, 0.9, 0.12), Vector3.new(0, 5.3, -0.08), Color3.fromRGB(90, 150, 210))
	add(m, Vector3.new(1.8, 0.8, 0.13), CFrame.new(-0.5, 5.6, -0.09) * CFrame.Angles(0, 0, math.rad(15)), Color3.fromRGB(110, 170, 80))
	ball(m, 0.5, Vector3.new(0.9, 6.7, -0.1), Color3.fromRGB(255, 214, 80))
end

builders.wall_lamp = function(m)
	add(m, Vector3.new(0.5, 0.8, 0.2), Vector3.new(0, 6.6, 0.2), C.iron, M.Metal)
	add(m, Vector3.new(0.2, 0.2, 0.5), Vector3.new(0, 6.9, -0.05), C.iron, M.Metal)
	local glass = add(m, Vector3.new(0.7, 1, 0.7), Vector3.new(0, 7.3, -0.15), C.warm, M.Neon, nil, true)
	light(glass, 16, 1.0)
end

builders.menu_board = function(m)
	local board = add(m, Vector3.new(2.2, 3.4, 0.15), CFrame.new(0, 2.1, -0.4) * CFrame.Angles(math.rad(-12), 0, 0), Color3.fromRGB(40, 46, 42), M.Slate)
	add(m, Vector3.new(2.2, 3.4, 0.15), CFrame.new(0, 2.1, 0.4) * CFrame.Angles(math.rad(12), 0, 0), Color3.fromRGB(40, 46, 42), M.Slate)
	add(m, Vector3.new(2.4, 0.2, 0.3), Vector3.new(0, 3.9, 0), C.wood, M.Wood)
	label(board, Enum.NormalId.Front, "🍕 TODAY\nFRESH\nPIZZA!", Color3.fromRGB(245, 245, 235), 30)
end

---------------------------------------------------------------- garden
builders.tree = function(m)
	add(m, Vector3.new(1.6, 7, 1.6), Vector3.new(0, 3.5, 0), Color3.fromRGB(120, 80, 50), M.Wood)
	local offs = { Vector3.new(0, 9, 0), Vector3.new(2.2, 7.6, 1.2), Vector3.new(-2, 7.8, -1.4), Vector3.new(0.6, 11, -0.4) }
	for i, o in offs do
		ball(m, i == 4 and 5 or 6.5, o, (i % 2 == 0) and C.leaf or C.leaf2, M.Grass)
	end
end

builders.bush = function(m)
	ball(m, 2.6, Vector3.new(0, 1.3, 0), C.leaf, M.Grass)
	ball(m, 1.8, Vector3.new(0.8, 1.6, 0.4), C.leaf2, M.Grass)
	ball(m, 0.5, Vector3.new(0.4, 2.6, -0.6), C.red)
end

builders.flower_bed = function(m)
	add(m, Vector3.new(6, 0.8, 3), Vector3.new(0, 0.4, 0), C.darkwood, M.Wood, nil, true)
	add(m, Vector3.new(5.6, 0.2, 2.6), Vector3.new(0, 0.85, 0), C.soil, M.Ground)
	for i = 0, 6 do
		for j = 0, 1 do
			local x = -2.4 + i * 0.8
			local z = -0.6 + j * 1.2
			ball(m, 0.6, Vector3.new(x, 1.15, z), C.leaf, M.Grass)
			ball(m, 0.5, Vector3.new(x, 1.5, z), FLOWERS[((i + j) % #FLOWERS) + 1])
		end
	end
end

builders.bench = function(m)
	add(m, Vector3.new(6, 0.4, 2), Vector3.new(0, 1.8, 0), C.wood, M.WoodPlanks, nil, true)
	add(m, Vector3.new(6, 1.6, 0.3), Vector3.new(0, 3, 0.9), C.wood, M.WoodPlanks, nil, true)
	for _, x in { -2.6, 2.6 } do
		add(m, Vector3.new(0.4, 1.6, 2), Vector3.new(x, 0.8, 0), C.iron, M.Metal)
	end
end

builders.lamp_post = function(m)
	add(m, Vector3.new(1.4, 0.6, 1.4), Vector3.new(0, 0.3, 0), C.iron, M.Metal)
	add(m, Vector3.new(0.5, 9, 0.5), Vector3.new(0, 4.8, 0), C.iron, M.Metal)
	local lantern = add(m, Vector3.new(1.3, 1.6, 1.3), Vector3.new(0, 9.9, 0), C.warm, M.Neon, nil, true)
	add(m, Vector3.new(1.8, 0.4, 1.8), Vector3.new(0, 10.9, 0), C.iron, M.Metal)
	light(lantern, 18, 0.8)
end

---------------------------------------------------------------- buildings
-- Garage: open front (-Z) for deliveries, a 5-wide opening in the right (+X) wall to the restaurant's back door.
builders.garage = function(m)
	add(m, Vector3.new(16, 0.2, 16), Vector3.new(0, 0.1, 0), Color3.fromRGB(150, 152, 158), M.Concrete)
	add(m, Vector3.new(1, 10, 16), Vector3.new(-7.5, 5.2, 0), C.brick, M.Brick, nil, true)
	add(m, Vector3.new(16, 10, 1), Vector3.new(0, 5.2, 7.5), C.brick, M.Brick, nil, true)
	add(m, Vector3.new(1, 10, 5.5), Vector3.new(7.5, 5.2, -5.25), C.brick, M.Brick, nil, true)
	add(m, Vector3.new(1, 10, 5.5), Vector3.new(7.5, 5.2, 5.25), C.brick, M.Brick, nil, true)
	add(m, Vector3.new(1, 2, 5), Vector3.new(7.5, 9.2, 0), C.brick, M.Brick, nil, true)
	add(m, Vector3.new(2, 10, 1.2), Vector3.new(-7, 5.2, -7.5), C.stone, M.Slate)
	add(m, Vector3.new(2, 10, 1.2), Vector3.new(7, 5.2, -7.5), C.stone, M.Slate)
	local header = add(m, Vector3.new(16, 2.6, 1.2), Vector3.new(0, 9, -7.5), C.stone, M.Slate)
	for i = 0, 3 do
		add(m, Vector3.new(12, 0.3, 0.3), Vector3.new(0, 7.2 + i * 0.32, -7.7), Color3.fromRGB(150, 156, 164), M.Metal)
	end
	add(m, Vector3.new(18, 1, 18), Vector3.new(0, 10.7, 0), C.terracotta, M.ClayRoofTiles, nil, true)
	for i = 0, 4 do
		add(m, Vector3.new(1.2, 0.05, 10), Vector3.new(-4.8 + i * 2.4, 0.22, -1), (i % 2 == 0) and Color3.fromRGB(250, 205, 50) or Color3.fromRGB(40, 40, 45))
	end
	label(header, Enum.NormalId.Front, "📦 DELIVERIES", Color3.fromRGB(60, 40, 32), 30)
end

---------------------------------------------------------------- drone areas
-- a dock with 5 charging pads (Pad1..Pad5) and a sign with the task
local function dock(m, task)
	local info = Config.DroneTasks[task]
	add(m, Vector3.new(8, 0.4, 3), Vector3.new(0, 0.2, 0), Color3.fromRGB(60, 64, 72), M.DiamondPlate, nil, true)
	for i = 1, 5 do
		local pad = cyl(m, 0.12, 1.3, Vector3.new(-3.2 + (i - 1) * 1.6, 0.46, -0.3), Color3.fromRGB(80, 200, 255), M.Neon, NOCOLLIDE)
		pad.Name = "Pad" .. i
	end
	for _, x in { -2.6, 2.6 } do
		add(m, Vector3.new(0.3, 2.2, 0.3), Vector3.new(x, 1.5, 1.2), C.iron, M.Metal, NOCOLLIDE)
	end
	local sign = add(m, Vector3.new(6, 1.2, 0.2), Vector3.new(0, 2.8, 1.2), Color3.fromRGB(40, 44, 52), M.SmoothPlastic, NOCOLLIDE)
	label(sign, Enum.NormalId.Front, info.icon .. " " .. string.upper(info.name) .. " DRONES", Color3.fromRGB(120, 220, 255), 30)
end

for task in Config.DroneTasks do
	builders["dock_" .. task] = function(m)
		dock(m, task)
	end
end

---------------------------------------------------------------- build / place / paint
-- Returns a Model whose PrimaryPart "Root" is an invisible box the size of the footprint.
-- opts.skins = { front skin, back skin } for walls.
function PieceBuilder.build(id, opts)
	opts = opts or {}
	local def = Config.Pieces[id]
	assert(def, "unknown piece " .. tostring(id))
	local model
	local folder = ReplicatedStorage:FindFirstChild("PieceModels")
	local custom = folder and folder:FindFirstChild(id)
	if custom and custom:IsA("Model") then
		model = custom:Clone()
		local bbCF, bbSize = model:GetBoundingBox()
		model:TranslateBy(-(bbCF.Position - Vector3.new(0, bbSize.Y / 2, 0)))
	else
		model = Instance.new("Model")
		local builder = builders[id]
		if builder then
			builder(model, opts)
		end
	end
	model.Name = id
	local root = Instance.new("Part")
	root.Name = "Root"
	root.Size = def.size
	root.Transparency = 1
	root.Anchored = true
	root.CanCollide = false
	root.CanQuery = true -- the station prompts live on this part
	root.CanTouch = false
	root.CFrame = CFrame.new(0, def.size.Y / 2, 0)
	root.Parent = model
	model.PrimaryPart = root
	for _, p in model:GetDescendants() do
		if p:IsA("BasePart") and p ~= root then
			p.Anchored = true
			p.CanTouch = false
			if not def.solid then
				p.CanCollide = false
			end
		end
	end
	return model
end

-- Moves a built piece so its footprint's bottom centre sits at baseCF.
function PieceBuilder.place(model, baseCF)
	local def = Config.Pieces[model.Name]
	model:PivotTo(baseCF * CFrame.new(0, def.size.Y / 2, 0))
end

-- Recolours the paintable parts. side = "front" / "back" for walls (nil = all).
function PieceBuilder.paint(model, color, material, side)
	for _, p in model:GetDescendants() do
		local tag = p:IsA("BasePart") and p:GetAttribute("Paint")
		if tag and (side == nil or tag == side or tag == "main") then
			if color then
				p.Color = color
			end
			if material then
				p.Material = material
			end
		end
	end
end

return PieceBuilder
```

### Config (ReplicatedStorage > Shared > Config), 464 lines

Every number in the game. For the plots, the important parts are Config.Pieces (each piece's size, layer and price) and Config.StarterLayout (the starter restaurant).

```lua
-- Config: every number of the game in one place (prices, timers, menu, pieces, drones).
-- Change numbers here; the rest of the code reads them from this file.
local Config = {}

Config.StartCash = 100

Config.Timers = {
	Bake = 12, -- seconds a pizza needs in the oven
	BurnAfter = 20, -- seconds a ready pizza can stay in the oven before it burns
	Cut = 1.5, -- seconds to cut one vegetable
	Patience = 90, -- seconds a seated customer waits for the pizza
	Eat = 8, -- seconds a customer eats
	CustomerEvery = 20, -- seconds between new customers (while the restaurant is open)
	NoTableEvery = 30, -- seconds between "no table" customers when no chair stands at a table
	Delivery = 15, -- seconds until an order from the manager PC lands in the garage
}

Config.Pay = {
	TipMax = 0.5, -- up to +50 % tip for fast service
	WrongPizza = 0.5, -- a wrong pizza pays half, no tip
}

-- Star rating. Each customer scores 1-5: 1 + right pizza (+1) + speed (+2 fast / +1 ok) + cozy table (+1).
-- A wrong pizza scores at most WrongPizzaMax; a customer who leaves hungry scores 1.
-- Stars = the average of the last Window scores. More stars = customers come more often and tip more.
Config.Rating = {
	Window = 30, -- stars = the average of the last 30 customer scores
	Start = 2.0, -- stars of a brand-new restaurant (the empty part of the list counts as this)
	FastestEvery = 8, -- seconds between customers at 5 stars (at the start stars: Timers.CustomerEvery)
	TipMaxAt5 = 1.0, -- the biggest tip at 5 stars: +100 % (at the start stars: Pay.TipMax)
	FastLeft = 0.6, -- served with 60 % of the patience (or more) left = fast: +2
	OkLeft = 0.3, -- 30 % (or more) left = ok: +1
	WrongPizzaMax = 2, -- the best score a wrong pizza can get
	CozyRadius = 12, -- decor this close (studs) to the customer's table counts
	CozyDecor = 2, -- decor pieces a table needs to be cozy: +1
	Decor = { -- piece ids that count as decor
		plant = true, lamp = true, wall_lamp = true, painting = true, flower_bed = true,
		bush = true, tree = true, menu_board = true, lamp_post = true,
	},
}

-- Special customers: ONE entry per type; add a new type by adding an entry.
-- oneIn = chance (1 in N customers), stars = rating needed, name = shown on the serve prompt,
-- badge = emoji next to the face, look = 3D extras from Server/Customers LOOKS ("crown", "critic",
-- "balloons", "cloud"; leave it out = none), arrive = message to the owner when they sit down (optional).
-- Rules: payMul = price x this, ordersBest = orders your most expensive pizza, fullTip = always the biggest tip,
-- patienceMul = patience x this, happyLeft + happyBonus = served with this much patience left: + bonus x price,
-- critic = their score changes the stars for a while (greatScore or more: +bonus for bonusMinutes;
-- badScore or less: -dip for dipMinutes), faces = 5 waiting faces (full patience -> none).
Config.SpecialCustomers = {
	vip = {
		name = "VIP", oneIn = 20, stars = 3, badge = "👑", look = "crown",
		payMul = 3, ordersBest = true,
		arrive = "👑 A VIP is here! They pay x3",
	},
	critic = {
		name = "Food Critic", oneIn = 25, stars = 2, badge = "📋", look = "critic",
		critic = true, greatScore = 4, bonus = 0.3, bonusMinutes = 10, badScore = 2, dip = 0.1, dipMinutes = 5,
		arrive = "📋 A Food Critic is here! Fast and cozy wins",
	},
	birthday = {
		name = "Birthday Kid", oneIn = 20, stars = 1, badge = "🎈", look = "balloons",
		fullTip = true,
	},
	grumpy = {
		name = "Grumpy", oneIn = 15, stars = 1, badge = "☁️", look = "cloud",
		patienceMul = 0.8, happyLeft = 0.5, happyBonus = 0.5, faces = { "😒", "😒", "😤", "😤", "😠" },
		arrive = "😤 A grumpy customer! Serve fast to cheer them up",
	},
}

Config.FridgeCapacity = 60 -- items one fridge holds
Config.MaxCustomersPerPlot = 12

-- cut = portions you get when you cut one (only things that must be cut first)
-- box / boxPrice = what one box from the manager PC holds and costs
Config.Ingredients = {
	dough = { name = "Dough", icon = "🥖", order = 1, color = Color3.fromRGB(240, 215, 160), box = 5, boxPrice = 10 },
	sauce = { name = "Sauce", icon = "🥫", order = 2, color = Color3.fromRGB(200, 40, 30), box = 5, boxPrice = 10 },
	cheese = { name = "Cheese", icon = "🧀", order = 3, color = Color3.fromRGB(255, 220, 90), box = 5, boxPrice = 10 },
	pepperoni = { name = "Pepperoni", icon = "🔴", order = 4, color = Color3.fromRGB(170, 30, 30), box = 5, boxPrice = 10 },
	ham = { name = "Ham", icon = "🍖", order = 5, color = Color3.fromRGB(240, 150, 150), box = 5, boxPrice = 10 },
	tomato = { name = "Tomato", icon = "🍅", order = 6, color = Color3.fromRGB(220, 50, 40), cut = 2, box = 4, boxPrice = 10 },
	pineapple = { name = "Pineapple", icon = "🍍", order = 7, color = Color3.fromRGB(255, 220, 60), cut = 2, box = 4, boxPrice = 10 },
	mushroom = { name = "Mushroom", icon = "🍄", order = 8, color = Color3.fromRGB(205, 185, 165), cut = 2, box = 4, boxPrice = 10 },
	pepper = { name = "Pepper", icon = "🌶️", order = 9, color = Color3.fromRGB(60, 160, 60), cut = 2, box = 4, boxPrice = 10 },
	-- for the recipes you unlock later
	onion = { name = "Onion", icon = "🧅", order = 10, color = Color3.fromRGB(236, 222, 240), cut = 2, box = 4, boxPrice = 15 },
	olive = { name = "Olives", icon = "🫒", order = 11, color = Color3.fromRGB(70, 80, 45), cut = 2, box = 4, boxPrice = 20 },
	chicken = { name = "Chicken", icon = "🍗", order = 12, color = Color3.fromRGB(226, 182, 128), box = 5, boxPrice = 25 },
	bacon = { name = "Bacon", icon = "🥓", order = 13, color = Color3.fromRGB(196, 86, 72), box = 5, boxPrice = 25 },
	corn = { name = "Corn", icon = "🌽", order = 14, color = Color3.fromRGB(255, 214, 64), box = 5, boxPrice = 15 },
	basil = { name = "Basil", icon = "🌿", order = 15, color = Color3.fromRGB(58, 150, 58), box = 5, boxPrice = 20 },
	gold = { name = "Gold Leaf", icon = "✨", order = 16, color = Color3.fromRGB(240, 196, 60), box = 2, boxPrice = 500 },
}

Config.MaxBoxesInGarage = 18 -- the garage floor holds this many boxes
Config.MaxBoxesPerOrder = 10

-- toppings = what goes on the dough (every pizza starts with dough). weight = how often customers order it.
-- unlock = price in the Recipe Book (no unlock = on the menu from the start), stars = rating needed to unlock it.
-- Recipe ladder (2026-10-25, from the research): each new recipe pays more, so income keeps up with the drone prices.
Config.Menu = {
	margherita = { name = "Margherita", price = 15, toppings = { "sauce", "cheese", "tomato" }, weight = 3 },
	pepperoni = { name = "Pepperoni", price = 18, toppings = { "sauce", "cheese", "pepperoni" }, weight = 3 },
	hawaii = { name = "Hawaii", price = 20, toppings = { "sauce", "cheese", "ham", "pineapple" }, weight = 2 },
	veggie = { name = "Veggie", price = 20, toppings = { "sauce", "cheese", "mushroom", "pepper" }, weight = 2 },
	bbq_chicken = { name = "BBQ Chicken", price = 40, toppings = { "sauce", "cheese", "chicken", "onion" }, weight = 3, unlock = 750, stars = 2 },
	capricciosa = { name = "Capricciosa", price = 60, toppings = { "sauce", "cheese", "ham", "mushroom", "olive" }, weight = 3, unlock = 2500, stars = 2.5 },
	diavola = { name = "Diavola", price = 90, toppings = { "sauce", "cheese", "pepperoni", "pepper", "onion" }, weight = 3, unlock = 8000, stars = 3 },
	garden = { name = "Garden", price = 150, toppings = { "sauce", "cheese", "mushroom", "pepper", "corn", "basil" }, weight = 3, unlock = 25000, stars = 3.5 },
	meat_lovers = { name = "Meat Lovers", price = 250, toppings = { "sauce", "cheese", "pepperoni", "ham", "chicken", "bacon" }, weight = 3, unlock = 80000, stars = 4 },
	supreme = {
		name = "Supreme", price = 400, toppings = { "sauce", "cheese", "pepperoni", "ham", "mushroom", "pepper", "onion", "olive" },
		weight = 3, unlock = 250000, stars = 4.5,
	},
	golden = { name = "Golden Pizza", price = 1000, toppings = { "sauce", "cheese", "basil", "gold" }, weight = 2, unlock = 1000000, stars = 4.8 },
}
Config.MaxToppings = 8 -- the most toppings one pizza can have (the Supreme)

-- Which menu pizza has exactly these toppings? Returns the menu id or nil.
function Config.matchMenu(toppings)
	local set = {}
	for _, t in toppings do
		set[t] = true
	end
	for id, pizza in Config.Menu do
		if #pizza.toppings == #toppings then
			local same = true
			for _, t in pizza.toppings do
				if not set[t] then
					same = false
					break
				end
			end
			if same then
				return id
			end
		end
	end
	return nil
end

function Config.toppingIcons(toppings)
	local s = ""
	for _, t in toppings do
		s ..= Config.Ingredients[t].icon
	end
	return s
end

-- Drones: one drone area (dock) per task, max 5 drones each. price = the first drone; every extra drone in
-- the same area costs twice the one before. The user: "a lot like 1k 10k 500k 2m smth like that".
Config.DroneTasks = {
	order = { name = "Ordering", icon = "💻", price = 1000, order = 1 },
	carry = { name = "Carrying", icon = "📦", price = 10000, order = 2 },
	cut = { name = "Cutting", icon = "🔪", price = 100000, order = 3 },
	topping = { name = "Toppings", icon = "🍕", price = 500000, order = 4 },
	oven = { name = "Oven", icon = "🔥", price = 2000000, order = 5 },
	serve = { name = "Serving", icon = "🛎️", price = 5000000, order = 6 },
}
Config.MaxDronesPerArea = 5
-- Upgrades apply to ALL drones: 10 levels each, level 1 costs $250 and every level doubles.
Config.DroneUpgrades = {
	speed = { name = "Speed", icon = "⚡", perLevel = 0.15, order = 1 }, -- +15 % flying + working speed
	capacity = { name = "Capacity", icon = "🎒", perLevel = 1, order = 2 }, -- +1 item carried at once
	battery = { name = "Battery", icon = "🔋", perLevel = 0.2, order = 3 }, -- +20 % working time
}
Config.DroneUpgradeLevels = 10
Config.DroneUpgradeBasePrice = 250
Config.DroneBase = { speed = 14, battery = 120, recharge = 20, capacity = 1 } -- studs/s, seconds of work, seconds to charge, items

-- Quests: the tutorial for new players (ends with the first drone) and endless quests after it.
-- Rewards are paid when the player taps CLAIM. Change the numbers freely; set a template's weight to 0 to switch it off.
Config.Quests = {
	TutorialPizza = "margherita", -- the pizza the tutorial teaches (step 1 shows its ingredients)
	-- The tutorial, one step after the other. kind = what the step asks for (the kinds are in Server/Quests),
	-- reward = $ on CLAIM, goal = how many (where it makes sense), name = the step's name in Roblox analytics,
	-- tutorialPizzaOnly = customers only order the TutorialPizza during this step, celebrate = big banner + fanfare.
	Tutorial = {
		{ kind = "order", reward = 20, name = "Order ingredients", tutorialPizzaOnly = true },
		{ kind = "carry", goal = 4, reward = 20, name = "Fill the fridge", tutorialPizzaOnly = true },
		{ kind = "cut", reward = 15, name = "Cut a tomato", tutorialPizzaOnly = true },
		{ kind = "open", reward = 15, name = "Open the restaurant", tutorialPizzaOnly = true },
		{ kind = "make", reward = 25, name = "Make a pizza", tutorialPizzaOnly = true },
		{ kind = "bake", reward = 25, name = "Bake the pizza", tutorialPizzaOnly = true },
		{
			kind = "serve", reward = 50, name = "First pizza", tutorialPizzaOnly = true,
			celebrate = { title = "First pizza! 🍕", text = "Your first happy customer!" },
		},
		{ kind = "serveMore", goal = 5, reward = 80, name = "Serve 5 pizzas", tutorialPizzaOnly = true },
		{ kind = "build", reward = 50, name = "Buy and place an item" },
		{ kind = "serveMore", goal = 10, reward = 100, name = "Serve 10 pizzas" },
		{
			kind = "buyDrone", param = "order", reward = 150, name = "First drone",
			celebrate = { title = "Your first drone! 🤖", text = "It orders ingredients for you. Tutorial done! 🎉" },
		},
	},
	AutoClaimSeconds = 15, -- tutorial only: a finished step pays out by itself after this long (0 = never)
	VeteranPizzas = 5, -- players without quest data who already served this many pizzas skip the tutorial
	-- After the tutorial: one quest at a time, picked at random from these templates (only ones that fit the player).
	-- weight = how often (0 = never), minutes = how long it should take at the player's own pace,
	-- min / max = limits for the goal, share = reward as a part of the player's next big goal price,
	-- soonMinutes = only offer purchases the player can afford within this many minutes, maxGoal = the highest star goal.
	Templates = {
		pizzas = { weight = 3, minutes = 4, min = 5, max = 200, share = 0.12 }, -- Serve 12 pizzas
		perfect = { weight = 2, minutes = 5, min = 2, max = 80, share = 0.15 }, -- Serve 3 pizzas super fast
		earn = { weight = 3, minutes = 4, min = 100, share = 0.12 }, -- Earn $1,500
		cutMany = { weight = 1, minutes = 4, min = 6, max = 120, share = 0.1 }, -- Cut 10 vegetables
		recipeServe = { weight = 2, minutes = 5, min = 2, max = 60, share = 0.14 }, -- Serve 4 Hawaii pizzas
		stars = { weight = 1, share = 0.18, maxGoal = 4.5 }, -- Reach ⭐ 2.5
		decor = { weight = 1, min = 2, max = 6, share = 0.1 }, -- Place 3 decorations
		unlockRecipe = { weight = 2, share = 0.15, soonMinutes = 10 }, -- Unlock the BBQ Chicken pizza
		buyDrone = { weight = 2, share = 0.15, soonMinutes = 10 }, -- Buy the Carrying drone
		upgrade = { weight = 1, share = 0.1, soonMinutes = 6 }, -- Upgrade your drones
	},
	MinReward = 25, -- the smallest reward of an endless quest
	StarsStep = 0.5, -- star quests aim for the next half star (2.0 -> 2.5)
	-- Until the game has measured the player's own pace (2+ minutes of play this visit):
	FallbackPizzasPerMinute = 1.5,
	FallbackCutsPerMinute = 1,
	FallbackIncomeShare = 0.03, -- income per minute = 3 % of the next big goal price
}

-- Kitchen signs + drone behaviour
Config.Kitchen = {
	SignDistance = 60, -- studs: station signs and "needs" bubbles show up to this far away
	NeedDelay = 4, -- seconds a station must wait before its "needs" bubble shows (drones that keep up never trigger it)
	LowCut = 2, -- fewer cut portions than this (with whole ones in the fridge) = the cutting board asks for cutting
	BurnWarning = 5, -- the oven sign flashes red / white for the last seconds before a pizza burns
	OrderTargetBoxes = 2, -- an ordering drone keeps at most this many boxes of each needed ingredient around
	CutTarget = 6, -- a cutting drone keeps this many cut portions of each needed vegetable ready
	MakeTime = 3, -- seconds a topping drone works on one pizza (faster with the speed upgrade)
	BatteryMargin = 20, -- seconds of battery a drone keeps for the way home
	BobHeight = 0.25, -- studs a working drone bobs up and down (0 = off, saves a little network)
	StaleHatch = 45, -- seconds before a waiter drone throws away a pizza nobody wants from a hatch
}

-- Day and night (read by ServerScriptService.DayNightCycle)
Config.DayNight = {
	DayMinutes = 20, -- one full day + night in real minutes
	NightSpeed = 2, -- nights run this many times faster than days (more daytime for kids)
	StartTime = 9, -- clock time (hours) when a server starts
	UpdateEvery = 0.2, -- seconds between lighting updates
	LampDay = 1, -- lamp brightness x this during the day
	LampNight = 2.2, -- lamp brightness x this at night
	LampNightRange = 1.3, -- lamp range x this at night
	AmbienceVolume = 0.3, -- birds / crickets volume
	WaterVolume = 0.8, -- waterfall volume (3D)
}

-- Saving: offline earnings. Only players who own at least one drone get them.
Config.Save = {
	OfflineShare = 0.25, -- while you're away, drones earn this share of your last visit's income per minute
	OfflineMaxMinutes = 120, -- at most 2 hours count
	OfflineMinMinutes = 5, -- away for less than this: nothing (stops rejoin farming)
	OfflineMinSessionMinutes = 5, -- a visit must last this long before its income per minute is measured
}

-- Height of the ground and of the floor on a plot (the plot's base is 0.4 thick, floor tiles 0.2).
Config.GroundY = 0.4
Config.FloorY = 0.6

-- Pieces you can place. size = width (X), height (Y), depth (Z) in studs; the front of a piece is its -Z side.
-- layer "floor" lies on the ground, "wall" pieces have two looks (skins: front side, back side), the rest are objects.
-- solid = false: players and customers walk through it (chairs, decor). shop = sold in the build menu's shop.
Config.Pieces = {
	-- floors (16 x 16)
	floor_wood = { name = "Wood Floor", category = "Floors", price = 40, size = Vector3.new(16, 0.2, 16), layer = "floor", solid = true, shop = true },
	floor_kitchen = { name = "Kitchen Tiles", category = "Floors", price = 50, size = Vector3.new(16, 0.2, 16), layer = "floor", solid = true, shop = true },
	floor_office = { name = "Carpet", category = "Floors", price = 40, size = Vector3.new(16, 0.2, 16), layer = "floor", solid = true, shop = true },
	floor_storage = { name = "Concrete Floor", category = "Floors", price = 20, size = Vector3.new(16, 0.2, 16), layer = "floor", solid = true, shop = true },
	floor_terrace = { name = "Stone Terrace", category = "Floors", price = 60, size = Vector3.new(16, 0.2, 16), layer = "floor", solid = true, shop = true },
	-- walls (8 wide; the entrance 16)
	wall = { name = "Wall", category = "Walls", price = 15, size = Vector3.new(8, 12, 1), layer = "wall", solid = true },
	wall_window = { name = "Window", category = "Walls", price = 25, size = Vector3.new(8, 12, 1), layer = "wall", solid = true },
	wall_door = { name = "Door", category = "Walls", price = 30, size = Vector3.new(8, 12, 1), layer = "wall", solid = true },
	wall_pass = { name = "Serving Hatch", category = "Walls", price = 40, size = Vector3.new(8, 12, 1), layer = "wall", solid = true, station = "pass" },
	entrance = { name = "Entrance", category = "Walls", price = 200, size = Vector3.new(16, 12, 1), layer = "wall", solid = true },
	-- dining
	table = { name = "Table", category = "Dining", price = 60, size = Vector3.new(4, 3, 4), layer = "object", solid = true, isTable = true, shop = true },
	chair = { name = "Chair", category = "Dining", price = 30, size = Vector3.new(2, 4, 2), layer = "object", solid = false, isChair = true, shop = true },
	umbrella_table = { name = "Terrace Table", category = "Dining", price = 150, size = Vector3.new(4, 9, 4), layer = "object", solid = true, isTable = true, shop = true },
	host_stand = { name = "Host Stand", category = "Dining", price = 80, size = Vector3.new(2.4, 4, 1.6), layer = "object", solid = true, shop = true },
	-- kitchen
	fridge = { name = "Fridge", category = "Kitchen", price = 400, size = Vector3.new(4, 7, 3), layer = "object", solid = true, station = "fridge", shop = true },
	cutting_board = { name = "Cutting Board", category = "Kitchen", price = 300, size = Vector3.new(4, 3.6, 3), layer = "object", solid = true, station = "cut", shop = true },
	prep_table = { name = "Prep Table", category = "Kitchen", price = 300, size = Vector3.new(4, 3.6, 3), layer = "object", solid = true, station = "prep", shop = true },
	oven = { name = "Pizza Oven", category = "Kitchen", price = 800, size = Vector3.new(4, 5.5, 3), layer = "object", solid = true, station = "oven", shop = true },
	trash_bin = { name = "Trash Bin", category = "Kitchen", price = 25, size = Vector3.new(2, 3, 2), layer = "object", solid = true, station = "trash", shop = true },
	counter = { name = "Counter", category = "Kitchen", price = 50, size = Vector3.new(4, 3.6, 3), layer = "object", solid = true, shop = true },
	kitchen_shelf = { name = "Shelf", category = "Kitchen", price = 60, size = Vector3.new(4, 7, 1.5), layer = "object", solid = true, shop = true },
	-- office
	manager_desk = { name = "Manager Desk", category = "Office", price = 100, size = Vector3.new(6, 3.2, 3), layer = "object", solid = true, station = "pc" },
	office_chair = { name = "Office Chair", category = "Office", price = 20, size = Vector3.new(2, 4, 2), layer = "object", solid = false, shop = true },
	bookshelf = { name = "Bookshelf", category = "Office", price = 60, size = Vector3.new(4, 7, 1.5), layer = "object", solid = true, shop = true },
	-- decor
	plant = { name = "Plant", category = "Decor", price = 15, size = Vector3.new(2, 4, 2), layer = "object", solid = false, shop = true },
	lamp = { name = "Floor Lamp", category = "Decor", price = 25, size = Vector3.new(1.5, 7, 1.5), layer = "object", solid = false, shop = true },
	painting = { name = "Painting", category = "Decor", price = 40, size = Vector3.new(4, 8, 0.4), layer = "object", solid = false, shop = true },
	wall_lamp = { name = "Wall Lamp", category = "Decor", price = 30, size = Vector3.new(1.5, 8, 0.6), layer = "object", solid = false, shop = true },
	menu_board = { name = "Menu Board", category = "Decor", price = 30, size = Vector3.new(2.4, 5, 1.6), layer = "object", solid = false, shop = true },
	-- garden
	tree = { name = "Tree", category = "Garden", price = 50, size = Vector3.new(6, 14, 6), layer = "object", solid = false, shop = true },
	bush = { name = "Bush", category = "Garden", price = 15, size = Vector3.new(3, 3, 3), layer = "object", solid = false, shop = true },
	flower_bed = { name = "Flower Bed", category = "Garden", price = 30, size = Vector3.new(6, 1.5, 3), layer = "object", solid = false, shop = true },
	bench = { name = "Bench", category = "Garden", price = 40, size = Vector3.new(6, 3.5, 2), layer = "object", solid = true, shop = true },
	lamp_post = { name = "Lamp Post", category = "Garden", price = 40, size = Vector3.new(1.5, 11, 1.5), layer = "object", solid = false, shop = true },
	-- buildings
	garage = { name = "Garage", category = "Buildings", price = 300, size = Vector3.new(16, 11, 16), layer = "object", solid = true, station = "garage" },
	-- drone areas (one per task, see Config.DroneTasks)
	dock_order = { name = "Ordering Drones", category = "Drones", price = 0, size = Vector3.new(8, 1.2, 3), layer = "object", solid = false, station = "dock", task = "order" },
	dock_carry = { name = "Carrying Drones", category = "Drones", price = 0, size = Vector3.new(8, 1.2, 3), layer = "object", solid = false, station = "dock", task = "carry" },
	dock_cut = { name = "Cutting Drones", category = "Drones", price = 0, size = Vector3.new(8, 1.2, 3), layer = "object", solid = false, station = "dock", task = "cut" },
	dock_topping = { name = "Topping Drones", category = "Drones", price = 0, size = Vector3.new(8, 1.2, 3), layer = "object", solid = false, station = "dock", task = "topping" },
	dock_oven = { name = "Oven Drones", category = "Drones", price = 0, size = Vector3.new(8, 1.2, 3), layer = "object", solid = false, station = "dock", task = "oven" },
	dock_serve = { name = "Serving Drones", category = "Drones", price = 0, size = Vector3.new(8, 1.2, 3), layer = "object", solid = false, station = "dock", task = "serve" },
}

-- The restaurant every new owner starts with (64 x 64, laid out like a real restaurant). Every piece can be
-- changed later. x, z = studs from the plot centre (negative z = towards the street), rot = degrees
-- (0 = the front faces the street), skins = { front side, back side } for walls.
-- Footprint x -32..32, z -36..28. Dining room z -36..-4 (front). Behind it: storage x -32..-16 (fridges, back
-- door to the garage), kitchen x -16..16 (serving hatches + kitchen door to the dining room), office x 16..32.
local layout = {}
local function add(id, x, z, rot, skins)
	table.insert(layout, { id = id, x = x, z = z, rot = rot or 0, skins = skins })
end
local B = "brick"

-- floors
for _, x in { -24, -8, 8, 24 } do
	add("floor_wood", x, -28)
	add("floor_wood", x, -12)
end
for _, z in { 4, 20 } do
	add("floor_storage", -24, z)
	add("floor_kitchen", -8, z)
	add("floor_kitchen", 8, z)
	add("floor_office", 24, z)
end
add("floor_terrace", -16, -44)
add("floor_terrace", 16, -44)

-- front (street side): windows and the big entrance in the middle
add("wall_window", -28, -36, 0, { B, "dining" })
add("wall_window", -20, -36, 0, { B, "dining" })
add("wall", -12, -36, 0, { B, "dining" })
add("entrance", 0, -36, 0, { B, "dining" })
add("wall", 12, -36, 0, { B, "dining" })
add("wall_window", 20, -36, 0, { B, "dining" })
add("wall_window", 28, -36, 0, { B, "dining" })
-- back (faces outwards)
add("wall", -28, 28, 180, { B, "storage" })
add("wall", -20, 28, 180, { B, "storage" })
for _, x in { -12, -4, 4, 12 } do
	add("wall", x, 28, 180, { B, "kitchen" })
end
add("wall", 20, 28, 180, { B, "office" })
add("wall_window", 28, 28, 180, { B, "office" })
-- west side
add("wall_window", -32, -32, 90, { B, "dining" })
add("wall", -32, -24, 90, { B, "dining" })
add("wall_window", -32, -16, 90, { B, "dining" })
add("wall", -32, -8, 90, { B, "dining" })
add("wall", -32, 0, 90, { B, "storage" })
add("wall_door", -32, 8, 90, { B, "storage" }) -- back door to the garage
add("wall", -32, 16, 90, { B, "storage" })
add("wall", -32, 24, 90, { B, "storage" })
-- east side
add("wall_window", 32, -32, 270, { B, "dining" })
add("wall", 32, -24, 270, { B, "dining" })
add("wall_window", 32, -16, 270, { B, "dining" })
add("wall", 32, -8, 270, { B, "dining" })
add("wall", 32, 0, 270, { B, "office" })
add("wall_window", 32, 8, 270, { B, "office" })
add("wall", 32, 16, 270, { B, "office" })
add("wall", 32, 24, 270, { B, "office" })
-- between the dining room and the back: storage wall, 2 serving hatches, kitchen door, office wall
add("wall", -28, -4, 0, { "dining", "storage" })
add("wall", -20, -4, 0, { "dining", "storage" })
add("wall_pass", -12, -4, 0, { "dining", "kitchen" })
add("wall_pass", -4, -4, 0, { "dining", "kitchen" })
add("wall", 4, -4, 0, { "dining", "kitchen" })
add("wall_door", 12, -4, 0, { "dining", "kitchen" })
add("wall", 20, -4, 0, { "dining", "office" })
add("wall", 28, -4, 0, { "dining", "office" })
-- storage | kitchen
add("wall_door", -16, 0, 90, { "storage", "kitchen" })
for _, z in { 8, 16, 24 } do
	add("wall", -16, z, 90, { "storage", "kitchen" })
end
-- kitchen | office
for _, z in { 0, 8, 16 } do
	add("wall", 16, z, 270, { "office", "kitchen" })
end
add("wall_door", 16, 24, 270, { "office", "kitchen" })

-- dining room: 2 tables with 2 chairs each (more come from the shop), host stand, decor, serving drones
add("table", -14, -22)
add("chair", -17.5, -22, 270)
add("chair", -10.5, -22, 90)
add("table", 14, -22)
add("chair", 10.5, -22, 270)
add("chair", 17.5, -22, 90)
add("host_stand", 8, -31)
add("plant", -29.5, -33.5)
add("plant", 29.5, -33.5)
add("plant", 29.5, -6.5)
add("painting", -31.3, -28, 270)
add("painting", -31.3, -12, 270)
add("painting", 31.3, -28, 90)
add("painting", 31.3, -12, 90)
add("wall_lamp", -31.2, -20, 270)
add("wall_lamp", 31.2, -20, 90)
add("dock_serve", -24, -6)
-- kitchen: the line along the back wall + 3 drone areas
add("cutting_board", -12, 26)
add("prep_table", -6, 26)
add("oven", 2, 26)
add("trash_bin", 8.5, 26.5)
add("kitchen_shelf", 13, 26.75)
add("dock_cut", -14, 8, 270)
add("dock_topping", -14, 18, 270)
add("dock_oven", 14, 8, 90)
-- storage: fridges + carrying drones
add("fridge", -30, 16, 270)
add("fridge", -30, 21, 270)
add("kitchen_shelf", -17.25, 12, 90)
add("dock_carry", -24, 26)
-- office: the manager PC + ordering drones
add("manager_desk", 24, 25)
add("office_chair", 24, 21.5, 180)
add("bookshelf", 17.25, 10, 270)
add("plant", 30, 26)
add("dock_order", 30, 6, 90)
-- outside: garage (deliveries come in through the back door), terrace (empty: buy terrace tables), garden
add("garage", -48, 8)
add("menu_board", 9.5, -40)
add("lamp_post", -8, -58)
add("lamp_post", 8, -58)
add("flower_bed", -40, -50)
add("flower_bed", 40, -50)
add("bush", -36, -40)
add("bush", 36, -40)
add("tree", -50, -40)
add("tree", 50, -40)
add("tree", 48, 46)
add("tree", -20, 48)
add("tree", 20, 48)
add("bench", 46, 12, 270)
add("bench", -46, 40, 90)
Config.StarterLayout = layout

-- Inside the garage piece (piece coordinates): where delivered boxes land, in rows of 3 x 3, then stacked.
Config.GarageDrop = { x0 = -3, z0 = -4, step = 3 }

-- Where customers appear (outside the plot gate) and the restaurant entrance (plot coordinates)
Config.CustomerSpawnZ = -74
Config.DoorOutside = Vector3.new(0, 0, -40)
Config.DoorInside = Vector3.new(0, 0, -30)

return Config
```

---

**Related:** [[Lobby code]] · [[Limits and safe use]] · [[Game overview]]
