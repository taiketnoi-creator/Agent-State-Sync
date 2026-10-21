#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render 11 Visual Cards (1080x1350, 4:5 aspect ratio) for Campaign CAMP-20261020-today-launch.
Follows CEO-approved visual standards:
- knowledge/quy-chuan-anh-bai-dang-ai-players.md (Style 02 & Style 03)
- knowledge/quy-chuan-anh-bai-dang-page-ban-hang.md (Sales Style 01 & Sales Style 02)
- campaigns/2026-10-20/today-launch/01-mkt-sku-and-github-repos.md (Gate 1 Verified Data)
"""

import os
import subprocess
import tempfile
from pathlib import Path
from PIL import Image

BASE_DIR = Path(r"d:\Phiên bản Ai agent\Subagent")
OUTPUT_DIR = BASE_DIR / "campaigns" / "2026-10-20" / "today-launch" / "images"

BROWSER_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def find_browser() -> str:
    for path in BROWSER_CANDIDATES:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Neither Chrome nor Edge found for headless rendering.")


def render_html_to_png(html_content: str, output_path: Path, width: int = 1080, height: int = 1350) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    browser = find_browser()
    with tempfile.TemporaryDirectory() as tmpdir:
        html_file = Path(tmpdir) / "card.html"
        raw_png = Path(tmpdir) / "raw.png"
        html_file.write_text(html_content, encoding="utf-8")

        cmd = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={width + 120},{height + 160}",
            f"--screenshot={raw_png}",
            str(html_file),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        with Image.open(raw_png) as im:
            if im.size != (width, height):
                im = im.crop((0, 0, width, height))
            im.save(output_path, format="PNG", optimize=True)


# ============================================================================
# 1. AI PLAYERS — STYLE 02 TEMPLATE (Aurora Mesh + Isometric Grid + Tilted Pills)
# ============================================================================

def build_ai_style02_html(
    kicker_badge: str,
    preview_title: str,
    preview_items: list[tuple[str, str, str]],
    headline_lines: list[str],
    boxed_line_idx: int,
    pill_1_text: str,
    pill_2_text: str,
    summary_line_1: str,
    summary_line_2: str,
    footer_left_top: str,
    footer_left_bold: str,
    footer_mid_top: str,
    footer_mid_bold: str,
) -> str:
    items_html = ""
    for num, title, desc in preview_items:
        items_html += f"""
        <div class="mod-item">
          <div class="mod-num">{num}</div>
          <div class="mod-text">
            <div class="mod-title">{title}</div>
            <div class="mod-desc">{desc}</div>
          </div>
        </div>
        """

    hl_html = ""
    for idx, line in enumerate(headline_lines):
        if idx == boxed_line_idx:
            hl_html += f"""
            <div class="hl-box-wrap">
              <span class="hl-line boxed">{line}</span>
              <span class="handle tl"></span>
              <span class="handle tm"></span>
              <span class="handle tr"></span>
              <span class="handle bl"></span>
              <span class="handle bm"></span>
              <span class="handle br"></span>
              <span class="pen-icon">✒️</span>
            </div>
            """
        else:
            hl_html += f'<div class="hl-line">{line}</div>'

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px;
    height: 1350px;
    overflow: hidden;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #0D7A5F;
    position: relative;
    color: #0B4F3E;
  }}
  /* Aurora Mesh Gradient matching style-02-cta-tilted-pills.jpg */
  .aurora-bg {{
    position: absolute;
    inset: 0;
    background:
      radial-gradient(circle at 92% 8%, rgba(190, 242, 100, 0.92) 0%, rgba(163, 230, 53, 0.55) 25%, transparent 54%),
      radial-gradient(circle at 78% 58%, rgba(244, 249, 232, 0.96) 0%, rgba(236, 252, 203, 0.88) 28%, rgba(217, 249, 157, 0.45) 52%, transparent 72%),
      radial-gradient(circle at 22% 62%, rgba(244, 249, 232, 0.92) 0%, rgba(163, 230, 53, 0.72) 36%, transparent 66%),
      radial-gradient(circle at 38% 82%, rgba(163, 230, 53, 0.85) 0%, rgba(34, 197, 94, 0.45) 38%, transparent 68%),
      linear-gradient(155deg, #0D7A5F 0%, #15803D 32%, #84CC16 64%, #0D7A5F 100%);
  }}
  /* Isometric Diamond Perspective Grid */
  .iso-grid {{
    position: absolute;
    inset: -200px;
    background-image:
      linear-gradient(30deg, rgba(255,255,255,0.14) 1px, transparent 1px),
      linear-gradient(150deg, rgba(255,255,255,0.14) 1px, transparent 1px);
    background-size: 56px 56px;
    mask-image: radial-gradient(circle at 50% 38%, black 0%, rgba(0,0,0,0.6) 45%, transparent 78%);
    -webkit-mask-image: radial-gradient(circle at 50% 38%, black 0%, rgba(0,0,0,0.6) 45%, transparent 78%);
    pointer-events: none;
  }}
  /* Top Glassmorphic Showcase Card */
  .top-showcase {{
    position: relative;
    z-index: 2;
    margin: 56px 68px 0 68px;
    background: rgba(255, 255, 255, 0.86);
    border: 10px solid rgba(255, 255, 255, 0.92);
    border-radius: 28px;
    box-shadow: 0 24px 50px rgba(9, 59, 46, 0.22), inset 0 2px 6px rgba(255,255,255,0.9);
    padding: 28px 34px 30px 34px;
    backdrop-filter: blur(16px);
  }}
  .top-pill-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
  }}
  .kicker-badge {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(90deg, #0D7A5F 0%, #16A34A 100%);
    color: #FFFFFF;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 19px;
    font-weight: 700;
    letter-spacing: 0.06em;
    padding: 9px 20px;
    border-radius: 999px;
    box-shadow: 0 6px 16px rgba(13, 122, 95, 0.28);
  }}
  .brand-mini {{
    font-size: 18px;
    font-weight: 700;
    color: #0D7A5F;
    background: #ECFCCB;
    border: 2px solid #84CC16;
    padding: 7px 18px;
    border-radius: 999px;
  }}
  .showcase-title {{
    font-size: 25px;
    font-weight: 800;
    color: #0B4F3E;
    margin-bottom: 18px;
    letter-spacing: -0.01em;
  }}
  .mod-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }}
  .mod-item {{
    display: flex;
    align-items: flex-start;
    gap: 14px;
    background: linear-gradient(135deg, #F4F9E8 0%, #FFFFFF 100%);
    border: 2px solid rgba(132, 204, 22, 0.45);
    border-radius: 18px;
    padding: 15px 18px;
  }}
  .mod-num {{
    min-width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #0D7A5F 0%, #22C55E 100%);
    color: #FFFFFF;
    font-weight: 900;
    font-size: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 6px 12px rgba(13,122,95,0.22);
  }}
  .mod-title {{
    font-size: 19px;
    font-weight: 800;
    color: #0B4F3E;
    margin-bottom: 3px;
  }}
  .mod-desc {{
    font-size: 15.5px;
    font-weight: 600;
    color: #1F5E4B;
    line-height: 1.32;
  }}

  /* Center Headline + Tilted 3D Pill Stickers (Exact Style 02 DNA) */
  .hero-middle {{
    position: relative;
    z-index: 3;
    margin-top: 62px;
    padding: 0 68px;
    height: 440px;
  }}
  .headline-stack {{
    position: relative;
    max-width: 620px;
  }}
  .hl-line {{
    font-size: 104px;
    font-weight: 900;
    line-height: 1.02;
    letter-spacing: -0.03em;
    color: #0B4F3E;
    text-shadow: 0 2px 0 rgba(255,255,255,0.5);
  }}
  .hl-box-wrap {{
    position: relative;
    display: inline-block;
    margin: 10px 0 8px 0;
    padding: 4px 20px 10px 16px;
    border: 3.5px solid #16A34A;
    background: rgba(236, 252, 203, 0.52);
  }}
  .hl-line.boxed {{
    font-size: 96px;
    color: #093B2E;
  }}
  .handle {{
    position: absolute;
    width: 14px;
    height: 14px;
    background: #0D7A5F;
    border: 2px solid #FFFFFF;
    border-radius: 3px;
  }}
  .handle.tl {{ top: -8px; left: -8px; }}
  .handle.tm {{ top: -8px; left: 48%; }}
  .handle.tr {{ top: -8px; right: -8px; }}
  .handle.bl {{ bottom: -8px; left: -8px; }}
  .handle.bm {{ bottom: -8px; left: 48%; }}
  .handle.br {{ bottom: -8px; right: -8px; }}
  .pen-icon {{
    position: absolute;
    right: -36px;
    bottom: -34px;
    font-size: 30px;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.18));
  }}

  /* Decorative 3D Star & Dots next to Headline */
  .sparkle-cluster {{
    position: absolute;
    left: 470px;
    top: -18px;
    width: 120px;
    height: 120px;
  }}

  /* Tilted Pill Stickers on Right */
  .pills-zone {{
    position: absolute;
    right: 52px;
    top: 120px;
    width: 530px;
    height: 290px;
  }}
  .pill-upper {{
    position: absolute;
    top: 18px;
    left: 0;
    transform: rotate(-13deg);
    background: rgba(244, 249, 232, 0.94);
    border: 10px solid rgba(217, 249, 157, 0.88);
    border-radius: 999px;
    padding: 16px 34px;
    box-shadow: 0 20px 36px rgba(9, 59, 46, 0.22);
    z-index: 4;
    white-space: nowrap;
  }}
  .pill-upper span {{
    font-family: 'Consolas', 'Segoe UI', monospace;
    font-size: 25px;
    font-weight: 900;
    letter-spacing: 0.04em;
    color: #0B4F3E;
  }}
  .pill-lower {{
    position: absolute;
    top: 112px;
    left: 48px;
    transform: rotate(-6deg);
    background: linear-gradient(95deg, #0D7A5F 0%, #16A34A 52%, #84CC16 100%);
    border: 12px solid rgba(255, 255, 255, 0.92);
    border-radius: 999px;
    padding: 18px 42px;
    box-shadow: 0 24px 44px rgba(9, 59, 46, 0.30);
    display: inline-flex;
    align-items: center;
    gap: 18px;
    z-index: 5;
    white-space: nowrap;
  }}
  .pill-lower .bm-icon {{
    width: 42px;
    height: 46px;
    background: #FFFFFF;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #0D7A5F;
    font-size: 25px;
    font-weight: 900;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
  }}
  .pill-lower .bm-text {{
    font-size: 46px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.02em;
  }}

  /* Bottom Editorial Summary & 3-Column Footer */
  .bottom-section {{
    position: absolute;
    bottom: 52px;
    left: 68px;
    right: 68px;
    z-index: 3;
  }}
  .summary-box {{
    border-top: 2px solid rgba(255, 255, 255, 0.42);
    border-bottom: 2px solid rgba(255, 255, 255, 0.42);
    padding: 26px 0;
    margin-bottom: 28px;
  }}
  .summary-text {{
    font-size: 26px;
    font-weight: 600;
    color: #F4F9E8;
    line-height: 1.42;
    text-shadow: 0 2px 8px rgba(9, 59, 46, 0.35);
  }}
  .summary-text strong {{
    color: #ECFCCB;
    font-weight: 800;
  }}
  .editorial-footer {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #ECFCCB;
    font-size: 21px;
  }}
  .foot-col .sub {{
    color: rgba(244, 249, 232, 0.78);
    font-size: 18px;
    font-weight: 500;
  }}
  .foot-col .main {{
    font-weight: 800;
    color: #FFFFFF;
    font-size: 22px;
    margin-top: 2px;
  }}
  .foot-col.center {{ text-align: center; }}
  .foot-col.right {{ text-align: right; }}
</style>
</head>
<body>
  <div class="aurora-bg"></div>
  <div class="iso-grid"></div>

  <!-- Top Showcase Card -->
  <div class="top-showcase">
    <div class="top-pill-row">
      <div class="kicker-badge">{kicker_badge}</div>
      <div class="brand-mini">✦ AI Players • Người chơi hệ AI</div>
    </div>
    <div class="showcase-title">{preview_title}</div>
    <div class="mod-grid">
      {items_html}
    </div>
  </div>

  <!-- Center Hero Headline + Tilted 3D Pill Stickers -->
  <div class="hero-middle">
    <div class="headline-stack">
      {hl_html}
      <svg class="sparkle-cluster" viewBox="0 0 120 120">
        <circle cx="25" cy="18" r="6" fill="#0D7A5F"/>
        <circle cx="26" cy="40" r="4.5" fill="#15803D"/>
        <circle cx="52" cy="48" r="10" fill="#84CC16"/>
        <circle cx="96" cy="95" r="6" fill="#84CC16"/>
        <path d="M55 62 C62 62, 66 56, 70 62 C74 68, 82 70, 76 78 C70 86, 74 96, 65 92 C56 88, 48 94, 46 84 C44 74, 36 72, 44 66 Z" fill="#0D7A5F"/>
      </svg>
    </div>

    <div class="pills-zone">
      <div class="pill-upper">
        <span>{pill_1_text}</span>
      </div>
      <div class="pill-lower">
        <div class="bm-icon">✓</div>
        <div class="bm-text">{pill_2_text}</div>
      </div>
    </div>
  </div>

  <!-- Editorial Summary & Footer -->
  <div class="bottom-section">
    <div class="summary-box">
      <div class="summary-text">
        {summary_line_1}<br>
        <strong>{summary_line_2}</strong>
      </div>
    </div>
    <div class="editorial-footer">
      <div class="foot-col">
        <div class="sub">{footer_left_top}</div>
        <div class="main">{footer_left_bold}</div>
      </div>
      <div class="foot-col center">
        <div class="sub">{footer_mid_top}</div>
        <div class="main">{footer_mid_bold}</div>
      </div>
      <div class="foot-col right">
        <div class="sub">Curated by</div>
        <div class="main">AI Players 🔖</div>
      </div>
    </div>
  </div>
</body>
</html>
"""


