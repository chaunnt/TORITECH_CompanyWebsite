# -*- coding: utf-8 -*-
"""Sinh toàn bộ site tĩnh TORITECH (HTML5) ra thư mục gốc repo.
Chạy: python3 tools/build.py
"""
import json
import os
import sys
from html import escape

sys.path.insert(0, os.path.dirname(__file__))
from site_config import SITE_URL, COMPANY, EFFECTIVE, VERSION  # noqa: E402
import legal  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CO = COMPANY


def email_or(v, label="Đang cập nhật"):
    return f'<a href="mailto:{v}">{v}</a>' if v else f"<span>{label}</span>"


# ---------------------------------------------------------------- icons
I = {
    "eye": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
    "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M8 14h2M14 14h2M8 18h2"/></svg>',
    "ai": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="7" width="10" height="10" rx="2"/><path d="M10 1v3M14 1v3M10 20v3M14 20v3M20 10h3M20 14h3M1 10h3M1 14h3"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>',
    "share": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/></svg>',
    "print": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>',
    "video": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="14" height="14" rx="2"/><path d="M22 8l-6 4 6 4V8z"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h8M8 9h2"/></svg>',
    "arrow": "→",
}
LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#22d3ee"/><stop offset="1" stop-color="#14b8a6"/></linearGradient></defs>'
        '<path d="M20 3l15 8.5v17L20 37 5 28.5v-17z" fill="url(#lg)"/><path d="M20 3l15 8.5L20 20 5 11.5z" fill="#a5f3fc" opacity=".55"/>'
        '<path d="M13 15h14M20 15v13" stroke="#062029" stroke-width="3.2" stroke-linecap="round"/></svg>')


def tools_bar(video=None, video_name=None, share_url=None, title=None, print_btn=True):
    out = ['<div class="toolbar no-print-inner">']
    attr = f' data-share-url="{share_url}"' if share_url else ""
    attr += f' data-share-title="{escape(title)}"' if title else ""
    out.append(f'<button class="tool" type="button" data-share{attr}>{I["share"]}Chia sẻ</button>')
    if print_btn:
        out.append(f'<button class="tool" type="button" data-print>{I["print"]}In / PDF</button>')
    if video:
        nm = f' data-video-name="{video_name}"' if video_name else ""
        tt = f' data-video-title="{escape(title)}"' if title else ""
        out.append(f'<button class="tool" type="button" data-video="{video}"{nm}{tt}>{I["video"]}Xuất MP4</button>')
    out.append("</div>")
    return "".join(out)


# ---------------------------------------------------------------- navigation
# Hạng mục: mọi dự án phải thuộc 1 hạng mục. page = trang hạng mục; solution = trang giải pháp (nếu có)
CATS = {
    "vision": {"name": "AI Vision & VMS", "cls": "v", "page": "du-an-ai-vision-vms.html", "solution": "ai-vision-vms.html",
               "lead": "Giám sát bằng camera AI, quản lý video tập trung (VMS) và dữ liệu đăng kiểm, giao thông đô thị."},
    "booking": {"name": "Đặt lịch & Điều phối", "cls": "b", "page": "du-an-dat-lich.html", "solution": "dat-lich.html",
                "lead": "Đặt lịch hẹn quy mô lớn, điều phối dịch vụ, kiểm định, thanh toán và danh bạ cơ sở dịch vụ."},
    "mcp": {"name": "MCP & AI Agent", "cls": "m", "page": "du-an-mcp-ai-agent.html", "solution": "mcp.html",
            "lead": "AI Agent kết nối hệ thống qua Model Context Protocol (MCP): dịch vụ công, văn thư, vận hành doanh nghiệp."},
    "game": {"name": "Game & Giải trí", "cls": "g", "page": "du-an-game-giai-tri.html", "solution": None,
             "lead": "Game và ứng dụng giải trí chạy trực tiếp trên trình duyệt do TORITECH phát triển."},
}

NAV = [
    ("Giải pháp", [
        ("ai-vision-vms.html", "AI Camera Vision & VMS", "Thị giác máy tính, giám sát tập trung"),
        ("dat-lich.html", "Nền tảng Đặt lịch & Điều phối", "Chịu tải cao, đa kênh, chống nghẽn"),
        ("mcp.html", "Hệ sinh thái MCP & AI Agent", "Dịch vụ công · Doanh nghiệp · Nhân sự"),
    ]),
    ("Dự án", [("du-an.html", "Tất cả dự án & mô hình", "Toàn bộ theo hạng mục")] + [(c["page"], c["name"], c["lead"].split(":")[0].split(",")[0]) for c in CATS.values()]),
    ("trust-center.html", "Bảo mật & Tuân thủ"),
    ("tai-lieu.html", "Tài liệu kỹ thuật"),
    ("ve-chung-toi.html", "Về chúng tôi"),
]
LEGAL_LINKS = [
    ("dieu-khoan-su-dung.html", "Điều khoản sử dụng"),
    ("chinh-sach-bao-ve-du-lieu-ca-nhan.html", "Chính sách bảo vệ dữ liệu cá nhân"),
    ("chinh-sach-bao-mat-ai-mcp.html", "Chính sách bảo mật AI & MCP"),
    ("mien-tru-trach-nhiem-dich-vu-cong.html", "Miễn trừ trách nhiệm dữ liệu dịch vụ công"),
    ("thoa-thuan-xu-ly-du-lieu-dpa.html", "Thỏa thuận xử lý dữ liệu (DPA)"),
    ("cam-ket-chat-luong-sla.html", "Cam kết chất lượng dịch vụ (SLA)"),
    ("chinh-sach-thanh-toan-hoan-huy.html", "Chính sách thanh toán & hoàn huỷ"),
    ("chinh-sach-cookie.html", "Chính sách Cookie"),
]


def header(active):
    items = []
    for it in NAV:
        if isinstance(it[1], list):
            subs = "".join(f'<a href="{h}"><b>{t}</b><span>{d}</span></a>' for h, t, d in it[1])
            cur = any(active == h for h, _, _ in it[1])
            items.append(f'<li class="has-sub"><button type="button" aria-expanded="false"{" aria-current=page" if cur else ""}>{it[0]} ▾</button><div class="sub">{subs}</div></li>')
        else:
            cur = ' aria-current="page"' if active == it[0] else ""
            items.append(f'<li><a href="{it[0]}"{cur}>{it[1]}</a></li>')
    return f'''<a class="skip" href="#main">Bỏ qua điều hướng</a>
<header class="site-header"><div class="wrap hdr">
<a class="brand" href="index.html" aria-label="TORITECH – Trang chủ">{LOGO}<span>TORITECH<small>AI VISION · BOOKING · MCP</small></span></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav">☰</button>
<nav class="site-nav" id="nav" aria-label="Điều hướng chính"><ul>{"".join(items)}</ul>
<a class="btn btn-primary btn-sm nav-cta" href="lien-he.html">Liên hệ tư vấn</a></nav>
</div></header>'''


def footer():
    legal_li = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in LEGAL_LINKS)
    return f'''<footer class="site-footer"><div class="wrap">
<div class="foot">
 <div class="entity"><a class="brand" href="index.html">{LOGO}<span>TORITECH</span></a><br>
  <p><b>{CO["legal_name"]}</b></p>
  <p>MST: {CO["tax_id"]} · cấp ngày {CO["tax_date"]}</p>
  <p>Người đại diện theo pháp luật: {CO["rep"]}</p>
  <p>Trụ sở: {CO["address"]}</p>
  <p>Hotline: <a href="tel:{CO["hotline_tel"]}">{CO["hotline"]}</a> · Zalo: <a href="https://zalo.me/{CO["zalo"]}" rel="noopener">{CO["hotline"]}</a></p>
  <p>Hỗ trợ kỹ thuật: {email_or(CO["email_support"])}</p>
  <p>Báo cáo bảo mật: {email_or(CO["email_security"], "qua hotline / trang Trust Center")}</p>
 </div>
 <div><h4>Sản phẩm</h4><ul>
  <li><a href="ai-vision-vms.html">AI Camera &amp; VMS</a></li><li><a href="dat-lich.html">Hệ thống Đặt lịch</a></li>
  <li><a href="mcp.html#dvc">MCP Dịch vụ công</a></li><li><a href="mcp.html#doanh-nghiep">MCP Doanh nghiệp</a></li><li><a href="mcp.html#nhan-su">MCP Nhân sự</a></li>
  <li><a href="du-an.html">Dự án &amp; Mô hình</a></li></ul></div>
 <div><h4>Tài nguyên</h4><ul>
  <li><a href="tai-lieu.html#api">Tài liệu API / MCP</a></li><li><a href="tai-lieu.html#kien-truc">Kiến trúc hệ thống</a></li>
  <li><a href="tai-lieu.html#trang-thai">Trạng thái dịch vụ</a></li><li><a href="tai-lieu.html#faq">Câu hỏi thường gặp</a></li>
  <li><a href="ho-so-nang-luc.html">Hồ sơ năng lực</a></li><li><a href="trust-center.html">Trust Center</a></li></ul></div>
 <div><h4>Pháp lý &amp; Chính sách</h4><ul>{legal_li}</ul></div>
</div>
<div class="legal-strip"><span>© <span data-year>2026</span> {CO["legal_name"]}. Bảo lưu mọi quyền.</span>
<nav aria-label="Pháp lý"><a href="dieu-khoan-su-dung.html">Điều khoản</a><a href="chinh-sach-bao-ve-du-lieu-ca-nhan.html">Bảo vệ dữ liệu cá nhân</a><a href="chinh-sach-cookie.html">Cookie</a><button type="button" class="tool" style="padding:2px 10px;font-size:.78rem" data-cookie-reset>Tuỳ chọn cookie</button><a href="llms.txt">llms.txt</a></nav></div>
</div></footer>'''


