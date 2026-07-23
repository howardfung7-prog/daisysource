#!/usr/bin/env python3
"""
Multi-language generator for daisysource.vip.

- Source of truth: ../index.html (English).
- Injects (idempotently) into the English source: language-switcher CSS + markup,
  and hreflang alternate links.
- Generates ../<lang>/index.html for every non-English language by applying the
  translation table, switching <html lang/dir>, rewriting asset paths to absolute,
  swapping the canonical URL, marking the active language, and (for Arabic) adding
  an RTL stylesheet.

Run:  python3 i18n/build.py       (from the repo root)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "index.html")
BASE = "https://daisysource.vip"

# code, subpath, native label, short code, direction
LANGS = [
    ("en", "/",     "English",           "EN", "ltr"),
    ("es", "/es/",  "Español",           "ES", "ltr"),
    ("pt", "/pt/",  "Português",         "PT", "ltr"),
    ("fr", "/fr/",  "Français",          "FR", "ltr"),
    ("ja", "/ja/",  "日本語",             "JA", "ltr"),
    ("ko", "/ko/",  "한국어",             "KO", "ltr"),
    ("id", "/id/",  "Bahasa Indonesia",  "ID", "ltr"),
    ("ar", "/ar/",  "العربية",           "AR", "rtl"),
]

SWITCHER_CSS = """
  /* ---------- language switcher ---------- */
  .nav .right { display: flex; align-items: center; gap: 14px; }
  .lang { position: relative; }
  .lang > summary { list-style: none; cursor: pointer; font-size: 13px; font-weight: 600; color: var(--ink-soft); display: inline-flex; align-items: center; gap: 5px; padding: 8px 4px; white-space: nowrap; }
  .lang > summary::-webkit-details-marker { display: none; }
  .lang > summary::after { content: "\\25BE"; font-size: 9px; }
  .lang[open] > summary { color: var(--ink); }
  .lang-menu { position: absolute; right: 0; top: calc(100% + 6px); background: var(--white); border: 1px solid var(--line); border-radius: 12px; box-shadow: 0 18px 40px -20px rgba(80,55,25,.42); padding: 6px; min-width: 170px; z-index: 60; display: flex; flex-direction: column; }
  .lang-menu a { font-size: 14px; padding: 9px 12px; border-radius: 8px; color: var(--ink-soft); }
  .lang-menu a:hover { background: var(--cream-2); color: var(--ink); }
  .lang-menu a.is-cur { color: var(--bronze-deep); font-weight: 700; }
  [dir="rtl"] .lang-menu { right: auto; left: 0; }
"""

RTL_CSS = """
<style>
  /* ---------- RTL (Arabic) overrides ---------- */
  body { direction: rtl; }
  .sec-head:not(.center) { text-align: right; }
  .eyebrow { flex-direction: row-reverse; }
  .eyebrow::before { }
  .svc-list li, .case-wins li { text-align: right; }
  .case-wins li { padding-left: 0; padding-right: 28px; }
  .case-wins li::before { left: auto; right: 0; }
  .tl-step { grid-template-columns: 1fr 56px; }
  .tl-step:not(:last-child)::before { left: auto; right: 27px; }
  .metric { direction: rtl; }
  .cta-form input, .cta-form small { text-align: right; }
  .foot-bottom { direction: rtl; }
