#!/usr/bin/env python3
"""
Generate the Tools & Materials catalog grid and individual product detail pages.

- Rewrites the filter bar + card grid inside tools/index.html from PRODUCTS.
- Writes tools/p/<slug>/index.html (English) + /<lang>/tools/p/<slug>/ (7 langs).

The catalog mirrors the seller's own AliExpress store (AILI YQW TOOLS Store, 29
products) grouped into four display categories:
    flux   Soldering Flux
    paste  Soldering Paste
    wire   Solder Wire & Ball
    tool   Solder Tool

Images: assets/tools/tool-<...>.webp (card/main) and
assets/tools/gallery/<slug>/g1..gN.webp (detail gallery), scraped from the
seller's listings. Prices for the 12 original items are kept as set; the 17
added items are converted from the store's RM prices.

Run:  python3 tools/build_products.py      (then python3 i18n/build.py)
"""
import os, json, html as _html, urllib.parse, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N = os.path.join(ROOT, "i18n")
WA = "8618174278678"
EMAIL = "daisysource6@gmail.com"
BASE = "https://daisysource.vip"

LANGS = [("es", "ltr"), ("pt", "ltr"), ("fr", "ltr"), ("ja", "ltr"),
         ("ko", "ltr"), ("id", "ltr"), ("ar", "rtl")]
ALL_CODES = ["en"] + [c for c, _ in LANGS]

RTL_CSS = ('<style>body{direction:rtl}.crumb,.meta,.price,.acts,.band .wrap,'
           '.foot,.thumbs,.nav{direction:rtl}</style>')

# filter key -> filter-bar label (shown on /tools/)
CATS = [("flux", "Soldering Flux"), ("paste", "Soldering Paste"),
        ("wire", "Solder Wire &amp; Ball"), ("tool", "Solder Tool")]

