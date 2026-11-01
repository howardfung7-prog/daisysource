#!/usr/bin/env python3
"""Merge detail-page translations for the 17 added products into
translations_detail.json: product overviews (wire & SAC0307 families generated
from per-language templates, the rest hand-translated) plus the new spec keys
and descriptive spec values. Idempotent. Run: python3 i18n/_add_detail_tr.py
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "translations_detail.json")
L = ["es", "pt", "fr", "ja", "ko", "id", "ar"]
def row(*v): return dict(zip(L, v))

ENTRIES = {}

# ---------- wire family overviews (template) ----------
EN_WIRE = "KEK {alloy} solder wire with a rosin flux core, available in 0.8 mm and 1.0 mm diameters, supplied as a {size} for PCB and electronics repair and DIY soldering."
WIRE_T = {
 "es": "Alambre de soldadura KEK {alloy} con núcleo de flux de colofonia, disponible en diámetros de 0,8 mm y 1,0 mm, en {size} para reparación de PCB y electrónica y soldadura DIY.",
 "pt": "Fio de solda KEK {alloy} com núcleo de fluxo de breu, disponível em diâmetros de 0,8 mm e 1,0 mm, em {size} para reparo de PCB e eletrônica e solda DIY.",
 "fr": "Fil à souder KEK {alloy} à âme de flux à la colophane, disponible en diamètres de 0,8 mm et 1,0 mm, en {size} pour la réparation de PCB et d'électronique et la soudure DIY.",
 "ja": "KEK {alloy} はんだ線。ロジンフラックス入りで0.8mmと1.0mmの径があり、{size}。PCB・電子機器の修理やDIYはんだ付けに適しています。",
 "ko": "KEK {alloy} 땜납 와이어. 로진 플럭스 코어이며 0.8mm 및 1.0mm 직경으로 제공되고 {size}입니다. PCB·전자 수리 및 DIY 납땜에 적합합니다.",
 "id": "Kawat solder KEK {alloy} dengan inti fluks rosin, tersedia dalam diameter 0,8 mm dan 1,0 mm, dalam {size} untuk perbaikan PCB dan elektronik serta solder DIY.",
 "ar": "سلك لحام KEK {alloy} بقلب من تدفق الراتنج، متوفر بقطر 0.8 مم و1.0 مم، في {size} لإصلاح لوحات PCB والإلكترونيات واللحام اليدوي.",
}
ALLOY = {
 "Sn63": {l: "Sn63" for l in L},
 "Sn99.3Cu0.7 lead-free": row("Sn99.3Cu0.7 sin plomo","Sn99.3Cu0.7 sem chumbo","Sn99.3Cu0.7 sans plomb","Sn99.3Cu0.7 無鉛","Sn99.3Cu0.7 무연","Sn99.3Cu0.7 bebas timbal","Sn99.3Cu0.7 خالٍ من الرصاص"),
 "Sn99Ag0.3Cu0.7 lead-free": row("Sn99Ag0.3Cu0.7 sin plomo","Sn99Ag0.3Cu0.7 sem chumbo","Sn99Ag0.3Cu0.7 sans plomb","Sn99Ag0.3Cu0.7 無鉛","Sn99Ag0.3Cu0.7 무연","Sn99Ag0.3Cu0.7 bebas timbal","Sn99Ag0.3Cu0.7 خالٍ من الرصاص"),
 "63% tin": row("63% estaño","63% estanho","63% étain","63%スズ","63% 주석","timah 63%","قصدير 63%"),
 "60/40 tin-lead": row("60/40 estaño-plomo","60/40 estanho-chumbo","60/40 étain-plomb","60/40 スズ鉛","60/40 주석-납","60/40 timah-timbal","60/40 قصدير-رصاص"),
}
SIZE = {
 "50 g roll": row("rollo de 50 g","rolo de 50 g","bobine de 50 g","50gロール","50g 롤","gulungan 50g","لفة 50g"),
 "100 g roll": row("rollo de 100 g","rolo de 100 g","bobine de 100 g","100gロール","100g 롤","gulungan 100g","لفة 100g"),
 "3 m tube": row("tubo de 3 m","tubo de 3 m","tube de 3 m","3mチューブ","3m 튜브","tabung 3m","أنبوب 3m"),
}
WIRES = [("Sn63","50 g roll"),("Sn63","3 m tube"),("Sn99.3Cu0.7 lead-free","3 m tube"),
         ("Sn99.3Cu0.7 lead-free","100 g roll"),("Sn99Ag0.3Cu0.7 lead-free","100 g roll"),
         ("63% tin","100 g roll"),("60/40 tin-lead","50 g roll")]
for al, sz in WIRES:
    en = EN_WIRE.format(alloy=al, size=sz)
    ENTRIES[en] = {l: WIRE_T[l].format(alloy=ALLOY[al][l], size=SIZE[sz][l]) for l in L}

# ---------- SAC0307 family overviews (template) ----------
EN_SAC = "SAC0307 lead-free solder paste (Sn99.0 / Ag0.3 / Cu0.7) with a reflow range around 227 °C, in a {size} syringe supplied with two needles and a push rod for PCB and SMD rework."
SAC_T = {
 "es": "Pasta de soldadura sin plomo SAC0307 (Sn99.0 / Ag0.3 / Cu0.7) con un rango de reflujo en torno a 227 °C, en una jeringa de {g} g con dos agujas y un émbolo para retrabajo de PCB y SMD.",
 "pt": "Pasta de solda sem chumbo SAC0307 (Sn99.0 / Ag0.3 / Cu0.7) com faixa de refluxo em torno de 227 °C, em uma seringa de {g} g com duas agulhas e um êmbolo para retrabalho de PCB e SMD.",
 "fr": "Pâte à souder sans plomb SAC0307 (Sn99.0 / Ag0.3 / Cu0.7) avec une plage de refusion autour de 227 °C, en seringue de {g} g avec deux aiguilles et un piston pour la reprise PCB et SMD.",
 "ja": "SAC0307 無鉛ソルダーペースト（Sn99.0 / Ag0.3 / Cu0.7）。リフロー温度は約227°Cで、{g}gシリンジに針2本とプッシュロッドが付属し、PCB・SMDのやり直しに使えます。",
 "ko": "SAC0307 무연 솔더 페이스트(Sn99.0 / Ag0.3 / Cu0.7). 리플로우 온도는 약 227°C이며, 바늘 2개와 푸시로드가 포함된 {g}g 주사기로 PCB·SMD 리워크에 사용합니다.",
 "id": "Pasta solder bebas timbal SAC0307 (Sn99.0 / Ag0.3 / Cu0.7) dengan rentang reflow sekitar 227 °C, dalam jarum suntik {g} g dengan dua jarum dan push rod untuk rework PCB dan SMD.",
 "ar": "معجون لحام SAC0307 خالٍ من الرصاص (Sn99.0 / Ag0.3 / Cu0.7) بنطاق إعادة انصهار حوالي 227 °C، في حقنة {g}g مع إبرتين وقضيب دفع لإعادة عمل PCB وSMD.",
}
for g in ["50", "35", "20"]:
    en = EN_SAC.format(size=g + " g")
    ENTRIES[en] = {l: SAC_T[l].format(g=g) for l in L}

# ---------- 7 unique overviews ----------
ENTRIES["NC-559-ASM in a larger 10ml applicator, a no-clean soldering flux for BGA, PCB and SMD IC rework and general electronics repair. It wets quickly and leaves low residue, so boards can usually be used without a cleaning step."] = row(
 "NC-559-ASM en un aplicador más grande de 10 ml, un flux de soldadura sin limpieza para retrabajo de BGA, PCB y SMD y reparación electrónica general. Humecta rápido y deja poco residuo, por lo que las placas suelen poder usarse sin un paso de limpieza.",
 "NC-559-ASM em um aplicador maior de 10 ml, um fluxo de solda sem limpeza para retrabalho de BGA, PCB e SMD e reparo eletrônico geral. Molha rápido e deixa pouco resíduo, então as placas geralmente podem ser usadas sem uma etapa de limpeza.",
 "NC-559-ASM dans un applicateur plus grand de 10 ml, un flux à souder sans nettoyage pour la reprise BGA, PCB et SMD et la réparation électronique générale. Il mouille vite et laisse peu de résidu, si bien que les cartes peuvent souvent être utilisées sans nettoyage.",
 "NC-559-ASM をより大きな10mlアプリケーターに収めた無洗浄フラックス。BGA・PCB・SMD ICのやり直しや一般的な電子機器修理向けで、素早く濡れ広がり残渣が少ないため、多くの場合洗浄せずに基板を使えます。",
 "NC-559-ASM을 더 큰 10ml 어플리케이터에 담은 무세척 플럭스입니다. BGA·PCB·SMD IC 리워크와 일반 전자 수리에 적합하며, 빠르게 젖고 잔류물이 적어 대개 세척 없이 기판을 사용할 수 있습니다.",
 "NC-559-ASM dalam aplikator 10ml yang lebih besar, fluks solder no-clean untuk rework BGA, PCB, dan SMD serta perbaikan elektronik umum. Membasahi dengan cepat dan meninggalkan sedikit residu, sehingga papan biasanya bisa dipakai tanpa langkah pembersihan.",
 "NC-559-ASM في مِحقن أكبر سعة 10 مل، معجون لحام بدون تنظيف لإعادة عمل BGA وPCB وSMD وإصلاح الإلكترونيات عمومًا. يبلّل بسرعة ويترك أثرًا قليلًا، لذا يمكن عادةً استخدام اللوحات دون خطوة تنظيف.")
ENTRIES["A 30mL KEK soldering flux paste available in the popular NC-559-ASM, NC-558-ASM, RMA-223-ASM and NC-218-ASM formulas, supplied with a plunger and two tips for BGA and PCB repair. The larger volume suits busy repair benches."] = row(
 "Una pasta de flux de soldadura KEK de 30 ml disponible en las populares fórmulas NC-559-ASM, NC-558-ASM, RMA-223-ASM y NC-218-ASM, con émbolo y dos puntas para reparación de BGA y PCB. El mayor volumen conviene a bancos de reparación con mucho trabajo.",
 "Uma pasta de fluxo de solda KEK de 30 ml disponível nas populares fórmulas NC-559-ASM, NC-558-ASM, RMA-223-ASM e NC-218-ASM, com êmbolo e duas pontas para reparo de BGA e PCB. O maior volume é ideal para bancadas de reparo movimentadas.",
 "Une pâte de flux à souder KEK de 30 ml disponible dans les formules populaires NC-559-ASM, NC-558-ASM, RMA-223-ASM et NC-218-ASM, livrée avec un piston et deux embouts pour la réparation BGA et PCB. Le volume plus grand convient aux ateliers chargés.",
 "人気のNC-559-ASM・NC-558-ASM・RMA-223-ASM・NC-218-ASM処方から選べる30mlのKEKフラックスペースト。プランジャーとチップ2個が付属し、BGAやPCBの修理に使えます。容量が大きく、作業量の多い修理現場に向いています。",
 "인기 있는 NC-559-ASM, NC-558-ASM, RMA-223-ASM, NC-218-ASM 포뮬러로 제공되는 30ml KEK 플럭스 페이스트입니다. 플런저와 팁 2개가 포함되어 BGA 및 PCB 수리에 사용하며, 용량이 커 작업량이 많은 수리 현장에 적합합니다.",
 "Pasta fluks solder KEK 30ml yang tersedia dalam formula populer NC-559-ASM, NC-558-ASM, RMA-223-ASM, dan NC-218-ASM, dilengkapi plunger dan dua tip untuk perbaikan BGA dan PCB. Volume lebih besar cocok untuk meja reparasi yang sibuk.",
 "معجون لحام KEK سعة 30 مل متوفر بتركيبات شائعة NC-559-ASM وNC-558-ASM وRMA-223-ASM وNC-218-ASM، مع مكبس وطرفين لإصلاح BGA وPCB. الحجم الأكبر مناسب لطاولات الإصلاح المزدحمة.")
ENTRIES["HB-18 is a 30g rosin soldering flux paste for PCB repair, wire tinning and electronic-component soldering. The rosin base gives dependable wetting for everyday bench work while leaving minimal residue."] = row(
 "HB-18 es una pasta de flux de colofonia de 30 g para reparación de PCB, estañado de cables y soldadura de componentes electrónicos. La base de colofonia ofrece una humectación fiable para el trabajo diario dejando un residuo mínimo.",
 "HB-18 é uma pasta de fluxo de breu de 30 g para reparo de PCB, estanhagem de fios e solda de componentes eletrônicos. A base de breu oferece molhagem confiável para o trabalho diário deixando resíduo mínimo.",
 "HB-18 est une pâte de flux à la colophane de 30 g pour la réparation de PCB, l'étamage de fils et la soudure de composants électroniques. La base de colophane assure un bon mouillage au quotidien tout en laissant un résidu minimal.",
 "HB-18 は、PCB修理・線材のすず引き・電子部品のはんだ付け向けの30gロジンフラックスペースト。ロジンベースで日常作業に安定した濡れ性を与えつつ、残渣は最小限です。",
 "HB-18은 PCB 수리, 와이어 주석 도금, 전자 부품 납땜용 30g 로진 플럭스 페이스트입니다. 로진 베이스로 일상 작업에 안정적인 젖음성을 주면서 잔류물은 최소화합니다.",
 "HB-18 adalah pasta fluks rosin 30g untuk perbaikan PCB, pelapisan timah kawat, dan penyolderan komponen elektronik. Basis rosin memberi pembasahan andal untuk pekerjaan sehari-hari dengan residu minimal.",
 "HB-18 هو معجون لحام بالراتنج سعة 30g لإصلاح PCB وتقصدير الأسلاك ولحام المكونات الإلكترونية. يمنح أساس الراتنج ترطيبًا موثوقًا للعمل اليومي مع أثر ضئيل.")
ENTRIES["A box of traditional solid rosin soldering flux for PCB electronics repair, wire tinning and DIY soldering projects. Draw hot, tinned wire across the block for clean, low-cost fluxing."] = row(
 "Una caja de colofonia sólida tradicional para reparación electrónica de PCB, estañado de cables y proyectos de soldadura DIY. Pase el alambre caliente y estañado por el bloque para un fundente limpio y económico.",
 "Uma caixa de breu sólido tradicional para reparo eletrônico de PCB, estanhagem de fios e projetos de solda DIY. Passe o fio quente e estanhado pelo bloco para um fluxo limpo e econômico.",
 "Une boîte de colophane solide traditionnelle pour la réparation électronique de PCB, l'étamage de fils et les projets de soudure DIY. Passez le fil chaud et étamé sur le bloc pour un flux propre et économique.",
 "PCBの電子機器修理・線材のすず引き・DIYはんだ付け向けの、伝統的な固形ロジン（箱入り）。熱く錫めっきした線をブロックに擦り付ければ、清潔で低コストにフラックスを塗布できます。",
 "PCB 전자 수리, 와이어 주석 도금, DIY 납땜용 전통 고형 로진(박스)입니다. 뜨겁게 주석 도금한 선을 블록에 문지르면 깨끗하고 저렴하게 플럭스를 바를 수 있습니다.",
 "Kotak rosin padat tradisional untuk perbaikan elektronik PCB, pelapisan timah kawat, dan proyek solder DIY. Gesekkan kawat panas berlapis timah pada balok untuk fluks yang bersih dan hemat.",
 "علبة راتنج صلب تقليدي لإصلاح إلكترونيات PCB وتقصدير الأسلاك ومشاريع اللحام اليدوي. مرّر السلك الساخن المقصدر على الكتلة للحصول على تدفّق نظيف ومنخفض التكلفة.")
ENTRIES["KEK SAC305 solder paste (Sn96.5 / Ag3.0 / Cu0.5) with a 20-38µm powder, in a 50g jar for SMT, SMD and PCB assembly and rework. A mainstream lead-free alloy for stencil printing and reflow."] = row(
 "Pasta de soldadura KEK SAC305 (Sn96.5 / Ag3.0 / Cu0.5) con polvo de 20-38 µm, en bote de 50 g para montaje y retrabajo de SMT, SMD y PCB. Una aleación sin plomo de uso generalizado para impresión por estarcido y reflujo.",
 "Pasta de solda KEK SAC305 (Sn96.5 / Ag3.0 / Cu0.5) com pó de 20-38 µm, em pote de 50 g para montagem e retrabalho de SMT, SMD e PCB. Uma liga sem chumbo amplamente usada para impressão por estêncil e refluxo.",
 "Pâte à souder KEK SAC305 (Sn96.5 / Ag3.0 / Cu0.5) avec poudre de 20-38 µm, en pot de 50 g pour l'assemblage et la reprise SMT, SMD et PCB. Un alliage sans plomb courant pour l'impression au pochoir et la refusion.",
 "KEK SAC305 ソルダーペースト（Sn96.5 / Ag3.0 / Cu0.5）。20-38µmの粉末で、SMT・SMD・PCBの実装とやり直し向けの50gジャー入り。ステンシル印刷やリフローに使われる主流の無鉛合金です。",
 "KEK SAC305 솔더 페이스트(Sn96.5 / Ag3.0 / Cu0.5). 20-38µm 분말이며 SMT·SMD·PCB 조립 및 리워크용 50g 용기에 담겨 있습니다. 스텐실 인쇄와 리플로우에 쓰이는 대표적인 무연 합금입니다.",
 "Pasta solder KEK SAC305 (Sn96.5 / Ag3.0 / Cu0.5) dengan bubuk 20-38 µm, dalam toples 50g untuk perakitan dan rework SMT, SMD, dan PCB. Paduan bebas timbal arus utama untuk pencetakan stensil dan reflow.",
 "معجون لحام KEK SAC305 (Sn96.5 / Ag3.0 / Cu0.5) بمسحوق 20-38 ميكرون، في علبة 50g لتجميع وإعادة عمل SMT وSMD وPCB. سبيكة خالية من الرصاص شائعة لطباعة الاستنسل وإعادة الانصهار.")
ENTRIES["DP305-8010 is a 500g lead-free SAC305 solder paste (Sn96.5 / Ag3.0 / Cu0.5) with a 217-220°C reflow range, for SMT stencil printing and reflow assembly. RoHS-compliant and sized for production lines."] = row(
 "DP305-8010 es una pasta de soldadura SAC305 sin plomo de 500 g (Sn96.5 / Ag3.0 / Cu0.5) con rango de reflujo de 217-220 °C, para impresión por estarcido SMT y montaje por reflujo. Conforme a RoHS y dimensionada para líneas de producción.",
 "DP305-8010 é uma pasta de solda SAC305 sem chumbo de 500 g (Sn96.5 / Ag3.0 / Cu0.5) com faixa de refluxo de 217-220 °C, para impressão por estêncil SMT e montagem por refluxo. Conforme RoHS e dimensionada para linhas de produção.",
 "DP305-8010 est une pâte à souder SAC305 sans plomb de 500 g (Sn96.5 / Ag3.0 / Cu0.5) avec une plage de refusion de 217-220 °C, pour l'impression au pochoir SMT et l'assemblage par refusion. Conforme RoHS et dimensionnée pour les lignes de production.",
 "DP305-8010 は、217-220°Cのリフロー範囲を持つ500gの無鉛SAC305ソルダーペースト（Sn96.5 / Ag3.0 / Cu0.5）。SMTステンシル印刷とリフロー実装向けで、RoHS準拠、生産ライン向けの容量です。",
 "DP305-8010은 217-220°C 리플로우 범위를 가진 500g 무연 SAC305 솔더 페이스트(Sn96.5 / Ag3.0 / Cu0.5)입니다. SMT 스텐실 인쇄와 리플로우 조립용이며 RoHS를 준수하고 생산 라인에 맞는 용량입니다.",
 "DP305-8010 adalah pasta solder SAC305 bebas timbal 500g (Sn96.5 / Ag3.0 / Cu0.5) dengan rentang reflow 217-220 °C, untuk pencetakan stensil SMT dan perakitan reflow. Memenuhi RoHS dan berukuran untuk lini produksi.",
 "DP305-8010 هو معجون لحام SAC305 خالٍ من الرصاص بوزن 500g (Sn96.5 / Ag3.0 / Cu0.5) بنطاق إعادة انصهار 217-220 °C، لطباعة استنسل SMT والتجميع بإعادة الانصهار. متوافق مع RoHS وبحجم مناسب لخطوط الإنتاج.")
ENTRIES["A 500g tub of Sn63/Pb37 (6337) leaded solder paste for PCB, SMT, BGA and IC electronics repair and rework. The classic eutectic alloy offers a low, forgiving melting point and reliable joints; bulk size for production use."] = row(
 "Un bote de 500 g de pasta de soldadura con plomo Sn63/Pb37 (6337) para reparación y retrabajo de PCB, SMT, BGA e IC. La clásica aleación eutéctica ofrece un punto de fusión bajo y tolerante y uniones fiables; tamaño a granel para producción.",
 "Um pote de 500 g de pasta de solda com chumbo Sn63/Pb37 (6337) para reparo e retrabalho de PCB, SMT, BGA e IC. A clássica liga eutética oferece ponto de fusão baixo e tolerante e juntas confiáveis; tamanho a granel para produção.",
 "Un pot de 500 g de pâte à souder au plomb Sn63/Pb37 (6337) pour la réparation et la reprise PCB, SMT, BGA et IC. L'alliage eutectique classique offre un point de fusion bas et tolérant et des joints fiables ; format en vrac pour la production.",
 "PCB・SMT・BGA・ICの修理ややり直し向けの、有鉛Sn63/Pb37（6337）ソルダーペースト500gボトル。古典的な共晶合金で融点が低く扱いやすく、接合も安定。量産向けの大容量です。",
 "PCB·SMT·BGA·IC 수리 및 리워크용 유연 Sn63/Pb37(6337) 솔더 페이스트 500g 통입니다. 고전적인 공정 합금으로 융점이 낮아 다루기 쉽고 접합이 안정적이며, 양산용 대용량입니다.",
 "Wadah 500g pasta solder bertimbal Sn63/Pb37 (6337) untuk perbaikan dan rework PCB, SMT, BGA, dan IC. Paduan eutektik klasik menawarkan titik leleh rendah yang mudah diatur dan sambungan andal; ukuran besar untuk produksi.",
 "علبة 500g من معجون لحام بالرصاص Sn63/Pb37 (6337) لإصلاح وإعادة عمل PCB وSMT وBGA وIC. تقدّم السبيكة اليوتكتيكية الكلاسيكية نقطة انصهار منخفضة ومتسامحة ووصلات موثوقة؛ حجم كبير للإنتاج.")

# ---------- new spec keys ----------
ENTRIES["<td>Brand</td>"] = row("<td>Marca</td>","<td>Marca</td>","<td>Marque</td>","<td>ブランド</td>","<td>브랜드</td>","<td>Merek</td>","<td>العلامة التجارية</td>")
ENTRIES["<td>Powder</td>"] = row("<td>Polvo</td>","<td>Pó</td>","<td>Poudre</td>","<td>粉末</td>","<td>분말</td>","<td>Bubuk</td>","<td>المسحوق</td>")

# ---------- new descriptive spec values ----------
def tdval(en, *vals):
    ENTRIES["<td>%s</td>" % en] = {l: "<td>%s</td>" % v for l, v in zip(L, vals)}

tdval("No-clean flux","Flux sin limpieza","Fluxo sem limpeza","Flux sans nettoyage","無洗浄フラックス","무세척 플럭스","Fluks no-clean","معجون بدون تنظيف")
tdval("Lead-free solder paste","Pasta de soldadura sin plomo","Pasta de solda sem chumbo","Pâte à souder sans plomb","無鉛ソルダーペースト","무연 솔더 페이스트","Pasta solder bebas timbal","معجون لحام خالٍ من الرصاص")
tdval("Leaded solder paste","Pasta de soldadura con plomo","Pasta de solda com chumbo","Pâte à souder au plomb","有鉛ソルダーペースト","유연 솔더 페이스트","Pasta solder bertimbal","معجون لحام بالرصاص")
tdval("Solid rosin","Colofonia sólida","Breu sólido","Colophane solide","固形ロジン","고형 로진","Rosin padat","راتنج صلب")
tdval("Block (boxed)","Bloque (en caja)","Bloco (em caixa)","Bloc (en boîte)","ブロック（箱入り）","블록 (박스)","Balok (dalam kotak)","كتلة (معلبة)")
tdval("Jar","Bote","Pote","Pot","ジャー","용기","Toples","علبة")
tdval("1 x flux + plunger + tips","1 × flux + émbolo + puntas","1 × fluxo + êmbolo + pontas","1 × flux + piston + embouts","フラックス1本＋プランジャー＋チップ","플럭스 1개 + 플런저 + 팁","1 × fluks + plunger + tip","1 × معجون + مكبس + أطراف")
tdval("Flux + plunger + 2 tips","Flux + émbolo + 2 puntas","Fluxo + êmbolo + 2 pontas","Flux + piston + 2 embouts","フラックス＋プランジャー＋チップ2個","플럭스 + 플런저 + 팁 2개","Fluks + plunger + 2 tip","معجون + مكبس + طرفان")
tdval("Syringe + 2 needles + push rod","Jeringa + 2 agujas + émbolo","Seringa + 2 agulhas + êmbolo","Seringue + 2 aiguilles + piston","シリンジ＋針2本＋プッシュロッド","주사기 + 바늘 2개 + 푸시로드","Jarum suntik + 2 jarum + push rod","حقنة + إبرتان + قضيب دفع")
tdval("BGA / PCB repair","Reparación de BGA / PCB","Reparo de BGA / PCB","Réparation BGA / PCB","BGA・PCB修理","BGA·PCB 수리","Perbaikan BGA / PCB","إصلاح BGA / PCB")
tdval("PCB repair / tinning / soldering","Reparación de PCB / estañado / soldadura","Reparo de PCB / estanhagem / solda","Réparation PCB / étamage / soudure","PCB修理・すず引き・はんだ付け","PCB 수리 / 주석 도금 / 납땜","Perbaikan PCB / pelapisan timah / solder","إصلاح PCB / تقصدير / لحام")
tdval("Wire tinning / general soldering","Estañado de cables / soldadura general","Estanhagem de fios / solda geral","Étamage de fils / soudure générale","線材のすず引き・一般はんだ付け","와이어 주석 도금 / 일반 납땜","Pelapisan timah kawat / solder umum","تقصدير الأسلاك / لحام عام")
tdval("SMT / PCB assembly &amp; rework","Montaje SMT / PCB y retrabajo","Montagem SMT / PCB e retrabalho","Assemblage SMT / PCB et reprise","SMT・PCB実装とやり直し","SMT / PCB 조립 및 리워크","Perakitan SMT / PCB &amp; rework","تجميع SMT / PCB وإعادة العمل")
tdval("SMT stencil printing / reflow","Impresión por estarcido SMT / reflujo","Impressão por estêncil SMT / refluxo","Impression au pochoir SMT / refusion","SMTステンシル印刷・リフロー","SMT 스텐실 인쇄 / 리플로우","Pencetakan stensil SMT / reflow","طباعة استنسل SMT / إعادة الانصهار")
tdval("PCB / SMT / BGA / IC rework","Retrabajo de PCB / SMT / BGA / IC","Retrabalho de PCB / SMT / BGA / IC","Reprise PCB / SMT / BGA / IC","PCB・SMT・BGA・ICのやり直し","PCB / SMT / BGA / IC 리워크","Rework PCB / SMT / BGA / IC","إعادة عمل PCB / SMT / BGA / IC")
tdval("PCB / electronics soldering","Soldadura de PCB / electrónica","Solda de PCB / eletrônica","Soudure PCB / électronique","PCB・電子機器のはんだ付け","PCB / 전자 납땜","Solder PCB / elektronik","لحام PCB / الإلكترونيات")
tdval("Rosin flux (2.2%)","Flux de colofonia (2,2%)","Fluxo de breu (2,2%)","Flux colophane (2,2%)","ロジンフラックス（2.2%）","로진 플럭스 (2.2%)","Fluks rosin (2,2%)","تدفق راتنجي (2.2%)")
tdval("Rosin flux (2.0%)","Flux de colofonia (2,0%)","Fluxo de breu (2,0%)","Flux colophane (2,0%)","ロジンフラックス（2.0%）","로진 플럭스 (2.0%)","Fluks rosin (2,0%)","تدفق راتنجي (2.0%)")
tdval("3 m (tube)","3 m (tubo)","3 m (tubo)","3 m (tube)","3m（チューブ）","3m (튜브)","3 m (tabung)","3m (أنبوب)")
tdval("Sn99.3Cu0.7 (lead-free)","Sn99.3Cu0.7 (sin plomo)","Sn99.3Cu0.7 (sem chumbo)","Sn99.3Cu0.7 (sans plomb)","Sn99.3Cu0.7（無鉛）","Sn99.3Cu0.7 (무연)","Sn99.3Cu0.7 (bebas timbal)","Sn99.3Cu0.7 (خالٍ من الرصاص)")
tdval("Sn99Ag0.3Cu0.7 (lead-free)","Sn99Ag0.3Cu0.7 (sin plomo)","Sn99Ag0.3Cu0.7 (sem chumbo)","Sn99Ag0.3Cu0.7 (sans plomb)","Sn99Ag0.3Cu0.7（無鉛）","Sn99Ag0.3Cu0.7 (무연)","Sn99Ag0.3Cu0.7 (bebas timbal)","Sn99Ag0.3Cu0.7 (خالٍ من الرصاص)")
tdval("63% tin","63% estaño","63% estanho","63% étain","63%スズ","63% 주석","Timah 63%","قصدير 63%")

with open(P, encoding="utf-8") as f:
    data = json.load(f)
data.update(ENTRIES)
with open(P, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("merged %d detail entries (now %d keys)" % (len(ENTRIES), len(data)))
