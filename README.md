# TORITECH_CompanyWebsite

Landing page HTML5 đa trang của **CÔNG TY TNHH TORITECH** – AI Camera Vision & VMS, Nền tảng đặt lịch quy mô lớn, Hệ sinh thái MCP & AI Agent.

- Site: https://chaunnt.github.io/TORITECH_CompanyWebsite/
- Hoạ tiết 2.5D (Canvas, không thư viện) cho từng giải pháp: chế độ **Vấn đề → Giải pháp** (`assets/js/scenes.js`)
- Nút **Chia sẻ** (Facebook, Zalo, LinkedIn, X, Telegram, Email, sao chép, Web Share), **In / PDF**, **Xuất MP4** (MediaRecorder, 1280×720, tạo ngay trên trình duyệt; WebM nếu trình duyệt không hỗ trợ MP4)
- Trang pháp lý: Điều khoản, Bảo vệ DLCN (Luật 91/2025/QH15, NĐ 356/2025/NĐ-CP), Bảo mật AI & MCP, Miễn trừ DVC, DPA, SLA, Thanh toán & hoàn huỷ, Cookie
- `showcase/`: các bản trình diễn (artifact) hiện có, phân theo 3 trụ cột
- SEO/GEO: Open Graph, JSON-LD (Organization, FAQPage), `sitemap.xml`, `robots.txt`, `llms.txt`

## Chỉnh sửa
Nội dung sinh từ `tools/build.py` (trang), `tools/legal.py` (chính sách), `tools/site_config.py` (pháp nhân, email, URL).

```bash
python3 tools/build.py          # sinh lại toàn bộ HTML
python3 -m http.server 8000     # xem thử tại http://localhost:8000
```

Deploy tự động bằng GitHub Actions (`.github/workflows/pages.yml`) khi push lên `main`.