# Each product: dict with
#   slug, img (basename, no .webp), cat (filter key), badge (card chip + detail
#   breadcrumb label), title, now, was, save, sold, galn, short, overview, specs
P = lambda **k: k
PRODUCTS = [
 # ---------------- Soldering Flux ----------------
 P(slug="s800-flux", img="tool-01-s800-flux", cat="flux", badge="Flux",
   catlabel="Soldering Flux", title="S800 10cc Soldering Flux Paste",
   now="2.05", was="2.53", save="19", sold="316 sold", galn=6,
   short="Syringe with dispensing needle for BGA, PCB & SMD IC repair and rework.",
   overview="S800 is a ready-to-use soldering flux paste in a 10cc syringe with a dispensing needle, made for BGA, PCB and SMD IC repair and rework. It holds components in place and promotes clean, even solder wetting during reballing and chip-level work, on both leaded and lead-free joints.",
   specs=[("Model","S800"),("Net content","10cc"),("Form","Paste (syringe)"),("Application","BGA / PCB / SMD IC repair & rework"),("Package","1 x flux syringe + push rod + needle")]),
 P(slug="nc559-noclean", img="tool-04-nc559-noclean", cat="flux", badge="Flux",
   catlabel="Soldering Flux", title="NC-559-ASM 10cc No-Clean Flux",
   now="1.17", was="1.94", save="40", sold="76 sold", galn=6,
   short="No-clean BGA flux paste syringe for PCB & SMD IC repair and rework.",
   overview="The no-clean version of NC-559-ASM in a 10cc syringe. Its low-residue formula means boards can often be used without a cleaning step, while still giving strong wetting for BGA reballing and SMD rework.",
   specs=[("Model","NC-559-ASM"),("Net content","10cc"),("Type","No-clean paste"),("Application","BGA / PCB / SMD IC rework"),("Package","1 x syringe + push rod + needles")]),
 P(slug="nc559-10ml", img="tool-nc559-10ml", cat="flux", badge="Flux",
   catlabel="Soldering Flux", title="NC-559-ASM 10ml No-Clean Soldering Flux",
   now="1.85", was="3.69", save="50", sold="23 sold", galn=6,
   short="10ml no-clean flux for BGA, PCB & SMD IC rework and electronics repair.",
   overview="NC-559-ASM in a larger 10ml applicator, a no-clean soldering flux for BGA, PCB and SMD IC rework and general electronics repair. It wets quickly and leaves low residue, so boards can usually be used without a cleaning step.",
   specs=[("Model","NC-559-ASM"),("Net content","10ml"),("Type","No-clean flux"),("Application","BGA / PCB / SMD IC rework"),("Package","1 x flux + plunger + tips")]),
 P(slug="nc559-bga", img="tool-03-nc559-flux", cat="flux", badge="Flux",
   catlabel="Soldering Flux", title="NC-559-ASM 10cc BGA Flux Paste",
   now="2.24", was="3.73", save="40", sold="15 sold", galn=6,
   short="Welding flux syringe for PCB & SMD IC repair and rework work.",
   overview="NC-559-ASM is a BGA soldering flux paste in a 10cc syringe for PCB and SMD IC repair and rework. It wets quickly and helps solder flow evenly during reballing and fine-pitch soldering.",
   specs=[("Model","NC-559-ASM"),("Net content","10cc"),("Form","Paste (syringe)"),("Application","BGA / PCB / SMD IC rework"),("Package","1 x syringe + push rod + needles")]),
 P(slug="flux-100g", img="tool-05-flux-100g", cat="flux", badge="Flux",
   catlabel="Soldering Flux", title="100g Soldering Flux Paste (223/558/559/808)",
   now="5.75", was="9.13", save="37", sold="20 sold", galn=5,
   short="Bulk flux tub for BGA, PCB & SMD electronics repair and rework.",
   overview="A 100g tub of soldering flux paste for BGA, PCB and SMD electronics repair and rework, available in the popular 223, 558, 559 and 808 formulas. The bulk size suits busy repair benches and production rework.",
   specs=[("Net content","100g"),("Formulas","223 / 558 / 559 / 808"),("Form","Paste (tub)"),("Application","BGA / PCB / SMD repair & rework")]),
 P(slug="kek-flux-30ml", img="tool-kek-flux-30ml", cat="flux", badge="Flux",
   catlabel="Soldering Flux", title="KEK 30mL Soldering Flux Paste (Multi-Formula)",
   now="3.94", was="5.26", save="25", sold="New", galn=6,
   short="30mL flux in NC-559/558, RMA-223 and NC-218 formulas, with plunger & tips.",
   overview="A 30mL KEK soldering flux paste available in the popular NC-559-ASM, NC-558-ASM, RMA-223-ASM and NC-218-ASM formulas, supplied with a plunger and two tips for BGA and PCB repair. The larger volume suits busy repair benches.",
   specs=[("Model","KEK 30mL"),("Net content","30ml"),("Formulas","NC-559 / NC-558 / RMA-223 / NC-218"),("Application","BGA / PCB repair"),("Package","Flux + plunger + 2 tips")]),
 P(slug="rosin-30g", img="tool-07-rosin-30g", cat="flux", badge="Flux",
   catlabel="Soldering Flux", title="30g Rosin Soldering Flux Paste",
   now="1.15", was="1.83", save="37", sold="13 sold", galn=6,
   short="General-purpose rosin flux for soldering and tinning.",
   overview="A compact 30g tin of general-purpose rosin soldering flux paste for soldering and tinning. A low-cost staple for hobby and repair benches.",
   specs=[("Net content","30g"),("Type","Rosin paste"),("Application","General soldering & tinning")]),
 P(slug="hb18-rosin", img="tool-hb18-rosin", cat="flux", badge="Flux",
   catlabel="Soldering Flux", title="HB-18 30g Rosin Soldering Flux Paste",
   now="0.85", was="1.58", save="46", sold="New", galn=4,
   short="30g rosin flux paste for PCB repair, wire tinning and soldering.",
   overview="HB-18 is a 30g rosin soldering flux paste for PCB repair, wire tinning and electronic-component soldering. The rosin base gives dependable wetting for everyday bench work while leaving minimal residue.",
   specs=[("Model","HB-18"),("Net content","30g"),("Type","Rosin paste"),("Application","PCB repair / tinning / soldering")]),
 P(slug="zj18-rosin", img="tool-06-zj18-rosin", cat="flux", badge="Flux",
   catlabel="Soldering Flux", title="ZJ-18 50g Rosin Flux Paste",
   now="1.29", was="1.67", save="23", sold="2 sold", galn=6,
   short="No-clean rosin paste for PCB & SMD soldering and tinning.",
   overview="ZJ-18 is a 50g no-clean rosin flux paste for PCB and SMD soldering and tinning. The rosin base gives reliable wetting for general bench soldering while leaving minimal residue.",
   specs=[("Model","ZJ-18"),("Net content","50g"),("Type","No-clean rosin paste"),("Application","PCB / SMD soldering & tinning")]),
 P(slug="solid-rosin", img="tool-solid-rosin", cat="flux", badge="Flux",
   catlabel="Soldering Flux", title="Solid Rosin Soldering Flux Box",
   now="0.58", was="0.92", save="37", sold="New", galn=6,
   short="Traditional solid rosin block for wire tinning and DIY soldering.",
   overview="A box of traditional solid rosin soldering flux for PCB electronics repair, wire tinning and DIY soldering projects. Draw hot, tinned wire across the block for clean, low-cost fluxing.",
   specs=[("Type","Solid rosin"),("Form","Block (boxed)"),("Application","Wire tinning / general soldering")]),
 # ---------------- Soldering Paste ----------------
 P(slug="rl403-lowtemp", img="tool-11-rl403-lowtemp", cat="paste", badge="Solder Paste",
   catlabel="Solder Paste", title="RL-403 10cc Low-Temp Solder Paste 183°C",
   now="5.45", was="8.13", save="33", sold="New", galn=5,
   short="No-clean syringe for BGA, PCB & SMD mobile-phone repair.",
   overview="RL-403 is a low-temperature, no-clean solder paste in a 10cc syringe that reflows around 183°C, reducing thermal stress during BGA, PCB and SMD mobile-phone repair.",
   specs=[("Model","RL-403"),("Net content","10cc"),("Melting point","183°C"),("Type","No-clean solder paste"),("Application","BGA / PCB / SMD phone repair")]),
 P(slug="sac0307-50g", img="tool-sac0307-50g", cat="paste", badge="Solder Paste",
   catlabel="Solder Paste", title="SAC0307 Lead-Free Solder Paste 50g (227°C)",
   now="7.05", was="13.05", save="46", sold="New", galn=6,
   short="Sn99Ag0.3Cu0.7 lead-free paste, 50g syringe with needles & push rod.",
   overview="SAC0307 lead-free solder paste (Sn99.0 / Ag0.3 / Cu0.7) with a ~227°C reflow range, in a 50g syringe supplied with two needles and a push rod for PCB and SMD rework. Lead-free and RoHS-friendly.",
   specs=[("Alloy","Sn99Ag0.3Cu0.7 (SAC0307)"),("Melting point","227°C"),("Net content","50g"),("Type","Lead-free solder paste"),("Package","Syringe + 2 needles + push rod")]),
 P(slug="sac0307-35g", img="tool-sac0307-35g", cat="paste", badge="Solder Paste",
   catlabel="Solder Paste", title="SAC0307 Lead-Free Solder Paste 35g (227°C)",
   now="6.04", was="11.19", save="46", sold="New", galn=6,
   short="Sn99Ag0.3Cu0.7 lead-free paste, 35g syringe with needles & push rod.",
   overview="SAC0307 lead-free solder paste (Sn99.0 / Ag0.3 / Cu0.7) with a ~227°C reflow range, in a 35g syringe supplied with two needles and a push rod for PCB and SMD rework. Lead-free and RoHS-friendly.",
   specs=[("Alloy","Sn99Ag0.3Cu0.7 (SAC0307)"),("Melting point","227°C"),("Net content","35g"),("Type","Lead-free solder paste"),("Package","Syringe + 2 needles + push rod")]),
 P(slug="sac0307-20g", img="tool-sac0307-20g", cat="paste", badge="Solder Paste",
   catlabel="Solder Paste", title="SAC0307 Lead-Free Solder Paste 20g (227°C)",
   now="4.06", was="7.51", save="46", sold="New", galn=6,
   short="Sn99Ag0.3Cu0.7 lead-free paste, 20g syringe with needles & push rod.",
   overview="SAC0307 lead-free solder paste (Sn99.0 / Ag0.3 / Cu0.7) with a ~227°C reflow range, in a 20g syringe supplied with two needles and a push rod for PCB and SMD rework. Lead-free and RoHS-friendly.",
   specs=[("Alloy","Sn99Ag0.3Cu0.7 (SAC0307)"),("Melting point","227°C"),("Net content","20g"),("Type","Lead-free solder paste"),("Package","Syringe + 2 needles + push rod")]),
 P(slug="sac305-jar", img="tool-sac305-jar", cat="paste", badge="Solder Paste",
   catlabel="Solder Paste", title="KEK SAC305 Solder Paste 50g Jar",
   now="6.40", was="11.85", save="46", sold="New", galn=6,
   short="Sn96.5Ag3.0Cu0.5, 20-38µm powder, 50g jar for SMT & PCB assembly.",
   overview="KEK SAC305 solder paste (Sn96.5 / Ag3.0 / Cu0.5) with a 20-38µm powder, in a 50g jar for SMT, SMD and PCB assembly and rework. A mainstream lead-free alloy for stencil printing and reflow.",
   specs=[("Alloy","SAC305 (Sn96.5/Ag3.0/Cu0.5)"),("Powder","20-38µm"),("Net content","50g"),("Form","Jar"),("Application","SMT / PCB assembly & rework")]),
 P(slug="dp305-500g", img="tool-dp305-500g", cat="paste", badge="Solder Paste",
   catlabel="Solder Paste", title="DP305-8010 SAC305 Solder Paste 500g (217-220°C)",
   now="64.00", was="118.52", save="46", sold="New", galn=6,
   short="Lead-free SAC305, 500g, for SMT stencil printing & reflow (RoHS).",
   overview="DP305-8010 is a 500g lead-free SAC305 solder paste (Sn96.5 / Ag3.0 / Cu0.5) with a 217-220°C reflow range, for SMT stencil printing and reflow assembly. RoHS-compliant and sized for production lines.",
   specs=[("Model","DP305-8010"),("Alloy","SAC305 (Sn96.5/Ag3.0/Cu0.5)"),("Melting point","217-220°C"),("Net content","500g"),("Application","SMT stencil printing / reflow")]),
 P(slug="paste-6337-500g", img="tool-paste-6337-500g", cat="paste", badge="Solder Paste",
   catlabel="Solder Paste", title="Sn63Pb37 Solder Paste 500g (6337)",
   now="7.12", was="59.33", save="88", sold="New", galn=3,
   short="Leaded 63/37 solder paste, 500g, for PCB, SMT, BGA & IC repair.",
   overview="A 500g tub of Sn63/Pb37 (6337) leaded solder paste for PCB, SMT, BGA and IC electronics repair and rework. The classic eutectic alloy offers a low, forgiving melting point and reliable joints; bulk size for production use.",
   specs=[("Alloy","Sn63Pb37 (6337)"),("Type","Leaded solder paste"),("Net content","500g"),("Application","PCB / SMT / BGA / IC rework")]),
 P(slug="pcb-redglue", img="tool-09-pcb-redglue", cat="paste", badge="Adhesive",
   catlabel="Adhesive", title="30g PCB Red Glue (SMT)",
   now="9.45", was="18.90", save="50", sold="5 sold", galn=6,
   short="High-temperature curing SMT/BGA patch dispensing glue for screen printing.",
   overview="A 30g syringe of SMT/BGA red adhesive (PCB red glue) that cures at high temperature to hold components before reflow. Suited to stencil / screen-printing and dispensing on steel and copper screens.",
   specs=[("Net content","30g"),("Type","SMT / BGA red adhesive"),("Cure","High-temperature"),("Use","Screen / stencil dispensing")]),
 # ---------------- Solder Wire & Ball ----------------
 P(slug="solderwire-300cm", img="tool-08-solderwire-300cm", cat="wire", badge="Solder Wire",
   catlabel="Solder Wire", title="Multi-Function Solder Wire 300cm Ø1.0mm",
   now="2.99", was="4.15", save="28", sold="40 sold", galn=6,
   short="Special-core wire for stainless steel, aluminum and nickel soldering.",
   overview="A 300cm length of 1.0mm multi-function solder wire with a special core that lets it bond stainless steel, aluminum and nickel as well as standard electronics work - useful where ordinary solder will not wet the metal.",
   specs=[("Diameter","1.0 mm"),("Length","300 cm"),("Core","Special multi-metal core"),("Works on","Stainless steel / aluminum / nickel")]),
 P(slug="wire-sn63-50g", img="tool-wire-sn63-50g", cat="wire", badge="Solder Wire",
   catlabel="Solder Wire", title="KEK Sn63 Rosin-Core Solder Wire 50g",
   now="1.50", was="2.37", save="37", sold="New", galn=6,
   short="Sn63 rosin-core wire, Ø0.8/1.0mm, 50g, for PCB & electronics repair.",
   overview="KEK Sn63 solder wire with a 2.2% rosin flux core, available in 0.8mm and 1.0mm, in a 50g roll for PCB and electronics repair and DIY soldering. The Sn63 eutectic alloy melts cleanly at a low, stable temperature.",
   specs=[("Brand","KEK"),("Alloy","Sn63"),("Diameter","0.8 / 1.0 mm"),("Core","Rosin flux (2.2%)"),("Net content","50g"),("Application","PCB / electronics soldering")]),
 P(slug="wire-sn63-3m", img="tool-wire-sn63-3m", cat="wire", badge="Solder Wire",
   catlabel="Solder Wire", title="KEK Sn63 Solder Wire 3m Tube",
   now="2.15", was="3.41", save="37", sold="New", galn=6,
   short="Sn63 rosin-core wire, Ø0.8/1.0mm, 3m tube, for PCB & electronics repair.",
   overview="KEK Sn63 solder wire with a 2.2% rosin flux core, available in 0.8mm and 1.0mm, in a handy 3m tube for PCB and electronics repair. The Sn63 eutectic alloy melts cleanly at a low, stable temperature.",
   specs=[("Brand","KEK"),("Alloy","Sn63"),("Diameter","0.8 / 1.0 mm"),("Core","Rosin flux (2.2%)"),("Length","3 m (tube)"),("Application","PCB / electronics soldering")]),
 P(slug="wire-sn993-3m", img="tool-wire-sn993-3m", cat="wire", badge="Solder Wire",
   catlabel="Solder Wire", title="KEK Sn99.3Cu0.7 Solder Wire 3m Tube",
   now="2.40", was="3.81", save="37", sold="New", galn=6,
   short="Lead-free Sn99.3Cu0.7 wire, Ø0.8/1.0mm, 3m tube, rosin flux core.",
   overview="KEK Sn99.3 / Cu0.7 lead-free solder wire with a 2.2% rosin flux core, available in 0.8mm and 1.0mm, in a 3m tube for PCB and electronics repair. A lead-free tin-copper alloy for RoHS work.",
   specs=[("Brand","KEK"),("Alloy","Sn99.3Cu0.7 (lead-free)"),("Diameter","0.8 / 1.0 mm"),("Core","Rosin flux (2.2%)"),("Length","3 m (tube)"),("Application","PCB / electronics soldering")]),
 P(slug="wire-sn993-100g", img="tool-wire-sn993-100g", cat="wire", badge="Solder Wire",
   catlabel="Solder Wire", title="KEK Sn99.3Cu0.7 Solder Wire 100g",
   now="7.14", was="11.33", save="37", sold="New", galn=5,
   short="Lead-free Sn99.3Cu0.7 wire, Ø1.0mm, 100g roll, rosin flux core.",
   overview="KEK Sn99.3 / Cu0.7 lead-free tin-copper solder wire with a 2.2% rosin flux core, in a 100g roll at 1.0mm for PCB and electronics repair and DIY soldering. RoHS-compliant and economical for volume work.",
   specs=[("Brand","KEK"),("Alloy","Sn99.3Cu0.7 (lead-free)"),("Diameter","1.0 mm"),("Core","Rosin flux (2.2%)"),("Net content","100g"),("Application","PCB / electronics soldering")]),
 P(slug="wire-sn99-100g", img="tool-wire-sn99-100g", cat="wire", badge="Solder Wire",
   catlabel="Solder Wire", title="KEK Sn99 Ag0.3 Cu0.7 Solder Wire 100g",
   now="7.47", was="11.85", save="37", sold="New", galn=4,
   short="Lead-free Sn99Ag0.3Cu0.7 wire, Ø0.8/1.0mm, 100g, rosin flux core.",
   overview="KEK Sn99 / Ag0.3 / Cu0.7 lead-free solder wire with a 2.2% rosin flux core, available in 0.8mm and 1.0mm, in a 100g roll for PCB and electronics repair. The silver-bearing alloy gives bright, strong joints.",
   specs=[("Brand","KEK"),("Alloy","Sn99Ag0.3Cu0.7 (lead-free)"),("Diameter","0.8 / 1.0 mm"),("Core","Rosin flux (2.2%)"),("Net content","100g"),("Application","PCB / electronics soldering")]),
 P(slug="wire-63-100g", img="tool-wire-63-100g", cat="wire", badge="Solder Wire",
   catlabel="Solder Wire", title="KEK 63% Tin Solder Wire 100g",
   now="3.31", was="5.26", save="37", sold="New", galn=6,
   short="63% tin alloy wire, Ø0.8/1.0mm, 100g roll, 2.0% rosin flux core.",
   overview="KEK 63%-tin alloy solder wire with a 2.0% rosin flux core, available in 0.8mm and 1.0mm, in a 100g roll for PCB and electronics repair and DIY soldering. A low-melting, easy-flowing everyday solder.",
   specs=[("Brand","KEK"),("Alloy","63% tin"),("Diameter","0.8 / 1.0 mm"),("Core","Rosin flux (2.0%)"),("Net content","100g"),("Application","PCB / electronics soldering")]),
 P(slug="wire-6040-50g", img="tool-wire-6040-50g", cat="wire", badge="Solder Wire",
   catlabel="Solder Wire", title="KEK 60/40 Solder Wire 50g",
   now="2.67", was="3.81", save="30", sold="New", galn=5,
   short="60/40 tin-lead wire, Ø0.8/1.0mm, 50g roll, 2.0% rosin flux core.",
   overview="KEK 60/40 tin-lead solder wire with a 2.0% rosin flux core, available in 0.8mm and 1.0mm, in a 50g roll for PCB and electronics repair and DIY soldering. The 60/40 alloy is a forgiving, general-purpose solder.",
   specs=[("Brand","KEK"),("Alloy","60/40 Sn-Pb"),("Diameter","0.8 / 1.0 mm"),("Core","Rosin flux (2.0%)"),("Net content","50g"),("Application","PCB / electronics soldering")]),
 P(slug="solderball-sac305", img="tool-02-solderball-sac305", cat="wire", badge="Solder Balls",
   catlabel="Solder Balls", title="Lead-Free BGA Solder Balls (SAC305)",
   now="3.36", was="5.33", save="37", sold="30 sold", galn=6,
   short="0.25-0.76mm leadless tin beads, 2,500 pcs bottled, for BGA reballing.",
   overview="Lead-free BGA reballing solder balls in SAC305 alloy (Sn96.5 / Ag3.0 / Cu0.5). Supplied bottled in roughly 2,500-piece quantities across common diameters, for reballing BGA chips during board-level and phone repair.",
   specs=[("Alloy","SAC305 (Sn96.5/Ag3.0/Cu0.5)"),("Diameters","0.25 - 0.76 mm"),("Quantity","approx. 2,500 pcs / bottle"),("Type","Lead-free"),("Application","BGA reballing")]),
 # ---------------- Solder Tool ----------------
 P(slug="usb-iron", img="tool-10-usb-iron", cat="tool", badge="Tool",
   catlabel="Tool", title="USB Wireless Soldering Iron Set (USB-102)",
   now="19.09", was="32.91", save="42", sold="13 sold", galn=6,
   short="Mini 18650-battery iron, 1500mA removable, large-capacity portable kit.",
   overview="USB-102 is a cordless mini soldering iron set powered by a removable 18650 battery (1500mA), for soldering away from a bench or mains outlet. The large-capacity kit is built for portable field and hobby repair.",
   specs=[("Model","USB-102"),("Power source","18650 battery (removable)"),("Battery","1500mA"),("Type","Cordless / USB-charge portable kit")]),
 P(slug="magnifier", img="tool-12-magnifier", cat="tool", badge="Optics",
   catlabel="Optics", title="You Qian Magnifier 1x / 2x / 3x",
   now="4.29", was="5.43", save="21", sold="New", galn=4,
   short="Optical instrument for reading and close-up repair and inspection work.",
   overview="A You Qian optical magnifier offering 1x, 2x and 3x views for reading and close-up repair and inspection work - handy for checking solder joints, fine print and small components.",
   specs=[("Magnification","1x / 2x / 3x"),("Type","Optical magnifier"),("Use","Reading / close-up repair & inspection")]),
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


def esc(s):
    return _html.escape(s, quote=True)


def _write(d, html):
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def gen():
    for p in PRODUCTS:
        slug, title = p["slug"], p["title"]
        gbase = "/assets/tools/gallery/" + slug
        imgs = [gbase + "/g%d.webp" % i for i in range(1, p["galn"] + 1)]
        thumbs = "".join(
            '<button class="%s" data-src="%s"><img src="%s" alt="view %d"></button>'
            % ("active" if i == 0 else "", u, u, i + 1) for i, u in enumerate(imgs))
        detailimgs = "".join('<img src="%s" alt="%s detail %d" loading="lazy">' % (u, esc(title), i + 1) for i, u in enumerate(imgs))
        specrows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (esc(k), esc(v)) for k, v in p["specs"])
        repl = {
            "@@SLUG@@": slug, "@@CAT@@": esc(p["catlabel"]), "@@TITLE@@": esc(title),
            "@@NOW@@": p["now"], "@@WAS@@": p["was"], "@@SAVE@@": p["save"], "@@SOLD@@": esc(p["sold"]),
            "@@SHORT@@": esc(p["short"]), "@@OVERVIEW@@": esc(p["overview"]),
            "@@G1@@": imgs[0], "@@THUMBS@@": thumbs, "@@DETAILIMGS@@": detailimgs, "@@SPECROWS@@": specrows,
            "@@WA@@": WA, "@@EMAIL@@": EMAIL, "@@Q@@": urllib.parse.quote(title),
        }
        page = PAGE
        for k, v in repl.items():
            page = page.replace(k, v)
        page_en = page.replace(
            '<link rel="canonical" href="%s/tools/p/%s/">' % (BASE, slug),
            head_block(slug, "en"), 1)
        _write(os.path.join(ROOT, "tools", "p", slug), page_en)
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


