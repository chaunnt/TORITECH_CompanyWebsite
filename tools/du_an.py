# -*- coding: utf-8 -*-
"""Phần chung cho các trang dự án trong du-an/ (gọi từ build.py, không chạy riêng).

- ensure_images(): chụp ảnh đại diện còn thiếu (node tools/og_shots.js) + tạo thumbnail WebP cho trang hạng mục.
- inject_chrome(): chèn vào mỗi trang dự án: thẻ SEO/OG trong <head>, header chung (về trang hạng mục) đầu <body>,
  chân trang có danh sách bài cùng hạng mục trước </body>. Mỗi khối nằm giữa marker <!-- toritech:... --> nên chạy lại
  không nhân bản; nội dung artifact giữ nguyên.
- write_redirects(): trang chuyển hướng cho đường dẫn cũ (old_href trong projects.json).
"""
import os
import re
import subprocess
from html import escape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG_DIR = "assets/img/du-an"
MARKS = ("meta", "top", "foot")


def stem(w):
    return os.path.splitext(os.path.basename(w["href"]))[0]


def img_rel(w):
    return f"{IMG_DIR}/{stem(w)}.jpg"


def thumb_rel(w):
    return f"{IMG_DIR}/thumb/{stem(w)}.webp"


def ensure_images(works):
    missing = [w for w in works if not os.path.exists(os.path.join(ROOT, img_rel(w)))]
    if missing:
        subprocess.run(["node", os.path.join(ROOT, "tools/og_shots.js")], check=True, cwd=ROOT)
    from PIL import Image
    os.makedirs(os.path.join(ROOT, IMG_DIR, "thumb"), exist_ok=True)
    for w in works:
        src, dst = os.path.join(ROOT, img_rel(w)), os.path.join(ROOT, thumb_rel(w))
        if os.path.exists(src) and (not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src)):
            Image.open(src).convert("RGB").resize((640, 336), Image.LANCZOS).save(dst, "WEBP", quality=78, method=6)


def _strip(html):
    for m in MARKS:
        html = re.sub(rf"<!-- toritech:{m} -->.*?<!-- /toritech:{m} -->\n?", "", html, flags=re.S)
    return html


FIT_JS = '<script>(function(){function fit(){var W=document.documentElement.clientWidth;["tt-top","tt-foot"].forEach(function(id){var e=document.getElementById(id);if(!e)return;e.style.marginLeft="0";e.style.width="";var r=e.getBoundingClientRect();if(Math.abs(r.left)>.5||Math.abs(r.width-W)>.5){e.style.marginLeft=(-r.left)+"px";e.style.width=W+"px";e.style.maxWidth="none"}});var t=document.getElementById("tt-top");if(t){t.style.marginTop="0";var y=t.getBoundingClientRect().top+(window.scrollY||0);if(y>.5)t.style.marginTop=(-y)+"px"}}fit();addEventListener("resize",fit);addEventListener("load",fit)})();</script>'

