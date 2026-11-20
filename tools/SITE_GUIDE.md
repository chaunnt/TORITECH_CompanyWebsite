# TORITECH website – Tiêu chí & quy trình bổ sung trang

Tài liệu nội bộ (không deploy). Dùng khi cần thêm/sửa trang, và cho tác vụ đồng bộ artifact hằng ngày.

## 1. Thông tin cố định
- Production: https://toritech.vn/ · Bản GitHub Pages: https://chaunnt.github.io/TORITECH_CompanyWebsite/
- Repo: `chaunnt/TORITECH_CompanyWebsite`, nhánh `main`. Push `main` → GitHub Actions deploy (không chạy build).
- **Không bao giờ deploy** `tools/`, `.github/`, `README.md` (đã loại trừ trong `.github/workflows/pages.yml` – giữ nguyên dòng `rsync --exclude`).
- Site là HTML tĩnh. `tools/build.py` sinh lại toàn bộ `.html` từ `tools/build.py` + `tools/legal.py` + `tools/site_config.py` + `tools/showcase.json` và **ghi đè** HTML sửa tay → trước khi chạy, kiểm tra `git log` xem có ai sửa tay file HTML không; nếu có thì chuyển phần sửa đó vào tools trước.
- Pháp nhân: CÔNG TY TNHH TORITECH · MST 0317545179 · Hotline/Zalo 0343 902 960 · email chính thức: chưa có (điền vào `site_config.py` khi có).

## 2. Kiến trúc nội dung (Platform Hub)
- Header: Giải pháp (AI Vision & VMS · Nền tảng Đặt lịch · Hệ sinh thái MCP) · Dự án & Hồ sơ · Bảo mật & Tuân thủ · Tài liệu kỹ thuật · Về chúng tôi · CTA "Liên hệ tư vấn".
- Hero: 2 luồng CTA – Doanh nghiệp/Đối tác ("Đặt lịch Demo", "Khám phá MCP") và Cơ quan quản lý/Hạ tầng ("Hồ sơ năng lực & Tiêu chuẩn kỹ thuật").
- 3 trụ cột (`cat`): `vision` = AI Camera Vision & VMS · `booking` = Đặt lịch & Điều phối · `mcp` = MCP & AI Agent (Dịch vụ công / Doanh nghiệp / Trợ lý nhân viên).
- Mục phụ `game` = Game & Giải trí (game, mô phỏng giải trí do công ty làm) – chỉ hiện ở Dự án & Hồ sơ, không có trang giải pháp riêng.
- Mỗi giải pháp: cảnh 2.5D (Vấn đề ↔ Giải pháp), năng lực, lợi ích theo vai trò (quản lý vs kỹ thuật), bảng thông số, dự án liên quan, CTA.
- Footer 4 cột (Pháp nhân · Sản phẩm · Tài nguyên · Pháp lý) + dải pháp lý.
- Mọi trang: nút Chia sẻ (FB, Zalo, LinkedIn, X, Telegram, Email, copy, Web Share), In/PDF, Xuất MP4 (trang có cảnh 2.5D); OG image, JSON-LD, canonical; cập nhật `sitemap.xml`, `llms.txt` (build.py tự làm).

## 3. Trang pháp lý bắt buộc (đã có – giữ đồng bộ)
Điều khoản sử dụng · Bảo vệ dữ liệu cá nhân & sinh trắc học · Bảo mật & quản trị AI/MCP · Miễn trừ trách nhiệm dữ liệu dịch vụ công · DPA · SLA & quy chuẩn kỹ thuật · Thanh toán/hoàn huỷ/gia hạn · Cookie. Thông tin pháp nhân ở footer + Về chúng tôi.
- Căn cứ hiện hành: Luật BVDLCN 91/2025/QH15 + NĐ 356/2025/NĐ-CP (thay NĐ 13/2023 từ 01/01/2026); Luật Dữ liệu 60/2024/QH15; Luật GDĐT 20/2023/QH15; Luật TMĐT 122/2025/QH15; Luật BVQLNTD 19/2023/QH15; QCVN 103:2024/BGTVT.
- Trước khi trích dẫn văn bản pháp luật mới: tra cứu xác minh số hiệu, năm, hiệu lực.
- Còn treo: luật sư rà soát trang pháp lý & con số SLA; email support/security/dpo; logo Bộ Công Thương nếu bật thanh toán trực tuyến.

