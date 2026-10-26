---
tags:
  - manuel
  - pictures
updated: 2026-10-26
---

# Picture Checklist

Part of [[Manuel Home]]. All 90 menu pictures, from `ServerStorage > TeamGuide > 2_IMAGE_PROMPTS` in the game (copied 2026-10-26). Tick a box when the image is in `UIAssets` and checked in Play.

## How it works
1. Make all images in the **same ChatGPT chat**. If one looks different, say: "same style as the previous ones".
2. Every prompt ends with STYLE. Paste the STYLE text below at the end of the prompt.
3. Send the PNG to Manuel's Claude (or: Studio > Window > Asset Manager > Import > right-click > **Copy Asset ID**).
4. The ID goes into `ReplicatedStorage > Shared > UIAssets`: `tomato = { image = "rbxassetid://THE_NUMBER", emoji = "🍅" },`
5. Play (F5) and check. A new image can take a few minutes while Roblox checks it.
6. After the session: 1-3 lines at the top of PART 1 in the team notebook (in Studio) + [[Manuel Changelog]].
**STYLE** (copy this):
```text
cute chunky cartoon game icon, thick dark-brown outline, soft cel shading, light from the top left, bright happy colours, rounded shapes, centred with empty space around it, square image, transparent background PNG, no text, no letters, kid-friendly
```

**Sizes:** icons 256x256, pizzas + the celebration icon 512x512, small symbols 128x128 (the subject fills about 80 % of the image).

**Slot names:** "ing.tomato" = in UIAssets, the line "tomato" under UIAssets.Ingredients. (ing = Ingredients, pizza = Pizzas, drone = DroneTasks, upgrade = DroneUpgrades, hud = HUD, stat = Stats, build = Build, station = Stations, no dot = Misc)

## Ingredients (256x256) · 16
- [ ] **ing.dough**: A soft round ball of pizza dough with a little flour dust, STYLE
- [ ] **ing.sauce**: A small red can of tomato sauce with a tomato on the label, STYLE
- [ ] **ing.cheese**: A yellow wedge of cheese with round holes, STYLE
- [ ] **ing.pepperoni**: Three round red pepperoni slices stacked, STYLE
- [ ] **ing.ham**: A pink slice of ham with a light edge, STYLE
- [x] **ing.tomato**: A shiny red tomato with a green leaf top, STYLE
- [x] **ing.pineapple**: A small whole pineapple with spiky green leaves, STYLE
- [x] **ing.mushroom**: A cute brown-capped mushroom, STYLE
- [x] **ing.pepper**: A shiny green pepper, STYLE
- [x] **ing.onion**: A purple and white onion with a little sprout, STYLE
- [x] **ing.olive**: Two dark green olives on a small leaf, STYLE
- [ ] **ing.chicken**: A golden roasted chicken drumstick, STYLE
- [ ] **ing.bacon**: A wavy strip of crispy bacon, STYLE
- [x] **ing.corn**: A yellow corn cob with green husk leaves, STYLE
- [x] **ing.basil**: A sprig of fresh green basil leaves, STYLE
- [ ] **ing.gold**: A sparkly sheet of edible gold leaf with tiny stars around it, STYLE

## Pizzas (512x512) · 11
- [ ] **pizza.margherita**: A round Margherita pizza seen from slightly above: red tomato sauce, melted mozzarella and fresh tomato slices, STYLE
- [ ] **pizza.pepperoni**: A round pepperoni pizza seen from slightly above: melted cheese covered with pepperoni slices, STYLE
- [ ] **pizza.hawaii**: A round Hawaii pizza seen from slightly above: melted cheese with ham pieces and pineapple chunks, STYLE
- [ ] **pizza.veggie**: A round veggie pizza seen from slightly above: melted cheese with mushrooms and green pepper slices, STYLE
- [ ] **pizza.bbq_chicken**: A round BBQ chicken pizza seen from slightly above: melted cheese with chicken pieces and red onion rings, STYLE
- [ ] **pizza.capricciosa**: A round Capricciosa pizza seen from slightly above: ham, mushrooms and dark olives on melted cheese, STYLE
- [ ] **pizza.diavola**: A round Diavola pizza seen from slightly above: pepperoni, red chili slices and onion on melted cheese, STYLE
- [ ] **pizza.garden**: A round garden pizza seen from slightly above: mushrooms, green pepper, corn and basil leaves on melted cheese, STYLE
- [ ] **pizza.meat_lovers**: A round meat lovers pizza seen from slightly above, piled with pepperoni, ham, chicken and bacon, STYLE
- [ ] **pizza.supreme**: A round supreme pizza seen from slightly above, loaded with pepperoni, ham, mushrooms, peppers, onion and olives, STYLE
- [ ] **pizza.golden**: A round golden pizza seen from slightly above: shiny golden crust, basil leaves and gold leaf flakes with sparkles, STYLE