OVERLAYS = '''<div class="overlay" id="share-sheet" hidden><div class="sheet-panel" role="dialog" aria-modal="true" aria-labelledby="sh-t" tabindex="-1">
<h3 id="sh-t">Chia sẻ trang này <button class="x" type="button" data-close aria-label="Đóng">×</button></h3>
<div class="nets">
<a data-net="facebook" href="#" rel="noopener"><i style="background:#1877f2">f</i>Facebook</a>
<button type="button" data-zalo><i style="background:#0068ff">Z</i>Zalo</button>
<a data-net="linkedin" href="#" rel="noopener"><i style="background:#0a66c2">in</i>LinkedIn</a>
<a data-net="x" href="#" rel="noopener"><i style="background:#0f1419">X</i>X / Twitter</a>
<a data-net="telegram" href="#" rel="noopener"><i style="background:#229ed9">✈</i>Telegram</a>
<a data-net="email" href="#"><i style="background:#475569">@</i>Email</a>
<button type="button" data-copy><i style="background:#0e7490">⧉</i>Sao chép</button>
<button type="button" data-share-native hidden><i style="background:#14b8a6">↗</i>Khác…</button>
</div>
<div class="copyrow"><input id="share-url" readonly aria-label="Liên kết"><button class="btn btn-dark btn-sm" type="button" data-copy>Sao chép</button></div>
</div></div>
<div class="overlay" id="video-modal" hidden data-state="rec"><div class="sheet-panel" role="dialog" aria-modal="true" aria-labelledby="vm-t" tabindex="-1">
<h3 id="vm-t">Xuất video MP4 <button class="x" type="button" data-close aria-label="Đóng">×</button></h3>
<div data-show="rec"><p>Đang dựng video 1280×720 từ hoạ tiết 2.5D (vấn đề → giải pháp). Vui lòng giữ tab này mở.</p>
<div class="vm-bar"><i></i></div><p class="vm-note"><span class="vm-pct">0%</span> · video được tạo ngay trên trình duyệt của bạn, không tải lên máy chủ.</p>
<button class="btn btn-ghost btn-sm" type="button" data-cancel>Huỷ</button></div>
<div data-show="done"><video controls playsinline muted></video><p class="vm-note"></p>
<div class="actions"><a class="btn btn-primary" data-dl href="#">Tải video</a><button class="btn btn-dark" type="button" data-share-video hidden>Chia sẻ video</button></div></div>
<div data-show="err"><p class="vm-err"></p><button class="btn btn-dark btn-sm" type="button" data-close>Đóng</button></div>
</div></div>
<div id="cookie-banner" hidden role="region" aria-label="Thông báo cookie"><p>Website chỉ dùng cookie/bộ nhớ trình duyệt <b>thiết yếu</b> (ghi nhớ lựa chọn này). Chúng tôi không cài mã theo dõi quảng cáo. <a href="chinh-sach-cookie.html">Tìm hiểu thêm</a></p>
<div class="actions"><button class="btn btn-ghost btn-sm" type="button" data-cookie="essential">Chỉ thiết yếu</button><button class="btn btn-primary btn-sm" type="button" data-cookie="all">Đồng ý</button></div></div>'''


def org_jsonld():
    return {
        "@context": "https://schema.org", "@type": "Organization", "name": CO["short"], "legalName": CO["legal_name"],
        "url": SITE_URL, "logo": SITE_URL + "assets/img/logo.svg", "taxID": CO["tax_id"], "telephone": CO["hotline_tel"],
        "address": {"@type": "PostalAddress", "streetAddress": "139/21/2A Thạnh Lộc 27, Khu phố 3C, Phường An Phú Đông", "addressLocality": "Thành phố Hồ Chí Minh", "addressCountry": "VN"},
        "founder": {"@type": "Person", "name": CO["rep"]},
    }


def layout(path, title, desc, body, active=None, jsonld=None, scenes=True, dark_hero=True, og_image=None):
    og = og_image or SITE_URL + "assets/img/og.png"
    url = SITE_URL + ("" if path == "index.html" else path)
    ld = [org_jsonld()] + (jsonld or [])
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    full_title = title if path == "index.html" else f"{title} | TORITECH"
    scripts = '<script src="assets/js/scenes.js" defer></script>' if scenes else ""
    cfg = json.dumps({"email": CO["email_support"], "zalo": CO["zalo"]})
    return f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0b1426">
<meta property="og:type" content="website"><meta property="og:site_name" content="TORITECH">
<meta property="og:title" content="{escape(full_title)}"><meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="vi_VN">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(full_title)}"><meta name="twitter:description" content="{escape(desc)}"><meta name="twitter:image" content="{og}">
<link rel="icon" href="assets/img/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
{ld_html}
<script>window.TORI_CFG={cfg};</script>
</head>
<body>
{header(active or path)}
<main id="main">
{body}
</main>
{footer()}
{OVERLAYS}
{scripts}
<script src="assets/js/site.js" defer></script>
</body>
</html>
'''


def page_hero(crumb, eyebrow, h1, lead, extra="", video=None, title=None):
    return f'''<section class="dark page-hero"><div class="wrap">
<div class="crumbs"><a href="index.html">Trang chủ</a> / {crumb}</div>
<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lead">{lead}</p>{extra}
{tools_bar(video=video, title=title or h1)}
</div></section>'''


def scene_block(key, anchor, title, problem, solution, bullets=None, flip=False, page="index.html", auto=False):
    bl = "".join(f"<li>{b}</li>" for b in (bullets or []))
    bl = f'<ul class="check" style="margin-bottom:16px">{bl}</ul>' if bl else ""
    return f'''<article class="scene{" flip" if flip else ""} reveal" id="{anchor}" data-scene-root data-state="solution">
<div class="scene-stage"><canvas data-scene="{key}"{" data-auto" if auto else ""} role="img" aria-label="Minh hoạ 2.5D: {escape(title)} – vấn đề và giải pháp"></canvas></div>
<div class="scene-copy"><h3>{title}</h3>
<div class="seg" role="group" aria-label="Chế độ minh hoạ"><button type="button" data-scene-toggle="problem" aria-pressed="false">Vấn đề</button><button type="button" data-scene-toggle="solution" aria-pressed="true">Giải pháp</button></div>
<div class="ps"><div class="p"><b>Vấn đề</b>{problem}</div><div class="s"><b>Giải pháp TORITECH</b>{solution}</div></div>
{bl}
{tools_bar(video=key, video_name="toritech-" + anchor, share_url=page + "#" + anchor, title=title, print_btn=False)}
</div></article>'''


def cta_band(h="Sẵn sàng đánh giá giải pháp cho đơn vị của bạn?", p="Đặt lịch demo 30 phút với kỹ sư giải pháp, hoặc nhận hồ sơ năng lực và tiêu chuẩn kỹ thuật để thẩm định."):
    return f'''<section><div class="wrap"><div class="band reveal"><div><h2>{h}</h2><p>{p}</p></div>
<div class="actions"><a class="btn btn-dark" href="lien-he.html?topic=demo">Đặt lịch Demo</a><a class="btn btn-ghost" style="color:#fff;border-color:rgba(255,255,255,.5)" href="ho-so-nang-luc.html">Hồ sơ năng lực</a></div></div></div></section>'''


# ---------------------------------------------------------------- dự án (tools/projects.json)
import du_an  # noqa: E402

with open(os.path.join(os.path.dirname(__file__), "projects.json"), encoding="utf-8") as _f:
    _PRJ = json.load(_f)
WORKS = _PRJ["works"]   # trang dự án HTML trong du-an/
DOCS = []  # công văn/đề xuất là tài liệu cơ mật: KHÔNG đăng lên website (chủ sở hữu 20/11/2026)
for _x in WORKS + DOCS:
    if _x.get("cat") not in CATS:
        raise SystemExit(f'projects.json: "{_x.get("title")}" thiếu hạng mục hợp lệ (cat ∈ {list(CATS)})')


def work_card(w):
    c = CATS[w["cat"]]
    return f'''<article class="work reveal" data-cat="{w["cat"]}">
<a class="thumb" href="{w["href"]}"><span class="tag {c["cls"]}">{c["name"]}</span><img src="{du_an.thumb_rel(w)}" alt="Ảnh trang {escape(w["title"])}" loading="lazy" decoding="async" width="640" height="336"></a>
<div class="body"><span class="tag d" style="align-self:flex-start">{w["kind"]}</span><h3><a href="{w["href"]}">{w["title"]}</a></h3><p>{w["desc"]}</p>
<div class="meta"><a class="btn btn-dark btn-sm" href="{w["href"]}">Xem dự án →</a>
<button class="tool" type="button" data-share data-share-url="{w["href"]}" data-share-title="{escape(w["title"])}">{I["share"]}Chia sẻ</button></div></div></article>'''


def doc_card(d):
    c = CATS[d["cat"]]
    return f'''<article class="work reveal" data-cat="{d["cat"]}">
