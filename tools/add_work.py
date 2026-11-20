# -*- coding: utf-8 -*-
"""Thêm 1 dự án vào website bằng một lệnh (không cần đọc/sửa tay projects.json).

python3 tools/add_work.py --src <file.html tải từ artifact> --name <ten-khong-dau> --cat vision|booking|mcp|game \
    --slug <artifact uuid> --title "..." --desc "..." --kind "Mô hình tương tác"
python3 tools/add_work.py --doc --slug ... --title ...                           # công văn/đề xuất: CƠ MẬT → chỉ ghi vào skipped, không đăng
python3 tools/add_work.py --skip --slug ... --title ... --reason "..."           # đã xét, không đăng

Sau đó chạy: python3 tools/build.py  (tự chụp ảnh, tạo thumbnail, chèn header/chân trang/meta).
"""
import argparse
import json
import os
import re
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "tools", "projects.json")
CATS = ("vision", "booking", "mcp", "game")
KINDS = ("Mô hình tương tác", "Mô phỏng 2.5D", "Trang sản phẩm", "Đề xuất dự án", "Đề xuất kiến trúc", "Ứng dụng web")

ap = argparse.ArgumentParser()
ap.add_argument("--src"); ap.add_argument("--name"); ap.add_argument("--cat", choices=CATS)
ap.add_argument("--slug", required=True); ap.add_argument("--title", required=True); ap.add_argument("--desc")
ap.add_argument("--kind", default="Mô hình tương tác")
ap.add_argument("--doc", action="store_true"); ap.add_argument("--skip", action="store_true"); ap.add_argument("--reason")
a = ap.parse_args()

d = json.load(open(DATA, encoding="utf-8"))
known = {x["artifact_slug"] for k in ("works", "docs", "skipped") for x in d[k]}
if a.slug in known:
    raise SystemExit(f"{a.slug} đã có trong projects.json")

if a.skip:
    d["skipped"].append({"artifact_slug": a.slug, "title": a.title, "reason": a.reason or ""})
elif a.doc:
    d["skipped"].append({"artifact_slug": a.slug, "title": a.title, "reason": "không đăng: công văn/đề xuất gửi cơ quan là tài liệu cơ mật"})
else:
    assert a.src and a.name and a.cat and a.desc, "cần --src --name --cat --desc"
    assert re.fullmatch(r"[a-z0-9-]+", a.name), "--name chỉ gồm a-z, 0-9, '-'"
    if a.kind not in KINDS:
        print("Cảnh báo: kind ngoài danh sách", KINDS)
    href = f"du-an/{a.name}.html"
    if os.path.exists(os.path.join(ROOT, href)):
        raise SystemExit(f"{href} đã tồn tại")
    shutil.copyfile(a.src, os.path.join(ROOT, href))
    d["works"].append({"artifact_slug": a.slug, "href": href, "cat": a.cat, "title": a.title, "desc": a.desc, "kind": a.kind})

with open(DATA, "w", encoding="utf-8") as f:
    f.write(json.dumps(d, ensure_ascii=False, indent=2))
print("OK – giờ chạy: python3 tools/build.py")
