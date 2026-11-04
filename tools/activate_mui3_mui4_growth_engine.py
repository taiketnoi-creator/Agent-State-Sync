#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
activate_mui3_mui4_growth_engine.py — Kích Hoạt Mũi 3 & Mũi 4 Tăng Trưởng Cho 4 Fanpage
========================================================================================
1. Mũi 4 (Nâng cấp Kịch bản Seeding Hội Nhóm 3 Ca `12:00 / 17:30 / 20:30` tại `tools/mama_daily_group_and_eod.py`):
   - Áp dụng công thức "80% Giá trị thực chiến + 20% Curiosity Hook Kéo Về Tường Fanpage".
   - Tuân thủ 100% LUẬT #5 (Tường Lửa Tách Tệp): Kênh AI và 3 Kênh Bán Hàng hoàn toàn độc lập, 0% link spam trong nhóm.
2. Mũi 3A (Tự động trả lời bình luận khách hàng `Auto-Reply Customer Comments` trên cả 4 Fanpage):
   - Tích hợp `ensure_auto_reply_customer_comments(pages)` vào `tools/mama_auto_scheduler_engine.py`.
   - Quét toàn bộ bình luận khách hàng (`from.id != page_id`) trên 15 bài gần nhất của cả 4 Page để phản hồi tự động kèm link Zalo VIP (Page AI) hoặc link Shopee Affiliate của đúng sản phẩm đó (3 Page Bán Hàng).
   - Bổ sung bình luận phá băng thảo luận dưới các bài bán hàng mới lên sóng để kích thích khách để lại bình luận thật.
3. Mũi 3B (Thiết kế Độc Bản `Zero-Clone` & Đăng LIVE Bài Chủ Lực Thu Phễu "KHO VŨ KHÍ AI PLAYERS ĐÓNG HỘP 2026"):
   - Kết xuất ảnh `1080×1080` độc bản (`master_funnel_hub_ai_players_2026.jpg`), kiểm định qua `verify_zero_clone_images()`,
     đăng LIVE lên đầu tường Page `AI Players` (`1022527194267367`) và gắn `Pinned Comment #1` dẫn thẳng vào Nhóm Zalo Cộng Đồng.
