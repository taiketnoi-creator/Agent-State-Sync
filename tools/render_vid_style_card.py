#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_vid_style_card.py — Core Headless Chrome HTML/SVG-to-Image Engine (1080×1080)
====================================================================================
LƯU Ý QUAN TRỌNG (LUẬT #1 & LUẬT #9 — ZERO-CLONE BESPOKE IMAGE DESIGN):
- ĐÃ XÓA VĨNH VIỄN 5 hàm template cố định cũ (render_template_hero_showcase,
  render_template_curriculum_breakdown, render_template_feature_matrix,
  render_template_offer_card, render_template_urgency_slots) theo lệnh CEO.
- File này CHỈ cung cấp bộ nạp Font TTF Offline (get_local_fonts_css) và hàm kết xuất
  Headless Chrome (render_html_to_image).
- Mọi bài ảnh đăng lên Page "AI Players - Người chơi hệ AI" BẮT BUỘC được thiết kế
  độc bản 100% (1 Bài Ảnh = 1 Kiến Trúc Bố Cục Không Gian + 1 Bảng Màu Nhấn + 1 Đồ Họa
  SVG riêng biệt) tại `tools/build_bespoke_ai_players_images.py` và đi qua cổng
  `verify_zero_clone_images()` trong `tools/zero_repost_gate.py`.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
FONT_CSS_PATH = SUBAGENT_DIR / "brand-kit" / "fonts" / "local_ttf_fonts.css"
ASSETS_DIR = SUBAGENT_DIR / "brand-kit" / "vid_assets"

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def find_browser() -> str:
    if os.path.exists(CHROME_PATH):
        return CHROME_PATH
    if os.path.exists(EDGE_PATH):
        return EDGE_PATH
    raise FileNotFoundError("Neither Chrome nor Edge found.")


def get_local_fonts_css() -> str:
    if FONT_CSS_PATH.exists():
        return FONT_CSS_PATH.read_text(encoding="utf-8")
    return ""


def render_html_to_image(html_content: str, output_path: Path, width: int = 1080, height: int = 1080) -> None:
    """Kết xuất HTML/CSS/SVG độc bản thành ảnh 1080×1080 sắc nét bằng Headless Chrome."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    browser = find_browser()
    with tempfile.TemporaryDirectory() as tmpdir:
        html_file = Path(tmpdir) / "card.html"
        raw_png = Path(tmpdir) / "raw.png"
        user_data_dir = Path(tmpdir) / "chrome_user_data"
        html_file.write_text(html_content, encoding="utf-8")

        cmd = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            "--virtual-time-budget=1200",
            f"--user-data-dir={user_data_dir}",
            f"--window-size={width + 140},{height + 180}",
            f"--screenshot={raw_png}",
            html_file.as_uri(),
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            raise RuntimeError(f"Browser render failed: {res.stderr.decode('utf-8', errors='ignore')}")

        with Image.open(raw_png) as im:
            im = im.crop((0, 0, width, height))
            if str(output_path).lower().endswith((".jpg", ".jpeg")):
                im.convert("RGB").save(output_path, format="JPEG", quality=96, subsampling=0, optimize=True)
            else:
                im.save(output_path, format="PNG", optimize=True)
