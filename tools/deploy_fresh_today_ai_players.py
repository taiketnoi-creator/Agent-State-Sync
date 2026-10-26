#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deploy_fresh_today_ai_players.py — Khởi Tạo & Triển Khai 5 Bài Ảnh Độc Bản 100% MỚI Cho Hôm Nay (26/10)
Triệt tiêu hoàn toàn lỗi tái sử dụng bài cũ của ngày 20/10:
- Bài 1 (ĐĂNG LIVE NGAY): Kiến Trúc Multi-Agent 2026 (CTA: MULTIAGENT)
- Bài 2 (HẸN 15:45): Top 5 Kho Mã Nguồn Mở Tự Động Hóa Dữ Liệu Q4/2026 (CTA: TOP5REPO)
- Bài 3 (HẸN 17:15): Bí Quyết Context Firewall Giúp AI Chạy Cả Ngày Không Bị Loạn (CTA: FIREWALL)
- Bài 4 (HẸN 18:45): Sơ Đồ Bắn Báo Cáo Doanh Thu Từ SQLite Về Telegram (CTA: TELEGRAMHUB)
- Bài 5 (HẸN 20:45): Khảo Sát: Bạn Dùng AI Tiết Kiệm Được Bao Nhiêu Giờ/Tuần? (CTA: GIO)
"""

import datetime as dt
import json
import mimetypes
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
VAULT_DIR = SUBAGENT_DIR / "campaigns" / "2026-10-26" / "ai-players-weekly-vault"
IMAGES_DIR = VAULT_DIR / "images"
CAPTIONS_DIR = VAULT_DIR / "captions"
VAULT_PATH = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / "pages_vault.json"

AI_PAGE_ID = "1022527194267367"
GRAPH_VERSION = "v22.0"
VN_TZ = dt.timezone(dt.timedelta(hours=7))

FONT_BOLD_PATH = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REG_PATH = "C:/Windows/Fonts/segoeui.ttf"


def get_token() -> str:
    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
    for p in vault.get("pages", []):
        if str(p.get("id")) == AI_PAGE_ID:
            return p.get("access_token", "")
    return ""


def get_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def render_card(output_path: Path, title: str, cta_kw: str, archetype: str, highlight_items: list[tuple[str, str]]):
    w, h = 1080, 1080
    im = Image.new("RGB", (w, h), "#050A1A")
    draw = ImageDraw.Draw(im)

    # Grid
    for x in range(0, w, 54):
        draw.line([(x, 0), (x, h)], fill="#0B1430", width=1)
    for y in range(0, h, 54):
        draw.line([(0, y), (w, y)], fill="#0B1430", width=1)

    accent_lime = "#87FF00"
    # Corners
    for cx, cy in [(40, 40), (w - 40, 40), (40, h - 40), (w - 40, h - 40)]:
        dx = 80 if cx == 40 else -80
        dy = 80 if cy == 40 else -80
        draw.line([(cx, cy), (cx + dx, cy)], fill=accent_lime, width=4)
        draw.line([(cx, cy), (cx, cy + dy)], fill=accent_lime, width=4)

    # Top Header
    draw.rounded_rectangle([70, 70, w - 70, 124], radius=10, fill="#0E1A40", outline=accent_lime, width=1)
    draw.text((95, 84), "AI PLAYERS • ĐỘC BẢN THỰC CHIẾN 2026", fill=accent_lime, font=get_font(FONT_BOLD_PATH, 24))
    draw.text((w - 320, 86), archetype.upper(), fill="#94A3B8", font=get_font(FONT_REG_PATH, 18))

    # Title
    words = title.split()
    lines, cur = [], []
    for word in words:
        test = " ".join(cur + [word])
        if len(test) > 28 and cur:
            lines.append(" ".join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(" ".join(cur))

    y_pos = 165
    for idx, l in enumerate(lines[:3]):
        color = accent_lime if idx == 0 else "#FFFFFF"
        draw.text((80, y_pos), l, fill=color, font=get_font(FONT_BOLD_PATH, 44))
        y_pos += 60

    # Glass Box
    box_top = max(y_pos + 30, 370)
    box_bot = 880
    draw.rounded_rectangle([70, box_top, w - 70, box_bot], radius=20, fill="#0B1736", outline="#1D3670", width=2)
    draw.rounded_rectangle([70, box_top, w - 70, box_top + 50], radius=15, fill="#122352")
    draw.text((95, box_top + 13), "⚡ PHÂN TÍCH KIẾN TRÚC & GIẢI PHÁP ĐỘT PHÁ", fill=accent_lime, font=get_font(FONT_BOLD_PATH, 20))

    fy = box_top + 80
    for num, txt in highlight_items:
        draw.rounded_rectangle([95, fy, 145, fy + 42], radius=8, fill="#18316B", outline=accent_lime, width=1)
        draw.text((106, fy + 8), num, fill=accent_lime, font=get_font(FONT_BOLD_PATH, 20))
        draw.text((165, fy + 10), txt, fill="#E2E8F0", font=get_font(FONT_REG_PATH, 23))
        fy += 75

    draw.line([(95, box_bot - 55), (w - 95, box_bot - 55)], fill="#1B3264", width=1)
    draw.text((95, box_bot - 42), "CHUẨN HÓA: ANTHROPIC MCP • GEMINI 4 FLASH • PYTHON LOCAL • 0-TOKEN", fill="#64748B", font=get_font(FONT_REG_PATH, 16))

    # Giant CTA
    draw.rounded_rectangle([70, 920, w - 70, 1010], radius=16, fill=accent_lime)
    cta_str = f"BÌNH LUẬN \"{cta_kw}\" ĐỂ LẤY SƠ ĐỒ Ở COMMENT ĐẦU"
    draw.text((95, 942), cta_str, fill="#050A1A", font=get_font(FONT_BOLD_PATH, 32))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    im.save(output_path, quality=95)


def post_or_schedule(token: str, img_path: Path, caption: str, sched_ts: int | None = None) -> dict:
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{AI_PAGE_ID}/photos"
    boundary = f"----FreshJavisBoundary{uuid.uuid4().hex}"
    body = bytearray()

    def add_f(k, v):
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{v}\r\n".encode("utf-8"))

    add_f("access_token", token)
    add_f("message", caption)
    if sched_ts:
        add_f("published", "false")
        add_f("scheduled_publish_time", str(sched_ts))
    else:
        add_f("published", "true")

    mime_type = mimetypes.guess_type(str(img_path))[0] or "image/jpeg"
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="source"; filename="{img_path.name}"\r\n'.encode("utf-8"))
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    body.extend(img_path.read_bytes())
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        url, data=bytes(body), headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=40.0) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode("utf-8", errors="ignore"), "code": e.code}


def post_comment(token: str, post_id: str, message: str) -> dict:
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{post_id}/comments"
    data = urllib.parse.urlencode({"message": message, "access_token": token}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20.0) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode("utf-8", errors="ignore"), "code": e.code}


FRESH_PACK = [
    {
        "id": "fresh_01",
        "action": "LIVE_NOW",
        "title": "Kiến Trúc Multi-Agent 2026: Tại Sao 1 Chatbot Sẽ Bị Thay Thế Bởi Đội Ngũ Tự Hành?",
        "archetype": "Layout #1: 3D Hero Scene",
        "cta_kw": "MULTIAGENT",
        "items": [
            ("01", "Mỗi Subagent giữ đúng 1 vai trò: Nghiên cứu, Viết, Dựng, Kiểm duyệt."),
            ("02", "Tường lửa ngữ cảnh độc lập, không làm tràn bộ nhớ khi xử lý việc lớn."),
            ("03", "Phân tầng Model thông minh: Gemini 4 cho sáng tạo, Flash cho hậu cần."),
        ],
        "caption": (
            "Năm 2026, khoảng cách về hiệu suất không còn nằm ở việc ai gõ câu lệnh hay hơn, "
            "mà nằm ở việc bạn đang dùng 1 khung chat đơn độc hay đang sở hữu một Đội quân Subagent tự hành! ⚡\n\n"
            "Tại sao nhồi 10 việc vào 1 khung chat thì AI hay bị loạn và quên sạch dữ liệu?\n"
            "Bí mật nằm ở nguyên lý Context Firewall: Chia nhỏ luồng làm việc thành các chuyên gia độc lập — "
            "từ Săn sản phẩm, Viết kịch bản, Thiết kế visual cho đến Thanh tra kiểm duyệt 10 tiêu chí.\n\n"
            "👉 Bình luận ngay \"MULTIAGENT\" hoặc xem ở bình luận đầu tiên để nhận trọn bộ sơ đồ kiến trúc nhé!\n\n"
            "#AIPlayers #MultiAgent #Subagent #TuDongHoa #AI2026 #KienTrucAI"
        ),
        "comment": (
            "🎯 [BÌNH LUẬN GHIM - TÀI LIỆU MULTI-AGENT THỰC CHIẾN]\n\n"
            "Chào bạn! Sơ đồ kiến trúc Đội quân Subagent và tài liệu triển khai từ khóa \"MULTIAGENT\" đã sẵn sàng tại:\n"
            "🔗 Nhóm Zalo AI Players: https://zalo.me/g/etllok798 (Mã mở khóa: AIPLAYERS2026)\n\n"
            "❓ Giao lưu nhanh: Trong công việc hiện tại, bạn thấy khâu nào tốn nhiều thời gian nhất khiến bạn muốn có 1 nhân sự AI tự làm thay?"
        ),
    },
    {
        "id": "fresh_02",
        "action": "SCHEDULE",
        "slot_time": "2026-10-26 15:45",
        "title": "Top 5 Kho Mã Nguồn Mở Tự Động Hóa Dữ Liệu Đình Đám Nhất Quý 4/2026",
        "archetype": "Layout #4: Asymmetric Editorial",
        "cta_kw": "TOP5REPO",
        "items": [
            ("01", "Bộ công cụ tự động cào dữ liệu và phân tích đối thủ cạnh tranh."),
            ("02", "Server MCP kết nối database SQLite cục bộ với AI an toàn tuyệt đối."),
            ("03", "Pipeline chuyển hóa kịch bản thành đồ họa chuyển động Remotion 0đ."),
        ],
        "caption": (
            "Thay vì bỏ ra hàng chục triệu mua các phần mềm đóng gói sẵn, cộng đồng mã nguồn mở 2026 "
            "đang cung cấp những vũ khí tự động hóa cực kỳ mạnh mẽ mà hoàn toàn miễn phí! 🚀\n\n"
            "Tổng hợp 5 repository GitHub chất lượng cao nhất cho dân tự động hóa:\n"
            "1. Hệ thống điều khiển trình duyệt không chạm.\n"
            "2. Cầu nối n8n Webhook đa kênh.\n"
            "3. Trạm trích xuất giọng đọc phòng thu AI.\n"
            "4. Công cụ kiểm soát ảo giác số liệu.\n"
            "5. Kho template dựng video slide công nghệ bằng code.\n\n"
            "👉 Bình luận \"TOP5REPO\" để nhận danh sách link và hướng dẫn cài đặt ở bình luận đầu tiên nhé!\n\n"
            "#AIPlayers #GitHubOpenSource #AutomationTools #CodeLess #DevCommunity"
        ),
        "comment": (
            "🎯 [BÌNH LUẬN GHIM - TOP 5 REPO GITHUB 2026]\n\n"
            "Link tải toàn bộ tài liệu cài đặt cho từ khóa \"TOP5REPO\":\n"
            "🔗 Kho tài liệu cộng đồng: https://zalo.me/g/etllok798 (Mã bảo mật: AIPLAYERS2026)\n\n"
            "❓ Bạn đã từng triển khai công cụ mã nguồn mở nào vào công việc chưa hay chủ yếu dùng tool trả phí?"
        ),
    },
    {
        "id": "fresh_03",
        "action": "SCHEDULE",
        "slot_time": "2026-10-26 17:15",
        "title": "Bí Quyết Context Firewall Giúp AI Chạy Cả Ngày Không Bị Tràn Bộ Nhớ",
        "archetype": "Layout #5: Giant Centerpiece",
        "cta_kw": "FIREWALL",
        "items": [
            ("01", "Cơ chế Zero-Waste: Giao tiếp qua tệp trung gian, không đổ dữ liệu thô ra chat."),
            ("02", "Báo cáo cô đọng tối đa 10-15 dòng kèm điểm chất lượng Rubric /10."),
            ("03", "Lưu vĩnh viễn bối cảnh quan trọng vào SQLite và thư mục tri thức Bộ Não Thứ 2."),
        ],
        "caption": (
            "Lỗi phổ biến nhất khi dùng AI làm việc quy mô lớn: Càng chat nhiều thì AI càng chậm, "
            "bắt đầu 'ảo giác', quên các chỉ dẫn ban đầu và tiêu tốn hàng đống chi phí API! 🛑\n\n"
            "Giải pháp kỹ thuật mang tên 'Context Firewall' (Tường Lửa Ngữ Cảnh):\n"
            "- Tách biệt hoàn toàn bộ nhớ của từng tác vụ.\n"
            "- Chỉ chuyển giao tóm tắt 10–15 dòng giữa các agent.\n"
            "- Lưu trữ dữ liệu nặng vào Database SQLite nội bộ thay vì nhồi vào context window.\n\n"
            "👉 Bình luận từ khóa \"FIREWALL\" để xem chi tiết kiến trúc triển khai ở comment đầu nhé!\n\n"
            "#AIPlayers #ContextFirewall #TokenOptimization #AIArchitecture #TechTips"
        ),
        "comment": (
            "🎯 [BÌNH LUẬN GHIM - TÀI LIỆU CONTEXT FIREWALL]\n\n"
            "Sơ đồ và bài viết chi tiết từ khóa \"FIREWALL\" đã có tại:\n"
            "🔗 Nhóm Zalo AI Players: https://zalo.me/g/etllok798 (Mã mở khóa: AIPLAYERS2026)\n\n"
            "❓ Bạn có gặp tình trạng AI càng nói chuyện lâu càng quên mất yêu cầu gốc ban đầu không?"
        ),
    },
    {
        "id": "fresh_04",
        "action": "SCHEDULE",
        "slot_time": "2026-10-26 18:45",
        "title": "Sơ Đồ Bắn Báo Cáo Doanh Thu Từ SQLite Về Telegram Cực Đơn Giản",
        "archetype": "Layout #3: Isometric Pipeline",
        "cta_kw": "TELEGRAMHUB",
        "items": [
            ("01", "Không cần máy chủ đắt tiền: Chạy script Python nhẹ tênh trên máy cá nhân."),
            ("02", "Tự động kích hoạt đúng 09:00 sáng và 21:30 tối mỗi ngày."),
            ("03", "Trực quan hóa số liệu trực tiếp thành biểu đồ và bảng tóm tắt trên điện thoại."),
        ],
        "caption": (
            "Đi uống cà phê hay đang trên đường vẫn nắm trọn vẹn số liệu vận hành của cả hệ thống "
            "chỉ với một chiếc điện thoại và ứng dụng Telegram quen thuộc! 📱\n\n"
            "Quy trình tự động hóa 3 bước không tốn 1 xu chi phí duy trì:\n"
            "1. Script Python nội bộ tự quét dữ liệu từ SQLite local lúc 09h00 sáng.\n"
            "2. Định dạng lại các chỉ số cốt lõi (Số đơn, Lượt xem, Tương tác).\n"
            "3. Bắn tin nhắn tóm tắt kèm nút bấm hành động về kênh Telegram bảo mật của riêng bạn.\n\n"
            "👉 Bình luận \"TELEGRAMHUB\" để nhận code mẫu Python kết nối Telegram Bot ở bình luận đầu tiên nhé!\n\n"
            "#AIPlayers #TelegramBot #PythonAutomation #BaoCaoTuDong #TietKiemThoiGian"
        ),
        "comment": (
            "🎯 [BÌNH LUẬN GHIM - CODE MẪU TELEGRAM BOT]\n\n"
            "Source code Python kết nối Telegram cho từ khóa \"TELEGRAMHUB\" đã được chia sẻ tại:\n"
            "🔗 Nhóm Zalo AI Players: https://zalo.me/g/etllok798 (Mã truy cập: AIPLAYERS2026)\n\n"
            "❓ Hiện tại mỗi sáng bạn đang theo dõi báo cáo công việc qua email, Excel hay dashboard nào?"
        ),
    },
    {
        "id": "fresh_05",
        "action": "SCHEDULE",
        "slot_time": "2026-10-26 20:45",
        "title": "Khảo Sát Thực Tế: Tuần Qua Bạn Dùng AI Tiết Kiệm Được Bao Nhiêu Giờ?",
        "archetype": "Layout #6: Bento Grid 4 Ô",
        "cta_kw": "GIO",
        "items": [
            ("A", "Dưới 2 giờ: Chủ yếu mới dùng để dịch thuật và tóm tắt văn bản ngắn."),
            ("B", "2 - 5 giờ: Bắt đầu dùng AI viết email, phác thảo nội dung và hỗ trợ tìm kiếm."),
            ("C", "5 - 10 giờ: Đã đóng gói được 1-2 quy trình tự động hóa công việc văn phòng."),
            ("D", "Trên 10 giờ: Có cả hệ thống Subagent tự vận hành, giải phóng hoàn toàn thời gian."),
        ],
        "caption": (
            "Một tuần mới lại bắt đầu! Nhìn lại 7 ngày vừa qua, công nghệ AI đã thực sự giúp ích "
            "được gì cho công việc và cuộc sống của bạn? 📊\n\n"
            "Hãy để lại bình luận mức độ hiện tại của bạn:\n"
            "A. Dưới 2 giờ / tuần\n"
            "B. 2 đến 5 giờ / tuần\n"
            "C. 5 đến 10 giờ / tuần\n"
            "D. Trên 10 giờ / tuần (Đã có hệ thống tự động hóa)\n\n"
            "👉 Bình luận \"GIO\" hoặc chữ cái A/B/C/D để nhận lộ trình nâng cấp từ người hỏi đáp sang kiến trúc sư AI nhé!\n\n"
            "#AIPlayers #KhaoSatCongDong #HieuSuatLamViec #AIProductivity #TuDongHoa"
        ),
        "comment": (
            "🎯 [BÌNH LUẬN GHIM - LỘ TRÌNH TỐI ƯU THỜI GIAN VỚI AI]\n\n"
            "Cảm ơn bạn đã tham gia khảo sát! Tài liệu lộ trình giải phóng thời gian bằng AI từ khóa \"GIO\":\n"
            "🔗 Nhóm Zalo AI Players: https://zalo.me/g/etllok798 (Passcode: AIPLAYERS2026)\n\n"
            "❓ Khó khăn lớn nhất khiến bạn chưa tiết kiệm được nhiều thời gian hơn là do thiếu công cụ hay chưa rõ quy trình?"
        ),
    },
]


def main():
    print("=" * 70)
    print("🚀 BẮT ĐẦU TRIỂN KHAI 5 BÀI ẢNH ĐỘC BẢN 100% MỚI CHO HÔM NAY (26/10)")
    print("=" * 70)

    token = get_token()
    if not token:
        print("❌ Không tìm thấy Token!")
        return

    now_ts = int(time.time())

    for p in FRESH_PACK:
        pid = p["id"]
        title = p["title"]
        cta = p["cta_kw"]
        arch = p["archetype"]
        items = p["items"]
        action = p["action"]

        img_file = IMAGES_DIR / f"today_fresh_{pid}_{cta.lower()}.jpg"
        print(f"\n🎨 Đang render ảnh mới: {title}...")
        render_card(img_file, title, cta, arch, items)
        print(f"  ✅ Đã lưu ảnh: {img_file.name} ({round(img_file.stat().st_size/1024, 1)} KB)")

        if action == "LIVE_NOW":
            print(f"  🚀 ĐĂNG LIVE NGAY lên Facebook Page AI Players...")
            res = post_or_schedule(token, img_file, p["caption"], sched_ts=None)
            post_id = res.get("id") or res.get("post_id")
            print(f"  🎉 KẾT QUẢ ĐĂNG LIVE: {post_id}")
            if post_id:
                time.sleep(2)
                cmt_res = post_comment(token, post_id, p["comment"])
                print(f"  📌 KẾT QUẢ GHIM BÌNH LUẬN #1: {cmt_res.get('id')}")
        else:
            slot_str = p["slot_time"]
            target_dt = dt.datetime.strptime(slot_str, "%Y-%m-%d %H:%M").replace(tzinfo=VN_TZ)
            sched_ts = int(target_dt.timestamp())
            print(f"  📅 LÊN LỊCH HẸN GIỜ ({slot_str})...")
            res = post_or_schedule(token, img_file, p["caption"], sched_ts=sched_ts)
            print(f"  🎉 KẾT QUẢ HẸN GIỜ: {res.get('id')}")
        time.sleep(2)

    print("\n🏁 HOÀN TẤT TRIỂN KHAI 5 BÀI ĐỘC BẢN CHO HÔM NAY!")


if __name__ == "__main__":
    main()