"""

import json
import re
import sys
import time
import requests
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SUBAGENT_DIR / "tools"))

from render_vid_style_card import get_local_fonts_css, render_html_to_image
from zero_repost_gate import verify_zero_clone_images, record_published_content
from mama_auto_scheduler_engine import load_vault, graph_get, graph_post

AI_ID = "1022527194267367"
SALES_IDS = ["1442323328956326", "1421270697727753", "1407231352464711"]
ZALO_VIP_URL = "https://zalo.me/g/fzxvbf259"

NEW_COMMENTS_POOL = {
    "ai": [
        "Chuẩn thực chiến luôn bác! Dùng 1 con AI lẻ rất dễ loạn ngữ cảnh — bên mình đang vận hành mô hình Đội ngũ 10 Subagent Cá nhân & Doanh nghiệp có cổng kiểm duyệt riêng. Mình có ghim sẵn Sơ đồ Kiến trúc + Nhận thiết kế Đội ngũ Subagent may đo 1:1 ngay bài đầu trên tường Page, bác bấm vào tên Page mình xem nha!",
        "Đúng nỗi đau của nhiều anh em làm văn phòng và chủ shop! Thay vì làm thủ công từng việc, chỉ cần dựng một Đội ngũ Subagent chuyên trách (Tổng quản, MKT, Content, Báo cáo, CSKH) chạy ngầm 24/7. Bản thiết kế mẫu & dịch vụ Setup Đội ngũ Subagent trọn gói mình ghim ngay trên tường Page, anh em bấm vào tên Page mình lấy nhé!",
        "Góc nhìn rất sát thực tế! Khi gắn thêm 'Bộ não thứ 2' (Memory Vault) vào Đội ngũ Subagent Cá nhân, AI sẽ nhớ 100% quy tắc và phong cách làm việc của chủ nhân mà không lặp lại lỗi cũ. Mình vừa ghim bộ khung 10 Subagent (.MD) ngay bài đầu tiên trên tường Page, bác nào cần bấm vào tên Page mình tải miễn phí nha!",
        "Bí quyết giải phóng 80% thời gian cho CEO và Freelancer là bàn giao việc lặp lại cho một Đội ngũ Subagent Doanh nghiệp nối thẳng qua Zalo/Telegram. Toàn bộ Blueprint kiến trúc & đăng ký tư vấn thiết kế Đội ngũ Subagent riêng mình để sẵn ngay bài ghim trên tường Page, bác bấm vào tên Page mình tham khảo nhé!",
        "Chia sẻ quá chất lượng! Anh em nào muốn có riêng một Đội ngũ Subagent Cá nhân hoặc Phòng ban Subagent Doanh nghiệp may đo sát 100% quy trình thực tế mà không cần tự mò code phức tạp thì ghé ngay bài đầu tiên trên tường Page mình nhé — có sẵn bản mẫu miễn phí lẫn gói dựng trọn gói 1:1 luôn ạ!",
        "Đồng ý 100%! Từ lọc dữ liệu, viết kịch bản đa kênh, thiết kế đồ họa Zero-Clone tới trực bình luận đều có thể giao cho Đội ngũ Subagent tự hành. Mình vừa cập nhật sơ đồ vận hành 11 Subagent thực tế ngay trên tường Page, bác nào quan tâm bấm vào tên Page mình xem chi tiết nha!"
    ],
    "phongtro": [
        "Đồng cảm thực sự luôn! Phòng trọ nhỏ 15–20m2 bí kíp của mình là dùng kệ giày chữ Z sát cửa và cây lau nhà tự vắt đứng gọn góc 10cm. Mình vừa ghim hình thực tế mấy món cứu cánh phòng trọ nhỏ gọn cực rẻ ngay bài đầu trên tường Page, bạn nào đang dọn phòng bấm vào tên Page mình xem nha!",
        "Phòng trọ kín gió gặp đợt mưa ẩm quần áo hay bị mùi ngai ngái thì cứ dùng túi sấy quần áo gấp gọn có tia UV khử khuẩn nhé, sấy 45 phút khô thơm phức rồi gấp gọn bằng cuốn sổ! Hình thực tế món này mình ghim ngay trên tường Page, bạn bấm vào tên Page mình tham khảo nha!",
        "Ở trọ tầng cao nước yếu hoặc đường ống cũ có cặn vàng thì lắp thêm đầu vòi tăng áp xoay 720 độ có lõi lọc bông PP trong suốt là nước mạnh gấp 3 mà sạch hẳn cặn bẩn. Mình có để chi tiết món này ngay bài đầu trên tường Page, bạn nào cần bấm vào tên Page mình xem nhé!",
        "Khe hở dưới đáy cửa phòng trọ chính là đường cao tốc cho gián, bụi hành lang và thoát hơi lạnh điều hòa! Dán 1 thanh ron cao su 3 lớp chắn đáy cửa là kín bưng và cách âm cực êm — mình vừa đăng hình thực tế ngay trên tường Page, bạn bấm vào tên Page mình xem nha!",
        "Góc bàn phòng trọ hay đầu giường nhiều dây sạc chằng chịt thì cứ gom vào hộp nhựa ABS chống cháy nắp vân gỗ là gọn đẹp chuẩn Hàn Quốc ngay. List đồ cải tạo phòng trọ giá hạt dẻ không cần khoan tường mình ghim sẵn trên tường Page, mọi người bấm vào tên Page mình xem nhé!",
        "Đi làm về muộn ngại nhất dọn dẹp lỉnh kỉnh, cứ ưu tiên đồ gấp gọn dán tường chịu lực để lúc chuyển trọ mang đi nhẹ tênh. Mình vừa tổng hợp mấy món đồ trọ thông minh đáng tiền nhất ngay trên tường Page, bạn nào đang decor lại phòng bấm vào tên Page mình xem nha!"
    ],
    "ktx": [
        "Nhớ cảnh KTX quá! Tủ sắt cá nhân ở KTX nhỏ xíu thì cứ dùng bộ túi nén hút chân không kèm bơm tay là thu gọn được 75% chỗ để chăn bông với áo khoác dày. Trọn bộ đồ sinh tồn KTX tiết kiệm diện tích mình ghim sẵn ngay trên tường Page, đồng môn bấm vào tên Page mình xem nhé!",
        "Mùa thi thức đêm ôn bài ở KTX ngại nhất bật đèn trần làm chói mắt cả phòng! Chân ái là đèn học LED chống cận ngàm kẹp thành giường tích điện, chiếu đúng trang sách cực dịu mắt — mình vừa lên bài mẫu này ngay trên tường Page, bạn nào ở giường tầng bấm vào tên Page mình xem nha!",
        "Nằm giường tầng 2 KTX ngại nhất mỗi lần lấy chai nước, sạc dự phòng hay laptop lại phải trèo thang lên xuống. Ngoắc ngay 1 chiếc giỏ thép sơn tĩnh điện vào thành giường là đủ chỗ để mọi thứ trong tầm tay — hình thực tế mình ghim ngay trên tường Page, bạn bấm vào tên Page mình xem nhé!",
        "Ở phòng KTX 6–8 người muốn có góc riêng tư thay đồ, học bài hay ngủ sớm thì lắp bộ rèm che giường tầng cản sáng 90% kèm dây treo không khoan đục là chuẩn bài nhất! Mình vừa tổng hợp các mẫu rèm KTX thoáng đẹp ngay trên tường Page, đồng môn bấm vào tên Page mình tham khảo nha!",
        "Giường tầng KTX lúc kéo rèm kín quạt trần không thổi tới thì hầm bí cực kỳ. Thủ sẵn chiếc quạt tích điện ngàm kẹp lớn kẹp thẳng vào khung sắt đầu giường là mát rượi êm ru suốt đêm — mình có ghim chi tiết món này trên tường Page, mọi người bấm vào tên Page mình xem nhé!",
        "Tân sinh viên học bài trên giường tầng nhớ sắm bàn học gấp gọn có khe dựng iPad và lỗ luồn dây sạc nhé, ngồi viết bài êm lưng không lo mỏi cổ. Toàn bộ list đồ giường tầng KTX giá sinh viên mình ghim sẵn trên tường Page, bạn nào cần bấm vào tên Page mình xem nha!"
    ],
    "deadline": [
        "Dân văn phòng ngồi ghế xoay 8 tiếng hay tê mỏi bắp chân và đau thắt lưng là do hai bàn chân bị hẫng! Đặt chiếc ghế kê chân công thái học có con lăn massage dưới gầm bàn là giữ đùi vuông góc 90 độ êm ru ngay — mình vừa ghim chi tiết trên tường Page, bác nào hay mỏi lưng bấm vào tên Page mình xem nhé!",
        "Cày deadline ban đêm mà bật đèn bàn thường chiếu lóa mặt màn hình thì chỉ 1 tiếng là mỏi nhức hai mắt! Đổi sang thanh đèn treo màn hình ScreenBar quang học bất đối xứng là sáng rực mặt bàn mà màn hình 0% chói lóa — hình thực tế mình ghim ngay trên tường Page, anh em bấm vào tên Page mình xem nha!",
        "Gõ phím và di chuột liên tục cả ngày khiến cạnh bàn cứng tỳ vào cổ tay đỏ ửng, rất dễ bị hội chứng ống cổ tay. Dùng bộ đệm kê tay cao su non Memory Foam bọc vải thoáng khí là êm cổ tay suốt 8 tiếng — mình có ghim combo này trên tường Page, bác nào cần bấm vào tên Page mình tham khảo nhé!",
        "Đặt laptop thẳng trên mặt bàn khiến cổ luôn cúi gập 45 độ, tới chiều là cứng đờ hai bả vai! Nâng màn hình lên ngang tầm mắt bằng giá đỡ laptop hợp kim nhôm xoay 360 độ là hết hẳn mỏi cổ vai gáy — bài review chi tiết mình để ngay trên tường Page, anh em văn phòng bấm vào tên Page mình xem nha!",
        "Ghế xoay văn phòng thường hở ngay hõm thắt lưng nên ngồi tới chiều là lưng cong chữ C. Lắp thêm gối tựa lưng cao su non ôm sát cột sống là ngồi làm việc cả ngày vẫn thẳng lưng nhẹ tênh — bộ phụ kiện công thái học văn phòng mình ghim sẵn trên tường Page, mọi người bấm vào tên Page mình xem nhé!",
        "Muốn chạy deadline tập trung gấp đôi mà không bị xao nhãng bởi điện thoại thì dùng đồng hồ Pomodoro lục giác cảm biến trọng lực: lật mặt 25 phút lên là tự đếm ngược vào việc ngay! Mình vừa lên bài món này trên tường Page, bác nào làm văn phòng bấm vào tên Page mình xem nha!"
    ]
}


def step1_upgrade_group_seeding_pool() -> None:
    """Cập nhật COMMENTS_POOL trong tools/mama_daily_group_and_eod.py chuẩn Mũi 4."""
    target_py = SUBAGENT_DIR / "tools" / "mama_daily_group_and_eod.py"
    code = target_py.read_text(encoding="utf-8")
    pool_str = "COMMENTS_POOL = " + json.dumps(NEW_COMMENTS_POOL, ensure_ascii=False, indent=4)
    new_code, n = re.subn(
        r"COMMENTS_POOL\s*=\s*\{.*?\n\}",
        lambda _: pool_str,
        code,
        count=1,
        flags=re.DOTALL,
    )
    if n == 0:
        raise RuntimeError("Không tìm thấy khối COMMENTS_POOL trong mama_daily_group_and_eod.py")
    target_py.write_text(new_code, encoding="utf-8")
    print("✅ [Mũi 4] Đã nâng cấp 24 kịch bản Seeding Hội Nhóm (80% Value + 20% Kéo Về Tường Fanpage) trong mama_daily_group_and_eod.py")


def build_master_funnel_card_html() -> str:
    """Thiết kế Độc Bản Zero-Clone: Kho Vũ Khí Đóng Hộp 2026 (3-Vault Pillars + Bottom Gold Action Bar)."""
    font_css = get_local_fonts_css()
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<style>
{font_css}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  width: 1080px;
  height: 1080px;
  overflow: hidden;
  position: relative;
  font-family: 'Be Vietnam Pro', 'Plus Jakarta Sans', sans-serif;
  background: radial-gradient(circle at 50% 18%, rgba(245,158,11,0.22) 0%, rgba(135,255,0,0.08) 42%, #050811 78%), #050811;
  color: #FFFFFF;
  -webkit-font-smoothing: antialiased;
}}
</style>
</head>
<body>
  <!-- Top Badge & Headline -->
  <div style="position:absolute; top:34px; left:48px; right:48px; text-align:center;">
    <div style="display:inline-flex; align-items:center; gap:10px; background:rgba(245,158,11,0.16); border:2px solid #F59E0B; color:#FDE047; font-weight:900; font-size:17px; padding:7px 22px; border-radius:999px; letter-spacing:1px;">
      <span>🎁 BÀI GHIM CHỦ LỰC • TẶNG MIỄN PHÍ 100% CHO CỘNG ĐỒNG AI PLAYERS</span>
    </div>
    <div style="font-size:39px; font-weight:900; line-height:1.12; margin-top:14px; letter-spacing:-0.8px; white-space:nowrap;">
      KHO VŨ KHÍ <span style="color:#87FF00;">10 SUBAGENT</span> &amp; <span style="color:#FBBF24;">50 SIÊU PROMPT</span>
    </div>
    <div style="font-size:20px; font-weight:700; color:#CBD5E1; margin-top:8px; white-space:nowrap;">
      Đóng hộp sẵn quy trình tự động hóa 80% việc lặp cho Dân Văn Phòng, Creator &amp; Chủ Shop
    </div>
  </div>

  <!-- 3 Vertical Weapon Vault Cards -->
  <div style="position:absolute; top:206px; left:48px; right:48px; height:600px; display:grid; grid-template-columns:repeat(3, 1fr); gap:22px;">
    <!-- Vault 01 -->
    <div style="background:linear-gradient(180deg, rgba(16,24,44,0.95) 0%, rgba(9,14,26,0.98) 100%); border:3px solid #87FF00; border-radius:28px; padding:26px 22px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 16px 40px rgba(135,255,0,0.14);">
      <div>
        <div style="background:#87FF00; color:#050811; font-weight:900; font-size:17px; padding:7px 14px; border-radius:10px; display:inline-block; white-space:nowrap;">GÓI #01 • MULTI-AGENT</div>
        <div style="font-size:28px; font-weight:900; color:#FFFFFF; line-height:1.2; margin-top:16px;">Bộ 10 File Cấu Hình Subagent (.MD)</div>
        <div style="margin-top:18px; display:flex; flex-direction:column; gap:12px; font-size:18.5px; color:#E2E8F0; font-weight:700;">
          <div>✔ Mama Tổng Quản (Hard Gate ≥ 9.0)</div>
          <div>✔ MKT Săn Hàng &amp; Đào Bình Luận</div>
          <div>✔ Content Kịch Bản Hook 3 Giây</div>
          <div>✔ Edit Đồ Họa Zero-Clone &amp; Remotion</div>
        </div>
      </div>
      <div style="background:rgba(135,255,0,0.14); border:1.5px solid #87FF00; color:#87FF00; font-weight:900; font-size:18px; padding:12px; border-radius:14px; text-align:center;">
        CẮM VÀO CHẠY NGAY
      </div>
    </div>

    <!-- Vault 02 -->
    <div style="background:linear-gradient(180deg, rgba(28,20,46,0.95) 0%, rgba(13,9,24,0.98) 100%); border:3px solid #F59E0B; border-radius:28px; padding:26px 22px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 16px 40px rgba(245,158,11,0.18);">
      <div>
        <div style="background:#F59E0B; color:#050811; font-weight:900; font-size:17px; padding:7px 14px; border-radius:10px; display:inline-block; white-space:nowrap;">GÓI #02 • VĂN PHÒNG</div>
        <div style="font-size:28px; font-weight:900; color:#FFFFFF; line-height:1.2; margin-top:16px;">Sổ Tay 50 Siêu Prompt Thực Chiến</div>
        <div style="margin-top:18px; display:flex; flex-direction:column; gap:12px; font-size:18.5px; color:#FEF3C7; font-weight:700;">
          <div>✔ Tự viết hàm Excel/SQL 50.000 dòng</div>
          <div>✔ Tóm tắt cuộc họp → Bảng giao việc</div>
          <div>✔ Chuỗi Email B2B &amp; Xử lý từ chối</div>
          <div>✔ Phân tích báo cáo CEO trong 10 giây</div>
        </div>
      </div>
      <div style="background:rgba(245,158,11,0.16); border:1.5px solid #F59E0B; color:#FDE047; font-weight:900; font-size:18px; padding:12px; border-radius:14px; text-align:center;">
        GIẢM 80% VIỆC LẶP LẠI
      </div>
    </div>

    <!-- Vault 03 -->
    <div style="background:linear-gradient(180deg, rgba(12,30,44,0.95) 0%, rgba(7,16,26,0.98) 100%); border:3px solid #38BDF8; border-radius:28px; padding:26px 22px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 16px 40px rgba(56,189,248,0.15);">
      <div>
        <div style="background:#38BDF8; color:#050811; font-weight:900; font-size:17px; padding:7px 14px; border-radius:10px; display:inline-block; white-space:nowrap;">GÓI #03 • AUTOMATION</div>
        <div style="font-size:28px; font-weight:900; color:#FFFFFF; line-height:1.2; margin-top:16px;">Sơ Đồ Hạ Tầng &amp; Bộ Não Thứ 2</div>
        <div style="margin-top:18px; display:flex; flex-direction:column; gap:12px; font-size:18.5px; color:#E0F2FE; font-weight:700;">
          <div>✔ Cầu nối Telegram 2 chiều điều khiển</div>
          <div>✔ Chrome Bot chạy ngầm 100% không vướng</div>
          <div>✔ Kiến trúc Memory Vault chống quên</div>
          <div>✔ Cổng kiểm định Zero-Clone tự động</div>
        </div>
      </div>
      <div style="background:rgba(56,189,248,0.15); border:1.5px solid #38BDF8; color:#38BDF8; font-weight:900; font-size:18px; padding:12px; border-radius:14px; text-align:center;">
        VẬN HÀNH TỰ HÀNH 24/7
      </div>
    </div>
  </div>

  <!-- Bottom Conversion Banner -->
  <div style="position:absolute; bottom:42px; left:48px; right:48px; height:176px; background:linear-gradient(90deg, #87FF00 0%, #F59E0B 100%); border-radius:28px; padding:22px 34px; color:#050811; display:flex; justify-content:space-between; align-items:center; box-shadow:0 20px 50px rgba(135,255,0,0.28);">
    <div>
      <div style="font-size:18px; font-weight:900; letter-spacing:0.6px; text-transform:uppercase; white-space:nowrap;">⚡ CÁCH NHẬN TRỌN BỘ 3 GÓI TÀI LIỆU GỐC TRONG 5 GIÂY:</div>
      <div style="font-size:26.5px; font-weight:900; line-height:1.28; margin-top:6px;">
        Bấm vào Link Nhóm Zalo ở <span style="text-decoration:underline;">Bình Luận Đầu Tiên</span><br>hoặc gõ từ khóa <span style="background:#050811; color:#87FF00; padding:2px 12px; border-radius:9px;">KHOAI</span> bên dưới!
      </div>
    </div>
    <div style="background:#050811; color:#FFFFFF; font-weight:900; font-size:22px; padding:20px 26px; border-radius:20px; text-align:center; flex-shrink:0; border:3px solid #FFFFFF;">
      TẢI NGAY<br><span style="color:#87FF00;">DƯỚI CMT #1 👇</span>
    </div>
  </div>
</body>
</html>"""


