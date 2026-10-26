#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
schedule_ai_players_queue.py — Nạp Kho Bài Hẹn Giờ (Scheduled Queue) Chuẩn Vàng Cho Fanpage AI Players.

Lên lịch cho 2 ngày tới (26/10 và 27/10/2026):
1. Hôm nay 26/10:
   - 11:45: Video Reel (OpenRouter Mindmap Explainer 9:16)
   - 16:30: Ảnh Vuông 1:1 (Lead Magnet PROMPT50 - 50 Prompt Thực Chiến)
   - 20:00: Video Reel (MCP Remotion Explainer Chuẩn Vàng 9:16)
2. Ngày mai 27/10:
   - 11:45: Ảnh Vuông 1:1 (Lead Magnet HETHONG - Sơ Đồ Subagent Đóng Hộp)
   - 16:30: Ảnh Vuông 1:1 (Review GitHub Hot Repo - Browser-Use)
   - 20:00: Video Reel (AI Hallucination Remotion Explainer Chuẩn Vàng 9:16)
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

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
VAULT_PATH = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / "pages_vault.json"
REPORTS_DIR = SUBAGENT_DIR / "campaigns" / "daily-reports"
VN_TZ = dt.timezone(dt.timedelta(hours=7))

AI_PAGE_ID = "1022527194267367"
GRAPH_VERSION = "v22.0"


def get_token() -> str:
    if not VAULT_PATH.exists():
        return ""
    data = json.loads(VAULT_PATH.read_text(encoding="utf-8", errors="ignore"))
    for p in data.get("pages", []):
        if str(p.get("id")) == AI_PAGE_ID:
            return p.get("access_token", "")
    return ""


def graph_get(endpoint: str, token: str) -> dict:
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{endpoint}&access_token={urllib.parse.quote(token)}" if "?" in endpoint else f"https://graph.facebook.com/{GRAPH_VERSION}/{endpoint}?access_token={urllib.parse.quote(token)}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8", errors="ignore"))