# ============================================================================
# 2. AI PLAYERS — STYLE 03 TEMPLATE (3D Hero UI Toolkit + Vector Box + 5 Cards)
# ============================================================================

def build_ai_style03_html(
    top_kicker: str,
    badge_text: str,
    boxed_headline: str,
    sub_headline: str,
    repo_url: str,
    sidebar_items: list[tuple[str, str]],
    hero_card_title: str,
    hero_card_subtitle: str,
    hero_bullets: list[str],
    card_number: str,
    right_pill_text: str,
    mini_cards: list[tuple[str, str, str, bool]],
) -> str:
    sidebar_html = ""
    for icon_sym, label in sidebar_items:
        sidebar_html += f"""
        <div class="sb-item">
          <div class="sb-icon">{icon_sym}</div>
          <div class="sb-label">{label}</div>
        </div>
        """

    bullets_html = ""
    for b in hero_bullets:
        bullets_html += f'<div class="hb-item"><span class="hb-dot">✦</span><span>{b}</span></div>'

    mini_html = ""
    for num, m_title, m_sub, is_green in mini_cards:
        cls = "mini-card green" if is_green else "mini-card white"
        mini_html += f"""
        <div class="{cls}">
          <div class="mc-top">{m_sub}</div>
          <div class="mc-title">{m_title}</div>
          <div class="mc-num">{num}</div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px;
    height: 1350px;
    overflow: hidden;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    position: relative;
    background: linear-gradient(165deg, #F4F9E8 0%, #ECFCCB 28%, #86EFAC 62%, #15803D 88%, #0D7A5F 100%);
    color: #0B4F3E;
  }}
  .mesh-glow {{
    position: absolute;
    inset: 0;
    background:
      radial-gradient(circle at 18% 12%, rgba(244, 249, 232, 0.95) 0%, transparent 48%),
      radial-gradient(circle at 88% 24%, rgba(163, 230, 53, 0.55) 0%, transparent 52%),
      radial-gradient(circle at 50% 92%, rgba(13, 122, 95, 0.92) 0%, transparent 60%);
  }}
  .iso-grid {{
    position: absolute;
    inset: -150px;
    background-image:
      linear-gradient(35deg, rgba(13, 122, 95, 0.08) 1px, transparent 1px),
      linear-gradient(145deg, rgba(13, 122, 95, 0.08) 1px, transparent 1px);
    background-size: 52px 52px;
    pointer-events: none;
  }}

  /* Top Kicker & Floating Indigo Badge */
  .top-header {{
    position: relative;
    z-index: 3;
    text-align: center;
    padding-top: 44px;
  }}
  .kicker-top {{
    font-size: 22px;
    font-weight: 800;
    color: #15803D;
    letter-spacing: 0.02em;
  }}
  .kicker-sub {{
    font-size: 20px;
    font-weight: 600;
    color: #22C55E;
    margin-top: 2px;
  }}
  .indigo-badge-wrap {{
    margin-top: 24px;
    display: inline-block;
    position: relative;
  }}
  .indigo-badge-shadow {{
    position: absolute;
    inset: 8px -10px -10px 10px;
    background: rgba(22, 163, 74, 0.38);
    border-radius: 26px;
    transform: rotate(3deg);
  }}
  .indigo-badge {{
    position: relative;
    background: linear-gradient(135deg, #0EA5E9 0%, #3B82F6 45%, #4F46E5 100%);
    color: #FFFFFF;
    font-size: 24px;
    font-weight: 800;
    padding: 15px 34px;
    border-radius: 24px;
    box-shadow: 0 14px 28px rgba(37, 99, 235, 0.28);
    letter-spacing: 0.02em;
  }}

  /* Vector Selection Bounding Box Headline */
  .vector-title-area {{
    position: relative;
    z-index: 3;
    text-align: center;
    margin-top: 24px;
  }}
  .vector-box {{
    display: inline-block;
    position: relative;
    border: 3.5px solid #22C55E;
    background: rgba(255, 255, 255, 0.42);
    padding: 10px 36px 14px 36px;
    margin: 0 auto;
  }}
  .vector-box h1 {{
    font-size: 58px;
    font-weight: 900;
    color: #0B4F3E;
    letter-spacing: -0.02em;
    line-height: 1.08;
  }}
  .vh {{
    position: absolute;
    width: 15px;
    height: 15px;
    background: #0D7A5F;
    border: 2px solid #FFFFFF;
    border-radius: 3px;
  }}
  .vh.tl {{ top: -9px; left: -9px; }}
  .vh.tr {{ top: -9px; right: -9px; }}
  .vh.bl {{ bottom: -9px; left: -9px; }}
  .vh.br {{ bottom: -9px; right: -9px; }}
  .vh.tm {{ top: -9px; left: 50%; transform: translateX(-50%); background: #84CC16; }}
  .vh.bm {{ bottom: -9px; left: 50%; transform: translateX(-50%); background: #84CC16; }}

  .sub-h2 {{
    font-family: 'Consolas', 'Segoe UI', monospace;
    font-size: 46px;
    font-weight: 900;
    color: #0B4F3E;
    margin-top: 10px;
    letter-spacing: -0.01em;
  }}
  .cursor-3d {{
    position: absolute;
    right: 96px;
    bottom: -6px;
    width: 44px;
    height: 44px;
    filter: drop-shadow(0 8px 12px rgba(13,122,95,0.35));
  }}
  .left-sparkle-ring {{
    position: absolute;
    left: 88px;
    bottom: -48px;
    width: 84px;
    height: 84px;
    border-radius: 50%;
    border: 3px solid rgba(255,255,255,0.75);
    background: rgba(255,255,255,0.25);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #FFFFFF;
    font-size: 36px;
  }}

  /* Tilted 3D UI Window + 2 Stacked Glass Deck Layers */
  .ui-stage {{
    position: relative;
    z-index: 4;
    margin: 36px auto 0 auto;
    width: 880px;
    height: 690px;
  }}
  .deck-layer-2 {{
    position: absolute;
    bottom: 6px;
    left: 86px;
    right: 66px;
    height: 120px;
    background: rgba(255, 255, 255, 0.34);
    border: 2px solid rgba(255,255,255,0.5);
    border-radius: 28px;
    transform: rotate(-0.8deg);
    backdrop-filter: blur(8px);
  }}
  .deck-layer-1 {{
    position: absolute;
    bottom: 28px;
    left: 52px;
    right: 38px;
    height: 140px;
    background: rgba(255, 255, 255, 0.58);
    border: 2px solid rgba(255,255,255,0.75);
    border-radius: 28px;
    transform: rotate(-1.2deg);
    box-shadow: 0 18px 36px rgba(9, 59, 46, 0.18);
  }}
  .ui-window {{
    position: relative;
    width: 860px;
    height: 625px;
    margin: 0 auto;
    background: #F8FAFC;
    border: 10px solid rgba(255, 255, 255, 0.96);
    border-radius: 30px;
    transform: rotate(-1.6deg);
    box-shadow: 0 28px 60px rgba(9, 59, 46, 0.28);
    overflow: visible;
    display: flex;
    flex-direction: column;
  }}
  .ui-topbar {{
    height: 68px;
    background: linear-gradient(90deg, #3B82F6 0%, #4F46E5 55%, #6366F1 100%);
    border-radius: 20px 20px 0 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    color: #FFFFFF;
  }}
  .repo-path {{
    font-family: 'Consolas', monospace;
    font-size: 22px;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .top-actions {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .plus-circle {{
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: rgba(255,255,255,0.22);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
  }}
  .share-btn {{
    background: #FFFFFF;
    color: #1E1B4B;
    font-size: 17px;
    font-weight: 800;
    padding: 8px 18px;
    border-radius: 12px;
  }}

  /* UI Body: Left Sidebar + Main Hero Emerald Card */
  .ui-body {{
    display: flex;
    padding: 20px 24px 14px 18px;
    gap: 18px;
    flex: 1;
  }}
  .ui-sidebar {{
    width: 96px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding-top: 8px;
  }}
  .sb-item {{
    text-align: center;
  }}
  .sb-icon {{
    width: 44px;
    height: 44px;
    margin: 0 auto 4px auto;
    border-radius: 12px;
    background: #ECFCCB;
    border: 2px solid #84CC16;
    color: #0D7A5F;
    font-size: 19px;
    font-weight: 900;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .sb-label {{
    font-size: 13px;
    font-weight: 700;
    color: #334155;
  }}

  /* Main Emerald-Lime Hero Card inside UI Window */
  .hero-green-card {{
    flex: 1;
    background: linear-gradient(135deg, #84CC16 0%, #10B981 48%, #0D7A5F 100%);
    border-radius: 22px;
    padding: 26px 30px;
    color: #FFFFFF;
    position: relative;
    box-shadow: inset 0 2px 6px rgba(255,255,255,0.35), 0 12px 26px rgba(13,122,95,0.18);
    overflow: hidden;
  }}
  .hgc-title {{
    font-size: 36px;
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: -0.02em;
    max-width: 470px;
  }}
  .hgc-sub {{
    font-size: 20px;
    font-weight: 700;
    color: #ECFCCB;
    margin-top: 6px;
    margin-bottom: 18px;
  }}
  .hb-list {{
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-width: 470px;
    position: relative;
    z-index: 2;
  }}
  .hb-item {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 18px;
    font-weight: 700;
    line-height: 1.32;
    background: rgba(9, 59, 46, 0.28);
    padding: 9px 14px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.22);
  }}
  .hb-dot {{ color: #ECFCCB; }}
  .giant-num {{
    position: absolute;
    right: 22px;
    bottom: -18px;
    font-size: 156px;
    font-weight: 900;
    color: #FFFFFF;
    line-height: 1;
    letter-spacing: -0.05em;
    opacity: 0.96;
    text-shadow: 0 10px 25px rgba(9, 59, 46, 0.25);
  }}

  /* Floating Color Swatch Pill (Left Edge) & Tilted CTA Pill (Right Edge) */
  .swatch-pill {{
    position: absolute;
    left: -46px;
    bottom: 146px;
    background: rgba(244, 249, 232, 0.96);
    border: 7px solid #FFFFFF;
    border-radius: 999px;
    padding: 8px 14px;
    display: flex;
    gap: 10px;
    box-shadow: 0 12px 24px rgba(9, 59, 46, 0.22);
    z-index: 6;
  }}
  .sw-dot {{ width: 26px; height: 26px; border-radius: 50%; }}
  .right-pill-sticker {{
    position: absolute;
    right: -36px;
    top: 112px;
    transform: rotate(3.5deg);
    background: linear-gradient(90deg, #0D7A5F 0%, #84CC16 100%);
    border: 9px solid rgba(244, 249, 232, 0.94);
    border-radius: 999px;
    padding: 11px 28px;
    color: #FFFFFF;
    font-family: 'Consolas', 'Segoe UI', monospace;
    font-size: 20px;
    font-weight: 900;
    letter-spacing: 0.05em;
    box-shadow: 0 16px 32px rgba(9, 59, 46, 0.28);
    z-index: 6;
  }}

  /* Bottom Strip of 5 Mini Preview Cards inside UI Window */
  .mini-strip {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    padding: 0 22px 20px 22px;
  }}
  .mini-card {{
    height: 92px;
    border-radius: 14px;
    padding: 10px 12px;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  }}
  .mini-card.white {{
    background: #FFFFFF;
    border: 2px solid #E2E8F0;
    color: #0B4F3E;
  }}
  .mini-card.green {{
    background: linear-gradient(135deg, #84CC16 0%, #0D7A5F 100%);
    color: #FFFFFF;
  }}
  .mc-top {{
    font-size: 11.5px;
    font-weight: 800;
    opacity: 0.82;
    text-transform: uppercase;
  }}
  .mc-title {{
    font-size: 14.5px;
    font-weight: 800;
    line-height: 1.2;
  }}
  .mc-num {{
    position: absolute;
    right: 10px;
    bottom: 6px;
    font-size: 15px;
    font-weight: 900;
    opacity: 0.85;
  }}

  /* Bottom Footer */
  .bottom-bar {{
    position: absolute;
    bottom: 38px;
    left: 68px;
    right: 68px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #F4F9E8;
    z-index: 5;
  }}
  .bb-left .sub {{ font-size: 18px; opacity: 0.85; }}
  .bb-left .main {{ font-size: 24px; font-weight: 800; color: #FFFFFF; }}
  .bb-mid {{
    font-family: 'Consolas', monospace;
    font-size: 19px;
    font-weight: 700;
    background: rgba(9, 59, 46, 0.35);
    padding: 8px 22px;
    border-radius: 999px;
    border: 1.5px solid rgba(255,255,255,0.3);
  }}
  .bb-right {{
    width: 52px;
    height: 52px;
    border-radius: 14px;
    border: 3px solid #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    color: #FFFFFF;
  }}
</style>
</head>
<body>
  <div class="mesh-glow"></div>
  <div class="iso-grid"></div>

  <div class="top-header">
    <div class="kicker-top">{top_kicker}</div>
    <div class="kicker-sub">Open-Source AI Toolkit • Thực Chiến 2026</div>
    <div class="indigo-badge-wrap">
      <div class="indigo-badge-shadow"></div>
      <div class="indigo-badge">{badge_text}</div>
    </div>
  </div>

  <div class="vector-title-area">
    <div class="vector-box">
      <h1>{boxed_headline}</h1>
      <span class="vh tl"></span><span class="vh tm"></span><span class="vh tr"></span>
      <span class="vh bl"></span><span class="vh bm"></span><span class="vh br"></span>
    </div>
    <div class="sub-h2">{sub_headline}</div>
    <div class="left-sparkle-ring">✦</div>
    <svg class="cursor-3d" viewBox="0 0 50 50">
      <path d="M10 8 L42 22 L26 28 L20 44 Z" fill="#0D7A5F" stroke="#FFFFFF" stroke-width="3" stroke-linejoin="round"/>
    </svg>
  </div>

  <div class="ui-stage">
    <div class="deck-layer-2"></div>
    <div class="deck-layer-1"></div>

    <div class="ui-window">
      <div class="ui-topbar">
        <div class="repo-path">⚡ {repo_url}</div>
        <div class="top-actions">
          <div class="plus-circle">+</div>
          <div class="share-btn">↗ Star &amp; Clone</div>
        </div>
      </div>

      <div class="ui-body">
        <div class="ui-sidebar">
          {sidebar_html}
        </div>
        <div class="hero-green-card">
          <div class="hgc-title">{hero_card_title}</div>
          <div class="hgc-sub">{hero_card_subtitle}</div>
          <div class="hb-list">
            {bullets_html}
          </div>
          <div class="giant-num">{card_number}</div>
        </div>
      </div>

      <div class="mini-strip">
        {mini_html}
      </div>

      <div class="swatch-pill">
        <div class="sw-dot" style="background:#0B4F3E"></div>
        <div class="sw-dot" style="background:#10B981"></div>
        <div class="sw-dot" style="background:#A3E635"></div>
      </div>
      <div class="right-pill-sticker">{right_pill_text}</div>
    </div>
  </div>

  <div class="bottom-bar">
    <div class="bb-left">
      <div class="sub">Curated by</div>
      <div class="main">AI Players - Người chơi hệ AI</div>
    </div>
    <div class="bb-mid">GITHUB TRENDING • 2026 OCTOBER</div>
    <div class="bb-right">🔖</div>
  </div>
</body>
</html>
"""


