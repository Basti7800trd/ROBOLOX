#!/usr/bin/env python3
"""Reads the vault (Todo, checklists, git history) and writes _site/index.html.
Runs in GitHub Actions on every push. Standard library only."""
import json, os, re, subprocess, datetime as dt
from zoneinfo import ZoneInfo
VIE = ZoneInfo("Europe/Vienna")
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
TEAM = ["JAN", "MANUEL", "SEBASTIAN"]
STATUSES = ["open", "doing", "blocked", "done"]

# ---------- who is who
cfg = json.load(open(os.path.join(HERE, "team.json"), encoding="utf-8"))
alias = {}
for person in TEAM:
    alias[person.lower()] = person
    for a in cfg.get(person, []):
        alias[a.lower()] = person
def who(name):
    return alias.get((name or "").strip().lower())

def read(p):
    try:
        return open(os.path.join(ROOT, p), encoding="utf-8").read()
    except OSError:
        return ""

# ---------- tasks in Todo.md
TASK = re.compile(r"^\s*[-*]\s+\[(.)\]\s+(.*)$")
tasks = []
for line in read("Todo.md").splitlines():
    m = TASK.match(line)
    if not m:
        continue
    box, text = m.group(1), m.group(2)
    owners = [o.upper() for o in re.findall(r"\[\[([^\]|#]+)", text) if o.upper() in TEAM]
    tag = next((s for s in STATUSES if re.search(r"#" + s + r"\b", text)), None)
    status = "done" if box.lower() == "x" else (tag if tag and tag != "done" else "open")
    title = re.sub(r"\s*—?\s*\[\[[^\]]+\]\]", "", text)
    title = re.sub(r"#\w+", "", title)
    title = re.sub(r"📅\s*\S+", "", title).strip(" —-")
    due = re.search(r"📅\s*(\d{4}-\d{2}-\d{2})", text)
    if title.lower() in ("task", ""):
        continue  # template placeholder lines
    tasks.append({"title": title, "owners": owners, "status": status, "due": due.group(1) if due else None})

# ---------- checklists on each person's page
checklists = {}
for p in TEAM:
    t = read(f"Team/{p}.md")
    boxes = [m.group(1) for m in map(TASK.match, t.splitlines()) if m]
    checklists[p] = {"done": sum(b.lower() == "x" for b in boxes), "total": len(boxes)}

# ---------- git history
SEP = "\x1e"
log = subprocess.run(
    ["git", "log", "--no-merges", f"--format={SEP}%H%x1f%an%x1f%aI%x1f%s", "--numstat"],
    cwd=ROOT, capture_output=True, text=True).stdout
commits = []
for block in log.split(SEP)[1:]:
    head, _, rest = block.partition("\n")
    h, author, date, subject = head.split("\x1f", 3)
    added = deleted = 0
    files = []
    for ln in rest.strip().splitlines():
        parts = ln.split("\t")
        if len(parts) != 3:
            continue
        a, d, f = parts
        if f.startswith(".obsidian") or f.startswith(".github") or f == "Dashboard.md":
            continue  # settings and the dashboard itself don't count as work
        files.append(f)
        if a != "-":
            added += int(a); deleted += int(d)
    if author in ("dashboard-bot", "github-actions[bot]"):
        continue
    commits.append({"hash": h[:7], "author": author, "person": who(author), "date": date,
                    "subject": subject, "added": added, "deleted": deleted, "files": files})

# ---------- leaderboard (it's a joke, but a fair-ish joke)
# commit with real changes 10 · finished task 50 · ticked checklist box 15 · lines: 1 pt per 10, max 20 per commit
score = defaultdict(lambda: {"commits": 0, "lines": 0, "tasks_done": 0, "boxes": 0,
                             "night": 0, "points": 0, "shortest": None})
