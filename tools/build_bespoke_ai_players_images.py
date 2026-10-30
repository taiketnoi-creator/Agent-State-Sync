#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_bespoke_ai_players_images.py — Động cơ Kết xuất Ảnh Bài Đăng Độc Bản 100% (Zero-Clone Bespoke Image Engine)
cho Fanpage "AI Players - Người chơi hệ AI" (1022527194267367).

TUÂN THỦ TUYỆT ĐỐI MỆNH LỆNH CỦA CEO (2026-10-30):
- XÓA BỎ VĨNH VIỄN việc "luân phiên 5 Master Templates" khiến các bài ảnh nhìn na ná nhau.
- MỖI BÀI ẢNH (1080x1080) LÀ 1 THIẾT KẾ ĐỘC BẢN 100%:
  + Không có 2 bài nào dùng chung hàm bố cục HTML/CSS.
  + Không có 2 bài nào có cùng vị trí đặt hộp màu, cùng kiểu lưới hay cùng bảng màu chủ đạo liên tiếp.
  + Tự động kiểm định qua `verify_zero_clone_images()` (quét lưới 8x8 = 64 phân vùng không gian) và xuất `bespoke_12_images_qa_grid.jpg` trước khi đăng/lên lịch lên Meta Graph API.
"""

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SUBAGENT_DIR / "tools"))

from render_vid_style_card import get_local_fonts_css, render_html_to_image
from zero_repost_gate import verify_zero_clone_images, record_published_content

VAULT_DIR = SUBAGENT_DIR / "campaigns" / "2026-10-26" / "ai-players-weekly-vault"
IMAGES_DIR = VAULT_DIR / "images"
QA_GRID_PATH = VAULT_DIR / "bespoke_12_images_qa_grid.jpg"
MANIFEST_PATH = VAULT_DIR / "bespoke_12_images_manifest.json"
PAGES_VAULT_PATH = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / "pages_vault.json"
AI_PAGE_ID = "1022527194267367"
VN_TZ = dt.timezone(dt.timedelta(hours=7))
ZALO_URL = "https://zalo.me/g/etllok798"


def _common_reset_css(bg_css: str) -> str:
    font_css = get_local_fonts_css()
    return f"""
    {font_css}
    * {{ margin: 0; padding: 0; box-sizing: border-box; -webkit-font-smoothing: antialiased; }}
    body {{
      width: 1080px;
      height: 1080px;
      overflow: hidden;
      font-family: 'Be Vietnam Pro', 'Plus Jakarta Sans', sans-serif;
      color: #FFFFFF;
      position: relative;
      {bg_css}
    }}
    """


# ==============================================================================
# 12 HÀM THIẾT KẾ ĐỘC BẢN 100% (1 BÀI = 1 KIẾN TRÚC BỐ CỤC + 1 HỆ MÀU RIÊNG)
# ==============================================================================

def card_01_computer_use_os_window() -> str:
    """Card 01: Desktop OS Window + Cyan Crosshair HUD (Theme: Electric Cyan #00F0FF & Deep Sapphire #040B16)"""
    bg = """
    background: radial-gradient(circle at 75% 45%, rgba(0, 240, 255, 0.22) 0%, rgba(4, 11, 22, 0) 58%),
                linear-gradient(145deg, #030812 0%, #071426 55%, #040911 100%);
    """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    {_common_reset_css(bg)}
    .grid-lines {{
      position:absolute; inset:0;
      background-image: linear-gradient(rgba(0,240,255,0.06) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(0,240,255,0.06) 1px, transparent 1px);
      background-size: 54px 54px;
    }}
    </style></head><body>
    <div class="grid-lines"></div>
    <!-- Top Left Header -->
    <div style="position:absolute; top:46px; left:58px; right:58px; display:flex; justify-content:space-between; align-items:flex-start;">
      <div>
        <div style="display:inline-flex; align-items:center; gap:10px; background:rgba(0,240,255,0.14); border:2px solid #00F0FF; padding:8px 20px; border-radius:8px; color:#00F0FF; font-weight:800; font-size:20px; letter-spacing:1px;">
          <span>🎯 ANTHROPIC COMPUTER USE API</span>
        </div>
        <div style="margin-top:14px; font-weight:900; font-size:46px; line-height:1.12; letter-spacing:-1px; color:#FFFFFF;">
          KHI AI BIẾT <span style="color:#00F0FF; text-shadow:0 0 28px rgba(0,240,255,0.55);">CẦM CHUỘT</span><br>
          &amp; GÕ PHÍM NHƯ NGƯỜI THẬT
        </div>
      </div>
      <div style="background:#0B192E; border:2px solid rgba(0,240,255,0.45); border-radius:16px; padding:14px 22px; text-align:right; flex-shrink:0;">
        <div style="font-size:14px; color:#7DD3FC; font-weight:700;">AI PLAYERS // GUI AGENT</div>
        <div style="font-size:28px; color:#00F0FF; font-weight:900; margin-top:4px;">1080p VISION</div>
      </div>
    </div>

    <!-- Center Giant macOS/Windows Desktop App Window -->
    <div style="position:absolute; top:236px; left:58px; right:58px; height:596px; background:#091322; border:3px solid #00F0FF; border-radius:24px; box-shadow:0 28px 70px rgba(0,0,0,0.9), 0 0 40px rgba(0,240,255,0.2); overflow:hidden;">
      <!-- Window Titlebar -->
      <div style="height:52px; background:#0F213A; border-bottom:2px solid rgba(0,240,255,0.3); display:flex; align-items:center; padding:0 22px; justify-content:space-between;">
        <div style="display:flex; gap:10px;">
          <span style="width:16px; height:16px; border-radius:50%; background:#FF5F56;"></span>
          <span style="width:16px; height:16px; border-radius:50%; background:#FFBD2E;"></span>
          <span style="width:16px; height:16px; border-radius:50%; background:#27C93F;"></span>
        </div>
        <div style="font-family:monospace; font-size:18px; color:#BAE6FD; font-weight:700;">erp-accounting-portal.internal/invoices/new</div>
        <div style="background:#00F0FF; color:#030812; font-weight:900; font-size:14px; padding:4px 12px; border-radius:6px;">LIVE CONTROL</div>
      </div>

      <!-- Inside Window Content -->
      <div style="padding:28px 32px; display:grid; grid-template-columns: 1.15fr 1fr; gap:28px; height:544px;">
        <div style="display:flex; flex-direction:column; justify-content:space-between;">
          <div style="background:#0D1D33; border:1.5px solid #1E3A5F; border-radius:14px; padding:14px 20px;">
            <div style="font-size:15px; color:#7DD3FC; font-weight:700;">MÃ HÓA ĐƠN TỰ ĐỘNG ĐIỀN</div>
            <div style="font-size:26px; color:#FFFFFF; font-weight:800; margin-top:4px; font-family:monospace;">INV-2026-88492 ✓</div>
          </div>
          <div style="background:#0D1D33; border:1.5px solid #1E3A5F; border-radius:14px; padding:14px 20px;">
            <div style="font-size:15px; color:#7DD3FC; font-weight:700;">SỐ TIỀN ĐỐI SOÁT</div>
            <div style="font-size:26px; color:#38BDF8; font-weight:800; margin-top:4px; font-family:monospace;">42,500,000 VNĐ ✓</div>
          </div>
          <div style="background:#020617; border:2.5px solid #38BDF8; border-radius:16px; padding:16px 20px;">
            <div style="font-family:monospace; font-size:16px; color:#38BDF8; font-weight:800;">&gt; AGENT_ACTION_LOG:</div>
            <div style="font-family:monospace; font-size:18px; color:#E2E8F0; margin-top:8px; line-height:1.45;">
              1. Screenshot() -&gt; OK<br>
              2. MoveMouse(742, 518)<br>
              3. LeftClick() -&gt; <span style="color:#00F0FF; font-weight:800;">DONE!</span>
            </div>
          </div>
          <div style="background:linear-gradient(90deg, #00F0FF 0%, #0284C7 100%); border-radius:16px; padding:18px; text-align:center; color:#020617; font-weight:900; font-size:24px; box-shadow:0 0 30px rgba(0,240,255,0.6);">
            XUẤT BÁO CÁO &amp; GỬI EMAIL
          </div>
        </div>

        <!-- Right Radar Crosshair Lock -->
        <div style="background:#060E1A; border:2px dashed rgba(0,240,255,0.45); border-radius:18px; position:relative; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:20px;">
          <svg width="240" height="240" viewBox="0 0 220 220">
            <circle cx="110" cy="110" r="88" stroke="#00F0FF" stroke-width="2.5" stroke-dasharray="10 6" fill="rgba(0,240,255,0.06)"/>
            <circle cx="110" cy="110" r="52" stroke="#38BDF8" stroke-width="2" fill="rgba(0,240,255,0.12)"/>
            <circle cx="110" cy="110" r="10" fill="#00F0FF"/>
            <line x1="110" y1="6" x2="110" y2="214" stroke="#00F0FF" stroke-width="2.5"/>
            <line x1="6" y1="110" x2="214" y2="110" stroke="#00F0FF" stroke-width="2.5"/>
          </svg>
          <div style="font-family:monospace; font-size:24px; font-weight:800; color:#00F0FF; margin-top:14px;">CLICK(X=742, Y=518)</div>
          <div style="font-size:19px; color:#CBD5E1; margin-top:6px;">Tự nhìn màn hình • Tự di chuột</div>
        </div>
      </div>
    </div>

    <!-- Bottom 3 Telemetry Pills -->
    <div style="position:absolute; bottom:46px; left:58px; right:58px; display:grid; grid-template-columns:1fr 1fr 1fr; gap:20px;">
      <div style="background:#0B192E; border-left:6px solid #00F0FF; border-radius:12px; padding:18px 22px;">
        <div style="font-size:15px; color:#7DD3FC; font-weight:700;">BƯỚC 01</div>
        <div style="font-size:23px; font-weight:900; color:#FFF; margin-top:4px;">Chụp màn hình</div>
      </div>
      <div style="background:#0B192E; border-left:6px solid #38BDF8; border-radius:12px; padding:18px 22px;">
        <div style="font-size:15px; color:#7DD3FC; font-weight:700;">BƯỚC 02</div>
        <div style="font-size:23px; font-weight:900; color:#FFF; margin-top:4px;">Tính tọa độ X, Y</div>
      </div>
      <div style="background:#0B192E; border-left:6px solid #00F0FF; border-radius:12px; padding:18px 22px;">
        <div style="font-size:15px; color:#7DD3FC; font-weight:700;">BƯỚC 03</div>
        <div style="font-size:23px; font-weight:900; color:#00F0FF; margin-top:4px;">Click &amp; Gõ phím</div>
      </div>
    </div>
    </body></html>"""


def card_02_code_vs_nocode_split() -> str:
    """Card 02: Asymmetric Dual-Tower VS Battle Arena (Theme: Solar Amber #FFB800 vs Neon Violet #D946EF)"""
    bg = """
    background: linear-gradient(115deg, #1A1103 0%, #09080E 48%, #190622 100%);
    """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    {_common_reset_css(bg)}
    </style></head><body>
    <!-- Top Centered Title Banner -->
    <div style="position:absolute; top:38px; left:56px; right:56px; text-align:center;">
      <div style="font-size:20px; font-weight:800; color:#E2E8F0; letter-spacing:2px; text-transform:uppercase;">⚔️ ĐỐI ĐẦU KIẾN TRÚC TỰ ĐỘNG HÓA 2026</div>
      <div style="font-size:54px; font-weight:900; margin-top:8px; line-height:1.1;">
        <span style="color:#FFB800;">CODE THUẦN</span> HAY <span style="color:#E879F9;">NO-CODE</span>?
      </div>
    </div>

    <!-- Left Tower: PYTHON CODE (Solar Amber) -->
    <div style="position:absolute; top:185px; left:52px; width:462px; height:635px; background:linear-gradient(180deg, rgba(255,184,0,0.16) 0%, rgba(18,14,7,0.95) 100%); border:3px solid #FFB800; border-radius:30px; padding:32px; display:flex; flex-direction:column; gap:20px; box-shadow:0 20px 50px rgba(0,0,0,0.85);">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="background:#FFB800; color:#0B0904; font-weight:900; font-size:22px; padding:8px 20px; border-radius:10px;">PYTHON / TS</span>
        <span style="font-size:36px; font-weight:900; color:#FFB800;">100%</span>
      </div>
      <div style="font-size:36px; font-weight:900; color:#FFFFFF; line-height:1.15;">TÙY BIẾN SÂU &amp; CHI PHÍ 0Đ</div>
      <div style="background:#0B0905; border:1.5px solid rgba(255,184,0,0.4); border-radius:16px; padding:18px; font-family:monospace; font-size:19px; color:#FDE68A; line-height:1.5;">
        def run_agent(task):<br>
        &nbsp;&nbsp;res = llm.invoke(task)<br>
        &nbsp;&nbsp;return verify_gate(res)
      </div>
      <div style="display:flex; flex-direction:column; gap:14px; margin-top:auto;">
        <div style="background:rgba(255,184,0,0.12); padding:14px 18px; border-radius:12px; font-size:22px; font-weight:700; color:#FEF3C7;">✔ Kiểm soát 100% logic &amp; bảo mật</div>
        <div style="background:rgba(255,184,0,0.12); padding:14px 18px; border-radius:12px; font-size:22px; font-weight:700; color:#FEF3C7;">✔ Quản lý phiên bản qua Git</div>
        <div style="background:rgba(255,184,0,0.12); padding:14px 18px; border-radius:12px; font-size:22px; font-weight:700; color:#FEF3C7;">✔ Chạy hàng triệu tác vụ 0đ</div>
      </div>
    </div>

    <!-- Center VS Lightning Badge -->
    <div style="position:absolute; top:455px; left:492px; width:96px; height:96px; border-radius:50%; background:#FFFFFF; border:6px solid #09080E; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:34px; color:#09080E; z-index:20; box-shadow:0 0 40px rgba(255,255,255,0.6);">
      VS
    </div>

    <!-- Right Tower: NO-CODE (Neon Violet) -->
    <div style="position:absolute; top:185px; right:52px; width:462px; height:635px; background:linear-gradient(180deg, rgba(217,70,239,0.18) 0%, rgba(19,8,26,0.95) 100%); border:3px solid #E879F9; border-radius:30px; padding:32px; display:flex; flex-direction:column; gap:20px; box-shadow:0 20px 50px rgba(0,0,0,0.85);">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="background:#E879F9; color:#14051E; font-weight:900; font-size:22px; padding:8px 20px; border-radius:10px;">n8n / MAKE</span>
        <span style="font-size:36px; font-weight:900; color:#E879F9;">15 PHÚT</span>
      </div>
      <div style="font-size:36px; font-weight:900; color:#FFFFFF; line-height:1.15;">KÉO THẢ NHANH &amp; SẴN WEBHOOK</div>
      <!-- Node Flow Diagram -->
      <div style="background:#110617; border:1.5px solid rgba(232,121,249,0.4); border-radius:16px; padding:20px; display:flex; align-items:center; justify-content:space-between;">
        <div style="background:#701A75; padding:10px 14px; border-radius:10px; font-weight:800; font-size:17px;">Webhook</div>
        <span style="color:#E879F9; font-size:24px; font-weight:900;">➔</span>
        <div style="background:#86198F; padding:10px 14px; border-radius:10px; font-weight:800; font-size:17px;">AI Node</div>
        <span style="color:#E879F9; font-size:24px; font-weight:900;">➔</span>
        <div style="background:#A21CAF; padding:10px 14px; border-radius:10px; font-weight:800; font-size:17px;">Telegram</div>
      </div>
      <div style="display:flex; flex-direction:column; gap:14px; margin-top:auto;">
        <div style="background:rgba(232,121,249,0.12); padding:14px 18px; border-radius:12px; font-size:22px; font-weight:700; color:#FAE8FF;">✔ Dựng luồng mẫu trong 15 phút</div>
        <div style="background:rgba(232,121,249,0.12); padding:14px 18px; border-radius:12px; font-size:22px; font-weight:700; color:#FAE8FF;">✔ Kết nối nhanh 400+ dịch vụ</div>
        <div style="background:rgba(232,121,249,0.12); padding:14px 18px; border-radius:12px; font-size:22px; font-weight:700; color:#FAE8FF;">✔ Giao diện kéo thả trực quan</div>
      </div>
    </div>

    <!-- Bottom Hybrid Verdict Bar -->
    <div style="position:absolute; bottom:42px; left:52px; right:52px; height:158px; background:linear-gradient(90deg, #FFB800 0%, #E879F9 100%); border-radius:26px; padding:4px; box-shadow:0 20px 50px rgba(0,0,0,0.9);">
      <div style="width:100%; height:100%; background:#0B0A10; border-radius:22px; display:flex; align-items:center; justify-content:space-between; padding:0 38px;">
        <div>
          <div style="font-size:18px; font-weight:800; color:#FFB800; letter-spacing:1px;">★ LỜI GIẢI THỰC CHIẾN TỪ AI PLAYERS: MÔ HÌNH HYBRID</div>
          <div style="font-size:30px; font-weight:900; color:#FFFFFF; margin-top:6px;">Dùng <span style="color:#E879F9;">n8n</span> bắt sự kiện ngoài + <span style="color:#FFB800;">Python</span> xử lý lõi AI nặng!</div>
        </div>
        <div style="background:#FFFFFF; color:#0B0A10; font-weight:900; font-size:24px; padding:16px 28px; border-radius:16px; white-space:nowrap;">HYBRID 10/10</div>
      </div>
    </div>
    </body></html>"""


def card_03_git_state_sync_radar() -> str:
    """Card 03: Central Circular Radar Orbit & Dual-PC Sync Bridge (Theme: Emerald Matrix #00FF88 & Forest #03130C)"""
    bg = """
    background: radial-gradient(circle at 50% 54%, rgba(0, 255, 136, 0.25) 0%, rgba(3, 19, 12, 0) 60%),
                #030F0A;
    """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    {_common_reset_css(bg)}
    </style></head><body>
    <!-- Top Header -->
    <div style="position:absolute; top:42px; left:60px; right:60px; text-align:center;">
      <span style="background:rgba(0,255,136,0.15); border:2px solid #00FF88; color:#00FF88; font-weight:800; font-size:19px; padding:7px 24px; border-radius:999px;">
        🔄 GIAO THỨC AGENT-STATE-SYNC 2 CHIỀU
      </span>
      <div style="font-size:50px; font-weight:900; color:#FFFFFF; margin-top:16px; line-height:1.1;">
        ĐỒNG BỘ TỨC THỜI GIỮA <span style="color:#00FF88;">MÁY CÔNG TY &amp; MÁY NHÀ</span>
      </div>
    </div>

    <!-- Center Radar SVG -->
    <svg width="1080" height="1080" viewBox="0 0 1080 1080" style="position:absolute; inset:0;">
      <circle cx="540" cy="565" r="320" stroke="rgba(0,255,136,0.18)" stroke-width="2" stroke-dasharray="8 8" fill="none"/>
      <circle cx="540" cy="565" r="235" stroke="rgba(0,255,136,0.32)" stroke-width="2.5" fill="rgba(0,255,136,0.03)"/>
      <circle cx="540" cy="565" r="145" stroke="#00FF88" stroke-width="4" fill="#052116"/>
      <!-- Left and Right Connector Beams -->
      <path d="M 290 520 Q 415 430 430 510" stroke="#00FF88" stroke-width="5" fill="none"/>
      <path d="M 650 510 Q 665 430 790 520" stroke="#00FF88" stroke-width="5" fill="none"/>
      <path d="M 290 610 Q 415 700 430 620" stroke="#34D399" stroke-width="4" stroke-dasharray="10 6" fill="none"/>
      <path d="M 650 620 Q 665 700 790 610" stroke="#34D399" stroke-width="4" stroke-dasharray="10 6" fill="none"/>
    </svg>

    <!-- Central Hub Text -->
    <div style="position:absolute; top:485px; left:425px; width:230px; height:160px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div style="font-size:18px; font-weight:800; color:#6EE7B7;">GIT HUB VAULT</div>
      <div style="font-size:36px; font-weight:900; color:#00FF88; margin-top:4px;">0-CONFLICT</div>
      <div style="font-size:16px; color:#D1FAE5; margin-top:6px;">pull / push tự động</div>
    </div>

    <!-- Left Workstation Card (Company PC) -->
    <div style="position:absolute; top:430px; left:44px; width:275px; height:270px; background:#072318; border:3px solid #00FF88; border-radius:26px; padding:24px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; box-shadow:0 20px 45px rgba(0,0,0,0.85);">
      <div style="width:72px; height:72px; border-radius:18px; background:#00FF88; color:#03130C; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:30px;">PC 1</div>
      <div style="font-size:28px; font-weight:900; color:#FFF; margin-top:16px;">MÁY CÔNG TY</div>
      <div style="font-size:19px; color:#6EE7B7; margin-top:8px; line-height:1.35;">Chốt quy tắc &amp; xuất bản chiến dịch</div>
    </div>

    <!-- Right Workstation Card (Home PC) -->
    <div style="position:absolute; top:430px; right:44px; width:275px; height:270px; background:#072318; border:3px solid #00FF88; border-radius:26px; padding:24px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; box-shadow:0 20px 45px rgba(0,0,0,0.85);">
      <div style="width:72px; height:72px; border-radius:18px; background:#00FF88; color:#03130C; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:30px;">PC 2</div>
      <div style="font-size:28px; font-weight:900; color:#FFF; margin-top:16px;">MÁY Ở NHÀ</div>
      <div style="font-size:19px; color:#6EE7B7; margin-top:8px; line-height:1.35;">Nhận tiếp 100% mạch việc &amp; Cookie</div>
    </div>

    <!-- 4 Orbiting File Nodes (Top-Left, Top-Right, Bottom-Left, Bottom-Right) -->
    <div style="position:absolute; top:245px; left:135px; background:#0A2E20; border:2px solid #34D399; padding:14px 24px; border-radius:16px; font-weight:800; font-size:21px; color:#ECFDF5;">
      📄 WORK-HISTORY.md
    </div>
    <div style="position:absolute; top:245px; right:135px; background:#0A2E20; border:2px solid #34D399; padding:14px 24px; border-radius:16px; font-weight:800; font-size:21px; color:#ECFDF5;">
      🔐 fb_bot_session_vault.json
    </div>
    <div style="position:absolute; bottom:175px; left:135px; background:#0A2E20; border:2px solid #34D399; padding:14px 24px; border-radius:16px; font-weight:800; font-size:21px; color:#ECFDF5;">
      🧠 .agents/GEMINI.md
    </div>
    <div style="position:absolute; bottom:175px; right:135px; background:#0A2E20; border:2px solid #34D399; padding:14px 24px; border-radius:16px; font-weight:800; font-size:21px; color:#ECFDF5;">
      🚫 Chặn file nặng .MP4 / .DB
    </div>

    <!-- Bottom Status Strip -->
    <div style="position:absolute; bottom:42px; left:140px; right:140px; background:#00FF88; color:#03130C; font-weight:900; font-size:26px; text-align:center; padding:18px; border-radius:999px; box-shadow:0 0 35px rgba(0,255,136,0.45);">
      TỰ ĐỘNG PULL ĐẦU PHIÊN • TỰ ĐỘNG PUSH CUỐI PHIÊN
    </div>
    </body></html>"""


def card_04_json_schema_funnel() -> str:
    """Card 04: 3-Layer Laser Filter Funnel & Split Code Output (Theme: Crimson Laser #FF2E54 & Ice White on Slate #0B0F19)"""
    bg = """
    background: linear-gradient(180deg, #16070C 0%, #0B0F19 48%, #09131C 100%);
    """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    {_common_reset_css(bg)}
    </style></head><body>
    <!-- Top Right Pill & Left Headline -->
    <div style="position:absolute; top:42px; left:58px; right:58px; display:flex; justify-content:space-between; align-items:center;">
      <div style="font-size:48px; font-weight:900; line-height:1.1;">
        KHÓA CỨNG ĐẦU RA AI BẰNG<br><span style="color:#FF2E54;">100% JSON SCHEMA</span>
      </div>
      <div style="background:#FF2E54; color:#FFFFFF; font-weight:900; font-size:24px; padding:14px 26px; border-radius:16px; box-shadow:0 10px 30px rgba(255,46,84,0.4);">
        ZERO PARSE ERROR
      </div>
    </div>

    <!-- Stage 1: Raw Messy Prompt Output (Crossed Out) -->
    <div style="position:absolute; top:195px; left:120px; right:120px; height:150px; background:rgba(255,46,84,0.1); border:2.5px dashed #FF2E54; border-radius:22px; padding:22px 32px; display:flex; align-items:center; justify-content:space-between;">
      <div>
        <div style="font-size:17px; font-weight:800; color:#FF2E54;">❌ ĐẦU RA CHAT THÔNG THƯỜNG (DỄ VỠ CODE BACKEND):</div>
        <div style="font-family:monospace; font-size:22px; color:#FDA4AF; margin-top:8px;">
          "Dạ đây là danh sách của bạn nhé: {{ title: 'Video 1', thiếu_dấu_ngoặc..."
        </div>
      </div>
      <div style="font-size:46px; font-weight:900; color:#FF2E54;">CRASH!</div>
    </div>

    <!-- Stage 2: Full-Width Laser Schema Gate -->
    <div style="position:absolute; top:390px; left:48px; right:48px; height:128px; background:linear-gradient(90deg, #FF2E54 0%, #FB7185 50%, #FF2E54 100%); border-radius:24px; display:flex; align-items:center; justify-content:space-between; padding:0 42px; box-shadow:0 0 50px rgba(255,46,84,0.55);">
      <div style="font-size:32px; font-weight:900; color:#FFFFFF; letter-spacing:0.5px;">
        ⚡ CỔNG ÉP KHUÔN PYDANTIC / STRICT JSON SCHEMA
      </div>
      <div style="background:#0B0F19; color:#FFFFFF; font-family:monospace; font-weight:800; font-size:22px; padding:10px 22px; border-radius:12px;">
        strict: true
      </div>
    </div>

    <!-- Stage 3: Bottom Split (Clean JSON IDE Left + 3 Guarantees Right) -->
    <div style="position:absolute; top:565px; left:58px; width:560px; height:455px; background:#060911; border:3px solid #38BDF8; border-radius:26px; padding:28px; font-family:monospace; box-shadow:0 24px 60px rgba(0,0,0,0.9);">
      <div style="color:#38BDF8; font-size:18px; font-weight:800; margin-bottom:14px;">// OUTPUT ĐÃ QUA KIỂM ĐỊNH 100%:</div>
      <div style="font-size:23px; line-height:1.58; color:#E2E8F0;">
        {{<br>
        &nbsp;&nbsp;<span style="color:#7DD3FC;">"campaign_id"</span>: <span style="color:#4ADE80;">"ai_vault_2026"</span>,<br>
        &nbsp;&nbsp;<span style="color:#7DD3FC;">"rubric_score"</span>: <span style="color:#FACC15;">9.6</span>,<br>
        &nbsp;&nbsp;<span style="color:#7DD3FC;">"zero_clone_passed"</span>: <span style="color:#FF2E54;">true</span>,<br>
        &nbsp;&nbsp;<span style="color:#7DD3FC;">"channels"</span>: [<span style="color:#4ADE80;">"FB"</span>, <span style="color:#4ADE80;">"YT"</span>]<br>
        }}
      </div>
    </div>

    <div style="position:absolute; top:565px; right:58px; width:375px; height:455px; display:flex; flex-direction:column; gap:20px;">
      <div style="flex:1; background:#111827; border:2px solid rgba(255,255,255,0.2); border-radius:22px; padding:22px; display:flex; flex-direction:column; justify-content:center;">
        <div style="font-size:17px; color:#94A3B8; font-weight:700;">ĐỘ CHÍNH XÁC CÚ PHÁP</div>
        <div style="font-size:44px; font-weight:900; color:#4ADE80; margin-top:4px;">100.0%</div>
      </div>
      <div style="flex:1; background:#111827; border:2px solid rgba(255,255,255,0.2); border-radius:22px; padding:22px; display:flex; flex-direction:column; justify-content:center;">
        <div style="font-size:17px; color:#94A3B8; font-weight:700;">NỐI THẲNG DATABASE</div>
        <div style="font-size:32px; font-weight:900; color:#FFFFFF; margin-top:4px;">SQLite &amp; Webhook</div>
      </div>
      <div style="flex:1; background:#FF2E54; border-radius:22px; padding:22px; display:flex; align-items:center; justify-content:center; text-align:center; font-size:28px; font-weight:900; color:#FFFFFF;">
        LOẠI BỎ 100% VĂN THỪA
      </div>
    </div>
    </body></html>"""


def card_05_second_brain_constellation() -> str:
    """Card 05: Radial Neural Mindmap Constellation + Bottom Banner (Theme: Gold #FBBF24 & Cosmic Indigo #09061C)"""
    bg = """
    background: radial-gradient(circle at 50% 42%, rgba(251, 191, 36, 0.24) 0%, rgba(9, 6, 28, 0) 58%),
                linear-gradient(180deg, #070516 0%, #110B29 100%);
    """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    {_common_reset_css(bg)}
    .node-box {{
      position:absolute; width:260px; background:rgba(20, 15, 45, 0.94);
      border:2.5px solid #FBBF24; border-radius:20px; padding:18px 20px;
      box-shadow:0 15px 35px rgba(0,0,0,0.85);
    }}
    </style></head><body>
    <!-- SVG Synaptic Spokes -->
    <svg width="1080" height="1080" viewBox="0 0 1080 1080" style="position:absolute; inset:0;">
      <line x1="540" y1="415" x2="190" y2="165" stroke="#FBBF24" stroke-width="3.5"/>
      <line x1="540" y1="415" x2="890" y2="165" stroke="#FBBF24" stroke-width="3.5"/>
      <line x1="540" y1="415" x2="175" y2="415" stroke="#F59E0B" stroke-width="3.5"/>
      <line x1="540" y1="415" x2="905" y2="415" stroke="#F59E0B" stroke-width="3.5"/>
      <line x1="540" y1="415" x2="220" y2="665" stroke="#FBBF24" stroke-width="3.5"/>
      <line x1="540" y1="415" x2="860" y2="665" stroke="#FBBF24" stroke-width="3.5"/>
      <circle cx="540" cy="415" r="128" fill="#FBBF24" stroke="#FFFBEB" stroke-width="6"/>
    </svg>

    <!-- Central Golden Brain Hub -->
    <div style="position:absolute; top:325px; left:420px; width:240px; height:180px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; color:#09061C;">
      <div style="font-size:17px; font-weight:900; letter-spacing:1px;">SUBAGENT</div>
      <div style="font-size:34px; font-weight:900; line-height:1.05; margin-top:4px;">BỘ NÃO<br>THỨ 2</div>
      <div style="font-size:15px; font-weight:800; margin-top:6px; background:#09061C; color:#FBBF24; padding:3px 12px; border-radius:999px;">INDEX.MD</div>
    </div>

    <!-- 6 Surrounding Memory Nodes -->
    <div class="node-box" style="top:85px; left:52px;">
      <div style="color:#FBBF24; font-weight:800; font-size:15px;">MEM-01 // VISUAL</div>
      <div style="font-size:22px; font-weight:900; margin-top:4px;">Luật Zero-Clone</div>
      <div style="font-size:16px; color:#CBD5E1; margin-top:4px;">Cấm lặp bố cục ảnh/video</div>
    </div>

    <div class="node-box" style="top:85px; right:52px;">
      <div style="color:#FBBF24; font-weight:800; font-size:15px;">MEM-02 // AUDIO</div>
      <div style="font-size:22px; font-weight:900; margin-top:4px;">Chuẩn Voice -3dB</div>
      <div style="font-size:16px; color:#CBD5E1; margin-top:4px;">Vbee Mạnh Dũng &amp; BGM</div>
    </div>

    <div class="node-box" style="top:350px; left:42px;">
      <div style="color:#FBBF24; font-weight:800; font-size:15px;">MEM-03 // SAFETY</div>
      <div style="font-size:22px; font-weight:900; margin-top:4px;">Tường Lửa Cá Nhân</div>
      <div style="font-size:16px; color:#CBD5E1; margin-top:4px;">Chỉ bình luận bằng Fanpage</div>
    </div>

    <div class="node-box" style="top:350px; right:42px;">
      <div style="color:#FBBF24; font-weight:800; font-size:15px;">MEM-04 // SALES</div>
      <div style="font-size:22px; font-weight:900; margin-top:4px;">Editorial 3-Grid</div>
      <div style="font-size:16px; color:#CBD5E1; margin-top:4px;">Chuẩn ảnh 3 Page Bán Hàng</div>
    </div>

    <div class="node-box" style="top:605px; left:68px;">
      <div style="color:#FBBF24; font-weight:800; font-size:15px;">MEM-05 // PURGE</div>
      <div style="font-size:22px; font-weight:900; margin-top:4px;">Xóa Tư Liệu Cũ</div>
      <div style="font-size:16px; color:#CBD5E1; margin-top:4px;">Dọn sạch code lỗi thời</div>
    </div>

    <div class="node-box" style="top:605px; right:68px;">
      <div style="color:#FBBF24; font-weight:800; font-size:15px;">MEM-06 // SYNC</div>
      <div style="font-size:22px; font-weight:900; margin-top:4px;">Đồng Bộ 2 Máy</div>
      <div style="font-size:16px; color:#CBD5E1; margin-top:4px;">Git &amp; Cookie Vault tự động</div>
    </div>

    <!-- Bottom-Anchored Hero Title Block -->
    <div style="position:absolute; bottom:44px; left:52px; right:52px; background:linear-gradient(90deg, rgba(251,191,36,0.2) 0%, rgba(20,15,45,0.96) 100%); border:3px solid #FBBF24; border-radius:28px; padding:28px 40px; display:flex; align-items:center; justify-content:space-between;">
      <div>
        <div style="font-size:19px; font-weight:800; color:#FBBF24;">🧠 KIẾN TRÚC TRÍ NHỚ DÀI HẠN CHO AI AGENT</div>
        <div style="font-size:40px; font-weight:900; color:#FFFFFF; margin-top:6px; line-height:1.12;">
          ĐỘI NGŨ AI CÀNG LÀM VIỆC CÀNG THÔNG MINH!
        </div>
      </div>
      <div style="background:#FBBF24; color:#09061C; font-weight:900; font-size:26px; padding:18px 28px; border-radius:18px; white-space:nowrap;">
        0% MẤT TRÍ NHỚ
      </div>
    </div>
    </body></html>"""


def card_06_four_kpi_speedometers() -> str:
    """Card 06: 4 Circular Speedometer Dial Gauges + Bottom Telemetry (Theme: Acid Lime #D4FF00 & Racing Carbon)"""
    bg = """
    background: radial-gradient(circle at 50% 15%, rgba(212,255,0,0.18) 0%, transparent 55%), #08090C;
    """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    {_common_reset_css(bg)}
    .dial-card {{
      background:#11141C; border:2.5px solid rgba(212,255,0,0.45); border-radius:26px;
      padding:24px 16px; display:flex; flex-direction:column; align-items:center; text-align:center;
      box-shadow:0 18px 40px rgba(0,0,0,0.85);
    }}
    </style></head><body>
    <!-- Top Header -->
    <div style="position:absolute; top:42px; left:56px; right:56px; text-align:center;">
      <div style="font-size:20px; font-weight:800; color:#D4FF00; letter-spacing:2px;">📈 ĐO LƯỜNG HIỆU SUẤT THỰC CHIẾN — BỎ QUA VIEW ẢO</div>
      <div style="font-size:52px; font-weight:900; color:#FFFFFF; margin-top:8px;">
        4 ĐỒNG HỒ CHỈ SỐ QUYẾT ĐỊNH <span style="color:#D4FF00;">DOANH SỐ</span>
      </div>
    </div>

    <!-- 4 Circular Speedometer Gauges in a Row -->
    <div style="position:absolute; top:220px; left:48px; right:48px; display:grid; grid-template-columns:repeat(4, 1fr); gap:20px;">
      <div class="dial-card">
        <svg width="170" height="170" viewBox="0 0 160 160">
          <circle cx="80" cy="80" r="64" stroke="#1E293B" stroke-width="14" fill="none"/>
          <circle cx="80" cy="80" r="64" stroke="#D4FF00" stroke-width="14" stroke-dasharray="280 402" stroke-linecap="round" transform="rotate(-90 80 80)" fill="none"/>
          <text x="80" y="92" text-anchor="middle" font-size="38" font-weight="900" fill="#D4FF00">&gt;65%</text>
        </svg>
        <div style="font-size:24px; font-weight:900; color:#FFF; margin-top:14px;">HOOK 3 GIÂY</div>
        <div style="font-size:17px; color:#94A3B8; margin-top:6px;">Tỷ lệ giữ chân người xem qua 3s đầu</div>
      </div>

      <div class="dial-card" style="border-color:#F42F6C;">
        <svg width="170" height="170" viewBox="0 0 160 160">
          <circle cx="80" cy="80" r="64" stroke="#1E293B" stroke-width="14" fill="none"/>
          <circle cx="80" cy="80" r="64" stroke="#F42F6C" stroke-width="14" stroke-dasharray="310 402" stroke-linecap="round" transform="rotate(-90 80 80)" fill="none"/>
          <text x="80" y="92" text-anchor="middle" font-size="38" font-weight="900" fill="#F42F6C">12.4%</text>
        </svg>
        <div style="font-size:24px; font-weight:900; color:#FFF; margin-top:14px;">CTR BÌNH LUẬN</div>
        <div style="font-size:17px; color:#94A3B8; margin-top:6px;">Tỷ lệ bấm link ở Pinned Comment #1</div>
      </div>

      <div class="dial-card">
        <svg width="170" height="170" viewBox="0 0 160 160">
          <circle cx="80" cy="80" r="64" stroke="#1E293B" stroke-width="14" fill="none"/>
          <circle cx="80" cy="80" r="64" stroke="#D4FF00" stroke-width="14" stroke-dasharray="260 402" stroke-linecap="round" transform="rotate(-90 80 80)" fill="none"/>
          <text x="80" y="92" text-anchor="middle" font-size="38" font-weight="900" fill="#D4FF00">42%</text>
        </svg>
        <div style="font-size:24px; font-weight:900; color:#FFF; margin-top:14px;">TỶ LỆ VÀO PHỄU</div>
        <div style="font-size:17px; color:#94A3B8; margin-top:6px;">Khách nhận tài liệu gia nhập cộng đồng</div>
      </div>

      <div class="dial-card" style="border-color:#F42F6C;">
        <svg width="170" height="170" viewBox="0 0 160 160">
          <circle cx="80" cy="80" r="64" stroke="#1E293B" stroke-width="14" fill="none"/>
          <circle cx="80" cy="80" r="64" stroke="#F42F6C" stroke-width="14" stroke-dasharray="340 402" stroke-linecap="round" transform="rotate(-90 80 80)" fill="none"/>
          <text x="80" y="92" text-anchor="middle" font-size="38" font-weight="900" fill="#F42F6C">4.8X</text>
        </svg>
        <div style="font-size:24px; font-weight:900; color:#FFF; margin-top:14px;">ROAS / LỢI NHUẬN</div>
        <div style="font-size:17px; color:#94A3B8; margin-top:6px;">Doanh thu chia tổng chi phí Token AI</div>
      </div>
    </div>

    <!-- Bottom Executive Comparison Deck -->
    <div style="position:absolute; bottom:48px; left:48px; right:48px; height:360px; background:#10131B; border:3px solid #D4FF00; border-radius:30px; padding:34px 42px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="font-size:28px; font-weight:900; color:#D4FF00;">⚡ QUY TẮC RA QUYẾT ĐỊNH CỦA SUBAGENT `HIEU-SUAT`:</div>
      <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:22px;">
        <div style="background:#171C28; border-top:6px solid #22C55E; padding:20px; border-radius:16px;">
          <div style="font-size:24px; font-weight:900; color:#22C55E;">KEEP &amp; SCALE</div>
          <div style="font-size:19px; color:#E2E8F0; margin-top:8px;">Hook &gt; 60% &amp; CTR &gt; 10%: Nhân bản góc tiếp cận sang 3 kênh.</div>
        </div>
        <div style="background:#171C28; border-top:6px solid #FACC15; padding:20px; border-radius:16px;">
          <div style="font-size:24px; font-weight:900; color:#FACC15;">ITERATE HOOK</div>
          <div style="font-size:19px; color:#E2E8F0; margin-top:8px;">CTR cao nhưng rớt 3s đầu: Giữ nguyên sản phẩm, thay câu mở đầu.</div>
        </div>
        <div style="background:#171C28; border-top:6px solid #F42F6C; padding:20px; border-radius:16px;">
          <div style="font-size:24px; font-weight:900; color:#F42F6C;">STOP NGAY</div>
          <div style="font-size:19px; color:#E2E8F0; margin-top:8px;">Xem hết video nhưng 0 click: Đổi quà Lead Magnet hoặc đổi SKU.</div>
        </div>
      </div>
    </div>
    </body></html>"""


def card_07_fasthtml_left_pillar_staircase() -> str:
    """Card 07: Left Vertical Pillar + Right 3-Step Ascending Staircase (Theme: Sky Blue #38BDF8 & Python Gold #FACC15)"""
    bg = """
    background: linear-gradient(135deg, #040D1A 0%, #0A192F 100%);
    """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    {_common_reset_css(bg)}
    </style></head><body>
    <!-- Left Vertical Hero Sidebar -->
    <div style="position:absolute; top:44px; left:44px; bottom:44px; width:340px; background:linear-gradient(180deg, #0284C7 0%, #0369A1 55%, #1E3A8A 100%); border:3px solid #38BDF8; border-radius:32px; padding:36px 28px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 24px 60px rgba(0,0,0,0.85);">
      <div style="background:#FACC15; color:#040D1A; font-weight:900; font-size:20px; padding:10px 18px; border-radius:12px; text-align:center;">
        🐍 PYTHON THUẦN 100%
      </div>
      <div>
        <div style="font-size:74px; font-weight:900; color:#FFFFFF; line-height:0.95; letter-spacing:-2px;">FAST<br><span style="color:#FACC15;">HTML</span></div>
        <div style="font-size:24px; font-weight:700; color:#E0F2FE; margin-top:20px; line-height:1.35;">
          Xây dựng Web App AI tốc độ cao không cần viết phức tạp React, Node hay Webpack!
        </div>
      </div>
      <div style="background:rgba(4,13,26,0.75); border:2px solid #FACC15; border-radius:18px; padding:18px; text-align:center;">
        <div style="font-size:15px; color:#BAE6FD; font-weight:700;">DUNG LƯỢNG SOURCE</div>
        <div style="font-size:38px; font-weight:900; color:#FACC15; margin-top:4px;">&lt; 60 DÒNG</div>
      </div>
    </div>

    <!-- Right 3 Ascending Staircase Cards -->
    <div style="position:absolute; top:48px; left:420px; right:44px; height:295px; background:#0D1F38; border:3px solid #38BDF8; border-radius:28px; padding:28px 34px; display:flex; flex-direction:column; justify-content:center;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="color:#38BDF8; font-weight:900; font-size:22px;">TẦNG 01 // KHỞI TẠO TRONG 10 GIÂY</span>
        <span style="background:#0284C7; padding:6px 16px; border-radius:8px; font-family:monospace; font-weight:800;">pip install python-fasthtml</span>
      </div>
      <div style="font-family:monospace; font-size:22px; color:#FDE047; background:#06101E; padding:18px 22px; border-radius:16px; margin-top:16px; border:1px solid rgba(56,189,248,0.3);">
        from fasthtml.common import *<br>
        app, rt = fast_app()
      </div>
    </div>

    <div style="position:absolute; top:380px; left:455px; right:44px; height:295px; background:#0D1F38; border:3px solid #FACC15; border-radius:28px; padding:28px 34px; display:flex; flex-direction:column; justify-content:center;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="color:#FACC15; font-weight:900; font-size:22px;">TẦNG 02 // PHẢN HỒI THỜI GIAN THỰC HTMX</span>
        <span style="background:#CA8A04; color:#040D1A; padding:6px 16px; border-radius:8px; font-weight:900;">0% JAVASCRIPT</span>
      </div>
      <div style="font-size:24px; color:#FFFFFF; font-weight:700; margin-top:16px; line-height:1.45;">
        Mọi thao tác bấm nút, gửi form, stream câu trả lời của AI đều cập nhật trực tiếp trên DOM mà không cần tải lại trang.
      </div>
    </div>

    <div style="position:absolute; top:712px; left:490px; right:44px; height:320px; background:linear-gradient(135deg, #112847 0%, #091526 100%); border:3px solid #38BDF8; border-radius:28px; padding:28px 34px; display:flex; flex-direction:column; justify-content:center;">
      <div style="color:#38BDF8; font-weight:900; font-size:22px;">TẦNG 03 // TRIỂN KHAI LÊN CLOUD TRONG 1 LỆNH</div>
      <div style="font-size:32px; font-weight:900; color:#FFFFFF; margin-top:12px; line-height:1.2;">
        Đóng gói hoàn chỉnh Dashboard điều khiển đội Subagent AI!
      </div>
      <div style="margin-top:20px; background:#FACC15; color:#040D1A; font-weight:900; font-size:22px; padding:14px 24px; border-radius:14px; text-align:center;">
        BÌNH LUẬN "FASTHTML" NHẬN SOURCE MẪU
      </div>
    </div>
    </body></html>"""


def card_08_subagent_roi_waterfall() -> str:
    """Card 08: Full-Canvas Cost-Drop Waterfall Bar Chart (Theme: Neon Mint #2DD4BF & Rose Red #FB7185)"""
    bg = """
    background: linear-gradient(180deg, #071013 0%, #0B191E 100%);
    """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    {_common_reset_css(bg)}
    </style></head><body>
    <!-- Top Header -->
    <div style="position:absolute; top:42px; left:58px; right:58px; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-size:20px; font-weight:800; color:#2DD4BF;">📊 BÀI TOÁN KINH TẾ &amp; LỢI TỨC ĐẦU TƯ (ROI)</div>
        <div style="font-size:48px; font-weight:900; color:#FFFFFF; margin-top:6px;">
          CẮT GIẢM <span style="color:#2DD4BF;">92% CHI PHÍ VẬN HÀNH</span> BẰNG SUBAGENT
        </div>
      </div>
    </div>

    <!-- Chart Frame -->
    <div style="position:absolute; top:195px; left:58px; right:58px; bottom:56px; background:#050B0E; border:2.5px solid rgba(45,212,191,0.4); border-radius:30px; padding:40px;">
      <!-- Left Tall Bar: Manual Team -->
      <div style="position:absolute; bottom:110px; left:85px; width:260px; height:560px; background:linear-gradient(180deg, #FB7185 0%, #9F1239 100%); border:3px solid #FDA4AF; border-radius:24px 24px 0 0; display:flex; flex-direction:column; align-items:center; justify-content:space-between; padding:28px 18px; box-shadow:0 0 40px rgba(251,113,133,0.3);">
        <div style="font-size:42px; font-weight:900; color:#FFF;">45 TR</div>
        <div style="font-size:20px; font-weight:700; color:#FFE4E6; text-align:center; line-height:1.4;">
          4 Nhân sự thủ công<br>• Viết kịch bản<br>• Thiết kế ảnh<br>• Dựng video<br>• Trực bình luận
        </div>
        <div style="background:#4C0519; padding:8px 16px; border-radius:8px; font-weight:800; font-size:17px;">8 GIỜ / NGÀY</div>
      </div>

      <!-- Diagonal Waterfall Drop Arrow SVG -->
      <svg width="400" height="450" viewBox="0 0 400 450" style="position:absolute; top:140px; left:335px;">
        <path d="M 20 60 C 160 60, 180 340, 310 340" stroke="#2DD4BF" stroke-width="8" stroke-dasharray="14 8" fill="none"/>
        <polygon points="310,322 345,340 310,358" fill="#2DD4BF"/>
      </svg>

      <!-- Floating Savings Callout in Upper Right -->
      <div style="position:absolute; top:55px; right:65px; width:510px; background:linear-gradient(135deg, #0F292E 0%, #08181B 100%); border:3px solid #2DD4BF; border-radius:26px; padding:28px 32px; box-shadow:0 20px 50px rgba(0,0,0,0.85);">
        <div style="font-size:19px; font-weight:800; color:#2DD4BF;">⚡ HIỆU QUẢ ĐỘT PHÁ NGAY THÁNG ĐẦU:</div>
        <div style="font-size:56px; font-weight:900; color:#FFFFFF; margin-top:6px;">TIẾT KIỆM 41.8 TRIỆU</div>
        <div style="font-size:22px; color:#CCFBF1; margin-top:10px; line-height:1.4;">
          Tốc độ sản xuất tăng gấp <b>6 lần</b>, vận hành 4 Fanpage xuyên đêm không nghỉ lễ!
        </div>
      </div>

      <!-- Right Short Bar: 10 Subagents -->
      <div style="position:absolute; bottom:110px; right:95px; width:260px; height:175px; background:linear-gradient(180deg, #2DD4BF 0%, #0D9488 100%); border:3px solid #99F6E4; border-radius:24px 24px 0 0; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:16px; box-shadow:0 0 45px rgba(45,212,191,0.5);">
        <div style="font-size:44px; font-weight:900; color:#042F2E;">3.2 TR</div>
        <div style="font-size:18px; font-weight:900; color:#042F2E; margin-top:4px;">10 SUBAGENT 24/7</div>
      </div>

      <!-- Bottom Axis Line -->
      <div style="position:absolute; bottom:106px; left:50px; right:50px; height:4px; background:#334155;"></div>
      <div style="position:absolute; bottom:42px; left:85px; width:260px; text-align:center; font-size:24px; font-weight:900; color:#FB7185;">MÔ HÌNH CŨ</div>
      <div style="position:absolute; bottom:42px; right:95px; width:260px; text-align:center; font-size:24px; font-weight:900; color:#2DD4BF;">ĐỘI SUBAGENT AI</div>
    </div>
    </body></html>"""


def card_09_cleanup_storage_ring() -> str:
    """Card 09: Giant Left Donut Ring + Right 4 Hardware Toggle Switches (Theme: Blaze Orange #FF6B00 & Cyan #00E5FF)"""
    bg = """
    background: radial-gradient(circle at 25% 55%, rgba(255,107,0,0.2) 0%, transparent 55%), #0B0D13;
    """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    {_common_reset_css(bg)}
    .sw-row {{
      background:#131722; border:2.5px solid rgba(0,229,255,0.4); border-radius:22px;
      padding:22px 28px; display:flex; align-items:center; justify-content:space-between;
    }}
    .sw-pill {{
      width:88px; height:44px; background:#00E5FF; border-radius:999px; position:relative;
      display:flex; align-items:center; padding:4px; justify-content:flex-end;
      box-shadow:0 0 20px rgba(0,229,255,0.5);
    }}
    .sw-knob {{ width:36px; height:36px; background:#0B0D13; border-radius:50%; }}
    </style></head><body>
    <!-- Header -->
    <div style="position:absolute; top:42px; left:56px; right:56px; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-size:20px; font-weight:800; color:#FF6B00;">🧹 GIAO THỨC PURGE-ON-UPGRADE &amp; DỌN RÁC ĐỊNH KỲ</div>
        <div style="font-size:50px; font-weight:900; color:#FFFFFF; margin-top:6px;">
          GIỮ HỆ THỐNG AI <span style="color:#00E5FF;">NHANH NHƯ MỚI</span>
        </div>
      </div>
    </div>

    <!-- Left Giant Donut Ring Card -->
    <div style="position:absolute; top:205px; left:52px; width:445px; bottom:52px; background:#111520; border:3px solid #FF6B00; border-radius:32px; padding:32px; display:flex; flex-direction:column; align-items:center; justify-content:space-between;">
      <div style="font-size:24px; font-weight:900; color:#FF6B00;">DUNG LƯỢNG &amp; CPU TỐI ƯU</div>
      <svg width="320" height="320" viewBox="0 0 280 280">
        <circle cx="140" cy="140" r="110" stroke="#1E293B" stroke-width="26" fill="none"/>
        <circle cx="140" cy="140" r="110" stroke="#FF6B00" stroke-width="26" stroke-dasharray="580 691" stroke-linecap="round" transform="rotate(-90 140 140)" fill="none"/>
        <text x="140" y="135" text-anchor="middle" font-size="56" font-weight="900" fill="#FFFFFF">-28GB</text>
        <text x="140" y="175" text-anchor="middle" font-size="22" font-weight="800" fill="#00E5FF">ĐÃ DỌN SẠCH</text>
      </svg>
      <div style="width:100%; background:#0B0D13; border:2px solid rgba(255,107,0,0.45); border-radius:20px; padding:20px; text-align:center;">
        <div style="font-size:18px; color:#94A3B8; font-weight:700;">CHỐNG NHẦM TƯ LIỆU CŨ</div>
        <div style="font-size:32px; font-weight:900; color:#00E5FF; margin-top:6px;">100% CLEAN TREE</div>
      </div>
    </div>

    <!-- Right 4 Toggle Switch Rows -->
    <div style="position:absolute; top:205px; right:52px; width:505px; bottom:52px; display:flex; flex-direction:column; justify-content:space-between;">
      <div class="sw-row">
        <div>
          <div style="font-size:26px; font-weight:900; color:#FFF;">1. Xóa Template &amp; Ảnh Cũ</div>
          <div style="font-size:18px; color:#94A3B8; margin-top:4px;">Triệt tiêu nguy cơ Agent đọc nhầm mẫu cũ</div>
        </div>
        <div class="sw-pill"><div class="sw-knob"></div></div>
      </div>

      <div class="sw-row">
        <div>
          <div style="font-size:26px; font-weight:900; color:#FFF;">2. Đóng Chrome Bot Ngầm</div>
          <div style="font-size:18px; color:#94A3B8; margin-top:4px;">Tự giải phóng RAM ngay sau ca tương tác</div>
        </div>
        <div class="sw-pill"><div class="sw-knob"></div></div>
      </div>

      <div class="sw-row">
        <div>
          <div style="font-size:26px; font-weight:900; color:#FFF;">3. Dọn Bundle &amp; Log Rác</div>
          <div style="font-size:18px; color:#94A3B8; margin-top:4px;">Xóa file tạm quá 7 ngày tự động</div>
        </div>
        <div class="sw-pill"><div class="sw-knob"></div></div>
      </div>

      <div class="sw-row" style="border-color:#FF6B00;">
        <div>
          <div style="font-size:26px; font-weight:900; color:#FF6B00;">4. Khóa Chặn Tiến Trình Lạ</div>
          <div style="font-size:18px; color:#E2E8F0; margin-top:4px;">Giữ CPU luôn mát ở mức 2% – 5%</div>
        </div>
        <div class="sw-pill" style="background:#FF6B00;"><div class="sw-knob"></div></div>
      </div>
    </div>
    </body></html>"""


def card_10_voc_comment_mining_strata() -> str:
    """Card 10: 3 Horizontal Geological Mining Strata Layers (Theme: Amethyst Purple #A855F7 & Cyber Gold #FDE047)"""
    bg = """
    background: linear-gradient(180deg, #120722 0%, #090412 100%);
    """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    {_common_reset_css(bg)}
    </style></head><body>
    <!-- Top Banner -->
    <div style="position:absolute; top:40px; left:58px; right:58px; text-align:center;">
      <div style="font-size:20px; font-weight:800; color:#FDE047; letter-spacing:1.5px;">⛏️ KỸ THUẬT COMMENT MINING &amp; VOICE OF CUSTOMER (VOC)</div>
      <div style="font-size:50px; font-weight:900; color:#FFFFFF; margin-top:8px;">
        ĐÀO <span style="color:#C084FC;">10,000+ BÌNH LUẬN</span> TÌM KỊCH BẢN TRIỆU VIEW
      </div>
    </div>

    <!-- Strata Layer 1: Raw Surface Comments -->
    <div style="position:absolute; top:200px; left:58px; right:58px; height:225px; background:#1B0E30; border:3px solid #A855F7; border-radius:28px; padding:26px 36px; display:flex; align-items:center; justify-content:space-between;">
      <div style="width:660px;">
        <div style="color:#C084FC; font-weight:900; font-size:20px;">TẦNG ĐỊA CHẤT 01 // MẶT ĐẤT BÌNH LUẬN THÔ</div>
        <div style="font-size:32px; font-weight:900; color:#FFF; margin-top:8px;">Quét tự động bình luận bài Viral đối thủ</div>
        <div style="font-size:20px; color:#E9D5FF; margin-top:8px;">Thu thập câu hỏi thật, từ lóng thật và những bức xúc chưa được giải quyết của khách hàng.</div>
      </div>
      <div style="background:#2E1065; border:2px solid #C084FC; padding:22px 28px; border-radius:20px; text-align:center;">
        <div style="font-size:44px; font-weight:900; color:#FFF;">10,000+</div>
        <div style="font-size:17px; font-weight:800; color:#C084FC;">RAW COMMENTS</div>
      </div>
    </div>

    <!-- Downward Laser Drill Arrows -->
    <div style="position:absolute; top:432px; left:490px; font-size:38px; color:#FDE047; font-weight:900;">▼▼▼</div>

    <!-- Strata Layer 2: AI VOC Classifier -->
    <div style="position:absolute; top:485px; left:98px; right:98px; height:225px; background:#251142; border:3px solid #E879F9; border-radius:28px; padding:26px 36px; display:flex; align-items:center; justify-content:space-between;">
      <div>
        <div style="color:#F0ABFC; font-weight:900; font-size:20px;">TẦNG ĐỊA CHẤT 02 // MÁY KHOAN PHÂN LOẠI NỖI ĐAU</div>
        <div style="font-size:32px; font-weight:900; color:#FFF; margin-top:8px;">Tách 3 nhóm: Nỗi sợ • Rào cản giá • Khao khát</div>
        <div style="font-size:20px; color:#F5D0FE; margin-top:8px;">Loại bỏ bình luận rác, gom cụm các câu phàn nàn xuất hiện lặp lại trên 50 lần.</div>
      </div>
      <div style="background:#4A044E; border:2px solid #F0ABFC; padding:22px 28px; border-radius:20px; text-align:center;">
        <div style="font-size:44px; font-weight:900; color:#F0ABFC;">TOP 1%</div>
        <div style="font-size:17px; font-weight:800; color:#FFF;">INSIGHT ĐẮT GIÁ</div>
      </div>
    </div>

    <div style="position:absolute; top:717px; left:490px; font-size:38px; color:#FDE047; font-weight:900;">▼▼▼</div>

    <!-- Strata Layer 3: Pure Gold Hook Vault -->
    <div style="position:absolute; top:770px; left:138px; right:138px; height:250px; background:linear-gradient(135deg, #FDE047 0%, #F59E0B 100%); border-radius:30px; padding:28px 40px; color:#090412; display:flex; align-items:center; justify-content:space-between; box-shadow:0 0 50px rgba(253,224,71,0.45);">
      <div>
        <div style="font-weight:900; font-size:20px; letter-spacing:1px;">💎 TẦNG MỎ VÀNG 03 // KỊCH BẢN CHỐT ĐƠN</div>
        <div style="font-size:38px; font-weight:900; margin-top:8px; line-height:1.15;">
          Dùng chính ngôn ngữ khách hàng<br>làm câu Hook 3 giây đầu tiên!
        </div>
      </div>
      <div style="background:#090412; color:#FDE047; font-weight:900; font-size:28px; padding:22px 30px; border-radius:22px; text-align:center;">
        X3 TỶ LỆ<br>CHUYỂN ĐỔI
      </div>
    </div>
    </body></html>"""


def card_11_github_multiagent_podium() -> str:
    """Card 11: 3-Column Olympic Podium Rising From Bottom (Theme: Trophy Gold #F59E0B, Platinum #E2E8F0, Blue #3B82F6)"""
    bg = """
    background: radial-gradient(circle at 50% 35%, rgba(245,158,11,0.22) 0%, transparent 60%), #050811;
    """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    {_common_reset_css(bg)}
    </style></head><body>
    <!-- Top Ticker & Title -->
    <div style="position:absolute; top:42px; left:56px; right:56px; text-align:center;">
      <div style="display:inline-block; background:#1E293B; border:2px solid #F59E0B; color:#FDE68A; font-weight:800; font-size:19px; padding:8px 26px; border-radius:999px;">
        🏆 BẢNG XẾP HẠNG GITHUB MULTI-AGENT 2026
      </div>
      <div style="font-size:52px; font-weight:900; color:#FFFFFF; margin-top:14px;">
        3 FRAMEWORK ĐỘI NGŨ AI <span style="color:#F59E0B;">ĐÁNG DÙNG NHẤT</span>
      </div>
    </div>

    <!-- Left Podium #2: AutoGen (Silver/Platinum) -->
    <div style="position:absolute; bottom:48px; left:64px; width:292px; height:560px; background:linear-gradient(180deg, #334155 0%, #0F172A 100%); border:3px solid #CBD5E1; border-radius:28px 28px 12px 12px; padding:28px 24px; display:flex; flex-direction:column; align-items:center; text-align:center;">
      <div style="width:74px; height:74px; border-radius:50%; background:#E2E8F0; color:#0F172A; font-weight:900; font-size:38px; display:flex; align-items:center; justify-content:center;">#2</div>
      <div style="font-size:34px; font-weight:900; color:#FFF; margin-top:18px;">AUTOGEN</div>
      <div style="font-size:18px; color:#94A3B8; font-weight:700; margin-top:4px;">Microsoft Research</div>
      <div style="margin-top:24px; font-size:21px; color:#E2E8F0; line-height:1.45;">
        Mạnh về đối thoại đa chiều giữa các Agent và tự sinh code thực thi trong Docker.
      </div>
      <div style="margin-top:auto; width:100%; background:#1E293B; padding:14px; border-radius:14px; font-weight:900; font-size:24px; color:#E2E8F0;">★ 42,000+ STARS</div>
    </div>

    <!-- Center Tallest Podium #1: LangGraph + MCP (Trophy Gold) -->
    <div style="position:absolute; bottom:48px; left:386px; width:308px; height:710px; background:linear-gradient(180deg, #78350F 0%, #1C1917 100%); border:4px solid #F59E0B; border-radius:32px 32px 12px 12px; padding:32px 24px; display:flex; flex-direction:column; align-items:center; text-align:center; box-shadow:0 0 60px rgba(245,158,11,0.38); z-index:10;">
      <div style="background:#F59E0B; color:#050811; font-weight:900; font-size:18px; padding:6px 18px; border-radius:999px; margin-bottom:12px;">👑 QUÁN QUÂN THỰC CHIẾN</div>
      <div style="width:92px; height:92px; border-radius:50%; background:linear-gradient(135deg, #FDE047, #F59E0B); color:#050811; font-weight:900; font-size:48px; display:flex; align-items:center; justify-content:center;">#1</div>
      <div style="font-size:38px; font-weight:900; color:#FDE047; margin-top:18px;">SUBAGENT<br>+ MCP</div>
      <div style="font-size:19px; color:#FDE68A; font-weight:700; margin-top:6px;">Kiến trúc DAG &amp; Hard Gate</div>
      <div style="margin-top:24px; font-size:22px; color:#FFFBEB; line-height:1.45;">
        Kiểm soát 100% trạng thái qua SQLite/Git, phân tầng Model tiết kiệm 90% token, không vòng lặp vô hạn!
      </div>
      <div style="margin-top:auto; width:100%; background:#F59E0B; padding:16px; border-radius:16px; font-weight:900; font-size:25px; color:#050811;">CHUẨN PRODUCTION</div>
    </div>

    <!-- Right Podium #3: CrewAI (Electric Blue) -->
    <div style="position:absolute; bottom:48px; right:64px; width:292px; height:495px; background:linear-gradient(180deg, #1E3A8A 0%, #091326 100%); border:3px solid #3B82F6; border-radius:28px 28px 12px 12px; padding:28px 24px; display:flex; flex-direction:column; align-items:center; text-align:center;">
      <div style="width:74px; height:74px; border-radius:50%; background:#3B82F6; color:#FFFFFF; font-weight:900; font-size:38px; display:flex; align-items:center; justify-content:center;">#3</div>
      <div style="font-size:34px; font-weight:900; color:#FFF; margin-top:18px;">CREW AI</div>
      <div style="font-size:18px; color:#93C5FD; font-weight:700; margin-top:4px;">Role-Playing Agents</div>
      <div style="margin-top:20px; font-size:21px; color:#DBEAFE; line-height:1.45;">
        Cấu hình YAML đơn giản, rất hợp làm mẫu thử nghiệm nhanh cho người mới bắt đầu.
      </div>
      <div style="margin-top:auto; width:100%; background:#1D4ED8; padding:14px; border-radius:14px; font-weight:900; font-size:24px; color:#FFFFFF;">★ 28,000+ STARS</div>
    </div>
    </body></html>"""


def card_12_weekend_autopilot_split() -> str:
    """Card 12: Top/Bottom Day-Night Split + Central 24/7 Autopilot Core (Theme: Neon Green #22C55E & Sunset Coral #FF5E7E)"""
    bg = """
    background: #06090F;
    """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    {_common_reset_css(bg)}
    </style></head><body>
    <!-- Top Half: Human Weekend Freedom (Warm Sunset Coral/Amber) -->
    <div style="position:absolute; top:0; left:0; right:0; height:530px; background:linear-gradient(135deg, #2A0B18 0%, #160A1E 100%); border-bottom:4px solid #22C55E; padding:48px 64px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="background:#FF5E7E; color:#FFF; font-weight:900; font-size:20px; padding:8px 22px; border-radius:999px;">☕ CHẾ ĐỘ CUỐI TUẦN CỦA CEO</span>
        <span style="font-size:22px; font-weight:800; color:#FDA4AF;">0% QUẤY RẦY MÀN HÌNH</span>
      </div>
      <div style="font-size:56px; font-weight:900; color:#FFFFFF; margin-top:26px; line-height:1.1;">
        BẠN THẢNH THƠI NGHỈ NGƠI,<br><span style="color:#FF5E7E;">HỆ THỐNG VẪN CHẠY 100%!</span>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:24px; margin-top:32px;">
        <div style="background:rgba(255,94,126,0.14); border:2px solid #FF5E7E; border-radius:20px; padding:20px 26px;">
          <div style="font-size:26px; font-weight:900; color:#FFF;">Không bật cửa sổ vướng mắt</div>
          <div style="font-size:19px; color:#FECDD3; margin-top:6px;">Toàn bộ trình duyệt Bot chạy ngầm --headless=new</div>
        </div>
        <div style="background:rgba(255,94,126,0.14); border:2px solid #FF5E7E; border-radius:20px; padding:20px 26px;">
          <div style="font-size:26px; font-weight:900; color:#FFF;">Chỉ nhận báo cáo Telegram</div>
          <div style="font-size:19px; color:#FECDD3; margin-top:6px;">Kiểm tra kết quả 4 kênh ngay trên điện thoại</div>
        </div>
      </div>
    </div>

    <!-- Center 24/7 Autopilot Core Badge -->
    <div style="position:absolute; top:482px; left:360px; width:360px; height:96px; background:#22C55E; color:#041309; border:6px solid #06090F; border-radius:999px; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:30px; z-index:20; box-shadow:0 0 45px rgba(34,197,94,0.6);">
      ⚡ AUTOPILOT 24/7 ON
    </div>

    <!-- Bottom Half: Green Autonomous Engine -->
    <div style="position:absolute; top:530px; left:0; right:0; bottom:0; background:linear-gradient(180deg, #041A10 0%, #030B08 100%); padding:82px 64px 48px 64px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:22px;">
        <div style="background:#072919; border:2.5px solid #22C55E; border-radius:22px; padding:24px;">
          <div style="color:#4ADE80; font-weight:900; font-size:18px;">CA SÁNG • TRƯA • TỐI</div>
          <div style="font-size:32px; font-weight:900; color:#FFF; margin-top:8px;">9 Bài AI + 6 Bài Sales</div>
          <div style="font-size:18px; color:#A7F3D0; margin-top:8px;">Tự động xuất bản &amp; ghim link bình luận đầu tiên</div>
        </div>
        <div style="background:#072919; border:2.5px solid #22C55E; border-radius:22px; padding:24px;">
          <div style="color:#4ADE80; font-weight:900; font-size:18px;">12:00 • 17:30 • 20:30</div>
          <div style="font-size:32px; font-weight:900; color:#FFF; margin-top:8px;">3 Ca Đi Tương Tác</div>
          <div style="font-size:18px; color:#A7F3D0; margin-top:8px;">Chạy ngầm 100%, tương tác xong tự đóng trình duyệt</div>
        </div>
        <div style="background:#072919; border:2.5px solid #22C55E; border-radius:22px; padding:24px;">
          <div style="color:#4ADE80; font-weight:900; font-size:18px;">ĐỒNG BỘ 2 MÁY</div>
          <div style="font-size:32px; font-weight:900; color:#FFF; margin-top:8px;">State Sync Git</div>
          <div style="font-size:18px; color:#A7F3D0; margin-top:8px;">Thứ Hai mở máy công ty tiếp tục ngay 100%</div>
        </div>
      </div>

      <div style="background:#0A3622; border:2px solid #4ADE80; border-radius:18px; padding:18px 30px; display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:24px; font-weight:800; color:#ECFDF5;">🎁 Muốn dựng hệ thống Subagent tự hành như vậy?</span>
        <span style="background:#22C55E; color:#041309; font-weight:900; font-size:22px; padding:10px 24px; border-radius:12px;">XEM BÌNH LUẬN ĐẦU TIÊN 👇</span>
      </div>
    </div>
    </body></html>"""


CARDS_SPEC = [
    {
        "code": "day5_img1_0830_compuse",
        "slot_dt": "2026-10-30 08:30",
        "live_now": True,
        "builder": card_01_computer_use_os_window,
        "cta_kw": "COMPUSE",
        "caption": (
            "🖱️ KHI AI BIẾT CẦM CHUỘT VÀ GÕ PHÍM NHƯ MỘT NHÂN VIÊN THỰC THỤ!\n\n"
            "Không chỉ dừng ở việc chat văn bản, công nghệ Computer Use cho phép AI tự chụp ảnh màn hình, tính toán tọa độ X-Y, tự di chuyển con trỏ chuột và điền biểu mẫu trên mọi phần mềm máy tính.\n\n"
            "👇 Bình luận 'COMPUSE' hoặc bấm vào link Nhóm Cộng Đồng ở bình luận đầu tiên để nhận tài liệu tích hợp thực chiến!"
        ),
    },
    {
        "code": "day5_img2_1015_codevsno",
        "slot_dt": "2026-10-30 10:15",
        "live_now": True,
        "builder": card_02_code_vs_nocode_split,
        "cta_kw": "HYBRID",
        "caption": (
            "⚖️ NÊN VIẾT CODE THUẦN (PYTHON) HAY DÙNG NỀN TẢNG NO-CODE (n8n / MAKE) ĐỂ TỰ ĐỘNG HÓA?\n\n"
            "Câu trả lời thực chiến nhất không phải là chọn 1 bỏ 1, mà là kiến trúc Hybrid:\n"
            "- Dùng n8n để bắt Webhook và kết nối nhanh các dịch vụ bên ngoài.\n"
            "- Dùng Python thuần cho các tác vụ xử lý lõi AI, kiểm duyệt Gate và kết xuất đồ họa 0đ chi phí thuê bao.\n\n"
            "👇 Lấy trọn bộ sơ đồ kết nối n8n + Python tại bình luận đầu tiên nhé!"
        ),
    },
    {
        "code": "day5_img3_1330_syncsys",
        "slot_dt": "2026-10-30 13:30",
        "live_now": False,
        "builder": card_03_git_state_sync_radar,
        "cta_kw": "SYNCSYS",
        "caption": (
            "🔄 LÀM SAO ĐỂ TIẾP TỤC DỰ ÁN AI TRÊN MÁY TÍNH KHÁC MÀ KHÔNG BỊ LỆCH TRẠNG THÁI?\n\n"
            "Đang làm việc trên máy công ty, tối về mở máy ở nhà làm tiếp — nhờ cơ chế Agent-State-Sync, toàn bộ lịch sử công việc, bộ nhớ quy tắc và phiên đăng nhập được đồng bộ tự động trong 3 giây mà không cần đẩy file video nặng.\n\n"
            "👇 Nhận script đồng bộ 2 máy tự động ở bình luận đầu tiên bên dưới!"
        ),
    },
    {
        "code": "day5_img4_1515_jsonprompt",
        "slot_dt": "2026-10-30 15:15",
        "live_now": False,
        "builder": card_04_json_schema_funnel,
        "cta_kw": "JSON100",
        "caption": (
            "📋 CÁCH KHÓA CỨNG ĐẦU RA AI ĐÚNG ĐỊNH DẠNG JSON SCHEMA 100% KHÔNG BAO GIỜ VỠ CODE!\n\n"
            "Khi nối AI vào hệ thống tự động hóa, chỉ cần AI trả thừa một câu chào hỏi là hàm parse JSON sẽ báo lỗi ngay. Hãy áp dụng cổng Structured Outputs / Pydantic Schema để đạt độ chính xác 100%.\n\n"
            "👇 Xem bộ 15 JSON Schema mẫu tại bình luận đầu tiên nhé!"
        ),
    },
    {
        "code": "day5_img5_1815_bonaothu2",
        "slot_dt": "2026-10-30 18:15",
        "live_now": False,
        "builder": card_05_second_brain_constellation,
        "cta_kw": "BONAO2",
        "caption": (
            "🧠 XÂY DỰNG 'BỘ NÃO THỨ 2' ĐỂ ĐỘI NGŨ SUBAGENT CÀNG LÀM VIỆC CÀNG THÔNG MINH!\n\n"
            "Mỗi khi bạn chỉnh sửa một quy chuẩn thiết kế hay một bài học thực chiến, Subagent Bộ Não Thứ 2 sẽ đóng gói thành ký ức chuẩn hóa có gắn thẻ để toàn bộ đội ngũ tự động tra cứu trước mỗi ca làm việc.\n\n"
            "👇 Tải cấu trúc thư mục Bộ Não Thứ 2 ở bình luận đầu tiên!"
        ),
    },
    {
        "code": "day5_img6_2115_4chiso",
        "slot_dt": "2026-10-30 21:15",
        "live_now": False,
        "builder": card_06_four_kpi_speedometers,
        "cta_kw": "4KPI",
        "caption": (
            "📈 ĐỪNG CHỈ NHÌN VÀO LƯỢT VIEW ẢO: 4 CHỈ SỐ THỰC TẾ QUYẾT ĐỊNH DOANH SỐ CỦA BẠN!\n\n"
            "Một hệ thống kênh AI hiệu quả không đo bằng cảm tính mà bằng 4 đồng hồ: Hook 3s (>65%), CTR Bình luận ghim (>10%), Tỷ lệ vào phễu cộng đồng và ROAS lợi nhuận ròng.\n\n"
            "👇 Nhận bảng tính theo dõi 4 chỉ số tự động tại bình luận đầu tiên!"
        ),
    },
    {
        "code": "day6_img1_0830_fasthtml",
        "slot_dt": "2026-10-31 08:30",
        "live_now": False,
        "builder": card_07_fasthtml_left_pillar_staircase,
        "cta_kw": "FASTHTML",
        "caption": (
            "🚀 FASTHTML: XÂY DỰNG WEB APP CHO AI BẰNG 100% PYTHON THUẦN!\n\n"
            "Nếu bạn là kỹ sư Python hoặc làm tự động hóa AI và ngại dựng giao diện bằng React/Webpack cồng kềnh, FastHTML kết hợp HTMX giúp bạn tạo Web Dashboard thời gian thực chỉ với chưa đầy 60 dòng code Python.\n\n"
            "👇 Nhận source code mẫu tại bình luận đầu tiên nhé!"
        ),
    },
    {
        "code": "day6_img2_1015_roiai",
        "slot_dt": "2026-10-31 10:15",
        "live_now": False,
        "builder": card_08_subagent_roi_waterfall,
        "cta_kw": "ROIAI",
        "caption": (
            "📊 BÀI TOÁN KINH TẾ: TẠI SAO TỰ ĐỘNG HÓA BẰNG ĐỘI NGŨ SUBAGENT LẠI CÓ ROI VƯỢT TRỘI?\n\n"
            "Khi tách quy trình thành 10 Subagent chuyên biệt và phân tầng model hợp lý (chỉ dùng model lớn cho khâu sáng tạo/duyệt Gate, dùng model Flash cho khâu hậu cần), chi phí vận hành giảm tới 92% trong khi tốc độ tăng gấp 6 lần.\n\n"
            "👇 Xem bản phân tích chi phí chi tiết ở bình luận đầu tiên!"
        ),
    },
    {
        "code": "day6_img3_1330_cleanup7d",
        "slot_dt": "2026-10-31 13:30",
        "live_now": False,
        "builder": card_09_cleanup_storage_ring,
        "cta_kw": "CLEAN7D",
        "caption": (
            "🧹 CÁCH GIỮ HỆ THỐNG AI LUÔN CHẠY NHANH NHƯ MỚI VỚI GIAO THỨC TỰ DỌN RÁC!\n\n"
            "Khi vận hành render video và tương tác tự động mỗi ngày, việc tự động xóa bỏ tư liệu cũ lỗi thời, đóng trình duyệt chạy ngầm ngay sau ca và dọn bộ nhớ đệm giúp máy luôn nhẹ nhàng ở mức 2-5% CPU.\n\n"
            "👇 Tải script dọn dẹp tự động ở bình luận đầu tiên!"
        ),
    },
    {
        "code": "day6_img4_1515_promptmkt",
        "slot_dt": "2026-10-31 15:15",
        "live_now": False,
        "builder": card_10_voc_comment_mining_strata,
        "cta_kw": "VOCMINE",
        "caption": (
            "🎯 ĐÀO BỚI HÀNG NGHÌN BÌNH LUẬN ĐỂ TÌM Ý TƯỞNG VIDEO BẰNG KỸ THUẬT VOC MINING!\n\n"
            "Đừng ngồi đoán mò khách hàng thích gì. Hãy dùng AI quét bình luận trên các bài viết cùng ngách, lọc ra đúng những câu hỏi lặp đi lặp lại nhiều nhất và biến chúng thành câu Hook 3 giây đầu tiên.\n\n"
            "👇 Lấy bộ Prompt đào Insight khách hàng tại bình luận đầu tiên!"
        ),
    },
    {
        "code": "day6_img5_1815_top10agents",
        "slot_dt": "2026-10-31 18:15",
        "live_now": False,
        "builder": card_11_github_multiagent_podium,
        "cta_kw": "TOPAGENT",
        "caption": (
            "🏆 BẢNG XẾP HẠNG CÁC KIẾN TRÚC MULTI-AGENT ĐÁNG DÙNG NHẤT NĂM 2026!\n\n"
            "Từ CrewAI dễ làm quen, AutoGen mạnh về hội thoại đa chiều, cho tới kiến trúc Subagent + MCP có cổng kiểm soát chất lượng (Hard Gate) chặt chẽ — đâu là lựa chọn phù hợp nhất cho hệ thống của bạn?\n\n"
            "👇 Xem bảng đối sánh chi tiết tại bình luận đầu tiên nhé!"
        ),
    },
    {
        "code": "day6_img6_2115_cuoituan",
        "slot_dt": "2026-10-31 21:15",
        "live_now": False,
        "builder": card_12_weekend_autopilot_split,
        "cta_kw": "AUTOPILOT",
        "caption": (
            "☕ CUỐI TUẦN NÀY BẠN CÓ ĐANG ĐƯỢC THẢNH THƠI NGHỈ NGƠI KHÔNG?\n\n"
            "Giá trị lớn nhất của việc xây dựng hệ thống Subagent tự hành chạy ngầm 100% là trả lại thời gian cho chính bạn: Không có cửa sổ trình duyệt bật lên làm phiền, mọi lịch đăng và tương tác đều tự vận hành và gửi báo cáo gọn gàng về Telegram.\n\n"
            "👇 Tham gia cộng đồng thực chiến tại bình luận đầu tiên!"
        ),
    },
]


def build_qa_grid(image_paths: list[Path], out_grid: Path) -> None:
    from PIL import Image
    cols, rows = 4, 3
    cell = 360
    canvas = Image.new("RGB", (cols * cell, rows * cell), (10, 12, 16))
    for idx, p in enumerate(image_paths[:12]):
        with Image.open(p) as im:
            thumb = im.convert("RGB").resize((cell - 8, cell - 8), Image.Resampling.LANCZOS)
            x = (idx % cols) * cell + 4
            y = (idx // cols) * cell + 4
            canvas.paste(thumb, (x, y))
    canvas.save(out_grid, format="JPEG", quality=92, optimize=True)


def publish_and_schedule_12_cards(manifest_items: list[dict]) -> list[dict]:
    import requests
    from mama_auto_scheduler_engine import load_vault, graph_post
    from zero_repost_gate import record_published_content

    pages = load_vault()
    ai_obj = pages[AI_PAGE_ID]
    tok = ai_obj["access_token"]

    for item in manifest_items:
        img_path = Path(item["image_path"])
        dt_obj = dt.datetime.strptime(item["slot_dt"], "%Y-%m-%d %H:%M").replace(tzinfo=VN_TZ)
        sched_ts = 0 if item.get("live_now") else int(dt_obj.timestamp())
        pinned_msg = (
            f"🎁 [TÀI LIỆU & MÃ NGUỒN MIỄN PHÍ — MÃ: {item['cta_kw']}]\n"
            f"👉 Tham gia ngay Nhóm Zalo Cộng Đồng VIP \"AI Players — Thực Chiến Subagent\" để tải trọn bộ Sơ đồ Kiến trúc, File .MD & Bộ 30 Quà tặng đóng hộp:\n"
            f"🔗 Link vào nhóm ngay: {ZALO_URL} (Mã duyệt tự động: AIPLAYERS2026)"
        )
        data = {"caption": item["caption"], "access_token": tok}
        if sched_ts > 0:
            data["published"] = "false"
            data["scheduled_publish_time"] = str(sched_ts)
        else:
            data["published"] = "true"

        with open(img_path, "rb") as f:
            r = requests.post(
                f"https://graph.facebook.com/v22.0/{AI_PAGE_ID}/photos",
                data=data,
                files={"source": (img_path.name, f, "image/jpeg")},
                timeout=90,
            )
        res = r.json()
        post_id = res.get("post_id") or res.get("id", "")
        cmt_id = ""
        if post_id:
            record_published_content(
                page_id=AI_PAGE_ID,
                media_path=img_path,
                caption=item["caption"],
                post_id=str(post_id),
            )
            c_res = graph_post(f"{post_id}/comments", tok, {"message": pinned_msg})
            cmt_id = c_res.get("id", "")
            item["status"] = "LIVE_PUBLISHED" if sched_ts == 0 else "SCHEDULED"
            item["post_id"] = post_id
            item["comment_id"] = cmt_id
            print(f"✅ [{item['code']}] {item['status']} ({item['slot_dt']}) -> post_id={post_id} | cmt_id={cmt_id}", flush=True)
        else:
            item["status"] = "ERROR"
            item["error"] = res
            print(f"❌ [{item['code']}] Lỗi: {res}", flush=True)
        time.sleep(1.2)
    return manifest_items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true", help="Đăng 2 bài sáng nay & hẹn giờ 10 bài tiếp theo lên Page AI Players")
    args = parser.parse_args()

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    rendered_paths = []
    manifest_items = []

    print("🎨 Đang kết xuất 12 Ảnh Bài Đăng Độc Bản 100% (Zero-Clone Bespoke Designs)...")
    for idx, spec in enumerate(CARDS_SPEC, 1):
        out_jpg = IMAGES_DIR / f"{spec['code']}.jpg"
        html = spec["builder"]()
        render_html_to_image(html, out_jpg, width=1080, height=1080)
        rendered_paths.append(out_jpg)
        manifest_items.append({
            "index": idx,
            "code": spec["code"],
            "slot_dt": spec["slot_dt"],
            "live_now": spec["live_now"],
            "cta_kw": spec["cta_kw"],
            "image_path": str(out_jpg),
            "caption": spec["caption"],
        })
        print(f"  ✔ [{idx:02d}/12] Đã render thiết kế độc bản: {out_jpg.name}", flush=True)

    # Kiểm định qua Cổng Khóa Cứng Zero-Clone Image Gate
    ok, gate_msg = verify_zero_clone_images(IMAGES_DIR, max_similarity=0.58)
    print(("🛡️ " if ok else "🛑 ") + gate_msg, flush=True)
    if not ok:
        sys.exit(1)

    build_qa_grid(rendered_paths, QA_GRID_PATH)
    print(f"🖼️ Đã tạo bảng QA Grid 12 thiết kế độc bản tại: {QA_GRID_PATH}", flush=True)

    if args.publish:
        manifest_items = publish_and_schedule_12_cards(manifest_items)

    MANIFEST_PATH.write_text(json.dumps(manifest_items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📄 Đã lưu Manifest tại: {MANIFEST_PATH}", flush=True)


if __name__ == "__main__":
    main()