# ============================================================================
# 3. SALES PAGES — STYLE 02 TEMPLATE (Editorial Macro + 3-Detail Grid)
# ============================================================================

def build_sales_style02_html(
    page_name: str,
    page_sub: str,
    accent_color: str,
    product_title_spaced: str,
    product_subtitle: str,
    product_italic_hook: str,
    price_tag: str,
    hero_svg: str,
    macro_bg_svg: str,
    macro_kicker: str,
    macro_lines: list[str],
    detail_boxes: list[tuple[str, str, str]],
) -> str:
    m_lines_html = "".join(f'<div class="m-line">{ln}</div>' for ln in macro_lines)
    d_boxes_html = ""
    for d_svg, d_title, d_desc in detail_boxes:
        d_boxes_html += f"""
        <div class="detail-col">
          <div class="detail-img-box">
            {d_svg}
          </div>
          <div class="detail-cap-title">{d_title}</div>
          <div class="detail-cap-desc">{d_desc}</div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px;
    height: 1350px;
    overflow: hidden;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #F8F8F6;
    color: #1E2225;
    position: relative;
  }}
  /* Top 72% Split Editorial Layout */
  .top-editorial {{
    position: relative;
    width: 1080px;
    height: 940px;
    display: flex;
  }}
  .left-studio {{
    width: 640px;
    padding: 54px 0 0 64px;
    position: relative;
    z-index: 3;
  }}
  .brand-kicker {{
    font-size: 22px;
    font-weight: 900;
    color: {accent_color};
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }}
  .brand-sub {{
    font-size: 13px;
    font-weight: 700;
    color: #64748B;
    letter-spacing: 0.28em;
    margin-top: 3px;
    margin-bottom: 28px;
  }}
  .prod-spaced-title {{
    font-size: 62px;
    font-weight: 800;
    color: #111827;
    letter-spacing: 0.18em;
    line-height: 1.08;
    text-transform: uppercase;
  }}
  .prod-sub {{
    font-size: 24px;
    font-weight: 700;
    color: {accent_color};
    letter-spacing: 0.08em;
    margin-top: 10px;
    text-transform: uppercase;
  }}
  .prod-italic {{
    font-size: 19px;
    font-style: italic;
    color: #475569;
    margin-top: 8px;
  }}
  .price-pill {{
    display: inline-block;
    margin-top: 16px;
    background: {accent_color};
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 0.06em;
    padding: 7px 18px;
    border-radius: 999px;
  }}
  .hero-product-stage {{
    position: absolute;
    left: 56px;
    top: 295px;
    width: 660px;
    height: 620px;
    z-index: 4;
  }}

  /* Right 40% Macro Texture Column with Feathered Bottom Fade */
  .right-macro {{
    position: absolute;
    right: 0;
    top: 0;
    width: 455px;
    height: 910px;
    overflow: hidden;
    z-index: 2;
  }}
  .macro-art {{
    width: 100%;
    height: 100%;
  }}
  .macro-fade {{
    position: absolute;
    inset: 0;
    background:
      linear-gradient(to bottom, rgba(248,248,246,0) 0%, rgba(248,248,246,0) 68%, #F8F8F6 98%),
      linear-gradient(to right, #F8F8F6 0%, rgba(248,248,246,0) 18%);
  }}
  .macro-text-overlay {{
    position: absolute;
    top: 96px;
    left: 44px;
    right: 36px;
    text-align: center;
    color: #FFFFFF;
    z-index: 5;
  }}
  .macro-kicker {{
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    opacity: 0.9;
    margin-bottom: 58px;
  }}
  .m-line {{
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 0.14em;
    line-height: 1.65;
    text-transform: uppercase;
    text-shadow: 0 2px 12px rgba(0,0,0,0.45);
  }}

  /* Bottom 28% Strip: 3 Detail Squares + 2-Line Captions */
  .bottom-grid-strip {{
    position: absolute;
    bottom: 34px;
    left: 56px;
    right: 56px;
    height: 365px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 28px;
    z-index: 6;
  }}
  .detail-col {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }}
  .detail-img-box {{
    width: 100%;
    height: 265px;
    background: #FFFFFF;
    border: 4px solid #FFFFFF;
    border-radius: 8px;
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
    overflow: hidden;
    position: relative;
  }}
  .detail-cap-title {{
    margin-top: 16px;
    font-size: 17.5px;
    font-weight: 900;
    letter-spacing: 0.1em;
    color: #1E293B;
    text-transform: uppercase;
  }}
  .detail-cap-desc {{
    margin-top: 4px;
    font-size: 16px;
    font-style: italic;
    font-weight: 600;
    color: #475569;
  }}
</style>
</head>
<body>
  <div class="top-editorial">
    <div class="left-studio">
      <div class="brand-kicker">{page_name}</div>
      <div class="brand-sub">{page_sub}</div>
      <div class="prod-spaced-title">{product_title_spaced}</div>
      <div class="prod-sub">{product_subtitle}</div>
      <div class="prod-italic">{product_italic_hook}</div>
      <div class="price-pill">{price_tag}</div>
    </div>

    <div class="hero-product-stage">
      {hero_svg}
    </div>

    <div class="right-macro">
      <div class="macro-art">{macro_bg_svg}</div>
      <div class="macro-fade"></div>
      <div class="macro-text-overlay">
        <div class="macro-kicker">{macro_kicker}</div>
        {m_lines_html}
      </div>
    </div>
  </div>

  <div class="bottom-grid-strip">
    {d_boxes_html}
  </div>
</body>
</html>
"""


