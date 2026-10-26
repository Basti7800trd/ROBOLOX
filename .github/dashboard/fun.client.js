/* The Stats Lab: the page code. fun.py puts the numbers above this line (window.FUN_DATA).
   It adds a fun-fact ticker, a "Stats Lab" button and the Stats Lab section to index.html.
   Every widget is wrapped, so one broken widget never breaks the page. Made by Jan's Claude. */
(function () {
  "use strict";
  const F = window.FUN_DATA;
  const wrap = document.querySelector(".wrap");
  if (!F || !wrap) return;

  const TEAM = F.team || [];
  const REDUCE = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  const COLORS = { JAN: "var(--tomato)", MANUEL: "var(--basil)", SEBASTIAN: "var(--cheese)", CLAUDE: "#8e6cc1", BOT: "#6b7c8f" };
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const nm = (p) => (F.names && F.names[p]) || p || "Nobody";
  const col = (p) => COLORS[p] || "var(--char)";
  const fmt = (n) => Math.round(Number(n) || 0).toLocaleString("en-US");
  const pad = (n) => String(n).padStart(2, "0");
  const pct = (v, total) => (total ? Math.round((100 * v) / total) : 0);
  const dot = (p) => `<i class="fx-dot" style="background:${col(p)}"></i>`;
  const who = (p) => (p ? `<span class="fx-name">${dot(p)}${esc(nm(p))}</span>` : `<span class="fx-name fx-muted">nobody yet</span>`);
  const hm = (min) => (min >= 60 ? `${Math.floor(min / 60)} h ${min % 60} min` : `${min} min`);
  const pane = (id) => document.getElementById("fx-p-" + id);
  const fmtWhen = (iso) => {
    try { return new Date(iso).toLocaleString("en-GB", { timeZone: "Europe/Vienna", day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }); }
    catch (e) { return iso; }
  };
  const fmtDay = (d) => {
    try { return new Date(d + "T12:00:00").toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" }); }
    catch (e) { return d; }
  };
  const fmtDate = (d) => {
    try { return new Date(d + "T12:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" }); }
    catch (e) { return d; }
  };
  const ago = (iso) => {
    const s = (Date.now() - new Date(iso)) / 1000;
    if (!isFinite(s)) return "recently";
    if (s < 90) return "just now";
    if (s < 3600) return Math.round(s / 60) + " min ago";
    if (s < 86400) return Math.round(s / 3600) + " h ago";
    return Math.round(s / 86400) + " days ago";
  };
  const guard = (box, fn) => {
    try { fn(); }
    catch (e) {
      if (box) box.innerHTML = `<div class="fx-burnt">🔥 This part got burnt in the oven. The chefs have been told (they're asleep).</div>`;
      if (window.console) console.error("Stats Lab:", e);
    }
  };
  const legend = (list) => list.map((p) => `<span>${dot(p)}${esc(nm(p))}</span>`).join("");

  const FORTUNES = [
    "🥠 Why did the pizza get a job? It wanted to make some dough.",
    "🥠 Your next change will be legendary. Probably. Maybe. Possibly a typo.",
    "🥠 The oven believes in you.",
    "🥠 Today's lucky topping: extra cheese.",
    "🥠 Somewhere, a drone is delivering a pizza right now. Be like the drone.",
    "🥠 Error 404: crust not found.",
    "🥠 If at first you don't succeed, add more cheese.",
    "🥠 The stats say: take a snack break. The stats are always right.",
    "🥠 Legends say the dashboard bot dreams of pepperoni.",
    "🥠 Keep calm and knead dough.",
    "🥠 A pizza a day keeps the boredom away.",
    "🥠 Pineapple on pizza is a valid opinion. Discuss quietly.",
    "🥠 Fortune says: commit early, commit often, eat pizza in between.",
    "🥠 The secret ingredient is always more stats.",
  ];

  const CSS = `
.fx-ticker{display:flex;align-items:center;gap:12px;background:var(--tomato);color:#fff;border-radius:999px;padding:7px 18px 7px 7px;
  cursor:pointer;min-height:42px;box-shadow:0 10px 28px -18px var(--tomato);user-select:none}
.fx-ticker .fx-tag{flex:none;background:#fff;color:var(--tomato);border-radius:999px;padding:6px 10px;font:700 .68rem/1 var(--mono);letter-spacing:.12em}
.fx-ticker .fx-say{min-width:0;font:600 .93rem/1.35 var(--body);transition:opacity .3s,transform .3s}
.fx-ticker .fx-say.out{opacity:0;transform:translateY(5px)}
.btn.fx-labbtn{background:var(--ink);border-color:var(--ink);color:var(--panel)}
.btn.fx-labbtn:hover{border-color:var(--tomato)}
#lab{--ai:#8e6cc1;scroll-margin-top:12px}
#lab .eyebrow{display:block}
#lab .fx-banner{position:relative;overflow:hidden;border-radius:20px;padding:22px;border:1px solid var(--line);display:flex;align-items:center;
  justify-content:space-between;gap:18px;background:repeating-conic-gradient(color-mix(in srgb,var(--tomato) 16%,transparent) 0 25%,transparent 0 50%) 0 0/34px 34px,var(--panel)}
#lab .fx-banner-text{background:var(--panel);border-radius:14px;padding:14px 18px;display:grid;gap:6px;max-width:580px;box-shadow:0 14px 30px -22px rgba(0,0,0,.55)}
#lab .fx-banner h2{font-size:clamp(1.7rem,4vw,2.5rem);font-weight:700}
#lab .fx-banner p{margin:0;color:var(--muted)}
#lab .fx-spin{flex:none;width:124px;height:124px;filter:drop-shadow(0 10px 14px rgba(0,0,0,.25));animation:fx-spin 28s linear infinite}
@keyframes fx-spin{to{transform:rotate(360deg)}}
#lab .fx-hero{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px}
#lab .fx-tile{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 10px;display:grid;gap:5px;justify-items:center;text-align:center;min-width:0}
#lab .fx-tile .ic{font-size:1.55rem;line-height:1}
#lab .fx-tile b{font:700 clamp(1.15rem,2.5vw,1.65rem)/1.1 var(--display);font-variant-numeric:tabular-nums}
#lab .fx-tile span{font-size:.76rem;color:var(--muted);line-height:1.25}
#lab .fx-tabs{display:flex;gap:8px;flex-wrap:wrap;position:sticky;top:0;z-index:3;padding:10px 0;background:var(--bg)}
#lab .fx-tab{font:600 .92rem var(--display);padding:9px 15px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--ink);cursor:pointer}
#lab .fx-tab:hover{border-color:var(--tomato)}
#lab .fx-tab[aria-selected="true"]{background:var(--tomato);border-color:var(--tomato);color:#fff}
#lab .fx-pane{display:grid;gap:18px;min-width:0}
#lab .fx-pane[hidden]{display:none}
#lab .fx-h{font-size:1.15rem;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin:0}
#lab .fx-h small{font:600 .68rem var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
#lab .fx-card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:16px;min-width:0;display:grid;gap:12px;align-content:start}
#lab .fx-muted,#lab .fx-foot,#lab .fx-empty-p{color:var(--muted)}
#lab .fx-foot{font-size:.82rem;margin:0}
#lab .fx-empty-p{font-size:.9rem;margin:0}
#lab .fx-name{font-weight:700}
#lab .fx-dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:1px}
#lab .fx-legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:.86rem}
#lab .fx-legend b{font-variant-numeric:tabular-nums}
#lab .fx-players{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;align-items:start}
#lab .fx-player{--c:var(--char);position:relative;background:var(--panel);border:2px solid color-mix(in srgb,var(--c) 45%,var(--line));
  border-radius:20px;padding:16px;display:grid;gap:12px;min-width:0;overflow:hidden}
#lab .fx-player::before{content:"";position:absolute;inset:0 0 auto 0;height:88px;pointer-events:none;
  background:linear-gradient(135deg,color-mix(in srgb,var(--c) 32%,transparent),transparent 75%)}
#lab .fx-player>*{position:relative}
#lab .fx-player.fx-top{border-color:var(--cheese);box-shadow:0 0 0 4px color-mix(in srgb,var(--cheese) 28%,transparent),0 18px 44px -22px var(--cheese)}
#lab .fx-ptop{display:flex;align-items:center;gap:12px}
#lab .fx-ava{width:50px;height:50px;border-radius:15px;display:grid;place-items:center;background:var(--c);color:#fff;font:700 1.45rem var(--display);flex:none;
  box-shadow:0 8px 18px -10px var(--c)}
#lab .fx-pname{display:grid;min-width:0}
#lab .fx-pname strong{font:700 1.3rem/1.1 var(--display)}
#lab .fx-pname span{font-size:.86rem;color:var(--muted)}
#lab .fx-lv{margin-left:auto;display:grid;justify-items:center;background:var(--ink);color:var(--panel);border-radius:12px;padding:6px 10px;min-width:56px}
#lab .fx-lv small{font:700 .56rem var(--mono);letter-spacing:.14em}
#lab .fx-lv b{font:700 1.45rem/1 var(--display)}
#lab .fx-crown{position:absolute;top:2px;right:8px;font-size:1.5rem;line-height:1;cursor:pointer;background:none;border:0;padding:4px;z-index:2}
#lab .fx-player.fx-top .fx-lv{margin-right:34px}
#lab .fx-meta{font:600 .72rem var(--mono);letter-spacing:.05em;color:var(--muted);text-transform:uppercase}
#lab .fx-xpbar{height:12px;border-radius:999px;background:var(--line);overflow:hidden}
#lab .fx-xpbar i{display:block;height:100%;width:0;border-radius:999px;background:linear-gradient(90deg,var(--c),color-mix(in srgb,var(--c) 55%,#fff));
  transition:width 1.2s cubic-bezier(.2,.8,.2,1)}
#lab .fx-xptext{display:flex;justify-content:space-between;gap:8px;font-size:.82rem;color:var(--muted);margin-top:6px;flex-wrap:wrap}
#lab .fx-xptext b{color:var(--ink);font-variant-numeric:tabular-nums}
#lab .fx-radar{width:100%;max-width:270px;justify-self:center;height:auto;overflow:visible}
#lab .fx-radar text{fill:var(--muted);font:600 10px var(--mono)}
#lab .fx-grid{fill:none;stroke:var(--line);stroke-width:1}
#lab .fx-pstats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
#lab .fx-ps{background:var(--bg);border-radius:10px;padding:8px;display:grid;gap:2px;min-width:0}
#lab .fx-ps b{font:700 1.05rem/1.1 var(--display);font-variant-numeric:tabular-nums;overflow-wrap:anywhere}
#lab .fx-ps span{font-size:.7rem;color:var(--muted);line-height:1.2}
#lab .fx-badges{display:flex;flex-wrap:wrap;gap:6px}
#lab .fx-badge{width:34px;height:34px;display:grid;place-items:center;border-radius:10px;background:var(--bg);border:1px solid var(--line);font-size:1.1rem;cursor:help}
#lab details.fx-why summary{cursor:pointer;font-size:.82rem;color:var(--muted)}
#lab details.fx-why ul{margin:8px 0 0;padding-left:18px;font-size:.84rem;display:grid;gap:2px}
#lab .fx-duels{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
#lab .fx-duel-head{display:flex;align-items:center;justify-content:space-between;gap:8px;font:700 1.05rem var(--display)}
#lab .fx-score{font:700 1.15rem var(--mono);background:var(--bg);border-radius:8px;padding:2px 8px}
#lab .fx-drow{display:grid;gap:4px}
#lab .fx-dlabel{display:flex;justify-content:space-between;font-size:.78rem;color:var(--muted);gap:6px}
#lab .fx-dlabel b{color:var(--ink);font-variant-numeric:tabular-nums}
#lab .fx-tug{display:flex;height:8px;border-radius:999px;overflow:hidden;background:var(--line)}
#lab .fx-tug i{display:block;height:100%}
#lab .fx-records{display:grid;grid-template-columns:repeat(auto-fill,minmax(235px,1fr));gap:12px}
#lab .fx-rec{gap:6px}
#lab .fx-rec .ic{font-size:2.1rem;line-height:1}
#lab .fx-rec .fx-val{font:700 1.35rem/1.15 var(--display);overflow-wrap:anywhere}
#lab .fx-rec .fx-det{font-size:.84rem;color:var(--muted);overflow-wrap:anywhere}
#lab .fx-charts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
#lab .fx-wide{grid-column:1/-1}
#lab .fx-svg{width:100%;height:auto;display:block;max-width:420px;justify-self:center}
#lab .fx-wide .fx-svg{max-width:none}
#lab .fx-svg text{fill:var(--muted);font:600 11px var(--mono)}
#lab .fx-night{fill:color-mix(in srgb,var(--ink) 9%,transparent)}
#lab .fx-ring{fill:none;stroke:var(--line)}
#lab .fx-svg .fx-clock-big{font:700 30px var(--display);fill:var(--ink)}
#lab .fx-crust{fill:#c98a48}
#lab .fx-cheese{fill:#f5cf62}
#lab .fx-pep{fill:#b8322a;opacity:.92}
#lab .fx-cut{stroke:#fff8e6;stroke-width:3}
#lab .fx-svg .fx-slice{fill:#2a211c;font:700 15px var(--display)}
#lab .fx-heat{display:flex;gap:6px;overflow-x:auto;padding-bottom:4px}
#lab .fx-hdays{display:grid;grid-template-rows:repeat(7,16px);gap:4px;font:600 .62rem/16px var(--mono);color:var(--muted)}
#lab .fx-hgrid{display:flex;gap:4px}
#lab .fx-hcol{display:grid;grid-template-rows:repeat(7,16px);gap:4px}
#lab .fx-hc{display:block;width:16px;height:16px;border-radius:4px;background:var(--line)}
#lab .fx-hc.l1{background:color-mix(in srgb,var(--tomato) 30%,var(--line))}
#lab .fx-hc.l2{background:color-mix(in srgb,var(--tomato) 55%,var(--line))}
#lab .fx-hc.l3{background:color-mix(in srgb,var(--tomato) 80%,var(--line))}
#lab .fx-hc.l4{background:var(--tomato)}
#lab .fx-hc.fx-future{background:transparent;border:1px dashed var(--line)}
#lab .fx-hlegend{display:flex;align-items:center;gap:4px;font-size:.78rem;color:var(--muted)}
#lab .fx-ach{overflow-x:auto;background:var(--panel);border:1px solid var(--line);border-radius:16px}
#lab .fx-ach table{width:100%;border-collapse:collapse;font-size:.9rem}
#lab .fx-ach th,#lab .fx-ach td{padding:10px 12px;border-top:1px solid var(--line);text-align:center;white-space:normal;vertical-align:middle}
#lab .fx-ach th{border-top:0;font:600 .7rem var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
#lab .fx-ach td:first-child,#lab .fx-ach th:first-child{text-align:left}
#lab .fx-aname{display:flex;gap:10px;align-items:center;min-width:230px}
#lab .fx-aname .ic{font-size:1.45rem}
#lab .fx-aname small{display:block;color:var(--muted);font-size:.78rem}
#lab .fx-got{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;color:#fff;font-weight:700}
#lab .fx-lock{opacity:.35}
#lab .fx-tagx{font:700 .62rem var(--mono);letter-spacing:.06em;text-transform:uppercase;border-radius:6px;padding:2px 6px;margin-left:6px;vertical-align:2px}
#lab .fx-tagx.none{color:var(--tomato);border:1px solid var(--tomato)}
#lab .fx-tagx.rare{color:#8e6cc1;border:1px solid #8e6cc1}
#lab .fx-vtiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
#lab .fx-cloud{display:flex;flex-wrap:wrap;gap:4px 14px;align-items:baseline;justify-content:center;line-height:1.15;padding:6px 0}
#lab .fx-cloud span{font-family:var(--display);font-weight:600;cursor:default}
#lab .fx-cloud .c0{color:var(--tomato)} #lab .fx-cloud .c1{color:var(--basil)} #lab .fx-cloud .c2{color:var(--ink)} #lab .fx-cloud .c3{color:#8e6cc1}
#lab .fx-2col{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
#lab .fx-list{list-style:none;margin:0;padding:0;display:grid;gap:9px}
#lab .fx-list li{display:grid;gap:4px;min-width:0}
#lab .fx-row{display:flex;justify-content:space-between;gap:10px;font-size:.9rem;min-width:0}
#lab .fx-row span{overflow-wrap:anywhere;min-width:0}
#lab .fx-row b{font-variant-numeric:tabular-nums;white-space:nowrap}
#lab .fx-meter{height:8px;border-radius:999px;background:var(--line);overflow:hidden}
#lab .fx-meter i{display:block;height:100%;border-radius:999px;background:var(--basil)}
#lab .fx-big{font:700 clamp(2rem,6vw,3.1rem)/1 var(--display);font-variant-numeric:tabular-nums}
#lab .fx-chips{display:flex;flex-wrap:wrap;gap:6px}
#lab .fx-chip{font:600 .78rem/1 var(--mono);padding:6px 9px;border-radius:999px;border:1px solid var(--line);background:var(--bg)}
#lab .fx-machines{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
#lab .fx-mach .ic{font-size:2.3rem;line-height:1}
#lab .fx-split{display:flex;height:24px;border-radius:999px;overflow:hidden;background:var(--line)}
#lab .fx-split i{display:block;height:100%}
#lab .fx-oracle{display:flex;align-items:center;gap:16px;flex-wrap:wrap;background:var(--panel);border:1.5px dashed var(--line);border-radius:16px;padding:16px}
#lab .fx-oracle button{font:700 1rem var(--display);padding:12px 18px;border-radius:999px;border:0;background:linear-gradient(135deg,#8e6cc1,var(--tomato));
  color:#fff;cursor:pointer;box-shadow:0 12px 26px -16px #8e6cc1}
#lab .fx-oracle button:hover{filter:brightness(1.08)}
#lab .fx-oracle p{margin:0;flex:1;min-width:220px;font-size:1rem}
#lab .fx-burnt{border:1.5px dashed var(--tomato);color:var(--tomato);border-radius:12px;padding:12px;font-size:.9rem}
.fx-drop{position:fixed;top:-70px;z-index:9999;pointer-events:none;animation:fx-fall linear forwards}
@keyframes fx-fall{to{transform:translateY(calc(100vh + 140px)) rotate(540deg)}}
@media (prefers-reduced-motion:reduce){#lab .fx-spin{animation:none}#lab .fx-xpbar i{transition:none}}
@media (max-width:860px){#lab .fx-hero{grid-template-columns:repeat(3,minmax(0,1fr))}#lab .fx-players,#lab .fx-duels,#lab .fx-machines,
  #lab .fx-charts,#lab .fx-2col{grid-template-columns:1fr}#lab .fx-vtiles{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:480px){#lab .fx-hero{grid-template-columns:repeat(2,minmax(0,1fr))}#lab .fx-banner{padding:12px}#lab .fx-spin{display:none}
  #lab .fx-tab{padding:8px 11px;font-size:.84rem}.fx-ticker .fx-say{font-size:.84rem}}
`;

  // ---------- charts (plain SVG, no libraries)
  function radar(values, labels, color) {
    const S = 260, c = S / 2, R = S / 2 - 40, n = values.length;
    const pt = (i, r) => {
      const a = -Math.PI / 2 + (i * 2 * Math.PI) / n;
      return [c + r * Math.cos(a), c + r * Math.sin(a)];
    };
    let g = "";
    [0.25, 0.5, 0.75, 1].forEach((f) => {
      g += `<polygon class="fx-grid" points="${values.map((_, i) => pt(i, R * f).map((v) => v.toFixed(1)).join(",")).join(" ")}"/>`;
    });
    labels.forEach((l, i) => {
      const [x, y] = pt(i, R), [lx, ly] = pt(i, R + 19);
      g += `<line class="fx-grid" x1="${c}" y1="${c}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}"/>`;
      g += `<text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" text-anchor="middle" dominant-baseline="middle">${esc(l)}</text>`;
    });
    const pts = values.map((v, i) => pt(i, R * Math.max(0.05, v / 100)));
    g += `<polygon points="${pts.map((p) => p.map((v) => v.toFixed(1)).join(",")).join(" ")}" style="fill:${color};fill-opacity:.3;stroke:${color};stroke-width:2.5;stroke-linejoin:round"/>`;
    pts.forEach(([x, y], i) => { g += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="3.5" style="fill:${color}"><title>${esc(labels[i])}: ${values[i]}/100</title></circle>`; });
    return `<svg class="fx-radar" viewBox="0 0 ${S} ${S}" role="img" aria-label="Skill radar: ${labels.map((l, i) => l + " " + values[i]).join(", ")}">${g}</svg>`;
  }

  function clockSvg() {
    const clock = F.clock || {}, people = Object.keys(clock);
    const S = 360, c = S / 2, r0 = 58, r1 = 150;
    const tot = Array.from({ length: 24 }, (_, h) => people.reduce((a, p) => a + (clock[p][h] || 0), 0));
    const max = Math.max(1, ...tot);
    const P = (a, r) => [c + r * Math.cos(a), c + r * Math.sin(a)];
    const ang = (h) => (h / 24) * 2 * Math.PI - Math.PI / 2;
    const f = (v) => v.toFixed(1);
    const sector = (a0, a1, ra, rb) => {
      const [x0, y0] = P(a0, rb), [x1, y1] = P(a1, rb), [x2, y2] = P(a1, ra), [x3, y3] = P(a0, ra);
      const large = a1 - a0 > Math.PI ? 1 : 0;
      return `M${f(x0)},${f(y0)}A${rb},${rb} 0 ${large} 1 ${f(x1)},${f(y1)}L${f(x2)},${f(y2)}A${ra},${ra} 0 ${large} 0 ${f(x3)},${f(y3)}Z`;
    };
    let g = `<path class="fx-night" d="${sector(ang(0), ang(5), r0 - 8, r1 + 8)}"><title>Midnight to 5 am: should be sleeping</title></path>`;
    [0.5, 1].forEach((k) => { g += `<circle class="fx-ring" cx="${c}" cy="${c}" r="${r0 + (r1 - r0) * k}"/>`; });
    for (let h = 0; h < 24; h++) {
      const a0 = ang(h) + 0.025, a1 = ang(h + 1) - 0.025;
      let base = 0;
      people.forEach((p) => {
        const v = clock[p][h] || 0;
        if (!v) return;
        const ra = r0 + ((r1 - r0) * base) / max, rb = r0 + ((r1 - r0) * (base + v)) / max;
        g += `<path d="${sector(a0, a1, ra, rb)}" style="fill:${col(p)}"><title>${esc(nm(p))}: ${v} change${v === 1 ? "" : "s"} at ${pad(h)}:00</title></path>`;
        base += v;
      });
    }
    for (let h = 0; h < 24; h += 3) {
      const [x, y] = P(ang(h), r1 + 20);
      g += `<text x="${f(x)}" y="${f(y)}" text-anchor="middle" dominant-baseline="middle">${pad(h)}</text>`;
    }
    const [mx, my] = P(ang(2.5), r1 - 18);
    g += `<text x="${f(mx)}" y="${f(my)}" text-anchor="middle" dominant-baseline="middle" style="font-size:18px">🌙</text>`;
    const peak = tot.indexOf(Math.max(...tot));
    g += `<text class="fx-clock-big" x="${c}" y="${c + 2}" text-anchor="middle">${pad(peak)}:00</text>`;
    g += `<text x="${c}" y="${c + 22}" text-anchor="middle">busiest hour</text>`;
    return `<svg class="fx-svg" viewBox="0 0 ${S} ${S}" role="img" aria-label="Changes by hour of the day; busiest hour ${pad(peak)}:00">${g}</svg>`;
  }

  function pizzaSvg(owners) {
    const S = 320, c = S / 2, R = 146, rc = 130;
    const total = owners.reduce((a, [, v]) => a + v, 0) || 1;
    let seed = 11;
    const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
    const f = (v) => v.toFixed(1);
    let g = `<circle class="fx-crust" cx="${c}" cy="${c}" r="${R}"/><circle class="fx-cheese" cx="${c}" cy="${c}" r="${rc}"/>`;
    let a = -Math.PI / 2, cuts = "", labels = "";
    owners.forEach(([p, v]) => {
      const span = (2 * Math.PI * v) / total;
      if (span <= 0.0001) return;
      const a1 = a + span, share = Math.round((100 * v) / total);
      const [x0, y0] = [c + rc * Math.cos(a), c + rc * Math.sin(a)], [x1, y1] = [c + rc * Math.cos(a1), c + rc * Math.sin(a1)];
      const tip = `<title>${esc(nm(p))}: ${fmt(v)} words (${share}%)</title>`;
      g += span >= 2 * Math.PI - 0.0001
        ? `<circle cx="${c}" cy="${c}" r="${rc}" style="fill:${col(p)};fill-opacity:.5">${tip}</circle>`
        : `<path d="M${c},${c}L${f(x0)},${f(y0)}A${rc},${rc} 0 ${span > Math.PI ? 1 : 0} 1 ${f(x1)},${f(y1)}Z" style="fill:${col(p)};fill-opacity:.5">${tip}</path>`;
      const n = Math.max(1, Math.round((14 * v) / total));
      for (let i = 0; i < n; i++) {
        const aa = a + span * (0.12 + 0.76 * rnd()), rr = rc * (0.28 + 0.6 * rnd());
        g += `<circle class="fx-pep" cx="${f(c + rr * Math.cos(aa))}" cy="${f(c + rr * Math.sin(aa))}" r="${f(7 + 4 * rnd())}"/>`;
      }
      if (owners.length > 1) cuts += `<line class="fx-cut" x1="${c}" y1="${c}" x2="${f(x0)}" y2="${f(y0)}"/>`;
      if (span > 0.3) {
        const mid = a + span / 2;
        labels += `<text class="fx-slice" x="${f(c + rc * 0.58 * Math.cos(mid))}" y="${f(c + rc * 0.58 * Math.sin(mid))}" text-anchor="middle" dominant-baseline="middle">${share}%</text>`;
      }
      a = a1;
    });
    [[0.3, 0.42], [2.2, 0.72], [4.1, 0.5]].forEach(([aa, rr]) => {
      const x = c + rc * rr * Math.cos(aa), y = c + rc * rr * Math.sin(aa);
      g += `<ellipse cx="${f(x)}" cy="${f(y)}" rx="7" ry="4" fill="#3d8a4c" transform="rotate(35 ${f(x)} ${f(y)})"/>`;
    });
    return `<svg class="fx-svg" viewBox="0 0 ${S} ${S}" role="img" aria-label="Who wrote the words in the vault">${g}${cuts}${labels}</svg>`;
  }

  function weekSvg() {
    const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], W = 720, H = 220, padL = 30, padB = 28, padT = 12;
    const wk = F.weekdays || {};
    const max = Math.max(1, ...TEAM.flatMap((p) => wk[p] || [0]));
    const step = Math.max(1, Math.ceil(max / 4)), top = step * 4;
    const y = (v) => padT + (H - padT - padB) * (1 - v / top);
    const gw = (W - padL) / 7, bw = (gw * 0.76) / Math.max(1, TEAM.length);
    let g = "";
    for (let v = 0; v <= top; v += step) g += `<line class="fx-ring" x1="${padL}" x2="${W}" y1="${y(v)}" y2="${y(v)}"/><text x="${padL - 6}" y="${y(v) + 4}" text-anchor="end">${v}</text>`;
    days.forEach((d, i) => {
      if (i >= 5) g += `<rect x="${padL + i * gw}" y="${padT}" width="${gw}" height="${H - padT - padB}" style="fill:var(--line);fill-opacity:.35"/>`;
      TEAM.forEach((p, j) => {
        const v = (wk[p] || [])[i] || 0;
        if (!v) return;
        const x = padL + i * gw + gw * 0.12 + j * bw;
        g += `<rect x="${x.toFixed(1)}" y="${y(v).toFixed(1)}" width="${(bw - 3).toFixed(1)}" height="${(y(0) - y(v)).toFixed(1)}" rx="4" style="fill:${col(p)}"><title>${esc(nm(p))}: ${v} on ${d}</title></rect>`;
      });
      g += `<text x="${(padL + i * gw + gw / 2).toFixed(1)}" y="${H - 8}" text-anchor="middle">${d}${i >= 5 ? " 🎮" : ""}</text>`;
    });
    return `<svg class="fx-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="Changes by weekday">${g}</svg>`;
  }

  function heatHtml() {
    const days = F.heatmap || [];
    const max = Math.max(1, ...days.map((d) => d.n));
    const level = (n) => (n === 0 ? 0 : Math.min(4, Math.ceil((4 * n) / max)));
    let cols = "";
    for (let w = 0; w * 7 < days.length; w++) {
      let cells = "";
      for (let r = 0; r < 7; r++) {
        const d = days[w * 7 + r];
        if (!d) { cells += `<i class="fx-hc fx-future"></i>`; continue; }
        const by = Object.entries(d.by || {}).map(([p, n]) => `${nm(p)} ${n}`).join(", ");
        cells += `<i class="fx-hc l${level(d.n)}" title="${esc(`${fmtDay(d.d)}: ${d.n} change${d.n === 1 ? "" : "s"}${by ? " (" + by + ")" : ""}`)}"></i>`;
      }
      cols += `<div class="fx-hcol">${cells}</div>`;
    }
    const busy = days.filter((d) => d.n).length;
    return `<div class="fx-heat"><div class="fx-hdays"><span>Mon</span><span></span><span>Wed</span><span></span><span>Fri</span><span></span><span>Sun</span></div>
      <div class="fx-hgrid">${cols}</div></div>
      <div class="fx-hlegend">less <i class="fx-hc l0"></i><i class="fx-hc l1"></i><i class="fx-hc l2"></i><i class="fx-hc l3"></i><i class="fx-hc l4"></i> more
        · <b>${busy}</b> active day${busy === 1 ? "" : "s"} out of ${days.length}</div>`;
  }

  const pizzaLogo = () => {
    const f = (v) => v.toFixed(1);
    let cuts = "";
    [0, 60, 120].forEach((d) => {
      const a = (d * Math.PI) / 180;
      cuts += `<line x1="${f(62 - 56 * Math.cos(a))}" y1="${f(62 - 56 * Math.sin(a))}" x2="${f(62 + 56 * Math.cos(a))}" y2="${f(62 + 56 * Math.sin(a))}" stroke="#fff8e6" stroke-width="2.5"/>`;
    });
    return `<svg class="fx-spin" viewBox="0 0 124 124" aria-hidden="true"><circle cx="62" cy="62" r="60" fill="#c98a48"/><circle cx="62" cy="62" r="51" fill="#f5cf62"/>
      ${[[62, 30], [36, 50], [88, 48], [46, 86], [80, 84], [62, 62]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="8.5" fill="#b8322a"/>`).join("")}
      ${[[50, 40], [74, 70], [38, 68]].map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="6" ry="3.4" fill="#3d8a4c" transform="rotate(35 ${x} ${y})"/>`).join("")}${cuts}</svg>`;
  };

  // ---------- cards
  function playerCard(p) {
    const c = col(p.id);
    const span = p.xp_next - p.xp_now;
    const width = span > 0 ? Math.max(3, Math.round((100 * (p.xp - p.xp_now)) / span)) : 100;
    const toNext = Math.max(0, p.xp_next - p.xp);
    const R = F.radar || [];
    const unlocked = (F.achievements || []).filter((a) => a.holders.includes(p.id));
    const stat = (v, l) => `<div class="fx-ps"><b>${v}</b><span>${esc(l)}</span></div>`;
    const top = p.rank === 1 && p.xp > 0;
    const why = p.xp_parts || {};
    return `<article class="fx-player${top ? " fx-top" : ""}" style="--c:${c}">
      ${top ? `<button class="fx-crown" type="button" title="Number one. Click for a party.">👑</button>` : ""}
      <div class="fx-ptop"><span class="fx-ava">${esc(nm(p.id).charAt(0))}</span>
        <div class="fx-pname"><strong>${esc(nm(p.id))}</strong><span>${esc(p.title)}</span></div>
        <div class="fx-lv"><small>LEVEL</small><b>${p.level}</b></div></div>
      <div class="fx-meta">#${p.rank} · ${esc(p.chrono[1])} ${esc(p.chrono[0])}${p.streak ? ` · 🔥 ${p.streak}-day streak` : ""}</div>
      <div><div class="fx-xpbar"><i data-w="${width}"></i></div>
        <div class="fx-xptext"><b>${fmt(p.xp)} XP</b><span>${toNext ? `${fmt(toNext)} XP to level ${p.level + 1}` : "max level. Respect."}</span></div></div>
      ${p.changes ? radar(R.map(([k]) => (p.radar || {})[k] || 0), R.map(([, l]) => l), c)
        : `<p class="fx-empty-p">No changes yet. The oven is still warming up. 🔥<br>The first push unlocks 🍕 First Slice.</p>`}
      <div class="fx-pstats">${stat(fmt(p.words), "words in the vault")}${stat(fmt(p.changes), "changes pushed")}${stat(fmt(p.created), "notes created")}
        ${stat(fmt(p.best_streak) + (p.best_streak ? " 🔥" : ""), "best streak (days)")}${stat(fmt(p.night), "night shifts")}${stat(fmt(p.tasks), "tasks served")}</div>
      <div class="fx-badges">${unlocked.map((a) => `<span class="fx-badge" title="${esc(a.name)}: ${esc(a.desc)}">${a.icon}</span>`).join("")
        || `<span class="fx-empty-p">No badges yet.</span>`}</div>
      <details class="fx-why"><summary>Where the ${fmt(p.xp)} XP come from</summary><ul>
        <li>✍️ Words in the vault: <b>${fmt(why.words)}</b></li><li>🍕 Changes: <b>${fmt(why.changes)}</b></li>
        <li>🗂️ Notes created: <b>${fmt(why.notes)}</b></li><li>✅ Tasks served: <b>${fmt(why.tasks)}</b></li>
        <li>☑️ Checklist boxes: <b>${fmt(why.boxes)}</b></li><li>🏅 Achievements: <b>${fmt(why.achievements)}</b></li>
        ${p.next_title ? `<li>Next title: <b>${esc(p.next_title)}</b> at level ${p.next_title_level}</li>` : ""}</ul></details>
    </article>`;
  }

  function duel(r) {
    const [sa, sb] = r.score;
    const rows = r.rows.map((x) => {
      const total = x.a + x.b, share = total ? (100 * x.a) / total : 50;
      return `<div class="fx-drow"><div class="fx-dlabel"><b>${fmt(x.a)}</b><span>${esc(x.label)}</span><b>${fmt(x.b)}</b></div>
        <div class="fx-tug"><i style="width:${share}%;background:${col(r.a)}"></i><i style="width:${100 - share}%;background:${col(r.b)}"></i></div></div>`;
    }).join("");
    const verdict = sa === sb ? "Dead even. Rematch!" : `${nm(sa > sb ? r.a : r.b)} wins ${Math.max(sa, sb)} of ${r.rows.length} categories.`;
    return `<div class="fx-card"><div class="fx-duel-head">${who(r.a)}<span class="fx-score">${sa} : ${sb}</span>${who(r.b)}</div>${rows}<p class="fx-foot">${esc(verdict)}</p></div>`;
  }

  const recCard = (r) => `<div class="fx-card fx-rec"><span class="ic">${r.icon}</span><span class="eyebrow">${esc(r.title)}</span>${r.who ? who(r.who) : ""}
    <div class="fx-val">${esc(r.value)}</div><div class="fx-det">${esc(r.detail)}${r.when ? ` · ${esc(fmtWhen(r.when))}` : ""}</div></div>`;

  // ---------- build the section
  try {
    const style = document.createElement("style");
    style.id = "fx-style";
    style.textContent = CSS;
    document.head.appendChild(style);
  } catch (e) { return; }

  guard(null, () => {
    const facts = (F.facts || []).filter(Boolean);
    if (!facts.length) return;
    const t = document.createElement("div");
    t.className = "fx-ticker";
    t.setAttribute("role", "status");
    t.title = "Click for the next fact";
    t.innerHTML = `<b class="fx-tag">BREAKING</b><span class="fx-say"></span>`;
    wrap.insertBefore(t, wrap.querySelector("header") || wrap.firstChild);
    const say = t.querySelector(".fx-say");
    let i = Math.floor(Math.random() * facts.length), timer = null;
    const show = () => {
      const next = facts[i++ % facts.length];
      if (REDUCE) { say.textContent = next; return; }
      say.classList.add("out");
      setTimeout(() => { say.textContent = next; say.classList.remove("out"); }, 300);
    };
    say.textContent = facts[i++ % facts.length];
    const start = () => { if (!timer && facts.length > 1) timer = setInterval(show, 7000); };
    const stop = () => { clearInterval(timer); timer = null; };
    t.addEventListener("click", () => { stop(); show(); start(); });
    t.addEventListener("mouseenter", stop);
    t.addEventListener("mouseleave", start);
    start();
  });

  guard(null, () => {
    const links = document.getElementById("links");
    if (!links) return;
    const a = document.createElement("a");
    a.className = "btn fx-labbtn";
    a.href = "#lab";
    a.textContent = "🧪 Stats Lab";
    links.insertBefore(a, links.children[1] || null);
  });

  const lab = document.createElement("section");
  lab.id = "lab";
  lab.setAttribute("aria-labelledby", "fx-h");
  const board = document.getElementById("board");
  const after = board && board.closest("section");
  if (after) after.after(lab);
  else wrap.insertBefore(lab, wrap.querySelector("footer"));

  const TABS = [["players", "🏅 Players"], ["fame", "🏆 Hall of Fame"], ["charts", "📊 Charts"],
                ["badges", "🎖️ Achievements"], ["vault", "📚 Vault"], ["machines", "🤖 Machines"]];
  lab.innerHTML = `
    <div class="fx-banner"><div class="fx-banner-text"><span class="eyebrow">ROBOLOX · freshly baked numbers</span>
      <h2 id="fx-h">🧪 The Stats Lab</h2><p>Silly, but true. Rebuilt on every push · baked ${esc(ago(F.built))}.</p></div>${pizzaLogo()}</div>
    <div class="fx-hero" id="fx-hero"></div>
    <div class="fx-tabs" role="tablist" aria-label="Stats Lab sections">${TABS.map(([id, label]) =>
      `<button class="fx-tab" type="button" role="tab" id="fx-t-${id}" aria-controls="fx-p-${id}" aria-selected="false">${label}</button>`).join("")}</div>
    ${TABS.map(([id]) => `<div class="fx-pane" role="tabpanel" id="fx-p-${id}" aria-labelledby="fx-t-${id}" hidden></div>`).join("")}
    <div class="fx-oracle"><button type="button" id="fx-oracle-btn">🔮 Ask the Pizza Oracle</button>
      <p id="fx-oracle-say">The oracle knows every number in this vault. Go on, ask it.</p></div>
    <p class="fx-foot">Made by Jan's Claude from the git history and the notes. Psst: type <b>pizza</b> anywhere on this page.</p>`;

  guard(document.getElementById("fx-hero"), () => {
    const V = F.vault || {}, T = F.totals || {};
    const tiles = [["📚", V.words, "words in the vault"], ["🍕", V.pizzas, "pizzas of text (1 pizza = 100 words)"],
      ["⏱️", null, "to read it all", hm(V.minutes || 0)], ["🧑‍🍳", T.human, "changes by humans"],
      ["🤖", T.machine, "changes by bots and AI"], ["🗓️", null, "of the pizza empire", "Day " + fmt((T.days || 0) + 1)]];
    document.getElementById("fx-hero").innerHTML = tiles.map(([ic, n, label, text]) =>
      `<div class="fx-tile"><span class="ic">${ic}</span><b${n != null ? ` data-count="${Number(n) || 0}"` : ""}>${n != null ? fmt(n) : esc(text)}</b><span>${esc(label)}</span></div>`).join("");
  });

  guard(pane("players"), () => {
    const players = (F.players || []).slice().sort((a, b) => a.rank - b.rank);
    let html = `<div class="fx-players">${players.map(playerCard).join("")}</div>`;
    if ((F.rivalries || []).length) html += `<h3 class="fx-h">⚔️ Rivalries <small>six categories · most wins takes the duel</small></h3><div class="fx-duels">${F.rivalries.map(duel).join("")}</div>`;
    if ((F.guests || []).length) html += `<p class="fx-foot">Unknown chefs: ${F.guests.map(([n, k]) => `${esc(n)} (${k})`).join(", ")}. Add them to <code>.github/dashboard/team.json</code>.</p>`;
    html += `<p class="fx-foot">XP = 10 × √(your words in the vault) + 8 per hand-made change + 1 per autosave + 25 per note created + 60 per task served + 15 per ticked box + 30 per achievement. Level n needs 50 × n² XP. The square root keeps it fair: pasting the dictionary won't win.</p>`;
    pane("players").innerHTML = html;
  });

  guard(pane("fame"), () => {
    const R = F.records || [];
    pane("fame").innerHTML = R.length ? `<div class="fx-records">${R.map(recCard).join("")}</div><p class="fx-foot">Checked on every push. Nobody's record is safe.</p>`
      : `<div class="fx-card"><p class="fx-empty-p">No records yet. Go make history.</p></div>`;
  });

  guard(pane("charts"), () => {
    pane("charts").innerHTML = `<div class="fx-charts">
      <div class="fx-card" id="fx-c-clock"><h3 class="fx-h">🕰️ The pizza clock <small>changes by hour · Vienna time</small></h3></div>
      <div class="fx-card" id="fx-c-pizza"><h3 class="fx-h">🍕 Who baked the vault <small>words still in it, by writer</small></h3></div>
      <div class="fx-card fx-wide" id="fx-c-week"><h3 class="fx-h">📆 Weekly rhythm <small>changes by weekday</small></h3></div>
      <div class="fx-card fx-wide" id="fx-c-heat"><h3 class="fx-h">🔥 Heat map <small>changes per day · last 12 weeks</small></h3></div></div>`;
    const add = (id, fn) => { const box = document.getElementById(id); guard(box, () => box.insertAdjacentHTML("beforeend", fn())); };
    add("fx-c-clock", () => clockSvg() + `<div class="fx-legend">${legend(Object.keys(F.clock || {}))}</div>`);
    add("fx-c-pizza", () => {
      const owners = Object.entries((F.vault || {}).owners || {}).filter(([, v]) => v > 0);
      const total = owners.reduce((a, [, v]) => a + v, 0);
      return pizzaSvg(owners) + `<div class="fx-legend">${owners.map(([p, v]) => `<span>${dot(p)}${esc(nm(p))} <b>${pct(v, total)}%</b> · ${fmt(v)} words</span>`).join("")}</div>`;
    });
    add("fx-c-week", () => weekSvg() + `<div class="fx-legend">${legend(TEAM)}<span>🎮 = weekend</span></div>`);
    add("fx-c-heat", heatHtml);
  });

  guard(pane("badges"), () => {
    const A = F.achievements || [];
    const P = TEAM.map((id) => (F.players || []).find((p) => p.id === id)).filter(Boolean);
    const count = (id) => A.filter((a) => a.holders.includes(id)).length;
    const nobody = A.filter((a) => !a.holders.length).length;
    const rows = A.map((a) => `<tr><td><div class="fx-aname"><span class="ic">${a.icon}</span><div><b>${esc(a.name)}</b>${!a.holders.length ? `<span class="fx-tagx none">nobody yet</span>`
      : a.holders.length === 1 ? `<span class="fx-tagx rare">rare</span>` : ""}<small>${esc(a.desc)}</small></div></div></td>
      ${P.map((p) => `<td>${a.holders.includes(p.id) ? `<span class="fx-got" style="background:${col(p.id)}" title="${esc(nm(p.id))} has it">✓</span>` : `<span class="fx-lock" title="locked">🔒</span>`}</td>`).join("")}</tr>`).join("");
    pane("badges").innerHTML = `<div class="fx-legend">${P.map((p) => `<span>${dot(p.id)}${esc(nm(p.id))} <b>${count(p.id)} / ${A.length}</b></span>`).join("")}
        <span>🔒 <b>${nobody}</b> nobody has yet</span></div>
      <div class="fx-ach"><table><thead><tr><th>Achievement</th>${P.map((p) => `<th>${esc(nm(p.id))}</th>`).join("")}</tr></thead><tbody>${rows}</tbody></table></div>
      <p class="fx-foot">Every achievement is worth 30 XP. They unlock by themselves on the next push.</p>`;
  });

  guard(pane("vault"), () => {
    const V = F.vault || {};
    const tile = ([ic, v, label]) => `<div class="fx-tile"><span class="ic">${ic}</span><b>${v}</b><span>${esc(label)}</span></div>`;
    const done = V.boxes_done || 0, boxes = done + (V.boxes_open || 0);
    const tiles = [["🗒️", fmt(V.notes), "notes"], ["📝", fmt(V.words), "words"], ["🔗", fmt(V.links), "[[links]]"], ["🏷️", fmt(V.tags), "different #tags"],
      ["😋", fmt(V.emoji), "emojis"], ["☑️", `${fmt(done)} / ${fmt(boxes)}`, "checkboxes ticked"], ["⏱️", hm(V.minutes || 0), "to read everything"], ["🍕", fmt(V.pizzas), "pizzas of text"]];
    const cloud = (V.cloud || []).slice();
    const hi = cloud.length ? cloud[0][1] : 1, lo = cloud.length ? cloud[cloud.length - 1][1] : 0;
    const cloudHtml = cloud.sort((a, b) => a[0].localeCompare(b[0])).map(([w, n], i) =>
      `<span class="c${i % 4}" style="font-size:${(0.85 + 1.6 * Math.sqrt((n - lo) / Math.max(1, hi - lo))).toFixed(2)}rem" title="${n}×">${esc(w)}</span>`).join("");
    const bars = (list, unit) => {
      const max = Math.max(1, ...list.map(([, n]) => n));
      return `<ul class="fx-list">${list.map(([k, n]) => `<li><div class="fx-row"><span>${esc(k)}</span><b>${fmt(n)}${unit}</b></div><div class="fx-meter"><i style="width:${(100 * n) / max}%"></i></div></li>`).join("")}</ul>`;
    };
    const P = V.prediction;
    const A = F.ayoo || {};
    pane("vault").innerHTML = `<div class="fx-vtiles">${tiles.map(tile).join("")}</div>
      <div class="fx-card"><h3 class="fx-h">☁️ What we write about <small>the 40 most used words</small></h3><div class="fx-cloud">${cloudHtml || `<span class="fx-empty-p">Write something first!</span>`}</div></div>
      <div class="fx-2col">
        <div class="fx-card"><h3 class="fx-h">🏘️ Where the words live <small>by folder</small></h3>${bars(V.folders || [], " words")}</div>
        <div class="fx-card"><h3 class="fx-h">🧲 Most linked notes <small>other notes point here</small></h3>${bars(V.popular || [], " links")}</div>
        <div class="fx-card"><h3 class="fx-h">🦕 Longest notes <small>words</small></h3>${bars(V.longest || [], "")}</div>
        <div class="fx-card"><h3 class="fx-h">🔮 The prophecy <small>based on the last 7 days</small></h3>
          ${P ? `<div class="fx-big">${esc(fmtDate(P.date))}</div><p class="fx-empty-p">is when the vault reaches <b>${fmt(P.goal)} words</b>, if everyone keeps typing about ${fmt(P.per_day)} words a day.</p>`
            : `<p class="fx-empty-p">The vault is resting this week, so the crystal ball sees nothing. Write something to wake it up.</p>`}
          <h3 class="fx-h">📣 AYOOOO meter <small>all-time</small></h3><div class="fx-big">${fmt(A.total)}</div>
          <div class="fx-legend">${Object.entries(A.by || {}).map(([p, n]) => `<span>${dot(p)}${esc(nm(p))} <b>${fmt(n)}</b></span>`).join("") || `<span class="fx-empty-p">Suspiciously quiet.</span>`}</div></div>
      </div>
      <div class="fx-card"><h3 class="fx-h">💬 Favourite words in change messages</h3><div class="fx-chips">${(V.message_words || []).map(([w, n]) => `<span class="fx-chip">${esc(w)} × ${n}</span>`).join("") || `<span class="fx-empty-p">Nothing yet.</span>`}</div></div>`;
  });

  guard(pane("machines"), () => {
    const M = F.machines || {}, bot = M.bot || {}, ai = M.claude || {};
    const parts = [["Humans, by hand", M.human_manual || 0, "var(--tomato)"], ["Autosave timers", M.autosave || 0, "var(--cheese)"],
      ["Claude (AI intern)", ai.changes || 0, "#8e6cc1"], ["Dashboard bot", bot.changes || 0, "#6b7c8f"]];
    const total = parts.reduce((a, [, n]) => a + n, 0) || 1;
    const machines = (M.autosave || 0) + (ai.changes || 0) + (bot.changes || 0);
    const verdict = machines > (M.human_manual || 0) ? "🤖 The machines are winning. Type faster, humans!" : "🧑‍🍳 Humans are still in charge. For now.";
    pane("machines").innerHTML = `<div class="fx-machines">
      <div class="fx-card fx-mach"><span class="ic">🤖</span><span class="eyebrow">Dashboard bot</span><div class="fx-big">${fmt(bot.changes)}</div>
        <p class="fx-empty-p">website updates${bot.first ? `, on duty since ${esc(fmtWhen(bot.first))}` : ""}. Never sleeps, never eats, still not on the leaderboard.</p></div>
      <div class="fx-card fx-mach"><span class="ic">🧠</span><span class="eyebrow">Claude, the AI intern</span><div class="fx-big">${fmt(ai.changes)}</div>
        <p class="fx-empty-p">changes made directly, ${fmt(ai.lines)} lines. Payment so far: zero pizza. Suspiciously polite.</p></div>
      <div class="fx-card fx-mach"><span class="ic">💾</span><span class="eyebrow">Autosave timers</span><div class="fx-big">${fmt(M.autosave)}</div>
        <p class="fx-empty-p">changes saved by a clock while someone typed. The most loyal employee is a timer.</p></div></div>
      <div class="fx-card"><h3 class="fx-h">⚖️ Humans vs machines <small>every change ever pushed</small></h3>
        <div class="fx-split" role="img" aria-label="${parts.map(([l, n]) => `${l} ${n}`).join(", ")}">${parts.map(([l, n, c]) => n ? `<i style="width:${(100 * n) / total}%;background:${c}" title="${esc(l)}: ${n}"></i>` : "").join("")}</div>
        <div class="fx-legend">${parts.map(([l, n, c]) => `<span><i class="fx-dot" style="background:${c}"></i>${esc(l)} <b>${pct(n, total)}%</b></span>`).join("")}</div>
        <p class="fx-empty-p"><b>${esc(verdict)}</b></p></div>`;
  });

  // ---------- tabs, animations, oracle, easter eggs
  let seen = false;
  const grow = (root) => root.querySelectorAll(".fx-xpbar i[data-w]").forEach((i) => requestAnimationFrame(() => { i.style.width = i.dataset.w + "%"; }));
  const select = (id) => {
    TABS.forEach(([t]) => {
      const on = t === id;
      document.getElementById("fx-t-" + t).setAttribute("aria-selected", String(on));
      pane(t).hidden = !on;
    });
    try { localStorage.setItem("fx-tab", id); } catch (e) { /* private mode */ }
    if (seen) grow(pane(id));
  };
  TABS.forEach(([t]) => document.getElementById("fx-t-" + t).addEventListener("click", () => select(t)));
  let first = "players";
  try { const saved = localStorage.getItem("fx-tab"); if (TABS.some(([t]) => t === saved)) first = saved; } catch (e) { /* private mode */ }
  select(first);

  const countUp = () => lab.querySelectorAll("[data-count]").forEach((b) => {
    const end = Number(b.dataset.count) || 0;
    if (REDUCE || end < 10) { b.textContent = fmt(end); return; }
    const t0 = performance.now(), dur = 1300;
    const step = (now) => {
      const k = Math.min(1, (now - t0) / dur);
      b.textContent = fmt(end * (1 - Math.pow(1 - k, 3)));
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  });
  const wake = () => { if (seen) return; seen = true; countUp(); grow(lab); };
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => { if (entries.some((e) => e.isIntersecting)) { io.disconnect(); wake(); } }, { threshold: 0.05 });
    io.observe(lab);
  } else wake();

  guard(null, () => {
    const pool = (F.facts || []).concat(FORTUNES);
    const out = document.getElementById("fx-oracle-say");
    let last = -1;
    document.getElementById("fx-oracle-btn").addEventListener("click", () => {
      let i = Math.floor(Math.random() * pool.length);
      if (pool.length > 1 && i === last) i = (i + 1) % pool.length;
      last = i;
      out.textContent = pool[i];
      if (!REDUCE && out.animate) out.animate([{ opacity: 0, transform: "translateY(6px)" }, { opacity: 1, transform: "none" }], { duration: 350, easing: "ease-out" });
    });
  });

  const rain = (chars, n) => {
    if (REDUCE) return;
    for (let k = 0; k < n; k++) {
      const s = document.createElement("span");
      s.className = "fx-drop";
      s.textContent = chars[k % chars.length];
      s.style.left = Math.random() * 96 + "vw";
      s.style.fontSize = 22 + Math.random() * 24 + "px";
      s.style.animationDuration = 2.2 + Math.random() * 2.2 + "s";
      s.style.animationDelay = Math.random() * 0.9 + "s";
      document.body.appendChild(s);
      setTimeout(() => s.remove(), 6000);
    }
  };
  let typed = "";
  document.addEventListener("keydown", (e) => {
    if (e.target && /^(input|textarea|select)$/i.test(e.target.tagName)) return;
    typed = (typed + (e.key || "")).toLowerCase().slice(-5);
    if (typed === "pizza") rain(["🍕"], 40);
  });
  lab.addEventListener("click", (e) => { if (e.target.closest(".fx-crown")) rain(["🎉", "🍕", "⭐", "👑"], 44); });
})();
