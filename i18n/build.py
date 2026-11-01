#!/usr/bin/env python3
"""
Multi-language, multi-page generator for daisysource.vip.

Site is a supply-chain portal with three English source pages:
    index.html         -> portal (home)        served at /
    lashes/index.html  -> Beauty & Lashes       served at /lashes/
    tools/index.html   -> Tools & Materials      served at /tools/

For every non-English language XX this generates the same three pages under
/XX/ :  /XX/ , /XX/lashes/ , /XX/tools/  — so switching language stays on the
same page type. The English sources are patched in place (language switcher +
hreflang block + canonical) so every language, English included, is consistent.

Translation tables (English string -> {lang: translation}):
    translations_nav.json      shared header/footer chrome, applied to every page
    translations_portal.json   portal-only strings
    translations.json          lashes-only strings  (the original table)
    translations_tools.json    tools-only strings

Run:  python3 i18n/build.py        (from the repo root)
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://daisysource.vip"

# code, native label, short code, direction
LANGS = [
    ("en", "English",           "EN", "ltr"),
    ("es", "Español",           "ES", "ltr"),
    ("pt", "Português",         "PT", "ltr"),
    ("fr", "Français",          "FR", "ltr"),
    ("ja", "日本語",             "JA", "ltr"),
    ("ko", "한국어",             "KO", "ltr"),
    ("id", "Bahasa Indonesia",  "ID", "ltr"),
    ("ar", "العربية",           "AR", "rtl"),
]

# key, source file (relative to ROOT), url sub-path, page translation table
PAGES = [
    ("portal", "index.html",        "",        "translations_portal.json"),
    ("lashes", "lashes/index.html", "lashes/", "translations.json"),
    ("tools",  "tools/index.html",  "tools/",  "translations_tools.json"),
]

RTL_CSS = """
<style>
  /* ---------- RTL (Arabic) overrides ---------- */
  body { direction: rtl; }
  .nav .right { flex-direction: row-reverse; }
  .sec-head:not(.center) { text-align: right; }
  .eyebrow, .kick { flex-direction: row-reverse; }
  .hero-stats, .hero-specs, .div-tags, .filters, .band .wrap, .foot-top, .foot, .foot-bottom { direction: rtl; }
  .svc-list li, .case-wins li { text-align: right; }
  .case-wins li { padding-left: 0; padding-right: 28px; }
  .case-wins li::before { left: auto; right: 0; }
  .tl-step:not(:last-child)::before { left: auto; right: 27px; }
  .metric { direction: rtl; }
  .cta-form input, .cta-form small { text-align: right; }
</style>
"""


def url_for(code, sub):
    """Absolute path for a page in a given language."""
    prefix = "" if code == "en" else f"/{code}"
    return f"{prefix}/{sub}"


def build_switcher(cur_code, sub):
    items = []
    for code, label, short, _ in LANGS:
        cur = ' class="is-cur"' if code == cur_code else ""
        items.append(f'        <a href="{url_for(code, sub)}"{cur} hreflang="{code}">{label}</a>')
    menu = "\n".join(items)
    cur_short = next(s for c, l, s, d in LANGS if c == cur_code)
    return (
        "<!--LANGSWITCH-->"
        '<details class="lang">'
        f'<summary aria-label="Language">{cur_short}</summary>'
        '<div class="lang-menu">\n'
        f"{menu}\n"
        "      </div></details>"
        "<!--/LANGSWITCH-->"
    )


def build_hreflang(cur_code, sub):
    lines = ["<!--I18N-ALT-->"]
    lines.append(f'<link rel="canonical" href="{BASE}{url_for(cur_code, sub)}">')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}{url_for("en", sub)}">')
    for code, *_ in LANGS:
        lines.append(f'<link rel="alternate" hreflang="{code}" href="{BASE}{url_for(code, sub)}">')
    lines.append("<!--/I18N-ALT-->")
    return "\n".join(lines)


def set_head(html, cur_code, sub):
    block = build_hreflang(cur_code, sub)
    if "<!--I18N-ALT-->" in html:
        return re.sub(r"<!--I18N-ALT-->.*?<!--/I18N-ALT-->", lambda m: block, html, flags=re.S)
    # no markers yet: replace the lone canonical link
    return re.sub(r'<link rel="canonical"[^>]*>', block, html, count=1)


def set_switcher(html, cur_code, sub):
    return re.sub(r"<!--LANGSWITCH-->.*?<!--/LANGSWITCH-->",
                  lambda m: build_switcher(cur_code, sub), html, flags=re.S)


def relink_nav(html, code):
    """Prefix internal page links with /<code> for a translated page.

    This also prefixes /tools/p/<slug>/ detail-page links, which are generated
    per language by tools/build_products.py.
    """
    html = html.replace('href="/tools/', f'href="/{code}/tools/')
    html = html.replace('href="/lashes/', f'href="/{code}/lashes/')
    html = html.replace('href="/"', f'href="/{code}/"')
    return html


def apply_table(html, table, code):
    for en, vals in sorted(table.items(), key=lambda kv: len(kv[0]), reverse=True):
        tr = vals.get(code)
        if tr:
            html = html.replace(en, tr)
    return html


def load(name):
    path = os.path.join(HERE, name)
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    nav = load("translations_nav.json")

    for key, src_rel, sub, table_name in PAGES:
        src = os.path.join(ROOT, src_rel)
        with open(src, encoding="utf-8") as f:
            html_en = f.read()

        # patch the English source in place (switcher + hreflang active = en)
        html_en = set_switcher(html_en, "en", sub)
        html_en = set_head(html_en, "en", sub)
        with open(src, "w", encoding="utf-8") as f:
            f.write(html_en)
        print(f"patched {src_rel} (en)")

        page_tbl = load(table_name)

        for code, label, short, direction in LANGS:
            if code == "en":
                continue
            html = html_en
            # translations: shared nav chrome first, then page-specific
            html = apply_table(html, nav, code)
            html = apply_table(html, page_tbl, code)
            # <html lang/dir>
            if direction == "rtl":
                html = html.replace('<html lang="en">', f'<html lang="{code}" dir="rtl">', 1)
            else:
                html = html.replace('<html lang="en">', f'<html lang="{code}">', 1)
            # internal nav links -> /<code>/...
            html = relink_nav(html, code)
            # absolute asset paths (safety; sources already absolute)
            html = html.replace('src="assets/', 'src="/assets/').replace('href="assets/', 'href="/assets/')
            # switcher + hreflang for this language/page
            html = set_switcher(html, code, sub)
            html = set_head(html, code, sub)
            # RTL stylesheet
            if direction == "rtl":
                html = html.replace("</head>", RTL_CSS + "</head>", 1)

            out_dir = os.path.join(ROOT, code, *( [sub.rstrip("/")] if sub else [] ))
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
        print(f"  generated {key}: /{{{','.join(c for c,*_ in LANGS if c!='en')}}}/{sub}")


if __name__ == "__main__":
    main()
