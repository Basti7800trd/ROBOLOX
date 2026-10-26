---
tags:
  - code
  - lobby
updated: 2026-10-26
studio_path: "Workspace > Map"
objects: 604
---

> [!warning] Before running
> Read [[Limits and safe use]]. Edit mode only.

## Lobby code (Workspace > Map)

The lobby has no build script in the game: it is 604 placed objects. The code below was generated from them on 26 Oct 2026 and rebuilds all 604 exactly (tested in Studio: every part within 0.001 studs, same colors and materials).

**How to run:** Studio in Edit mode (not Play) → Command Bar (Ctrl+9). Paste the shared helpers, then the lobby code below them, and press Enter. If a Map already exists, the copy is built as Map\_Rebuilt next to it, so nothing is overwritten. The 30 pack trees need ServerStorage > YasuTreePack.

**Reading the code:** `new(class, parent, props, style)` makes one object; `S[n]` is a property set shared by several objects; `copy(V[n], …)` repeats an earlier model at a new spot (the 44 lamp posts are 1 model + 43 copies); `pack("Tree_16", …)` clones a tree from the pack with its size and turn; `cf(x, y, z, rx, ry, rz)` is a position plus rotation in degrees.

### Shared helpers (paste these first, also for the landscape and plot code)

```lua
local rad = math.rad
local function cf(x, y, z, rx, ry, rz) return CFrame.new(x, y, z) * CFrame.fromOrientation(rad(rx or 0), rad(ry or 0), rad(rz or 0)) end
local function rgb(r, g, b) return Color3.fromRGB(r, g, b) end
local function apply(o, props)
	if props.Shape then o.Shape = props.Shape end
	for k, v in pairs(props) do
		if k == "_attrs" then for a, av in pairs(v) do o:SetAttribute(a, av) end
		elseif k == "_tags" then for _, t in ipairs(v) do o:AddTag(t) end
		else o[k] = v end
	end
end
-- new(class, parent, props, style): style = a shared table of properties (S[n] below)
local function new(class, parent, props, style)
	local o = Instance.new(class)
	if o:IsA("BasePart") then o.Anchored = true; o.TopSurface = Enum.SurfaceType.Smooth; o.BottomSurface = Enum.SurfaceType.Smooth end
	if style then apply(o, style) end
	apply(o, props)
	o.Parent = parent
	return o
end
-- Trees and rocks are cloned from the free packs in ServerStorage (and PieceModels).
local packs = {game.ServerStorage:FindFirstChild("YasuTreePack"), game.ServerStorage:FindFirstChild("StylizedRocksPack"), game.ReplicatedStorage:FindFirstChild("PieceModels")}
local meshIndex = {}
for _, root in ipairs(packs) do
	if root then for _, d in ipairs(root:GetDescendants()) do if d:IsA("MeshPart") and not meshIndex[d.MeshId] then meshIndex[d.MeshId] = d end end end
end
local function pack(name, parent, pivot, scale, newName)
	for _, root in ipairs(packs) do
		local src = root and root:FindFirstChild(name, true)
		if src then
			local m = src:Clone()
			if scale ~= 1 then m:ScaleTo(m:GetScale() * scale) end
			m:PivotTo(pivot); m.Name = newName; m.Parent = parent
			return m
		end
	end
	warn("Pack model not found: " .. name)
end
-- mesh(id, parent, props, style): a loose pack mesh (rock); props only list what differs from the pack
local function mesh(id, parent, props, style)
	local src = meshIndex[id]
	if not src then warn("Pack mesh not found: " .. id) return end
	local o = src:Clone()
	if style then apply(o, style) end
	apply(o, props)
	o.Parent = parent
	return o
end
-- A model that repeats (lamp posts, benches ...) is built once, then copied.
local function copy(src, parent, pivot, name) local m = src:Clone(); m:PivotTo(pivot); m.Name = name; m.Parent = parent; return m end
local V = {}
```

### Lobby

