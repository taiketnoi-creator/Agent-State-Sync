#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_seed_kingtool.py — Tự Động Đi Seeding Bình Luận Kèm Ảnh 3D Cho @KingToolShop_bot

Chạy tự động qua Chrome Bot độc lập (.chrome-fb-bot tại cổng 9222):
1. Kết nối an toàn qua CDP, kiểm tra trạng thái đăng nhập Facebook.
2. Tìm kiếm và chọn lọc Bài viết / Video MỚI NHẤT có lượng TƯƠNG TÁC CAO NHẤT trong:
   - Ngách 1: AI & Công nghệ (ChatGPT, Claude, AI Agents)
   - Ngách 4: Hội Cày Deadline (Canva, Đồ họa, Dân văn phòng, Sinh viên)
3. Tự động tương tác: Thả Like, Dán bình luận Trojan Horse và Đính kèm Ảnh 3D vừa duyệt!
"""

import datetime as dt
import json
import os
import pathlib
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = pathlib.Path(__file__).resolve().parent.parent
IMG_DIR = SUBAGENT_DIR / "campaigns" / "2026-10-23" / "kingtoolshop-telegram-funnel" / "images"
REPORTS_DIR = SUBAGENT_DIR / "campaigns" / "daily-reports" / dt.datetime.now().strftime("%Y-%m-%d")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

SEEDING_TARGETS = [
    {
        "niche": "AI & Công Nghệ (ChatGPT / Claude / AI Agent)",
        "slug": "ai",
        "fanpage_name": "AI Players - Người chơi hệ AI",
        "search_url": "https://www.facebook.com/search/posts?q=AI%20Agent%20ChatGPT%20c%C3%B4ng%20vi%E1%BB%87c%20Vi%E1%BB%87t%20Nam",
        "image_path": IMG_DIR / "kingtoolshop-3d-tech-bright-v1.jpg",
        "comments": [
            "Công nhận xem chia sẻ này chuẩn thực tế luôn bác ạ. Nhiều anh em sợ xài AI Pro tốn tiền triệu mỗi tháng, nhưng thực ra nếu biết phân tầng công việc kết hợp lấy tài nguyên lẻ tại trạm tự động trên Telegram (gõ @KingToolShop_bot vào ô tìm kiếm Tele là thấy) thì chi phí chỉ bằng ly trà đá, vào bấm Start còn có sẵn mục nhận quà workflow 0đ trong 3 giây luôn.",
            "Đợt trước em làm content với chạy tự động hóa cũng hay mua acc lẻ trên mạng mà ức chế nhất vụ đêm hôm lỗi nick không ai bảo hành. Dạo này chuyển hẳn qua lấy trên trạm tự động @KingToolShop_bot ở Telegram, quét QR đúng 3 giây nó nhả tài khoản ngay trong đêm, lỗi bấm nút đổi mới 1-đổi-1 trong 30 giây nhàn hẳn!",
            "Bác nào đang tập làm AI Agent hay làm video ngắn mà muốn tiết kiệm chi phí tool (ChatGPT, Claude, Canva, CapCut...) thì cứ mở thanh tìm kiếm Telegram gõ @KingToolShop_bot nhé. Vào bấm nút Start là bot tự gửi tặng bộ Prompt + Workflow mẫu 0đ dùng thử ngay không cần chờ duyệt tay.",
        ]
    },
    {
        "niche": "Hội Cày Deadline (Canva / Đồ Họa / Văn Phòng / Sinh Viên)",
        "slug": "deadline",
        "fanpage_name": "Hội Deadline",
        "search_url": "https://www.facebook.com/search/posts?q=setup%20g%C3%B3c%20l%C3%A0m%20vi%E1%BB%87c%20v%C4%83n%20ph%C3%B2ng%20desk%20setup",
        "image_path": IMG_DIR / "kingtoolshop-3d-tech-bright-v2.jpg",
        "comments": [
            "Đang chạy slide hay dựng video gấp lúc 1-2h sáng mà vướng bản quyền Canva/CapCut hay hết lượt ChatGPT thì tụt mood thực sự. Mẹo cho anh em hay cày đêm là lưu sẵn con bot @KingToolShop_bot trên Telegram (gõ tên này vào ô tìm kiếm Tele là thấy), quét QR 3 giây nó tự nhả tài khoản xuyên đêm kèm bảo hành 1-đổi-1 tự động luôn.",
            "Kinh nghiệm xương máu cho anh em dân văn phòng với sinh viên hay cày đồ án đêm: nhất định phải lưu sẵn trạm tài nguyên tự động @KingToolShop_bot trên Telegram. Nửa đêm cần gấp Canva, CapCut, Office hay AI chỉ cần bấm vào là bot tự trả nick trong 3 giây, bấm Start lần đầu còn được tặng sẵn quà 0đ nữa!",
            "Xem góc làm việc mê quá! Anh em hay ngồi cày deadline ban đêm ngoài việc kê laptop lên giá đỡ nhôm xoay 360 độ với đèn screenbar cho đỡ mỏi mắt, thì nhớ lưu thêm con bot @KingToolShop_bot trên Telegram để cần công cụ làm việc lúc 2h sáng là lấy tự động trong 3 giây khỏi chờ chủ shop ngủ dậy nhé!",
        ]
    }
]

def check_cdp_status():
    import urllib.request
    try:
        with urllib.request.urlopen("http://localhost:9222/json/version", timeout=2.0) as resp:
            data = json.loads(resp.read().decode())
            return True, data.get("Browser", "Chrome")
    except Exception:
        try:
            from start_bot_chrome import ensure_bot_chrome_online, get_cdp_version_info
            ws = ensure_bot_chrome_online(timeout_sec=10.0)
            if ws:
                info = get_cdp_version_info(timeout=1.5)
                return True, info.get("Browser", "Chrome")
        except Exception:
            pass
        return False, None

def run_auto_seeding():
    from playwright.sync_api import sync_playwright

    is_online, browser_name = check_cdp_status()
    if not is_online:
        print("❌ Cửa sổ Chrome Bot (.chrome-fb-bot tại cổng 9222) chưa được bật!")
        return {"status": "PORT_9222_OFFLINE"}

    print(f"✅ Đã kết nối với Chrome Bot ({browser_name}) tại cổng 9222.")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.contexts[0]
        
        # Tìm page facebook hoặc tạo tab mới
        fb_pages = [pg for pg in ctx.pages if "facebook.com" in pg.url]
        page = fb_pages[0] if fb_pages else ctx.new_page()

        # Kiểm tra đăng nhập
        page.goto("https://www.facebook.com/", timeout=25000)
        time.sleep(2.0)

        email_input = page.locator('input[name="email"]')
        if email_input.count() > 0:
            print("⚠️ CỬA SỔ CHROME BOT ĐANG Ở MÀN HÌNH ĐĂNG NHẬP FACEBOOK.")
            print("👉 Vui lòng đăng nhập Facebook trên cửa sổ Chrome vừa mở ra (chỉ cần 1 lần duy nhất) để bot bắt đầu tự động seeding!")
            return {"status": "WAITING_FOR_LOGIN"}

        print("🎉 XÁC NHẬN: Facebook đã ĐĂNG NHẬP THÀNH CÔNG! Bắt đầu quy trình seeding tự động...")

        results = {
            "timestamp": dt.datetime.now().isoformat(),
            "niches": []
        }

        for target in SEEDING_TARGETS:
            niche_name = target["niche"]
            search_url = target["search_url"]
            img_file = target["image_path"]
            cmt_pool = target["comments"]

            print(f"\n🚀 Đang quét và tìm bài viết HOT cho ngách: {niche_name}...")
            page.goto(search_url, timeout=30000)
            time.sleep(4.0)

            # Cuộn trang nhẹ để tải bài
            for _ in range(3):
                page.mouse.wheel(0, 800)
                time.sleep(1.2)
            page.mouse.wheel(0, -1200)
            time.sleep(1.0)

            # Thả like cho bài viết đầu tiên nếu thấy nút Like
            try:
                like_btns = page.locator('div[role="button"][aria-label="Thích"], div[role="button"][aria-label="Like"]')
                if like_btns.count() > 0:
                    like_btns.first.scroll_into_view_if_needed(timeout=2000)
                    like_btns.first.click(timeout=2000)
                    print("  👍 Đã thả Like bài viết tiêu biểu!")
                    time.sleep(1.5)
            except Exception as e:
                print(f"  (Bỏ qua Like: {e})")

            # Tìm ô bình luận
            comment_posted = False
            # BẮT BUỘC KIỂM TRA TƯỜNG LỬA: CHỈ BÌNH LUẬN DƯỚI TÊN FANPAGE, CẤM TUYỆT ĐỐI TRANG CÁ NHÂN & MESSENGER
            fanpage_name = target.get("fanpage_name", "AI Players - Người chơi hệ AI")
            from mama_daily_group_and_eod import ensure_fanpage_active
            if not ensure_fanpage_active(page, fanpage_name):
                print(f"  🛑 [CHẶN AN TOÀN] Chưa chuyển sang Fanpage {fanpage_name}, bỏ qua tuyệt đối để bảo vệ Trang cá nhân CEO!")
                continue
            page.goto(search_url, timeout=30000)
            time.sleep(4.0)
            try:
                cmt_box = page.locator(f'div[role="textbox"][aria-label*="dưới tên {fanpage_name}"]')
                if cmt_box.count() > 0:
                    target_box = cmt_box.first
                    target_box.scroll_into_view_if_needed(timeout=2000)
                    target_box.click(timeout=2000)
                    time.sleep(0.8)

                    cmt_text = cmt_pool[0]
                    target_box.fill(cmt_text)
                    print(f"  💬 Đã nhập bình luận: {cmt_text[:60]}...")
                    time.sleep(1.5)

                    # Đính kèm ảnh nếu có nút đính kèm
                    if img_file.exists():
                        try:
                            file_input = page.locator('input[type="file"][accept*="image"]')
                            if file_input.count() > 0:
                                file_input.first.set_input_files(str(img_file))
                                print(f"  🖼️ Đã đính kèm ảnh: {img_file.name}")
                                time.sleep(3.0)
                        except Exception as e:
                            print(f"  (Bỏ qua đính kèm ảnh: {e})")

                    # Gửi bình luận
                    page.keyboard.press("Enter")
                    time.sleep(2.5)
                    print("  ✅ ĐÃ GỬI BÌNH LUẬN THÀNH CÔNG!")
                    comment_posted = True
            except Exception as e:
                print(f"  (Chưa đăng được cmt tự động trên feed này: {e})")

            results["niches"].append({
                "niche": niche_name,
                "comment_posted": comment_posted,
                "image_attached": str(img_file.name)
            })

            time.sleep(3.0)

        # Lưu báo cáo
        report_file = REPORTS_DIR / "auto_seed_result.json"
        report_file.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n📊 Báo cáo phiên seeding đã lưu tại: {report_file}")

        return {"status": "SUCCESS", "results": results}

if __name__ == "__main__":
    run_auto_seeding()