CSS = """<style>
#tt-top,#tt-top :not(svg,svg *),#tt-foot,#tt-foot :not(svg,svg *){all:revert;box-sizing:border-box}
#tt-top{display:block;width:100%;align-self:stretch;justify-self:stretch;grid-column:1/-1;margin:0;background:#0b1426;color:#e2e8f0;font:500 14px/1.4 "Be Vietnam Pro",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;border-bottom:1px solid #1e2a44;position:relative;z-index:2147483000}
#tt-top .tt-in{max-width:1200px;margin:0 auto;padding:9px 16px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
#tt-top a{color:inherit;text-decoration:none}
#tt-top .tt-brand{display:flex;align-items:center;gap:8px;font-weight:800;letter-spacing:.04em;color:#fff}
#tt-top .tt-brand svg{width:26px;height:26px;display:block}
#tt-top .tt-crumb{flex:1;min-width:0;color:#94a3b8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:13px}
#tt-top .tt-crumb a{color:#cbd5e1}#tt-top .tt-crumb a:hover{color:#22d3ee}
#tt-top .tt-btn{display:inline-block;padding:6px 12px;border-radius:999px;border:1px solid #334155;font-size:13px;font-weight:600;white-space:nowrap}
#tt-top .tt-btn:hover{border-color:#22d3ee;color:#22d3ee}
#tt-top .tt-cta{background:#14b8a6;border-color:#14b8a6;color:#04201c}
#tt-top .tt-cta:hover{background:#2dd4bf;color:#04201c}
#tt-foot{display:block;width:100%;align-self:stretch;justify-self:stretch;grid-column:1/-1;margin:0;background:#0b1426;color:#cbd5e1;font:400 14px/1.55 "Be Vietnam Pro",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;position:relative;z-index:2}
#tt-foot .tt-in{max-width:1200px;margin:0 auto;padding:32px 16px 22px}
#tt-foot h2{margin:0 0 4px;font-size:20px;font-weight:700;color:#fff}
#tt-foot .tt-sub{margin:0 0 18px;color:#94a3b8;font-size:13.5px}
#tt-foot a{color:inherit;text-decoration:none}
#tt-foot ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:12px}
#tt-foot li{margin:0;padding:0}
#tt-foot li a{display:flex;gap:12px;align-items:flex-start;padding:10px;border:1px solid #1e2a44;border-radius:12px;background:#111c33;height:100%}
#tt-foot li a:hover{border-color:#22d3ee}
#tt-foot li img{width:112px;height:59px;object-fit:cover;border-radius:6px;flex:none;background:#1e2a44;display:block}
#tt-foot li b{display:block;color:#fff;font-size:14px;font-weight:600;line-height:1.35}
#tt-foot li small{display:block;color:#94a3b8;font-size:12px;margin-top:3px}
#tt-foot .tt-more{display:inline-block;margin-top:16px;color:#22d3ee;font-weight:600}
#tt-foot .tt-legal{margin-top:24px;padding-top:14px;border-top:1px solid #1e2a44;font-size:12.5px;color:#94a3b8;display:flex;gap:6px 16px;flex-wrap:wrap}
#tt-foot .tt-legal a:hover{color:#22d3ee}
@media print{#tt-top,#tt-foot{display:none}}
</style>"""


def _meta(w, cat_name, site_url):
    url, t, d = site_url + w["href"], escape(f'{w["title"]} – {cat_name} | TORITECH'), escape(w["desc"])
    img = site_url + img_rel(w)
    return (f'<!-- toritech:meta -->\n<meta name="description" content="{d}"><link rel="canonical" href="{url}">\n'
            f'<link rel="icon" href="../assets/img/logo.svg" type="image/svg+xml">\n'
            f'<meta property="og:type" content="article"><meta property="og:site_name" content="TORITECH"><meta property="og:locale" content="vi_VN">\n'
            f'<meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">\n'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{img}">\n'
            f'<!-- /toritech:meta -->\n')


def _top(w, cat_name, cat_page, logo):
    return (f'<!-- toritech:top -->\n{CSS}\n<div id="tt-top" role="banner"><div class="tt-in">'
            f'<a class="tt-brand" href="../index.html" aria-label="TORITECH – Trang chủ">{logo}TORITECH</a>'
            f'<nav class="tt-crumb" aria-label="Vị trí"><a href="../du-an.html">Dự án</a> / <a href="../{cat_page}">{escape(cat_name)}</a> / {escape(w["title"])}</nav>'
            f'<a class="tt-btn" href="../{cat_page}">← Về hạng mục {escape(cat_name)}</a>'
            f'<a class="tt-btn tt-cta" href="../lien-he.html">Liên hệ</a></div></div>\n<!-- /toritech:top -->\n')


