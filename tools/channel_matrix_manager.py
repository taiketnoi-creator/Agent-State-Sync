#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
channel_matrix_manager.py — Hệ Thống Quản Trị Ma Trận Đa Kênh (16 -> 100 Kênh) 0-Token.

Giải quyết triệt để bài toán:
1. Gom nhóm theo mô hình "Brand Pod" (1 Pod = 1 Thương hiệu/Ngách = 4 Kênh: FB + IG + Threads + YouTube).
2. Lưu trữ tập trung vào SQLite (`aff_system.db`) gồm 3 bảng mới:
   - `brand_pods`: Quản lý 25 Cụm thương hiệu (4 Pod Active = 16 kênh, 21 Pod Dự phòng = 84 kênh -> Tổng 100 kênh).
   - `channels`: Định danh từng kênh (`POD01_FB`, `POD01_IG`, `POD01_TH`, `POD01_YT`), khóa cứng vị trí đặt link, khung giờ đăng lệch pha, Chrome Profile và IP/Proxy Group.
   - `multi_channel_posts`: Hàng đợi xuất bản đa kênh có kiểm soát (`Content Firewall` chống đăng nhầm kênh bán hàng và kênh khóa học AI).
3. Tự động sinh bộ Link Shopee Affiliate (`Sub_ID` 5 chiều) hoặc Link Phễu `AI Players` (`UTM`) chuẩn xác cho cả 4 nền tảng của từng Pod.

Cách sử dụng:
  python tools/channel_matrix_manager.py --init
  python tools/channel_matrix_manager.py --dashboard
  python tools/channel_matrix_manager.py --pod POD-01
  python tools/channel_matrix_manager.py --generate-pack --pod POD-01 --sku quat_imi_01 --url "https://shopee.vn/product/123/456" --title "Quạt cầm tay sò lạnh iMI"
