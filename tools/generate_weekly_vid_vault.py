#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_weekly_vid_vault.py — Tạo Trọn Bộ 42 Ảnh Vuông 1:1 Chuẩn Style c:\\Users\\guicci\\Downloads\\vid
Cho Kho Nội Dung 1 Tuần Của Page AI Players (26/10 - 01/11/2026)

Tuân thủ tuyệt đối:
- Zero Raw Pillow Geometry: 100% render bằng headless Chrome engine (render_vid_style_card.py).
- Unclipped 1080x1080 Viewport: Window margin +120x170 để không mất viền dưới.
- Luân phiên 5 Archetypes từ bộ ảnh tham chiếu:
  + Layout 1: Hero Showcase (Tool Lime Card + Model Neon Grid Tunnel)
  + Layout 2: Curriculum 4 Skills / Breakdown (Lime numbers 01-04 + vertical/horizontal lines)
  + Layout 3: Matrix 2x2 (Level pill + Bracket title + 2x2 pills + 8-spoke Asterisk logo)
  + Layout 4: Offer / Lead Magnet (Top lime tab + 3 date boxes + Zoom logo + CTA button)
  + Layout 5: Urgency Slots (Sold Out header + 2 progress bars + clock dial CTA)
"""

import os
import sys
import json
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
VAULT_DIR = SUBAGENT_DIR / "campaigns" / "2026-10-26" / "ai-players-weekly-vault"
IMAGES_DIR = VAULT_DIR / "images"
CAPTIONS_DIR = VAULT_DIR / "captions"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
CAPTIONS_DIR.mkdir(parents=True, exist_ok=True)

# Import các hàm render từ render_vid_style_card.py
from render_vid_style_card import (
    render_template_hero_showcase,
    render_template_curriculum_breakdown,
    render_template_feature_matrix,
    render_template_offer_card,
    render_template_urgency_slots,
)

# ==============================================================================
# DANH MỤC 42 BÀI ĐĂNG CHI TIẾT CHO 7 NGÀY (6 BÀI / NGÀY)
# ==============================================================================

VAULT_POSTS = [
    # -------------------------------------------------------------------------
    # NGÀY 1: Thứ Hai 26/10
    # -------------------------------------------------------------------------
    {
        "day": 1, "date": "2026-10-26", "slot": "14:15", "code": "day1_img1_1415_repo",
        "template": 1,
        "params": {
            "top_badge": "Thực hành với",
            "tool_title_line1": "BROWSER",
            "tool_title_line2": "USE",
            "bottom_badge": "Cốt lõi công nghệ",
            "model_name": "STAGEHAND 2.0"
        },
        "title": "Review GitHub Hot: Repo browser-use (55,000+ Stars)",
        "cta_kw": "REPO",
        "caption": "🔥 REPO HOT NHẤT GITHUB TUẦN QUA: BROWSER-USE (55,000+ STARS)!\n\nBạn có tin chỉ cần gõ 1 dòng prompt bằng tiếng Việt, AI sẽ tự bật trình duyệt, điền form, săn vé máy bay giá rẻ và tải hóa đơn về máy cho bạn?\n\nĐó chính là sức mạnh của browser-use kết hợp mô hình Stagehand 2.0. Không còn cảnh phải viết code Selenium hay Puppeteer phức tạp nữa.\n\n👇 Muốn nhận trọn bộ tài liệu cài đặt và mã nguồn mẫu? Hãy bình luận 'REPO' ngay bên dưới, mình gửi link Drive qua inbox trong 30 giây!",
        "comment": "👉 Nhận tài liệu và mã nguồn cài đặt browser-use 100% miễn phí tại đây nhé: https://github.com/browser-use/browser-use (Hoặc chat từ khóa REPO để nhận hướng dẫn Việt hóa)"
    },
    {
        "day": 1, "date": "2026-10-26", "slot": "15:45", "code": "day1_img2_1545_voice",
        "template": 2,
        "params": {
            "left_badge": "So sánh thực chiến",
            "right_badge": "4 tiêu chí",
            "items": [
                {"num": "01", "title": "TỐC ĐỘ GENERATE LOCAL", "desc": "Xử lý 100% trên card GPU không lo gián đoạn mạng hay nghẽn API máy chủ.", "pink_kw": "Xử lý 100% trên card GPU"},
                {"num": "02", "title": "CHI PHÍ VẬN HÀNH 0Đ", "desc": "Tiết kiệm hoàn toàn $99/tháng tiền thuê server cloud giọng đọc nước ngoài.", "pink_kw": "Tiết kiệm hoàn toàn $99/tháng"},
                {"num": "03", "title": "KHẢ NĂNG CLONE GIỌNG", "desc": "Nhân bản giọng nói chuẩn xác chỉ với 5 giây mẫu audio sạch không lẫn tạp âm.", "pink_kw": "5 giây mẫu audio sạch"},
                {"num": "04", "title": "BẢO MẬT DỮ LIỆU TUYỆT ĐỐI", "desc": "Dữ liệu thoại và kịch bản kinh doanh không bao giờ rời khỏi máy tính cá nhân.", "pink_kw": "Bảo mật dữ liệu tuyệt đối"}
            ]
        },
        "title": "So Sánh Thực Chiến: F5-TTS 0đ Local vs Voice Tool $99/Tháng",
        "cta_kw": "VOICE",
        "caption": "🎙️ TẠI SAO BẠN PHẢI TRẢ $99/THÁNG TRONG KHI CÓ THỂ CHẠY F5-TTS LOCAL 0Đ?\n\nNhiều anh em làm video ngắn vẫn đang cúng tiền hàng tháng cho các tool cloud nước ngoài vì nghĩ AI giọng đọc local phức tạp.\n\nNhìn vào 4 tiêu chí so sánh thực tế trên ảnh: F5-TTS local vượt trội về tốc độ render, chi phí 0đ trọn đời và đặc biệt là độ bảo mật kịch bản.\n\n👇 Bình luận 'VOICE' để nhận file Docker compose và notebook chạy F5-TTS trên máy của bạn!",
        "comment": "👉 Kho voice clone F5-TTS local chuẩn tiếng Việt cho anh em dựng video: https://github.com/SWivid/F5-TTS (Gõ 'VOICE' để lấy prompt tinh chỉnh ngữ điệu)"
    },
    {
        "day": 1, "date": "2026-10-26", "slot": "17:15", "code": "day1_img3_1715_prompt50",
        "template": 4,
        "params": {
            "header_badge": "Quà tặng độc quyền",
            "bracket_title_colored": '[ <span style="color:#CCFF00">SIÊU</span> <span style="color:#FF2A6D">PROMPT 50</span> ]',
            "selector_badge": "Tải ngay trọn bộ template thực chiến",
            "date_cards": [
                {"label": "Tài liệu", "date": "68 Trang", "highlight": False},
                {"label": "Kho mẫu", "date": "50 Mẫu", "highlight": True},
                {"label": "Định dạng", "date": "Copy 1-Click", "highlight": True}
            ],
            "time_badge": "Mở cổng nhận quà: Hôm nay - Hết tuần",
            "delivery_text": "Nhận link Drive tự động qua",
            "cta_button_text": "NHẬN MIỄN PHÍ"
        },
        "title": "Tặng Sổ Tay 50 Siêu Prompt Văn Phòng & Lập Trình Thực Chiến",
        "cta_kw": "PROMPT50",
        "caption": "🎁 TẶNG MIỄN PHÍ: SỔ TAY 50 SIÊU PROMPT DÀNH CHO DÂN CÔNG NGHỆ & MARKETING!\n\nKhông phải prompt chung chung kiểu 'hãy đóng vai một chuyên gia'. Đây là 50 prompt có cấu trúc chặt chẽ (Role - Context - Task - Constraints - Output Format) được tinh chỉnh thực chiến suốt 6 tháng qua.\n\nÁp dụng được ngay cho ChatGPT, Claude 3.5, Gemini và Cursor để x3 tốc độ làm việc.\n\n👇 Bình luận 'PROMPT50' ngay bên dưới, bot sẽ gửi link tải trực tiếp vào tin nhắn của bạn!",
        "comment": "👉 Đã mở link tải trọn bộ Sổ tay 50 Siêu Prompt (bản PDF + Markdown): Nhắn 'PROMPT50' để nhận link Drive không qua rút gọn!"
    },
    {
        "day": 1, "date": "2026-10-26", "slot": "18:45", "code": "day1_img4_1845_khobau",
        "template": 1,
        "params": {
            "top_badge": "Khám phá repo hot",
            "tool_title_line1": "AWESOME",
            "tool_title_line2": "LLM APPS",
            "bottom_badge": "Kiến trúc tích hợp",
            "model_name": "LANGCHAIN & RAG"
        },
        "title": "Mở Rương Kho Báu: 30,000+ Stars Repo Awesome-LLM-Apps",
        "cta_kw": "KHOBAU",
        "caption": "💎 MỞ RƯƠNG KHO BÁU: 30,000+ STARS REPO AWESOME-LLM-APPS!\n\nNếu bạn muốn xây dựng app AI thực tế nhưng chưa biết bắt đầu từ đâu, đừng sáng tạo lại bánh xe.\n\nRepo này tập hợp hơn 100 dự án mã nguồn mở hoàn chỉnh: từ Chatbot hỏi đáp PDF, Trợ lý phân tích thị trường chứng khoán đến Agent tự động nghiên cứu mạng xã hội.\n\n👇 Để lại bình luận 'KHOBAU' để nhận danh sách phân loại chi tiết theo từng lĩnh vực!",
        "comment": "👉 Xem trực tiếp repo Awesome-LLM-Apps tại: https://github.com/Shubhamsaboo/awesome-llm-apps (Bình luận 'KHOBAU' để nhận bộ slide dịch tiếng Việt)"
    },
    {
        "day": 1, "date": "2026-10-26", "slot": "20:45", "code": "day1_img5_2045_hethong",
        "template": 3,
        "params": {
            "level_badge": "Hệ Thống Tự Hành",
            "bracket_title_colored": '[ <span style="color:#CCFF00">AGENT</span> <span style="color:#FF2A6D">JAVIS</span> ]',
            "meta_info_left": "Vận hành 24/7 qua",
            "meta_info_right": "10 Subagent Chuyên Biệt | Đồng Bộ 2 Chiều",
            "cards_2x2": [
                {"icon": "flow", "title": "mama Chief", "subtitle": "Tổng quản điều phối"},
                {"icon": "book", "title": "mkt & content", "subtitle": "Săn trend & viết script"},
                {"icon": "key", "title": "edit & voice", "subtitle": "Dựng video & làm giọng"},
                {"icon": "num", "num_or_icon": "4", "title": "Vận hành kênh", "subtitle": "Đăng bài & chăm sóc"}
            ],
            "footer_title_white": "ĐỘI NGŨ SUBAGENT TỰ HÀNH",
            "footer_title_pink": "THAY THẾ 1 PHÒNG VẬN HÀNH"
        },
        "title": "Sơ Đồ Dây Chuyền Subagent 24/7 Tự Hành Thay Thế 1 Phòng Vận Hành",
        "cta_kw": "HETHONG",
        "caption": "⚙️ CÁCH 1 NGƯỜI VẬN HÀNH 4 KÊNH MẠNG XÃ HỘI VỚI ĐỘI NGŨ 10 SUBAGENT AI!\n\nKhông cần thuê cả team marketing cồng kềnh. Bằng cách phân tách vai trò rõ ràng theo mô hình Chief of Staff (`mama`), mỗi Subagent chịu trách nhiệm đúng 1 khâu:\n- `mkt`: Nghiên cứu đối thủ & săn sản phẩm hot.\n- `content`: Viết kịch bản theo công thức Hook 3s.\n- `edit`: Lên Storyboard & Motion Prompt chuẩn xác.\n- `quan-ly-kenh`: Tự động lên lịch vào khung giờ vàng.\n\n👇 Comment 'HETHONG' để nhận sơ đồ kiến trúc và file prompt gốc của đội Subagent!",
        "comment": "👉 Chi tiết kiến trúc đội Subagent tự hành 10 vai trò: Bình luận 'HETHONG' để xem bản vẽ kỹ thuật và checklist triển khai."
    },
    {
        "day": 1, "date": "2026-10-26", "slot": "21:45", "code": "day1_img6_2145_abcd",
        "template": 2,
        "params": {
            "left_badge": "Tự động hóa 2026",
            "right_badge": "4 tác vụ",
            "items": [
                {"num": "01", "title": "QUÉT & TỔNG HỢP TIN TỨC", "desc": "Theo dõi 20 nguồn công nghệ quốc tế và gửi bản tin tóm tắt vào 8h00 mỗi sáng.", "pink_kw": "bản tin tóm tắt vào 8h00"},
                {"num": "02", "title": "TÁI CẤU TRÚC ĐA NỀN TẢNG", "desc": "Chuyển 1 bài viết dài thành bài post ngắn, Reels script và Threads carousel.", "pink_kw": "Chuyển 1 bài viết dài"},
                {"num": "03", "title": "KIỂM TRA LỖI CODE TỰ ĐỘNG", "desc": "Quét sạch cú pháp, type check và format chuẩn trước khi commit vào git.", "pink_kw": "Quét sạch cú pháp"},
                {"num": "04", "title": "CHĂM SÓC BÌNH LUẬN 24/7", "desc": "Tự động bắt từ khóa để gửi tài liệu và chăm sóc khách hàng ngay lập tức.", "pink_kw": "chăm sóc khách hàng ngay lập tức"}
            ]
        },
        "title": "Khảo Sát Tương Tác: 4 Việc Nên Giao Cho AI Tự Làm Ngay Hôm Nay",
        "cta_kw": "ABCD",
        "caption": "📊 BẠN NÊN GIAO VIỆC NÀO CHO AI TỰ LÀM ĐẦU TIÊN TRONG 4 VIỆC TRÊN?\n\nA. Quét & tổng hợp tin tức công nghệ mỗi sáng\nB. Tái cấu trúc nội dung từ 1 bài dài sang đa nền tảng\nC. Tự động kiểm tra lỗi code và định dạng dự án\nD. Bắt từ khóa để chăm sóc bình luận và gửi link tài liệu\n\n👇 Hãy để lại chữ cái lựa chọn của bạn (A, B, C hoặc D) bên dưới nhé, mình sẽ chia sẻ script mẫu cho lựa chọn có nhiều vote nhất!",
        "comment": "👉 Vote ngay A, B, C hoặc D bên dưới! Kết quả và script giải pháp sẽ được công bố vào 20:00 tối mai."
    },

    # -------------------------------------------------------------------------
    # NGÀY 2: Thứ Ba 27/10
    # -------------------------------------------------------------------------
    {
        "day": 2, "date": "2026-10-27", "slot": "08:30", "code": "day2_img1_0830_artifacts",
        "template": 1,
        "params": {
            "top_badge": "Thực hành với",
            "tool_title_line1": "CLAUDE",
            "tool_title_line2": "ARTIFACTS",
            "bottom_badge": "Kiến trúc tương tác",
            "model_name": "SONNET 3.5"
        },
        "title": "Claude 3.5 Artifacts: Biến Ý Tưởng Thành App Chạy Được Trong 30 Giây",
        "cta_kw": "ARTIFACTS",
        "caption": "⚡ CLAUDE 3.5 ARTIFACTS: BIẾN Ý TƯỞNG THÀNH APP WEB CHẠY ĐƯỢC TRONG 30 GIÂY!\n\nKhông cần mở VS Code, không cần cài node hay npm. Bạn chỉ cần mô tả giao diện bằng tiếng Việt, Claude sẽ tự viết React component và hiển thị bản live demo trực tiếp bên cạnh cửa sổ chat.\n\n👇 Bình luận 'ARTIFACTS' để nhận bộ 10 prompt mẫu tạo Dashboard, Game mini và Công cụ tính toán nhanh!",
        "comment": "👉 Xem trọn bộ tài liệu làm chủ Claude Artifacts: Bình luận 'ARTIFACTS' nhận link kho mã nguồn mẫu."
    },
    {
        "day": 2, "date": "2026-10-27", "slot": "10:15", "code": "day2_img2_1015_ollama",
        "template": 2,
        "params": {
            "left_badge": "Kiến trúc mô hình",
            "right_badge": "4 yếu tố",
            "items": [
                {"num": "01", "title": "BẢO MẬT TUYỆT ĐỐI (AIR-GAPPED)", "desc": "Dữ liệu mật của doanh nghiệp không bao giờ gửi ra ngoài máy chủ nội bộ.", "pink_kw": "Bảo mật tuyệt đối"},
                {"num": "02", "title": "CHI PHÍ API BẰNG 0", "desc": "Chạy hàng triệu token mỗi ngày không phát sinh chi phí hóa đơn cuối tháng.", "pink_kw": "Chi phí API bằng 0"},
                {"num": "03", "title": "YÊU CẦU PHẦN CỨNG THỰC TẾ", "desc": "Cần tối thiểu 16GB RAM cho model 7B và GPU 12GB VRAM để chạy mượt mà.", "pink_kw": "GPU 12GB VRAM"},
                {"num": "04", "title": "ĐỘ CHÍNH XÁC & SUY LUẬN", "desc": "Cloud API (Claude/GPT-4o) vẫn nhỉnh hơn ở các tác vụ lập luận đa bước phức tạp.", "pink_kw": "Cloud API vẫn nhỉnh hơn"}
            ]
        },
        "title": "Local LLM vs Cloud API: Khi Nào Nên Chạy Ollama Trên Máy Riêng?",
        "cta_kw": "OLLAMA",
        "caption": "💻 KHI NÀO NÊN DÙNG OLLAMA LOCAL VÀ KHI NÀO NÊN GỌI CLOUD API?\n\nChạy LLM offline trên máy tính cá nhân đang là xu hướng cực nóng nhờ Ollama. Nhưng không phải bài toán nào cũng nên chạy local.\n\nHãy đọc kỹ 4 yếu tố then chốt trên ảnh trước khi quyết định đầu tư dàn PC đắt tiền.\n\n👇 Bình luận 'OLLAMA' để nhận danh sách top 5 model local tiếng Việt tốt nhất hiện nay!",
        "comment": "👉 Tải Ollama và hướng dẫn cấu hình: https://ollama.com (Gõ 'OLLAMA' để lấy lệnh kéo model Llama 3.2 tiếng Việt)"
    },
    {
        "day": 2, "date": "2026-10-27", "slot": "13:30", "code": "day2_img3_1330_subagent",
        "template": 3,
        "params": {
            "level_badge": "Cấu Trúc Subagent",
            "bracket_title_colored": '[ <span style="color:#CCFF00">SUB</span><span style="color:#FF2A6D">AGENT.MD</span> ]',
            "meta_info_left": "Đóng gói chuẩn",
            "meta_info_right": "Mô Hình Chuyên Biệt | 0-Token Leak",
            "cards_2x2": [
                {"icon": "key", "title": "Persona & Rule", "subtitle": "Định vị vai trò cốt lõi"},
                {"icon": "book", "title": "Knowledge Path", "subtitle": "Chỉ đọc tài liệu chuyên môn"},
                {"icon": "flow", "title": "Hard Gates", "subtitle": "Chặn lỗi trước khi bàn giao"},
                {"icon": "num", "num_or_icon": "10", "title": "Rubric /10", "subtitle": "Tự chấm điểm chất lượng"}
            ],
            "footer_title_white": "ĐÓNG GÓI SUBAGENT .MD",
            "footer_title_pink": "TIÊU CHUẨN VẬN HÀNH 2026"
        },
        "title": "Bản Vẽ Quy Trình Đóng Gói Prompt Thành Subagent .MD Độc Lập",
        "cta_kw": "SUBAGENT",
        "caption": "📁 CÁCH ĐÓNG GÓI 1 CHUYÊN GIA AI THÀNH 1 FILE .MD DUY NHẤT!\n\nThay vì viết những prompt dài cả nghìn chữ nhồi nhét vào 1 cửa sổ chat, bí quyết của các đội kỹ sư AI hàng đầu là 'Subagent Modularization':\n1 file `.md` chứa đủ Role, Knowledge Rules, Output Schema và Rubric tự chấm điểm.\n\n👇 Bình luận 'SUBAGENT' để nhận trọn bộ template mẫu chuẩn Antigravity / Claude Code!",
        "comment": "👉 Nhận template file Subagent.md chuẩn quốc tế: Comment 'SUBAGENT' để lấy repo mã nguồn mẫu."
    },
    {
        "day": 2, "date": "2026-10-27", "slot": "15:15", "code": "day2_img4_1515_sqlai",
        "template": 4,
        "params": {
            "header_badge": "Tài liệu kỹ thuật",
            "bracket_title_colored": '[ <span style="color:#CCFF00">SQL</span> & <span style="color:#FF2A6D">AI 2026</span> ]',
            "selector_badge": "20 Siêu Prompt Truy Vấn Dữ Liệu",
            "date_cards": [
                {"label": "Cơ sở", "date": "SQLite / Postgre", "highlight": False},
                {"label": "Kho mẫu", "date": "20 Prompt", "highlight": True},
                {"label": "Độ chính xác", "date": "100% No-Leak", "highlight": True}
            ],
            "time_badge": "Mở cổng nhận quà: Hôm nay - Hết tuần",
            "delivery_text": "Tự động gửi link Drive qua",
            "cta_button_text": "NHẬN TÀI LIỆU"
        },
        "title": "Bộ 20 Prompt Tối Ưu Hóa Truy Vấn SQL & Xử Lý Dữ Liệu Báo Cáo",
        "cta_kw": "SQLAI",
        "caption": "📊 TRUY VẤN DỮ LIỆU BẰNG TIẾNG VIỆT TỰ NHIÊN: BỘ 20 PROMPT SQL CHO DÂN DATA!\n\nKhông cần nhớ câu lệnh JOIN phức tạp hay hàm WINDOW function. Bộ prompt này giúp bạn chuyển câu hỏi nghiệp vụ thành câu truy vấn SQL chuẩn xác, tối ưu index và chống SQL Injection.\n\n👇 Comment 'SQLAI' ngay bên dưới để bot gửi file PDF hướng dẫn vào inbox nhé!",
        "comment": "👉 Tải bộ 20 prompt SQL tối ưu dữ liệu báo cáo: Bình luận 'SQLAI' để nhận tài liệu ngay."
    },
    {
        "day": 2, "date": "2026-10-27", "slot": "18:15", "code": "day2_img5_1815_deepseek",
        "template": 1,
        "params": {
            "top_badge": "Mô hình mã nguồn mở",
            "tool_title_line1": "DEEPSEEK",
            "tool_title_line2": "CODER",
            "bottom_badge": "Kiến trúc MoE",
            "model_name": "DEEPSEEK V3"
        },
        "title": "Giải Phẫu Kiến Trúc DeepSeek-Coder: Đỉnh Cao Code Open-Source",
        "cta_kw": "DEEPSEEK",
        "caption": "🧠 GIẢI PHẪU DEEPSEEK-CODER: TẠI SAO CẢ THẾ GIỚI PHẢI BẤT NGỜ?\n\nVới chi phí huấn luyện chỉ bằng một phần nhỏ so với các ông lớn công nghệ, DeepSeek V3 và DeepSeek-Coder đã đạt điểm số ngang ngửa GPT-4o trên các bảng xếp hạng lập trình khắt khe nhất.\n\nBí mật nằm ở kiến trúc MoE (Mixture of Experts) thông minh và cơ chế tối ưu token cực hạn.\n\n👇 Bình luận 'DEEPSEEK' để nhận tài liệu phân tích kỹ thuật và hướng dẫn gọi API với giá siêu rẻ!",
        "comment": "👉 Tìm hiểu thêm về DeepSeek V3 và trải nghiệm trực tiếp: https://chat.deepseek.com (Comment 'DEEPSEEK' để lấy guide tích hợp vào Cursor)"
    },
    {
        "day": 2, "date": "2026-10-27", "slot": "21:15", "code": "day2_img6_2115_n8nhub",
        "template": 2,
        "params": {
            "left_badge": "Tự động hóa n8n",
            "right_badge": "4 bước",
            "items": [
                {"num": "01", "title": "TẠO WEBHOOK TRIGGER TRÊN N8N", "desc": "Mở endpoint nhận tín hiệu POST từ mạng xã hội hoặc CRM chỉ trong 1 click.", "pink_kw": "chỉ trong 1 click"},
                {"num": "02", "title": "BÓC TÁCH DỮ LIỆU BẰNG CODE NODE", "desc": "Chuẩn hóa payload đầu vào thành JSON sạch sẽ, loại bỏ ký tự rác và HTML thừa.", "pink_kw": "Chuẩn hóa payload"},
                {"num": "03", "title": "GỌI AI MODEL PHÂN TÍCH NHANH", "desc": "Sử dụng Gemini Flash hoặc Claude Haiku với tốc độ phản hồi dưới 1 giây.", "pink_kw": "dưới 1 giây"},
                {"num": "04", "title": "BẮN THÔNG BÁO VỀ TELEGRAM", "desc": "Gửi kết quả kèm nút bấm hành động trực tiếp vào nhóm quản lý nội bộ.", "pink_kw": "nút bấm hành động trực tiếp"}
            ]
        },
        "title": "Checklist 4 Bước Triển Khai n8n Webhook Không Cần Biết Viết Code",
        "cta_kw": "N8NHUB",
        "caption": "⚡ CHECKLIST 4 BƯỚC TỰ ĐỘNG HÓA VỚI N8N WEBHOOK CHO NGƯỜI MỚI BẮT ĐẦU!\n\nn8n đang là nền tảng tự động hóa mã nguồn mở mạnh mẽ nhất hiện nay. Chỉ với 4 bước đơn giản như trên ảnh, bạn đã có thể xây xong một trạm điều phối tự động kết nối mạng xã hội với bot Telegram.\n\n👇 Bình luận 'N8NHUB' để nhận file workflow .json kéo-thả dùng được ngay!",
        "comment": "👉 Tải workflow n8n tự động hóa miễn phí: Comment 'N8NHUB' để nhận file template JSON import 1-click."
    },

    # -------------------------------------------------------------------------
    # NGÀY 3: Thứ Tư 28/10
    # -------------------------------------------------------------------------
    {
        "day": 3, "date": "2026-10-28", "slot": "08:30", "code": "day3_img1_0830_remotion",
        "template": 1,
        "params": {
            "top_badge": "Dựng video bằng code",
            "tool_title_line1": "REMOTION",
            "tool_title_line2": "FRAMEWORK",
            "bottom_badge": "Render Engine",
            "model_name": "REACT & FFMPEG"
        },
        "title": "Remotion 4.0: Biến Code React Thành Video Ngắn 9:16 Không Cần Mở Premiere",
        "cta_kw": "REMOTION",
        "caption": "🎬 DỰNG VIDEO BẰNG REACT CODE THAY VÌ PHẦN MỀM THỦ CÔNG: BẠN ĐÃ THỬ CHƯA?\n\nRemotion cho phép bạn biến toàn bộ hiệu ứng chuyển cảnh, chữ chạy kinetic và nhạc nền thành mã nguồn React. Render hàng trăm video ngắn chuẩn 1080x1920 chỉ bằng 1 dòng lệnh terminal.\n\n👇 Comment 'REMOTION' để nhận template video explainer chuẩn vàng đang được dùng trên kênh này!",
        "comment": "👉 Kho template Remotion video ngắn chuẩn vàng: Bình luận 'REMOTION' để nhận source code GitHub."
    },
    {
        "day": 3, "date": "2026-10-28", "slot": "10:15", "code": "day3_img2_1015_voicetest",
        "template": 2,
        "params": {
            "left_badge": "Kiểm nghiệm giọng đọc",
            "right_badge": "4 yếu tố",
            "items": [
                {"num": "01", "title": "ĐỘ TỰ NHIÊN CỦA NGỮ ĐIỆU", "desc": "Giọng Edge-TTS (Nam Minh, Hoài My) ngắt nghỉ chuẩn theo dấu phẩy tiếng Việt.", "pink_kw": "ngắt nghỉ chuẩn theo dấu phẩy"},
                {"num": "02", "title": "TỐC ĐỘ XỬ LÝ SIÊU TỐC", "desc": "Render file mp3 60 giây chỉ mất chưa đầy 1.5 giây qua giao thức websocket.", "pink_kw": "chưa đầy 1.5 giây"},
                {"num": "03", "title": "ĐIỀU CHỈNH ÂM LƯỢNG & TỐC ĐỘ", "desc": "Tăng speed 1.12x và volume -3dB để giọng đọc chắc nịch, cuốn hút người nghe.", "pink_kw": "Tăng speed 1.12x"},
                {"num": "04", "title": "TÍCH HỢP TỰ ĐỘNG HÓA HOÀN TOÀN", "desc": "Gọi trực tiếp từ Python script mà không cần token API hay thẻ thanh toán quốc tế.", "pink_kw": "không cần token API"}
            ]
        },
        "title": "Giọng Đọc AI Miễn Phí (Edge-TTS) Đối Đầu Giọng Đọc Trả Phí Studio",
        "cta_kw": "VOICETEST",
        "caption": "🔊 BÍ MẬT GIỌNG ĐỌC AI TRIỆU VIEW HOÀN TOÀN MIỄN PHÍ BẰNG EDGE-TTS!\n\nNhiều bạn nghĩ giọng đọc AI nghe 'rô-bốt' vì chưa biết cách tinh chỉnh tốc độ (speed) và pitch chuẩn xác. Chỉ cần tăng speed lên 1.12x và hạ nhẹ volume -3dB, giọng đọc Nam Minh của Edge-TTS sẽ nghe cuốn hút chẳng kém MC chuyên nghiệp.\n\n👇 Bình luận 'VOICETEST' để nhận script Python tạo file âm thanh tự động chỉ bằng 1 lệnh!",
        "comment": "👉 Nhận script Python Edge-TTS 0-đồng: Bình luận 'VOICETEST' để lấy mã nguồn và hướng dẫn cài đặt."
    },
    {
        "day": 3, "date": "2026-10-28", "slot": "13:30", "code": "day3_img3_1330_zalohub",
        "template": 3,
        "params": {
            "level_badge": "Phễu Chuyển Đổi",
            "bracket_title_colored": '[ <span style="color:#CCFF00">FUNNEL</span> <span style="color:#FF2A6D">3 TẦNG</span> ]',
            "meta_info_left": "Tự động hóa qua",
            "meta_info_right": "Khách Hàng Tự Động | Tỷ Lệ Đóng 18%",
            "cards_2x2": [
                {"icon": "key", "title": "Tầng 1: Pinned Cmt", "subtitle": "Bình luận ghim chứa link"},
                {"icon": "book", "title": "Tầng 2: Auto-DM", "subtitle": "Gửi quà tặng qua tin nhắn"},
                {"icon": "flow", "title": "Tầng 3: Community", "subtitle": "Dẫn vào nhóm Zalo / Discord"},
                {"icon": "num", "num_or_icon": "3", "title": "Tỷ lệ chuyển đổi", "subtitle": "Tăng gấp 4 lần kênh thường"}
            ],
            "footer_title_white": "KIẾN TRÚC PHỄU TỰ ĐỘNG",
            "footer_title_pink": "TỪ BÌNH LUẬN RA ĐƠN HÀNG"
        },
        "title": "Kiến Trúc Phễu 3 Tầng: Bình Luận FB -> Auto-DM -> Nhóm Zalo Bảo Mật",
        "cta_kw": "ZALOHUB",
        "caption": "🚀 CÁCH XÂY DỰNG PHỄU DẪN KHÁCH TỰ ĐỘNG TỪ BÀI VIẾT VÀO NHÓM CỘNG ĐỒNG!\n\nĐừng để người xem đọc xong bài viết rồi lướt đi mất. Kiến trúc phễu 3 tầng này giúp bạn giữ chân khán giả và chuyển hóa họ thành thành viên trung thành:\n- Tầng 1: Pinned Comment kêu gọi nhận quà độc quyền.\n- Tầng 2: Auto-DM phản hồi trong 30 giây gửi link Drive.\n- Tầng 3: Nhóm hỗ trợ kín trao đổi chuyên sâu.\n\n👇 Comment 'ZALOHUB' để nhận bản vẽ chi tiết cách thiết lập với n8n!",
        "comment": "👉 Tham gia nhóm thảo luận chuyên sâu về AI & Tự động hóa: Nhắn 'ZALOHUB' để nhận link tham gia kín."
    },
    {
        "day": 3, "date": "2026-10-28", "slot": "15:15", "code": "day3_img4_1515_hook3s",
        "template": 4,
        "params": {
            "header_badge": "Bí kíp giữ chân",
            "bracket_title_colored": '[ <span style="color:#CCFF00">HOOK</span> <span style="color:#FF2A6D">3 GIÂY ĐẦU</span> ]',
            "selector_badge": "30 Công Thức Mở Đầu Video Triệu View",
            "date_cards": [
                {"label": "Thời lượng", "date": "00 - 03 Giây", "highlight": False},
                {"label": "Kho mẫu", "date": "30 Hook", "highlight": True},
                {"label": "Retention", "date": "Đạt 65%+", "highlight": True}
            ],
            "time_badge": "Mở cổng nhận quà: Hôm nay - Hết tuần",
            "delivery_text": "Gửi link tải trực tiếp qua",
            "cta_button_text": "TẢI SỔ TAY"
        },
        "title": "Sổ Tay 30 Hook 3 Giây Đầu Giữ Chân Khán Giả Xem Video Ngắn Đạt 60%+",
        "cta_kw": "HOOK3S",
        "caption": "⏱️ 80% NGƯỜI XEM SẼ LƯỚT QUA NẾU 3 GIÂY ĐẦU KHÔNG ĐỦ HẤP DẪN!\n\nCấm kỵ lớn nhất khi làm video ngắn là mở đầu bằng lời chào hỏi rườm rà. Bạn phải đánh thẳng vào nỗi đau hoặc đưa ra một nghịch lý khiến người xem không thể rời mắt.\n\nSổ tay 30 Hook 3s này đã được kiểm chứng qua hàng trăm video đạt triệu view.\n\n👇 Comment 'HOOK3S' để nhận trọn bộ sổ tay ngay bây giờ!",
        "comment": "👉 Tải ngay Sổ tay 30 Hook 3 Giây Đột Phá: Bình luận 'HOOK3S' để nhận file PDF qua inbox."
    },
    {
        "day": 3, "date": "2026-10-28", "slot": "18:15", "code": "day3_img5_1815_mcpserver",
        "template": 1,
        "params": {
            "top_badge": "Giao thức kết nối",
            "tool_title_line1": "MODEL",
            "tool_title_line2": "CONTEXT",
            "bottom_badge": "Kiến trúc giao tiếp",
            "model_name": "MCP PROTOCOL"
        },
        "title": "Kho Vũ Khí MCP: Top 5 MCP Servers Không Thể Thiếu Cho Dân Tự Động Hóa",
        "cta_kw": "MCPSERVER",
        "caption": "🔌 MODEL CONTEXT PROTOCOL (MCP): CÂY CẦU NỐI AI VỚI MỌI PHẦN MỀM THỰC TẾ!\n\nAI sẽ mãi chỉ là chatbot nói suông nếu không thể đọc file, truy vấn cơ sở dữ liệu hay điều khiển trình duyệt. MCP do Anthropic khởi xướng đã giải quyết triệt để vấn đề này.\n\n5 MCP Server cốt lõi bạn nên cài ngay hôm nay: Filesystem, SQLite, Fetch, Browser, và Facebook API.\n\n👇 Comment 'MCPSERVER' để nhận hướng dẫn cấu hình chi tiết cho Claude Desktop và Antigravity!",
        "comment": "👉 Tìm hiểu thêm về MCP và danh sách server thông dụng: https://modelcontextprotocol.io (Comment 'MCPSERVER' để lấy config mẫu)"
    },
    {
        "day": 3, "date": "2026-10-28", "slot": "21:15", "code": "day3_img6_2115_rubric10",
        "template": 2,
        "params": {
            "left_badge": "Kiểm duyệt chất lượng",
            "right_badge": "4 tiêu chí",
            "items": [
                {"num": "01", "title": "HOOK 3S KHÔNG CHÀO HỎI", "desc": "Mở đầu trực diện bằng vấn đề gây tò mò, tuyệt đối không chào hỏi lãng phí thời gian.", "pink_kw": "tuyệt đối không chào hỏi"},
                {"num": "02", "title": "TỐC ĐỘ TỪ NGỮ CHUẨN XÁC", "desc": "Giới hạn tối đa 85 từ cho video 30 giây để voice đọc rõ ràng không bị nuốt chữ.", "pink_kw": "tối đa 85 từ cho 30 giây"},
                {"num": "03", "title": "BỐ CỤC VISUAL & AN TOÀN", "desc": "Toàn bộ chữ và thành phần tương tác nằm gọn trong vùng an toàn Safe Zone 9:16.", "pink_kw": "Safe Zone 9:16"},
                {"num": "04", "title": "LỜI KÊU GỌI HÀNH ĐỘNG DUY NHẤT", "desc": "Chỉ đưa ra đúng 1 Call-to-Action duy nhất ở 3 giây cuối cùng của video.", "pink_kw": "đúng 1 Call-to-Action duy nhất"}
            ]
        },
        "title": "Bảng Chấm Điểm 10 Tiêu Chí Nghiệm Thu Kịch Bản Trước Khi Render",
        "cta_kw": "RUBRIC10",
        "caption": "📋 RUBRIC 10 TIÊU CHÍ: BỘ LỌC CHẤT LƯỢNG KỊCH BẢN ĐẠT ĐIỂM 9+/10!\n\nTrước khi bấm nút render video, mọi kịch bản của team mình đều phải đi qua bảng kiểm định 10 tiêu chí khắt khe để đảm bảo tỷ lệ chuyển đổi cao nhất.\n\nÁp dụng bộ tiêu chí này, bạn sẽ loại bỏ được 95% những kịch bản nhạt nhẽo và lãng phí thời gian dựng phim.\n\n👇 Comment 'RUBRIC10' để nhận bảng checklist dạng Google Sheet dùng được cho cả team!",
        "comment": "👉 Nhận bảng Rubric 10 tiêu chí kiểm duyệt kịch bản video: Bình luận 'RUBRIC10' để tải sheet mẫu."
    },

    # -------------------------------------------------------------------------
    # NGÀY 4: Thứ Năm 29/10
    # -------------------------------------------------------------------------
    {
        "day": 4, "date": "2026-10-29", "slot": "08:30", "code": "day4_img1_0830_cursor",
        "template": 1,
        "params": {
            "top_badge": "Lập trình thế hệ mới",
            "tool_title_line1": "CURSOR",
            "tool_title_line2": "WINDSURF",
            "bottom_badge": "Agentic Coding",
            "model_name": "CLAUDE 3.7"
        },
        "title": "Cursor & Windsurf: Kỷ Nguyên Lập Trình Với AI Agent Tự Sửa Đa File",
        "cta_kw": "CURSOR",
        "caption": "💻 TẠI SAO CÁC LẬP TRÌNH VIÊN ĐỀU ĐANG CHUYỂN SANG CURSOR VÀ WINDSURF?\n\nKhông chỉ là tính năng autocomplete đơn giản, các AI Code Editor thế hệ mới có thể đọc hiểu toàn bộ codebase hàng chục nghìn dòng code và tự động sửa lỗi đồng thời trên nhiều file chỉ với 1 phím tắt.\n\n👇 Comment 'CURSOR' để nhận bộ .cursorrules tối ưu chuẩn nhất cho dự án TypeScript & Python!",
        "comment": "👉 Tải bộ quy tắc .cursorrules mẫu cho dự án: Bình luận 'CURSOR' để nhận link GitHub."
    },
    {
        "day": 4, "date": "2026-10-29", "slot": "10:15", "code": "day4_img2_1015_flashtest",
        "template": 2,
        "params": {
            "left_badge": "Tối ưu chi phí AI",
            "right_badge": "4 nguyên tắc",
            "items": [
                {"num": "01", "title": "PHÂN TẦNG NHIỆM VỤ RÕ RÀNG", "desc": "Việc khó (lập luận, lên dàn ý) dùng Claude 3.5; việc lặp lại dùng Gemini Flash.", "pink_kw": "việc lặp lại dùng Gemini Flash"},
                {"num": "02", "title": "TIẾT KIỆM 90% CHI PHÍ API", "desc": "Gemini 1.5/2.0 Flash có giá siêu rẻ, phù hợp cho việc tóm tắt và bóc tách dữ liệu.", "pink_kw": "Tiết kiệm 90% chi phí"},
                {"num": "03", "title": "TỐC ĐỘ PHẢN HỒI DƯỚI 500MS", "desc": "Mô hình Flash xử lý gần như tức thì, lý tưởng cho chatbot chăm sóc khách hàng live.", "pink_kw": "dưới 500ms"},
                {"num": "04", "title": "KÍCH HOẠT HỆ THỐNG DỰ PHÒNG", "desc": "Tự động chuyển đổi giữa các nhà cung cấp nếu một bên gặp sự cố nghẽn mạng.", "pink_kw": "Hệ thống dự phòng"}
            ]
        },
        "title": "Mô Hình AI Đắt Tiền vs Mô Hình Rẻ: Đoạn Nào Nên Dùng Gemini Flash?",
        "cta_kw": "FLASHTEST",
        "caption": "💰 ĐỪNG DÙNG DAO MỔ TRÂU ĐỂ GIẾT GÀ: BÍ QUYẾT PHÂN TẦNG MODEL TIẾT KIỆM 90% CHI PHÍ!\n\nNhiều người có thói quen dùng model đắt tiền nhất (như GPT-4o hay Claude Opus) cho tất cả mọi việc, kể cả việc phân loại bình luận hay sửa lỗi chính tả.\n\nBiết cách phân tầng model sẽ giúp bạn cắt giảm 90% hóa đơn API mà chất lượng đầu ra vẫn hoàn hảo.\n\n👇 Comment 'FLASHTEST' để nhận bảng so sánh giá và hiệu năng của 10 model phổ biến nhất!",
        "comment": "👉 Bảng tra cứu giá token & benchmark chi tiết: Comment 'FLASHTEST' để nhận file tổng hợp."
    },
    {
        "day": 4, "date": "2026-10-29", "slot": "13:30", "code": "day4_img3_1330_sqliteai",
        "template": 3,
        "params": {
            "level_badge": "Bộ Nhớ Bền Vững",
            "bracket_title_colored": '[ <span style="color:#CCFF00">SQLITE</span> <span style="color:#FF2A6D">MEMORY</span> ]',
            "meta_info_left": "Lưu trữ dữ liệu qua",
            "meta_info_right": "100% Local File | Tốc Độ Mili-giây",
            "cards_2x2": [
                {"icon": "key", "title": "Trạng thái việc", "subtitle": "Lưu tiến độ từng Subagent"},
                {"icon": "book", "title": "Lịch sử đăng bài", "subtitle": "Chống trùng lặp nội dung"},
                {"icon": "flow", "title": "Danh mục sản phẩm", "subtitle": "Quản lý SKU & affiliate link"},
                {"icon": "num", "num_or_icon": "0", "title": "Chi phí duy trì", "subtitle": "0đ máy chủ điện toán mây"}
            ],
            "footer_title_white": "BỘ NHỚ BỀN VỮNG SQLITE",
            "footer_title_pink": "CHO ĐỘI NGŨ AI TỰ HÀNH"
        },
        "title": "Sơ Đồ Kết Nối SQLite Local Với AI Để Lưu Nhớ Bối Cảnh Vĩnh Viễn",
        "cta_kw": "SQLITEAI",
        "caption": "🗄️ LÀM THẾ NÀO ĐỂ AI KHÔNG BỊ 'MẤT TRÍ NHỚ' SAU MỖI LẦN BẬT TẮT PHIÊN LÀM VIỆC?\n\nContext window của AI có giới hạn và tốn kém nếu phải nhồi nhét lại từ đầu. Giải pháp tối ưu nhất là sử dụng một cơ sở dữ liệu SQLite local siêu nhẹ làm 'bộ nhớ ngoài'.\n\nMọi quyết định, trạng thái nhiệm vụ và lịch sử đăng bài đều được lưu bền vững vào 1 file database duy nhất.\n\n👇 Bình luận 'SQLITEAI' để nhận file schema database mẫu cho dự án của bạn!",
        "comment": "👉 File schema SQLite mẫu tối ưu cho AI Agent: Nhắn 'SQLITEAI' để nhận script khởi tạo database 0đ."
    },
    {
        "day": 4, "date": "2026-10-29", "slot": "15:15", "code": "day4_img4_1515_mamaprompt",
        "template": 4,
        "params": {
            "header_badge": "Tổng quản điều phối",
            "bracket_title_colored": '[ <span style="color:#CCFF00">MAMA</span> <span style="color:#FF2A6D">CHIEF</span> ]',
            "selector_badge": "System Prompt Trợ Lý Điều Phối Dự Án",
            "date_cards": [
                {"label": "Vai trò", "date": "Chief of Staff", "highlight": False},
                {"label": "Đội ngũ", "date": "10 Subagent", "highlight": True},
                {"label": "Cơ chế", "date": "Zero-Waste", "highlight": True}
            ],
            "time_badge": "Mở cổng nhận quà: Hôm nay - Hết tuần",
            "delivery_text": "Gửi file Markdown gốc qua",
            "cta_button_text": "NHẬN TEMPLATE"
        },
        "title": "Tặng Bộ Template System Prompt Cho Trợ Lý Chief of Staff Điều Phối",
        "cta_kw": "MAMAPROMPT",
        "caption": "👑 BỘ SYSTEM PROMPT ĐIỀU PHỐI ĐỘI AGENT (CHIEF OF STAFF - MAMA)!\n\nĐể điều hành một đội ngũ gồm nhiều AI chuyên gia, bạn cần một 'Tổng quản' có khả năng phân chia nhiệm vụ, kiểm soát cổng bàn giao (Hard Gates) và báo cáo ngắn gọn cho CEO.\n\nĐây là file system prompt thực tế đang được vận hành trơn tru trong hệ thống Agent-Javis.\n\n👇 Comment 'MAMAPROMPT' để tải file Markdown gốc về áp dụng ngay cho dự án của bạn!",
        "comment": "👉 Tải trọn bộ System Prompt Chief of Staff: Bình luận 'MAMAPROMPT' để nhận link Drive trực tiếp."
    },
    {
        "day": 4, "date": "2026-10-29", "slot": "18:15", "code": "day4_img5_1815_antihallu",
        "template": 1,
        "params": {
            "top_badge": "Bảo vệ độ chính xác",
            "tool_title_line1": "ANTI",
            "tool_title_line2": "HALLUCINATION",
            "bottom_badge": "Cơ chế 3 lớp khóa",
            "model_name": "GROUNDED AI"
        },
        "title": "Giải Phẫu Cơ Chế Anti-Hallucination: 3 Lớp Khóa Chặt Dữ Liệu Bịa Đặt",
        "cta_kw": "ANTIHALLU",
        "caption": "🛡️ 3 LỚP KHÓA CHẶT TÌNH TRẠNG AI BỊA ĐẶT THÔNG TIN (HALLUCINATION)!\n\nNỗi sợ lớn nhất khi ứng dụng AI vào công việc là tình trạng AI trả lời tự tin nhưng hoàn toàn sai sự thật.\n\nCơ chế 3 lớp khóa của chúng mình:\n1. Khóa tài liệu nguồn (Grounding strictly to Knowledge Base).\n2. Ép xuất JSON Schema định dạng chuẩn.\n3. Agent Linter độc lập kiểm tra đối chiếu trước khi publish.\n\n👇 Comment 'ANTIHALLU' để nhận tài liệu hướng dẫn cài đặt cơ chế kiểm duyệt tự động!",
        "comment": "👉 Hướng dẫn khóa chặt AI Hallucination: Bình luận 'ANTIHALLU' để nhận bài viết kỹ thuật chi tiết."
    },
    {
        "day": 4, "date": "2026-10-29", "slot": "21:15", "code": "day4_img6_2115_raocan",
        "template": 2,
        "params": {
            "left_badge": "Khảo sát cộng đồng",
            "right_badge": "4 rào cản",
            "items": [
                {"num": "01", "title": "KHÔNG BIẾT VIẾT CODE", "desc": "Nghĩ rằng phải là lập trình viên thâm niên mới xây dựng được hệ thống AI tự hành.", "pink_kw": "Nghĩ rằng phải là lập trình viên"},
                {"num": "02", "title": "CHI PHÍ PHẦN CỨNG & TOKEN", "desc": "Lo ngại chi phí duy trì hàng tháng quá cao vượt quá ngân sách ban đầu.", "pink_kw": "Lo ngại chi phí duy trì"},
                {"num": "03", "title": "QUÁ NHIỀU TOOL KHÔNG BIẾT CHỌN", "desc": "Bị ngợp giữa hàng trăm công cụ mới ra mắt mỗi ngày mà không có lộ trình rõ ràng.", "pink_kw": "Bị ngợp giữa hàng trăm công cụ"},
                {"num": "04", "title": "KHÔNG ĐỦ THỜI GIAN SETUP", "desc": "Bận rộn với công việc hiện tại nên chưa thể dành thời gian tối ưu quy trình.", "pink_kw": "chưa thể dành thời gian"}
            ]
        },
        "title": "Khảo Sát: Rào Cản Lớn Nhất Của Bạn Khi Tự Động Hóa Bằng AI Là Gì?",
        "cta_kw": "RAOCAN",
        "caption": "🤔 RÀO CẢN LỚN NHẤT KHIẾN BẠN CHƯA THỂ TỰ ĐỘNG HÓA CÔNG VIỆC BẰNG AI LÀ GÌ?\n\n1. Chưa biết viết code\n2. Lo ngại chi phí phần cứng và token\n3. Quá nhiều tool mới ra mắt mỗi ngày không biết chọn ai\n4. Không có thời gian để tìm hiểu và setup\n\n👇 Hãy để lại con số 1, 2, 3 hoặc 4 bên dưới nhé. Mình sẽ làm video giải quyết cụ thể vấn đề được quan tâm nhiều nhất!",
        "comment": "👉 Bình luận con số 1, 2, 3 hoặc 4 bên dưới để nhận tài liệu giải pháp tương ứng nhé!"
    },

    # -------------------------------------------------------------------------
    # NGÀY 5: Thứ Sáu 30/10
    # -------------------------------------------------------------------------
    {
        "day": 5, "date": "2026-10-30", "slot": "08:30", "code": "day5_img1_0830_compuse",
        "template": 1,
        "params": {
            "top_badge": "Công nghệ đột phá",
            "tool_title_line1": "COMPUTER",
            "tool_title_line2": "USE",
            "bottom_badge": "Tự động hóa GUI",
            "model_name": "CLAUDE 3.5 SONNET"
        },
        "title": "Anthropic Computer Use: Khi AI Tự Di Chuột & Gõ Phím Thay Bạn",
        "cta_kw": "COMPUSE",
        "caption": "🖱️ KHI AI BIẾT CẦM CHUỘT VÀ GÕ PHÍM NHƯ MỘT NHÂN VIÊN THỰC THỤ!\n\nTính năng Computer Use của Anthropic đánh dấu bước chuyển mình lớn: AI không chỉ xử lý văn bản mà còn có thể nhìn màn hình, di chuyển con trỏ chuột, click vào nút bấm và điền dữ liệu trên bất kỳ ứng dụng nào.\n\n👇 Comment 'COMPUSE' để nhận video demo thực tế và hướng dẫn chạy thử nghiệm an toàn trong Docker!",
        "comment": "👉 Tìm hiểu công nghệ Anthropic Computer Use: https://docs.anthropic.com (Bình luận 'COMPUSE' để lấy script mẫu)"
    },
    {
        "day": 5, "date": "2026-10-30", "slot": "10:15", "code": "day5_img2_1015_codevsno",
        "template": 2,
        "params": {
            "left_badge": "Lựa chọn công nghệ",
            "right_badge": "4 tiêu chuẩn",
            "items": [
                {"num": "01", "title": "ĐỘ LINH HOẠT VÀ TÙY BIẾN", "desc": "Code thuần cho phép can thiệp 100% vào logic xử lý mà không bị giới hạn tính năng.", "pink_kw": "can thiệp 100% vào logic"},
                {"num": "02", "title": "TỐC ĐỘ TRIỂN KHAI BAN ĐẦU", "desc": "Nền tảng No-code (n8n, Make) giúp dựng luồng tự động hóa chạy được trong 15 phút.", "pink_kw": "chạy được trong 15 phút"},
                {"num": "03", "title": "KHẢ NĂNG BẢO TRÌ DÀI HẠN", "desc": "Hệ thống code được quản lý bằng Git giúp theo dõi lịch sử và phối hợp mượt mà.", "pink_kw": "quản lý bằng Git"},
                {"num": "04", "title": "MÔ HÌNH LAI HYBRID TỐI ƯU", "desc": "Dùng No-code cho giao tiếp bên ngoài và Code thuần cho xử lý nghiệp vụ nặng.", "pink_kw": "Mô hình lai Hybrid"}
            ]
        },
        "title": "Tự Động Hóa Bằng Code Thuần vs Dùng Nền Tảng No-Code: Chọn Đường Nào?",
        "cta_kw": "CODEVSNO",
        "caption": "⚖️ NÊN VIẾT CODE THUẦN HAY DÙNG NỀN TẢNG NO-CODE ĐỂ TỰ ĐỘNG HÓA?\n\nKhông có công cụ nào hoàn hảo cho mọi bài toán. Lời khuyên tốt nhất năm 2026 là mô hình Hybrid:\n- Dùng No-code (như n8n) để hứng webhook và kết nối các ứng dụng nhanh chóng.\n- Dùng Code thuần (Python/TypeScript) để xử lý logic phức tạp, render đồ họa và bảo mật dữ liệu.\n\n👇 Comment 'CODEVSNO' để nhận case study thực tế kết hợp cả hai mô hình!",
        "comment": "👉 Đọc phân tích chi tiết mô hình Hybrid: Bình luận 'CODEVSNO' để nhận bài viết hướng dẫn."
    },
    {
        "day": 5, "date": "2026-10-30", "slot": "13:30", "code": "day5_img3_1330_syncsys",
        "template": 3,
        "params": {
            "level_badge": "Đồng Bộ 2 Chiều",
            "bracket_title_colored": '[ <span style="color:#CCFF00">SYNC</span> <span style="color:#FF2A6D">LIGHT</span> ]',
            "meta_info_left": "Đồng bộ qua",
            "meta_info_right": "Git Repo Siêu Nhẹ | 0-Conflict",
            "cards_2x2": [
                {"icon": "key", "title": "Work History", "subtitle": "Nhật ký việc & bàn giao"},
                {"icon": "book", "title": "Changelog", "subtitle": "Lịch sử cập nhật công cụ"},
                {"icon": "flow", "title": "Blueprint", "subtitle": "Bản vẽ tổng thể dự án"},
                {"icon": "num", "num_or_icon": "0", "title": "File rác", "subtitle": "Chặn mp4 & node_modules"}
            ],
            "footer_title_white": "ĐỒNG BỘ HAI CHIỀU SIÊU NHẸ",
            "footer_title_pink": "GIỮA MÁY NHÀ VÀ VĂN PHÒNG"
        },
        "title": "Bản Vẽ Hệ Thống Đồng Bộ Hai Chiều Giữa Máy Ở Nhà Và Máy Văn Phòng",
        "cta_kw": "SYNCSYS",
        "caption": "🔄 LÀM SAO ĐỂ TIẾP TỤC DỰ ÁN TRÊN MÁY TÍNH KHÁC MÀ KHÔNG BỊ LỆCH TIẾN ĐỘ?\n\nGiải pháp là tách riêng phần 'não bộ và trạng thái' (Agent-State-Sync) ra khỏi phần tài nguyên nặng (video, database thô).\n\nMỗi khi kết thúc ca làm việc, hệ thống tự động ghi nhật ký và đẩy lên GitHub. Sang máy khác chỉ cần kéo về là làm tiếp trơn tru.\n\n👇 Comment 'SYNCSYS' để nhận script PowerShell tự động đồng bộ 1-click!",
        "comment": "👉 Nhận script đồng bộ tự động 1-click cho Windows: Bình luận 'SYNCSYS' để lấy code mẫu."
    },
    {
        "day": 5, "date": "2026-10-30", "slot": "15:15", "code": "day5_img4_1515_jsonprompt",
        "template": 4,
        "params": {
            "header_badge": "Cấu trúc dữ liệu",
            "bracket_title_colored": '[ <span style="color:#CCFF00">JSON</span> <span style="color:#FF2A6D">SCHEMA</span> ]',
            "selector_badge": "15 Template Ép Định Dạng AI 100%",
            "date_cards": [
                {"label": "Định dạng", "date": "JSON Chuẩn", "highlight": False},
                {"label": "Kho mẫu", "date": "15 Schema", "highlight": True},
                {"label": "Độ chính xác", "date": "100% Clean", "highlight": True}
            ],
            "time_badge": "Mở cổng nhận quà: Hôm nay - Hết tuần",
            "delivery_text": "Gửi kho mẫu trực tiếp qua",
            "cta_button_text": "TẢI SCHEMA"
        },
        "title": "Sổ Tay 15 Cấu Trúc JSON Schema Ép AI Xuất Đúng Định Dạng 100%",
        "cta_kw": "JSONPROMPT",
        "caption": "📋 CÁCH BẮT BUỘC AI PHẢI XUẤT RA DỮ LIỆU ĐÚNG ĐỊNH DẠNG JSON 100%!\n\nAI thường có tật xấu là tự động thêm lời dẫn kiểu 'Dưới đây là kết quả của bạn' làm gãy các luồng tự động hóa bằng code.\n\nSử dụng kỹ thuật JSON Schema Definition kết hợp System Instruction, bạn sẽ ép AI trả lời thuần JSON chuẩn xác không lẫn 1 ký tự rác.\n\n👇 Comment 'JSONPROMPT' để nhận trọn bộ 15 schema thông dụng nhất!",
        "comment": "👉 Tải bộ 15 template JSON Schema chuẩn cho AI: Bình luận 'JSONPROMPT' để nhận file tải về."
    },
    {
        "day": 5, "date": "2026-10-30", "slot": "18:15", "code": "day5_img5_1815_bonaothu2",
        "template": 1,
        "params": {
            "top_badge": "Quản trị tri thức",
            "tool_title_line1": "SECOND",
            "tool_title_line2": "BRAIN",
            "bottom_badge": "Cơ sở tri thức",
            "model_name": "MARKDOWN VAULT"
        },
        "title": "Kho Lưu Trữ Bài Học: Cách Xây Dựng Bộ Não Thứ 2 Cho Đội Ngũ AI",
        "cta_kw": "BONAOTHU2",
        "caption": "🧠 XÂY DỰNG 'BỘ NÃO THỨ 2' ĐỂ ĐỘI NGŨ AI CÀNG LÀM VIỆC CÀNG THÔNG MINH!\n\nSau mỗi chiến dịch hay mỗi lần mắc lỗi, hệ thống sẽ tự động rút ra bài học kinh nghiệm và lưu vào thư mục `knowledge/memories/`.\n\nNhờ vậy, các Subagent ở các phiên làm việc sau sẽ tự động đọc lại bài học cũ và không bao giờ lặp lại cùng một sai lầm.\n\n👇 Comment 'BONAOTHU2' để nhận cấu trúc thư mục và quy chuẩn ghi nhớ cho AI!",
        "comment": "👉 Khám phá phương pháp xây dựng Second Brain cho Agent: Comment 'BONAOTHU2' để nhận hướng dẫn."
    },
    {
        "day": 5, "date": "2026-10-30", "slot": "21:15", "code": "day5_img6_2115_4chiso",
        "template": 2,
        "params": {
            "left_badge": "Đo lường hiệu suất",
            "right_badge": "4 chỉ số",
            "items": [
                {"num": "01", "title": "RETENTION RATE 3S ĐẦU", "desc": "Tỷ lệ người xem ở lại sau 3 giây đầu tiên phải đạt tối thiểu 60% trở lên.", "pink_kw": "tối thiểu 60% trở lên"},
                {"num": "02", "title": "CLICK-THROUGH RATE (CTR)", "desc": "Tỷ lệ bấm vào link trong bình luận ghim đạt chuẩn 8% - 15% tổng lượt xem.", "pink_kw": "8% - 15% tổng lượt xem"},
                {"num": "03", "title": "TỶ LỆ CHUYỂN ĐỔI PHỄU LEAD", "desc": "Số người nhắn tin từ khóa nhận quà chuyển thành thành viên cộng đồng.", "pink_kw": "chuyển thành thành viên"},
                {"num": "04", "title": "CHI PHÍ TRÊN MỖI ĐƠN HÀNG (CPO)", "desc": "Đảm bảo lợi nhuận ròng hoa hồng luôn cao hơn tổng chi phí token và điện toán.", "pink_kw": "luôn cao hơn tổng chi phí"}
            ]
        },
        "title": "4 Chỉ Số Sống Còn Cần Đo Lường Khi Vận Hành Kênh Tự Động 2026",
        "cta_kw": "4CHISO",
        "caption": "📈 ĐỪNG CHỈ NHÌN VÀO LƯỢT VIEW: 4 CHỈ SỐ THỰC TẾ QUYẾT ĐỊNH DOANH SỐ CỦA BẠN!\n\nVideo triệu view nhưng không có người bấm link hay không ra đơn hàng thì cũng vô nghĩa. Một hệ thống vận hành tự động chuyên nghiệp cần theo dõi sát sao 4 chỉ số trên ảnh.\n\n👇 Comment '4CHISO' để nhận template Google Sheet theo dõi phễu chuyển đổi tự động cập nhật mỗi ngày!",
        "comment": "👉 Nhận sheet đo lường phễu chuyển đổi video ngắn: Bình luận '4CHISO' để lấy mẫu theo dõi."
    },

    # -------------------------------------------------------------------------
    # NGÀY 6: Thứ Bảy 31/10
    # -------------------------------------------------------------------------
    {
        "day": 6, "date": "2026-10-31", "slot": "08:30", "code": "day6_img1_0830_fasthtml",
        "template": 1,
        "params": {
            "top_badge": "Phát triển web siêu tốc",
            "tool_title_line1": "FAST",
            "tool_title_line2": "HTML",
            "bottom_badge": "Pure Python Web",
            "model_name": "PYTHON 3.12"
        },
        "title": "FastHTML: Xây Giao Diện Web Đẹp Cho Ứng Dụng AI Bằng 100% Python",
        "cta_kw": "FASTHTML",
        "caption": "🚀 FASTHTML: XÂY DỰNG WEB APP CHO AI BẰNG 100% PYTHON THUẦN!\n\nBạn là dân Data/AI ngại học JavaScript hay React phức tạp? FastHTML ra đời giúp bạn viết toàn bộ giao diện, backend và xử lý logic chỉ bằng một file Python duy nhất, tốc độ cực nhanh và hỗ trợ HTMX mượt mà.\n\n👇 Comment 'FASTHTML' để nhận repo mẫu tạo giao diện Chatbot AI trong 50 dòng code!",
        "comment": "👉 Khám phá framework FastHTML mới nhất: https://fastht.ml (Comment 'FASTHTML' để nhận template tiếng Việt)"
    },
    {
        "day": 6, "date": "2026-10-31", "slot": "10:15", "code": "day6_img2_1015_roiai",
        "template": 2,
        "params": {
            "left_badge": "Bài toán kinh tế",
            "right_badge": "4 so sánh",
            "items": [
                {"num": "01", "title": "CHI PHÍ LƯƠNG NHÂN SỰ", "desc": "1 phòng marketing truyền thống tốn 30 - 60 triệu/tháng; AI Agent chỉ tốn tiền điện.", "pink_kw": "tốn 30 - 60 triệu/tháng"},
                {"num": "02", "title": "THỜI GIAN LÀM VIỆC LIÊN TỤC", "desc": "Subagent vận hành bền bỉ 24/7 không cần nghỉ phép hay lo lắng biến động nhân sự.", "pink_kw": "bền bỉ 24/7 không cần nghỉ"},
                {"num": "03", "title": "TỐC ĐỘ XUẤT BẢN NỘI DUNG", "desc": "Sản xuất đồng thời 42 bài viết và 21 video ngắn mỗi tuần một cách chuẩn xác.", "pink_kw": "42 bài viết và 21 video"},
                {"num": "04", "title": "KHẢ NĂNG NHÂN BẢN QUY MÔ", "desc": "Mở rộng từ 1 kênh lên 10 kênh chỉ bằng cách nhân bản file cấu hình trong 5 phút.", "pink_kw": "nhân bản trong 5 phút"}
            ]
        },
        "title": "Chi Phí Nhân Sự Truyền Thống vs Vận Hành Bằng Đội 10 Subagent",
        "cta_kw": "ROIAI",
        "caption": "📊 BÀI TOÁN KINH TẾ: TẠI SAO TỰ ĐỘNG HÓA BẰNG SUBAGENT LẠI CÓ ROI VƯỢT TRỘI?\n\nKhông phải để thay thế con người hoàn toàn, mà để giải phóng bạn khỏi những việc lặp đi lặp lại vô nghĩa. 1 người điều phối giỏi kết hợp với 10 Subagent chuyên môn hóa có thể tạo ra sản lượng tương đương cả một phòng ban.\n\n👇 Comment 'ROIAI' để nhận bảng tính chi phí và lộ trình triển khai chi tiết!",
        "comment": "👉 Tải bảng tính ROI & chi phí triển khai AI Agent: Bình luận 'ROIAI' để nhận file Excel mẫu."
    },
    {
        "day": 6, "date": "2026-10-31", "slot": "13:30", "code": "day6_img3_1330_cleanup7d",
        "template": 3,
        "params": {
            "level_badge": "Bảo Trì Tự Động",
            "bracket_title_colored": '[ <span style="color:#CCFF00">CLEANUP</span> <span style="color:#FF2A6D">7 DAYS</span> ]',
            "meta_info_left": "Chạy tự động qua",
            "meta_info_right": "0-Token Chi Phí | Giải Phóng 50GB",
            "cards_2x2": [
                {"icon": "key", "title": "Dọn video thô", "subtitle": "Xóa clip thừa sau khi render"},
                {"icon": "book", "title": "Nén log chat", "subtitle": "Lưu trữ dạng tóm tắt gọn gàng"},
                {"icon": "flow", "title": "Dọn cache Chrome", "subtitle": "Giữ trình duyệt luôn chạy mượt"},
                {"icon": "num", "num_or_icon": "7", "title": "Chu kỳ cố định", "subtitle": "Tự động kích hoạt hàng tuần"}
            ],
            "footer_title_white": "QUY TRÌNH DỌN DẸP TỰ HÀNH",
            "footer_title_pink": "DUY TRÌ MÁY MÓC LUÔN NHẸ"
        },
        "title": "Quy Trình Tự Động Dọn Dẹp Kho Dữ Liệu Rác Định Kỳ 7 Ngày 0-Token",
        "cta_kw": "CLEANUP7D",
        "caption": "🧹 CÁCH GIỮ HỆ THỐNG LUÔN CHẠY NHANH NHƯ MỚI VỚI SCRIPT DỌN DẸP 7 NGÀY!\n\nLàm video và chạy AI thường xuyên sẽ sinh ra hàng chục GB file tạm, cache và log thừa khiến máy tính ì ạch. Script tự động dọn dẹp chạy ngầm vào cuối tuần sẽ giúp giải phóng dung lượng đĩa cứng mà không tốn một xu token nào.\n\n👇 Comment 'CLEANUP7D' để nhận file batch dọn dẹp 1-click cho máy tính của bạn!",
        "comment": "👉 Tải script tự động dọn rác hệ thống 0-token: Bình luận 'CLEANUP7D' để nhận mã nguồn."
    },
    {
        "day": 6, "date": "2026-10-31", "slot": "15:15", "code": "day6_img4_1515_promptmkt",
        "template": 4,
        "params": {
            "header_badge": "Nghiên cứu thị trường",
            "bracket_title_colored": '[ <span style="color:#CCFF00">VOICE</span> OF <span style="color:#FF2A6D">CUSTOMER</span> ]',
            "selector_badge": "Bộ Prompt Đào Sâu Nỗi Đau Khách Hàng",
            "date_cards": [
                {"label": "Phân tích", "date": "1,000+ Review", "highlight": False},
                {"label": "Bộ mẫu", "date": "12 Prompt", "highlight": True},
                {"label": "Hiệu quả", "date": "Bắt Trúng Pain", "highlight": True}
            ],
            "time_badge": "Mở cổng nhận quà: Hôm nay - Hết tuần",
            "delivery_text": "Gửi link tài liệu qua",
            "cta_button_text": "TẢI BỘ PROMPT"
        },
        "title": "Tặng Bộ Prompt Săn Sản Phẩm & Phân Tích Đánh Giá Khách Hàng VoC",
        "cta_kw": "PROMPTMKT",
        "caption": "🎯 ĐÀO BỚI HÀNG NGHÌN ĐÁNH GIÁ ĐỂ TÌM Ý TƯỞNG VIDEO BẰNG PROMPT VOC!\n\nMuốn bán được hàng hay làm video viral, bạn phải nói đúng ngôn ngữ của khách hàng. Bộ prompt Voice of Customer (VoC) này giúp bạn bóc tách 1.000 bình luận trên sàn thương mại điện tử chỉ trong vài giây để tìm ra chính xác nỗi đau lớn nhất của họ.\n\n👇 Comment 'PROMPTMKT' để tải ngay bộ prompt phân tích khách hàng độc quyền!",
        "comment": "👉 Nhận bộ prompt VoC phân tích tâm lý khách hàng: Bình luận 'PROMPTMKT' để tải trọn gói."
    },
    {
        "day": 6, "date": "2026-10-31", "slot": "18:15", "code": "day6_img5_1815_top10agents",
        "template": 1,
        "params": {
            "top_badge": "Xu hướng mã nguồn mở",
            "tool_title_line1": "MULTI",
            "tool_title_line2": "AGENTS",
            "bottom_badge": "Hệ sinh thái hàng đầu",
            "model_name": "LANGGRAPH & CREWAI"
        },
        "title": "Top 10 GitHub Trending Repos Về Multi-Agent Đáng Thử Nghiệm Nhất",
        "cta_kw": "TOP10AGENTS",
        "caption": "🔥 TOP 10 REPO GITHUB MULTI-AGENT ĐANG LÀM MƯA LÀM GIÓ NĂM 2026!\n\nTừ AutoGen, CrewAI cho đến LangGraph và MetaGPT, đâu là framework phù hợp nhất với dự án của bạn? Bài viết tổng hợp 10 dự án mã nguồn mở có số sao tăng trưởng nhanh nhất và tính ứng dụng thực tế cao nhất.\n\n👇 Comment 'TOP10AGENTS' để nhận danh sách tổng hợp kèm đường dẫn trực tiếp!",
        "comment": "👉 Xem danh sách Top 10 Multi-Agent Frameworks: Bình luận 'TOP10AGENTS' để nhận file tổng hợp."
    },
    {
        "day": 6, "date": "2026-10-31", "slot": "21:15", "code": "day6_img6_2115_cuoituan",
        "template": 2,
        "params": {
            "left_badge": "Tối ưu cuối tuần",
            "right_badge": "4 thói quen",
            "items": [
                {"num": "01", "title": "ĐỐI SOÁT DỮ LIỆU ĐĂNG BÀI", "desc": "Kiểm tra xem bài viết nào đạt tương tác cao nhất và bài nào cần cải thiện.", "pink_kw": "đạt tương tác cao nhất"},
                {"num": "02", "title": "CẬP NHẬT KHO BÀI HỌC KINH NGHIỆM", "desc": "Ghi nhận lại các lỗi phát sinh trong tuần vào bộ nhớ để không lặp lại.", "pink_kw": "Ghi nhận lại các lỗi"},
                {"num": "03", "title": "LÊN LỊCH NỘI DUNG CHO TUẦN MỚI", "desc": "Chuẩn bị sẵn toàn bộ kho ảnh và video để hệ thống tự chạy từ sáng thứ Hai.", "pink_kw": "Chuẩn bị sẵn toàn bộ kho"},
                {"num": "04", "title": "DÀNH THỜI GIAN NGHỈ NGƠI THẬT SỰ", "desc": "Khi hệ thống đã tự động hóa, bạn hoàn toàn có thể yên tâm tận hưởng cuối tuần.", "pink_kw": "yên tâm tận hưởng cuối tuần"}
            ]
        },
        "title": "Khảo Sát: Cuối Tuần Bạn Dành Mấy Tiếng Để Tối Ưu Lại Quy Trình Làm Việc?",
        "cta_kw": "CUOITUAN",
        "caption": "☕ CUỐI TUẦN NÀY BẠN CÓ ĐANG ĐƯỢC THẢNH THƠI NGHỈ NGƠI KHÔNG?\n\nMục tiêu cao nhất của việc ứng dụng AI và tự động hóa không phải để làm việc nhiều hơn, mà là để bạn có nhiều thời gian tự do hơn cho bản thân và gia đình.\n\nHãy chia sẻ với mình thói quen tối ưu quy trình làm việc cuối tuần của bạn bên dưới nhé!\n\n👇 Comment 'CUOITUAN' để nhận checklist bảo trì hệ thống 15 phút vào chiều Chủ Nhật!",
        "comment": "👉 Nhận checklist bảo trì hệ thống cuối tuần thảnh thơi: Bình luận 'CUOITUAN' để lấy file mẫu."
    },

    # -------------------------------------------------------------------------
    # NGÀY 7: Chủ Nhật 01/11
    # -------------------------------------------------------------------------
    {
        "day": 7, "date": "2026-11-01", "slot": "08:30", "code": "day7_img1_0830_telebot",
        "template": 1,
        "params": {
            "top_badge": "Trạm chỉ huy di động",
            "tool_title_line1": "TELEGRAM",
            "tool_title_line2": "COMMAND",
            "bottom_badge": "Quản lý từ xa",
            "model_name": "BOT API 2026"
        },
        "title": "Trạm Chỉ Huy Telegram Bot: Giao Việc & Nhận Báo Cáo Khi Đang Đi Cà Phê",
        "cta_kw": "TELEBOT",
        "caption": "📱 ĐIỀU HÀNH CẢ HỆ THỐNG TỰ ĐỘNG HÓA CHỈ VỚI CHIẾC ĐIỆN THOẠI TRÊN TAY!\n\nKhông cần lúc nào cũng phải ngồi trước máy tính. Kết nối AI Agent với Telegram Bot, bạn có thể gửi lệnh bằng giọng nói, duyệt bài đăng và nhận báo cáo doanh số mỗi tối ngay trên ứng dụng chat quen thuộc.\n\n👇 Comment 'TELEBOT' để nhận mã nguồn Python kết nối Telegram Bot an toàn bảo mật!",
        "comment": "👉 Hướng dẫn tạo Telegram Bot điều khiển AI Agent: Bình luận 'TELEBOT' để nhận file code mẫu."
    },
    {
        "day": 7, "date": "2026-11-01", "slot": "10:15", "code": "day7_img2_1015_specialist",
        "template": 2,
        "params": {
            "left_badge": "Tư duy thiết kế đội ngũ",
            "right_badge": "4 khác biệt",
            "items": [
                {"num": "01", "title": "TRỢ LÝ BIẾT TUỐT (GENERALIST)", "desc": "Biết mỗi thứ một ít nhưng chuyên môn nông, dễ nhầm lẫn và hay bịa thông tin.", "pink_kw": "chuyên môn nông, dễ nhầm lẫn"},
                {"num": "02", "title": "CHUYÊN GIA TINH GỌN (SPECIALIST)", "desc": "Mỗi Subagent chỉ làm đúng 1 việc xuất sắc với bộ quy tắc riêng không lẫn lộn.", "pink_kw": "chỉ làm đúng 1 việc xuất sắc"},
                {"num": "03", "title": "TIẾT KIỆM TỐI ĐA BỘ NHỚ CONTEXT", "desc": "Không cần nạp tài liệu thừa, mỗi chuyên gia chỉ đọc đúng tài liệu của mình.", "pink_kw": "Không cần nạp tài liệu thừa"},
                {"num": "04", "title": "DỄ DÀNG THAY THẾ VÀ NÂNG CẤP", "desc": "Nâng cấp một khâu mà không làm ảnh hưởng đến hoạt động của toàn bộ dây chuyền.", "pink_kw": "Dễ dàng thay thế"}
            ]
        },
        "title": "1 Trợ Lý Biết Tuốt (Generalist) vs 10 Chuyên Gia Tinh Gọn (Specialists)",
        "cta_kw": "SPECIALIST",
        "caption": "👥 TẠI SAO BẠN NÊN DÙNG ĐỘI NGŨ 10 CHUYÊN GIA TINH GỌN THAY VÌ 1 BOT BIẾT TUỐT?\n\nMô hình 'All-in-one' đã lỗi thời. Khi cố bắt một chatbot làm tất cả mọi việc từ viết lách, code, dịch thuật đến đăng bài, chất lượng sẽ giảm sút nghiêm trọng.\n\nPhân tách thành 10 Subagent chuyên biệt là chìa khóa để đạt chuẩn chất lượng 9.5/10 trong mọi tác vụ.\n\n👇 Comment 'SPECIALIST' để nhận sơ đồ tổ chức đội ngũ AI tinh gọn nhất hiện nay!",
        "comment": "👉 Sơ đồ ma trận 10 Subagent chuyên môn hóa: Bình luận 'SPECIALIST' để nhận tài liệu phân vai."
    },
    {
        "day": 7, "date": "2026-11-01", "slot": "13:30", "code": "day7_img3_1330_multichan",
        "template": 3,
        "params": {
            "level_badge": "Phân Phối Đa Kênh",
            "bracket_title_colored": '[ <span style="color:#CCFF00">REPURPOSE</span> <span style="color:#FF2A6D">VIDEO</span> ]',
            "meta_info_left": "Phân phối qua",
            "meta_info_right": "1 Video Gốc -> 3 Nền Tảng Lớn",
            "cards_2x2": [
                {"icon": "key", "title": "Facebook Reels", "subtitle": "Ghim link ở comment đầu tiên"},
                {"icon": "book", "title": "YouTube Shorts", "subtitle": "Tiêu đề dưới 60 ký tự + 3 thẻ"},
                {"icon": "flow", "title": "TikTok Feed", "subtitle": "Gắn nhãn AI Disclosure minh bạch"},
                {"icon": "num", "num_or_icon": "3", "title": "Độ phủ thương hiệu", "subtitle": "Tăng gấp 3 lần lượt xem"}
            ],
            "footer_title_white": "SƠ ĐỒ TÁI CẤU TRÚC ĐA KÊNH",
            "footer_title_pink": "TỐI ƯU HÓA TỪNG NỀN TẢNG"
        },
        "title": "Sơ Đồ Phân Phối Đa Nền Tảng: Từ 1 Video Gốc Ra FB Reels, Shorts & Threads",
        "cta_kw": "MULTICHAN",
        "caption": "🌐 NGUYÊN TẮC 'ONE PIECE, MULTI-PLATFORM': BIẾN 1 VIDEO THÀNH TÀI SẢN TRÊN MỌI KÊNH!\n\nĐừng làm video chỉ để đăng lên một nền tảng duy nhất. Nhưng cũng tuyệt đối không đăng rập khuôn cùng một caption lên mọi nơi.\n- FB Reels: Cấm chèn link trên caption, dồn link vào bình luận đầu tiên.\n- YT Shorts: Tiêu đề ngắn gọn dưới 60 ký tự kèm 3 hashtag cốt lõi.\n- TikTok: Bắt buộc gắn nhãn AI generated content để bảo vệ kênh.\n\n👇 Comment 'MULTICHAN' để nhận quy chuẩn đăng bài chuẩn thuật toán 2026!",
        "comment": "👉 Hướng dẫn tối ưu video đa nền tảng thuật toán mới: Comment 'MULTICHAN' để lấy tài liệu."
    },
    {
        "day": 7, "date": "2026-11-01", "slot": "15:15", "code": "day7_img4_1515_caidatmay",
        "template": 4,
        "params": {
            "header_badge": "Cài đặt môi trường",
            "bracket_title_colored": '[ <span style="color:#CCFF00">WINDOWS</span> <span style="color:#FF2A6D">SETUP AI</span> ]',
            "selector_badge": "Trọn Bộ Hướng Dẫn Cài Đặt Môi Trường",
            "date_cards": [
                {"label": "Hệ điều hành", "date": "Windows 11", "highlight": False},
                {"label": "Công cụ", "date": "FFmpeg + TTS", "highlight": True},
                {"label": "Thời gian", "date": "Xong trong 15P", "highlight": True}
            ],
            "time_badge": "Mở cổng nhận quà: Hôm nay - Hết tuần",
            "delivery_text": "Gửi hướng dẫn chi tiết qua",
            "cta_button_text": "NHẬN HƯỚNG DẪN"
        },
        "title": "Trọn Bộ Hướng Dẫn Cài Đặt Môi Trường Windows Cho Đội Subagent Tự Hành",
        "cta_kw": "CAIDATMAY",
        "caption": "💻 HƯỚNG DẪN CÀI ĐẶT MÔI TRƯỜNG CHẠY AI AGENT TỰ HÀNH TRÊN WINDOWS TỪ A ĐẾN Z!\n\nNhiều bạn gặp khó khăn khi cài đặt Python, FFmpeg, Node.js và n8n trên máy tính Windows vì hay bị lỗi đường dẫn PATH hoặc xung đột môi trường.\n\nBộ tài liệu này sẽ hướng dẫn bạn từng bước với các dòng lệnh PowerShell tự động, giúp bạn thiết lập xong cả trạm làm việc trong 15 phút.\n\n👇 Comment 'CAIDATMAY' để nhận file hướng dẫn cài đặt miễn phí!",
        "comment": "👉 Tải trọn bộ hướng dẫn cài đặt máy Windows chạy AI Agent: Bình luận 'CAIDATMAY' để lấy link."
    },
    {
        "day": 7, "date": "2026-11-01", "slot": "18:15", "code": "day7_img5_1815_eodreport",
        "template": 5,
        "params": {
            "top_badge": "Báo cáo tổng kết tuần",
            "sold_out_text": "WEEKLY EOD",
            "slots": [
                {"title": "MỤC TIÊU BÀI ẢNH", "badge": "42 Bài Đã Render", "percent": 100},
                {"title": "MỤC TIÊU VIDEO REELS", "badge": "21 Video Chuẩn Vàng", "percent": 100}
            ],
            "cta_badge": "ĐỐI SOÁT & TỐI ƯU",
            "footer_tag": "TỔNG KẾT TUẦN ĐỘI NGŨ AGENT",
            "offer_big_left": "100%",
            "offer_mid_top": "HOÀN THÀNH",
            "offer_mid_sub": "ĐÚNG KẾ HOẠCH"
        },
        "title": "Tổng Kết Tuần: Bảng Đối Soát Số Liệu & Quyết Định Duy Trì Hay Tối Ưu",
        "cta_kw": "EODREPORT",
        "caption": "📊 BÁO CÁO TỔNG KẾT TUẦN: VẬN HÀNH 100% THEO ĐÚNG MỤC TIÊU VÀ KẾ HOẠCH!\n\nChủ Nhật là thời điểm tuyệt vời nhất để nhìn lại toàn bộ số liệu của cả tuần:\n- 42 bài viết hình ảnh chất lượng cao chuẩn Visual DNA mới.\n- 21 video ngắn được lên lịch đều đặn vào 3 khung giờ vàng mỗi ngày.\n- Duy trì 3 ca tương tác hội nhóm mỗi ngày để thu hút khán giả tự nhiên.\n\n👇 Comment 'EODREPORT' để nhận mẫu báo cáo End-of-Day chuẩn của Chief of Staff!",
        "comment": "👉 Nhận mẫu báo cáo vận hành tuần cho đội ngũ AI: Bình luận 'EODREPORT' để lấy file mẫu."
    },
    {
        "day": 7, "date": "2026-11-01", "slot": "21:15", "code": "day7_img6_2115_muctieu",
        "template": 2,
        "params": {
            "left_badge": "Mục tiêu tuần mới",
            "right_badge": "4 trọng tâm",
            "items": [
                {"num": "01", "title": "GIA TĂNG TƯƠNG TÁC THỰC", "desc": "Tham gia thảo luận sâu tại các hội nhóm AI lớn để xây dựng uy tín trang.", "pink_kw": "xây dựng uy tín trang"},
                {"num": "02", "title": "TỐI ƯU TỶ LỆ CHUYỂN ĐỔI LINK", "desc": "Thử nghiệm các mẫu bình luận ghim mới với quà tặng giá trị cao hơn.", "pink_kw": "quà tặng giá trị cao hơn"},
                {"num": "03", "title": "MỞ RỘNG KHO TÀI LIỆU MẪU", "desc": "Đóng gói thêm các bộ prompt và mã nguồn tự động hóa thực chiến cho cộng đồng.", "pink_kw": "mã nguồn tự động hóa thực chiến"},
                {"num": "04", "title": "TỰ ĐỘNG HÓA THÊM 1 KHÂU MỚI", "desc": "Tích hợp thêm bot tự động gửi tin nhắn chăm sóc thành viên khi họ bình luận.", "pink_kw": "tự động gửi tin nhắn chăm sóc"}
            ]
        },
        "title": "Khảo Sát Mục Tiêu Tuần Tới: Bạn Sẽ Tự Động Hóa Khâu Nào Đầu Tiên?",
        "cta_kw": "MUCTIEU",
        "caption": "🎯 MỤC TIÊU TUẦN MỚI CỦA BẠN LÀ GÌ? CHÚNG MÌNH SẴN SÀNG ĐỒNG HÀNH CÙNG BẠN!\n\n1 tuần mới lại sắp bắt đầu. Đừng để những công việc lặp đi lặp lại chiếm hết năng lượng sáng tạo của bạn. Hãy chọn 1 khâu bạn ghét làm nhất và tìm cách tự động hóa nó ngay trong tuần tới!\n\n👇 Hãy chia sẻ mục tiêu của bạn bên dưới hoặc gõ 'MUCTIEU' để nhận lộ trình 7 ngày bắt đầu!",
        "comment": "👉 Nhận lộ trình 7 ngày làm chủ tự động hóa: Bình luận 'MUCTIEU' để nhận bản kế hoạch hành động."
    },
]


def render_all_vault_posts():
    print(f"Bắt đầu kết xuất trọn bộ {len(VAULT_POSTS)} bài ảnh chuẩn phong cách Downloads\\vid...")
    start_time = time.time()
    
    success_count = 0
    for idx, post in enumerate(VAULT_POSTS):
        code = post["code"]
        tpl = post["template"]
        params = post["params"]
        img_out = IMAGES_DIR / f"{code}.jpg"
        cap_out = CAPTIONS_DIR / f"{code}_caption.txt"
        cmt_out = CAPTIONS_DIR / f"{code}_comment.txt"

        print(f"[{idx+1}/{len(VAULT_POSTS)}] Rendering {code}.jpg (Layout #{tpl})...")

        # 1. Render ảnh chuẩn theo template tương ứng
        if tpl == 1:
            render_template_hero_showcase(
                top_badge=params["top_badge"],
                tool_title_line1=params["tool_title_line1"],
                tool_title_line2=params["tool_title_line2"],
                bottom_badge=params["bottom_badge"],
                model_name=params["model_name"],
                output_path=img_out,
            )
        elif tpl == 2:
            render_template_curriculum_breakdown(
                left_badge=params["left_badge"],
                right_badge=params["right_badge"],
                items=params["items"],
                output_path=img_out,
            )
        elif tpl == 3:
            render_template_feature_matrix(
                level_badge=params["level_badge"],
                bracket_title_colored=params["bracket_title_colored"],
                meta_info_left=params["meta_info_left"],
                meta_info_right=params["meta_info_right"],
                cards_2x2=params["cards_2x2"],
                footer_title_white=params["footer_title_white"],
                footer_title_pink=params["footer_title_pink"],
                output_path=img_out,
            )
        elif tpl == 4:
            render_template_offer_card(
                header_badge=params["header_badge"],
                bracket_title_colored=params["bracket_title_colored"],
                selector_badge=params["selector_badge"],
                date_cards=params["date_cards"],
                time_badge=params["time_badge"],
                delivery_text=params["delivery_text"],
                cta_button_text=params["cta_button_text"],
                output_path=img_out,
            )
        elif tpl == 5:
            render_template_urgency_slots(
                top_badge=params["top_badge"],
                sold_out_text=params["sold_out_text"],
                slots=params["slots"],
                cta_badge=params["cta_badge"],
                footer_tag=params["footer_tag"],
                offer_big_left=params["offer_big_left"],
                offer_mid_top=params["offer_mid_top"],
                offer_mid_sub=params["offer_mid_sub"],
                output_path=img_out,
            )

        # 2. Ghi caption và pinned comment
        cap_out.write_text(post["caption"], encoding="utf-8")
        cmt_out.write_text(post["comment"], encoding="utf-8")
        success_count += 1

    elapsed = time.time() - start_time
    print(f"\n Hoàn tất xuất xưởng {success_count}/{len(VAULT_POSTS)} ảnh vuông 1:1 chuẩn Downloads\\vid trong {elapsed:.1f} giây!")
    print(f"📁 Thư mục ảnh: {IMAGES_DIR}")
    print(f"📁 Thư mục caption: {CAPTIONS_DIR}")


if __name__ == "__main__":
    render_all_vault_posts()