## Drones + upgrades (256x256) · 9
- [ ] **drone.order**: A cute round flying drone with four propellers holding a tiny laptop, STYLE
- [ ] **drone.carry**: A cute round flying drone with four propellers carrying a cardboard box, STYLE
- [ ] **drone.cut**: A cute round flying drone with four propellers above a cutting board with a sliced tomato, STYLE
- [ ] **drone.topping**: A cute round flying drone with four propellers sprinkling cheese onto a pizza, STYLE
- [ ] **drone.oven**: A cute round flying drone with four propellers next to a small brick pizza oven with a warm glow, STYLE
- [ ] **drone.serve**: A cute round flying drone with four propellers carrying a pizza on a silver tray, STYLE
- [ ] **upgrade.speed**: A yellow lightning bolt with speed lines, STYLE
- [ ] **upgrade.capacity**: A small backpack stuffed with cardboard boxes, STYLE
- [ ] **upgrade.battery**: A green full battery with a small lightning bolt, STYLE

## Big buttons on the left (256x256) · 8
- [ ] **hud.open**: A little shop door wide open with warm light and a green glow, STYLE
- [ ] **hud.closed**: A little shop door shut with a red sign hanging on the handle, STYLE
- [ ] **hud.home**: A cute little house with a red roof and a round window, STYLE
- [x] **hud.recipes**: An open recipe book with a pizza drawing on one page, STYLE · ✅ 2026-10-26: Manuel's blue book with a gold compass star, `rbxassetid://87000022272572`
- [ ] **hud.build**: A cartoon hammer with a wooden handle, STYLE
- [ ] **hud.drones**: A cute round flying drone with four propellers and a friendly face, STYLE
- [ ] **hud.stats**: A bar chart with three colourful bars and a small star, STYLE
- [ ] **hud.quests**: A rolled paper scroll with a red ribbon, STYLE

## Stats (256x256) · 18
- [ ] **stat.pizzasServed**: A shiny silver service bell, STYLE
- [ ] **stat.perfectPizzas**: A pizza slice with a big golden star badge, STYLE
- [ ] **stat.tipsEarned**: A glass jar full of gold coins, STYLE
- [ ] **stat.bestTip**: A big shiny gold coin with sparkles, STYLE
- [ ] **stat.fastestPizza**: A stopwatch with speed lines, STYLE
- [ ] **stat.customersLost**: A small sad grey rain cloud, STYLE
- [ ] **stat.dronesBought**: A cute round flying drone with a gift bow on top, STYLE
- [ ] **stat.boxesOrdered**: A stack of three cardboard boxes, STYLE
- [ ] **stat.veggiesCut**: A wooden cutting board with sliced vegetables, STYLE
- [ ] **stat.pizzasMade**: A ball of dough next to a wooden rolling pin, STYLE
- [ ] **stat.pizzasBaked**: A small brick pizza oven with a warm orange glow, STYLE
- [ ] **stat.pizzasBurnt**: A slightly burnt pizza with a small puff of grey smoke, STYLE
- [ ] **stat.itemsPlaced**: A cute wooden chair, STYLE
- [ ] **stat.recipesUnlocked**: An open recipe book with sparkles around it, STYLE
- [ ] **stat.playSeconds**: A round red alarm clock, STYLE
- [ ] **stat.Earned**: A stack of green banknotes, STYLE
- [ ] **stat.Stars**: A big shiny golden star with a happy face, STYLE
- [ ] **stat.PizzasPerMinute**: A pizza slice with a lightning bolt, STYLE

## Build mode (256x256) · 6
- [ ] **build.shop**: A red shopping cart, STYLE
- [ ] **build.backpack**: A cute orange backpack, STYLE
- [ ] **build.edit**: A white cartoon glove hand pointing, STYLE
- [ ] **build.rotate**: A round arrow going in a full circle, STYLE
- [ ] **build.move**: A white cartoon glove hand with four small arrows around it, STYLE
- [ ] **build.store**: A backpack with a big arrow pointing into it, STYLE

## Stations (256x256) · 6
- [ ] **station.pc**: A retro computer monitor showing a pizza on the screen, STYLE
- [ ] **station.cut**: A wooden cutting board with a small kitchen knife and a tomato, STYLE
- [ ] **station.prep**: A raw pizza with toppings on a wooden pizza peel, STYLE
- [ ] **station.garage**: A closed cardboard delivery box with tape, STYLE
- [ ] **station.fridge**: A cute light-blue fridge, STYLE
- [ ] **station.truck**: A cute small delivery truck, STYLE