"""

import argparse
import datetime
import json
import os
import sqlite3
import sys
import urllib.parse
from pathlib import Path

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
SCRATCH_DB = Path.home() / ".gemini" / "antigravity" / "scratch" / "ai-aff-video-system" / "data" / "aff_system.db"
FALLBACK_DB = SUBAGENT_DIR / "database" / "aff_system.db"
FB_ENV_PATH = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / ".env"
DEFAULT_SHOPEE_AFF_ID = "17395830088"


def get_db_path() -> Path:
    if SCRATCH_DB.parent.exists():
        return SCRATCH_DB
    FALLBACK_DB.parent.mkdir(parents=True, exist_ok=True)
    return FALLBACK_DB


def get_shopee_aff_id() -> str:
    if FB_ENV_PATH.exists():
        for line in FB_ENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.strip().startswith("SHOPEE_AFFILIATE_ID="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val
    return os.environ.get("SHOPEE_AFFILIATE_ID", DEFAULT_SHOPEE_AFF_ID)


# Danh sách 4 Brand Pods chủ lực giai đoạn 1 (16 Kênh) + 21 Brand Pods mở rộng (tổng 25 Pods = 100 Kênh)
BRAND_PODS_SEED = [
    # --- GIAI ĐOẠN 1: 4 POD CHỦ LỰC ĐANG VẬN HÀNH (16 KÊNH) ---
    {
        "pod_id": "POD-01",
        "pod_code": "pthetcuu",
        "pod_name": "Phòng Trọ Hết Cứu",
        "cluster_group": "CỤM 1: Sinh viên & Phòng trọ",
        "business_model": "SHOPEE_AFFILIATE",
        "target_audience": "Sinh viên, người thuê trọ 18-26t cần đồ cứu cánh giá rẻ < 200k",
        "content_firewall": "CHỈ đăng đồ gia dụng mini, decor trọ, cứu nóng/ẩm mốc. CẤM đăng khóa học AI.",
        "fb_page_id": "1442323328956326",
        "handle_base": "phongtrohetcuu",
        "browser_profile": "Chrome_Profile_01_Meta_SV",
        "proxy_group": "VN_RESIDENTIAL_IP_01",
        "phase_status": "PHASE_1_ACTIVE",
    },
    {
        "pod_id": "POD-02",
        "pod_code": "ktxcobien",
        "pod_name": "Ký Túc Xá Có Biến",
        "cluster_group": "CỤM 1: Sinh viên & Phòng trọ",
        "business_model": "SHOPEE_AFFILIATE",
        "target_audience": "Sinh viên KTX, GenZ thích drama phòng trọ & đồ tiện ích thông minh",
        "content_firewall": "CHỈ đăng POV tình huống KTX, drama bạn cùng phòng & đồ tiện ích < 150k.",
        "fb_page_id": "1421270697727753",
        "handle_base": "kytucxacobien",
        "browser_profile": "Chrome_Profile_01_Meta_SV",
        "proxy_group": "VN_RESIDENTIAL_IP_01",
        "phase_status": "PHASE_1_ACTIVE",
    },
    {
        "pod_id": "POD-03",
        "pod_code": "hoideadline",
        "pod_name": "Hội Deadline",
        "cluster_group": "CỤM 2: Văn phòng & Góc làm việc",
        "business_model": "SHOPEE_AFFILIATE",
        "target_audience": "Dân văn phòng, freelancer 22-35t đau mỏi cổ vai gáy, nghiện setup bàn làm việc",
        "content_firewall": "CHỈ đăng phụ kiện công thái học, đồ công nghệ bàn làm việc, cứu mỏi lưng/cổ.",
        "fb_page_id": "1407231352464711",
        "handle_base": "hoideadline.vn",
        "browser_profile": "Chrome_Profile_02_Meta_VP",
        "proxy_group": "VN_RESIDENTIAL_IP_02",
        "phase_status": "PHASE_1_ACTIVE",
    },
    {
        "pod_id": "POD-04",
        "pod_code": "aiplayers",
        "pod_name": "AI Players - Người chơi hệ AI",
        "cluster_group": "CỤM ĐẶC BIỆT: Cộng đồng & Khóa học AI",
        "business_model": "LEAD_COURSE_FUNNEL",
        "target_audience": "Người đi làm, chủ shop, creator muốn dùng AI & Subagent tự động hóa X10 hiệu suất",
        "content_firewall": "CHỈ đăng kiến thức AI, Subagent, Lead Magnet & dẫn phễu Zalo/Khóa học. CẤM bán đồ gia dụng lặt vặt.",
        "fb_page_id": "1022527194267367",
        "handle_base": "aiplayers.vn",
        "browser_profile": "Chrome_Profile_03_AI_Education",
        "proxy_group": "VN_RESIDENTIAL_IP_03",
        "phase_status": "PHASE_1_ACTIVE",
    },
    # --- GIAI ĐOẠN 2 & 3: LỘ TRÌNH MỞ RỘNG LÊN 25 PODS = 100 KÊNH ---
    {"pod_id": "POD-05", "pod_code": "banhocdaichien", "pod_name": "Bàn Học Đại Chiến", "cluster_group": "CỤM 1: Sinh viên & Phòng trọ", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Học sinh, sinh viên decor góc học tập", "content_firewall": "Đồ học tập, đèn bàn, giá sách mini", "fb_page_id": "PENDING", "handle_base": "banhocdaichien", "browser_profile": "Profile_04", "proxy_group": "VN_IP_04", "phase_status": "PHASE_2_READY"},
    {"pod_id": "POD-06", "pod_code": "toigiannuamua", "pod_name": "Tối Giản Nửa Mùa", "cluster_group": "CỤM 1: Sinh viên & Phòng trọ", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Người trẻ thích dọn phòng gọn gàng", "content_firewall": "Hộp收纳, kệ đa năng, đồ lưu trữ", "fb_page_id": "PENDING", "handle_base": "toigiannuamua", "browser_profile": "Profile_04", "proxy_group": "VN_IP_04", "phase_status": "PHASE_2_READY"},
    {"pod_id": "POD-07", "pod_code": "dorecuudeadline", "pod_name": "Đồ Rẻ Cứu Deadline", "cluster_group": "CỤM 1: Sinh viên & Phòng trọ", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Sinh viên chạy đồ án thức đêm", "content_firewall": "Đồ công nghệ giá sinh viên < 150k", "fb_page_id": "PENDING", "handle_base": "dorecuudeadline", "browser_profile": "Profile_05", "proxy_group": "VN_IP_05", "phase_status": "PHASE_2_READY"},
    {"pod_id": "POD-08", "pod_code": "vanphonghetpin", "pod_name": "Văn Phòng Hết Pin", "cluster_group": "CỤM 2: Văn phòng & Góc làm việc", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Nhân viên văn phòng cần nạp năng lượng trưa", "content_firewall": "Gối ngủ trưa, máy massage mini, bình giữ nhiệt", "fb_page_id": "PENDING", "handle_base": "vanphonghetpin", "browser_profile": "Profile_05", "proxy_group": "VN_IP_05", "phase_status": "PHASE_2_READY"},
    {"pod_id": "POD-09", "pod_code": "goclamviecbietnoi", "pod_name": "Góc Làm Việc Biết Nói", "cluster_group": "CỤM 2: Văn phòng & Góc làm việc", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Dân IT, Designer mê desk setup", "content_firewall": "Đèn màn hình, kê tay, hub chuyển đổi", "fb_page_id": "PENDING", "handle_base": "goclamviecbietnoi", "browser_profile": "Profile_06", "proxy_group": "VN_IP_06", "phase_status": "PHASE_2_READY"},
    {"pod_id": "POD-10", "pod_code": "dongnghiepmuondo", "pod_name": "Đồng Nghiệp Mượn Đồ", "cluster_group": "CỤM 2: Văn phòng & Góc làm việc", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Dân công sở thích đồ độc lạ ai nhìn cũng hỏi", "content_firewall": "Văn phòng phẩm thông minh, quạt để bàn", "fb_page_id": "PENDING", "handle_base": "dongnghiepmuondo", "browser_profile": "Profile_06", "proxy_group": "VN_IP_06", "phase_status": "PHASE_2_READY"},
    {"pod_id": "POD-11", "pod_code": "5phuttruoccuochop", "pod_name": "5 Phút Trước Cuộc Họp", "cluster_group": "CỤM 2: Văn phòng & Góc làm việc", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Dân công sở cần chỉnh chu nhanh gọn", "content_firewall": "Bàn ủi hơi nước mini, cây lăn bụi, máy cạo lông xù", "fb_page_id": "PENDING", "handle_base": "5phuttruochop", "browser_profile": "Profile_07", "proxy_group": "VN_IP_07", "phase_status": "PHASE_3_SCALE"},
    {"pod_id": "POD-12", "pod_code": "nhanhomlamchuyen", "pod_name": "Nhà Nhỏ Lắm Chuyện", "cluster_group": "CỤM 3: Gia dụng mini & Theo mùa", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Gia đình trẻ ở chung cư nhỏ", "content_firewall": "Gia dụng tiết kiệm diện tích, vệ sinh nhà cửa", "fb_page_id": "PENDING", "handle_base": "nhanholamchuyen", "browser_profile": "Profile_07", "proxy_group": "VN_IP_07", "phase_status": "PHASE_3_SCALE"},
    {"pod_id": "POD-13", "pod_code": "bepminicodrama", "pod_name": "Bếp Mini Có Drama", "cluster_group": "CỤM 3: Gia dụng mini & Theo mùa", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Người độc thân & sinh viên nấu ăn nhanh", "content_firewall": "Nồi điện mini, máy xay tỏi, hộp đựng thực phẩm", "fb_page_id": "PENDING", "handle_base": "bepminicodrama", "browser_profile": "Profile_08", "proxy_group": "VN_IP_08", "phase_status": "PHASE_3_SCALE"},
    {"pod_id": "POD-14", "pod_code": "cuocchienmuamua", "pod_name": "Cuộc Chiến Mùa Mưa", "cluster_group": "CỤM 3: Gia dụng mini & Theo mùa", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Người đi làm/sinh viên mùa mưa nồm", "content_firewall": "Máy sấy giày, túi hút ẩm, áo mưa/ô tự động", "fb_page_id": "PENDING", "handle_base": "cuocchienmuamua", "browser_profile": "Profile_08", "proxy_group": "VN_IP_08", "phase_status": "PHASE_3_SCALE"},
    {"pod_id": "POD-15", "pod_code": "muanongkhongcau", "pod_name": "Mùa Nóng Không Cáu", "cluster_group": "CỤM 3: Gia dụng mini & Theo mùa", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Học sinh, người di chuyển ngoài trời mùa hè", "content_firewall": "Quạt sò lạnh, tấm chắn nắng, bình nước giữ lạnh", "fb_page_id": "PENDING", "handle_base": "muanongkhongcau", "browser_profile": "Profile_09", "proxy_group": "VN_IP_09", "phase_status": "PHASE_3_SCALE"},
    {"pod_id": "POD-16", "pod_code": "docuphucthu", "pod_name": "Đồ Cũ Phục Thù", "cluster_group": "CỤM 3: Gia dụng mini & Theo mùa", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Người thích phục hồi đồ cũ như mới", "content_firewall": "Dung dịch tẩy trắng giày, máy cạo lông xù, keo vá", "fb_page_id": "PENDING", "handle_base": "docuphucthu", "browser_profile": "Profile_09", "proxy_group": "VN_IP_09", "phase_status": "PHASE_3_SCALE"},
    {"pod_id": "POD-17", "pod_code": "doicuuhododac", "pod_name": "Đội Cứu Hộ Đồ Đạc", "cluster_group": "CỤM 4: Nhân vật & IP Mở rộng", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Khán giả thích hoạt hình 3D giải cứu đồ vật", "content_firewall": "Video 3D nhân hóa đồ vật + cắt sang hàng thật giây 8", "fb_page_id": "PENDING", "handle_base": "doicuuhododac", "browser_profile": "Profile_10", "proxy_group": "VN_IP_10", "phase_status": "PHASE_3_SCALE"},
    {"pod_id": "POD-18", "pod_code": "toaantienich", "pod_name": "Tòa Án Tiện Ích", "cluster_group": "CỤM 4: Nhân vật & IP Mở rộng", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Người tiêu dùng thông thái thích xem phán quyết Mua/Bỏ", "content_firewall": "Format thẩm phán test hàng thật vs quảng cáo", "fb_page_id": "PENDING", "handle_base": "toaantienich", "browser_profile": "Profile_10", "proxy_group": "VN_IP_10", "phase_status": "PHASE_2_READY"},
    {"pod_id": "POD-19", "pod_code": "phonglab99k", "pod_name": "Phòng Lab 99K", "cluster_group": "CỤM 4: Nhân vật & IP Mở rộng", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Người mê mổ xẻ cơ chế kỹ thuật đồ dưới 99k", "content_firewall": "Test cực hạn, đo thông số đồ giá rẻ", "fb_page_id": "PENDING", "handle_base": "phonglab99k", "browser_profile": "Profile_11", "proxy_group": "VN_IP_11", "phase_status": "PHASE_3_SCALE"},
    {"pod_id": "POD-20", "pod_code": "thamtusanloi", "pod_name": "Thám Tử Săn Lỗi", "cluster_group": "CỤM 4: Nhân vật & IP Mở rộng", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Khách hàng sợ mua phải hàng dởm trên mạng", "content_firewall": "Soi lỗi sản phẩm trước rồi chỉ ra điểm đáng tiền", "fb_page_id": "PENDING", "handle_base": "thamtusanloi", "browser_profile": "Profile_11", "proxy_group": "VN_IP_11", "phase_status": "PHASE_3_SCALE"},
    {"pod_id": "POD-21", "pod_code": "vutrudovat", "pod_name": "Vũ Trụ Đồ Vật", "cluster_group": "CỤM 4: Nhân vật & IP Mở rộng", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Tệp đại chúng giải trí 3D POV", "content_firewall": "3D POV đồ vật tự kể chuyện + gắn giỏ hàng", "fb_page_id": "PENDING", "handle_base": "vutrudovat", "browser_profile": "Profile_12", "proxy_group": "VN_IP_12", "phase_status": "PHASE_3_SCALE"},
    {"pod_id": "POD-22", "pod_code": "ifnagency", "pod_name": "IFN - Xây Kênh & Livestream", "cluster_group": "CỤM ĐẶC BIỆT: Dịch vụ & B2B", "business_model": "LEAD_COURSE_FUNNEL", "target_audience": "Chủ shop, Brand cần dịch vụ xây kênh/livestream", "content_firewall": "Case study xây kênh, booking KOL/KOC, dịch vụ B2B", "fb_page_id": "591875884001523", "handle_base": "ifn.media", "browser_profile": "Chrome_Profile_03_AI_Education", "proxy_group": "VN_RESIDENTIAL_IP_03", "phase_status": "PHASE_2_READY"},
    {"pod_id": "POD-23", "pod_code": "gocdecor99k", "pod_name": "Góc Decor 99K", "cluster_group": "CỤM 1: Sinh viên & Phòng trọ", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Nữ sinh viên thích decor phòng Hàn Quốc", "content_firewall": "Đèn ngủ, gương để bàn, kệ mỹ phẩm", "fb_page_id": "PENDING", "handle_base": "gocdecor99k", "browser_profile": "Profile_13", "proxy_group": "VN_IP_13", "phase_status": "PHASE_3_SCALE"},
    {"pod_id": "POD-24", "pod_code": "congnghecuusinh", "pod_name": "Công Nghệ Cứu Sinh", "cluster_group": "CỤM 2: Văn phòng & Góc làm việc", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Nam giới công sở mê phụ kiện sạc/cáp/pin", "content_firewall": "Sạc dự phòng, cáp tự ngắt, giá đỡ từ tính", "fb_page_id": "PENDING", "handle_base": "congnghecuusinh", "browser_profile": "Profile_13", "proxy_group": "VN_IP_13", "phase_status": "PHASE_3_SCALE"},
    {"pod_id": "POD-25", "pod_code": "bietdoitietkiem", "pod_name": "Biệt Đội Tiết Kiệm", "cluster_group": "CỤM 3: Gia dụng mini & Theo mùa", "business_model": "SHOPEE_AFFILIATE", "target_audience": "Người săn deal hời dưới 100k", "content_firewall": "Combo gia dụng tiết kiệm, bảng xếp hạng đồ rẻ bền", "fb_page_id": "PENDING", "handle_base": "bietdoitietkiem", "browser_profile": "Profile_14", "proxy_group": "VN_IP_14", "phase_status": "PHASE_3_SCALE"},
]

PLATFORM_TEMPLATES = [
    {
        "suffix": "FB",
        "platform": "FB_REELS",
        "slot_1": "11:45",
        "slot_2": "20:00",
        "link_placement_rule": "CẤM link ở Caption -> Gắn link ở Pinned Comment #1",
        "sub_id_placement": "pin",
        "platform_short": "fb",
    },
    {
        "suffix": "IG",
        "platform": "IG_REELS",
        "slot_1": "12:15",
        "slot_2": "20:30",
        "link_placement_rule": "CẤM link ở Caption -> Auto-DM Keyword ('LINK') + Link in Bio",
        "sub_id_placement": "dm",
        "platform_short": "ig",
    },
    {
        "suffix": "TH",
        "platform": "THREADS",
        "slot_1": "08:30",
        "slot_2": "21:30",
        "link_placement_rule": "CẤM link ở Root Post -> Gắn link ở Self-Reply #1",
        "sub_id_placement": "rep1",
        "platform_short": "th",
    },
    {
        "suffix": "YT",
        "platform": "YT_SHORTS",
        "slot_1": "12:00",
        "slot_2": "19:30",
        "link_placement_rule": "Link Shorts bị khóa -> Dẫn qua Related Video + Bio 14 Links + YT Shopping",
        "sub_id_placement": "rel",
        "platform_short": "yt",
    },
]


def init_matrix_tables(db_path: Path) -> dict:
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS brand_pods (
            pod_id TEXT PRIMARY KEY,
            pod_code TEXT NOT NULL,
            pod_name TEXT NOT NULL,
            cluster_group TEXT NOT NULL,
            business_model TEXT NOT NULL,
            target_audience TEXT,
            content_firewall TEXT,
            fb_page_id TEXT,
            handle_base TEXT,
            browser_profile TEXT,
            proxy_group TEXT,
            phase_status TEXT DEFAULT 'PHASE_1_ACTIVE',
            updated_at TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS channels (
            channel_id TEXT PRIMARY KEY,
            pod_id TEXT NOT NULL,
            platform TEXT NOT NULL,
            display_name TEXT NOT NULL,
            handle TEXT NOT NULL,
            external_account_id TEXT,
            slot_1 TEXT NOT NULL,
            slot_2 TEXT NOT NULL,
            link_placement_rule TEXT NOT NULL,
            sub_id_prefix TEXT NOT NULL,
            browser_profile TEXT,
            proxy_group TEXT,
            connection_status TEXT NOT NULL,
            updated_at TEXT,
            FOREIGN KEY (pod_id) REFERENCES brand_pods(pod_id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS multi_channel_posts (
            post_job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id TEXT,
            pod_id TEXT NOT NULL,
            channel_id TEXT NOT NULL,
            platform TEXT NOT NULL,
            sku_code TEXT,
            asset_id TEXT,
            video_variant_path TEXT,
            video_md5_hash TEXT,
            title_or_hook TEXT,
            caption_no_link TEXT,
            comment_or_dm_payload TEXT,
            tracked_url TEXT,
            sub_id_tag TEXT,
            scheduled_slot TEXT,
            approval_status TEXT DEFAULT 'DRAFT_ONLY',
            live_post_id TEXT,
            created_at TEXT
        )
        """
    )

    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    pods_inserted = 0
    channels_inserted = 0

    for pod in BRAND_PODS_SEED:
        cur.execute(
            """
            INSERT INTO brand_pods (
                pod_id, pod_code, pod_name, cluster_group, business_model,
                target_audience, content_firewall, fb_page_id, handle_base,
                browser_profile, proxy_group, phase_status, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(pod_id) DO UPDATE SET
                pod_code=excluded.pod_code,
                pod_name=excluded.pod_name,
                cluster_group=excluded.cluster_group,
                business_model=excluded.business_model,
                target_audience=excluded.target_audience,
                content_firewall=excluded.content_firewall,
                fb_page_id=excluded.fb_page_id,
                handle_base=excluded.handle_base,
                browser_profile=excluded.browser_profile,
                proxy_group=excluded.proxy_group,
                phase_status=excluded.phase_status,
                updated_at=excluded.updated_at
            """,
            (
                pod["pod_id"],
                pod["pod_code"],
                pod["pod_name"],
                pod["cluster_group"],
                pod["business_model"],
                pod["target_audience"],
                pod["content_firewall"],
                pod["fb_page_id"],
                pod["handle_base"],
                pod["browser_profile"],
                pod["proxy_group"],
                pod["phase_status"],
                now_iso,
            ),
        )
        pods_inserted += 1

        pod_num = pod["pod_id"].replace("-", "")
        for tpl in PLATFORM_TEMPLATES:
            channel_id = f"{pod_num}_{tpl['suffix']}"
            handle = f"@{pod['handle_base']}"
            ext_id = pod["fb_page_id"] if tpl["suffix"] == "FB" else f"PENDING_{channel_id}"
            if tpl["suffix"] == "FB" and pod["fb_page_id"] != "PENDING":
                conn_status = "CONNECTED_GRAPH_API"
            elif pod["phase_status"] == "PHASE_1_ACTIVE":
                conn_status = "PHASE1_SETUP_READY"
            else:
                conn_status = "PLANNED_SCALING"

            sub_prefix = f"{tpl['platform_short']}_{pod['pod_code']}_{tpl['sub_id_placement']}"
            cur.execute(
                """
                INSERT INTO channels (
                    channel_id, pod_id, platform, display_name, handle,
                    external_account_id, slot_1, slot_2, link_placement_rule,
                    sub_id_prefix, browser_profile, proxy_group, connection_status, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(channel_id) DO UPDATE SET
                    display_name=excluded.display_name,
                    handle=excluded.handle,
                    external_account_id=excluded.external_account_id,
                    slot_1=excluded.slot_1,
                    slot_2=excluded.slot_2,
                    link_placement_rule=excluded.link_placement_rule,
                    sub_id_prefix=excluded.sub_id_prefix,
                    browser_profile=excluded.browser_profile,
                    proxy_group=excluded.proxy_group,
                    connection_status=excluded.connection_status,
                    updated_at=excluded.updated_at
                """,
                (
                    channel_id,
                    pod["pod_id"],
                    tpl["platform"],
                    pod["pod_name"],
                    handle,
                    ext_id,
                    tpl["slot_1"],
                    tpl["slot_2"],
                    tpl["link_placement_rule"],
                    sub_prefix,
                    pod["browser_profile"],
                    pod["proxy_group"],
                    conn_status,
                    now_iso,
                ),
            )
            channels_inserted += 1

    conn.commit()
    conn.close()
    return {
        "db_path": str(db_path),
        "total_pods": pods_inserted,
        "total_channels": channels_inserted,
    }