<div class="thumb"><span class="tag {c["cls"]}">{c["name"]}</span><div class="doc-thumb"><div>{I["doc"]}<b>Hồ sơ đề xuất gửi cơ quan quản lý</b></div></div></div>
<div class="body"><span class="tag d" style="align-self:flex-start">Công văn / Đề xuất</span><h3>{d["title"]}</h3><p>{d["desc"]}</p>
<div class="meta"><a class="btn btn-dark btn-sm" href="lien-he.html?topic=hoso">Yêu cầu bản đầy đủ</a></div></div></article>'''


def cat_cards(cat):
    return "".join(work_card(w) for w in WORKS if w["cat"] == cat), "".join(doc_card(d) for d in DOCS if d["cat"] == cat)


INTEGRATIONS = [
    ("Camera IP · ONVIF / RTSP", "đa hãng"), ("Đầu ghi NVR", "chuẩn QCVN 103:2024/BGTVT"),
    ("Ví điện tử", "các ví điện tử phổ biến"), ("Ngân hàng", "app ngân hàng số, cổng thanh toán"),
    ("Thu phí tự động", "ví thu phí ETC"), ("Hoá đơn điện tử", "theo NĐ 123/2020/NĐ-CP"),
    ("Thông báo đa kênh", "Zalo OA/ZNS, SMS, Email, Push"), ("LLM", "Claude, ChatGPT, Gemini, Copilot"),
    ("Lưu trữ & văn phòng", "Google Drive, OneDrive, Excel, Gmail, Outlook"), ("Dịch vụ công", "Cổng BHXH, cổng thuế, ứng dụng giao thông"),
]


def integrations_html():
    return ('<div class="logos">' + "".join(f"<span>{a}<em>{b}</em></span>" for a, b in INTEGRATIONS) + "</div>"
            '<p class="meta-line" style="margin-top:14px">Danh mục thể hiện khả năng tích hợp kỹ thuật; không phải danh sách đối tác đã ký kết.</p>')


FAQ_HOME = [
    ("AI và camera có làm lộ dữ liệu của chúng tôi không?", "Dữ liệu hình ảnh và dữ liệu cá nhân được lưu trữ tại Việt Nam, mã hoá khi truyền và khi lưu, truy cập theo phân quyền RBAC và được ghi nhật ký. Với cơ quan nhà nước, hệ thống có thể triển khai On-Premise hoặc Private Cloud, dữ liệu không rời khỏi hạ tầng của đơn vị."),
    ("Dữ liệu của khách hàng có được dùng để huấn luyện AI không?", "Không. TORITECH cam kết Zero Data Training: dữ liệu khách hàng, dữ liệu truy xuất qua MCP và nhật ký hội thoại không được dùng để huấn luyện hay tinh chỉnh mô hình. Xem Chính sách bảo mật AI & MCP."),
    ("AI Agent có thể tự ý sửa, xoá dữ liệu ERP/kế toán không?", "Mặc định MCP Server chỉ cấp quyền đọc. Các lệnh ghi, sửa, xoá hoặc gửi ra ngoài phải được khai báo trong phạm vi quyền và đi qua bước phê duyệt của người có thẩm quyền (Human-in-the-loop). Mọi lệnh đều có Audit Log."),
    ("Có tận dụng được camera và đầu ghi đang có không?", "Có. Nền tảng VMS kết nối camera IP và đầu ghi NVR sẵn có qua chuẩn ONVIF/RTSP, không yêu cầu thay thiết bị nếu thiết bị đáp ứng yêu cầu tối thiểu về luồng video."),
    ("Thời gian triển khai thường mất bao lâu?", "Một đợt thí điểm điển hình kéo dài khoảng 3 tháng: khảo sát 1–2 tuần, kết nối và cấu hình 3–5 tuần, vận hành thử và đo kết quả trong thời gian còn lại. Tiến độ cụ thể phụ thuộc hiện trạng hạ tầng."),
    ("Có xuất hoá đơn VAT và hợp đồng theo quy định không?", "Có. TORITECH xuất hoá đơn điện tử theo quy định và ký hợp đồng kèm Phụ lục SLA và Thỏa thuận xử lý dữ liệu (DPA) khi khách hàng là bên kiểm soát dữ liệu."),
]


def faq_html(items):
    return "".join(f"<details class=\"reveal\"><summary>{q}</summary><p>{a}</p></details>" for q, a in items)


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


SC = {
    "vision": ("Camera nhiều nhưng không ai xem hết: người trực dán mắt vào màn hình, sự cố chỉ được phát hiện khi đã muộn; tra lại video mất hàng giờ.",
               "AI phân tích luồng video thời gian thực, nhận diện phương tiện, hành vi bất thường và đẩy cảnh báo; VMS gom mọi camera, đầu ghi về một màn hình giám sát tập trung."),
    "booking": ("Hàng nghìn người cùng truy cập một lúc: máy chủ quá tải, xe xếp hàng nhiều giờ, người dân không biết khi nào đến lượt.",
                "Mỗi lượt đặt giữ chỗ trên bộ đếm slot chung, phần nặng chạy ở Edge của đối tác; khung giờ được phân bổ đều, nhắc lịch qua Zalo, SMS, app ngân hàng."),
    "mcp": ("Nhân viên đăng nhập từng cổng, tải từng file, gõ lại số liệu giữa ERP, kế toán, thuế, BHXH – 10–15 phút mỗi đơn vị mỗi kỳ, dễ sai và khó truy vết.",
            "AI Agent thao tác qua MCP Server có phân quyền: đọc dữ liệu, tổng hợp, nhắc hạn, soạn báo cáo; lệnh quan trọng cần người duyệt, mọi hành động có Audit Log."),
    "notice": ("Mỗi vụ vi phạm sinh thông báo, biên bản, quyết định phải gửi người dân: văn thư gấp phong bì, ghi địa chỉ, gửi bưu cục; thư bị chuyển hoàn, chậm chấp hành.",
               "Văn thư chỉ cần scan cả tập. AI Agent đọc, phân loại theo biển số, gửi thông báo qua cổng đa kênh tới app ngân hàng, ví điện tử, ví thu phí ETC trong cùng ngày."),
    "trust": ("Video, ảnh khuôn mặt, CCCD, biển số nằm rải rác ở nhiều máy, không phân quyền, không ai biết ai đã xem hay tải gì.",
              "Phân lớp bảo vệ: lưu trữ tại Việt Nam, mã hoá đầu cuối, RBAC cho cả người và AI Agent, nhật ký kiểm toán bất biến, lựa chọn triển khai On-Premise/Private Cloud."),
}

# ================================================================ PAGES


def p_index():
    pillars = f'''<div class="grid g3">
<article class="pillar reveal" style="--acc:#0891b2"><div class="ico">{I["eye"]}</div><span class="eyebrow">Trụ cột 1</span><h3>AI Camera Vision &amp; Hệ thống quản lý tập trung (VMS)</h3>
<ul><li>Xử lý luồng video thời gian thực, nhận diện phương tiện, khuôn mặt (khi được phép), hành vi</li><li>Lưu trữ tập trung, giám sát từ xa, phân quyền theo đơn vị</li><li>Kết nối camera IP, NVR sẵn có theo QCVN 103:2024/BGTVT</li></ul>
<a class="more" href="ai-vision-vms.html">Tìm hiểu AI Vision &amp; VMS →</a></article>
<article class="pillar reveal" style="--acc:#0d9488"><div class="ico">{I["cal"]}</div><span class="eyebrow">Trụ cột 2</span><h3>Nền tảng Đặt lịch hẹn &amp; Điều phối dịch vụ quy mô lớn</h3>
<ul><li>Chịu tải cao (High Concurrency), chống nghẽn cổ chai bằng bộ đếm slot chung</li><li>Thông báo đa kênh: Zalo, SMS, Email, app ngân hàng, ví điện tử</li><li>Tích hợp thanh toán, xác thực, đối soát cuối ngày</li></ul>
<a class="more" href="dat-lich.html">Tìm hiểu nền tảng đặt lịch →</a></article>
<article class="pillar reveal" style="--acc:#7c3aed"><div class="ico">{I["ai"]}</div><span class="eyebrow">Trụ cột 3</span><h3>Hệ sinh thái MCP (Model Context Protocol) &amp; AI Agent</h3>
<ul><li><b>MCP Dịch vụ công:</b> tra cứu thủ tục, trạng thái hồ sơ, nhắc lịch tuân thủ</li><li><b>MCP Doanh nghiệp:</b> kết nối AI vào ERP, CRM, kế toán, thuế, kho vận</li><li><b>MCP Trợ lý nhân viên:</b> tự động hoá tác vụ lặp lại, tra quy trình nội bộ</li></ul>
<a class="more" href="mcp.html">Khám phá hệ sinh thái MCP →</a></article></div>'''

    audience = '''<div class="grid g3">
<div class="card reveal"><div class="num">G</div><h3>Cơ quan quản lý · B2G</h3><p>Sở, ngành, đơn vị hạ tầng cần giám sát tập trung, số hoá văn thư, điều phối dịch vụ công và dữ liệu phục vụ điều hành.</p></div>
<div class="card reveal"><div class="num">B</div><h3>Doanh nghiệp &amp; Trung tâm vận hành · B2B</h3><p>Trung tâm đăng kiểm, chuỗi dịch vụ, ngân hàng, ví điện tử, kế toán dịch vụ – cần chịu tải cao và tự động hoá nghiệp vụ.</p></div>
<div class="card reveal"><div class="num">C</div><h3>Người dân &amp; Nhân sự · B2C</h3><p>Đặt lịch trên ứng dụng quen thuộc, được nhắc hạn, nhận thông báo đúng kênh; nhân viên được AI làm thay việc lặp lại.</p></div></div>'''

    scenes = "".join([
        scene_block("vision", "giai-phap-vision", "Giám sát bằng AI thay cho mắt người", *SC["vision"], ["Nhận diện thời gian thực trên luồng RTSP", "Cảnh báo tức thì theo quy tắc nghiệp vụ", "Tìm lại sự kiện theo biển số, thời gian, vị trí"]),
        scene_block("booking", "giai-phap-dat-lich", "Không còn cảnh xếp hàng nhiều giờ", *SC["booking"], ["Bộ đếm slot chung – không chia quota giữa các kênh", "Edge node tại đối tác gánh phần lớn tải", "Sổ sự kiện ký số, đối soát cuối ngày"], flip=True),
        scene_block("mcp", "giai-phap-mcp", "AI Agent làm việc lặp lại – an toàn, có kiểm soát", *SC["mcp"], ["RBAC, OAuth/API key cho từng MCP Server", "Human-in-the-loop với lệnh ghi/xoá", "Zero Data Training"]),
        scene_block("notice", "giai-phap-van-thu", "Văn thư số: từ tập hồ sơ giấy đến điện thoại người dân", *SC["notice"], ["Scan cả tập, không cần sắp xếp trước", "Phân loại theo biển số, đối chiếu chủ phương tiện", "Gửi qua kênh người dân đang dùng hằng ngày"], flip=True),
    ])

    featured = "".join(work_card(w) for w in WORKS[:3])
    steps = "".join(f'<div class="card reveal"><div class="num">{i+1}</div><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate([
        ("Khảo sát", "Đánh giá hạ tầng camera, hệ thống nghiệp vụ, luồng dữ liệu và yêu cầu pháp lý của đơn vị."),
        ("Thiết kế & DPA", "Chốt kiến trúc (Cloud, Private Cloud hay On-Premise), phạm vi dữ liệu, ký thỏa thuận xử lý dữ liệu."),
        ("Thí điểm", "Kết nối, cấu hình, vận hành thử trên một phạm vi nhỏ, đo bằng chỉ tiêu cụ thể."),
        ("Mở rộng & vận hành", "Nhân rộng theo lộ trình, giám sát 24/7, báo cáo SLA định kỳ."),
    ]))

    body = f'''<section class="dark hero"><div class="wrap hero-grid">
<div><span class="eyebrow">Enterprise &amp; Government-grade · B2G · B2B · B2C</span>
<h1>Hạ tầng <span class="hl">thị giác máy tính thông minh</span> &amp; hệ sinh thái AI Agent (MCP)</h1>
<p class="lead">Tự động hoá vận hành cho doanh nghiệp và dịch vụ công: camera AI giám sát tập trung, nền tảng đặt lịch chịu tải lớn, và AI Agent kết nối an toàn vào dữ liệu thực tế của đơn vị.</p>
<div class="cta-split">
 <div class="cta-box"><small>Doanh nghiệp · Đối tác tích hợp</small><div class="actions"><a class="btn btn-primary btn-sm" href="lien-he.html?topic=demo">Đặt lịch Demo</a><a class="btn btn-ghost btn-sm" href="mcp.html">Khám phá MCP</a></div></div>
 <div class="cta-box"><small>Cơ quan quản lý · Hạ tầng</small><div class="actions"><a class="btn btn-primary btn-sm" href="ho-so-nang-luc.html">Hồ sơ năng lực &amp; Tiêu chuẩn kỹ thuật</a></div></div>