def _card(p):
    q = urllib.parse.quote(p["title"])
    sold = ('<span class="sold">%s</span>' % esc(p["sold"])) if "sold" in p["sold"] else ""
    return (
        '      <article class="card" data-cat="%s">\n'
        '        <a class="ph" href="/tools/p/%s/" aria-label="View details"><span class="cat">%s</span>%s<img src="/assets/tools/%s.webp" alt="%s" loading="lazy"></a>\n'
        '        <div class="body">\n'
        '          <h3><a href="/tools/p/%s/">%s</a></h3>\n'
        '          <p class="desc">%s</p>\n'
        '          <div class="price"><span class="now">$%s</span><span class="was">$%s</span><span class="save">-%s%%</span></div>\n'
        '          <div class="acts"><a class="wa" href="https://wa.me/%s?text=Inquiry%%3A%%20%s" target="_blank" rel="noopener">WhatsApp</a><a class="em" href="mailto:%s?subject=Inquiry%%3A%%20%s">Email</a></div>\n'
        '        </div>\n'
        '      </article>\n'
    ) % (p["cat"], p["slug"], esc(p["badge"]), sold, p["img"], esc(p["title"]),
         p["slug"], esc(p["title"]), esc(p["short"]), p["now"], p["was"], p["save"],
         WA, q, EMAIL, q)