def build_tracked_url(raw_url: str, sub_id_tag: str, business_model: str, aff_id: str) -> str:
    raw_url = raw_url.strip()
    if not raw_url:
        return ""
    if business_model == "SHOPEE_AFFILIATE" and ("shopee.vn" in raw_url):
        if "an_redir" in raw_url:
            return raw_url
        clean_origin = raw_url.split("?")[0]
        encoded_origin = urllib.parse.quote(clean_origin, safe="")
        encoded_sub = urllib.parse.quote(sub_id_tag, safe="")
        return f"https://s.shopee.vn/an_redir?origin_link={encoded_origin}&affiliate_id={aff_id}&sub_id={encoded_sub}"
    sep = "&" if "?" in raw_url else "?"
    parts = sub_id_tag.split("_")
    plat = parts[0] if len(parts) > 0 else "multi"
    pod = parts[1] if len(parts) > 1 else "pod"
    place = parts[2] if len(parts) > 2 else "link"
    return f"{raw_url}{sep}utm_source={plat}&utm_medium={place}&utm_campaign={pod}&utm_content={sub_id_tag}"


def print_dashboard(db_path: Path) -> None:
    if not db_path.exists():
        init_matrix_tables(db_path)
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM brand_pods")
    total_pods = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM channels")
    total_channels = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM channels WHERE connection_status = 'CONNECTED_GRAPH_API'")
    connected_fb = cur.fetchone()[0]

    print("=" * 95)
    print(f"🌐 BẢNG ĐIỀU KHIỂN MA TRẬN ĐA KÊNH (BRAND POD REGISTRY) — DB: {db_path.name}")
    print(f"📊 Quy mô đã định danh: {total_pods} Brand Pods × 4 Nền tảng = {total_channels} Kênh (Đã kết nối API: {connected_fb} Fanpage)")
    print("=" * 95)

    cur.execute(
        """
        SELECT pod_id, pod_name, cluster_group, business_model, fb_page_id, browser_profile, proxy_group
        FROM brand_pods
        WHERE phase_status = 'PHASE_1_ACTIVE'
        ORDER BY pod_id
        """
    )
    active_pods = cur.fetchall()
    for pod_id, pod_name, cluster, bmodel, fb_id, bprof, pgrp in active_pods:
        print(f"\n🔹 [{pod_id}] {pod_name.upper()} ({cluster}) | Mô hình: {bmodel}")
        print(f"   🛡️ Cách ly: Browser={bprof} | IP Group={pgrp} | FB Page ID={fb_id}")
        print("   " + "-" * 90)
        cur.execute(
            """
            SELECT channel_id, platform, handle, slot_1, slot_2, sub_id_prefix, link_placement_rule, connection_status
            FROM channels
            WHERE pod_id = ?
            ORDER BY channel_id
            """,
            (pod_id,),
        )
        for cid, plat, handle, s1, s2, sub_pre, rule, status in cur.fetchall():
            print(f"   • {cid:<9} | {plat:<10} | {handle:<18} | Giờ: {s1}/{s2} | SubID: {sub_pre}_<sku> | {status}")
            print(f"               ↳ Quy tắc Link: {rule}")

    print("\n" + "=" * 95)
    print("🚀 TỔNG HỢP LỘ TRÌNH 25 BRAND PODS (100 KÊNH ĐA NỀN TẢNG):")
    cur.execute(
        """
        SELECT phase_status, COUNT(DISTINCT pod_id) as pods, COUNT(driver.channel_id) as chs
        FROM brand_pods bp
        JOIN channels driver USING(pod_id)
        GROUP BY phase_status
        ORDER BY phase_status
        """
    )
    for phase, p_cnt, c_cnt in cur.fetchall():
        print(f"   - {phase:<18}: {p_cnt:>2} Brand Pods = {c_cnt:>3} Kênh (FB + IG + Threads + YouTube)")
    print("=" * 95)
    conn.close()