</div>
{tools_bar(video="hero,vision,booking,mcp,notice,trust", video_name="toritech-gioi-thieu", title="TORITECH – Giới thiệu nền tảng")}
</div>
<canvas class="hero-canvas" data-scene="hero" role="img" aria-label="Minh hoạ 2.5D ba trụ cột của nền tảng TORITECH"></canvas>
</div></section>

<section><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Phục vụ đa tệp khách hàng</span><h2>Một nền tảng cho cơ quan quản lý, doanh nghiệp và người dân</h2></div>{audience}</div></section>

<section style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Hệ sinh thái giải pháp</span><h2>Ba trụ cột công nghệ</h2><p class="lead">Mỗi trụ cột dùng được độc lập, kết hợp lại thành một luồng vận hành khép kín: camera phát hiện, nền tảng điều phối, AI Agent xử lý và thông báo.</p></div>{pillars}</div></section>

<section class="dark" id="van-de-giai-phap"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Vấn đề → Giải pháp</span><h2>Xem trực quan từng bài toán được giải quyết thế nào</h2><p class="lead">Bấm <b>Vấn đề</b> / <b>Giải pháp</b> để chuyển cảnh. Nút <b>Xuất MP4</b> dựng video ngắn ngay trên trình duyệt để chia sẻ lên mạng xã hội.</p></div>
<div class="stack">{scenes}</div></div></section>

<section id="trust"><div class="wrap trust-row">
<div class="reveal"><span class="eyebrow">Trust &amp; Governance Center</span><h2>“AI và camera có làm lộ dữ liệu không?”</h2>
<p class="lead">Câu hỏi đầu tiên của mọi cơ quan và doanh nghiệp. Câu trả lời nằm trong kiến trúc, không chỉ trong lời hứa.</p>
<ul class="check"><li><b>Mã hoá đầu cuối</b> – dữ liệu được mã hoá khi truyền (TLS) và khi lưu trữ.</li><li><b>RBAC cho người và AI Agent</b> – mỗi MCP Server chỉ thấy đúng phạm vi được cấp.</li><li><b>Lưu trữ tại Việt Nam</b> – Data Residency theo Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15.</li><li><b>On-Premise / Private Cloud</b> – dữ liệu không rời hạ tầng của cơ quan.</li><li><b>Audit Log &amp; Human-in-the-loop</b> – mọi hành động của AI đều truy vết được.</li></ul>
<p style="margin-top:18px"><a class="btn btn-dark" href="trust-center.html">Vào Trust Center</a></p></div>
<div class="scene reveal" data-scene-root data-state="solution" style="grid-template-columns:1fr"><div class="scene-stage"><canvas data-scene="trust" data-auto role="img" aria-label="Minh hoạ 2.5D các lớp bảo mật dữ liệu"></canvas></div>
{tools_bar(video="trust", video_name="toritech-bao-mat", share_url="index.html#trust", title="Kiến trúc bảo mật TORITECH", print_btn=False)}</div>
</div></section>

<section style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Ecosystem &amp; Integration</span><h2>Kết nối mượt với hạ tầng sẵn có</h2></div>{integrations_html()}</div></section>

<section style="background:#eef3fa"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Dự án &amp; Mô hình</span><h2>Dự án và mô hình tiêu biểu</h2><p class="lead">Các mô phỏng, kiến trúc và đề xuất TORITECH đã xây dựng cho bài toán đăng kiểm, giao thông và dịch vụ công.</p></div>
<div class="grid g3">{featured}</div><p style="margin-top:22px"><a class="btn btn-dark" href="du-an.html">Xem tất cả {len(WORKS)} dự án &amp; mô hình →</a></p></div></section>

<section><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Mô hình hợp tác</span><h2>Triển khai theo 4 bước, bắt đầu bằng thí điểm</h2></div><div class="grid g4">{steps}</div></div></section>

<section style="padding-top:0"><div class="wrap" style="max-width:880px"><div class="sec-head reveal"><span class="eyebrow">Câu hỏi thường gặp</span><h2>Giải đáp trước khi ra quyết định</h2></div>{faq_html(FAQ_HOME)}</div></section>
{cta_band()}'''
    return layout("index.html", "TORITECH – Hạ tầng thị giác máy tính & hệ sinh thái AI Agent (MCP)",
                  "TORITECH cung cấp AI Camera Vision & VMS, nền tảng đặt lịch quy mô lớn và hệ sinh thái AI Agent (MCP) cho doanh nghiệp và dịch vụ công, chuẩn Enterprise & Government-grade.",
                  body, jsonld=[faq_ld(FAQ_HOME)])


def spec_table(rows):
    return '<div class="prose" style="max-width:none;padding:0;border:0;background:none"><table><thead><tr><th>Hạng mục</th><th>Mô tả</th></tr></thead><tbody>' + "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in rows) + "</tbody></table></div>"


def related(cat):
    w, d = cat_cards(cat)
    c = CATS[cat]
    return f'<section style="background:#eef3fa"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Dự án liên quan</span><h2>Dự án &amp; hồ sơ: {c["name"]}</h2></div><div class="grid g3">{w}{d}</div><p style="margin-top:22px"><a class="btn btn-dark" href="{c["page"]}">Xem hạng mục {c["name"]} →</a></p></div></section>'


def roles(mgr, eng):
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    return f'''<div class="grid g2"><div class="card reveal"><h3>Dành cho lãnh đạo / quản lý</h3><ul class="check">{li(mgr)}</ul></div>
<div class="card reveal"><h3>Dành cho đội kỹ thuật / vận hành</h3><ul class="check">{li(eng)}</ul></div></div>'''


def p_vision():
    caps = "".join(f'<div class="card reveal"><h3>{a}</h3><p>{b}</p></div>' for a, b in [
        ("Phân tích video thời gian thực", "Nhận diện phương tiện, biển số, đối tượng và hành vi trên luồng RTSP; quy tắc cảnh báo cấu hình theo nghiệp vụ."),
        ("VMS – quản lý tập trung", "Gom camera, đầu ghi từ nhiều cơ sở về một bản đồ; xem trực tiếp, xem lại, tìm sự kiện theo thời gian, vị trí."),
        ("Tận dụng hạ tầng sẵn có", "Kết nối camera IP và đầu ghi NVR qua ONVIF/RTSP; không yêu cầu thay thiết bị nếu đạt yêu cầu tối thiểu."),
        ("Bảo vệ dữ liệu hình ảnh", "Làm mờ khuôn mặt, biển số khi chia sẻ; thời hạn lưu trữ cấu hình được; mọi lượt xem/tải đều có nhật ký."),
        ("Báo cáo điều hành", "Dashboard tỷ lệ camera trực tuyến, số sự kiện, thời gian xử lý; xuất báo cáo định kỳ cho cơ quan quản lý."),
        ("Triển khai linh hoạt", "Cloud tại Việt Nam, Private Cloud hoặc On-Premise trong trung tâm dữ liệu của đơn vị."),
    ])
    body = page_hero("Giải pháp / AI Camera Vision &amp; VMS", "Trụ cột 1", "AI Camera Vision &amp; Hệ thống quản lý video tập trung (VMS)",
                     "Biến hệ thống camera rời rạc thành một trung tâm giám sát chủ động: AI xem thay mắt người, VMS gom mọi luồng về một nơi, cảnh báo đúng người, đúng lúc.", video="vision", title="AI Camera Vision & VMS") + f'''
<section><div class="wrap stack">{scene_block("vision", "minh-hoa", "Từ camera rời rạc đến giám sát chủ động", *SC["vision"], page="ai-vision-vms.html")}</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Năng lực cốt lõi</span><h2>Những gì hệ thống làm được</h2></div><div class="grid g3">{caps}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Theo vai trò</span><h2>Lợi ích cho từng nhóm người dùng</h2></div>
{roles(["Nắm toàn cảnh hoạt động của mọi cơ sở trên một bản đồ", "Phát hiện sớm vi phạm, xe dừng sai vị trí, khu vực bất thường", "Báo cáo minh bạch, có số liệu cho thanh tra, kiểm tra"],
       ["Kết nối ONVIF/RTSP, không khoá chặt theo hãng thiết bị", "API/Webhook đẩy sự kiện sang hệ thống nghiệp vụ", "Giám sát sức khoẻ camera, đầu ghi, đường truyền"])}</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Thông số &amp; tiêu chuẩn</span><h2>Thông tin kỹ thuật</h2></div>
{spec_table([("Giao thức", "ONVIF Profile S/T, RTSP, RTMP; xuất sự kiện qua Webhook/REST"), ("Tiêu chuẩn chuyên ngành", "Đáp ứng yêu cầu hình ảnh giám sát của QCVN 103:2024/BGTVT đối với cơ sở đăng kiểm (theo thiết bị hiện có của cơ sở)"),
             ("Bảo vệ dữ liệu", "Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15, Nghị định 356/2025/NĐ-CP; làm mờ/ẩn danh; thời hạn lưu trữ cấu hình"),
             ("Mô hình triển khai", "Cloud đặt tại Việt Nam · Private Cloud · On-Premise"), ("Phân quyền", "RBAC theo đơn vị, khu vực, vai trò; SSO khi tích hợp")])}</div></section>
{related("vision")}{cta_band()}'''
    return layout("ai-vision-vms.html", "AI Camera Vision & VMS", "Phân tích video thời gian thực, VMS quản lý tập trung, kết nối camera IP/NVR sẵn có theo ONVIF/RTSP, bảo vệ dữ liệu hình ảnh theo Luật BVDLCN.", body)


def p_booking():
    caps = "".join(f'<div class="card reveal"><h3>{a}</h3><p>{b}</p></div>' for a, b in [
        ("Chịu tải cao", "Mỗi lượt đặt chỉ là một lệnh giữ chỗ nhẹ trên bộ đếm slot chung; danh sách giờ trống phát qua snapshot 30–60 giây cho các kênh tự cache."),
        ("Đa kênh, không chia quota", "App, website, Zalo mini app, app ngân hàng, ví điện tử cùng giữ chỗ trên một bộ đếm – ai đặt trước được trước, không nơi thừa nơi thiếu."),
        ("Thông báo tự động", "Xác nhận, nhắc lịch, đổi giờ, mã QR check-in qua Zalo, SMS, Email, push notification."),
        ("Thanh toán & xác thực", "Tích hợp ví điện tử, ngân hàng, cổng thanh toán; hoá đơn điện tử; xác thực người dùng theo kênh đối tác."),
        ("Đối soát & toàn vẹn", "Sự kiện có số thứ tự và chuỗi hash, ký bằng khoá đối tác; Core phát hiện thiếu/trùng/sửa và đối soát cuối ngày."),
        ("Điều hành theo dữ liệu", "Dashboard công suất từng cơ sở, khung giờ cao điểm, tỷ lệ đến đúng hẹn; gợi ý điều tiết cho cơ quan quản lý."),
    ])
    body = page_hero("Giải pháp / Nền tảng Đặt lịch", "Trụ cột 2", "Nền tảng Đặt lịch hẹn &amp; Điều phối dịch vụ quy mô lớn",
                     "Kinh nghiệm từ đặt lịch đăng kiểm ô tô sau đợt ùn tắc 2022–2023: thiết kế để hàng triệu người đặt lịch qua kênh quen thuộc mà không nghẽn.", video="booking", title="Nền tảng đặt lịch quy mô lớn") + f'''