def schedule_photo(page_id: str, token: str, img_path: Path, caption: str, sched_ts: int) -> dict:
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{page_id}/photos"
    boundary = f"----AgentJavisBoundary{uuid.uuid4().hex}"
    body = bytearray()

    def add_field(name: str, value: str):
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{value}\r\n".encode("utf-8"))

    add_field("access_token", token)
    add_field("message", caption)
    add_field("published", "false")
    add_field("scheduled_publish_time", str(sched_ts))

    mime_type = mimetypes.guess_type(str(img_path))[0] or "image/jpeg"
    file_bytes = img_path.read_bytes()

    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(
        f'Content-Disposition: form-data; name="source"; filename="{img_path.name}"\r\n'.encode("utf-8")
    )
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    body.extend(file_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8", errors="ignore"))


def schedule_video_reel(page_id: str, token: str, video_path: Path, title: str, description: str, sched_ts: int) -> dict:
    # 1. Start Phase
    start_url = f"https://graph.facebook.com/{GRAPH_VERSION}/{page_id}/video_reels"
    start_data = json.dumps({"upload_phase": "start", "access_token": token}).encode("utf-8")
    req_start = urllib.request.Request(
        start_url,
        data=start_data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req_start, timeout=30) as resp:
        start_res = json.loads(resp.read().decode("utf-8", errors="ignore"))

    video_id = start_res.get("video_id")
    upload_url = start_res.get("upload_url")
    if not video_id or not upload_url:
        raise RuntimeError(f"Lỗi khởi tạo upload video reel: {start_res}")

    # 2. Upload Phase
    video_bytes = video_path.read_bytes()
    req_upload = urllib.request.Request(
        upload_url,
        data=video_bytes,
        headers={
            "Authorization": f"OAuth {token}",
            "offset": "0",
            "file_size": str(len(video_bytes)),
            "Content-Type": "application/octet-stream",
        },
        method="POST",
    )
    with urllib.request.urlopen(req_upload, timeout=180) as resp:
        json.loads(resp.read().decode("utf-8", errors="ignore"))

    # 3. Finish Phase (Schedule)
    finish_params = {
        "access_token": token,
        "video_id": video_id,
        "upload_phase": "finish",
        "description": description,
        "title": title,
        "video_state": "SCHEDULED",
        "scheduled_publish_time": str(sched_ts),
    }
    finish_data = urllib.parse.urlencode(finish_params).encode("utf-8")
    req_finish = urllib.request.Request(start_url, data=finish_data, method="POST")
    with urllib.request.urlopen(req_finish, timeout=60) as resp:
        finish_res = json.loads(resp.read().decode("utf-8", errors="ignore"))

    return {
        "success": True,
        "video_id": video_id,
        "post_id": finish_res.get("post_id", video_id),
        "finish_res": finish_res,
    }


POSTS_TO_SCHEDULE = [
    {
        "id": "ai_video_openrouter_261145",
        "type": "video",
        "slot_vn": "2026-10-26 11:45",
        "file": SUBAGENT_DIR / "campaigns/2026-10-24/openrouter-mindmap-test/openrouter_mindmap_explainer.mp4",
        "title": "OpenRouter: 1 API Kết Nối Toàn Bộ Claude 3.5, GPT-4o & Gemini",
        "caption": (
            "Thay vì phải mua 5 tài khoản AI riêng biệt và chuyển qua lại giữa các tab, "
            "đây là cách các kỹ sư AI kết nối toàn bộ Claude 3.5 Sonnet, GPT-4o và Gemini qua đúng 1 API duy nhất! 🚀\n\n"
            "📌 OpenRouter giải quyết triệt để 3 vấn đề lớn:\n"
            "1. Đa dạng mô hình: Đổi model chỉ bằng 1 dòng code cấu hình.\n"
            "2. Tiết kiệm chi phí: Chỉ trả tiền theo token thực tế sử dụng, nạp $5 dùng cả tháng.\n"
            "3. Không lo nghẽn mạng: Tự động fallback sang server dự phòng khi một bên quá tải.\n\n"
            "👉 Xem sơ đồ chi tiết và nhận template code kết nối ngay ở bình luận đầu tiên nhé!\n"
            "#AIPlayers #OpenRouter #AIAgent #Python #Automation #TechTips #LapTrinh"
        ),
        "pinned_cmt": (
            "📌 SƠ ĐỒ KIẾN TRÚC OPENROUTER & TEMPLATE CODE KẾT NỐI ĐA MODEL:\n"
            "Anh em quan tâm cách thiết lập chi tiết, bình luận \"OPENROUTER\" bên dưới, "
            "mình gửi link Google Drive tài liệu và code mẫu Python/Node.js chạy ngay nhé! 👇"
        ),
    },
    {
        "id": "ai_photo_prompt50_261630",
        "type": "photo",
        "slot_vn": "2026-10-26 16:30",
        "file": SUBAGENT_DIR / "campaigns/2026-10-20/today-launch/images/ai-square-01-lead-prompt50.jpg",
        "caption": (
            "Nhiều người dùng ChatGPT suốt 1 năm qua vẫn chỉ dừng lại ở mức \"viết lại đoạn văn này cho hay hơn\" hoặc \"tóm tắt bài viết này giúp tôi\".\n\n"
            "Nhưng với dân Lập trình & Tự động hóa, một bộ Prompt chuẩn cấu trúc có thể biến AI thành trợ lý đắc lực: Tự debug code, tự sinh API schema, tự viết test cases và tối ưu hóa truy vấn SQL trong vài giây.\n\n"
            "Tổng hợp 50 cấu trúc Prompt thực chiến nhất 2026 chia theo 5 nhóm:\n"
            "1. System Prompt cho Subagent tự hành.\n"
            "2. Prompt phân tích & refactor mã nguồn.\n"
            "3. Prompt thiết kế luồng n8n & Webhook.\n"
            "4. Prompt tối ưu token & chống ảo giác.\n"
            "5. Prompt trích xuất dữ liệu có cấu trúc JSON.\n\n"
            "👉 Tặng miễn phí trọn bộ tài liệu, xem ngay ở bình luận đầu tiên nhé!\n"
            "#AIPlayers #PromptEngineering #Subagent #ChatGPT #Claude #Automation"
        ),
        "pinned_cmt": (
            "🎁 TẶNG MIỄN PHÍ TRỌN BỘ 50 PROMPT THỰC CHIẾN 2026:\n"
            "Bình luận \"PROMPT50\" bên dưới bài viết này, Mama sẽ gửi link tải trực tiếp trọn bộ tài liệu cho bạn ngay nhé! 👇"
        ),
    },
    {
        "id": "ai_video_mcp_262000",
        "type": "video",
        "slot_vn": "2026-10-26 20:00",
        "file": SUBAGENT_DIR / "campaigns/2026-10-20/mcp-ai-explainer-40s/mcp-ai-explainer-40s.mp4",
        "title": "Model Context Protocol (MCP) Là Gì? Cuộc Cách Mạng Kết Nối AI Agent",
        "caption": (
            "Tại sao các tập đoàn công nghệ hàng đầu thế giới đang đồng loạt chuyển sang chuẩn MCP (Model Context Protocol) của Anthropic? ⚡\n\n"
            "Nếu trước đây mỗi lần muốn AI đọc dữ liệu từ Database, GitHub hay Chrome bạn phải viết code kết nối riêng lẻ cực kỳ phức tạp... "
            "Thì giờ đây MCP biến mọi công cụ thành cổng \"USB-C\" chuẩn hóa cho AI!\n\n"
            "AI Agent chỉ cần cắm vào là tự hiểu schema, tự truy vấn dữ liệu và tự thao tác một cách an toàn tuyệt đối.\n\n"
            "👉 Xem giải mã chi tiết và nhận tài liệu MCP tiếng Việt ở bình luận đầu tiên!\n"
            "#AIPlayers #ModelContextProtocol #MCP #Anthropic #AIAgent #CongNghe"
        ),
        "pinned_cmt": (
            "📌 TRỌN BỘ HƯỚNG DẪN MCP TIẾNG VIỆT & TEMPLATE TỰ HÀNH:\n"
            "Bình luận \"MCP\" bên dưới để nhận tài liệu giải phẫu MCP chi tiết kèm bộ khung cài đặt MCP Server cho máy tính nhé! 👇"
        ),
    },
    {
        "id": "ai_photo_hethong_271145",
        "type": "photo",
        "slot_vn": "2026-10-27 11:45",
        "file": SUBAGENT_DIR / "campaigns/2026-10-20/today-launch/images/ai-square-05-lead-hethong.jpg",
        "caption": (
            "Sự khác biệt lớn nhất giữa một \"Chatbot trả lời câu hỏi\" và một \"Hệ thống Subagent tự hành\":\n\n"
            "- Chatbot: Bạn hỏi 1 câu, nó trả lời 1 câu. Bạn phải tự copy kết quả, tự dán sang công cụ khác, tự kiểm tra lỗi và tự chạy tiếp.\n"
            "- Subagent: Bạn giao mục tiêu lớn, Subagent tự lập kế hoạch, chia việc cho các agent chuyên môn, tự chạy kiểm thử và chỉ báo cáo khi đã xong việc!\n\n"
            "Hôm nay mình chia sẻ sơ đồ kiến trúc Đội 10 Subagent vận hành thực chiến:\n"
            "- Mama: Tổng quản điều phối.\n"
            "- MKT & Content: Nghiên cứu thị trường & sáng tạo kịch bản.\n"
            "- Edit & Voice: Tự động kết xuất video, ảnh & giọng đọc.\n"
            "- Chăm sóc kênh & Phân tích: Giữ tương tác & đo lường hiệu quả.\n\n"
            "👉 Nhận sơ đồ kiến trúc Subagent đóng hộp ở bình luận đầu tiên!\n"
            "#AIPlayers #Subagent #AutonomousAI #AiAgent #KienTrucAI #HeThongTuDong"
        ),
        "pinned_cmt": (
            "🎁 TẶNG SƠ ĐỒ KIẾN TRÚC SUBAGENT ĐÓNG HỘP 2026:\n"
            "Bình luận \"HETHONG\" bên dưới, Mama sẽ gửi sơ đồ Mindmap chi tiết và hướng dẫn phân vai cho từng agent nhé! 👇"
        ),
    },
    {
        "id": "ai_photo_browseruse_271630",
        "type": "photo",
        "slot_vn": "2026-10-27 16:30",
        "file": SUBAGENT_DIR / "campaigns/2026-10-20/today-launch/images/ai-square-02-github-browser-use.jpg",
        "caption": (
            "Khám phá thư viện mã nguồn mở đang làm mưa làm gió trên GitHub: Browser-Use! 🌐\n\n"
            "Thay vì phải ngồi bấm chuột cào dữ liệu hay kiểm tra giá sản phẩm thủ công, "
            "Browser-Use cho phép mô hình ngôn ngữ lớn (LLM) nhìn trực tiếp giao diện website, nhận diện nút bấm, nhập form và thực hiện toàn bộ tác vụ trên trình duyệt như một người thật.\n\n"
            "3 ứng dụng cực mạnh có thể triển khai ngay:\n"
            "1. Tự động hóa đăng nhập & kiểm tra báo cáo định kỳ.\n"
            "2. Trích xuất dữ liệu đối thủ và so sánh giá thị trường.\n"
            "3. Test giao diện người dùng (E2E Testing) tự động không cần viết script Selenium phức tạp.\n\n"
            "👉 Link GitHub Repo và code mẫu cài đặt ở bình luận đầu tiên nhé!\n"
            "#AIPlayers #BrowserUse #GitHub #OpenSource #WebScraping #Automation"
        ),
        "pinned_cmt": (
            "📌 LINK GITHUB REPO & BỘ CODE MẪU BROWSER-USE:\n"
            "Bình luận \"REPO\" bên dưới để nhận link GitHub chính thức kèm file notebook chạy thử ngay trên máy nhé! 👇"
        ),
    },
    {
        "id": "ai_video_hallucination_272000",
        "type": "video",
        "slot_vn": "2026-10-27 20:00",
        "file": SUBAGENT_DIR / "campaigns/2026-10-20/ai-hallucination-45s/ai-hallucination-45s.mp4",
        "title": "3 Kỹ Thuật Triệt Tiêu Ảo Giác AI (AI Hallucination)",
        "caption": (
            "Nỗi sợ lớn nhất khi ứng dụng AI vào công việc thực tế là gì? Chính là \"Ảo giác AI\" (AI Hallucination) — khi AI tự tin bịa ra số liệu, đường dẫn hoặc thông tin không có thật! 🛑\n\n"
            "3 kỹ thuật thực chiến giúp bạn kiểm soát và dập tắt hoàn toàn lỗi bịa chuyện:\n"
            "1. RAG (Retrieval-Augmented Generation): Khóa cứng nguồn tài liệu thực tế, cấm suy diễn ngoài phạm vi.\n"
            "2. Structured Output Enforcement: Ép kiểu dữ liệu JSON Schema chặt chẽ, kiểm tra cú pháp tự động bằng Pydantic.\n"
            "3. Multi-Agent Verification: Một agent thực hiện, một agent độc lập kiểm tra chéo (Auditor Gate) trước khi xuất kết quả.\n\n"
            "👉 Xem tài liệu chi tiết ở bình luận đầu tiên!\n"
            "#AIPlayers #AIHallucination #RAG #MultiAgent #TechEducation #AiForWork"
        ),
        "pinned_cmt": (
            "📌 CẨM NANG TRIỆT TIÊU ẢO GIÁC AI & CODE MẪU VERIFICATION:\n"
            "Bình luận \"BANDO\" bên dưới bài viết này để nhận cẩm nang kỹ thuật chi tiết nhé! 👇"
        ),
    },
]


def main():
    token = get_token()
    if not token:
        print("❌ Không tìm thấy token cho Page AI Players trong pages_vault.json!")
        sys.exit(1)

    now_vn = dt.datetime.now(VN_TZ)
    now_ts = int(time.time())
    print(f"🚀 BẮT ĐẦU NẠP KHO LỊCH HẸN GIỜ CHO PAGE AI PLAYERS (ID: {AI_PAGE_ID})")
    print(f"🕒 Thời gian hiện tại: {now_vn.strftime('%Y-%m-%d %H:%M:%S')} (Giờ VN)")

    # 1. Kiểm tra các bài đã có trong scheduled_posts
    existing_sched_ts = []
    try:
        sp_data = graph_get(f"{AI_PAGE_ID}/scheduled_posts?fields=id,scheduled_publish_time", token).get("data", [])
        existing_sched_ts = [int(sp.get("scheduled_publish_time", 0)) for sp in sp_data]
        print(f"📊 Đã có {len(existing_sched_ts)} bài hẹn giờ trên Graph API.")
    except Exception as e:
        print(f"⚠️ Lỗi đọc scheduled_posts: {e}")

    results = []
    for item in POSTS_TO_SCHEDULE:
        slot_dt = dt.datetime.strptime(item["slot_vn"], "%Y-%m-%d %H:%M").replace(tzinfo=VN_TZ)
        sched_ts = int(slot_dt.timestamp())

        # Kiểm tra nếu khung giờ này đã qua
        if sched_ts < now_ts + 600:
            print(f"⏩ Bỏ qua {item['id']} ({item['slot_vn']}) vì thời gian < 10 phút tính từ hiện tại.")
            continue

        # Kiểm tra nếu khung giờ này đã có bài hẹn giờ
        if any(abs(ts - sched_ts) < 1800 for ts in existing_sched_ts):
            print(f"⏩ Bỏ qua {item['id']} ({item['slot_vn']}) vì đã có bài hẹn giờ gần mốc này.")
            continue

        fpath = Path(item["file"])
        if not fpath.exists():
            print(f"❌ Không tìm thấy file media: {fpath}")
            continue

        print(f"\n⏳ Đang lên lịch [{item['type'].upper()}] slot {item['slot_vn']}...")
        try:
            if item["type"] == "photo":
                res = schedule_photo(AI_PAGE_ID, token, fpath, item["caption"], sched_ts)
                post_id = res.get("post_id") or res.get("id")
                print(f"  ✅ Đã lên lịch PHOTO thành công! Post ID: {post_id}")
                results.append({
                    "id": item["id"],
                    "slot_vn": item["slot_vn"],
                    "type": "photo",
                    "post_id": post_id,
                    "pinned_cmt": item["pinned_cmt"],
                })
            elif item["type"] == "video":
                res = schedule_video_reel(AI_PAGE_ID, token, fpath, item["title"], item["caption"], sched_ts)
                post_id = res.get("post_id") or res.get("video_id")
                print(f"  ✅ Đã lên lịch VIDEO REEL thành công! Post ID: {post_id}")
                results.append({
                    "id": item["id"],
                    "slot_vn": item["slot_vn"],
                    "type": "video",
                    "post_id": post_id,
                    "pinned_cmt": item["pinned_cmt"],
                })
        except Exception as e:
            print(f"  ❌ Lỗi khi lên lịch {item['id']}: {e}")

    # Lưu kết quả manifest
    out_dir = SUBAGENT_DIR / "campaigns" / "2026-10-26"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_file = out_dir / "ai_players_scheduled_queue.json"
    manifest_file.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n🎉 HOÀN TẤT! Đã nạp thành công {len(results)} bài vào hàng đợi hẹn giờ của Page AI Players.")
    print(f"📁 Chi tiết đã ghi tại: {manifest_file}")

    # Xóa cache báo cáo cũ để báo cáo mới nhận diện ngay
    cache_file = REPORTS_DIR / ".metrics_cache.json"
    if cache_file.exists():
        cache_file.unlink()
        print("🧹 Đã làm mới cache báo cáo (.metrics_cache.json).")


if __name__ == "__main__":
    main()