# ============================================================================
# 4. SALES PAGES — STYLE 01 TEMPLATE (Organic Stepped L-Shape Cutout Card)
# ============================================================================

def build_sales_style01_html(
    bg_hex: str,
    cream_hex: str,
    page_name: str,
    page_tagline: str,
    product_badge: str,
    benefit_lines: list[str],
    cta_pill_text: str,
    cutout_product_svg: str,
    footer_left: str,
    footer_right: str,
) -> str:
    b_html = "".join(f'<div class="ben-line">{b}</div>' for b in benefit_lines)

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px;
    height: 1350px;
    overflow: hidden;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    background: {bg_hex};
    color: {cream_hex};
    position: relative;
  }}
  /* Top Center Minimalist Brand Logo (Exact Style 01 reference) */
  .top-brand {{
    position: relative;
    z-index: 3;
    text-align: center;
    padding-top: 48px;
  }}
  .brand-icon-box {{
    width: 68px;
    height: 54px;
    margin: 0 auto 10px auto;
  }}
  .brand-title {{
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: {cream_hex};
  }}
  .brand-sub {{
    font-size: 15px;
    opacity: 0.78;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 3px;
  }}

  /* Center Organic Stepped L-Shape Cream Card (SVG path with smooth concave inner fillet) */
  .l-card-stage {{
    position: relative;
    width: 1080px;
    height: 980px;
    margin-top: 24px;
    z-index: 2;
  }}
  .l-shape-svg {{
    position: absolute;
    inset: 0;
    width: 1080px;
    height: 980px;
  }}

  /* Upper-Left Benefit Copy & Pill inside Cream Card */
  .copy-zone {{
    position: absolute;
    top: 112px;
    left: 185px;
    width: 465px;
    z-index: 4;
    color: {bg_hex};
  }}
  .prod-kicker {{
    display: inline-block;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 6px 16px;
    border-radius: 999px;
    border: 2px solid {bg_hex};
    margin-bottom: 18px;
  }}
  .ben-line {{
    font-size: 52px;
    font-weight: 600;
    line-height: 1.17;
    letter-spacing: -0.02em;
    color: {bg_hex};
  }}
  .cta-pill {{
    display: inline-block;
    margin-top: 28px;
    background: {bg_hex};
    color: {cream_hex};
    font-size: 22px;
    font-weight: 700;
    padding: 13px 34px;
    border-radius: 999px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
  }}

  /* Lower-Right Product Cutout with 3D Frame-Break over bottom edge */
  .product-cutout-zone {{
    position: absolute;
    right: 95px;
    bottom: 20px;
    width: 580px;
    height: 600px;
    z-index: 5;
  }}

  /* Bottom Footer */
  .bottom-footer {{
    position: absolute;
    bottom: 48px;
    left: 96px;
    right: 96px;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    color: {cream_hex};
    z-index: 4;
  }}
  .bf-left .sub {{ font-size: 20px; opacity: 0.85; }}
  .bf-left .main {{ font-size: 24px; font-weight: 700; margin-top: 2px; }}
  .bf-right {{
    font-size: 24px;
    font-weight: 700;
    background: rgba(255,255,255,0.10);
    border: 1.5px solid rgba(255,255,255,0.28);
    padding: 10px 24px;
    border-radius: 999px;
  }}
</style>
</head>
<body>
  <div class="top-brand">
    <svg class="brand-icon-box" viewBox="0 0 80 60" fill="none" stroke="{cream_hex}" stroke-width="3">
      <rect x="14" y="8" width="52" height="14" rx="5"/>
      <rect x="10" y="22" width="60" height="14" rx="5"/>
      <line x1="22" y1="36" x2="22" y2="52"/>
      <line x1="58" y1="36" x2="58" y2="52"/>
      <circle cx="40" cy="15" r="2" fill="{cream_hex}"/>
      <circle cx="40" cy="29" r="2" fill="{cream_hex}"/>
    </svg>
    <div class="brand-title">{page_name}</div>
    <div class="brand-sub">{page_tagline}</div>
  </div>

  <div class="l-card-stage">
    <!-- Unified Stepped L-Shape with rounded outer corners AND smooth concave inner corners -->
    <svg class="l-shape-svg" viewBox="0 0 1080 980">
      <defs>
        <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
          <feDropShadow dx="0" dy="20" stdDeviation="24" flood-color="#000000" flood-opacity="0.22"/>
        </filter>
      </defs>
      <path filter="url(#cardShadow)" fill="{cream_hex}" d="
        M 210 50
        L 570 50
        A 80 80 0 0 1 650 130
        L 650 280
        A 80 80 0 0 0 730 360
        L 870 360
        A 80 80 0 0 1 950 440
        L 950 800
        A 80 80 0 0 1 870 880
        L 490 880
        A 80 80 0 0 1 410 800
        L 410 660
        A 80 80 0 0 0 330 580
        L 210 580
        A 80 80 0 0 1 130 500
        L 130 130
        A 80 80 0 0 1 210 50
        Z
      "/>
      <!-- Ground contact shadow on the lower step of the Cream card -->
      <ellipse cx="690" cy="852" rx="210" ry="24" fill="rgba(0,0,0,0.18)"/>
    </svg>

    <div class="copy-zone">
      <div class="prod-kicker">{product_badge}</div>
      {b_html}
      <div class="cta-pill">{cta_pill_text}</div>
    </div>

    <div class="product-cutout-zone">
      {cutout_product_svg}
    </div>
  </div>

  <div class="bottom-footer">
    <div class="bf-left">
      <div class="sub">Mua chính hãng giá tốt:</div>
      <div class="main">{footer_left}</div>
    </div>
    <div class="bf-right">{footer_right}</div>
  </div>
</body>
</html>
"""


# ============================================================================
# 5. HIGH-PRECISION STUDIO SVG ILLUSTRATIONS FOR THE 6 SHOPEE SKUS
# ============================================================================

# --- SKU 1: Máy hút bụi mini cầm tay không dây đa đầu hút (Sạc Type-C) ---
VACUUM_HERO_SVG = """
<svg viewBox="0 0 660 620" width="100%" height="100%">
  <defs>
    <linearGradient id="vacBody" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#374151"/>
      <stop offset="45%" stop-color="#1F2937"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="vacCup" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="rgba(226,232,240,0.82)"/>
      <stop offset="50%" stop-color="rgba(148,163,184,0.45)"/>
      <stop offset="100%" stop-color="rgba(203,213,225,0.85)"/>
    </linearGradient>
    <linearGradient id="hepaGold" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#445D27"/>
      <stop offset="100%" stop-color="#65A30D"/>
    </linearGradient>
  </defs>
  <!-- Studio Floor Contact Shadow -->
  <ellipse cx="315" cy="545" rx="235" ry="30" fill="rgba(15,23,42,0.14)"/>
  <ellipse cx="305" cy="542" rx="150" ry="16" fill="rgba(15,23,42,0.22)"/>

  <!-- Main Angled Cordless Mini Vacuum Assembly -->
  <g transform="translate(55, 95) rotate(-14, 280, 210)">
    <!-- 2-in-1 Crevice Nozzle + Brush Attachment -->
    <polygon points="10,188 165,168 165,206 10,202" fill="#334155" stroke="#475569" stroke-width="2"/>
    <!-- Brush Bristles on Nozzle Tip -->
    <g fill="#0F172A">
      <rect x="6" y="176" width="24" height="34" rx="4" fill="#445D27"/>
      <line x1="6" y1="180" x2="-12" y2="175" stroke="#1E293B" stroke-width="3"/>
      <line x1="6" y1="186" x2="-14" y2="184" stroke="#1E293B" stroke-width="3"/>
      <line x1="6" y1="192" x2="-14" y2="192" stroke="#1E293B" stroke-width="3"/>
      <line x1="6" y1="198" x2="-14" y2="200" stroke="#1E293B" stroke-width="3"/>
      <line x1="6" y1="204" x2="-12" y2="208" stroke="#1E293B" stroke-width="3"/>
    </g>

    <!-- 200ml Transparent Dust Cup + Inner Washable HEPA Pleated Filter -->
    <rect x="160" y="132" width="138" height="114" rx="18" fill="url(#vacCup)" stroke="#94A3B8" stroke-width="3"/>
    <!-- Inner HEPA Filter Cylinder -->
    <rect x="206" y="148" width="74" height="82" rx="8" fill="#F8FAFC" stroke="#64748B" stroke-width="2"/>
    <g stroke="#CBD5E1" stroke-width="2">
      <line x1="216" y1="152" x2="216" y2="226"/>
      <line x1="226" y1="152" x2="226" y2="226"/>
      <line x1="236" y1="152" x2="236" y2="226"/>
      <line x1="246" y1="152" x2="246" y2="226"/>
      <line x1="256" y1="152" x2="256" y2="226"/>
      <line x1="266" y1="152" x2="266" y2="226"/>
    </g>
    <rect x="274" y="142" width="16" height="94" rx="4" fill="url(#hepaGold)"/>

    <!-- Main Motor Turbine Cylinder -->
    <rect x="292" y="124" width="195" height="130" rx="62" fill="url(#vacBody)" stroke="#475569" stroke-width="2"/>
    <!-- Metallic Olive Accent Ring -->
    <rect x="292" y="124" width="18" height="130" rx="6" fill="url(#hepaGold)"/>
    <!-- Side Air Exhaust Vents -->
    <g fill="#0F172A" stroke="#64748B" stroke-width="1.5">
      <rect x="355" y="158" width="48" height="8" rx="4"/>
      <rect x="355" y="174" width="48" height="8" rx="4"/>
      <rect x="355" y="190" width="48" height="8" rx="4"/>
    </g>
    <!-- Power Button & LED Indicator -->
    <circle cx="332" cy="148" r="7" fill="#84CC16"/>
    <!-- Ergonomic Handle & Type-C Base -->
    <path d="M 380 246 L 435 375 C 442 392, 478 390, 474 368 L 448 242 Z" fill="url(#vacBody)" stroke="#374151" stroke-width="2"/>
    <!-- Type-C Charging Port Highlight at Base -->
    <rect x="444" y="362" width="18" height="7" rx="3.5" fill="#A3E635"/>
  </g>

  <!-- Secondary Wide Floor/Mattress Nozzle Lying on Studio Floor -->
  <g transform="translate(115, 445)">
    <rect x="0" y="20" width="165" height="44" rx="12" fill="#1E293B" stroke="#475569" stroke-width="2"/>
    <rect x="58" y="0" width="48" height="26" rx="6" fill="#334155"/>
    <line x1="16" y1="54" x2="148" y2="54" stroke="#84CC16" stroke-width="3"/>
  </g>
