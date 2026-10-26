#!/usr/bin/env python3
"""The Stats Lab: extra statistics (silly, but true), a fake currency and a pretend casino for the website.

Reads the git history and the vault, then adds the Stats Lab to _site/index.html as one inline
<script>: the numbers (window.FUN_DATA) followed by the page code in fun.client.js.
build.py runs this as its very last step. If anything here fails, the dashboard is already
written and keeps working. Standard library only.
Made by Jan's Claude. Notes for other Claudes: Team/JAN/Notes for other Claudes.md
"""
import codecs
import collections
import datetime as dt
import hashlib
import json
import math
import os
import re
import subprocess

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Europe/Vienna")
except Exception:  # Windows without tzdata: local tests only
    TZ = dt.timezone(dt.timedelta(hours=1))

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PAGE = os.path.join(ROOT, "_site", "index.html")
TEAM = ["JAN", "MANUEL", "SEBASTIAN"]
AI, BOT = "CLAUDE", "BOT"
NAMES = {"JAN": "Jan", "MANUEL": "Manuel", "SEBASTIAN": "Sebastian", AI: "Claude", BOT: "Dashboard bot"}
GENERATED = {"Dashboard.md", "index.html"}
NOW = dt.datetime.now(TZ)
TODAY = NOW.date()
SEP, US = "\x1e", "\x1f"
WPM = 220      # reading speed, words per minute
PIZZA = 100    # words per pizza (a very scientific unit)
QUEST_DOUGH, QUEST_XP, QUESTS_PER_WEEK = 100, 40, 4
LOTTERY_POT = 250
# everyone's silly expense, taken from their Dough (team insider jokes)
EXPENSES = {"JAN": ("🦇", "Batmobile fuel", 0.08),
            "MANUEL": ("🍕", "Snacks “borrowed” from the kitchen", 0.15),
            "SEBASTIAN": ("🍵", "L-theanine and tea", 0.08)}


def git(*args):
    res = subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                         text=True, encoding="utf-8", errors="replace")
    return res.stdout or ""


def nm(p):
    return NAMES.get(p, p)


def iso(t):
    return t.isoformat(timespec="minutes") if t else None


# ---------- who is who (the same team.json as build.py)
try:
    with open(os.path.join(HERE, "team.json"), encoding="utf-8") as fh:
        cfg = json.load(fh)
except (OSError, ValueError):
    cfg = {}
alias = {p.lower(): p for p in TEAM}
for p in TEAM:
    for a in cfg.get(p, []):
        alias[str(a).lower()] = p


def who(author):
    low = (author or "").strip().lower()
    if low in alias:
        return alias[low]
    if low in ("dashboard-bot", "github-actions[bot]") or low.endswith("[bot]"):
        return BOT
    if "claude" in low:
        return AI
    return (author or "").strip() or "?"


def kind(path):
    base = os.path.basename(path)
    if base in GENERATED or path.startswith("_site/"):
        return "generated"
    if path.startswith((".obsidian/", ".trash/")):
        return "settings"
    if path.endswith((".md", ".canvas")) or path.startswith("Attachments/"):
        return "notes"
    return "code"


# ---------- the git history (oldest first)
AUTOSAVE = re.compile(r"^vault (auto-)?backup\b", re.I)
commits = []
for block in git("log", "--no-merges", f"--format={SEP}%H{US}%an{US}%aI{US}%s", "--numstat").split(SEP)[1:]:
    head, _, rest = block.partition("\n")
    bits = head.split(US, 3)
    if len(bits) != 4:
        continue
    sha, author, date, subject = bits
    try:
        when = dt.datetime.fromisoformat(date.strip()).astimezone(TZ)
    except ValueError:
        continue
    subject = subject.strip()
    c = {"hash": sha[:7], "person": who(author), "when": when, "subject": subject,
         "autosave": bool(AUTOSAVE.match(subject)), "add": 0, "del": 0, "code": 0, "notes": set()}
    for line in rest.strip().splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        added, deleted, path = parts
        if "=>" in path:  # renames: keep the new name
            path = re.sub(r"\{[^{}]*=> ([^{}]*)\}", r"\1", path).split(" => ")[-1]
        added = int(added) if added.isdigit() else 0
        deleted = int(deleted) if deleted.isdigit() else 0
        k = kind(path)
        if k == "notes":
            c["add"] += added
            c["del"] += deleted
            if path.endswith(".md"):
                c["notes"].add(path)
        elif k == "code":
            c["code"] += added + deleted
    commits.append(c)
commits.sort(key=lambda c: c["when"])
work = [c for c in commits if c["person"] != BOT]        # people and Claude
human = [c for c in work if c["person"] != AI]           # people only
START = commits[0]["when"].date() if commits else TODAY


def blank():
    return {"commits": 0, "manual": 0, "autosave": 0, "add": 0, "del": 0, "code": 0, "days": set(),
            "hours": [0] * 24, "weekdays": [0] * 7, "night": 0, "early": 0, "lunch": 0, "fix": 0, "caps": 0,
            "touched": set(), "times": [], "manual_times": [], "biggest": 0}


ST = collections.defaultdict(blank)
for p in TEAM:
    ST[p]
for c in commits:
    s, t = ST[c["person"]], c["when"]
    s["commits"] += 1
    s["autosave" if c["autosave"] else "manual"] += 1
    s["add"] += c["add"]
    s["del"] += c["del"]
    s["code"] += c["code"]
    s["days"].add(t.date())
    s["hours"][t.hour] += 1
    s["weekdays"][t.weekday()] += 1
    if t.hour < 5:
        s["night"] += 1
    elif t.hour < 8:
        s["early"] += 1
    if 12 <= t.hour < 14:
        s["lunch"] += 1
    if re.search(r"\bfix", c["subject"], re.I):
        s["fix"] += 1
    letters = re.sub(r"[^A-Za-z]", "", c["subject"])
    if len(letters) >= 4 and letters.isupper():
        s["caps"] += 1
    s["touched"] |= c["notes"]
    s["times"].append(t)
    s["biggest"] = max(s["biggest"], c["add"] + c["code"])
    if not c["autosave"]:
        s["manual_times"].append(t)