## 4. Tiêu chuẩn biên tập (Editorial checklist)
| Hạng mục | Đạt | Loại bỏ |
|---|---|---|
| Mở bài | Nêu vấn đề & giá trị trong 3 câu đầu | Vòng vo, định nghĩa sách giáo khoa |
| Nội dung | Ví dụ thực tế, cơ chế kỹ thuật, số liệu có nguồn | Hứa hẹn chung chung, số liệu bịa |
| Trình bày | H1 duy nhất, H2/H3 cụ thể, đoạn ≤ 3–4 dòng, bảng/bullet | Khối chữ đặc |
| Văn phong | Chuyên gia, điềm tĩnh; giải thích viết tắt lần đầu (MCP, VMS, RBAC, SLA…) | "Siêu phẩm", "số 1", "duy nhất" |
| An toàn dữ liệu | Che khuôn mặt, biển số, SĐT cá nhân, CCCD, API key/token; dùng dữ liệu giả lập | Lộ thông tin thật |
| Chuyển đổi | CTA đúng ngữ cảnh (giữa bài + cuối bài) | Kết thúc cụt |
| SEO/GEO | Từ khoá ở H1/100 chữ đầu/1 H2/meta; câu trả lời trực diện dưới tiêu đề dạng câu hỏi; alt ảnh | — |
| Form | Ô đồng ý **không** tick sẵn | Tick sẵn |
- Không công bố: chứng nhận (ISO, SOC 2…) chưa có; danh sách đối tác chưa ký (chỉ ghi "khả năng tích hợp").

## 5. Quy trình bổ sung artifact vào website (thủ công hoặc tác vụ hằng ngày)
1. Liệt kê artifact của chủ tài khoản (`list_artifacts`, chỉ `rel = mine`, bỏ `soft_deleted`). So với `artifact_slug` trong `tools/showcase.json` (`works`, `docs`, `skipped`).
2. Với mỗi artifact mới, quyết định:
   - Chủ sở hữu (20/11/2026): artifact là showcase dự án của công ty → mặc định đưa lên. Liên quan 1 trong 3 trụ cột → `vision`/`booking`/`mcp`; game/giải trí → `game`. Chỉ `skipped` khi là việc cá nhân, đối soát, nội dung quảng bá thuần cho bên thứ ba, hoặc vướng an toàn dữ liệu ở bước 3.
   - Trang HTML trình diễn/sản phẩm/kiến trúc → `works`: tải về `showcase/<slug-tieng-viet-khong-dau>.html` (artifact nhiều file: tải đủ file phụ; thư viện `/_runtime/...` → vendor vào `showcase/vendor/`).
   - Docs (công văn, đề xuất gửi cơ quan, bản nháp có chỗ trống `[…]`) → `docs`: chỉ thẻ tóm tắt 1–2 câu, không đăng toàn văn.
3. Kiểm tra an toàn trước khi đăng: không chứa SĐT/email cá nhân, CCCD, token/API key thật, dữ liệu khách hàng thật, mật khẩu; không mạo danh cơ quan; nếu có → `skipped` với lý do "cần người duyệt" (không tự sửa nội dung artifact).
4. Viết `title` (giữ tên artifact, chỉnh cho rõ), `desc` 1–2 câu theo checklist mục 4, `kind` (Mô hình tương tác / Mô phỏng 2.5D / Trang sản phẩm / Đề xuất dự án / Đề xuất kiến trúc / Ứng dụng web).
5. `node tools/og_shots.js` (tạo ảnh xem trước 1200×630 cho trang showcase mới vào `assets/img/showcase/`), rồi `python3 tools/build.py` (tự chèn thẻ OG/canonical vào `<head>` trang showcase giữa `<!-- toritech:meta -->`, không đổi nội dung), xem thử bằng trình duyệt headless (không lỗi JS, thẻ hiển thị đúng hạng mục), rồi commit & push `main`.
6. Ghi tóm tắt: đã thêm gì, vào hạng mục nào, đã bỏ qua gì và vì sao.

## 6. Khi được yêu cầu "bổ sung trang"
Thêm hàm `p_<ten>()` trong `tools/build.py` (hoặc trang pháp lý trong `tools/legal.py`), thêm vào `pages` trong `main()`, thêm link ở `NAV`/footer nếu cần, build, kiểm tra, push. Giữ đúng mục 2–4.