</svg>
"""

VACUUM_MACRO_SVG = """
<svg viewBox="0 0 455 910" width="100%" height="100%">
  <defs>
    <linearGradient id="mVacBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2E3F1C"/>
      <stop offset="50%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <pattern id="hepaMesh" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="rotate(25)">
      <rect width="9" height="18" fill="rgba(255,255,255,0.08)"/>
      <line x1="0" y1="0" x2="0" y2="18" stroke="rgba(163,230,53,0.28)" stroke-width="2"/>
    </pattern>
  </defs>
  <rect width="455" height="910" fill="url(#mVacBg)"/>
  <circle cx="280" cy="440" r="290" fill="url(#hepaMesh)" stroke="rgba(163,230,53,0.4)" stroke-width="8"/>
  <circle cx="280" cy="440" r="195" fill="none" stroke="rgba(255,255,255,0.18)" stroke-width="22" stroke-dasharray="14 10"/>
  <circle cx="280" cy="440" r="110" fill="#111827" stroke="#84CC16" stroke-width="4"/>
</svg>
"""

VACUUM_D1_SVG = """
<svg viewBox="0 0 300 265" width="100%" height="100%">
  <rect width="300" height="265" fill="#F1F5F9"/>
  <rect x="40" y="112" width="170" height="36" rx="8" fill="#1E293B"/>
  <rect x="175" y="96" width="52" height="68" rx="8" fill="#445D27"/>
  <g stroke="#0F172A" stroke-width="3">
    <line x1="227" y1="104" x2="262" y2="98"/><line x1="227" y1="116" x2="265" y2="114"/>
    <line x1="227" y1="130" x2="266" y2="130"/><line x1="227" y1="144" x2="265" y2="146"/>
    <line x1="227" y1="156" x2="262" y2="162"/>
  </g>
  <text x="150" y="232" text-anchor="middle" font-size="15" font-weight="700" fill="#445D27">Đầu hút dẹt + Chổi quét</text>
</svg>
"""

VACUUM_D2_SVG = """
<svg viewBox="0 0 300 265" width="100%" height="100%">
  <rect width="300" height="265" fill="#F1F5F9"/>
  <rect x="85" y="48" width="130" height="145" rx="16" fill="#FFFFFF" stroke="#64748B" stroke-width="4"/>
  <rect x="85" y="48" width="130" height="26" rx="8" fill="#445D27"/>
  <g stroke="#CBD5E1" stroke-width="4">
    <line x1="105" y1="82" x2="105" y2="182"/><line x1="123" y1="82" x2="123" y2="182"/>
    <line x1="141" y1="82" x2="141" y2="182"/><line x1="159" y1="82" x2="159" y2="182"/>
    <line x1="177" y1="82" x2="177" y2="182"/><line x1="195" y1="82" x2="195" y2="182"/>
  </g>
  <circle cx="215" cy="175" r="24" fill="#38BDF8" opacity="0.85"/>
  <text x="215" y="181" text-anchor="middle" font-size="14" font-weight="800" fill="#FFF">H2O</text>
  <text x="150" y="232" text-anchor="middle" font-size="15" font-weight="700" fill="#445D27">Rửa sạch tái sử dụng</text>
</svg>
"""

VACUUM_D3_SVG = """
<svg viewBox="0 0 300 265" width="100%" height="100%">
  <rect width="300" height="265" fill="#F1F5F9"/>
  <rect x="55" y="65" width="190" height="115" rx="22" fill="#1E293B"/>
  <rect x="108" y="106" width="84" height="34" rx="17" fill="#0F172A" stroke="#84CC16" stroke-width="3"/>
  <rect x="126" y="119" width="48" height="8" rx="4" fill="#84CC16"/>
  <text x="150" y="232" text-anchor="middle" font-size="15" font-weight="700" fill="#445D27">Cổng sạc nhanh USB Type-C</text>
</svg>
"""


# --- SKU 3: Quạt tích điện mini kẹp thành giường & để bàn xoay 360 độ ---
FAN_HERO_SVG = """
<svg viewBox="0 0 660 620" width="100%" height="100%">
  <defs>
    <linearGradient id="fanShell" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="60%" stop-color="#E2E8F0"/>
      <stop offset="100%" stop-color="#CBD5E1"/>
    </linearGradient>
    <linearGradient id="navyBlade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#284166"/>
      <stop offset="100%" stop-color="#1E3A8A"/>
    </linearGradient>
  </defs>
  <ellipse cx="320" cy="555" rx="215" ry="26" fill="rgba(15,23,42,0.14)"/>

  <!-- 360 U-Shaped Gimbal Neck Arm -->
  <path d="M 185 235 C 155 340, 210 425, 320 425 C 430 425, 485 340, 455 235" fill="none" stroke="#94A3B8" stroke-width="22" stroke-linecap="round"/>
  <!-- 360 Pivot Knobs on Left & Right -->
  <circle cx="180" cy="235" r="20" fill="#284166" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="460" cy="235" r="20" fill="#284166" stroke="#FFFFFF" stroke-width="3"/>

  <!-- Circular Fan Head + Dense Detachable Safety Grille -->
  <circle cx="320" cy="220" r="158" fill="url(#fanShell)" stroke="#94A3B8" stroke-width="6"/>
  <circle cx="320" cy="220" r="142" fill="#1E293B"/>
  <!-- 5 Aerodynamic Quiet Blades inside -->
  <g transform="translate(320, 220)" fill="url(#navyBlade)" opacity="0.92">
    <ellipse cx="0" cy="-76" rx="34" ry="58" transform="rotate(15)"/>
    <ellipse cx="0" cy="-76" rx="34" ry="58" transform="rotate(87)"/>
    <ellipse cx="0" cy="-76" rx="34" ry="58" transform="rotate(159)"/>
    <ellipse cx="0" cy="-76" rx="34" ry="58" transform="rotate(231)"/>
    <ellipse cx="0" cy="-76" rx="34" ry="58" transform="rotate(303)"/>
  </g>
  <!-- Front Radial Grille Spokes -->
  <g transform="translate(320, 220)" stroke="#E2E8F0" stroke-width="2.2" opacity="0.88">
    <circle r="136" fill="none"/><circle r="105" fill="none"/><circle r="72" fill="none"/>
    <line x1="-140" y1="0" x2="140" y2="0"/><line x1="0" y1="-140" x2="0" y2="140"/>
    <line x1="-99" y1="-99" x2="99" y2="99"/><line x1="-99" y1="99" x2="99" y2="-99"/>
    <line x1="-130" y1="-52" x2="130" y2="52"/><line x1="-52" y1="-130" x2="52" y2="130"/>
    <line x1="130" y1="-52" x2="-130" y2="52"/><line x1="52" y1="-130" x2="-52" y2="130"/>
  </g>
  <!-- Center Hub Cap -->
  <circle cx="320" cy="220" r="40" fill="url(#fanShell)" stroke="#284166" stroke-width="4"/>
  <text x="320" y="226" text-anchor="middle" font-size="16" font-weight="900" fill="#284166">360°</text>

  <!-- Vertical Neck Pivot + Heavy-Duty Spring Bed Clamp Base -->
  <rect x="292" y="418" width="56" height="54" rx="10" fill="#CBD5E1" stroke="#94A3B8" stroke-width="3"/>
  <!-- Upper & Lower Clamp Jaws with Silicone Anti-Slip Pads -->
  <path d="M 205 468 L 435 468 C 455 468, 462 495, 435 498 L 245 498 L 245 524 L 442 524 C 466 524, 466 556, 435 556 L 195 556 C 175 556, 175 468, 205 468 Z" fill="url(#fanShell)" stroke="#94A3B8" stroke-width="4"/>
  <!-- Silicone Anti-Slip Pads Inside Clamp -->
  <rect x="260" y="496" width="155" height="9" rx="4" fill="#284166"/>
  <rect x="260" y="517" width="155" height="9" rx="4" fill="#284166"/>
</svg>
"""

FAN_MACRO_SVG = """
<svg viewBox="0 0 455 910" width="100%" height="100%">
  <defs>
    <linearGradient id="mFanBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1E3A8A"/>
      <stop offset="55%" stop-color="#284166"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>
  <rect width="455" height="910" fill="url(#mFanBg)"/>
  <g transform="translate(310, 430)" stroke="rgba(255,255,255,0.22)" stroke-width="4" fill="none">
    <circle r="320"/><circle r="270"/><circle r="220"/><circle r="170"/><circle r="120"/><circle r="70"/>
    <line x1="-340" y1="0" x2="340" y2="0"/><line x1="0" y1="-340" x2="0" y2="340"/>
    <line x1="-240" y1="-240" x2="240" y2="240"/><line x1="-240" y1="240" x2="240" y2="-240"/>
  </g>
</svg>
"""

FAN_D1_SVG = """
<svg viewBox="0 0 300 265" width="100%" height="100%">
  <rect width="300" height="265" fill="#F1F5F9"/>
  <path d="M 55 75 L 235 75 L 235 108 L 105 108 L 105 148 L 240 148 L 240 182 L 55 182 Z" fill="#CBD5E1" stroke="#64748B" stroke-width="3"/>
  <rect x="115" y="106" width="110" height="12" rx="4" fill="#284166"/>
  <rect x="115" y="138" width="110" height="12" rx="4" fill="#284166"/>
  <text x="150" y="232" text-anchor="middle" font-size="15" font-weight="700" fill="#284166">Đệm Silicon bám chặt thành giường</text>
</svg>
"""

FAN_D2_SVG = """
<svg viewBox="0 0 300 265" width="100%" height="100%">
  <rect width="300" height="265" fill="#F1F5F9"/>
  <circle cx="150" cy="122" r="58" fill="#E2E8F0" stroke="#284166" stroke-width="4"/>
  <path d="M 80 122 A 70 32 0 1 0 220 122" fill="none" stroke="#0EA5E9" stroke-width="4" stroke-dasharray="6 4"/>
  <path d="M 150 52 A 32 70 0 1 0 150 192" fill="none" stroke="#0EA5E9" stroke-width="4" stroke-dasharray="6 4"/>
  <text x="150" y="128" text-anchor="middle" font-size="20" font-weight="900" fill="#284166">360°</text>
  <text x="150" y="232" text-anchor="middle" font-size="15" font-weight="700" fill="#284166">Xoay ngang &amp; dọc linh hoạt</text>
</svg>
"""

FAN_D3_SVG = """
<svg viewBox="0 0 300 265" width="100%" height="100%">
  <rect width="300" height="265" fill="#F1F5F9"/>
  <circle cx="150" cy="122" r="68" fill="#1E293B" stroke="#94A3B8" stroke-width="5"/>
  <circle cx="150" cy="122" r="48" fill="none" stroke="#CBD5E1" stroke-width="2"/>
  <circle cx="150" cy="122" r="24" fill="#284166"/>
  <text x="150" y="232" text-anchor="middle" font-size="15" font-weight="700" fill="#284166">Lồng đan khít tháo rời rửa dễ</text>