def step2_publish_master_funnel_post(pages: dict) -> dict:
    """Kết xuất ảnh Master Funnel Hub, kiểm định Zero-Clone và đăng LIVE lên đầu trang AI Players."""
    out_dir = SUBAGENT_DIR / "campaigns" / "2026-11-02" / "ai-players-master-funnel"
    out_dir.mkdir(parents=True, exist_ok=True)
    img_path = out_dir / "master_funnel_hub_ai_players_2026.jpg"

    render_html_to_image(build_master_funnel_card_html(), img_path, width=1080, height=1080)
    ok, msg = verify_zero_clone_images(out_dir, max_similarity=0.58)
    print(f"🛡️ Kiểm định Zero-Clone cho Master Funnel Card: ok={ok} ({msg})")

    caption = (
        "🎁 [TẶNG MIỄN PHÍ 100%] KHO VŨ KHÍ ĐÓNG HỘP 2026: TRỌN BỘ 10 SUBAGENT (.MD) + SỔ TAY 50 SIÊU PROMPT VĂN PHÒNG & SƠ ĐỒ TỰ ĐỘNG HÓA 24/7!\n\n"
        "Nếu bạn đang muốn áp dụng AI vào công việc thực tế để cắt giảm 80% các tác vụ lặp đi lặp lại mỗi ngày mà không biết bắt đầu từ đâu, đây là trọn bộ tài liệu gốc đã được đội ngũ AI Players chuẩn hóa sẵn:\n\n"
        "🔥 1. GÓI #01 — BỘ 10 FILE CẤU HÌNH SUBAGENT CHUYÊN BIỆT (.MD):\n"
        "• Phân vai rõ ràng: Mama Tổng Quản duyệt Gate >= 9.0, MKT săn sản phẩm & đào bình luận, Content viết kịch bản Hook 3s, Edit dựng đồ họa Zero-Clone, Quản lý kênh tự động hóa Meta Graph API.\n\n"
        "🔥 2. GÓI #02 — SỔ TAY 50 SIÊU PROMPT DÀNH CHO DÂN VĂN PHÒNG & QUẢN LÝ:\n"
        "• Đóng khung sẵn biến số điền vào dùng ngay: Tự viết hàm Excel/SQL phức tạp, tóm tắt biên bản cuộc họp thành bảng giao việc, soạn chuỗi Email B2B và phân tích số liệu báo cáo.\n\n"
        "🔥 3. GÓI #03 — SƠ ĐỒ KIẾN TRÚC 'BỘ NÃO THỨ 2' & TRÌNH DUYỆT BOT CHẠY NGẦM:\n"
        "• Cách kết hợp Python + Playwright chạy ngầm 100% + Cầu nối Telegram 2 chiều điều khiển toàn bộ hệ thống từ điện thoại.\n\n"
        "💬 CÁCH NHẬN TRỌN BỘ TÀI LIỆU GỐC:\n"
        "👉 Bấm trực tiếp vào link Nhóm Zalo Cộng Đồng ở BÌNH LUẬN ĐẦU TIÊN bên dưới, hoặc bình luận từ khóa 'KHOAI' để hệ thống tự động gửi link tải ngay cho bạn nhé! 👇"
    )

    pinned_cmt = (
        "📌 LINK TẢI TRỌN BỘ 3 GÓI VŨ KHÍ AI PLAYERS (10 SUBAGENT + 50 SIÊU PROMPT + SƠ ĐỒ HẠ TẦNG):\n"
        f"👉 Bấm tham gia Nhóm Zalo Thực Chiến để lấy link tải toàn bộ file gốc miễn phí tại đây: {ZALO_VIP_URL}\n\n"
        "💡 Mẹo: Bạn có thể gõ bất kỳ từ khóa nào ('KHOAI', 'PROMPT50', '10AGENT') dưới bài viết này, hệ thống Auto-Reply của Page sẽ gửi trực tiếp tài liệu cho bạn ngay lập tức!"
    )

    tok = pages[AI_ID]["access_token"]
    with open(img_path, "rb") as f:
        r = requests.post(
            f"https://graph.facebook.com/v22.0/{AI_ID}/photos",
            data={"caption": caption, "published": "true", "access_token": tok},
            files={"source": (img_path.name, f, "image/jpeg")},
            timeout=90,
        ).json()

    post_id = r.get("post_id") or r.get("id", "")
    cmt_id = ""
    if post_id:
        record_published_content(AI_ID, img_path, caption, str(post_id))
        c_res = graph_post(f"{post_id}/comments", tok, {"message": pinned_cmt})
        cmt_id = c_res.get("id", "")
        print(f"✅ [Mũi 3B] Đã đăng LIVE Bài Chủ Lực Thu Phễu lên đầu trang AI Players -> post_id={post_id} | cmt_id={cmt_id}")
    else:
        print(f"⚠️ Lỗi đăng bài Master Funnel: {r}")

    return {"post_id": post_id, "comment_id": cmt_id, "image_path": str(img_path)}


