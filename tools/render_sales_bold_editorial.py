#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_sales_bold_editorial.py — Bộ Kết Xuất Minimal Pop-Bold Typography Cho 3 Page Bán Hàng
=============================================================================================
Triết lý thiết kế theo chỉ đạo của CEO:
- ÍT TEXT TỐI ĐA (Bỏ toàn bộ tag phụ, bỏ spec pills, bỏ thanh 01-02-03, không làm rối mắt).
- TEXT CHÍNH DÀY DẶN & MÀU SẮC BẮT MẮT:
  + Góc trên trái CHỈ hiển thị đúng 2 dòng Tiêu Đề Chính cỡ đại (54px–68px, Font Black 900 cực dày)
    với bảng màu rực rỡ bắt mắt (Dòng 1 chữ dày có viền nổi 3D + Dòng 2 bọc Khối Màu Nổi 3D).
  + Dưới 3 ô chi tiết đáy chỉ gắn nhãn ngắn 2–3 từ gọn gàng ở sát mép dưới.
"""

import base64
import sys
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SUBAGENT_DIR / "tools"))
from render_vid_style_card import get_local_fonts_css, render_html_to_image


def clean_photo_zones_to_data_uri(src_image_path: Path, erase_legacy_text: bool = False) -> tuple[str, str]:
    """
    Chuẩn hóa ảnh gốc về 1080×1080.
    - Ảnh raw mới sinh không chữ (`erase_legacy_text=False`): giữ nguyên 100% ảnh sản phẩm & nền Studio.
    - Ảnh mẫu cũ có chữ sẵn (`erase_legacy_text=True`): xóa vùng chữ cũ bằng màu nền Studio.
    """
    with Image.open(src_image_path) as im:
        canvas = im.convert("RGB").resize((1080, 1080), Image.Resampling.LANCZOS)

    bg_rgb = canvas.getpixel((12, 12))
    if erase_legacy_text:
        draw = ImageDraw.Draw(canvas)
        draw.rectangle([0, 0, 680, 350], fill=bg_rgb)
        draw.rectangle([660, 560, 1080, 752], fill=bg_rgb)
        draw.rectangle([0, 966, 1080, 1080], fill=bg_rgb)

    buf = BytesIO()
    canvas.save(buf, format="JPEG", quality=96)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}", f"rgb({bg_rgb[0]}, {bg_rgb[1]}, {bg_rgb[2]})"


def build_bold_sales_card_html(
    bg_data_uri: str,
    bg_css_color: str,
    page_badge: str,
    title_line1: str,
    title_highlight: str,
    spec_pills: list[str] | None = None,
    macro_points: list[tuple[str, str]] | None = None,
    detail_items: list[tuple[str, str]] | None = None,
    accent_hex: str = "#FF3D00",
    accent_dark_hex: str = "#9A1B00",
    secondary_hex: str = "#111827",
) -> str:
    """
    Sinh HTML/CSS 1080×1080 chuẩn Minimal Pop-Bold:
    - Ít chữ tối đa: Góc trên trái chỉ có đúng 2 dòng TEXT CHÍNH siêu dày, màu sắc rực rỡ bắt mắt.
    - 3 ô chi tiết đáy chỉ gắn nhãn 2-3 từ gọn gàng.
    """
    font_css = get_local_fonts_css()

    # Cỡ chữ tiêu đề chính cực dày & lớn nhưng luôn gọn trên 1 dòng
    len1 = len(title_line1)
    size1 = 68 if len1 <= 12 else (60 if len1 <= 15 else (53 if len1 <= 18 else 47))

    len2 = len(title_highlight)
    size2 = 52 if len2 <= 15 else (46 if len2 <= 18 else (41 if len2 <= 21 else 37))

    # Nhãn ngắn gọn duy nhất dưới mỗi ô chi tiết (chỉ 2-3 từ, đặt sát mép dưới không che ảnh)
    box_lefts = [42, 384, 726]
    details_html = ""
    if detail_items:
        for (d_title, _), left_px in zip(detail_items[:3], box_lefts):
            details_html += f"""
            <div style="position:absolute; top:994px; left:{left_px - 4}px; width:320px; display:flex; justify-content:center;">
              <div class="detail-pill">{d_title}</div>
            </div>
            """

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
  font-family: 'Be Vietnam Pro', 'Montserrat', sans-serif;
  background-color: {bg_css_color};
  background-image: url('{bg_data_uri}');
  background-size: 1080px 1080px;
  background-repeat: no-repeat;
  -webkit-font-smoothing: antialiased;
}}

.hero-title-line1 {{
  font-weight: 900;
  font-size: {size1}px;
  line-height: 1.04;
  letter-spacing: -2px;
  color: {accent_hex};
  text-transform: uppercase;
  -webkit-text-stroke: 2.5px {secondary_hex};
  paint-order: stroke fill;
  text-shadow:
    0 5px 0 {secondary_hex},
    0 10px 20px rgba(0,0,0,0.14);
  white-space: nowrap;
}}

.hero-title-highlight {{
  display: inline-block;
  margin-top: 14px;
  background: {accent_hex};
  color: #FFFFFF;
  font-weight: 900;
  font-size: {size2}px;
  line-height: 1.05;
  letter-spacing: -1.2px;
  padding: 11px 26px 14px 26px;
  border-radius: 18px;
  border: 3.5px solid {secondary_hex};
  box-shadow:
    0 8px 0 {secondary_hex},
    0 16px 28px rgba(0,0,0,0.18);
  text-transform: uppercase;
  white-space: nowrap;
}}

.detail-pill {{
  background: {secondary_hex};
  color: #FFFFFF;
  font-weight: 900;
  font-size: 19px;
  line-height: 1.1;
  letter-spacing: -0.2px;
  padding: 8px 22px;
  border-radius: 999px;
  border: 2.5px solid #FFFFFF;
  box-shadow: 0 4px 0 {accent_hex}, 0 8px 16px rgba(0,0,0,0.15);
  text-transform: uppercase;
  white-space: nowrap;
}}
</style>
</head>
<body>
  <!-- CHỈ 2 DÒNG TEXT CHÍNH SIÊU DÀY & MÀU BẮT MẮT Ở GÓC TRÊN TRÁI -->
  <div style="position:absolute; top:42px; left:42px;">
    <div class="hero-title-line1">{title_line1}</div>
    <div class="hero-title-highlight">{title_highlight}</div>
  </div>

  <!-- 3 Nhãn Ngắn Gọn Dưới 3 Ô Vuông Chi Tiết Đáy -->
  {details_html}
</body>
</html>"""


if __name__ == "__main__":
    src = SUBAGENT_DIR / "assets" / "sales-pages-image-styles" / "sales-style-master-macro-grid.jpg"
    out = SUBAGENT_DIR / "assets" / "sales-pages-image-styles" / "sales-style-master-macro-grid-bold-v2.jpg"
    uri, bg_col = clean_photo_zones_to_data_uri(src, erase_legacy_text=True)
    html = build_bold_sales_card_html(
        bg_data_uri=uri,
        bg_css_color=bg_col,
        page_badge="",
        title_line1="MÁY HÚT BỤI",
        title_highlight="CẦM TAY MINI 2-IN-1",
        detail_items=[
            ("ĐẦU HÚT 2-IN-1", ""),
            ("LÕI LỌC RỬA ĐƯỢC", ""),
            ("SẠC NHANH TYPE-C", ""),
        ],
        accent_hex="#FF3D00",
        accent_dark_hex="#9A1B00",
        secondary_hex="#111827",
    )
    render_html_to_image(html, out, width=1080, height=1080)
    print("Rendered clean bold preview:", out)
