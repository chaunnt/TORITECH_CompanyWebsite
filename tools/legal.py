# -*- coding: utf-8 -*-
"""Nội dung các trang pháp lý & chính sách. Bản công bố trên website – nên được luật sư rà soát trước khi áp dụng chính thức."""

LAWS = ("Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15 (hiệu lực 01/01/2026) và Nghị định số 356/2025/NĐ-CP "
        "quy định chi tiết, thay thế Nghị định 13/2023/NĐ-CP")


def ul(*xs):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"


def tbl(head, rows):
    return ("<table><thead><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>")


def pages(CO):
    contact = f'hotline/Zalo <a href="tel:{CO["hotline_tel"]}">{CO["hotline"]}</a>' + (f', email <a href="mailto:{CO["email_dpo"]}">{CO["email_dpo"]}</a>' if CO["email_dpo"] else "") + ' hoặc <a href="lien-he.html?topic=dulieu">biểu mẫu liên hệ</a>'
    name = CO["legal_name"]
    out = []

    # 1. Terms of service
    out.append(("dieu-khoan-su-dung.html", "Điều khoản sử dụng",
                "Điều khoản sử dụng website và dịch vụ phần mềm, API, MCP của TORITECH.",
                "Quy định quyền và nghĩa vụ khi truy cập website và sử dụng phần mềm, API, MCP Server do TORITECH cung cấp.", [
        ("Phạm vi áp dụng", f"<p>Điều khoản này áp dụng giữa {name} (“TORITECH”) và tổ chức, cá nhân truy cập website hoặc sử dụng dịch vụ (“Khách hàng”). Việc sử dụng dịch vụ đồng nghĩa với việc đồng ý với Điều khoản này và các chính sách được dẫn chiếu.</p>"),
        ("Dịch vụ", ul("AI Camera Vision &amp; VMS: phân tích video, quản lý camera và đầu ghi tập trung.", "Nền tảng đặt lịch hẹn &amp; điều phối dịch vụ, thông báo, thanh toán, đối soát.", "MCP Server &amp; AI Agent: kết nối mô hình AI với dịch vụ công và hệ thống của Khách hàng.") + "<p>Phạm vi, cấu hình và mức dịch vụ cụ thể được xác định trong hợp đồng, đơn đặt hàng hoặc gói dịch vụ đã đăng ký.</p>"),
        ("Tài khoản, API key và bảo mật", ul("Khách hàng chịu trách nhiệm bảo mật tài khoản, API key, token do TORITECH cấp và mọi hoạt động phát sinh từ đó.", "Phải thông báo ngay cho TORITECH khi nghi ngờ bị lộ để thu hồi key.", "Không chia sẻ, bán lại hoặc cho bên thứ ba sử dụng key khi chưa có chấp thuận bằng văn bản.")),
        ("Sử dụng được phép", ul("Không dùng dịch vụ để truy cập trái phép hệ thống, dữ liệu của người khác hoặc vượt quá quyền được cấp trên cổng dịch vụ công.", "Không dùng dịch vụ để giám sát, theo dõi cá nhân trái pháp luật.", "Không can thiệp, dò quét, tấn công hoặc làm quá tải hạ tầng.", "Khách hàng chịu trách nhiệm về tính hợp pháp của dữ liệu mình đưa vào hệ thống và về việc có căn cứ xử lý dữ liệu cá nhân.")),
        ("Sở hữu trí tuệ", "<p>Phần mềm, mã nguồn, mô hình, giao diện, tài liệu và thương hiệu TORITECH thuộc quyền sở hữu của TORITECH hoặc bên cấp phép. Khách hàng được cấp quyền sử dụng không độc quyền, không chuyển nhượng trong thời hạn dịch vụ. Dữ liệu của Khách hàng thuộc về Khách hàng.</p>"),
        ("Giới hạn trách nhiệm", "<p>TORITECH nỗ lực duy trì dịch vụ theo Cam kết chất lượng dịch vụ (SLA). Trong phạm vi pháp luật cho phép, TORITECH không chịu trách nhiệm đối với thiệt hại gián tiếp, mất lợi nhuận, hoặc thiệt hại phát sinh từ dữ liệu của cơ quan, hệ thống bên thứ ba (bao gồm cổng dịch vụ công) không chính xác hay gián đoạn. Tổng trách nhiệm bồi thường không vượt quá phí dịch vụ Khách hàng đã thanh toán trong 12 tháng gần nhất, trừ khi hợp đồng quy định khác.</p>"),
        ("Tạm ngừng và chấm dứt", ul("TORITECH có thể tạm ngừng dịch vụ khi Khách hàng vi phạm nghiêm trọng Điều khoản, có dấu hiệu lộ key, hoặc theo yêu cầu của cơ quan có thẩm quyền.", "Khi chấm dứt, dữ liệu được trả lại hoặc xoá theo Thỏa thuận xử lý dữ liệu (DPA).")),
        ("Luật áp dụng và giải quyết tranh chấp", "<p>Điều khoản được điều chỉnh bởi pháp luật Việt Nam. Tranh chấp được ưu tiên giải quyết bằng thương lượng; nếu không thành, được đưa ra Toà án nhân dân có thẩm quyền tại Thành phố Hồ Chí Minh hoặc trọng tài theo thỏa thuận trong hợp đồng.</p>"),
        ("Liên hệ", f"<p>{name} – MST {CO['tax_id']} – {CO['address']}. Liên hệ: {contact}.</p>"),
    ]))

    # 2. Personal data & biometric policy
    out.append(("chinh-sach-bao-ve-du-lieu-ca-nhan.html", "Chính sách bảo vệ dữ liệu cá nhân & dữ liệu sinh trắc học",
                "Chính sách bảo vệ dữ liệu cá nhân, dữ liệu hình ảnh và sinh trắc học của TORITECH theo Luật 91/2025/QH15 và Nghị định 356/2025/NĐ-CP.",
                f"Áp dụng cho dữ liệu thu thập qua website, nền tảng đặt lịch, hệ thống AI Camera &amp; VMS và MCP. Căn cứ {LAWS}.", [
        ("Vai trò của TORITECH", "<p>TORITECH là <b>bên kiểm soát dữ liệu</b> đối với dữ liệu thu thập trực tiếp qua website và tài khoản khách hàng; là <b>bên xử lý dữ liệu</b> khi vận hành VMS, SaaS đặt lịch hoặc MCP thay cho khách hàng (cơ quan, doanh nghiệp). Trong trường hợp sau, khách hàng là bên kiểm soát và chịu trách nhiệm về căn cứ xử lý; TORITECH xử lý theo chỉ dẫn và Thỏa thuận xử lý dữ liệu (DPA).</p>"),
        ("Loại dữ liệu và mục đích", tbl(["Nguồn", "Dữ liệu", "Mục đích"], [
            ["Form liên hệ website", "Họ tên, đơn vị, số điện thoại, email, nội dung", "Liên hệ tư vấn, gửi báo giá"],
            ["Nền tảng đặt lịch", "Số điện thoại, họ tên, biển số xe, mã đặt lịch; CCCD khi thủ tục yêu cầu", "Giữ chỗ, xác nhận, nhắc lịch, check-in, đối soát"],
            ["AI Camera &amp; VMS", "Hình ảnh, video phương tiện, biển số; hình ảnh khuôn mặt, hành vi (dữ liệu nhạy cảm) nếu có trong khung hình", "Giám sát an ninh, vận hành, phát hiện vi phạm theo yêu cầu của bên kiểm soát"],
            ["MCP / AI Agent", "Dữ liệu truy xuất từ hệ thống khách hàng hoặc cổng dịch vụ công trong phạm vi quyền được cấp; nhật ký lệnh", "Thực hiện tác vụ người dùng yêu cầu, kiểm toán"],
        ]) + "<p>Dữ liệu khuôn mặt, sinh trắc học chỉ được xử lý khi bên kiểm soát có căn cứ pháp lý và đã thông báo/thu thập sự đồng ý theo quy định đối với dữ liệu cá nhân nhạy cảm.</p>"),
        ("Thời hạn lưu trữ (Data Retention)", tbl(["Dữ liệu", "Thời hạn mặc định"], [
            ["Video giám sát thô", "Theo cấu hình của bên kiểm soát và quy chuẩn chuyên ngành; mặc định 30 ngày rồi ghi đè"],
            ["Ảnh/clip sự kiện đã trích", "Đến khi hồ sơ nghiệp vụ liên quan được xử lý xong, tối đa theo yêu cầu bên kiểm soát"],
            ["Dữ liệu đặt lịch", "Trong thời gian cung cấp dịch vụ và thời hạn lưu chứng từ kế toán theo luật"],
            ["Yêu cầu liên hệ", "Tối đa 24 tháng kể từ lần trao đổi cuối"],
            ["Audit Log MCP", "Tối thiểu 12 tháng hoặc theo hợp đồng"],
        ])),
        ("Ẩn danh hoá và làm mờ (Anonymization)", ul("Tự động làm mờ khuôn mặt, biển số trong ảnh/clip khi chia sẻ ra ngoài phạm vi nghiệp vụ, khi trình diễn hoặc đào tạo.", "Báo cáo thống kê chỉ dùng dữ liệu tổng hợp, không nhận dạng được cá nhân.", "Tài liệu, ảnh chụp màn hình công bố trên website dùng dữ liệu giả lập.")),
        ("Chia sẻ dữ liệu", ul("Không bán dữ liệu cá nhân.", "Chỉ chia sẻ cho: bên kiểm soát dữ liệu (khách hàng); nhà cung cấp hạ tầng, thông báo, thanh toán ký cam kết bảo mật; cơ quan nhà nước có thẩm quyền theo yêu cầu hợp pháp.", "Chuyển dữ liệu ra nước ngoài chỉ khi đáp ứng điều kiện và hồ sơ đánh giá tác động theo quy định.")),
        ("Biện pháp bảo vệ", ul("Mã hoá khi truyền và khi lưu; quản lý khoá tách biệt.", "Phân quyền RBAC, nguyên tắc đặc quyền tối thiểu; xác thực mạnh cho quản trị viên.", "Nhật ký truy cập, xem, tải dữ liệu; giám sát và cảnh báo bất thường.", "Lưu trữ tại Việt Nam; lựa chọn On-Premise/Private Cloud.", "Thông báo vi phạm dữ liệu cho bên kiểm soát và cơ quan chuyên trách trong thời hạn luật định.")),
        ("Quyền của chủ thể dữ liệu", "<p>Chủ thể dữ liệu có quyền được biết, đồng ý, rút lại sự đồng ý, truy cập, chỉnh sửa, xoá, hạn chế xử lý, phản đối xử lý, yêu cầu cung cấp dữ liệu, khiếu nại, tố cáo và yêu cầu bồi thường theo quy định.</p>"),
        ("Quy trình tiếp nhận yêu cầu xoá dữ liệu", "<ol><li>Gửi yêu cầu qua " + contact + ", nêu rõ dữ liệu và lý do.</li><li>TORITECH xác minh danh tính người yêu cầu.</li><li>Nếu TORITECH là bên kiểm soát: xử lý và phản hồi trong thời hạn luật định. Nếu là bên xử lý: chuyển yêu cầu tới bên kiểm soát (cơ quan/doanh nghiệp liên quan) và hỗ trợ thực hiện.</li><li>Thông báo kết quả; trường hợp không thể xoá (nghĩa vụ lưu trữ theo luật, hồ sơ xử phạt đang giải quyết…) sẽ nêu rõ căn cứ.</li></ol>"),
        ("Đầu mối bảo vệ dữ liệu cá nhân", f"<p>Bộ phận/nhân sự bảo vệ dữ liệu cá nhân của {name}. Liên hệ: {contact}.</p>"),
    ]))

    # 3. AI & MCP security policy
    out.append(("chinh-sach-bao-mat-ai-mcp.html", "Chính sách bảo mật & quản trị AI / MCP",
                "Cam kết Zero Data Training, xác thực OAuth/API key, Audit Log và Human-in-the-loop cho MCP Server và AI Agent của TORITECH.",
                "Giải đáp lo ngại lớn nhất của doanh nghiệp: AI tự ý sửa/xoá dữ liệu hoặc làm rò rỉ bí mật kinh doanh qua MCP Server.", [
        ("Nguyên tắc", ul("AI Agent chỉ làm những gì người dùng yêu cầu, trong phạm vi quyền được cấp.", "Mặc định chỉ đọc; quyền ghi được cấp riêng, có thời hạn, có phê duyệt.", "Mọi hành động đều truy vết được.")),
        ("Zero Data Training", "<p>Dữ liệu của khách hàng, dữ liệu truy xuất qua MCP, nội dung hội thoại và nhật ký <b>không được TORITECH dùng để huấn luyện, tinh chỉnh hay đánh giá mô hình AI</b>. Khi khách hàng dùng dịch vụ LLM của bên thứ ba (Claude, ChatGPT, Gemini, Copilot…), việc xử lý phía nhà cung cấp LLM tuân theo điều khoản của nhà cung cấp đó và cấu hình tài khoản của khách hàng; TORITECH khuyến nghị dùng gói doanh nghiệp có cam kết không huấn luyện trên dữ liệu.</p>"),
        ("Xác thực và phân quyền", ul("OAuth 2.0 hoặc API key riêng cho từng khách hàng/người dùng; có thể thu hồi tức thì.", "RBAC theo từng công cụ (tool) và phạm vi dữ liệu (đơn vị, mã số, kho, kỳ).", "Không lưu mật khẩu cổng dịch vụ công dạng đọc được; ưu tiên cơ chế phiên/uỷ quyền do người dùng cấp.", "Giới hạn tần suất gọi để ngăn lạm dụng.")),
        ("Human-in-the-loop", "<p>Các lệnh có tác động – ghi, sửa, xoá dữ liệu ERP/kế toán, gửi văn bản ra ngoài, thanh toán, nộp hồ sơ – phải được người có thẩm quyền xác nhận trước khi thực thi. Khách hàng cấu hình danh mục lệnh cần duyệt và người duyệt.</p>"),
        ("Nhật ký kiểm toán (Audit Log)", ul("Ghi lại: người dùng, AI client, công cụ được gọi, tham số (đã che thông tin nhạy cảm), kết quả, thời điểm, người phê duyệt.", "Nhật ký chỉ ghi thêm, không sửa; khách hàng được truy xuất và xuất báo cáo.")),
        ("Phòng chống rủi ro đặc thù AI", ul("Lọc chỉ dẫn độc hại trong dữ liệu đầu vào (prompt injection); nội dung lấy từ nguồn ngoài được coi là dữ liệu, không phải mệnh lệnh.", "Không trả về key, token, mật khẩu trong kết quả.", "Phân tách dữ liệu giữa các khách hàng (multi-tenant isolation).")),
        ("Sự cố", "<p>Khi phát hiện sự cố an ninh liên quan MCP, TORITECH thu hồi key bị ảnh hưởng, khoanh vùng, thông báo khách hàng và phối hợp xử lý; báo cáo theo quy định về bảo vệ dữ liệu cá nhân nếu có dữ liệu cá nhân bị ảnh hưởng.</p>"),
    ]))

    # 4. Government data disclaimer
    out.append(("mien-tru-trach-nhiem-dich-vu-cong.html", "Tuyên bố miễn trừ trách nhiệm dữ liệu dịch vụ công",
                "Phân định vai trò trung gian công nghệ của TORITECH khi cung cấp MCP tra cứu dịch vụ công.",
                "TORITECH cung cấp công cụ hỗ trợ kết nối và tổng hợp thông tin từ cổng dịch vụ công để tối ưu trải nghiệm người dùng.", [
        ("Vai trò trung gian công nghệ", "<p>TORITECH <b>không phải là cơ quan nhà nước</b>, không đại diện và không phát ngôn thay cho BHXH Việt Nam, cơ quan thuế, Cục Cảnh sát giao thông, Cục Đăng kiểm hay bất kỳ cơ quan nào. Các connector chỉ thao tác trên tài khoản mà chính người dùng được cấp hợp pháp.</p>"),
        ("Nguồn dữ liệu", "<p>Dữ liệu gốc thuộc về và phụ thuộc vào cổng thông tin chính thức của cơ quan nhà nước <b>tại thời điểm truy vấn</b>. Kết quả do AI tổng hợp chỉ mang tính hỗ trợ; khi có khác biệt, thông tin trên cổng chính thức và văn bản của cơ quan có thẩm quyền là căn cứ.</p>"),
        ("Gián đoạn và thay đổi", "<p>Cổng dịch vụ công có thể bảo trì, thay đổi giao diện hoặc giới hạn truy cập. TORITECH không chịu trách nhiệm về gián đoạn hay sai lệch phát sinh từ phía cổng, nhưng sẽ cập nhật connector trong thời gian hợp lý.</p>"),
        ("Trách nhiệm của người dùng", ul("Chỉ sử dụng tài khoản, mã đơn vị mình được quyền truy cập.", "Kiểm tra lại thông tin trước khi dùng cho kê khai, nộp tiền, quyết định pháp lý.", "TORITECH không yêu cầu chuyển tiền vào tài khoản cá nhân dưới danh nghĩa cơ quan nhà nước.")),
    ]))

    # 5. DPA
    out.append(("thoa-thuan-xu-ly-du-lieu-dpa.html", "Thỏa thuận xử lý dữ liệu (DPA)",
                "Mẫu Thỏa thuận xử lý dữ liệu giữa khách hàng (bên kiểm soát) và TORITECH (bên xử lý) cho VMS, SaaS đặt lịch và MCP.",
                f"Mẫu điều khoản áp dụng khi TORITECH xử lý dữ liệu cá nhân thay cho khách hàng, căn cứ {LAWS}; tham chiếu GDPR với khách hàng có yếu tố quốc tế.", [
        ("Các bên và phạm vi", "<p><b>Bên kiểm soát:</b> khách hàng (cơ quan, doanh nghiệp) quyết định mục đích và phương tiện xử lý. <b>Bên xử lý:</b> " + name + ". Phạm vi: dữ liệu khách hàng đưa lên VMS, nền tảng đặt lịch, hoặc kết nối qua MCP trong thời hạn hợp đồng.</p>"),
        ("Nghĩa vụ của bên xử lý", ul("Chỉ xử lý theo chỉ dẫn bằng văn bản của bên kiểm soát.", "Bảo đảm nhân sự tiếp cận dữ liệu có cam kết bảo mật.", "Áp dụng biện pháp kỹ thuật, tổ chức phù hợp (mã hoá, RBAC, nhật ký, sao lưu).", "Hỗ trợ bên kiểm soát thực hiện quyền của chủ thể dữ liệu và đánh giá tác động.", "Thông báo cho bên kiểm soát khi phát hiện vi phạm dữ liệu, không chậm trễ quá thời hạn luật định.", "Không dùng dữ liệu cho mục đích riêng, kể cả huấn luyện AI.")),
        ("Bên xử lý phụ", "<p>TORITECH chỉ sử dụng bên xử lý phụ (hạ tầng đám mây tại Việt Nam, dịch vụ thông báo, thanh toán) đã được thông báo cho bên kiểm soát và ràng buộc nghĩa vụ tương đương. Bên kiểm soát được phản đối việc thay đổi bên xử lý phụ.</p>"),
        ("Vị trí dữ liệu và chuyển ra nước ngoài", "<p>Dữ liệu được lưu trữ tại Việt Nam. Không chuyển ra nước ngoài nếu không có chấp thuận của bên kiểm soát và hồ sơ theo quy định.</p>"),
        ("Kiểm tra, đánh giá", "<p>Bên kiểm soát được yêu cầu báo cáo, bằng chứng tuân thủ và kiểm tra định kỳ với thông báo trước hợp lý.</p>"),
        ("Kết thúc xử lý", "<p>Khi hợp đồng chấm dứt, TORITECH trả lại dữ liệu theo định dạng thông dụng và/hoặc xoá toàn bộ bản sao trong thời hạn thỏa thuận, trừ dữ liệu phải lưu theo luật; có biên bản xác nhận.</p>"),
        ("Phụ lục", tbl(["Phụ lục", "Nội dung"], [["A", "Mô tả hoạt động xử lý: loại dữ liệu, chủ thể, mục đích, thời hạn"], ["B", "Biện pháp kỹ thuật và tổ chức"], ["C", "Danh sách bên xử lý phụ"]]) + '<p>Bản DPA để ký được cung cấp theo yêu cầu: <a href="lien-he.html?topic=hoso">liên hệ</a>.</p>'),
    ]))

    # 6. SLA
    out.append(("cam-ket-chat-luong-sla.html", "Cam kết chất lượng dịch vụ (SLA) & Quy chuẩn kỹ thuật",
                "Khung cam kết Uptime, thời gian phản hồi sự cố, RTO/RPO, sao lưu và tiêu chuẩn kỹ thuật áp dụng cho dịch vụ TORITECH.",
                "Hệ thống camera giám sát và đặt lịch hẹn phải hoạt động liên tục. Trang này nêu khung cam kết tham chiếu; mức chính thức được ghi trong Phụ lục SLA của hợp đồng.", [
        ("Mức sẵn sàng (Uptime)", tbl(["Gói", "Uptime mục tiêu/tháng", "Ghi chú"], [["Tiêu chuẩn", "99,5%", "SaaS dùng chung"], ["Doanh nghiệp", "99,9%", "Hạ tầng dự phòng, giám sát 24/7"], ["On-Premise", "Theo thiết kế hạ tầng của khách hàng", "TORITECH cam kết phần mềm và thời gian hỗ trợ"]]) + "<p>Không tính thời gian bảo trì có kế hoạch đã thông báo trước tối thiểu 48 giờ và sự cố do hạ tầng/thiết bị của khách hàng hoặc bên thứ ba (cổng dịch vụ công, nhà mạng).</p>"),
        ("Phân loại và thời gian phản hồi sự cố", tbl(["Mức", "Mô tả", "Phản hồi", "Khắc phục / giải pháp tạm"], [
            ["P1 – Nghiêm trọng", "Ngừng dịch vụ diện rộng, mất dữ liệu", "≤ 30 phút", "≤ 4 giờ"],
            ["P2 – Cao", "Một chức năng chính lỗi, có cách làm tạm", "≤ 2 giờ", "≤ 1 ngày làm việc"],
            ["P3 – Trung bình", "Lỗi không ảnh hưởng vận hành chính", "≤ 1 ngày làm việc", "Theo kế hoạch phát hành"],
        ])),
        ("Sao lưu và khôi phục", tbl(["Chỉ số", "Mục tiêu (gói Doanh nghiệp)"], [["RPO – mất dữ liệu tối đa", "≤ 15 phút đối với dữ liệu đặt lịch, sự kiện; video theo cấu hình lưu trữ"], ["RTO – thời gian khôi phục", "≤ 4 giờ"], ["Sao lưu", "Hằng ngày, lưu tại vị trí tách biệt trong lãnh thổ Việt Nam, kiểm thử khôi phục định kỳ"]])),
        ("Báo cáo và bồi hoàn", "<p>Khách hàng nhận báo cáo SLA định kỳ. Khi không đạt mức cam kết, khách hàng được bồi hoàn bằng tín dụng dịch vụ theo tỷ lệ quy định trong Phụ lục SLA.</p>"),
        ("Tiêu chuẩn & quy chuẩn kỹ thuật áp dụng", ul("QCVN 103:2024/BGTVT – yêu cầu hình ảnh giám sát tại cơ sở đăng kiểm (đối với giải pháp camera đăng kiểm).", "ONVIF Profile S/T, RTSP – kết nối camera, đầu ghi.", "Model Context Protocol (MCP), OAuth 2.0, TLS.", f"{LAWS}.", "Luật Dữ liệu số 60/2024/QH15; Luật Giao dịch điện tử số 20/2023/QH15.")),
    ]))

    # 7. Payment & refund
    out.append(("chinh-sach-thanh-toan-hoan-huy.html", "Chính sách thanh toán, hoàn huỷ & gia hạn",
                "Phương thức thanh toán, hoá đơn điện tử, điều kiện hoàn tiền, gia hạn và xử lý quá hạn cho dịch vụ TORITECH.",
                "Áp dụng cho gói dịch vụ đăng ký trực tuyến và hợp đồng dịch vụ của TORITECH.", [
        ("Phương thức thanh toán", ul(f"Chuyển khoản vào tài khoản doanh nghiệp đứng tên {name}.", "Cổng thanh toán, ví điện tử được tích hợp tại thời điểm đăng ký (nếu có).", "TORITECH không yêu cầu chuyển tiền vào tài khoản cá nhân.")),
        ("Hoá đơn điện tử", "<p>TORITECH xuất hoá đơn điện tử theo quy định về hoá đơn, chứng từ sau khi nhận thanh toán; thông tin xuất hoá đơn do khách hàng cung cấp.</p>"),
        ("Gia hạn", ul("Gói theo tháng/năm được thông báo gia hạn trước ngày hết hạn.", "Tự động gia hạn chỉ áp dụng khi khách hàng đã bật tuỳ chọn này.", "Quá hạn thanh toán: dịch vụ có thể bị giới hạn sau thời gian ân hạn đã thông báo; dữ liệu được giữ theo DPA.")),
        ("Huỷ gói và hoàn tiền", ul("Khách hàng có thể huỷ trước kỳ gia hạn tiếp theo.", "Hoàn tiền toàn bộ nếu TORITECH không kích hoạt được dịch vụ trong 03 ngày làm việc kể từ khi nhận thanh toán.", "Hoàn tiền theo tỷ lệ thời gian chưa sử dụng nếu TORITECH ngừng cung cấp dịch vụ hoặc dịch vụ gián đoạn kéo dài vượt mức SLA.", "Thời gian hoàn tiền: tối đa 15 ngày làm việc qua phương thức thanh toán ban đầu.")),
        ("Bảo vệ người tiêu dùng", "<p>Chính sách được áp dụng phù hợp Luật Bảo vệ quyền lợi người tiêu dùng số 19/2023/QH15 và Luật Thương mại điện tử số 122/2025/QH15. Khiếu nại gửi qua " + contact + ".</p>"),
    ]))

    # 8. Cookie
    out.append(("chinh-sach-cookie.html", "Chính sách Cookie",
                "Website TORITECH chỉ dùng cookie/bộ nhớ trình duyệt thiết yếu và không cài mã theo dõi quảng cáo.",
                "Giải thích loại cookie, bộ nhớ trình duyệt website sử dụng và cách bạn kiểm soát.", [
        ("Cookie website đang dùng", tbl(["Loại", "Mục đích", "Trạng thái"], [["Thiết yếu", "Ghi nhớ lựa chọn cookie (localStorage: tori-cookie-v1)", "Luôn bật"], ["Phân tích (Analytics)", "Đo lượt truy cập", "Không sử dụng"], ["Tiếp thị (Marketing)", "Quảng cáo, theo dõi chéo trang", "Không sử dụng"]]) + "<p>Font chữ được tải từ Google Fonts; nhà cung cấp có thể ghi nhận địa chỉ IP kỹ thuật khi tải font. Các nút chia sẻ chỉ mở trang của mạng xã hội khi bạn bấm.</p>"),
        ("Video tạo trên trình duyệt", "<p>Tính năng “Xuất MP4” dựng video ngay trên thiết bị của bạn; video không được tải lên máy chủ của TORITECH.</p>"),
        ("Kiểm soát", '<p>Bạn có thể thay đổi lựa chọn bất kỳ lúc nào bằng nút <button type="button" class="tool" data-cookie-reset>Tuỳ chọn cookie</button> hoặc xoá dữ liệu trang trong cài đặt trình duyệt.</p>'),
        ("Cập nhật", "<p>Nếu website bổ sung công cụ phân tích hoặc tiếp thị, banner đồng ý sẽ yêu cầu bạn chọn trước khi kích hoạt, và chính sách này được cập nhật.</p>"),
    ]))
    return out
