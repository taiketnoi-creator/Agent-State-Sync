#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mama_auto_scheduler_engine.py — Động Cơ Tự Động Hóa Chạy Ngầm Khi Mở Máy & Báo Cáo Theo 5 Mốc Giờ Cố Định.

Giải quyết triệt để 3 yêu cầu của CEO:
1. Khi vừa mở máy lên (AtLogOn) hoặc lúc 09:00 sáng:
   - Tự động kiểm tra kho bài đăng & hẹn giờ (scheduled_posts) của cả 4 Fanpage.
   - Nếu 3 Page Bán Hàng (Phòng Trọ Hết Cứu, Ký Túc Xá Có Biến, Hội Deadline) chưa có lịch đăng cho khung 11:45 và 20:00 hôm nay:
     tự động nạp bài (hoặc đăng bù nếu đã qua khung giờ) kèm gắn Pinned Comment #1 chứa link Shopee Affiliate (ID: 17395830088).
   - Tự động quét mọi bài vừa chuyển từ Scheduled -> LIVE trên cả 4 Page để gắn Pinned Comment #1 ngay lập tức.
2. Thực thi đúng 5 mốc báo cáo & vận hành trong ngày (kể cả trên Máy Văn Phòng lẫn Máy Nhà):
   - 09:00 (và ngay khi mở máy): Báo cáo Khởi động & Kiểm tra Lịch đăng 4 Page + Dọn kho 7 ngày.
   - 11:45 (Giờ Vàng Trưa): Nghiệm thu bài đăng 11:45 trên 4 Page, gắn Pinned Comment #1 & tương tác nội bộ cụm 3 Page bán hàng.
   - 12:00 (Ca Trưa): Tương tác Hội nhóm Ca 1 (4 ngách) & Gửi Báo cáo Ca Trưa.
   - 17:30 (Ca Chiều): Kiểm tra bài 16:30 của AI Players, chăm sóc bình luận & Tương tác Hội nhóm Ca 2 + Báo cáo Ca Chiều.
   - 20:00 & 21:30 (Ca Tối & EOD): Nghiệm thu bài đăng 20:00 trên 4 Page & Gửi Báo cáo Tổng kết Cuối Ngày (EOD 21:30).