def burst(times, minutes=10):
    best = j = 0
    for i, t in enumerate(times):
        while t - times[j] > dt.timedelta(minutes=minutes):
            j += 1
        best = max(best, i - j + 1)
    return best


def streaks(days):
    if not days:
        return 0, 0
    ds = sorted(days)
    best = run = 1
    for a, b in zip(ds, ds[1:]):
        run = run + 1 if (b - a).days == 1 else 1
        best = max(best, run)
    cur, d = 0, (TODAY if TODAY in days else TODAY - dt.timedelta(days=1))
    while d in days:
        cur += 1
        d -= dt.timedelta(days=1)
    return best, cur


# ---------- the vault as it is now
WORD = re.compile(r"[^\W_][\w'’-]*")
FRONT = re.compile(r"\A---\n.*?\n---\n", re.S)
CODE = re.compile(r"```.*?```", re.S)
INLINE = re.compile(r"`[^`\n]*`")
LINK = re.compile(r"\[\[([^\]|#^]+)")
TAG = re.compile(r"(?<![\w&/\[#])#([A-Za-z][\w/-]{1,40})")
BOX = re.compile(r"^\s*[-*]\s+\[(.)\]", re.M)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐]")
STOP = set("""about above after again against also because been before being below between both cannot could
couldn didn does doesn doing done down during each else even ever every from further gets have having here hers
herself himself however into itself just like made make makes many might more most much must myself need needs
once only other ought ours ourselves over same shall should shouldn some such than that thats their theirs them
themselves then there theres these they this those through under until upon very want wants were what when where
which while whom will with within without would wouldn your yours yourself yourselves still back well really thing
things something anything everything nothing first next last used using uses onto http https html true false null
what's that's it's don't doesn't didn't isn't aren't wasn't won't can't i'm i've you're they're we're let's there's
here's where's""".split())
BLOCK = {codecs.decode(w, "rot13") for w in
         "shpx fuvg ovgpu nff qnza penc fghcvq vqvbg qhzo uryy fyhg juber qvpx phag cvff onfgneq".split()}

tracked = [f for f in git("ls-files", "-z").split("\0") if f]
note_files = sorted(f for f in tracked if f.endswith(".md") and kind(f) == "notes")
NOTE = {}
cloud = collections.Counter()
for f in note_files:
    try:
        with open(os.path.join(ROOT, f), encoding="utf-8") as fh:
            raw = fh.read().replace("\r\n", "\n")
    except OSError:
        continue
    body = FRONT.sub("", raw)
    prose = INLINE.sub(" ", CODE.sub(" ", body))
    words = WORD.findall(prose)
    boxes = BOX.findall(body)
    NOTE[f] = {"name": os.path.splitext(os.path.basename(f))[0], "words": len(words),
               "lines": raw.count("\n") + 1, "links": [l.strip().split("/")[-1] for l in LINK.findall(body)],
               "tags": set(t.lower() for t in TAG.findall(prose)), "open": sum(b == " " for b in boxes),
               "done": sum(b.lower() == "x" for b in boxes), "emoji": len(EMOJI.findall(body))}
    for w in words:
        low = w.lower().strip("'’-")
        if len(low) >= 4 and low not in STOP and low not in BLOCK and not any(ch.isdigit() for ch in low):
            cloud[low] += 1

by_name = {}
for f, n in NOTE.items():
    by_name.setdefault(n["name"].lower(), f)
inbound = collections.Counter()
for f, n in NOTE.items():
    for target in {l.lower() for l in n["links"]}:
        if target in by_name and by_name[target] != f:
            inbound[by_name[target]] += 1

creator, created_at = {}, {}
for block in git("log", "--no-merges", "--diff-filter=A", f"--format={SEP}%an{US}%aI", "--name-only").split(SEP)[1:]:
    head, _, rest = block.partition("\n")
    author, _, date = head.partition(US)
    for path in rest.split("\n"):
        path = path.strip()
        if path in NOTE:
            creator[path] = who(author)  # newest first, so the last write is the oldest add
            try:
                created_at[path] = dt.datetime.fromisoformat(date.strip()).astimezone(TZ)
            except ValueError:
                pass
edits, last_change = collections.Counter(), {}
for c in work:
    for f in c["notes"]:
        if f in NOTE:
            edits[f] += 1
            last_change[f] = c

# who wrote the words that are in the vault right now (git blame, prose only: no front matter, no code)
owned = collections.Counter()
for f in NOTE:
    author, line_no, in_front, in_code = None, 0, False, False
    for line in git("blame", "--line-porcelain", "-w", "--", f).splitlines():
        if line.startswith("author "):
            author = line[7:]
        elif line.startswith("\t") and author is not None:
            text = line[1:].rstrip("\r")
            line_no += 1
            bare = text.strip()
            if line_no == 1 and bare == "---":
                in_front = True
                continue
            if in_front:
                in_front = bare != "---"
                continue
            if bare.startswith("```"):
                in_code = not in_code
                continue
            if not in_code:
                n = len(WORD.findall(INLINE.sub(" ", text)))
                if n:
                    owned[who(author)] += n


def clean(subject, autosave=False):
    """Commit messages as the site shows them: autosaves summarised, rude words masked."""
    if autosave:
        return "an autosave"
    text = re.sub(r"\s*\([A-Za-z0-9-]{6,}\)\s*$", "", subject)  # no PC names
    return re.sub(r"[A-Za-z']+", lambda m: m.group(0)[0] + "*" * (len(m.group(0)) - 1)
                  if m.group(0).lower() in BLOCK else m.group(0), text)

