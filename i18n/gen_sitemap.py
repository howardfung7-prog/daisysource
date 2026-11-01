#!/usr/bin/env python3
"""Generate sitemap.xml for the multilingual supply-chain site.

Mirrors the live structure produced by build.py / build_products.py:
    portal   ""            (/, /{lang}/)
    lashes   "lashes/"
    tools    "tools/"
    product  "tools/p/<slug>/"   (one per catalog product)

Each URL lists hreflang alternates for all languages (x-default = English).
Run from repo root:  python3 i18n/gen_sitemap.py
"""
import glob, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://daisysource.vip"
LANGS = ["en", "es", "pt", "fr", "ja", "ko", "id", "ar"]
TODAY = datetime.date.today().isoformat()


def url_for(code, sub):
    prefix = "" if code == "en" else f"/{code}"
    return f"{BASE}{prefix}/{sub}"


def product_subs():
    slugs = sorted(
        os.path.basename(p.rstrip("/"))
        for p in glob.glob(os.path.join(ROOT, "tools", "p", "*/"))
    )
    return [f"tools/p/{s}/" for s in slugs]


# (sub-path, priority)
PAGES = [("", "1.0"), ("lashes/", "0.8"), ("tools/", "0.8")]
PAGES += [(s, "0.6") for s in product_subs()]


def url_block(code, sub, priority):
    lines = [f"  <url>", f"    <loc>{url_for(code, sub)}</loc>"]
    lines.append(
        f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url_for("en", sub)}"/>'
    )
    for lc in LANGS:
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="{lc}" href="{url_for(lc, sub)}"/>'
        )
    lines.append(f"    <lastmod>{TODAY}</lastmod>")
    lines.append(f"    <changefreq>weekly</changefreq>")
    lines.append(f"    <priority>{priority}</priority>")
    lines.append("  </url>")
    return "\n".join(lines)


def main():
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for sub, pr in PAGES:
        for code in LANGS:
            out.append(url_block(code, sub, pr))
    out.append("</urlset>")
    out.append("")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"wrote sitemap.xml: {len(PAGES)} page types x {len(LANGS)} langs = "
          f"{len(PAGES) * len(LANGS)} urls")


if __name__ == "__main__":
    main()