</svg>
"""


# --- SKU 5: Giá đỡ điện thoại / Laptop xoay 360 độ hợp kim nhôm gấp gọn ---
STAND_HERO_SVG = """
<svg viewBox="0 0 660 620" width="100%" height="100%">
  <defs>
    <linearGradient id="aluMetal" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E2E8F0"/>
      <stop offset="45%" stop-color="#94A3B8"/>
      <stop offset="100%" stop-color="#475569"/>
    </linearGradient>
    <linearGradient id="aluDark" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#64748B"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
  </defs>
  <ellipse cx="330" cy="542" rx="230" ry="28" fill="rgba(15,23,42,0.16)"/>

  <!-- 360 Mechanical Gear Rotating Circular Base -->
  <ellipse cx="330" cy="510" rx="185" ry="38" fill="url(#aluDark)" stroke="#94A3B8" stroke-width="3"/>
  <ellipse cx="330" cy="500" rx="185" ry="36" fill="url(#aluMetal)" stroke="#CBD5E1" stroke-width="2"/>
  <!-- Mechanical Gear Ring Center -->
  <ellipse cx="330" cy="500" rx="95" ry="18" fill="none" stroke="#334155" stroke-width="5" stroke-dasharray="10 6"/>

  <!-- Dual Z-Pillar Heavy Anodized Support Arms -->
  <polygon points="245,495 275,495 365,275 335,275" fill="url(#aluDark)" stroke="#CBD5E1" stroke-width="2"/>
  <polygon points="355,495 385,495 455,275 425,275" fill="url(#aluMetal)" stroke="#CBD5E1" stroke-width="2"/>
  <!-- Ergonomic Torque Hinge Joints -->
  <circle cx="260" cy="492" r="14" fill="#1E293B" stroke="#E2E8F0" stroke-width="3"/>
  <circle cx="350" cy="278" r="14" fill="#1E293B" stroke="#E2E8F0" stroke-width="3"/>

  <!-- Tilted Top Aluminum Plate with Airflow Cutouts & Silicone Pads -->
  <g transform="translate(85, 95) rotate(-16, 240, 140)">
    <rect x="20" y="40" width="440" height="240" rx="26" fill="url(#aluMetal)" stroke="#F8FAFC" stroke-width="4"/>
    <!-- Hollow Heat-Dissipation Airflow Slots -->
    <g fill="#1E293B" opacity="0.82">
      <rect x="115" y="85" width="250" height="22" rx="11"/>
      <rect x="95" y="125" width="290" height="22" rx="11"/>
      <rect x="115" y="165" width="250" height="22" rx="11"/>
    </g>
    <!-- Non-Slip Dark Silicone Strips + Front Device Lip Hooks -->
    <rect x="48" y="64" width="26" height="180" rx="8" fill="#1E293B"/>
    <rect x="406" y="64" width="26" height="180" rx="8" fill="#1E293B"/>
    <rect x="95" y="258" width="68" height="30" rx="10" fill="#1E293B" stroke="#CBD5E1" stroke-width="2"/>
    <rect x="317" y="258" width="68" height="30" rx="10" fill="#1E293B" stroke="#CBD5E1" stroke-width="2"/>
  </g>
</svg>
"""

STAND_MACRO_SVG = """
<svg viewBox="0 0 455 910" width="100%" height="100%">
  <defs>
    <linearGradient id="mAluBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>
  <rect width="455" height="910" fill="url(#mAluBg)"/>
  <!-- CNC Anodized Gear Ring Macro -->
  <circle cx="300" cy="450" r="260" fill="none" stroke="rgba(226,232,240,0.22)" stroke-width="36" stroke-dasharray="18 12"/>
  <circle cx="300" cy="450" r="190" fill="none" stroke="rgba(148,163,184,0.35)" stroke-width="14"/>
  <circle cx="300" cy="450" r="120" fill="#1E293B" stroke="#94A3B8" stroke-width="6"/>
</svg>
"""

STAND_D1_SVG = """
<svg viewBox="0 0 300 265" width="100%" height="100%">
  <rect width="300" height="265" fill="#F1F5F9"/>
  <circle cx="150" cy="122" r="72" fill="#94A3B8" stroke="#334155" stroke-width="4"/>
  <circle cx="150" cy="122" r="50" fill="none" stroke="#1E293B" stroke-width="8" stroke-dasharray="10 6"/>
  <circle cx="150" cy="122" r="22" fill="#1E293B"/>
  <text x="150" y="232" text-anchor="middle" font-size="15" font-weight="700" fill="#1E293B">Bánh răng xoay 360° kêu cạch cạch</text>
</svg>
"""

STAND_D2_SVG = """
<svg viewBox="0 0 300 265" width="100%" height="100%">
  <rect width="300" height="265" fill="#F1F5F9"/>
  <rect x="45" y="75" width="210" height="95" rx="18" fill="#94A3B8" stroke="#475569" stroke-width="3"/>
  <rect x="68" y="95" width="164" height="24" rx="12" fill="#1E293B"/>
  <rect x="68" y="130" width="164" height="24" rx="12" fill="#1E293B"/>
  <text x="150" y="232" text-anchor="middle" font-size="15" font-weight="700" fill="#1E293B">Đệm Silicon dày chống trượt &amp; trầy</text>
</svg>
"""

STAND_D3_SVG = """
<svg viewBox="0 0 300 265" width="100%" height="100%">
  <rect width="300" height="265" fill="#F1F5F9"/>
  <rect x="48" y="65" width="204" height="115" rx="16" fill="#CBD5E1" stroke="#475569" stroke-width="3"/>
  <rect x="78" y="88" width="144" height="16" rx="8" fill="#0EA5E9"/>
  <rect x="78" y="114" width="144" height="16" rx="8" fill="#0EA5E9"/>
  <rect x="78" y="140" width="144" height="16" rx="8" fill="#0EA5E9"/>
  <text x="150" y="232" text-anchor="middle" font-size="15" font-weight="700" fill="#1E293B">Khe thoáng tản nhiệt nhanh</text>
</svg>
"""


# --- SKU 2 (Style 01): Dụng cụ cắt gọt rau củ đa năng kèm rổ ráo nước ---
SLICER_CUTOUT_SVG = """
<svg viewBox="0 0 580 600" width="100%" height="100%">
  <defs>
    <linearGradient id="bowlPP" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="65%" stop-color="#E2E8F0"/>
      <stop offset="100%" stop-color="#CBD5E1"/>
    </linearGradient>
    <linearGradient id="oliveLid" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#445D27"/>
      <stop offset="50%" stop-color="#65A30D"/>
      <stop offset="100%" stop-color="#365314"/>
    </linearGradient>
  </defs>

  <!-- Outer PP Drain Basin + Side Handles (Chồm nhẹ xuống đáy khối Kem tạo Frame Break 3D) -->
  <path d="M 75 265 L 505 265 L 465 515 C 455 558, 395 575, 290 575 C 185 575, 125 558, 115 515 Z" fill="url(#bowlPP)" stroke="#94A3B8" stroke-width="4"/>
  <!-- Left & Right Pivot Handles -->
  <rect x="38" y="252" width="52" height="28" rx="14" fill="url(#oliveLid)"/>
  <rect x="490" y="252" width="52" height="28" rx="14" fill="url(#oliveLid)"/>

  <!-- Inner Tilted Rotating Colander Strainer Slots Visible -->
  <g fill="#65A30D" opacity="0.78">
    <rect x="175" y="365" width="12" height="95" rx="6"/>
    <rect x="205" y="375" width="12" height="95" rx="6"/>
    <rect x="235" y="380" width="12" height="95" rx="6"/>
    <rect x="265" y="382" width="12" height="95" rx="6"/>
    <rect x="295" y="382" width="12" height="95" rx="6"/>
    <rect x="325" y="380" width="12" height="95" rx="6"/>
    <rect x="355" y="375" width="12" height="95" rx="6"/>
    <rect x="385" y="365" width="12" height="95" rx="6"/>
  </g>

  <!-- Top Slicing Deck + Stainless Steel 420 Blade Slot -->
  <ellipse cx="290" cy="255" rx="220" ry="52" fill="url(#oliveLid)" stroke="#FFFFFF" stroke-width="4"/>
  <rect x="175" y="232" width="230" height="44" rx="10" fill="#CBD5E1" stroke="#475569" stroke-width="3"/>
  <!-- Julienne Stainless Blade Teeth -->
  <line x1="200" y1="254" x2="380" y2="254" stroke="#334155" stroke-width="4" stroke-dasharray="10 6"/>

  <!-- Ergonomic Hand Guard Pusher Hat on Top -->
  <ellipse cx="320" cy="195" rx="68" ry="26" fill="#F97316" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M 272 195 C 272 145, 368 145, 368 195 Z" fill="#FB923C"/>
  <rect x="298" y="132" width="44" height="22" rx="11" fill="#EA580C"/>

  <!-- Floating Extra Interchangeable Blade Inserts -->
  <g transform="translate(165, 68) rotate(-10)">
    <rect x="0" y="0" width="125" height="54" rx="10" fill="#FFFFFF" stroke="#445D27" stroke-width="3"/>
    <line x1="18" y1="27" x2="107" y2="27" stroke="#64748B" stroke-width="5" stroke-dasharray="8 5"/>
  </g>
  <g transform="translate(385, 78) rotate(10)">
    <rect x="0" y="0" width="125" height="54" rx="10" fill="#FFFFFF" stroke="#445D27" stroke-width="3"/>
    <circle cx="40" cy="27" r="7" fill="#64748B"/><circle cx="64" cy="27" r="7" fill="#64748B"/><circle cx="88" cy="27" r="7" fill="#64748B"/>
  </g>

  <!-- Non-slip Base Legs Breaking Below the Cream Card Edge -->
  <rect x="175" y="558" width="38" height="28" rx="10" fill="#365314"/>
  <rect x="367" y="558" width="38" height="28" rx="10" fill="#365314"/>