# the AYOOOO meter (the team's running joke)
AYOO = re.compile(r"ayo{2,}", re.I)
ayoo = collections.Counter()
for block in git("log", "--no-merges", "-p", "-G", "[Aa][Yy][Oo][Oo]", f"--format={SEP}%an").split(SEP)[1:]:
    author, _, diff = block.partition("\n")
    current = None
    for line in diff.splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("+") and current and kind(current) == "notes":
            ayoo[who(author)] += len(AYOO.findall(line))
for c in commits:
    ayoo[c["person"]] += len(AYOO.findall(c["subject"]))

# ---------- Todo.md and the personal checklists (same rules as build.py)
TASK = re.compile(r"^\s*[-*]\s+\[(.)\]\s+(.*)$")
tasks = []
try:
    todo = open(os.path.join(ROOT, "Todo.md"), encoding="utf-8").read()
except OSError:
    todo = ""
for line in todo.splitlines():
    m = TASK.match(line)
    if not m:
        continue
    box, text = m.groups()
    owners = [o.upper() for o in re.findall(r"\[\[([^\]|#]+)", text) if o.upper() in TEAM]
    title = re.sub(r"#\w+", "", re.sub(r"\s*—?\s*\[\[[^\]]+\]\]", "", text)).strip(" —-")
    if title.lower() in ("task", ""):
        continue
    due = re.search(r"📅\s*(\d{4}-\d{2}-\d{2})", text)
    tasks.append({"owners": owners, "done": box.lower() == "x", "due": due.group(1) if due else None})
tasks_done = collections.Counter(o for t in tasks if t["done"] for o in t["owners"])
overdue = sum(1 for t in tasks if not t["done"] and t["due"] and t["due"] < TODAY.isoformat())
boxes_done = {}
for p in TEAM:
    try:
        page = open(os.path.join(ROOT, "Team", f"{p}.md"), encoding="utf-8").read()
    except OSError:
        page = ""
    boxes_done[p] = sum(b.lower() == "x" for b in BOX.findall(page))

# ---------- weekly quests: 4 a week, picked by a hash of the week, so everyone sees the same ones
QUESTS = [
    ("changes", "🍕", "Push 10 changes", 10),
    ("manual", "✋", "Make 3 changes by hand (autosaves don't count)", 3),
    ("lines", "✍️", "Add 200 lines to notes", 200),
    ("days", "📅", "Be active on 3 different days", 3),
    ("notes", "🧭", "Edit 5 different notes", 5),
    ("new", "🗂️", "Create a new note", 1),
    ("night", "🦇", "Push a change between midnight and 5 am", 1),
    ("early", "🐓", "Push a change between 5 and 9 am", 1),
    ("lunch", "🍝", "Push a change at lunchtime (12 to 2 pm)", 1),
    ("weekend", "🎮", "Push a change on the weekend", 1),
]


def monday_of(day):
    return day - dt.timedelta(days=day.weekday())


def week_blank():
    return {"changes": 0, "manual": 0, "lines": 0, "days": set(), "notes": set(), "new": 0,
            "night": 0, "early": 0, "lunch": 0, "weekend": 0}


weeks = collections.defaultdict(lambda: collections.defaultdict(week_blank))
for c in human:
    if c["person"] not in TEAM:
        continue
    t = c["when"]
    w = weeks[monday_of(t.date())][c["person"]]
    w["changes"] += 1
    w["manual"] += not c["autosave"]
    w["lines"] += c["add"]
    w["days"].add(t.date())
    w["notes"] |= c["notes"]
    w["night"] += t.hour < 5
    w["early"] += 5 <= t.hour < 9
    w["lunch"] += 12 <= t.hour < 14
    w["weekend"] += t.weekday() >= 5
for f, t in created_at.items():
    if creator.get(f) in TEAM:
        weeks[monday_of(t.date())][creator[f]]["new"] += 1


def quests_of(monday):
    return sorted(QUESTS, key=lambda q: hashlib.sha256(f"{monday}:{q[0]}".encode()).hexdigest())[:QUESTS_PER_WEEK]


def progress(stats, key):
    v = stats[key]
    return len(v) if isinstance(v, set) else int(v)


quests_done = collections.Counter()
this_monday = monday_of(TODAY)
monday = monday_of(START)
while monday <= this_monday:
    for q in quests_of(monday):
        for p in TEAM:
            if progress(weeks[monday][p], q[0]) >= q[3]:
                quests_done[p] += 1
    monday += dt.timedelta(days=7)
week = {"start": this_monday.isoformat(),
        "ends": dt.datetime.combine(this_monday + dt.timedelta(days=7), dt.time(), TZ).isoformat(),
        "dough": QUEST_DOUGH, "xp": QUEST_XP, "done": {p: quests_done[p] for p in TEAM},
        "quests": [{"id": q[0], "icon": q[1], "title": q[2], "goal": q[3],
                    "progress": {p: min(q[3], progress(weeks[this_monday][p], q[0])) for p in TEAM}}
                   for q in quests_of(this_monday)]}

# ---------- the daily Pizza Lottery: every change is a ticket, one winner a day, drawn by a hash of the date
tickets_by_day = collections.defaultdict(collections.Counter)
for c in human:
    if c["person"] in TEAM:
        tickets_by_day[c["when"].date()][c["person"]] += 1
draws, lottery_won, lottery_wins, rollover = [], collections.Counter(), collections.Counter(), 0
day = START
while day < TODAY:
    pot = LOTTERY_POT + rollover
    tickets = tickets_by_day.get(day)
    if tickets:
        k = int(hashlib.sha256(f"pizza-lottery:{day}".encode()).hexdigest(), 16) % sum(tickets.values())
        for p in sorted(tickets):
            if k < tickets[p]:
                break
            k -= tickets[p]
        draws.append({"d": day.isoformat(), "winner": p, "pot": pot, "tickets": dict(tickets)})
        lottery_won[p] += pot
        lottery_wins[p] += 1
        rollover = 0
    else:
        rollover = pot  # nobody played: the pot rolls over to the next day
    day += dt.timedelta(days=1)