<section><div class="wrap stack">{scene_block("booking", "minh-hoa", "Từ hàng dài chờ đợi đến khung giờ rõ ràng", *SC["booking"], page="dat-lich.html")}</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Năng lực cốt lõi</span><h2>Thiết kế cho giờ cao điểm</h2></div><div class="grid g3">{caps}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Theo vai trò</span><h2>Lợi ích cho từng nhóm người dùng</h2></div>
{roles(["Giảm ùn tắc tại cơ sở, người dân biết trước giờ phục vụ", "Số liệu công suất theo thời gian thực để điều tiết", "Mở rộng kênh tiếp cận qua ngân hàng, ví điện tử mà không mất quyền kiểm soát dữ liệu"],
       ["Kiến trúc Core – Edge, Edge chạy trên hạ tầng đối tác", "Outbox → ingest một chiều, sự kiện ký số, đối soát tự động", "API chuẩn REST, webhook, môi trường sandbox cho đối tác"])}</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Thông số kỹ thuật</span><h2>Kiến trúc tóm tắt</h2></div>
{spec_table([("Giữ chỗ", "Bộ đếm slot dùng chung theo trạm/ngày/khung giờ: UPDATE … SET reserved = reserved + 1 WHERE reserved &lt; capacity"), ("Giờ trống", "Snapshot do Core xuất mỗi 30–60 giây, Edge tự cache"),
             ("Đồng bộ", "Outbox gom lô đẩy về Core; số thứ tự liên tục, chuỗi hash, chữ ký đối tác"), ("Đối soát", "Cuối ngày: số lượng, tổng tiền, hash cuối chuỗi; lệch thì yêu cầu gửi lại đoạn thiếu"),
             ("Thông báo", "Zalo OA/ZNS, SMS, Email, push app đối tác"), ("Dữ liệu cá nhân", "Thu thập tối thiểu (SĐT, biển số); đồng ý rõ ràng; thời hạn lưu trữ theo chính sách")])}</div></section>
{related("booking")}{cta_band()}'''
    return layout("dat-lich.html", "Nền tảng Đặt lịch & Điều phối dịch vụ", "Nền tảng đặt lịch chịu tải cao, đa kênh qua ngân hàng và ví điện tử, thông báo tự động, thanh toán và đối soát cho dịch vụ công và trung tâm vận hành.", body)


def p_mcp():
    def block(anchor, title, lead, items, eyebrow):
        li = "".join(f"<li>{x}</li>" for x in items)
        return f'<div class="card reveal" id="{anchor}"><span class="eyebrow">{eyebrow}</span><h3>{title}</h3><p style="margin-bottom:12px">{lead}</p><ul class="check">{li}</ul></div>'
    blocks = "".join([
        block("dvc", "MCP Dịch vụ công", "Kết nối AI với cổng dịch vụ công để tra cứu và nhắc việc, thay cho thao tác đăng nhập từng cổng.",
              ["Tra cứu thủ tục, trạng thái hồ sơ", "Tải C12 BHXH theo lịch cho nhiều mã đơn vị", "Nhắc lịch tuân thủ: kê khai, nộp, gia hạn", "Lưu Google Drive/OneDrive, ghi Excel, gửi email tổng hợp", '<a href="du-an/vmgportal-ai-sms.html">VMGPortal</a>: AI vận hành Nền tảng nhắn tin SMS của VMG – soạn mẫu, gửi tin hằng ngày, kiểm tra số dư, báo cáo, đối soát'], "Dành cho kế toán, đại lý, doanh nghiệp"),
        block("doanh-nghiep", "MCP Công cụ Doanh nghiệp", "Đưa AI vào thẳng dữ liệu vận hành, với quyền đọc mặc định và quyền ghi có phê duyệt.",
              ["ERP, CRM, kế toán, thuế, kho vận", "Báo cáo tổng hợp bằng câu lệnh tự nhiên", "Phát hiện bất thường (số phải đóng tăng, tồn kho lệch)", "Lệnh ghi/xoá đi qua Human-in-the-loop"], "Dành cho ban điều hành, tài chính, vận hành"),
        block("nhan-su", "MCP Trợ lý Nhân viên", "Trợ lý làm thay việc lặp lại và trả lời theo đúng quy trình nội bộ của đơn vị.",
              ["Tự động hoá tác vụ lặp lại theo lịch", "Tra cứu quy trình, biểu mẫu nội bộ tức thì", "Văn thư số: scan, phân loại, gửi thông báo", "Chạy trên Claude, ChatGPT, Gemini, Copilot"], "Dành cho nhân sự, văn thư, hành chính"),
    ])
    body = page_hero("Giải pháp / Hệ sinh thái MCP", "Trụ cột 3", "Hệ sinh thái MCP &amp; AI Agent",
                     "Model Context Protocol (MCP) là chuẩn mở để mô hình AI (LLM) gọi công cụ và truy xuất dữ liệu bên ngoài. TORITECH xây MCP Server có phân quyền, nhật ký và phê duyệt – để AI làm việc thật trên dữ liệu thật, một cách an toàn.", video="mcp,notice", title="Hệ sinh thái MCP & AI Agent") + f'''
<section><div class="wrap stack">{scene_block("mcp", "minh-hoa", "Từ copy-paste thủ công đến AI Agent có kiểm soát", *SC["mcp"], page="mcp.html")}
{scene_block("notice", "van-thu-so", "AI Agent văn thư số cho thông báo vi phạm giao thông", *SC["notice"], flip=True, page="mcp.html")}</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Ba dòng sản phẩm MCP</span><h2>Dịch vụ công · Doanh nghiệp · Nhân sự</h2></div><div class="grid g3">{blocks}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Mô hình kiểm soát</span><h2>MCP an toàn theo thiết kế</h2></div>
{spec_table([("Xác thực", "OAuth 2.0 hoặc API key riêng cho từng khách hàng, thu hồi được ngay khi nghi lộ"), ("Phân quyền", "RBAC theo công cụ (tool) và phạm vi dữ liệu; mặc định chỉ đọc"),
             ("Phê duyệt", "Human-in-the-loop với lệnh ghi, sửa, xoá, gửi ra ngoài"), ("Nhật ký", "Audit Log cho mọi lệnh gọi: ai, công cụ nào, tham số, kết quả, thời điểm"),
             ("Dữ liệu huấn luyện", "Zero Data Training – không dùng dữ liệu khách hàng để huấn luyện/tinh chỉnh mô hình"), ("Thông tin đăng nhập", "Không lưu mật khẩu cổng dịch vụ công dạng đọc được; ưu tiên phiên đăng nhập do người dùng cấp"),
             ("Vai trò pháp lý", "TORITECH là trung gian kết nối kỹ thuật, không đại diện cơ quan nhà nước – xem Miễn trừ trách nhiệm dữ liệu dịch vụ công")])}</div></section>
{related("mcp")}{cta_band("Kết nối AI vào hệ thống của bạn – an toàn ngay từ ngày đầu", "Nhận tư vấn kiến trúc MCP miễn phí: phạm vi quyền, luồng phê duyệt, mô hình triển khai.")}'''
    return layout("mcp.html", "Hệ sinh thái MCP & AI Agent", "MCP Server cho dịch vụ công, ERP/CRM/kế toán/thuế và trợ lý nhân viên: phân quyền RBAC, OAuth, Audit Log, Human-in-the-loop, Zero Data Training.", body)


def p_trust():
    pol = "".join(f'<a class="card reveal" style="text-decoration:none" href="{h}"><h3>{t} →</h3><p>{d}</p></a>' for h, t, d in [
        ("chinh-sach-bao-ve-du-lieu-ca-nhan.html", "Bảo vệ dữ liệu cá nhân & sinh trắc học", "Mục đích xử lý, thời hạn lưu video/ảnh, ẩn danh hoá, quy trình tiếp nhận yêu cầu xoá dữ liệu."),
        ("chinh-sach-bao-mat-ai-mcp.html", "Bảo mật & Quản trị AI / MCP", "Zero Data Training, OAuth/API key, Audit Log, Human-in-the-loop cho lệnh quan trọng."),
        ("mien-tru-trach-nhiem-dich-vu-cong.html", "Miễn trừ trách nhiệm dữ liệu dịch vụ công", "Vai trò trung gian công nghệ; dữ liệu gốc thuộc cổng thông tin chính thức tại thời điểm truy vấn."),
        ("thoa-thuan-xu-ly-du-lieu-dpa.html", "Thỏa thuận xử lý dữ liệu (DPA)", "Trách nhiệm của TORITECH với tư cách bên xử lý dữ liệu cho VMS, SaaS đặt lịch và MCP."),
        ("cam-ket-chat-luong-sla.html", "Cam kết chất lượng dịch vụ (SLA)", "Uptime, thời gian phản hồi sự cố, RTO/RPO, sao lưu và tiêu chuẩn kỹ thuật áp dụng."),
        ("chinh-sach-cookie.html", "Chính sách Cookie", "Website chỉ dùng bộ nhớ trình duyệt thiết yếu, không mã theo dõi quảng cáo."),
    ])
    arch = "".join(f'<div class="card reveal"><div class="num">{i+1}</div><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate([
        ("Mã hoá đầu cuối", "TLS cho mọi kết nối; mã hoá dữ liệu khi lưu; khoá được quản lý tách biệt khỏi dữ liệu."),
        ("RBAC chi tiết", "Phân quyền theo đơn vị, vai trò, khu vực – áp dụng cho cả người dùng và AI Agent/MCP Server."),
        ("Lưu trữ tại Việt Nam", "Dữ liệu đặt tại trung tâm dữ liệu trong nước; chuyển ra nước ngoài chỉ khi có căn cứ pháp lý và đánh giá tác động."),
        ("On-Premise / Private Cloud", "Với cơ quan nhà nước: triển khai trong hạ tầng của đơn vị, dữ liệu không rời khỏi mạng nội bộ."),
        ("Nhật ký kiểm toán", "Mọi lượt xem, tải, chia sẻ, lệnh gọi MCP đều được ghi lại, phục vụ thanh tra, kiểm tra."),
        ("Ẩn danh & tối thiểu hoá", "Làm mờ khuôn mặt, biển số khi chia sẻ; chỉ thu thập dữ liệu cần cho mục đích đã thông báo."),
    ]))
    body = page_hero("Bảo mật &amp; Tuân thủ", "Trust &amp; Governance Center", "Bảo mật &amp; Tuân thủ",
                     "Tài liệu và cam kết để vượt qua vòng thẩm định pháp lý (Due Diligence) của đối tác lớn và cơ quan nhà nước – căn cứ Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15 và Nghị định 356/2025/NĐ-CP (thay thế Nghị định 13/2023/NĐ-CP từ 01/01/2026).", video="trust", title="Bảo mật & Tuân thủ – TORITECH") + f'''
