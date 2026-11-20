# TORITECH website – Tiêu chí & quy trình bổ sung trang

Tài liệu nội bộ (không deploy). Dùng khi cần thêm/sửa trang, và cho tác vụ đồng bộ artifact hằng ngày.

## 0a. Bảo mật nội dung (chủ sở hữu 20/11/2026 – bắt buộc)
- **Công văn, đề xuất/kiến nghị gửi cơ quan là tài liệu CƠ MẬT → KHÔNG đăng** dưới bất kỳ hình thức nào (kể cả thẻ tóm tắt). Artifact dạng công văn (có "Kính gửi", "Kiến nghị", số hiệu văn bản, chữ ký…) → `add_work.py --doc` (chỉ ghi vào `skipped`). Website chỉ đăng **mô hình, dự án**.
- **Không nêu tên riêng của đơn vị triển khai / đối tác** (cơ quan, sở, cục, ngân hàng, ví điện tử, nhà mạng, hãng bảo hiểm, nền tảng của đối tác…) **trừ khi chủ sở hữu ghi rõ trong yêu cầu**. Dùng tên chung: "cơ quan quản lý đô thị", "Sở quản lý", "CSGT", "cơ quan đăng kiểm", "ứng dụng giao thông", "ví điện tử", "ngân hàng", "ví thu phí ETC", "hãng bảo hiểm"…
  - Đã được phép nêu: **VMG** ("Nền tảng nhắn tin SMS của VMG").
  - Mô hình "Review đơn vị dịch vụ" (`du-an/review-tram-dang-kiem.html`): được giữ thương hiệu **TTDK** và tên các trạm đăng kiểm thật (dữ liệu công khai, chủ sở hữu duyệt 20/11/2026).
  - Được giữ: tên văn bản pháp luật và cơ quan ban hành khi trích dẫn căn cứ pháp lý; công nghệ/kênh phổ thông (Zalo, Google Drive, Claude, ChatGPT…).
  - Artifact mới có tên riêng đơn vị/đối tác: thay bằng tên chung trong bản trên website (chỉ đổi chữ hiển thị, không đổi mã/logic), hoặc `--skip` với lý do "cần chủ sở hữu duyệt" nếu tên gắn liền với nội dung (thương hiệu trang, danh sách cơ sở thật).

## 0. Quy tắc làm việc tiết kiệm (đọc trước)
- **Mọi phần chung đều do script làm.** Header/chân trang site, header + chân trang + "Cùng hạng mục" + thẻ SEO/OG của trang dự án, ảnh đại diện, thumbnail, trang hạng mục, sitemap, llms.txt, trang chuyển hướng → `python3 tools/build.py`. **Không** sửa tay file `.html` đã sinh, **không** đọc/ghi từng dòng danh sách; sửa ở `tools/` rồi build.
- Thêm dự án: `python3 tools/add_work.py ...` (xem docstring) → `python3 tools/build.py`. Không cần mở `projects.json`.
- Kiểm tra nhanh sau build: script playwright mở trang `du-an*.html`, `lien-he.html` và từng `du-an/*.html` (không lỗi JS; `#tt-top` ở y=0 không bị che; cuộn hết trang thấy `#tt-foot`).
- Không dùng chữ "showcase" ở URL/tên/nội dung mới. Thư mục `showcase/` chỉ còn trang chuyển hướng cho link cũ đã chia sẻ (sinh tự động từ `old_href`).

## 1. Thông tin cố định
- Production: https://toritech.vn/ · Bản GitHub Pages: https://chaunnt.github.io/TORITECH_CompanyWebsite/
- Repo: `chaunnt/TORITECH_CompanyWebsite`, nhánh `main`. Push `main` → GitHub Actions deploy (không chạy build).
- **Không bao giờ deploy** `tools/`, `.github/`, `README.md` (đã loại trừ trong `.github/workflows/pages.yml` – giữ nguyên dòng `rsync --exclude`).
- Site là HTML tĩnh. `tools/build.py` sinh lại toàn bộ `.html` từ `tools/build.py` + `tools/legal.py` + `tools/site_config.py` + `tools/projects.json` + `tools/du_an.py` và **ghi đè** HTML sửa tay → trước khi chạy, kiểm tra `git log` xem có ai sửa tay file HTML không; nếu có thì chuyển phần sửa đó vào tools trước.
- Pháp nhân: CÔNG TY TNHH TORITECH · MST 0317545179 · Hotline/Zalo 0343 902 960 · Email liên hệ: chau.nguyen@toritech.vn (`email_support`; email security/DPO chưa có).

## 2. Kiến trúc nội dung (Platform Hub)
- Header: Giải pháp (AI Vision & VMS · Nền tảng Đặt lịch · Hệ sinh thái MCP) · Dự án (menu: Tất cả + 4 hạng mục) · Bảo mật & Tuân thủ · Tài liệu kỹ thuật · Về chúng tôi · CTA "Liên hệ tư vấn".
- Hero: 2 luồng CTA – Doanh nghiệp/Đối tác ("Đặt lịch Demo", "Khám phá MCP") và Cơ quan quản lý/Hạ tầng ("Hồ sơ năng lực & Tiêu chuẩn kỹ thuật").
- 3 trụ cột (`cat`): `vision` = AI Camera Vision & VMS · `booking` = Đặt lịch & Điều phối · `mcp` = MCP & AI Agent (Dịch vụ công / Doanh nghiệp / Trợ lý nhân viên).
- Mục phụ `game` = Game & Giải trí (game, mô phỏng giải trí do công ty làm) – không có trang giải pháp riêng.
- **Mọi dự án/hồ sơ phải có `cat`** (build báo lỗi nếu thiếu). Cấu hình hạng mục: `CATS` trong `build.py`.
- Cấu trúc URL dự án:
  - `du-an.html` – "Dự án & Mô hình", chia section theo hạng mục (không có công văn/hồ sơ đề xuất).
  - Trang hạng mục: `du-an-ai-vision-vms.html`, `du-an-dat-lich.html`, `du-an-mcp-ai-agent.html`, `du-an-game-giai-tri.html` (thẻ dùng **ảnh WebP**, không nhúng iframe/HTML5 – nhẹ trang).
  - Trang dự án: `du-an/<ten-khong-dau>.html` (HTML gốc artifact + khối build chèn: header chung về trang hạng mục, chân trang có danh sách cùng hạng mục). Ảnh: `assets/img/du-an/<ten>.jpg` (OG 1200×630) và `assets/img/du-an/thumb/<ten>.webp`.
