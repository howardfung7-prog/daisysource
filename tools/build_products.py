#!/usr/bin/env python3
"""
Generate individual product detail pages for the Tools & Materials division.

Output: tools/p/<slug>/index.html  (English; industrial theme, matches /tools/).
Also injects a "view details" link into each card in tools/index.html.

Images live in assets/tools/gallery/<slug>/g1.webp ... gN.webp (scraped from the
seller's own AliExpress listings). Run:  python3 tools/build_products.py
"""
import os, json, html as _html, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N = os.path.join(ROOT, "i18n")
WA = "8618174278678"
EMAIL = "daisysource6@gmail.com"
BASE = "https://daisysource.vip"

# code, direction — must match i18n/build.py LANGS
LANGS = [("es", "ltr"), ("pt", "ltr"), ("fr", "ltr"), ("ja", "ltr"),
         ("ko", "ltr"), ("id", "ltr"), ("ar", "rtl")]
ALL_CODES = ["en"] + [c for c, _ in LANGS]

RTL_CSS = ('<style>body{direction:rtl}.crumb,.meta,.price,.acts,.band .wrap,'
           '.foot,.thumbs,.nav{direction:rtl}</style>')


def _load(name):
    p = os.path.join(I18N, name)
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def apply_table(html, table, code):
    for en, vals in sorted(table.items(), key=lambda kv: len(kv[0]), reverse=True):
        tr = vals.get(code)
        if tr:
            html = html.replace(en, tr)
    return html


def relink_detail(html, code):
    html = html.replace('href="/tools/', 'href="/%s/tools/' % code)
    html = html.replace('href="/lashes/', 'href="/%s/lashes/' % code)
    html = html.replace('href="/"', 'href="/%s/"' % code)
    return html


def head_block(slug, cur):
    def url(c):
        pre = "" if c == "en" else "/" + c
        return "%s%s/tools/p/%s/" % (BASE, pre, slug)
    lines = ['<link rel="canonical" href="%s">' % url(cur),
             '<link rel="alternate" hreflang="x-default" href="%s">' % url("en")]
    for c in ALL_CODES:
        lines.append('<link rel="alternate" hreflang="%s" href="%s">' % (c, url(c)))
    return "\n".join(lines)