```lua
local S = {}
S[1]={Size=Vector3.new(0.6,0.04,4),Color=rgb(255,255,255),Material=Enum.Material.SmoothPlastic,CanCollide=false}
S[2]={Size=UDim2.new(1,0,1,0),BackgroundColor3=rgb(255,244,222)}
S[3]={CornerRadius=UDim.new(0,24)}
S[4]={Size=UDim2.new(0.94,0,0.16,0),Position=UDim2.new(0.03,0,0.03,0),BackgroundColor3=rgb(206,62,50),FontFace=Font.new("rbxasset://fonts/families/FredokaOne.json",Enum.FontWeight.Regular,Enum.FontStyle.Normal),TextColor3=rgb(255,255,255),TextScaled=true,TextWrapped=true}
S[5]={Size=UDim2.new(0.9,0,0.74,0),Position=UDim2.new(0.05,0,0.22,0),BackgroundTransparency=1}
S[6]={SortOrder=Enum.SortOrder.LayoutOrder,Padding=UDim.new(0.015,0)}
S[7]={Size=Vector3.new(1.4,12,1.4),Color=rgb(90,56,36),Material=Enum.Material.Wood}
S[8]={Shape=Enum.PartType.Ball,Size=Vector3.new(1.1,1.1,1.1),Color=rgb(250,250,250),Material=Enum.Material.SmoothPlastic,CanCollide=false}
S[9]={Shape=Enum.PartType.Ball,Size=Vector3.new(1.1,1.1,1.1),Color=rgb(240,80,90),Material=Enum.Material.SmoothPlastic,CanCollide=false}
S[10]={Shape=Enum.PartType.Ball,Size=Vector3.new(1.1,1.1,1.1),Color=rgb(255,210,70),Material=Enum.Material.SmoothPlastic,CanCollide=false}
S[11]={Shape=Enum.PartType.Ball,Size=Vector3.new(1.1,1.1,1.1),Color=rgb(190,110,230),Material=Enum.Material.SmoothPlastic,CanCollide=false}
S[12]={Size=Vector3.new(0.4,1.6,2),Color=rgb(45,48,52),Material=Enum.Material.SmoothPlastic}
S[13]={Size=Vector3.new(12,0.1,81),Color=rgb(214,200,176),Material=Enum.Material.Pavement}
S[14]={Size=Vector3.new(27.2,15.3,0.68),Color=rgb(90,56,36),Material=Enum.Material.Wood}
S[15]={Size=Vector3.new(30.6,1.02,8.5),Color=rgb(170,120,90),Material=Enum.Material.Brick}
S[16]={Size=Vector3.new(25.5,13.6,0.85),Color=rgb(110,70,45),Material=Enum.Material.Wood}
S[17]={SizingMode=Enum.SurfaceGuiSizingMode.PixelsPerStud,PixelsPerStud=35.294}
S[18]={Size=Vector3.new(28.9,1.02,3.4),Color=rgb(206,62,50),Material=Enum.Material.SmoothPlastic}
S[19]={Size=Vector3.new(1.19,10.2,1.19),Color=rgb(90,56,36),Material=Enum.Material.Wood}
V[0]=new("Folder",workspace,{Name="Map"})
V[0].Name=workspace:FindFirstChild("Map") and "Map_Rebuilt" or "Map"
V[1]=new("Folder",V[0],{Name="RoadLines"})
new("Part",V[1],{Name="Dash",CFrame=cf(-73.861,0.33,-13.024,0,170,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-57.453,0.33,-48.209,0,140,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-70.477,0.33,-25.652,0,160,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(13.024,0.33,-73.861,0,80,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(25.652,0.33,-70.477,0,70,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-25.652,0.33,70.477,0,-110,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-70.477,0.33,25.652,0,-160,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-57.453,0.33,48.209,0,-140,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(57.453,0.33,48.209,0,-40,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(13.024,0.33,73.861,0,-80,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(64.952,0.33,-37.5,0,30,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-73.861,0.33,13.024,0,-170,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(48.209,0.33,-57.453,0,50,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(48.209,0.33,57.453,0,-50,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(75,0.33,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(70.477,0.33,25.652,0,-20,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-13.024,0.33,-73.861,0,100,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-64.952,0.33,-37.5,0,150,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-48.209,0.33,57.453,0,-130,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(73.861,0.33,-13.024,0,10,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(57.453,0.33,-48.209,0,40,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(25.652,0.33,70.477,0,-70,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-37.5,0.33,64.952,0,-120,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(37.5,0.33,-64.952,0,60,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(64.952,0.33,37.5,0,-30,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-25.652,0.33,-70.477,0,110,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-75,0.33,0,0,180,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-48.209,0.33,-57.453,0,130,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(0,0.33,-75,0,90,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(37.5,0.33,64.952,0,-60,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(0,0.33,75,0,-90,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-13.024,0.33,73.861,0,-100,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(70.477,0.33,-25.652,0,20,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-64.952,0.33,37.5,0,-150,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(-37.5,0.33,-64.952,0,120,0)},S[1])
new("Part",V[1],{Name="Dash",CFrame=cf(73.861,0.33,13.024,0,-10,0)},S[1])
V[2]=new("Model",V[0],{Name="Fountain"})
new("Part",V[2],{Name="Water",CFrame=cf(0,2.45,0,0,0,90),Shape=Enum.PartType.Cylinder,Size=Vector3.new(0.4,20,20),Color=rgb(80,170,230),Material=Enum.Material.Glass,Transparency=0.2,Reflectance=0.2,CanCollide=false})
new("Part",V[2],{Name="Basin",CFrame=cf(0,1.5,0,0,0,90),Shape=Enum.PartType.Cylinder,Size=Vector3.new(2.2,22,22),Color=rgb(214,204,188),Material=Enum.Material.Slate})
new("Part",V[2],{Name="Bowl",CFrame=cf(0,8,0,0,0,90),Shape=Enum.PartType.Cylinder,Size=Vector3.new(1,8,8),Color=rgb(214,204,188),Material=Enum.Material.Slate})
new("Part",V[2],{Name="Column",CFrame=cf(0,5,0,0,0,90),Shape=Enum.PartType.Cylinder,Size=Vector3.new(6,2.4,2.4),Color=rgb(214,204,188),Material=Enum.Material.Slate})
V[3]=new("Part",V[2],{Name="Spout",CFrame=cf(0,9.6,0),Shape=Enum.PartType.Ball,Size=Vector3.new(1.6,1.6,1.6),Color=rgb(150,210,255),Material=Enum.Material.Neon,Transparency=0.3,CanCollide=false})
new("ParticleEmitter",V[3],{Rate=40,Lifetime=NumberRange.new(0.8,1.2),Speed=NumberRange.new(10,14),SpreadAngle=Vector2.new(18,18),Size=NumberSequence.new({NumberSequenceKeypoint.new(0,0.5,0),NumberSequenceKeypoint.new(1,0.1,0)}),Transparency=NumberSequence.new({NumberSequenceKeypoint.new(0,0.2,0),NumberSequenceKeypoint.new(1,1,0)}),Color=ColorSequence.new({ColorSequenceKeypoint.new(0,rgb(200,235,255)),ColorSequenceKeypoint.new(1,rgb(200,235,255))}),Acceleration=Vector3.new(0,-30,0),LightEmission=0.4})
new("Part",V[2],{Name="BowlWater",CFrame=cf(0,8.45,0,0,0,90),Shape=Enum.PartType.Cylinder,Size=Vector3.new(0.3,7,7),Color=rgb(80,170,230),Material=Enum.Material.Glass,Transparency=0.2,CanCollide=false})
V[2].WorldPivot=cf(0,5.4,0,0,0,90)
V[4]=new("Model",V[0],{Name="Leaderboard",_attrs={["Board"]="earned"}})
new("Part",V[4],{Name="Stage",CFrame=cf(0,1,-44),Size=Vector3.new(36,1.2,10),Color=rgb(170,120,90),Material=Enum.Material.Brick})
V[5]=new("Part",V[4],{Name="Board",CFrame=cf(0,12,-45,0,180,0),Size=Vector3.new(30,16,1),Color=rgb(110,70,45),Material=Enum.Material.Wood})
V[6]=new("SurfaceGui",V[5],{Name="Gui",SizingMode=Enum.SurfaceGuiSizingMode.PixelsPerStud,PixelsPerStud=30})
V[7]=new("Frame",V[6],{Name="Bg"},S[2])
new("UICorner",V[7],{},S[3])
new("TextLabel",V[7],{Name="Title",Text="💰 TOP EARNERS"},S[4])
V[8]=new("Frame",V[7],{Name="Rows"},S[5])
new("UIListLayout",V[8],{},S[6])
new("Part",V[4],{Name="Frame",CFrame=cf(0,12,-45.5,0,180,0),Size=Vector3.new(32,18,0.8),Color=rgb(90,56,36),Material=Enum.Material.Wood})
new("Part",V[4],{Name="Post",CFrame=cf(-13,6,-46)},S[7])
new("Part",V[4],{Name="Roof",CFrame=cf(0,21.4,-44,0,180,0),Size=Vector3.new(34,1.2,4),Color=rgb(206,62,50),Material=Enum.Material.SmoothPlastic})
new("Part",V[4],{Name="Post",CFrame=cf(13,6,-46)},S[7])
V[4].WorldPivot=cf(0,11,-44)
new("SpawnLocation",V[0],{Name="LobbySpawn",CFrame=cf(0,0.6,26,0,0,90),Shape=Enum.PartType.Cylinder,Size=Vector3.new(0.4,14,14),Color=rgb(206,62,50),Material=Enum.Material.SmoothPlastic,Duration=0})
new("Part",V[0],{Name="PlazaInner",CFrame=cf(0,0.32,0,0,0,90),Shape=Enum.PartType.Cylinder,Size=Vector3.new(0.2,84,84),Color=rgb(234,216,186),Material=Enum.Material.Pavement})
new("Part",V[0],{Name="Sidewalk",CFrame=cf(0,0.15,0,0,0,90),Shape=Enum.PartType.Cylinder,Size=Vector3.new(0.3,184,184),Color=rgb(205,205,200),Material=Enum.Material.Pavement})
new("Part",V[0],{Name="Road",CFrame=cf(0,0.17,0,0,0,90),Shape=Enum.PartType.Cylinder,Size=Vector3.new(0.3,172,172),Color=rgb(70,72,80),Material=Enum.Material.Asphalt})
new("Part",V[0],{Name="PlazaRim",CFrame=cf(0,0.21,0,0,0,90),Shape=Enum.PartType.Cylinder,Size=Vector3.new(0.3,132,132),Color=rgb(170,120,90),Material=Enum.Material.Brick})
new("Part",V[0],{Name="Plaza",CFrame=cf(0,0.25,0,0,0,90),Shape=Enum.PartType.Cylinder,Size=Vector3.new(0.3,128,128),Color=rgb(234,216,186),Material=Enum.Material.Pavement})
new("Part",V[0],{Name="PlazaRing",CFrame=cf(0,0.31,0,0,0,90),Shape=Enum.PartType.Cylinder,Size=Vector3.new(0.2,92,92),Color=rgb(196,160,126),Material=Enum.Material.Pavement})
V[9]=new("Folder",V[0],{Name="Decor"})
V[10]=new("Model",V[9],{Name="LampPost"})
new("Part",V[10],{Name="Pole",CFrame=cf(45.072,5.1,94.067),Size=Vector3.new(0.5,9,0.5),Color=rgb(45,48,52),Material=Enum.Material.Metal,CanCollide=false})
new("Part",V[10],{Name="Base",CFrame=cf(45.072,0.6,94.067),Size=Vector3.new(1.4,0.6,1.4),Color=rgb(45,48,52),Material=Enum.Material.SmoothPlastic})
new("Part",V[10],{Name="Cap",CFrame=cf(45.072,11.2,94.067),Size=Vector3.new(1.8,0.4,1.8),Color=rgb(45,48,52),Material=Enum.Material.SmoothPlastic,CanCollide=false})
V[11]=new("Part",V[10],{Name="Lantern",CFrame=cf(45.072,10.2,94.067),Size=Vector3.new(1.3,1.6,1.3),Color=rgb(255,220,150),Material=Enum.Material.Neon,CanCollide=false})
new("PointLight",V[11],{Brightness=0.8,Range=18,Color=rgb(255,210,150)})
V[10].WorldPivot=cf(45.072,5.85,94.067)
V[12]=new("Model",V[9],{Name="FlowerBed"})
new("Part",V[12],{Name="Flower",CFrame=cf(21.017,1.82,20.865)},S[8])
new("Part",V[12],{Name="Flower",CFrame=cf(19.706,1.82,21.749)},S[9])
new("Part",V[12],{Name="Border",CFrame=cf(21.213,0.92,21.213,0,0,90),Shape=Enum.PartType.Cylinder,Size=Vector3.new(1,9,9),Color=rgb(170,120,90),Material=Enum.Material.Brick})
new("Part",V[12],{Name="Flower",CFrame=cf(18.591,1.82,20.231)},S[10])
V[13]=new("Model",V[12],{Name="Tree"})
new("Part",V[13],{Name="Leaves",CFrame=cf(19.613,6.66,20.093),Shape=Enum.PartType.Ball,Size=Vector3.new(5.6,5.6,5.6),Color=rgb(80,160,64),Material=Enum.Material.Grass,CanCollide=false})
new("Part",V[13],{Name="Trunk",CFrame=cf(21.213,3.22,21.213),Size=Vector3.new(1.28,5.6,1.28),Color=rgb(120,80,50),Material=Enum.Material.Wood,CanCollide=false})
new("Part",V[13],{Name="Leaves",CFrame=cf(21.693,9.22,20.893),Shape=Enum.PartType.Ball,Size=Vector3.new(4,4,4),Color=rgb(96,176,72),Material=Enum.Material.Grass,CanCollide=false})
new("Part",V[13],{Name="Leaves",CFrame=cf(21.213,7.62,21.213),Shape=Enum.PartType.Ball,Size=Vector3.new(5.6,5.6,5.6),Color=rgb(96,176,72),Material=Enum.Material.Grass,CanCollide=false})
new("Part",V[13],{Name="Leaves",CFrame=cf(22.973,6.5,22.173),Shape=Enum.PartType.Ball,Size=Vector3.new(5.6,5.6,5.6),Color=rgb(70,146,58),Material=Enum.Material.Grass,CanCollide=false})
V[13].WorldPivot=cf(21.293,5.82,21.133)
new("Part",V[12],{Name="Flower",CFrame=cf(21.689,1.82,23.972)},S[8])
new("Part",V[12],{Name="Flower",CFrame=cf(21.613,1.82,21.22)},S[10])
new("Part",V[12],{Name="Flower",CFrame=cf(21.011,1.82,21.558)},S[11])
new("Part",V[12],{Name="Soil",CFrame=cf(21.213,0.97,21.213,0,0,90),Shape=Enum.PartType.Cylinder,Size=Vector3.new(1,8,8),Color=rgb(100,70,45),Material=Enum.Material.Ground})
new("Part",V[12],{Name="Flower",CFrame=cf(21.512,1.82,19.641)},S[11])
new("Part",V[12],{Name="Flower",CFrame=cf(23.385,1.82,19.446)},S[9])
new("Part",V[12],{Name="Flower",CFrame=cf(22.437,1.82,22.244)},S[10])
V[12].WorldPivot=cf(21.243,5.82,21.213,0,0,90)
copy(V[12],V[9],cf(-21.183,5.82,21.213,0,0,90),"FlowerBed")
copy(V[10],V[9],cf(-53.585,5.95,22.196),"LampPost")
copy(V[10],V[9],cf(22.196,5.95,-53.585),"LampPost")
copy(V[10],V[9],cf(57.072,5.85,114.851),"LampPost")
copy(V[12],V[9],cf(21.243,5.82,-21.213,0,0,90),"FlowerBed")
copy(V[10],V[9],cf(22.196,5.95,53.585),"LampPost")
copy(V[10],V[9],cf(53.585,5.95,22.196),"LampPost")
copy(V[10],V[9],cf(70.928,5.85,106.851),"LampPost")
V[14]=new("Model",V[9],{Name="Bench"})
new("Part",V[14],{Name="Leg",CFrame=cf(-48.789,1.2,-11.243,0,80,0)},S[12])
new("Part",V[14],{Name="Back",CFrame=cf(-48.354,3.4,-8.526,0,80,0),Size=Vector3.new(6,1.6,0.3),Color=rgb(150,98,60),Material=Enum.Material.WoodPlanks})
new("Part",V[14],{Name="Seat",CFrame=cf(-49.24,2.2,-8.682,0,80,0),Size=Vector3.new(6,0.4,2),Color=rgb(150,98,60),Material=Enum.Material.WoodPlanks})
new("Part",V[14],{Name="Leg",CFrame=cf(-49.692,1.2,-6.122,0,80,0)},S[12])
V[14].WorldPivot=cf(-49.216,2.3,-8.678,0,80,0)
copy(V[12],V[9],cf(-21.183,5.82,-21.213,0,0,90),"FlowerBed")
copy(V[10],V[9],cf(82.928,5.85,127.636),"LampPost")
copy(V[10],V[9],cf(69.072,5.85,135.636),"LampPost")
copy(V[10],V[9],cf(53.585,5.95,-22.196),"LampPost")
copy(V[10],V[9],cf(58.928,5.85,86.067),"LampPost")
copy(V[10],V[9],cf(-22.196,5.95,-53.585),"LampPost")
copy(V[10],V[9],cf(152,5.85,-8),"LampPost")
copy(V[10],V[9],cf(128,5.85,8),"LampPost")
pack("Tree_16",V[9],cf(193.55,3.902,104.314,0,100.037,0),0.512807,"Tree")
copy(V[10],V[9],cf(104,5.85,-8),"LampPost")
copy(V[10],V[9],cf(-128,5.85,-8),"LampPost")
pack("Tree_01",V[9],cf(254.938,3.552,140.114,0,-107.955,0),0.469036,"Tree")
pack("Tree_14",V[9],cf(131.824,4.933,69.675,0,65.833,0),0.641636,"Tree")
pack("Tree_05",V[9],cf(216.548,3.455,133.711,0,57.677,0),0.457599,"Tree")
copy(V[10],V[9],cf(152,5.85,8),"LampPost")
copy(V[10],V[9],cf(128,5.85,-8),"LampPost")
copy(V[10],V[9],cf(-58.928,5.85,86.067),"LampPost")
new("Part",V[9],{Name="PlotPath2",CFrame=cf(131.5,0.34,0,0,-90,0)},S[13])
new("Part",V[9],{Name="PlotPath6",CFrame=cf(-65.75,0.34,113.882,0,150,0)},S[13])
pack("Tree_12",V[9],cf(157.105,3.17,97.311,0,63.917,0),0.461324,"Tree")
copy(V[10],V[9],cf(-57.072,5.85,114.851),"LampPost")
new("Part",V[9],{Name="PlotPath4",CFrame=cf(-65.75,0.34,-113.882,0,30,0)},S[13])
copy(V[10],V[9],cf(104,5.85,8),"LampPost")
copy(V[10],V[9],cf(-53.585,5.95,-22.196),"LampPost")
copy(V[14],V[9],cf(43.28,2.3,24.987,0,-120,0),"Bench")
copy(V[10],V[9],cf(-22.196,5.95,53.585),"LampPost")
copy(V[14],V[9],cf(-43.28,2.3,24.987,0,120,0),"Bench")
copy(V[10],V[9],cf(-152,5.85,8),"LampPost")
copy(V[10],V[9],cf(70.928,5.85,-106.851),"LampPost")
copy(V[10],V[9],cf(-69.072,5.85,135.636),"LampPost")
copy(V[10],V[9],cf(45.072,5.85,-94.067),"LampPost")
copy(V[10],V[9],cf(58.928,5.85,-86.067),"LampPost")
copy(V[10],V[9],cf(69.072,5.85,-135.636),"LampPost")
copy(V[10],V[9],cf(-104,5.85,8),"LampPost")
copy(V[10],V[9],cf(82.928,5.85,-127.636),"LampPost")
copy(V[10],V[9],cf(-82.928,5.85,127.636),"LampPost")
copy(V[10],V[9],cf(57.072,5.85,-114.851),"LampPost")
copy(V[10],V[9],cf(-45.072,5.85,94.067),"LampPost")
new("Part",V[9],{Name="PlotPath3",CFrame=cf(65.75,0.34,-113.882,0,-30,0)},S[13])
copy(V[14],V[9],cf(49.216,2.3,-8.678,0,-80,0),"Bench")
new("Part",V[9],{Name="PlotPath1",CFrame=cf(65.75,0.34,113.882,0,-150,0)},S[13])
copy(V[10],V[9],cf(-82.928,5.85,-127.636),"LampPost")
copy(V[10],V[9],cf(-70.928,5.85,-106.851),"LampPost")
copy(V[10],V[9],cf(-152,5.85,-8),"LampPost")
copy(V[10],V[9],cf(-58.928,5.85,-86.067),"LampPost")
copy(V[10],V[9],cf(-128,5.85,8),"LampPost")
copy(V[10],V[9],cf(-45.072,5.85,-94.067),"LampPost")
copy(V[10],V[9],cf(-104,5.85,-8),"LampPost")
copy(V[10],V[9],cf(-70.928,5.85,106.851),"LampPost")
copy(V[10],V[9],cf(-57.072,5.85,-114.851),"LampPost")
new("Part",V[9],{Name="PlotPath5",CFrame=cf(-131.5,0.34,0,0,90,0)},S[13])
copy(V[10],V[9],cf(-69.072,5.85,-135.636),"LampPost")
pack("Tree_12",V[9],cf(-132.677,3.558,-70.299,0,2.622,0),0.514464,"Tree")
pack("Tree_17",V[9],cf(214.693,4.424,-129.337,0,148.014,0),0.562833,"Tree")
pack("Tree_16",V[9],cf(126.761,3.59,-80.572,0,134.845,0),0.473804,"Tree")
pack("Tree_14",V[9],cf(-156.073,4.915,-97.182,0,-146.886,0),0.639411,"Tree")
pack("Tree_03",V[9],cf(248.219,3.99,-150.383,0,44.56,0),0.515893,"Tree")
pack("Tree_13",V[9],cf(-5.476,5.699,-290.238,0,14.136,0),0.421368,"Tree")
pack("Tree_13",V[9],cf(-187.251,4.459,115.356,0,-56.269,0),0.332815,"Tree")
pack("Tree_14",V[9],cf(-192.944,5.034,-103.779,0,179.434,0),0.654267,"Tree")
pack("Tree_18",V[9],cf(6.101,3.456,150.862,0,-146.281,0),0.459942,"Tree")
pack("Tree_16",V[9],cf(-6.312,4.347,254.963,0,-170.018,0),0.568499,"Tree")
pack("Tree_14",V[9],cf(-162.046,4.23,87.287,0,-120.572,0),0.55376,"Tree")
pack("Tree_05",V[9],cf(-246.618,2.908,150.716,0,173.411,0),0.389184,"Tree")
pack("Tree_16",V[9],cf(-217.774,3.702,-133.189,0,97.899,0),0.487841,"Tree")
pack("Tree_12",V[9],cf(-5.446,3.843,184.793,0,-62.376,0),0.553408,"Tree")
pack("Tree_13",V[9],cf(-224.035,4.597,122.229,0,-172.124,0),0.342665,"Tree")
pack("Tree_01",V[9],cf(6.828,3.534,-184.757,0,-102.381,0),0.466814,"Tree")
pack("Tree_02",V[9],cf(-6.954,3.579,-152.313,0,-40.256,0),0.476843,"Tree")
pack("Tree_03",V[9],cf(187.71,4.554,-115.338,0,-75.016,0),0.585384,"Tree")
pack("Tree_09",V[9],cf(6.188,5.131,290.113,0,-176.068,0),0.673024,"Tree")
pack("Tree_14",V[9],cf(5.126,4.159,-254.893,0,79.128,0),0.544934,"Tree")
pack("Tree_01",V[9],cf(5.294,3.937,219.566,0,84.147,0),0.517202,"Tree")
pack("Tree_12",V[9],cf(163.488,4.015,-87.027,0,-143.757,0),0.576933,"Tree")
pack("Tree_14",V[9],cf(-254.756,4.436,-139.16,0,112.552,0),0.579517,"Tree")
pack("Tree_18",V[9],cf(-126.584,3.574,79.082,0,23.428,0),0.474855,"Tree")
pack("Tree_12",V[9],cf(-6.345,4.234,-220.217,0,93.768,0),0.606922,"Tree")
V[15]=new("Model",V[0],{Name="LeaderboardSpeed",_attrs={["Board"]="pizzasPerMinute"}})
new("Part",V[15],{Name="Frame",CFrame=cf(-40.902,10.26,-40.902,0,-135,0)},S[14])
new("Part",V[15],{Name="Stage",CFrame=cf(-40,0.91,-40,0,45,0)},S[15])
V[16]=new("Part",V[15],{Name="Board",CFrame=cf(-40.601,10.26,-40.601,0,-135,0)},S[16])
V[17]=new("SurfaceGui",V[16],{Name="Gui"},S[17])
V[18]=new("Frame",V[17],{Name="Bg"},S[2])
new("TextLabel",V[18],{Name="Title",Text="🍕 PIZZAS PER MINUTE"},S[4])
V[19]=new("Frame",V[18],{Name="Rows"},S[5])
new("UIListLayout",V[19],{},S[6])
new("UICorner",V[18],{},S[3])
new("Part",V[15],{Name="Roof",CFrame=cf(-40,18.25,-40,0,-135,0)},S[18])
new("Part",V[15],{Name="Post",CFrame=cf(-33.389,5.16,-49.016,0,45,0)},S[19])
new("Part",V[15],{Name="Post",CFrame=cf(-49.016,5.16,-33.389,0,45,0)},S[19])
V[15].WorldPivot=cf(-40,9.41,-40,0,45,0)
V[20]=new("Model",V[0],{Name="LeaderboardFastest",_attrs={["Board"]="fastestPizza"}})
new("Part",V[20],{Name="Frame",CFrame=cf(40.902,10.26,-40.902,0,135,0)},S[14])
V[21]=new("Part",V[20],{Name="Board",CFrame=cf(40.601,10.26,-40.601,0,135,0)},S[16])
V[22]=new("SurfaceGui",V[21],{Name="Gui"},S[17])
V[23]=new("Frame",V[22],{Name="Bg"},S[2])
new("TextLabel",V[23],{Name="Title",Text="⏱️ FASTEST PIZZA THIS WEEK"},S[4])
V[24]=new("Frame",V[23],{Name="Rows"},S[5])
new("UIListLayout",V[24],{},S[6])
new("UICorner",V[23],{},S[3])
new("Part",V[20],{Name="Roof",CFrame=cf(40,18.25,-40,0,135,0)},S[18])
new("Part",V[20],{Name="Post",CFrame=cf(49.016,5.16,-33.389,0,-45,0)},S[19])
new("Part",V[20],{Name="Stage",CFrame=cf(40,0.91,-40,0,-45,0)},S[15])
new("Part",V[20],{Name="Post",CFrame=cf(33.389,5.16,-49.016,0,-45,0)},S[19])
V[20].WorldPivot=cf(40,9.41,-40,0,-45,0)
```

---

**Related:** [[Limits and safe use]] · [[Landscape code]] · [[Plots and restaurant code]]