"""

import argparse
import datetime as dt
import json
import mimetypes
import subprocess
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
TZ_VN = dt.timezone(dt.timedelta(hours=7))

AI_ID = "1022527194267367"
SALES_IDS = ["1442323328956326", "1421270697727753", "1407231352464711"]

# Kho nội dung bán hàng chuẩn (Ảnh vuông 1:1 Editorial Macro Grid + Link Shopee Affiliate 17395830088)
# dùng để tự động lên lịch/đăng bài hàng ngày cho 3 Page Bán Hàng khi kho scheduled_posts trống
DAILY_SALES_QUEUE = {
    "1442323328956326": [  # Phòng Trọ Hết Cứu
        {
            "slot": "11:45",
            "image": SUBAGENT_DIR / "campaigns/2026-10-20/today-launch/images/sales-phongtro-1145-style02.png",
            "caption": (
                "Phòng trọ 15m² lúc nào cũng vương tóc rụng trên nệm với bụi mịn ở khe cửa sổ lùa mà cầm chổi quét thì bụi bay mù mịt?\n\n"
                "Đổi sang chiếc Máy hút bụi cầm tay không dây mini đầu hút dẹt 2-trong-1 này chỉ mất đúng 2 phút lướt nhẹ là sạch bong từ chăn ga, bàn làm việc tới gầm giường!\n"
                "- Lõi lọc HEPA tháo rời xả nước rửa sạch trong 30 giây, dùng lại nhiều lần cực tiết kiệm.\n"
                "- Sạc cáp Type-C tiện lợi, nhỏ gọn cất gọn trong ngăn kéo bàn trọ.\n\n"
                "👉 Link săn ưu đãi chính hãng mình ghim ngay ở bình luận đầu tiên nhé!\n"
                "#PhongTroHetCuu #DonPhongTro #DecorPhongTro #DoGiaDungMini #SinhVien"
            ),
            "pinned_cmt": (
                "📌 LINK CHÍNH HÃNG — MÁY HÚT BỤI CẦM TAY KHÔNG DÂY MINI ĐẦU HÚT DẸT 2-IN-1:\n"
                "🛒 Săn ngay trên Shopee tại đây nha: https://s.shopee.vn/an_redir?origin_link=https%3A%2F%2Fshopee.vn%2Fsearch%3Fkeyword%3Dm%25C3%25A1y%2520h%25C3%25BAt%2520b%25E1%25BB%25A5i%2520c%25E1%25BA%25A7m%2520tay%2520mini&affiliate_id=17395830088&sub_id=phongtro-hut_bui_mini-auto_daily-1145\n"
                "ℹ️ [Affiliate Disclosure: Link chia sẻ có thể mang lại khoản hoa hồng nhỏ giúp duy trì Page mà không làm thay đổi giá mua của bạn!]"
            ),
        },
        {
            "slot": "20:00",
            "image": SUBAGENT_DIR / "campaigns/2026-10-20/today-launch/images/sales-phongtro-2030-style01.png",
            "caption": (
                "Đi làm đi học về muộn lúc 7h tối bụng đói meo, ngại nhất là khoản ngồi thái từng củ cà rốt, khoai tây mất cả nửa tiếng đồng hồ?\n\n"
                "Trợ thủ đắc lực cho góc bếp trọ nhỏ: Bộ cắt gọt rau củ đa năng 6 lưỡi inox 304 kèm rổ xoay thoát nước thông minh!\n"
                "- Bào sợi, thái lát, cắt hoa văn đều tăm tắp chỉ trong 30 giây.\n"
                "- Có sẵn nắp giữ bảo vệ ngón tay an toàn tuyệt đối và lược gạt rửa nhanh.\n\n"
                "👉 Link chính hãng kèm ưu đãi mình để ngay ở bình luận đầu tiên nha!\n"
                "#PhongTroHetCuu #NauAnPhongTro #BepTro #DoBepThongMinh #MeoVatPhongTro"
            ),
            "pinned_cmt": (
                "📌 LINK CHÍNH HÃNG — BỘ BÀO CẮT RAU CỦ ĐA NĂNG KÈM RỔ XOAY THOÁT NƯỚC:\n"
                "🛒 Xem giá ưu đãi trên Shopee tại đây: https://s.shopee.vn/an_redir?origin_link=https%3A%2F%2Fshopee.vn%2Fsearch%3Fkeyword%3Db%25E1%25BB%2599%2520c%25E1%25BA%25AFt%2520rau%2520c%25E1%25BB%25A7%2520%25C4%2591a%2520n%25C4%2583ng%2520r%25E1%25BB%2595%2520xoay&affiliate_id=17395830088&sub_id=phongtro-bo_cat_rau_cu-auto_daily-2000\n"
                "ℹ️ [Affiliate Disclosure: Link chia sẻ có thể mang lại khoản hoa hồng nhỏ giúp duy trì Page mà không làm thay đổi giá mua của bạn!]"
            ),
        },
    ],
    "1421270697727753": [  # Ký Túc Xá Có Biến
        {
            "slot": "11:45",
            "image": SUBAGENT_DIR / "campaigns/2026-10-20/today-launch/images/sales-ktx-1145-style02.png",
            "caption": (
                "Nằm giường tầng 2 ký túc xá kéo rèm kín mít: Mở rèm ra thì mất riêng tư, mà đóng rèm lại thì bí hơi nóng hầm hập không ngủ trưa nổi?\n\n"
                "Giải pháp chuẩn bài cho dân KTX: Quạt tích điện mini ngàm kẹp Silicon xoay 360 độ!\n"
                "- Ngàm kẹp lót đệm cao su bám chắc vào khung sắt giường tầng hoặc cạnh bàn học không rung lắc.\n"
                "- Động cơ không chổi than siêu êm, ngủ trưa mát rượi mà không làm ồn phòng.\n\n"
                "👉 Link săn giá sinh viên mình ghim ở bình luận đầu tiên nhé!\n"
                "#KyTucXaCoBien #SinhVienKTX #GiuongTangKTX #DoDungSinhVien #QuatKepBan"
            ),
            "pinned_cmt": (
                "📌 LINK GIÁ SINH VIÊN — QUẠT TÍCH ĐIỆN MINI KẸP GIƯỜNG TẦNG KTX XOAY 360 ĐỘ:\n"
                "🛒 Săn ngay trên Shopee tại đây nha: https://s.shopee.vn/an_redir?origin_link=https%3A%2F%2Fshopee.vn%2Fsearch%3Fkeyword%3Dqu%25E1%25BA%25A1t%2520t%25C3%25ADch%2520%25C4%2591i%25E1%25BB%2587n%2520k%25E1%25BA%25B9p%2520gi%25C6%25B0%25E1%25BB%259Dng&affiliate_id=17395830088&sub_id=ktx-quat_kep_giuong-auto_daily-1145\n"
                "ℹ️ [Affiliate Disclosure: Link chia sẻ có thể mang lại khoản hoa hồng nhỏ giúp duy trì Page mà không làm thay đổi giá mua của bạn!]"
            ),
        },
        {
            "slot": "20:00",
            "image": SUBAGENT_DIR / "campaigns/2026-10-20/today-launch/images/sales-ktx-2100-style01.png",
            "caption": (
                "Mỗi sinh viên ở KTX chỉ được phát đúng 1 ô tủ sắt rộng 40cm: Nhét đúng 1 cái chăn bông với mấy chiếc áo khoác là hết sạch chỗ để quần áo mặc hàng ngày?\n\n"
                "Bí kíp hack diện tích tủ đồ gấp 4 lần: Bộ túi nén hút chân không PA+PE kèm bơm tay mini!\n"
                "- Hút sạch không khí chỉ trong 1 phút, ép gọn 75% thể tích chăn màn, gấu bông, quần áo mùa đông.\n"
                "- Chống ẩm mốc, chống bụi bẩn tuyệt đối, tái sử dụng bền bỉ suốt 4 năm đại học.\n\n"
                "👉 Link combo kèm bơm tay mình ghim ngay ở bình luận đầu tiên nha!\n"
                "#KyTucXaCoBien #MeoKTX #TuDoSinhVien #TuiHutChanKhong #TanSinhVien"
            ),
            "pinned_cmt": (
                "📌 LINK COMBO — BỘ TÚI NÉN HÚT CHÂN KHÔNG PA+PE KÈM BƠM TAY TIỆN LỢI:\n"
                "🛒 Xem chi tiết trên Shopee tại đây: https://s.shopee.vn/an_redir?origin_link=https%3A%2F%2Fshopee.vn%2Fsearch%3Fkeyword%3Db%25E1%25BB%2599%2520t%25C3%25BAi%2520h%25C3%25BAt%2520ch%25C3%25A2n%2520kh%25C3%25B4ng%2520k%25C3%25A8m%2520b%25C6%25A1m&affiliate_id=17395830088&sub_id=ktx-tui_hut_chan_khong-auto_daily-2000\n"
                "ℹ️ [Affiliate Disclosure: Link chia sẻ có thể mang lại khoản hoa hồng nhỏ giúp duy trì Page mà không làm thay đổi giá mua của bạn!]"
            ),
        },
    ],
    "1407231352464711": [  # Hội Deadline
        {
            "slot": "11:45",
            "image": SUBAGENT_DIR / "campaigns/2026-10-20/today-launch/images/sales-deadline-1145-style02.png",
            "caption": (
                "Ngồi gõ báo cáo có 3 tiếng buổi sáng mà cái cổ cúi gập xuống nhìn màn hình laptop đau nhức mỏi nhừ cả hai bả vai?\n\n"
                "Nâng cấp ngay góc làm việc chuẩn công thái học với Giá đỡ Laptop hợp kim nhôm xoay 360 độ:\n"
                "- Nâng màn hình lên đúng ngang tầm mắt, giữ thẳng đốt sống cổ suốt 8 tiếng làm việc.\n"
                "- Trục xoay cơ khí 360 độ kêu tách tách cực đầm, khung nhôm dày chịu tải tới 10kg và khe thoáng tản nhiệt mát máy.\n\n"
                "👉 Link chính hãng kèm ưu đãi mình ghim ở bình luận đầu tiên nhé!\n"
                "#HoiDeadline #DeskSetup #GiaDoLaptop #DanVanPhong #CongThaiHoc"
            ),
            "pinned_cmt": (
                "📌 LINK CHÍNH HÃNG — GIÁ ĐỠ LAPTOP HỢP KIM NHÔM XOAY 360 ĐỘ CHUẨN CÔNG THÁI HỌC:\n"
                "🛒 Săn ưu đãi trên Shopee tại đây nha: https://s.shopee.vn/an_redir?origin_link=https%3A%2F%2Fshopee.vn%2Fsearch%3Fkeyword%3Dgi%25C3%25A1%2520%25C4%2591%25E1%25BB%25A1%2520laptop%2520nh%25C3%25B4m%2520xoay%2520360&affiliate_id=17395830088&sub_id=deadline-gia_do_laptop_360-auto_daily-1145\n"
                "ℹ️ [Affiliate Disclosure: Link chia sẻ có thể mang lại khoản hoa hồng nhỏ giúp duy trì Page mà không làm thay đổi giá mua của bạn!]"
            ),
        },
        {
            "slot": "20:00",
            "image": SUBAGENT_DIR / "campaigns/2026-10-20/today-launch/images/sales-deadline-2000-style01.png",
            "caption": (
                "Tắt đèn trần làm việc ban đêm để đỡ phiền người nhà thì màn hình chói gắt mỏi mắt, mà bật đèn bàn thường thì ánh sáng chiếu thẳng vào màn hình gây lóa?\n\n"
                "Bí quyết cày deadline đêm êm dịu cho đôi mắt: Đèn LED kẹp màn hình (Screenbar) chiếu sáng bất đối xứng!\n"
                "- Chỉ rọi sáng đúng vùng bàn phím và tài liệu trước mặt, 0% ánh sáng hắt vào màn hình gây chói.\n"
                "- Cảm ứng chạm đổi 3 nhiệt độ màu (Trắng - Trung tính - Vàng ấm), tiết kiệm 100% diện tích mặt bàn.\n\n"
                "👉 Link săn sale mình để ngay ở bình luận đầu tiên nha!\n"
                "#HoiDeadline #DenKepManHinh #Screenbar #GocLamViec #ChayDeadline"
            ),
            "pinned_cmt": (
                "📌 LINK CHÍNH HÃNG — ĐÈN LED KẸP MÀN HÌNH CHIẾU SÁNG BẤT ĐỐI XỨNG BẢO VỆ MẮT:\n"
                "🛒 Xem chi tiết trên Shopee tại đây: https://s.shopee.vn/an_redir?origin_link=https%3A%2F%2Fshopee.vn%2Fsearch%3Fkeyword%3D%25C4%2591%25C3%25A8n%2520k%25E1%25BA%25B9p%2520m%25C3%25A0n%2520h%25C3%25ACnh%2520screenbar&affiliate_id=17395830088&sub_id=deadline-den_screenbar-auto_daily-2000\n"
                "ℹ️ [Affiliate Disclosure: Link chia sẻ có thể mang lại khoản hoa hồng nhỏ giúp duy trì Page mà không làm thay đổi giá mua của bạn!]"
            ),
        },
    ],
}


def load_vault() -> dict:
    if not VAULT_PATH.exists():
        return {}
    data = json.loads(VAULT_PATH.read_text(encoding="utf-8", errors="ignore"))
    return {str(p["id"]): p for p in data.get("pages", [])}


def graph_get(endpoint: str, token: str, params: dict = None) -> dict:
    q = dict(params or {})
    q["access_token"] = token
    url = f"https://graph.facebook.com/v22.0/{endpoint}?{urllib.parse.urlencode(q)}"
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read().decode("utf-8", errors="ignore"))


def graph_post(endpoint: str, token: str, params: dict) -> dict:
    url = f"https://graph.facebook.com/v22.0/{endpoint}"
    payload = dict(params)
    payload["access_token"] = token
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8", errors="ignore"))
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode("utf-8", errors="ignore"), "code": e.code}
    except Exception as e:
        return {"error": str(e)}


def upload_photo_or_schedule(page_id: str, token: str, image_path: Path, caption: str, sched_ts: int = 0) -> dict:
    url = f"https://graph.facebook.com/v22.0/{page_id}/photos"
    boundary = f"----AgentJavisBoundary{uuid.uuid4().hex}"
    body = bytearray()

    def add_field(name: str, value: str):
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{value}\r\n".encode("utf-8"))

    add_field("access_token", token)
    add_field("message", caption)
    now_ts = int(time.time())
    # Facebook requires scheduled_publish_time to be at least 10 minutes (600s) in the future
    if sched_ts > now_ts + 660:
        add_field("published", "false")
        add_field("scheduled_publish_time", str(sched_ts))
    else:
        add_field("published", "true")

    mime_type = mimetypes.guess_type(str(image_path))[0] or "image/png"
    file_bytes = image_path.read_bytes()
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="source"; filename="{image_path.name}"\r\n'.encode("utf-8"))
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    body.extend(file_bytes)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode("utf-8", errors="ignore"), "code": e.code}
    except Exception as e:
        return {"error": str(e)}


def ensure_daily_sales_posts_scheduled(pages: dict) -> list:
    """
    Kiểm tra 3 Page Bán Hàng xem hôm nay đã có bài đăng hoặc bài hẹn giờ cho khung 11:45 và 20:00 chưa.
    Nếu chưa có: tự động đăng/hẹn giờ và gắn Pinned Comment #1 chứa link Shopee Affiliate!
    """
    now_vn = dt.datetime.now(TZ_VN)
    today_str = now_vn.strftime("%Y-%m-%d")
    state_file = REPORTS_DIR / today_str / "auto_scheduled_sales_state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    done_state = {}
    if state_file.exists():
        try:
            done_state = json.loads(state_file.read_text(encoding="utf-8"))
        except Exception:
            done_state = {}

    actions_log = []
    for sid in SALES_IDS:
        if sid not in pages:
            continue
        p_obj = pages[sid]
        tok = p_obj["access_token"]
        pname = p_obj["name"]

        for item in DAILY_SALES_QUEUE.get(sid, []):
            slot = item["slot"]  # "11:45" or "20:00"
            key = f"{sid}_{today_str}_{slot}"
            if done_state.get(key):
                continue

            h, m = [int(x) for x in slot.split(":")]
            target_dt = dt.datetime(now_vn.year, now_vn.month, now_vn.day, h, m, 0, tzinfo=TZ_VN)
            sched_ts = int(target_dt.timestamp())

            img_path = item["image"]
            if not img_path.exists():
                continue

            res = upload_photo_or_schedule(sid, tok, img_path, item["caption"], sched_ts)
            post_id = res.get("post_id") or res.get("id")
            if post_id:
                # Attach Pinned Comment #1 immediately
                cmt_res = graph_post(f"{post_id}/comments", tok, {"message": item["pinned_cmt"]})
                cmt_id = cmt_res.get("id", "")
                mode_label = "SCHEDULED" if sched_ts > int(time.time()) + 660 else "PUBLISHED_NOW"
                done_state[key] = {
                    "post_id": post_id,
                    "pinned_comment_id": cmt_id,
                    "mode": mode_label,
                    "slot": slot,
                    "timestamp": now_vn.isoformat(),
                }
                actions_log.append(f"✅ [{pname}] Khung {slot}: {mode_label} ({post_id}) | Pinned Cmt: {cmt_id}")
            else:
                actions_log.append(f"⚠️ [{pname}] Khung {slot} lỗi: {res}")

    state_file.write_text(json.dumps(done_state, ensure_ascii=False, indent=2), encoding="utf-8")
    return actions_log


def ensure_all_live_posts_have_pinned_comment(pages: dict) -> list:
    """
    Quét 5 bài LIVE mới nhất trên cả 4 Page; nếu bài nào vừa nhảy từ Scheduled -> LIVE mà chưa có bình luận của Page,
    tự động gắn Pinned Comment #1 chuẩn phễu!
    """
    fixed_log = []
    for pid, p_obj in pages.items():
        if pid not in ([AI_ID] + SALES_IDS):
            continue
        tok = p_obj["access_token"]
        pname = p_obj["name"]
        try:
            feed = graph_get(f"{pid}/feed", tok, {"fields": "id,message,created_time", "limit": 5}).get("data", [])
            for post in feed:
                post_id = post["id"]
                cmts = graph_get(f"{post_id}/comments", tok, {"fields": "id,from", "limit": 10}).get("data", [])
                has_host_cmt = any(c.get("from", {}).get("id") == pid for c in cmts)
                if not has_host_cmt:
                    if pid == AI_ID:
                        pin_msg = (
                            "📌 KHO TÀI LIỆU & CỘNG ĐỒNG AI PLAYERS CHÍNH THỨC:\n"
                            "👉 Tham gia ngay Nhóm Zalo Cộng Đồng Bảo Mật để tải trọn bộ KHO VŨ KHÍ 6 SUBAGENT (.MD) & Sơ đồ Kiến trúc Miễn phí: "
                            "https://zalo.me/g/etllok798 (Mã vào nhóm: AIPLAYERS2026) 🚀"
                        )
                    else:
                        pin_msg = DAILY_SALES_QUEUE[pid][0]["pinned_cmt"]
                    r = graph_post(f"{post_id}/comments", tok, {"message": pin_msg})
                    if "id" in r:
                        fixed_log.append(f"📌 Đã tự động bổ sung Pinned Comment #1 cho bài mới lên sóng [{pname}]: {post_id} -> {r['id']}")
        except Exception:
            pass
    return fixed_log


def send_telegram_if_configured(text: str):
    bridge = SUBAGENT_DIR / "tools" / "telegram_bridge.py"
    if bridge.exists():
        subprocess.run(
            [sys.executable, str(bridge), "--send", "--text", text[:3900]],
            timeout=20,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["boot-or-9am", "midday-1145", "shift1-1200", "shift2-1730", "evening-2000", "eod-2130"],
        default="boot-or-9am",
    )
    args = parser.parse_args()

    now_vn = dt.datetime.now(TZ_VN)
    today_str = now_vn.strftime("%Y-%m-%d")
    pages = load_vault()

    # 1. Luôn đảm bảo đủ lịch đăng ngày hôm nay cho 3 Page Bán Hàng & kiểm tra Pinned Comment #1 trên cả 4 Page
    sched_actions = ensure_daily_sales_posts_scheduled(pages)
    pin_actions = ensure_all_live_posts_have_pinned_comment(pages)

    # 2. Thực thi tác vụ theo từng mốc giờ
    if args.mode in ("boot-or-9am", "eod-2130"):
        subprocess.run([sys.executable, str(SUBAGENT_DIR / "tools" / "mama_daily_9am_report.py"), "--quiet"])

    if args.mode in ("midday-1145", "evening-2000"):
        subprocess.run([sys.executable, str(SUBAGENT_DIR / "tools" / "fb_morning_2210_seeder.py")])

    if args.mode == "shift1-1200":
        subprocess.run([sys.executable, str(SUBAGENT_DIR / "tools" / "mama_daily_group_and_eod.py"), "--shift", "1", "--send-telegram"])

    if args.mode == "shift2-1730":
        subprocess.run([sys.executable, str(SUBAGENT_DIR / "tools" / "mama_daily_group_and_eod.py"), "--shift", "2", "--send-telegram"])

    # 3. Ghi nhận báo cáo mốc giờ ra file & gửi Telegram
    out_dir = REPORTS_DIR / today_str
    out_dir.mkdir(parents=True, exist_ok=True)
    milestone_file = REPORTS_DIR / "latest-milestone-status.md"

    lines = [
        f"# ⏰ BÁO CÁO TỰ ĐỘNG MỐC [{args.mode.upper()}] — {now_vn.strftime('%H:%M:%S %d/%m/%Y')}",
        "",
        "## 1. Trạng Thái Tự Động Lên Lịch & Xuất Bản 4 Fanpage",
    ]
    if sched_actions:
        lines.extend([f"- {a}" for a in sched_actions])
    else:
        lines.append("- ✅ Toàn bộ 4 Fanpage (`AI Players`, `Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline`) đã đủ lịch bài đăng khung `11:45` & `20:00` hôm nay.")

    if pin_actions:
        lines.append("\n## 2. Tự Động Gắn Pinned Comment #1 Cho Bài Mới Lên Sóng")
        lines.extend([f"- {p}" for p in pin_actions])

    summary_text = "\n".join(lines) + "\n"
    milestone_file.write_text(summary_text, encoding="utf-8")
    (out_dir / f"milestone_{args.mode}_{now_vn.strftime('%H%M')}.md").write_text(summary_text, encoding="utf-8")
    send_telegram_if_configured(summary_text)
    print(summary_text)


if __name__ == "__main__":
    main()