## Other · 16
- [ ] **cash** (256): A stack of green banknotes with a gold coin in front, STYLE
- [ ] **coin** (128): A shiny gold coin with a dollar sign, seen from the front, STYLE
- [ ] **star** (128): A shiny golden star, STYLE
- [ ] **starEmpty** (128): The same star shape but flat light grey and empty, STYLE
- [ ] **lock** (128): A cute golden padlock, STYLE
- [ ] **close** (128): A white X mark, STYLE
- [ ] **check** (128): A white check mark, STYLE
- [ ] **plus** (128): A white plus sign, STYLE
- [ ] **minus** (128): A white minus sign, STYLE
- [ ] **arrow** (256): A big bouncy yellow arrow pointing straight down, STYLE
- [ ] **gift** (256): A wrapped gift box with a red ribbon, STYLE
- [ ] **refill** (256): Two green circular arrows around a small box, STYLE
- [ ] **celebrate** (512): A party popper bursting with colourful confetti, STYLE

These 3 are **WHITE** (the game colours them), so **WITHOUT STYLE**:
- [ ] **confetti** (64): One small confetti piece: a plain pure-white rounded rectangle, flat, no outline, no shading, transparent background
- [ ] **rays** (512): Plain pure-white sun rays bursting from the centre, soft edges, flat, no outline, transparent background
- [ ] **beam** (256x64): A seamless horizontal strip with three plain white chevron arrows pointing right, flat, no outline, transparent background; the left and right edges must line up when the strip repeats

**Total: 90 slots**

## New: seed packets for the hotbar (2026-10-26) · 8
For the seed tools from the slot machine. Not in UIAssets yet: when they're made, Manuel's Claude puts them on the tools (TextureId).
- [ ] **seed.tomato**: A small paper seed packet with a tomato on the front, STYLE
- [ ] **seed.mushroom**: A small paper seed packet with a mushroom on the front, STYLE
- [ ] **seed.pepper**: A small paper seed packet with a green pepper on the front, STYLE
- [ ] **seed.pineapple**: A small paper seed packet with a pineapple on the front, STYLE
- [ ] **seed.onion**: A small paper seed packet with an onion on the front, STYLE
- [ ] **seed.corn**: A small paper seed packet with a corn cob on the front, STYLE
- [ ] **seed.olive**: A small paper seed packet with olives on the front, STYLE
- [ ] **seed.basil**: A small paper seed packet with basil leaves on the front, STYLE

## New: the 24 new seeds (2026-10-26) · 24
One picture per seed: the vegetable/fruit itself (256x256). It's used on the hotbar, the bag, the slot machine and the odds board. In UIAssets: `ing.<id>`.
- [x] **ing.spinach**: A bunch of fresh dark-green spinach leaves, STYLE
- [x] **ing.carrot**: An orange carrot with green leaves on top, STYLE
- [x] **ing.potato**: A round brown potato with small spots, STYLE
- [x] **ing.cucumber**: A green cucumber with a bumpy skin, STYLE
- [x] **ing.chili**: A bright red chili pepper with a curly green stem, STYLE
- [x] **ing.garlic**: A white garlic bulb with one clove next to it, STYLE
- [x] **ing.strawberry**: A shiny red strawberry with green leaves, STYLE
- [x] **ing.broccoli**: A small green broccoli tree, STYLE
- [x] **ing.banana**: A yellow banana, STYLE
- [x] **ing.eggplant**: A shiny purple eggplant with a green cap, STYLE
- [x] **ing.watermelon**: A slice of watermelon with black seeds, STYLE
- [x] **ing.kiwi**: A kiwi cut in half, bright green inside, STYLE
- [x] **ing.cocoa**: An open cocoa pod with cocoa beans and a small chocolate bar, STYLE
- [x] **ing.grapes**: A bunch of purple grapes with a leaf, STYLE
- [x] **ing.ghost_pepper**: A wrinkly orange-red ghost pepper with small flames around it, STYLE
- [x] **ing.dragonfruit**: A pink dragon fruit with green spikes, cut open showing white inside with black seeds, STYLE
- [x] **ing.starfruit**: A yellow star-shaped fruit slice with sparkles, STYLE
- ~~**ing.candy_corn**: Three candy corn sweets (yellow, orange, white stripes), STYLE~~ (seed removed from the game 2026-10-26)
- ~~**ing.golden_apple**: A shiny golden apple with sparkles and a gold leaf, STYLE~~ (seed removed from the game 2026-10-26)
- ~~**ing.rainbow_carrot**: A carrot with rainbow stripes and green leaves, STYLE~~ (seed removed from the game 2026-10-26)
- ~~**ing.moon_melon**: A round pale-blue melon with a glowing crescent moon pattern, STYLE~~ (seed removed from the game 2026-10-26)
- ~~**ing.ghost_pumpkin**: A white glowing pumpkin with a cute ghost face, STYLE~~ (seed removed from the game 2026-10-26)
- ~~**ing.crystal_berry**: A berry made of shiny light-blue crystal, STYLE~~ (seed removed from the game 2026-10-26)
- ~~**ing.galaxy_mushroom**: A mushroom with a dark purple cap full of stars, like a galaxy, STYLE~~ (seed removed from the game 2026-10-26)

---

**Related:** [[Manuel Home]] · [[Manuel Changelog]] · [[MANUEL]]