</svg>
"""


# --- SKU 4 (Style 01): Bộ túi nén chân không kèm bơm tay ---
VACBAG_CUTOUT_SVG = """
<svg viewBox="0 0 580 600" width="100%" height="100%">
  <defs>
    <linearGradient id="paBag" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="rgba(255,255,255,0.92)"/>
      <stop offset="50%" stop-color="rgba(224,242,254,0.82)"/>
      <stop offset="100%" stop-color="rgba(186,230,253,0.90)"/>
    </linearGradient>
  </defs>

  <!-- Stack of 3 Compressed Vacuum Bags Showing 75% Space Saving -->
  <!-- Bottom Bag #3 -->
  <g transform="translate(45, 365)">
    <rect x="0" y="0" width="430" height="96" rx="24" fill="url(#paBag)" stroke="#38BDF8" stroke-width="3.5"/>
    <rect x="26" y="18" width="378" height="60" rx="14" fill="#FDE68A" opacity="0.75"/>
    <line x1="18" y1="12" x2="412" y2="12" stroke="#0284C7" stroke-width="5"/>
  </g>

  <!-- Middle Bag #2 -->
  <g transform="translate(55, 255)">
    <rect x="0" y="0" width="430" height="96" rx="24" fill="url(#paBag)" stroke="#38BDF8" stroke-width="3.5"/>
    <rect x="26" y="18" width="378" height="60" rx="14" fill="#BFDBFE" opacity="0.82"/>
    <line x1="18" y1="12" x2="412" y2="12" stroke="#0284C7" stroke-width="5"/>
  </g>

  <!-- Top Bag #1 with One-Way Air Valve & Double-Zip Slider -->
  <g transform="translate(65, 135)">
    <rect x="0" y="0" width="430" height="108" rx="26" fill="url(#paBag)" stroke="#0284C7" stroke-width="4"/>
    <rect x="28" y="24" width="374" height="64" rx="16" fill="#A7F3D0" opacity="0.78"/>
    <!-- Double-Zip Seal Lines + Slider Clip -->
    <line x1="20" y1="14" x2="410" y2="14" stroke="#0369A1" stroke-width="4"/>
    <line x1="20" y1="20" x2="410" y2="20" stroke="#0369A1" stroke-width="4"/>
    <rect x="320" y="6" width="38" height="20" rx="6" fill="#0284C7"/>
    <!-- One-Way Suction Valve -->
    <circle cx="215" cy="56" r="32" fill="#FFFFFF" stroke="#0284C7" stroke-width="4"/>
    <circle cx="215" cy="56" r="18" fill="#0284C7"/>
  </g>

  <!-- Hand Suction Pump Breaking Out Below the Bottom Edge of Cream Card -->
  <g transform="translate(365, 260) rotate(16)">
    <!-- T-Handle -->
    <rect x="18" y="0" width="110" height="26" rx="12" fill="#1E293B"/>
    <rect x="64" y="24" width="18" height="55" fill="#94A3B8"/>
    <!-- Pump Cylinder -->
    <rect x="38" y="75" width="70" height="235" rx="18" fill="#F8FAFC" stroke="#0284C7" stroke-width="4"/>
    <rect x="38" y="75" width="70" height="32" rx="8" fill="#0284C7"/>
    <rect x="44" y="306" width="58" height="28" rx="8" fill="#0284C7"/>
  </g>
</svg>
"""


# --- SKU 6 (Style 01): Đèn kẹp màn hình bảo vệ mắt chiếu sáng bất đối xứng ---
LAMP_CUTOUT_SVG = """
<svg viewBox="0 0 580 600" width="100%" height="100%">
  <defs>
    <linearGradient id="warmBeam" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="rgba(253, 224, 71, 0.58)"/>
      <stop offset="55%" stop-color="rgba(254, 240, 138, 0.22)"/>
      <stop offset="100%" stop-color="rgba(254, 240, 138, 0.0)"/>
    </linearGradient>
    <linearGradient id="monitorScreen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>

  <!-- Desktop Monitor Frame + Stand Breaking Out Over Bottom Cream Edge -->
  <rect x="75" y="145" width="430" height="275" rx="18" fill="url(#monitorScreen)" stroke="#475569" stroke-width="6"/>
  <!-- Screen UI Preview (Zero Glare!) -->
  <rect x="98" y="172" width="180" height="16" rx="6" fill="#334155"/>
  <rect x="98" y="200" width="380" height="95" rx="10" fill="rgba(255,255,255,0.06)"/>
  <rect x="98" y="310" width="260" height="80" rx="10" fill="rgba(255,255,255,0.06)"/>
  <text x="290" y="256" text-anchor="middle" font-size="22" font-weight="800" fill="#94A3B8">0% GLARE • MÀN HÌNH TRONG VẮT</text>

  <!-- Monitor Stand Neck & Heavy Base Breaking Below Card -->
  <rect x="262" y="420" width="56" height="115" fill="#475569"/>
  <path d="M 165 535 L 415 535 L 445 572 L 135 572 Z" fill="#334155" stroke="#64748B" stroke-width="3"/>

  <!-- Asymmetric 45-Degree Light Cone Illuminating the Desk -->
  <polygon points="95,118 485,118 555,525 25,525" fill="url(#warmBeam)"/>

  <!-- Counterweight Silicone Clip + Sleek Aluminum Light Bar on Top of Monitor -->
  <rect x="248" y="88" width="84" height="58" rx="12" fill="#1E293B" stroke="#94A3B8" stroke-width="3"/>
  <!-- Sleek Cylindrical LED Bar -->
  <rect x="42" y="96" width="496" height="28" rx="14" fill="#0F172A" stroke="#CBD5E1" stroke-width="3"/>
  <!-- Warm LED Strip Glow Underneath Bar -->
  <rect x="64" y="118" width="452" height="7" rx="3.5" fill="#FDE047"/>
  <!-- Touch Dimming Icons on Bar Center -->
  <circle cx="265" cy="110" r="5" fill="#38BDF8"/>
  <circle cx="290" cy="110" r="5" fill="#FDE047"/>
  <circle cx="315" cy="110" r="5" fill="#F8FAFC"/>