<section><div class="wrap stack">{scene_block("trust", "minh-hoa", "Nhiều lớp bảo vệ quanh dữ liệu của bạn", *SC["trust"], page="trust-center.html")}</div></section>
<section style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Kiến trúc bảo mật</span><h2>Sáu nguyên tắc thiết kế</h2></div><div class="grid g3">{arch}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Chính sách &amp; văn bản</span><h2>Bộ tài liệu tuân thủ</h2></div><div class="grid g3">{pol}</div></div></section>
<section style="padding-top:0"><div class="wrap grid g2">
<div class="card reveal" id="quyen-chu-the"><h3>Thực hiện quyền của chủ thể dữ liệu</h3><p style="margin-bottom:10px">Công dân có thể yêu cầu xem, chỉnh sửa, xoá, hạn chế xử lý hoặc rút lại sự đồng ý đối với dữ liệu cá nhân.</p>
<ul class="check"><li>Gửi yêu cầu qua hotline/Zalo {CO["hotline"]} hoặc biểu mẫu Liên hệ (chọn “Yêu cầu về dữ liệu cá nhân”)</li><li>Xác minh danh tính người yêu cầu</li><li>Phản hồi trong thời hạn luật định</li><li>Nếu TORITECH là bên xử lý thay cho khách hàng, yêu cầu được chuyển tới bên kiểm soát dữ liệu</li></ul>
<p style="margin-top:12px"><a class="btn btn-dark btn-sm" href="lien-he.html?topic=dulieu">Gửi yêu cầu</a></p></div>
<div class="card reveal" id="bao-cao-lo-hong"><h3>Báo cáo lỗ hổng bảo mật</h3><p style="margin-bottom:10px">Chúng tôi trân trọng các nhà nghiên cứu báo cáo lỗ hổng một cách có trách nhiệm.</p>
<ul class="check"><li>Liên hệ: {email_or(CO["email_security"], "hotline/Zalo " + CO["hotline"])}</li><li>Mô tả lỗ hổng, bước tái hiện, phạm vi ảnh hưởng</li><li>Không truy cập, sửa, xoá dữ liệu của người khác; không tấn công từ chối dịch vụ</li><li>Chúng tôi xác nhận tiếp nhận và thông báo tiến độ xử lý</li></ul></div>
</div></section>{cta_band("Cần bộ hồ sơ tuân thủ cho thẩm định?", "Nhận DPA mẫu, phụ lục SLA, mô tả kiến trúc bảo mật và danh mục tiêu chuẩn kỹ thuật.")}'''
    return layout("trust-center.html", "Bảo mật & Tuân thủ – Trust Center", "Mã hoá đầu cuối, RBAC cho MCP, lưu trữ tại Việt Nam, On-Premise, Audit Log; chính sách bảo vệ dữ liệu cá nhân theo Luật 91/2025/QH15 và NĐ 356/2025/NĐ-CP.", body)


def p_projects():
    secs, table = [], []
    for k, c in CATS.items():
        w, d = cat_cards(k)
        n = sum(1 for x in WORKS + DOCS if x["cat"] == k)
        secs.append(f'''<section id="{k}"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Hạng mục · {n} mục</span><h2><a href="{c["page"]}">{c["name"]}</a></h2><p class="lead">{c["lead"]}</p></div>
<div class="grid g3">{w}{d}</div><p style="margin-top:22px"><a class="btn btn-dark" href="{c["page"]}">Mở hạng mục {c["name"]} →</a></p></div></section>''')
        table += [f'<tr><td><a href="{c["page"]}">{c["name"]}</a></td><td>{x["title"]}</td><td>{x.get("kind", "Công văn / Đề xuất")}</td></tr>' for x in WORKS + DOCS if x["cat"] == k]
    jump = '<div class="filters" role="navigation" aria-label="Hạng mục">' + "".join(f'<a class="tool" href="{c["page"]}">{c["name"]}</a>' for c in CATS.values()) + "</div>"
    body = page_hero("Dự án &amp; Mô hình", "Portfolio", "Dự án &amp; mô hình trình diễn",
                     f"{len(WORKS)} dự án và mô hình trình diễn của TORITECH, chia theo {len(CATS)} hạng mục. Mở từng dự án để xem trực tiếp.", extra=jump, title="Dự án & Hồ sơ – TORITECH") + "".join(secs) + f'''
<section><div class="wrap"><div class="prose reveal" style="max-width:none"><h2>Danh mục theo hạng mục</h2><table><thead><tr><th>Hạng mục</th><th>Tên</th><th>Loại</th></tr></thead><tbody>{"".join(table)}</tbody></table>
<p class="meta-line">Dữ liệu trong các dự án trình diễn là dữ liệu mẫu hoặc dữ liệu công khai của cơ sở kinh doanh (địa chỉ, giờ làm việc, hotline); thông tin cá nhân đã được che hoặc thay bằng dữ liệu giả lập.</p></div></div></section>{cta_band()}'''
    return layout("du-an.html", "Dự án & Mô hình", "Dự án và mô hình trình diễn của TORITECH theo hạng mục: AI Vision & VMS, Đặt lịch & Điều phối, MCP & AI Agent, Game & Giải trí.", body, scenes=False)


def p_category(k):
    c = CATS[k]
    w, d = cat_cards(k)
    first = next((x for x in WORKS if x["cat"] == k), None)
    sol = f'<a class="btn btn-ghost btn-sm" style="color:#fff;border-color:rgba(255,255,255,.4)" href="{c["solution"]}">Giải pháp {c["name"]} →</a>' if c["solution"] else ""
    others = '<div class="filters" role="navigation" aria-label="Hạng mục khác"><a class="tool" href="du-an.html">Tất cả</a>' + "".join(f'<a class="tool" href="{o["page"]}"{" aria-current=page" if o is c else ""}>{o["name"]}</a>' for o in CATS.values()) + "</div>"
    body = page_hero(f'<a href="du-an.html">Dự án</a> / {c["name"]}', "Hạng mục dự án", c["name"], c["lead"], extra=f'<div class="actions" style="margin:14px 0">{sol}</div>{others}', title=f'Dự án {c["name"]} – TORITECH')
    body += f'<section><div class="wrap"><div class="grid g3">{w}</div></div></section>' if w else ""
    body += f'<section id="ho-so" style="background:#eef3fa"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Hồ sơ đề xuất</span><h2>Công văn &amp; đề xuất</h2><p class="lead">Bản tóm tắt; bản đầy đủ cung cấp theo yêu cầu.</p></div><div class="grid g3">{d}</div></div></section>' if d else ""
    items = [{"@type": "ListItem", "position": i + 1, "url": SITE_URL + x["href"], "name": x["title"]} for i, x in enumerate(x for x in WORKS if x["cat"] == k)]
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": f'Dự án {c["name"]}', "url": SITE_URL + c["page"], "mainEntity": {"@type": "ItemList", "itemListElement": items}}]
    return layout(c["page"], f'Dự án {c["name"]}', f'{c["lead"]} Danh sách dự án và mô hình của TORITECH.', body + cta_band(), active="du-an.html", jsonld=ld, scenes=False,
                  og_image=SITE_URL + du_an.img_rel(first) if first else None)


def p_docs():
    body = page_hero("Tài liệu kỹ thuật", "Docs · API · MCP", "Tài liệu kỹ thuật",
                     "Dành cho CTO, kỹ sư tích hợp và đội vận hành: kiến trúc, cách kết nối MCP Server, API đặt lịch, sự kiện VMS và trạng thái dịch vụ.", title="Tài liệu kỹ thuật – TORITECH") + f'''