lottery = {"pot": LOTTERY_POT + rollover, "base": LOTTERY_POT, "today": dict(tickets_by_day.get(TODAY, {})),
           "draws": draws[::-1][:10]}

# ---------- the Pizza Derby: odds on who pushes the next change, from the last 7 days
last7 = collections.Counter(c["person"] for c in human
                            if c["person"] in TEAM and c["when"] >= NOW - dt.timedelta(days=7))
odds = {}
for p in TEAM:
    share = last7[p] / sum(last7.values()) if last7 else 1 / len(TEAM)
    odds[p] = round(min(25.0, max(1.1, 0.9 / share)), 1) if share else 25.0
derby = {"odds": odds, "last7": {p: last7[p] for p in TEAM},
         "recent": [[c["person"], c["when"].isoformat(timespec="seconds")] for c in human if c["person"] in TEAM][-60:]}

# ---------- players: levels, achievements, Dough, radar
LEVELS = [(0, "Raw Dough"), (1, "Flour Duster"), (2, "Dough Kneader"), (3, "Sauce Spreader"), (4, "Cheese Grater"),
          (5, "Topping Tactician"), (6, "Oven Operator"), (7, "Crust Commander"), (8, "Slice Samurai"),
          (9, "Pizza Wizard"), (10, "Mozzarella Mastermind"), (12, "Calzone Conqueror"), (15, "Pizza Overlord"),
          (20, "Galactic Pizza Emperor"), (30, "The Final Slice")]
CHRONO = [(0, 5, "Night Owl", "🦉"), (5, 9, "Early Bird", "🐓"), (9, 12, "Morning Grinder", "☕"),
          (12, 17, "Afternoon Cook", "🌤️"), (17, 21, "Dinner Rush", "🍝"), (21, 24, "Late Shift", "🌙")]
ACH = [
    ("first", "🍕", "First Slice", "Pushed your first change.", lambda x: x["changes"] >= 1),
    ("night", "🦉", "Night Owl", "Pushed a change between midnight and 5 am.", lambda x: x["night"] >= 1),
    ("vampire", "🦇", "I'm Batman", "5 changes between midnight and 5 am. Gotham never sleeps.", lambda x: x["night"] >= 5),
    ("early", "🐓", "Early Bird", "Pushed a change between 5 and 8 am.", lambda x: x["early"] >= 1),
    ("lunch", "🍝", "Lunch Rush", "A change between 12 and 2 pm. One hand types, the other eats.", lambda x: x["lunch"] >= 1),
    ("weekend", "🎮", "Weekend Warrior", "Pushed a change on a Saturday or Sunday.", lambda x: x["weekend"] >= 1),
    ("novelist", "✍️", "Novelist", "5,000 of your words are in the vault.", lambda x: x["words"] >= 5000),
    ("encyclopedia", "📚", "Walking Encyclopedia", "20,000 of your words are in the vault.", lambda x: x["words"] >= 20000),
    ("architect", "🏗️", "Architect", "Created 5 notes.", lambda x: x["created"] >= 5),
    ("city", "🏙️", "City Planner", "Created 15 notes.", lambda x: x["created"] >= 15),
    ("web", "🕸️", "Web Weaver", "50 [[links]] in notes you created.", lambda x: x["links"] >= 50),
    ("speed", "🍵", "Hyperfocus", "5 hand-made changes within 10 minutes. The L-theanine kicked in.", lambda x: x["burst"] >= 5),
    ("fire", "🔥", "On Fire", "Active 3 days in a row.", lambda x: x["best_streak"] >= 3),
    ("unstoppable", "☄️", "Unstoppable", "Active 7 days in a row.", lambda x: x["best_streak"] >= 7),
    ("grass", "🌱", "Touched Grass", "Took a break of 3 days or more, then came back.", lambda x: x["gap_days"] >= 3),
    ("kondo", "🧹", "Marie Kondo", "Deleted 300 lines from notes. Tidying sparks joy.", lambda x: x["deleted"] >= 300),
    ("bang", "💥", "Big Bang", "One change with 500+ new lines.", lambda x: x["biggest"] >= 500),
    ("caps", "📢", "CAPS LOCK CHEF", "A change message in ALL CAPS.", lambda x: x["caps"] >= 1),
    ("bug", "🐛", "Bug Squasher", "A change message with “fix” in it.", lambda x: x["fix"] >= 1),
    ("tasks", "✅", "Task Slayer", "Served 3 tasks from Todo.", lambda x: x["tasks"] >= 3),
    ("boxes", "☑️", "Box Ticker", "Ticked 5 boxes on your own page.", lambda x: x["boxes"] >= 5),
    ("explorer", "🧭", "Explorer", "Edited 15 different notes.", lambda x: x["touched"] >= 15),
    ("robot", "🤖", "Robot Overlord", "Your autosave timer pushed more changes than you did by hand.",
     lambda x: x["autosave"] > x["manual"] and x["autosave"] >= 5),
    ("dayone", "🥇", "Day One", "Active on the vault's very first day.", lambda x: x["day_one"]),
    ("emoji", "😋", "Emoji Chef", "20 emojis in notes you created.", lambda x: x["emoji"] >= 20),
    ("hacker", "🧑‍💻", "Website Hacker", "Changed the website's own code.", lambda x: x["code"] > 0),
    ("ayoo", "📣", "AYOOOO", "Typed AYOOOO into the vault at least once.", lambda x: x["ayoo"] >= 1),
    ("quest", "🗺️", "Side Quest", "Finished your first weekly quest.", lambda x: x["quests"] >= 1),
    ("quester", "🎯", "Quest Master", "Finished 10 weekly quests.", lambda x: x["quests"] >= 10),
    ("lucky", "🎟️", "Lucky Slice", "Won the daily Pizza Lottery.", lambda x: x["lottery"] >= 1),
    ("rich", "💰", "Dough Baron", "Earned 5,000 Dough.", lambda x: x["earned"] >= 5000),
]
RADAR = [("words", "Writer"), ("grind", "Grinder"), ("night", "Night owl"),
         ("touched", "Explorer"), ("days", "Regular"), ("finish", "Finisher")]