def build_grid():
    """Regenerate the filter bar + card grid inside tools/index.html."""
    path = os.path.join(ROOT, "tools", "index.html")
    with open(path, encoding="utf-8") as f:
        s = f.read()

    # filter bar
    counts = {k: sum(1 for p in PRODUCTS if p["cat"] == k) for k, _ in CATS}
    chips = ['    <span class="lab">Filter</span>',
             '    <button class="chip active" data-cat="all">All <span class="ct">%d</span></button>' % len(PRODUCTS)]
    for key, label in CATS:
        chips.append('    <button class="chip" data-cat="%s">%s <span class="ct">%d</span></button>'
                     % (key, label, counts[key]))
    filters_html = ('<div class="wrap filters" id="filters">\n' + "\n".join(chips) + "\n  </div>")
    s = re.sub(r'<div class="wrap filters" id="filters">.*?</div>', lambda m: filters_html, s, count=1, flags=re.S)

    # card grid (everything between grid open and the empty-state div)
    cards = "".join(_card(p) for p in PRODUCTS)
    start = s.index('<div class="grid" id="grid">')
    empty = s.index('<div class="empty"', start)
    new = '<div class="grid" id="grid">\n\n' + cards + '\n    </div>\n    '
    s = s[:start] + new + s[empty:]

    # card link styles (idempotent)
    if 'a.ph{display:block}' not in s:
        s = s.replace('</style>', '  a.ph{display:block} .card h3 a{color:inherit} .card h3 a:hover{color:var(--amber-deep)}\n</style>', 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print("rebuilt catalog grid: %d cards, counts %s" % (len(PRODUCTS), counts))


if __name__ == "__main__":
    NAV = _load("translations_nav.json")
    TOOLS = _load("translations_tools.json")
    DETAIL = _load("translations_detail.json")
    build_grid()
    gen()