# slug, main-image basename (in /assets/tools/), category label, title,
# now, was, save%, sold, gallery count, short desc, overview, specs[(k,v)]
PRODUCTS = [
 ("s800-flux", "tool-01-s800-flux", "Soldering Flux", "S800 10cc Soldering Flux Paste",
  "2.05", "2.53", "19", "316 sold", 6,
  "Syringe with dispensing needle for BGA, PCB & SMD IC repair and rework.",
  "S800 is a ready-to-use soldering flux paste in a 10cc syringe with a dispensing needle, made for BGA, PCB and SMD IC repair and rework. It holds components in place and promotes clean, even solder wetting during reballing and chip-level work, on both leaded and lead-free joints.",
  [("Model","S800"),("Net content","10cc"),("Form","Paste (syringe)"),("Application","BGA / PCB / SMD IC repair & rework"),("Package","1 x flux syringe + push rod + needle")]),
 ("solderball-sac305", "tool-02-solderball-sac305", "Solder Balls", "Lead-Free BGA Solder Balls (SAC305)",
  "3.36", "5.33", "37", "30 sold", 6,
  "0.25-0.76mm leadless tin beads, 2,500 pcs bottled, for BGA reballing.",
  "Lead-free BGA reballing solder balls in SAC305 alloy (Sn96.5 / Ag3.0 / Cu0.5). Supplied bottled in roughly 2,500-piece quantities across common diameters, for reballing BGA chips during board-level and phone repair.",
  [("Alloy","SAC305 (Sn96.5/Ag3.0/Cu0.5)"),("Diameters","0.25 - 0.76 mm"),("Quantity","approx. 2,500 pcs / bottle"),("Type","Lead-free"),("Application","BGA reballing")]),
 ("nc559-bga", "tool-03-nc559-flux", "Soldering Flux", "NC-559-ASM 10cc BGA Flux Paste",
  "2.24", "3.73", "40", "15 sold", 6,
  "Welding flux syringe for PCB & SMD IC repair and rework work.",
  "NC-559-ASM is a BGA soldering flux paste in a 10cc syringe for PCB and SMD IC repair and rework. It wets quickly and helps solder flow evenly during reballing and fine-pitch soldering.",
  [("Model","NC-559-ASM"),("Net content","10cc"),("Form","Paste (syringe)"),("Application","BGA / PCB / SMD IC rework"),("Package","1 x syringe + push rod + needles")]),
 ("nc559-noclean", "tool-04-nc559-noclean", "Soldering Flux", "NC-559-ASM 10cc No-Clean Flux",
  "1.17", "1.94", "40", "76 sold", 6,
  "No-clean BGA flux paste syringe for PCB & SMD IC repair and rework.",
  "The no-clean version of NC-559-ASM in a 10cc syringe. Its low-residue formula means boards can often be used without a cleaning step, while still giving strong wetting for BGA reballing and SMD rework.",
  [("Model","NC-559-ASM"),("Net content","10cc"),("Type","No-clean paste"),("Application","BGA / PCB / SMD IC rework"),("Package","1 x syringe + push rod + needles")]),
 ("flux-100g", "tool-05-flux-100g", "Soldering Flux", "100g Soldering Flux Paste (223/558/559/808)",
  "5.75", "9.13", "37", "20 sold", 5,
  "Bulk flux tub for BGA, PCB & SMD electronics repair and rework.",
  "A 100g tub of soldering flux paste for BGA, PCB and SMD electronics repair and rework, available in the popular 223, 558, 559 and 808 formulas. The bulk size suits busy repair benches and production rework.",
  [("Net content","100g"),("Formulas","223 / 558 / 559 / 808"),("Form","Paste (tub)"),("Application","BGA / PCB / SMD repair & rework")]),
 ("zj18-rosin", "tool-06-zj18-rosin", "Soldering Flux", "ZJ-18 50g Rosin Flux Paste",
  "1.29", "1.67", "23", "2 sold", 6,
  "No-clean rosin paste for PCB & SMD soldering and tinning.",
  "ZJ-18 is a 50g no-clean rosin flux paste for PCB and SMD soldering and tinning. The rosin base gives reliable wetting for general bench soldering while leaving minimal residue.",
  [("Model","ZJ-18"),("Net content","50g"),("Type","No-clean rosin paste"),("Application","PCB / SMD soldering & tinning")]),
 ("rosin-30g", "tool-07-rosin-30g", "Soldering Flux", "30g Rosin Soldering Flux Paste",
  "1.15", "1.83", "37", "13 sold", 6,
  "General-purpose rosin flux for soldering and tinning.",
  "A compact 30g tin of general-purpose rosin soldering flux paste for soldering and tinning. A low-cost staple for hobby and repair benches.",
  [("Net content","30g"),("Type","Rosin paste"),("Application","General soldering & tinning")]),
 ("solderwire-300cm", "tool-08-solderwire-300cm", "Solder Wire", "Multi-Function Solder Wire 300cm Ø1.0mm",
  "2.99", "4.15", "28", "40 sold", 6,
  "Special-core wire for stainless steel, aluminum and nickel soldering.",
  "A 300cm length of 1.0mm multi-function solder wire with a special core that lets it bond stainless steel, aluminum and nickel as well as standard electronics work - useful where ordinary solder will not wet the metal.",
  [("Diameter","1.0 mm"),("Length","300 cm"),("Core","Special multi-metal core"),("Works on","Stainless steel / aluminum / nickel")]),
 ("pcb-redglue", "tool-09-pcb-redglue", "Adhesive", "30g PCB Red Glue (SMT)",
  "9.45", "18.90", "50", "5 sold", 6,
  "High-temperature curing SMT/BGA patch dispensing glue for screen printing.",
  "A 30g syringe of SMT/BGA red adhesive (PCB red glue) that cures at high temperature to hold components before reflow. Suited to stencil / screen-printing and dispensing on steel and copper screens.",
  [("Net content","30g"),("Type","SMT / BGA red adhesive"),("Cure","High-temperature"),("Use","Screen / stencil dispensing")]),
 ("usb-iron", "tool-10-usb-iron", "Tool", "USB Wireless Soldering Iron Set (USB-102)",
  "19.09", "32.91", "42", "13 sold", 6,
  "Mini 18650-battery iron, 1500mA removable, large-capacity portable kit.",
  "USB-102 is a cordless mini soldering iron set powered by a removable 18650 battery (1500mA), for soldering away from a bench or mains outlet. The large-capacity kit is built for portable field and hobby repair.",
  [("Model","USB-102"),("Power source","18650 battery (removable)"),("Battery","1500mA"),("Type","Cordless / USB-charge portable kit")]),
 ("rl403-lowtemp", "tool-11-rl403-lowtemp", "Solder Paste", "RL-403 10cc Low-Temp Solder Paste 183°C",
  "5.45", "8.13", "33", "New", 5,
  "No-clean syringe for BGA, PCB & SMD mobile-phone repair.",
  "RL-403 is a low-temperature, no-clean solder paste in a 10cc syringe that reflows around 183°C, reducing thermal stress during BGA, PCB and SMD mobile-phone repair.",
  [("Model","RL-403"),("Net content","10cc"),("Melting point","183°C"),("Type","No-clean solder paste"),("Application","BGA / PCB / SMD phone repair")]),
 ("magnifier", "tool-12-magnifier", "Optics", "You Qian Magnifier 1x / 2x / 3x",
  "4.29", "5.43", "21", "New", 4,
  "Optical instrument for reading and close-up repair and inspection work.",
  "A You Qian optical magnifier offering 1x, 2x and 3x views for reading and close-up repair and inspection work - handy for checking solder joints, fine print and small components.",
  [("Magnification","1x / 2x / 3x"),("Type","Optical magnifier"),("Use","Reading / close-up repair & inspection")]),
]

PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@@TITLE@@ — Daisysource Tools &amp; Materials</title>
<meta name="description" content="@@SHORT@@">
<link rel="canonical" href="https://daisysource.vip/tools/p/@@SLUG@@/">
<meta name="theme-color" content="#14161a">
<link rel="icon" type="image/svg+xml" href="/assets/logo-a-icon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
  :root { --bg:#eef0f2; --surface:#fff; --ink:#15181d; --ink-soft:#596273; --line:#d9dde3; --graphite:#14161a; --amber:#ef6a24; --amber-deep:#d2520f; --ok:#15a35b; --disp:"Space Grotesk",system-ui,sans-serif; --sans:"Inter",system-ui,sans-serif; --mono:"JetBrains Mono",ui-monospace,monospace; }
  @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#0f1114; --surface:#171a1f; --ink:#e9edf2; --ink-soft:#9aa3b2; --line:#272b33; } }
  :root[data-theme="dark"] { --bg:#0f1114; --surface:#171a1f; --ink:#e9edf2; --ink-soft:#9aa3b2; --line:#272b33; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:var(--bg); color:var(--ink); font-family:var(--sans); font-size:16px; line-height:1.6; -webkit-font-smoothing:antialiased; }
  .wrap { width:min(1180px,92vw); margin:0 auto; }
  a { color:inherit; text-decoration:none; }
  h1,h2,h3 { font-family:var(--disp); font-weight:600; line-height:1.15; letter-spacing:-.01em; }
  .mono { font-family:var(--mono); }
  .hazard { height:5px; background:repeating-linear-gradient(135deg,var(--amber) 0 16px,var(--graphite) 16px 32px); }
  header { background:color-mix(in srgb,var(--bg) 90%,transparent); backdrop-filter:blur(12px); border-bottom:1px solid var(--line); position:sticky; top:0; z-index:50; }
  .nav { display:flex; align-items:center; justify-content:space-between; height:64px; gap:18px; }
  .brand { display:flex; align-items:center; gap:11px; }
  .brand .mark { width:30px; height:30px; border-radius:8px; background:var(--graphite); display:grid; place-items:center; color:var(--amber); flex:none; }
  .brand b { font-family:var(--disp); font-size:17px; font-weight:700; letter-spacing:-.02em; display:block; line-height:1.05; }
  .brand small { font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:var(--ink-soft); font-weight:600; }
  .nav-links { display:flex; gap:24px; font-size:14.5px; font-weight:600; }
  .nav-links a { color:var(--ink-soft); } .nav-links a:hover { color:var(--amber); }
  .nav-back { font-size:13px; color:var(--ink-soft); } .nav-back:hover { color:var(--ink); }
  @media (max-width:820px) { .nav-links { display:none; } }
  .crumb { font-family:var(--mono); font-size:12.5px; color:var(--ink-soft); padding:22px 0 6px; }
  .crumb a:hover { color:var(--amber); }
  .top { display:grid; grid-template-columns:1fr 1fr; gap:38px; padding:12px 0 46px; }
  @media (max-width:820px) { .top { grid-template-columns:1fr; gap:26px; } }
  .gal .main { background:#fff; border:1px solid var(--line); border-radius:14px; aspect-ratio:1/1; display:grid; place-items:center; overflow:hidden; }
  .gal .main img { width:100%; height:100%; object-fit:contain; padding:18px; }
  .thumbs { display:flex; gap:9px; margin-top:12px; flex-wrap:wrap; }
  .thumbs button { width:62px; height:62px; border:1px solid var(--line); border-radius:9px; background:#fff; padding:4px; cursor:pointer; overflow:hidden; }
  .thumbs button.active { border-color:var(--amber); }
  .thumbs img { width:100%; height:100%; object-fit:contain; }
  .cat { font-family:var(--mono); font-size:11px; text-transform:uppercase; letter-spacing:.08em; background:var(--graphite); color:#fff; padding:5px 10px; border-radius:6px; display:inline-block; }
  .info h1 { font-size:clamp(24px,3.4vw,33px); margin:14px 0 10px; }
  .meta { display:flex; gap:14px; align-items:center; font-family:var(--mono); font-size:12.5px; color:var(--ink-soft); }
  .meta .sold { color:var(--ok); font-weight:700; }
  .price { display:flex; align-items:baseline; gap:12px; margin:20px 0; padding:18px 0; border-top:1px solid var(--line); border-bottom:1px solid var(--line); }
  .price .now { font-family:var(--disp); font-size:38px; font-weight:700; color:var(--amber-deep); }
  .price .was { font-size:16px; color:var(--ink-soft); text-decoration:line-through; }
  .price .save { font-family:var(--mono); font-size:12px; font-weight:700; color:var(--ok); background:rgba(21,163,91,.12); padding:4px 9px; border-radius:6px; }
  .lede { color:var(--ink-soft); font-size:15.5px; }
  .acts { display:flex; gap:11px; margin:22px 0 12px; flex-wrap:wrap; }
  .btn { display:inline-flex; align-items:center; gap:8px; padding:14px 22px; border-radius:9px; font-family:var(--disp); font-weight:700; font-size:15px; transition:transform .18s; }
  .btn:hover { transform:translateY(-2px); }
  .btn-wa { background:#25d366; color:#0a3d20; } .btn-am { background:var(--graphite); color:#fff; }
  .note { font-family:var(--mono); font-size:12px; color:var(--ink-soft); }
  section.block { padding:40px 0; border-top:1px solid var(--line); }
  section.block h2 { font-size:24px; margin-bottom:18px; }
  .overview { max-width:70ch; color:var(--ink); font-size:16px; }
  table.specs { width:100%; max-width:640px; border-collapse:collapse; font-size:14.5px; }
  table.specs td { padding:11px 14px; border:1px solid var(--line); }
  table.specs td:first-child { font-family:var(--mono); font-size:12.5px; color:var(--ink-soft); width:40%; background:color-mix(in srgb,var(--ink) 3%,transparent); }
  .detail-imgs { display:flex; flex-direction:column; gap:14px; max-width:820px; margin:0 auto; }
  .detail-imgs img { width:100%; border:1px solid var(--line); border-radius:12px; background:#fff; }
  .band { background:var(--graphite); color:#eef1f5; padding:54px 0; margin-top:10px; }
  .band .wrap { display:flex; justify-content:space-between; align-items:center; gap:24px; flex-wrap:wrap; }
  .band h2 { color:#fff; font-size:clamp(22px,3vw,30px); max-width:20ch; }
  .band .mono { color:var(--amber); font-size:14px; margin-top:8px; }
  footer { background:var(--bg); border-top:1px solid var(--line); padding:34px 0; }
  .foot { display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap; font-size:13.5px; color:var(--ink-soft); }
  .foot a:hover { color:var(--amber); }
  .disc { font-family:var(--mono); font-size:12px; color:var(--ink-soft); opacity:.8; margin-top:14px; }
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <path id="petal" d="M0,-11 C4.5,-16 5.5,-30 0.5,-41 C-5,-31 -4.5,-16 0,-11 Z"/>
  <g id="daisy"><use href="#petal"/><use href="#petal" transform="rotate(30)"/><use href="#petal" transform="rotate(60)"/><use href="#petal" transform="rotate(90)"/><use href="#petal" transform="rotate(120)"/><use href="#petal" transform="rotate(150)"/><use href="#petal" transform="rotate(180)"/><use href="#petal" transform="rotate(210)"/><use href="#petal" transform="rotate(240)"/><use href="#petal" transform="rotate(270)"/><use href="#petal" transform="rotate(300)"/><use href="#petal" transform="rotate(330)"/></g>
</defs></svg>
<div class="hazard"></div>
<header><div class="wrap nav">
  <a class="brand" href="/"><span class="mark"><svg width="18" height="18" viewBox="-46 -46 92 92"><use href="#daisy" fill="currentColor"/><circle r="8" fill="#ef6a24"/></svg></span><span><b>Daisysource</b><small>Tools &amp; Materials</small></span></a>
  <nav class="nav-links"><a href="/lashes/">Beauty &amp; Lashes</a><a href="/tools/">Tools &amp; Materials</a><a href="#contact">Contact</a></nav>
  <a class="nav-back" href="/tools/">← Catalog</a>
</div></header>

<div class="wrap">
  <div class="crumb"><a href="/tools/">Tools &amp; Materials</a> / <a href="/tools/#catalog">@@CAT@@</a> / @@TITLE@@</div>
  <div class="top">
    <div class="gal">
      <div class="main"><img id="mainimg" src="@@G1@@" alt="@@TITLE@@"></div>
      <div class="thumbs">@@THUMBS@@</div>
    </div>
    <div class="info">
      <span class="cat">@@CAT@@</span>
      <h1>@@TITLE@@</h1>
      <div class="meta"><span class="sold">@@SOLD@@</span><span>·</span><span>Factory-direct · wholesale</span></div>
      <div class="price"><span class="now">$@@NOW@@</span><span class="was">$@@WAS@@</span><span class="save">-@@SAVE@@%</span></div>
      <p class="lede">@@SHORT@@</p>
      <div class="acts">
        <a class="btn btn-wa" href="https://wa.me/@@WA@@?text=Inquiry%3A%20@@Q@@" target="_blank" rel="noopener">WhatsApp inquiry</a>
        <a class="btn btn-am" href="mailto:@@EMAIL@@?subject=Inquiry%3A%20@@Q@@">Email us</a>
      </div>
      <p class="note">// No online checkout — we quote &amp; ship directly. Reference price; confirmed on inquiry.</p>
    </div>
  </div>
</div>

<div class="wrap">
  <section class="block"><h2>Product overview</h2><p class="overview">@@OVERVIEW@@</p></section>
  <section class="block"><h2>Specifications</h2><table class="specs">@@SPECROWS@@</table></section>
  <section class="block"><h2>Product gallery</h2><div class="detail-imgs">@@DETAILIMGS@@</div></section>
</div>

<section class="band" id="contact"><div class="wrap">
  <div><h2>Interested in this item?</h2><p style="color:#b4bcc8;margin-top:8px">Ask for a wholesale quote — email or WhatsApp only.</p><div class="mono">@@EMAIL@@</div></div>
  <div class="acts">
    <a class="btn btn-wa" href="https://wa.me/@@WA@@?text=Inquiry%3A%20@@Q@@" target="_blank" rel="noopener">WhatsApp us</a>
    <a class="btn btn-am" style="background:var(--amber);color:#fff" href="mailto:@@EMAIL@@?subject=Inquiry%3A%20@@Q@@">Email us</a>
  </div>
</div></section>

<footer><div class="wrap">
  <div class="foot"><span>© 2026 Daisysource · Tools &amp; Materials</span><span><a href="/tools/">← Back to catalog</a> &nbsp;·&nbsp; <a href="/">Daisysource</a></span></div>
  <p class="disc">// Product specs and reference pricing are indicative and subject to confirmation on inquiry. Images for reference.</p>
</div></footer>
<script>
  var mi=document.getElementById('mainimg');
  document.querySelectorAll('.thumbs button').forEach(function(b){
    b.addEventListener('click',function(){
      document.querySelectorAll('.thumbs button').forEach(function(x){x.classList.remove('active');});
      b.classList.add('active'); mi.src=b.getAttribute('data-src');
    });
  });
</script>
</body>
</html>
"""


def esc(s):
    return _html.escape(s, quote=True)


def gen():
    for (slug, mainimg, cat, title, now, was, save, sold, galn, short, overview, specs) in PRODUCTS:
        gbase = "/assets/tools/gallery/" + slug
        imgs = [gbase + "/g%d.webp" % i for i in range(1, galn + 1)]
        thumbs = "".join(
            '<button class="%s" data-src="%s"><img src="%s" alt="view %d"></button>'
            % ("active" if i == 0 else "", u, u, i + 1) for i, u in enumerate(imgs))
        detailimgs = "".join('<img src="%s" alt="%s detail %d" loading="lazy">' % (u, esc(title), i + 1) for i, u in enumerate(imgs))
        specrows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (esc(k), esc(v)) for k, v in specs)
        repl = {
            "@@SLUG@@": slug, "@@CAT@@": esc(cat), "@@TITLE@@": esc(title),
            "@@NOW@@": now, "@@WAS@@": was, "@@SAVE@@": save, "@@SOLD@@": esc(sold),
            "@@SHORT@@": esc(short), "@@OVERVIEW@@": esc(overview),
            "@@G1@@": imgs[0], "@@THUMBS@@": thumbs, "@@DETAILIMGS@@": detailimgs, "@@SPECROWS@@": specrows,
            "@@WA@@": WA, "@@EMAIL@@": EMAIL, "@@Q@@": urllib.parse.quote(title),
        }
        page = PAGE
        for k, v in repl.items():
            page = page.replace(k, v)
        page_en = page.replace(
            '<link rel="canonical" href="%s/tools/p/%s/">' % (BASE, slug),
            head_block(slug, "en"), 1)
        # English
        _write(os.path.join(ROOT, "tools", "p", slug), page_en)
        # localized
        for code, direction in LANGS:
            h = page
            h = apply_table(h, NAV, code)
            h = apply_table(h, TOOLS, code)
            h = apply_table(h, DETAIL, code)
            if direction == "rtl":
                h = h.replace('<html lang="en">', '<html lang="%s" dir="rtl">' % code, 1)
            else:
                h = h.replace('<html lang="en">', '<html lang="%s">' % code, 1)
            h = relink_detail(h, code)
            h = h.replace(
                '<link rel="canonical" href="%s/tools/p/%s/">' % (BASE, slug),
                head_block(slug, code), 1)
            if direction == "rtl":
                h = h.replace("</head>", RTL_CSS + "</head>", 1)
            _write(os.path.join(ROOT, code, "tools", "p", slug), h)
    print("generated detail pages (en + %d langs) for %d products" % (len(LANGS), len(PRODUCTS)))


def _write(d, html):
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def link_catalog():
    """Wrap each card image + title in tools/index.html with a link to its detail page."""
    path = os.path.join(ROOT, "tools", "index.html")
    with open(path, encoding="utf-8") as f:
        src = f.read()
    changed = 0
    for (slug, mainimg, *_rest) in PRODUCTS:
        href = "/tools/p/" + slug + "/"
        card_img = '<img src="/assets/tools/%s.webp"' % mainimg
        if card_img not in src or ('href="%s"' % href) in src:
            continue
        ci = src.index(card_img)
        ph = src.rfind('<div class="ph">', 0, ci)
        ph_end = src.index('</div>', ci) + len('</div>')
        inner = src[ph + len('<div class="ph">'):ph_end - len('</div>')]
        newblock = '<a class="ph" href="%s" aria-label="View details">%s</a>' % (href, inner)
        src = src[:ph] + newblock + src[ph_end:]
        h3i = src.index('<h3>', ph)
        h3e = src.index('</h3>', h3i)
        title_txt = src[h3i + 4:h3e]
        src = src[:h3i] + '<h3><a href="%s">%s</a></h3>' % (href, title_txt) + src[h3e + len('</h3>'):]
        changed += 1
    if changed and 'a.ph{display:block}' not in src:
        src = src.replace('</style>', '  a.ph{display:block} .card h3 a{color:inherit} .card h3 a:hover{color:var(--amber-deep)}\n</style>', 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    print("linked %d catalog cards -> detail pages" % changed)


if __name__ == "__main__":
    NAV = _load("translations_nav.json")
    TOOLS = _load("translations_tools.json")
    DETAIL = _load("translations_detail.json")
    gen()
    link_catalog()
