#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_sales_bold_editorial.py — Bộ Kết Xuất Typography Dày Dặn & Có Điểm Nhấn Cho 3 Page Bán Hàng
====================================================================================================
Kết hợp:
1. Ảnh chụp sản phẩm thật chuẩn Studio Photorealistic (Editorial Macro & 3-Detail Grid:
   Sản phẩm góc 3/4 trung tâm trái + Cận cảnh chất liệu Macro góc trên phải + 3 Ô vuông chi tiết đáy).
2. Lớp Typography HTML/CSS/SVG kết xuất bằng Headless Chrome (1080×1080) với:
   - Font chữ cực dày dặn (Be Vietnam Pro Black 900 / ExtraBold 800, không dùng chữ mảnh mờ nhạt).
   - Điểm nhấn thị giác mạnh (High-Impact Accent Highlight Block có gờ nổi 3D, huy hiệu Page tương phản cao,
     3 thẻ thông số đóng khung đậm, 3 thanh tính năng đánh số 01-02-03 dưới ảnh Macro, và tiêu đề 3 ô đáy dày dặn).
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
    - Nếu là ảnh raw mới sinh không chữ (`erase_legacy_text=False`): giữ nguyên 100% ảnh sản phẩm & bóng đổ tự nhiên!
    - Nếu là ảnh mẫu cũ có chữ sẵn (`erase_legacy_text=True`): xóa vùng chữ cũ bằng màu nền Studio.
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
    spec_pills: list[str],
    macro_points: list[tuple[str, str]],
    detail_items: list[tuple[str, str]],
    accent_hex: str = "#EA580C",
    accent_dark_hex: str = "#9A3412",
    secondary_hex: str = "#0F172A",
) -> str:
    """
    Sinh HTML/CSS 1080×1080 với Typography dày dặn (font-weight: 800-900), 1 dòng gọn gàng không đè hình.
    """
    font_css = get_local_fonts_css()

    # Tự động cân chỉnh cỡ chữ tiêu đề để luôn nằm gọn trên 1 dòng duy nhất (không rớt dòng đè lên sản phẩm)
    len1 = len(title_line1)
    size1 = 52 if len1 <= 14 else (46 if len1 <= 17 else 41)

    len2 = len(title_highlight)
    size2 = 44 if len2 <= 16 else (39 if len2 <= 20 else 35)

    pills_html = "".join(
        f'<span class="spec-pill"><span class="dot">●</span>{sp}</span>'
        for sp in spec_pills
    )

    macro_html = ""
    for idx, (kw, rest) in enumerate(macro_points, 1):
        macro_html += f"""
        <div class="macro-row">
          <span class="macro-num">0{idx}</span>
          <span class="macro-txt"><b class="kw">{kw}</b> {rest}</span>
        </div>
        """

    box_lefts = [42, 384, 726]
    details_html = ""
    for idx, ((d_title, d_sub), left_px) in enumerate(zip(detail_items, box_lefts), 1):
        details_html += f"""
        <!-- Nhãn số góc trên trái mỗi ô vuông chi tiết -->
        <div style="position:absolute; top:746px; left:{left_px + 10}px; background:{accent_hex}; color:#FFFFFF; font-weight:900; font-size:14px; padding:4px 10px; border-radius:7px; box-shadow:0 4px 10px rgba(0,0,0,0.32); letter-spacing:0.5px;">
          #{idx:02d}
        </div>
        <!-- Khung chữ dày dặn dưới mỗi ô vuông -->
        <div style="position:absolute; top:964px; left:{left_px - 6}px; width:324px; text-align:center; display:flex; flex-direction:column; align-items:center;">
          <div style="background:{secondary_hex}; color:#FFFFFF; font-weight:900; font-size:18.5px; line-height:1.15; padding:6px 15px; border-radius:8px; letter-spacing:-0.2px; box-shadow:0 3px 0 {accent_hex}; white-space:nowrap;">
            {d_title}
          </div>
          <div style="margin-top:6px; font-weight:800; font-size:16px; color:#1E293B; line-height:1.22; white-space:nowrap;">
            {d_sub}
          </div>
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
  font-family: 'Be Vietnam Pro', 'Plus Jakarta Sans', sans-serif;
  background-color: {bg_css_color};
  background-image: url('{bg_data_uri}');
  background-size: 1080px 1080px;
  background-repeat: no-repeat;
  -webkit-font-smoothing: antialiased;
}}

.page-pill {{
  display: inline-flex;
  align-items: center;
  gap: 9px;
  background: {secondary_hex};
  color: #FFFFFF;
  font-weight: 900;
  font-size: 16.5px;
  letter-spacing: 1px;
  padding: 8px 20px;
  border-radius: 999px;
  border: 2px solid {accent_hex};
  box-shadow: 0 4px 0 {accent_hex}, 0 8px 18px rgba(15,23,42,0.15);
  text-transform: uppercase;
  white-space: nowrap;
}}

.page-pill .badge-dot {{
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: {accent_hex};
  box-shadow: 0 0 8px {accent_hex};
}}

.hero-title-line1 {{
  margin-top: 12px;
  font-weight: 900;
  font-size: {size1}px;
  line-height: 1.04;
  letter-spacing: -1.5px;
  color: {secondary_hex};
  text-transform: uppercase;
  text-shadow: 0 2px 0 rgba(255,255,255,0.95);
  white-space: nowrap;
}}

.hero-title-highlight {{
  display: inline-block;
  margin-top: 7px;
  background: {accent_hex};
  color: #FFFFFF;
  font-weight: 900;
  font-size: {size2}px;
  line-height: 1.06;
  letter-spacing: -1.1px;
  padding: 6px 18px 9px 18px;
  border-radius: 13px;
  box-shadow: 0 6px 0 {accent_dark_hex}, 0 12px 22px rgba(15,23,42,0.18);
  text-transform: uppercase;
  white-space: nowrap;
}}

.spec-row {{
  margin-top: 14px;
  display: flex;
  flex-wrap: nowrap;
  gap: 8px;
}}

.spec-pill {{
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #FFFFFF;
  color: {secondary_hex};
  font-weight: 800;
  font-size: 15.5px;
  padding: 6px 12px;
  border-radius: 9px;
  border: 2.5px solid {secondary_hex};
  box-shadow: 0 3px 0 {secondary_hex};
  white-space: nowrap;
}}

.spec-pill .dot {{
  color: {accent_hex};
  font-size: 12px;
}}

.macro-box {{
  position: absolute;
  top: 560px;
  left: 615px;
  right: 22px;
  display: flex;
  flex-direction: column;
  gap: 7px;
}}

.macro-row {{
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255,255,255,0.96);
  border: 2.5px solid {secondary_hex};
  border-left: 7px solid {accent_hex};
  border-radius: 10px;
  padding: 6px 10px;
  box-shadow: 0 4px 10px rgba(15,23,42,0.08);
  overflow: hidden;
}}

.macro-num {{
  background: {accent_hex};
  color: #FFFFFF;
  font-weight: 900;
  font-size: 12.5px;
  padding: 3px 6px;
  border-radius: 5px;
  flex-shrink: 0;
}}

.macro-txt {{
  font-weight: 800;
  font-size: 11.8px;
  color: {secondary_hex};
  line-height: 1.15;
  text-transform: uppercase;
  letter-spacing: -0.3px;
  white-space: nowrap;
}}

.macro-txt .kw {{
  color: {accent_hex};
  font-weight: 900;
}}
</style>
</head>
<body>
  <!-- Góc trên trái: Huy hiệu Page + Tiêu đề dày dặn 1 dòng có khối Highlight + 3 Thẻ Spec -->
  <div style="position:absolute; top:28px; left:38px; width:640px;">
    <div class="page-pill">
      <span class="badge-dot"></span>
      <span>{page_badge}</span>
    </div>
    <div class="hero-title-line1">{title_line1}</div>
    <div class="hero-title-highlight">{title_highlight}</div>
    <div class="spec-row">
      {pills_html}
    </div>
  </div>

  <!-- Cột phải dưới ảnh Macro: 3 Thanh Điểm Nhấn Đánh Số 01-02-03 -->
  <div class="macro-box">
    {macro_html}
  </div>

  <!-- Dải đáy: 3 Ô Vuông Chi Tiết kèm Tiêu Đề Đóng Khung Đậm -->
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
        page_badge="PHÒNG TRỌ HẾT CỨU • DEAL CHUẨN",
        title_line1="MÁY HÚT BỤI",
        title_highlight="CẦM TAY MINI 2-IN-1",
        spec_pills=["Không Dây Gọn Nhẹ", "Lực Hút Mạnh", "Sạc Nhanh Type-C"],
        macro_points=[
            ("LÕI LỌC HEPA", "RỬA SẠCH DƯỚI VÒI NƯỚC"),
            ("HỘP BỤI TRONG", "QUAN SÁT BỤI ĐẦY TỨC THÌ"),
            ("CỔNG TYPE-C", "DÙNG CHUNG SẠC ĐIỆN THOẠI"),
        ],
        detail_items=[
            ("ĐẦU HÚT KHE 2-IN-1", "Hút sạch rãnh cửa, góc nệm"),
            ("LÕI HEPA GIẶT ĐƯỢC", "Tái sử dụng bền bỉ, tiết kiệm"),
            ("SẠC NHANH TYPE-C", "Đầy pin nhanh, dùng mọi nơi"),
        ],
        accent_hex="#EA580C",
        accent_dark_hex="#9A3412",
        secondary_hex="#0F172A",
    )
    render_html_to_image(html, out, width=1080, height=1080)
    print("Rendered bold preview:", out)
