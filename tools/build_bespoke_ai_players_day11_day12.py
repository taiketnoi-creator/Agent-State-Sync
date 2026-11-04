#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_bespoke_ai_players_day11_day12.py — Bộ Kết Xuất 12 Ảnh Độc Bản Tiếp Theo (Card 37..48: Ngày 05/11 & 06/11)
Cho Fanpage "AI Players - Người chơi hệ AI" (1022527194267367)
- Tuân thủ tuyệt đối LUẬT #1 (Zero-Clone Bespoke Image Design):
  1 Bài Ảnh = 1 Kiến Trúc Bố Cục Không Gian + 1 Bảng Màu Nhấn & Ánh Sáng Nền + 1 Đồ Họa SVG Độc Bản.
- Kiểm định toàn bộ ảnh trong thư mục qua cổng `verify_zero_clone_images()` (< 58% tương đồng).
"""

import argparse
import datetime as dt
import json
import shutil
import sys
import time
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SUBAGENT_DIR / "tools"))

from render_vid_style_card import get_local_fonts_css, render_html_to_image
from zero_repost_gate import verify_zero_clone_images, record_published_content

AI_PAGE_ID = "1022527194267367"
ZALO_URL = "https://zalo.me/g/fzxvbf259"
VN_TZ = dt.timezone(dt.timedelta(hours=7))

OUT_ROOT = SUBAGENT_DIR / "campaigns" / "2026-11-04" / "ai-players-day11-day12-vault"
IMAGES_DIR = OUT_ROOT / "images"
QA_GRID_D1112_PATH = OUT_ROOT / "bespoke_day11_day12_qa_grid.jpg"
MANIFEST_D1112_PATH = OUT_ROOT / "bespoke_day11_day12_manifest.json"


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


def card_37_mobile_cloudflare_tunnel() -> str:
    """Card 37: Left Smartphone Frame + Right 3-Tier Cloud Tunnel Bridge (Cyan #06B6D4 & Deep Navy #030A16)"""
    bg = "background: radial-gradient(circle at 22% 55%, rgba(6,182,212,0.32) 0%, transparent 55%), linear-gradient(135deg, #030A16 0%, #07192E 100%);"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:52px; right:52px; display:flex; justify-content:space-between; align-items:center;">
      <div style="background:#06B6D4; color:#030A16; font-weight:900; font-size:18px; padding:8px 22px; border-radius:999px;">📱 MOBILE COMMAND // CLOUDFLARED HTTPS TUNNEL</div>
      <div style="border:2px solid #22D3EE; color:#67E8F9; font-weight:800; font-size:17px; padding:6px 18px; border-radius:999px;">ZERO PORT-FORWARDING</div>
    </div>
    <div style="position:absolute; top:100px; left:52px; right:52px; font-size:44px; font-weight:900; line-height:1.1;">
      ĐIỀU KHIỂN <span style="color:#22D3EE;">VĂN PHÒNG 3D AI</span> TRÊN ĐIỆN THOẠI MỌI LÚC MỌI NƠI
    </div>

    <!-- Left Phone Mockup -->
    <div style="position:absolute; top:235px; left:52px; width:390px; bottom:52px; background:#071E36; border:5px solid #06B6D4; border-radius:46px; padding:26px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 24px 60px rgba(6,182,212,0.3);">
      <div style="width:120px; height:14px; background:#030A16; border-radius:999px; margin:0 auto;"></div>
      <div style="background:#0B2B4C; border:2px solid #22D3EE; border-radius:22px; padding:20px; text-align:center;">
        <div style="color:#67E8F9; font-size:16px; font-weight:800;">HTTPS ENCRYPTED STREAM</div>
        <div style="font-size:34px; font-weight:900; margin-top:6px;">11 AGENT 3D</div>
        <div style="font-size:17px; color:#CCFBF1; margin-top:6px;">Pin 1 dòng gọn nhẹ + Cụm phím D-Pad nổi bên phải</div>
      </div>
      <div style="background:#041324; border-radius:22px; padding:20px; border-left:6px solid #06B6D4;">
        <div style="color:#22D3EE; font-weight:900; font-size:18px;">💬 KHUNG CHAT DI ĐỘNG</div>
        <div style="font-size:21px; font-weight:800; margin-top:6px;">Cuộn mượt 60fps • Gửi lệnh trực tiếp vào Antigravity</div>
      </div>
      <div style="background:linear-gradient(90deg, #06B6D4, #0284C7); color:#030A16; font-weight:900; font-size:22px; padding:18px; border-radius:20px; text-align:center;">
        MỞ BẰNG 4G / 5G / WIFI
      </div>
    </div>

    <!-- Right 3-Tier Architecture -->
    <div style="position:absolute; top:235px; right:52px; width:545px; height:240px; background:#082038; border:3px solid #22D3EE; border-radius:28px; padding:28px;">
      <div style="color:#67E8F9; font-size:18px; font-weight:900;">TẦNG 01 // AUTO-START BOOTSTRAP</div>
      <div style="font-size:30px; font-weight:900; margin-top:8px;">Mở máy là tự bật ngầm 100%</div>
      <div style="font-size:19px; color:#E0F2FE; margin-top:10px; line-height:1.4;">Kết hợp Hook SessionStart + Windows Task Scheduler + Startup Folder trên cả máy công ty và máy nhà.</div>
    </div>

    <div style="position:absolute; top:505px; right:52px; width:545px; height:240px; background:#082038; border:3px solid #38BDF8; border-radius:28px; padding:28px;">
      <div style="color:#7DD3FC; font-size:18px; font-weight:900;">TẦNG 02 // CLOUDFLARED TRYCLOUDFLARE</div>
      <div style="font-size:30px; font-weight:900; margin-top:8px;">Tự động cấp phát đường hầm SSL</div>
      <div style="font-size:19px; color:#E0F2FE; margin-top:10px; line-height:1.4;">Không cần mở port modem, tự động đẩy link Mobile bảo mật kèm mã khóa ?k=8899 về Telegram.</div>
    </div>

    <div style="position:absolute; bottom:52px; right:52px; width:545px; height:250px; background:linear-gradient(135deg, #06B6D4 0%, #0369A1 100%); border-radius:28px; padding:28px; color:#030A16; display:flex; align-items:center; justify-content:space-between;">
      <div style="width:310px;">
        <div style="font-weight:900; font-size:19px; color:#E0F2FE;">BÌNH LUẬN NHẬN SCRIPT</div>
        <div style="font-size:34px; font-weight:900; color:#FFF; margin-top:6px;">GÕ "TUNNEL"</div>
        <div style="font-size:18px; color:#CFFAFE; margin-top:6px;">Tặng trọn bộ code bật Văn phòng 3D online trên điện thoại!</div>
      </div>
      <div style="width:155px; height:155px; background:#030A16; border-radius:26px; display:flex; flex-direction:column; align-items:center; justify-content:center; border:4px solid #67E8F9;">
        <div style="font-size:38px; font-weight:900; color:#22D3EE;">18ms</div>
        <div style="font-size:15px; font-weight:800; color:#FFF;">ĐỘ TRỄ RAM</div>
      </div>
    </div>
    </body></html>"""


def card_38_ram_transcript_cache() -> str:
    """Card 38: Top Speedometer Comparison Bar + Bottom Asymmetric 2-Column Benchmark (Electric Lime #84CC16 & Charcoal #0D1308)"""
    bg = "background: radial-gradient(circle at 80% 80%, rgba(132,204,22,0.28) 0%, transparent 58%), #0B1006;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:40px; left:52px; right:52px; background:#16230B; border:2.5px solid #84CC16; border-radius:24px; padding:24px 32px; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="color:#BEF264; font-weight:900; font-size:18px;">⚡ KỸ THUẬT TỐI ƯU BACKEND // RAM TRANSCRIPT CACHE</div>
        <div style="font-size:38px; font-weight:900; margin-top:6px;">GIẢM THỜI GIAN TẢI CHAT TỪ <span style="color:#F87171;">3.2 GIÂY</span> XUỐNG <span style="color:#A3E635;">18ms</span></div>
      </div>
      <div style="background:#84CC16; color:#0B1006; font-weight:900; font-size:32px; padding:16px 26px; border-radius:18px;">177× FASTER</div>
    </div>

    <!-- Middle Horizontal Bar Chart Comparison -->
    <div style="position:absolute; top:225px; left:52px; right:52px; height:290px; background:#121B0A; border:2px solid #4D7C0F; border-radius:28px; padding:30px; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="display:flex; justify-content:space-between; font-size:22px; font-weight:900; color:#FCA5A5; margin-bottom:10px;">
          <span>❌ CÁCH CŨ: Đọc lại file .jsonl từ ổ cứng mỗi 3.5 giây</span>
          <span>3.200 ms (Đơ giao diện)</span>
        </div>
        <div style="width:100%; height:38px; background:#271212; border-radius:999px; overflow:hidden;">
          <div style="width:96%; height:100%; background:linear-gradient(90deg, #EF4444, #B91C1C);"></div>
        </div>
      </div>
      <div>
        <div style="display:flex; justify-content:space-between; font-size:22px; font-weight:900; color:#BEF264; margin-bottom:10px;">
          <span>✅ CÁCH MỚI: Kiểm tra mtime + size trong RAM & Bundled Snapshot</span>
          <span>18 ms (Tức thì)</span>
        </div>
        <div style="width:100%; height:38px; background:#1A2E05; border-radius:999px; overflow:hidden;">
          <div style="width:8%; height:100%; background:#84CC16; box-shadow:0 0 20px #84CC16;"></div>
        </div>
      </div>
    </div>

    <!-- Bottom 3 Pillars -->
    <div style="position:absolute; bottom:52px; left:52px; width:305px; height:480px; background:#15200B; border:3px solid #65A30D; border-radius:28px; padding:26px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="background:#84CC16; color:#0B1006; font-weight:900; font-size:20px; padding:8px 16px; border-radius:12px; display:inline-block; width:fit-content;">BƯỚC 01</div>
      <div style="font-size:30px; font-weight:900; color:#ECFCCB;">Khóa chữ ký mtime & byte size</div>
      <div style="font-size:19px; color:#D9F99D; line-height:1.45;">Nếu file log chưa có dòng mới, trả thẳng kết quả từ bộ nhớ RAM trong 0.001 giây mà không mở file.</div>
      <div style="font-size:44px; font-weight:900; color:#A3E635;">0 DISK I/O</div>
    </div>

    <div style="position:absolute; bottom:52px; left:387px; width:305px; height:480px; background:#15200B; border:3px solid #84CC16; border-radius:28px; padding:26px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="background:#A3E635; color:#0B1006; font-weight:900; font-size:20px; padding:8px 16px; border-radius:12px; display:inline-block; width:fit-content;">BƯỚC 02</div>
      <div style="font-size:30px; font-weight:900; color:#ECFCCB;">Gộp chung vào gói /api/snapshot</div>
      <div style="font-size:19px; color:#D9F99D; line-height:1.45;">Loại bỏ hoàn toàn vòng lặp gọi API phụ trên điện thoại, mở khung chat là có sẵn tin nhắn ngay lập tức.</div>
      <div style="font-size:44px; font-weight:900; color:#A3E635;">1 REQUEST</div>
    </div>

    <div style="position:absolute; bottom:52px; right:52px; width:305px; height:480px; background:linear-gradient(160deg, #84CC16 0%, #4D7C0F 100%); border-radius:28px; padding:26px; color:#0B1006; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="background:#0B1006; color:#BEF264; font-weight:900; font-size:20px; padding:8px 16px; border-radius:12px; display:inline-block; width:fit-content;">BƯỚC 03</div>
      <div style="font-size:30px; font-weight:900;">Chống giật vị trí cuộn DOM</div>
      <div style="font-size:19px; font-weight:800; color:#1A2E05; line-height:1.45;">Chỉ cập nhật HTML khi chữ ký tin nhắn thực sự thay đổi, giúp vuốt đọc lịch sử dài mượt như ứng dụng gốc.</div>
      <div style="background:#0B1006; color:#FFF; padding:16px; border-radius:16px; font-weight:900; font-size:19px; text-align:center;">CMT "RAMCACHE" NHẬN CODE</div>
    </div>
    </body></html>"""


def card_39_outlier_post_finder() -> str:
    """Card 39: Central Scatter-Plot SVG with Outlier Spike + 4 Corner Badges (Coral Red #F43F5E & Wine Dark #19050B)"""
    bg = "background: radial-gradient(circle at 50% 50%, rgba(244,63,94,0.32) 0%, transparent 60%), #140409;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:52px; right:52px; text-align:center;">
      <div style="display:inline-block; background:#F43F5E; color:#FFF; font-weight:900; font-size:18px; padding:8px 26px; border-radius:999px;">🔥 SOCIAL INTELLIGENCE // OUTLIER POST FINDER</div>
      <div style="font-size:44px; font-weight:900; margin-top:12px; line-height:1.1;">CÔNG THỨC SĂN VIDEO <span style="color:#FB7185;">ĐỘT BIẾN GẤP 5 LẦN</span> MỨC TRUNG VỊ</div>
    </div>

    <!-- Central Radar / Chart Box -->
    <div style="position:absolute; top:230px; left:190px; right:190px; height:490px; background:#230711; border:4px solid #F43F5E; border-radius:36px; padding:28px; box-shadow:0 0 70px rgba(244,63,94,0.3);">
      <svg width="640" height="340" viewBox="0 0 640 340">
        <line x1="40" y1="290" x2="600" y2="290" stroke="#881337" stroke-width="4"/>
        <line x1="40" y1="200" x2="600" y2="200" stroke="#FB7185" stroke-width="3" stroke-dasharray="10,8"/>
        <text x="50" y="190" fill="#FDA4AF" font-size="18" font-weight="800">MỨC NỀN TRUNG VỊ (MEDIAN BASELINE = 1.0x)</text>
        <circle cx="110" cy="220" r="14" fill="#9F1239"/>
        <circle cx="195" cy="195" r="14" fill="#9F1239"/>
        <circle cx="280" cy="235" r="14" fill="#9F1239"/>
        <circle cx="370" cy="205" r="14" fill="#9F1239"/>
        <circle cx="455" cy="215" r="14" fill="#9F1239"/>
        <line x1="535" y1="290" x2="535" y2="55" stroke="#F43F5E" stroke-width="6"/>
        <circle cx="535" cy="55" r="28" fill="#F43F5E"/>
        <text x="350" y="55" fill="#FFF" font-size="24" font-weight="900">HUGE OUTLIER (≥ 5.0x)</text>
      </svg>
      <div style="background:#140409; border:2px solid #FB7185; border-radius:18px; padding:16px 24px; text-align:center; font-size:24px; font-weight:900; color:#FFE4E6;">
        Lift Score = Lượt xem bài đăng ÷ Trung vị 20 bài gần nhất
      </div>
    </div>

    <!-- Bottom 3 Action Cards -->
    <div style="position:absolute; bottom:48px; left:52px; width:305px; height:260px; background:#2A0814; border:2.5px solid #FB7185; border-radius:24px; padding:24px;">
      <div style="color:#FDA4AF; font-size:18px; font-weight:900;">TẠI SAO DÙNG TRUNG VỊ?</div>
      <div style="font-size:25px; font-weight:900; margin-top:10px;">Không bị 1 bài siêu viral làm lệch chuẩn</div>
      <div style="font-size:17px; color:#FECDD3; margin-top:8px;">Giúp phát hiện kênh nhỏ nhưng có bài nổ gấp 8 lần bình thường.</div>
    </div>

    <div style="position:absolute; bottom:48px; left:387px; width:305px; height:260px; background:#2A0814; border:2.5px solid #FB7185; border-radius:24px; padding:24px;">
      <div style="color:#FDA4AF; font-size:18px; font-weight:900;">NGƯỠNG ĐÁNH GIÁ</div>
      <div style="font-size:25px; font-weight:900; margin-top:10px;">≥ 2.0x: Strong Outlier<br>≥ 5.0x: Huge Outlier</div>
      <div style="font-size:17px; color:#FECDD3; margin-top:8px;">Chỉ bóc tách kịch bản của những bài vượt ngưỡng ≥ 2.0x.</div>
    </div>

    <div style="position:absolute; bottom:48px; right:52px; width:305px; height:260px; background:#F43F5E; color:#140409; border-radius:24px; padding:24px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="background:#140409; color:#FDA4AF; font-weight:900; font-size:17px; padding:6px 14px; border-radius:10px; width:fit-content;">0-TOKEN CLI SCRIPT</div>
      <div style="font-size:28px; font-weight:900; color:#FFF;">Tự động chấm điểm hàng loạt</div>
      <div style="background:#140409; color:#FFF; padding:14px; border-radius:14px; font-weight:900; font-size:18px; text-align:center;">BÌNH LUẬN "OUTLIER"</div>
    </div>
    </body></html>"""


def card_40_comment_mining_honeycomb() -> str:
    """Card 40: 6-Bucket Grid (3x2) on Left + Right Summary Pillar (Gold Yellow #EAB308 & Espresso #171204)"""
    bg = "background: radial-gradient(circle at 30% 60%, rgba(234,179,8,0.28) 0%, transparent 58%), #120E03;"
    buckets = [
        ("01. BUYING INTENT", "Hỏi giá, xin link, phí ship", "#EAB308", 52, 220),
        ("02. OBJECTIONS", "Sợ tốn điện, sợ nhảy át KTX", "#F59E0B", 365, 220),
        ("03. PAIN POINTS", "Phàn nàn đồ cũ nhanh hỏng", "#FACC15", 52, 495),
        ("04. QUESTIONS", "Hỏi kích thước, bảo hành", "#FDE047", 365, 495),
        ("05. PRAISE PROOF", "Điểm khách đã mua khen nhất", "#EAB308", 52, 770),
        ("06. EXACT SLANG", "Từ lóng nguyên văn của khách", "#F59E0B", 365, 770),
    ]
    b_html = ""
    for title, desc, col, lx, ty in buckets:
        b_html += f"""
        <div style="position:absolute; left:{lx}px; top:{ty}px; width:292px; height:250px; background:#211905; border:3px solid {col}; border-radius:26px; padding:24px; display:flex; flex-direction:column; justify-content:space-between;">
          <div style="background:{col}; color:#120E03; font-weight:900; font-size:17px; padding:6px 14px; border-radius:10px; width:fit-content;">{title}</div>
          <div style="font-size:26px; font-weight:900; color:#FEF9C3;">{desc}</div>
          <div style="font-size:16px; color:#FDE68A; font-weight:700;">Đưa thẳng vào Hook 3s & Pinned Comment</div>
        </div>
        """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:52px; right:52px;">
      <div style="color:#FACC15; font-weight:900; font-size:19px;">⛏️ COMMENT MINING // ĐÀO MỎ BÌNH LUẬN THỰC CHIẾN</div>
      <div style="font-size:44px; font-weight:900; margin-top:6px;">PHÂN LOẠI BÌNH LUẬN VÀO <span style="color:#FACC15;">6 NHÓM TÍN HIỆU MUA HÀNG</span></div>
    </div>
    {b_html}
    <!-- Right Tall Pillar -->
    <div style="position:absolute; top:220px; right:52px; width:345px; bottom:60px; background:linear-gradient(180deg, #EAB308 0%, #CA8A04 100%); border-radius:32px; padding:32px; color:#120E03; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="background:#120E03; color:#FACC15; font-weight:900; font-size:18px; padding:8px 18px; border-radius:12px; display:inline-block;">VOICE OF CUSTOMER</div>
        <div style="font-size:38px; font-weight:900; margin-top:18px; line-height:1.1;">Đừng tự bịa câu quảng cáo!</div>
        <div style="font-size:21px; font-weight:800; margin-top:16px; line-height:1.45; color:#271E05;">Hãy lấy đúng câu phàn nàn nhiều nhất của khách trên bài đối thủ làm câu mở đầu 3 giây đầu tiên.</div>
      </div>
      <div style="background:#120E03; color:#FFF; border-radius:24px; padding:24px; text-align:center;">
        <div style="font-size:52px; font-weight:900; color:#FACC15;">+68%</div>
        <div style="font-size:18px; font-weight:800; margin-top:4px;">TỶ LỆ CHỐT ĐƠN QUA BÌNH LUẬN</div>
      </div>
      <div style="background:#FEF08A; color:#120E03; padding:18px; border-radius:18px; font-weight:900; font-size:20px; text-align:center;">
        GÕ "MINING" NHẬN TOOL
      </div>
    </div>
    </body></html>"""


def card_41_transcript_intelligence_anatomy() -> str:
    """Card 41: Horizontal Waveform Timeline SVG + 4 Vertical Slice Columns (Violet #8B5CF6 & Indigo #0B051D)"""
    bg = "background: radial-gradient(circle at 50% 25%, rgba(139,92,246,0.34) 0%, transparent 58%), #090418;"
    slices = [
        ("00s – 03s", "EXACT HOOK", "Câu mở đầu phá vỡ quán tính lướt, cấm chào hỏi", "#A855F7", 52),
        ("03s – 10s", "PAIN & SETUP", "Xoáy thẳng bối cảnh phòng trọ, bàn làm việc", "#8B5CF6", 298),
        ("10s – 23s", "VISUAL PROOF", "Cận cảnh chứng minh Before / After thực tế", "#6366F1", 544),
        ("23s – 30s", "PAYOFF & CTA", "Lý do phải bấm ngay vào Bình luận ghim #1", "#EC4899", 790),
    ]
    s_html = ""
    for time_lbl, name, desc, col, lx in slices:
        s_html += f"""
        <div style="position:absolute; top:470px; left:{lx}px; width:236px; bottom:52px; background:#150B30; border:3px solid {col}; border-radius:26px; padding:24px; display:flex; flex-direction:column; justify-content:space-between;">
          <div style="background:{col}; color:#FFF; font-weight:900; font-size:22px; padding:10px 16px; border-radius:14px; text-align:center;">{time_lbl}</div>
          <div style="font-size:28px; font-weight:900; color:#F3E8FF;">{name}</div>
          <div style="font-size:19px; color:#DDD6FE; line-height:1.45;">{desc}</div>
          <div style="height:10px; background:{col}; border-radius:999px;"></div>
        </div>
        """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:52px; right:52px; display:flex; justify-content:space-between; align-items:center;">
      <div style="background:#8B5CF6; color:#FFF; font-weight:900; font-size:18px; padding:8px 22px; border-radius:999px;">🎙️ TRANSCRIPT INTELLIGENCE // GIẢI PHẪU LỜI THOẠI</div>
      <div style="color:#C4B5FD; font-weight:900; font-size:20px;">CHUẨN ≤ 85 TỪ / 30 GIÂY</div>
    </div>
    <div style="position:absolute; top:100px; left:52px; right:52px; font-size:44px; font-weight:900; line-height:1.1;">
      BÓC TÁCH KỊCH BẢN TRIỆU VIEW THÀNH <span style="color:#C084FC;">4 LÁT CẮT THỜI GIAN</span>
    </div>

    <!-- Waveform Timeline Box -->
    <div style="position:absolute; top:225px; left:52px; right:52px; height:215px; background:#13092B; border:2.5px solid #A855F7; border-radius:28px; padding:24px 36px; display:flex; align-items:center; justify-content:space-between;">
      <svg width="620" height="140" viewBox="0 0 620 140">
        <rect x="10" y="45" width="18" height="50" rx="6" fill="#A855F7"/>
        <rect x="40" y="15" width="18" height="110" rx="6" fill="#EC4899"/>
        <rect x="70" y="30" width="18" height="80" rx="6" fill="#A855F7"/>
        <rect x="100" y="50" width="18" height="40" rx="6" fill="#8B5CF6"/>
        <rect x="130" y="25" width="18" height="90" rx="6" fill="#8B5CF6"/>
        <rect x="160" y="40" width="18" height="60" rx="6" fill="#6366F1"/>
        <rect x="190" y="10" width="18" height="120" rx="6" fill="#EC4899"/>
        <rect x="220" y="35" width="18" height="70" rx="6" fill="#6366F1"/>
        <rect x="250" y="20" width="18" height="100" rx="6" fill="#A855F7"/>
        <rect x="280" y="45" width="18" height="50" rx="6" fill="#8B5CF6"/>
        <rect x="310" y="15" width="18" height="110" rx="6" fill="#EC4899"/>
        <rect x="340" y="30" width="18" height="80" rx="6" fill="#A855F7"/>
        <rect x="370" y="20" width="18" height="100" rx="6" fill="#6366F1"/>
        <rect x="400" y="40" width="18" height="60" rx="6" fill="#8B5CF6"/>
        <rect x="430" y="12" width="18" height="116" rx="6" fill="#EC4899"/>
        <rect x="460" y="35" width="18" height="70" rx="6" fill="#A855F7"/>
        <rect x="490" y="25" width="18" height="90" rx="6" fill="#6366F1"/>
        <rect x="520" y="45" width="18" height="50" rx="6" fill="#8B5CF6"/>
        <rect x="550" y="18" width="18" height="104" rx="6" fill="#EC4899"/>
      </svg>
      <div style="background:#8B5CF6; color:#FFF; padding:22px 28px; border-radius:22px; text-align:center; width:300px;">
        <div style="font-size:20px; font-weight:800;">BỘ LỌC LINTER TỰ ĐỘNG</div>
        <div style="font-size:28px; font-weight:900; margin-top:6px;">CẤM "XIN CHÀO" 3 GIÂY ĐẦU!</div>
      </div>
    </div>
    {s_html}
    </body></html>"""


def card_42_triple_layer_profile_firewall() -> str:
    """Card 42: Left Concentric Shield Rings SVG + Right 3 Security Lock Steps (Teal #14B8A6 & Abyssal Green #031614)"""
    bg = "background: radial-gradient(circle at 25% 55%, rgba(20,184,166,0.3) 0%, transparent 58%), #021210;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:52px; right:52px;">
      <div style="color:#2DD4BF; font-weight:900; font-size:19px;">🔒 LUẬT #4 // TRIPLE-LAYER PERSONAL PROFILE FIREWALL</div>
      <div style="font-size:44px; font-weight:900; margin-top:6px;">TƯỜNG LỬA 3 LỚP BẢO VỆ <span style="color:#2DD4BF;">TRANG CÁ NHÂN & MESSENGER</span></div>
    </div>

    <!-- Left Concentric Shield Box -->
    <div style="position:absolute; top:215px; left:52px; width:440px; bottom:52px; background:#052420; border:3px solid #14B8A6; border-radius:34px; padding:28px; display:flex; flex-direction:column; align-items:center; justify-content:space-between;">
      <svg width="360" height="360" viewBox="0 0 360 360">
        <circle cx="180" cy="180" r="160" fill="none" stroke="#0F766E" stroke-width="6" stroke-dasharray="14,10"/>
        <circle cx="180" cy="180" r="118" fill="none" stroke="#14B8A6" stroke-width="8"/>
        <circle cx="180" cy="180" r="76" fill="#14B8A6"/>
        <text x="180" y="172" text-anchor="middle" fill="#021210" font-size="28" font-weight="900">100%</text>
        <text x="180" y="202" text-anchor="middle" fill="#021210" font-size="18" font-weight="900">ISOLATED</text>
      </svg>
      <div style="background:#021210; border:2px solid #2DD4BF; border-radius:22px; padding:22px; text-align:center; width:100%;">
        <div style="color:#5EEAD4; font-size:18px; font-weight:900;">CHẾ ĐỘ AN TOÀN TUYỆT ĐỐI</div>
        <div style="font-size:26px; font-weight:900; margin-top:8px;">Phát hiện tên cá nhân → Dừng ngay lập tức!</div>
      </div>
      <div style="background:#14B8A6; color:#021210; width:100%; padding:18px; border-radius:18px; font-weight:900; font-size:21px; text-align:center;">
        GÕ "FIREWALL" NHẬN MÃ NGUỒN
      </div>
    </div>

    <!-- Right 3 Layers -->
    <div style="position:absolute; top:215px; right:52px; width:505px; height:250px; background:#062925; border-left:10px solid #2DD4BF; border-radius:24px; padding:26px;">
      <div style="color:#5EEAD4; font-size:18px; font-weight:900;">LỚP KHÓA 01 // SWITCH PROFILE VERIFICATION</div>
      <div style="font-size:28px; font-weight:900; margin-top:8px;">Tự động chuyển sang đúng Fanpage</div>
      <div style="font-size:19px; color:#CCFBF1; margin-top:8px; line-height:1.4;">Gọi hàm ensure_fanpage_active() trước mọi ca tương tác để đảm bảo đang đứng dưới danh nghĩa Fanpage.</div>
    </div>

    <div style="position:absolute; top:495px; right:52px; width:505px; height:250px; background:#062925; border-left:10px solid #14B8A6; border-radius:24px; padding:26px;">
      <div style="color:#5EEAD4; font-size:18px; font-weight:900;">LỚP KHÓA 02 // MESSENGER POPUP KILLER</div>
      <div style="font-size:28px; font-weight:900; margin-top:8px;">Tự động đóng mọi cửa sổ chat nổi</div>
      <div style="font-size:19px; color:#CCFBF1; margin-top:8px; line-height:1.4;">Quét DOM liên tục để đóng toàn bộ hộp thoại Messenger, không bao giờ gõ nhầm vào tin nhắn riêng tư.</div>
    </div>

    <div style="position:absolute; bottom:52px; right:52px; width:505px; height:250px; background:#062925; border-left:10px solid #0D9488; border-radius:24px; padding:26px;">
      <div style="color:#5EEAD4; font-size:18px; font-weight:900;">LỚP KHÓA 03 // ARIA-LABEL IDENTITY GATE</div>
      <div style="font-size:28px; font-weight:900; margin-top:8px;">Kiểm tra nhãn ô bình luận trước khi gõ</div>
      <div style="font-size:19px; color:#CCFBF1; margin-top:8px; line-height:1.4;">Chỉ cho phép gửi bình luận khi ô nhập liệu xác nhận đúng dòng "Bình luận dưới tên &lt;Tên Fanpage&gt;".</div>
    </div>
    </body></html>"""


def card_43_bot_chrome_cookie_vault() -> str:
    """Card 43: Top-Left PC Node + Bottom-Right PC Node + Center Vault Conduit (Sky Blue #38BDF8 & Midnight #05101F)"""
    bg = "background: radial-gradient(circle at 75% 25%, rgba(56,189,248,0.3) 0%, transparent 55%), #040D1A;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:52px; right:52px; display:flex; justify-content:space-between; align-items:center;">
      <div style="background:#38BDF8; color:#040D1A; font-weight:900; font-size:18px; padding:8px 22px; border-radius:999px;">🔄 CROSS-PC SESSION VAULT // PORT 9222 HEADLESS</div>
      <div style="border:2px solid #38BDF8; color:#7DD3FC; font-weight:800; font-size:17px; padding:6px 18px; border-radius:999px;">ZERO TASKKILL</div>
    </div>
    <div style="position:absolute; top:100px; left:52px; right:52px; font-size:44px; font-weight:900; line-height:1.1;">
      ĐỒNG BỘ <span style="color:#38BDF8;">PHIÊN ĐĂNG NHẬP BOT</span> GIỮA MÁY CÔNG TY & MÁY NHÀ
    </div>

    <!-- Top-Left Node: Company PC -->
    <div style="position:absolute; top:230px; left:52px; width:460px; height:260px; background:#0A1D37; border:3px solid #38BDF8; border-radius:28px; padding:26px;">
      <div style="color:#7DD3FC; font-weight:900; font-size:18px;">💻 NODE A // MÁY VĂN PHÒNG (Ổ D:\\)</div>
      <div style="font-size:30px; font-weight:900; margin-top:8px;">Chạy ngầm --headless=new</div>
      <div style="font-size:19px; color:#E0F2FE; margin-top:10px; line-height:1.4;">Không bật cửa sổ làm phiền, không đụng chạm tới trình duyệt Chrome cá nhân đang mở của bạn.</div>
    </div>

    <!-- Center Encrypted Vault Bar -->
    <div style="position:absolute; top:515px; left:52px; right:52px; height:210px; background:linear-gradient(90deg, #0284C7 0%, #2563EB 100%); border-radius:30px; padding:28px 36px; display:flex; align-items:center; justify-content:space-between; box-shadow:0 20px 50px rgba(37,99,235,0.35);">
      <div>
        <div style="color:#BAE6FD; font-weight:900; font-size:19px;">🔐 FB_BOT_SESSION_VAULT.JSON + GIT AUTO-SYNC</div>
        <div style="font-size:34px; font-weight:900; margin-top:6px;">Kết thúc ca → Tự động xuất Cookie & đóng trình duyệt</div>
        <div style="font-size:19px; color:#E0F2FE; margin-top:6px;">Giải phóng 100% RAM ngay trong khối finally:, đẩy thẳng phiên mới nhất lên kho đồng bộ.</div>
      </div>
      <div style="background:#040D1A; color:#38BDF8; font-weight:900; font-size:28px; padding:20px 28px; border-radius:22px; text-align:center; min-width:190px;">
        29 COOKIES<br><span style="font-size:16px; color:#FFF;">SYNCED ✓</span>
      </div>
    </div>

    <!-- Bottom-Left Stat -->
    <div style="position:absolute; bottom:52px; left:52px; width:460px; height:270px; background:#08182E; border:2.5px dashed #7DD3FC; border-radius:28px; padding:26px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="color:#38BDF8; font-weight:900; font-size:20px;">🛡️ BẢO VỆ CHROME CÁ NHÂN 100%</div>
      <div style="font-size:26px; font-weight:800;">Chỉ đóng đúng PID của cổng 9222, cấm vĩnh viễn lệnh taskkill toàn cục!</div>
      <div style="background:#38BDF8; color:#040D1A; padding:16px; border-radius:16px; font-weight:900; font-size:20px; text-align:center;">BÌNH LUẬN "VAULT" NHẬN CODE</div>
    </div>

    <!-- Bottom-Right Node: Home PC -->
    <div style="position:absolute; bottom:52px; right:52px; width:490px; height:270px; background:#0A1D37; border:3px solid #38BDF8; border-radius:28px; padding:26px;">
      <div style="color:#7DD3FC; font-weight:900; font-size:18px;">🏠 NODE B // MÁY Ở NHÀ (Ổ F:\\)</div>
      <div style="font-size:30px; font-weight:900; margin-top:8px;">Tự nạp Cookie qua CDP Network</div>
      <div style="font-size:19px; color:#E0F2FE; margin-top:10px; line-height:1.4;">Mở máy ở nhà lên là tiếp tục chạy 3 ca tương tác hội nhóm (12:00, 17:30, 20:30) không cần đăng nhập lại!</div>
    </div>
    </body></html>"""


def card_44_purge_on_upgrade_protocol() -> str:
    """Card 44: Top Legacy Purge vs Bottom Clean Gold Standard + Center Vortex (Orange Flame #F97316 & Obsidian #180B04)"""
    bg = "background: radial-gradient(circle at 50% 50%, rgba(249,115,22,0.3) 0%, transparent 60%), #140802;"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:52px; right:52px; text-align:center;">
      <div style="display:inline-block; background:#F97316; color:#140802; font-weight:900; font-size:18px; padding:8px 26px; border-radius:999px;">🔥 LUẬT #9 // PURGE-ON-UPGRADE PROTOCOL</div>
      <div style="font-size:44px; font-weight:900; margin-top:12px;">CÓ CHUẨN MỚI LÀ <span style="color:#FB923C;">XÓA VĨNH VIỄN</span> MẪU CŨ NGAY LẬP TỨC!</div>
    </div>

    <!-- Left Denied Legacy Box -->
    <div style="position:absolute; top:220px; left:52px; width:465px; height:480px; background:#260E05; border:3px solid #EF4444; border-radius:30px; padding:30px; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="background:#EF4444; color:#FFF; font-weight:900; font-size:19px; padding:8px 18px; border-radius:12px; width:fit-content;">❌ NGUY CƠ KHI GIỮ FILE CŨ</div>
      <div style="font-size:32px; font-weight:900; color:#FCA5A5; line-height:1.15;">AI Subagent đọc nhầm code cũ đã lỗi thời</div>
      <div style="font-size:20px; color:#FED7AA; line-height:1.45;">Khi trong thư mục tồn tại song song script cũ và script mới, các Agent rất dễ import nhầm mẫu cũ gây lặp lại lỗi thiết kế.</div>
      <div style="background:#140802; border:2px dashed #EF4444; padding:18px; border-radius:18px; font-size:22px; font-weight:900; color:#F87171; text-align:center;">
        ĐÃ XÓA SẠCH 72 FILE & THƯ MỤC CŨ
      </div>
    </div>

    <!-- Right Clean Upgrade Box -->
    <div style="position:absolute; top:220px; right:52px; width:465px; height:480px; background:linear-gradient(155deg, #F97316 0%, #EA580C 100%); border-radius:30px; padding:30px; color:#140802; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="background:#140802; color:#FDBA74; font-weight:900; font-size:19px; padding:8px 18px; border-radius:12px; width:fit-content;">✅ GIAO THỨC DỌN SẠCH TỰ ĐỘNG</div>
      <div style="font-size:32px; font-weight:900; color:#FFF; line-height:1.15;">Chỉ giữ lại duy nhất 1 nguồn sự thật (Single Source of Truth)</div>
      <div style="font-size:20px; font-weight:800; color:#2A1004; line-height:1.45;">Thực thi unlink & rmtree đồng thời trên cả Workspace chính lẫn kho Git đồng bộ đa máy ngay khi nâng cấp.</div>
      <div style="background:#140802; color:#FFF; padding:18px; border-radius:18px; font-size:22px; font-weight:900; text-align:center;">
        0% RỦI RO TÁI SỬ DỤNG MẪU LỖI
      </div>
    </div>

    <!-- Bottom Full-Width Action Bar -->
    <div style="position:absolute; bottom:52px; left:52px; right:52px; height:245px; background:#231006; border:3px solid #F97316; border-radius:28px; padding:28px 36px; display:flex; align-items:center; justify-content:space-between;">
      <div style="width:650px;">
        <div style="color:#FDBA74; font-weight:900; font-size:20px;">⚡ QUY TẮC VẬN HÀNH ĐỘI 10 SUBAGENT</div>
        <div style="font-size:32px; font-weight:900; margin-top:8px;">Bộ nhớ sạch = Đầu ra chuẩn xác 100%</div>
        <div style="font-size:19px; color:#FFEDD5; margin-top:6px;">Kết hợp cùng Cổng kiểm duyệt Bộ Não Thứ 2 trước mọi lệnh xuất bản.</div>
      </div>
      <div style="background:#F97316; color:#140802; font-weight:900; font-size:24px; padding:24px 32px; border-radius:22px; text-align:center;">
        GÕ "PURGE"<br><span style="font-size:17px;">NHẬN SCRIPT</span>
      </div>
    </div>
    </body></html>"""


def card_45_sqlite_n8n_zero_token_hub() -> str:
    """Card 45: 3 Horizontal Swimlanes + Right Database Cylinder Metric (Mint Green #10B981 & Slate #071712)"""
    bg = "background: radial-gradient(circle at 80% 50%, rgba(16,185,129,0.28) 0%, transparent 58%), #05120E;"
    lanes = [
        ("LUỒNG 01 // SQLITE LOCAL MCP", "Lưu trữ sản phẩm, link Shopee Affiliate & lịch sử bài đăng với chi phí 0 Token", "#10B981", 225),
        ("LUỒNG 02 // N8N WEBHOOK HUB (PORT 5678)", "Kích hoạt tự động chuỗi đăng bài đa kênh & đồng bộ số liệu chuyển đổi", "#34D399", 475),
        ("LUỒNG 03 // PYTHON CLI LINTERS", "Kiểm tra độ dài kịch bản ≤ 85 từ, băm SHA-256 chống trùng lặp dưới 0.1 giây", "#059669", 725),
    ]
    l_html = ""
    for title, desc, col, ty in lanes:
        l_html += f"""
        <div style="position:absolute; top:{ty}px; left:52px; width:630px; height:220px; background:#0A261E; border:3px solid {col}; border-radius:26px; padding:26px; display:flex; flex-direction:column; justify-content:center;">
          <div style="color:{col}; font-weight:900; font-size:19px;">{title}</div>
          <div style="font-size:28px; font-weight:900; color:#FFF; margin-top:10px; line-height:1.25;">{desc}</div>
        </div>
        """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:52px; right:52px;">
      <div style="color:#34D399; font-weight:900; font-size:19px;">⚙️ HYBRID ZERO-WASTE ARCHITECTURE // SQLITE + N8N</div>
      <div style="font-size:44px; font-weight:900; margin-top:6px;">TIẾT KIỆM <span style="color:#34D399;">85% TOKEN AI</span> NHỜ ĐẨY TÁC VỤ LẶP VỀ LOCAL SCRIPT</div>
    </div>
    {l_html}
    <!-- Right Vertical Metric Tower -->
    <div style="position:absolute; top:225px; right:52px; width:315px; bottom:135px; background:linear-gradient(180deg, #10B981 0%, #047857 100%); border-radius:30px; padding:30px; color:#05120E; display:flex; flex-direction:column; justify-content:space-between; text-align:center;">
      <div style="background:#05120E; color:#34D399; font-weight:900; font-size:18px; padding:10px; border-radius:14px;">TOKEN FIREWALL</div>
      <div>
        <div style="font-size:74px; font-weight:900; color:#FFF;">0₫</div>
        <div style="font-size:22px; font-weight:900; margin-top:6px;">CHI PHÍ LƯU TRỮ & KIỂM ĐỊNH</div>
      </div>
      <div style="font-size:19px; font-weight:800; color:#042F2E; line-height:1.4;">AI chỉ tập trung sáng tạo ý tưởng & duyệt chất lượng; việc nặng để Python & SQLite lo!</div>
      <div style="background:#05120E; color:#FFF; padding:18px; border-radius:18px; font-weight:900; font-size:20px;">GÕ "HYBRID" NHẬN SƠ ĐỒ</div>
    </div>
    </body></html>"""


def card_46_ad_library_teardown_matrix() -> str:
    """Card 46: 2x2 Quadrant Matrix in Center + Bottom CTA Strip (Hot Magenta #EC4899 & Plum #1A0614)"""
    bg = "background: radial-gradient(circle at 50% 45%, rgba(236,72,153,0.3) 0%, transparent 60%), #13040E;"
    quads = [
        ("GÓC 01 // REPEATED ADS", "Tìm quảng cáo đối thủ chạy lặp lại trên 14 ngày", "Đó mới là bài đang ra đơn thật, đừng copy bài mới chạy thử 1 ngày!", "#EC4899", 52, 220),
        ("GÓC 02 // PAIN CLUSTERING", "Gom cụm nỗi đau khách hàng đang bị bỏ ngỏ", "Đối thủ nói về giá rẻ? Hãy đánh vào độ bền và tính an toàn!", "#F472B6", 554, 220),
        ("GÓC 03 // VISUAL CONCEPT", "Giải phẫu 3 giây mở đầu của Top 5 bài thắng", "Họ dùng góc máy cận cảnh Macro hay tình huống phòng trọ?", "#DB2777", 52, 525),
        ("GÓC 04 // 3 GAP ANGLES", "Đề xuất 3 góc kịch bản mới không đụng hàng", "Đánh chiếm ngách thị trường trước khi đối thủ kịp nhận ra!", "#BE185D", 554, 525),
    ]
    q_html = ""
    for tag, title, sub, col, lx, ty in quads:
        q_html += f"""
        <div style="position:absolute; left:{lx}px; top:{ty}px; width:474px; height:280px; background:#24081B; border:3px solid {col}; border-radius:28px; padding:26px; display:flex; flex-direction:column; justify-content:space-between;">
          <div style="background:{col}; color:#FFF; font-weight:900; font-size:17px; padding:6px 16px; border-radius:10px; width:fit-content;">{tag}</div>
          <div style="font-size:29px; font-weight:900; color:#FCE7F3; line-height:1.18;">{title}</div>
          <div style="font-size:19px; color:#FBCFE8; line-height:1.4;">{sub}</div>
        </div>
        """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:52px; right:52px; text-align:center;">
      <div style="display:inline-block; background:#EC4899; color:#FFF; font-weight:900; font-size:18px; padding:8px 24px; border-radius:999px;">🕵️ AD LIBRARY TEARDOWN // GIẢI PHẪU QUẢNG CÁO ĐỐI THỦ</div>
      <div style="font-size:43px; font-weight:900; margin-top:10px;">MA TRẬN 4 GÓC TÌM <span style="color:#F472B6;">KHOẢNG TRỐNG THỊ TRƯỜNG (ANGLE GAP)</span></div>
    </div>
    {q_html}
    <div style="position:absolute; bottom:48px; left:52px; right:52px; height:180px; background:linear-gradient(90deg, #EC4899 0%, #9333EA 100%); border-radius:26px; padding:24px 36px; display:flex; align-items:center; justify-content:space-between;">
      <div>
        <div style="font-size:20px; font-weight:900; color:#FCE7F3;">🎯 QUY TẮC VÀNG CỦA SUBAGENT MKT</div>
        <div style="font-size:32px; font-weight:900; color:#FFF; margin-top:6px;">Chỉ học cấu trúc thắng — Tuyệt đối không đạo nhái nguyên xi!</div>
      </div>
      <div style="background:#13040E; color:#F472B6; font-weight:900; font-size:22px; padding:20px 28px; border-radius:18px; text-align:center;">
        CMT "TEARDOWN"
      </div>
    </div>
    </body></html>"""


def card_47_lead_magnet_50_prompts() -> str:
    """Card 47: Big Left Hero Box + Right 5-Step Stacked Ladder (Royal Blue #3B82F6 & Deep Space #060D21)"""
    bg = "background: radial-gradient(circle at 20% 50%, rgba(59,130,246,0.34) 0%, transparent 58%), #050B1C;"
    steps = [
        ("NHÓM 01", "10 Prompt Săn Sản Phẩm & Đào Bình Luận", "#3B82F6", 225),
        ("NHÓM 02", "10 Prompt Viết Kịch Bản Hook 3 Giây", "#60A5FA", 380),
        ("NHÓM 03", "10 Prompt Thiết Kế Ảnh & Video Độc Bản", "#2563EB", 535),
        ("NHÓM 04", "10 Prompt Chuyển Hóa Đa Kênh Tự Động", "#38BDF8", 690),
        ("NHÓM 05", "10 Prompt Phân Tích Phễu & Chốt Đơn", "#818CF8", 845),
    ]
    st_html = ""
    for tag, txt, col, ty in steps:
        st_html += f"""
        <div style="position:absolute; top:{ty}px; right:52px; width:535px; height:135px; background:#0C1938; border:2.5px solid {col}; border-radius:22px; padding:20px 26px; display:flex; align-items:center; justify-content:space-between;">
          <div>
            <div style="color:{col}; font-weight:900; font-size:17px;">{tag}</div>
            <div style="font-size:24px; font-weight:900; color:#FFF; margin-top:4px;">{txt}</div>
          </div>
          <div style="background:{col}; color:#050B1C; font-weight:900; font-size:20px; padding:10px 16px; border-radius:12px;">10×</div>
        </div>
        """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:52px; right:52px;">
      <div style="color:#60A5FA; font-weight:900; font-size:19px;">🎁 LEAD MAGNET #01 // BỘ QUÀ TẶNG ĐÓNG HỘP</div>
      <div style="font-size:44px; font-weight:900; margin-top:6px;">TRỌN BỘ <span style="color:#60A5FA;">50 PROMPT SUBAGENT</span> VẬN HÀNH PHÒNG MARKETING AI</div>
    </div>

    <!-- Left Hero Box -->
    <div style="position:absolute; top:225px; left:52px; width:415px; bottom:100px; background:linear-gradient(160deg, #2563EB 0%, #1D4ED8 100%); border-radius:34px; padding:34px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 24px 60px rgba(37,99,235,0.4);">
      <div style="background:#050B1C; color:#60A5FA; font-weight:900; font-size:18px; padding:8px 18px; border-radius:12px; width:fit-content;">COPY & PASTE READY</div>
      <div>
        <div style="font-size:88px; font-weight:900; line-height:1;">50</div>
        <div style="font-size:32px; font-weight:900; margin-top:8px;">PROMPT THỰC CHIẾN</div>
        <div style="font-size:19px; color:#DBEAFE; margin-top:12px; line-height:1.45;">Đã chuẩn hóa đầu vào, đầu ra và thang điểm kiểm duyệt Rubric 9.0/10 cho từng vị trí chuyên môn.</div>
      </div>
      <div style="background:#050B1C; color:#FFF; padding:20px; border-radius:20px; font-weight:900; font-size:21px; text-align:center; border:2px solid #93C5FD;">
        BÌNH LUẬN "50PROMPT"<br><span style="font-size:16px; color:#93C5FD;">TẢI MIỄN PHÍ TRONG ZALO VIP</span>
      </div>
    </div>
    {st_html}
    </body></html>"""


def card_48_funnel_audit_traffic_lights() -> str:
    """Card 48: 3 Vertical Traffic-Light Columns (Green KEEP, Amber ITERATE, Red STOP) (Neon Green #22C55E & Dark #08120B)"""
    bg = "background: radial-gradient(circle at 50% 80%, rgba(34,197,94,0.25) 0%, transparent 60%), #060E08;"
    cols = [
        ("🟢 KEEP & SCALE", "#22C55E", "#052E16", "Giữ & Nhân Bản", "3s Hold ≥ 65%\nCTR ≥ 3.5%\nĐơn hàng dương", "Tăng tần suất phân phối, tạo thêm 3 biến thể cùng góc tiếp cận thắng.", 52),
        ("🟡 ITERATE HOOK", "#F59E0B", "#271705", "Sửa Ngay 3s Đầu", "Xem hết cao nhưng\n3s đầu < 50%\nhoặc ít click link", "Giữ nguyên phần thân demo, thay câu mở đầu và tiêu đề ảnh bắt mắt hơn.", 387),
        ("🔴 STOP & PURGE", "#EF4444", "#2A0808", "Dừng Ngay Lập Tức", "3s Hold < 35%\nCTR < 1.0%\nsau 48 giờ test", "Không cố cứu sản phẩm sai tệp; chuyển ngân sách sang mã hàng mới.", 722),
    ]
    c_html = ""
    for badge, col, bg_box, title, metrics, action, lx in cols:
        c_html += f"""
        <div style="position:absolute; top:230px; left:{lx}px; width:305px; bottom:52px; background:{bg_box}; border:3.5px solid {col}; border-radius:30px; padding:28px; display:flex; flex-direction:column; justify-content:space-between;">
          <div style="background:{col}; color:#060E08; font-weight:900; font-size:20px; padding:10px 18px; border-radius:14px; text-align:center;">{badge}</div>
          <div style="font-size:32px; font-weight:900; color:#FFF; text-align:center;">{title}</div>
          <div style="background:#060E08; border:2px solid {col}; border-radius:20px; padding:20px; font-size:22px; font-weight:800; color:#F8FAFC; white-space:pre-line; line-height:1.5; text-align:center;">{metrics}</div>
          <div style="font-size:19px; color:#E2E8F0; line-height:1.45;">{action}</div>
          <div style="height:12px; background:{col}; border-radius:999px;"></div>
        </div>
        """
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_reset_css(bg)}</style></head><body>
    <div style="position:absolute; top:38px; left:52px; right:52px; text-align:center;">
      <div style="display:inline-block; background:#22C55E; color:#060E08; font-weight:900; font-size:18px; padding:8px 26px; border-radius:999px;">📊 SUBAGENT HIỆU SUẤT // DECISION MATRIX</div>
      <div style="font-size:44px; font-weight:900; margin-top:12px;">MA TRẬN RA QUYẾT ĐỊNH <span style="color:#4ADE80;">KEEP • ITERATE • STOP</span> SAU 48 GIỜ</div>
    </div>
    {c_html}
    </body></html>"""


CARDS_D1112_SPEC = [
    {
        "code": "card_37_mobile_cloudflare_tunnel",
        "slot_dt": "2026-11-05 08:30",
        "cta_kw": "TUNNEL",
        "builder": card_37_mobile_cloudflare_tunnel,
        "caption": (
            "📱 ĐIỀU KHIỂN VĂN PHÒNG ẢO 3D AI TRÊN ĐIỆN THOẠI MỌI LÚC MỌI NƠI QUA CLOUDFLARED TUNNEL!\n\n"
            "Không cần ngồi trước màn hình máy tính, giờ đây bạn có thể mở điện thoại bằng 4G/5G để quan sát trực tiếp 11 nhân sự AI đang làm việc và gửi lệnh thẳng vào Antigravity IDE:\n"
            "🔹 Tự động khởi chạy ngầm 100% khi bật máy ở cả công ty lẫn ở nhà.\n"
            "🔹 Cấp phát đường hầm HTTPS bảo mật kèm mã khóa riêng mà không cần mở port modem.\n"
            "🔹 Giao diện Mobile tối ưu: cụm phím điều hướng D-Pad nổi và khung chat tốc độ phản hồi 18ms.\n\n"
            "👇 Anh em muốn điều khiển hệ thống AI từ điện thoại bằng 1 chạm hay qua Telegram? Bình luận 'TUNNEL' hoặc xem Bình luận ghim #1 để lấy trọn bộ script nhé!"
        ),
    },
    {
        "code": "card_38_ram_transcript_cache",
        "slot_dt": "2026-11-05 10:15",
        "cta_kw": "RAMCACHE",
        "builder": card_38_ram_transcript_cache,
        "caption": (
            "⚡ TỐI ƯU BACKEND: GIẢM THỜI GIAN TẢI LỊCH SỬ CHAT AI TỪ 3.2 GIÂY XUỐNG CÒN 18ms!\n\n"
            "Khi file nhật ký hội thoại (.jsonl) của Agent phình to lên hàng chục MB, việc đọc lại ổ cứng mỗi 3 giây sẽ làm đơ cứng khung chat trên điện thoại. Đây là cách đội ngũ xử lý dứt điểm:\n"
            "1️⃣ Lưu chữ ký (mtime + byte size) trong bộ nhớ RAM: nếu file không đổi, trả kết quả ngay trong 0.001 giây.\n"
            "2️⃣ Đóng gói sẵn cuộc trò chuyện đang mở vào chung 1 gói tin duy nhất.\n"
            "3️⃣ Khóa chữ ký DOM trên trình duyệt để không làm nhảy vị trí khi đang vuốt đọc tin nhắn cũ.\n\n"
            "👇 Hệ thống của bạn có đang bị nghẽn cổ chai I/O không? Xem ngay Bình luận ghim #1 để tải mẫu kiến trúc RAM Cache nhé!"
        ),
    },
    {
        "code": "card_39_outlier_post_finder",
        "slot_dt": "2026-11-05 13:30",
        "cta_kw": "OUTLIER",
        "builder": card_39_outlier_post_finder,
        "caption": (
            "🔥 ĐỪNG NHÌN LƯỢT VIEW THÔ — HÃY TÍNH CHỈ SỐ ĐỘT BIẾN (OUTLIER LIFT SCORE ≥ 5.0x)!\n\n"
            "Một video 100.000 view trên kênh 2 triệu người theo dõi thực chất là một bài thất bại. Ngược lại, một video 50.000 view trên kênh mới lập 500 người theo dõi chính là mỏ vàng cần giải phẫu ngay:\n"
            "✅ Bước 1: Quét 20 bài đăng gần nhất của kênh đối thủ.\n"
            "✅ Bước 2: Tính mức Trung vị (Median) thay vì Trung bình cộng để không bị lệch chuẩn.\n"
            "✅ Bước 3: Chỉ mổ xẻ những bài có Lift Score vượt ngưỡng từ 2.0x đến 5.0x trở lên.\n\n"
            "👇 Bạn đang tìm ý tưởng theo cảm tính hay theo dữ liệu Outlier? Bấm vào Bình luận ghim #1 để nhận công cụ Python chấm điểm tự động!"
        ),
    },
    {
        "code": "card_40_comment_mining_honeycomb",
        "slot_dt": "2026-11-05 15:15",
        "cta_kw": "MINING",
        "builder": card_40_comment_mining_honeycomb,
        "caption": (
            "⛏️ ĐÀO MỎ BÌNH LUẬN (COMMENT MINING): LẤY ĐÚNG NGÔN NGỮ KHÁCH HÀNG ĐỂ VIẾT HOOK 3 GIÂY!\n\n"
            "Tại sao kịch bản AI viết ra nghe rất bóng bẩy nhưng khách lại lướt qua? Vì nó thiếu ngôn ngữ đời thực của người mua! Hãy phân loại bình luận vào 6 rổ tín hiệu:\n"
            "🔸 Nhóm 1 (Buying Intent): Khách hỏi giá, xin link, hỏi combo.\n"
            "🔸 Nhóm 2 (Objections): Rào cản sợ tốn điện, sợ ký túc xá cấm dùng, sợ hàng mỏng.\n"
            "🔸 Nhóm 3–6: Nỗi đau thực tế, thắc mắc tính năng, lời khen sau mua và từ lóng nguyên văn.\n\n"
            "👇 Lấy ngay câu phàn nàn nhiều nhất của khách làm câu mở đầu! Nhận script phân loại bình luận tại Bình luận ghim #1 nhé!"
        ),
    },
    {
        "code": "card_41_transcript_intelligence_anatomy",
        "slot_dt": "2026-11-05 18:15",
        "cta_kw": "TRANSCRIPT",
        "builder": card_41_transcript_intelligence_anatomy,
        "caption": (
            "🎙️ GIẢI PHẪU LỜI THOẠI (TRANSCRIPT INTELLIGENCE): 4 LÁT CẮT CỦA VIDEO NGẮN CHUYỂN ĐỔI CAO!\n\n"
            "Mọi video ngắn 30 giây giữ chân người xem trên 65% đều tuân thủ nghiêm ngặt nhịp độ 4 chặng và giới hạn dưới 85 từ:\n"
            "⏱️ [00–03s] Exact Hook: Câu hỏi xoáy nỗi đau hoặc cảnh báo trực diện (tuyệt đối cấm chào hỏi).\n"
            "⏱️ [03–10s] Pain & Setup: Đặt ngay vào bối cảnh phòng trọ, ký túc xá hoặc bàn làm việc.\n"
            "⏱️ [10–23s] Visual Proof: Chứng minh bằng hình ảnh Before/After rõ nét.\n"
            "⏱️ [23–30s] Payoff & CTA: Chỉ dẫn dứt khoát xuống Bình luận ghim #1.\n\n"
            "👇 Tải ngay bộ Linter kiểm tra kịch bản tự động ở Bình luận ghim #1!"
        ),
    },
    {
        "code": "card_42_triple_layer_profile_firewall",
        "slot_dt": "2026-11-05 21:15",
        "cta_kw": "FIREWALL",
        "builder": card_42_triple_layer_profile_firewall,
        "caption": (
            "🔒 TƯỜNG LỬA 3 LỚP BẢO VỆ TRANG CÁ NHÂN & MESSENGER KHI CHẠY BOT TƯƠNG TÁC TỰ ĐỘNG!\n\n"
            "Sai lầm nguy hiểm nhất khi dùng trình duyệt tự động đi seeding hội nhóm là để Bot dùng nhầm nick cá nhân hoặc gõ nhầm vào cửa sổ chat Messenger. Đây là 3 chốt chặn bắt buộc:\n"
            "🛡️ Lớp 1: Tự động chuyển hồ sơ (Switch Profile) sang đúng Fanpage trước mỗi ca chạy.\n"
            "🛡️ Lớp 2: Quét và đóng toàn bộ popup Messenger nổi trên màn hình.\n"
            "🛡️ Lớp 3: Kiểm tra thuộc tính aria-label của ô nhập liệu — chỉ gõ khi xác nhận đúng tên Fanpage.\n\n"
            "👇 Xem chi tiết mã nguồn Tường Lửa 3 Lớp tại Bình luận ghim #1!"
        ),
    },
    {
        "code": "card_43_bot_chrome_cookie_vault",
        "slot_dt": "2026-11-06 08:30",
        "cta_kw": "VAULT",
        "builder": card_43_bot_chrome_cookie_vault,
        "caption": (
            "🔄 ĐỒNG BỘ PHIÊN ĐĂNG NHẬP BOT GIỮA MÁY CÔNG TY & MÁY NHÀ KHÔNG CẦN LOGIN LẠI!\n\n"
            "Làm sao để Bot chạy ngầm ở công ty lúc 12:00 trưa, rồi tối về nhà lúc 20:30 tự động chạy tiếp mà không bao giờ hỏi mật khẩu hay mã 2FA?\n"
            "🔹 Khởi chạy trình duyệt Bot độc lập ở cổng 9222 với chế độ chạy ngầm --headless=new.\n"
            "🔹 Ngay khi kết thúc ca tương tác, tự động trích xuất Cookie lưu vào Vault và đóng trình duyệt giải phóng RAM.\n"
            "🔹 Tuyệt đối không dùng lệnh taskkill toàn cục làm ảnh hưởng đến trình duyệt làm việc của bạn.\n\n"
            "👇 Nhận ngay kiến trúc Cross-PC Session Vault tại Bình luận ghim #1!"
        ),
    },
    {
        "code": "card_44_purge_on_upgrade_protocol",
        "slot_dt": "2026-11-06 10:15",
        "cta_kw": "PURGE",
        "builder": card_44_purge_on_upgrade_protocol,
        "caption": (
            "🔥 GIAO THỨC PURGE-ON-UPGRADE: TẠI SAO PHẢI XÓA SẠCH CODE & MẪU CŨ NGAY KHI CÓ CHUẨN MỚI?\n\n"
            "Khi vận hành đội ngũ 10 AI Subagent, nếu bạn giữ lại các thư mục mẫu cũ đã lỗi thời, sớm muộn cũng có Agent đọc nhầm và sản xuất ra phiên bản cũ. Quy tắc sống còn:\n"
            "1️⃣ Ngay khi chốt quy chuẩn thiết kế mới, chạy script dọn sạch toàn bộ mẫu cũ trên cả máy chính lẫn kho đồng bộ Git.\n"
            "2️⃣ Chỉ để lại duy nhất 1 nguồn sự thật (Single Source of Truth) trong codebase.\n"
            "3️⃣ Khóa cổng kiểm duyệt Bộ Não Thứ 2 để chặn mọi tham chiếu tới quy tắc cũ.\n\n"
            "👇 Bấm vào Bình luận ghim #1 để tải bộ quy tắc quản trị bộ nhớ sạch cho đội Agent!"
        ),
    },
    {
        "code": "card_45_sqlite_n8n_zero_token_hub",
        "slot_dt": "2026-11-06 13:30",
        "cta_kw": "HYBRID",
        "builder": card_45_sqlite_n8n_zero_token_hub,
        "caption": (
            "⚙️ KIẾN TRÚC HYBRID ZERO-WASTE: TIẾT KIỆM 85% TOKEN NHỜ KẾT HỢP GEMINI 4 + SQLITE + N8N!\n\n"
            "Đừng bắt mô hình AI đắt đỏ phải làm những việc lặp đi lặp lại như đếm chữ, nối chuỗi link hay lưu bảng dữ liệu:\n"
            "🟢 Giao cho AI: Nghiên cứu góc tiếp cận, sáng tạo kịch bản và kiểm duyệt chất lượng.\n"
            "🟢 Giao cho SQLite & Python CLI: Lưu trữ danh mục sản phẩm, kiểm tra trùng lặp SHA-256 và xuất file với chi phí 0 đồng.\n"
            "🟢 Giao cho n8n Local: Tự động hóa lịch đăng và báo cáo về Telegram.\n\n"
            "👇 Tải trọn bộ sơ đồ kết nối MCP SQLite + n8n tại Bình luận ghim #1 nhé!"
        ),
    },
    {
        "code": "card_46_ad_library_teardown_matrix",
        "slot_dt": "2026-11-06 15:15",
        "cta_kw": "TEARDOWN",
        "builder": card_46_ad_library_teardown_matrix,
        "caption": (
            "🕵️ MA TRẬN GIẢI PHẪU QUẢNG CÁO ĐỐI THỦ (AD LIBRARY TEARDOWN) TÌM KHOẢNG TRỐNG THỊ TRƯỜNG!\n\n"
            "Đừng nhìn thấy một quảng cáo đang bật mà vội kết luận nó đang ra đơn khủng. Hãy dùng quy trình 4 bước của Subagent MKT:\n"
            "1️⃣ Lọc các quảng cáo chạy lặp lại dài ngày (Repeated Ads > 14 ngày).\n"
            "2️⃣ Gom cụm thông điệp theo: Nỗi đau -> Ưu đãi -> Bối cảnh hình ảnh.\n"
            "3️⃣ Tìm ra 3 góc tiếp cận mới (Gap Angles) mà đối thủ đang bỏ trống.\n\n"
            "👇 Nhận ngay mẫu prompt Ad Library Teardown tại Bình luận ghim #1!"
        ),
    },
    {
        "code": "card_47_lead_magnet_50_prompts",
        "slot_dt": "2026-11-06 18:15",
        "cta_kw": "50PROMPT",
        "builder": card_47_lead_magnet_50_prompts,
        "caption": (
            "🎁 TẶNG MIỄN PHÍ: BỘ 50 PROMPT SUBAGENT ĐÓNG HỘP VẬN HÀNH PHÒNG MARKETING TỰ ĐỘNG!\n\n"
            "Toàn bộ hệ thống câu lệnh thực chiến đã được chia sẵn thành 5 nhóm chuyên môn để bạn copy vào dùng ngay:\n"
            "📌 10 Prompt Nghiên cứu thị trường & Đào bình luận khách hàng.\n"
            "📌 10 Prompt Viết kịch bản video ngắn & Hook 3 giây.\n"
            "📌 10 Prompt Thiết kế hình ảnh & Storyboard chuyển động.\n"
            "📌 10 Prompt Biến thể nội dung đa kênh & Chăm sóc bình luận.\n"
            "📌 10 Prompt Phân tích phễu chuyển đổi & Tối ưu hiệu suất.\n\n"
            "👇 Bình luận '50PROMPT' hoặc bấm thẳng vào link ở Bình luận ghim #1 để nhận toàn bộ tài liệu nhé!"
        ),
    },
    {
        "code": "card_48_funnel_audit_traffic_lights",
        "slot_dt": "2026-11-06 21:15",
        "cta_kw": "FUNNEL",
        "builder": card_48_funnel_audit_traffic_lights,
        "caption": (
            "📊 MA TRẬN ĐÈN GIAO THÔNG (KEEP • ITERATE • STOP): ĐỌC SỐ LIỆU SAU 48 GIỜ ĐỂ TỐI ƯU CHUYỂN ĐỔI!\n\n"
            "Sau khi xuất bản nội dung 48 giờ, Subagent Hiệu Suất sẽ tự động phân tích phễu 3 tầng và ra quyết định dứt khoát:\n"
            "🟢 KEEP (Giữ & Nhân bản): Tỷ lệ giữ chân 3s đầu ≥ 65%, tỷ lệ bấm link ≥ 3.5% -> Nhân bản ngay 3 biến thể mới.\n"
            "🟡 ITERATE (Sửa Hook): Nội dung giữa tốt nhưng 3s đầu rơi rụng nhiều -> Giữ phần thân, làm lại tiêu đề và mở đầu.\n"
            "🔴 STOP (Dừng ngay): Cả giữ chân lẫn tương tác đều thấp -> Dừng ngay để tập trung nguồn lực cho chủ đề thắng.\n\n"
            "👇 Lấy bảng tính Funnel tự động tại Bình luận ghim #1!"
        ),
    },
]


def build_qa_grid(image_paths: list[Path], out_grid: Path) -> None:
    cols, rows = 4, 3
    cell = 320
    canvas = Image.new("RGB", (cols * cell, rows * cell), (9, 13, 22))
    for idx, p in enumerate(image_paths[:12]):
        with Image.open(p) as im:
            thumb = im.convert("RGB").resize((cell - 12, cell - 12), Image.Resampling.LANCZOS)
            x = (idx % cols) * cell + 6
            y = (idx // cols) * cell + 6
            canvas.paste(thumb, (x, y))
    canvas.save(out_grid, format="JPEG", quality=92, optimize=True)


def schedule_12_cards(manifest_items: list[dict]) -> list[dict]:
    import requests
    from mama_auto_scheduler_engine import load_vault, graph_post

    pages = load_vault()
    tok = pages[AI_PAGE_ID]["access_token"]
    now_ts = int(dt.datetime.now(VN_TZ).timestamp())

    for item in manifest_items:
        img_path = Path(item["image_path"])
        dt_obj = dt.datetime.strptime(item["slot_dt"], "%Y-%m-%d %H:%M").replace(tzinfo=VN_TZ)
        sched_ts = int(dt_obj.timestamp())
        if sched_ts <= now_ts + 900:
            sched_ts = now_ts + 1200

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
        time.sleep(1.0)
    return manifest_items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true", help="Hẹn giờ 12 bài ảnh độc bản ngày 05/11 & 06/11 lên Page AI Players")
    args = parser.parse_args()

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    rendered_paths = []
    manifest_items = []

    print("🎨 Đang kết xuất 12 Ảnh Bài Đăng Độc Bản Tiếp Theo (Card 37..48 — Ngày 05/11 & 06/11)...")
    for idx, spec in enumerate(CARDS_D1112_SPEC, 37):
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
        print(f"  ✔ [{idx:02d}/48] Đã render thiết kế độc bản: {out_jpg.name}", flush=True)

    ok, gate_msg = verify_zero_clone_images(IMAGES_DIR, max_similarity=0.58)
    print(("🛡️ " if ok else "🛑 ") + gate_msg, flush=True)
    if not ok:
        sys.exit(1)

    build_qa_grid(rendered_paths, QA_GRID_D1112_PATH)
    print(f"🖼️ Đã tạo bảng QA Grid 12 thiết kế độc bản (05/11 - 06/11) tại: {QA_GRID_D1112_PATH}", flush=True)

    if args.publish:
        manifest_items = schedule_12_cards(manifest_items)

    MANIFEST_D1112_PATH.write_text(json.dumps(manifest_items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📄 Đã lưu Manifest tại: {MANIFEST_D1112_PATH}", flush=True)


if __name__ == "__main__":
    main()