for c in commits:
    p = c["person"] or c["author"]
    s = score[p]
    if c["files"]:
        s["commits"] += 1
        s["points"] += 10 + min(20, (c["added"] + c["deleted"]) // 10)
    s["lines"] += c["added"] + c["deleted"]
    hour = dt.datetime.fromisoformat(c["date"]).hour
    if hour >= 23 or hour < 5:
        s["night"] += 1
    if s["shortest"] is None or len(c["subject"]) < len(s["shortest"]):
        s["shortest"] = c["subject"]
for t in tasks:
    if t["status"] == "done":
        for o in t["owners"]:
            score[o]["tasks_done"] += 1
            score[o]["points"] += 50
for p, cl in checklists.items():
    score[p]["boxes"] += cl["done"]
    score[p]["points"] += 15 * cl["done"]
for p in TEAM:
    score[p]  # everyone appears, even with 0

board = sorted(({"name": k, **v} for k, v in score.items()), key=lambda r: (-r["points"], r["name"]))

# fun awards
def best(key):
    rows = [r for r in board if r[key]]
    return max(rows, key=lambda r: r[key])["name"] if rows else None
awards = []
if best("night"):
    awards.append({"title": "Night oven", "who": best("night"), "why": "most commits between 23:00 and 05:00"})
if best("lines"):
    awards.append({"title": "Keyboard smasher", "who": best("lines"), "why": "most lines changed (capped in points, sorry)"})
msgs = [(len(c["subject"]), c) for c in commits if c["files"]]
if msgs:
    _, c = min(msgs, key=lambda x: x[0])
    awards.append({"title": "Poet laureate", "who": c["person"] or c["author"], "why": f"commit message: “{c['subject']}”"})

data = {
    "built": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"),
    "team": TEAM,
    "tasks": tasks,
    "checklists": checklists,
    "board": board,
    "awards": awards,
    "recent": [{k: c[k] for k in ("hash", "author", "person", "date", "subject", "added", "deleted")} for c in commits[:20]],
    "commit_count": len(commits),
    "repo": os.environ.get("GITHUB_REPOSITORY", "Basti7800trd/ROBOLOX"),
}


# ---------- write Dashboard.md
def nm(p): return p.capitalize() if p in TEAM else p
def link(p): return f"[[{p}]]" if p in TEAM else p
def bar(done, total, width=20):
    if not total: return "`" + "░" * width + "`"
    n = round(width * done / total)
    return "`" + "█" * n + "░" * (width - n) + "`"
count = {s: sum(t["status"] == s for t in tasks) for s in STATUSES}
total = len(tasks)
pct = round(100 * count["done"] / total) if total else 0
LABEL = {"open": "Open", "doing": "In the oven", "blocked": "Blocked", "done": "Served"}
TITLES = ["Head pizzaiolo", "Sous-chef", "Dishwasher", "Delivery drone"]
MEDAL = ["🥇", "🥈", "🥉"]
stamp = dt.datetime.now(VIE).strftime("%d %b %Y, %H:%M")

L = []
L += ["---", "tags:", "  - dashboard", f"updated: {dt.date.today().isoformat()}", "---", ""]
L += ["# Dashboard", "",
      f"> [!info] Updated automatically on every push · last update {stamp} (Vienna) · {len(commits)} changes so far",
      "> Don't edit this note by hand — it gets overwritten. Change [[Todo]] instead.", ""]
L += ["## Kitchen status", "",
      f"**{pct}%** done — {count['done']} of {total} tasks served", "",
      bar(count["done"], total, 30), "",
      " · ".join(f"{LABEL[s]} **{count[s]}**" for s in STATUSES), ""]

L += ["## Order rail", ""]
if not tasks:
    L += ["> [!tip] No tasks yet", "> Add one to [[Todo]]: `- [ ] Build the drone menu — [[MANUEL]] #open`", ""]
else:
    for s, icon in [("doing", "🔥"), ("blocked", "⛔"), ("open", "📝"), ("done", "✅")]:
        rows = [t for t in tasks if t["status"] == s]
        if not rows: continue
        L += [f"### {icon} {LABEL[s]} ({len(rows)})", ""]
        for t in rows:
            owners = ", ".join(link(o) for o in t["owners"]) or "*no owner*"
            due = f" · due {t['due']}" if t["due"] else ""
            L.append(f"- {'~~' + t['title'] + '~~' if s == 'done' else t['title']} — {owners}{due}")
        L.append("")

L += ["## Kitchen crew", "", "| | Tasks served | In the oven | Blocked | Own checklist |", "| --- | --- | --- | --- | --- |"]
for p in TEAM:
    mine = [t for t in tasks if p in t["owners"]]
    by = {s: sum(t["status"] == s for t in mine) for s in STATUSES}
    cl = checklists[p]
    clt = f"{bar(cl['done'], cl['total'], 10)} {cl['done']}/{cl['total']}" if cl["total"] else "—"
    L.append(f"| {link(p)} | {by['done']} / {len(mine)} | {by['doing']} | {by['blocked']} | {clt} |")
L.append("")

L += ["## Employee of the month", "", "*Extremely scientific.*", "",
      "| | Who | Title | Points | Tasks | Boxes | Commits | Lines |", "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |"]
for i, r in enumerate(board):
    rank = MEDAL[i] if i < 3 else str(i + 1)
    L.append(f"| {rank} | **{nm(r['name'])}** | {TITLES[min(i, len(TITLES)-1)]} | **{r['points']}** | {r['tasks_done']} | {r['boxes']} | {r['commits']} | {r['lines']} |")
L.append("")
for a in awards:
    L += [f"> [!quote] {a['title']}: {nm(a['who'])}", f"> {a['why']}", ""]
L += ["> [!note]- How points work",
      "> Finished task in [[Todo]] **50** · ticked box on your own page **15** · commit **10** + 1 per 10 lines changed (max 20 per commit, so spamming “AYOOOO” doesn't win). Settings files and this note don't count.", ""]

L += ["## Order log", "", "| When | Who | What | Lines |", "| --- | --- | --- | ---: |"]
for c in commits[:15]:
    when = dt.datetime.fromisoformat(c["date"]).astimezone(VIE).strftime("%d %b %H:%M")
    subj = c["subject"].replace("|", "\\|")
    L.append(f"| {when} | {nm(c['person']) if c['person'] else c['author']} | {subj} | +{c['added']} −{c['deleted']} |")
L.append("")
L += ["---", "", "**Related:** [[Home]] · [[Todo]] · [[Team]]", ""]
open(os.path.join(ROOT, "Dashboard.md"), "w", encoding="utf-8").write("\n".join(L))
print(f"tasks={len(tasks)} commits={len(commits)} leader={board[0]['name']}")
