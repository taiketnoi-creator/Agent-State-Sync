#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
schedule_today_ai_players.py — Nạp Hàng Đợi 7 Bài Chiều & Tối Hôm Nay (26/10) Cho Page AI Players:
Đảm bảo hoàn tất đúng chỉ tiêu 8-9 bài hôm nay (3 Video Reels Remotion Vàng + 6 Bài Ảnh Vuông 1:1).
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
VN_TZ = dt.timezone(dt.timedelta(hours=7))
AI_PAGE_ID = "1022527194267367"
GRAPH_VERSION = "v22.0"


def get_token() -> str:
    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
    for p in vault.get("pages", []):
        if str(p.get("id")) == AI_PAGE_ID:
            return p.get("access_token", "")
    return ""


def schedule_photo(token: str, img_path: Path, caption: str, sched_ts: int) -> dict:
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{AI_PAGE_ID}/photos"
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
    body.extend(f'Content-Disposition: form-data; name="source"; filename="{img_path.name}"\r\n'.encode("utf-8"))
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    body.extend(file_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8", errors="ignore"))


def schedule_video_reel(token: str, video_path: Path, title: str, description: str, sched_ts: int) -> dict:
    start_url = f"https://graph.facebook.com/{GRAPH_VERSION}/{AI_PAGE_ID}/video_reels"
    start_data = json.dumps({"upload_phase": "start", "access_token": token}).encode("utf-8")
    req_start = urllib.request.Request(start_url, data=start_data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req_start, timeout=30) as resp:
        start_res = json.loads(resp.read().decode("utf-8", errors="ignore"))

    video_id = start_res.get("video_id")
    upload_url = start_res.get("upload_url")
    if not video_id or not upload_url:
        raise RuntimeError(f"Lỗi khởi tạo upload: {start_res}")

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

    return {"video_id": video_id, "post_id": finish_res.get("post_id", video_id)}


TODAY_POSTS = [
    {
        "slot": "2026-10-26 15:45",
        "type": "photo",
        "file": SUBAGENT_DIR / "campaigns/2026-10-20/today-launch/images/ai-square-03-github-f5-tts.jpg",
        "caption": (
            "Nhân bản giọng nói tiếng Việt chỉ trong 5 giây với mô hình mã nguồn mở F5-TTS! 🎙️\n\n"
            "Thay vì trả $99/tháng cho các công cụ Voice AI đóng gói sẵn trên đám mây, F5-TTS cho phép bạn chạy trực tiếp trên máy local:\n"
            "- Chỉ cần 3-5 giây âm thanh mẫu là sao chép được âm sắc, ngữ điệu.\n"
            "- Tốc độ sinh giọng cực nhanh (RTF ~0.15), khớp từng nhịp cảm xúc.\n"
            "- 0đ chi phí API, dữ liệu hoàn toàn bảo mật.\n\n"
            "👉 Xem video demo và nhận hướng dẫn cài đặt ở bình luận đầu tiên nhé!\n"
            "#AIPlayers #VoiceAI #F5TTS #OpenSource #TextToSpeech #TTS"
        ),
    },
    {
        "slot": "2026-10-26 16:30",
        "type": "video",
        "file": SUBAGENT_DIR / "campaigns/2026-10-20/mcp-ai-explainer-40s/mcp-ai-explainer-40s.mp4",
        "title": "Model Context Protocol (MCP) Là Gì? Cổng USB-C Cho AI",
        "caption": (
            "Tại sao các tập đoàn công nghệ hàng đầu thế giới đang đồng loạt chuyển sang chuẩn MCP (Model Context Protocol) của Anthropic? ⚡\n\n"
            "Nếu trước đây mỗi lần muốn AI đọc dữ liệu từ Database, GitHub hay Chrome bạn phải viết code kết nối riêng lẻ cực kỳ phức tạp... "
            "Thì giờ đây MCP biến mọi công cụ thành cổng \"USB-C\" chuẩn hóa cho AI!\n\n"
            "AI Agent chỉ cần cắm vào là tự hiểu schema, tự truy vấn dữ liệu và tự thao tác một cách an toàn tuyệt đối.\n\n"
            "👉 Xem giải mã chi tiết và nhận tài liệu MCP tiếng Việt ở bình luận đầu tiên!\n"
            "#AIPlayers #ModelContextProtocol #MCP #Anthropic #AIAgent #CongNghe"
        ),
    },
    {
        "slot": "2026-10-26 17:15",
        "type": "photo",
        "file": SUBAGENT_DIR / "campaigns/2026-10-20/today-launch/images/ai-square-01-lead-prompt50.jpg",
        "caption": (
            "Tặng trọn bộ Sổ tay 50 Siêu Prompt Thực Chiến 2026 cho Dân Văn Phòng & Lập Trình! 📘\n\n"
            "Một bộ Prompt chuẩn cấu trúc có thể biến AI thành trợ lý đắc lực: Tự debug code, tự sinh API schema, tự viết test cases và tối ưu hóa truy vấn SQL trong vài giây.\n\n"
            "Tổng hợp 50 cấu trúc Prompt chia theo 5 nhóm giá trị nhất:\n"
            "1. System Prompt cho Subagent tự hành.\n"
            "2. Prompt phân tích & refactor mã nguồn.\n"
            "3. Prompt thiết kế luồng n8n & Webhook.\n"
            "4. Prompt tối ưu token & chống ảo giác.\n"
            "5. Prompt trích xuất dữ liệu có cấu trúc JSON.\n\n"
            "👉 Nhận trọn bộ Google Drive miễn phí ở bình luận đầu tiên nhé!\n"
            "#AIPlayers #PromptEngineering #Subagent #ChatGPT #Claude #Automation"
        ),
    },
    {
        "slot": "2026-10-26 18:45",
        "type": "photo",
        "file": SUBAGENT_DIR / "campaigns/2026-10-20/today-launch/images/ai-square-04-github-awesome-llm.jpg",
        "caption": (
            "Kho báu hơn 30,000 Stars trên GitHub: Repo awesome-llm-apps tổng hợp mọi thứ về ứng dụng LLM thực chiến! 💎\n\n"
            "Nếu bạn đang tìm kiếm ý tưởng hoặc bộ khung code mẫu để dựng các giải pháp AI cho doanh nghiệp, đây là nơi không thể bỏ qua:\n"
            "- Đầy đủ từ RAG nâng cao, Local LLM, Multi-Agent Teams đến Voice Assistant.\n"
            "- Có sẵn code mẫu Python chạy ngay trong 5 phút.\n\n"
            "👉 Xem đường dẫn repo và tài liệu hướng dẫn ở bình luận đầu tiên!\n"
            "#AIPlayers #AwesomeLLM #GitHub #AIAgents #Python #OpenSource"
        ),
    },
    {
        "slot": "2026-10-26 20:00",
        "type": "video",
        "file": SUBAGENT_DIR / "campaigns/2026-10-20/ai-hallucination-45s/ai-hallucination-45s.mp4",
        "title": "Căn Bệnh Ảo Giác Của Trí Tuệ Nhân Tạo & Cách Khóa Chặt 3 Lớp",
        "caption": (
            "Nỗi sợ lớn nhất khi ứng dụng AI vào công việc thực tế là gì? Chính là \"Ảo giác AI\" (AI Hallucination) — khi AI tự tin bịa ra số liệu, đường dẫn hoặc thông tin không có thật! 🛑\n\n"
            "3 kỹ thuật thực chiến giúp bạn kiểm soát và dập tắt hoàn toàn lỗi bịa chuyện:\n"
            "1. RAG (Retrieval-Augmented Generation): Khóa cứng nguồn tài liệu thực tế, cấm suy diễn ngoài phạm vi.\n"
            "2. Structured Output Enforcement: Ép kiểu dữ liệu JSON Schema chặt chẽ, kiểm tra cú pháp tự động bằng Pydantic.\n"
            "3. Multi-Agent Verification: Một agent thực hiện, một agent độc lập kiểm tra chéo (Auditor Gate) trước khi xuất kết quả.\n\n"
            "👉 Xem tài liệu chi tiết ở bình luận đầu tiên!\n"
            "#AIPlayers #AIHallucination #RAG #MultiAgent #TechEducation #AiForWork"
        ),
    },
    {
        "slot": "2026-10-26 20:45",
        "type": "photo",
        "file": SUBAGENT_DIR / "campaigns/2026-10-20/today-launch/images/ai-square-05-lead-hethong.jpg",
        "caption": (
            "Sơ đồ dây chuyền Đội quân 10 Subagent 24/7 tự hành thay thế một phòng vận hành thủ công! ⚙️\n\n"
            "Thay vì bắt một trợ lý AI ôm đồm tất cả, hãy tách thành các chuyên gia độc lập:\n"
            "- Mama: Tổng quản điều phối.\n"
            "- MKT & Content: Nghiên cứu thị trường & sáng tạo nội dung.\n"
            "- Edit & Voice: Dựng video, kết xuất ảnh & làm chủ giọng đọc.\n"
            "- Chăm sóc & Phân tích: Giữ tương tác & đối soát dữ liệu.\n\n"
            "👉 Nhận sơ đồ Mindmap kiến trúc chi tiết ở bình luận đầu tiên!\n"
            "#AIPlayers #Subagent #AutonomousAI #AiAgent #KienTrucAI #HeThongTuDong"
        ),
    },
    {
        "slot": "2026-10-26 21:45",
        "type": "photo",
        "file": SUBAGENT_DIR / "campaigns/2026-10-20/today-launch/images/ai-square-06-4tasks-grid.jpg",
        "caption": (
            "Khảo sát nhanh: 4 công việc bạn nên giao ngay cho AI tự làm hôm nay để tiết kiệm 2 tiếng mỗi ngày! 📊\n\n"
            "A. Tự động hóa báo cáo số liệu đầu ngày lúc 9h sáng.\n"
            "B. Soạn thảo kịch bản & phân tích nội dung viral đối thủ.\n"
            "C. Kiểm thử code, debug lỗi và viết tài liệu kỹ thuật.\n"
            "D. Lọc dữ liệu khách hàng và tự động phản hồi bình luận.\n\n"
            "Bạn đang cần tự động hóa khâu nào nhất? Bình luận chữ cái A, B, C hoặc D bên dưới nhé! 👇\n"
            "#AIPlayers #KhaoSat #AiForWork #Automation #NangSuat"
        ),
    },
]


def main():
    token = get_token()
    if not token:
        print("❌ Không tìm thấy token cho Page AI Players!")
        sys.exit(1)

    print(f"🚀 BẮT ĐẦU LÊN LỊCH 7 BÀI ĐĂNG CHIỀU & TỐI HÔM NAY CHO PAGE AI PLAYERS")
    now_vn = dt.datetime.now(VN_TZ)
    now_ts = int(time.time())

    for idx, item in enumerate(TODAY_POSTS, 1):
        slot_dt = dt.datetime.strptime(item["slot"], "%Y-%m-%d %H:%M").replace(tzinfo=VN_TZ)
        sched_ts = int(slot_dt.timestamp())

        if sched_ts < now_ts + 600:
            print(f"⏩ Bỏ qua {item['slot']} vì < 10 phút tính từ hiện tại.")
            continue

        fpath = Path(item["file"])
        if not fpath.exists():
            print(f"❌ Không tìm thấy file: {fpath}")
            continue

        print(f"\n⏳ [{idx}/7] Lên lịch {item['type'].upper()} slot {item['slot']}...")
        try:
            if item["type"] == "photo":
                res = schedule_photo(token, fpath, item["caption"], sched_ts)
                pid = res.get("post_id") or res.get("id")
                print(f"  ✅ Đã lên lịch PHOTO thành công! Post ID: {pid}")
            elif item["type"] == "video":
                res = schedule_video_reel(token, fpath, item["title"], item["caption"], sched_ts)
                pid = res.get("post_id") or res.get("video_id")
                print(f"  ✅ Đã lên lịch VIDEO REEL thành công! Post ID: {pid}")
        except Exception as e:
            print(f"  ❌ Lỗi khi lên lịch: {e}")

    print("\n🎉 HOÀN TẤT LÊN LỊCH 7 BÀI CHO CHIỀU VÀ TỐI HÔM NAY!")


if __name__ == "__main__":
    main()
