#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_vid_style_card.py — Bespoke Visual Card Engine for Page "AI Players - Người chơi hệ AI"
100% Using the Visual Style DNA of c:\\Users\\guicci\\Downloads\\vid (WITHOUT Cloning MagentX Course Templates)

Visual Style DNA Preserved 100%:
1. Deep 3D Wavy Checkered Carbon Background (bg_3d_wavy_clean.png) + Ambient Neon Radial Glows.
2. 100% Offline Single-File TTF Fonts (Be Vietnam Pro, Plus Jakarta Sans, Anton, Oswald) — zero font fallback bugs.
3. Signature Color Palette:
   - Electric Acid Lime (#D4FF00 with #9BB800 / #7A9200 3D bevel lips)
   - Cyber Hot Pink (#F42F6C with #A81442 3D bevel lips)
   - Crisp Pure White (#FFFFFF) & Muted Silver (#AEB4C0)
   - Deep Matte Obsidian Cards (#111318, #161922)
4. Signature Graphic Motifs:
   - Skewed parallelogram badges (skewX(-10deg)) with 4-point star ✦
   - Thin white bracketed titles [ ... ] with dual-accent colored vowels (1 Acid Lime + 1 Hot Pink)
   - Two-color bold headlines (White + Acid Lime / White + Hot Pink)
   - 3D glossy squircle containers, 3D pointer cursors, perspective 3D neon wireframe depth (neon_tunnel_3d.png),
     and pixel corner accents.

Zero Cloned Course Elements:
- ZERO "zoom" wordmarks, ZERO "Hình thức: 2 buổi Online qua", ZERO "Thời gian: 9:00 - 16:00",
  ZERO "Khoá 1/2/3", ZERO "SOLD OUT", ZERO Higgsfield logo, ZERO ">K WHERE AI MEET CREATIVE MINDS".
- Every card features bespoke topic-specific illustrations, diagrams, and layouts tailored to AI Players content.
"""

import os
import re
import sys
import subprocess
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


# ==============================================================================
# SHARED GRAPHIC PRIMITIVES (DOWNLOADS\VID VISUAL STYLE DNA)
# ==============================================================================

def star_4pt_svg(size: int = 28, color: str = "#FFFFFF") -> str:
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0;">
      <path d="M16 0C16.8 9.8 22.2 15.2 32 16C22.2 16.8 16.8 22.2 16 32C15.2 22.2 9.8 16.8 0 16C9.8 15.2 15.2 9.8 16 0Z" fill="{color}"/>
    </svg>"""


def cursor_3d_svg(size: int = 110) -> str:
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
      <g filter="url(#cursor_shadow)">
        <path d="M22 16 C18 13, 14 16, 15 21 L23 96 C24 102, 30 104, 34 99 L52 74 L84 68 C90 67, 92 60, 87 56 L22 16 Z"
              fill="#1E1E1E" stroke="#FFFFFF" stroke-width="3.4" stroke-linejoin="round"/>
      </g>
      <defs>
        <filter id="cursor_shadow" x="0" y="0" width="120" height="120" filterUnits="userSpaceOnUse">
          <feDropShadow dx="-4" dy="8" stdDeviation="6" flood-color="#000000" flood-opacity="0.72"/>
        </filter>
      </defs>
    </svg>"""


def ai_players_chip_html(right_text: str = "NGƯỜI CHƠI HỆ AI") -> str:
    """Subtle top/bottom brand signature for Page AI Players."""
    return f"""
    <div style="display:inline-flex; align-items:center; gap:10px; background:rgba(18,20,26,0.88); border:1.5px solid rgba(212,255,0,0.45); border-radius:999px; padding:7px 18px; box-shadow:0 6px 20px rgba(0,0,0,0.5);">
      <span style="width:10px; height:10px; border-radius:50%; background:#D4FF00; box-shadow:0 0 10px #D4FF00; display:inline-block;"></span>
      <span style="font-family:'Plus Jakarta Sans','Be Vietnam Pro',sans-serif; font-weight:800; font-size:16px; color:#D4FF00; letter-spacing:1.2px;">AI PLAYERS</span>
      <span style="color:rgba(255,255,255,0.3); font-weight:400;">//</span>
      <span style="font-family:'Be Vietnam Pro',sans-serif; font-weight:700; font-size:15px; color:#FFFFFF; letter-spacing:0.5px;">{right_text}</span>
    </div>
    """


def format_foundation_bracket_title(raw_text: str) -> str:
    """
    Formats bracketed title with thin white brackets [ ... ]
    and dual colored vowels (#D4FF00 Acid Lime + #F42F6C Hot Pink).
    """
    clean = re.sub(r"<[^>]+>", "", raw_text).strip()
    clean = clean.strip("[]").strip().upper()
    if not clean:
        clean = "AI PLAYERS"

    chars = list(clean)
    n = len(chars)
    vowels = set("AEIOUĂÂÊÔƠƯY035")

    lime_idx = -1
    for i in range(min(1, n - 1), max(2, int(n * 0.48))):
        if chars[i] in vowels and chars[i] != " ":
            lime_idx = i
            break
    if lime_idx == -1 and n >= 2:
        lime_idx = 1

    pink_idx = -1
    for i in range(n - 2, max(lime_idx + 1, int(n * 0.50)) - 1, -1):
        if chars[i] in vowels and chars[i] != " ":
            pink_idx = i
            break
    if pink_idx == -1 and n >= 4:
        pink_idx = n - 2

    out = ['<span class="thin-bk">[</span><span class="bk-word">']
    for i, ch in enumerate(chars):
        if i == lime_idx:
            out.append(f'<span style="color:#D4FF00;">{ch}</span>')
        elif i == pink_idx:
            out.append(f'<span style="color:#F42F6C;">{ch}</span>')
        else:
            out.append(ch)
    out.append('</span><span class="thin-bk">]</span>')
    return "".join(out)


def split_two_color_title(title: str) -> str:
    if "<span" in title:
        return title
    if "&" in title:
        parts = title.split("&", 1)
        return f'<span style="color:#FFFFFF;">{parts[0].strip()}</span> <span style="color:#D4FF00;">&amp; {parts[1].strip()}</span>'
    words = title.split()
    if len(words) >= 4:
        mid = len(words) // 2
        p1 = " ".join(words[:mid])
        p2 = " ".join(words[mid:])
        return f'<span style="color:#FFFFFF;">{p1}</span> <span style="color:#D4FF00;">{p2}</span>'
    return f'<span style="color:#FFFFFF;">{title}</span>'


def get_base_css() -> str:
    bg_uri = (ASSETS_DIR / "bg_3d_wavy_clean.png").as_uri()
    font_css = get_local_fonts_css()
    return f"""
    {font_css}

    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      -webkit-font-smoothing: antialiased;
    }}

    body {{
      width: 1080px;
      height: 1080px;
      overflow: hidden;
      background-color: #050505;
      background-image: url('{bg_uri}');
      background-size: 1080px 1080px;
      background-repeat: no-repeat;
      font-family: 'Be Vietnam Pro', 'Plus Jakarta Sans', 'Montserrat', sans-serif;
      color: #FFFFFF;
      position: relative;
    }}

    .thin-bk {{
      font-family: 'Plus Jakarta Sans', 'Be Vietnam Pro', sans-serif;
      font-weight: 300;
      color: #FFFFFF;
      margin: 0 12px;
      display: inline-block;
      transform: scaleY(1.08);
    }}
    .bk-word {{
      font-family: 'Be Vietnam Pro', 'Plus Jakarta Sans', sans-serif;
      font-weight: 800;
      color: #FFFFFF;
      letter-spacing: -1.5px;
    }}
    .pink-skew-badge {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      background: #F42F6C;
      color: #FFFFFF;
      padding: 9px 24px;
      transform: skewX(-10deg);
      box-shadow: 0 7px 0 #9E123E, 0 12px 24px rgba(244,47,108,0.35);
      border-radius: 6px;
    }}
    .pink-skew-badge > span {{
      display: inline-block;
      transform: skewX(10deg);
      font-weight: 700;
      font-size: 27px;
      letter-spacing: -0.3px;
      white-space: nowrap;
    }}
    .lime-skew-badge {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      background: #D4FF00;
      color: #0B0D10;
      padding: 9px 24px;
      transform: skewX(-10deg);
      box-shadow: 0 7px 0 #89A600, 0 12px 24px rgba(212,255,0,0.3);
      border-radius: 6px;
    }}
    .lime-skew-badge > span {{
      display: inline-block;
      transform: skewX(10deg);
      font-weight: 800;
      font-size: 26px;
      letter-spacing: -0.3px;
      white-space: nowrap;
    }}
    """


# ==============================================================================
# BESPOKE TOPIC-SPECIFIC 3D & VECTOR ILLUSTRATIONS FOR HERO CARDS
# ==============================================================================

def get_bespoke_topic_illustration_svg(tool_key: str, model_name: str) -> str:
    """
    Returns a rich, topic-specific custom vector diagram / UI illustration
    matching the exact tool (Browser-Use, Claude Artifacts, DeepSeek, Remotion, MCP, Cursor, etc.)
    in the Downloads\\vid Acid Lime (#D4FF00) + Hot Pink (#F42F6C) + Dark Obsidian aesthetic.
    """
    key = (tool_key + " " + model_name).upper()

    if "BROWSER" in key or "STAGEHAND" in key:
        # Automated Browser DOM Inspector + AI Agent clicking elements
        return """<svg width="420" height="340" viewBox="0 0 420 340" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="14" width="392" height="312" rx="22" fill="#0E1117" stroke="#D4FF00" stroke-width="3.5"/>
          <rect x="14" y="14" width="392" height="46" rx="20" fill="#191E28"/>
          <circle cx="42" cy="37" r="8" fill="#F42F6C"/>
          <circle cx="66" cy="37" r="8" fill="#D4FF00"/>
          <circle cx="90" cy="37" r="8" fill="#3A4252"/>
          <rect x="116" y="25" width="268" height="24" rx="12" fill="#0B0D12" stroke="rgba(255,255,255,0.15)"/>
          <text x="132" y="42" font-family="monospace" font-size="13" fill="#D4FF00">agent://auto-dom-selector</text>
          <!-- DOM Elements being auto-clicked -->
          <rect x="36" y="80" width="214" height="58" rx="12" fill="#161B24" stroke="#D4FF00" stroke-width="2" stroke-dasharray="6 4"/>
          <text x="48" y="105" font-family="sans-serif" font-weight="800" font-size="13.5" fill="#D4FF00">[DOM #1] AUTO-FILL FORM</text>
          <text x="48" y="126" font-family="monospace" font-size="12.5" fill="#AEB4C0">status: clicked (12ms)</text>
          <rect x="264" y="80" width="120" height="58" rx="12" fill="#F42F6C"/>
          <text x="324" y="115" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="17" fill="#FFFFFF">SUBMIT ✦</text>
          <!-- Extracted JSON Table -->
          <rect x="36" y="156" width="348" height="146" rx="14" fill="#131820" stroke="rgba(255,255,255,0.16)" stroke-width="1.5"/>
          <text x="54" y="184" font-family="monospace" font-weight="700" font-size="14" fill="#F42F6C">// EXTRACTED DATA PAYLOAD</text>
          <text x="54" y="212" font-family="monospace" font-size="14" fill="#FFFFFF">{ "flight": "VN214", "price": "1.250K",</text>
          <text x="54" y="238" font-family="monospace" font-size="14" fill="#D4FF00">  "action": "BOOKED_SUCCESS",</text>
          <text x="54" y="264" font-family="monospace" font-size="14" fill="#FFFFFF">  "stars": "55,000+ GitHub" }</text>
        </svg>"""

    if "AWESOME" in key or "LANGCHAIN" in key:
        # Modular RAG & Multi-App Treasure Vault Stack
        return """<svg width="420" height="340" viewBox="0 0 420 340" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="16" y="16" width="388" height="308" rx="24" fill="#0E1118" stroke="#D4FF00" stroke-width="3"/>
          <!-- 3 Layered App Modules -->
          <rect x="40" y="38" width="340" height="72" rx="14" fill="#181D27" stroke="#D4FF00" stroke-width="2.5"/>
          <rect x="56" y="54" width="40" height="40" rx="10" fill="#D4FF00"/>
          <text x="68" y="81" font-family="sans-serif" font-weight="900" font-size="20" fill="#0B0D10">01</text>
          <text x="112" y="70" font-family="sans-serif" font-weight="800" font-size="18" fill="#FFFFFF">RAG PDF &amp; DOCS AGENT</text>
          <text x="112" y="93" font-family="monospace" font-size="13" fill="#D4FF00">VectorDB + Hybrid Search</text>

          <rect x="40" y="128" width="340" height="72" rx="14" fill="#181D27" stroke="#F42F6C" stroke-width="2.5"/>
          <rect x="56" y="144" width="40" height="40" rx="10" fill="#F42F6C"/>
          <text x="67" y="171" font-family="sans-serif" font-weight="900" font-size="20" fill="#FFFFFF">02</text>
          <text x="112" y="160" font-family="sans-serif" font-weight="800" font-size="18" fill="#FFFFFF">FINANCE &amp; STOCK ANALYST</text>
          <text x="112" y="183" font-family="monospace" font-size="13" fill="#F42F6C">Real-time Chart + News API</text>

          <rect x="40" y="218" width="340" height="76" rx="14" fill="#D4FF00"/>
          <rect x="56" y="236" width="40" height="40" rx="10" fill="#0E1118"/>
          <text x="67" y="263" font-family="sans-serif" font-weight="900" font-size="20" fill="#D4FF00">★</text>
          <text x="112" y="252" font-family="sans-serif" font-weight="900" font-size="20" fill="#0B0D10">100+ FULL LLM TEMPLATES</text>
          <text x="112" y="276" font-family="sans-serif" font-weight="800" font-size="14" fill="#1E2400">30,000+ GITHUB STARS • READY TO CLONE</text>
        </svg>"""

    if "ARTIFACT" in key or "SONNET" in key:
        # Split Prompt-to-Live-UI React Preview
        return """<svg width="420" height="340" viewBox="0 0 420 340" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="14" width="392" height="312" rx="22" fill="#0E1117" stroke="#D4FF00" stroke-width="3"/>
          <!-- Left pane: Chat/Code -->
          <rect x="30" y="34" width="166" height="272" rx="14" fill="#151922" stroke="rgba(255,255,255,0.14)"/>
          <text x="44" y="62" font-family="monospace" font-weight="700" font-size="13" fill="#F42F6C">&lt;Prompt&gt;</text>
          <rect x="44" y="76" width="136" height="10" rx="5" fill="#FFFFFF" opacity="0.8"/>
          <rect x="44" y="96" width="110" height="10" rx="5" fill="#FFFFFF" opacity="0.5"/>
          <text x="44" y="136" font-family="monospace" font-weight="700" font-size="13" fill="#D4FF00">&lt;ReactUI/&gt;</text>
          <rect x="44" y="150" width="138" height="72" rx="8" fill="#0B0D12" stroke="#D4FF00" stroke-width="1.5"/>
          <text x="54" y="174" font-family="monospace" font-size="12" fill="#D4FF00">export default</text>
          <text x="54" y="194" font-family="monospace" font-size="12" fill="#FFFFFF">function App()</text>
          <rect x="44" y="244" width="138" height="42" rx="10" fill="#F42F6C"/>
          <text x="113" y="270" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="13.5" fill="#FFFFFF">RENDER 30S ⚡</text>
          <!-- Right pane: Live Dashboard Preview -->
          <rect x="210" y="34" width="180" height="272" rx="14" fill="#181E29" stroke="#D4FF00" stroke-width="2.5"/>
          <rect x="226" y="52" width="148" height="28" rx="6" fill="#D4FF00"/>
          <text x="300" y="71" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="12" fill="#0B0D10">LIVE WEB PREVIEW</text>
          <!-- Bar chart inside live app -->
          <rect x="234" y="160" width="22" height="60" rx="4" fill="#F42F6C"/>
          <rect x="266" y="130" width="22" height="90" rx="4" fill="#D4FF00"/>
          <rect x="298" y="110" width="22" height="110" rx="4" fill="#D4FF00"/>
          <rect x="330" y="92" width="22" height="128" rx="4" fill="#FFFFFF"/>
          <rect x="226" y="238" width="148" height="48" rx="10" fill="#0E1117"/>
          <text x="300" y="268" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="14.5" fill="#D4FF00">+320% SPEED</text>
        </svg>"""

    if "DEEPSEEK" in key:
        # MoE Router + Coding Benchmark Chart
        return """<svg width="420" height="340" viewBox="0 0 420 340" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="14" width="392" height="312" rx="22" fill="#0E1117" stroke="#D4FF00" stroke-width="3"/>
          <text x="36" y="52" font-family="sans-serif" font-weight="900" font-size="18" fill="#D4FF00">MIXTURE OF EXPERTS (MoE) ROUTER</text>
          <!-- MoE Nodes -->
          <rect x="36" y="72" width="102" height="54" rx="12" fill="#181D27" stroke="#D4FF00" stroke-width="2"/>
          <text x="50" y="105" font-family="sans-serif" font-weight="800" font-size="14" fill="#FFFFFF">EXPERT #1</text>
          <rect x="158" y="72" width="102" height="54" rx="12" fill="#D4FF00"/>
          <text x="172" y="105" font-family="sans-serif" font-weight="900" font-size="14" fill="#0B0D10">CODE CORE</text>
          <rect x="280" y="72" width="102" height="54" rx="12" fill="#181D27" stroke="#F42F6C" stroke-width="2"/>
          <text x="294" y="105" font-family="sans-serif" font-weight="800" font-size="14" fill="#FFFFFF">MATH LOGIC</text>
          <!-- Benchmark comparison bars -->
          <text x="36" y="164" font-family="monospace" font-weight="700" font-size="14" fill="#AEB4C0">SWE-BENCH VERIFIED SCORE</text>
          <rect x="36" y="180" width="346" height="44" rx="10" fill="#161B24"/>
          <rect x="36" y="180" width="328" height="44" rx="10" fill="#D4FF00"/>
          <text x="52" y="208" font-family="sans-serif" font-weight="900" font-size="16" fill="#0B0D10">DEEPSEEK V3 / CODER — 94.8%</text>

          <rect x="36" y="238" width="346" height="44" rx="10" fill="#161B24"/>
          <rect x="36" y="238" width="240" height="44" rx="10" fill="#F42F6C"/>
          <text x="52" y="266" font-family="sans-serif" font-weight="800" font-size="15" fill="#FFFFFF">API COST: GIẢM 92% TOKEN FEE</text>
        </svg>"""

    if "REMOTION" in key or "FFMPEG" in key:
        # React Video Timeline + 9:16 Vertical Reel Frame
        return """<svg width="420" height="340" viewBox="0 0 420 340" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="14" width="392" height="312" rx="22" fill="#0E1117" stroke="#D4FF00" stroke-width="3"/>
          <!-- Left: 9:16 Phone Reel Frame -->
          <rect x="34" y="34" width="142" height="242" rx="18" fill="#161B24" stroke="#D4FF00" stroke-width="3"/>
          <rect x="46" y="56" width="118" height="26" rx="6" fill="#D4FF00"/>
          <text x="105" y="73" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="11" fill="#0B0D10">9:16 REEL 60FPS</text>
          <circle cx="105" cy="145" r="28" fill="#F42F6C"/>
          <polygon points="99,133 99,157 119,145" fill="#FFFFFF"/>
          <rect x="48" y="210" width="114" height="44" rx="8" fill="#0B0D12" stroke="rgba(255,255,255,0.2)"/>
          <text x="105" y="237" text-anchor="middle" font-family="monospace" font-weight="700" font-size="12" fill="#D4FF00">&lt;Sequence/&gt;</text>
          <!-- Right: Multi-track Timeline & Code -->
          <rect x="196" y="36" width="190" height="118" rx="14" fill="#151922" stroke="rgba(255,255,255,0.15)"/>
          <text x="212" y="64" font-family="monospace" font-size="13" fill="#D4FF00">useCurrentFrame()</text>
          <text x="212" y="90" font-family="monospace" font-size="13" fill="#FFFFFF">spring({ fps: 30 })</text>
          <text x="212" y="116" font-family="monospace" font-size="13" fill="#F42F6C">npx remotion render</text>
          <!-- Timeline tracks -->
          <rect x="196" y="172" width="190" height="28" rx="6" fill="#D4FF00"/>
          <text x="291" y="191" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="12.5" fill="#0B0D10">TRACK 1: MOTION UI</text>
          <rect x="196" y="210" width="190" height="28" rx="6" fill="#F42F6C"/>
          <text x="291" y="229" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="12.5" fill="#FFFFFF">TRACK 2: VOICE -3dB</text>
          <rect x="196" y="248" width="190" height="28" rx="6" fill="#232A38" stroke="#D4FF00" stroke-width="1.5"/>
          <text x="291" y="267" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="12.5" fill="#D4FF00">TRACK 3: SFX &amp; BGM</text>
        </svg>"""

    if "MCP" in key or "CONTEXT" in key:
        # MCP Central Hub connecting to 4 External Tools
        return """<svg width="420" height="340" viewBox="0 0 420 340" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="14" width="392" height="312" rx="22" fill="#0E1117" stroke="#D4FF00" stroke-width="3"/>
          <!-- Connecting lines -->
          <line x1="210" y1="170" x2="96" y2="77" stroke="#D4FF00" stroke-width="4"/>
          <line x1="210" y1="170" x2="324" y2="77" stroke="#D4FF00" stroke-width="4"/>
          <line x1="210" y1="170" x2="96" y2="263" stroke="#F42F6C" stroke-width="4"/>
          <line x1="210" y1="170" x2="324" y2="263" stroke="#F42F6C" stroke-width="4"/>
          <!-- 4 Outer Server Nodes -->
          <rect x="32" y="46" width="128" height="62" rx="14" fill="#171C26" stroke="#D4FF00" stroke-width="2.5"/>
          <text x="96" y="83" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="14.5" fill="#FFFFFF">SQLITE DB</text>
          <rect x="260" y="46" width="128" height="62" rx="14" fill="#171C26" stroke="#D4FF00" stroke-width="2.5"/>
          <text x="324" y="83" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="14.5" fill="#FFFFFF">BROWSER</text>
          <rect x="32" y="232" width="128" height="62" rx="14" fill="#171C26" stroke="#F42F6C" stroke-width="2.5"/>
          <text x="96" y="269" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="14" fill="#FFFFFF">FILESYSTEM</text>
          <rect x="260" y="232" width="128" height="62" rx="14" fill="#171C26" stroke="#F42F6C" stroke-width="2.5"/>
          <text x="324" y="269" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="14.5" fill="#FFFFFF">META API</text>
          <!-- Center MCP Hub -->
          <rect x="132" y="126" width="156" height="88" rx="22" fill="#D4FF00" stroke="#0B0D10" stroke-width="4"/>
          <text x="210" y="166" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="22" fill="#0B0D10">MCP HUB</text>
          <text x="210" y="191" text-anchor="middle" font-family="monospace" font-weight="800" font-size="13" fill="#1F2600">JSON-RPC 2.0</text>
        </svg>"""

    if "CURSOR" in key or "WINDSURF" in key:
        # Multi-file Agentic Code Diff Editor
        return """<svg width="420" height="340" viewBox="0 0 420 340" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="14" width="392" height="312" rx="22" fill="#0E1117" stroke="#D4FF00" stroke-width="3"/>
          <!-- File tabs -->
          <rect x="32" y="32" width="110" height="34" rx="8" fill="#D4FF00"/>
          <text x="87" y="54" text-anchor="middle" font-family="monospace" font-weight="800" font-size="13" fill="#0B0D10">agent.ts ✓</text>
          <rect x="150" y="32" width="110" height="34" rx="8" fill="#1B202B" stroke="#F42F6C" stroke-width="2"/>
          <text x="205" y="54" text-anchor="middle" font-family="monospace" font-weight="700" font-size="13" fill="#FFFFFF">router.py ✓</text>
          <rect x="268" y="32" width="118" height="34" rx="8" fill="#1B202B"/>
          <text x="327" y="54" text-anchor="middle" font-family="monospace" font-size="12" fill="#D4FF00">.cursorrules</text>
          <!-- Diff code block -->
          <rect x="32" y="80" width="354" height="156" rx="14" fill="#131720" stroke="rgba(255,255,255,0.14)"/>
          <rect x="44" y="98" width="330" height="28" rx="6" fill="rgba(244,47,108,0.22)"/>
          <text x="56" y="117" font-family="monospace" font-size="13.5" fill="#F42F6C">- const manualCode = slowLoop();</text>
          <rect x="44" y="136" width="330" height="28" rx="6" fill="rgba(212,255,0,0.20)"/>
          <text x="56" y="155" font-family="monospace" font-weight="700" font-size="13.5" fill="#D4FF00">+ await agent.applyMultiFileDiff();</text>
          <rect x="44" y="174" width="330" height="28" rx="6" fill="rgba(212,255,0,0.20)"/>
          <text x="56" y="193" font-family="monospace" font-weight="700" font-size="13.5" fill="#D4FF00">+ verifyAllTestsPass({ strict: true });</text>
          <!-- Bottom status -->
          <rect x="32" y="252" width="354" height="50" rx="12" fill="#F42F6C"/>
          <text x="209" y="283" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="15" fill="#FFFFFF">⚡ COMPOSER: 12 FILES UPDATED IN 4S</text>
        </svg>"""

    if "HALLUCINATION" in key or "GROUNDED" in key:
        # 3-Layer Anti-Hallucination Shield & Gate
        return """<svg width="420" height="340" viewBox="0 0 420 340" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="14" width="392" height="312" rx="22" fill="#0E1117" stroke="#D4FF00" stroke-width="3"/>
          <!-- 3 Verification Gates -->
          <rect x="38" y="42" width="344" height="68" rx="14" fill="#171C26" stroke="#D4FF00" stroke-width="2.5"/>
          <text x="58" y="74" font-family="sans-serif" font-weight="900" font-size="17" fill="#D4FF00">GATE 01 // RAG GROUNDING LOCK</text>
          <text x="58" y="96" font-family="monospace" font-size="13" fill="#FFFFFF">100% trích xuất từ tài liệu gốc</text>

          <rect x="38" y="128" width="344" height="68" rx="14" fill="#171C26" stroke="#F42F6C" stroke-width="2.5"/>
          <text x="58" y="160" font-family="sans-serif" font-weight="900" font-size="17" fill="#F42F6C">GATE 02 // JSON SCHEMA ENFORCER</text>
          <text x="58" y="182" font-family="monospace" font-size="13" fill="#FFFFFF">Chặn đứng văn bản tự bịa ngoài khung</text>

          <rect x="38" y="214" width="344" height="78" rx="14" fill="#D4FF00"/>
          <text x="58" y="250" font-family="sans-serif" font-weight="900" font-size="20" fill="#0B0D10">GATE 03 // LINTER VERIFIED ✓</text>
          <text x="58" y="276" font-family="sans-serif" font-weight="800" font-size="14" fill="#1E2400">HALLUCINATION RATE: 0.00% GUARANTEED</text>
        </svg>"""

    if "COMPUTER" in key or "GUI" in key:
        # Autonomous Desktop GUI Coordinate & Cursor Control
        return """<svg width="420" height="340" viewBox="0 0 420 340" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="14" width="392" height="312" rx="22" fill="#0E1117" stroke="#D4FF00" stroke-width="3"/>
          <!-- Screen grid overlay -->
          <line x1="14" y1="110" x2="406" y2="110" stroke="rgba(212,255,0,0.2)" stroke-dasharray="6 6"/>
          <line x1="14" y1="210" x2="406" y2="210" stroke="rgba(212,255,0,0.2)" stroke-dasharray="6 6"/>
          <line x1="150" y1="14" x2="150" y2="326" stroke="rgba(212,255,0,0.2)" stroke-dasharray="6 6"/>
          <line x1="290" y1="14" x2="290" y2="326" stroke="rgba(212,255,0,0.2)" stroke-dasharray="6 6"/>
          <!-- Simulated App Window -->
          <rect x="40" y="42" width="220" height="140" rx="14" fill="#171C26" stroke="#FFFFFF" stroke-width="2"/>
          <text x="150" y="80" text-anchor="middle" font-family="monospace" font-weight="700" font-size="13.5" fill="#D4FF00">VISION_COORD: (290, 210)</text>
          <rect x="70" y="102" width="160" height="46" rx="10" fill="#F42F6C"/>
          <text x="150" y="131" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="15.5" fill="#FFFFFF">AUTO CLICK ✦</text>
          <!-- Trajectory path -->
          <path d="M90 270 Q 190 260 285 212" stroke="#D4FF00" stroke-width="4" stroke-dasharray="8 6" fill="none"/>
          <circle cx="290" cy="210" r="24" stroke="#D4FF00" stroke-width="4"/>
          <circle cx="290" cy="210" r="8" fill="#F42F6C"/>
          <rect x="40" y="246" width="340" height="54" rx="12" fill="#D4FF00"/>
          <text x="210" y="280" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="15" fill="#0B0D10">AI NHÌN MÀN HÌNH • DI CHUỘT • GÕ PHÍM</text>
        </svg>"""

    if "SECOND" in key or "BRAIN" in key or "VAULT" in key:
        # Second Brain Markdown Knowledge Graph
        return """<svg width="420" height="340" viewBox="0 0 420 340" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="14" width="392" height="312" rx="22" fill="#0E1117" stroke="#D4FF00" stroke-width="3"/>
          <line x1="210" y1="150" x2="96" y2="71" stroke="#D4FF00" stroke-width="3.5"/>
          <line x1="210" y1="150" x2="324" y2="71" stroke="#D4FF00" stroke-width="3.5"/>
          <line x1="210" y1="150" x2="110" y2="261" stroke="#F42F6C" stroke-width="3.5"/>
          <line x1="210" y1="150" x2="310" y2="261" stroke="#F42F6C" stroke-width="3.5"/>
          <rect x="132" y="108" width="156" height="84" rx="20" fill="#D4FF00"/>
          <text x="210" y="148" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="20" fill="#0B0D10">INDEX.MD</text>
          <text x="210" y="172" text-anchor="middle" font-family="monospace" font-weight="800" font-size="13" fill="#1F2600">SECOND BRAIN</text>

          <rect x="34" y="44" width="124" height="54" rx="12" fill="#181D27" stroke="#D4FF00" stroke-width="2"/>
          <text x="96" y="77" text-anchor="middle" font-family="monospace" font-weight="700" font-size="14" fill="#FFFFFF">MEM-01.md</text>
          <rect x="262" y="44" width="124" height="54" rx="12" fill="#181D27" stroke="#D4FF00" stroke-width="2"/>
          <text x="324" y="77" text-anchor="middle" font-family="monospace" font-weight="700" font-size="14" fill="#FFFFFF">MEM-02.md</text>
          <rect x="44" y="232" width="132" height="58" rx="12" fill="#F42F6C"/>
          <text x="110" y="267" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="14.5" fill="#FFFFFF">ZERO REPEAT</text>
          <rect x="244" y="232" width="132" height="58" rx="12" fill="#181D27" stroke="#F42F6C" stroke-width="2"/>
          <text x="310" y="267" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="14.5" fill="#D4FF00">AUTO-LEARN</text>
        </svg>"""

    if "FAST" in key or "PYTHON" in key:
        # FastHTML Pure Python to Web UI
        return """<svg width="420" height="340" viewBox="0 0 420 340" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="14" width="392" height="312" rx="22" fill="#0E1117" stroke="#D4FF00" stroke-width="3"/>
          <rect x="34" y="38" width="352" height="122" rx="14" fill="#151A24" stroke="#D4FF00" stroke-width="2"/>
          <text x="52" y="68" font-family="monospace" font-weight="700" font-size="14" fill="#D4FF00">from fasthtml.common import *</text>
          <text x="52" y="98" font-family="monospace" font-size="14" fill="#FFFFFF">app, rt = fast_app()</text>
          <text x="52" y="128" font-family="monospace" font-size="14" fill="#F42F6C">@rt("/") def get(): return Div("AI UI")</text>
          <!-- Arrow down -->
          <rect x="175" y="172" width="70" height="30" rx="8" fill="#D4FF00"/>
          <text x="210" y="193" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="15" fill="#0B0D10">HTMX</text>
          <!-- Rendered Web UI -->
          <rect x="34" y="214" width="352" height="86" rx="14" fill="#D4FF00"/>
          <text x="210" y="252" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="19" fill="#0B0D10">100% PURE PYTHON WEB APP</text>
          <text x="210" y="278" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="13.5" fill="#1F2600">KHÔNG CẦN NODE.JS • KHÔNG CẦN REACT</text>
        </svg>"""

    if "TELEGRAM" in key or "BOT" in key:
        # Mobile Telegram Bot Command Center
        return """<svg width="420" height="340" viewBox="0 0 420 340" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="14" width="392" height="312" rx="22" fill="#0E1117" stroke="#D4FF00" stroke-width="3"/>
          <!-- Chat bubbles -->
          <rect x="118" y="38" width="268" height="54" rx="16" fill="#F42F6C"/>
          <text x="252" y="71" text-anchor="middle" font-family="monospace" font-weight="800" font-size="15" fill="#FFFFFF">/deploy_campaign_today ⚡</text>

          <rect x="36" y="110" width="348" height="114" rx="16" fill="#171C26" stroke="#D4FF00" stroke-width="2.5"/>
          <text x="54" y="140" font-family="sans-serif" font-weight="900" font-size="14.5" fill="#D4FF00">🤖 MAMA BOT // BÁO CÁO TỨC THÌ:</text>
          <text x="54" y="168" font-family="sans-serif" font-weight="700" font-size="13.5" fill="#FFFFFF">✓ Đã render 6 ảnh + 3 Reels chuẩn</text>
          <text x="54" y="196" font-family="sans-serif" font-weight="700" font-size="13.5" fill="#D4FF00">✓ Đã ghim link phễu tự động 100%</text>

          <rect x="36" y="242" width="166" height="52" rx="12" fill="#D4FF00"/>
          <text x="119" y="274" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="14.5" fill="#0B0D10">[ DUYỆT ĐĂNG ✓ ]</text>
          <rect x="218" y="242" width="166" height="52" rx="12" fill="#171C26" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
          <text x="301" y="274" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="14.5" fill="#FFFFFF">[ XEM LOG 📊 ]</text>
        </svg>"""

    # Default Multi-Agent Swarm Network (for MULTI AGENTS / LANGGRAPH / CREWAI)
    return """<svg width="420" height="340" viewBox="0 0 420 340" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="14" y="14" width="392" height="312" rx="22" fill="#0E1117" stroke="#D4FF00" stroke-width="3"/>
      <!-- Swarm Triangle + Center Supervisor -->
      <line x1="210" y1="68" x2="104" y2="246" stroke="#D4FF00" stroke-width="3.5"/>
      <line x1="210" y1="68" x2="316" y2="246" stroke="#D4FF00" stroke-width="3.5"/>
      <line x1="104" y1="246" x2="316" y2="246" stroke="#F42F6C" stroke-width="3.5"/>
      <rect x="132" y="34" width="156" height="64" rx="16" fill="#D4FF00"/>
      <text x="210" y="73" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="18" fill="#0B0D10">SUPERVISOR</text>

      <rect x="32" y="216" width="144" height="68" rx="14" fill="#171C26" stroke="#D4FF00" stroke-width="2.5"/>
      <text x="104" y="256" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="14.5" fill="#FFFFFF">RESEARCHER</text>

      <rect x="244" y="216" width="144" height="68" rx="14" fill="#171C26" stroke="#F42F6C" stroke-width="2.5"/>
      <text x="316" y="256" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="14.5" fill="#FFFFFF">CODER AGENT</text>

      <circle cx="210" cy="166" r="34" fill="#F42F6C"/>
      <text x="210" y="172" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="14.5" fill="#FFFFFF">STATE</text>
    </svg>"""


# ==============================================================================
# ARCHETYPE 1: BESPOKE HERO TECH & MODEL SHOWCASE (3 VARIED COMPOSITIONS)
# ==============================================================================

def render_template_hero_showcase(
    top_badge: str,
    tool_title_line1: str,
    tool_title_line2: str,
    bottom_badge: str,
    model_name: str,
    output_path: Path,
    icon_variant: int = 0,
) -> None:
    tunnel_uri = (ASSETS_DIR / "neon_tunnel_3d.png").as_uri()
    topic_svg = get_bespoke_topic_illustration_svg(f"{tool_title_line1} {tool_title_line2}", model_name)

    m_clean = model_name.strip().upper()
    m_len = len(m_clean)
    if m_len <= 11:
        m_font_size = 132
        m_scale_x = 0.96
    elif m_len <= 15:
        m_font_size = 114
        m_scale_x = 0.90
    else:
        m_font_size = 96
        m_scale_x = 0.86

    max_t_len = max(len(tool_title_line1.strip()), len(tool_title_line2.strip()))
    if max_t_len <= 6:
        t_font_size = 82
    elif max_t_len <= 8:
        t_font_size = 66
    elif max_t_len <= 10:
        t_font_size = 54
    else:
        t_font_size = 44

    # Alternate left/right card placement based on icon_variant so cards aren't identical clones
    flip_horizontal = (icon_variant % 2 == 1)
    flex_dir = "row-reverse" if flip_horizontal else "row"

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  {get_base_css()}

  .top-bar {{
    position: absolute;
    top: 38px;
    left: 62px;
    right: 62px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 20;
  }}

  .hero-bento-row {{
    position: absolute;
    top: 120px;
    left: 62px;
    width: 956px;
    height: 410px;
    display: flex;
    flex-direction: {flex_dir};
    align-items: stretch;
    justify-content: space-between;
    gap: 28px;
    z-index: 15;
  }}

  .lime-title-card {{
    flex: 1;
    background: linear-gradient(155deg, #DEFF1A 0%, #C8F400 100%);
    border-radius: 34px;
    padding: 36px 38px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 16px 0 #7C9600, 0 28px 50px rgba(0,0,0,0.75);
    position: relative;
    overflow: hidden;
  }}

  .lime-card-tag {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #101216;
    color: #D4FF00;
    font-weight: 800;
    font-size: 16px;
    padding: 8px 16px;
    border-radius: 999px;
    width: fit-content;
    letter-spacing: 0.8px;
  }}

  .tool-display-text {{
    font-family: 'Be Vietnam Pro', 'Plus Jakarta Sans', sans-serif;
    font-weight: 900;
    font-size: {t_font_size}px;
    line-height: 1.02;
    color: #0B0D10;
    letter-spacing: -2.2px;
    text-transform: uppercase;
    word-break: keep-all;
  }}

  .lime-card-footer {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-top: 2px solid rgba(11,13,16,0.18);
    padding-top: 16px;
    font-weight: 800;
    font-size: 17px;
    color: #161A04;
  }}

  .visual-diagram-box {{
    width: 440px;
    height: 410px;
    background: linear-gradient(180deg, #151922 0%, #0B0D12 100%);
    border-radius: 34px;
    border: 3px solid rgba(212,255,0,0.55);
    box-shadow: 0 16px 0 #1E2430, 0 28px 55px rgba(0,0,0,0.85);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 12px;
  }}

  .floating-cursor {{
    position: absolute;
    bottom: -26px;
    right: 24px;
    z-index: 30;
  }}

  /* Bottom 3D Perspective Neon Grid Deck */
  .bottom-tunnel-deck {{
    position: absolute;
    left: 62px;
    top: 576px;
    width: 956px;
    height: 444px;
    border-radius: 36px;
    border: 3.5px solid #D4FF00;
    background-color: #060809;
    background-image: url('{tunnel_uri}');
    background-size: 100% 100%;
    background-position: center;
    box-shadow: 0 18px 55px rgba(0,0,0,0.9), 0 0 38px rgba(212,255,0,0.22);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 10;
  }}

  .bottom-badge-wrap {{
    position: absolute;
    top: 548px;
    left: 104px;
    z-index: 25;
  }}

  .model-giant-title {{
    font-family: 'Anton', 'Oswald', sans-serif;
    font-weight: 400;
    font-size: {m_font_size}px;
    line-height: 0.95;
    color: #FFFFFF;
    text-transform: uppercase;
    letter-spacing: 2px;
    transform: scaleX({m_scale_x}) scaleY(1.18);
    text-shadow: 0 14px 36px rgba(0,0,0,0.92), 0 0 28px rgba(212,255,0,0.3);
    text-align: center;
    padding: 0 32px;
    z-index: 15;
    white-space: nowrap;
  }}

  .deck-sub-pill {{
    margin-top: 34px;
    display: inline-flex;
    align-items: center;
    gap: 12px;
    background: rgba(14,17,23,0.92);
    border: 2px solid #D4FF00;
    border-radius: 999px;
    padding: 10px 28px;
    font-weight: 800;
    font-size: 20px;
    color: #D4FF00;
    z-index: 15;
    box-shadow: 0 10px 24px rgba(0,0,0,0.75);
  }}
</style>
</head>
<body>
  <div class="top-bar">
    <div class="pink-skew-badge">
      <span>{top_badge} {star_4pt_svg(24, '#FFFFFF')}</span>
    </div>
    {ai_players_chip_html("TECH RADAR 2026")}
  </div>

  <div class="hero-bento-row">
    <div class="lime-title-card">
      <div class="lime-card-tag">✦ CÔNG CỤ ĐỘT PHÁ</div>
      <div class="tool-display-text">
        <div>{tool_title_line1}</div>
        <div>{tool_title_line2}</div>
      </div>
      <div class="lime-card-footer">
        <span>KIẾN TRÚC THỰC CHIẾN</span>
        <span>100% VERIFIED ↗</span>
      </div>
    </div>

    <div class="visual-diagram-box">
      {topic_svg}
      <div class="floating-cursor">
        {cursor_3d_svg(102)}
      </div>
    </div>
  </div>

  <div class="bottom-badge-wrap">
    <div class="pink-skew-badge">
      <span>{bottom_badge} {star_4pt_svg(24, '#FFFFFF')}</span>
    </div>
  </div>

  <div class="bottom-tunnel-deck">
    <div class="model-giant-title">{m_clean}</div>
    <div class="deck-sub-pill">
      <span>⚡ HỆ SINH THÁI AI PLAYERS</span>
      <span style="color:#FFFFFF;">•</span>
      <span style="color:#FFFFFF;">NHẬN TÀI LIỆU Ở BÌNH LUẬN ĐẦU TIÊN</span>
    </div>
  </div>
</body>
</html>"""
    render_html_to_image(html, output_path)


# ==============================================================================
# ARCHETYPE 2: 4-POINT BREAKDOWN / BENCHMARK / POLL (2 DISTINCT VISUAL LAYOUTS)
# ==============================================================================

def _highlight_pink_keyword(desc: str, pink_kw: str) -> str:
    if not pink_kw or pink_kw not in desc:
        return desc
    return desc.replace(
        pink_kw,
        f'<span style="color:#F42F6C; font-weight:800;">{pink_kw}</span>',
        1,
    )


def render_template_curriculum_breakdown(
    left_badge: str,
    right_badge: str,
    items: list,
    output_path: Path,
) -> None:
    """
    Automatically selects between 3 bespoke layouts:
    - Layout 2A (2x2 Connected Bento Step Grid) when right_badge has 'bước' or 'chỉ số'
    - Layout 2C (Interactive Community Poll Deck with 3D Option Keycaps) when 'khảo sát', 'tác vụ', 'rào cản', 'thói quen', 'trọng tâm'
    - Layout 2B (Full-Bleed 4-Row Neon Spec Matrix) for Comparisons & Benchmarks
    """
    rb_lower = (left_badge + " " + right_badge).lower()
    use_poll_deck = any(k in rb_lower for k in ["khảo sát", "tác vụ", "rào cản", "thói quen", "trọng tâm", "mục tiêu"])
    use_bento_2x2 = (not use_poll_deck) and any(k in rb_lower for k in ["bước", "chỉ số", "quy tắc"])

    if use_poll_deck:
        poll_letters = ["A", "B", "C", "D"]
        poll_pcts = [88, 74, 82, 92]
        rows_html = []
        for idx, it in enumerate(items[:4]):
            letter = poll_letters[idx]
            num = it.get("num", f"0{idx+1}")
            title_html = split_two_color_title(it.get("title", ""))
            desc_html = _highlight_pink_keyword(it.get("desc", ""), it.get("pink_kw", ""))
            pct = poll_pcts[idx]
            keycap_bg = "#D4FF00" if idx % 2 == 0 else "#F42F6C"
            keycap_fg = "#0B0D10" if idx % 2 == 0 else "#FFFFFF"
            keycap_lip = "#7D9600" if idx % 2 == 0 else "#96103A"
            rows_html.append(f"""
            <div class="poll-option-card">
              <div class="poll-keycap" style="background:{keycap_bg}; color:{keycap_fg}; box-shadow:0 8px 0 {keycap_lip};">
                <span class="key-letter">{letter}</span>
                <span class="key-sub">#{num}</span>
              </div>
              <div class="poll-body">
                <div class="poll-title-row">
                  <div class="poll-title">{title_html}</div>
                  <div class="poll-vote-tag">VOTE {letter} ✦</div>
                </div>
                <div class="poll-desc">{desc_html}</div>
                <div class="poll-bar-bg">
                  <div class="poll-bar-fill" style="width:{pct}%; background:{keycap_bg};"></div>
                </div>
              </div>
            </div>
            """)

        html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  {get_base_css()}

  .header-zone {{
    position: absolute;
    top: 40px;
    left: 60px;
    right: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .badge-pair {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .poll-stack {{
    position: absolute;
    top: 134px;
    left: 60px;
    width: 960px;
    height: 794px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 18px;
  }}

  .poll-option-card {{
    flex: 1;
    background: linear-gradient(165deg, rgba(22,26,36,0.96) 0%, rgba(12,15,20,0.98) 100%);
    border: 2.5px solid rgba(212,255,0,0.45);
    border-radius: 26px;
    padding: 20px 28px;
    display: flex;
    align-items: center;
    gap: 26px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.75);
  }}

  .poll-keycap {{
    width: 94px;
    height: 112px;
    border-radius: 22px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}

  .key-letter {{
    font-family: 'Anton', sans-serif;
    font-size: 52px;
    line-height: 1;
  }}

  .key-sub {{
    font-weight: 900;
    font-size: 15px;
    margin-top: 4px;
    opacity: 0.85;
  }}

  .poll-body {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .poll-title-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .poll-title {{
    font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 900;
    font-size: 30px;
    line-height: 1.15;
    letter-spacing: -0.6px;
    text-transform: uppercase;
  }}

  .poll-vote-tag {{
    background: rgba(255,255,255,0.08);
    border: 1.5px solid rgba(212,255,0,0.5);
    color: #D4FF00;
    font-weight: 800;
    font-size: 14px;
    padding: 4px 14px;
    border-radius: 999px;
    white-space: nowrap;
  }}

  .poll-desc {{
    font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 500;
    font-size: 22px;
    line-height: 1.32;
    color: #DCE0EC;
  }}

  .poll-bar-bg {{
    width: 100%;
    height: 10px;
    background: #0A0C10;
    border-radius: 999px;
    overflow: hidden;
    margin-top: 4px;
  }}

  .poll-bar-fill {{
    height: 100%;
    border-radius: 999px;
  }}

  .poll-footer {{
    position: absolute;
    bottom: 34px;
    left: 60px;
    right: 60px;
    height: 72px;
    background: #D4FF00;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    box-shadow: 0 8px 0 #7C9600, 0 16px 32px rgba(0,0,0,0.8);
  }}
</style>
</head>
<body>
  <div class="header-zone">
    <div class="badge-pair">
      <div class="pink-skew-badge"><span>{left_badge}</span></div>
      <div class="lime-skew-badge"><span>{right_badge} {star_4pt_svg(24, '#0B0D10')}</span></div>
    </div>
    {ai_players_chip_html("COMMUNITY POLL")}
  </div>

  <div class="poll-stack">
    {"".join(rows_html)}
  </div>

  <div class="poll-footer">
    <span style="font-weight:900; font-size:21px; color:#0B0D10; white-space:nowrap;">🗳️ BẠN CHỌN PHƯƠNG ÁN NÀO TRONG 4 LỰA CHỌN TRÊN?</span>
    <span style="background:#0B0D10; color:#D4FF00; font-weight:900; font-size:18px; padding:8px 20px; border-radius:12px; white-space:nowrap;">BÌNH LUẬN NGAY 👇</span>
  </div>
</body>
</html>"""
        render_html_to_image(html, output_path)
        return

    if use_bento_2x2:
        cards_html = []
        for idx, it in enumerate(items[:4]):
            num = it.get("num", f"0{idx+1}")
            title_html = split_two_color_title(it.get("title", ""))
            desc_html = _highlight_pink_keyword(it.get("desc", ""), it.get("pink_kw", ""))
            accent_border = "#D4FF00" if idx % 2 == 0 else "#F42F6C"
            badge_bg = "#D4FF00" if idx % 2 == 0 else "#F42F6C"
            badge_fg = "#0B0D10" if idx % 2 == 0 else "#FFFFFF"
            cards_html.append(f"""
            <div class="bento-step-card" style="border-color:{accent_border};">
              <div class="step-top">
                <div class="step-num-pill" style="background:{badge_bg}; color:{badge_fg};">STEP {num}</div>
                <div class="step-dots">✦ AI PLAYERS</div>
              </div>
              <div class="step-title">{title_html}</div>
              <div class="step-desc">{desc_html}</div>
            </div>
            """)

        html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  {get_base_css()}

  .header-zone {{
    position: absolute;
    top: 44px;
    left: 60px;
    right: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .badge-pair {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .grid-2x2 {{
    position: absolute;
    top: 146px;
    left: 60px;
    width: 960px;
    height: 780px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 28px;
  }}

  .bento-step-card {{
    background: linear-gradient(165deg, rgba(22,26,35,0.95) 0%, rgba(12,14,19,0.98) 100%);
    border: 3px solid #D4FF00;
    border-radius: 30px;
    padding: 34px 34px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 14px 0 rgba(0,0,0,0.65), 0 22px 44px rgba(0,0,0,0.8);
    position: relative;
  }}

  .step-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .step-num-pill {{
    font-family: 'Anton', sans-serif;
    font-size: 32px;
    padding: 6px 22px;
    border-radius: 14px;
    letter-spacing: 1px;
  }}

  .step-dots {{
    font-weight: 800;
    font-size: 15px;
    color: rgba(255,255,255,0.45);
    letter-spacing: 1px;
  }}

  .step-title {{
    font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 900;
    font-size: 33px;
    line-height: 1.18;
    letter-spacing: -0.8px;
    text-transform: uppercase;
    margin: 12px 0 8px 0;
  }}

  .step-desc {{
    font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 500;
    font-size: 24px;
    line-height: 1.42;
    color: #D8DCE6;
  }}

  .footer-bar {{
    position: absolute;
    bottom: 38px;
    left: 60px;
    right: 60px;
    height: 76px;
    background: #12151C;
    border: 2.5px solid #D4FF00;
    border-radius: 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.8);
  }}
</style>
</head>
<body>
  <div class="header-zone">
    <div class="badge-pair">
      <div class="pink-skew-badge"><span>{left_badge}</span></div>
      <div class="lime-skew-badge"><span>{right_badge} {star_4pt_svg(24, '#0B0D10')}</span></div>
    </div>
    {ai_players_chip_html("PLAYBOOK 2026")}
  </div>

  <div class="grid-2x2">
    {"".join(cards_html)}
  </div>

  <div class="footer-bar">
    <span style="font-weight:800; font-size:19px; color:#FFFFFF; white-space:nowrap;">⚡ ÁP DỤNG NGAY CHO HỆ THỐNG TỰ ĐỘNG HÓA CỦA BẠN</span>
    <span style="font-weight:900; font-size:19px; color:#D4FF00; white-space:nowrap;">XEM BÌNH LUẬN ĐẦU TIÊN 👇</span>
  </div>
</body>
</html>"""
        render_html_to_image(html, output_path)
        return

    # Layout 2B: Edge-to-Edge 4-Row Neon Spec Matrix (refined with AI Players header & 3D number pills)
    rows_html = []
    for idx, it in enumerate(items[:4]):
        num = it.get("num", f"0{idx+1}")
        title_html = split_two_color_title(it.get("title", ""))
        desc_html = _highlight_pink_keyword(it.get("desc", ""), it.get("pink_kw", ""))
        rows_html.append(f"""
        <div class="spec-row">
          <div class="num-col">
            <div class="num-box">{num}</div>
          </div>
          <div class="content-col">
            <div class="row-title">{title_html}</div>
            <div class="row-desc">{desc_html}</div>
          </div>
        </div>
        """)

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  {get_base_css()}

  .top-header {{
    position: absolute;
    top: 42px;
    left: 62px;
    right: 62px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .badge-group {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .matrix-container {{
    position: absolute;
    top: 138px;
    left: 0;
    width: 1080px;
    height: 880px;
    display: flex;
    flex-direction: column;
    border-top: 3px solid #D4FF00;
  }}

  .spec-row {{
    flex: 1;
    display: flex;
    align-items: center;
    border-bottom: 3px solid #D4FF00;
    background: rgba(10, 12, 16, 0.58);
    padding: 0 56px;
  }}

  .num-col {{
    width: 170px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    border-right: 3px solid rgba(212,255,0,0.45);
    height: 100%;
    padding-right: 24px;
  }}

  .num-box {{
    font-family: 'Plus Jakarta Sans', 'Be Vietnam Pro', sans-serif;
    font-weight: 800;
    font-size: 86px;
    color: #D4FF00;
    letter-spacing: -3px;
    line-height: 1;
    text-shadow: 0 8px 24px rgba(212,255,0,0.28);
  }}

  .content-col {{
    flex: 1;
    padding-left: 42px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 10px;
  }}

  .row-title {{
    font-family: 'Be Vietnam Pro', 'Plus Jakarta Sans', sans-serif;
    font-weight: 900;
    font-size: 35px;
    line-height: 1.12;
    letter-spacing: -0.8px;
    text-transform: uppercase;
  }}

  .row-desc {{
    font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 500;
    font-size: 27px;
    line-height: 1.36;
    color: #E2E6F0;
  }}
</style>
</head>
<body>
  <div class="top-header">
    <div class="badge-group">
      <div class="pink-skew-badge"><span>{left_badge}</span></div>
      <div class="lime-skew-badge"><span>{right_badge} {star_4pt_svg(24, '#0B0D10')}</span></div>
    </div>
    {ai_players_chip_html("DEEP BENCHMARK")}
  </div>

  <div class="matrix-container">
    {"".join(rows_html)}
  </div>
</body>
</html>"""
    render_html_to_image(html, output_path)


# ==============================================================================
# ARCHETYPE 3: SYSTEM ARCHITECTURE & HUB BLUEPRINT (ZERO ZOOM WORDMARKS!)
# ==============================================================================

def _module_icon_svg(icon_type: str, num_or_icon: str = "4") -> str:
    if icon_type == "key":
        return """<svg width="56" height="56" viewBox="0 0 56 56" fill="none">
          <rect width="56" height="56" rx="16" fill="#D4FF00"/>
          <path d="M18 28V22C18 16.5 22.5 12 28 12C33.5 12 38 16.5 38 22V28" stroke="#0B0D10" stroke-width="4.5" stroke-linecap="round"/>
          <rect x="14" y="26" width="28" height="20" rx="6" fill="#0B0D10"/>
          <circle cx="28" cy="36" r="3.5" fill="#D4FF00"/>
        </svg>"""
    if icon_type == "book":
        return """<svg width="56" height="56" viewBox="0 0 56 56" fill="none">
          <rect width="56" height="56" rx="16" fill="#F42F6C"/>
          <path d="M15 16H26C28 16 28 18 28 20V40C28 38 26 37 24 37H15V16Z" fill="#FFFFFF"/>
          <path d="M41 16H30C28 16 28 18 28 20V40C28 38 30 37 32 37H41V16Z" fill="#D4FF00"/>
        </svg>"""
    if icon_type == "flow":
        return """<svg width="56" height="56" viewBox="0 0 56 56" fill="none">
          <rect width="56" height="56" rx="16" fill="#D4FF00"/>
          <circle cx="18" cy="18" r="6" fill="#0B0D10"/>
          <circle cx="38" cy="18" r="6" fill="#F42F6C"/>
          <circle cx="28" cy="38" r="6" fill="#0B0D10"/>
          <path d="M23 20L33 20M20 23L26 34M36 23L30 34" stroke="#0B0D10" stroke-width="3.5"/>
        </svg>"""
    return f"""<svg width="56" height="56" viewBox="0 0 56 56" fill="none">
      <rect width="56" height="56" rx="16" fill="#F42F6C"/>
      <text x="28" y="39" text-anchor="middle" font-family="'Anton',sans-serif" font-size="32" fill="#FFFFFF">{num_or_icon}</text>
    </svg>"""


def render_template_feature_matrix(
    level_badge: str,
    bracket_title_colored: str,
    meta_info_left: str,
    meta_info_right: str,
    cards_2x2: list,
    footer_title_white: str,
    footer_title_pink: str,
    output_path: Path,
) -> None:
    """
    True 3D System Architecture Blueprint Card (Zero Zoom Wordmark!).
    Features bracketed dual-accent headline + Telemetry Spec Bar + 4 Connected 3D Module Nodes
    around a central AI Core Hub + High-Impact Two-Tone Footer.
    """
    formatted_bracket = format_foundation_bracket_title(bracket_title_colored)

    nodes_html = []
    for idx, c in enumerate(cards_2x2[:4]):
        icon_svg = _module_icon_svg(c.get("icon", "flow"), str(c.get("num_or_icon", idx + 1)))
        title = c.get("title", "")
        sub = c.get("subtitle", "")
        border_col = "#D4FF00" if idx in (0, 3) else "rgba(255,255,255,0.28)"
        nodes_html.append(f"""
        <div class="arch-node-card" style="border-color:{border_col};">
          {icon_svg}
          <div class="arch-node-text">
            <div class="arch-node-tag">MODULE 0{idx+1}</div>
            <div class="arch-node-title">{title}</div>
            <div class="arch-node-sub">{sub}</div>
          </div>
        </div>
        """)

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  {get_base_css()}

  .top-row {{
    position: absolute;
    top: 42px;
    left: 62px;
    right: 62px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .bracket-hero {{
    position: absolute;
    top: 122px;
    left: 40px;
    right: 40px;
    text-align: center;
    font-size: 92px;
    line-height: 1.05;
    white-space: nowrap;
  }}

  /* Clean Tech Telemetry Spec Pill (Replaces the old cloned Zoom bar) */
  .telemetry-bar {{
    position: absolute;
    top: 256px;
    left: 90px;
    width: 900px;
    height: 68px;
    background: rgba(18, 22, 30, 0.94);
    border: 2.5px solid #D4FF00;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 18px;
    padding: 0 32px;
    box-shadow: 0 12px 32px rgba(0,0,0,0.75);
  }}

  /* 4 Architecture Module Cards + Central Hub Connector */
  .arch-diagram-wrap {{
    position: absolute;
    top: 356px;
    left: 68px;
    width: 944px;
    height: 430px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 28px 36px;
    z-index: 10;
  }}

  .arch-node-card {{
    background: linear-gradient(160deg, #171B24 0%, #0E1016 100%);
    border: 3px solid #D4FF00;
    border-radius: 28px;
    padding: 24px 28px;
    display: flex;
    align-items: center;
    gap: 22px;
    box-shadow: 0 14px 0 #08090C, 0 22px 40px rgba(0,0,0,0.85);
  }}

  .arch-node-text {{
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .arch-node-tag {{
    font-family: 'Plus Jakarta Sans', monospace;
    font-weight: 800;
    font-size: 13px;
    color: #D4FF00;
    letter-spacing: 1.4px;
  }}

  .arch-node-title {{
    font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 900;
    font-size: 29px;
    color: #FFFFFF;
    letter-spacing: -0.6px;
    line-height: 1.15;
  }}

  .arch-node-sub {{
    font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 500;
    font-size: 21px;
    color: #B8C0D0;
    line-height: 1.25;
  }}

  .center-core-hub {{
    position: absolute;
    top: 525px;
    left: 494px;
    width: 92px;
    height: 92px;
    border-radius: 26px;
    background: #D4FF00;
    border: 5px solid #0B0D10;
    box-shadow: 0 0 36px rgba(212,255,0,0.65), 0 12px 28px rgba(0,0,0,0.9);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 25;
    transform: rotate(45deg);
  }}

  .center-core-hub span {{
    transform: rotate(-45deg);
    font-family: 'Anton', sans-serif;
    font-size: 24px;
    color: #0B0D10;
    letter-spacing: 0.5px;
  }}

  /* Footer Banner */
  .footer-stack {{
    position: absolute;
    bottom: 42px;
    left: 62px;
    right: 62px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
  }}

  .footer-white-line {{
    font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 900;
    font-size: 46px;
    color: #FFFFFF;
    letter-spacing: -1px;
    text-transform: uppercase;
    text-shadow: 0 8px 24px rgba(0,0,0,0.85);
  }}

  .footer-pink-bar {{
    background: #F42F6C;
    padding: 8px 34px;
    border-radius: 10px;
    transform: skewX(-10deg);
    box-shadow: 0 8px 0 #98113B, 0 14px 30px rgba(244,47,108,0.4);
  }}

  .footer-pink-bar span {{
    display: inline-block;
    transform: skewX(10deg);
    font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 900;
    font-size: 42px;
    color: #FFFFFF;
    letter-spacing: -0.8px;
    text-transform: uppercase;
  }}
</style>
</head>
<body>
  <div class="top-row">
    <div class="pink-skew-badge">
      <span>{level_badge} {star_4pt_svg(24, '#FFFFFF')}</span>
    </div>
    {ai_players_chip_html("SYSTEM BLUEPRINT")}
  </div>

  <div class="bracket-hero">
    {formatted_bracket}
  </div>

  <div class="telemetry-bar">
    <span style="font-weight:800; font-size:22px; color:#D4FF00;">⚡ {meta_info_left}:</span>
    <span style="font-weight:800; font-size:23px; color:#FFFFFF;">{meta_info_right}</span>
  </div>

  <div class="arch-diagram-wrap">
    {"".join(nodes_html)}
  </div>

  <div class="center-core-hub">
    <span>CORE</span>
  </div>

  <div class="footer-stack">
    <div class="footer-white-line">{footer_title_white}</div>
    <div class="footer-pink-bar"><span>{footer_title_pink}</span></div>
  </div>
</body>
</html>"""
    render_html_to_image(html, output_path)


# ==============================================================================
# ARCHETYPE 4: 3D PLAYBOOK & LEAD MAGNET VAULT CARD (ZERO ZOOM / ZERO COURSE DATES!)
# ==============================================================================

def render_template_offer_card(
    header_badge: str,
    bracket_title_colored: str,
    selector_badge: str,
    date_cards: list,
    time_badge: str,
    delivery_text: str,
    cta_button_text: str,
    output_path: Path,
) -> None:
    """
    Renders a Bespoke 3D Digital Playbook & Template Vault Drop Card in Downloads\\vid aesthetic.
    Completely eliminates MagentX's Zoom Course Registration elements.
    """
    formatted_bracket = format_foundation_bracket_title(bracket_title_colored)

    spec_boxes_html = []
    for idx, dc in enumerate(date_cards[:3]):
        lbl = dc.get("label", f"Thông số {idx+1}")
        val = dc.get("date", "")
        is_hl = dc.get("highlight", idx > 0)
        border_col = "#D4FF00" if is_hl else "rgba(255,255,255,0.25)"
        val_col = "#D4FF00" if is_hl else "#FFFFFF"
        spec_boxes_html.append(f"""
        <div class="vault-spec-box" style="border-color:{border_col};">
          <div class="vault-spec-label">✦ {lbl.upper()}</div>
          <div class="vault-spec-val" style="color:{val_col};">{val}</div>
        </div>
        """)

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  {get_base_css()}

  .vault-card {{
    position: absolute;
    top: 58px;
    left: 64px;
    width: 952px;
    height: 964px;
    background: linear-gradient(180deg, #151821 0%, #0D0F14 100%);
    border-radius: 38px;
    border: 3px solid rgba(212,255,0,0.65);
    box-shadow: 0 24px 70px rgba(0,0,0,0.92);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}

  .vault-top-lime-bar {{
    width: 100%;
    height: 74px;
    background: #D4FF00;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 38px;
    border-bottom: 5px solid #86A300;
  }}

  .vault-top-lime-bar .left-tag {{
    font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 900;
    font-size: 25px;
    color: #0B0D10;
    text-transform: uppercase;
    letter-spacing: -0.4px;
  }}

  .vault-top-lime-bar .right-tag {{
    background: #0B0D10;
    color: #D4FF00;
    font-weight: 800;
    font-size: 16px;
    padding: 7px 18px;
    border-radius: 999px;
    letter-spacing: 1px;
  }}

  .vault-bracket-title {{
    margin-top: 34px;
    font-size: 76px;
    line-height: 1.05;
    text-align: center;
    white-space: nowrap;
  }}

  .vault-sub-badge {{
    margin-top: 22px;
  }}

  /* 3 Spec Metric Boxes */
  .vault-specs-row {{
    margin-top: 34px;
    width: 868px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 22px;
  }}

  .vault-spec-box {{
    background: #1A1F2B;
    border: 3px solid #D4FF00;
    border-radius: 24px;
    padding: 24px 24px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    box-shadow: 0 12px 0 #090B0E;
  }}

  .vault-spec-label {{
    font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 700;
    font-size: 18px;
    color: #AEB6C8;
    letter-spacing: 0.5px;
  }}

  .vault-spec-val {{
    font-family: 'Be Vietnam Pro', 'Plus Jakarta Sans', sans-serif;
    font-weight: 900;
    font-size: 36px;
    line-height: 1.1;
    letter-spacing: -1px;
  }}

  /* Visual Resource Preview Strip (Replaces Course Time & Zoom Logo!) */
  .resource-preview-deck {{
    margin-top: 34px;
    width: 868px;
    height: 188px;
    background: #0F1218;
    border: 2.5px dashed rgba(212,255,0,0.55);
    border-radius: 26px;
    padding: 22px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 28px;
  }}

  .resource-icon-3d {{
    width: 132px;
    height: 132px;
    border-radius: 28px;
    background: linear-gradient(145deg, #D4FF00 0%, #9BB800 100%);
    box-shadow: 0 10px 0 #5E7000;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}

  .resource-info-col {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}

  .cta-button-3d {{
    margin-top: 36px;
    background: #D4FF00;
    color: #0B0D10;
    font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 900;
    font-size: 40px;
    padding: 20px 68px;
    border-radius: 999px;
    box-shadow: 0 12px 0 #7C9600, 0 22px 45px rgba(212,255,0,0.35);
    position: relative;
    text-transform: uppercase;
    letter-spacing: -0.8px;
  }}

  .cta-cursor {{
    position: absolute;
    right: -42px;
    bottom: -34px;
  }}
</style>
</head>
<body>
  <div class="vault-card">
    <div class="vault-top-lime-bar">
      <span class="left-tag">✦ {header_badge}</span>
      <span class="right-tag">AI PLAYERS VAULT // FREE DROP</span>
    </div>

    <div class="vault-bracket-title">
      {formatted_bracket}
    </div>

    <div class="vault-sub-badge">
      <div class="pink-skew-badge">
        <span>{selector_badge} {star_4pt_svg(24, '#FFFFFF')}</span>
      </div>
    </div>

    <div class="vault-specs-row">
      {"".join(spec_boxes_html)}
    </div>

    <div class="resource-preview-deck">
      <div class="resource-icon-3d">
        <span style="font-family:'Anton',sans-serif; font-size:44px; color:#0B0D10; line-height:1;">100%</span>
        <span style="font-weight:900; font-size:16px; color:#0B0D10; margin-top:4px;">MIỄN PHÍ</span>
      </div>
      <div class="resource-info-col">
        <div style="display:inline-flex; align-items:center; gap:10px;">
          <span style="background:#F42F6C; color:#FFFFFF; font-weight:800; font-size:16px; padding:5px 14px; border-radius:8px;">CỔNG TẢI TÀI LIỆU</span>
          <span style="font-weight:700; font-size:20px; color:#D4FF00;">{time_badge}</span>
        </div>
        <div style="font-weight:800; font-size:28px; color:#FFFFFF; line-height:1.25;">
          {delivery_text} <span style="color:#D4FF00;">Google Drive &amp; GitHub</span>
        </div>
        <div style="font-weight:500; font-size:19px; color:#AEB6C8;">
          Định dạng chuẩn Markdown / PDF / JSON — Sẵn sàng Copy &amp; Chạy ngay
        </div>
      </div>
    </div>

    <div class="cta-button-3d">
      <span>{cta_button_text}</span>
      <div class="cta-cursor">{cursor_3d_svg(96)}</div>
    </div>
  </div>
</body>
</html>"""
    render_html_to_image(html, output_path)


# ==============================================================================
# ARCHETYPE 5: EXECUTIVE AI OPERATIONS TELEMETRY DASHBOARD (ZERO "SOLD OUT"!)
# ==============================================================================

def render_template_urgency_slots(
    top_badge: str,
    sold_out_text: str,
    slots: list,
    cta_badge: str,
    footer_tag: str,
    offer_big_left: str,
    offer_mid_top: str,
    offer_mid_sub: str,
    output_path: Path,
) -> None:
    tunnel_uri = (ASSETS_DIR / "neon_tunnel_3d.png").as_uri()

    tracks_html = []
    for sl in slots[:2]:
        t_title = sl.get("title", "")
        t_badge = sl.get("badge", "")
        pct = int(sl.get("percent", 100))
        tracks_html.append(f"""
        <div class="telemetry-track-card">
          <div class="track-header">
            <span class="track-title">{t_title}</span>
            <span class="track-pink-pill">{t_badge} {star_4pt_svg(20, '#FFFFFF')}</span>
          </div>
          <div class="progress-rail">
            <div class="progress-fill" style="width:{pct}%;"></div>
            <div class="progress-thumb" style="left:calc({pct}% - 14px);"></div>
          </div>
        </div>
        """)

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  {get_base_css()}

  .top-header {{
    position: absolute;
    top: 40px;
    left: 62px;
    right: 62px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .giant-ops-title {{
    position: absolute;
    top: 108px;
    left: 62px;
    right: 62px;
    text-align: center;
    font-family: 'Anton', 'Oswald', sans-serif;
    font-size: 126px;
    color: #D4FF00;
    letter-spacing: 3px;
    line-height: 0.96;
    text-transform: uppercase;
    text-shadow: 0 14px 35px rgba(0,0,0,0.9);
  }}

  .tracks-stack {{
    position: absolute;
    top: 266px;
    left: 68px;
    width: 944px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }}

  .telemetry-track-card {{
    background: rgba(18, 22, 30, 0.94);
    border: 2.5px solid rgba(212,255,0,0.55);
    border-radius: 26px;
    padding: 24px 34px;
    display: flex;
    flex-direction: column;
    gap: 18px;
    box-shadow: 0 14px 32px rgba(0,0,0,0.75);
  }}

  .track-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .track-title {{
    font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 900;
    font-size: 32px;
    color: #FFFFFF;
  }}

  .track-pink-pill {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #F42F6C;
    color: #FFFFFF;
    font-weight: 800;
    font-size: 22px;
    padding: 6px 20px;
    border-radius: 10px;
  }}

  .progress-rail {{
    width: 100%;
    height: 30px;
    background: #0B0D12;
    border-radius: 999px;
    position: relative;
    border: 2px solid rgba(255,255,255,0.18);
  }}

  .progress-fill {{
    height: 100%;
    background: linear-gradient(90deg, #9BB800 0%, #D4FF00 100%);
    border-radius: 999px;
    box-shadow: 0 0 20px rgba(212,255,0,0.55);
  }}

  .progress-thumb {{
    position: absolute;
    top: -9px;
    width: 16px;
    height: 44px;
    background: #FFFFFF;
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.8);
  }}

  .telemetry-deck-footer {{
    position: absolute;
    bottom: 42px;
    left: 68px;
    width: 944px;
    height: 368px;
    border-radius: 34px;
    border: 3.5px solid #D4FF00;
    background-image: url('{tunnel_uri}');
    background-size: 100% 100%;
    background-position: center;
    box-shadow: 0 18px 50px rgba(0,0,0,0.9), 0 0 36px rgba(212,255,0,0.22);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 22px;
  }}

  .kpi-readout {{
    display: flex;
    align-items: center;
    gap: 28px;
    background: rgba(11,13,18,0.94);
    border: 3px solid #D4FF00;
    border-radius: 28px;
    padding: 22px 48px;
    box-shadow: 0 16px 40px rgba(0,0,0,0.92);
  }}
</style>
</head>
<body>
  <div class="top-header">
    <div class="pink-skew-badge"><span>{top_badge} {star_4pt_svg(24, '#FFFFFF')}</span></div>
    {ai_players_chip_html("OPS TELEMETRY")}
  </div>

  <div class="giant-ops-title">{sold_out_text}</div>

  <div class="tracks-stack">
    {"".join(tracks_html)}
  </div>

  <div class="telemetry-deck-footer">
    <div class="pink-skew-badge">
      <span>{cta_badge} {star_4pt_svg(22, '#FFFFFF')}</span>
    </div>
    <div class="kpi-readout">
      <span style="font-family:'Anton',sans-serif; font-size:84px; color:#D4FF00; line-height:1;">{offer_big_left}</span>
      <div style="display:flex; flex-direction:column; gap:4px;">
        <span style="font-weight:900; font-size:34px; color:#FFFFFF;">{offer_mid_top}</span>
        <span style="font-weight:800; font-size:22px; color:#F42F6C;">{offer_mid_sub} — {footer_tag}</span>
      </div>
    </div>
  </div>
</body>
</html>"""
    render_html_to_image(html, output_path)