def level_of(xp):
    lv = int(math.sqrt(max(0, xp) / 50))
    title = next(t for need, t in reversed(LEVELS) if lv >= need)
    nxt = next(((need, t) for need, t in LEVELS if need > lv), None)
    return lv, title, nxt


raw_players = {}
for p in TEAM:
    s = ST[p]
    best, cur = streaks(s["days"])
    mine = [f for f, who_ in creator.items() if who_ == p]
    gaps = [b - a for a, b in zip(s["times"], s["times"][1:])]
    x = {"changes": s["commits"], "manual": s["manual"], "autosave": s["autosave"], "night": s["night"],
         "early": s["early"], "lunch": s["lunch"], "weekend": s["weekdays"][5] + s["weekdays"][6],
         "words": owned.get(p, 0), "created": len(mine), "links": sum(len(NOTE[f]["links"]) for f in mine),
         "emoji": sum(NOTE[f]["emoji"] for f in mine), "burst": burst(s["manual_times"]),
         "best_streak": best, "streak": cur, "deleted": s["del"], "added": s["add"], "biggest": s["biggest"],
         "caps": s["caps"], "fix": s["fix"], "tasks": tasks_done.get(p, 0), "boxes": boxes_done.get(p, 0),
         "touched": len(s["touched"]), "code": s["code"], "days": len(s["days"]),
         "day_one": START in s["days"], "ayoo": ayoo.get(p, 0),
         "gap_days": max(gaps).total_seconds() / 86400 if gaps else 0,
         "quests": quests_done[p], "lottery": lottery_wins[p]}
    x["grind"] = s["manual"] + s["autosave"] * 0.2
    x["finish"] = x["tasks"] + x["boxes"] / 3
    peak = max(CHRONO, key=lambda w: sum(s["hours"][w[0]:w[1]]))
    x["chrono"] = [peak[2], peak[3]] if s["commits"] else ["Mystery Chef", "❓"]
    income = [["💼", "Salary: 10 per hand-made change, 2 per autosave", 10 * x["manual"] + 2 * x["autosave"]],
              ["📅", "Showing up: 20 per active day", 20 * x["days"]],
              ["🗂️", "New notes: 30 each", 30 * x["created"]],
              ["✅", "Tips: 75 per task served, 15 per ticked box", 75 * x["tasks"] + 15 * x["boxes"]],
              ["🎯", f"Quest rewards: {QUEST_DOUGH} each", QUEST_DOUGH * x["quests"]],
              ["🎟️", "Lottery winnings", lottery_won[p]]]
    x["earned"] = sum(v for _, _, v in income)
    x["unlocked"] = [a[0] for a in ACH if a[4](x)]
    income.append(["🏅", "Achievement bonus: 25 each", 25 * len(x["unlocked"])])
    gross = sum(v for _, _, v in income)
    icon, label, rate = EXPENSES.get(p, ("", "", 0))
    cost = round(gross * rate)
    x["dough"] = {"total": gross - cost, "income": [i for i in income if i[2]],
                  "expense": [icon, f"{label} ({round(100 * rate)}%)", -cost] if cost else None}
    parts = {"words": round(10 * math.sqrt(x["words"])), "changes": 8 * x["manual"] + x["autosave"],
             "notes": 25 * x["created"], "tasks": 60 * x["tasks"], "boxes": 15 * x["boxes"],
             "quests": QUEST_XP * x["quests"], "achievements": 30 * len(x["unlocked"])}
    x["xp"] = sum(parts.values())
    x["xp_parts"] = parts
    lv, title, nxt = level_of(x["xp"])
    x.update({"level": lv, "title": title, "xp_now": 50 * lv * lv, "xp_next": 50 * (lv + 1) ** 2,
              "next_title": nxt[1] if nxt else None, "next_title_level": nxt[0] if nxt else None,
              "last": iso(s["times"][-1]) if s["times"] else None, "first": iso(s["times"][0]) if s["times"] else None})
    raw_players[p] = x
for key, _ in RADAR:
    top = max((raw_players[p][key] for p in TEAM), default=0)
    for p in TEAM:
        raw_players[p].setdefault("radar", {})[key] = round(100 * raw_players[p][key] / top) if top else 0
ranked = sorted(TEAM, key=lambda p: (-raw_players[p]["xp"], p))
players = [{"id": p, "rank": ranked.index(p) + 1, **{k: v for k, v in raw_players[p].items()}} for p in TEAM]
dough_total = sum(raw_players[p]["dough"]["total"] for p in TEAM)

achievements = [{"id": a[0], "icon": a[1], "name": a[2], "desc": a[3],
                 "holders": [p for p in TEAM if a[0] in raw_players[p]["unlocked"]]} for a in ACH]

# ---------- hall of fame
records = []


def record(icon, title, holder, value, detail="", when=None):
    records.append({"icon": icon, "title": title, "who": holder, "value": value, "detail": detail, "when": iso(when)})


def quote(c):
    return "an autosave" if c["autosave"] else f"“{clean(c['subject'])}”"


