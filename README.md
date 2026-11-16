# TORITECH_CompanyWebsite

Landing page HTML5 đa trang của **CÔNG TY TNHH TORITECH** – AI Camera Vision & VMS, Nền tảng đặt lịch quy mô lớn, Hệ sinh thái MCP & AI Agent.

- Site: https://toritech.vn/ (bản GitHub Pages: https://chaunnt.github.io/TORITECH_CompanyWebsite/)
- Tiêu chí & quy trình bổ sung trang/artifact: `tools/SITE_GUIDE.md`
- Hoạ tiết 2.5D (Canvas, không thư viện) cho từng giải pháp: chế độ **Vấn đề → Giải pháp** (`assets/js/scenes.js`)
- Nút **Chia sẻ** (Facebook, Zalo, LinkedIn, X, Telegram, Email, sao chép, Web Share), **In / PDF**, **Xuất MP4** (MediaRecorder, 1280×720, tạo ngay trên trình duyệt; WebM nếu trình duyệt không hỗ trợ MP4)
- Trang pháp lý: Điều khoản, Bảo vệ DLCN (Luật 91/2025/QH15, NĐ 356/2025/NĐ-CP), Bảo mật AI & MCP, Miễn trừ DVC, DPA, SLA, Thanh toán & hoàn huỷ, Cookie
- `showcase/`: các bản trình diễn (artifact) hiện có, phân theo 3 trụ cột
- SEO/GEO: Open Graph, JSON-LD (Organization, FAQPage), `sitemap.xml`, `robots.txt`, `llms.txt`

## Chỉnh sửa
Site là HTML tĩnh: có thể sửa trực tiếp các file `.html`, `assets/css/site.css`, `assets/js/*.js`.

`tools/` là công cụ sinh trang (tuỳ chọn, chạy trên máy): `tools/build.py` (trang), `tools/legal.py` (chính sách), `tools/site_config.py` (pháp nhân, email, URL).

```bash
python3 tools/build.py          # sinh lại toàn bộ HTML – GHI ĐÈ các file .html đã sửa tay
python3 -m http.server 8000     # xem thử tại http://localhost:8000
```

Deploy: GitHub Actions (`.github/workflows/pages.yml`) chép file lên Pages khi push `main`, không chạy build, và **không** đưa `.github/`, `tools/`, `README.md` lên site.