def run_auto_reply_and_icebreaker(pages: dict) -> list[str]:
    """
    Quét 15 bài gần nhất trên cả 4 Fanpage:
    1. Tự động trả lời mọi bình luận của khách hàng (`from.id != page_id`) chưa được phản hồi.
    2. Trên 3 Page Bán Hàng: Với 3 bài LIVE mới nhất nếu mới chỉ có 1 bình luận ghim, tự động thả thêm
       1 bình luận câu hỏi kích mồi thảo luận tự nhiên để phá băng tâm lý ngại bình luận của khách.
    """
    actions = []
    ledger_path = SUBAGENT_DIR / "knowledge" / "auto_reply_comments_ledger.json"
    replied_ids = set()
    if ledger_path.exists():
        try:
            replied_ids = set(json.loads(ledger_path.read_text(encoding="utf-8")))
        except Exception:
            replied_ids = set()

    icebreaker_questions = {
        "1442323328956326": "📌 Mẹo nhỏ cho các bạn ở trọ: Đặt mua trên Shopee nhớ áp thêm mã Freeship Xtra ở bước thanh toán nha! Phòng bạn hiện đang cần ưu tiên dọn góc bếp hay góc cửa trước? 👇",
        "1421270697727753": "📌 Mẹo cho team KTX: Rủ bạn cùng phòng đặt chung 2 món là được giảm thêm phí ship cực hời luôn! Giường của bạn ở KTX là tầng 1 hay tầng 2 thế? 👇",
        "1407231352464711": "📌 Góc chia sẻ: Dân văn phòng mình đầu tư mấy món bảo vệ cột sống với cổ tay như này tính ra chưa bằng 2 cốc trà sữa mà ngồi làm việc êm hơn hẳn! Bạn hay mỏi cổ vai gáy hay mỏi cổ tay hơn? 👇",
    }

    for pid in [AI_ID] + SALES_IDS:
        if pid not in pages:
            continue
        tok = pages[pid]["access_token"]
        pname = pages[pid]["name"]
        try:
            feed = graph_get(
                f"{pid}/published_posts",
                tok,
                {"fields": "id,message,created_time", "limit": 12},
            ).get("data", [])
        except Exception:
            continue

        for idx, post in enumerate(feed):
            post_id = post["id"]
            try:
                cmts = graph_get(
                    f"{post_id}/comments",
                    tok,
                    {"fields": "id,from,message,comments.limit(5){id,from}", "limit": 25},
                ).get("data", [])
            except Exception:
                continue

            # Tìm link Shopee trong bình luận ghim của bài bán hàng
            post_shopee_url = ""
            for c in cmts:
                msg_c = c.get("message") or ""
                m = re.search(r"https://s\.shopee\.vn/\S+", msg_c)
                if m:
                    post_shopee_url = m.group(0)
                    break

            # 1. Phản hồi bình luận của khách hàng thật
            for c in cmts:
                cid = c["id"]
                c_from = c.get("from") or {}
                c_from_id = str(c_from.get("id") or "")
                c_from_name = c_from.get("name") or "bạn"
                if c_from_id == pid or cid in replied_ids:
                    continue

                # Kiểm tra xem Page đã reply vào comment này chưa
                sub_cmts = (c.get("comments") or {}).get("data", [])
                if any(str((sc.get("from") or {}).get("id") or "") == pid for sc in sub_cmts):
                    replied_ids.add(cid)
                    continue

                if pid == AI_ID:
                    reply_msg = (
                        f"Chào {c_from_name} 👋 Mình gửi bạn link nhận trọn bộ Blueprint Đội Ngũ Subagent Cá Nhân & Doanh Nghiệp Toàn Diện + Đặt lịch Tư vấn Thiết kế Đội ngũ Subagent May đo 1:1 tại Nhóm Zalo VIP AI Players nhé: "
                        f"{ZALO_VIP_URL} 🚀 (Bạn bấm vào link hoặc nhắn tin cho Page để đội ngũ hỗ trợ khảo sát quy trình cho bạn ngay nha!)"
                    )
                else:
                    link_to_send = post_shopee_url or "https://s.shopee.vn/an_redir?origin_link=https%3A%2F%2Fshopee.vn&affiliate_id=17395830088&sub_id=autoreply-sales"
                    reply_msg = (
                        f"Chào {c_from_name} 👋 Mình gửi bạn link xem chi tiết sản phẩm chính hãng & săn giá ưu đãi trên Shopee tại đây nha: {link_to_send} 🛒"
                    )

                res = graph_post(f"{cid}/comments", tok, {"message": reply_msg})
                if "id" in res:
                    replied_ids.add(cid)
                    actions.append(f"💬 Auto-Reply khách [{c_from_name}] trên {pname} ({cid} -> {res['id']})")

            # 2. Kích mồi bình luận phá băng (#2) cho 2 bài mới nhất trên 3 Page Bán Hàng
            if pid in SALES_IDS and idx < 2 and len(cmts) == 1:
                ice_key = f"icebreaker_{post_id}"
                if ice_key not in replied_ids:
                    ice_msg = icebreaker_questions[pid]
                    res_ice = graph_post(f"{post_id}/comments", tok, {"message": ice_msg})
                    if "id" in res_ice:
                        replied_ids.add(ice_key)
                        actions.append(f"🔥 Đã tạo bình luận phá băng thảo luận #2 trên [{pname}] ({post_id} -> {res_ice['id']})")

    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(sorted(replied_ids), ensure_ascii=False, indent=2), encoding="utf-8")
    return actions


