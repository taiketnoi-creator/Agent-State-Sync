#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_and_schedule_6_subagent_golden_video_slides.py
Kết xuất và lên lịch 6 Video Slide Chuẩn 5 Quy Tắc Vàng (`templates/remotion-cuongit-template`)
cho Page `AI Players - Người chơi hệ AI` (`1022527194267367`) ngày 04/11 – 05/11/2026:
- 100% đúng chuẩn Video Slide 5 Quy Tắc Vàng:
  + Nền xanh sáng `BG-video-motion.jpg` + 2 Neon Orbs trôi nổi.
  + Tiêu đề màu `#87ff00` + Khung thẻ kính mờ trong suốt `Transparent Frosted Glass` (`bg-white/[0.08] backdrop-blur-md`).
  + Bố cục Độc bản `Zero-Clone` từng bài & từng cảnh (`verify_zero_clone_tsx()`).
  + Phụ đề 1 dòng trượt từ dưới lên `SubtitleBox` tại `bottom-[380px]` (không khung bao, không icon loa `🎙️`).
  + Nhạc nền `1.The Violins.mp3` (-18dB) + SFX `apple-pay-sound.mp3` & `discord-notification.mp3` + Voiceover Vbee `-3dB`.
- 100% Caption & Pinned Comment #1 gắn chặt với định vị `Hệ Sinh Thái Subagent Cá Nhân & Doanh Nghiệp Toàn Diện — Nhận Xây Dựng Đội Ngũ Subagent Trọn Gói`.
"""

import datetime
import json
import shutil
import ssl
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from zero_repost_gate import (
    record_published_content,
    verify_video_slide_brandkit_compliance,
    verify_zero_clone_tsx,
)
from fix_and_publish_21_reels_now import (
    BUNDLE_DIR,
    NODE_EXE,
    REMOTION_DIR,
    SRC_DIR,
    get_ai_players_credentials,
    parse_vn_schedule_time,
    post_comment_on_video,
    upload_video_to_meta,
)

OUT_DIR = ROOT_DIR / "campaigns" / "2026-11-04" / "ai-players-subagent-agency-vault" / "golden_video_slides"
OUT_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST_PATH = OUT_DIR / "golden_6_video_slides_manifest.json"

ZALO_VIP_URL = "https://zalo.me/g/fzxvbf259"

SIX_GOLDEN_VIDEO_SLIDES = [
    {
        "id": "reel01",
        "comp_id": "Reel01DeepResearch",
        "schedule_vn": "LIVE_NOW",
        "keyword": "DEEPRESEARCH",
        "title": "SUBAGENT NGHIÊN CỨU THỊ TRƯỜNG TỰ ĐỘNG — QUÉT CHÉO 200 BÁO CÁO TRONG 3 PHÚT",
        "caption": (
            "🤖 TRONG ĐỘI NGŨ SUBAGENT CÁ NHÂN & DOANH NGHIỆP CỦA BẠN, AI ĐANG LÀM VIỆC NGHIÊN CỨU THỊ TRƯỜNG?\n\n"
            "Thay vì tự mở 50 tab trình duyệt đọc thủ công suốt cả buổi chiều mà vẫn bỏ sót dữ liệu, hãy giao việc đó cho **Subagent Nghiên Cứu Chuyên Sâu (Deep Research Subagent)** trong Hệ sinh thái Subagent của bạn:\n"
            "✅ Tự động chia câu hỏi lớn thành 10 nhánh quét đồng loạt 200 nguồn báo cáo uy tín.\n"
            "✅ Tự mở vòng truy vấn phụ để kiểm chứng chéo khi phát hiện hai con số mâu thuẫn.\n"
            "✅ Hoàn tất bản báo cáo chiến lược 10 trang kèm biểu đồ & trích dẫn nguồn chỉ trong 3 phút!\n\n"
            "💬 Bạn muốn tự kích hoạt Subagent này hay muốn đội ngũ AI Players thiết kế trọn gói Hệ sinh thái Subagent riêng cho bạn? Xem ngay tại **Bình luận ghim đầu tiên (#1)** hoặc bình luận từ khóa **DEEPRESEARCH** bên dưới nhé! 👇"
        ),
    },
    {
        "id": "reel07",
        "comp_id": "Reel07VoiceToAction",
        "schedule_vn": "2026-11-04 16:30",
        "keyword": "VOICEAGENT",
        "title": "SUBAGENT TRỢ LÝ ĐIỀU HÀNH BẰNG GIỌNG NÓI THỜI GIAN THỰC — RA LỆNH 1 CÂU CHẠY 3 TÁC VỤ",
        "caption": (
            "🎙️ ĐANG DI CHUYỂN NGOÀI ĐƯỜNG VẪN ĐIỀU HÀNH TRỌN VẸN CÔNG VIỆC VỚI SUBAGENT TRỢ LÝ GIỌNG NÓI CÁ NHÂN!\n\n"
            "Một Hệ sinh thái Subagent Cá nhân Toàn diện không bắt bạn phải ngồi trước màn hình máy tính gõ từng dòng lệnh:\n"
            "⚡ Phản hồi tức thì trong 300 mili-giây — nhanh tương đương trò chuyện trực tiếp với thư ký thật.\n"
            "⚡ Chỉ cần nói 1 câu tự nhiên qua điện thoại: Subagent tự động kiểm tra tồn kho, đặt lịch họp đối tác và phát thông báo cho đội nhóm.\n"
            "⚡ Hoàn tất chuỗi 3 tác vụ liên hoàn chỉ trong đúng 5 giây rảnh tay!\n\n"
            "💬 Xem ngay hướng dẫn kết nối & đăng ký Tư vấn xây dựng Đội ngũ Subagent Cá nhân may đo 1:1 tại **Bình luận ghim đầu tiên (#1)** hoặc bình luận **VOICEAGENT** bên dưới! 👇"
        ),
    },
    {
        "id": "reel03",
        "comp_id": "Reel03GraphRagMatrix",
        "schedule_vn": "2026-11-04 20:00",
        "keyword": "GRAPHRAG",
        "title": "SUBAGENT CỐ VẤN ĐỒ THỊ TRI THỨC DOANH NGHIỆP — NỐI KẾT HÀNG NGÀN TÀI LIỆU NỘI BỘ",
        "caption": (
            "🏢 TẠI SAO NẠP HÀNG TRĂM FILE VÀO AI MÀ VẪN KHÔNG TRẢ LỜI ĐƯỢC BỨC TRANH TỔNG THỂ CỦA DOANH NGHIỆP?\n\n"
            "Khi xây dựng **Đội ngũ Subagent Doanh nghiệp Toàn diện**, chúng tôi không dùng kiểu tra cứu cắt vụn tài liệu cũ kỹ, mà trang bị **Subagent Đồ Thị Tri Thức (GraphRAG Architect)**:\n"
            "🔗 Tự động nối kết Nhân sự — Dự án — Đơn hàng — Biên bản họp xuyên suốt hàng ngàn file PDF nội bộ.\n"
            "🔗 Lần theo từng nhánh cầu nối để xâu chuỗi nguyên nhân & hệ quả liên phòng ban.\n"
            "🔗 Biến kho tài liệu tĩnh của công ty bạn thành một Cố vấn Chiến lược thấu hiểu mọi ngóc ngách vận hành 24/7!\n\n"
            "💬 Nhận sơ đồ kiến trúc hoặc Đặt lịch thiết kế Đội ngũ Subagent riêng cho Doanh nghiệp của bạn tại **Bình luận ghim đầu tiên (#1)** (hoặc bình luận **GRAPHRAG**)! 👇"
        ),
    },
    {
        "id": "reel08",
        "comp_id": "Reel08CodeSandboxExec",
        "schedule_vn": "2026-11-05 11:45",
        "keyword": "SANDBOX",
        "title": "SUBAGENT CHUYÊN GIA PHÂN TÍCH SỐ LIỆU & KẾ TOÁN — XỬ LÝ BẢNG 5.000 DÒNG CHUẨN 100%",
        "caption": (
            "📊 ĐỪNG BẮT CHATGPT CỘNG NHẨM EXCEL NỮA — HÃY GIAO CHO SUBAGENT PHÂN TÍCH SỐ LIỆU CHUYÊN BIỆT!\n\n"
            "Mô hình ngôn ngữ thông thường chỉ đoán chữ theo xác suất nên rất dễ lệch số lẻ. Trong **Đội ngũ Subagent Doanh nghiệp & Cá nhân**, nhiệm vụ này do **Subagent Thực Thi Mã (Code Sandbox Analyst)** đảm trách:\n"
            "✅ Tự động viết công thức tính toán chạy trong máy ảo cô lập — chuẩn xác tuyệt đối 100% tới từng con số lẻ.\n"
            "✅ Tự phát hiện và làm sạch các cột ngày tháng, định dạng bị lệch trong bảng 5.000 dòng.\n"
            "✅ Xuất ngay biểu đồ tăng trưởng sắc nét & báo cáo tổng hợp chỉ trong vài giây!\n\n"
            "💬 Lấy bộ câu lệnh & Đặt lịch xây dựng Đội ngũ Subagent may đo trọn gói tại **Bình luận ghim đầu tiên (#1)** hoặc bình luận **SANDBOX** bên dưới! 👇"
        ),
    },
    {
        "id": "reel09",
        "comp_id": "Reel09SelfHealingWorkflow",
        "schedule_vn": "2026-11-05 16:30",
        "keyword": "SELFHEAL",
        "title": "ĐỘI NGŨ SUBAGENT TỰ CHỮA LÀNH — VẬN HÀNH XUYÊN ĐÊM 99.9% KHÔNG BAO GIỜ ĐỨNG HÌNH",
        "caption": (
            "🛡️ HẸN ĐỘI NGŨ SUBAGENT CHẠY VIỆC LÚC 2 GIỜ SÁNG, LỠ NGHẼN MẠNG THÌ SAO?\n\n"
            "Sự khác biệt giữa một kịch bản nghiệp dư và một **Hệ sinh thái Subagent Doanh nghiệp Toàn diện** do AI Players xây dựng nằm ở **Cơ chế Tự Chữa Lành 2 Lớp (Self-Healing Architecture)**:\n"
            "🔄 Lớp giáp 1: Tự động đợi 3 giây và thử lại thông minh theo cấp số nhân khi máy chủ quốc tế chập chờn.\n"
            "⚡ Lớp giáp 2: Cầu dao chuyển mạch tự động bẻ lái sang cổng mô hình dự phòng trong 1 giây nếu cổng chính quá tải.\n"
            "🌙 Giúp bạn ngủ ngon giấc mỗi đêm, 6 giờ sáng thức dậy toàn bộ khối lượng công việc đã bàn giao chuẩn 100%!\n\n"
            "💬 Xem chi tiết dịch vụ Xây dựng Đội ngũ Subagent Trọn gói & Nhận bản vẽ mẫu tại **Bình luận ghim đầu tiên (#1)** (hoặc bình luận **SELFHEAL**)! 👇"
        ),
    },
    {
        "id": "reel17",
        "comp_id": "Reel17CustomerIntentRouter",
        "schedule_vn": "2026-11-05 20:00",
        "keyword": "ROUTER",
        "title": "SUBAGENT LỄ TÂN ĐỊNH TUYẾN HỘP THƯ 0.5 GIÂY — PHÂN LUỒNG CHỐT ĐƠN & CHĂM SÓC KHÁCH HÀNG",
        "caption": (
            "💬 KHÁCH ĐANG KHIẾU NẠI ĐƠN HÀNG MÀ CHATBOT CŨ LẠI CHÀO MỜI MUA THÊM? ĐÓ LÀ VÌ BẠN THIẾU SUBAGENT ĐIỀU PHỐI!\n\n"
            "Trong **Đội ngũ Subagent Doanh nghiệp & Chủ Shop**, không bao giờ có chuyện 1 kịch bản ôm đồm mọi tin nhắn. Ngay ở cửa ngõ hộp thư là **Subagent Lễ Tân Định Tuyến (Intent Router Subagent)**:\n"
            "🎯 Đọc vị ý định và cảm xúc của khách hàng chỉ trong 0.5 giây.\n"
            "🛒 Khách hỏi giá -> Chuyển ngay cho **Subagent Tư Vấn Chốt Đơn** gửi ảnh thật & lên đơn.\n"
            "📦 Khách hỏi hàng -> Chuyển cho **Subagent Tra Cứu Vận Đơn** báo giờ giao.\n"
            "🚨 Khách bức xúc -> Lập tức ngắt bot và bắn cảnh báo khẩn cấp về điện thoại quản lý!\n\n"
            "💬 Đăng ký thiết kế Đội ngũ Subagent Bán hàng & CSKH tự động tại **Bình luận ghim đầu tiên (#1)** hoặc bình luận **ROUTER** ngay bên dưới! 👇"
        ),
    },
]


def build_pinned_comment(keyword: str) -> str:
    return (
        f"🚀 [ĐẶT LỊCH XÂY DỰNG ĐỘI NGŨ SUBAGENT CÁ NHÂN & DOANH NGHIỆP TRỌN GÓI — MÃ: {keyword}]\n"
        f"Bạn muốn sở hữu trọn bộ Hệ sinh thái Subagent tự động hóa nghiên cứu, vận hành, phân tích số liệu và chăm sóc khách hàng 24/7?\n\n"
        f"1️⃣ ĐẶT LỊCH TƯ VẤN & THIẾT KẾ ĐỘI NGŨ SUBAGENT MAY ĐO 1:1 (CÁ NHÂN / DOANH NGHIỆP):\n"
        f"👉 Nhắn trực tiếp vào Fanpage hoặc bấm vào Nhóm Zalo VIP bên dưới để đội ngũ Kiến trúc sư AI Players khảo sát quy trình & dựng hệ thống trọn gói cho bạn.\n\n"
        f"2️⃣ NHẬN MIỄN PHÍ BỘ KHUNG MẪU & SƠ ĐỒ KIẾN TRÚC SUBAGENT (MÃ: {keyword}):\n"
        f"🔗 Tham gia Nhóm Zalo Cộng Đồng VIP tại đây: {ZALO_VIP_URL}\n"
        f"💡 Vào nhóm bấm lên Tin nhắn ghim trên cùng để tải ngay bộ tài liệu & đặt lịch tư vấn 1:1 nhé!"
    )


def main():
    render_only = "--render-only" in sys.argv

    ok_zc, msg_zc = verify_zero_clone_tsx(SRC_DIR)
    if not ok_zc:
        print(f"❌ DỪNG KHẨN CẤP [Zero-Clone Gate]: {msg_zc}", flush=True)
        sys.exit(1)
    print(f"🛡️ {msg_zc}", flush=True)

    cli_js = str(REMOTION_DIR / "node_modules" / "@remotion" / "cli" / "remotion-cli.js")
    page_id, page_token, page_name = get_ai_players_credentials()
    print(f"🔑 Đã kết nối Fanpage: {page_name} ({page_id})", flush=True)

    results = []
    for idx, item in enumerate(SIX_GOLDEN_VIDEO_SLIDES, 1):
        rid = item["id"]
        comp_id = item["comp_id"]
        kw = item["keyword"]
        mp4_path = OUT_DIR / f"golden_slide_{idx:02d}_{rid}_{comp_id}.mp4"

        if not mp4_path.is_file() or mp4_path.stat().st_size < 1_000_000:
            t0 = time.time()
            print(f"\n🎬 [{idx}/6] Đang render Video Slide chuẩn 5 Quy Tắc Vàng `{comp_id}` -> {mp4_path.name} ...", flush=True)
            proc = subprocess.run(
                [
                    NODE_EXE,
                    cli_js,
                    "render",
                    str(BUNDLE_DIR),
                    comp_id,
                    str(mp4_path),
                    "--concurrency=2",
                    "--crf=23",
                    "--overwrite",
                ],
                cwd=str(REMOTION_DIR),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
            )
            elapsed = round(time.time() - t0, 1)
            if proc.returncode != 0 or not mp4_path.is_file():
                print(f"❌ [{rid}] Lỗi render `{comp_id}`:\n{(proc.stderr or proc.stdout)[-800:]}", flush=True)
                sys.exit(1)
            mb = round(mp4_path.stat().st_size / (1024 * 1024), 2)
            print(f"✅ [{idx}/6] Render hoàn tất `{comp_id}` trong {elapsed}s ({mb} MB)", flush=True)
        else:
            mb = round(mp4_path.stat().st_size / (1024 * 1024), 2)
            print(f"⏩ [{idx}/6] Đã có sẵn MP4 chuẩn ({mb} MB): {mp4_path.name}", flush=True)

        # Kiểm định chuẩn 5 Quy Tắc Vàng Video Slide (Brand-Kit Gate)
        ok_brand, msg_brand = verify_video_slide_brandkit_compliance(mp4_path)
        if not ok_brand:
            print(f"❌ DỪNG KHẨN CẤP: {msg_brand}", flush=True)
            sys.exit(1)
        print(f"  🛡️ {msg_brand}", flush=True)

        if render_only:
            continue

        pinned_text = build_pinned_comment(kw)
        if item["schedule_vn"] == "LIVE_NOW":
            print(f"🚀 [{idx}/6] Đang đăng LIVE Video Slide `{comp_id}` bù ca trưa 04/11...", flush=True)
            up = upload_video_to_meta(page_id, page_token, mp4_path, item["title"], item["caption"], published=True)
            mode_status = "LIVE_PUBLISHED"
        else:
            sched_ts = parse_vn_schedule_time(item["schedule_vn"])
            print(f"☁️ [{idx}/6] Đang tải lên & hẹn giờ `{comp_id}` ({item['schedule_vn']})...", flush=True)
            up = upload_video_to_meta(page_id, page_token, mp4_path, item["title"], item["caption"], published=False, schedule_ts=sched_ts)
            mode_status = "SCHEDULED"

        if "error" in up:
            print(f"❌ [{rid}] Lỗi upload Meta: {up['error']}", flush=True)
            continue

        vid = up["video_id"]
        pid = up["post_id"]
        cmt = post_comment_on_video(page_id, vid, pid, page_token, pinned_text)
        cmt_id = cmt.get("id", "")
        record_published_content(page_id, mp4_path, item["caption"], post_id=str(pid or vid))

        rec = {
            **item,
            "mp4_path": str(mp4_path),
            "fb_video_id": vid,
            "fb_post_id": pid,
            "fb_comment_id": cmt_id,
            "status": mode_status,
        }
        results.append(rec)
        MANIFEST_PATH.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ [{idx}/6] Hoàn tất {mode_status} ({item['schedule_vn']}) | video_id={vid} | comment_id={cmt_id}", flush=True)

    print(f"\n🎉 HOÀN TẤT {len(results)}/6 VIDEO SLIDE CHUẨN 5 QUY TẮC VÀNG TRÊN PAGE AI PLAYERS!", flush=True)


if __name__ == "__main__":
    main()
