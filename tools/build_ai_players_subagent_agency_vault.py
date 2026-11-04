#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_ai_players_subagent_agency_vault.py — Chuyển Đổi Toàn Bộ Tuyến Nội Dung Hình Ảnh (04/11 - 06/11)
Page "AI Players - Người chơi hệ AI" (1022527194267367) sang Định Vị Mới:
  1. Đội ngũ Subagent Cá nhân Toàn diện (Personal All-in-One Subagent Team)
  2. Đội ngũ Subagent Doanh nghiệp (Enterprise / SME Multi-Agent Workforce)
  3. Dịch vụ Nhận Thiết kế & Xây dựng Đội ngũ Subagent May đo 1:1 cho Khách hàng Cá nhân & Doanh nghiệp
"""

import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SUBAGENT_DIR / "tools"))

from render_vid_style_card import render_html_to_image
from zero_repost_gate import verify_zero_clone_images, record_published_content
from mama_auto_scheduler_engine import load_vault, graph_get, graph_post, SSL_CTX
import build_bespoke_ai_players_day9_day10 as d910
import build_bespoke_ai_players_day11_day12 as d1112

AI_PAGE_ID = "1022527194267367"
ZALO_URL = "https://zalo.me/g/fzxvbf259"
VN_TZ = dt.timezone(dt.timedelta(hours=7))

OUT_ROOT = SUBAGENT_DIR / "campaigns" / "2026-11-04" / "ai-players-subagent-agency-vault"
IMAGES_DIR = OUT_ROOT / "images"
QA_GRID_PATH = OUT_ROOT / "subagent_agency_17_images_qa_grid.jpg"
MANIFEST_PATH = OUT_ROOT / "subagent_agency_17_images_manifest.json"


def update_seeding_and_pinned_templates() -> None:
    """Cập nhật kịch bản Seeding Hội Nhóm và Pinned Comment mặc định của Page AI sang định vị Subagent Agency."""
    new_ai_comments = [
        "Công nhận chia sẻ này chuẩn thực chiến luôn bác ạ! Dùng 1 con AI đơn lẻ ôm đồm hết mọi việc rất dễ bị loạn ngữ cảnh. Giải pháp chuẩn nhất là thiết lập một Đội ngũ Subagent Cá nhân Toàn diện (1 Tổng quản + các Subagent Thư ký, Nghiên cứu, Nội dung, Tài chính) — bên mình vừa ghim trọn bộ Sơ đồ Kiến trúc & Nhận thiết kế Đội ngũ Subagent may đo 1:1 cho Cá nhân/Doanh nghiệp ngay trên tường Page, bác nào cần bấm vào tên Page mình xem nhé!",
        "Chuẩn luôn bác ơi! Với các chủ shop và SME, thay vì thuê thêm nhân sự làm các việc lặp lại, hiện nay có thể triển khai Phòng ban Subagent Doanh nghiệp (Marketing đa kênh, CSKH 24/7, Kế toán đối soát, Nhân sự SOP) phối hợp tự động. Bên mình có chia sẻ bộ Blueprint mẫu & Nhận xây dựng Đội ngũ Subagent trọn gói theo quy trình riêng ngay trên tường Page, anh em bấm vào tên Page mình tham khảo nha!",
        "Đúng chủ đề nhiều anh em đang tìm kiếm! Một Hệ sinh thái Subagent Cá nhân Toàn diện khi gắn thêm 'Bộ não thứ 2' (Memory Vault) sẽ nhớ 100% phong cách làm việc, lịch trình và quy tắc riêng của chủ nhân mà không bao giờ lặp lại lỗi cũ. Mình có ghim sẵn bản thiết kế mẫu kèm dịch vụ Setup Đội ngũ Subagent may đo ngay bài đầu tiên trên tường Page, bác nào cần bấm vào tên Page mình xem nha!",
        "Góc nhìn rất sát thực tế! Bí quyết để giải phóng 80% thời gian cho CEO và Freelancer không phải là học hàng trăm công cụ rời rạc, mà là sở hữu một Đội ngũ Subagent chuyên môn hóa có cổng kiểm duyệt chéo (Hard Gate). Bên mình đang tặng miễn phí Bộ Khung 10 Subagent (.MD) và nhận tư vấn xây dựng Đội ngũ Subagent riêng cho từng doanh nghiệp ngay trên tường Page, anh em bấm vào tên Page mình nhận nhé!",
        "Bài viết chất lượng quá! Bổ sung thêm cho anh em: khi xây dựng Đội ngũ Subagent cho Doanh nghiệp, quan trọng nhất là nối thẳng vào Zalo/Telegram của sếp để điều khiển bằng ngôn ngữ tự nhiên mọi lúc mọi nơi. Toàn bộ mô hình Phòng ban Subagent 24/7 này bên mình đã đóng gói sẵn và nhận triển khai trọn gói ngay trên tường Page, bác nào quan tâm bấm vào tên Page mình tham khảo nhé!",
        "Đồng ý 100% với tác giả! Từ quản lý lịch trình cá nhân, đọc báo cáo chuyên sâu, viết nội dung đa kênh cho tới vận hành quy trình doanh nghiệp đều có thể bàn giao cho Đội ngũ Subagent chuyên trách. Mình vừa cập nhật trọn bộ giải pháp Thiết kế & Bàn giao Đội ngũ Subagent Cá nhân / Doanh nghiệp Toàn diện ngay trên tường Page, bác nào muốn áp dụng thực tế cứ bấm vào tên Page mình xem chi tiết nha!",
    ]
    from activate_mui3_mui4_growth_engine import NEW_COMMENTS_POOL
    NEW_COMMENTS_POOL["ai"] = new_ai_comments
    target_py = SUBAGENT_DIR / "tools" / "mama_daily_group_and_eod.py"
    code = target_py.read_text(encoding="utf-8")
    pool_str = "COMMENTS_POOL = " + json.dumps(NEW_COMMENTS_POOL, ensure_ascii=False, indent=4)
    new_code, n = re.subn(r"COMMENTS_POOL\s*=\s*\{.*?\n\}", lambda _: pool_str, code, count=1, flags=re.DOTALL)
    if n > 0:
        target_py.write_text(new_code, encoding="utf-8")

    sched_py = SUBAGENT_DIR / "tools" / "mama_auto_scheduler_engine.py"
    scode = sched_py.read_text(encoding="utf-8")
    scode = scode.replace(
        "https://zalo.me/g/etllok798 (Mã vào nhóm: AIPLAYERS2026) 🚀",
        f"{ZALO_URL} (Hoặc bình luận 'SETUP' để đăng ký Tư vấn & Thiết kế Đội ngũ Subagent Cá nhân / Doanh nghiệp may đo 1:1!) 🚀",
    )
    sched_py.write_text(scode, encoding="utf-8")
    print("✅ Đã cập nhật Kịch bản Seeding Hội Nhóm & Pinned Comment mặc định sang Định vị Subagent Agency.")


def _swap(html: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        html = html.replace(old, new)
    return html


# 17 Bespoke Subagent Agency Builders (kế thừa 17 kiến trúc không gian độc bản đã qua cổng < 58%)
def build_c01():
    return _swap(d910.card_26_isometric_virtual_office(), [
        ("🏢 VĂN PHÒNG ẢO 3D AGENT-JAVIS // PORT 4800", "🤖 HỆ SINH THÁI SUBAGENT CÁ NHÂN TOÀN DIỆN // ALL-IN-ONE"),
        ("QUAN SÁT 11 NHÂN SỰ AI LÀM VIỆC TRỰC TIẾP", "1 TRỢ LÝ TỔNG QUẢN + 6 SUBAGENT PHỤC VỤ RIÊNG BẠN"),
        ("3D LIVE VIEW", "PERSONAL TEAM"),
        ("PHÒNG CHỈ HUY", "TỔNG QUẢN MAMA"), ("Mama (Chief of Staff)", "Điều phối & Duyệt việc"),
        ("PHÒNG NGHIÊN CỨU", "SUBAGENT NGHIÊN CỨU"), ("MKT + Bộ Não Thứ 2", "Đọc báo cáo & Tóm tắt"),
        ("PHÒNG BIÊN KỊCH", "SUBAGENT NỘI DUNG"), ("Content + Đa Kênh", "Viết bài & Email chuẩn"),
        ("STUDIO ĐỒ HỌA 3D", "SUBAGENT TÀI CHÍNH & LỊCH"), ("Edit + Edit-2 (TVC)", "Nhắc việc & Quản lý chi tiêu"),
        ("PHÒNG THU ÂM", "BỘ NÃO THỨ 2 CÁ NHÂN"), ("Voice (-3dB Vbee)", "Ghi nhớ 100% thói quen"),
        ("⚡ ĐỒNG BỘ 2 CHIỀU VỚI ANTIGRAVITY IDE", "🎯 DỊCH VỤ THIẾT KẾ ĐỘI NGŨ SUBAGENT CÁ NHÂN MAY ĐO 1:1"),
        ("Ai đang gõ phím, ai đang duyệt bài, ai đang ra quán cà phê đều hiển thị thời gian thực!", "Giải phóng 80% việc lặp lại mỗi ngày cho CEO, Quản lý, Chuyên gia & Freelancer!"),
        ("11 AGENTS", "GÕ \"CANHAN\""), ("7 PHÒNG BAN CHUYÊN BIỆT", "TƯ VẤN SETUP 1:1"),
    ])

def build_c02():
    return _swap(d910.card_25_second_brain_gatekeeper(), [
        ("🛡️ LUẬT #10 // SECOND-BRAIN GATEKEEPER", "🏢 GIẢI PHÁP DOANH NGHIỆP // MULTI-AGENT WORKFORCE"),
        ("FINAL COMPLIANCE AUDITOR", "24/7 AUTONOMOUS DEPT"),
        ("CỔNG KIỂM DUYỆT <span style=\"color:#34D399;\">BỘ NÃO THỨ 2</span> CHỐNG DÙNG NHẦM KÝ ỨC CŨ", "XÂY DỰNG <span style=\"color:#34D399;\">4 PHÒNG BAN SUBAGENT</span> CHO DOANH NGHIỆP SME"),
        ("CHỐT CHẶN 01 // TRƯỚC KHI GIAO VIỆC", "PHÒNG BAN 01 // MARKETING ĐA KÊNH"),
        ("Đối chiếu Manifest Quy Tắc Mới Nhất", "Tự động nghiên cứu & sản xuất bài"),
        ("Tự động quét mọi Tab trò chuyện trên 2 máy để khóa chặt các chỉ đạo vừa cập nhật.", "Lên kịch bản, thiết kế hình ảnh độc bản và hẹn giờ xuất bản đa kênh 24/7."),
        ("VERDICT ENGINE v2.0", "PHÒNG BAN 02 & 03 // CHỦ LỰC"),
        ("APPROVED BY SECOND BRAIN ✓", "SALES CSKH & KẾ TOÁN SỐ LIỆU"),
        ("Chặn đứng 100% lệnh gọi mẫu cũ (5-template cũ, video bán hàng đang đóng băng, hoặc lộ thông tin nhạy cảm).", "Phản hồi khách hàng tức thì 24/7, tự động đối soát đơn hàng, chi phí và báo cáo doanh thu mỗi sáng."),
        ("0% RỦI RO TÁI SỬ DỤNG CODE CŨ", "TIẾT KIỆM 80% CHI PHÍ VẬN HÀNH"),
        ("CHỐT CHẶN 02 // NGƯỜI DUYỆT CUỐI CÙNG", "PHÒNG BAN 04 // NHÂN SỰ & ĐÀO TẠO"),
        ("Kiểm tra đầu ra của 9 Subagent", "Trợ lý SOP đào tạo nhân viên mới"),
        ("✔ Kiểm tra độ độc bản &lt; 58%", "✔ Nắm vững 100% quy chế công ty"),
        ("✔ Khóa Tường Lửa Tách Tệp", "✔ Kiểm duyệt đầu ra đạt chuẩn ≥ 9.0"),
        ("BÌNH LUẬN \"GATEKEEPER\" NHẬN CODE", "BÌNH LUẬN \"DOANHNGHIEP\" TƯ VẤN"),
        ("TỐC ĐỘ KIỂM DUYỆT", "HIỆU SUẤT PHÒNG BAN"), ("0.15s", "24/7"), ("CHUẨN MỚI", "TỰ ĐỘNG"),
    ])

def build_c03():
    return _swap(d910.card_28_structured_json_schema(), [
        ("🔒 BÍ QUYẾT NỐI AI VÀO DATABASE KHÔNG BAO GIỜ LỖI", "🚀 DỊCH VỤ XÂY DỰNG ĐỘI NGŨ SUBAGENT TRỌN GÓI A-Z"),
        ("ÉP KHUÔN <span style=\"color:#38BDF8;\">100% JSON SCHEMA</span> CHO MỌI TÁC NHÂN AI", "NHẬN THIẾT KẾ <span style=\"color:#38BDF8;\">ĐỘI NGŨ SUBAGENT</span> CÁ NHÂN &amp; DOANH NGHIỆP"),
        ("schema_validator.json — Strict Mode: TRUE", "custom_subagent_team_blueprint.json — May Đo 1:1"),
        ("0% SYNTAX ERROR", "BÀN GIAO TRỌN GÓI"),
        ("\"verdict\"", "\"buoc_1_khao_sat\""), ("\"APPROVED_BY_GATEKEEPER\"", "\"Phân tích quy trình & Nỗi đau thực tế\""),
        ("\"rubric_score\"", "\"buoc_2_kien_truc\""), ("9.6", "\"Thiết kế Tổng quản + Đội Subagent chuyên môn\""),
        ("\"zero_clone_similarity\"", "\"buoc_3_bo_nao_thu_2\""), ("0.31", "\"Nạp tài liệu, SOP & Phong cách cá nhân\""),
        ("\"pinned_comment_ready\"", "\"buoc_4_dau_noi_kenh\""), ("true", "\"Tích hợp Zalo, Telegram, Fanpage, Excel\""),
        ("\"required_fields_locked\"", "\"buoc_5_ban_giao\""), ("[\"hook_3s\", \"cta_url\", \"sub_id\"]", "\"Cầm tay chỉ việc & Bảo hành vận hành\""),
        ("Cấm Bịa Thêm Trường Lạ", "Thiết Kế May Đo 100%"),
        ("Khóa chặt thuộc tính bổ sung, nạp thẳng vào SQLite &amp; n8n.", "Xây dựng đúng theo ngành nghề, dữ liệu và thói quen của riêng bạn."),
        ("Ép Kiểu Dữ Liệu Cứng", "Sở Hữu Vĩnh Viễn"),
        ("Số tiền, khung giờ, mã SKU luôn đúng định dạng 100%.", "Bàn giao toàn bộ mã nguồn, file cấu hình .MD và Bộ não thứ 2."),
    ])

def build_c04():
    return _swap(d910.card_33_code_sandbox_loop(), [
        ("🐍 CODE INTERPRETER SANDBOX THỰC CHIẾN", "👑 VAI TRÒ CỦA TRỢ LÝ TỔNG QUẢN (MAMA CHIEF OF STAFF)"),
        ("ĐỪNG ĐỂ AI TÍNH NHẨM: HÃY CHO NÓ <span style=\"color:#2DD4BF;\">TỰ CHẠY CODE PYTHON</span>", "CHỈ CẦN GIAO 1 LỆNH: <span style=\"color:#2DD4BF;\">TỔNG QUẢN TỰ ĐIỀU PHỐI</span> CẢ ĐỘI"),
        ("1. AI Tự Viết Script", "1. Nhận Lệnh Từ Sếp"),
        ("2. Chạy Trong Hộp Cát Cô Lập", "2. Chia Việc Cho Các Subagent"),
        ("3. Tự Sửa Lỗi &amp; Xuất Biểu Đồ", "3. Duyệt Chéo &amp; Báo Cáo Kết Quả"),
        ("CHÍNH XÁC 100% SỐ LIỆU TÀI CHÍNH", "CHẤM ĐIỂM RUBRIC ≥ 9.0 MỚI TRÌNH SẾP"),
        ("ƯU ĐIỂM 01 // XỬ LÝ FILE EXCEL 100,000 DÒNG", "NHIỆM VỤ 01 // PHÂN RÃ MỤC TIÊU TỰ ĐỘNG"),
        ("Không bị tràn ngữ cảnh LLM", "Biến 1 yêu cầu ngắn thành kế hoạch chi tiết"),
        ("Dùng Pandas lọc và tính tổng trực tiếp trong 0.5 giây.", "Tự động xác định Subagent nào cần chạy trước, Subagent nào chạy song song."),
        ("ƯU ĐIỂM 02 // CƠ CHẾ TỰ BẮT LỖI (SELF-DEBUG)", "NHIỆM VỤ 02 // CỔNG KIỂM DUYỆT CHẤT LƯỢNG"),
        ("Đọc Traceback và tự viết lại code", "Bắt lỗi và yêu cầu Subagent làm lại ngay"),
        ("Không cần con người can thiệp khi gặp dữ liệu khuyết thiếu.", "Bạn không còn phải tự mình đọc sửa từng bản nháp sơ sài của AI."),
        ("ƯU ĐIỂM 03 // AN TOÀN TUYỆT ĐỐI", "NHIỆM VỤ 03 // ĐỒNG BỘ BÁO CÁO ĐA MÁY"),
        ("Môi trường cô lập không chạm ổ cứng chính", "Gửi báo cáo ngắn gọn 4-8 dòng qua Telegram"),
        ("Bảo vệ toàn vẹn hệ thống dữ liệu doanh nghiệp.", "Giúp bạn nắm trọn tiến độ công việc dù đang ở văn phòng hay ở nhà."),
    ])

def build_c05():
    return _swap(d910.card_36_prompt_injection_shield(), [
        ("🛡️ BẢO MẬT TÁC NHÂN AI DOANH NGHIỆP", "🧠 KIẾN TRÚC SUBAGENT \"BỘ NÃO THỨ 2\" CÁ NHÂN &amp; DOANH NGHIỆP"),
        ("3 VÒNG KHIÊN CHẶN ĐỨNG <span style=\"color:#EF4444;\">PROMPT INJECTION</span>", "3 TẦNG TRÍ NHỚ GIÚP <span style=\"color:#EF4444;\">ĐỘI SUBAGENT</span> KHÔNG QUÊN"),
        ("LÕI DỮ LIỆU<br>AN TOÀN", "BỘ NÃO<br>THỨ 2"),
        ("VÒNG 01 // LỌC ĐẦU VÀO (INPUT GUARD)", "TẦNG 01 // GHI NHỚ TỨC THỜI MỌI CHỈ ĐẠO"),
        ("Chặn câu lệnh gài bẫy \"Hãy quên mọi chỉ dẫn trước đó\"", "Mỗi khi bạn nhắc nhở quy tắc mới, Subagent tự động lưu vào sổ tay vĩnh viễn"),
        ("VÒNG 02 // PHÂN QUYỀN TỐI THIỂU", "TẦNG 02 // CHUẨN HÓA HỒ SƠ &amp; QUY TRÌNH"),
        ("Chatbot CSKH chỉ có quyền đọc bảng giá, cấm quyền sửa/xóa DB", "Lưu trữ toàn bộ văn phong cá nhân, danh mục sản phẩm và quy trình SOP"),
        ("VÒNG 03 // KIỂM DUYỆT ĐẦU RA", "TẦNG 03 // KIỂM DUYỆT CHỐNG LẶP LẠI LỖI CŨ"),
        ("Quét ẩn toàn bộ API Key, Token &amp; dữ liệu nhạy cảm", "Đối chiếu lịch sử trước khi xuất bản để đảm bảo đúng ý chủ nhân 100%"),
        ("🔒 TUÂN THỦ LUẬT BẢO MẬT ZERO-LEAKS", "🎯 NHẬN XÂY DỰNG BỘ NÃO THỨ 2 &amp; ĐỘI NGŨ SUBAGENT RIÊNG"),
        ("Đừng triển khai AI cho khách hàng nếu chưa lắp 3 lớp rào chắn bảo mật này!", "Càng làm việc cùng bạn lâu, Đội ngũ Subagent càng hiểu rõ phong cách của bạn!"),
        ("NHẬN BỘ RULE<br>BẢO MẬT AI", "GÕ \"BONAO\"<br>TƯ VẤN NGAY"),
    ])

def build_c06():
    return _swap(d1112.card_37_mobile_cloudflare_tunnel(), [
        ("📱 MOBILE COMMAND // CLOUDFLARED HTTPS TUNNEL", "📱 ĐIỀU HÀNH TỪ XA // MOBILE SUBAGENT COMMAND CENTER"),
        ("ZERO PORT-FORWARDING", "ZALO & TELEGRAM 24/7"),
        ("ĐIỀU KHIỂN <span style=\"color:#22D3EE;\">VĂN PHÒNG 3D AI</span> TRÊN ĐIỆN THOẠI MỌI LÚC MỌI NƠI", "CHỈ HUY <span style=\"color:#22D3EE;\">ĐỘI NGŨ SUBAGENT</span> TRÊN ĐIỆN THOẠI MỌI LÚC MỌI NƠI"),
        ("11 AGENT 3D", "ĐỘI SUBAGENT"),
        ("Pin 1 dòng gọn nhẹ + Cụm phím D-Pad nổi bên phải", "Giao diện trực quan trên điện thoại + Kết nối Telegram 2 chiều"),
        ("Cuộn mượt 60fps • Gửi lệnh trực tiếp vào Antigravity", "Nhắn 1 câu tự nhiên • Cả đội Subagent tự động phối hợp chạy việc"),
        ("TẦNG 01 // AUTO-START BOOTSTRAP", "TIỆN ÍCH 01 // RA LỆNH KHI ĐANG DI CHUYỂN"),
        ("Mở máy là tự bật ngầm 100%", "Đang ngồi cà phê vẫn điều hành công việc"),
        ("TẦNG 02 // CLOUDFLARED TRYCLOUDFLARE", "TIỆN ÍCH 02 // ĐỒNG BỘ MÁY CÔNG TY & MÁY NHÀ"),
        ("Tự động cấp phát đường hầm SSL", "Mạch công việc liền mạch 100% giữa 2 nơi"),
        ("BÌNH LUẬN NHẬN SCRIPT", "ĐẶT LỊCH THIẾT KẾ RIÊNG"),
        ("GÕ \"TUNNEL\"", "GÕ \"MOBILE\""),
        ("Tặng trọn bộ code bật Văn phòng 3D online trên điện thoại!", "Nhận tư vấn xây dựng Đội ngũ Subagent điều khiển qua điện thoại!"),
    ])

def build_c07():
    return _swap(d1112.card_38_ram_transcript_cache(), [
        ("⚡ KỸ THUẬT TỐI ƯU BACKEND // RAM TRANSCRIPT CACHE", "⚡ SO SÁNH THỰC CHIẾN // 1 AI ĐƠN LẺ VS ĐỘI NGŨ SUBAGENT"),
        ("GIẢM THỜI GIAN TẢI CHAT TỪ <span style=\"color:#F87171;\">3.2 GIÂY</span> XUỐNG <span style=\"color:#A3E635;\">18ms</span>", "TẠI SAO <span style=\"color:#F87171;\">1 CHATGPT ĐƠN LẺ</span> HAY SAI CÒN <span style=\"color:#A3E635;\">ĐỘI SUBAGENT</span> THẮNG LỚN?"),
        ("177× FASTER", "CHUẨN 100%"),
        ("❌ CÁCH CŨ: Đọc lại file .jsonl từ ổ cứng mỗi 3.5 giây", "❌ CÁCH CŨ: Nhồi nhét 10 việc vào 1 cửa sổ chat duy nhất"),
        ("3.200 ms (Đơ giao diện)", "Loạn ngữ cảnh & Quên quy tắc"),
        ("✅ CÁCH MỚI: Kiểm tra mtime + size trong RAM & Bundled Snapshot", "✅ CÁCH MỚI: Tách thành Đội ngũ Subagent chuyên môn hóa có Tổng quản"),
        ("18 ms (Tức thì)", "Chính xác & Tự động hóa 80%"),
        ("BƯỚC 01", "TRỤ CỘT 01"), ("Khóa chữ ký mtime & byte size", "Chuyên môn hóa từng vị trí"),
        ("Nếu file log chưa có dòng mới, trả thẳng kết quả từ bộ nhớ RAM trong 0.001 giây mà không mở file.", "Mỗi Subagent chỉ tập trung làm 1 nghề giỏi nhất: Nghiên cứu, Viết bài, Thiết kế hoặc Kiểm toán."),
        ("0 DISK I/O", "CHUYÊN SÂU"),
        ("BƯỚC 02", "TRỤ CỘT 02"), ("Gộp chung vào gói /api/snapshot", "Cổng kiểm duyệt chéo độc lập"),
        ("Loại bỏ hoàn toàn vòng lặp gọi API phụ trên điện thoại, mở khung chat là có sẵn tin nhắn ngay lập tức.", "Subagent Kiểm duyệt tự động rà soát chất lượng đầu ra của các Subagent khác trước khi bàn giao."),
        ("1 REQUEST", "HARD GATE"),
        ("BƯỚC 03", "TRỤ CỘT 03"), ("Chống giật vị trí cuộn DOM", "Nhận Thiết Kế Đội Ngũ May Đo"),
        ("Chỉ cập nhật HTML khi chữ ký tin nhắn thực sự thay đổi, giúp vuốt đọc lịch sử dài mượt như ứng dụng gốc.", "Chúng tôi khảo sát và xây dựng trọn gói Đội ngũ Subagent riêng cho Cá nhân & Doanh nghiệp của bạn."),
        ("CMT \"RAMCACHE\" NHẬN CODE", "CMT \"SUBAGENT\" TƯ VẤN"),
    ])

def build_c08():
    return _swap(d1112.card_39_outlier_post_finder(), [
        ("🔥 SOCIAL INTELLIGENCE // OUTLIER POST FINDER", "💼 ĐỘI NGŨ SUBAGENT PHÒNG SALES & CSKH TỰ ĐỘNG 24/7"),
        ("CÔNG THỨC SĂN VIDEO <span style=\"color:#FB7185;\">ĐỘT BIẾN GẤP 5 LẦN</span> MỨC TRUNG VỊ", "TĂNG <span style=\"color:#FB7185;\">+240% TỶ LỆ CHỐT ĐƠN</span> NHỜ ĐỘI SUBAGENT TRỰC PAGE 24/7"),
        ("MỨC NỀN TRUNG VỊ (MEDIAN BASELINE = 1.0x)", "PHẢN HỒI KHÁCH HÀNG TRONG 3 GIÂY (24/7/365)"),
        ("HUGE OUTLIER (≥ 5.0x)", "CHỐT ĐƠN +240%"),
        ("Lift Score = Lượt xem bài đăng ÷ Trung vị 20 bài gần nhất", "Tự động bắt bình luận + Gửi báo giá chuẩn + Nhắc lịch chăm sóc khách cũ"),
        ("TẠI SAO DÙNG TRUNG VỊ?", "SUBAGENT TRỰC BÌNH LUẬN"),
        ("Không bị 1 bài siêu viral làm lệch chuẩn", "Không bỏ sót 1 khách hỏi giá nào lúc nửa đêm"),
        ("Giúp phát hiện kênh nhỏ nhưng có bài nổ gấp 8 lần bình thường.", "Tự động nhận diện nhu cầu mua và phản hồi đúng sản phẩm khách đang hỏi."),
        ("NGƯỠNG ĐÁNH GIÁ", "SUBAGENT TƯ VẤN KỊCH BẢN"),
        ("≥ 2.0x: Strong Outlier<br>≥ 5.0x: Huge Outlier", "Xử lý từ chối khéo léo<br>theo đúng quy chuẩn Shop"),
        ("Chỉ bóc tách kịch bản của những bài vượt ngưỡng ≥ 2.0x.", "Kết nối trực tiếp bảng tồn kho và chương trình khuyến mãi hiện hành."),
        ("0-TOKEN CLI SCRIPT", "NHẬN SETUP TRỌN GÓI"),
        ("Tự động chấm điểm hàng loạt", "Xây dựng Phòng Sales AI riêng"),
        ("BÌNH LUẬN \"OUTLIER\"", "BÌNH LUẬN \"SALESAI\""),
    ])

def build_c09():
    return _swap(d1112.card_40_comment_mining_honeycomb(), [
        ("⛏️ COMMENT MINING // ĐÀO MỎ BÌNH LUẬN THỰC CHIẾN", "📣 ĐỘI NGŨ SUBAGENT PHÒNG MARKETING ĐA KÊNH TOÀN DIỆN"),
        ("PHÂN LOẠI BÌNH LUẬN VÀO <span style=\"color:#FACC15;\">6 NHÓM TÍN HIỆU MUA HÀNG</span>", "6 SUBAGENT PHỐI HỢP VẬN HÀNH <span style=\"color:#FACC15;\">PHÒNG MARKETING TỰ HÀNH</span>"),
        ("01. BUYING INTENT", "01. SUBAGENT MKT"), ("Hỏi giá, xin link, phí ship", "Nghiên cứu thị trường & đối thủ"),
        ("02. OBJECTIONS", "02. SUBAGENT CONTENT"), ("Sợ tốn điện, sợ nhảy át KTX", "Viết kịch bản & bài đăng Hook 3s"),
        ("03. PAIN POINTS", "03. SUBAGENT EDIT"), ("Phàn nàn đồ cũ nhanh hỏng", "Thiết kế Ảnh & Video Độc bản"),
        ("04. QUESTIONS", "04. SUBAGENT VOICE"), ("Hỏi kích thước, bảo hành", "Thu âm giọng đọc AI chuẩn -3dB"),
        ("05. PRAISE PROOF", "05. SUBAGENT ĐA KÊNH"), ("Điểm khách đã mua khen nhất", "Chuyển hóa FB, TikTok, Shorts"),
        ("06. EXACT SLANG", "06. SUBAGENT QUẢN KÊNH"), ("Từ lóng nguyên văn của khách", "Lên lịch tự động & Ghim link #1"),
        ("Đưa thẳng vào Hook 3s & Pinned Comment", "Phối hợp nhịp nhàng qua Cổng duyệt Mama"),
        ("VOICE OF CUSTOMER", "PHÒNG MKT IN-HOUSE"),
        ("Đừng tự bịa câu quảng cáo!", "Vận hành 4 Fanpage chỉ với 15 phút/ngày!"),
        ("Hãy lấy đúng câu phàn nàn nhiều nhất của khách trên bài đối thủ làm câu mở đầu 3 giây đầu tiên.", "Nhận thiết kế và bàn giao trọn bộ Phòng Marketing Subagent may đo riêng cho thương hiệu của bạn."),
        ("+68%", "-85%"), ("TỶ LỆ CHỐT ĐƠN QUA BÌNH LUẬN", "THỜI GIAN SẢN XUẤT NỘI DUNG"),
        ("GÕ \"MINING\" NHẬN TOOL", "GÕ \"MKTAGENT\" TƯ VẤN"),
    ])

def build_c10():
    return _swap(d1112.card_41_transcript_intelligence_anatomy(), [
        ("🎙️ TRANSCRIPT INTELLIGENCE // GIẢI PHẪU LỜI THOẠI", "📊 ĐỘI NGŨ SUBAGENT TRỢ LÝ TÀI CHÍNH, KẾ TOÁN & BÁO CÁO"),
        ("CHUẨN ≤ 85 TỪ / 30 GIÂY", "CHÍNH XÁC 100% SỐ LIỆU"),
        ("BÓC TÁCH KỊCH BẢN TRIỆU VIEW THÀNH <span style=\"color:#C084FC;\">4 LÁT CẮT THỜI GIAN</span>", "TỰ ĐỘNG ĐỐI SOÁT &amp; BÁO CÁO TÀI CHÍNH QUA <span style=\"color:#C084FC;\">4 TRẠM SUBAGENT</span>"),
        ("BỘ LỌC LINTER TỰ ĐỘNG", "TỰ CHẠY CODE PYTHON"),
        ("CẤM \"XIN CHÀO\" 3 GIÂY ĐẦU!", "KHÔNG BAO GIỜ LỆCH SỐ LẺ!"),
        ("00s – 03s", "TRẠM 01"), ("EXACT HOOK", "ĐỌC HÓA ĐƠN"), ("Câu mở đầu phá vỡ quán tính lướt, cấm chào hỏi", "Tự động bóc tách hóa đơn PDF, ảnh chụp biên lai và sao kê ngân hàng"),
        ("03s – 10s", "TRẠM 02"), ("PAIN & SETUP", "ĐỐI SOÁT ĐƠN"), ("Xoáy thẳng bối cảnh phòng trọ, bàn làm việc", "Khớp nối 50.000 dòng đơn hàng, phí sàn và chi phí quảng cáo trong 5 giây"),
        ("10s – 23s", "TRẠM 03"), ("VISUAL PROOF", "PHÂN TÍCH LÃI LỖ"), ("Cận cảnh chứng minh Before / After thực tế", "Cảnh báo ngay các mã hàng hoặc chiến dịch đang vượt ngưỡng chi phí"),
        ("23s – 30s", "TRẠM 04"), ("PAYOFF & CTA", "BÁO CÁO SẾP"), ("Lý do phải bấm ngay vào Bình luận ghim #1", "Xuất biểu đồ trực quan và gửi tóm tắt 6 dòng về Zalo/Telegram mỗi 8h sáng"),
    ])

def build_c11():
    return _swap(d1112.card_42_triple_layer_profile_firewall(), [
        ("🔒 LUẬT #4 // TRIPLE-LAYER PERSONAL PROFILE FIREWALL", "🎓 ĐỘI NGŨ SUBAGENT PHÒNG NHÂN SỰ & ĐÀO TẠO NỘI BỘ (SOP)"),
        ("TƯỜNG LỬA 3 LỚP BẢO VỆ <span style=\"color:#2DD4BF;\">TRANG CÁ NHÂN & MESSENGER</span>", "BIẾN QUY TRÌNH CÔNG TY THÀNH <span style=\"color:#2DD4BF;\">MENTOR AI ĐÀO TẠO 24/7</span>"),
        ("ISOLATED", "SOP READY"),
        ("CHẾ ĐỘ AN TOÀN TUYỆT ĐỐI", "GIẢM 90% THỜI GIAN KÈM NGƯỜI MỚI"),
        ("Phát hiện tên cá nhân → Dừng ngay lập tức!", "Nhân sự mới hỏi tới đâu → Subagent chỉ dẫn đúng chuẩn tới đó!"),
        ("GÕ \"FIREWALL\" NHẬN MÃ NGUỒN", "GÕ \"HRSOP\" ĐẶT LỊCH TƯ VẤN"),
        ("LỚP KHÓA 01 // SWITCH PROFILE VERIFICATION", "SUBAGENT 01 // TRỢ LÝ ONBOARDING NHÂN SỰ MỚI"),
        ("Tự động chuyển sang đúng Fanpage", "Hướng dẫn quy trình từng bước theo vị trí"),
        ("Gọi hàm ensure_fanpage_active() trước mọi ca tương tác để đảm bảo đang đứng dưới danh nghĩa Fanpage.", "Nạp toàn bộ sổ tay quy chế, tài liệu đào tạo và biểu mẫu nội bộ để giải đáp tức thì 24/7."),
        ("LỚP KHÓA 02 // MESSENGER POPUP KILLER", "SUBAGENT 02 // SÁT HẠCH & CHẤM ĐIỂM NGHIỆP VỤ"),
        ("Tự động đóng mọi cửa sổ chat nổi", "Đóng vai khách hàng khó tính để nhân viên tập luyện"),
        ("Quét DOM liên tục để đóng toàn bộ hộp thoại Messenger, không bao giờ gõ nhầm vào tin nhắn riêng tư.", "Tự động tạo tình huống thực tế, chấm điểm theo thang Rubric và góp ý sửa lỗi ngay lập tức."),
        ("LỚP KHÓA 03 // ARIA-LABEL IDENTITY GATE", "SUBAGENT 03 // TỔNG HỢP BIÊN BẢN HỌP & GIAO VIỆC"),
        ("Kiểm tra nhãn ô bình luận trước khi gõ", "Chuyển ghi âm cuộc họp thành bảng Action Items"),
        ("Chỉ cho phép gửi bình luận khi ô nhập liệu xác nhận đúng dòng \"Bình luận dưới tên &lt;Tên Fanpage&gt;\".", "Tự động nhắc lịch deadline cho từng thành viên trong đội nhóm không cần sếp phải giục."),
    ])

def build_c12():
    return _swap(d1112.card_43_bot_chrome_cookie_vault(), [
        ("🔄 CROSS-PC SESSION VAULT // PORT 9222 HEADLESS", "🚀 GÓI SUBAGENT CÁ NHÂN CHO FREELANCER & SOLOPRENEUR"),
        ("ZERO TASKKILL", "1 NGƯỜI = 10 NHÂN SỰ"),
        ("ĐỒNG BỘ <span style=\"color:#38BDF8;\">PHIÊN ĐĂNG NHẬP BOT</span> GIỮA MÁY CÔNG TY & MÁY NHÀ", "1 CÁ NHÂN VẬN HÀNH CÔNG SUẤT NGANG <span style=\"color:#38BDF8;\">CÔNG TY 10 NGƯỜI</span>"),
        ("💻 NODE A // MÁY VĂN PHÒNG (Ổ D:\\)", "🎯 NHÁNH A // SUBAGENT SĂN VIỆC & VIẾT PROPOSAL"),
        ("Chạy ngầm --headless=new", "Tự động nghiên cứu khách hàng & soạn báo giá"),
        ("Không bật cửa sổ làm phiền, không đụng chạm tới trình duyệt Chrome cá nhân đang mở của bạn.", "Chuẩn bị hồ sơ năng lực và bản đề xuất giải pháp cá nhân hóa chỉ trong 5 phút thay vì cả buổi."),
        ("🔐 FB_BOT_SESSION_VAULT.JSON + GIT AUTO-SYNC", "⚡ TRỢ LÝ TỔNG QUẢN CÁ NHÂN ĐỒNG HÀNH 24/7"),
        ("Kết thúc ca → Tự động xuất Cookie & đóng trình duyệt", "Bạn tập trung chuyên môn cốt lõi → Việc hậu cần để Subagent lo!"),
        ("Giải phóng 100% RAM ngay trong khối finally:, đẩy thẳng phiên mới nhất lên kho đồng bộ.", "Quản lý tiến độ dự án, nhắc lịch họp, viết bài xây dựng thương hiệu cá nhân đều đặn mỗi ngày."),
        ("29 COOKIES<br><span style=\"font-size:16px; color:#FFF;\">SYNCED ✓</span>", "X5 LẦN<br><span style=\"font-size:16px; color:#FFF;\">THU NHẬP ✓</span>"),
        ("🛡️ BẢO VỆ CHROME CÁ NHÂN 100%", "🛠️ NHẬN THIẾT KẾ ĐỘI SUBAGENT CÁ NHÂN MAY ĐO"),
        ("Chỉ đóng đúng PID của cổng 9222, cấm vĩnh viễn lệnh taskkill toàn cục!", "Cấu hình đúng theo lĩnh vực chuyên môn của bạn: Tư vấn, Thiết kế, Lập trình, Đào tạo, BĐS..."),
        ("BÌNH LUẬN \"VAULT\" NHẬN CODE", "BÌNH LUẬN \"SOLO\" TƯ VẤN 1:1"),
        ("🏠 NODE B // MÁY Ở NHÀ (Ổ F:\\)", "📈 NHÁNH B // SUBAGENT XÂY KÊNH THƯƠNG HIỆU CÁ NHÂN"),
        ("Tự nạp Cookie qua CDP Network", "Biến kiến thức của bạn thành bài đăng & video ngắn"),
        ("Mở máy ở nhà lên là tiếp tục chạy 3 ca tương tác hội nhóm (12:00, 17:30, 20:30) không cần đăng nhập lại!", "Giúp bạn thu hút khách hàng tiềm năng tự nhiên mỗi ngày mà không tốn thời gian ngồi viết bài."),
    ])

def build_c13():
    return _swap(d1112.card_44_purge_on_upgrade_protocol(), [
        ("🔥 LUẬT #9 // PURGE-ON-UPGRADE PROTOCOL", "🛒 GÓI ĐỘI NGŨ SUBAGENT CHO CHỦ SHOP TMĐT & AFFILIATE"),
        ("CÓ CHUẨN MỚI LÀ <span style=\"color:#FB923C;\">XÓA VĨNH VIỄN</span> MẪU CŨ NGAY LẬP TỨC!", "TỰ ĐỘNG HÓA <span style=\"color:#FB923C;\">CHUỖI BÁN HÀNG ĐA KÊNH</span> VỚI ĐỘI SUBAGENT"),
        ("❌ NGUY CƠ KHI GIỮ FILE CŨ", "❌ CẢNH CHỦ SHOP TỰ LÀM THỦ CÔNG"),
        ("AI Subagent đọc nhầm code cũ đã lỗi thời", "Quá tải vì vừa tìm hàng, vừa làm ảnh, vừa trực chat"),
        ("Khi trong thư mục tồn tại song song script cũ và script mới, các Agent rất dễ import nhầm mẫu cũ gây lặp lại lỗi thiết kế.", "Ngày làm 14 tiếng vẫn không kịp đăng bài đều đặn lên các Fanpage, bỏ lỡ hàng trăm bình luận hỏi mua."),
        ("ĐÃ XÓA SẠCH 72 FILE & THƯ MỤC CŨ", "KIỆT SỨC & ĐỨT QUÃNG DOANH THU"),
        ("✅ GIAO THỨC DỌN SẠCH TỰ ĐỘNG", "✅ KHI BÀN GIAO CHO ĐỘI NGŨ SUBAGENT"),
        ("Chỉ giữ lại duy nhất 1 nguồn sự thật (Single Source of Truth)", "Săn mã hàng thắng + Thiết kế ảnh + Lên lịch tự động 100%"),
        ("Thực thi unlink & rmtree đồng thời trên cả Workspace chính lẫn kho Git đồng bộ đa máy ngay khi nâng cấp.", "Tự động gắn bình luận ghim chứa link mua hàng và trả lời từng khách bình luận chỉ trong vài giây."),
        ("0% RỦI RO TÁI SỬ DỤNG MẪU LỖI", "VẬN HÀNH NHÀN NHÃ 4-10 FANPAGE CÙNG LÚC"),
        ("⚡ QUY TẮC VẬN HÀNH ĐỘI 10 SUBAGENT", "🎯 NHẬN XÂY DỰNG ĐỘI NGŨ SUBAGENT BÁN HÀNG RIÊNG"),
        ("Bộ nhớ sạch = Đầu ra chuẩn xác 100%", "Thiết kế trọn gói từ phễu nội dung tới kịch bản chốt đơn tự động"),
        ("Kết hợp cùng Cổng kiểm duyệt Bộ Não Thứ 2 trước mọi lệnh xuất bản.", "Bàn giao tận tay kèm hướng dẫn vận hành chi tiết cho chủ shop và đội ngũ."),
        ("GÕ \"PURGE\"<br><span style=\"font-size:17px;\">NHẬN SCRIPT</span>", "GÕ \"SHOPAI\"<br><span style=\"font-size:17px;\">TƯ VẤN NGAY</span>"),
    ])

def build_c14():
    return _swap(d1112.card_45_sqlite_n8n_zero_token_hub(), [
        ("⚙️ HYBRID ZERO-WASTE ARCHITECTURE // SQLITE + N8N", "🔒 CAM KẾT BẢO MẬT KHI XÂY DỰNG ĐỘI NGŨ SUBAGENT RIÊNG"),
        ("TIẾT KIỆM <span style=\"color:#34D399;\">85% TOKEN AI</span> NHỜ ĐẨY TÁC VỤ LẶP VỀ LOCAL SCRIPT", "DỮ LIỆU NỘI BỘ <span style=\"color:#34D399;\">NẰM TRÊN MÁY CỦA BẠN</span> — AN TOÀN TUYỆT ĐỐI 100%"),
        ("LUỒNG 01 // SQLITE LOCAL MCP", "LỚP BẢO VỆ 01 // LƯU TRỮ TRỰC TIẾP TRÊN MÁY CÁ NHÂN / SERVER RIÊNG"),
        ("Lưu trữ sản phẩm, link Shopee Affiliate & lịch sử bài đăng với chi phí 0 Token", "Toàn bộ cơ sở dữ liệu khách hàng, bảng giá và tài liệu mật nằm gọn trong hạ tầng của bạn"),
        ("LUỒNG 02 // N8N WEBHOOK HUB (PORT 5678)", "LỚP BẢO VỆ 02 // PHÂN QUYỀN CHẶT CHẼ TỪNG SUBAGENT PHÒNG BAN"),
        ("Kích hoạt tự động chuỗi đăng bài đa kênh & đồng bộ số liệu chuyển đổi", "Subagent Marketing không thể đọc bảng lương; Subagent CSKH không thể tự ý sửa giá bán"),
        ("LUỒNG 03 // PYTHON CLI LINTERS", "LỚP BẢO VỆ 03 // TƯỜNG LỬA TÁCH BIỆT TÀI KHOẢN CÁ NHÂN & FANPAGE"),
        ("Kiểm tra độ dài kịch bản ≤ 85 từ, băm SHA-256 chống trùng lặp dưới 0.1 giây", "Chạy ngầm trên hồ sơ độc lập, bảo vệ tuyệt đối tài khoản cá nhân và tin nhắn riêng tư của sếp"),
        ("TOKEN FIREWALL", "PRIVATE VAULT"),
        ("CHI PHÍ LƯU TRỮ & KIỂM ĐỊNH", "RÒ RỈ DỮ LIỆU RA BÊN NGOÀI"),
        ("AI chỉ tập trung sáng tạo ý tưởng & duyệt chất lượng; việc nặng để Python & SQLite lo!", "Chúng tôi bàn giao 100% quyền làm chủ hệ thống cho cá nhân và doanh nghiệp của bạn!"),
        ("GÕ \"HYBRID\" NHẬN SƠ ĐỒ", "GÕ \"BAOMAT\" TƯ VẤN"),
    ])

def build_c15():
    return _swap(d1112.card_46_ad_library_teardown_matrix(), [
        ("🕵️ AD LIBRARY TEARDOWN // GIẢI PHẪU QUẢNG CÁO ĐỐI THỦ", "📈 BÀI TOÁN ROI: THUÊ NHÂN SỰ THỜI VỤ VS XÂY ĐỘI NGŨ SUBAGENT"),
        ("MA TRẬN 4 GÓC TÌM <span style=\"color:#F472B6;\">KHOẢNG TRỐNG THỊ TRƯỜNG (ANGLE GAP)</span>", "4 LÝ DO DOANH NGHIỆP CHUYỂN SANG <span style=\"color:#F472B6;\">ĐỘI NGŨ SUBAGENT MAY ĐO</span>"),
        ("GÓC 01 // REPEATED ADS", "LỢI ÍCH 01 // CHI PHÍ ĐẦU TƯ"),
        ("Tìm quảng cáo đối thủ chạy lặp lại trên 14 ngày", "Thiết lập 1 lần — Sử dụng bền bỉ nhiều năm"),
        ("Đó mới là bài đang ra đơn thật, đừng copy bài mới chạy thử 1 ngày!", "Chi phí xây dựng cả một đội ngũ 10 Subagent chỉ tương đương 1-2 tháng lương nhân sự thời vụ!"),
        ("GÓC 02 // PAIN CLUSTERING", "LỢI ÍCH 02 // TỐC ĐỘ & QUY MÔ"),
        ("Gom cụm nỗi đau khách hàng đang bị bỏ ngỏ", "Nhân bản công suất gấp 10 lần ngay lập tức"),
        ("Đối thủ nói về giá rẻ? Hãy đánh vào độ bền và tính an toàn!", "Vào mùa cao điểm cuối năm, đội ngũ Subagent xử lý gấp 10 lần khối lượng việc mà không cần tuyển thêm người."),
        ("GÓC 03 // VISUAL CONCEPT", "LỢI ÍCH 03 // KHÔNG MẤT TRI THỨC"),
        ("Giải phẫu 3 giây mở đầu của Top 5 bài thắng", "Không lo nhân sự nghỉ việc mang theo quy trình"),
        ("Họ dùng góc máy cận cảnh Macro hay tình huống phòng trọ?", "Mọi kinh nghiệm thực chiến đều được tích lũy vĩnh viễn trong Bộ não thứ 2 của doanh nghiệp."),
        ("GÓC 04 // 3 GAP ANGLES", "LỢI ÍCH 04 // ĐỒNG BỘ 100%"),
        ("Đề xuất 3 góc kịch bản mới không đụng hàng", "Tuân thủ kỷ luật & quy chuẩn chất lượng 100%"),
        ("Đánh chiếm ngách thị trường trước khi đối thủ kịp nhận ra!", "Không làm việc theo cảm xúc, luôn đi qua cổng kiểm duyệt chất lượng trước khi xuất bản."),
        ("🎯 QUY TẮC VÀNG CỦA SUBAGENT MKT", "🎯 ĐĂNG KÝ TÍNH TOÁN ROI CHO DOANH NGHIỆP CỦA BẠN"),
        ("Chỉ học cấu trúc thắng — Tuyệt đối không đạo nhái nguyên xi!", "Nhắn tin hoặc bình luận để đội ngũ khảo sát quy trình và lập phương án tiết kiệm chi phí ngay!"),
        ("CMT \"TEARDOWN\"", "CMT \"ROI\""),
    ])

def build_c16():
    return _swap(d1112.card_47_lead_magnet_50_prompts(), [
        ("🎁 LEAD MAGNET #01 // BỘ QUÀ TẶNG ĐÓNG HỘP", "🎁 QUÀ TẶNG ĐẶC BIỆT // HỒ SƠ THIẾT KẾ ĐỘI NGŨ SUBAGENT"),
        ("TRỌN BỘ <span style=\"color:#60A5FA;\">50 PROMPT SUBAGENT</span> VẬN HÀNH PHÒNG MARKETING AI", "TẶNG BỘ KHUNG <span style=\"color:#60A5FA;\">10 SUBAGENT CÁ NHÂN &amp; DOANH NGHIỆP</span> (.MD)"),
        ("COPY & PASTE READY", "BLUEPRINT THỰC CHIẾN"),
        (">50<", ">10<"), ("PROMPT THỰC CHIẾN", "SUBAGENT ĐÓNG HỘP"),
        ("Đã chuẩn hóa đầu vào, đầu ra và thang điểm kiểm duyệt Rubric 9.0/10 cho từng vị trí chuyên môn.", "Trọn bộ cấu trúc phân vai, cổng kiểm duyệt Hard Gate và mẫu thiết lập Bộ não thứ 2 cho Cá nhân & SME."),
        ("BÌNH LUẬN \"50PROMPT\"", "BÌNH LUẬN \"10AGENT\""),
        ("NHÓM 01", "VỊ TRÍ 01-02"), ("10 Prompt Săn Sản Phẩm & Đào Bình Luận", "Tổng Quản Mama + Thủ Thư Bộ Não Thứ 2"),
        ("NHÓM 02", "VỊ TRÍ 03-04"), ("10 Prompt Viết Kịch Bản Hook 3 Giây", "Subagent Nghiên Cứu MKT + Biên Kịch Content"),
        ("NHÓM 03", "VỊ TRÍ 05-06"), ("10 Prompt Thiết Kế Ảnh & Video Độc Bản", "Subagent Đồ Họa Edit + Phòng Thu Voice AI"),
        ("NHÓM 04", "VỊ TRÍ 07-08"), ("10 Prompt Chuyển Hóa Đa Kênh Tự Động", "Subagent Đa Kênh + Quản Trị Lịch Xuất Bản"),
        ("NHÓM 05", "VỊ TRÍ 09-10"), ("10 Prompt Phân Tích Phễu & Chốt Đơn", "Subagent Chăm Sóc Khách Hàng + Kiểm Toán ROI"),
    ])

def build_c17():
    return _swap(d1112.card_48_funnel_audit_traffic_lights(), [
        ("📊 SUBAGENT HIỆU SUẤT // DECISION MATRIX", "🤝 DỊCH VỤ THIẾT KẾ & XÂY DỰNG ĐỘI NGŨ SUBAGENT MAY ĐO 1:1"),
        ("MA TRẬN RA QUYẾT ĐỊNH <span style=\"color:#4ADE80;\">KEEP • ITERATE • STOP</span> SAU 48 GIỜ", "3 GÓI GIẢI PHÁP <span style=\"color:#4ADE80;\">XÂY DỰNG ĐỘI NGŨ SUBAGENT</span> THEO NHU CẦU"),
        ("🟢 KEEP & SCALE", "🟢 GÓI CÁ NHÂN PRO"),
        ("Giữ & Nhân Bản", "Đội Subagent Cá Nhân"),
        ("3s Hold ≥ 65%\nCTR ≥ 3.5%\nĐơn hàng dương", "1 Tổng Quản Mama\n+ 5 Subagent Chuyên Môn\n+ Bộ Não Thứ 2 Cá Nhân"),
        ("Tăng tần suất phân phối, tạo thêm 3 biến thể cùng góc tiếp cận thắng.", "Dành cho CEO, Quản lý, Chuyên gia, KOL & Freelancer muốn giải phóng 80% việc lặp mỗi ngày."),
        ("🟡 ITERATE HOOK", "🟡 GÓI PHÒNG BAN SME"),
        ("Sửa Ngay 3s Đầu", "Phòng Ban Tự Hành"),
        ("Xem hết cao nhưng\n3s đầu < 50%\nhoặc ít click link", "Phòng Marketing / Sales\n+ Tự Động Hóa Đa Kênh\n+ Báo Cáo Zalo / Telegram"),
        ("Giữ nguyên phần thân demo, thay câu mở đầu và tiêu đề ảnh bắt mắt hơn.", "Dành cho Chủ Shop, Đội nhóm kinh doanh & SME cần vận hành đa kênh và chăm sóc khách hàng 24/7."),
        ("🔴 STOP & PURGE", "🔴 GÓI DOANH NGHIỆP"),
        ("Dừng Ngay Lập Tức", "Hệ Sinh Thái Toàn Diện"),
        ("3s Hold < 35%\nCTR < 1.0%\nsau 48 giờ test", "Đa Phòng Ban Phối Hợp\n+ Tích Hợp ERP / CRM\n+ Đào Tạo & Bảo Hành 1:1"),
        ("Không cố cứu sản phẩm sai tệp; chuyển ngân sách sang mã hàng mới.", "Thiết kế may đo 100% theo quy trình riêng của doanh nghiệp. Bình luận \"SETUP\" để đặt lịch khảo sát!"),
    ])


CARDS_17_SPEC = [
    ("subagent_01_personal_all_in_one", "2026-11-04 10:15", "CANHAN", build_c01,
     "🤖 HỆ SINH THÁI SUBAGENT CÁ NHÂN TOÀN DIỆN: KHI BẠN SỞ HỮU 1 TRỢ LÝ TỔNG QUẢN & 6 TRợ LÝ CHUYÊN MÔN RIÊNG!\n\n"
     "Thay vì tự mình bơi trong hàng chục đầu việc lặp đi lặp lại mỗi ngày, hãy để Đội ngũ Subagent Cá nhân Toàn diện đồng hành cùng bạn:\n"
     "🔹 1 Tổng quản (Chief of Staff) nhận lệnh trực tiếp từ bạn và phân việc cho cả đội.\n"
     "🔹 Subagent Nghiên cứu & Tóm tắt tài liệu, báo cáo dài trong 30 giây.\n"
     "🔹 Subagent Biên kịch & Nội dung viết email, bài đăng thương hiệu cá nhân đúng văn phong của bạn.\n"
     "🔹 Subagent Lịch trình & Tài chính nhắc việc, tổng hợp thu chi và gắn liền với 'Bộ não thứ 2' không bao giờ quên.\n\n"
     "👉 Bên mình nhận Tư vấn, Thiết kế & Xây dựng Đội ngũ Subagent Cá nhân may đo 1:1! Bình luận 'CANHAN' hoặc bấm vào link ở Bình luận ghim #1 để nhận bộ khung mẫu và đặt lịch tư vấn nhé! 👇"),
    ("subagent_02_enterprise_departments", "2026-11-04 13:30", "DOANHNGHIEP", build_c02,
     "🏢 XÂY DỰNG 4 PHÒNG BAN SUBAGENT DOANH NGHIỆP VẬN HÀNH TỰ ĐỘNG 24/7 CHO CHỦ SHOP & SME!\n\n"
     "Làm sao để mở rộng quy mô kinh doanh mà không bị phình to quỹ lương cố định? Giải pháp đột phá nhất 2026 là thiết lập các Phòng ban Subagent chuyên trách:\n"
     "✅ Phòng Marketing Subagent: Nghiên cứu xu hướng, viết kịch bản, thiết kế ảnh/video độc bản và hẹn giờ đa kênh.\n"
     "✅ Phòng Sales & CSKH Subagent: Trực bình luận và phản hồi khách hàng trong 3 giây suốt ngày đêm.\n"
     "✅ Phòng Kế toán & Báo cáo Subagent: Tự động đối soát đơn hàng, chi phí và gửi báo cáo lãi lỗ mỗi sáng.\n"
     "✅ Phòng Nhân sự & Đào tạo Subagent: Hướng dẫn nhân viên mới theo đúng quy trình SOP công ty.\n\n"
     "👉 Bình luận 'DOANHNGHIEP' hoặc xem Bình luận ghim #1 để đăng ký Khảo sát & Xây dựng Đội ngũ Subagent cho doanh nghiệp của bạn! 👇"),
    ("subagent_03_custom_setup_5steps", "2026-11-04 15:15", "SETUP", build_c03,
     "🚀 DỊCH VỤ NHẬN TẠO ĐỘI NGŨ SUBAGENT MAY ĐO 1:1 CHO KHÁCH HÀNG CÁ NHÂN & DOANH NGHIỆP (QUY TRÌNH 5 BƯỚC)!\n\n"
     "Bạn muốn sở hữu một đội ngũ nhân sự AI làm việc đúng theo quy trình riêng nhưng không có thời gian tự mày mò kỹ thuật? Đội ngũ AI Players nhận thiết kế & bàn giao trọn gói từ A-Z:\n"
     "1️⃣ Khảo sát 1:1 quy trình làm việc và các điểm nghẽn tốn thời gian nhất của bạn.\n"
     "2️⃣ Thiết kế Kiến trúc Đội ngũ Subagent (Tổng quản + các Subagent chuyên môn).\n"
     "3️⃣ Xây dựng 'Bộ não thứ 2' nạp sẵn tài liệu, quy chuẩn và phong cách riêng của bạn.\n"
     "4️⃣ Đấu nối trực tiếp vào Zalo, Telegram, Fanpage, Google Sheets/CRM bạn đang dùng.\n"
     "5️⃣ Bàn giao trọn bộ mã nguồn, hướng dẫn cầm tay chỉ việc và đồng hành bảo hành.\n\n"
     "👉 Bình luận 'SETUP' hoặc bấm vào Bình luận ghim #1 để đặt lịch tư vấn thiết kế Đội ngũ Subagent riêng ngay hôm nay! 👇"),
    ("subagent_04_chief_of_staff_mama", "2026-11-04 18:15", "TONGQUAN", build_c04,
     "👑 TRỢ LÝ TỔNG QUẢN (CHIEF OF STAFF SUBAGENT): BÍ QUYẾT CHỈ GIAO 1 LỆNH MÀ CẢ ĐỘI SUBAGENT TỰ CHẠY XONG VIỆC!\n\n"
     "Điểm khác biệt lớn nhất giữa người dùng AI nghiệp dư và một Hệ sinh thái Subagent chuyên nghiệp chính là vị trí Tổng Quản (Mama):\n"
     "🔹 Bạn không cần phải mở từng công cụ AI để copy-paste qua lại.\n"
     "🔹 Chỉ cần nhắn 1 yêu cầu cho Tổng Quản, hệ thống sẽ tự chia nhỏ đầu việc cho từng Subagent chuyên môn chạy song song.\n"
     "🔹 Trước khi báo cáo cho bạn, Tổng Quản tự động chấm điểm chất lượng (Hard Gate ≥ 9.0/10) — chưa đạt chuẩn sẽ bắt Subagent sửa lại ngay!\n\n"
     "👉 Muốn sở hữu một Trợ lý Tổng quản điều hành đội ngũ Subagent riêng? Bình luận 'TONGQUAN' hoặc xem Bình luận ghim #1 nhé! 👇"),
    ("subagent_05_second_brain_memory", "2026-11-04 21:15", "BONAO", build_c05,
     "🧠 SUBAGENT 'BỘ NÃO THỨ 2': GIÚP ĐỘI NGŨ AI CỦA BẠN NHỚ 100% QUY TẮC & KHÔNG BAO GIỜ LẶP LẠI LỖI CŨ!\n\n"
     "Nỗi bực mình lớn nhất khi dùng ChatGPT thông thường là hôm trước vừa dặn xong, hôm sau mở tab mới nó lại quên sạch! Khi chúng tôi xây dựng Đội ngũ Subagent cho Cá nhân & Doanh nghiệp, thành phần bắt buộc luôn là Subagent Bộ Não Thứ 2:\n"
     "✨ Tự động lắng nghe và ghi chép mọi quy tắc, sở thích và lưu ý sửa lỗi của bạn vào kho ký ức dài hạn.\n"
     "✨ Đóng vai trò Người Kiểm Duyệt Cuối Cùng trước khi bất kỳ Subagent nào xuất bản kết quả.\n\n"
     "👉 Bình luận 'BONAO' hoặc bấm vào Bình luận ghim #1 để nhận sơ đồ kiến trúc & tư vấn thiết lập Bộ não thứ 2 cho riêng bạn! 👇"),
    ("subagent_06_mobile_zalo_telegram_command", "2026-11-05 08:30", "MOBILE", build_c06,
     "📱 CHỈ HUY ĐỘI NGŨ SUBAGENT TRÊN ĐIỆN THOẠI QUA ZALO & TELEGRAM MỌI LÚC MỌI NƠI!\n\n"
     "Khi sở hữu Đội ngũ Subagent Cá nhân & Doanh nghiệp do AI Players thiết kế, bạn không cần phải ngồi dính trước màn hình máy tính:\n"
     "🔹 Đang đi công tác hay ngồi cà phê, chỉ cần mở điện thoại nhắn 1 câu tự nhiên là cả đội Subagent ở văn phòng/ở nhà tự động phối hợp xử lý.\n"
     "🔹 Nhận báo cáo nghiệm thu ngắn gọn 4–8 dòng kèm kết quả ngay trên điện thoại.\n"
     "🔹 Đồng bộ liền mạch 100% lịch sử công việc giữa máy tính công ty và máy tính ở nhà.\n\n"
     "👉 Bình luận 'MOBILE' hoặc xem Bình luận ghim #1 để trải nghiệm và đặt lịch xây dựng Đội ngũ Subagent điều khiển từ xa nhé! 👇"),
    ("subagent_07_single_ai_vs_subagent_team", "2026-11-05 10:15", "SUBAGENT", build_c07,
     "⚡ TẠI SAO 1 CHATGPT ĐƠN LẺ THẤT BẠI CÒN ĐỘI NGŨ SUBAGENT CHUYÊN MÔN HÓA THẮNG ÁP ĐẢO?\n\n"
     "Bắt 1 cửa sổ AI duy nhất vừa nghiên cứu thị trường, vừa viết bài, vừa làm kế toán chẳng khác nào bắt 1 nhân viên làm thay cả công ty — kết quả chắc chắn sẽ hời hợt và đầy lỗi sai!\n"
     "Khi chuyển sang mô hình Đội ngũ Subagent Toàn diện:\n"
     "1️⃣ Chuyên môn hóa sâu: Mỗi Subagent được huấn luyện bộ quy chuẩn riêng cho đúng 1 nghiệp vụ.\n"
     "2️⃣ Kiểm duyệt chéo độc lập: Có Subagent chuyên bắt lỗi trước khi bàn giao.\n"
     "3️⃣ Thiết kế may đo: Khớp 100% với quy trình thực tế của cá nhân hoặc doanh nghiệp bạn.\n\n"
     "👉 Bình luận 'SUBAGENT' hoặc bấm vào Bình luận ghim #1 để nhận tư vấn xây dựng Đội ngũ Subagent riêng nha! 👇"),
    ("subagent_08_sales_cskh_subagent_247", "2026-11-05 13:30", "SALESAI", build_c08,
     "💼 ĐỘI NGŨ SUBAGENT PHÒNG SALES & CSKH: TRỰC FANPAGE 24/7, PHẢN HỒI TRONG 3 GIÂY & TĂNG +240% CHUYỂN ĐỔI!\n\n"
     "Khách hàng để lại bình luận hỏi giá lúc 11h đêm nhưng sáng hôm sau nhân viên mới trả lời thì 80% khách đã sang mua của đối thủ! Đội ngũ Subagent Phòng Sales & CSKH giải quyết triệt để:\n"
     "✅ Tự động bắt mọi bình luận của khách trên toàn bộ hệ thống Fanpage và phản hồi ngay lập tức.\n"
     "✅ Tư vấn đúng thông tin sản phẩm, gửi đúng link ưu đãi và kích mồi thảo luận tự nhiên.\n"
     "✅ Ghi sổ theo dõi khách hàng tiềm năng để đội ngũ Sales chốt đơn dễ dàng.\n\n"
     "👉 Bạn muốn xây dựng Phòng Sales & CSKH Subagent cho shop/doanh nghiệp của mình? Bình luận 'SALESAI' hoặc xem Bình luận ghim #1 nhé! 👇"),
    ("subagent_09_marketing_content_subagent", "2026-11-05 15:15", "MKTAGENT", build_c09,
     "📣 PHÒNG MARKETING 6 SUBAGENT TỰ HÀNH: VẬN HÀNH 4–10 KÊNH TRUYỀN THÔNG CHỈ VỚI 15 PHÚT DUYỆT BÀI MỖI NGÀY!\n\n"
     "Đây chính là mô hình Phòng Marketing Subagent thực chiến đang vận hành trực tiếp hệ thống của chúng tôi:\n"
     "1️⃣ Subagent MKT: Nghiên cứu sản phẩm thắng, đào bình luận tìm nỗi đau khách hàng.\n"
     "2️⃣ Subagent Content: Viết kịch bản video ngắn và bài đăng có Hook 3s sắc bén.\n"
     "3️⃣ Subagent Edit & Voice: Kết xuất hình ảnh/video độc bản Zero-Clone và giọng đọc phòng thu.\n"
     "4️⃣ Subagent Đa Kênh & Quản Lý Kênh: Lên lịch tự động và gắn bình luận ghim dẫn phễu.\n\n"
     "👉 Chúng tôi nhận đóng gói & xây dựng trọn bộ Phòng Marketing Subagent này cho doanh nghiệp của bạn! Bình luận 'MKTAGENT' hoặc xem Bình luận ghim #1 nha! 👇"),
    ("subagent_10_finance_report_subagent", "2026-11-05 18:15", "BAOCAO", build_c10,
     "📊 ĐỘI NGŨ SUBAGENT TRỢ LÝ TÀI CHÍNH, KẾ TOÁN & BÁO CÁO SỐ LIỆU TỰ ĐỘNG CHO CEO!\n\n"
     "Thay vì chờ đợi báo cáo tổng hợp vào cuối tuần, Đội ngũ Subagent Tài chính & Số liệu giúp chủ doanh nghiệp nắm bắt sức khỏe dòng tiền mỗi sáng:\n"
     "🔹 Trạm 1: Tự động đọc và bóc tách dữ liệu từ hóa đơn, biên lai, file Excel/CSV.\n"
     "🔹 Trạm 2: Tự chạy mã tính toán đối soát hàng chục nghìn dòng đơn hàng chính xác tuyệt đối 100%.\n"
     "🔹 Trạm 3 & 4: Phát hiện sớm các khoản chi vượt định mức và gửi báo cáo tóm tắt 6 dòng về điện thoại của sếp đúng 8h sáng.\n\n"
     "👉 Bình luận 'BAOCAO' hoặc bấm vào Bình luận ghim #1 để được tư vấn xây dựng Subagent Trợ lý Số liệu & Báo cáo riêng nhé! 👇"),
    ("subagent_11_hr_sop_onboarding_subagent", "2026-11-05 21:15", "HRSOP", build_c11,
     "🎓 SUBAGENT PHÒNG NHÂN SỰ & ĐÀO TẠO NỘI BỘ: BIẾN QUY TRÌNH CÔNG TY THÀNH MENTOR KÈM NHÂN VIÊN MỚI 24/7!\n\n"
     "Mỗi lần tuyển nhân sự mới, trưởng bộ phận lại mất hàng tuần để chỉ lại từ đầu những quy trình cơ bản. Hãy bàn giao việc đó cho Đội ngũ Subagent Đào tạo Nội bộ (SOP Mentor):\n"
     "✨ Nạp toàn bộ quy chế, kịch bản bán hàng, quy trình xử lý công việc vào Bộ não thứ 2 của công ty.\n"
     "✨ Nhân viên mới vướng ở bước nào chỉ cần hỏi, Subagent sẽ hướng dẫn từng bước đúng chuẩn công ty.\n"
     "✨ Tự động đóng vai khách hàng giả lập để sát hạch nhân viên mới trước khi cho tiếp xúc khách thật.\n\n"
     "👉 Bình luận 'HRSOP' hoặc xem Bình luận ghim #1 để thiết lập Đội ngũ Subagent Đào tạo & Quản trị quy trình cho doanh nghiệp bạn! 👇"),
    ("subagent_12_freelancer_solopreneur_team", "2026-11-06 08:30", "SOLO", build_c12,
     "🚀 GÓI ĐỘI NGŨ SUBAGENT CÁ NHÂN CHO CHUYÊN GIA ĐỘC LẬP, KOL & SOLOPRENEUR (1 NGƯỜI = CÔNG TY 10 NHÂN SỰ)!\n\n"
     "Khi làm việc độc lập, thời gian của bạn chính là tài sản quý giá nhất. Đừng để các việc hành chính, viết bài, làm báo giá ngốn mất thời gian làm chuyên môn:\n"
     "🔹 Nhánh Subagent Săn việc & Proposal: Tự động nghiên cứu khách hàng và soạn bản đề xuất cá nhân hóa trong 5 phút.\n"
     "🔹 Nhánh Subagent Thương hiệu Cá nhân: Biến kinh nghiệm thực tế của bạn thành chuỗi bài viết & video thu hút khách hàng tiềm năng mỗi ngày.\n"
     "🔹 Trợ lý Tổng quản Cá nhân: Quản lý lịch hẹn, theo dõi hợp đồng và nhắc việc tự động.\n\n"
     "👉 Bình luận 'SOLO' hoặc bấm vào Bình luận ghim #1 để nhận tư vấn thiết kế Đội ngũ Subagent Cá nhân may đo 1:1 nhé! 👇"),
    ("subagent_13_ecommerce_affiliate_subagent", "2026-11-06 10:15", "SHOPAI", build_c13,
     "🛒 GÓI ĐỘI NGŨ SUBAGENT DÀNH RIÊNG CHO CHỦ SHOP THƯƠNG MẠI ĐIỆN TỬ & HỆ THỐNG FANPAGE AFFILIATE!\n\n"
     "Làm sao để vận hành cùng lúc 3–10 Fanpage bán hàng có nội dung sắc nét, lên bài đúng khung giờ vàng và trả lời khách ngay lập tức mà chỉ cần 1 người quản lý?\n"
     "✅ Subagent Săn hàng: Chọn lọc các mã sản phẩm đang vào mùa có đánh giá ≥ 4.8 sao.\n"
     "✅ Subagent Thiết kế Studio: Tạo ảnh bài đăng chữ nổi bắt mắt, kiểm tra chống trùng lặp 100%.\n"
     "✅ Subagent Vận hành Kênh: Tự động lên lịch khung giờ vàng, gắn link dưới bình luận đầu tiên và phản hồi khách hỏi mua.\n\n"
     "👉 Bình luận 'SHOPAI' hoặc xem Bình luận ghim #1 để đặt lịch xây dựng Đội ngũ Subagent Bán hàng riêng cho shop của bạn! 👇"),
    ("subagent_14_security_private_data_shield", "2026-11-06 13:30", "BAOMAT", build_c14,
     "🔒 CAM KẾT BẢO MẬT & QUYỀN SỞ HỮU 100% KHI XÂY DỰNG ĐỘI NGŨ SUBAGENT RIÊNG TẠI AI PLAYERS!\n\n"
     "Nhiều doanh nghiệp và cá nhân muốn ứng dụng AI nhưng lo ngại rò rỉ dữ liệu khách hàng hoặc phụ thuộc vào bên thứ ba. Kiến trúc Đội ngũ Subagent của chúng tôi giải quyết triệt để:\n"
     "🛡️ Lưu trữ локально (Local-First): Toàn bộ cơ sở dữ liệu, tài liệu SOP và Bộ não thứ 2 nằm trực tiếp trên máy tính/server riêng của bạn.\n"
     "🛡️ Phân quyền từng Subagent: Khóa chặt phạm vi truy cập dữ liệu giữa các phòng ban.\n"
     "🛡️ Bàn giao toàn quyền sở hữu: Bạn nắm giữ 100% mã nguồn và cấu hình hệ thống.\n\n"
     "👉 Bình luận 'BAOMAT' hoặc bấm vào Bình luận ghim #1 để nhận tư vấn kiến trúc Subagent bảo mật riêng cho doanh nghiệp bạn! 👇"),
    ("subagent_15_case_study_roi_comparison", "2026-11-06 15:15", "ROI", build_c15,
     "📈 BÀI TOÁN ĐẦU TƯ THÔNG MINH: THUÊ THÊM NHÂN SỰ THỜI VỤ HAY XÂY DỰNG ĐỘI NGŨ SUBAGENT VẬN HÀNH LÂU DÀI?\n\n"
     "Hãy nhìn vào 4 con số thực tế khi doanh nghiệp sở hữu một Đội ngũ Subagent được thiết kế bài bản:\n"
     "1️⃣ Chi phí tối ưu: Đầu tư thiết lập 1 lần với ngân sách chỉ bằng 1–2 tháng lương nhân sự thời vụ nhưng sử dụng bền bỉ nhiều năm.\n"
     "2️⃣ Mở rộng tức thì: Mùa cao điểm có thể tăng gấp 10 lần công suất xử lý mà không tốn thời gian tuyển dụng.\n"
     "3️⃣ Tài sản tri thức vĩnh viễn: Mọi quy trình và kinh nghiệm đều nằm lại trong Bộ não thứ 2 của công ty.\n"
     "4️⃣ Kỷ luật 100%: Làm việc 24/7/365 và luôn tuân thủ cổng kiểm duyệt chất lượng.\n\n"
     "👉 Bình luận 'ROI' hoặc xem Bình luận ghim #1 để đội ngũ tính toán phương án Subagent tối ưu nhất cho bạn! 👇"),
    ("subagent_16_blueprint_10_subagents_gift", "2026-11-06 18:15", "10AGENT", build_c16,
     "🎁 TẶNG MIỄN PHÍ: BỘ HỒ SƠ THIẾT KẾ 10 SUBAGENT CÁ NHÂN & DOANH NGHIỆP TOÀN DIỆN (.MD BLUEPRINT)!\n\n"
     "Để bạn hình dung rõ nhất cách một Đội ngũ Subagent phối hợp làm việc như thế nào, AI Players gửi tặng cộng đồng trọn bộ Hồ sơ Thiết kế 10 Vị trí Subagent thực chiến:\n"
     "📌 Nhóm Chỉ huy & Trí nhớ: Tổng quản Mama + Thủ thư Bộ não thứ 2.\n"
     "📌 Nhóm Nghiên cứu & Sáng tạo: Subagent MKT + Subagent Biên kịch Content.\n"
     "📌 Nhóm Sản xuất Media: Subagent Đồ họa Edit + Subagent Phòng thu Voice AI.\n"
     "📌 Nhóm Xuất bản & Chuyển đổi: Subagent Đa kênh + Quản lý kênh + CSKH + Kiểm toán Hiệu suất.\n\n"
     "👉 Bình luận '10AGENT' hoặc bấm thẳng vào link ở Bình luận ghim #1 để tải miễn phí và đăng ký tư vấn thiết kế riêng nhé! 👇"),
    ("subagent_17_book_1on1_subagent_audit", "2026-11-06 21:15", "SETUP", build_c17,
     "🤝 CHỌN GÓI ĐỘI NGŨ SUBAGENT PHÙ HỢP NHẤT VỚI BẠN: CÁ NHÂN PRO • PHÒNG BAN SME • DOANH NGHIỆP TOÀN DIỆN!\n\n"
     "Dù bạn là một cá nhân bận rộn muốn có dàn trợ lý riêng hay là chủ doanh nghiệp muốn tự động hóa các phòng ban, chúng tôi đều có lộ trình thiết kế may đo 1:1:\n"
     "🟢 GÓI CÁ NHÂN PRO: 1 Tổng quản + 5 Subagent chuyên môn + Bộ não thứ 2 cá nhân hóa.\n"
     "🟡 GÓI PHÒNG BAN SME: Đóng gói Phòng Marketing đa kênh hoặc Phòng Sales/CSKH tự động 24/7.\n"
     "🔴 GÓI DOANH NGHIỆP TOÀN DIỆN: Hệ sinh thái đa phòng ban phối hợp + Đấu nối dữ liệu nội bộ + Đào tạo & Bảo hành trọn gói.\n\n"
     "👉 Bình luận 'SETUP' hoặc bấm vào link Nhóm Zalo VIP tại Bình luận ghim #1 để đặt lịch Khảo sát & Tư vấn 1:1 cùng đội ngũ AI Players ngay hôm nay! 👇"),
]


def delete_19_old_scheduled_posts(pages: dict) -> int:
    tok = pages[AI_PAGE_ID]["access_token"]
    sp = graph_get(f"{AI_PAGE_ID}/scheduled_posts", tok, {"fields": "id,message,scheduled_publish_time", "limit": 50}).get("data", [])
    deleted = 0
    for item in sp:
        pid = item["id"]
        try:
            req = urllib.request.Request(
                f"https://graph.facebook.com/v22.0/{pid}?access_token={urllib.parse.quote(tok)}",
                method="DELETE",
            )
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=15):
                deleted += 1
                print(f"🗑️ Đã xóa bài hẹn giờ cũ trên AI Players: {pid}", flush=True)
        except Exception as e:
            print(f"⚠️ Không xóa được {pid}: {e}", flush=True)
    return deleted


def build_qa_grid(image_paths: list[Path], out_grid: Path) -> None:
    cols, rows = 5, 4
    cell = 280
    canvas = Image.new("RGB", (cols * cell, rows * cell), (8, 12, 22))
    for idx, p in enumerate(image_paths[:20]):
        with Image.open(p) as im:
            thumb = im.convert("RGB").resize((cell - 12, cell - 12), Image.Resampling.LANCZOS)
            x = (idx % cols) * cell + 6
            y = (idx // cols) * cell + 6
            canvas.paste(thumb, (x, y))
    canvas.save(out_grid, format="JPEG", quality=92, optimize=True)


def schedule_17_cards(manifest_items: list[dict], pages: dict) -> list[dict]:
    import requests
    tok = pages[AI_PAGE_ID]["access_token"]
    now_ts = int(dt.datetime.now(VN_TZ).timestamp())

    for item in manifest_items:
        img_path = Path(item["image_path"])
        dt_obj = dt.datetime.strptime(item["slot_dt"], "%Y-%m-%d %H:%M").replace(tzinfo=VN_TZ)
        sched_ts = int(dt_obj.timestamp())
        if sched_ts <= now_ts + 900:
            sched_ts = now_ts + 1200

        pinned_msg = (
            f"📌 [TÀI LIỆU & ĐẶT LỊCH THIẾT KẾ ĐỘI NGŨ SUBAGENT 1:1 — MÃ: {item['cta_kw']}]\n"
            f"👉 Bấm vào Nhóm Zalo VIP \"AI Players — Hệ Sinh Thái Subagent Cá Nhân & Doanh Nghiệp\" để tải miễn phí Bộ Khung 10 Subagent (.MD) & Đăng ký Khảo sát Xây dựng Đội ngũ Subagent may đo riêng cho bạn:\n"
            f"🔗 Link nhận tài liệu & tư vấn 1:1: {ZALO_URL}"
        )
        data = {
            "caption": item["caption"],
            "access_token": tok,
            "published": "false",
            "scheduled_publish_time": str(sched_ts),
        }
        with open(img_path, "rb") as f:
            r = requests.post(
                f"https://graph.facebook.com/v22.0/{AI_PAGE_ID}/photos",
                data=data,
                files={"source": (img_path.name, f, "image/jpeg")},
                timeout=90,
            )
        res = r.json()
        post_id = res.get("post_id") or res.get("id", "")
        cmt_id = ""
        if post_id:
            record_published_content(page_id=AI_PAGE_ID, media_path=img_path, caption=item["caption"], post_id=str(post_id))
            c_res = graph_post(f"{post_id}/comments", tok, {"message": pinned_msg})
            cmt_id = c_res.get("id", "")
            item["status"] = "SCHEDULED"
            item["post_id"] = post_id
            item["comment_id"] = cmt_id
            print(f"✅ [{item['code']}] SCHEDULED ({item['slot_dt']}) -> post_id={post_id} | cmt_id={cmt_id}", flush=True)
        else:
            item["status"] = "ERROR"
            item["error"] = res
            print(f"❌ [{item['code']}] Lỗi: {res}", flush=True)
        time.sleep(0.8)
    return manifest_items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true", help="Xóa 19 bài cũ & Hẹn giờ 17 bài ảnh Subagent Agency mới lên AI Players")
    args = parser.parse_args()

    update_seeding_and_pinned_templates()
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    rendered_paths = []
    manifest_items = []

    print("🎨 Đang kết xuất 17 Ảnh Độc Bản Tuyến Nội Dung Mới (Subagent Cá Nhân & Doanh Nghiệp Toàn Diện)...")
    for idx, (code, slot_dt, cta_kw, builder, caption) in enumerate(CARDS_17_SPEC, 1):
        out_jpg = IMAGES_DIR / f"{code}.jpg"
        html = builder()
        render_html_to_image(html, out_jpg, width=1080, height=1080)
        rendered_paths.append(out_jpg)
        manifest_items.append({
            "index": idx,
            "code": code,
            "slot_dt": slot_dt,
            "cta_kw": cta_kw,
            "image_path": str(out_jpg),
            "caption": caption,
        })
        print(f"  ✔ [{idx:02d}/17] Đã render: {out_jpg.name}", flush=True)

    ok, gate_msg = verify_zero_clone_images(IMAGES_DIR, max_similarity=0.58)
    print(("🛡️ " if ok else "🛑 ") + gate_msg, flush=True)
    if not ok:
        sys.exit(1)

    build_qa_grid(rendered_paths, QA_GRID_PATH)
    print(f"🖼️ Đã tạo bảng QA Grid 17 thiết kế độc bản tại: {QA_GRID_PATH}", flush=True)

    if args.publish:
        pages = load_vault()
        deleted = delete_19_old_scheduled_posts(pages)
        print(f"🧹 Đã dọn sạch {deleted} bài hẹn giờ cũ trên Page AI Players.", flush=True)
        manifest_items = schedule_17_cards(manifest_items, pages)

    MANIFEST_PATH.write_text(json.dumps(manifest_items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📄 Đã lưu Manifest tại: {MANIFEST_PATH}", flush=True)


if __name__ == "__main__":
    main()