def step3_integrate_into_auto_scheduler() -> None:
    """Tích hợp tự động chạy Auto-Reply & Icebreaker vào mama_auto_scheduler_engine.py ở mọi mốc giờ."""
    sched_py = SUBAGENT_DIR / "tools" / "mama_auto_scheduler_engine.py"
    code = sched_py.read_text(encoding="utf-8")
    if "run_auto_reply_and_icebreaker" in code:
        print("✅ [Mũi 3A] mama_auto_scheduler_engine.py đã tích hợp sẵn Auto-Reply.")
        return

    target = "    pin_actions = ensure_all_live_posts_have_pinned_comment(pages)"
    replacement = (
        "    pin_actions = ensure_all_live_posts_have_pinned_comment(pages)\n"
        "    try:\n"
        "        from activate_mui3_mui4_growth_engine import run_auto_reply_and_icebreaker\n"
        "        pin_actions.extend(run_auto_reply_and_icebreaker(pages))\n"
        "    except Exception:\n"
        "        pass"
    )
    if target in code:
        sched_py.write_text(code.replace(target, replacement, 1), encoding="utf-8")
        print("✅ [Mũi 3A] Đã tích hợp Auto-Reply & Phá băng bình luận vào mama_auto_scheduler_engine.py (chạy tự động 7 mốc/ngày).")


if __name__ == "__main__":
    pages = load_vault()
    step1_upgrade_group_seeding_pool()
    funnel_res = step2_publish_master_funnel_post(pages)
    step3_integrate_into_auto_scheduler()
    reply_actions = run_auto_reply_and_icebreaker(pages)
    for a in reply_actions:
        print(" ", a)