def _foot(w, cat_name, cat_page, works, docs, co):
    items = []
    for o in works:
        if o is w or o["cat"] != w["cat"]:
            continue
        items.append(f'<li><a href="{os.path.basename(o["href"])}"><img src="../{thumb_rel(o)}" alt="" loading="lazy" width="112" height="59">'
                     f'<span><b>{escape(o["title"])}</b><small>{escape(o["kind"])}</small></span></a></li>')
    for d in docs:
        if d["cat"] == w["cat"]:
            items.append(f'<li><a href="../{cat_page}#ho-so"><span><b>{escape(d["title"])}</b><small>Công văn / Đề xuất · cung cấp theo yêu cầu</small></span></a></li>')
    lst = f'<ul>{"".join(items)}</ul>' if items else '<p class="tt-sub">Chưa có bài khác trong hạng mục này.</p>'
    email = f' · <a href="mailto:{co["email_support"]}">{co["email_support"]}</a>' if co["email_support"] else ""
    return (f'<!-- toritech:foot -->\n<div id="tt-foot" role="contentinfo"><div class="tt-in">'
            f'<h2>Cùng hạng mục: {escape(cat_name)}</h2><p class="tt-sub">Các dự án và hồ sơ khác của TORITECH trong hạng mục này.</p>{lst}'
            f'<a class="tt-more" href="../{cat_page}">Xem toàn bộ hạng mục {escape(cat_name)} →</a>'
            f'<div class="tt-legal"><span>© {co["legal_name"]} · MST {co["tax_id"]}</span>'
            f'<span>Hotline/Zalo <a href="tel:{co["hotline_tel"]}">{co["hotline"]}</a>{email}</span>'
            f'<a href="../index.html">Trang chủ</a><a href="../du-an.html">Tất cả dự án</a><a href="../lien-he.html">Liên hệ</a>'
            f'<a href="../chinh-sach-bao-ve-du-lieu-ca-nhan.html">Bảo vệ dữ liệu cá nhân</a></div></div></div>{FIT_JS}\n<!-- /toritech:foot -->\n')


def inject_chrome(works, docs, cats, co, site_url, logo):
    logo = logo.replace('id="lg"', 'id="tt-lg"').replace("url(#lg)", "url(#tt-lg)")
    for w in works:
        fp = os.path.join(ROOT, w["href"])
        html = _strip(open(fp, encoding="utf-8").read())
        cat_name, cat_page = cats[w["cat"]]["name"], cats[w["cat"]]["page"]
        m = re.search(r"<meta[^>]*charset[^>]*>\n?", html, flags=re.I) or re.search(r"<head[^>]*>\n?", html, flags=re.I)
        nl = "" if html[m.end() - 1] == "\n" else "\n"
        html = html[:m.end()] + nl + _meta(w, cat_name, site_url) + html[m.end():]
        m = re.search(r"<body[^>]*>\n?", html, flags=re.I)
        nl = "" if html[m.end() - 1] == "\n" else "\n"
        html = html[:m.end()] + nl + _top(w, cat_name, cat_page, logo) + html[m.end():]
        i = html.lower().rfind("</body>")
        html = html[:i] + _foot(w, cat_name, cat_page, works, docs, co) + html[i:]
        with open(fp, "w", encoding="utf-8") as f:
            f.write(html)


def write_redirects(works, site_url):
    for w in works:
        old = w.get("old_href")
        if not old:
            continue
        url, t, d = site_url + w["href"], escape(w["title"]), escape(w["desc"])
        img = site_url + img_rel(w)
        page = f'''<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8"><title>{t} | TORITECH</title>
<link rel="canonical" href="{url}"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url={url}">
<meta property="og:title" content="{t} | TORITECH"><meta property="og:description" content="{d}"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{img}">
<script>location.replace("{url}"+location.hash)</script></head><body><p>Trang đã chuyển tới <a href="{url}">{t}</a>.</p></body></html>
'''
        fp = os.path.join(ROOT, old)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(page)
