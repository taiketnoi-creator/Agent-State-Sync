#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_bespoke_ai_players_day7_day8.py — Bộ Kết Xuất 12 Ảnh Độc Bản Tiếp Theo (Card 13..24: Ngày 01/11 & 02/11)
Cho Fanpage "AI Players - Người chơi hệ AI" (1022527194267367)
==============================================================================================================
- Tuân thủ tuyệt đối LUẬT #1 (Zero-Clone Bespoke Image Design):
  1 Bài Ảnh = 1 Kiến Trúc Bố Cục Không Gian + 1 Bảng Màu Nhấn & Ánh Sáng Nền + 1 Đồ Họa SVG Độc Bản.
- Kiểm định toàn bộ 24 ảnh (Card 01..24) qua cổng `verify_zero_clone_images()` (< 58% tương đồng).
"""

import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SUBAGENT_DIR / "tools"))

from render_vid_style_card import get_local_fonts_css, render_html_to_image
from zero_repost_gate import verify_zero_clone_images, record_published_content

AI_PAGE_ID = "1022527194267367"
ZALO_URL = "https://zalo.me/g/fzxvbf259"
VN_TZ = dt.timezone(dt.timedelta(hours=7))

OUT_ROOT = SUBAGENT_DIR / "campaigns" / "2026-10-26" / "ai-players-weekly-vault"
IMAGES_DIR = OUT_ROOT / "images"
QA_GRID_D78_PATH = OUT_ROOT / "bespoke_day7_day8_qa_grid.jpg"
MANIFEST_D78_PATH = OUT_ROOT / "bespoke_day7_day8_manifest.json"


def _reset_css(bg_css: str) -> str:
    font_css = get_local_fonts_css()
    return f"""
    {font_css}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      width: 1080px; height: 1080px; overflow: hidden;
      font-family: 'Be Vietnam Pro', 'Plus Jakarta Sans', sans-serif;
      color: #FFFFFF; position: relative;
      {bg_css}
    }}
    """


def card_13_tele_remote_phone() -> str:
    """Card 13: Left Smartphone Frame + Right 3 Command Beams (Theme: Electric Rose #F43F5E & Deep Obsidian #0D0612)"""
    bg = "background: radial-gradient(circle at 22% 55%, rgba(244,63,94,0.22) 0%, transparent 55%), #09050D;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:42px; left:54px; right:54px;">
      <div style="display:inline-block; background:#F43F5E; color:#FFF; font-weight:900; font-size:18px; padding:7px 20px; border-radius:999px;">📱 TELEGRAM 2-WAY BRIDGE</div>
      <div style="font-size:48px; font-weight:900; margin-top:12px; line-height:1.08;">ĐIỀU KHIỂN CẢ ĐỘI SUBAGENT <span style="color:#FB7185;">TRÊN ĐIỆN THOẠI</span></div>
    </div>

    <!-- Left Smartphone Mockup -->
    <div style="position:absolute; top:210px; left:54px; width:390px; bottom:52px; background:#140B1D; border:5px solid #F43F5E; border-radius:44px; padding:26px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 24px 60px rgba(0,0,0,0.85);">
      <div style="width:120px; height:12px; background:#2E1A3E; border-radius:999px; margin:0 auto;"></div>
      <div style="background:#1F112B; border:2px solid #FB7185; border-radius:20px; padding:18px;">
        <div style="font-size:15px; color:#FDA4AF; font-weight:800;">👤 CEO NHẮN TELEGRAM:</div>
        <div style="font-size:21px; font-weight:800; color:#FFF; margin-top:6px;">"Báo cáo kết quả 4 Page và nạp lịch ảnh cuối tuần"</div>
      </div>
      <div style="background:#F43F5E; color:#FFF; border-radius:20px; padding:18px;">
        <div style="font-size:15px; color:#FFE4E6; font-weight:800;">🤖 MAMA PHẢN HỒI (7 DÒNG):</div>
        <div style="font-size:19px; font-weight:800; margin-top:6px; line-height:1.35;">📊 Đã lên lịch 9 bài Sales + 12 bài AI độc bản!<br>✅ 100% Pinned Comment #1</div>
      </div>
      <div style="background:#09050D; border:2px solid #F43F5E; border-radius:16px; padding:14px; text-align:center; font-weight:900; font-size:20px; color:#FB7185;">0 TOKEN LỆNH NHANH /STATUS</div>
    </div>

    <!-- Right 3 Action Modules -->
    <div style="position:absolute; top:210px; right:54px; width:535px; bottom:52px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="background:#170D22; border-left:8px solid #F43F5E; border-radius:22px; padding:26px 30px;">
        <div style="color:#FB7185; font-weight:900; font-size:20px;">TẦNG 01 // LỆNH NHANH 0-TOKEN (1 GIÂY)</div>
        <div style="font-size:28px; font-weight:900; color:#FFF; margin-top:8px;">Gõ /status, /pages, /sync</div>
        <div style="font-size:19px; color:#E2E8F0; margin-top:6px;">Phản hồi tức thì bằng Python thuần, không tốn 1 token LLM.</div>
      </div>
      <div style="background:#170D22; border-left:8px solid #FB7185; border-radius:22px; padding:26px 30px;">
        <div style="color:#FB7185; font-weight:900; font-size:20px;">TẦNG 02 // REACTIVE WAKEUP TỰ ĐỘNG</div>
        <div style="font-size:28px; font-weight:900; color:#FFF; margin-top:8px;">Đánh thức Mama ngay khi có tin nhắn</div>
        <div style="font-size:19px; color:#E2E8F0; margin-top:6px;">Không cần mở màn hình máy tính, tự phân việc cho 9 Subagent.</div>
      </div>
      <div style="background:#170D22; border-left:8px solid #F43F5E; border-radius:22px; padding:26px 30px;">
        <div style="color:#FB7185; font-weight:900; font-size:20px;">TẦNG 03 // BÁO CÁO NGẮN GỌN 4–8 DÒNG</div>
        <div style="font-size:28px; font-weight:900; color:#FFF; margin-top:8px;">Đi thẳng vào số liệu thực tế</div>
        <div style="font-size:19px; color:#E2E8F0; margin-top:6px;">Loại bỏ hoàn toàn bảng kẻ ngang vỡ khung trên điện thoại.</div>
      </div>
    </div>
    </body></html>"""


def card_14_ten_agents_roundtable() -> str:
    """Card 14: Central Mama Core + 8 Surrounding Specialist Pods (Theme: Cyan #06B6D4 & Gold #FBBF24)"""
    bg = "background: radial-gradient(circle at 50% 54%, rgba(6,182,212,0.22) 0%, transparent 60%), #041017;"
    pods = [
        ("MKT", "Săn SKU <300k", 80, 210),
        ("CONTENT", "Kịch bản 30s", 740, 210),
        ("EDIT", "Zero-Clone UI", 40, 445),
        ("VOICE", "Vbee -3dB", 780, 445),
        ("ĐA KÊNH", "Copy 4 nền tảng", 60, 680),
        ("QUẢN LÝ", "Lịch Meta API", 760, 680),
        ("CHĂM SÓC", "Pinned Cmt #1", 210, 880),
        ("HIỆU SUẤT", "Đo phễu & ROI", 610, 880),
    ]
    pods_html = ""
    for name, desc, lx, ty in pods:
        pods_html += f"""
        <div style="position:absolute; left:{lx}px; top:{ty}px; width:260px; background:#082230; border:2.5px solid #06B6D4; border-radius:20px; padding:16px 20px; text-align:center; box-shadow:0 12px 30px rgba(0,0,0,0.7);">
          <div style="font-size:22px; font-weight:900; color:#22D3EE;">{name}</div>
          <div style="font-size:17px; font-weight:700; color:#E0F2FE; margin-top:4px;">{desc}</div>
        </div>
        """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:54px; right:54px; text-align:center;">
      <div style="color:#FBBF24; font-weight:900; font-size:20px; letter-spacing:1.5px;">⚡ KIẾN TRÚC MULTI-AGENT CHUYÊN MÔN HÓA</div>
      <div style="font-size:48px; font-weight:900; margin-top:8px;">TẠI SAO <span style="color:#22D3EE;">10 SUBAGENT RIÊNG BIỆT</span> THẮNG 1 SIÊU PROMPT?</div>
    </div>
    <svg width="1080" height="1080" style="position:absolute; inset:0;">
      <circle cx="540" cy="555" r="285" stroke="rgba(34,211,238,0.3)" stroke-width="3" stroke-dasharray="12 8" fill="none"/>
      <circle cx="540" cy="555" r="175" stroke="rgba(251,191,36,0.45)" stroke-width="2.5" fill="none"/>
    </svg>
    {pods_html}
    <div style="position:absolute; left:395px; top:410px; width:290px; height:290px; border-radius:50%; background:linear-gradient(135deg, #FBBF24 0%, #D97706 100%); border:6px solid #FFF; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#041017; text-align:center; box-shadow:0 0 60px rgba(251,191,36,0.5);">
      <div style="font-size:20px; font-weight:900;">CHỈ HUY TRƯỞNG</div>
      <div style="font-size:46px; font-weight:900; line-height:1.05; margin-top:4px;">MAMA</div>
      <div style="font-size:17px; font-weight:800; margin-top:8px; background:#041017; color:#FBBF24; padding:6px 16px; border-radius:999px;">HARD GATE ≥ 9.0</div>
    </div>
    </body></html>"""


def card_15_one_piece_multi_platform() -> str:
    """Card 15: Top Source Gem Splitting Into 4 Vertical Channel Columns (Theme: Violet #8B5CF6 & Lime #A3E635)"""
    bg = "background: linear-gradient(180deg, #0E0720 0%, #070410 100%);"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:42px; left:48px; right:48px; text-align:center;">
      <div style="font-size:40px; font-weight:900;">NGUYÊN TẮC <span style="color:#A3E635;">1 MASTER ASSET</span> → <span style="color:#C4B5FD;">4 KÊNH TỰ ĐỘNG</span></div>
    </div>

    <!-- Top Master Source Box -->
    <div style="position:absolute; top:128px; left:240px; width:600px; height:155px; background:linear-gradient(90deg, #6D28D9, #4C1D95); border:3px solid #A3E635; border-radius:26px; display:flex; flex-direction:column; align-items:center; justify-content:center; box-shadow:0 18px 45px rgba(109,40,217,0.45);">
      <div style="color:#A3E635; font-weight:900; font-size:19px;">💎 CONTENT MASTER ĐÃ DUYỆT GATE</div>
      <div style="font-size:32px; font-weight:900; color:#FFF; margin-top:6px;">1 Kịch Bản + 1 Bộ Đồ Họa Gốc</div>
    </div>

    <!-- 4 Vertical Channel Pillars -->
    <div style="position:absolute; top:355px; left:48px; right:48px; bottom:54px; display:grid; grid-template-columns:repeat(4, 1fr); gap:20px;">
      <div style="background:#160D2E; border:3px solid #38BDF8; border-radius:26px; padding:26px 20px; display:flex; flex-direction:column; justify-content:space-between;">
        <div style="background:#38BDF8; color:#070410; font-weight:900; font-size:20px; padding:8px; border-radius:12px; text-align:center;">FB REELS</div>
        <div style="font-size:22px; font-weight:800; line-height:1.4;">Không chèn link ở Caption. Dẫn 100% khách xuống Bình luận ghim #1.</div>
        <div style="font-size:28px; font-weight:900; color:#38BDF8; text-align:center;">9:16 DỌC</div>
      </div>
      <div style="background:#160D2E; border:3px solid #F43F5E; border-radius:26px; padding:26px 20px; display:flex; flex-direction:column; justify-content:space-between;">
        <div style="background:#F43F5E; color:#FFF; font-weight:900; font-size:20px; padding:8px; border-radius:12px; text-align:center;">YT SHORTS</div>
        <div style="font-size:22px; font-weight:800; line-height:1.4;">Tiêu đề &lt; 60 ký tự chứa từ khóa tìm kiếm + đúng 3 Hashtag chuẩn.</div>
        <div style="font-size:28px; font-weight:900; color:#F43F5E; text-align:center;">SEO TOP</div>
      </div>
      <div style="background:#160D2E; border:3px solid #A3E635; border-radius:26px; padding:26px 20px; display:flex; flex-direction:column; justify-content:space-between;">
        <div style="background:#A3E635; color:#070410; font-weight:900; font-size:20px; padding:8px; border-radius:12px; text-align:center;">THREADS</div>
        <div style="font-size:22px; font-weight:800; line-height:1.4;">Mở đầu tranh luận sắc bén, thả link tài liệu ở Self-Reply #1.</div>
        <div style="font-size:28px; font-weight:900; color:#A3E635; text-align:center;">VIRAL TEXT</div>
      </div>
      <div style="background:#160D2E; border:3px solid #FBBF24; border-radius:26px; padding:26px 20px; display:flex; flex-direction:column; justify-content:space-between;">
        <div style="background:#FBBF24; color:#070410; font-weight:900; font-size:20px; padding:8px; border-radius:12px; text-align:center;">GROUP SEED</div>
        <div style="font-size:22px; font-weight:800; line-height:1.4;">Chia sẻ giá trị thật 0% spam link, kéo tò mò bấm về Fanpage.</div>
        <div style="font-size:28px; font-weight:900; color:#FBBF24; text-align:center;">3 CA / NGÀY</div>
      </div>
    </div>
    </body></html>"""


def card_16_env_server_rack() -> str:
    """Card 16: 4 Stacked Hardware Server Rack Blades With Status LEDs (Theme: Emerald #10B981 & Dark Slate #060B11)"""
    bg = "background: #060B11;"
    racks = [
        ("BLADE 01 // PYTHON 3.11 + PLAYWRIGHT CDP", "Điều khiển Chrome Bot ngầm --headless=new cổng 9222", "ONLINE", "#10B981"),
        ("BLADE 02 // REMOTION 4.0 + FFMPEG STUDIO", "Kết xuất Video 9:16 & Ảnh vuông 1:1 chuẩn 60FPS", "READY", "#38BDF8"),
        ("BLADE 03 // SQLITE WAL + ZERO-REPOST GATE", "Chặn trùng lặp bài đăng & kiểm định Zero-Clone <58%", "LOCKED", "#FACC15"),
        ("BLADE 04 // GITHUB AGENT-STATE-SYNC", "Đồng bộ tức thời bộ nhớ & Cookie giữa 2 máy tính", "SYNCED", "#A855F7"),
    ]
    rack_html = ""
    for title, desc, badge, col in racks:
        rack_html += f"""
        <div style="background:#0D1622; border:3px solid {col}; border-radius:22px; padding:24px 32px; display:flex; align-items:center; justify-content:space-between; box-shadow:0 12px 30px rgba(0,0,0,0.7);">
          <div style="display:flex; align-items:center; gap:22px;">
            <div style="width:22px; height:64px; background:{col}; border-radius:6px; box-shadow:0 0 18px {col};"></div>
            <div>
              <div style="font-family:monospace; font-size:22px; font-weight:900; color:{col};">{title}</div>
              <div style="font-size:23px; font-weight:800; color:#FFF; margin-top:6px;">{desc}</div>
            </div>
          </div>
          <div style="background:#060B11; border:2px solid {col}; color:{col}; font-family:monospace; font-weight:900; font-size:20px; padding:10px 20px; border-radius:12px;">● {badge}</div>
        </div>
        """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:42px; left:56px; right:56px;">
      <div style="color:#10B981; font-family:monospace; font-weight:900; font-size:20px;">🖥️ LOCAL AI SERVER RACK ARCHITECTURE</div>
      <div style="font-size:48px; font-weight:900; margin-top:8px;">4 TẦNG HẠ TẦNG CHẠY <span style="color:#10B981;">AI AGENT TỰ HÀNH 24/7</span></div>
    </div>
    <div style="position:absolute; top:200px; left:56px; right:56px; bottom:54px; display:flex; flex-direction:column; justify-content:space-between;">
      {rack_html}
    </div>
    </body></html>"""


def card_17_weekly_equalizer_bars() -> str:
    """Card 17: 7 Vertical Equalizer Bars For Mon-Sun Schedule (Theme: Flame Orange #F97316 & Sky #38BDF8)"""
    bg = "background: linear-gradient(135deg, #130905 0%, #090D16 100%);"
    days = [("T2", 82), ("T3", 86), ("T4", 90), ("T5", 88), ("T6", 94), ("T7", 98), ("CN", 100)]
    bars_html = ""
    for d, pct in days:
        h = int(pct * 4.2)
        col = "#F97316" if d in ("T6", "T7", "CN") else "#38BDF8"
        bars_html += f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:flex-end; height:520px;">
          <div style="font-size:20px; font-weight:900; color:{col}; margin-bottom:10px;">15 BÀI</div>
          <div style="width:92px; height:{h}px; background:linear-gradient(180deg, {col} 0%, #1E293B 100%); border:3px solid {col}; border-radius:18px 18px 8px 8px;"></div>
          <div style="font-size:26px; font-weight:900; color:#FFF; margin-top:14px;">{d}</div>
        </div>
        """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:42px; left:56px; right:56px; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="color:#F97316; font-weight:900; font-size:20px;">📊 BÁO CÁO TỔNG KẾT VẬN HÀNH TUẦN</div>
        <div style="font-size:48px; font-weight:900; margin-top:6px;">DUY TRÌ KỶ LUẬT <span style="color:#F97316;">105 BÀI ĐĂNG / TUẦN</span></div>
      </div>
      <div style="background:#F97316; color:#090D16; font-weight:900; font-size:28px; padding:16px 26px; border-radius:20px;">100% TỰ ĐỘNG</div>
    </div>

    <div style="position:absolute; top:215px; left:56px; right:56px; height:580px; background:#0D131F; border:3px solid rgba(249,115,22,0.45); border-radius:30px; padding:30px 40px; display:flex; justify-content:space-between; align-items:flex-end;">
      {bars_html}
    </div>

    <div style="position:absolute; bottom:52px; left:56px; right:56px; display:grid; grid-template-columns:1fr 1fr 1fr; gap:22px;">
      <div style="background:#171F30; border-bottom:6px solid #F97316; border-radius:18px; padding:22px; text-align:center;">
        <div style="font-size:36px; font-weight:900; color:#F97316;">63 BÀI AI</div>
        <div style="font-size:18px; color:#CBD5E1; margin-top:4px;">42 Ảnh + 21 Video Reels</div>
      </div>
      <div style="background:#171F30; border-bottom:6px solid #38BDF8; border-radius:18px; padding:22px; text-align:center;">
        <div style="font-size:36px; font-weight:900; color:#38BDF8;">42 BÀI SALES</div>
        <div style="font-size:18px; color:#CBD5E1; margin-top:4px;">3 Page Bán Hàng 1:1</div>
      </div>
      <div style="background:#171F30; border-bottom:6px solid #22C55E; border-radius:18px; padding:22px; text-align:center;">
        <div style="font-size:36px; font-weight:900; color:#22C55E;">21 CA SEED</div>
        <div style="font-size:18px; color:#CBD5E1; margin-top:4px;">Tương tác hội nhóm ngầm</div>
      </div>
    </div>
    </body></html>"""


def card_18_bullseye_weekly_goals() -> str:
    """Card 18: Left Giant Concentric Bullseye Target + Right 3 Goal Cards (Theme: Crimson #EF4444 & Gold #FACC15)"""
    bg = "background: radial-gradient(circle at 30% 58%, rgba(239,68,68,0.24) 0%, transparent 55%), #0B0709;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:42px; left:56px; right:56px;">
      <div style="color:#FACC15; font-weight:900; font-size:20px;">🎯 CHIẾN LƯỢC TĂNG TRƯỞNG TUẦN MỚI</div>
      <div style="font-size:50px; font-weight:900; margin-top:6px;">3 MỤC TIÊU TRỌNG TÂM <span style="color:#EF4444;">Bứt Phá Chuyển Đổi</span></div>
    </div>

    <!-- Left Bullseye Target -->
    <div style="position:absolute; top:215px; left:48px; width:460px; height:790px; background:#160D11; border:3px solid #EF4444; border-radius:32px; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:24px;">
      <svg width="380" height="380" viewBox="0 0 360 360">
        <circle cx="180" cy="180" r="160" fill="#2A1215" stroke="#EF4444" stroke-width="6"/>
        <circle cx="180" cy="180" r="115" fill="#451A1E" stroke="#F87171" stroke-width="5"/>
        <circle cx="180" cy="180" r="70" fill="#EF4444" stroke="#FACC15" stroke-width="5"/>
        <circle cx="180" cy="180" r="28" fill="#FACC15"/>
      </svg>
      <div style="font-size:34px; font-weight:900; color:#FACC15; margin-top:26px;">100% ZERO-CLONE</div>
      <div style="font-size:20px; color:#FCA5A5; text-align:center; margin-top:8px;">Mỗi bài đăng là một thiết kế độc bản có điểm nhấn riêng biệt</div>
    </div>

    <!-- Right 3 Dart Cards -->
    <div style="position:absolute; top:215px; right:52px; width:490px; height:790px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="background:#1F1014; border:3px solid #FACC15; border-radius:26px; padding:28px;">
        <div style="color:#FACC15; font-weight:900; font-size:22px;">MŨI TÊN #1 // PHỄU CỘNG ĐỒNG</div>
        <div style="font-size:30px; font-weight:900; margin-top:8px;">Tặng Bộ 30 Quà Lead Magnet</div>
        <div style="font-size:19px; color:#FECACA; margin-top:8px;">Kéo khán giả từ Reels &amp; Bài ảnh vào thẳng Nhóm Zalo thực chiến.</div>
      </div>
      <div style="background:#1F1014; border:3px solid #EF4444; border-radius:26px; padding:28px;">
        <div style="color:#F87171; font-weight:900; font-size:22px;">MŨI TÊN #2 // CHỮ DÀY &amp; NỔI BẬT</div>
        <div style="font-size:30px; font-weight:900; margin-top:8px;">Nâng cấp Typography 3 Page Sales</div>
        <div style="font-size:19px; color:#FECACA; margin-top:8px;">Tăng tỷ lệ dừng ngón tay và bấm link Shopee ở Bình luận #1.</div>
      </div>
      <div style="background:#1F1014; border:3px solid #FACC15; border-radius:26px; padding:28px;">
        <div style="color:#FACC15; font-weight:900; font-size:22px;">MŨI TÊN #3 // TỰ ĐỘNG HÓA 2 MÁY</div>
        <div style="font-size:30px; font-weight:900; margin-top:8px;">Đồng bộ tức thời Công ty &amp; Nhà</div>
        <div style="font-size:19px; color:#FECACA; margin-top:8px;">Chạy ngầm 100%, báo cáo Telegram gói gọn 7 dòng súc tích.</div>
      </div>
    </div>
    </body></html>"""


def card_19_browser_use_dom_tree() -> str:
    """Card 19: Top-Down DOM Tree Nodes + Bottom Browser Action Bar (Theme: Royal Blue #3B82F6 & Cyber Yellow #FDE047)"""
    bg = "background: linear-gradient(160deg, #040B1A 0%, #0B1D3A 100%);"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:40px; left:56px; right:56px; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="color:#FDE047; font-weight:900; font-size:20px;">🌐 OPEN-SOURCE REPO: BROWSER-USE (55,000+ STARS)</div>
        <div style="font-size:48px; font-weight:900; margin-top:6px;">CÁCH AI ĐỌC <span style="color:#60A5FA;">CÂY DOM HTML</span> THAY VÌ ĐOÁN MÒ</div>
      </div>
    </div>

    <!-- Center DOM Tree Diagram -->
    <div style="position:absolute; top:195px; left:56px; right:56px; height:570px; background:#071226; border:3px solid #3B82F6; border-radius:30px; padding:34px; position:relative;">
      <div style="width:420px; margin:0 auto; background:#1D4ED8; border:3px solid #FDE047; border-radius:18px; padding:18px; text-align:center; font-family:monospace; font-size:26px; font-weight:900;">
        &lt;body role="application"&gt;
      </div>
      <svg width="900" height="110" style=" display:block; margin:0 auto;">
        <line x1="450" y1="0" x2="160" y2="100" stroke="#60A5FA" stroke-width="4"/>
        <line x1="450" y1="0" x2="450" y2="100" stroke="#FDE047" stroke-width="5"/>
        <line x1="450" y1="0" x2="740" y2="100" stroke="#60A5FA" stroke-width="4"/>
      </svg>
      <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:24px;">
        <div style="background:#0F2447; border:2.5px solid #60A5FA; border-radius:20px; padding:22px; text-align:center;">
          <div style="font-family:monospace; font-size:22px; color:#93C5FD; font-weight:900;">[Node #12]</div>
          <div style="font-size:24px; font-weight:900; margin-top:8px;">Ô Tìm Kiếm</div>
          <div style="font-size:17px; color:#CBD5E1; margin-top:6px;">input[type="search"]</div>
        </div>
        <div style="background:#1E3A8A; border:4px solid #FDE047; border-radius:20px; padding:22px; text-align:center; box-shadow:0 0 35px rgba(253,224,71,0.35);">
          <div style="font-family:monospace; font-size:22px; color:#FDE047; font-weight:900;">[Node #24 • LOCKED]</div>
          <div style="font-size:24px; font-weight:900; margin-top:8px;">Ô Bình Luận Fanpage</div>
          <div style="font-size:17px; color:#FEF08A; margin-top:6px;">aria-label*="dưới tên Page"</div>
        </div>
        <div style="background:#0F2447; border:2.5px solid #60A5FA; border-radius:20px; padding:22px; text-align:center;">
          <div style="font-family:monospace; font-size:22px; color:#93C5FD; font-weight:900;">[Node #39]</div>
          <div style="font-size:24px; font-weight:900; margin-top:8px;">Nút Chia Sẻ</div>
          <div style="font-size:17px; color:#CBD5E1; margin-top:6px;">div[role="button"]</div>
        </div>
      </div>
      <div style="margin-top:34px; background:#040B1A; border:2px solid #3B82F6; border-radius:16px; padding:18px 26px; display:flex; justify-content:space-between; align-items:center;">
        <span style="font-family:monospace; font-size:21px; color:#FDE047; font-weight:800;">&gt; Tốc độ trích xuất DOM: 120ms</span>
        <span style="background:#FDE047; color:#040B1A; font-weight:900; font-size:19px; padding:6px 18px; border-radius:8px;">CHÍNH XÁC 100%</span>
      </div>
    </div>

    <div style="position:absolute; bottom:52px; left:56px; right:56px; height:195px; background:linear-gradient(90deg, #FDE047 0%, #F59E0B 100%); border-radius:26px; padding:28px 40px; color:#040B1A; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-size:20px; font-weight:900;">🔥 ỨNG DỤNG THỰC TẾ TẠI AI PLAYERS:</div>
        <div style="font-size:34px; font-weight:900; margin-top:6px;">Tự động hóa trình duyệt ngầm không bao giờ bấm nhầm nút!</div>
      </div>
      <div style="background:#040B1A; color:#FDE047; font-weight:900; font-size:24px; padding:20px 28px; border-radius:18px; flex-shrink:0;">NHẬN CODE 👇</div>
    </div>
    </body></html>"""


def card_20_voice_audio_mastering() -> str:
    """Card 20: Dual Audio Waveform Tracks & dB VU Meter (Theme: Hot Pink #EC4899 & Cyan #2DD4BF)"""
    bg = "background: #08060C;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:42px; left:56px; right:56px;">
      <div style="color:#2DD4BF; font-weight:900; font-size:20px;">🎙️ STUDIO AUDIO MASTERING PIPELINE</div>
      <div style="font-size:48px; font-weight:900; margin-top:6px;">CÔNG THỨC ÂM THANH <span style="color:#EC4899;">GIỮ CHÂN KHÁN GIẢ REELS</span></div>
    </div>

    <!-- Track 1: Voiceover -3dB -->
    <div style="position:absolute; top:205px; left:56px; right:56px; height:360px; background:#140D1E; border:3px solid #EC4899; border-radius:28px; padding:30px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:28px; font-weight:900; color:#F472B6;">TRACK 01 // GIỌNG ĐỌC VBEE MẠNH DŨNG</span>
        <span style="background:#EC4899; color:#FFF; font-weight:900; font-size:24px; padding:8px 22px; border-radius:12px;">CHUẨN -3 dB</span>
      </div>
      <svg width="900" height="150" viewBox="0 0 900 150" style="margin-top:24px;">
        <rect x="10" y="45" width="18" height="60" rx="6" fill="#EC4899"/><rect x="42" y="20" width="18" height="110" rx="6" fill="#EC4899"/>
        <rect x="74" y="10" width="18" height="130" rx="6" fill="#F472B6"/><rect x="106" y="35" width="18" height="80" rx="6" fill="#EC4899"/>
        <rect x="138" y="15" width="18" height="120" rx="6" fill="#F472B6"/><rect x="170" y="40" width="18" height="70" rx="6" fill="#EC4899"/>
        <rect x="202" y="8" width="18" height="134" rx="6" fill="#F472B6"/><rect x="234" y="28" width="18" height="94" rx="6" fill="#EC4899"/>
        <rect x="266" y="18" width="18" height="114" rx="6" fill="#EC4899"/><rect x="298" y="45" width="18" height="60" rx="6" fill="#EC4899"/>
        <rect x="330" y="12" width="18" height="126" rx="6" fill="#F472B6"/><rect x="362" y="30" width="18" height="90" rx="6" fill="#EC4899"/>
        <rect x="394" y="16" width="18" height="118" rx="6" fill="#F472B6"/><rect x="426" y="38" width="18" height="74" rx="6" fill="#EC4899"/>
        <rect x="458" y="10" width="18" height="130" rx="6" fill="#F472B6"/><rect x="490" y="25" width="18" height="100" rx="6" fill="#EC4899"/>
        <rect x="522" y="42" width="18" height="66" rx="6" fill="#EC4899"/><rect x="554" y="14" width="18" height="122" rx="6" fill="#F472B6"/>
        <rect x="586" y="22" width="18" height="106" rx="6" fill="#EC4899"/><rect x="618" y="10" width="18" height="130" rx="6" fill="#F472B6"/>
        <rect x="650" y="34" width="18" height="82" rx="6" fill="#EC4899"/><rect x="682" y="18" width="18" height="114" rx="6" fill="#F472B6"/>
        <rect x="714" y="28" width="18" height="94" rx="6" fill="#EC4899"/><rect x="746" y="12" width="18" height="126" rx="6" fill="#F472B6"/>
        <rect x="778" y="36" width="18" height="78" rx="6" fill="#EC4899"/><rect x="810" y="20" width="18" height="110" rx="6" fill="#EC4899"/>
      </svg>
      <div style="font-size:21px; color:#FBCFE8; font-weight:700; margin-top:12px;">Tốc độ 4.5 từ/giây • Cắt bỏ khoảng lặng &gt; 0.25s • Giọng trầm ấm dứt khoát</div>
    </div>

    <!-- Track 2: BGM & SFX -18dB -->
    <div style="position:absolute; top:605px; left:56px; right:56px; bottom:54px; background:#0B191B; border:3px solid #2DD4BF; border-radius:28px; padding:30px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:28px; font-weight:900; color:#2DD4BF;">TRACK 02 // NHẠC NỀN VIOLINS &amp; SFX CHUYỂN CẢNH</span>
        <span style="background:#2DD4BF; color:#08060C; font-weight:900; font-size:24px; padding:8px 22px; border-radius:12px;">NỀN -18 dB</span>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:24px;">
        <div style="background:#071012; border:2px solid #2DD4BF; border-radius:18px; padding:22px;">
          <div style="font-size:24px; font-weight:900; color:#FFF;">🎻 BGM 1.The Violins.mp3</div>
          <div style="font-size:19px; color:#99F6E4; margin-top:8px;">Tạo nhịp căng thẳng cuốn hút mà không bao giờ lấn át giọng nói chính.</div>
        </div>
        <div style="background:#071012; border:2px solid #2DD4BF; border-radius:18px; padding:22px;">
          <div style="font-size:24px; font-weight:900; color:#FFF;">🔔 SFX Apple Pay &amp; Discord</div>
          <div style="font-size:19px; color:#99F6E4; margin-top:8px;">Điểm xuyết đúng giây chuyển cảnh để đánh thức não bộ người xem.</div>
        </div>
      </div>
    </div>
    </body></html>"""


def card_21_fifty_office_prompts_grid() -> str:
    """Card 21: 6 Vault Cards Grid (2x3) + Bottom Gold Key Bar (Theme: Gold #EAB308 & Deep Navy #050914)"""
    bg = "background: radial-gradient(circle at 50% 25%, rgba(234,179,8,0.2) 0%, transparent 58%), #050914;"
    boxes = [
        ("#01 • EXCEL & SQL", "Tự viết hàm phức tạp & làm sạch bảng 50.000 dòng"),
        ("#02 • EMAIL B2B", "Soạn chuỗi thư chào hàng & xử lý từ chối khéo léo"),
        ("#03 • HỌP & BIÊN BẢN", "Tóm tắt băng ghi âm cuộc họp thành bảng giao việc"),
        ("#04 • BÁO CÁO CEO", "Chuyển số liệu thô thành 5 gạch đầu dòng chiến lược"),
        ("#05 • NGHIÊN CỨU ĐỐI THỦ", "Bóc tách điểm yếu & khoảng trống sản phẩm trên sàn"),
        ("#06 • TỰ ĐỘNG HÓA PYTHON", "Sinh script gộp 100 file báo cáo chỉ trong 5 giây"),
    ]
    grid_html = ""
    for title, desc in boxes:
        grid_html += f"""
        <div style="background:#0D1528; border:2.5px solid #EAB308; border-radius:22px; padding:24px; display:flex; flex-direction:column; justify-content:space-between;">
          <div style="background:rgba(234,179,8,0.18); color:#FDE047; font-weight:900; font-size:19px; padding:6px 14px; border-radius:8px; display:inline-block; width:fit-content;">{title}</div>
          <div style="font-size:23px; font-weight:800; color:#FFF; line-height:1.35; margin-top:12px;">{desc}</div>
        </div>
        """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:48px; right:48px; text-align:center;">
      <div style="color:#FDE047; font-weight:900; font-size:20px;">🎁 QUÀ TẶNG MIỄN PHÍ CHO DÂN VĂN PHÒNG &amp; QUẢN LÝ</div>
      <div style="font-size:40px; font-weight:900; margin-top:8px;">SỔ TAY <span style="color:#EAB308;">50 SIÊU PROMPT</span> CẮT GIẢM 80% VIỆC LẶP</div>
    </div>

    <div style="position:absolute; top:165px; left:56px; right:56px; height:640px; display:grid; grid-template-columns:1fr 1fr; gap:22px;">
      {grid_html}
    </div>

    <div style="position:absolute; bottom:52px; left:56px; right:56px; height:155px; background:linear-gradient(90deg, #EAB308 0%, #CA8A04 100%); border-radius:24px; padding:24px 36px; color:#050914; display:flex; justify-content:space-between; align-items:center;">
      <div style="font-size:32px; font-weight:900; line-height:1.2;">Tải trọn bộ 50 Prompt đóng hộp<br>tại Bình luận đầu tiên!</div>
      <div style="background:#050914; color:#FDE047; font-weight:900; font-size:26px; padding:18px 28px; border-radius:16px;">MÃ: PROMPT50</div>
    </div>
    </body></html>"""


def card_22_awesome_llm_pyramid() -> str:
    """Card 22: 3-Tier Ascending Pyramid Architecture (Theme: Emerald #34D399 & Violet #C084FC)"""
    bg = "background: linear-gradient(180deg, #04120E 0%, #090614 100%);"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:42px; left:48px; right:48px; text-align:center;">
      <div style="color:#34D399; font-weight:900; font-size:20px;">💎 GIẢI PHẪU KHO BÁU 30,000+ STARS: AWESOME-LLM-APPS</div>
      <div style="font-size:41px; font-weight:900; margin-top:8px;">THÁP 3 TẦNG <span style="color:#34D399;">ỨNG DỤNG AI THỰC CHIẾN</span></div>
    </div>

    <!-- Tier 1 Top Narrow -->
    <div style="position:absolute; top:185px; left:230px; width:620px; height:225px; background:linear-gradient(135deg, #059669 0%, #047857 100%); border:4px solid #6EE7B7; border-radius:28px; padding:24px 32px; text-align:center; box-shadow:0 15px 40px rgba(16,185,129,0.35);">
      <div style="color:#A7F3D0; font-weight:900; font-size:19px;">ĐỈNH THÁP // MULTI-AGENT TEAMS</div>
      <div style="font-size:34px; font-weight:900; color:#FFF; margin-top:8px;">Đội ngũ AI tự phối hợp &amp; duyệt Gate</div>
      <div style="font-size:20px; color:#ECFDF5; margin-top:8px;">Tự nghiên cứu, viết kịch bản, dựng hình và xuất bản đa kênh</div>
    </div>

    <!-- Tier 2 Middle -->
    <div style="position:absolute; top:450px; left:140px; width:800px; height:235px; background:#131026; border:3px solid #C084FC; border-radius:28px; padding:26px 36px; text-align:center;">
      <div style="color:#C084FC; font-weight:900; font-size:19px;">TẦNG GIỮA // AGENTIC RAG &amp; MEMORY VAULT</div>
      <div style="font-size:34px; font-weight:900; color:#FFF; margin-top:8px;">Bộ não thứ 2 truy xuất tri thức chính xác 100%</div>
      <div style="font-size:20px; color:#E9D5FF; margin-top:8px;">Kết hợp SQLite + Vector Search + Markdown Memory có kiểm chứng</div>
    </div>

    <!-- Tier 3 Base Wide -->
    <div style="position:absolute; top:730px; left:56px; right:56px; height:270px; background:#0B1F1A; border:3px solid #34D399; border-radius:30px; padding:30px 40px; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="color:#34D399; font-weight:900; font-size:20px;">ĐẾ THÁP // MCP SERVERS &amp; LOCAL TOOLS</div>
        <div style="font-size:36px; font-weight:900; color:#FFF; margin-top:8px;">Kết nối trực tiếp Graph API, Chrome CDP &amp; FFmpeg</div>
        <div style="font-size:21px; color:#A7F3D0; margin-top:8px;">Biến lời nói của AI thành hành động thực tế trên máy tính của bạn!</div>
      </div>
      <div style="background:#34D399; color:#04120E; font-weight:900; font-size:24px; padding:22px 28px; border-radius:20px; flex-shrink:0; text-align:center;">LẤY LINK<br>REPO 👇</div>
    </div>
    </body></html>"""


def card_23_one_person_four_pages_quadrant() -> str:
    """Card 23: 2x2 Quadrant Matrix With Central Hub Badge (Theme: Coral #FB923C & Cyan #22D3EE)"""
    bg = "background: #070A12;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:42px; left:48px; right:48px; text-align:center;">
      <div style="font-size:40px; font-weight:900;">CÁCH <span style="color:#FB923C;">1 NGƯỜI</span> VẬN HÀNH <span style="color:#22D3EE;">4 FANPAGE CÙNG LÚC</span></div>
    </div>

    <!-- 2x2 Grid -->
    <div style="position:absolute; top:145px; left:56px; right:56px; bottom:56px; display:grid; grid-template-columns:1fr 1fr; grid-template-rows:1fr 1fr; gap:36px;">
      <div style="background:#0F172A; border:3px solid #22D3EE; border-radius:30px; padding:32px; display:flex; flex-direction:column; justify-content:space-between;">
        <div style="color:#22D3EE; font-weight:900; font-size:22px;">KÊNH #1 // PAGE THƯƠNG HIỆU AI</div>
        <div style="font-size:36px; font-weight:900;">AI Players</div>
        <div style="font-size:21px; color:#CBD5E1; line-height:1.4;">6 Ảnh độc bản + 3 Video Reels mỗi ngày. Thu phễu cộng đồng Zalo VIP.</div>
        <div style="background:rgba(34,211,238,0.15); color:#22D3EE; font-weight:900; font-size:20px; padding:10px 18px; border-radius:12px; width:fit-content;">9 BÀI / NGÀY</div>
      </div>

      <div style="background:#0F172A; border:3px solid #FB923C; border-radius:30px; padding:32px; display:flex; flex-direction:column; justify-content:space-between; text-align:right; align-items:flex-end;">
        <div style="color:#FB923C; font-weight:900; font-size:22px;">KÊNH #2 // NGÁCH PHÒNG TRỌ</div>
        <div style="font-size:36px; font-weight:900;">Phòng Trọ Hết Cứu</div>
        <div style="font-size:21px; color:#CBD5E1; line-height:1.4;">Ảnh vuông 1:1 chữ dày nổi bật + Link Shopee Affiliate bình luận #1.</div>
        <div style="background:rgba(251,146,60,0.15); color:#FB923C; font-weight:900; font-size:20px; padding:10px 18px; border-radius:12px; width:fit-content;">11:45 &amp; 20:00</div>
      </div>

      <div style="background:#0F172A; border:3px solid #38BDF8; border-radius:30px; padding:32px; display:flex; flex-direction:column; justify-content:space-between;">
        <div style="color:#38BDF8; font-weight:900; font-size:22px;">KÊNH #3 // NGÁCH SINH VIÊN</div>
        <div style="font-size:36px; font-weight:900;">Ký Túc Xá Có Biến</div>
        <div style="font-size:21px; color:#CBD5E1; line-height:1.4;">Đồ dùng giường tầng, đèn kẹp, ổ cắm KTX. Tự động đi seeding 3 ca/ngày.</div>
        <div style="background:rgba(56,189,248,0.15); color:#38BDF8; font-weight:900; font-size:20px; padding:10px 18px; border-radius:12px; width:fit-content;">11:45 &amp; 20:00</div>
      </div>

      <div style="background:#0F172A; border:3px solid #F43F5E; border-radius:30px; padding:32px; display:flex; flex-direction:column; justify-content:space-between; text-align:right; align-items:flex-end;">
        <div style="color:#F43F5E; font-weight:900; font-size:22px;">KÊNH #4 // NGÁCH VĂN PHÒNG</div>
        <div style="font-size:36px; font-weight:900;">Hội Deadline</div>
        <div style="font-size:21px; color:#CBD5E1; line-height:1.4;">Phụ kiện công thái học, bảo vệ cổ tay &amp; mắt cho dân văn phòng.</div>
        <div style="background:rgba(244,63,94,0.15); color:#F43F5E; font-weight:900; font-size:20px; padding:10px 18px; border-radius:12px; width:fit-content;">11:45 &amp; 20:00</div>
      </div>
    </div>

    <!-- Center Hub -->
    <div style="position:absolute; top:485px; left:410px; width:260px; height:160px; background:#FB923C; color:#070A12; border:6px solid #070A12; border-radius:28px; display:flex; flex-direction:column; align-items:center; justify-content:center; box-shadow:0 0 50px rgba(251,146,60,0.6);">
      <div style="font-size:18px; font-weight:900;">ĐIỀU PHỐI BỞI</div>
      <div style="font-size:34px; font-weight:900;">10 SUBAGENT</div>
    </div>
    </body></html>"""


def card_24_task_delegation_matrix() -> str:
    """Card 24: Left/Right Split Matrix — Automate First vs Keep Human Approval (Theme: Acid Lime #84CC16 & Amber #F59E0B)"""
    bg = "background: linear-gradient(135deg, #091306 0%, #120D05 100%);"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:40px; left:56px; right:56px;">
      <div style="color:#A3E635; font-weight:900; font-size:20px;">🧭 MA TRẬN PHÂN QUYỀN CON NGƯỜI &amp; AI AGENT</div>
      <div style="font-size:48px; font-weight:900; margin-top:6px;">VIỆC NÀO <span style="color:#A3E635;">GIAO AI 100%</span> — VIỆC NÀO <span style="color:#FBBF24;">CEO GIỮ CHỐT?</span></div>
    </div>

    <!-- Top Wide Box: Giao AI 100% -->
    <div style="position:absolute; top:195px; left:56px; right:56px; height:460px; background:#0F1E0B; border:3px solid #84CC16; border-radius:30px; padding:32px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:30px; font-weight:900; color:#A3E635;">✅ GIAO SUBAGENT TỰ ĐỘNG HÓA 100% (85% KHỐI LƯỢNG)</span>
        <span style="background:#84CC16; color:#091306; font-weight:900; font-size:20px; padding:8px 20px; border-radius:10px;">CHẠY NGẦM 24/7</span>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-top:26px;">
        <div style="background:#162B10; border-radius:18px; padding:22px;">
          <div style="font-size:24px; font-weight:900; color:#FFF;">1. Quét Trend &amp; Đào Bình Luận</div>
          <div style="font-size:19px; color:#D9F99D; margin-top:6px;">Tự lọc sản phẩm &gt;4.7 sao và gom từ khóa nỗi đau khách hàng.</div>
        </div>
        <div style="background:#162B10; border-radius:18px; padding:22px;">
          <div style="font-size:24px; font-weight:900; color:#FFF;">2. Kết Xuất Ảnh &amp; Video Độc Bản</div>
          <div style="font-size:19px; color:#D9F99D; margin-top:6px;">Tự chạy Headless Chrome, Remotion và kiểm tra cổng Zero-Clone.</div>
        </div>
        <div style="background:#162B10; border-radius:18px; padding:22px;">
          <div style="font-size:24px; font-weight:900; color:#FFF;">3. Lên Lịch &amp; Ghim Bình Luận #1</div>
          <div style="font-size:19px; color:#D9F99D; margin-top:6px;">Đẩy bài lên Meta Graph API và tự động gắn link Shopee / Zalo.</div>
        </div>
        <div style="background:#162B10; border-radius:18px; padding:22px;">
          <div style="font-size:24px; font-weight:900; color:#FFF;">4. Đi Tương Tác Hội Nhóm 3 Ca</div>
          <div style="font-size:19px; color:#D9F99D; margin-top:6px;">Bật Chrome ngầm, chuyển đúng Fanpage, tương tác xong tự đóng.</div>
        </div>
      </div>
    </div>

    <!-- Bottom Wide Box: CEO Giữ Quyền Quyết Định -->
    <div style="position:absolute; top:690px; left:56px; right:56px; bottom:52px; background:#241807; border:3px solid #F59E0B; border-radius:30px; padding:32px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="font-size:30px; font-weight:900; color:#FBBF24;">👑 3 QUYỀN TỐI THƯỢNG CEO NẮM GIỮ (15% CHIẾN LƯỢC)</div>
      <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:20px;">
        <div style="background:#140D04; border:2px solid #F59E0B; border-radius:16px; padding:18px; text-align:center;">
          <div style="font-size:23px; font-weight:900; color:#FFF;">Định Hướng Thẩm Mỹ</div>
          <div style="font-size:17px; color:#FDE68A; margin-top:4px;">Duyệt chuẩn Visual &amp; Luật cứng</div>
        </div>
        <div style="background:#140D04; border:2px solid #F59E0B; border-radius:16px; padding:18px; text-align:center;">
          <div style="font-size:23px; font-weight:900; color:#FFF;">Phê Duyệt Ngân Sách</div>
          <div style="font-size:17px; color:#FDE68A; margin-top:4px;">Quyết định mở rộng hay dừng</div>
        </div>
        <div style="background:#140D04; border:2px solid #F59E0B; border-radius:16px; padding:18px; text-align:center;">
          <div style="font-size:23px; font-weight:900; color:#FFF;">Nhận Báo Cáo 7 Dòng</div>
          <div style="font-size:17px; color:#FDE68A; margin-top:4px;">Chỉ đạo từ xa qua Telegram</div>
        </div>
      </div>
    </div>
    </body></html>"""


CARDS_D78_SPEC = [
    {
        "code": "day7_img1_0830_telecontrol",
        "slot_dt": "2026-11-01 08:30",
        "builder": card_13_tele_remote_phone,
        "cta_kw": "TELEBOT",
        "caption": (
            "📱 ĐIỀU HÀNH CẢ ĐỘI NGŨ 10 SUBAGENT CHỈ VỚI CHIẾC ĐIỆN THOẠI TRÊN TAY!\n\n"
            "Nhờ cầu nối Telegram 2 chiều, bạn có thể kiểm tra nhanh số liệu 4 Fanpage trong 1 giây bằng lệnh /status hoặc nhắn tin giao việc tự nhiên để đánh thức hệ thống tự động thực thi trên máy tính.\n\n"
            "👇 Nhận mã nguồn Telegram 2-Way Bridge ở bình luận đầu tiên nhé!"
        ),
    },
    {
        "code": "day7_img2_1015_10subagents",
        "slot_dt": "2026-11-01 10:15",
        "builder": card_14_ten_agents_roundtable,
        "cta_kw": "10AGENT",
        "caption": (
            "👥 TẠI SAO ĐỘI NGŨ 10 SUBAGENT CHUYÊN BIỆT LẠI HIỆU QUẢ HƠN 1 SIÊU PROMPT ÔM ĐỒM?\n\n"
            "Khi tách nhỏ quy trình cho từng chuyên gia (MKT săn hàng, Content viết kịch bản, Edit dựng đồ họa Zero-Clone, Quản lý kênh lên lịch Meta API) dưới sự kiểm soát Gate >= 9.0 của Mama, chất lượng đầu ra luôn đồng nhất và không bị loạn ngữ cảnh.\n\n"
            "👇 Tải trọn bộ 10 file cấu hình Subagent tại bình luận đầu tiên!"
        ),
    },
    {
        "code": "day7_img3_1330_1video4kenh",
        "slot_dt": "2026-11-01 13:30",
        "builder": card_15_one_piece_multi_platform,
        "cta_kw": "1RA4",
        "caption": (
            "🌐 NGUYÊN TẮC '1 MASTER ASSET → 4 KÊNH TỰ ĐỘNG': NHÂN BẢN ĐỘ PHỦ MÀ KHÔNG NHÂN BẢN SỨC NGƯỜI!\n\n"
            "Từ 1 nội dung gốc đã qua cổng kiểm duyệt, Subagent Đa Kênh tự động chuyển hóa thành định dạng chuẩn thuật toán cho từng nền tảng: Facebook gắn link ở Bình luận #1, YouTube Shorts tối ưu SEO <60 ký tự, Threads thả link ở Self-Reply #1.\n\n"
            "👇 Lấy quy trình phân phối đa kênh ở bình luận đầu tiên!"
        ),
    },
    {
        "code": "day7_img4_1515_envsetup",
        "slot_dt": "2026-11-01 15:15",
        "builder": card_16_env_server_rack,
        "cta_kw": "RACK4",
        "caption": (
            "🖥️ BÊN TRONG 4 TẦNG HẠ TẦNG GIÚP HỆ THỐNG AI AGENT TỰ HÀNH 24/7 TRÊN MÁY TÍNH CÁ NHÂN!\n\n"
            "Không cần thuê máy chủ đắt đỏ, bạn hoàn toàn có thể kết hợp Python + Playwright chạy ngầm, Remotion + FFmpeg dựng hình, SQLite khóa cổng chống trùng lặp và Git đồng bộ trạng thái giữa 2 máy tính.\n\n"
            "👇 Xem hướng dẫn cài đặt chi tiết tại bình luận đầu tiên nhé!"
        ),
    },
    {
        "code": "day7_img5_1815_baocaotuan",
        "slot_dt": "2026-11-01 18:15",
        "builder": card_17_weekly_equalizer_bars,
        "cta_kw": "105BAI",
        "caption": (
            "📊 TỔNG KẾT TUẦN VẬN HÀNH: LÀM SAO DUY TRÌ KỶ LUẬT 105 BÀI ĐĂNG & 21 CA TƯƠNG TÁC MỖI TUẦN?\n\n"
            "Sự khác biệt giữa làm nội dung thủ công và hệ thống tự động hóa nằm ở tính kỷ luật: Đúng giờ vàng mỗi ngày, 9 bài trên kênh AI và 6 bài trên cụm kênh Bán hàng tự động lên sóng kèm bình luận ghim chuẩn phễu.\n\n"
            "👇 Tham khảo lịch vận hành mẫu ở bình luận đầu tiên!"
        ),
    },
    {
        "code": "day7_img6_2115_muctieutuan",
        "slot_dt": "2026-11-01 21:15",
        "builder": card_18_bullseye_weekly_goals,
        "cta_kw": "MUCTIEU",
        "caption": (
            "🎯 3 MŨI TÊN TRỌNG TÂM ĐỂ TỐI ƯU TỶ LỆ CHUYỂN ĐỔI TRONG TUẦN MỚI!\n\n"
            "Sau khi hệ thống đăng bài đã chạy ổn định, bước tiếp theo là nâng cấp độ dày & điểm nhấn thị giác của chữ trên ảnh, mở rộng kho quà tặng thực chiến và tối ưu kịch bản kích cầu bình luận.\n\n"
            "👇 Tham gia cộng đồng thực chiến tại bình luận đầu tiên nhé!"
        ),
    },
    {
        "code": "day8_img1_0830_browseruse",
        "slot_dt": "2026-11-02 08:30",
        "builder": card_19_browser_use_dom_tree,
        "cta_kw": "DOMTREE",
        "caption": (
            "🌐 TẠI SAO BROWSER-USE ĐẠT HƠN 55,000 STARS TRÊN GITHUB? BÍ MẬT NẰM Ở CÁCH ĐỌC CÂY DOM!\n\n"
            "Thay vì chỉ nhìn ảnh chụp màn hình dễ bị lệch tọa độ khi cuộn trang, việc bóc tách trực tiếp các nút tương tác trên cây DOM HTML giúp AI bấm chuẩn xác 100% vào đúng ô bình luận dưới tên Fanpage.\n\n"
            "👇 Nhận tài liệu tích hợp tại bình luận đầu tiên!"
        ),
    },
    {
        "code": "day8_img2_1015_vbeeffmpeg",
        "slot_dt": "2026-11-02 10:15",
        "builder": card_20_voice_audio_mastering,
        "cta_kw": "AUDIO3DB",
        "caption": (
            "🎙️ CÔNG THỨC PHỐI ÂM THANH (-3dB VOICE / -18dB BGM) GIÚP VIDEO REELS GIỮ CHÂN NGƯỜI XEM!\n\n"
            "Một video có hình ảnh đẹp nhưng giọng đọc đều đều hoặc nhạc nền quá to sẽ khiến khán giả lướt qua ngay. Hãy chuẩn hóa giọng đọc ở mức -3dB tốc độ 4.5 từ/giây và nén nhạc nền ở mức -18dB.\n\n"
            "👇 Lấy script FFmpeg chuẩn hóa âm thanh tự động ở bình luận đầu tiên!"
        ),
    },
    {
        "code": "day8_img3_1330_50promptvp",
        "slot_dt": "2026-11-02 13:30",
        "builder": card_21_fifty_office_prompts_grid,
        "cta_kw": "PROMPT50",
        "caption": (
            "🎁 TẶNG MIỄN PHÍ: SỔ TAY 50 SIÊU PROMPT DÀNH CHO DÂN VĂN PHÒNG & NGƯỜI LÀM QUẢN LÝ!\n\n"
            "Từ viết hàm Excel/SQL phức tạp, tóm tắt biên bản cuộc họp, viết email B2B cho tới phân tích số liệu báo cáo — tất cả đã được đóng gói sẵn kèm biến số điền vào dùng ngay.\n\n"
            "👇 Bình luận 'PROMPT50' hoặc bấm vào link ở bình luận đầu tiên để tải về ngay!"
        ),
    },
    {
        "code": "day8_img4_1515_awesomellm",
        "slot_dt": "2026-11-02 15:15",
        "builder": card_22_awesome_llm_pyramid,
        "cta_kw": "LLM30K",
        "caption": (
            "💎 GIẢI PHẪU KHO BÁU 30,000+ STARS AWESOME-LLM-APPS: THÁP 3 TẦNG ỨNG DỤNG AI THỰC CHIẾN!\n\n"
            "Để xây dựng một hệ thống AI làm việc thật sự, bạn cần kết hợp cả 3 tầng: Đế tháp là MCP & Local Tools để thao tác thật, tầng giữa là Bộ não thứ 2 lưu trữ ký ức, và đỉnh tháp là đội ngũ Multi-Agent phối hợp nhịp nhàng.\n\n"
            "👇 Xem danh sách chọn lọc hay nhất tại bình luận đầu tiên nhé!"
        ),
    },
    {
        "code": "day8_img5_1815_1nguoi4page",
        "slot_dt": "2026-11-02 18:15",
        "builder": card_23_one_person_four_pages_quadrant,
        "cta_kw": "4PAGES",
        "caption": (
            "⚙️ CÁCH 1 NGƯỜI VẬN HÀNH CÙNG LÚC 4 FANPAGE VỚI TƯỜNG LỬA TÁCH TỆP TUYỆT ĐỐI!\n\n"
            "1 kênh Thương hiệu AI thu phễu cộng đồng + 3 kênh Bán hàng ngách (Phòng Trọ, Ký Túc Xá, Văn Phòng) chạy hoàn toàn độc lập nhưng được điều phối chung bởi 1 trung tâm chỉ huy tự động.\n\n"
            "👇 Xem sơ đồ kiến trúc 4 kênh tại bình luận đầu tiên!"
        ),
    },
    {
        "code": "day8_img6_2115_chonviecai",
        "slot_dt": "2026-11-02 21:15",
        "builder": card_24_task_delegation_matrix,
        "cta_kw": "MA_TRAN",
        "caption": (
            "🧭 BẠN NÊN GIAO VIỆC NÀO CHO AI TỰ LÀM 100% VÀ GIỮ LẠI QUYỀN QUYẾT ĐỊNH NÀO CHO MÌNH?\n\n"
            "Hãy giao toàn bộ 85% khối lượng việc lặp lại (quét dữ liệu, kết xuất đồ họa, lên lịch đăng, đi tương tác ngầm) cho đội ngũ Subagent, để bạn tập trung 100% tâm trí vào 15% quyết định chiến lược và thẩm mỹ.\n\n"
            "👇 Tải bảng phân quyền AI Agent ở bình luận đầu tiên nhé!"
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


def schedule_12_cards(manifest_items: list[dict]) -> list[dict]:
    import requests
    from mama_auto_scheduler_engine import load_vault, graph_post

    pages = load_vault()
    tok = pages[AI_PAGE_ID]["access_token"]

    for item in manifest_items:
        img_path = Path(item["image_path"])
        dt_obj = dt.datetime.strptime(item["slot_dt"], "%Y-%m-%d %H:%M").replace(tzinfo=VN_TZ)
        sched_ts = int(dt_obj.timestamp())
        pinned_msg = (
            f"🎁 [TÀI LIỆU & MÃ NGUỒN MIỄN PHÍ — MÃ: {item['cta_kw']}]\n"
            f"👉 Tham gia ngay Nhóm Zalo Cộng Đồng VIP \"AI Players — Thực Chiến Subagent\" để tải trọn bộ Sơ đồ Kiến trúc, File .MD & Bộ 30 Quà tặng đóng hộp:\n"
            f"🔗 Link vào nhóm ngay: {ZALO_URL} (Mã duyệt tự động: AIPLAYERS2026)"
        )
        data = {
            "caption": item["caption"],
            "access_token": tok,
            "published": "false",
            "scheduled_publish_time": str(sched_ts),
        }
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
            item["status"] = "SCHEDULED"
            item["post_id"] = post_id
            item["comment_id"] = cmt_id
            print(f"✅ [{item['code']}] SCHEDULED ({item['slot_dt']}) -> post_id={post_id} | cmt_id={cmt_id}", flush=True)
        else:
            item["status"] = "ERROR"
            item["error"] = res
            print(f"❌ [{item['code']}] Lỗi: {res}", flush=True)
        time.sleep(1.2)
    return manifest_items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true", help="Hẹn giờ 12 bài ảnh độc bản ngày 01/11 & 02/11 lên Page AI Players")
    args = parser.parse_args()

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    rendered_paths = []
    manifest_items = []

    print("🎨 Đang kết xuất 12 Ảnh Bài Đăng Độc Bản Tiếp Theo (Card 13..24 — Ngày 01/11 & 02/11)...")
    for idx, spec in enumerate(CARDS_D78_SPEC, 13):
        out_jpg = IMAGES_DIR / f"{spec['code']}.jpg"
        html = spec["builder"]()
        render_html_to_image(html, out_jpg, width=1080, height=1080)
        rendered_paths.append(out_jpg)
        manifest_items.append({
            "index": idx,
            "code": spec["code"],
            "slot_dt": spec["slot_dt"],
            "cta_kw": spec["cta_kw"],
            "image_path": str(out_jpg),
            "caption": spec["caption"],
        })
        print(f"  ✔ [{idx:02d}/24] Đã render thiết kế độc bản: {out_jpg.name}", flush=True)

    # Kiểm định toàn bộ 24 ảnh trong IMAGES_DIR qua Cổng Khóa Cứng Zero-Clone Image Gate
    ok, gate_msg = verify_zero_clone_images(IMAGES_DIR, max_similarity=0.58)
    print(("🛡️ " if ok else "🛑 ") + gate_msg, flush=True)
    if not ok:
        sys.exit(1)

    build_qa_grid(rendered_paths, QA_GRID_D78_PATH)
    print(f"🖼️ Đã tạo bảng QA Grid 12 thiết kế độc bản (01/11 - 02/11) tại: {QA_GRID_D78_PATH}", flush=True)

    if args.publish:
        manifest_items = schedule_12_cards(manifest_items)

    MANIFEST_D78_PATH.write_text(json.dumps(manifest_items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📄 Đã lưu Manifest tại: {MANIFEST_D78_PATH}", flush=True)


if __name__ == "__main__":
    main()
