# Before Publish Checklist

Part of [[Roblox Home]]. What must be true before the user presses "Publish to Roblox". Items marked "(unchecked)" come from the Starter Brief and get verified on create.roblox.com before the first publish.

- [ ] Publishing goes live at once for NEW servers; there's no review queue. (unchecked)
- [ ] Test switches / test buttons off; test-only code runs only under `RunService:IsStudio()`. (unchecked)
- [ ] Experiments happened in the separate test place, not in the real one.
- [ ] Every new image/mesh/audio is owned by the game's owner (the group in a group game) and passed moderation; animations must be owned by the experience owner. (unchecked)
- [ ] Purchases: `ProcessReceipt` saves first, then returns `PurchaseGranted`, and handles the same receipt twice. (unchecked)
- [ ] Paid random items: every outcome with numeric odds summing to 100 %, behind an "Info"/"Details" button. (✔ in the brief, 2026-10-25)
- [ ] Phone check: UI sized in Scale, big touch buttons.
- [ ] After publishing: old servers keep the old version until they're restarted/migrated. (unchecked)
- [ ] Changelog entry + update text ready; the user posts it.
