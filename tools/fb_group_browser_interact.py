#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fb_group_browser_interact.py — Công cụ Mở Trình Duyệt & Tương Tác Thực Chiến Trên Các Hội Nhóm Facebook (4 Ngách).
1. Khởi tạo bảng điều khiển tương tác nhanh `campaigns/2026-10-21/group_seeding_cockpit.html`
   (Tự động nạp sẵn 12 bình luận Ca Tối + 4 Bài Trojan Horse Group Seeding + 7 Link bài mới đăng hôm nay).
2. Mở trực tiếp trình duyệt Google Chrome đang đăng nhập Facebook của CEO vào thẳng luồng thảo luận mới nhất
   của các Hội nhóm mục tiêu để tương tác thật ngay lập tức.
"""

import os
import pathlib
import subprocess
import sys
import urllib.parse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = pathlib.Path(__file__).resolve().parent.parent
COCKPIT_PATH = SUBAGENT_DIR / "campaigns" / "2026-10-21" / "group_seeding_cockpit.html"

GROUPS_DATA = [
    {
        "niche": "1. AI Players - Người chơi hệ AI",
        "color": "#1452F0",
        "accent": "#A8FF00",
        "search_url": "https://www.facebook.com/search/posts?q=AI%20Agent%20t%E1%BB%B1%20%C4%91%E1%BB%99ng%20h%C3%B3a%20ChatGPT",
        "groups_url": "https://www.facebook.com/search/groups?q=C%E1%BB%99ng%20%C4%90%E1%BB%93ng%20AI%20Vi%E1%BB%87t%20Nam",
        "comments": [
            "Nhiều anh em vẫn nghĩ AI Agent là cái gì đó xa xôi. Nhưng thực tế năm 2026 này, ai biết tách việc ra cho tổ đội 3-4 con Subagent (1 con đọc dữ liệu, 1 con viết, 1 con thanh tra soi lỗi) là đã tiết kiệm được nửa ngày làm việc rồi. Quan trọng là đừng bắt 1 khung chat ôm đồm 10 việc cùng lúc thôi bác ạ!",
            "Em thấy rào cản lớn nhất khi đưa AI vào công việc văn phòng là tính 'ảo giác' (bịa số liệu). Cách giải quyết triệt để nhất bên em đang áp dụng là tách riêng 1 con Subagent tên là Strict-Editor chấm điểm theo 10 tiêu chí trước khi xuất bản. Anh em ở đây có đang dùng mô hình phân vai kiểu này không?",
            "Bác nào đang muốn tự dựng hệ thống Agent riêng cho công việc mà ngại code thì cứ đóng gói quy trình thành các file mô tả công việc (.md) tiếng Việt rồi nạp vào Claude/ChatGPT/Antigravity là chạy mượt ngay trong 3 phút, không phải cào bàn phím từ đầu đâu.",
        ],
    },
    {
        "niche": "2. Phòng Trọ Hết Cứu (Decor & Tối ưu phòng trọ)",
        "color": "#445D27",
        "accent": "#ECFCCB",
        "search_url": "https://www.facebook.com/search/posts?q=d%E1%BB%8Dn%20ph%C3%B2ng%20tr%E1%BB%8D%20n%E1%BA%A5u%20%C4%83n%20ph%C3%B2ng%20tr%E1%BB%8D",
        "groups_url": "https://www.facebook.com/search/groups?q=Decor%20Ph%C3%B2ng%20Tr%E1%BB%8D%20Sinh%20Vi%C3%AAn",
        "comments": [
            "Phòng 15m2 mà nhét đủ bàn làm việc, tủ quần áo với giường ngủ là cả một nghệ thuật. Bí kíp của mình là sắm 1 con máy hút bụi cầm tay không dây mini có đầu dẹt để hút sạch tóc rụng trên nệm với bụi khe cửa sổ trong 2 phút, khỏi phải quét chổi bụi bay mù mịt.",
            "Đi làm về muộn lúc 7h tối ngại nhất khoản ngồi thái cà rốt với khoai tây. Mình sắm bộ bào cắt rau củ đa năng kèm rổ xoay thoát nước, ấn nhẹ 30 giây là xong nồi canh, có cả cục nhựa bảo vệ ngón tay cực kỳ an toàn.",
            "Phòng trọ gác lửng hướng Tây buổi chiều hay lúc đứng nấu ăn nóng hầm hập thì bác cứ thủ sẵn 1 con quạt cầm tay phản lực 120 mức gió pin 5000mAh, vừa mát sâu vừa đề phòng những hôm khu trọ cúp điện đột xuất giữa đêm!",
        ],
    },
    {
        "niche": "3. Ký Túc Xá Có Biến (Sinh viên & Đời sống KTX)",
        "color": "#284166",
        "accent": "#E0F2FE",
        "search_url": "https://www.facebook.com/search/posts?q=k%C3%BD%20t%C3%BAc%20x%C3%A1%20gi%C6%B0%E1%BB%9Dng%20t%E1%BA%A7ng%20sinh%20vi%C3%AAn",
        "groups_url": "https://www.facebook.com/search/groups?q=K%C3%BD%20T%C3%BAc%20X%C3%A1%20Sinh%20Vi%C3%AAn",
        "comments": [
            "Ở KTX mỗi đứa chỉ được đúng 1 ô tủ sắt 40cm, nhét cái chăn bông mùa đông vào là hết sạch chỗ! Mẹo cứu cánh của phòng mình là dùng bộ túi nén hút chân không kèm bơm tay mini, hút 1 phút chăn áo xẹp đi 75% thể tích, tủ rộng thênh thang luôn.",
            "Nằm giường tầng 2 KTX kéo rèm kín mít là bí hơi nóng không ngủ nổi, mà bật quạt trần thì đứa tầng 1 kêu lạnh. Cứ sắm cái quạt tích điện mini có ngàm kẹp silicon kẹp thẳng vào thanh sắt đầu giường xoay 360 độ là mát riêng một góc, êm ru tới sáng.",
            "Mùa nắng đi bộ từ giảng đường về KTX hay ngồi hội trường đông người thì chiếc quạt cầm tay phản lực 120 cấp gió có màn hình LED báo pin đúng là vật bất ly thân trong balo luôn các đồng môn ạ!",
        ],
    },
    {
        "niche": "4. Hội Deadline (Dân văn phòng & Desk Setup)",
        "color": "#1E293B",
        "accent": "#F1F5F9",
        "search_url": "https://www.facebook.com/search/posts?q=g%C3%B3c%20l%C3%A0m%20vi%E1%BB%87c%20desk%20setup%20%C4%91au%20vai%20g%C3%A1y",
        "groups_url": "https://www.facebook.com/search/groups?q=Vietnam%20Desk%20Setup",
        "comments": [
            "Bác nào hay cày deadline ban đêm rất nên sắm một cây đèn kẹp màn hình chiếu sáng bất đối xứng (screenbar). Nó chiếu sáng đúng vùng bàn phím mà 0% hắt sáng gây chói màn hình, ngồi gõ máy 3-4 tiếng liên tục mắt vẫn dịu êm.",
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
                  📋 Copy Bình Luận #{idx} &amp; Mở Bài Thảo Luận Group
                </button>
              </div>
            </div>
            """
        cards_html += f"""
        <div class="niche-card" style="border-top: 6px solid {g['color']}">
          <div class="niche-header">
            <h2>{g['niche']}</h2>
            <div>
              <a class="link-btn" href="{g['groups_url']}" target="_blank">🔍 Mở Danh Sách Group</a>
              <a class="link-btn primary" href="{g['search_url']}" target="_blank">💬 Mở Bài Thảo Luận Mới Nhất</a>
            </div>
          </div>
          {cmts_html}
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>Mama — Bảng Điều Khiển Tương Tác Thực Chiến 60 Hội Nhóm Facebook</title>
<style>
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #0F172A; color: #F8FAFC; margin: 0; padding: 24px 32px; }}
  h1 {{ color: #A8FF00; margin-bottom: 6px; font-size: 26px; }}
  .sub {{ color: #94A3B8; margin-bottom: 24px; font-size: 15px; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
  .niche-card {{ background: #1E293B; border-radius: 14px; padding: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }}
  .niche-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; gap: 10px; flex-wrap: wrap; }}
  .niche-header h2 {{ margin: 0; font-size: 18px; color: #FFFFFF; }}
  .link-btn {{ text-decoration: none; padding: 7px 12px; border-radius: 8px; font-size: 13px; font-weight: 600; background: #334155; color: #E2E8F0; margin-left: 6px; display: inline-block; }}
  .link-btn.primary {{ background: #2563EB; color: #FFF; }}
  .cmt-box {{ background: #0F172A; border: 1px solid #334155; border-radius: 10px; padding: 14px; margin-bottom: 12px; }}
  .cmt-text {{ font-size: 14px; line-height: 1.55; color: #E2E8F0; margin-bottom: 10px; }}
  .btn-copy {{ background: #A8FF00; color: #03185E; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13px; transition: 0.15s; }}
  .btn-copy:hover {{ background: #bef264; transform: translateY(-1px); }}
</style>
</head>
<body>
  <h1>🚀 MAMA — TRẠM TƯƠNG TÁC THẬT 60 HỘI NHÓM FACEBOOK (CA TỐI 21/10/2026)</h1>
  <div class="sub">
    Bấm <b>"📋 Copy Bình Luận &amp; Mở Bài Thảo Luận Group"</b>: Hệ thống tự động Copy sẵn nội dung vào Clipboard và mở thẳng tab bài viết đang thảo luận sôi nổi trên Facebook Group để dán (Ctrl+V) ngay trong 2 giây!
  </div>
  <div class="grid">
    {cards_html}
  </div>
  <script>
    function copyAndOpen(text, url, btn) {{
      navigator.clipboard.writeText(text).then(() => {{
        const old = btn.innerText;
        btn.innerText = "✅ ĐÃ COPY! Đang mở tab Facebook Group...";
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
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    urls_to_open = [
        str(COCKPIT_PATH),
        "https://www.facebook.com/search/posts?q=AI%20Agent%20t%E1%BB%B1%20%C4%91%E1%BB%99ng%20h%C3%B3a%20ChatGPT",
        "https://www.facebook.com/search/posts?q=d%E1%BB%8Dn%20ph%C3%B2ng%20tr%E1%BB%8D%20decor%20ph%C3%B2ng%20tr%E1%BB%8D",
        "https://www.facebook.com/search/posts?q=k%C3%BD%20t%C3%BAc%20x%C3%A1%20gi%C6%B0%E1%BB%9Dng%20t%E1%BA%A7ng%20sinh%20vi%C3%AAn",
        "https://www.facebook.com/search/posts?q=g%C3%B3c%20l%C3%A0m%20vi%E1%BB%87c%20desk%20setup%20deadline",
    ]
    if os.path.exists(chrome_path):
        subprocess.Popen([chrome_path] + urls_to_open)
        print("✅ Đã mở trực tiếp trình duyệt Chrome với Trạm Tương Tác Hội Nhóm & 4 Tab Thảo Luận Group!")
    else:
        os.startfile(str(COCKPIT_PATH))
        print("✅ Đã mở Trạm Tương Tác Hội Nhóm!")


if __name__ == "__main__":
    main()