<section><div class="wrap legal"><aside><b>Mục lục</b><a href="#kien-truc">Kiến trúc hệ thống</a><a href="#api">Kết nối MCP</a><a href="#dat-lich-api">API đặt lịch</a><a href="#vms-api">Sự kiện VMS</a><a href="#trang-thai">Trạng thái dịch vụ</a><a href="#faq">Câu hỏi thường gặp</a></aside>
<div class="prose">
<h2 id="kien-truc">1. Kiến trúc hệ thống</h2>
<p>Nền tảng gồm ba khối chạy độc lập, giao tiếp qua API và hàng đợi sự kiện:</p>
<table><thead><tr><th>Khối</th><th>Thành phần</th><th>Triển khai</th></tr></thead><tbody>
<tr><td>AI Vision &amp; VMS</td><td>Bộ thu luồng RTSP/ONVIF, dịch vụ suy luận AI, lưu trữ video/sự kiện, bản đồ giám sát</td><td>Edge tại cơ sở + trung tâm (Cloud VN / On-Premise)</td></tr>
<tr><td>Đặt lịch &amp; Điều phối</td><td>Core (bộ đếm slot, sổ sự kiện ký số, đối soát), Edge node tại đối tác, dịch vụ thông báo</td><td>Core tại Việt Nam; Edge trên hạ tầng đối tác</td></tr>
<tr><td>MCP &amp; AI Agent</td><td>MCP Server theo lĩnh vực, cổng xác thực OAuth/API key, Audit Log, hàng đợi phê duyệt</td><td>SaaS hoặc Private Cloud của khách hàng</td></tr></tbody></table>
<h2 id="api">2. Kết nối MCP Server</h2>
<p>MCP Server của TORITECH dùng giao thức Model Context Protocol qua HTTP (Streamable HTTP). Các trợ lý hỗ trợ MCP như Claude, ChatGPT, Gemini, Copilot có thể thêm connector bằng URL do TORITECH cấp.</p>
<ol><li>Nhận URL MCP và API key (hoặc thực hiện đăng nhập OAuth) sau khi kích hoạt dịch vụ.</li><li>Trong trợ lý AI, mở phần cài đặt connector / tích hợp, thêm connector tuỳ chỉnh với URL được cấp.</li><li>Khai báo key theo hướng dẫn kèm theo; không chia sẻ key qua kênh công khai.</li><li>Thử một lệnh chỉ đọc, ví dụ: “Liệt kê các công cụ có sẵn”.</li></ol>
<div class="note">Key là thông tin bí mật của từng khách hàng. Khi nghi bị lộ, liên hệ TORITECH để thu hồi key và xoá thông tin đã lưu.</div>
<h3>Ví dụ cấu hình (giá trị giả lập)</h3>
<pre style="background:#0b1426;color:#e2e8f0;padding:16px;border-radius:12px;overflow:auto;font-size:.85rem">{{
  "mcpServers": {{
    "toritech-dvc": {{
      "url": "https://mcp.example.vn/dvc",
      "headers": {{ "Authorization": "Bearer ••••••••••••" }}
    }}
  }}
}}</pre>
<h2 id="dat-lich-api">3. API đặt lịch (tóm tắt)</h2>
<table><thead><tr><th>Luồng</th><th>Mô tả</th></tr></thead><tbody>
<tr><td>Lấy giờ trống</td><td>Đọc snapshot khung giờ theo cơ sở/ngày (cache 30–60 giây)</td></tr>
<tr><td>Giữ chỗ</td><td>Một lệnh giữ chỗ nhẹ trên bộ đếm slot chung; trả về mã đặt lịch</td></tr>
<tr><td>Xác nhận / Huỷ / Đổi giờ</td><td>Ghi sự kiện vào outbox, đẩy về Core theo lô</td></tr>
<tr><td>Đối soát</td><td>Cuối ngày gửi tổng số lượng, tổng tiền, hash cuối chuỗi</td></tr></tbody></table>
<p>Tài liệu OpenAPI đầy đủ và môi trường sandbox được cấp cho đối tác sau khi ký thỏa thuận tích hợp.</p>
<h2 id="vms-api">4. Sự kiện VMS</h2>
<p>Sự kiện AI (phương tiện, vi phạm vùng, camera mất tín hiệu…) được đẩy qua Webhook/REST với mã sự kiện, thời gian, camera, ảnh trích đã làm mờ theo cấu hình. Ảnh chụp màn hình và log minh hoạ trong tài liệu luôn dùng dữ liệu giả lập.</p>
<h2 id="trang-thai">5. Trạng thái dịch vụ</h2>
<p>Khách hàng doanh nghiệp được cấp trang trạng thái và báo cáo SLA định kỳ theo hợp đồng. Thông báo sự cố và bảo trì có kế hoạch được gửi qua email/Zalo đã đăng ký. Trang trạng thái công khai đang được chuẩn bị.</p>
<h2 id="faq">6. Câu hỏi thường gặp</h2>{faq_html(FAQ_HOME[2:5])}
</div></div></section>'''
    return layout("tai-lieu.html", "Tài liệu kỹ thuật – Docs, API, MCP", "Kiến trúc hệ thống, hướng dẫn kết nối MCP Server với Claude, ChatGPT, Gemini, Copilot, API đặt lịch, sự kiện VMS và trạng thái dịch vụ.", body, scenes=False)


def entity_table():
    rows = [("Tên doanh nghiệp", CO["legal_name"]), ("Tên viết tắt", CO["short"]), ("Mã số doanh nghiệp / MST", f'{CO["tax_id"]} – cấp ngày {CO["tax_date"]}'),
            ("Người đại diện theo pháp luật", CO["rep"]), ("Địa chỉ trụ sở", CO["address"]), ("Ngành nghề", CO["industries"]),
            ("Hotline / Zalo", CO["hotline"]), ("Email hỗ trợ", CO["email_support"] or "Đang cập nhật"), ("Email bảo vệ dữ liệu", CO["email_dpo"] or "Đang cập nhật")]
    return "<table><tbody>" + "".join(f"<tr><th style='width:34%'>{a}</th><td>{b}</td></tr>" for a, b in rows) + "</tbody></table>"


def p_about():
    vals = "".join(f'<div class="card reveal"><h3>{a}</h3><p>{b}</p></div>' for a, b in [
        ("Thực chiến", "Giải pháp xuất phát từ bài toán vận hành thật: ùn tắc đăng kiểm, văn thư xử phạt, thao tác dịch vụ công lặp lại."),
        ("An toàn theo thiết kế", "Bảo vệ dữ liệu, phân quyền và nhật ký được thiết kế từ đầu, không phải bổ sung sau."),
        ("Mở và tương thích", "Dùng chuẩn mở (ONVIF, RTSP, MCP, REST) để khách hàng không bị khoá chặt vào một nhà cung cấp."),
    ])
    body = page_hero("Về chúng tôi", "Về TORITECH", "Công nghệ để vận hành công và doanh nghiệp tốt hơn mỗi ngày",
                     "TORITECH phát triển hạ tầng thị giác máy tính, nền tảng đặt lịch quy mô lớn và hệ sinh thái AI Agent (MCP) cho cơ quan quản lý, doanh nghiệp và người dân tại Việt Nam.", title="Về TORITECH") + f'''
<section><div class="wrap"><div class="grid g3">{vals}</div></div></section>
<section style="padding-top:0"><div class="wrap legal"><aside><b>Nội dung</b><a href="#phap-nhan">Thông tin pháp nhân</a><a href="#nang-luc">Năng lực</a><a href="#lien-he">Liên hệ</a></aside>
<div class="prose"><h2 id="phap-nhan">Thông tin pháp nhân</h2>{entity_table()}
<p class="meta-line">Thông tin công bố theo quy định về thương mại điện tử (Luật Thương mại điện tử số 122/2025/QH15 và văn bản hướng dẫn).</p>
<h2 id="nang-luc">Năng lực</h2><ul><li>Vận hành nền tảng đặt lịch đăng kiểm ô tô kết nối nhiều trung tâm đăng kiểm trên cả nước.</li><li>Xây dựng MCP connector cho dịch vụ công (BHXH) và công cụ văn phòng.</li><li>Thiết kế kiến trúc dữ liệu đăng kiểm, giám sát camera cho cơ quan quản lý cấp tỉnh/thành.</li></ul>
<p><a class="btn btn-dark" href="ho-so-nang-luc.html">Xem hồ sơ năng lực</a></p>
<h2 id="lien-he">Liên hệ</h2><p>Hotline/Zalo: <a href="tel:{CO["hotline_tel"]}">{CO["hotline"]}</a> · Trụ sở: {CO["address"]}</p><p><a class="btn btn-primary" href="lien-he.html">Gửi yêu cầu tư vấn</a></p></div></div></section>'''
    return layout("ve-chung-toi.html", "Về chúng tôi", "Thông tin pháp nhân CÔNG TY TNHH TORITECH (MST 0317545179), năng lực và liên hệ.", body, scenes=False)


def p_profile():
    prod = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in [
        ("AI Camera Vision & VMS", "Phân tích video thời gian thực, quản lý tập trung camera/đầu ghi, cảnh báo, báo cáo", "Sở/ngành, cơ sở đăng kiểm, trung tâm vận hành"),
        ("Nền tảng Đặt lịch & Điều phối", "Đặt lịch đa kênh chịu tải cao, thông báo, thanh toán, đối soát", "Trung tâm đăng kiểm, kiểm định khí thải, dịch vụ công"),
        ("MCP Dịch vụ công", "Tra cứu, tải hồ sơ theo lịch, nhắc hạn tuân thủ", "Doanh nghiệp, kế toán dịch vụ, đại lý"),
        ("MCP Doanh nghiệp", "Kết nối AI với ERP, CRM, kế toán, thuế, kho vận", "Doanh nghiệp vừa và lớn"),
        ("MCP Trợ lý nhân viên / Văn thư số", "Tự động hoá tác vụ lặp lại, số hoá và gửi thông báo", "Cơ quan, đơn vị hành chính"),
    ])
    std = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in [
        ("Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15; Nghị định 356/2025/NĐ-CP", "Xử lý dữ liệu cá nhân, dữ liệu nhạy cảm (hình ảnh, CCCD, biển số)"),
        ("Luật Dữ liệu số 60/2024/QH15", "Quản trị, chia sẻ dữ liệu số"),
        ("Luật Giao dịch điện tử số 20/2023/QH15", "Văn bản, chữ ký, thông báo điện tử"),
        ("Luật Thương mại điện tử số 122/2025/QH15", "Công bố thông tin trên website, giao dịch trực tuyến"),
        ("QCVN 103:2024/BGTVT", "Cơ sở vật chất kỹ thuật, vị trí cơ sở đăng kiểm (hình ảnh giám sát)"),
        ("ONVIF Profile S/T, RTSP", "Kết nối camera IP, đầu ghi NVR đa hãng"),
        ("Model Context Protocol (MCP)", "Kết nối mô hình AI với công cụ và dữ liệu"),
        ("OAuth 2.0, TLS", "Xác thực, mã hoá kênh truyền"),
    ])
    body = page_hero("Hồ sơ năng lực", "Dành cho cơ quan quản lý &amp; đối tác hạ tầng", "Hồ sơ năng lực &amp; Tiêu chuẩn kỹ thuật",
                     "Bản tóm tắt để thẩm định: pháp nhân, danh mục sản phẩm, mô hình triển khai, tiêu chuẩn áp dụng và các dự án, mô hình đã thực hiện. Bấm “In / PDF” để lưu thành tệp PDF.", title="Hồ sơ năng lực TORITECH") + f'''
