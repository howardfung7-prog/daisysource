#!/usr/bin/env python3
"""Merge catalog translations for the 17 added products (+ 3 new filter labels)
into translations_tools.json. Idempotent: re-running just overwrites the same keys.
Run:  python3 i18n/_add_tools_tr.py
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "translations_tools.json")

L = ["es", "pt", "fr", "ja", "ko", "id", "ar"]
def row(*vals):
    return dict(zip(L, vals))

ENTRIES = {
 # ---- filter chip labels (new categories) ----
 'data-cat="paste">Soldering Paste <span': row(
   'data-cat="paste">Pasta de soldadura <span', 'data-cat="paste">Pasta de solda <span',
   'data-cat="paste">Pâte à souder <span', 'data-cat="paste">ソルダーペースト <span',
   'data-cat="paste">솔더 페이스트 <span', 'data-cat="paste">Pasta solder <span',
   'data-cat="paste">معجون اللحام <span'),
 'data-cat="wire">Solder Wire &amp; Ball <span': row(
   'data-cat="wire">Alambre y bolas <span', 'data-cat="wire">Fio e esferas <span',
   'data-cat="wire">Fil et billes <span', 'data-cat="wire">はんだ線・ボール <span',
   'data-cat="wire">와이어·볼 <span', 'data-cat="wire">Kawat &amp; bola <span',
   'data-cat="wire">سلك وكرات اللحام <span'),
 'data-cat="tool">Solder Tool <span': row(
   'data-cat="tool">Herramientas <span', 'data-cat="tool">Ferramentas <span',
   'data-cat="tool">Outils <span', 'data-cat="tool">工具 <span',
   'data-cat="tool">공구 <span', 'data-cat="tool">Peralatan <span',
   'data-cat="tool">أدوات اللحام <span'),

 # ---- titles (17) ----
 "NC-559-ASM 10ml No-Clean Soldering Flux": row(
   "Flux de soldadura sin limpieza NC-559-ASM 10ml", "Fluxo de solda sem limpeza NC-559-ASM 10ml",
   "Flux de soudure sans nettoyage NC-559-ASM 10 ml", "NC-559-ASM 10ml 無洗浄フラックス",
   "NC-559-ASM 10ml 무세척 플럭스", "Fluks Solder No-Clean NC-559-ASM 10ml",
   "معجون لحام NC-559-ASM 10ml بدون تنظيف"),
 "KEK 30mL Soldering Flux Paste (Multi-Formula)": row(
   "Pasta de flux de soldadura KEK 30mL (multifórmula)", "Pasta de fluxo de solda KEK 30mL (multifórmula)",
   "Pâte de flux à souder KEK 30 ml (multi-formule)", "KEK 30mL フラックスペースト（マルチ処方）",
   "KEK 30mL 플럭스 페이스트 (멀티 포뮬러)", "Pasta Fluks Solder KEK 30mL (Multi-Formula)",
   "معجون لحام KEK 30mL (متعدد التركيبات)"),
 "HB-18 30g Rosin Soldering Flux Paste": row(
   "Pasta de flux de colofonia HB-18 30g", "Pasta de fluxo de breu HB-18 30g",
   "Pâte de flux à la colophane HB-18 30 g", "HB-18 30g ロジンフラックスペースト",
   "HB-18 30g 로진 플럭스 페이스트", "Pasta Fluks Rosin HB-18 30g",
   "معجون لحام بالراتنج HB-18 30g"),
 "Solid Rosin Soldering Flux Box": row(
   "Caja de colofonia sólida para soldadura", "Caixa de breu sólido para solda",
   "Boîte de colophane solide à souder", "固形ロジンフラックス（箱入り）",
   "고형 로진 플럭스 (박스)", "Kotak Rosin Padat untuk Solder",
   "علبة راتنج صلب للحام"),
 "SAC0307 Lead-Free Solder Paste 50g (227°C)": row(
   "Pasta de soldadura sin plomo SAC0307 50g (227°C)", "Pasta de solda sem chumbo SAC0307 50g (227°C)",
   "Pâte à souder sans plomb SAC0307 50 g (227°C)", "SAC0307 無鉛ソルダーペースト 50g（227°C）",
   "SAC0307 무연 솔더 페이스트 50g (227°C)", "Pasta Solder Bebas Timbal SAC0307 50g (227°C)",
   "معجون لحام خالٍ من الرصاص SAC0307 50g (227°C)"),
 "SAC0307 Lead-Free Solder Paste 35g (227°C)": row(
   "Pasta de soldadura sin plomo SAC0307 35g (227°C)", "Pasta de solda sem chumbo SAC0307 35g (227°C)",
   "Pâte à souder sans plomb SAC0307 35 g (227°C)", "SAC0307 無鉛ソルダーペースト 35g（227°C）",
   "SAC0307 무연 솔더 페이스트 35g (227°C)", "Pasta Solder Bebas Timbal SAC0307 35g (227°C)",
   "معجون لحام خالٍ من الرصاص SAC0307 35g (227°C)"),
 "SAC0307 Lead-Free Solder Paste 20g (227°C)": row(
   "Pasta de soldadura sin plomo SAC0307 20g (227°C)", "Pasta de solda sem chumbo SAC0307 20g (227°C)",
   "Pâte à souder sans plomb SAC0307 20 g (227°C)", "SAC0307 無鉛ソルダーペースト 20g（227°C）",
   "SAC0307 무연 솔더 페이스트 20g (227°C)", "Pasta Solder Bebas Timbal SAC0307 20g (227°C)",
   "معجون لحام خالٍ من الرصاص SAC0307 20g (227°C)"),
 "KEK SAC305 Solder Paste 50g Jar": row(
   "Pasta de soldadura KEK SAC305 50g (bote)", "Pasta de solda KEK SAC305 50g (pote)",
   "Pâte à souder KEK SAC305 50 g (pot)", "KEK SAC305 ソルダーペースト 50g（ジャー）",
   "KEK SAC305 솔더 페이스트 50g (용기)", "Pasta Solder KEK SAC305 50g (Toples)",
   "معجون لحام KEK SAC305 50g (علبة)"),
 "DP305-8010 SAC305 Solder Paste 500g (217-220°C)": row(
   "Pasta de soldadura SAC305 DP305-8010 500g (217-220°C)", "Pasta de solda SAC305 DP305-8010 500g (217-220°C)",
   "Pâte à souder SAC305 DP305-8010 500 g (217-220°C)", "DP305-8010 SAC305 ソルダーペースト 500g（217-220°C）",
   "DP305-8010 SAC305 솔더 페이스트 500g (217-220°C)", "Pasta Solder SAC305 DP305-8010 500g (217-220°C)",
   "معجون لحام SAC305 DP305-8010 500g (217-220°C)"),
 "Sn63Pb37 Solder Paste 500g (6337)": row(
   "Pasta de soldadura Sn63Pb37 500g (6337)", "Pasta de solda Sn63Pb37 500g (6337)",
   "Pâte à souder Sn63Pb37 500 g (6337)", "Sn63Pb37 ソルダーペースト 500g（6337）",
   "Sn63Pb37 솔더 페이스트 500g (6337)", "Pasta Solder Sn63Pb37 500g (6337)",
   "معجون لحام Sn63Pb37 500g (6337)"),
 "KEK Sn63 Rosin-Core Solder Wire 50g": row(
   "Alambre de soldadura KEK Sn63 con núcleo de colofonia 50g", "Fio de solda KEK Sn63 com núcleo de breu 50g",
   "Fil à souder KEK Sn63 à âme de colophane 50 g", "KEK Sn63 ヤニ入りはんだ線 50g",
   "KEK Sn63 로진 코어 땜납 와이어 50g", "Kawat Solder KEK Sn63 Inti Rosin 50g",
   "سلك لحام KEK Sn63 بقلب راتنجي 50g"),
 "KEK Sn63 Solder Wire 3m Tube": row(
   "Alambre de soldadura KEK Sn63 tubo de 3m", "Fio de solda KEK Sn63 tubo de 3m",
   "Fil à souder KEK Sn63 tube de 3 m", "KEK Sn63 はんだ線 3mチューブ",
   "KEK Sn63 땜납 와이어 3m 튜브", "Kawat Solder KEK Sn63 Tabung 3m",
   "سلك لحام KEK Sn63 أنبوب 3m"),
 "KEK Sn99.3Cu0.7 Solder Wire 3m Tube": row(
   "Alambre de soldadura KEK Sn99.3Cu0.7 tubo de 3m", "Fio de solda KEK Sn99.3Cu0.7 tubo de 3m",
   "Fil à souder KEK Sn99.3Cu0.7 tube de 3 m", "KEK Sn99.3Cu0.7 はんだ線 3mチューブ",
   "KEK Sn99.3Cu0.7 땜납 와이어 3m 튜브", "Kawat Solder KEK Sn99.3Cu0.7 Tabung 3m",
   "سلك لحام KEK Sn99.3Cu0.7 أنبوب 3m"),
 "KEK Sn99.3Cu0.7 Solder Wire 100g": row(
   "Alambre de soldadura KEK Sn99.3Cu0.7 100g", "Fio de solda KEK Sn99.3Cu0.7 100g",
   "Fil à souder KEK Sn99.3Cu0.7 100 g", "KEK Sn99.3Cu0.7 はんだ線 100g",
   "KEK Sn99.3Cu0.7 땜납 와이어 100g", "Kawat Solder KEK Sn99.3Cu0.7 100g",
   "سلك لحام KEK Sn99.3Cu0.7 100g"),
 "KEK Sn99 Ag0.3 Cu0.7 Solder Wire 100g": row(
   "Alambre de soldadura KEK Sn99 Ag0.3 Cu0.7 100g", "Fio de solda KEK Sn99 Ag0.3 Cu0.7 100g",
   "Fil à souder KEK Sn99 Ag0.3 Cu0.7 100 g", "KEK Sn99 Ag0.3 Cu0.7 はんだ線 100g",
   "KEK Sn99 Ag0.3 Cu0.7 땜납 와이어 100g", "Kawat Solder KEK Sn99 Ag0.3 Cu0.7 100g",
   "سلك لحام KEK Sn99 Ag0.3 Cu0.7 100g"),
 "KEK 63% Tin Solder Wire 100g": row(
   "Alambre de soldadura KEK 63% estaño 100g", "Fio de solda KEK 63% estanho 100g",
   "Fil à souder KEK 63% étain 100 g", "KEK 63% スズはんだ線 100g",
   "KEK 63% 주석 땜납 와이어 100g", "Kawat Solder KEK Timah 63% 100g",
   "سلك لحام KEK قصدير 63% 100g"),
 "KEK 60/40 Solder Wire 50g": row(
   "Alambre de soldadura KEK 60/40 50g", "Fio de solda KEK 60/40 50g",
   "Fil à souder KEK 60/40 50 g", "KEK 60/40 はんだ線 50g",
   "KEK 60/40 땜납 와이어 50g", "Kawat Solder KEK 60/40 50g",
   "سلك لحام KEK 60/40 50g"),

 # ---- short descriptions (17) ----
 "10ml no-clean flux for BGA, PCB & SMD IC rework and electronics repair.": row(
   "Flux sin limpieza de 10 ml para retrabajo de BGA, PCB y SMD y reparación electrónica.",
   "Fluxo sem limpeza de 10 ml para retrabalho de BGA, PCB e SMD e reparo eletrônico.",
   "Flux sans nettoyage de 10 ml pour reprise BGA, PCB & SMD et réparation électronique.",
   "BGA・PCB・SMD ICのやり直しと電子機器修理向けの10ml無洗浄フラックス。",
   "BGA, PCB, SMD IC 리워크 및 전자 수리를 위한 10ml 무세척 플럭스.",
   "Fluks no-clean 10ml untuk rework BGA, PCB & SMD dan perbaikan elektronik.",
   "معجون لحام 10ml بدون تنظيف لإعادة عمل BGA وPCB وSMD وإصلاح الإلكترونيات."),
 "30mL flux in NC-559/558, RMA-223 and NC-218 formulas, with plunger & tips.": row(
   "Flux de 30 ml en fórmulas NC-559/558, RMA-223 y NC-218, con émbolo y puntas.",
   "Fluxo de 30 ml nas fórmulas NC-559/558, RMA-223 e NC-218, com êmbolo e pontas.",
   "Flux de 30 ml en formules NC-559/558, RMA-223 et NC-218, avec piston et embouts.",
   "NC-559/558・RMA-223・NC-218処方の30mlフラックス、プランジャーとチップ付き。",
   "NC-559/558, RMA-223, NC-218 포뮬러 30ml 플럭스, 플런저·팁 포함.",
   "Fluks 30ml dalam formula NC-559/558, RMA-223 dan NC-218, dengan plunger & tip.",
   "معجون لحام 30ml بتركيبات NC-559/558 وRMA-223 وNC-218، مع مكبس وأطراف."),
 "30g rosin flux paste for PCB repair, wire tinning and soldering.": row(
   "Pasta de flux de colofonia de 30 g para reparación de PCB, estañado de cables y soldadura.",
   "Pasta de fluxo de breu de 30 g para reparo de PCB, estanhagem de fios e solda.",
   "Pâte de flux à la colophane de 30 g pour réparation de PCB, étamage de fils et soudure.",
   "PCB修理・線材のすず引き・はんだ付け向けの30gロジンフラックスペースト。",
   "PCB 수리, 와이어 주석 도금, 납땜용 30g 로진 플럭스 페이스트.",
   "Pasta fluks rosin 30g untuk perbaikan PCB, pelapisan timah kawat, dan penyolderan.",
   "معجون لحام بالراتنج 30g لإصلاح PCB وتقصدير الأسلاك واللحام."),
 "Traditional solid rosin block for wire tinning and DIY soldering.": row(
   "Bloque de colofonia sólida tradicional para estañado de cables y soldadura DIY.",
   "Bloco de breu sólido tradicional para estanhagem de fios e solda DIY.",
   "Bloc de colophane solide traditionnel pour étamage de fils et soudure DIY.",
   "線材のすず引きやDIYはんだ付け向けの伝統的な固形ロジン。",
   "와이어 주석 도금 및 DIY 납땜용 전통 고형 로진 블록.",
   "Balok rosin padat tradisional untuk pelapisan timah kawat dan solder DIY.",
   "كتلة راتنج صلب تقليدية لتقصدير الأسلاك واللحام اليدوي."),
 "Sn99Ag0.3Cu0.7 lead-free paste, 50g syringe with needles & push rod.": row(
   "Pasta sin plomo Sn99Ag0.3Cu0.7, jeringa de 50 g con agujas y émbolo.",
   "Pasta sem chumbo Sn99Ag0.3Cu0.7, seringa de 50 g com agulhas e êmbolo.",
   "Pâte sans plomb Sn99Ag0.3Cu0.7, seringue de 50 g avec aiguilles et piston.",
   "Sn99Ag0.3Cu0.7 無鉛ペースト、針とプッシュロッド付き50gシリンジ。",
   "Sn99Ag0.3Cu0.7 무연 페이스트, 바늘·푸시로드 포함 50g 주사기.",
   "Pasta bebas timbal Sn99Ag0.3Cu0.7, jarum suntik 50g dengan jarum & push rod.",
   "معجون خالٍ من الرصاص Sn99Ag0.3Cu0.7، حقنة 50g مع إبر وقضيب دفع."),
 "Sn99Ag0.3Cu0.7 lead-free paste, 35g syringe with needles & push rod.": row(
   "Pasta sin plomo Sn99Ag0.3Cu0.7, jeringa de 35 g con agujas y émbolo.",
   "Pasta sem chumbo Sn99Ag0.3Cu0.7, seringa de 35 g com agulhas e êmbolo.",
   "Pâte sans plomb Sn99Ag0.3Cu0.7, seringue de 35 g avec aiguilles et piston.",
   "Sn99Ag0.3Cu0.7 無鉛ペースト、針とプッシュロッド付き35gシリンジ。",
   "Sn99Ag0.3Cu0.7 무연 페이스트, 바늘·푸시로드 포함 35g 주사기.",
   "Pasta bebas timbal Sn99Ag0.3Cu0.7, jarum suntik 35g dengan jarum & push rod.",
   "معجون خالٍ من الرصاص Sn99Ag0.3Cu0.7، حقنة 35g مع إبر وقضيب دفع."),
 "Sn99Ag0.3Cu0.7 lead-free paste, 20g syringe with needles & push rod.": row(
   "Pasta sin plomo Sn99Ag0.3Cu0.7, jeringa de 20 g con agujas y émbolo.",
   "Pasta sem chumbo Sn99Ag0.3Cu0.7, seringa de 20 g com agulhas e êmbolo.",
   "Pâte sans plomb Sn99Ag0.3Cu0.7, seringue de 20 g avec aiguilles et piston.",
   "Sn99Ag0.3Cu0.7 無鉛ペースト、針とプッシュロッド付き20gシリンジ。",
   "Sn99Ag0.3Cu0.7 무연 페이스트, 바늘·푸시로드 포함 20g 주사기.",
   "Pasta bebas timbal Sn99Ag0.3Cu0.7, jarum suntik 20g dengan jarum & push rod.",
   "معجون خالٍ من الرصاص Sn99Ag0.3Cu0.7، حقنة 20g مع إبر وقضيب دفع."),
 "Sn96.5Ag3.0Cu0.5, 20-38µm powder, 50g jar for SMT & PCB assembly.": row(
   "Sn96.5Ag3.0Cu0.5, polvo de 20-38 µm, bote de 50 g para montaje SMT y PCB.",
   "Sn96.5Ag3.0Cu0.5, pó de 20-38 µm, pote de 50 g para montagem SMT e PCB.",
   "Sn96.5Ag3.0Cu0.5, poudre de 20-38 µm, pot de 50 g pour assemblage SMT et PCB.",
   "Sn96.5Ag3.0Cu0.5、20-38µm粉末、SMT・PCB実装向け50gジャー。",
   "Sn96.5Ag3.0Cu0.5, 20-38µm 분말, SMT·PCB 조립용 50g 용기.",
   "Sn96.5Ag3.0Cu0.5, bubuk 20-38µm, toples 50g untuk perakitan SMT & PCB.",
   "Sn96.5Ag3.0Cu0.5، مسحوق 20-38µm، علبة 50g لتجميع SMT وPCB."),
 "Lead-free SAC305, 500g, for SMT stencil printing & reflow (RoHS).": row(
   "SAC305 sin plomo, 500 g, para impresión por estarcido SMT y reflujo (RoHS).",
   "SAC305 sem chumbo, 500 g, para impressão por estêncil SMT e refluxo (RoHS).",
   "SAC305 sans plomb, 500 g, pour impression au pochoir SMT et refusion (RoHS).",
   "無鉛SAC305、500g、SMTステンシル印刷・リフロー向け（RoHS）。",
   "무연 SAC305, 500g, SMT 스텐실 인쇄·리플로우용 (RoHS).",
   "SAC305 bebas timbal, 500g, untuk pencetakan stensil SMT & reflow (RoHS).",
   "SAC305 خالٍ من الرصاص، 500g، لطباعة استنسل SMT وإعادة الانصهار (RoHS)."),
 "Leaded 63/37 solder paste, 500g, for PCB, SMT, BGA & IC repair.": row(
   "Pasta de soldadura con plomo 63/37, 500 g, para reparación de PCB, SMT, BGA e IC.",
   "Pasta de solda com chumbo 63/37, 500 g, para reparo de PCB, SMT, BGA e IC.",
   "Pâte à souder au plomb 63/37, 500 g, pour réparation PCB, SMT, BGA et IC.",
   "有鉛63/37ソルダーペースト、500g、PCB・SMT・BGA・IC修理向け。",
   "유연 63/37 솔더 페이스트, 500g, PCB, SMT, BGA, IC 수리용.",
   "Pasta solder bertimbal 63/37, 500g, untuk perbaikan PCB, SMT, BGA & IC.",
   "معجون لحام بالرصاص 63/37، 500g، لإصلاح PCB وSMT وBGA وIC."),
 "Sn63 rosin-core wire, Ø0.8/1.0mm, 50g, for PCB & electronics repair.": row(
   "Alambre Sn63 con núcleo de colofonia, Ø0.8/1.0 mm, 50 g, para reparación de PCB y electrónica.",
   "Fio Sn63 com núcleo de breu, Ø0.8/1.0 mm, 50 g, para reparo de PCB e eletrônica.",
   "Fil Sn63 à âme de colophane, Ø0,8/1,0 mm, 50 g, pour réparation PCB et électronique.",
   "Sn63ヤニ入り線、Ø0.8/1.0mm、50g、PCB・電子機器修理向け。",
   "Sn63 로진 코어 와이어, Ø0.8/1.0mm, 50g, PCB·전자 수리용.",
   "Kawat Sn63 inti rosin, Ø0.8/1.0mm, 50g, untuk perbaikan PCB & elektronik.",
   "سلك Sn63 بقلب راتنجي، Ø0.8/1.0mm، 50g، لإصلاح PCB والإلكترونيات."),
 "Sn63 rosin-core wire, Ø0.8/1.0mm, 3m tube, for PCB & electronics repair.": row(
   "Alambre Sn63 con núcleo de colofonia, Ø0.8/1.0 mm, tubo de 3 m, para reparación de PCB y electrónica.",
   "Fio Sn63 com núcleo de breu, Ø0.8/1.0 mm, tubo de 3 m, para reparo de PCB e eletrônica.",
   "Fil Sn63 à âme de colophane, Ø0,8/1,0 mm, tube de 3 m, pour réparation PCB et électronique.",
   "Sn63ヤニ入り線、Ø0.8/1.0mm、3mチューブ、PCB・電子機器修理向け。",
   "Sn63 로진 코어 와이어, Ø0.8/1.0mm, 3m 튜브, PCB·전자 수리용.",
   "Kawat Sn63 inti rosin, Ø0.8/1.0mm, tabung 3m, untuk perbaikan PCB & elektronik.",
   "سلك Sn63 بقلب راتنجي، Ø0.8/1.0mm، أنبوب 3m، لإصلاح PCB والإلكترونيات."),
 "Lead-free Sn99.3Cu0.7 wire, Ø0.8/1.0mm, 3m tube, rosin flux core.": row(
   "Alambre sin plomo Sn99.3Cu0.7, Ø0.8/1.0 mm, tubo de 3 m, núcleo de flux de colofonia.",
   "Fio sem chumbo Sn99.3Cu0.7, Ø0.8/1.0 mm, tubo de 3 m, núcleo de fluxo de breu.",
   "Fil sans plomb Sn99.3Cu0.7, Ø0,8/1,0 mm, tube de 3 m, âme de flux à la colophane.",
   "無鉛Sn99.3Cu0.7線、Ø0.8/1.0mm、3mチューブ、ロジンフラックス入り。",
   "무연 Sn99.3Cu0.7 와이어, Ø0.8/1.0mm, 3m 튜브, 로진 플럭스 코어.",
   "Kawat bebas timbal Sn99.3Cu0.7, Ø0.8/1.0mm, tabung 3m, inti fluks rosin.",
   "سلك خالٍ من الرصاص Sn99.3Cu0.7، Ø0.8/1.0mm، أنبوب 3m، قلب راتنجي."),
 "Lead-free Sn99.3Cu0.7 wire, Ø1.0mm, 100g roll, rosin flux core.": row(
   "Alambre sin plomo Sn99.3Cu0.7, Ø1.0 mm, rollo de 100 g, núcleo de flux de colofonia.",
   "Fio sem chumbo Sn99.3Cu0.7, Ø1.0 mm, rolo de 100 g, núcleo de fluxo de breu.",
   "Fil sans plomb Sn99.3Cu0.7, Ø1,0 mm, bobine de 100 g, âme de flux à la colophane.",
   "無鉛Sn99.3Cu0.7線、Ø1.0mm、100gロール、ロジンフラックス入り。",
   "무연 Sn99.3Cu0.7 와이어, Ø1.0mm, 100g 롤, 로진 플럭스 코어.",
   "Kawat bebas timbal Sn99.3Cu0.7, Ø1.0mm, gulungan 100g, inti fluks rosin.",
   "سلك خالٍ من الرصاص Sn99.3Cu0.7، Ø1.0mm، لفة 100g، قلب راتنجي."),
 "Lead-free Sn99Ag0.3Cu0.7 wire, Ø0.8/1.0mm, 100g, rosin flux core.": row(
   "Alambre sin plomo Sn99Ag0.3Cu0.7, Ø0.8/1.0 mm, 100 g, núcleo de flux de colofonia.",
   "Fio sem chumbo Sn99Ag0.3Cu0.7, Ø0.8/1.0 mm, 100 g, núcleo de fluxo de breu.",
   "Fil sans plomb Sn99Ag0.3Cu0.7, Ø0,8/1,0 mm, 100 g, âme de flux à la colophane.",
   "無鉛Sn99Ag0.3Cu0.7線、Ø0.8/1.0mm、100g、ロジンフラックス入り。",
   "무연 Sn99Ag0.3Cu0.7 와이어, Ø0.8/1.0mm, 100g, 로진 플럭스 코어.",
   "Kawat bebas timbal Sn99Ag0.3Cu0.7, Ø0.8/1.0mm, 100g, inti fluks rosin.",
   "سلك خالٍ من الرصاص Sn99Ag0.3Cu0.7، Ø0.8/1.0mm، 100g، قلب راتنجي."),
 "63% tin alloy wire, Ø0.8/1.0mm, 100g roll, 2.0% rosin flux core.": row(
   "Alambre de aleación 63% estaño, Ø0.8/1.0 mm, rollo de 100 g, núcleo de flux de colofonia 2.0%.",
   "Fio de liga 63% estanho, Ø0.8/1.0 mm, rolo de 100 g, núcleo de fluxo de breu 2.0%.",
   "Fil alliage 63% étain, Ø0,8/1,0 mm, bobine de 100 g, âme de flux colophane 2,0%.",
   "63%スズ合金線、Ø0.8/1.0mm、100gロール、2.0%ロジンフラックス入り。",
   "63% 주석 합금 와이어, Ø0.8/1.0mm, 100g 롤, 2.0% 로진 플럭스 코어.",
   "Kawat paduan timah 63%, Ø0.8/1.0mm, gulungan 100g, inti fluks rosin 2.0%.",
   "سلك سبيكة قصدير 63%، Ø0.8/1.0mm، لفة 100g، قلب راتنجي 2.0%."),
 "60/40 tin-lead wire, Ø0.8/1.0mm, 50g roll, 2.0% rosin flux core.": row(
   "Alambre estaño-plomo 60/40, Ø0.8/1.0 mm, rollo de 50 g, núcleo de flux de colofonia 2.0%.",
   "Fio estanho-chumbo 60/40, Ø0.8/1.0 mm, rolo de 50 g, núcleo de fluxo de breu 2.0%.",
   "Fil étain-plomb 60/40, Ø0,8/1,0 mm, bobine de 50 g, âme de flux colophane 2,0%.",
   "60/40スズ鉛線、Ø0.8/1.0mm、50gロール、2.0%ロジンフラックス入り。",
   "60/40 주석-납 와이어, Ø0.8/1.0mm, 50g 롤, 2.0% 로진 플럭스 코어.",
   "Kawat timah-timbal 60/40, Ø0.8/1.0mm, gulungan 50g, inti fluks rosin 2.0%.",
   "سلك قصدير-رصاص 60/40، Ø0.8/1.0mm، لفة 50g، قلب راتنجي 2.0%."),
}

with open(P, encoding="utf-8") as f:
    data = json.load(f)
data.update(ENTRIES)
with open(P, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("merged %d entries -> translations_tools.json (now %d keys)" % (len(ENTRIES), len(data)))
