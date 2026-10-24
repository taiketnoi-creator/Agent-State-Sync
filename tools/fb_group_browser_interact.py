#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fb_group_browser_interact.py — Công cụ Mở Trình Duyệt & Tương Tác Thực Chiến Trên Các Hội Nhóm + Video Ngang/Dọc (4 Ngách).

Nâng cấp v2.0 (2026-10-23):
1. Khởi tạo bảng điều khiển tương tác nhanh `campaigns/daily-reports/group_seeding_cockpit.html`
   với 3 nút mở nhanh cho mỗi ngách:
   - 🔥 Bài Mới Nhiều Like/Cmt (Group Posts)
   - 🎬 Video Ngang Hội Nhóm (16:9)
   - 📱 Video Dọc / Reels Cùng Tệp (9:16)
2. Copy sẵn bình luận chuyên sâu vào Clipboard và mở thẳng luồng bài/video đang thảo luận sôi nổi nhất.
"""

import os
import pathlib
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = pathlib.Path(__file__).resolve().parent.parent
COCKPIT_PATH = SUBAGENT_DIR / "campaigns" / "daily-reports" / "group_seeding_cockpit.html"

GROUPS_DATA = [
    {
        "niche": "1. AI Players - Người chơi hệ AI",
        "color": "#1452F0",
        "accent": "#A8FF00",
        "search_url": "https://www.facebook.com/search/posts?q=AI%20Agent%20ChatGPT%20c%C3%B4ng%20vi%E1%BB%87c%20Vi%E1%BB%87t%20Nam",
        "video_horiz_url": "https://www.facebook.com/search/videos?q=h%C6%B0%E1%BB%9Bng%20d%E1%BA%ABn%20AI%20ChatGPT%20t%E1%BB%B1%20%C4%91%E1%BB%99ng%20h%C3%B3a%20c%C3%B4ng%20vi%E1%BB%87c",
        "video_vert_url": "https://www.facebook.com/search/videos?q=m%E1%BA%B9o%20d%C3%B9ng%20AI%20ChatGPT%20reels",
        "groups_url": "https://www.facebook.com/search/groups?q=C%E1%BB%99ng%20%C4%90%E1%BB%93ng%20AI%20Vi%E1%BB%87t%20Nam",
        "comments": [
            "Công nhận xem clip/bài chia sẻ này chuẩn thực tế luôn bác ạ. Nhiều anh em sợ xài AI Pro tốn tiền triệu mỗi tháng, nhưng thực ra nếu biết phân tầng công việc kết hợp lấy tài nguyên lẻ tại trạm tự động trên Telegram (gõ @KingToolShop_bot vào ô tìm kiếm Tele là thấy) thì chi phí chỉ bằng ly trà đá, vào bấm Start còn có sẵn mục nhận quà workflow 0đ trong 3 giây luôn.",
            "Đúng chủ đề đang hot luôn! Mình đang dựng tổ đội 6 con Subagent chuyên biệt kết nối thẳng qua Telegram để giao việc từ xa. Tách riêng 1 con viết nội dung và 1 con Strict-Editor kiểm duyệt chéo theo 10 tiêu chí giúp giảm hẳn lỗi ảo giác và tiết kiệm cả nửa ngày làm việc!",
            "Bác nào xem xong mà muốn tự dựng hệ thống Agent riêng cho công việc nhưng ngại code thì cứ đóng gói quy trình thành các file mô tả công việc (.md) tiếng Việt rồi nạp vào Claude/ChatGPT/Antigravity là chạy mượt ngay trong 3 phút, không phải cào bàn phím từ đầu đâu.",
        ],
    },
    {
        "niche": "2. Phòng Trọ Hết Cứu (Decor & Tối ưu phòng trọ)",
        "color": "#445D27",
        "accent": "#ECFCCB",
        "search_url": "https://www.facebook.com/search/posts?q=c%E1%BA%A3i%20t%E1%BA%A1o%20d%E1%BB%8Dn%20ph%C3%B2ng%20tr%E1%BB%8D%20sinh%20vi%C3%AAn",
        "video_horiz_url": "https://www.facebook.com/search/videos?q=c%E1%BA%A3i%20t%E1%BA%A1o%20decor%20ph%C3%B2ng%20tr%E1%BB%8D%20nh%E1%BB%8F",
        "video_vert_url": "https://www.facebook.com/search/videos?q=%C4%91%E1%BB%93%20d%C3%B9ng%20ph%C3%B2ng%20tr%E1%BB%8D%20sinh%20vi%C3%AAn%20reels",
        "groups_url": "https://www.facebook.com/search/groups?q=Decor%20Ph%C3%B2ng%20Tr%E1%BB%8D%20Sinh%20Vi%C3%AAn",
        "comments": [
            "Xem mà đồng cảm thực sự! Phòng trọ nhỏ tầm 15-20m2 bí kíp của mình là sắm 1 chiếc máy hút bụi cầm tay không dây mini có đầu hút khe dẹt để hút sạch tóc rụng trên nệm với bụi bậu cửa sổ trong 2 phút, thêm bộ rổ bào cắt rau củ đa năng là tối đi làm về nấu canh nhanh gọn cực kỳ!",
            "Đi làm về muộn lúc 7h tối ngại nhất khoản ngồi thái cà rốt với khoai tây. Mình sắm bộ bào cắt rau củ đa năng kèm rổ xoay thoát nước, ấn nhẹ 30 giây là xong nồi canh, có cả cục nhựa bảo vệ ngón tay cực kỳ an toàn.",
            "Phòng trọ gác lửng hướng Tây buổi chiều hay lúc đứng nấu ăn nóng hầm hập thì bác cứ thủ sẵn 1 con quạt cầm tay phản lực 120 mức gió pin 5000mAh, vừa mát sâu vừa đề phòng những hôm khu trọ cúp điện đột xuất giữa đêm!",
        ],
    },
    {
        "niche": "3. Ký Túc Xá Có Biến (Sinh viên & Đời sống KTX)",
        "color": "#284166",
        "accent": "#E0F2FE",
        "search_url": "https://www.facebook.com/search/posts?q=k%C3%BD%20t%C3%BAc%20x%C3%A1%20sinh%20vi%C3%AAn%20gi%C6%B0%E1%BB%9Dng%20t%E1%BA%A7ng",
        "video_horiz_url": "https://www.facebook.com/search/videos?q=k%C3%BD%20t%C3%BAc%20x%C3%A1%20sinh%20vi%C3%AAn%20review",
        "video_vert_url": "https://www.facebook.com/search/videos?q=k%C3%BD%20t%C3%BAc%20x%C3%A1%20sinh%20vi%C3%AAn%20reels",
        "groups_url": "https://www.facebook.com/search/groups?q=K%C3%BD%20T%C3%BAc%20X%C3%A1%20Sinh%20Vi%C3%AAn",
        "comments": [
            "Xem clip/bài này nhớ cảnh KTX quá! Ở KTX tủ đồ nhỏ thì cứ dùng bộ túi nén hút chân không kèm bơm tay mini là gọn được 75% chỗ để chăn áo mùa đông. Còn nằm giường tầng 2 kéo rèm kín hơi bí thì kẹp thêm chiếc quạt tích điện xoay 360 độ vào thành giường là mát êm ru tới sáng luôn!",
            "Nằm giường tầng 2 KTX kéo rèm kín mít là bí hơi nóng không ngủ nổi, mà bật quạt trần thì đứa tầng 1 kêu lạnh. Cứ sắm cái quạt tích điện mini có ngàm kẹp silicon kẹp thẳng vào thanh sắt đầu giường xoay 360 độ là mát riêng một góc, êm ru tới sáng.",
            "Mùa nắng đi bộ từ giảng đường về KTX hay ngồi hội trường đông người thì chiếc quạt cầm tay phản lực 120 cấp gió có màn hình LED báo pin đúng là vật bất ly thân trong balo luôn các đồng môn ạ!",
        ],
    },
    {
        "niche": "4. Hội Deadline (Dân văn phòng & Desk Setup)",
        "color": "#1E293B",
        "accent": "#F1F5F9",
        "search_url": "https://www.facebook.com/search/posts?q=setup%20g%C3%B3c%20l%C3%A0m%20vi%E1%BB%87c%20v%C4%83n%20ph%C3%B2ng%20desk%20setup",
        "video_horiz_url": "https://www.facebook.com/search/videos?q=setup%20g%C3%B3c%20l%C3%A0m%20vi%E1%BB%87c%20desk%20setup%20v%C4%83n%20ph%C3%B2ng",
        "video_vert_url": "https://www.facebook.com/search/videos?q=g%C3%B3c%20l%C3%A0m%20vi%E1%BB%87c%20d%C3%A2n%20v%C4%83n%20ph%C3%B2ng%20reels",
        "groups_url": "https://www.facebook.com/search/groups?q=Vietnam%20Desk%20Setup",
        "comments": [
            "Đang chạy slide hay dựng video gấp lúc 1-2h sáng mà vướng bản quyền Canva/CapCut hay hết lượt ChatGPT thì tụt mood thực sự. Mẹo cho anh em hay cày đêm là lưu sẵn con bot @KingToolShop_bot trên Telegram (gõ tên này vào ô tìm kiếm Tele là thấy), quét QR 3 giây nó tự nhả tài khoản xuyên đêm kèm bảo hành 1-đổi-1 tự động luôn.",
            "Xem góc làm việc mê quá! Bác nào hay cày deadline ban đêm rất nên sắm một cây đèn kẹp màn hình chiếu sáng bất đối xứng (screenbar). Nó chiếu sáng đúng vùng bàn phím mà 0% hắt sáng gây chói màn hình, ngồi gõ máy 3-4 tiếng liên tục mắt vẫn dịu êm.",
            "Cảnh báo anh em dân văn phòng đừng đặt laptop nằm bẹt trực tiếp trên mặt bàn nhé, cúi cổ 30-45 độ suốt 8 tiếng là thoái hóa đốt sống cổ sớm luôn. Kê lên chiếc giá đỡ hợp kim nhôm xoay 360 độ cho màn hình ngang đúng tầm mắt là hết mỏi gáy ngay!",
            "Trưa văn phòng tắt điều hòa tổng hoặc sáng đi bộ từ hầm gửi xe lên công ty nóng bức thì cứ đặt sẵn 1 em quạt phản lực mini vỏ hợp kim màu champagne trên mặt bàn làm việc, vừa sang vừa mát tức thì.",
        ],
    },
]


def build_html() -> str:
    cards_html = ""
    for g in GROUPS_DATA:
        cmts_html = ""
        for idx, c in enumerate(g["comments"], 1):
            escaped = c.replace('"', "&quot;")
            cmts_html += f"""
            <div class="cmt-box">
              <div class="cmt-text" id="cmt-{g['niche'][:1]}-{idx}">{c}</div>
              <div class="btn-row">
                <button class="btn-copy" onclick="copyAndOpen('{escaped}', '{g['search_url']}', this)">
                  🔥 Copy &amp; Mở Bài Group Nhiều Like/Cmt
                </button>
                <button class="btn-copy video-h" onclick="copyAndOpen('{escaped}', '{g['video_horiz_url']}', this)">
                  🎬 Copy &amp; Mở Video Ngang (16:9)
                </button>
                <button class="btn-copy video-v" onclick="copyAndOpen('{escaped}', '{g['video_vert_url']}', this)">
                  📱 Copy &amp; Mở Video Dọc / Reels (9:16)
                </button>
              </div>
            </div>
            """
        cards_html += f"""
        <div class="niche-card" style="border-top: 6px solid {g['color']}">
          <div class="niche-header">
            <h2>{g['niche']}</h2>
            <div>
              <a class="link-btn" href="{g['groups_url']}" target="_blank">🔍 DS Group</a>
              <a class="link-btn primary" href="{g['search_url']}" target="_blank">🔥 Bài HOT</a>
              <a class="link-btn video" href="{g['video_horiz_url']}" target="_blank">🎬 Video Ngang</a>
              <a class="link-btn reel" href="{g['video_vert_url']}" target="_blank">📱 Video Dọc/Reels</a>
            </div>
          </div>
          {cmts_html}
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>Mama — Bảng Điều Khiển Tương Tác Bài HOT & Video Ngang/Dọc 60 Hội Nhóm</title>
<style>
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #0F172A; color: #F8FAFC; margin: 0; padding: 24px 32px; }}
  h1 {{ color: #A8FF00; margin-bottom: 6px; font-size: 25px; }}
  .sub {{ color: #94A3B8; margin-bottom: 22px; font-size: 14px; line-height: 1.5; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
  .niche-card {{ background: #1E293B; border-radius: 14px; padding: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }}
  .niche-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; gap: 8px; flex-wrap: wrap; }}
  .niche-header h2 {{ margin: 0; font-size: 17px; color: #FFFFFF; }}
  .link-btn {{ text-decoration: none; padding: 6px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; background: #334155; color: #E2E8F0; margin-left: 4px; display: inline-block; }}
  .link-btn.primary {{ background: #2563EB; color: #FFF; }}
  .link-btn.video {{ background: #0EA5E9; color: #FFF; }}
  .link-btn.reel {{ background: #EC4899; color: #FFF; }}
  .cmt-box {{ background: #0F172A; border: 1px solid #334155; border-radius: 10px; padding: 14px; margin-bottom: 12px; }}
  .cmt-text {{ font-size: 13.5px; line-height: 1.55; color: #E2E8F0; margin-bottom: 10px; }}
  .btn-row {{ display: flex; gap: 8px; flex-wrap: wrap; }}
  .btn-copy {{ background: #A8FF00; color: #03185E; border: none; padding: 7px 12px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 12px; transition: 0.15s; }}
  .btn-copy.video-h {{ background: #38BDF8; color: #082F49; }}
  .btn-copy.video-v {{ background: #F472B6; color: #500724; }}
  .btn-copy:hover {{ opacity: 0.92; transform: translateY(-1px); }}
</style>
</head>
<body>
  <h1>🚀 MAMA — TRẠM TƯƠNG TÁC BÀI MỚI NHIỀU LIKE/CMT &amp; VIDEO NGANG/DỌC CÙNG TỆP</h1>
  <div class="sub">
    Ưu tiên tuyệt đối tương tác vào <b>Bài viết mới, nhiều Like, nhiều Bình luận</b> cùng <b>Video Ngang (16:9)</b> và <b>Video Dọc/Reels (9:16)</b> trong các Hội nhóm cùng tệp để kéo phễu hiệu quả nhất!
  </div>
  <div class="grid">
    {cards_html}
  </div>
  <script>
    function copyAndOpen(text, url, btn) {{
      navigator.clipboard.writeText(text).then(() => {{
        btn.innerText = "✅ ĐÃ COPY! Đang mở luồng...";
        btn.style.background = "#22C55E";
        btn.style.color = "#FFFFFF";
        setTimeout(() => {{
          window.open(url, "_blank");
        }}, 250);
      }});
    }}
  </script>
</body>
</html>"""


def main():
    COCKPIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    COCKPIT_PATH.write_text(build_html(), encoding="utf-8")
    print(f"✅ Đã cập nhật Bảng Điều Khiển Tương Tác Bài HOT & Video Ngang/Dọc tại: {COCKPIT_PATH}")


if __name__ == "__main__":
    main()
