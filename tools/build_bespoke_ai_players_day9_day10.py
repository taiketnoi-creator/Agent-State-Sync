#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_bespoke_ai_players_day9_day10.py — Bộ Kết Xuất 12 Ảnh Độc Bản Tiếp Theo (Card 25..36: Ngày 03/11 & 04/11)
Cho Fanpage "AI Players - Người chơi hệ AI" (1022527194267367)
==============================================================================================================
- Tuân thủ tuyệt đối LUẬT #1 (Zero-Clone Bespoke Image Design):
  1 Bài Ảnh = 1 Kiến Trúc Bố Cục Không Gian + 1 Bảng Màu Nhấn & Ánh Sáng Nền + 1 Đồ Họa SVG Độc Bản.
- Kiểm định toàn bộ ảnh trong thư mục qua cổng `verify_zero_clone_images()` (< 58% tương đồng).
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

OUT_ROOT = SUBAGENT_DIR / "campaigns" / "2026-11-02" / "ai-players-day9-day10-vault"
IMAGES_DIR = OUT_ROOT / "images"
QA_GRID_D910_PATH = OUT_ROOT / "bespoke_day9_day10_qa_grid.jpg"
MANIFEST_D910_PATH = OUT_ROOT / "bespoke_day9_day10_manifest.json"


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