def generate_pod_publish_pack(
    db_path: Path,
    pod_id: str,
    sku_code: str,
    raw_url: str,
    title: str,
    campaign_id: str = "CAMP-AUTO",
) -> dict:
    if not db_path.exists():
        init_matrix_tables(db_path)
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute(
        "SELECT pod_name, business_model, content_firewall FROM brand_pods WHERE pod_id = ?",
        (pod_id,),
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        raise ValueError(f"Không tìm thấy Pod ID: {pod_id}")

    pod_name, business_model, firewall = row
    aff_id = get_shopee_aff_id()

    # Kiểm tra Content Firewall: Chặn gắn link Shopee gia dụng vào Pod AI Players
    if business_model == "LEAD_COURSE_FUNNEL" and "shopee.vn" in raw_url.lower():
        conn.close()
        raise ValueError(
            f"[CONTENT FIREWALL BLOCKED] {pod_id} ({pod_name}) thuộc nhánh {business_model}. "
            f"Cấm gắn link bán lẻ Shopee ({raw_url}) vào kênh cộng đồng/khóa học AI!"
        )

    cur.execute(
        """
        SELECT channel_id, platform, handle, slot_1, slot_2, sub_id_prefix, link_placement_rule
        FROM channels
        WHERE pod_id = ?
        ORDER BY channel_id
        """,
        (pod_id,),
    )
    channels = cur.fetchall()
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    pack_channels = {}

    for cid, plat, handle, s1, s2, sub_prefix, rule in channels:
        clean_sku = sku_code.lower().replace("-", "").replace("_", "")[:12]
        sub_id_tag = f"{sub_prefix}_{clean_sku}"
        tracked_url = build_tracked_url(raw_url, sub_id_tag, business_model, aff_id)

        if plat == "FB_REELS":
            caption = f"{title} — Xem kỹ đoạn test ở giây thứ 8 nhé!\n\n👉 Link chính hãng tui ghim ở bình luận đầu tiên nha! #review #{clean_sku}"
            payload = f"🔥 Chốt đơn chính hãng đúng phân loại tại đây nha: {tracked_url}"
        elif plat == "IG_REELS":
            caption = f"{title} ✨\nComment chữ 'LINK' bên dưới mình gửi thẳng link vào hộp thư (DM) trong 3 giây, hoặc bấm vào Bio đầu trang nhé! #{clean_sku} #reelsvn"
            payload = f"[AUTO-DM KEYWORD: LINK] Gửi bạn link chính hãng của {pod_name}: {tracked_url}"
        elif plat == "THREADS":
            caption = f"Thật sự không nghĩ một món đồ nhỏ gọn như {title} lại giải quyết gọn lẹ vấn đề này. Đã test kỹ 3 ngày, để lại link chỗ mua uy tín ở dưới cmt cho ai cần nhé 👇"
            payload = f"[SELF-REPLY #1] Chỗ mình săn được giá hời đây nha: {tracked_url} (#affiliate)"
        else:  # YT_SHORTS
            tags_str = f" #Shorts #review #{clean_sku[:10]}"
            max_title_len = 59 - len(tags_str)
            trimmed_title = title[:max_title_len].rsplit(" ", 1)[0] if len(title) > max_title_len else title
            caption = f"{trimmed_title}{tags_str}"
            payload = f"[RELATED VIDEO / BIO LINK] Xem chi tiết & lấy link chính hãng tại đây: {tracked_url}"

        cur.execute(
            """
            INSERT INTO multi_channel_posts (
                campaign_id, pod_id, channel_id, platform, sku_code,
                title_or_hook, caption_no_link, comment_or_dm_payload,
                tracked_url, sub_id_tag, scheduled_slot, approval_status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'DRAFT_ONLY', ?)
            """,
            (
                campaign_id,
                pod_id,
                cid,
                plat,
                sku_code,
                title,
                caption,
                payload,
                tracked_url,
                sub_id_tag,
                s1,
                now_iso,
            ),
        )

        pack_channels[cid] = {
            "platform": plat,
            "handle": handle,
            "schedule_slots": [s1, s2],
            "sub_id_tag": sub_id_tag,
            "tracked_url": tracked_url,
            "caption_no_link": caption,
            "conversion_payload": payload,
            "placement_rule": rule,
        }

    conn.commit()
    conn.close()
    return {
        "pod_id": pod_id,
        "pod_name": pod_name,
        "business_model": business_model,
        "content_firewall": firewall,
        "sku_code": sku_code,
        "channels": pack_channels,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Quản trị Ma trận Đa kênh (16 -> 100 Kênh)")
    parser.add_argument("--init", action="store_true", help="Khởi tạo / Cập nhật bảng brand_pods, channels, multi_channel_posts")
    parser.add_argument("--dashboard", action="store_true", help="Hiển thị bảng điều khiển 4 Pod chủ lực (16 kênh) & lộ trình 100 kênh")
    parser.add_argument("--generate-pack", action="store_true", help="Tạo gói định tuyến link & copy cho 4 kênh của 1 Pod")
    parser.add_argument("--pod", default="POD-01", help="Mã Pod (VD: POD-01, POD-02, POD-03, POD-04)")
    parser.add_argument("--sku", default="quat_imi_01", help="Mã SKU ngắn (VD: quat_imi_01)")
    parser.add_argument("--url", default="https://shopee.vn/product/123456/789012", help="URL gốc của sản phẩm hoặc Landing Page")
    parser.add_argument("--title", default="Quạt cầm tay sò lạnh iMI làm mát tức thì", help="Tiêu đề / Hook chính")
    args = parser.parse_args()

    db_path = get_db_path()
    if args.init:
        res = init_matrix_tables(db_path)
        print(f"✅ Đã khởi tạo thành công {res['total_pods']} Brand Pods ({res['total_channels']} kênh) trong {res['db_path']}")

    if args.dashboard or (not args.init and not args.generate_pack):
        print_dashboard(db_path)

    if args.generate_pack:
        pack = generate_pod_publish_pack(db_path, args.pod, args.sku, args.url, args.title)
        print(json.dumps(pack, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
