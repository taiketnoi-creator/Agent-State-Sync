#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_vid_style_card.py — Render Visual Cards Matching c:\\Users\\guicci\\Downloads\\vid Exact Style
For Page AI Players (1022527194267367)

Style DNA from Downloads\\vid (ref_1 to ref_8):
- Background: Deep carbon black (#07080a) with subtle checkered grid pattern
- Colors: Electric Neon Lime (#CCFF00), Hot Pink (#FF2A6D), Crisp White (#FFFFFF), Deep Black (#000000)
- Badges: Skewed parallelogram (#FF2A6D) with ✦ star, lime pills (#CCFF00)
- Typography: Heavy sans-serif (Montserrat 900), bracketed titles [ TITLE ], condensed 3D headers
- Devices: Glossy 3D squircle app icon + vector cursor ↖, 3D neon cyber perspective grid tunnel,
           2x2 outline pill matrix, 4-row curriculum list with giant numbers, 8-directional asterisk star logo.
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def find_browser() -> str:
    if os.path.exists(CHROME_PATH):
        return CHROME_PATH
    if os.path.exists(EDGE_PATH):
        return EDGE_PATH
    raise FileNotFoundError("Neither Chrome nor Edge found.")

def render_html_to_image(html_content: str, output_path: Path, width: int = 1080, height: int = 1080) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    browser = find_browser()
    with tempfile.TemporaryDirectory() as tmpdir:
        html_file = Path(tmpdir) / "card.html"
        raw_png = Path(tmpdir) / "raw.png"
        user_data_dir = Path(tmpdir) / "chrome_user_data"
        html_file.write_text(html_content, encoding="utf-8")

        # Give generous window margin so Chrome viewport is guaranteed >= width x height on Windows
        cmd = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--user-data-dir={user_data_dir}",
            f"--window-size={width + 120},{height + 170}",
            f"--screenshot={raw_png}",
            str(html_file),
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            raise RuntimeError(f"Browser render failed: {res.stderr.decode('utf-8', errors='ignore')}")

        with Image.open(raw_png) as im:
            # Crop exact width x height from top-left
            im = im.crop((0, 0, width, height))
            if str(output_path).lower().endswith(".jpg") or str(output_path).lower().endswith(".jpeg"):
                im.convert("RGB").save(output_path, format="JPEG", quality=95, optimize=True)
            else:
                im.save(output_path, format="PNG", optimize=True)


# ==============================================================================
# SVG ASSETS & ICONS
# ==============================================================================

CURSOR_SVG = """
<svg class="cursor-pointer" width="46" height="46" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M3 3L10.5 21L13.5 13.5L21 10.5L3 3Z" fill="#18181B" stroke="#FFFFFF" stroke-width="1.8" stroke-linejoin="round"/>
</svg>
"""

ZOOM_LOGO_SVG = """
<svg height="28" viewBox="0 0 120 30" fill="none" xmlns="http://www.w3.org/2000/svg">
  <text x="0" y="24" font-family="'Montserrat', sans-serif" font-weight="900" font-size="28" fill="#FFFFFF" letter-spacing="-1">zoom</text>
  <rect x="74" y="8" width="16" height="12" rx="3" fill="#2D8CFF"/>
  <polygon points="91,11 98,7 98,21 91,17" fill="#2D8CFF"/>
</svg>
"""

ASTERISK_LOGO_SVG = """
<svg width="74" height="74" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="13" fill="#CCFF00"/>
  <rect x="43" y="6" width="14" height="26" rx="7" fill="#CCFF00"/>
  <rect x="43" y="68" width="14" height="26" rx="7" fill="#CCFF00"/>
  <rect x="6" y="43" width="26" height="14" rx="7" fill="#CCFF00"/>
  <rect x="68" y="43" width="26" height="14" rx="7" fill="#CCFF00"/>
  <path d="M22 22 L36 36 M22 36 L22 22 L36 22" stroke="#CCFF00" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M78 22 L64 36 M78 36 L78 22 L64 22" stroke="#CCFF00" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M22 78 L36 64 M22 64 L22 78 L36 78" stroke="#CCFF00" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M78 78 L64 64 M78 64 L78 78 L64 78" stroke="#CCFF00" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

CORNER_BRACKETS_SVG = """
<div class="corner-bracket top-left"></div>
<div class="corner-bracket top-right"></div>
<div class="corner-bracket bottom-left"></div>
<div class="corner-bracket bottom-right"></div>
"""

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,600;0,700;0,800;0,900;1,800;1,900&family=Inter:wght@400;500;600;700;800&family=Chakra+Petch:wght@700;800;900&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  width: 1080px;
  height: 1080px;
  overflow: hidden;
  background-color: #07080a;
  background-image: 
    radial-gradient(circle at 50% 50%, rgba(26, 32, 42, 0.45) 0%, rgba(7, 8, 10, 0.98) 100%),
    linear-gradient(45deg, #111317 25%, transparent 25%, transparent 75%, #111317 75%, #111317),
    linear-gradient(45deg, #111317 25%, #07080a 25%, #07080a 75%, #111317 75%, #111317);
  background-size: 100% 100%, 72px 72px, 72px 72px;
  background-position: 0 0, 0 0, 36px 36px;
  font-family: 'Montserrat', sans-serif;
  color: #FFFFFF;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 30px;
}

/* Skewed hot pink badge */
.badge-pink-skew {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: #FF2A6D;
  color: #FFFFFF;
  padding: 8px 24px;
  border-radius: 8px;
  transform: skewX(-14deg);
  font-family: 'Montserrat', sans-serif;
  font-weight: 800;
  font-size: 22px;
  letter-spacing: -0.3px;
  box-shadow: 0 5px 18px rgba(255, 42, 109, 0.4);
}
.badge-pink-skew span {
  transform: skewX(14deg);
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

/* Pill badges */
.badge-pink-pill {
  display: inline-flex;
  align-items: center;
  background: #FF2A6D;
  color: #FFFFFF;
  padding: 8px 24px;
  border-radius: 999px;
  font-weight: 800;
  font-size: 22px;
}
.badge-lime-pill {
  display: inline-flex;
  align-items: center;
  background: #CCFF00;
  color: #000000;
  padding: 8px 24px;
  border-radius: 999px;
  font-weight: 800;
  font-size: 21px;
  box-shadow: 0 4px 15px rgba(204, 255, 0, 0.3);
}

/* Cursor pointer */
.cursor-pointer {
  position: absolute;
  filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));
}

/* Corner Cyber Brackets */
.corner-bracket {
  position: absolute;
  width: 28px;
  height: 28px;
  border: 4px solid #FF2A6D;
  z-index: 10;
}
.corner-bracket.top-left { top: 16px; left: 16px; border-right: none; border-bottom: none; }
.corner-bracket.top-right { top: 16px; right: 16px; border-left: none; border-bottom: none; }
.corner-bracket.bottom-left { bottom: 16px; left: 16px; border-right: none; border-top: none; }
.corner-bracket.bottom-right { bottom: 16px; right: 16px; border-left: none; border-top: none; }
"""


# ==============================================================================
# TEMPLATE 1: TOOL & MODEL SHOWCASE (REF 1)
# ==============================================================================

def render_template_hero_showcase(
    top_badge: str,
    tool_title_line1: str,
    tool_title_line2: str,
    bottom_badge: str,
    model_name: str,
    output_path: Path,
) -> None:
    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <style>
    {BASE_CSS}

    .t1-container {{
      width: 1000px;
      height: 1000px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    /* Top Section */
    .t1-top-wrap {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .t1-badge-row {{
      display: flex;
      padding-left: 20px;
    }}
    .t1-lime-card {{
      background: #CCFF00;
      border-radius: 40px;
      padding: 32px 48px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: relative;
      box-shadow: 0 12px 40px rgba(204, 255, 0, 0.25);
      height: 290px;
    }}
    .t1-lime-text {{
      display: flex;
      flex-direction: column;
    }}
    .t1-lime-text h1 {{
      font-family: 'Montserrat', 'Arial Black', sans-serif;
      font-size: 78px;
      font-weight: 900;
      line-height: 0.95;
      color: #000000;
      text-transform: uppercase;
      letter-spacing: -2px;
    }}
    .t1-app-icon-wrap {{
      position: relative;
    }}
    .t1-app-icon {{
      width: 200px;
      height: 200px;
      border-radius: 46px;
      background: linear-gradient(135deg, #d8ff33 0%, #a6d800 100%);
      box-shadow: inset 0 6px 10px rgba(255,255,255,0.7), inset 0 -8px 16px rgba(0,0,0,0.2), 0 16px 36px rgba(0,0,0,0.25);
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .t1-app-icon svg {{
      width: 140px;
      height: 140px;
    }}
    .t1-app-cursor {{
      position: absolute;
      bottom: -12px;
      right: -12px;
      width: 56px;
      height: 56px;
      filter: drop-shadow(0 6px 12px rgba(0,0,0,0.5));
    }}

    /* Bottom Section */
    .t1-bottom-wrap {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .t1-neon-tunnel {{
      width: 100%;
      height: 380px;
      border-radius: 40px;
      border: 3px solid #CCFF00;
      position: relative;
      overflow: hidden;
      box-shadow: 0 0 35px rgba(204, 255, 0, 0.35), inset 0 0 30px rgba(204, 255, 0, 0.2);
      background: #060807;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .t1-grid-svg {{
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
      opacity: 0.85;
    }}
    .t1-model-typography {{
      position: relative;
      z-index: 5;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }}
    .t1-model-name {{
      font-family: 'Chakra Petch', 'Montserrat', sans-serif;
      font-size: 96px;
      font-weight: 900;
      color: #FFFFFF;
      text-transform: uppercase;
      letter-spacing: 2px;
      line-height: 1;
      text-shadow: 0 0 25px rgba(255, 255, 255, 0.6), 0 0 50px rgba(204, 255, 0, 0.5);
    }}
    .t1-orbital-wrap {{
      margin-top: -6px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
  </style>
</head>
<body>
  <div class="t1-container">
    <div class="t1-top-wrap">
      <div class="t1-badge-row">
        <div class="badge-pink-skew"><span>✦ {top_badge}</span></div>
      </div>
      <div class="t1-lime-card">
        <div class="t1-lime-text">
          <h1>{tool_title_line1}</h1>
          <h1>{tool_title_line2}</h1>
        </div>
        <div class="t1-app-icon-wrap">
          <div class="t1-app-icon">
            <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M25 35 C25 20, 50 15, 65 25 C80 35, 75 55, 55 60 C35 65, 30 80, 45 90 C60 100, 85 85, 85 70" 
                    stroke="#141416" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <svg class="t1-app-cursor" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 3L10.5 21L13.5 13.5L21 10.5L3 3Z" fill="#18181B" stroke="#FFFFFF" stroke-width="1.8" stroke-linejoin="round"/>
          </svg>
        </div>
      </div>
    </div>

    <div class="t1-bottom-wrap">
      <div class="t1-badge-row">
        <div class="badge-pink-skew"><span>✦ {bottom_badge}</span></div>
      </div>
      <div class="t1-neon-tunnel">
        <svg class="t1-grid-svg" viewBox="0 0 1000 380" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
          <line x1="0" y1="0" x2="420" y2="160" stroke="#CCFF00" stroke-width="1.5" opacity="0.6"/>
          <line x1="1000" y1="0" x2="580" y2="160" stroke="#CCFF00" stroke-width="1.5" opacity="0.6"/>
          <line x1="0" y1="380" x2="420" y2="220" stroke="#CCFF00" stroke-width="1.5" opacity="0.6"/>
          <line x1="1000" y1="380" x2="580" y2="220" stroke="#CCFF00" stroke-width="1.5" opacity="0.6"/>
          
          <rect x="20" y="20" width="960" height="340" rx="28" fill="none" stroke="#CCFF00" stroke-width="1.5" opacity="0.7"/>
          <rect x="120" y="55" width="760" height="270" rx="20" fill="none" stroke="#CCFF00" stroke-width="1.2" opacity="0.5"/>
          <rect x="250" y="100" width="500" height="180" rx="15" fill="none" stroke="#CCFF00" stroke-width="1" opacity="0.4"/>
          <rect x="380" y="140" width="240" height="100" rx="10" fill="none" stroke="#CCFF00" stroke-width="0.8" opacity="0.3"/>

          <line x1="200" y1="0" x2="440" y2="160" stroke="#CCFF00" stroke-width="1" opacity="0.35"/>
          <line x1="400" y1="0" x2="470" y2="160" stroke="#CCFF00" stroke-width="1" opacity="0.35"/>
          <line x1="600" y1="0" x2="530" y2="160" stroke="#CCFF00" stroke-width="1" opacity="0.35"/>
          <line x1="800" y1="0" x2="560" y2="160" stroke="#CCFF00" stroke-width="1" opacity="0.35"/>
          <line x1="200" y1="380" x2="440" y2="220" stroke="#CCFF00" stroke-width="1" opacity="0.35"/>
          <line x1="400" y1="380" x2="470" y2="220" stroke="#CCFF00" stroke-width="1" opacity="0.35"/>
          <line x1="600" y1="380" x2="530" y2="220" stroke="#CCFF00" stroke-width="1" opacity="0.35"/>
          <line x1="800" y1="380" x2="560" y2="220" stroke="#CCFF00" stroke-width="1" opacity="0.35"/>
        </svg>

        <div class="t1-model-typography">
          <div class="t1-model-name">{model_name}</div>
          <div class="t1-orbital-wrap">
            <svg width="280" height="40" viewBox="0 0 280 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <ellipse cx="140" cy="20" rx="130" ry="12" stroke="#FFFFFF" stroke-width="2.5" opacity="0.9"/>
              <circle cx="230" cy="12" r="5" fill="#CCFF00"/>
              <path d="M230 4 L232 12 L240 12 L233 16 L236 24 L230 19 L224 24 L227 16 L220 12 L228 12 Z" fill="#CCFF00"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""
    render_html_to_image(html, output_path)


# ==============================================================================
# TEMPLATE 2: 4-ITEM CURRICULUM & BREAKDOWN (REF 2)
# ==============================================================================

def render_template_curriculum_breakdown(
    left_badge: str,
    right_badge: str,
    items: list[dict],
    output_path: Path,
) -> None:
    rows_html = ""
    for idx, it in enumerate(items):
        num = it.get("num", f"0{idx+1}")
        title = it.get("title", "")
        desc = it.get("desc", "")
        pink_kw = it.get("pink_kw", "")
        
        desc_highlighted = desc
        if pink_kw and pink_kw in desc:
            desc_highlighted = desc.replace(pink_kw, f'<span class="t2-pink-kw">{pink_kw}</span>')

        rows_html += f"""
        <div class="t2-row">
          <div class="t2-num-col">{num}</div>
          <div class="t2-content-col">
            <h2 class="t2-item-title">{title}</h2>
            <p class="t2-item-desc">{desc_highlighted}</p>
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <style>
    {BASE_CSS}

    .t2-container {{
      width: 1000px;
      height: 1000px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .t2-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      padding: 0 10px;
    }}

    .t2-table {{
      width: 100%;
      display: flex;
      flex-direction: column;
      border-top: 1.8px solid #CCFF00;
      position: relative;
    }}
    .t2-table::before {{
      content: '';
      position: absolute;
      top: 0;
      bottom: 0;
      left: 170px;
      width: 1.8px;
      background: #CCFF00;
      z-index: 2;
    }}

    .t2-row {{
      display: flex;
      border-bottom: 1.8px solid #CCFF00;
      height: 215px;
      align-items: center;
      position: relative;
    }}

    .t2-num-col {{
      width: 170px;
      font-family: 'Montserrat', sans-serif;
      font-weight: 900;
      font-size: 84px;
      color: #CCFF00;
      display: flex;
      align-items: center;
      justify-content: center;
      letter-spacing: -2px;
      flex-shrink: 0;
    }}

    .t2-content-col {{
      padding-left: 36px;
      padding-right: 20px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .t2-item-title {{
      font-family: 'Montserrat', sans-serif;
      font-weight: 800;
      font-size: 25px;
      color: #FFFFFF;
      text-transform: uppercase;
      letter-spacing: -0.5px;
      line-height: 1.2;
    }}

    .t2-item-desc {{
      font-family: 'Inter', sans-serif;
      font-size: 20px;
      font-weight: 400;
      color: #E4E4E7;
      line-height: 1.45;
    }}

    .t2-pink-kw {{
      color: #FF2A6D;
      font-weight: 800;
    }}
  </style>
</head>
<body>
  <div class="t2-container">
    <div class="t2-header">
      <div class="badge-pink-skew"><span>✦ {left_badge}</span></div>
      <div class="badge-pink-pill">{right_badge}</div>
    </div>
    <div class="t2-table">
      {rows_html}
    </div>
  </div>
</body>
</html>"""
    render_html_to_image(html, output_path)


# ==============================================================================
# TEMPLATE 3: 2x2 FEATURE MATRIX & BRANDING (REF 6 & 7)
# ==============================================================================

def render_template_feature_matrix(
    level_badge: str,
    bracket_title_colored: str,
    meta_info_left: str,
    meta_info_right: str,
    cards_2x2: list[dict],
    footer_title_white: str,
    footer_title_pink: str,
    output_path: Path,
) -> None:
    cards_html = ""
    for c in cards_2x2:
        icon_type = c.get("icon", "num")
        icon_val = c.get("num_or_icon", "1")
        title = c.get("title", "")
        sub = c.get("subtitle", "")

        if icon_type == "num":
            icon_markup = f'<div class="t3-pill-icon num">{icon_val}</div>'
        elif icon_type == "key":
            icon_markup = f'''
            <div class="t3-pill-icon key">
              <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#CCFF00" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="7.5" cy="15.5" r="4.5"/>
                <path d="m21 2-9.6 9.6M15.5 7.5l3 3M18.5 4.5l3 3"/>
              </svg>
            </div>'''
        elif icon_type == "book":
            icon_markup = f'''
            <div class="t3-pill-icon book">
              <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#CCFF00" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/>
                <path d="M6 6h10M6 10h10"/>
              </svg>
            </div>'''
        elif icon_type == "flow":
            icon_markup = f'''
            <div class="t3-pill-icon flow">
              <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#CCFF00" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="6" cy="6" r="3"/>
                <rect x="15" y="3" width="6" height="6" rx="1"/>
                <circle cx="6" cy="18" r="3"/>
                <path d="M6 9v6M9 6h6"/>
              </svg>
            </div>'''
        else:
            icon_markup = f'<div class="t3-pill-icon num">{icon_val}</div>'

        cards_html += f"""
        <div class="t3-pill-card">
          {icon_markup}
          <div class="t3-pill-text">
            <span class="t3-pill-t">{title}</span>
            <span class="t3-pill-s">{sub}</span>
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <style>
    {BASE_CSS}

    .t3-container {{
      width: 1000px;
      height: 980px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      padding: 10px 0;
    }}

    .t3-level-badge {{
      display: inline-flex;
      align-items: center;
      background: #FF2A6D;
      color: #FFFFFF;
      padding: 9px 36px;
      border-radius: 999px;
      font-size: 24px;
      font-weight: 800;
      letter-spacing: -0.5px;
      box-shadow: 0 4px 20px rgba(255, 42, 109, 0.4);
    }}

    .t3-bracket-title {{
      font-family: 'Montserrat', sans-serif;
      font-weight: 900;
      font-size: 74px;
      color: #FFFFFF;
      letter-spacing: 2px;
      margin-top: 10px;
      line-height: 1;
    }}

    .t3-meta-bar {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 24px;
      margin-top: 12px;
      font-size: 19px;
      font-weight: 600;
      color: #FFFFFF;
    }}
    .t3-meta-divider {{
      width: 2px;
      height: 30px;
      background: #FFFFFF;
      opacity: 0.8;
    }}
    .t3-meta-zoom {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .t3-grid-2x2 {{
      width: 100%;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-top: 10px;
      padding: 0 10px;
    }}
    .t3-pill-card {{
      background: rgba(255, 255, 255, 0.04);
      border: 1.8px solid rgba(255, 255, 255, 0.6);
      border-radius: 999px;
      padding: 16px 26px;
      display: flex;
      align-items: center;
      gap: 18px;
      text-align: left;
    }}
    .t3-pill-icon {{
      width: 48px;
      height: 48px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}
    .t3-pill-icon.num {{
      font-family: 'Montserrat', sans-serif;
      font-size: 42px;
      font-weight: 900;
      color: #CCFF00;
    }}
    .t3-pill-text {{
      display: flex;
      flex-direction: column;
      line-height: 1.25;
    }}
    .t3-pill-t {{
      font-size: 21px;
      font-weight: 700;
      color: #FFFFFF;
    }}
    .t3-pill-s {{
      font-size: 21px;
      font-weight: 700;
      color: #FF2A6D;
    }}

    .t3-footer {{
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 28px;
      padding: 0 20px;
    }}
    .t3-footer-logo {{
      flex-shrink: 0;
    }}
    .t3-footer-text {{
      display: flex;
      flex-direction: column;
      text-align: left;
      line-height: 1.15;
    }}
    .t3-ft-white {{
      font-size: 32px;
      font-weight: 900;
      color: #FFFFFF;
      text-transform: uppercase;
      letter-spacing: -0.5px;
    }}
    .t3-ft-pink {{
      font-size: 32px;
      font-weight: 900;
      color: #FF2A6D;
      text-transform: uppercase;
      letter-spacing: -0.5px;
    }}
  </style>
</head>
<body>
  <div class="t3-container">
    <div>
      <div class="t3-level-badge">{level_badge}</div>
      <div class="t3-bracket-title">{bracket_title_colored}</div>
      <div class="t3-meta-bar">
        <div class="t3-meta-zoom">
          <span>{meta_info_left}</span>
          {ZOOM_LOGO_SVG}
        </div>
        <div class="t3-meta-divider"></div>
        <div>{meta_info_right}</div>
      </div>
    </div>

    <div class="t3-grid-2x2">
      {cards_html}
    </div>

    <div class="t3-footer">
      <div class="t3-footer-logo">
        {ASTERISK_LOGO_SVG}
      </div>
      <div class="t3-footer-text">
        <span class="t3-ft-white">{footer_title_white}</span>
        <span class="t3-ft-pink">{footer_title_pink}</span>
      </div>
    </div>
  </div>
</body>
</html>"""
    render_html_to_image(html, output_path)


# ==============================================================================
# TEMPLATE 4: LEAD MAGNET / ACTION SCHEDULE CARD (REF 4)
# ==============================================================================

def render_template_offer_card(
    header_badge: str,
    bracket_title_colored: str,
    selector_badge: str,
    date_cards: list[dict],
    time_badge: str,
    delivery_text: str,
    cta_button_text: str,
    output_path: Path,
) -> None:
    dates_html = ""
    for d in date_cards:
        lbl = d.get("label", "")
        dt = d.get("date", "")
        hl = d.get("highlight", False)
        date_color = "#CCFF00" if hl else "#FFFFFF"
        dates_html += f"""
        <div class="t4-date-card">
          <span class="t4-date-lbl">{lbl}</span>
          <span class="t4-date-val" style="color: {date_color};">{dt}</span>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <style>
    {BASE_CSS}

    .t4-outer {{
      width: 1000px;
      height: 1000px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }}

    .t4-card {{
      width: 100%;
      height: 980px;
      background: #111317;
      border-radius: 40px;
      border: 1px solid rgba(255, 255, 255, 0.14);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      overflow: hidden;
      box-shadow: 0 16px 50px rgba(0, 0, 0, 0.6);
      position: relative;
      padding-bottom: 24px;
    }}

    .t4-top-tab {{
      width: 100%;
      height: 52px;
      background: #CCFF00;
      border-radius: 40px 40px 0 0;
      flex-shrink: 0;
    }}

    .t4-badge-row {{
      margin-top: -26px;
      z-index: 5;
    }}

    .t4-bracket-title {{
      font-family: 'Montserrat', sans-serif;
      font-weight: 900;
      font-size: 70px;
      color: #FFFFFF;
      letter-spacing: 2px;
      margin-top: 6px;
      line-height: 1;
    }}

    .t4-dates-row {{
      display: flex;
      gap: 16px;
      width: 90%;
      justify-content: center;
      margin-top: 10px;
    }}
    .t4-date-card {{
      flex: 1;
      background: #191B20;
      border: 1.5px solid rgba(255, 255, 255, 0.25);
      border-radius: 22px;
      padding: 12px 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
    }}
    .t4-date-lbl {{
      font-size: 16px;
      font-weight: 600;
      color: #D4D4D8;
    }}
    .t4-date-val {{
      font-family: 'Montserrat', sans-serif;
      font-size: 36px;
      font-weight: 900;
    }}

    .t4-delivery-row {{
      display: flex;
      align-items: center;
      gap: 14px;
      font-size: 20px;
      font-weight: 600;
      color: #FFFFFF;
      margin-top: 4px;
    }}

    .t4-cta-wrap {{
      position: relative;
      margin-top: 6px;
      margin-bottom: 6px;
    }}
    .t4-cta-btn {{
      display: inline-flex;
      align-items: center;
      gap: 12px;
      background: #CCFF00;
      color: #000000;
      padding: 14px 40px;
      border-radius: 999px;
      font-family: 'Montserrat', sans-serif;
      font-weight: 900;
      font-size: 25px;
      text-transform: uppercase;
      box-shadow: 0 8px 30px rgba(204, 255, 0, 0.4);
    }}
    .t4-cta-arrow {{
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: #000000;
      color: #CCFF00;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      font-weight: 900;
    }}
    .t4-cta-cursor {{
      position: absolute;
      bottom: -12px;
      right: 8px;
      width: 44px;
      height: 44px;
    }}
  </style>
</head>
<body>
  {CORNER_BRACKETS_SVG}
  <div class="t4-outer">
    <div class="t4-card">
      <div class="t4-top-tab"></div>
      
      <div class="t4-badge-row">
        <div class="badge-pink-skew"><span>✦ {header_badge}</span></div>
      </div>

      <div class="t4-bracket-title">{bracket_title_colored}</div>

      <div class="badge-lime-pill">✦ {selector_badge} ✦</div>

      <div class="t4-dates-row">
        {dates_html}
      </div>

      <div class="badge-lime-pill">✦ {time_badge} ✦</div>

      <div class="t4-delivery-row">
        <span>{delivery_text}</span>
        {ZOOM_LOGO_SVG}
      </div>

      <div class="t4-cta-wrap">
        <div class="t4-cta-btn">
          <span>{cta_button_text}</span>
          <div class="t4-cta-arrow">&gt;</div>
        </div>
        <svg class="t4-cta-cursor" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 3L10.5 21L13.5 13.5L21 10.5L3 3Z" fill="#18181B" stroke="#FFFFFF" stroke-width="1.8" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>
  </div>
</body>
</html>"""
    render_html_to_image(html, output_path)


# ==============================================================================
# TEMPLATE 5: URGENCY & PROGRESS SLOTS (REF 5)
# ==============================================================================

def render_template_urgency_slots(
    top_badge: str,
    sold_out_text: str,
    slots: list[dict],
    cta_badge: str,
    footer_tag: str,
    offer_big_left: str,
    offer_mid_top: str,
    offer_mid_sub: str,
    output_path: Path,
) -> None:
    slots_html = ""
    for s in slots:
        t = s.get("title", "")
        b = s.get("badge", "")
        p = s.get("percent", 50)
        slots_html += f"""
        <div class="t5-slot-row">
          <div class="t5-slot-title">{t}</div>
          <div class="t5-slot-badge">{b}</div>
          <div class="t5-progress-bar">
            <div class="t5-progress-fill" style="width: {p}%;">
              <span class="t5-progress-txt">Còn {p}% vị trí</span>
            </div>
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <style>
    {BASE_CSS}

    .t5-container {{
      width: 1000px;
      height: 980px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      position: relative;
    }}

    .t5-top {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
    }}

    .t5-sold-out {{
      font-family: 'Montserrat', sans-serif;
      font-weight: 900;
      font-size: 100px;
      color: #FFFFFF;
      letter-spacing: -2px;
      line-height: 0.95;
      text-shadow: 0 0 30px rgba(255, 255, 255, 0.4);
    }}

    .t5-slots-wrap {{
      width: 92%;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .t5-slot-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }}
    .t5-slot-title {{
      font-size: 24px;
      font-weight: 900;
      color: #FFFFFF;
      width: 270px;
      text-align: left;
    }}
    .t5-slot-badge {{
      background: #181A20;
      border: 1.5px solid rgba(255, 255, 255, 0.3);
      border-radius: 16px;
      padding: 8px 16px;
      font-size: 17px;
      font-weight: 700;
      color: #FFFFFF;
      white-space: nowrap;
    }}
    .t5-progress-bar {{
      flex: 1;
      height: 36px;
      background: #181A20;
      border-radius: 999px;
      border: 1.5px solid rgba(255, 255, 255, 0.3);
      position: relative;
      overflow: hidden;
      display: flex;
      align-items: center;
    }}
    .t5-progress-fill {{
      height: 100%;
      background: #FF2A6D;
      border-radius: 999px;
      display: flex;
      align-items: center;
      padding-left: 14px;
      white-space: nowrap;
    }}
    .t5-progress-txt {{
      font-size: 15px;
      font-weight: 800;
      color: #FFFFFF;
    }}

    .t5-cta-btn {{
      display: inline-flex;
      align-items: center;
      gap: 12px;
      background: #FF2A6D;
      color: #FFFFFF;
      padding: 16px 48px;
      border-radius: 999px;
      font-size: 32px;
      font-weight: 900;
      letter-spacing: -0.5px;
      box-shadow: 0 8px 30px rgba(255, 42, 109, 0.5);
    }}

    .t5-bottom-card {{
      width: 100%;
      background: linear-gradient(180deg, #18280f 0%, #0d1408 100%);
      border: 2px solid #CCFF00;
      border-radius: 34px;
      padding: 22px 34px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: 0 0 35px rgba(204, 255, 0, 0.2);
    }}
    .t5-footer-tag {{
      align-self: flex-start;
      background: #181A20;
      border: 1.5px solid #FF2A6D;
      color: #FFFFFF;
      padding: 6px 18px;
      border-radius: 999px;
      font-size: 17px;
      font-weight: 800;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .t5-offer-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .t5-offer-left {{
      font-family: 'Montserrat', sans-serif;
      font-size: 80px;
      font-weight: 900;
      color: #FFFFFF;
      line-height: 0.9;
    }}
    .t5-offer-mid {{
      display: flex;
      flex-direction: column;
      text-align: left;
      line-height: 1.1;
    }}
    .t5-offer-m1 {{
      font-size: 32px;
      font-weight: 900;
      color: #FFFFFF;
    }}
    .t5-offer-m2 {{
      font-size: 32px;
      font-weight: 900;
      color: #FF2A6D;
    }}
  </style>
</head>
<body>
  <div class="t5-container">
    <div class="t5-top">
      <div class="badge-pink-skew"><span>✦ {top_badge}</span></div>
      <div class="t5-sold-out">{sold_out_text}</div>
    </div>

    <div class="t5-slots-wrap">
      {slots_html}
    </div>

    <div class="t5-cta-btn">
      <span style="color: #CCFF00;">✦</span> {cta_badge}
    </div>

    <div class="t5-bottom-card">
      <div class="t5-footer-tag"><span style="color: #FF2A6D;">✦</span> {footer_tag}</div>
      <div class="t5-offer-row">
        <div class="t5-offer-left">{offer_big_left}</div>
        <div class="t5-offer-mid">
          <span class="t5-offer-m1">{offer_mid_top}</span>
          <span class="t5-offer-m2">{offer_mid_sub}</span>
        </div>
        <div style="width: 140px; text-align: right;">
          {ASTERISK_LOGO_SVG}
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""
    render_html_to_image(html, output_path)


if __name__ == "__main__":
    print("Testing Vid-Style Card Templates v3 (Zero Cutoff)...")
    test_out = SUBAGENT_DIR / "campaigns" / "2026-10-26" / "ai-players-weekly-vault" / "test_samples"
    test_out.mkdir(parents=True, exist_ok=True)

    # 1. Test Template 1
    t1_path = test_out / "sample_t1_hero.jpg"
    print("Rendering T1 Hero Showcase...")
    render_template_hero_showcase(
        top_badge="Thực hành với",
        tool_title_line1="HIGGS",
        tool_title_line2="FIELD",
        bottom_badge="Với model",
        model_name="SEEDANCE 2.5",
        output_path=t1_path
    )
    print("T1 done:", t1_path.name)

    # 2. Test Template 2
    t2_path = test_out / "sample_t2_curriculum.jpg"
    print("Rendering T2 Curriculum Breakdown...")
    render_template_curriculum_breakdown(
        left_badge="Chi tiết giáo án",
        right_badge="4 skills",
        items=[
            {
                "num": "01",
                "title": "NHÂN VẬT CHÂN THẬT & CHẤT LƯỢNG INPUT",
                "desc": "Tạo nhân vật AI chân thật qua 8 yếu tố Human Realism, chuẩn hóa input trước khi animate.",
                "pink_kw": "Human Realism"
            },
            {
                "num": "02",
                "title": "KIỂM SOÁT REFERENCE & KHÓA NHẬN DIỆN",
                "desc": "Ra nhiều output vẫn đúng nhân vật, sản phẩm, logo — nhờ nguyên tắc LOCK / CHANGE.",
                "pink_kw": "LOCK / CHANGE"
            },
            {
                "num": "03",
                "title": "GIAO TIẾP VỚI AI & ĐIỀU KHIỂN VIDEO BẰNG PROMPT",
                "desc": "Làm chủ cú pháp Camera, Lighting & Motion không bị biến dạng hình thể.",
                "pink_kw": "Motion không bị biến dạng"
            },
            {
                "num": "04",
                "title": "LỰA CHỌN & ĐÁNH GIÁ AI MODEL",
                "desc": "Chọn đúng model trước khi generate theo độ chân thật, motion, tốc độ, chi phí.",
                "pink_kw": "Chọn đúng model"
            }
        ],
        output_path=t2_path
    )
    print("T2 done:", t2_path.name)

    # 3. Test Template 3
    t3_path = test_out / "sample_t3_feature_matrix.jpg"
    print("Rendering T3 Feature Matrix...")
    render_template_feature_matrix(
        level_badge="Level 01",
        bracket_title_colored='[ <span style="color:#CCFF00">FOU</span>NDA<span style="color:#FF2A6D">TION</span> ]',
        meta_info_left="Hình thức: 2 buổi Online qua",
        meta_info_right="Ngày: 17, 24 & 31/10 | Thời gian: 9:00 - 16:00",
        cards_2x2=[
            {"icon": "key", "title": "Mở khoá", "subtitle": "Tư duy AI"},
            {"icon": "book", "title": "Bản đồ Model", "subtitle": "& Nền tảng"},
            {"icon": "flow", "title": "Workflow", "subtitle": "Chuẩn thực chiến"},
            {"icon": "num", "num_or_icon": "3", "title": "Kỹ năng AI", "subtitle": "Đầu tiên"}
        ],
        footer_title_white="TẠO NHÂN VẬT & VIDEO",
        footer_title_pink="CÓ ĐỘ CHÂN THẬT CAO",
        output_path=t3_path
    )
    print("T3 done:", t3_path.name)

    # 4. Test Template 4
    t4_path = test_out / "sample_t4_offer_card.jpg"
    print("Rendering T4 Offer Card...")
    render_template_offer_card(
        header_badge="Chi tiết Khoá học",
        bracket_title_colored='[ <span style="color:#CCFF00">FOU</span>NDA<span style="color:#FF2A6D">TION</span> ]',
        selector_badge="Chọn 1 trong 3 khoá dưới đây",
        date_cards=[
            {"label": "Khoá 1", "date": "17/10", "highlight": False},
            {"label": "Khoá 2", "date": "24/10", "highlight": True},
            {"label": "Khoá 3", "date": "31/10", "highlight": True}
        ],
        time_badge="Thứ bảy: 09:00 - 12:00 & 13:00 - 16:00",
        delivery_text="Hình thức: 2 buổi Online qua",
        cta_button_text="THỰC CHIẾN NGAY",
        output_path=t4_path
    )
    print("T4 done:", t4_path.name)

    # 5. Test Template 5
    t5_path = test_out / "sample_t5_urgency.jpg"
    print("Rendering T5 Urgency Slots...")
    render_template_urgency_slots(
        top_badge="Thông báo chuẩn bị",
        sold_out_text="SOLD OUT",
        slots=[
            {"title": "[ FOUNDATION ]", "badge": "Khoá 1 17/10", "percent": 40},
            {"title": "CREATOR & COMMERCE", "badge": "Khoá 1 18/10", "percent": 30}
        ],
        cta_badge="GIỮ CHỖ NGAY",
        footer_tag="30 SLOT CUỐI CÙNG KHI ĐĂNG KÝ",
        offer_big_left="LV2",
        offer_mid_top="TẶNG NGAY",
        offer_mid_sub="LV1 MIỄN PHÍ",
        output_path=t5_path
    )
    print("T5 done:", t5_path.name)