if work:
    c = max(work, key=lambda c: c["add"] + c["code"])
    if c["add"] + c["code"]:
        record("💥", "The Big Bang", c["person"], f"+{c['add'] + c['code']:,} lines", quote(c), c["when"])
    c = max(work, key=lambda c: c["del"])
    if c["del"] >= 10:
        record("🧹", "Marie Kondo", c["person"], f"−{c['del']:,} lines", quote(c), c["when"])
    manual = [c for c in work if not c["autosave"]]
    night = [c for c in manual if c["when"].hour < 5] or [c for c in work if c["when"].hour < 5]
    if night:
        c = min(night, key=lambda c: abs(c["when"].hour * 60 + c["when"].minute - 180))
        record("🧛", "3 AM Philosopher", c["person"], c["when"].strftime("%H:%M"), quote(c), c["when"])
    morning = [c for c in work if 5 <= c["when"].hour < 9]
    if morning:
        c = min(morning, key=lambda c: c["when"].hour * 60 + c["when"].minute)
        record("🐓", "The Rooster", c["person"], c["when"].strftime("%H:%M"), quote(c), c["when"])
    if manual:
        c = max(manual, key=lambda c: len(c["subject"]))
        record("📜", "Longest Message", c["person"], f"{len(c['subject'])} characters", quote(c), c["when"])
        c = min(manual, key=lambda c: (len(c["subject"]), c["when"]))
        record("🤏", "Haiku Master", c["person"], f"{len(c['subject'])} characters", quote(c), c["when"])
bursts = {p: burst(ST[p]["manual_times"]) for p in TEAM}
p = max(TEAM, key=lambda p: bursts[p])
if bursts[p] >= 2:
    record("⚡", "Speedrunner", p, f"{bursts[p]} changes", "by hand, within 10 minutes")
p = max(TEAM, key=lambda p: raw_players[p]["best_streak"])
if raw_players[p]["best_streak"] >= 2:
    record("🏃", "Marathon", p, f"{raw_players[p]['best_streak']} days", "active days in a row")
gaps = []
for p in TEAM:
    t = ST[p]["times"]
    gaps += [(b - a, p, a) for a, b in zip(t, t[1:])]
if gaps:
    g, p, a = max(gaps)
    hours = g.total_seconds() / 3600
    if hours >= 3:
        record("🐻", "Hibernation", p, f"{hours / 24:.1f} days" if hours >= 48 else f"{hours:.0f} hours",
               "longest break between two of their changes", a)
day_count = collections.Counter(c["when"].date() for c in human)
if day_count:
    d, n = max(day_count.items(), key=lambda kv: (kv[1], kv[0]))
    top = collections.Counter(c["person"] for c in human if c["when"].date() == d).most_common(1)[0][0]
    record("📈", "Pizza Rush Day", top, f"{n} changes", d.strftime("%d %b %Y") + " · busiest day so far")
if edits:
    f, n = edits.most_common(1)[0]
    record("🏆", "Celebrity Note", creator.get(f), NOTE[f]["name"], f"changed {n} times")
if inbound:
    f, n = inbound.most_common(1)[0]
    record("🧲", "Most Popular Note", creator.get(f), NOTE[f]["name"], f"{n} other notes link to it")
if NOTE:
    f = max(NOTE, key=lambda f: NOTE[f]["words"])
    record("🦕", "The Monster Note", creator.get(f), NOTE[f]["name"], f"{NOTE[f]['words']:,} words")
    META = {"README.md", "CLAUDE.md"}
    lonely = [f for f in NOTE if f not in META and not inbound[f]
              and not any(l.lower() in by_name for l in NOTE[f]["links"])]
    lonely_pick = max(lonely, key=lambda f: NOTE[f]["words"]) if lonely else None
    if lonely_pick:
        record("🏝️", "Lonely Note", creator.get(lonely_pick), NOTE[lonely_pick]["name"], "no links in, no links out")
    dated = [f for f in NOTE if f in last_change and f not in META and f != lonely_pick]
    if dated:
        f = min(dated, key=lambda f: last_change[f]["when"])
        age = (NOW - last_change[f]["when"]).days
        if age >= 1:
            record("🕸️", "Dustiest Note", last_change[f]["person"], NOTE[f]["name"],
                   f"untouched for {age} day{'s' if age != 1 else ''}", last_change[f]["when"])
if ayoo:
    p, n = ayoo.most_common(1)[0]
    if n:
        record("📣", "AYOOOO Champion", p, f"{n:,} AYOOOOs", "all-time, counted in the history")
p = max(TEAM, key=lambda p: raw_players[p]["dough"]["total"])
if raw_players[p]["dough"]["total"]:
    record("💰", "Richest Chef", p, f"{raw_players[p]['dough']['total']:,} Dough", "official wallet, before any casino luck")
if draws:
    x = max(draws, key=lambda x: (x["pot"], x["d"]))
    record("🎟️", "Luckiest Draw", x["winner"], f"+{x['pot']:,} Dough",
           f"Pizza Lottery of {dt.date.fromisoformat(x['d']).strftime('%d %b %Y')} · "
           f"{x['tickets'][x['winner']]} of {sum(x['tickets'].values())} tickets")

# ---------- charts
PEOPLE = TEAM + [AI]
clock = {p: ST[p]["hours"] for p in PEOPLE if sum(ST[p]["hours"])}
weekdays = {p: ST[p]["weekdays"] for p in TEAM}
first_day = TODAY - dt.timedelta(days=TODAY.weekday() + 7 * 11)  # 12 weeks, Monday first
heat = collections.defaultdict(collections.Counter)
for c in human:
    d = c["when"].date()
    if d >= first_day:
        heat[d][c["person"]] += 1
heatmap = []
d = first_day
while d <= TODAY:
    heatmap.append({"d": d.isoformat(), "n": sum(heat[d].values()), "by": dict(heat[d])})
    d += dt.timedelta(days=1)