</style>
"""


def build_switcher(cur_code):
    items = []
    for code, path, label, short, _ in LANGS:
        cur = ' class="is-cur"' if code == cur_code else ""
        items.append(f'        <a href="{path}"{cur} hreflang="{code}">{label}</a>')
    menu = "\n".join(items)
    cur_short = next(s for c, p, l, s, d in LANGS if c == cur_code)
    return (
        "<!--LANGSWITCH-->"
        '<details class="lang">'
        f'<summary aria-label="Language">{cur_short}</summary>'
        '<div class="lang-menu">\n'
        f"{menu}\n"
        "      </div></details>"
        "<!--/LANGSWITCH-->"
    )


def build_hreflang(canonical_path):
    lines = ["<!--I18N-ALT-->"]
    lines.append(f'<link rel="canonical" href="{BASE}{canonical_path}">')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}/">')
    for code, path, *_ in LANGS:
        lines.append(f'<link rel="alternate" hreflang="{code}" href="{BASE}{path}">')
    lines.append("<!--/I18N-ALT-->")
    return "\n".join(lines)


def patch_source(html):
    """Idempotently add switcher CSS, switcher markup and hreflang block to the English source."""
    # 1) switcher CSS before </style> (first style block)
    if ".lang-menu" not in html:
        html = html.replace("</style>", SWITCHER_CSS + "</style>", 1)

    # 2) nav: wrap switcher + Get-a-Quote button in a .right container
    if "<!--LANGSWITCH-->" not in html:
        old = '    </nav>\n    <a class="btn" href="#contact">Get a Quote</a>\n  </div>'
        new = (
            "    </nav>\n"
            '    <div class="right">\n'
            "      " + build_switcher("en") + "\n"
            '      <a class="btn" href="#contact">Get a Quote</a>\n'
            "    </div>\n  </div>"
        )
        assert old in html, "nav pattern not found for switcher injection"
        html = html.replace(old, new)

    # 3) hreflang: replace the existing canonical line with the full alt block
    if "<!--I18N-ALT-->" not in html:
        old = '<link rel="canonical" href="https://daisysource.vip/">'
        assert old in html, "canonical line not found"
        html = html.replace(old, build_hreflang("/"), 1)

    return html


def make_language(html_en, code, path, direction):
    html = html_en

    # translations
    table = TRANSLATIONS
    pairs = sorted(table.items(), key=lambda kv: len(kv[0]), reverse=True)
    for en, vals in pairs:
        tr = vals.get(code)
        if tr is None:
            continue
        html = html.replace(en, tr)

    # <html lang / dir>
    if direction == "rtl":
        html = html.replace('<html lang="en">', f'<html lang="{code}" dir="rtl">', 1)
    else:
        html = html.replace('<html lang="en">', f'<html lang="{code}">', 1)

    # absolute asset paths (works from any subfolder)
    html = html.replace('src="assets/', 'src="/assets/')
    html = html.replace('href="assets/', 'href="/assets/')

    # canonical for this language
    html = html.replace(
        f'<link rel="canonical" href="{BASE}/">',
        f'<link rel="canonical" href="{BASE}{path}">', 1,
    )

    # language switcher active state
    html = re.sub(r"<!--LANGSWITCH-->.*?<!--/LANGSWITCH-->", lambda m: build_switcher(code), html, flags=re.S)

    # RTL stylesheet
    if direction == "rtl":
        html = html.replace("</head>", RTL_CSS + "</head>", 1)

    return html


def main():
    with open(os.path.join(os.path.dirname(__file__), "translations.json"), encoding="utf-8") as f:
        global TRANSLATIONS
        TRANSLATIONS = json.load(f)

    with open(SRC, encoding="utf-8") as f:
        html = f.read()

    html = patch_source(html)
    # rewrite the English source with switcher active = en
    html = re.sub(r"<!--LANGSWITCH-->.*?<!--/LANGSWITCH-->", lambda m: build_switcher("en"), html, flags=re.S)
    with open(SRC, "w", encoding="utf-8") as f:
        f.write(html)
    print("patched index.html (en)")

    for code, path, label, short, direction in LANGS:
        if code == "en":
            continue
        out = make_language(html, code, path, direction)
        d = os.path.join(ROOT, code)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(out)
        # report untranslated count
        missing = sum(1 for en, v in TRANSLATIONS.items() if code not in v)
        print(f"wrote {code}/index.html  (dir={direction}, keys missing for lang: {missing})")


if __name__ == "__main__":
    main()
