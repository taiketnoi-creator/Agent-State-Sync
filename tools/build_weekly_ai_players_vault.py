#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_weekly_ai_players_vault.py — Khởi Tạo Trọn Gói Kho Nội Dung 1 Tuần Cho Page AI Players
Theo Đúng Chỉ Đạo Của CEO:
- 1 Ngày 3 Video Reels (11:45, 16:30, 20:00) -> 21 Video Reels Remotion Chuẩn Vàng / Tuần.
- 1 Ngày 6 Bài Ảnh Vuông 1:1 Độc Bản (Luân phiên 6 Layout) -> 42 Bài Ảnh / Tuần.
- Tổng 63 Bài Đăng Hoàn Chỉnh Kèm Pinned Comment #1 Dẫn Phễu.
"""

import datetime as dt
import json
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
VAULT_DIR = SUBAGENT_DIR / "campaigns" / "2026-10-26" / "ai-players-weekly-vault"
VAULT_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# 1. MA TRẬN 42 BÀI ẢNH VUÔNG 1:1 (7 NGÀY X 6 LAYOUTS ARCHETYPES ĐỘC BẢN)
# ==============================================================================
LAYOUT_NAMES = {
    1: "Layout #1: 3D Hero Scene + Energy Rings (Cửa sổ UI nghiêng góc)",
    2: "Layout #2: VS Split-Screen Comparison (Chia đôi đối kháng Trái - Phải)",
    3: "Layout #3: Isometric 3D Pipeline Flowchart (Sơ đồ dây chuyền 3D)",
    4: "Layout #4: Asymmetric Left-Right Editorial (Bố cục tạp chí bất đối xứng)",
    5: "Layout #5: Giant Centerpiece + Anatomy Callouts (Giải phẫu vật thể tâm)",
    6: "Layout #6: Bento Modular Grid Asymmetric (Lưới Bento 4 ô đa kích thước)",
}

DAILY_THEMES_IMAGES = [
    # Ngày 1: Thứ Hai 26/10
    {
        "day": 1,
        "date": "2026-10-26",
        "posts": [
            {
                "slot": "14:15",
                "layout": 1,
                "title": "Review GitHub Hot: Repo browser-use (55,000+ Stars)",
                "image_file": "campaigns/2026-10-20/today-launch/images/ai-square-02-github-browser-use.jpg",
                "cta_kw": "REPO",
                "status": "PUBLISHED_LIVE",
                "post_id": "1022527194267367_122133384717248983",
            },
            {
                "slot": "15:45",
                "layout": 2,
                "title": "So Sánh Thực Chiến: F5-TTS 0đ Local vs. Voice Tool $99/Tháng",
                "image_file": "campaigns/2026-10-20/today-launch/images/ai-square-03-github-f5-tts.jpg",
                "cta_kw": "VOICE",
                "status": "QUEUED",
            },
            {
                "slot": "17:15",
                "layout": 4,
                "title": "Tặng Sổ Tay 50 Siêu Prompt Văn Phòng & Lập Trình Thực Chiến",
                "image_file": "campaigns/2026-10-20/today-launch/images/ai-square-01-lead-prompt50.jpg",
                "cta_kw": "PROMPT50",
                "status": "QUEUED",
            },
            {
                "slot": "18:45",
                "layout": 5,
                "title": "Mở Rương Kho Báu: 30,000+ Stars Repo Awesome-LLM-Apps",
                "image_file": "campaigns/2026-10-20/today-launch/images/ai-square-04-github-awesome-llm.jpg",
                "cta_kw": "KHOBAU",
                "status": "QUEUED",
            },
            {
                "slot": "20:45",
                "layout": 3,
                "title": "Sơ Đồ Dây Chuyền Subagent 24/7 Tự Hành Thay Thế 1 Phòng Vận Hành",
                "image_file": "campaigns/2026-10-20/today-launch/images/ai-square-05-lead-hethong.jpg",
                "cta_kw": "HETHONG",
                "status": "QUEUED",
            },
            {
                "slot": "21:45",
                "layout": 6,
                "title": "Khảo Sát Tương Tác: 4 Việc Nên Giao Cho AI Tự Làm Ngay Hôm Nay",
                "image_file": "campaigns/2026-10-20/today-launch/images/ai-square-06-4tasks-grid.jpg",
                "cta_kw": "ABCD",
                "status": "QUEUED",
            },
        ],
    },
    # Ngày 2: Thứ Ba 27/10
    {
        "day": 2,
        "date": "2026-10-27",
        "posts": [
            {"slot": "08:30", "layout": 1, "title": "Claude 3.5 Artifacts: Biến Ý Tưởng Thành App Chạy Được Trong 30 Giây", "cta_kw": "ARTIFACTS"},
            {"slot": "10:15", "layout": 2, "title": "Local LLM vs Cloud API: Khi Nào Nên Chạy Ollama Trên Máy Riêng?", "cta_kw": "OLLAMA"},
            {"slot": "13:30", "layout": 3, "title": "Bản Vẽ Quy Trình Đóng Gói Prompt Thành Subagent .MD Độc Lập", "cta_kw": "SUBAGENT"},
            {"slot": "15:15", "layout": 4, "title": "Bộ 20 Prompt Tối Ưu Hóa Truy Vấn SQL & Xử Lý Dữ Liệu Báo Cáo", "cta_kw": "SQLAI"},
            {"slot": "18:15", "layout": 5, "title": "Giải Phẫu Kiến Trúc DeepSeek-Coder: Đỉnh Cao Code Open-Source", "cta_kw": "DEEPSEEK"},
            {"slot": "21:15", "layout": 6, "title": "Checklist 4 Bước Triển Khai n8n Webhook Không Cần Biết Viết Code", "cta_kw": "N8NHUB"},
        ],
    },
    # Ngày 3: Thứ Tư 28/10
    {
        "day": 3,
        "date": "2026-10-28",
        "posts": [
            {"slot": "08:30", "layout": 1, "title": "Remotion 4.0: Biến Code React Thành Video Ngắn 9:16 Không Cần Mở Premiere", "cta_kw": "REMOTION"},
            {"slot": "10:15", "layout": 2, "title": "Giọng Đọc AI Miễn Phí (Edge-TTS) Đối Đầu Giọng Đọc Trả Phí Studio", "cta_kw": "VOICETEST"},
            {"slot": "13:30", "layout": 3, "title": "Kiến Trúc Phễu 3 Tầng: Bình Luận FB -> Auto-DM -> Nhóm Zalo Bảo Mật", "cta_kw": "ZALOHUB"},
            {"slot": "15:15", "layout": 4, "title": "Sổ Tay 30 Hook 3 Giây Đầu Giữ Chân Khán Giả Xem Video Ngắn Đạt 60%+", "cta_kw": "HOOK3S"},
            {"slot": "18:15", "layout": 5, "title": "Kho Vũ Khí MCP: Top 5 MCP Servers Không Thể Thiếu Cho Dân Tự Động Hóa", "cta_kw": "MCPSERVER"},
            {"slot": "21:15", "layout": 6, "title": "Bảng Chấm Điểm 10 Tiêu Chí Nghiệm Thu Kịch Bản Trước Khi Render", "cta_kw": "RUBRIC10"},
        ],
    },
    # Ngày 4: Thứ Năm 29/10
    {
        "day": 4,
        "date": "2026-10-29",
        "posts": [
            {"slot": "08:30", "layout": 1, "title": "Cursor & Windsurf: Kỷ Nguyên Lập Trình Với AI Agent Tự Sửa Đa File", "cta_kw": "CURSOR"},
            {"slot": "10:15", "layout": 2, "title": "Mô Hình AI Đắt Tiền vs Mô Hình Rẻ: Đoạn Nào Nên Dùng Gemini Flash?", "cta_kw": "FLASHTEST"},
            {"slot": "13:30", "layout": 3, "title": "Sơ Đồ Kết Nối SQLite Local Với AI Để Lưu Nhớ Bối Cảnh Vĩnh Viễn", "cta_kw": "SQLITEAI"},
            {"slot": "15:15", "layout": 4, "title": "Tặng Bộ Template System Prompt Cho Trợ Lý Chief of Staff Điều Phối", "cta_kw": "MAMAPROMPT"},
            {"slot": "18:15", "layout": 5, "title": "Giải Phẫu Cơ Chế Anti-Hallucination: 3 Lớp Khóa Chặt Dữ Liệu Bịa Đặt", "cta_kw": "ANTIHALLU"},
            {"slot": "21:15", "layout": 6, "title": "Khảo Sát: Rào Cản Lớn Nhất Của Bạn Khi Tự Động Hóa Bằng AI Là Gì?", "cta_kw": "RAOCAN"},
        ],
    },
    # Ngày 5: Thứ Sáu 30/10
    {
        "day": 5,
        "date": "2026-10-30",
        "posts": [
            {"slot": "08:30", "layout": 1, "title": "Anthropic Computer Use: Khi AI Tự Di Chuột & Gõ Phím Thay Bạn", "cta_kw": "COMPUSE"},
            {"slot": "10:15", "layout": 2, "title": "Tự Động Hóa Bằng Code Thuần vs Dùng Nền Tảng No-Code: Chọn Đường Nào?", "cta_kw": "CODEVSNO"},
            {"slot": "13:30", "layout": 3, "title": "Bản Vẽ Hệ Thống Đồng Bộ Hai Chiều Giữa Máy Ở Nhà Và Máy Văn Phòng", "cta_kw": "SYNCSYS"},
            {"slot": "15:15", "layout": 4, "title": "Sổ Tay 15 Cấu Trúc JSON Schema Ép AI Xuất Đúng Định Dạng 100%", "cta_kw": "JSONPROMPT"},
            {"slot": "18:15", "layout": 5, "title": "Kho Lưu Trữ Bài Học: Cách Xây Dựng Bộ Não Thứ 2 Cho Đội Ngũ AI", "cta_kw": "BONAOTHU2"},
            {"slot": "21:15", "layout": 6, "title": "4 Chỉ Số Sống Còn Cần Đo Lường Khi Vận Hành Kênh Tự Động 2026", "cta_kw": "4CHISO"},
        ],
    },
    # Ngày 6: Thứ Bảy 31/10
    {
        "day": 6,
        "date": "2026-10-31",
        "posts": [
            {"slot": "08:30", "layout": 1, "title": "FastHTML: Xây Giao Diện Web Đẹp Cho Ứng Dụng AI Bằng 100% Python", "cta_kw": "FASTHTML"},
            {"slot": "10:15", "layout": 2, "title": "Chi Phí Nhân Sự Truyền Thống vs Vận Hành Bằng Đội 10 Subagent", "cta_kw": "ROIAI"},
            {"slot": "13:30", "layout": 3, "title": "Quy Trình Tự Động Dọn Dẹp Kho Dữ Liệu Rác Định Kỳ 7 Ngày 0-Token", "cta_kw": "CLEANUP7D"},
            {"slot": "15:15", "layout": 4, "title": "Tặng Bộ Prompt Săn Sản Phẩm & Phân Tích Đánh Giá Khách Hàng VoC", "cta_kw": "PROMPTMKT"},
            {"slot": "18:15", "layout": 5, "title": "Top 10 GitHub Trending Repos Về Multi-Agent Đáng Thử Nghiệm Nhất", "cta_kw": "TOP10AGENTS"},
            {"slot": "21:15", "layout": 6, "title": "Khảo Sát: Cuối Tuần Bạn Dành Mấy Tiếng Để Tối Ưu Lại Quy Trình Làm Việc?", "cta_kw": "CUOITUAN"},
        ],
    },
    # Ngày 7: Chủ Nhật 01/11
    {
        "day": 7,
        "date": "2026-11-01",
        "posts": [
            {"slot": "08:30", "layout": 1, "title": "Trạm Chỉ Huy Telegram Bot: Giao Việc & Nhận Báo Cáo Khi Đang Đi Cà Phê", "cta_kw": "TELEBOT"},
            {"slot": "10:15", "layout": 2, "title": "1 Trợ Lý Biết Tuốt (Generalist) vs 10 Chuyên Gia Tinh Gọn (Specialists)", "cta_kw": "SPECIALIST"},
            {"slot": "13:30", "layout": 3, "title": "Sơ Đồ Phân Phối Đa Nền Tảng: Từ 1 Video Gốc Ra FB Reels, Shorts & Threads", "cta_kw": "MULTICHAN"},
            {"slot": "15:15", "layout": 4, "title": "Trọn Bộ Hướng Dẫn Cài Đặt Môi Trường Windows Cho Đội Subagent Tự Hành", "cta_kw": "CAIDATMAY"},
            {"slot": "18:15", "layout": 5, "title": "Tổng Kết Tuần: Bảng Đối Soát Số Liệu & Quyết Định Duy Trì Hay Tối Ưu", "cta_kw": "EODREPORT"},
            {"slot": "21:15", "layout": 6, "title": "Khảo Sát Mục Tiêu Tuần Tới: Bạn Sẽ Tự Động Hóa Khâu Nào Đầu Tiên?", "cta_kw": "MUCTIEU"},
        ],
    },
]

# ==============================================================================
# 2. MA TRẬN 21 VIDEO REELS REMOTION CHUẨN VÀNG (7 NGÀY X 3 REELS/NGÀY)
# Khung Giờ Vàng Cố Định: 11:45 (Trưa) - 16:30 (Chiều) - 20:00 (Tối)
# ==============================================================================
DAILY_THEMES_REELS = [
    # Ngày 1: Thứ Hai 26/10
    {
        "day": 1,
        "date": "2026-10-26",
        "reels": [
            {
                "slot": "15:00",  # Bù mốc trưa
                "id": "r01",
                "title": "AI Agent Tự Hành Khác Gì Chatbot Thông Thường?",
                "source": "templates/remotion-cuongit-template/src/AiHallucinationShort",
                "file_ready": "campaigns/2026-10-20/ai-agent-vs-chatbot-45s/ai-agent-vs-chatbot-45s.mp4",
                "cta_kw": "AGENT",
            },
            {
                "slot": "16:30",
                "id": "r02",
                "title": "Bản Đồ 4 Trụ Cột AI Hiện Tại & Bước Ngoặt Robotics 2026",
                "source": "templates/remotion-cuongit-template/src/AiHallucinationShort",
                "file_ready": "campaigns/2026-10-20/ai-map-pillars-45s/ai-map-pillars-45s.mp4",
                "cta_kw": "BANDO",
            },
            {
                "slot": "20:00",
                "id": "r03",
                "title": "Model Context Protocol (MCP) Là Gì? Cổng USB-C Cho AI",
                "source": "templates/remotion-cuongit-template/src/McpShort",
                "file_ready": "campaigns/2026-10-20/mcp-ai-explainer-40s/mcp-ai-explainer-40s.mp4",
                "cta_kw": "MCP",
            },
        ],
    },
    # Ngày 2: Thứ Ba 27/10
    {
        "day": 2,
        "date": "2026-10-27",
        "reels": [
            {
                "slot": "11:45",
                "id": "r04",
                "title": "Tại Sao 1 Khung Chat AI Hay Loạn, Còn Đội 6 Subagent Chạy Mượt Gấp 10 Lần?",
                "source": "tools/build_ai_players_4day_vault.py (v01)",
                "cta_kw": "SUBAGENT",
            },
            {
                "slot": "16:30",
                "id": "r05",
                "title": "Đừng Học Gõ Prompt Lẻ Tẻ Nữa! Hãy Đóng Gói Quy Trình Thành File .MD",
                "source": "tools/build_ai_players_4day_vault.py (v02)",
                "cta_kw": "PROMPTPACK",
            },
            {
                "slot": "20:00",
                "id": "r06",
                "title": "Căn Bệnh Ảo Giác Của Trí Tuệ Nhân Tạo & Cách Khóa Chặt 3 Lớp",
                "source": "templates/remotion-cuongit-template/src/AiHallucinationShort",
                "file_ready": "campaigns/2026-10-20/ai-hallucination-45s/ai-hallucination-45s.mp4",
                "cta_kw": "HALLUCINATION",
            },
        ],
    },
    # Ngày 3: Thứ Tư 28/10
    {
        "day": 3,
        "date": "2026-10-28",
        "reels": [
            {
                "slot": "11:45",
                "id": "r07",
                "title": "Kiến Trúc Zero-Token: Kết Hợp n8n Và SQLite Giảm 85% Chi Phí API",
                "source": "tools/build_ai_players_4day_vault.py (v03)",
                "cta_kw": "ZEROTOKEN",
            },
            {
                "slot": "16:30",
                "id": "r08",
                "title": "Làm Sao Chặn Đứng Lỗi AI Bịa Số Liệu? Đặt Ngay Trạm Kiểm Duyệt 10 Tiêu Chí",
                "source": "tools/build_ai_players_4day_vault.py (v04)",
                "cta_kw": "KIEMDUYET",
            },
            {
                "slot": "20:00",
                "id": "r09",
                "title": "Biến Telegram Thành Trạm Chỉ Huy AI Từ Xa: Đi Cà Phê Vẫn Điều Khiển Cả Hệ Thống",
                "source": "tools/build_ai_players_4day_vault.py (v05)",
                "cta_kw": "TELEGRAMAI",
            },
        ],
    },
    # Ngày 4: Thứ Năm 29/10
    {
        "day": 4,
        "date": "2026-10-29",
        "reels": [
            {
                "slot": "11:45",
                "id": "r10",
                "title": "Giải Phẫu Dây Chuyền Làm Video AI Tự Động Hoàn Tất Trong 5 Phút",
                "source": "tools/build_ai_players_4day_vault.py (v06)",
                "cta_kw": "AIVIDEO",
            },
            {
                "slot": "16:30",
                "id": "r11",
                "title": "Tại Sao AI Cứ Quên Việc Hôm Qua? Cách Xây Bộ Não Thứ Hai Lưu Trữ Vĩnh Viễn",
                "source": "tools/build_ai_players_4day_vault.py (v07)",
                "cta_kw": "BONAOTHU2",
            },
            {
                "slot": "20:00",
                "id": "r12",
                "title": "AI Tự Cầm Chuột Điều Khiển Trình Duyệt Chrome: Từ Hỏi Đáp Sang Thực Chiến",
                "source": "tools/build_ai_players_4day_vault.py (v08)",
                "cta_kw": "CHROMEAI",
            },
        ],
    },
    # Ngày 5: Thứ Sáu 30/10
    {
        "day": 5,
        "date": "2026-10-30",
        "reels": [
            {
                "slot": "11:45",
                "id": "r13",
                "title": "Chiến Thuật Phân Tầng Model: Khi Nào Dùng Bản Pro, Khi Nào Dùng Bản Flash?",
                "source": "tools/build_ai_players_4day_vault.py (v09)",
                "cta_kw": "TIERING",
            },
            {
                "slot": "16:30",
                "id": "r14",
                "title": "Tự Động Hóa Báo Cáo Mỗi Sáng: Để AI Tự Quét Số Liệu Và Đề Xuất Lúc 9 Giờ",
                "source": "tools/build_ai_players_4day_vault.py (v10)",
                "cta_kw": "AUTOREPORT",
            },
            {
                "slot": "20:00",
                "id": "r15",
                "title": "Đòn Bẩy Nhân Sự Số 2026: Một Người Vận Hành Cả Phòng Marketing Bằng Subagent",
                "source": "tools/build_ai_players_4day_vault.py (v11)",
                "cta_kw": "DONBAYAI",
            },
        ],
    },
    # Ngày 6: Thứ Bảy 31/10
    {
        "day": 6,
        "date": "2026-10-31",
        "reels": [
            {
                "slot": "11:45",
                "id": "r16",
                "title": "Bí Kíp Đóng Gói Prompt Thành Vũ Khí Thực Chiến Cho Freelancer & Creator",
                "source": "curated_vault_r16",
                "cta_kw": "PROMPTHUB",
            },
            {
                "slot": "16:30",
                "id": "r17",
                "title": "Bảo Vệ Tài Khoản & Quota API: 3 Cách Cắt Giảm Chi Phí LLM Thông Minh",
                "source": "curated_vault_r17",
                "cta_kw": "CUTCOST",
            },
            {
                "slot": "20:00",
                "id": "r18",
                "title": "Xây Dựng Phễu Thu Hút Khách Hàng Tự Động Từ Fanpage Vào Nhóm Zalo 0 Đồng",
                "source": "curated_vault_r18",
                "cta_kw": "PHEUZALO",
            },
        ],
    },
    # Ngày 7: Chủ Nhật 01/11
    {
        "day": 7,
        "date": "2026-11-01",
        "reels": [
            {
                "slot": "11:45",
                "id": "r19",
                "title": "Quy Chuẩn Chống Trùng Lặp Nội Dung (Anti-Clone): Tạo Khác Biệt Khi Làm Video AI",
                "source": "curated_vault_r19",
                "cta_kw": "ANTICLONE",
            },
            {
                "slot": "16:30",
                "id": "r20",
                "title": "Tại Sao Không Nên Làm Mọi Thứ Bằng Tay Khi AI Có Thể Làm Thay Bạn 80%?",
                "source": "curated_vault_r20",
                "cta_kw": "AUTOMATE",
            },
            {
                "slot": "20:00",
                "id": "r21",
                "title": "Lộ Trình Nâng Cấp Kỹ Năng Kỹ Sư AI 4.0: Từ Người Hỏi Chatbot Đến Kiến Trúc Sư AI",
                "source": "curated_vault_r21",
                "cta_kw": "LORINHAI",
            },
        ],
    },
]


def generate_master_manifest():
    manifest = {
        "campaign_id": "CAMP-20261026-AI-PLAYERS-WEEKLY-VAULT",
        "page_name": "AI Players - Người chơi hệ AI",
        "page_id": "1022527194267367",
        "total_days": 7,
        "period": "2026-10-26 to 2026-11-01",
        "kpi_target": "9 posts / day (3 Video Reels + 6 Square 1:1 Images)",
        "total_reels": 21,
        "total_images": 42,
        "total_posts": 63,
        "image_matrix": DAILY_THEMES_IMAGES,
        "reels_matrix": DAILY_THEMES_REELS,
    }
    out_file = VAULT_DIR / "master_vault_manifest.json"
    out_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Đã tạo Master Manifest tại: {out_file}")
    return manifest


if __name__ == "__main__":
    generate_master_manifest()