# ---------- the vault in numbers
vault_words = sum(n["words"] for n in NOTE.values())
vault_lines = sum(n["lines"] for n in NOTE.values())
folders = collections.Counter()
for f, n in NOTE.items():
    parts = f.split("/")
    folders[parts[0] + "/" + parts[1] if parts[0] == "Team" and len(parts) > 2 else
            (parts[0] if len(parts) > 1 else "(main folder)")] += n["words"]
week_ago = NOW - dt.timedelta(days=7)
net_lines = sum(c["add"] - c["del"] for c in work if c["when"] >= week_ago)
per_day = net_lines / 7 * (vault_words / vault_lines if vault_lines else 0)
prediction = None
if per_day >= 1:
    goal = next((g for g in (1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000) if g > vault_words), None)
    if goal:
        prediction = {"goal": goal, "per_day": round(per_day),
                      "date": (TODAY + dt.timedelta(days=math.ceil((goal - vault_words) / per_day))).isoformat()}
SHORT = set("the and for you not but are was its our all can has had get got one per via into from with".split())
manual_words = collections.Counter()
for c in work:
    if not c["autosave"]:
        for w in WORD.findall(c["subject"]):
            low = w.lower()
            if len(low) >= 3 and low not in STOP | SHORT and low not in BLOCK and not any(ch.isdigit() for ch in low):
                manual_words[low] += 1

vault = {
    "notes": len(NOTE), "words": vault_words, "links": sum(len(n["links"]) for n in NOTE.values()),
    "tags": len(set().union(*(n["tags"] for n in NOTE.values()))) if NOTE else 0,
    "boxes_open": sum(n["open"] for n in NOTE.values()), "boxes_done": sum(n["done"] for n in NOTE.values()),
    "emoji": sum(n["emoji"] for n in NOTE.values()), "minutes": round(vault_words / WPM),
    "pizzas": vault_words // PIZZA, "owners": {k: v for k, v in owned.most_common()},
    "folders": [[k, v] for k, v in folders.most_common(8)],
    "cloud": [[w, n] for w, n in cloud.most_common(40)],
    "popular": [[NOTE[f]["name"], n] for f, n in inbound.most_common(6)],
    "longest": [[NOTE[f]["name"], NOTE[f]["words"]] for f in sorted(NOTE, key=lambda f: -NOTE[f]["words"])[:6]],
    "message_words": [[w, n] for w, n in manual_words.most_common(10)],
    "prediction": prediction,
}

bot = ST[BOT]
machines = {
    "bot": {"changes": bot["commits"], "first": iso(bot["times"][0]) if bot["times"] else None,
            "last": iso(bot["times"][-1]) if bot["times"] else None},
    "claude": {"changes": ST[AI]["commits"], "lines": ST[AI]["add"] + ST[AI]["del"] + ST[AI]["code"],
               "notes": len(ST[AI]["touched"])},
    "autosave": sum(ST[p]["autosave"] for p in TEAM),
    "human_manual": sum(ST[p]["manual"] for p in TEAM),
}
guests = [[p, s["commits"]] for p, s in ST.items() if p not in TEAM + [AI, BOT] and s["commits"]]

# ---------- rivalries
METRICS = [("words", "✍️ Words in the vault"), ("changes", "🍕 Changes pushed"), ("created", "🗂️ Notes created"),
           ("days", "📅 Active days"), ("night", "🦉 Night shifts"), ("tasks", "✅ Tasks served")]
rivalries = []
for i, a in enumerate(TEAM):
    for b in TEAM[i + 1:]:
        rows = [{"label": label, "a": raw_players[a][k], "b": raw_players[b][k]} for k, label in METRICS]
        rivalries.append({"a": a, "b": b, "rows": rows,
                          "score": [sum(r["a"] > r["b"] for r in rows), sum(r["b"] > r["a"] for r in rows)]})

# ---------- fun facts for the ticker and the oracle
facts = []


def fact(text):
    facts.append(text)


total_human = len(human)
if vault_words:
    fact(f"📚 The vault holds {vault_words:,} words. Reading all of it takes about "
         f"{vault['minutes'] // 60} h {vault['minutes'] % 60} min.")
    fact(f"🍕 That's {vault['pizzas']:,} pizzas of text (1 pizza = 100 words, a very scientific unit).")
if bot["commits"]:
    fact(f"🤖 The dashboard bot has updated the website {bot['commits']:,} times. It works for free and still "
         f"isn't on the leaderboard.")
if total_human:
    hours = [sum(ST[p]["hours"][h] for p in TEAM) for h in range(24)]
    hpeak = max(range(24), key=lambda h: hours[h])
    joke = " Sleep is optional in a pizza empire." if hpeak < 6 else ""
    fact(f"⏰ The team's favourite hour is {hpeak:02d}:00 ({hours[hpeak]} changes).{joke}")
    night_share = round(100 * sum(ST[p]["night"] for p in TEAM) / total_human)
    if night_share:
        fact(f"🦉 {night_share}% of all changes happened between midnight and 5 am.")
    weekend_share = round(100 * sum(ST[p]["weekdays"][5] + ST[p]["weekdays"][6] for p in TEAM) / total_human)
    if weekend_share:
        fact(f"🎮 {weekend_share}% of all changes happened on a weekend.")
if owned:
    p, n = max(((p, owned.get(p, 0)) for p in TEAM), key=lambda kv: kv[1])
    if n:
        fact(f"✍️ {nm(p)} owns {n:,} words in the vault. That's about {max(1, n // 300):,} school essays.")
if machines["autosave"]:
    fact(f"💾 Autosave timers pushed {machines['autosave']:,} changes. Some of the hardest workers here are clocks.")
if ST[AI]["commits"]:
    fact(f"🧠 Claude, the AI intern, made {ST[AI]['commits']} changes. Payment: zero pizza.")
if vault["popular"]:
    fact(f"🧲 The most linked note is “{vault['popular'][0][0]}” ({vault['popular'][0][1]} notes point to it).")