</svg>
"""


# ============================================================================
# 6. MAIN BATCH GENERATOR FOR ALL 11 CAMPAIGN CARDS
# ============================================================================

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    jobs: list[tuple[str, str]] = []

    # 1. ai-01-lead-prompt50-style02.png
    jobs.append((
        "ai-01-lead-prompt50-style02.png",
        build_ai_style02_html(
            kicker_badge="🎁 LEAD MAGNET 11:45 • TẶNG MIỄN PHÍ 100%",
            preview_title="Sổ Tay 50 Siêu Prompt Tự Động Hóa 80% Việc Văn Phòng & Creator",
            preview_items=[
                ("01", "Khung Lệnh 5 Thành Phần", "Role • Context • Task • Constraints • Output Format chuẩn."),
                ("02", "20 Prompt Báo Cáo & Excel", "Phân tích bảng số liệu, viết hàm Sheets & tóm tắt họp 10s."),
                ("03", "20 Prompt Content Đa Kênh", "Nhân bản 1 ý tưởng ra bài FB, kịch bản Reels 30s & cmt mồi."),
                ("04", "10 Prompt Phản Biện Red-Team", "Biến AI thành sếp khó tính rà lỗ hổng kế hoạch trước khi nộp."),
            ],
            headline_lines=["TẶNG BỘ", "50 SIÊU PROMPT", "THỰC CHIẾN!"],
            boxed_line_idx=1,
            pill_1_text='COMMENT "PROMPT50" NHẬN LINK',
            pill_2_text="Save for Later",
            summary_line_1="Trọn bộ 50 cấu trúc lệnh Copy-Paste dùng ngay cho Claude, ChatGPT & Gemini.",
            summary_line_2='Bình luận từ khóa "PROMPT50" bên dưới để nhận trọn bộ tài liệu hoàn toàn miễn phí!',
            footer_left_top="Lead Magnet",
            footer_left_bold="50 Siêu Prompt AI",
            footer_mid_top="2026",
            footer_mid_bold="October",
        ),
    ))

    # 2. ai-02-github-browser-use-style03.png
    jobs.append((
        "ai-02-github-browser-use-style03.png",
        build_ai_style03_html(
            top_kicker="GitHub AI Trending #01 • Khung Giờ 12:30",
            badge_text="⭐ 55,000+ STARS • AI BROWSER AGENT",
            boxed_headline="Tự Động Hóa Trình Duyệt",
            sub_headline="browser-use / browser-use",
            repo_url="github.com/browser-use/browser-use",
            sidebar_items=[
                ("👁️", "Vision"),
                ("🗂️", "MultiTab"),
                ("🔌", "MCP"),
                ("🐍", "Python"),
            ],
            hero_card_title="AI Agent Tự Mở Web, Click Chuột & Điền Form",
            hero_card_subtitle="Kết nối Claude, GPT-4o, Gemini & DeepSeek điều khiển trình duyệt thật",
            hero_bullets=[
                "DOM + Vision Hybrid: Tự đánh số nút bấm trên web, không cần viết XPath.",
                "Multi-Tab & Persistent Session: Giữ nguyên cookies đăng nhập, chạy song song.",
                "Tích hợp chuẩn MCP: Cắm thẳng vào Claude Desktop, Cursor & n8n workflow.",
            ],
            card_number="01",
            right_pill_text='OPEN SOURCE • 100% FREE',
            mini_cards=[
                ("01", "Đọc DOM & Thị Giác", "Hybrid", False),
                ("02", "Giữ Phiên Đăng Nhập", "Session", True),
                ("03", "Chuẩn Kết Nối MCP", "Protocol", False),
                ("04", "Quét Giá & Điền Form", "Use Case", True),
                ("05", "Cài Nhanh pip install", "Setup", False),
            ],
        ),
    ))

    # 3. ai-03-github-f5-tts-style03.png
    jobs.append((
        "ai-03-github-f5-tts-style03.png",
        build_ai_style03_html(
            top_kicker="GitHub AI Trending #02 • Khung Giờ 14:00",
            badge_text="⭐ 16,000+ STARS • ZERO-SHOT VOICE AI",
            boxed_headline="Nhân Bản Giọng Nói 5 Giây",
            sub_headline="SWivid / F5-TTS",
            repo_url="github.com/SWivid/F5-TTS",
            sidebar_items=[
                ("🎙️", "Clone 5s"),
                ("⚡", "RTF 0.15"),
                ("🇻🇳", "VietTTS"),
                ("🔒", "Offline"),
            ],
            hero_card_title="Clone Giọng Truyền Cảm 0đ Đối Đầu ElevenLabs",
            hero_card_subtitle="Kiến trúc Flow Matching (DiT) chạy Offline 100% trên GPU cá nhân / Colab",
            hero_bullets=[
                "Zero-Shot Voice Cloning: Chỉ cần 3–10 giây audio mẫu sạch để bắt đúng âm sắc.",
                "Tốc độ Sway Sampling: Đạt RTF ~0.15, xuất hàng chục voice Reels trong vài phút.",
                "Multi-Style & Podcast: Ghép hội thoại nhiều nhân vật, hỗ trợ fine-tune tiếng Việt.",
            ],
            card_number="02",
            right_pill_text='0Đ CHI PHÍ • CHẠY OFFLINE',
            mini_cards=[
                ("01", "Mẫu Giọng 3-10 Giây", "Zero-Shot", False),
                ("02", "Tốc Độ Siêu Nhanh", "RTF 0.15", True),
                ("03", "Chạy Local 0 Đồng", "Free GPU", False),
                ("04", "Hỗ Trợ Tiếng Việt", "Fine-tune", True),
                ("05", "Làm Podcast 2 Người", "Multi-Voice", False),
            ],
        ),
    ))

    # 4. ai-04-github-awesome-llm-style03.png
    jobs.append((
        "ai-04-github-awesome-llm-style03.png",
        build_ai_style03_html(
            top_kicker="GitHub AI Trending #03 • Khung Giờ 18:30",
            badge_text="⭐ 30,000+ STARS • LLM APPS REPOSITORY",
            boxed_headline="Kho Ứng Dụng AI Thực Chiến",
            sub_headline="Shubhamsaboo / awesome-llm-apps",
            repo_url="github.com/Shubhamsaboo/awesome-llm-apps",
            sidebar_items=[
                ("🤖", "Agents"),
                ("👥", "Teams"),
                ("📚", "RAG PDF"),
                ("💻", "Ollama"),
            ],
            hero_card_title="Trọn Bộ Source Code AI Agent, RAG & Multi-Agent",
            hero_card_subtitle="Clone về dùng ngay với OpenAI, Claude, Gemini hoặc chạy Local miễn phí",
            hero_bullets=[
                "Starter AI Agents: Có sẵn Travel, Finance, Legal & Journalist Agent kèm Prompt.",
                "Multi-Agent Teams: Đội quân Researcher → Writer → Editor trên CrewAI & AutoGen.",
                "Advanced RAG & Local LLM: Chat với PDF/SQL chuẩn xác, chạy 0đ qua Ollama.",
            ],
            card_number="03",
            right_pill_text='CLONE NGAY • FULL TEMPLATES',
            mini_cards=[
                ("01", "Starter AI Agents", "Chuyên Biệt", False),
                ("02", "Multi-Agent Teams", "Phối Hợp", True),
                ("03", "Voice & Multimodal", "Thời Gian Thực", False),
                ("04", "Advanced RAG PDF", "Chống Bịa Tin", True),
                ("05", "Local LLM Ollama", "Miễn Phí API", False),
            ],
        ),
    ))

    # 5. ai-05-lead-hethong-style02.png
    jobs.append((
        "ai-05-lead-hethong-style02.png",
        build_ai_style02_html(
            kicker_badge="🚀 SYSTEM BLUEPRINT 20:00 • PHỄU CHỜ KHÓA HỌC",
            preview_title="Bản Vẽ Kiến Trúc Đội Quân Nhân Sự AI Tự Động Vận Hành Đa Kênh 24/7",
            preview_items=[
                ("01", "Sơ Đồ Orchestrator + Subagents", "1 người điều phối 4–5 Fanpage: Nghiên cứu → Viết bài → Thiết kế → QA."),
                ("02", "Checklist Công Cụ 0đ Tối Ưu", "Kết hợp AI Agent, MCP Server, n8n workflow & SQLite local tiết kiệm 90%."),
                ("03", "Giải Phẫu Quy Trình Tự Chạy", "Chuyển từ hỏi đáp AI lẻ tẻ sang dây chuyền sản xuất nội dung tự động."),
                ("04", "Vé Ưu Tiên Waitlist Thực Chiến", "Quyền đăng ký sớm danh sách chờ khóa học xây dựng Hệ Thống AI Agent."),
            ],
            headline_lines=["XÂY ĐỘI QUÂN", "NHÂN SỰ AI", "TỰ ĐỘNG 24/7!"],
            boxed_line_idx=1,
            pill_1_text='COMMENT "HETHONG" NHẬN BẢN VẼ',
            pill_2_text="Save for Later",
            summary_line_1="Bí quyết để 1 Solopreneur vận hành 4–5 kênh nội dung & bán hàng không cần thuê đội ngũ cồng kềnh.",
            summary_line_2='Bình luận "HETHONG" để nhận sơ đồ Flowchart + ưu tiên vào Waitlist khóa học!',
            footer_left_top="AI System Blueprint",
            footer_left_bold="Đội Quân Nhân Sự AI",
            footer_mid_top="2026",
            footer_mid_bold="October",
        ),
    ))

    # 6. sales-phongtro-1145-style02.png
    jobs.append((
        "sales-phongtro-1145-style02.png",
        build_sales_style02_html(
            page_name="PHÒNG TRỌ HẾT CỨU",
            page_sub="SMART LIVING • GỌN SẠCH PHÒNG TRỌ 15M²",
            accent_color="#445D27",
            product_title_spaced="MÁY HÚT BỤI",
            product_subtitle="MINI CẦM TAY KHÔNG DÂY ĐA ĐẦU HÚT",
            product_italic_hook="Hút gọn tóc rụng, vụn bánh tráng & bụi khe nệm chỉ trong 3 giây",
            price_tag="SHOPEE YÊU THÍCH+ • 139K – 179K (LINK Ở CMT ĐẦU)",
            hero_svg=VACUUM_HERO_SVG,
            macro_bg_svg=VACUUM_MACRO_SVG,
            macro_kicker="CẬN CẢNH CẤU TẠO & VẬT LIỆU",
            macro_lines=[
                "LÕI LỌC HEPA RỬA NƯỚC",
                "KHOANG BỤI TRONG SUỐT",
                "SẠC NHANH USB TYPE-C",
            ],
            detail_boxes=[
                (VACUUM_D1_SVG, "ĐẦU HÚT KHE 2-IN-1", "Quét & hút sạch rãnh cửa, góc nệm"),
                (VACUUM_D2_SVG, "LÕI LỌC HEPA GIẶT ĐƯỢC", "Giữ bụi mịn, tháo rửa dưới vòi 10 giây"),
                (VACUUM_D3_SVG, "CỐC BỤI 200ML & TYPE-C", "Nhìn rõ bụi bẩn, sạc chung dây ĐT"),
            ],
        ),
    ))

    # 7. sales-ktx-1145-style02.png
    jobs.append((
        "sales-ktx-1145-style02.png",
        build_sales_style02_html(
            page_name="KÝ TÚC XÁ CÓ BIẾN",
            page_sub="DORM ESSENTIALS • CỨU TINH GIƯỜNG TẦNG 2",
            accent_color="#284166",
            product_title_spaced="QUẠT KẸP GIƯỜNG",
            product_subtitle="TÍCH ĐIỆN MINI XOAY 360° PIN TYPE-C",
            product_italic_hook="Kẹp chắc thành giường tầng KTX — Gió mát êm ru không lo vướng dây",
            price_tag="SHOPEE MALL / YÊU THÍCH+ • 79K – 129K (LINK Ở CMT ĐẦU)",
            hero_svg=FAN_HERO_SVG,
            macro_bg_svg=FAN_MACRO_SVG,
            macro_kicker="CẬN CẢNH LỒNG QUẠT & ĐỘNG CƠ",
            macro_lines=[
                "LỒNG ĐAN KHÍT AN TOÀN",
                "ĐỘNG CƠ KHÔNG CHỔI THAN",
                "CHẠY ÊM GIỜ NGHỈ TRƯA",
            ],
            detail_boxes=[
                (FAN_D1_SVG, "NGÀM KẸP LÒ XO LÓT SILICON", "Kẹp cứng cáp khung sắt giường tầng"),
                (FAN_D2_SVG, "TRỤC CỔ XOAY KÉP 360°", "Chỉnh đúng hướng gió, không bay giấy"),
                (FAN_D3_SVG, "LỒNG QUẠT THÁO RỜI RỬA DỄ", "Vệ sinh cánh quạt nhanh trong 30 giây"),
            ],
        ),
    ))

    # 8. sales-deadline-1145-style02.png
    jobs.append((
        "sales-deadline-1145-style02.png",
        build_sales_style02_html(
            page_name="HỘI DEADLINE",
            page_sub="ERGONOMIC DESK SETUP • DÂN VĂN PHÒNG",
            accent_color="#1E2225",
            product_title_spaced="GIÁ ĐỠ XOAY 360°",
            product_subtitle="HỢP KIM NHÔM ANODIZED GẤP GỌN",
            product_italic_hook="Nâng màn hình ngang tầm mắt — Đỡ mỏi cổ khi cày báo cáo 8 tiếng",
            price_tag="SHOPEE MALL / YÊU THÍCH+ • 65K – 169K (LINK Ở CMT ĐẦU)",
            hero_svg=STAND_HERO_SVG,
            macro_bg_svg=STAND_MACRO_SVG,
            macro_kicker="CẬN CẢNH HỢP KIM NHÔM CNC",
            macro_lines=[
                "NHÔM ANODIZED DÀY DẶN",
                "BÁNH RĂNG CƠ KHÍ 360°",
                "ĐỆM SILICON CHỐNG TRƯỢT",
            ],
            detail_boxes=[
                (STAND_D1_SVG, "ĐẾ XOAY 360° CƠ KHÍ", "Xoay show màn hình mượt, đầm chắc"),
                (STAND_D2_SVG, "KHUNG NHÔM & ĐỆM SILICON", "Chịu tải khỏe, chống trầy xước máy"),
                (STAND_D3_SVG, "RÃNH KHOÉT TẢN NHIỆT", "Thoáng khí đáy máy khi chạy việc nặng"),
            ],
        ),
    ))

    # 9. sales-phongtro-2030-style01.png
    jobs.append((
        "sales-phongtro-2030-style01.png",
        build_sales_style01_html(
            bg_hex="#445D27",
            cream_hex="#EDEBD7",
            page_name="Phòng Trọ Hết Cứu",
            page_tagline="Bếp Trọ Gọn Gàng • Nấu Nhanh Ăn Ngon",
            product_badge="Bộ Cắt Gọt Rau Củ Đa Năng Kèm Rổ",
            benefit_lines=[
                "Thái bào siêu tốc,",
                "Sợi đều tăm tắp,",
                "Tích hợp rổ xoay &",
                "An toàn ngón tay.",
            ],
            cta_pill_text="Xem chi tiết ở bình luận đầu",
            cutout_product_svg=SLICER_CUTOUT_SVG,
            footer_left="Link Shopee chuẩn đã ghim tại Top Comment",
            footer_right="Shopee Yêu Thích+ • 85K – 125K",
        ),
    ))

    # 10. sales-ktx-2100-style01.png
    jobs.append((
        "sales-ktx-2100-style01.png",
        build_sales_style01_html(
            bg_hex="#355C57",
            cream_hex="#F4F3EA",
            page_name="Ký Túc Xá Có Biến",
            page_tagline="Giải Phóng Tủ Đồ Sinh Viên Giao Mùa",
            product_badge="Bộ Túi Nén Chân Không Kèm Bơm Tay",
            benefit_lines=[
                "Xẹp gọn tới 75%,",
                "Chống ẩm mốc mùi,",
                "Khóa Zip 2 rãnh &",
                "Nhìn xuyên dễ tìm.",
            ],
            cta_pill_text="Xem combo tại bình luận đầu",
            cutout_product_svg=VACBAG_CUTOUT_SVG,
            footer_left="Link Shopee chuẩn đã ghim tại Top Comment",
            footer_right="Combo Kèm Bơm • 45K – 89K",
        ),
    ))

    # 11. sales-deadline-2000-style01.png
    jobs.append((
        "sales-deadline-2000-style01.png",
        build_sales_style01_html(
            bg_hex="#2D3436",
            cream_hex="#EAE7DF",
            page_name="Hội Deadline",
            page_tagline="Minimalist Desk Setup • Cày Đêm Dịu Mắt",
            product_badge="Đèn Kẹp Màn Hình Chiếu Sáng Bất Đối Xứng",
            benefit_lines=[
                "Không chói màn hình,",
                "Dịu mắt cày đêm,",
                "Đổi 3 màu nắng &",
                "Giải phóng mặt bàn.",
            ],
            cta_pill_text="Xem chi tiết ở bình luận đầu",
            cutout_product_svg=LAMP_CUTOUT_SVG,
            footer_left="Link Shopee Mall đã ghim tại Top Comment",
            footer_right="Bảo Vệ Mắt • 159K – 249K",
        ),
    ))

    print(f"Rendering {len(jobs)} campaign cards (1080x1350) ...")
    for filename, html in jobs:
        out_path = OUTPUT_DIR / filename
        render_html_to_png(html, out_path, 1080, 1350)
        with Image.open(out_path) as im:
            print(f"  [OK] {filename} -> {im.size[0]}x{im.size[1]} ({out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
