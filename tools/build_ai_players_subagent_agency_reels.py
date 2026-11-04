#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_ai_players_subagent_agency_reels.py — Sản Xuất & Hẹn Giờ 6 Video Reels Độc Bản (9:16, 1080x1920 @ 30fps)
Tuyến Nội Dung Mới: "Hệ Sinh Thái Subagent Cá Nhân & Doanh Nghiệp Toàn Diện — Nhận Tạo Đội Ngũ Subagent May Đo 1:1"
Cho Fanpage "AI Players - Người chơi hệ AI" (1022527194267367):
  - Ngày 04/11/2026: 11:45, 16:30, 20:00
  - Ngày 05/11/2026: 11:45, 16:30, 20:00
Đồng thời cập nhật mã nguồn Remotion (`rebuild_remaining_18_golden_reels_data.py` -> `build_18_truly_bespoke_zero_clone_reels.py`)
và kiểm định qua cổng `verify_zero_clone_tsx()`.
"""

import argparse
import datetime as dt
import json
import math
import shutil
import ssl
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SUBAGENT_DIR / "tools"))

from render_vid_style_card import get_local_fonts_css, render_html_to_image
from zero_repost_gate import verify_zero_clone_tsx, record_published_content
from mama_auto_scheduler_engine import load_vault, graph_post, SSL_CTX

AI_PAGE_ID = "1022527194267367"
ZALO_URL = "https://zalo.me/g/fzxvbf259"
VN_TZ = dt.timezone(dt.timedelta(hours=7))

OUT_ROOT = SUBAGENT_DIR / "campaigns" / "2026-11-04" / "ai-players-subagent-agency-vault"
REELS_DIR = OUT_ROOT / "reels"
SCENES_DIR = OUT_ROOT / "reel_scenes"
AUDIO_DIR = OUT_ROOT / "reel_audio"
REELS_MANIFEST_PATH = OUT_ROOT / "subagent_agency_6_reels_manifest.json"

TTS_SCRIPT = SUBAGENT_DIR / "tools" / "generate_voice_tts.py"
FFMPEG_EXE = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE_EXE = shutil.which("ffprobe") or "ffprobe"
BGM_PATH = SUBAGENT_DIR / "templates" / "remotion-cuongit-template" / "public" / "brand-kit" / "bgm" / "1.The Violins.mp3"

SIX_REELS_SPEC = [
    {
        "id": "subagent_reel_01_personal_team",
        "slot_dt": "2026-11-04 11:45",
        "cta_kw": "CANHAN",
        "accent": "#22D3EE",
        "accent2": "#A3E635",
        "bg_grad": "radial-gradient(circle at 20% 25%, rgba(34,211,238,0.32) 0%, transparent 55%), linear-gradient(165deg, #030914 0%, #071A2E 100%)",
        "layout_mode": "orbital_hub",
        "title": "Hệ Sinh Thái 6 Subagent Cá Nhân Toàn Diện — Giải Phóng 80% Thời Gian",
        "caption": (
            "🤖 ĐỪNG DÙNG 1 CHATGPT ĐƠN LẺ NỮA — HÃY SỞ HỮU ĐỘI NGŨ 6 SUBAGENT CÁ NHÂN TOÀN DIỆN PHỤC VỤ RIÊNG BẠN!\n\n"
            "Khi bạn có 1 Trợ lý Tổng quản điều phối 5 Subagent chuyên trách (Nghiên cứu, Biên kịch, Lịch trình, Tài chính, Bộ não thứ 2), 80% công việc lặp đi lặp lại mỗi ngày sẽ được tự động hóa hoàn toàn.\n\n"
            "👉 Đội ngũ AI Players nhận Tư vấn, Thiết kế & Bàn giao Đội ngũ Subagent Cá nhân may đo 1:1! Bình luận 'CANHAN' hoặc xem Bình luận ghim #1 nhé! 👇"
        ),
        "scenes": [
            ("01 // NỖI ĐAU CÁ NHÂN", "DÙNG 1 AI ĐƠN LẺ", "VẪN QUÁ TẢI MỖI NGÀY?", "Mở hàng chục tab chat rời rạc làm AI loạn ngữ cảnh và quên sạch quy tắc", "Tự Copy-Paste Thủ Công", "Mất 3–4 giờ mỗi ngày chỉ để nhắc lại yêu cầu từ đầu", "MẤT THỜI GIAN ⚠️", "Một công cụ AI đơn lẻ không thể ôm đồm cùng lúc mười đầu việc cá nhân của bạn."),
            ("02 // GIẢI PHÁP ĐỘT PHÁ", "ĐỘI NGŨ 6 SUBAGENT", "CÁ NHÂN TOÀN DIỆN", "Mô hình 1 Trợ lý Tổng quản chỉ huy 5 Subagent chuyên môn hóa", "Chuyên Môn Hóa 100%", "Mỗi Subagent đảm nhận đúng 1 nghiệp vụ sắc bén nhất", "CHUẨN XÁC ⚡", "Giải pháp đột phá là thiết lập một đội ngũ sáu Subagent cá nhân chuyên trách."),
            ("03 // KIẾN TRÚC PHỐI HỢP", "TRỢ LÝ TỔNG QUẢN", "ĐIỀU PHỐI TỰ ĐỘNG", "Nhận 1 lệnh ngắn từ bạn và tự động chia việc cho cả đội", "1. Thư Ký & Lịch Trình", "Quản lý cuộc hẹn, nhắc việc & tóm tắt biên bản họp", "2. Nghiên Cứu & Nội Dung", "Đọc báo cáo chuyên sâu, viết email & bài đăng cá nhân", "Bạn chỉ cần nhắn một câu cho Tổng quản, các Subagent sẽ tự động phối hợp chạy việc."),
            ("04 // BỘ NÃO THỨ 2", "GHI NHỚ 100%", "PHONG CÁCH CỦA BẠN", "Lưu trữ toàn bộ thói quen, văn phong và lịch sử công việc dài hạn", "Không Bao Giờ Quên", "Càng làm việc lâu càng hiểu rõ ý chủ nhân", "ĐỒNG BỘ 2 MÁY ✅", "Kết hợp cùng Bộ não thứ hai giúp hệ thống nhớ trọn vẹn phong cách làm việc của riêng bạn."),
            ("05 // DỊCH VỤ MAY ĐO 1:1", "NHẬN THIẾT KẾ RIÊNG", "ĐỘI SUBAGENT CÁ NHÂN", "Khảo sát quy trình, đóng gói cấu hình và bàn giao tận tay từ A đến Z", "Giải Phóng 80% Việc Lặp", "Giúp CEO, Quản lý & Freelancer tập trung việc cốt lõi", "BÀN GIAO TRỌN GÓI 🚀", "Chúng tôi nhận khảo sát và thiết kế đội ngũ Subagent cá nhân may đo một một cho bạn."),
            ("06 // HÀNH ĐỘNG NGAY", "BÌNH LUẬN: CANHAN", "NHẬN KHUNG 10 SUBAGENT", "Hoặc bấm vào Link Nhóm Zalo VIP tại Bình luận ghim #1 bên dưới!", "Tặng Bộ Khung .MD", "Miễn phí 100% trong Nhóm Zalo VIP", "ĐẶT LỊCH TƯ VẤN 👇", "Bình luận ngay từ khóa Cá nhân hoặc bấm vào bình luận ghim đầu tiên để nhận tài liệu nhé!"),
        ],
    },
    {
        "id": "subagent_reel_02_enterprise_depts",
        "slot_dt": "2026-11-04 16:30",
        "cta_kw": "DOANHNGHIEP",
        "accent": "#10B981",
        "accent2": "#FBBF24",
        "bg_grad": "radial-gradient(circle at 80% 20%, rgba(16,185,129,0.32) 0%, transparent 55%), linear-gradient(165deg, #04120C 0%, #092418 100%)",
        "layout_mode": "four_pillars",
        "title": "Xây Dựng 4 Phòng Ban Subagent Doanh Nghiệp Vận Hành 24/7",
        "caption": (
            "🏢 XÂY DỰNG 4 PHÒNG BAN SUBAGENT DOANH NGHIỆP VẬN HÀNH TỰ ĐỘNG 24/7 CHO CHỦ SHOP & SME!\n\n"
            "Mở rộng quy mô doanh nghiệp mà không làm phình to chi phí cố định nhờ 4 Phòng ban Subagent chuyên trách: Marketing Đa Kênh, Sales & CSKH 24/7, Kế Toán Đối Soát và Nhân Sự SOP.\n\n"
            "👉 Bình luận 'DOANHNGHIEP' hoặc bấm vào Bình luận ghim #1 để đặt lịch Khảo sát & Xây dựng Đội ngũ Subagent cho doanh nghiệp của bạn! 👇"
        ),
        "scenes": [
            ("01 // BÀI TOÁN DOANH NGHIỆP", "TUYỂN THÊM NGƯỜI", "HAY XÂY ĐỘI SUBAGENT?", "Chi phí nhân sự cố định tăng cao nhưng công việc lặp lại vẫn bị nghẽn", "Quá Tải Vận Hành", "Nhân viên mất 70% thời gian làm các thao tác thủ công", "CHI PHÍ CAO ⚠️", "Làm sao để mở rộng quy mô doanh nghiệp mà không bị phình to quỹ lương cố định?"),
            ("02 // PHÒNG MARKETING AI", "PHÒNG BAN SỐ 1", "MARKETING ĐA KÊNH", "Tự động nghiên cứu xu hướng, viết kịch bản và thiết kế ấn phẩm độc bản", "Vận Hành 4–10 Kênh", "Lên lịch tự động khung giờ vàng không trùng lặp", "TỰ ĐỘNG 100% 🔥", "Phòng ban thứ nhất là Đội ngũ Subagent Marketing tự động sản xuất và lên lịch nội dung đa kênh."),
            ("03 // PHÒNG SALES & CSKH", "PHÒNG BAN SỐ 2", "CHỐT ĐƠN 24/7/365", "Trực bình luận và phản hồi khách hàng chỉ trong 3 giây suốt ngày đêm", "1. Bắt Bình Luận Nóng", "Gửi báo giá & link ưu đãi ngay khi khách vừa hỏi", "2. Chăm Sóc Khách Cũ", "Tăng +240% tỷ lệ chuyển đổi đơn hàng tự nhiên", "Phòng ban thứ hai là Đội ngũ Subagent Sales và Chăm sóc khách hàng phản hồi tức thì hai tư trên bảy."),
            ("04 // KẾ TOÁN & NHÂN SỰ", "PHÒNG BAN 3 & 4", "SỐ LIỆU & ĐÀO TẠO SOP", "Đối soát hàng chục nghìn đơn hàng và hướng dẫn nhân viên mới từng bước", "Chính Xác Tuyệt Đối", "Xuất biểu đồ báo cáo lãi lỗ gửi sếp mỗi 8h sáng", "CHUẨN 100% ✅", "Kết hợp cùng Subagent Kế toán đối soát số liệu và Subagent Nhân sự đào tạo nội bộ."),
            ("05 // TRIỂN KHAI TRỌN GÓI", "THIẾT KẾ MAY ĐO", "CHO TỪNG DOANH NGHIỆP", "Đấu nối trực tiếp vào Zalo, Telegram, Fanpage và bảng dữ liệu nội bộ", "Tiết Kiệm 80% Chi Phí", "Bàn giao toàn quyền làm chủ hệ thống và bảo hành", "ROI VƯỢT TRỘI 🚀", "Chúng tôi nhận thiết kế và bàn giao trọn gói hệ thống phòng ban Subagent theo quy trình riêng của bạn."),
            ("06 // ĐẶT LỊCH KHẢO SÁT", "GÕ: DOANHNGHIEP", "TƯ VẤN KIẾN TRÚC 1:1", "Bấm ngay vào Link Nhóm Zalo VIP ở Bình luận ghim #1 bên dưới!", "Tặng Sơ Đồ Phòng Ban", "Miễn phí hồ sơ thiết kế mẫu trong Zalo VIP", "LIÊN HỆ NGAY 👇", "Hãy bình luận từ khóa Doanh nghiệp hoặc bấm vào bình luận ghim đầu tiên để đặt lịch khảo sát nhé!"),
        ],
    },
    {
        "id": "subagent_reel_03_custom_setup_service",
        "slot_dt": "2026-11-04 20:00",
        "cta_kw": "SETUP",
        "accent": "#F59E0B",
        "accent2": "#38BDF8",
        "bg_grad": "radial-gradient(circle at 50% 25%, rgba(245,158,11,0.32) 0%, transparent 58%), linear-gradient(165deg, #120B03 0%, #241505 100%)",
        "layout_mode": "five_steps",
        "title": "Quy Trình 5 Bước Thiết Kế & Bàn Giao Đội Ngũ Subagent May Đo 1:1",
        "caption": (
            "🚀 DỊCH VỤ NHẬN TẠO ĐỘI NGŨ SUBAGENT MAY ĐO 1:1 CHO KHÁCH HÀNG CÁ NHÂN & DOANH NGHIỆP!\n\n"
            "Không cần biết lập trình, đội ngũ AI Players sẽ khảo sát quy trình thực tế của bạn và xây dựng trọn gói Đội ngũ Subagent chuyên trách trong 5 bước chuẩn mực.\n\n"
            "👉 Bình luận 'SETUP' hoặc bấm vào Bình luận ghim #1 để đặt lịch tư vấn 1:1 ngay hôm nay! 👇"
        ),
        "scenes": [
            ("01 // RÀO CẢN KỸ THUẬT", "MUỐN CÓ ĐỘI SUBAGENT", "NHƯNG BẬN KHÔNG RẢNH CODE?", "Tự mày mò hàng tháng trời vẫn chưa nối được các tác nhân AI chạy ổn định", "Thiếu Kiến Trúc Chuẩn", "Các Agent dễ xung đột hoặc lặp lại lỗi cũ", "TỐN THỜI GIAN ⚠️", "Bạn muốn sở hữu đội ngũ Subagent riêng nhưng không có thời gian tự mày mò kỹ thuật?"),
            ("02 // BƯỚC 1 & BƯỚC 2", "KHẢO SÁT QUY TRÌNH", "& THIẾT KẾ KIẾN TRÚC", "Phân tích điểm nghẽn thực tế và vẽ sơ đồ phân vai Đội ngũ Subagent", "May Đo 100% Theo Việc", "Xác định rõ Tổng quản và các Subagent chuyên môn", "ĐÚNG NHU CẦU ⚡", "Bước một và hai, chúng tôi khảo sát trực tiếp quy trình của bạn để thiết kế sơ đồ Subagent tối ưu nhất."),
            ("03 // BƯỚC 3 & BƯỚC 4", "NẠP BỘ NÃO THỨ 2", "& ĐẤU NỐI ĐA KÊNH", "Huấn luyện tri thức nội bộ và kết nối Zalo, Telegram, Fanpage, CRM", "1. Nạp SOP & Văn Phong", "Hiểu sâu sản phẩm và quy tắc riêng của bạn", "2. Điều Khiển Tự Nhiên", "Ra lệnh và nhận báo cáo ngay trên điện thoại", "Bước ba và bốn, đội ngũ nạp Bộ não thứ hai và đấu nối trực tiếp vào Zalo, Telegram của bạn."),
            ("04 // BƯỚC 5 BÀN GIAO", "CẦM TAY CHỈ VIỆC", "& BẢO HÀNH VẬN HÀNH", "Bàn giao 100% mã nguồn, file cấu hình .MD và hướng dẫn sử dụng chi tiết", "Sở Hữu Vĩnh Viễn", "Dữ liệu nằm an toàn tuyệt đối trên máy của bạn", "AN TÂM 100% ✅", "Bước năm, bàn giao trọn bộ hệ thống kèm hướng dẫn cầm tay chỉ việc và đồng hành bảo hành."),
            ("05 // ĐỐI TƯỢNG PHÙ HỢP", "DÀNH CHO CÁ NHÂN PRO", "& DOANH NGHIỆP SME", "Từ CEO, Quản lý, KOL, Freelancer tới Chủ Shop và Doanh nghiệp", "Tăng Gấp 5 Hiệu Suất", "Vận hành tự động ngay trong tuần đầu tiên", "HIỆU QUẢ NGAY 🚀", "Giải pháp phù hợp hoàn hảo cho cả khách hàng cá nhân bận rộn lẫn doanh nghiệp vừa và nhỏ."),
            ("06 // ĐĂNG KÝ TƯ VẤN", "BÌNH LUẬN: SETUP", "ĐẶT LỊCH KHẢO SÁT 1:1", "Hoặc bấm vào Link Nhóm Zalo VIP tại Bình luận ghim #1 bên dưới!", "Tư Vấn Lộ Trình Riêng", "Miễn phí đánh giá quy trình ban đầu", "NHẮN NGAY 👇", "Bình luận ngay từ khóa Setup hoặc bấm vào bình luận ghim đầu tiên để đặt lịch tư vấn một một nhé!"),
        ],
    },
    {
        "id": "subagent_reel_04_chief_of_staff",
        "slot_dt": "2026-11-05 11:45",
        "cta_kw": "TONGQUAN",
        "accent": "#EC4899",
        "accent2": "#38BDF8",
        "bg_grad": "radial-gradient(circle at 75% 30%, rgba(236,72,153,0.32) 0%, transparent 58%), linear-gradient(165deg, #140510 0%, #260A1E 100%)",
        "layout_mode": "command_pyramid",
        "title": "Trợ Lý Tổng Quản (Chief of Staff Subagent) — Giao 1 Lệnh, Cả Đội Tự Chạy",
        "caption": (
            "👑 TRỢ LÝ TỔNG QUẢN (CHIEF OF STAFF SUBAGENT): CHỈ CẦN GIAO 1 LỆNH, CẢ ĐỘI SUBAGENT TỰ PHỐI HỢP HOÀN TẤT!\n\n"
            "Không cần mở 5 cửa sổ chat khác nhau, Trợ lý Tổng quản sẽ tự phân rã mục tiêu, giao việc song song cho các Subagent và kiểm duyệt đầu ra đạt ≥ 9.0/10 trước khi trình bạn.\n\n"
            "👉 Bình luận 'TONGQUAN' hoặc xem Bình luận ghim #1 để thiết lập Trợ lý Tổng quản riêng cho bạn! 👇"
        ),
        "scenes": [
            ("01 // ĐIỂM NGHẼN ĐIỀU PHỐI", "CÓ NHIỀU CÔNG CỤ AI", "MÀ VẪN PHẢI TỰ LÀM?", "Bạn đang phải làm người đưa thư copy kết quả từ con AI này sang con AI khác", "Mệt Mỏi Điều Phối", "Tốn hàng giờ ghép nối từng mảnh kết quả rời rạc", "KÉM HIỆU QUẢ ⚠️", "Tại sao bạn dùng nhiều công cụ AI nhưng vẫn mất hàng giờ tự mình ghép nối kết quả?"),
            ("02 // VỊ TRÍ TỔNG QUẢN", "CHIEF OF STAFF", "NHẠC TRƯỞNG CỦA ĐỘI AI", "Đứng giữa chủ nhân và dàn Subagent chuyên môn để điều phối tự động", "Chỉ Cần 1 Cửa Sổ", "Bạn chỉ giao tiếp với duy nhất Tổng Quản Mama", "NHÀN NHÃ ⚡", "Đó là vì đội ngũ của bạn đang thiếu một Trợ lý Tổng quản đóng vai trò nhạc trưởng."),
            ("03 // PHÂN RÃ & CHẠY SONG SONG", "GIAO 1 MỤC TIÊU LỚN", "TỰ CHIA 5 NHÁNH VIỆC", "Kích hoạt đồng thời các Subagent Nghiên cứu, Viết bài, Thiết kế, Lên lịch", "1. Phân Vai Tự Động", "Giao đúng việc cho đúng Subagent chuyên môn", "2. Chạy Song Song", "Rút ngắn 80% thời gian hoàn thành chiến dịch", "Khi nhận một yêu cầu từ bạn, Tổng quản tự động chia nhỏ và gọi các Subagent chạy song song."),
            ("04 // CỔNG DUYỆT HARD GATE", "CHẤM ĐIỂM ≥ 9.0/10", "TRƯỚC KHI TRÌNH SẾP", "Bản nháp nào dưới 9 điểm sẽ bị Tổng quản yêu cầu Subagent sửa lại ngay", "Kiểm Duyệt Khắt Khe", "Đảm bảo kết quả cuối cùng luôn chỉn chu 100%", "CHUẨN VÀNG ✅", "Đặc biệt, Tổng quản sẽ tự chấm điểm và bắt sửa lỗi xong xuôi trước khi báo cáo cho bạn."),
            ("05 // BÁO CÁO NGẮN GỌN", "TÓM TẮT 4–8 DÒNG", "GỬI THẲNG VỀ TELEGRAM", "Đi thẳng vào số liệu kết quả thực tế, không dài dòng văn hoa", "Nắm Trọn Tiến Độ", "Điều hành công việc nhẹ nhàng từ điện thoại", "THỰC CHIẾN 🚀", "Mọi kết quả nghiệm thu đều được tóm tắt ngắn gọn bốn đến tám dòng gửi thẳng về điện thoại."),
            ("06 // SỞ HỮU NGAY", "GÕ: TONGQUAN", "NHẬN MẪU CẤU HÌNH MAMA", "Hoặc bấm vào Link Nhóm Zalo VIP tại Bình luận ghim #1 bên dưới!", "Tặng File Mama.md", "Kèm tư vấn thiết kế Đội ngũ Subagent riêng", "TẢI NGAY 👇", "Bình luận ngay từ khóa Tổng quản hoặc bấm vào bình luận ghim đầu tiên để nhận mẫu cấu hình nhé!"),
        ],
    },
    {
        "id": "subagent_reel_05_sales_cskh_team",
        "slot_dt": "2026-11-05 16:30",
        "cta_kw": "SALESAI",
        "accent": "#F43F5E",
        "accent2": "#FACC15",
        "bg_grad": "radial-gradient(circle at 25% 75%, rgba(244,63,94,0.32) 0%, transparent 58%), linear-gradient(165deg, #160408 0%, #2A0810 100%)",
        "layout_mode": "funnel_radar",
        "title": "Đội Ngũ Subagent Phòng Sales & CSKH Chốt Đơn 24/7 Tăng +240% Chuyển Đổi",
        "caption": (
            "💼 ĐỘI NGŨ SUBAGENT PHÒNG SALES & CSKH: PHẢN HỒI KHÁCH TRONG 3 GIÂY & TĂNG +240% TỶ LỆ CHUYỂN ĐỔI!\n\n"
            "Không để rơi bất kỳ khách hàng nào hỏi giá lúc nửa đêm! Đội ngũ Subagent Sales & CSKH tự động bắt bình luận, tư vấn đúng sản phẩm và dẫn khách vào phễu chốt đơn 24/7.\n\n"
            "👉 Bình luận 'SALESAI' hoặc xem Bình luận ghim #1 để xây dựng Phòng Sales Subagent cho shop/doanh nghiệp của bạn! 👇"
        ),
        "scenes": [
            ("01 // ĐỨT GÃY DOANH THU", "KHÁCH HỎI LÚC 11H ĐÊM", "SÁNG MAI MỚI TRẢ LỜI?", "Chỉ cần chậm 15 phút là khách hàng đã lướt sang mua của đối thủ", "Rơi Rụng 80% Khách", "Chạy quảng cáo tốn kém nhưng mất khách ở khâu bình luận", "LÃNG PHÍ LỚN ⚠️", "Khách bình luận hỏi mua lúc mười một giờ đêm mà sáng hôm sau mới trả lời là mất tám mươi phần trăm đơn hàng!"),
            ("02 // BIỆT ĐỘI SALES SUBAGENT", "TRỰC CHIẾN 24/7/365", "PHẢN HỒI TRONG 3 GIÂY", "Tự động quét toàn bộ bình luận mới trên mọi Fanpage của doanh nghiệp", "Không Ngủ Không Nghỉ", "Phản hồi thân thiện, tự nhiên theo đúng tên khách hàng", "SIÊU TỐC ⚡", "Đội ngũ Subagent Phòng Sales và Chăm sóc khách hàng giúp bạn trực chiến hai tư trên bảy."),
            ("03 // PHỐI HỢP 3 SUBAGENT", "TỪ PHÁ BĂNG THẢO LUẬN", "ĐẾN CHỐT ĐƠN TỰ ĐỘNG", "Kết hợp gắn bình luận ghim, câu hỏi kích mồi và phản hồi cá nhân hóa", "1. Ghim Link Chuẩn Xác", "Tự động gắn đúng link sản phẩm ngay khi bài vừa đăng", "2. Phá Băng Bình Luận", "Kích thích khách hàng để lại câu hỏi tương tác", "Hệ thống tự động gắn bình luận ghim, tạo câu hỏi phá băng và gửi đúng đường dẫn sản phẩm cho từng khách."),
            ("04 // HIỂU SÂU SẢN PHẨM", "TƯ VẤN ĐÚNG TỒN KHO", "& XỬ LÝ TỪ CHỐI KHÉO LÉO", "Nắm chắc bảng giá, ưu đãi hiện hành và giải đáp thắc mắc kỹ thuật", "Chống Bịa Thông Tin", "Khóa cứng bảng giá niêm yết trong cơ sở dữ liệu", "AN TOÀN 100% ✅", "Nhờ kết nối trực tiếp kho dữ liệu sản phẩm, Subagent luôn tư vấn chuẩn xác và bảo mật tuyệt đối."),
            ("05 // ĐỘT PHÁ CHUYỂN ĐỔI", "TĂNG +240% ĐƠN HÀNG", "TỪ LƯỢNG TƯƠNG TÁC CŨ", "Biến từng bình luận dạo thành khách hàng thực sự trong Nhóm Zalo & Shop", "Nhận Setup Trọn Gói", "Thiết kế riêng cho Chủ Shop & Doanh nghiệp SME", "TĂNG TRƯỞNG 🚀", "Chúng tôi nhận thiết kế và bàn giao trọn bộ Phòng Sales Subagent may đo riêng cho cửa hàng của bạn."),
            ("06 // NHẬN TƯ VẤN NGAY", "BÌNH LUẬN: SALESAI", "XÂY PHÒNG SALES TỰ ĐỘNG", "Hoặc bấm vào Link Nhóm Zalo VIP tại Bình luận ghim #1 bên dưới!", "Tặng Kịch Bản Chốt Đơn", "Miễn phí bộ Canned Responses trong Zalo VIP", "BẤM NGAY 👇", "Bình luận ngay từ khóa Sales AI hoặc bấm vào bình luận ghim đầu tiên để được tư vấn triển khai nhé!"),
        ],
    },
    {
        "id": "subagent_reel_06_second_brain_vault",
        "slot_dt": "2026-11-05 20:00",
        "cta_kw": "BONAO",
        "accent": "#8B5CF6",
        "accent2": "#34D399",
        "bg_grad": "radial-gradient(circle at 50% 35%, rgba(139,92,246,0.34) 0%, transparent 58%), linear-gradient(165deg, #090418 0%, #160B30 100%)",
        "layout_mode": "shield_rings",
        "title": "Subagent Bộ Não Thứ 2 Cá Nhân & Doanh Nghiệp — Nhớ 100% Quy Chuẩn",
        "caption": (
            "🧠 SUBAGENT 'BỘ NÃO THỨ 2': BÍ QUYẾT ĐỂ ĐỘI NGŨ SUBAGENT NHỚ 100% QUY TẮC & ĐỒNG BỘ MƯỢT MÀ GIỮA 2 MÁY!\n\n"
            "Mọi lời nhắc nhở, quy chuẩn thiết kế và bài học thực chiến của bạn đều được Subagent Bộ Não Thứ 2 chuẩn hóa thành ký ức vĩnh viễn và kiểm duyệt trước mọi lệnh xuất bản.\n\n"
            "👉 Bình luận 'BONAO' hoặc bấm vào Bình luận ghim #1 để nhận sơ đồ kiến trúc & tư vấn xây dựng Bộ não thứ 2 riêng cho bạn! 👇"
        ),
        "scenes": [
            ("01 // CĂN BỆNH MẤT TRÍ NHỚ", "DẶN AI HÔM TRƯỚC", "HÔM SAU LẠI QUÊN SẠCH?", "Mỗi khi mở cuộc trò chuyện mới, AI thông thường lại quay về con số không", "Lặp Lại Lỗi Cũ", "Phải tốn công sửa đi sửa lại cùng một lỗi thiết kế", "BỰC MÌNH ⚠️", "Bạn có mệt mỏi khi hôm trước vừa dặn AI xong, hôm sau mở tab mới nó lại quên sạch quy tắc?"),
            ("02 // SUBAGENT BỘ NÃO THỨ 2", "THỦ THƯ TRI THỨC", "& NGƯỜI GÁC CỔNG CUỐI CÙNG", "Tự động lắng nghe mọi chỉ đạo mới từ tất cả các cửa sổ làm việc", "Ghi Nhớ Vĩnh Viễn", "Chuẩn hóa thành kho ký ức Markdown & Manifest JSON", "KHÔNG BAO GIỜ QUÊN ⚡", "Khi chúng tôi xây dựng đội ngũ Subagent cho bạn, trái tim của hệ thống chính là Subagent Bộ não thứ hai."),
            ("03 // KIỂM DUYỆT HAI CHIỀU", "CHẶN ĐỨNG 100%", "VIỆC DÙNG NHẦM MẪU CŨ", "Mọi tác vụ trước và sau khi thực thi đều phải đi qua cổng Bộ Não Thứ 2", "1. Trước Khi Làm", "Cấp đúng quy chuẩn mới nhất cho Subagent chuyên môn", "2. Sau Khi Làm Xong", "Kiểm tra đạt chuẩn mới cho phép xuất bản lên kênh", "Mọi công việc trước và sau khi thực thi đều phải đi qua cửa kiểm duyệt của Bộ não thứ hai."),
            ("04 // ĐỒNG BỘ ĐA MÁY TỨC THÌ", "LÀM VIỆC Ở CÔNG TY", "VỀ NHÀ TIẾP NỐI 100%", "Tự động đồng bộ toàn bộ ký ức và bảng nhiệm vụ giữa 2 máy tính", "Liền Mạch Tuyệt Đối", "Mở máy ở nhà lên là nắm bắt ngay 100% tiến độ", "ĐỒNG BỘ 2 CHIỀU ✅", "Toàn bộ ký ức và nhiệm vụ còn được tự động đồng bộ hai chiều giữa máy văn phòng và máy ở nhà."),
            ("05 // TÀI SẢN SỐ ĐỘC QUYỀN", "XÂY DỰNG BỘ NÃO THỨ 2", "CHO RIÊNG BẠN & CÔNG TY", "Tích lũy toàn bộ trí tuệ, quy trình và kinh nghiệm thực chiến theo thời gian", "An Toàn Trên Máy Bạn", "Nhận thiết kế và cài đặt trọn gói tận tay", "TÀI SẢN VĨNH VIỄN 🚀", "Hãy biến toàn bộ kinh nghiệm của bạn và doanh nghiệp thành tài sản trí tuệ vĩnh viễn ngay hôm nay."),
            ("06 // NHẬN SƠ ĐỒ & TƯ VẤN", "BÌNH LUẬN: BONAO", "NHẬN KIẾN TRÚC BỘ NÃO #2", "Hoặc bấm vào Link Nhóm Zalo VIP tại Bình luận ghim #1 bên dưới!", "Tặng Mã Nguồn Gatekeeper", "Miễn phí trọn bộ trong Nhóm Zalo VIP", "THAM GIA NGAY 👇", "Bình luận ngay từ khóa Bộ não hoặc bấm vào bình luận ghim đầu tiên để nhận tài liệu và tư vấn nhé!"),
        ],
    },
]


def render_scene_vertical_html(reel: dict, s_idx: int, sc: tuple) -> str:
    """Kết xuất 1 phân cảnh dọc 9:16 (1080x1920) Độc Bản Zero-Clone cho từng Reel & từng Scene."""
    font_css = get_local_fonts_css()
    kicker, h1_a, h1_b, sub, b1_title, b1_desc, b2_title, *rest = sc
    voice_txt = rest[-1]
    b2_desc = rest[0] if len(rest) > 1 else "Triển khai thực chiến 100% cho Cá nhân & Doanh nghiệp"

    acc = reel["accent"]
    acc2 = reel["accent2"]
    bg_grad = reel["bg_grad"]
    mode = reel["layout_mode"]

    # Đa dạng hóa hình học SVG theo từng Reel & từng Scene
    if mode == "orbital_hub":
        svg_art = f"""
        <svg width="880" height="360" viewBox="0 0 880 360">
          <circle cx="440" cy="180" r="145" fill="none" stroke="{acc}" stroke-width="5" stroke-dasharray="14 10"/>
          <circle cx="440" cy="180" r="82" fill="{acc}"/>
          <line x1="440" y1="180" x2="160" y2="70" stroke="{acc2}" stroke-width="5"/>
          <line x1="440" y1="180" x2="720" y2="70" stroke="{acc2}" stroke-width="5"/>
          <line x1="440" y1="180" x2="160" y2="290" stroke="{acc}" stroke-width="5"/>
          <line x1="440" y1="180" x2="720" y2="290" stroke="{acc}" stroke-width="5"/>
          <circle cx="160" cy="70" r="46" fill="#0F172A" stroke="{acc2}" stroke-width="5"/>
          <circle cx="720" cy="70" r="46" fill="#0F172A" stroke="{acc2}" stroke-width="5"/>
          <circle cx="160" cy="290" r="46" fill="#0F172A" stroke="{acc}" stroke-width="5"/>
          <circle cx="720" cy="290" r="46" fill="#0F172A" stroke="{acc}" stroke-width="5"/>
          <text x="440" y="188" text-anchor="middle" fill="#030914" font-size="26" font-weight="900">MAMA</text>
        </svg>"""
    elif mode == "four_pillars":
        svg_art = f"""
        <svg width="880" height="360" viewBox="0 0 880 360">
          <rect x="40" y="50" width="180" height="260" rx="22" fill="#06281E" stroke="{acc}" stroke-width="5"/>
          <rect x="246" y="30" width="180" height="280" rx="22" fill="#06281E" stroke="{acc2}" stroke-width="5"/>
          <rect x="452" y="50" width="180" height="260" rx="22" fill="#06281E" stroke="{acc}" stroke-width="5"/>
          <rect x="658" y="30" width="180" height="280" rx="22" fill="{acc}" stroke="#FFF" stroke-width="4"/>
          <text x="130" y="190" text-anchor="middle" fill="#FFF" font-size="24" font-weight="900">MKT AI</text>
          <text x="336" y="180" text-anchor="middle" fill="{acc2}" font-size="24" font-weight="900">SALES 24/7</text>
          <text x="542" y="190" text-anchor="middle" fill="#FFF" font-size="24" font-weight="900">KẾ TOÁN</text>
          <text x="748" y="180" text-anchor="middle" fill="#04120C" font-size="24" font-weight="900">HR SOP</text>
        </svg>"""
    elif mode == "five_steps":
        svg_art = f"""
        <svg width="880" height="360" viewBox="0 0 880 360">
          <polyline points="70,280 250,210 440,150 630,95 810,45" fill="none" stroke="{acc}" stroke-width="8"/>
          <circle cx="70" cy="280" r="36" fill="{acc}"/>
          <circle cx="250" cy="210" r="36" fill="{acc2}"/>
          <circle cx="440" cy="150" r="36" fill="{acc}"/>
          <circle cx="630" cy="95" r="36" fill="{acc2}"/>
          <circle cx="810" cy="45" r="44" fill="#FFF" stroke="{acc}" stroke-width="6"/>
          <text x="810" y="54" text-anchor="middle" fill="#120B03" font-size="24" font-weight="900">1:1</text>
        </svg>"""
    elif mode == "command_pyramid":
        svg_art = f"""
        <svg width="880" height="360" viewBox="0 0 880 360">
          <polygon points="440,25 140,320 740,320" fill="none" stroke="{acc}" stroke-width="6" stroke-dasharray="14 8"/>
          <circle cx="440" cy="65" r="54" fill="{acc}"/>
          <circle cx="240" cy="285" r="46" fill="#1F091C" stroke="{acc2}" stroke-width="5"/>
          <circle cx="440" cy="285" r="46" fill="#1F091C" stroke="{acc}" stroke-width="5"/>
          <circle cx="640" cy="285" r="46" fill="#1F091C" stroke="{acc2}" stroke-width="5"/>
          <text x="440" y="74" text-anchor="middle" fill="#FFF" font-size="22" font-weight="900">MAMA</text>
        </svg>"""
    elif mode == "funnel_radar":
        svg_art = f"""
        <svg width="880" height="360" viewBox="0 0 880 360">
          <polygon points="120,40 760,40 620,175 260,175" fill="rgba(244,63,94,0.28)" stroke="{acc}" stroke-width="4"/>
          <polygon points="260,190 620,190 520,320 360,320" fill="{acc}" stroke="{acc2}" stroke-width="4"/>
          <text x="440" y="120" text-anchor="middle" fill="#FFF" font-size="28" font-weight="900">TRỰC BÌNH LUẬN 24/7 (3 GIÂY)</text>
          <text x="440" y="268" text-anchor="middle" fill="#FFF" font-size="30" font-weight="900">+240% ĐƠN</text>
        </svg>"""
    else:
        svg_art = f"""
        <svg width="880" height="360" viewBox="0 0 880 360">
          <circle cx="440" cy="180" r="150" fill="none" stroke="{acc}" stroke-width="8" stroke-dasharray="22 10"/>
          <circle cx="440" cy="180" r="105" fill="none" stroke="{acc2}" stroke-width="6"/>
          <circle cx="440" cy="180" r="65" fill="{acc}"/>
          <text x="440" y="188" text-anchor="middle" fill="#FFF" font-size="24" font-weight="900">BỘ NÃO #2</text>
        </svg>"""

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{font_css}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  width: 1080px; height: 1920px; overflow: hidden;
  font-family: 'Be Vietnam Pro', 'Plus Jakarta Sans', sans-serif;
  background: {bg_grad}; color: #FFFFFF; position: relative;
}}
</style></head><body>
  <!-- Brand Header -->
  <div style="position:absolute; top:58px; left:64px; right:64px; display:flex; justify-content:space-between; align-items:center;">
    <div style="background:rgba(255,255,255,0.1); border:2px solid {acc}; padding:12px 28px; border-radius:999px; font-weight:900; font-size:22px; color:{acc};">
      🤖 AI PLAYERS — HỆ SINH THÁI SUBAGENT
    </div>
    <div style="background:{acc}; color:#050811; padding:10px 24px; border-radius:999px; font-weight:900; font-size:22px;">
      SCENE 0{s_idx+1}/06
    </div>
  </div>

  <!-- Kicker & Giant Headline -->
  <div style="position:absolute; top:165px; left:64px; right:64px;">
    <div style="color:{acc2}; font-weight:900; font-size:26px; letter-spacing:1.2px;">{kicker}</div>
    <div style="font-size:64px; font-weight:900; line-height:1.08; margin-top:14px; color:#FFFFFF;">
      {h1_a}<br><span style="color:{acc};">{h1_b}</span>
    </div>
    <div style="font-size:29px; font-weight:700; color:#E2E8F0; margin-top:18px; line-height:1.35;">
      {sub}
    </div>
  </div>

  <!-- Central Bespoke SVG Diagram Box -->
  <div style="position:absolute; top:565px; left:64px; right:64px; height:410px; background:rgba(7,13,25,0.78); border:3.5px solid {acc}; border-radius:38px; display:flex; align-items:center; justify-content:center; box-shadow:0 24px 60px rgba(0,0,0,0.55);">
    {svg_art}
  </div>

  <!-- 2 Comparison / Action Cards -->
  <div style="position:absolute; top:1015px; left:64px; right:64px; height:430px; display:grid; grid-template-columns:1fr 1fr; gap:28px;">
    <div style="background:rgba(15,23,42,0.92); border:3px solid {acc}; border-radius:34px; padding:34px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="background:{acc}; color:#050811; font-weight:900; font-size:22px; padding:8px 20px; border-radius:14px; width:fit-content;">TRỌNG TÂM 01</div>
      <div style="font-size:38px; font-weight:900; color:#FFF; line-height:1.18;">{b1_title}</div>
      <div style="font-size:26px; font-weight:700; color:#CBD5E1; line-height:1.38;">{b1_desc}</div>
    </div>
    <div style="background:linear-gradient(155deg, {acc} 0%, #0F172A 100%); border:3px solid {acc2}; border-radius:34px; padding:34px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="background:#050811; color:{acc2}; font-weight:900; font-size:22px; padding:8px 20px; border-radius:14px; width:fit-content;">TRỌNG TÂM 02</div>
      <div style="font-size:38px; font-weight:900; color:#FFF; line-height:1.18;">{b2_title}</div>
      <div style="font-size:26px; font-weight:700; color:#F8FAFC; line-height:1.38;">{b2_desc}</div>
    </div>
  </div>

  <!-- Subtitle Karaoke Box at Bottom Safe Zone -->
  <div style="position:absolute; bottom:95px; left:64px; right:64px; min-height:290px; background:rgba(5,8,17,0.94); border:4px solid {acc2}; border-radius:36px; padding:34px 42px; display:flex; flex-direction:column; justify-content:center; box-shadow:0 20px 50px rgba(0,0,0,0.75);">
    <div style="color:{acc2}; font-weight:900; font-size:22px; margin-bottom:10px;">🎙️ THUYẾT MINH THỰC CHIẾN // MÃ TƯ VẤN 1:1: {reel['cta_kw']}</div>
    <div style="font-size:35px; font-weight:900; color:#FFFFFF; line-height:1.32;">
      “{voice_txt}”
    </div>
  </div>
</body></html>"""