- Phần **Phản biện** trong trang dự án là nội dung viết tay (khối `<section id="phan-bien">` ngay trước `<!-- toritech:foot -->`), không nằm trong marker của build → build giữ nguyên. Khi thay bản HTML mới của artifact, phải giữ/viết lại phần này.
- Trang dự án viết trực tiếp cho website (không có artifact): `artifact_slug` dạng `site-<ten>` (ví dụ `site-vmgportal`, `site-bao-hiem-zns`), dùng `../assets/css/site.css`.
- Trang Liên hệ: **không có form**; chỉ nút bấm trực tiếp Email (mailto, tiêu đề theo `?topic=`), Gọi, Zalo.
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
| **Phản biện cuối bài** | Khi **soạn nội dung** (artifact, trang giải pháp, bài viết, đề xuất), người viết **tự viết** phần **Phản biện** ở cuối, nằm trong thân bài: "Vì sao nên làm" (giá trị, lý do làm ngay) và "Nếu không làm thì sao" (hậu quả, rủi ro, chi phí cơ hội) – lập luận riêng cho bài toán, có căn cứ, không bịa số liệu. **Không** sinh tự động bằng script/footer, không dùng câu mẫu lặp lại giữa các bài | Thiếu phản biện; phản biện chung chung, dán khuôn, doạ dẫm |
| SEO/GEO | Từ khoá ở H1/100 chữ đầu/1 H2/meta; câu trả lời trực diện dưới tiêu đề dạng câu hỏi; alt ảnh | — |
| Form | Ô đồng ý **không** tick sẵn | Tick sẵn |
- Không công bố: chứng nhận (ISO, SOC 2…) chưa có; danh sách đối tác chưa ký (chỉ ghi "khả năng tích hợp").

## 5. Quy trình bổ sung artifact vào website (thủ công hoặc tác vụ hằng ngày)
1. Liệt kê artifact của chủ tài khoản (`list_artifacts`, chỉ `rel = mine`, bỏ `soft_deleted`). So với `artifact_slug` trong `tools/projects.json` (`works`, `docs`, `skipped`) – lấy nhanh bằng `python3 -c "import json;d=json.load(open('tools/projects.json'));print([x['artifact_slug'] for k in d if isinstance(d[k],list) for x in d[k]])"`.
2. Với mỗi artifact mới, quyết định:
   - Chủ sở hữu (20/11/2026): artifact là showcase dự án của công ty → mặc định đưa lên. Liên quan 1 trong 3 trụ cột → `vision`/`booking`/`mcp`; game/giải trí → `game`. Chỉ `skipped` khi là việc cá nhân, đối soát, nội dung quảng bá thuần cho bên thứ ba, hoặc vướng an toàn dữ liệu ở bước 3.
   - Trang HTML trình diễn/sản phẩm/kiến trúc → `works`: tải HTML (Artifact read `path: index.html` → file trong scratchpad) rồi `tools/add_work.py --src <file> --name <ten-khong-dau> ...` (artifact nhiều file: tải đủ file phụ vào `du-an/`; thư viện `/_runtime/...` → vendor vào `du-an/vendor/`).
   - Docs / công văn / đề xuất gửi cơ quan → **không đăng** (`add_work.py --doc` chỉ ghi vào `skipped`).
3. Kiểm tra an toàn trước khi đăng: không chứa SĐT/email cá nhân, CCCD, token/API key thật, dữ liệu khách hàng thật, mật khẩu; không mạo danh cơ quan; nếu có → `skipped` với lý do "cần người duyệt" (không tự sửa nội dung artifact).
4. Viết `title` (giữ tên artifact, chỉnh cho rõ), `desc` 1–2 câu theo checklist mục 4, `kind` (Mô hình tương tác / Mô phỏng 2.5D / Trang sản phẩm / Đề xuất dự án / Đề xuất kiến trúc / Ứng dụng web). Phản biện thuộc nội dung artifact (người làm artifact tự viết); tác vụ đồng bộ không tự thêm vào trang.
5. `python3 tools/build.py` (tự chụp ảnh còn thiếu qua `tools/og_shots.js`, tạo thumbnail, chèn khối `<!-- toritech:meta|top|foot -->` – chạy lại không nhân bản, nội dung artifact giữ nguyên), kiểm tra nhanh (mục 0), rồi commit & push `main`.
6. Ghi tóm tắt: đã thêm gì, vào hạng mục nào, đã bỏ qua gì và vì sao.

## 6. Khi được yêu cầu "bổ sung trang"
Thêm hàm `p_<ten>()` trong `tools/build.py` (hoặc trang pháp lý trong `tools/legal.py`), thêm vào `pages` trong `main()`, thêm link ở `NAV`/footer nếu cần, build, kiểm tra, push. Giữ đúng mục 2–4.
