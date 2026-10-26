---
aliases:
  - Sebastian
  - Basti
tags:
  - team
  - person
  - qa
updated: 2026-10-26
role: beta testing / QA
---

# SEBASTIAN

## Assignment: Test pass (beta QA)

Goal: test the three things [[Game overview#Not done yet|Game overview]] lists as untested — phones, several players in one server, real saving — and turn every problem into a clear bug report. No code changes needed; you touch nothing other people own.

### 1. Full loop by hand (solo, PC)

- [ ] New save: start with $100, follow all 11 tutorial steps to the first drone
- [ ] Check the numbers match the doc: box delivery 15 s, cut 1.5 s, oven 12 s, burns after 20 s more, customers wait 90 s
- [ ] Serve one wrong pizza: pays half, no tip?
- [ ] Let one customer time out: leaves without paying?

### 2. Phone (Studio Device Emulator + a real phone if possible)

- [ ] All 6 left buttons readable and tappable (OPEN, HOME, RECIPES, BUILD, DRONES, STATS)
- [ ] Build mode: can you place, turn and move items with touch?
- [ ] Carrying boxes, cutting, oven: doable without a keyboard?
- [ ] Nothing on screen overlaps (money, stars, quest pill, goal bar)

### 3. Several players (Studio Test > Clients and Servers, 2–3 players)

- [ ] Each player gets their own plot, gate faces the lobby
- [ ] Customers, money and drones stay on the right plot
- [ ] Leaderboards in the lobby update for both players

### 4. Saving (needs a test place with API access on — ask [[JAN]])

- [ ] Earn money, buy a seat and a drone, leave, rejoin: everything back?
- [ ] Wait 2+ min (auto-save), then force-quit: progress kept?
- [ ] Offline: leave 10 min with drones, rejoin: about 25% of last income per minute?
- [ ] Join from two devices at once: does the session lock stop it?

### Bug report format (one line each, under *Bugs found*)

`[Area] What you did → what happened → what should happen (device, players)`

Example: `[Oven] Took pizza out at 19 s → it burned → should still be fine (PC, solo)`

Done when: all boxes ticked and every bug written down. Then add your 1–3 lines to 0\_TEAM\_NOTEBOOK and tick it off in [[Todo]].

### Bugs found

- 