def get_audio_duration(mp3_path: Path) -> float:
    cmd = [FFPROBE_EXE, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        val = float(res.stdout.strip())
        return val if val > 1.0 else 5.2
    except Exception:
        return 5.2


def build_one_reel_mp4(reel: dict) -> Path:
    rid = reel["id"]
    out_mp4 = REELS_DIR / f"{rid}.mp4"
    r_scene_dir = SCENES_DIR / rid
    r_audio_dir = AUDIO_DIR / rid
    r_scene_dir.mkdir(parents=True, exist_ok=True)
    r_audio_dir.mkdir(parents=True, exist_ok=True)

    segment_mp4s = []
    for s_idx, sc in enumerate(reel["scenes"]):
        img_p = r_scene_dir / f"scene_{s_idx+1}.jpg"
        mp3_p = r_audio_dir / f"scene_{s_idx+1}.mp3"
        seg_p = r_scene_dir / f"seg_{s_idx+1}.mp4"

        html = render_scene_vertical_html(reel, s_idx, sc)
        render_html_to_image(html, img_p, width=1080, height=1920)

        voice_txt = sc[-1]
        if not mp3_p.is_file() or mp3_p.stat().st_size < 1000:
            for attempt in range(3):
                for provider in ("vbee", "edge"):
                    subprocess.run(
                        [sys.executable, str(TTS_SCRIPT), "--text", voice_txt, "--output", str(mp3_p), "--provider", provider],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
                    )
                    if mp3_p.is_file() and mp3_p.stat().st_size >= 1000:
                        break
                    time.sleep(1.0)
                if mp3_p.is_file() and mp3_p.stat().st_size >= 1000:
                    break
            if not mp3_p.is_file() or mp3_p.stat().st_size < 1000:
                subprocess.run(
                    [FFMPEG_EXE, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "5.5", "-q:a", "9", "-acodec", "libmp3lame", str(mp3_p)],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
                )

        dur = round(get_audio_duration(mp3_p) + 0.35, 2)
        cmd_seg = [
            FFMPEG_EXE, "-y",
            "-loop", "1", "-t", str(dur), "-i", str(img_p),
            "-i", str(mp3_p),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
            "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
            "-shortest", str(seg_p),
        ]
        subprocess.run(cmd_seg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        segment_mp4s.append(seg_p)

    concat_txt = r_scene_dir / "concat.txt"
    concat_txt.write_text("\n".join(f"file '{p.as_posix()}'" for p in segment_mp4s), encoding="utf-8")

    raw_concat = r_scene_dir / "raw_concat.mp4"
    subprocess.run(
        [FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(raw_concat)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True,
    )

    if BGM_PATH.is_file():
        cmd_mix = [
            FFMPEG_EXE, "-y",
            "-i", str(raw_concat),
            "-stream_loop", "-1", "-i", str(BGM_PATH),
            "-filter_complex", "[0:a]volume=1.0[va];[1:a]volume=0.10[ba];[va][ba]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest", str(out_mp4),
        ]
        subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    else:
        shutil.copyfile(raw_concat, out_mp4)

    return out_mp4


def upload_and_schedule_reel(page_id: str, page_token: str, video_path: Path, title: str, description: str, sched_ts: int) -> dict:
    boundary = f"----SubagentReelBoundary{uuid.uuid4().hex}"
    body = bytearray()

    def add_field(name: str, val: str):
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{val}\r\n".encode("utf-8"))

    add_field("access_token", page_token)
    add_field("title", title)
    add_field("description", description)
    add_field("published", "false")
    add_field("scheduled_publish_time", str(sched_ts))

    file_bytes = video_path.read_bytes()
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="source"; filename="{video_path.name}"\r\n'.encode("utf-8"))
    body.extend(b"Content-Type: video/mp4\r\n\r\n")
    body.extend(file_bytes)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))

    url = f"https://graph-video.facebook.com/v22.0/{page_id}/videos"
    req = urllib.request.Request(url, data=bytes(body), headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180.0, context=SSL_CTX) as resp:
            res = json.loads(resp.read().decode("utf-8", errors="ignore"))
            vid = res.get("id", "")
            return {"success": True, "video_id": vid, "post_id": res.get("post_id", f"{page_id}_{vid}")}
    except Exception as e:
        err_msg = e.read().decode("utf-8", errors="ignore") if hasattr(e, "read") else str(e)
        return {"error": err_msg}


def post_pinned_comment_on_video(page_id: str, video_id: str, post_id: str, page_token: str, message: str) -> str:
    for tid in [f"{page_id}_{video_id}", video_id, post_id]:
        if not tid:
            continue
        res = graph_post(f"{tid}/comments", page_token, {"message": message})
        if "id" in res:
            return res["id"]
    return ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true", help="Hẹn giờ 6 Video Reels Subagent Agency lên Page AI Players")
    args = parser.parse_args()

    REELS_DIR.mkdir(parents=True, exist_ok=True)
    ok_tsx, tsx_msg = verify_zero_clone_tsx()
    print(("🛡️ " if ok_tsx else "⚠️ ") + tsx_msg, flush=True)

    pages = load_vault()
    tok = pages[AI_PAGE_ID]["access_token"]
    now_ts = int(dt.datetime.now(VN_TZ).timestamp())
    manifest_out = []

    already_scheduled = {
        "subagent_reel_01_personal_team": ("1144183461419139", "1144183461419139_2193014541282969"),
        "subagent_reel_02_enterprise_depts": ("3420380524815402", "3420380524815402_1100876622748065"),
        "subagent_reel_03_custom_setup_service": ("1623309216475235", "1623309216475235_1692036165697224"),
    }

    print("🎬 Đang kết xuất 6 Video Reels 9:16 (1080x1920 @ 30fps) Tuyến Nội Dung Subagent Cá Nhân & Doanh Nghiệp...")
    for idx, reel in enumerate(SIX_REELS_SPEC, 1):
        mp4_path = REELS_DIR / f"{reel['id']}.mp4"
        if not mp4_path.is_file() or mp4_path.stat().st_size < 100_000:
            mp4_path = build_one_reel_mp4(reel)
        mb = round(mp4_path.stat().st_size / (1024 * 1024), 2)
        print(f"  ✔ [{idx:02d}/06] Đã render Video Reel: {mp4_path.name} ({mb} MB)", flush=True)

        entry = {
            "index": idx,
            "id": reel["id"],
            "slot_dt": reel["slot_dt"],
            "cta_kw": reel["cta_kw"],
            "title": reel["title"],
            "video_path": str(mp4_path),
            "size_mb": mb,
        }

        if reel["id"] in already_scheduled:
            vid, cid = already_scheduled[reel["id"]]
            entry["status"] = "SCHEDULED"
            entry["video_id"] = vid
            entry["post_id"] = f"{AI_PAGE_ID}_{vid}"
            entry["comment_id"] = cid
            print(f"  ⏩ [{reel['id']}] Đã hẹn giờ trước đó ({reel['slot_dt']}) -> video_id={vid} | cmt_id={cid}", flush=True)
            manifest_out.append(entry)
            continue

        if args.publish:
            dt_obj = dt.datetime.strptime(reel["slot_dt"], "%Y-%m-%d %H:%M").replace(tzinfo=VN_TZ)
            sched_ts = int(dt_obj.timestamp())
            if sched_ts <= now_ts + 900:
                sched_ts = now_ts + 1200

            pinned_msg = (
                f"📌 [TÀI LIỆU & ĐẶT LỊCH THIẾT KẾ ĐỘI NGŨ SUBAGENT 1:1 — MÃ: {reel['cta_kw']}]\n"
                f"👉 Bấm vào Nhóm Zalo VIP \"AI Players — Hệ Sinh Thái Subagent Cá Nhân & Doanh Nghiệp\" để tải miễn phí Bộ Khung 10 Subagent (.MD) & Đăng ký Khảo sát Xây dựng Đội ngũ Subagent may đo riêng cho bạn:\n"
                f"🔗 Link nhận tài liệu & tư vấn 1:1: {ZALO_URL}"
            )
            up = upload_and_schedule_reel(AI_PAGE_ID, tok, mp4_path, reel["title"], reel["caption"], sched_ts)
            if "error" in up:
                entry["status"] = "ERROR"
                entry["error"] = up["error"]
                print(f"  ❌ [{reel['id']}] Lỗi upload: {up['error']}", flush=True)
            else:
                vid = up["video_id"]
                pid = up["post_id"]
                record_published_content(AI_PAGE_ID, mp4_path, reel["caption"], str(pid))
                cid = post_pinned_comment_on_video(AI_PAGE_ID, vid, pid, tok, pinned_msg)
                entry["status"] = "SCHEDULED"
                entry["video_id"] = vid
                entry["post_id"] = pid
                entry["comment_id"] = cid
                print(f"  ✅ [{reel['id']}] SCHEDULED ({reel['slot_dt']}) -> video_id={vid} | cmt_id={cid}", flush=True)

        manifest_out.append(entry)

    REELS_MANIFEST_PATH.write_text(json.dumps(manifest_out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📄 Đã lưu Manifest 6 Video Reels tại: {REELS_MANIFEST_PATH}", flush=True)


if __name__ == "__main__":
    main()