<section><div class="wrap"><div class="prose" style="max-width:none">
<h2>1. Thông tin pháp nhân</h2>{entity_table()}
<h2>2. Danh mục sản phẩm</h2><table><thead><tr><th>Sản phẩm</th><th>Chức năng chính</th><th>Đối tượng</th></tr></thead><tbody>{prod}</tbody></table>
<h2>3. Mô hình triển khai</h2><table><thead><tr><th>Mô hình</th><th>Phù hợp</th></tr></thead><tbody>
<tr><td>SaaS – Cloud đặt tại Việt Nam</td><td>Doanh nghiệp cần triển khai nhanh</td></tr><tr><td>Private Cloud</td><td>Doanh nghiệp lớn, ngân hàng, ví điện tử</td></tr><tr><td>On-Premise</td><td>Cơ quan nhà nước, dữ liệu không rời hạ tầng nội bộ</td></tr></tbody></table>
<h2>4. Tiêu chuẩn &amp; căn cứ áp dụng</h2><table><thead><tr><th>Văn bản / tiêu chuẩn</th><th>Phạm vi</th></tr></thead><tbody>{std}</tbody></table>
<h2>5. Dự án &amp; mô hình trình diễn</h2><ul>{"".join(f"<li><b>{w['title']}</b> – {w['desc']}</li>" for w in WORKS + DOCS)}</ul>
<h2>6. Bộ tài liệu tuân thủ</h2><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in LEGAL_LINKS)}</ul>
<div class="note">Hợp đồng, phụ lục SLA, DPA và hồ sơ pháp lý (giấy chứng nhận đăng ký doanh nghiệp…) được cung cấp bản chính thức khi có yêu cầu thẩm định.</div>
</div></div></section>{cta_band("Cần trao đổi trực tiếp với kỹ sư giải pháp?", "Chúng tôi sẵn sàng trình bày kiến trúc và demo trên hạ tầng thử nghiệm của đơn vị.")}'''
    return layout("ho-so-nang-luc.html", "Hồ sơ năng lực & Tiêu chuẩn kỹ thuật", "Hồ sơ năng lực TORITECH: pháp nhân, sản phẩm, mô hình triển khai, tiêu chuẩn áp dụng và dự án tiêu biểu – in thành PDF để thẩm định.", body, scenes=False)


def p_contact():
    em = CO["email_support"]
    body = page_hero("Liên hệ", "Liên hệ tư vấn", "Đặt lịch Demo &amp; Liên hệ tư vấn",
                     "Gửi email hoặc gọi/Zalo trực tiếp cho kỹ sư giải pháp. Chúng tôi phản hồi trong giờ làm việc.", title="Liên hệ TORITECH") + f'''
<section><div class="wrap grid g3" style="align-items:stretch">
<a class="card contact-ch reveal" id="ct-email" href="mailto:{em}?subject=Li%C3%AAn%20h%E1%BB%87%20t%C6%B0%20v%E1%BA%A5n%20TORITECH"><span class="eyebrow">Email</span><h3>{em}</h3><p>Mô tả ngắn bài toán, quy mô, thời gian mong muốn. Có thể đính kèm tài liệu.</p><span class="btn btn-primary btn-sm">Gửi email →</span></a>
<a class="card contact-ch reveal" href="tel:{CO["hotline_tel"]}"><span class="eyebrow">Điện thoại</span><h3>{CO["hotline"]}</h3><p>Gọi trực tiếp trong giờ làm việc để đặt lịch demo hoặc trao đổi nhanh.</p><span class="btn btn-dark btn-sm">Gọi ngay →</span></a>
<a class="card contact-ch reveal" href="https://zalo.me/{CO["zalo"]}" rel="noopener" target="_blank"><span class="eyebrow">Zalo</span><h3>{CO["hotline"]}</h3><p>Nhắn Zalo để gửi hình ảnh, tài liệu hoặc hẹn lịch gọi video.</p><span class="btn btn-ghost btn-sm">Nhắn Zalo →</span></a>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="card"><h3>Thông tin pháp nhân</h3><div class="prose" style="padding:0;border:0">{entity_table()}</div></div></div></section>
<script>(function(){{var T={{demo:"Đặt lịch Demo giải pháp",vision:"Tư vấn AI Camera Vision & VMS",booking:"Tư vấn nền tảng đặt lịch",mcp:"Tư vấn hệ sinh thái MCP / AI Agent",hoso:"Yêu cầu hồ sơ năng lực",dulieu:"Yêu cầu về dữ liệu cá nhân"}};var t=new URLSearchParams(location.search).get("topic");if(t&&T[t]){{var a=document.getElementById("ct-email");a.href="mailto:{em}?subject="+encodeURIComponent(T[t]+" – TORITECH");}}}})();</script>'''
    return layout("lien-he.html", "Liên hệ tư vấn & Đặt lịch Demo", f"Liên hệ TORITECH qua email {em} hoặc hotline/Zalo {CO['hotline']} để đặt lịch demo AI Camera Vision & VMS, nền tảng đặt lịch, hệ sinh thái MCP, hoặc nhận hồ sơ năng lực.", body, scenes=False)


def p_legal(path, title, desc, sections, intro):
    toc = "".join(f'<a href="#s{i+1}">{i+1}. {h}</a>' for i, (h, _) in enumerate(sections))
    secs = "".join(f'<h2 id="s{i+1}">{i+1}. {h}</h2>{c}' for i, (h, c) in enumerate(sections))
    body = page_hero("Pháp lý / " + title, "Pháp lý &amp; Chính sách", title, intro, title=title) + f'''
<section><div class="wrap legal"><aside><b>Mục lục</b>{toc}<hr style="border:0;border-top:1px solid #e2e8f0;margin:12px 0">{"".join(f'<a href="{h}">{t}</a>' for h, t in LEGAL_LINKS if h != path)}</aside>
<div class="prose"><p class="meta-line">Phiên bản {VERSION} · Hiệu lực từ {EFFECTIVE} · Áp dụng cho website và dịch vụ của {CO["legal_name"]}</p>{secs}
<div class="note">Trường hợp hợp đồng hoặc phụ lục đã ký với khách hàng có quy định khác, quy định trong hợp đồng được ưu tiên áp dụng.</div></div></div></section>'''
    return layout(path, title, desc, body, scenes=False)


def p_404():
    body = '<section class="dark page-hero" style="min-height:50vh"><div class="wrap"><span class="eyebrow">404</span><h1>Không tìm thấy trang</h1><p class="lead">Đường dẫn có thể đã thay đổi. Quay lại trang chủ hoặc xem các giải pháp.</p><div class="actions"><a class="btn btn-primary" href="index.html">Về trang chủ</a><a class="btn btn-ghost" href="du-an.html">Dự án &amp; Hồ sơ</a></div></div></section>'
    html = layout("404.html", "Không tìm thấy trang", "Trang không tồn tại.", body, scenes=False)
    # 404 có thể được phục vụ ở đường dẫn con → dùng base tuyệt đối
    return html.replace("<head>\n", f'<head>\n<base href="{SITE_URL}">\n', 1)


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def main():
    du_an.ensure_images(WORKS)
    pages = {
        "index.html": p_index(), "ai-vision-vms.html": p_vision(), "dat-lich.html": p_booking(), "mcp.html": p_mcp(),
        "trust-center.html": p_trust(), "du-an.html": p_projects(), "tai-lieu.html": p_docs(), "ve-chung-toi.html": p_about(),
        "ho-so-nang-luc.html": p_profile(), "lien-he.html": p_contact(), "404.html": p_404(),
    }
    for path, title, desc, intro, sections in legal.pages(CO):
        pages[path] = p_legal(path, title, desc, sections, intro)
    for k in CATS:
        pages[CATS[k]["page"]] = p_category(k)
    for p, c in pages.items():
        write(p, c)
    du_an.inject_chrome(WORKS, DOCS, CATS, CO, SITE_URL, LOGO)
    du_an.write_redirects(WORKS, SITE_URL)

    # sitemap / robots / llms.txt
    urls = [p for p in pages if p != "404.html"] + [w["href"] for w in WORKS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{SITE_URL}{'' if u == 'index.html' else u}</loc><lastmod>2026-11-16</lastmod></url>\n" for u in urls) + "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n")
    llms = f"""# TORITECH

> {CO["legal_name"]} (MST {CO["tax_id"]}) cung cấp hạ tầng thị giác máy tính (AI Camera Vision & VMS), nền tảng đặt lịch hẹn & điều phối dịch vụ quy mô lớn, và hệ sinh thái AI Agent qua Model Context Protocol (MCP) cho cơ quan quản lý (B2G), doanh nghiệp (B2B) và người dân (B2C) tại Việt Nam.

Liên hệ: hotline/Zalo {CO["hotline"]} · Trụ sở: {CO["address"]}

## Giải pháp
- [AI Camera Vision & VMS]({SITE_URL}ai-vision-vms.html): phân tích video thời gian thực, quản lý tập trung camera/đầu ghi (ONVIF/RTSP), cảnh báo, báo cáo.
- [Nền tảng Đặt lịch & Điều phối]({SITE_URL}dat-lich.html): bộ đếm slot chung chịu tải cao, đa kênh qua ngân hàng/ví điện tử, thông báo, thanh toán, đối soát ký số.
- [Hệ sinh thái MCP & AI Agent]({SITE_URL}mcp.html): MCP Dịch vụ công, MCP Doanh nghiệp (ERP/CRM/kế toán/thuế), MCP Trợ lý nhân viên; RBAC, OAuth, Audit Log, Human-in-the-loop, Zero Data Training.

## Tin cậy & pháp lý
- [Trust Center]({SITE_URL}trust-center.html)
""" + "".join(f"- [{t}]({SITE_URL}{h})\n" for h, t in LEGAL_LINKS) + f"""
## Tài nguyên
- [Tài liệu kỹ thuật]({SITE_URL}tai-lieu.html)
- [Hồ sơ năng lực & tiêu chuẩn kỹ thuật]({SITE_URL}ho-so-nang-luc.html)
- [Dự án & mô hình]({SITE_URL}du-an.html)
""" + "".join(f"  - [{w['title']}]({SITE_URL}{w['href']}): {w['desc']}\n" for w in WORKS)
    write("llms.txt", llms)
    write(".nojekyll", "")
    print("Built", len(pages), "pages")


if __name__ == "__main__":
    main()