def card_25_second_brain_gatekeeper() -> str:
    """Card 25: Diagonal Dual-Gate Security Scanner + Central Hexagonal Shield (Emerald #10B981 & Deep Night #04130E)"""
    bg = "background: radial-gradient(circle at 80% 25%, rgba(16,185,129,0.28) 0%, transparent 55%), linear-gradient(135deg, #04130E 0%, #091E16 100%);"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:52px; right:52px; display:flex; justify-content:space-between; align-items:center;">
      <div style="background:#10B981; color:#04130E; font-weight:900; font-size:18px; padding:8px 22px; border-radius:999px;">🛡️ LUẬT #10 // SECOND-BRAIN GATEKEEPER</div>
      <div style="border:2px solid #34D399; color:#6EE7B7; font-weight:800; font-size:17px; padding:6px 18px; border-radius:999px;">FINAL COMPLIANCE AUDITOR</div>
    </div>
    <div style="position:absolute; top:102px; left:52px; right:52px; font-size:46px; font-weight:900; line-height:1.1;">
      CỔNG KIỂM DUYỆT <span style="color:#34D399;">BỘ NÃO THỨ 2</span> CHỐNG DÙNG NHẦM KÝ ỨC CŨ
    </div>

    <!-- Top-Left Input Gate -->
    <div style="position:absolute; top:250px; left:52px; width:440px; height:240px; background:#072319; border:3px solid #10B981; border-radius:26px; padding:26px;">
      <div style="color:#6EE7B7; font-size:18px; font-weight:900;">CHỐT CHẶN 01 // TRƯỚC KHI GIAO VIỆC</div>
      <div style="font-size:28px; font-weight:900; margin-top:10px;">Đối chiếu Manifest Quy Tắc Mới Nhất</div>
      <div style="font-size:18px; color:#D1FAE5; margin-top:10px; line-height:1.4;">Tự động quét mọi Tab trò chuyện trên 2 máy để khóa chặt các chỉ đạo vừa cập nhật.</div>
    </div>

    <!-- Center-Right Hexagonal Verdict Core -->
    <div style="position:absolute; top:340px; right:52px; width:500px; height:380px; background:linear-gradient(145deg, #10B981 0%, #059669 100%); border-radius:36px; padding:32px; color:#04130E; box-shadow:0 24px 60px rgba(16,185,129,0.35);">
      <div style="background:#04130E; color:#34D399; display:inline-block; padding:8px 18px; border-radius:12px; font-weight:900; font-size:18px;">VERDICT ENGINE v2.0</div>
      <div style="font-size:40px; font-weight:900; margin-top:18px; line-height:1.08;">APPROVED BY SECOND BRAIN ✓</div>
      <div style="font-size:20px; font-weight:800; margin-top:14px; color:#06281E; line-height:1.4;">Chặn đứng 100% lệnh gọi mẫu cũ (5-template cũ, video bán hàng đang đóng băng, hoặc lộ thông tin nhạy cảm).</div>
      <div style="margin-top:22px; background:#04130E; color:#FFF; padding:16px 22px; border-radius:18px; font-size:21px; font-weight:900; text-align:center;">0% RỦI RO TÁI SỬ DỤNG CODE CŨ</div>
    </div>

    <!-- Bottom-Left Audit Log Box -->
    <div style="position:absolute; bottom:52px; left:52px; width:440px; height:490px; background:#061B13; border:2.5px dashed #34D399; border-radius:26px; padding:26px; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="color:#34D399; font-weight:900; font-size:19px;">CHỐT CHẶN 02 // NGƯỜI DUYỆT CUỐI CÙNG</div>
        <div style="font-size:29px; font-weight:900; margin-top:8px;">Kiểm tra đầu ra của 9 Subagent</div>
      </div>
      <div style="background:#0B2E22; padding:18px; border-radius:18px; border-left:6px solid #10B981;">
        <div style="font-size:19px; font-weight:800; color:#A7F3D0;">✔ Kiểm tra độ độc bản &lt; 58%</div>
        <div style="font-size:17px; color:#E2E8F0; margin-top:4px;">Đối chiếu lưới 64 vùng màu tự động.</div>
      </div>
      <div style="background:#0B2E22; padding:18px; border-radius:18px; border-left:6px solid #34D399;">
        <div style="font-size:19px; font-weight:800; color:#A7F3D0;">✔ Khóa Tường Lửa Tách Tệp</div>
        <div style="font-size:17px; color:#E2E8F0; margin-top:4px;">Page AI và 3 Page Bán Hàng độc lập 100%.</div>
      </div>
      <div style="background:#10B981; color:#04130E; padding:16px; border-radius:16px; font-weight:900; font-size:20px; text-align:center;">BÌNH LUẬN "GATEKEEPER" NHẬN CODE</div>
    </div>

    <!-- Bottom-Right Stat Bar -->
    <div style="position:absolute; bottom:52px; right:52px; width:500px; height:245px; background:#072319; border:3px solid #34D399; border-radius:26px; padding:26px; display:flex; align-items:center; justify-content:space-between;">
      <div>
        <div style="font-size:20px; color:#6EE7B7; font-weight:800;">TỐC ĐỘ KIỂM DUYỆT</div>
        <div style="font-size:58px; font-weight:900; color:#FFF;">0.15s</div>
        <div style="font-size:18px; color:#A7F3D0;">Tự động hóa bằng Python CLI</div>
      </div>
      <div style="width:180px; height:180px; border-radius:999px; border:10px solid #10B981; display:flex; align-items:center; justify-content:center; flex-direction:column; background:#04130E;">
        <div style="font-size:38px; font-weight:900; color:#34D399;">100%</div>
        <div style="font-size:15px; font-weight:800; color:#FFF;">CHUẨN MỚI</div>
      </div>
    </div>
    </body></html>"""


def card_26_isometric_virtual_office() -> str:
    """Card 26: 7-Zone Isometric Floorplan Grid + Top Command Bar (Warm Amber #F59E0B & Slate #0F172A)"""
    bg = "background: radial-gradient(circle at 20% 80%, rgba(245,158,11,0.25) 0%, transparent 55%), #0B111E;"
    rooms = [
        ("PHÒNG CHỈ HUY", "Mama (Chief of Staff)", "#F59E0B", 54, 230, 310, 240),
        ("PHÒNG NGHIÊN CỨU", "MKT + Bộ Não Thứ 2", "#38BDF8", 385, 230, 310, 240),
        ("PHÒNG BIÊN KỊCH", "Content + Đa Kênh", "#A855F7", 716, 230, 310, 240),
        ("STUDIO ĐỒ HỌA 3D", "Edit + Edit-2 (TVC)", "#EC4899", 54, 495, 475, 250),
        ("PHÒNG THU ÂM", "Voice (-3dB Vbee)", "#10B981", 551, 495, 475, 250),
    ]
    rooms_html = ""
    for title, sub, col, lx, ty, w, h in rooms:
        rooms_html += f"""
        <div style="position:absolute; left:{lx}px; top:{ty}px; width:{w}px; height:{h}px; background:#151F32; border:3px solid {col}; border-radius:24px; padding:24px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 14px 32px rgba(0,0,0,0.5);">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="background:{col}; color:#0B111E; font-weight:900; font-size:16px; padding:5px 14px; border-radius:8px;">{title}</span>
            <span style="color:{col}; font-weight:900; font-size:18px;">● WORKING</span>
          </div>
          <div style="font-size:28px; font-weight:900; color:#FFF;">{sub}</div>
          <div style="height:10px; background:#0B111E; border-radius:999px; overflow:hidden;">
            <div style="width:88%; height:100%; background:{col};"></div>
          </div>
        </div>
        """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:54px; right:54px; background:#1E293B; border:2px solid #F59E0B; border-radius:22px; padding:22px 32px; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="color:#FBBF24; font-weight:900; font-size:18px;">🏢 VĂN PHÒNG ẢO 3D AGENT-JAVIS // PORT 4800</div>
        <div style="font-size:38px; font-weight:900; color:#FFF; margin-top:4px;">QUAN SÁT 11 NHÂN SỰ AI LÀM VIỆC TRỰC TIẾP</div>
      </div>
      <div style="background:#F59E0B; color:#0B111E; font-weight:900; font-size:24px; padding:16px 26px; border-radius:16px;">3D LIVE VIEW</div>
    </div>
    {rooms_html}
    <!-- Bottom Lounge & Analytics Bar -->
    <div style="position:absolute; left:54px; right:54px; bottom:48px; height:255px; background:linear-gradient(90deg, #F59E0B 0%, #EA580C 100%); border-radius:28px; padding:28px 38px; color:#0B111E; display:flex; align-items:center; justify-content:space-between;">
      <div style="width:620px;">
        <div style="font-weight:900; font-size:20px; letter-spacing:1px;">⚡ ĐỒNG BỘ 2 CHIỀU VỚI ANTIGRAVITY IDE</div>
        <div style="font-size:34px; font-weight:900; margin-top:8px; line-height:1.15;">Ai đang gõ phím, ai đang duyệt bài, ai đang ra quán cà phê đều hiển thị thời gian thực!</div>
      </div>
      <div style="background:#0B111E; color:#FBBF24; padding:24px 30px; border-radius:22px; text-align:center; font-weight:900;">
        <div style="font-size:42px;">11 AGENTS</div>
        <div style="font-size:18px; color:#FFF; margin-top:4px;">7 PHÒNG BAN CHUYÊN BIỆT</div>
      </div>
    </div>
    </body></html>"""


def card_27_graphrag_knowledge_web() -> str:
    """Card 27: Left Comparison Pillar + Right 7-Node Crystal Graph Network SVG (Neon Pink #EC4899 & Deep Violet #160626)"""
    bg = "background: radial-gradient(circle at 75% 55%, rgba(236,72,153,0.32) 0%, transparent 58%), #11051C;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:42px; left:52px; right:52px;">
      <div style="color:#F472B6; font-weight:900; font-size:20px;">🕸️ KIẾN TRÚC MICROSOFT GRAPHRAG VS VECTOR RAG</div>
      <div style="font-size:48px; font-weight:900; margin-top:6px; line-height:1.08;">TẠI SAO <span style="color:#EC4899;">ĐỒ THỊ TRI THỨC</span> HIỂU SÂU GẤP 3 LẦN TÌM KIẾM TỪ KHÓA?</div>
    </div>

    <!-- Left Pillar -->
    <div style="position:absolute; top:220px; left:52px; width:410px; bottom:52px; background:#1D0B30; border:3px solid #EC4899; border-radius:30px; padding:30px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="background:#3B0764; border-radius:20px; padding:22px;">
        <div style="color:#F9A8D4; font-weight:900; font-size:18px;">❌ VECTOR RAG THÔNG THƯỜNG</div>
        <div style="font-size:24px; font-weight:800; margin-top:8px;">Cắt văn bản thành đoạn vụn rời rạc</div>
        <div style="font-size:18px; color:#E9D5FF; margin-top:6px;">Mất toàn bộ mối liên hệ nhân quả giữa các sự kiện cách xa nhau.</div>
      </div>
      <div style="background:linear-gradient(135deg, #EC4899 0%, #9333EA 100%); border-radius:20px; padding:24px;">
        <div style="color:#FFF; font-weight:900; font-size:18px;">✅ ĐỒ THỊ GRAPHRAG</div>
        <div style="font-size:26px; font-weight:900; margin-top:8px;">Nối kết Thực Thể + Quan Hệ</div>
        <div style="font-size:18px; color:#FCE7F3; margin-top:6px;">Hiểu trọn vẹn bức tranh toàn cảnh của hàng nghìn tài liệu nội bộ.</div>
      </div>
      <div style="text-align:center; background:#11051C; border:2px solid #F472B6; padding:18px; border-radius:18px;">
        <div style="font-size:46px; font-weight:900; color:#F472B6;">+290%</div>
        <div style="font-size:17px; font-weight:800;">ĐỘ CHÍNH XÁC SUY LUẬN ĐA BƯỚC</div>
      </div>
    </div>

    <!-- Right SVG Graph Network -->
    <div style="position:absolute; top:220px; right:52px; width:535px; bottom:52px; background:#180828; border:2px solid #A855F7; border-radius:30px; position:relative; overflow:hidden;">
      <svg width="535" height="808" viewBox="0 0 535 808">
        <line x1="267" y1="380" x2="120" y2="160" stroke="#EC4899" stroke-width="5"/>
        <line x1="267" y1="380" x2="420" y2="160" stroke="#EC4899" stroke-width="5"/>
        <line x1="267" y1="380" x2="100" y2="420" stroke="#A855F7" stroke-width="5"/>
        <line x1="267" y1="380" x2="435" y2="420" stroke="#A855F7" stroke-width="5"/>
        <line x1="267" y1="380" x2="140" y2="650" stroke="#EC4899" stroke-width="5"/>
        <line x1="267" y1="380" x2="400" y2="650" stroke="#EC4899" stroke-width="5"/>
        <line x1="120" y1="160" x2="420" y2="160" stroke="#F472B6" stroke-width="3" stroke-dasharray="8 6"/>
        <line x1="140" y1="650" x2="400" y2="650" stroke="#F472B6" stroke-width="3" stroke-dasharray="8 6"/>
        <circle cx="267" cy="380" r="88" fill="#EC4899"/>
        <circle cx="120" cy="160" r="58" fill="#9333EA"/>
        <circle cx="420" cy="160" r="58" fill="#9333EA"/>
        <circle cx="100" cy="420" r="54" fill="#6B21A8"/>
        <circle cx="435" cy="420" r="54" fill="#6B21A8"/>
        <circle cx="140" cy="650" r="62" fill="#DB2777"/>
        <circle cx="400" cy="650" r="62" fill="#DB2777"/>
      </svg>
      <div style="position:absolute; top:345px; left:180px; width:175px; text-align:center; font-weight:900; font-size:22px;">LÕI ĐỒ THỊ<br>TRI THỨC</div>
      <div style="position:absolute; top:142px; left:62px; width:116px; text-align:center; font-weight:800; font-size:17px;">KHÁCH HÀNG</div>
      <div style="position:absolute; top:142px; left:362px; width:116px; text-align:center; font-weight:800; font-size:17px;">SẢN PHẨM</div>
      <div style="position:absolute; top:402px; left:42px; width:116px; text-align:center; font-weight:800; font-size:17px;">NỖI ĐAU</div>
      <div style="position:absolute; top:402px; left:377px; width:116px; text-align:center; font-weight:800; font-size:17px;">KỊCH BẢN</div>
      <div style="position:absolute; top:632px; left:82px; width:116px; text-align:center; font-weight:800; font-size:17px;">ĐƠN HÀNG</div>
      <div style="position:absolute; top:632px; left:342px; width:116px; text-align:center; font-weight:800; font-size:17px;">HOA HỒNG</div>
    </div>
    </body></html>"""


def card_28_structured_json_schema() -> str:
    """Card 28: Top Code Window + Bottom 3 Lock Pillars (Electric Sky #38BDF8 & Deep Graphite #060D17)"""
    bg = "background: linear-gradient(180deg, #06101E 0%, #03070E 100%);"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:40px; left:54px; right:54px; text-align:center;">
      <div style="display:inline-block; background:#0284C7; color:#FFF; font-weight:900; font-size:18px; padding:7px 22px; border-radius:999px;">🔒 BÍ QUYẾT NỐI AI VÀO DATABASE KHÔNG BAO GIỜ LỖI</div>
      <div style="font-size:48px; font-weight:900; margin-top:12px;">ÉP KHUÔN <span style="color:#38BDF8;">100% JSON SCHEMA</span> CHO MỌI TÁC NHÂN AI</div>
    </div>

    <!-- Center Terminal Window -->
    <div style="position:absolute; top:195px; left:54px; right:54px; height:430px; background:#0B192C; border:3.5px solid #38BDF8; border-radius:28px; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,0.7);">
      <div style="height:54px; background:#0284C7; padding:0 26px; display:flex; align-items:center; justify-content:space-between; font-weight:900; font-size:19px;">
        <span>schema_validator.json — Strict Mode: TRUE</span>
        <span>0% SYNTAX ERROR</span>
      </div>
      <div style="padding:28px 36px; font-family:monospace; font-size:24px; line-height:1.55; color:#E0F2FE;">
        <div><span style="color:#38BDF8; font-weight:900;">"verdict"</span>: <span style="color:#4ADE80;">"APPROVED_BY_GATEKEEPER"</span>,</div>
        <div><span style="color:#38BDF8; font-weight:900;">"rubric_score"</span>: <span style="color:#FACC15;">9.6</span>,</div>
        <div><span style="color:#38BDF8; font-weight:900;">"zero_clone_similarity"</span>: <span style="color:#FACC15;">0.31</span>,</div>
        <div><span style="color:#38BDF8; font-weight:900;">"pinned_comment_ready"</span>: <span style="color:#4ADE80;">true</span>,</div>
        <div><span style="color:#38BDF8; font-weight:900;">"required_fields_locked"</span>: <span style="color:#F472B6;">["hook_3s", "cta_url", "sub_id"]</span></div>
      </div>
    </div>

    <!-- Bottom 3 Lock Pillars -->
    <div style="position:absolute; bottom:52px; left:54px; right:54px; height:365px; display:flex; justify-content:space-between;">
      <div style="width:305px; background:#0A1829; border-top:8px solid #38BDF8; border-radius:24px; padding:28px; display:flex; flex-direction:column; justify-content:space-between;">
        <div style="font-size:44px; font-weight:900; color:#38BDF8;">01</div>
        <div style="font-size:28px; font-weight:900;">Cấm Bịa Thêm Trường Lạ</div>
        <div style="font-size:19px; color:#BAE6FD;">Khóa chặt thuộc tính bổ sung, nạp thẳng vào SQLite &amp; n8n.</div>
      </div>
      <div style="width:305px; background:#0A1829; border-top:8px solid #0EA5E9; border-radius:24px; padding:28px; display:flex; flex-direction:column; justify-content:space-between;">
        <div style="font-size:44px; font-weight:900; color:#0EA5E9;">02</div>
        <div style="font-size:28px; font-weight:900;">Ép Kiểu Dữ Liệu Cứng</div>
        <div style="font-size:19px; color:#BAE6FD;">Số tiền, khung giờ, mã SKU luôn đúng định dạng 100%.</div>
      </div>
      <div style="width:305px; background:#38BDF8; color:#06101E; border-radius:24px; padding:28px; display:flex; flex-direction:column; justify-content:space-between;">
        <div style="font-size:44px; font-weight:900;">03</div>
        <div style="font-size:28px; font-weight:900;">Chấm Dứt Văn Hoa Dài Dòng</div>
        <div style="font-size:19px; font-weight:800;">Tiết kiệm 55% Output Token khi giao tiếp giữa 10 Agent.</div>
      </div>
    </div>
    </body></html>"""


def card_29_cookie_vault_dual_pc_bridge() -> str:
    """Card 29: Horizontal Suspension Bridge Connecting 2 Machines + Center Encrypted Vault (Flame Orange #F97316 & Espresso #120904)"""
    bg = "background: radial-gradient(circle at 50% 50%, rgba(249,115,22,0.28) 0%, transparent 60%), #110804;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:42px; left:54px; right:54px; text-align:center;">
      <div style="color:#FB923C; font-weight:900; font-size:20px;">🔐 ĐỒNG BỘ PHIÊN CHROME BOT GIỮA 2 MÁY TÍNH</div>
      <div style="font-size:47px; font-weight:900; margin-top:8px;">CHuyển CA MƯỢT MÀ <span style="color:#F97316;">KHÔNG BỊ CHECKPOINT</span></div>
    </div>

    <!-- Left Machine: Company PC -->
    <div style="position:absolute; top:235px; left:48px; width:300px; height:470px; background:#211007; border:3px solid #F97316; border-radius:28px; padding:26px; text-align:center; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="background:#F97316; color:#110804; font-weight:900; font-size:19px; padding:10px; border-radius:14px;">MÁY CÔNG TY (GUICCI)</div>
      <div style="font-size:64px;">🏢</div>
      <div style="font-size:25px; font-weight:900;">Chạy Ca Sáng &amp; Trưa (12:00)</div>
      <div style="font-size:18px; color:#FED7AA;">Tự động đóng trình duyệt &amp; xuất Cookie ngay khi xong ca.</div>
    </div>

    <!-- Center Vault Core -->
    <div style="position:absolute; top:275px; left:380px; width:320px; height:390px; background:linear-gradient(180deg, #F97316 0%, #C2410C 100%); border-radius:999px; padding:34px; text-align:center; color:#110804; display:flex; flex-direction:column; justify-content:center; box-shadow:0 0 60px rgba(249,115,22,0.45);">
      <div style="font-size:20px; font-weight:900;">SESSION VAULT</div>
      <div style="font-size:40px; font-weight:900; margin-top:10px; line-height:1.1;">ĐỒNG BỘ 2 CHIỀU TỰ ĐỘNG</div>
      <div style="background:#110804; color:#FB923C; font-weight:900; font-size:18px; padding:12px; border-radius:999px; margin-top:18px;">HEADLESS 100%</div>
    </div>

    <!-- Right Machine: Home PC -->
    <div style="position:absolute; top:235px; right:48px; width:300px; height:470px; background:#211007; border:3px solid #FB923C; border-radius:28px; padding:26px; text-align:center; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="background:#FB923C; color:#110804; font-weight:900; font-size:19px; padding:10px; border-radius:14px;">MÁY Ở NHÀ (ADMIN-PC)</div>
      <div style="font-size:64px;">🏠</div>
      <div style="font-size:25px; font-weight:900;">Tiếp Quản Ca Chiều &amp; Tối (20:30)</div>
      <div style="font-size:18px; color:#FED7AA;">Nạp thẳng phiên Fanpage không cần đăng nhập lại.</div>
    </div>

    <!-- Bottom Firewall Rule Strip -->
    <div style="position:absolute; bottom:52px; left:48px; right:48px; height:255px; background:#1C0E07; border:3px solid #F97316; border-radius:28px; padding:28px 38px; display:flex; align-items:center; justify-content:space-between;">
      <div style="width:650px;">
        <div style="color:#FB923C; font-weight:900; font-size:20px;">🛡️ LUẬT #4 &amp; LUẬT #6 // BẢO VỆ TRANG CÁ NHÂN TUYỆT ĐỐI</div>
        <div style="font-size:30px; font-weight:900; margin-top:8px;">Tự động Switch Profile sang 4 Fanpage &amp; cấm đụng vào Chrome làm việc của CEO!</div>
      </div>
      <div style="background:#F97316; color:#110804; font-weight:900; font-size:26px; padding:24px 32px; border-radius:20px; text-align:center;">
        3 CA / NGÀY<br>100% NGẦM
      </div>
    </div>
    </body></html>"""


def card_30_zero_clone_8x8_matrix() -> str:
    """Card 30: Left 8x8 Heatmap Matrix SVG + Right Threshold Gauge (Acid Lime #84CC16 & Forest Black #071105)"""
    bg = "background: radial-gradient(circle at 30% 60%, rgba(132,204,22,0.24) 0%, transparent 55%), #071105;"
    cells_svg = ""
    colors = ["#1A2E05", "#365314", "#4D7C0F", "#65A30D", "#84CC16", "#A3E635", "#3F6212", "#1E3A1E"]
    for r in range(8):
        for c in range(8):
            col = colors[(r * 3 + c * 5) % len(colors)]
            cells_svg += f'<rect x="{c*54 + 14}" y="{r*54 + 14}" width="48" height="48" rx="8" fill="{col}" />'
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:40px; left:52px; right:52px;">
      <div style="display:inline-block; background:#84CC16; color:#071105; font-weight:900; font-size:18px; padding:7px 20px; border-radius:999px;">🧬 THUẬT TOÁN KIỂM ĐỊNH ĐỘC BẢN ZERO-CLONE</div>
      <div style="font-size:48px; font-weight:900; margin-top:10px; line-height:1.08;">QUÉT LƯỚI <span style="color:#A3E635;">64 VÙNG KHÔNG GIAN</span> CHẶN ĐỨNG ẢNH TRÙNG LẶP</div>
    </div>

    <!-- Left 8x8 Matrix -->
    <div style="position:absolute; top:225px; left:52px; width:460px; height:460px; background:#0F220A; border:4px solid #84CC16; border-radius:28px; display:flex; align-items:center; justify-content:center;">
      <svg width="454" height="454" viewBox="0 0 454 454">{cells_svg}</svg>
    </div>

    <!-- Right Threshold Panel -->
    <div style="position:absolute; top:225px; right:52px; width:485px; height:460px; background:#11260C; border:3px solid #A3E635; border-radius:28px; padding:32px; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="color:#A3E635; font-weight:900; font-size:20px;">NGƯỠNG CỔNG KHÓA CỨNG</div>
        <div style="font-size:76px; font-weight:900; color:#FFF; line-height:1;">&lt; 58%</div>
        <div style="font-size:22px; color:#D9F99D; font-weight:700; margin-top:8px;">Tương đồng bố cục tối đa cho phép</div>
      </div>
      <div style="background:#071105; border-left:7px solid #84CC16; padding:20px; border-radius:16px;">
        <div style="font-size:22px; font-weight:900; color:#A3E635;">Nếu vượt ngưỡng 58%:</div>
        <div style="font-size:19px; color:#ECFCCB; margin-top:6px;">Hệ thống lập tức hủy lệnh đăng (sys.exit(1)) và yêu cầu thiết kế kiến trúc mới.</div>
      </div>
    </div>

    <!-- Bottom Full-Width Summary -->
    <div style="position:absolute; bottom:52px; left:52px; right:52px; height:290px; background:linear-gradient(90deg, #84CC16 0%, #4D7C0F 100%); border-radius:28px; padding:30px 40px; color:#071105; display:flex; align-items:center; justify-content:space-between;">
      <div style="width:640px;">
        <div style="font-size:21px; font-weight:900;">🎨 BÃI BỎ VĨNH VIỄN LỐI MÒN 5 TEMPLATE CỐ ĐỊNH</div>
        <div style="font-size:36px; font-weight:900; margin-top:8px; line-height:1.15;">Mỗi bài đăng trên Page là một tác phẩm Infographic độc bản duy nhất!</div>
      </div>
      <div style="background:#071105; color:#A3E635; padding:26px 34px; border-radius:22px; text-align:center; font-weight:900;">
        <div style="font-size:44px;">36/36</div>
        <div style="font-size:18px; color:#FFF;">BÀI ĐẠT CHUẨN</div>
      </div>
    </div>
    </body></html>"""


def card_31_vision_ocr_scanner() -> str:
    """Card 31: Top Laser Document Scanner + Bottom 3 Extracted JSON Cards (Indigo #6366F1 & Cyan #22D3EE)"""
    bg = "background: radial-gradient(circle at 50% 25%, rgba(99,102,241,0.3) 0%, transparent 55%), #070617;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:40px; left:54px; right:54px; text-align:center;">
      <div style="color:#22D3EE; font-weight:900; font-size:20px;">📄 VISION-LANGUAGE OCR THẾ HỆ MỚI</div>
      <div style="font-size:48px; font-weight:900; margin-top:8px;">BÓC TÁCH <span style="color:#818CF8;">HÓA ĐƠN &amp; BẢNG BIỂU RỐI</span> TRONG 2 GIÂY</div>
    </div>

    <!-- Center Scanner Beam Box -->
    <div style="position:absolute; top:205px; left:54px; right:54px; height:380px; background:#11102E; border:3px solid #6366F1; border-radius:30px; padding:32px; position:relative; overflow:hidden;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div style="width:420px; background:#1E1B4B; padding:24px; border-radius:20px; border:2px dashed #818CF8;">
          <div style="color:#A5B4FC; font-weight:800; font-size:18px;">ĐẦU VÀO: ẢNH CHỤP NGHIÊNG / MỜ</div>
          <div style="font-size:26px; font-weight:900; margin-top:10px;">Hóa đơn giấy nhăn, bảng PDF nhiều cột gộp ô phức tạp</div>
        </div>
        <div style="font-size:56px; color:#22D3EE; font-weight:900;">⚡➔</div>
        <div style="width:420px; background:#06B6D4; color:#070617; padding:24px; border-radius:20px;">
          <div style="font-weight:900; font-size:18px;">ĐẦU RA: BẢNG SỐ LIỆU SẠCH 100%</div>
          <div style="font-size:26px; font-weight:900; margin-top:10px;">Tự động đối chiếu tổng tiền &amp; đẩy thẳng vào Excel / ERP</div>
        </div>
      </div>
      <div style="position:absolute; left:0; right:0; bottom:42px; height:8px; background:linear-gradient(90deg, transparent, #22D3EE, #6366F1, transparent); box-shadow:0 0 25px #22D3EE;"></div>
    </div>

    <!-- Bottom 3 Pillars -->
    <div style="position:absolute; bottom:52px; left:54px; right:54px; height:390px; display:flex; justify-content:space-between;">
      <div style="width:305px; background:#131136; border:2.5px solid #818CF8; border-radius:24px; padding:28px; display:flex; flex-direction:column; justify-content:space-between;">
        <div style="background:#6366F1; width:64px; height:64px; border-radius:16px; display:flex; align-items:center; justify-content:center; font-size:30px; font-weight:900;">1</div>
        <div style="font-size:27px; font-weight:900;">Hiểu Ngữ Cảnh Bảng</div>
        <div style="font-size:19px; color:#C7D2FE;">Không bị lệch dòng khi gặp các ô gộp ngang dọc.</div>
      </div>
      <div style="width:305px; background:#131136; border:2.5px solid #22D3EE; border-radius:24px; padding:28px; display:flex; flex-direction:column; justify-content:space-between;">
        <div style="background:#22D3EE; color:#070617; width:64px; height:64px; border-radius:16px; display:flex; align-items:center; justify-content:center; font-size:30px; font-weight:900;">2</div>
        <div style="font-size:27px; font-weight:900;">Đọc Chữ Viết Tay Việt</div>
        <div style="font-size:19px; color:#C7D2FE;">Nhận diện chính xác cả chữ viết tắt và dấu tiếng Việt.</div>
      </div>
      <div style="width:305px; background:#131136; border:2.5px solid #818CF8; border-radius:24px; padding:28px; display:flex; flex-direction:column; justify-content:space-between;">
        <div style="background:#6366F1; width:64px; height:64px; border-radius:16px; display:flex; align-items:center; justify-content:center; font-size:30px; font-weight:900;">3</div>
        <div style="font-size:27px; font-weight:900;">Tự Kiểm Tra Chéo</div>
        <div style="font-size:19px; color:#C7D2FE;">Phát hiện ngay nếu Đơn Giá × Số Lượng khác Thành Tiền.</div>
      </div>
    </div>
    </body></html>"""


def card_32_prompt_caching_compressor() -> str:
    """Card 32: Dual Horizontal Compression Bars + Giant Bottom Cost Saver Badge (Coral Red #FB7185 & Deep Plum #14060E)"""
    bg = "background: radial-gradient(circle at 80% 80%, rgba(251,113,133,0.26) 0%, transparent 58%), #13060C;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:42px; left:54px; right:54px;">
      <div style="color:#FB7185; font-weight:900; font-size:20px;">⚡ TỐI ƯU CHI PHÍ VẬN HÀNH ĐỘI NGŨ SUBAGENT</div>
      <div style="font-size:48px; font-weight:900; margin-top:8px; line-height:1.08;">KỸ THUẬT <span style="color:#FB7185;">PROMPT CACHING</span> GIẢM 90% TIỀN TOKEN</div>
    </div>

    <!-- Bar 1: Without Cache -->
    <div style="position:absolute; top:220px; left:54px; right:54px; height:210px; background:#260C18; border:3px solid #881337; border-radius:26px; padding:26px 34px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="display:flex; justify-content:space-between; font-size:22px; font-weight:900; color:#FDA4AF;">
        <span>❌ CÁCH CŨ: GỬI LẠI TOÀN BỘ TÀI LIỆU MỖI LƯỢT CHAT</span>
        <span>100% CHI PHÍ</span>
      </div>
      <div style="height:56px; background:#E11D48; border-radius:16px; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:22px;">NẠP LẠI 50,000 TOKENS QUY CHUẨN TỪ ĐẦU (CHẬM 12 GIÂY)</div>
    </div>

    <!-- Bar 2: With Cache -->
    <div style="position:absolute; top:460px; left:54px; right:54px; height:225px; background:#2D0E1D; border:3.5px solid #FB7185; border-radius:26px; padding:26px 34px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="display:flex; justify-content:space-between; font-size:22px; font-weight:900; color:#4ADE80;">
        <span>✅ CÁCH MỚI: KHÓA BỘ NHỚ ĐỆM PREFIX CACHE</span>
        <span>TIẾT KIỆM 90%</span>
      </div>
      <div style="display:flex; gap:14px; height:64px;">
        <div style="width:82%; background:#10B981; color:#052E16; border-radius:16px; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:22px;">ĐỌC TỪ CACHE SIÊU TỐC (GIẢM 90% GIÁ)</div>
        <div style="width:18%; background:#FB7185; color:#13060C; border-radius:16px; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:20px;">LỆNH MỚI</div>
      </div>
    </div>

    <!-- Bottom Split Impact -->
    <div style="position:absolute; bottom:52px; left:54px; right:54px; height:290px; display:flex; justify-content:space-between;">
      <div style="width:465px; background:#FB7185; color:#13060C; border-radius:28px; padding:32px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;">
        <div style="font-size:84px; font-weight:900; line-height:1;">-90%</div>
        <div style="font-size:26px; font-weight:900; margin-top:10px;">CHI PHÍ INPUT TOKEN HÀNG THÁNG</div>
      </div>
      <div style="width:465px; background:#260C18; border:3px solid #FB7185; border-radius:28px; padding:32px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;">
        <div style="font-size:84px; font-weight:900; color:#FB7185; line-height:1;">X4 LẦN</div>
        <div style="font-size:26px; font-weight:900; color:#FFF; margin-top:10px;">TỐC ĐỘ PHẢN HỒI TOKEN ĐẦU TIÊN</div>
      </div>
    </div>
    </body></html>"""


def card_33_code_sandbox_loop() -> str:
    """Card 33: 3-Corner Triangle Loop SVG + Right Execution Terminal (Teal #2DD4BF & Deep Ocean #031316)"""
    bg = "background: radial-gradient(circle at 25% 55%, rgba(45,212,191,0.25) 0%, transparent 58%), #031316;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:40px; left:52px; right:52px;">
      <div style="color:#2DD4BF; font-weight:900; font-size:20px;">🐍 CODE INTERPRETER SANDBOX THỰC CHIẾN</div>
      <div style="font-size:47px; font-weight:900; margin-top:8px; line-height:1.08;">ĐỪNG ĐỂ AI TÍNH NHẨM: HÃY CHO NÓ <span style="color:#2DD4BF;">TỰ CHẠY CODE PYTHON</span></div>
    </div>

    <!-- Left Triangle Loop -->
    <div style="position:absolute; top:220px; left:52px; width:460px; bottom:52px; background:#07252B; border:3px solid #2DD4BF; border-radius:30px; padding:28px; position:relative;">
      <svg width="400" height="520" viewBox="0 0 400 520">
        <polygon points="200,55 60,410 340,410" fill="none" stroke="#2DD4BF" stroke-width="6" stroke-dasharray="12 8"/>
        <circle cx="200" cy="55" r="46" fill="#2DD4BF"/>
        <circle cx="60" cy="410" r="46" fill="#0D9488"/>
        <circle cx="340" cy="410" r="46" fill="#0D9488"/>
      </svg>
      <div style="position:absolute; top:145px; left:100px; width:260px; text-align:center; font-weight:900; font-size:24px; color:#5EEAD4;">1. AI Tự Viết Script</div>
      <div style="position:absolute; bottom:110px; left:24px; width:170px; text-align:center; font-weight:800; font-size:20px;">2. Chạy Trong Hộp Cát Cô Lập</div>
      <div style="position:absolute; bottom:110px; right:24px; width:170px; text-align:center; font-weight:800; font-size:20px;">3. Tự Sửa Lỗi &amp; Xuất Biểu Đồ</div>
      <div style="position:absolute; bottom:26px; left:28px; right:28px; background:#2DD4BF; color:#031316; padding:14px; border-radius:14px; text-align:center; font-weight:900; font-size:20px;">CHÍNH XÁC 100% SỐ LIỆU TÀI CHÍNH</div>
    </div>

    <!-- Right 3 Benefit Cards -->
    <div style="position:absolute; top:220px; right:52px; width:490px; bottom:52px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="background:#08282E; border-right:8px solid #2DD4BF; border-radius:24px; padding:28px;">
        <div style="color:#5EEAD4; font-weight:900; font-size:19px;">ƯU ĐIỂM 01 // XỬ LÝ FILE EXCEL 100,000 DÒNG</div>
        <div style="font-size:27px; font-weight:900; margin-top:8px;">Không bị tràn ngữ cảnh LLM</div>
        <div style="font-size:19px; color:#CCFBF1; margin-top:6px;">Dùng Pandas lọc và tính tổng trực tiếp trong 0.5 giây.</div>
      </div>
      <div style="background:#08282E; border-right:8px solid #14B8A6; border-radius:24px; padding:28px;">
        <div style="color:#5EEAD4; font-weight:900; font-size:19px;">ƯU ĐIỂM 02 // CƠ CHẾ TỰ BẮT LỖI (SELF-DEBUG)</div>
        <div style="font-size:27px; font-weight:900; margin-top:8px;">Đọc Traceback và tự viết lại code</div>
        <div style="font-size:19px; color:#CCFBF1; margin-top:6px;">Không cần con người can thiệp khi gặp dữ liệu khuyết thiếu.</div>
      </div>
      <div style="background:#08282E; border-right:8px solid #2DD4BF; border-radius:24px; padding:28px;">
        <div style="color:#5EEAD4; font-weight:900; font-size:19px;">ƯU ĐIỂM 03 // AN TOÀN TUYỆT ĐỐI</div>
        <div style="font-size:27px; font-weight:900; margin-top:8px;">Môi trường cô lập không chạm ổ cứng chính</div>
        <div style="font-size:19px; color:#CCFBF1; margin-top:6px;">Bảo vệ toàn vẹn hệ thống dữ liệu doanh nghiệp.</div>
      </div>
    </div>
    </body></html>"""


def card_34_self_healing_workflow() -> str:
    """Card 34: 3 Parallel Circuit Failover Tracks (Cyber Yellow #FACC15 & Obsidian #121107)"""
    bg = "background: radial-gradient(circle at 50% 60%, rgba(250,204,21,0.22) 0%, transparent 60%), #121006;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:40px; left:54px; right:54px; text-align:center;">
      <div style="display:inline-block; background:#FACC15; color:#121006; font-weight:900; font-size:18px; padding:7px 22px; border-radius:999px;">🔄 SELF-HEALING WORKFLOW AUTOMATION</div>
      <div style="font-size:47px; font-weight:900; margin-top:10px;">CÁCH XÂY HỆ THỐNG AI <span style="color:#FACC15;">TỰ CHỮA LÀNH</span> KHI ĐỨT KẾT NỐI</div>
    </div>

    <!-- Track 1: Primary -->
    <div style="position:absolute; top:215px; left:54px; right:54px; height:235px; background:#231F0B; border:3px solid #EF4444; border-radius:26px; padding:26px 34px; display:flex; align-items:center; justify-content:space-between;">
      <div style="width:660px;">
        <div style="color:#F87171; font-weight:900; font-size:20px;">NHÁNH 01 // KHI MẠNG CHẬP CHỜN HOẶC QUÁ TẢI API</div>
        <div style="font-size:31px; font-weight:900; margin-top:8px;">Exponential Backoff (Thử lại sau 2s → 4s → 8s)</div>
        <div style="font-size:19px; color:#FEF08A; margin-top:6px;">Không bắn dồn dập làm khóa tài khoản, tự động chờ qua đỉnh nghẽn mạng.</div>
      </div>
      <div style="background:#7F1D1D; color:#FCA5A5; padding:22px 26px; border-radius:20px; font-weight:900; font-size:24px; text-align:center;">AUTO<br>RETRY</div>
    </div>

    <!-- Track 2: Fallback Model -->
    <div style="position:absolute; top:480px; left:54px; right:54px; height:235px; background:#231F0B; border:3px solid #FACC15; border-radius:26px; padding:26px 34px; display:flex; align-items:center; justify-content:space-between;">
      <div style="width:660px;">
        <div style="color:#FACC15; font-weight:900; font-size:20px;">NHÁNH 02 // TỰ ĐỘNG CHUYỂN ĐỔI DỰ PHÒNG (FALLBACK)</div>
        <div style="font-size:31px; font-weight:900; margin-top:8px;">Đổi ngay sang cổng dự phòng trong 0.5 giây</div>
        <div style="font-size:19px; color:#FEF08A; margin-top:6px;">Nếu máy chủ giọng đọc hoặc API chính bảo trì, luồng dự phòng lập tức tiếp quản.</div>
      </div>
      <div style="background:#FACC15; color:#121006; padding:22px 26px; border-radius:20px; font-weight:900; font-size:24px; text-align:center;">ZERO<br>DOWNTIME</div>
    </div>

    <!-- Track 3: Telegram Alert -->
    <div style="position:absolute; bottom:52px; left:54px; right:54px; height:245px; background:linear-gradient(90deg, #FACC15 0%, #EAB308 100%); border-radius:26px; padding:28px 36px; color:#121006; display:flex; align-items:center; justify-content:space-between;">
      <div style="width:660px;">
        <div style="font-weight:900; font-size:20px;">NHÁNH 03 // LƯU TRẠNG THÁI &amp; BÁO CÁO TELEGRAM NGẮN GỌN</div>
        <div style="font-size:33px; font-weight:900; margin-top:8px; line-height:1.15;">Ghi nhớ chính xác bước đang dở vào SQLite để chạy tiếp mà không bao giờ đăng trùng bài!</div>
      </div>
      <div style="background:#121006; color:#FACC15; padding:24px 30px; border-radius:20px; font-weight:900; font-size:30px; text-align:center;">99.9%<br><span style="font-size:17px; color:#FFF;">UPTIME</span></div>
    </div>
    </body></html>"""


def card_35_slm_local_edge_balance() -> str:
    """Card 35: Top Balance Scale Comparison + Bottom 2x2 Grid (Royal Blue #60A5FA & Midnight #070B19)"""
    bg = "background: radial-gradient(circle at 70% 30%, rgba(96,165,250,0.26) 0%, transparent 58%), #070B19;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:40px; left:54px; right:54px;">
      <div style="color:#60A5FA; font-weight:900; font-size:20px;">💻 XU HƯỚNG SMALL LANGUAGE MODELS (SLM)</div>
      <div style="font-size:47px; font-weight:900; margin-top:8px; line-height:1.08;">KHI NÀO MÔ HÌNH NHỎ <span style="color:#60A5FA;">7 TỶ THAM SỐ</span> THẮNG MÔ HÌNH KHỔNG LỒ?</div>
    </div>

    <!-- Center Dual Scale -->
    <div style="position:absolute; top:215px; left:54px; right:54px; height:320px; display:flex; justify-content:space-between;">
      <div style="width:465px; background:#0F172A; border:3px solid #475569; border-radius:28px; padding:28px; display:flex; flex-direction:column; justify-content:space-between;">
        <div style="color:#94A3B8; font-weight:900; font-size:19px;">MÔ HÌNH ĐẠI ĐA NĂNG (FRONTIER LLM)</div>
        <div style="font-size:34px; font-weight:900;">Giỏi lập kế hoạch &amp; sáng tạo phức tạp</div>
        <div style="font-size:19px; color:#CBD5E1;">Nhưng chi phí cao và độ trễ lớn nếu dùng cho các tác vụ phân loại lặp đi lặp lại.</div>
      </div>
      <div style="width:465px; background:linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); border:3px solid #93C5FD; border-radius:28px; padding:28px; display:flex; flex-direction:column; justify-content:space-between;">
        <div style="color:#DBEAFE; font-weight:900; font-size:19px;">MÔ HÌNH NHỎ CHUYÊN BIỆT (SLM 7B - 14B)</div>
        <div style="font-size:34px; font-weight:900;">Chạy siêu tốc cho 1 nhiệm vụ hẹp</div>
        <div style="font-size:19px; color:#EFF6FF;">Phân loại bình luận, trích xuất từ khóa, kiểm tra định dạng với chi phí gần bằng 0đ!</div>
      </div>
    </div>

    <!-- Bottom 2x2 Grid -->
    <div style="position:absolute; bottom:52px; left:54px; right:54px; height:440px; display:grid; grid-template-columns:1fr 1fr; grid-gap:26px;">
      <div style="background:#0E162B; border-left:7px solid #60A5FA; border-radius:22px; padding:24px;">
        <div style="font-size:36px; font-weight:900; color:#60A5FA;">0 ĐỒNG / THÁNG</div>
        <div style="font-size:22px; font-weight:800; margin-top:8px;">Chạy trực tiếp trên GPU máy cá nhân</div>
      </div>
      <div style="background:#0E162B; border-left:7px solid #38BDF8; border-radius:22px; padding:24px;">
        <div style="font-size:36px; font-weight:900; color:#38BDF8;">100% RIÊNG TƯ</div>
        <div style="font-size:22px; font-weight:800; margin-top:8px;">Dữ liệu nội bộ không rời khỏi máy tính</div>
      </div>
      <div style="background:#0E162B; border-left:7px solid #38BDF8; border-radius:22px; padding:24px;">
        <div style="font-size:36px; font-weight:900; color:#38BDF8;">PHẢN HỒI 0.2s</div>
        <div style="font-size:22px; font-weight:800; margin-top:8px;">Không phụ thuộc đường truyền cáp quang quốc tế</div>
      </div>
      <div style="background:#0E162B; border-left:7px solid #60A5FA; border-radius:22px; padding:24px;">
        <div style="font-size:36px; font-weight:900; color:#60A5FA;">PHỐI HỢP HYBRID</div>
        <div style="font-size:22px; font-weight:800; margin-top:8px;">Kết hợp Mô hình lớn chỉ huy + Mô hình nhỏ hậu cần</div>
      </div>
    </div>
    </body></html>"""


def card_36_prompt_injection_shield() -> str:
    """Card 36: Concentric 3-Ring Defense Dome SVG + Bottom Threat Filter (Crimson Red #EF4444 & Onyx #140505)"""
    bg = "background: radial-gradient(circle at 50% 48%, rgba(239,68,68,0.28) 0%, transparent 58%), #120505;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:54px; right:54px; text-align:center;">
      <div style="color:#F87171; font-weight:900; font-size:20px;">🛡️ BẢO MẬT TÁC NHÂN AI DOANH NGHIỆP</div>
      <div style="font-size:46px; font-weight:900; margin-top:8px;">3 VÒNG KHIÊN CHẶN ĐỨNG <span style="color:#EF4444;">PROMPT INJECTION</span></div>
    </div>

    <!-- Center Concentric Rings -->
    <div style="position:absolute; top:190px; left:54px; right:54px; height:530px; display:flex; align-items:center; justify-content:space-between;">
      <div style="width:500px; height:500px; position:relative; display:flex; align-items:center; justify-content:center;">
        <svg width="500" height="500" viewBox="0 0 500 500">
          <circle cx="250" cy="250" r="230" fill="none" stroke="#7F1D1D" stroke-width="18"/>
          <circle cx="250" cy="250" r="165" fill="none" stroke="#DC2626" stroke-width="18" stroke-dasharray="28 12"/>
          <circle cx="250" cy="250" r="100" fill="#EF4444"/>
        </svg>
        <div style="position:absolute; text-align:center; font-weight:900; font-size:24px; color:#120505;">LÕI DỮ LIỆU<br>AN TOÀN</div>
      </div>

      <div style="width:440px; display:flex; flex-direction:column; gap:22px;">
        <div style="background:#260A0A; border:2.5px solid #EF4444; border-radius:22px; padding:22px;">
          <div style="color:#FCA5A5; font-weight:900; font-size:18px;">VÒNG 01 // LỌC ĐẦU VÀO (INPUT GUARD)</div>
          <div style="font-size:23px; font-weight:800; margin-top:6px;">Chặn câu lệnh gài bẫy "Hãy quên mọi chỉ dẫn trước đó"</div>
        </div>
        <div style="background:#260A0A; border:2.5px solid #F87171; border-radius:22px; padding:22px;">
          <div style="color:#FCA5A5; font-weight:900; font-size:18px;">VÒNG 02 // PHÂN QUYỀN TỐI THIỂU</div>
          <div style="font-size:23px; font-weight:800; margin-top:6px;">Chatbot CSKH chỉ có quyền đọc bảng giá, cấm quyền sửa/xóa DB</div>
        </div>
        <div style="background:#260A0A; border:2.5px solid #EF4444; border-radius:22px; padding:22px;">
          <div style="color:#FCA5A5; font-weight:900; font-size:18px;">VÒNG 03 // KIỂM DUYỆT ĐẦU RA</div>
          <div style="font-size:23px; font-weight:800; margin-top:6px;">Quét ẩn toàn bộ API Key, Token &amp; dữ liệu nhạy cảm</div>
        </div>
      </div>
    </div>

    <!-- Bottom CTA Banner -->
    <div style="position:absolute; bottom:48px; left:54px; right:54px; height:245px; background:linear-gradient(90deg, #EF4444 0%, #B91C1C 100%); border-radius:28px; padding:28px 38px; display:flex; align-items:center; justify-content:space-between;">
      <div style="width:650px;">
        <div style="font-size:20px; font-weight:900; color:#FEE2E2;">🔒 TUÂN THỦ LUẬT BẢO MẬT ZERO-LEAKS</div>
        <div style="font-size:34px; font-weight:900; margin-top:8px; line-height:1.15;">Đừng triển khai AI cho khách hàng nếu chưa lắp 3 lớp rào chắn bảo mật này!</div>
      </div>
      <div style="background:#120505; color:#F87171; padding:22px 30px; border-radius:20px; font-weight:900; font-size:24px; text-align:center;">NHẬN BỘ RULE<br>BẢO MẬT AI</div>
    </div>
    </body></html>"""


CARDS_D910_SPEC = [
    # --- NGÀY 09 (2026-11-03): 6 ẢNH ĐỘC BẢN ---
    {
        "code": "day9_img1_0830_gatekeeper",
        "slot_dt": "2026-11-03 08:30",
        "builder": card_25_second_brain_gatekeeper,
        "cta_kw": "GATEKEEPER",
        "caption": (
            "🛡️ CÁCH XÂY CỔNG KIỂM DUYỆT 'BỘ NÃO THỨ 2' ĐỂ 10 SUBAGENT KHÔNG BAO GIỜ DÙNG NHẦM QUY TẮC CŨ!\n\n"
            "Khi bạn vận hành nhiều cửa sổ AI cùng lúc, rủi ro lớn nhất là một Agent chuyên môn quên mất chỉ đạo mới vừa chốt và quay lại dùng mẫu thiết kế cũ.\n\n"
            "Giải pháp triệt để là đặt một Chốt Chặn Kiểm Duyệt Cuối Cùng (Second-Brain Gatekeeper):\n"
            "✨ Tự động lắng nghe mọi quy tắc mới từ tất cả các Tab làm việc.\n"
            "✨ Kiểm tra chéo đầu vào & đầu ra trước khi cho phép xuất bản.\n\n"
            "💬 Hệ thống AI của bạn đã có lớp kiểm duyệt tự động này chưa? Xem ngay sơ đồ & mã nguồn tại bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "code": "day9_img2_1015_aioffice3d",
        "slot_dt": "2026-11-03 10:15",
        "builder": card_26_isometric_virtual_office,
        "cta_kw": "AIOFFICE",
        "caption": (
            "🏢 KHỞI CHẠY VĂN PHÒNG ẢO 3D: KHI 11 NHÂN SỰ SUBAGENT HIỆN LÊN TRực QUAN TRÊN MẶT SÀN LÀM VIỆC!\n\n"
            "Thay vì nhìn hàng chục dòng log đen trắng khô khan trong Terminal, giao diện Văn Phòng Ảo 3D giúp bạn quản lý cả đội ngũ AI trong một cái nhìn:\n"
            "✨ Biết ngay Agent nào đang gõ phím xử lý tác vụ, Agent nào đang kiểm duyệt bài, Agent nào đang rảnh.\n"
            "✨ Bấm trực tiếp vào từng nhân sự để giao việc hoặc xem lịch sử phối hợp giữa các phòng ban.\n\n"
            "💬 Bạn thích điều phối AI qua giao diện 3D trực quan hay qua dòng lệnh Terminal? Lấy hướng dẫn cài đặt ở bình luận đầu tiên nha! 👇"
        ),
    },
    {
        "code": "day9_img3_1330_graphrag",
        "slot_dt": "2026-11-03 13:30",
        "builder": card_27_graphrag_knowledge_web,
        "cta_kw": "GRAPHRAG",
        "caption": (
            "🕸️ GRAPHRAG VS VECTOR RAG: TẠI SAO ĐỒ THỊ TRI THỨC GIÚP AI SUY LUẬN SÂU GẤP 3 LẦN?\n\n"
            "Vector RAG truyền thống chỉ cắt tài liệu thành từng đoạn ngắn và tìm theo độ giống nhau của câu chữ — nên khi hỏi một câu cần tổng hợp toàn bộ quy trình, AI rất dễ bỏ sót mạch liên kết.\n\n"
            "Với GraphRAG, dữ liệu được ánh xạ thành mạng lưới Thực Thể & Mối Quan Hệ chặt chẽ, giúp AI nắm bắt trọn vẹn bức tranh chiến lược.\n\n"
            "💬 Bạn đang lưu trữ kiến thức cho AI bằng file Markdown hay Vector DB? Nhận tài liệu thiết lập GraphRAG tại bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "code": "day9_img4_1515_jsonschema",
        "slot_dt": "2026-11-03 15:15",
        "builder": card_28_structured_json_schema,
        "cta_kw": "JSON100",
        "caption": (
            "🔒 ÉP KHUÔN 100% JSON SCHEMA: BÍ QUYẾT KẾT NỐI AI VÀO SQLITE & N8N KHÔNG BAO GIỜ GÃY LUỒNG!\n\n"
            "Nếu để AI trả lời tự do bằng văn bản thông thường, chỉ cần một câu chào hỏi thừa ở đầu dòng là toàn bộ script tự động hóa phía sau sẽ báo lỗi cú pháp ngay lập tức.\n\n"
            "Hãy khóa cứng đầu ra bằng JSON Schema (Strict Mode) để mọi trường dữ liệu luôn đúng chuẩn 100%.\n\n"
            "💬 Bạn hay gặp lỗi gì nhất khi nối AI vào Webhook n8n? Tải ngay bộ khuôn mẫu JSON Schema tại bình luận đầu tiên nha! 👇"
        ),
    },
    {
        "code": "day9_img5_1815_cookievault",
        "slot_dt": "2026-11-03 18:15",
        "builder": card_29_cookie_vault_dual_pc_bridge,
        "cta_kw": "DUALPC",
        "caption": (
            "🔐 ĐỒNG BỘ PHIÊN CHROME BOT GIỮA MÁY CÔNG TY & MÁY Ở NHÀ MƯỢT MÀ KHÔNG BỊ CHECKPOINT!\n\n"
            "Làm sao để vừa làm việc ở văn phòng ban ngày, tối về nhà mở máy lên là toàn bộ phiên Fanpage và lịch sử công việc tiếp nối ngay lập tức mà không phải đăng nhập lại?\n\n"
            "Bí mật nằm ở cơ chế Session Vault tự động đóng gói trạng thái ngay khi kết thúc ca chạy ngầm!\n\n"
            "💬 Bạn đang vận hành hệ thống AI trên 1 máy cố định hay đồng bộ nhiều máy? Xem kiến trúc đồng bộ 2 chiều ở bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "code": "day9_img6_2115_zeroclone",
        "slot_dt": "2026-11-03 21:15",
        "builder": card_30_zero_clone_8x8_matrix,
        "cta_kw": "ZEROCLONE",
        "caption": (
            "🧬 THUẬT TOÁN QUÉT LƯỚI 64 VÙNG KHÔNG GIAN: CHẶN ĐỨNG 100% ẢNH ĐĂNG TRÙNG LẶP BỐ CỤC!\n\n"
            "Người đọc trên mạng xã hội rất nhạy với các bài đăng dùng đi dùng lại một khuôn mẫu cố định. Để mỗi bài viết là một thiết kế độc bản thật sự, cổng kiểm định Zero-Clone tự động chia ảnh thành lưới 8×8 = 64 vùng để đo vector màu và độ sáng trước khi cho phép hẹn giờ.\n\n"
            "💬 Theo bạn yếu tố nào quyết định một bức ảnh Infographic giữ chân người xem lâu nhất? Lấy script kiểm định ảnh ở bình luận đầu tiên nhé! 👇"
        ),
    },
    # --- NGÀY 10 (2026-11-04): 6 ẢNH ĐỘC BẢN ---
    {
        "code": "day10_img1_0830_visionocr",
        "slot_dt": "2026-11-04 08:30",
        "builder": card_31_vision_ocr_scanner,
        "cta_kw": "VISIONOCR",
        "caption": (
            "📄 BÓC TÁCH HÓA ĐƠN & BẢNG BIỂU PHỨC TẠP TRONG 2 GIÂY VỚI VISION-LANGUAGE OCR!\n\n"
            "Các phần mềm OCR đời cũ rất sợ hóa đơn chụp nghiêng hoặc bảng biểu có nhiều ô gộp ngang dọc. Khi kết hợp mô hình thị giác đa phương thức cùng bước kiểm tra chéo công thức toán học, bạn có thể tự động hóa 95% khâu nhập liệu kế toán & kho vận.\n\n"
            "💬 Công việc của bạn có phải xử lý nhiều file PDF hay hóa đơn giấy mỗi ngày không? Nhận bộ Prompt & Script OCR ở bình luận đầu tiên nha! 👇"
        ),
    },
    {
        "code": "day10_img2_1015_promptcache",
        "slot_dt": "2026-11-04 10:15",
        "builder": card_32_prompt_caching_compressor,
        "cta_kw": "CACHING90",
        "caption": (
            "⚡ KỸ THUẬT PROMPT CACHING: CÁCH GIẢM 90% CHI PHÍ TOKEN & TĂNG TỐC ĐỘ PHẢN HỒI GẤP 4 LẦN!\n\n"
            "Đừng gửi lại toàn bộ sổ tay quy chuẩn hàng chục nghìn từ ở mỗi lượt gọi API theo cách thủ công! Bằng cách đặt toàn bộ quy tắc cố định lên phần đầu (Static Prefix) để kích hoạt bộ nhớ đệm, bạn vừa tiết kiệm 90% ngân sách vừa giúp Subagent phản hồi tức thì.\n\n"
            "💬 Chi phí API hàng tháng của bạn hiện đang tốn nhiều nhất ở khâu nào? Xem hướng dẫn tối ưu Token ở bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "code": "day10_img3_1330_sandbox",
        "slot_dt": "2026-11-04 13:30",
        "builder": card_33_code_sandbox_loop,
        "cta_kw": "SANDBOX",
        "caption": (
            "🐍 ĐỪNG BẮT AI TÍNH NHẨM SỐ LIỆU: HÃY CHO NÓ TỰ VIẾT & CHẠY CODE PYTHON TRONG SANDBOX!\n\n"
            "Mô hình ngôn ngữ sinh ra để dự đoán từ tiếp theo chứ không phải máy tính bỏ túi. Khi cần phân tích bảng doanh thu 100,000 dòng, hãy cấp cho Agent quyền gọi Python Sandbox để tính toán chính xác tuyệt đối tới từng con số lẻ.\n\n"
            "💬 Bạn thường dùng AI để viết nội dung hay phân tích dữ liệu nhiều hơn? Tải cấu hình Sandbox an toàn tại bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "code": "day10_img4_1515_selfheal",
        "slot_dt": "2026-11-04 15:15",
        "builder": card_34_self_healing_workflow,
        "cta_kw": "SELFHEAL",
        "caption": (
            "🔄 WORKFLOW TỰ CHỮA LÀNH (SELF-HEALING): BÍ QUYẾT ĐỂ HỆ THỐNG TỰ ĐỘNG HÓA CHẠY BỀN BỈ 24/7!\n\n"
            "Một kịch bản tự động hóa thực chiến không bao giờ giả định mọi API luôn hoạt động hoàn hảo. Nhờ 3 cơ chế: Tự thử lại theo cấp số nhân (Exponential Backoff), Tự chuyển nhánh dự phòng (Fallback) và Ghi sổ trạng thái SQLite, hệ thống luôn vận hành trơn tru ngay cả khi bạn đang ngủ.\n\n"
            "💬 Luồng tự động hóa của bạn đã có nhánh Fallback dự phòng chưa? Nhận mẫu thiết kế luồng chống đứt gãy ở bình luận đầu tiên nha! 👇"
        ),
    },
    {
        "code": "day10_img5_1815_slmedge",
        "slot_dt": "2026-11-04 18:15",
        "builder": card_35_slm_local_edge_balance,
        "cta_kw": "SLM7B",
        "caption": (
            "💻 KHI NÀO MÔ HÌNH NHỎ (SLM 7B) THẮNG ÁP ĐẢO MÔ HÌNH KHỔNG LỒ?\n\n"
            "Không phải việc gì cũng cần gọi tới mô hình lớn nhất! Trong kiến trúc Smart Model Tiering, hãy để mô hình lớn làm Tổng chỉ huy và duyệt chất lượng, còn các tác vụ phân loại bình luận, lọc từ khóa, định dạng bài đăng hãy giao cho các mô hình nhỏ tốc độ cao.\n\n"
            "💬 Bạn đã thử kết hợp nhiều tầng mô hình (Multi-Model Tiering) trong dự án của mình chưa? Xem bảng phân tầng chi tiết tại bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "code": "day10_img6_2115_shield",
        "slot_dt": "2026-11-04 21:15",
        "builder": card_36_prompt_injection_shield,
        "cta_kw": "SHIELD3",
        "caption": (
            "🛡️ 3 VÒNG KHIÊN CHẶN ĐỨNG PROMPT INJECTION: BẢO VỆ CHATBOT & AGENT DOANH NGHIỆP!\n\n"
            "Khi mở cổng cho người dùng bên ngoài tương tác với AI, luôn có nguy cơ kẻ xấu gài các câu lệnh đánh lừa để khai thác prompt gốc hoặc thao túng hệ thống. Trang bị ngay 3 vòng rào chắn: Lọc đầu vào, Phân quyền tối thiểu và Kiểm duyệt đầu ra Zero-Leaks!\n\n"
            "💬 Yếu tố bảo mật nào khiến bạn quan tâm nhất khi ứng dụng AI vào công việc? Nhận bộ checklist bảo mật AI tại bình luận đầu tiên nhé! 👇"
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
    parser.add_argument("--publish", action="store_true", help="Hẹn giờ 12 bài ảnh độc bản ngày 03/11 & 04/11 lên Page AI Players")
    args = parser.parse_args()

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    rendered_paths = []
    manifest_items = []

    print("🎨 Đang kết xuất 12 Ảnh Bài Đăng Độc Bản Tiếp Theo (Card 25..36 — Ngày 03/11 & 04/11)...")
    for idx, spec in enumerate(CARDS_D910_SPEC, 25):
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
        print(f"  ✔ [{idx:02d}/36] Đã render thiết kế độc bản: {out_jpg.name}", flush=True)

    # Kiểm định qua Cổng Khóa Cứng Zero-Clone Image Gate (< 58% tương đồng)
    ok, gate_msg = verify_zero_clone_images(IMAGES_DIR, max_similarity=0.58)
    print(("🛡️ " if ok else "🛑 ") + gate_msg, flush=True)
    if not ok:
        sys.exit(1)

    build_qa_grid(rendered_paths, QA_GRID_D910_PATH)
    print(f"🖼️ Đã tạo bảng QA Grid 12 thiết kế độc bản (03/11 - 04/11) tại: {QA_GRID_D910_PATH}", flush=True)

    if args.publish:
        manifest_items = schedule_12_cards(manifest_items)

    MANIFEST_D910_PATH.write_text(json.dumps(manifest_items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📄 Đã lưu Manifest tại: {MANIFEST_D910_PATH}", flush=True)


if __name__ == "__main__":
    main()