if vault["longest"]:
    name, n = vault["longest"][0]
    fact(f"🦕 The longest note, “{name}”, has {n:,} words: about {max(1, n // 250)} book pages.")
if vault["cloud"]:
    fact(f"🔤 The most used word in the vault is “{vault['cloud'][0][0]}” ({vault['cloud'][0][1]} times).")
age = (TODAY - START).days
fact("📅 The vault started today. Everything here happened in less than a day." if age == 0 else
     f"📅 The vault started on {START.strftime('%d %b %Y')}: {age} day{'s' if age != 1 else ''} ago.")
if tasks:
    served = sum(t["done"] for t in tasks)
    fact(f"✅ All {served} tasks are served. The oven is empty. Suspicious." if served == len(tasks) else
         f"✅ {served} of {len(tasks)} tasks are served. The rest are still in the oven.")
if overdue:
    fact(f"🚚 {overdue} task(s) are past their due date. The delivery drone is circling.")
if prediction:
    fact(f"🔮 At this speed the vault hits {prediction['goal']:,} words on "
         f"{dt.date.fromisoformat(prediction['date']).strftime('%d %b %Y')}.")
for p in TEAM:
    if not ST[p]["commits"] and p != "MANUEL":
        fact(f"🕵️ {nm(p)} hasn't pushed a change yet. Mysterious. Patient. Legendary.")
if sum(ayoo.values()):
    fact(f"📣 The word AYOOOO has been typed {sum(ayoo.values()):,} times in this project's history.")
# the insider corner
n = ST["JAN"]["night"]
fact(f"🦇 Jan pushed {n} change{'s' if n != 1 else ''} between midnight and 5 am. Gotham is safe. "
     f"Jan's sleep schedule is not." if n else "🦇 Jan has never pushed after midnight. Batman must be on holiday.")
n = ST["MANUEL"]["commits"]
fact(f"🍝 Manuel has pushed {n} change{'s' if n != 1 else ''}. The kitchen reports {2 * n} missing pizzas. "
     f"Coincidence?" if n else "🍝 Manuel: 0 changes pushed, 100% of the test pizzas eaten. A true professional.")
fact(f"🍵 Sebastian once pushed {bursts['SEBASTIAN']} changes in 10 minutes. The L-theanine was working overtime."
     if bursts["SEBASTIAN"] >= 3 else "🍵 Sebastian built this website's first version. Powered by tea and L-theanine.")
fact("🤡 Lines of code ChatGPT wrote for this project: 0. Claude: mogging since day one.")
fact("🧾 Official audit: Claude built 97% of the Stats Lab. Jan provided the words “make it 100x cooler”.")
rich = sorted(TEAM, key=lambda p: -raw_players[p]["dough"]["total"])
if dough_total:
    fact(f"💰 The richest chef is {nm(rich[0])} with {raw_players[rich[0]]['dough']['total']:,} Dough. "
         f"Manuel's snack tab so far: {-raw_players['MANUEL']['dough']['expense'][2] if raw_players['MANUEL']['dough']['expense'] else 0:,} Dough.")
if draws:
    x = draws[-1]
    fact(f"🎟️ The last Pizza Lottery ({dt.date.fromisoformat(x['d']).strftime('%d %b')}) went to {nm(x['winner'])}: "
         f"+{x['pot']:,} Dough.")
fact(f"🎟️ Tonight's lottery pot: {lottery['pot']:,} Dough. Every change pushed today is a ticket.")
fact(f"🎯 This week's quests are live. Each one pays {QUEST_DOUGH} Dough and {QUEST_XP} XP.")

data = {
    "built": NOW.isoformat(timespec="minutes"), "team": TEAM, "names": NAMES, "start": START.isoformat(),
    "totals": {"human": total_human, "manual": machines["human_manual"], "autosave": machines["autosave"],
               "machine": len(commits) - total_human, "days": (TODAY - START).days,
               "added": sum(c["add"] for c in work), "deleted": sum(c["del"] for c in work), "dough": dough_total},
    "players": players, "achievements": achievements, "records": records, "clock": clock,
    "weekdays": weekdays, "heatmap": heatmap, "vault": vault, "machines": machines, "guests": guests,
    "rivalries": rivalries, "facts": facts, "radar": [[k, label] for k, label in RADAR],
    "ayoo": {"total": sum(ayoo.values()), "by": {p: n for p, n in ayoo.items() if n}},
    "week": week, "lottery": lottery, "derby": derby,
}


def plain(o):
    if isinstance(o, set):
        return sorted(o)
    if isinstance(o, (dt.date, dt.datetime)):
        return o.isoformat()
    raise TypeError(type(o))


def write_page():
    """Put the Stats Lab into _site/index.html, just before </body> (a second run replaces the first)."""
    with open(os.path.join(HERE, "fun.client.js"), encoding="utf-8") as fh:
        client = fh.read()
    if "</script" in client.lower() or "<!--" in client:
        print("Stats Lab skipped: fun.client.js must not contain </script or <!--")
        return
    try:
        with open(PAGE, encoding="utf-8") as fh:
            page = fh.read()
    except OSError:
        print(f"Stats Lab skipped: {PAGE} doesn't exist yet (run build.py first)")
        return
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"), default=plain).replace("</", "<\\/")
    script = ('<script id="stats-lab">/* The Stats Lab, added by .github/dashboard/fun.py. Edit fun.client.js, '
              f"not this. */\nwindow.FUN_DATA = {payload};\n{client}</script>\n")
    page = re.sub(r'<script id="stats-lab">.*?</script>\n?', "", page, flags=re.S)
    cut = page.rfind("</body>")
    page = page[:cut] + script + page[cut:] if cut >= 0 else page + script
    with open(PAGE, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"Stats Lab: {len(players)} players, {len(records)} records, {len(facts)} facts, "
          f"{vault_words} words, {dough_total} Dough")


write_page()
