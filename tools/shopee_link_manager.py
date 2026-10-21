#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
shopee_link_manager.py — Hệ Thống Tự Động Lấy Link, Quản Lý Kho SKU & Đối Soát Chuyển Đổi
Dành Riêng Cho Tài Khoản Shopee Affiliate Cá Nhân Tiêu Chuẩn (https://affiliate.shopee.vn/dashboard)

Chức năng cốt lõi (0-Token):
1. Trích xuất & lưu mã `SHOPEE_AFFILIATE_ID` cá nhân chỉ từ 1 link rút gọn mẫu (`s.shopee.vn/...` hoặc `shope.ee/...`).
2. Làm sạch link Shopee gốc (`https://shopee.vn/product/{shop_id}/{item_id}`) và tự động sinh bộ 3 Link Affiliate
   gắn sẵn 5 tầng `Sub_ID` (`sub_id1..5`) cho 3 Page Bán Hàng:
     - Page 1: Ký Túc Xá Có Biến (`ktx`      | ID: 1421270697727753)
     - Page 2: Hội Deadline      (`deadline` | ID: 1407231352464711)
     - Page 3: Phòng Trọ Hết Cứu (`phongtro` | ID: 1442323328956326)
3. Xuất đồng thời:
     - Link tự động `an_redir` chuẩn Shopee (dùng ngay lập tức không cần mở trình duyệt).
     - File Batch CSV (`campaigns/shopee-links/custom_link_batch.csv`) để nạp vào `affiliate.shopee.vn/offer/custom_link`
       khi muốn lấy shortlink `s.shopee.vn/xxxx`.
4. Quản lý tập trung toàn bộ SKU, Link từng Page, ID bài đăng/bình luận ghim trong SQLite (`aff_system.db`).
5. Đọc trực tiếp file CSV "Báo cáo chuyển đổi" xuất từ `affiliate.shopee.vn` (`--import-report`),
   bóc tách `Sub_ID` để thống kê Click, Đơn hàng hợp lệ, Hoa hồng và chẩn đoán `KEEP / ITERATE / STOP` cho từng Page.
"""

import argparse
import csv
import datetime
import json
import os
import re
import sqlite3
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
FB_MCP_DIR = Path.home() / ".codex" / "mcp" / "facebook-mcp-server"
ENV_PATH = FB_MCP_DIR / ".env"
VAULT_PATH = FB_MCP_DIR / "pages_vault.json"
DB_PATH = Path.home() / ".gemini" / "antigravity" / "scratch" / "ai-aff-video-system" / "data" / "aff_system.db"
EXPORT_DIR = SUBAGENT_DIR / "campaigns" / "shopee-links"

# Danh bạ cố định 3 Page Bán Hàng Affiliate
SALES_PAGES = [
    {
        "page_key": "ktx",
        "page_id": "1421270697727753",
        "page_name": "Ký Túc Xá Có Biến",
        "default_cta_prefix": "🔥 Link chính hãng giá sinh viên cho anh em KTX tại đây nha:",
    },
    {
        "page_key": "deadline",
        "page_id": "1407231352464711",
        "page_name": "Hội Deadline",
        "default_cta_prefix": "⚡ Cứu tinh góc bàn làm việc cho dân chạy Deadline ở đây nhé:",
    },
    {
        "page_key": "phongtro",
        "page_id": "1442323328956326",
        "page_name": "Phòng Trọ Hết Cứu",
        "default_cta_prefix": "🏠 Bảo bối dọn phòng trọ gọn sạch đang sale hời tại đây nha:",
    },
]


def parse_env(path: Path) -> dict:
    data = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def save_env_key(key: str, value: str) -> None:
    FB_MCP_DIR.mkdir(parents=True, exist_ok=True)
    if not ENV_PATH.exists():
        ENV_PATH.write_text(f"{key}={value}\n", encoding="utf-8")
        return
    lines = ENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines()
    found = False
    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={value}")
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f"\n# Cấu hình Shopee Affiliate Cá Nhân")
        new_lines.append(f"{key}={value}")
    ENV_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def get_affiliate_id() -> str:
    env_vars = parse_env(ENV_PATH)
    aff_id = os.environ.get("SHOPEE_AFFILIATE_ID") or env_vars.get("SHOPEE_AFFILIATE_ID", "")
    if not aff_id:
        aff_id = "17395830088"
        save_env_key("SHOPEE_AFFILIATE_ID", aff_id)
    return aff_id


def extract_affiliate_id_from_shortlink(short_url: str) -> str:
    """
    Giải mã HTTP Redirect từ 1 link rút gọn `s.shopee.vn/...` hoặc `shope.ee/...`
    để tự động tìm mã `affiliate_id` (VD: `173xxxxxx` trong `utm_source=an_173xxxxxx` hoặc `affiliate_id=173xxxxxx`).
    """
    req = urllib.request.Request(
        short_url.strip(),
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
        method="GET",
    )
    final_url = short_url
    try:
        with urllib.request.urlopen(req, timeout=8.0) as resp:
            final_url = resp.geturl()
    except urllib.error.HTTPError as e:
        final_url = e.geturl() or short_url
    except Exception:
        pass

    decoded = urllib.parse.unquote(final_url)
    patterns = [
        r"utm_source=an_(\d+)",
        r"affiliate_id=(\d+)",
        r"af_sub_siteid=(\d+)",
    ]
    for pat in patterns:
        m = re.search(pat, decoded)
        if m:
            return m.group(1)
    return ""


def refresh_all_links_with_aff_id(aff_id: str) -> None:
    conn = init_db()
    cur = conn.cursor()
    rows = cur.execute(
        """
        SELECT id, clean_origin_url, sub_id1, sub_id2, sub_id3, sub_id4, sub_id5, page_key
        FROM shopee_page_links
        """
    ).fetchall()
    page_prefix_map = {p["page_key"]: p["default_cta_prefix"] for p in SALES_PAGES}
    for r in rows:
        row_id, clean_url, s1, s2, s3, s4, s5, pkey = r
        new_auto = build_an_redir_link(clean_url, aff_id, [s1, s2, s3, s4, s5])
        prefix = page_prefix_map.get(pkey, "🔥 Link sản phẩm chính hãng tại đây nha:")
        new_comment = f"{prefix}\n👉 {new_auto}"
        cur.execute(
            """
            UPDATE shopee_page_links
            SET auto_deeplink_url=?,
                pinned_comment_text=CASE
                    WHEN short_aff_url IS NULL OR short_aff_url = '' THEN ?
                    ELSE pinned_comment_text
                END,
                updated_at=CURRENT_TIMESTAMP
            WHERE id=?
            """,
            (new_auto, new_comment, row_id),
        )
    conn.commit()
    conn.close()
    export_custom_link_batch_csv()


def scan_fb_sales_pages() -> int:
    if not VAULT_PATH.exists():
        print("❌ Chưa có kho `pages_vault.json`.")
        return 1
    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8", errors="ignore"))
    token_map = {p["id"]: p["access_token"] for p in vault.get("pages", []) if "id" in p and "access_token" in p}

    print("\n" + "=" * 82)
    print(" 📱 QUÉT BÀI ĐĂNG & BÌNH LUẬN GHIM TRÊN 3 PAGE BÁN HÀNG FACEBOOK")
    print("=" * 82)
    for sp in SALES_PAGES:
        pid = sp["page_id"]
        pname = sp["page_name"]
        pkey = sp["page_key"]
        tok = token_map.get(pid)
        if not tok:
            print(f"⚠️ Không tìm thấy token cho Page {pname} ({pid})")
            continue
        url = (
            f"https://graph.facebook.com/v22.0/{pid}/posts"
            f"?fields=id,message,created_time,comments.limit(5){{id,message,from}}"
            f"&limit=5&access_token={urllib.parse.quote(tok)}"
        )
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=8.0) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="ignore")).get("data", [])
                print(f"\n📌 [{pkey.upper()}] {pname} (ID: {pid}) — {len(data)} bài gần nhất:")
                for idx, post in enumerate(data, start=1):
                    post_id = post.get("id", "")
                    msg_preview = (post.get("message") or "[Không có caption]").splitlines()[0][:68]
                    comments = post.get("comments", {}).get("data", [])
                    print(f"   {idx}. Post `{post_id}`: {msg_preview}...")
                    for c in comments[:2]:
                        cid = c.get("id", "")
                        cmsg = (c.get("message") or "").replace("\n", " ")[:75]
                        print(f"      └─ Comment `{cid}`: {cmsg}")
        except Exception as e:
            print(f"❌ Lỗi quét Page {pname}: {e}")
    print("=" * 82 + "\n")
    return 0


LIVE_POST_COMMENT_TARGETS = [
    {
        "page_key": "ktx",
        "page_id": "1421270697727753",
        "page_name": "Ký Túc Xá Có Biến",
        "post_id": "1421270697727753_122106524439511096",
        "comment_id": "122106524439511096_1681189970310941",
        "sku_code": "tui_nen_chan_khong",
        "product_name": "Combo 8 Túi Nén Hút Chân Không PA+PE Kèm Bơm Tay Đựng Chăn Màn",
        "clean_product_url": "https://shopee.vn/product/121890267/18836537162",
        "price_vnd": 65000,
    },
    {
        "page_key": "ktx",
        "page_id": "1421270697727753",
        "page_name": "Ký Túc Xá Có Biến",
        "post_id": "1421270697727753_122106524061511096",
        "comment_id": "122106524061511096_1635038298270096",
        "sku_code": "quat_kep_giuong_360",
        "product_name": "Quạt Tích Điện Mini Để Bàn Có Đế Kẹp Giường Xoay 360 Độ",
        "clean_product_url": "https://shopee.vn/product/75279512/27584306480",
        "price_vnd": 99000,
    },
    {
        "page_key": "deadline",
        "page_id": "1407231352464711",
        "page_name": "Hội Deadline",
        "post_id": "1407231352464711_122111499867502096",
        "comment_id": "122111499867502096_2558864567929784",
        "sku_code": "den_kep_man_hinh",
        "product_name": "Đèn Treo Kẹp Màn Hình Máy Tính Chống Lóa Bảo Vệ Mắt TB-30",
        "clean_product_url": "https://shopee.vn/product/806240928/27831334571",
        "price_vnd": 189000,
    },
    {
        "page_key": "deadline",
        "page_id": "1407231352464711",
        "page_name": "Hội Deadline",
        "post_id": "1407231352464711_122111499567502096",
        "comment_id": "122111499567502096_1793301908590293",
        "sku_code": "gia_do_laptop_360",
        "product_name": "Kệ Giá Đỡ Laptop Hợp Kim Nhôm SE50 Nâng Cao Xoay 360 Độ",
        "clean_product_url": "https://shopee.vn/product/35958362/23171742273",
        "price_vnd": 89000,
    },
    {
        "page_key": "phongtro",
        "page_id": "1442323328956326",
        "page_name": "Phòng Trọ Hết Cứu",
        "post_id": "1442323328956326_122101744053514839",
        "comment_id": "122101744053514839_1707730694109011",
        "sku_code": "bo_cat_got_rau_cu",
        "product_name": "Bộ Dụng Cụ Bào Cắt Gọt Rau Củ Quả Đa Năng Kèm Rổ 9in1",
        "clean_product_url": "https://shopee.vn/product/239730392/6134468445",
        "price_vnd": 95000,
    },
    {
        "page_key": "phongtro",
        "page_id": "1442323328956326",
        "page_name": "Phòng Trọ Hết Cứu",
        "post_id": "1442323328956326_122101743429514839",
        "comment_id": "122101743429514839_4270790293220291",
        "sku_code": "may_hut_bui_mini",
        "product_name": "Máy Hút Bụi Cầm Tay Không Dây Mini 5 Trong 1 Đa Năng",
        "clean_product_url": "https://shopee.vn/product/196261835/40969424649",
        "price_vnd": 149000,
    },
]


def upgrade_live_fb_comments() -> int:
    aff_id = get_affiliate_id()
    if not aff_id:
        print("❌ Chưa có `SHOPEE_AFFILIATE_ID` trong `.env`.")
        return 1
    if not VAULT_PATH.exists():
        print("❌ Chưa có `pages_vault.json`.")
        return 1

    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8", errors="ignore"))
    token_map = {p["id"]: p["access_token"] for p in vault.get("pages", []) if "id" in p and "access_token" in p}
    conn = init_db()
    cur = conn.cursor()

    updated_count = 0
    for item in LIVE_POST_COMMENT_TARGETS:
        pid = item["page_id"]
        cid = item["comment_id"]
        pkey = item["page_key"]
        sku = item["sku_code"]
        pname = item["product_name"]
        tok = token_map.get(pid)
        if not tok:
            continue

        try:
            get_url = f"https://graph.facebook.com/v22.0/{cid}?fields=message&access_token={urllib.parse.quote(tok)}"
            with urllib.request.urlopen(get_url, timeout=15.0) as resp:
                old_msg = json.loads(resp.read().decode("utf-8", errors="ignore")).get("message", "")

            m_url = re.search(r"https://\S+", old_msg)
            if not m_url:
                continue
            old_link = m_url.group(0)
            # BẮT BUỘC dùng link đích sản phẩm trực tiếp (https://shopee.vn/product/{shop_id}/{item_id})
            # Tuyệt đối CẤM dùng link tìm kiếm từ khóa shopee.vn/search?keyword=...
            origin_target = item.get("clean_product_url") or old_link

            sub_list = [pkey, sku, "img_1x1", "20261020_live", "macro_grid"]
            sub_comb = "-".join(sub_list)
            tracked_link = build_an_redir_link(origin_target, aff_id, sub_list)
            new_msg = old_msg.replace(old_link, tracked_link)

            post_data = urllib.parse.urlencode(
                {"message": new_msg, "access_token": tok}
            ).encode("utf-8")
            req = urllib.request.Request(
                f"https://graph.facebook.com/v22.0/{cid}",
                data=post_data,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15.0) as u_resp:
                res_json = json.loads(u_resp.read().decode("utf-8", errors="ignore"))
                if res_json.get("success"):
                    updated_count += 1
                    print(f"✅ Đã gắn mã Affiliate `{aff_id}` + Sub_ID `{sub_comb}` lên Comment `{cid}` ({item['page_name']})")

            cur.execute(
                """
                INSERT INTO shopee_page_links (
                    sku_code, product_name, page_key, page_id, page_name,
                    clean_origin_url, sub_id1, sub_id2, sub_id3, sub_id4, sub_id5,
                    sub_id_combined, auto_deeplink_url, short_aff_url, pinned_comment_text,
                    fb_post_id, fb_comment_id, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '', ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(sku_code, page_key, sub_id3, sub_id4) DO UPDATE SET
                    auto_deeplink_url=excluded.auto_deeplink_url,
                    pinned_comment_text=excluded.pinned_comment_text,
                    fb_post_id=excluded.fb_post_id,
                    fb_comment_id=excluded.fb_comment_id,
                    updated_at=CURRENT_TIMESTAMP
                """,
                (
                    sku,
                    pname,
                    pkey,
                    pid,
                    item["page_name"],
                    origin_target,
                    sub_list[0],
                    sub_list[1],
                    sub_list[2],
                    sub_list[3],
                    sub_list[4],
                    sub_comb,
                    tracked_link,
                    new_msg,
                    item["post_id"],
                    cid,
                ),
            )
        except Exception as e:
            print(f"⚠️ Lỗi cập nhật Comment `{cid}`: {e}")

    conn.commit()
    conn.close()
    export_custom_link_batch_csv()
    print(f"\n🎯 Hoàn tất nâng cấp {updated_count}/6 Pinned Comment đang chạy thực tế trên 3 Fanpage!")
    return 0


def clean_shopee_product_url(raw_url: str) -> tuple[str, str, str]:
    """
    Trích xuất `shop_id` và `item_id` từ mọi dạng link sản phẩm Shopee:
      - https://shopee.vn/Ten-san-pham-i.965172716.26581062779?sp_atk=...
      - https://shopee.vn/product/965172716/26581062779
      - https://vn.shp.ee/... hoặc s.shopee.vn/... (tự động mở redirect nếu cần)
    Trả về: (clean_url, shop_id, item_id)
    """
    url = raw_url.strip()
    if any(short_dom in url for short_dom in ("s.shopee.vn", "shope.ee", "shp.ee")) and "an_redir" not in url:
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            )
            with urllib.request.urlopen(req, timeout=6.0) as resp:
                url = resp.geturl()
        except Exception:
            pass

    # Dạng 1: -i.{shop_id}.{item_id}
    m1 = re.search(r"-i\.(\d+)\.(\d+)", url)
    if m1:
        shop_id, item_id = m1.group(1), m1.group(2)
        return f"https://shopee.vn/product/{shop_id}/{item_id}", shop_id, item_id

    # Dạng 2: /product/{shop_id}/{item_id} hoặc /opaanlp/{shop_id}/{item_id}
    m2 = re.search(r"/(?:product|opaanlp)/(\d+)/(\d+)", url)
    if m2:
        shop_id, item_id = m2.group(1), m2.group(2)
        return f"https://shopee.vn/product/{shop_id}/{item_id}", shop_id, item_id

    # Fallback: bỏ query string
    clean_fallback = url.split("?")[0]
    return clean_fallback, "unknown", "unknown"


def init_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    # Đảm bảo bảng products gốc tồn tại
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            niche TEXT,
            score INTEGER DEFAULT 0,
            commission TEXT,
            pain_points TEXT,
            hook_angle TEXT,
            aff_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Bổ sung các cột quản lý SKU nâng cao nếu chưa có
    existing_cols = {r[1] for r in cur.execute("PRAGMA table_info(products)").fetchall()}
    extra_cols = {
        "sku_code": "TEXT",
        "shop_id": "TEXT",
        "item_id": "TEXT",
        "clean_origin_url": "TEXT",
        "price_vnd": "INTEGER DEFAULT 0",
        "is_xtra": "INTEGER DEFAULT 1",
        "status": "TEXT DEFAULT 'ACTIVE'",
    }
    for col, col_type in extra_cols.items():
        if col not in existing_cols:
            cur.execute(f"ALTER TABLE products ADD COLUMN {col} {col_type}")

    # Bảng 2: Ma trận Link Affiliate theo từng Page & Sub_ID
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS shopee_page_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku_code TEXT NOT NULL,
            product_name TEXT,
            page_key TEXT NOT NULL,
            page_id TEXT NOT NULL,
            page_name TEXT NOT NULL,
            clean_origin_url TEXT NOT NULL,
            sub_id1 TEXT,
            sub_id2 TEXT,
            sub_id3 TEXT,
            sub_id4 TEXT,
            sub_id5 TEXT,
            sub_id_combined TEXT,
            auto_deeplink_url TEXT,
            short_aff_url TEXT,
            pinned_comment_text TEXT,
            fb_post_id TEXT,
            fb_comment_id TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(sku_code, page_key, sub_id3, sub_id4)
        )
        """
    )

    # Bảng 3: Lịch sử chuyển đổi thực tế nhập từ Báo cáo Shopee Affiliate CSV
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS shopee_conversions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_date TEXT,
            page_key TEXT,
            sku_code TEXT,
            sub_id_raw TEXT,
            clicks INTEGER DEFAULT 0,
            valid_orders INTEGER DEFAULT 0,
            gross_sales_vnd REAL DEFAULT 0,
            net_commission_vnd REAL DEFAULT 0,
            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    return conn


def build_an_redir_link(clean_url: str, aff_id: str, sub_ids: list[str]) -> str:
    """
    Tạo link Affiliate tự động qua cổng Universal Redirect của Shopee (`s.shopee.vn/an_redir`).
    HARD GATE: Cấm tuyệt đối việc bọc link tìm kiếm `shopee.vn/search` hoặc `shopee.vn/list`!
    Bắt buộc `clean_url` phải là link sản phẩm cụ thể (`https://shopee.vn/product/{shop_id}/{item_id}`).
    """
    if "/search" in clean_url or "/list/" in clean_url:
        raise ValueError(f"HARD GATE BLOCKED: Cấm dùng link tìm kiếm '{clean_url}' làm link Affiliate! Phải dùng https://shopee.vn/product/{{shop_id}}/{{item_id}}")
    sub_str = "-".join(s for s in sub_ids if s)
    encoded_origin = urllib.parse.quote(clean_url, safe="")
    if aff_id:
        return (
            f"https://s.shopee.vn/an_redir"
            f"?origin_link={encoded_origin}"
            f"&affiliate_id={urllib.parse.quote(aff_id)}"
            f"&sub_id={urllib.parse.quote(sub_str)}"
        )
    return f"{clean_url}?utm_source=shopee_aff&utm_medium={sub_ids[0]}&utm_campaign={sub_str}"


def add_product_and_generate_3page_links(
    sku_code: str,
    name: str,
    raw_url: str,
    price_vnd: int = 0,
    commission: str = "12% (Xtra)",
    content_format: str = "reel_ai",
    date_slot: str = "",
    hook_angle: str = "hook_before_after",
    score: int = 92,
) -> dict:
    clean_url, shop_id, item_id = clean_shopee_product_url(raw_url)
    if not date_slot:
        date_slot = datetime.datetime.now().strftime("%Y%m%d_1145")

    aff_id = get_affiliate_id()
    conn = init_db()
    cur = conn.cursor()

    # Lưu/Cập nhật vào bảng products
    cur.execute("SELECT id FROM products WHERE sku_code = ?", (sku_code,))
    row = cur.fetchone()
    if row:
        cur.execute(
            """
            UPDATE products
            SET name=?, score=?, commission=?, hook_angle=?, aff_url=?,
                shop_id=?, item_id=?, clean_origin_url=?, price_vnd=?, status='ACTIVE'
            WHERE sku_code=?
            """,
            (name, score, commission, hook_angle, clean_url, shop_id, item_id, clean_url, price_vnd, sku_code),
        )
    else:
        cur.execute(
            """
            INSERT INTO products (
                name, niche, score, commission, pain_points, hook_angle,
                aff_url, sku_code, shop_id, item_id, clean_origin_url, price_vnd, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE')
            """,
            (
                name,
                "Gia dụng & Tiện ích Sinh viên/Văn phòng",
                score,
                commission,
                "Nhỏ gọn, giải quyết tức thì trong 3s",
                hook_angle,
                clean_url,
                sku_code,
                shop_id,
                item_id,
                clean_url,
                price_vnd,
            ),
        )

    generated_rows = []
    for p in SALES_PAGES:
        sub1 = p["page_key"]
        sub2 = sku_code
        sub3 = content_format
        sub4 = date_slot
        sub5 = hook_angle
        sub_combined = f"{sub1}-{sub2}-{sub3}-{sub4}-{sub5}"

        auto_link = build_an_redir_link(clean_url, aff_id, [sub1, sub2, sub3, sub4, sub5])
        price_str = f" (Đang sale chỉ ~{price_vnd:,}đ)" if price_vnd > 0 else ""
        pinned_text = f"{p['default_cta_prefix']}{price_str}\n👉 {auto_link}"

        cur.execute(
            """
            INSERT INTO shopee_page_links (
                sku_code, product_name, page_key, page_id, page_name,
                clean_origin_url, sub_id1, sub_id2, sub_id3, sub_id4, sub_id5,
                sub_id_combined, auto_deeplink_url, short_aff_url, pinned_comment_text, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(sku_code, page_key, sub_id3, sub_id4) DO UPDATE SET
                product_name=excluded.product_name,
                clean_origin_url=excluded.clean_origin_url,
                sub_id5=excluded.sub_id5,
                sub_id_combined=excluded.sub_id_combined,
                auto_deeplink_url=excluded.auto_deeplink_url,
                pinned_comment_text=CASE
                    WHEN shopee_page_links.short_aff_url IS NULL OR shopee_page_links.short_aff_url = ''
                    THEN excluded.pinned_comment_text
                    ELSE shopee_page_links.pinned_comment_text
                END,
                updated_at=CURRENT_TIMESTAMP
            """,
            (
                sku_code,
                name,
                sub1,
                p["page_id"],
                p["page_name"],
                clean_url,
                sub1,
                sub2,
                sub3,
                sub4,
                sub5,
                sub_combined,
                auto_link,
                "",
                pinned_text,
            ),
        )
        generated_rows.append(
            {
                "page_key": sub1,
                "page_name": p["page_name"],
                "page_id": p["page_id"],
                "clean_origin_url": clean_url,
                "sub_id1": sub1,
                "sub_id2": sub2,
                "sub_id3": sub3,
                "sub_id4": sub4,
                "sub_id5": sub5,
                "auto_deeplink_url": auto_link,
                "pinned_comment_text": pinned_text,
            }
        )

    conn.commit()
    conn.close()

    csv_path = export_custom_link_batch_csv()
    return {
        "sku_code": sku_code,
        "name": name,
        "shop_id": shop_id,
        "item_id": item_id,
        "clean_origin_url": clean_url,
        "affiliate_id_configured": bool(aff_id),
        "pages": generated_rows,
        "batch_csv_path": str(csv_path),
    }


def export_custom_link_batch_csv() -> Path:
    """
    Xuất file CSV chuẩn 6 cột (`Link gốc`, `Sub_id1`..`Sub_id5`) tương thích với
    công cụ "Chuyển đổi link hàng loạt" tại https://affiliate.shopee.vn/offer/custom_link
    """
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = EXPORT_DIR / "shopee_custom_link_batch.csv"
    conn = init_db()
    cur = conn.cursor()
    rows = cur.execute(
        """
        SELECT clean_origin_url, sub_id1, sub_id2, sub_id3, sub_id4, sub_id5,
               page_name, product_name, COALESCE(short_aff_url, auto_deeplink_url)
        FROM shopee_page_links
        ORDER BY updated_at DESC, id ASC
        """
    ).fetchall()
    conn.close()

    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Product Link (Link gốc Shopee)",
                "Sub_id1 (Page)",
                "Sub_id2 (SKU)",
                "Sub_id3 (Format)",
                "Sub_id4 (Date_Slot)",
                "Sub_id5 (Hook)",
                "Tên Fanpage",
                "Tên Sản Phẩm",
                "Link Đang Dùng (Shortlink / Auto Deeplink)",
            ]
        )
        for r in rows:
            writer.writerow(r)
    return csv_path


def import_shopee_conversion_report(csv_file: Path) -> int:
    """
    Đọc file CSV Báo Cáo Chuyển Đổi / Báo Cáo Click tải về từ:
      https://affiliate.shopee.vn/report/conversion_report
    Tự động gom nhóm theo `Sub_id1` (`ktx`, `deadline`, `phongtro`) và `Sub_id2` (`sku_code`).
    """
    if not csv_file.exists():
        print(f"❌ Không tìm thấy file báo cáo tại: {csv_file}")
        return 1

    conn = init_db()
    cur = conn.cursor()

    with open(csv_file, "r", encoding="utf-8-sig", errors="ignore") as f:
        reader = csv.DictReader(f)
        inserted = 0
        for row in reader:
            # Linh hoạt nhận diện tên cột tiếng Việt hoặc tiếng Anh của Shopee Affiliate CSV
            sub1 = (
                row.get("Sub_id1")
                or row.get("Sub_id 1")
                or row.get("sub_id1")
                or row.get("Sub ID 1")
                or ""
            ).strip()
            sub2 = (
                row.get("Sub_id2")
                or row.get("Sub_id 2")
                or row.get("sub_id2")
                or row.get("Sub ID 2")
                or ""
            ).strip()
            sub_raw = (
                row.get("Sub_id")
                or row.get("Mã Sub_id")
                or f"{sub1}-{sub2}"
            ).strip()

            if not sub1 and "-" in sub_raw:
                parts = sub_raw.split("-")
                sub1 = parts[0]
                if len(parts) > 1 and not sub2:
                    sub2 = parts[1]

            def to_float(val: str) -> float:
                if not val:
                    return 0.0
                cleaned = re.sub(r"[^\d.\-]", "", str(val).replace(",", ""))
                try:
                    return float(cleaned)
                except Exception:
                    return 0.0

            clicks = int(to_float(row.get("Clicks") or row.get("Lượt click") or row.get("Số lượt click") or "0"))
            orders = int(
                to_float(
                    row.get("Orders")
                    or row.get("Đơn hàng")
                    or row.get("Số đơn hàng")
                    or row.get("Valid Orders")
                    or "1"
                )
            )
            sales = to_float(
                row.get("Gross Sales")
                or row.get("Giá trị đơn hàng (₫)")
                or row.get("Doanh thu")
                or "0"
            )
            comm = to_float(
                row.get("Net Commission")
                or row.get("Hoa hồng ròng (₫)")
                or row.get("Tổng hoa hồng")
                or row.get("Estimated Commission")
                or "0"
            )
            r_date = (
                row.get("Conversion Time")
                or row.get("Thời gian đặt hàng")
                or row.get("Date")
                or datetime.date.today().isoformat()
            )[:10]

            cur.execute(
                """
                INSERT INTO shopee_conversions (
                    report_date, page_key, sku_code, sub_id_raw,
                    clicks, valid_orders, gross_sales_vnd, net_commission_vnd
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (r_date, sub1 or "untagged", sub2 or "unknown_sku", sub_raw, clicks, orders, sales, comm),
            )
            inserted += 1

    conn.commit()
    conn.close()
    print(f"✅ Đã nạp thành công {inserted} dòng dữ liệu chuyển đổi từ '{csv_file.name}' vào SQLite!")
    print_dashboard_summary()
    return 0


def print_dashboard_summary() -> int:
    conn = init_db()
    cur = conn.cursor()
    aff_id = get_affiliate_id()

    print("\n" + "=" * 82)
    print(" 🛒 BẢNG ĐIỀU KHIỂN QUẢN LÝ SẢN PHẨM & LINK SHOPEE AFFILIATE (3 PAGE BÁN HÀNG)")
    print("=" * 82)
    if aff_id:
        print(f"🔑 Trạng thái Tài Khoản Cá Nhân : ✅ ĐÃ KẾT NỐI (`SHOPEE_AFFILIATE_ID = {aff_id}`)")
    else:
        print(
            "🔑 Trạng thái Tài Khoản Cá Nhân : ⚠️ CHƯA LƯU `SHOPEE_AFFILIATE_ID`\n"
            "   👉 Cách lấy 1 lần duy nhất: Dán 1 link rút gọn `https://s.shopee.vn/xxxx` bất kỳ của bạn vào lệnh:\n"
            "      `python tools/shopee_link_manager.py --extract-aff-id https://s.shopee.vn/xxxx`"
        )

    links = cur.execute(
        """
        SELECT sku_code, product_name, page_key, page_name, sub_id_combined,
               COALESCE(NULLIF(short_aff_url, ''), auto_deeplink_url) AS active_link
        FROM shopee_page_links
        ORDER BY sku_code, id
        """
    ).fetchall()

    print("-" * 82)
    print(f"📦 DANH SÁCH LINK ĐÃ PHÂN BỔ CHO 3 PAGE ({len(links)} Link):")
    for r in links:
        sku, pname, pkey, pgname, sub_comb, link = r
        print(f"  • [{pkey.upper():8s}] {pgname:20s} | SKU: `{sku}` ({pname[:28]})")
        print(f"    ├─ Sub_ID : `{sub_comb}`")
        print(f"    └─ Link   : {link}")

    conv = cur.execute(
        """
        SELECT page_key, SUM(clicks), SUM(valid_orders), SUM(gross_sales_vnd), SUM(net_commission_vnd)
        FROM shopee_conversions
        GROUP BY page_key
        """
    ).fetchall()
    if conv:
        print("-" * 82)
        print("📊 BÁO CÁO ĐỐI SOÁT CHUYỂN ĐỔI THEO TỪNG PAGE (TỪ SHOPEE CSV):")
        for c in conv:
            pkey, clk, ords, sales, comm = c
            cvr = round((ords / clk) * 100, 2) if clk and clk > 0 else 0.0
            print(
                f"  • Page `{pkey}`: Clicks={clk:,} | Đơn hợp lệ={ords:,} (CVR: {cvr}%) "
                f"| Doanh số={sales:,.0f}đ | Hoa hồng={comm:,.0f}đ"
            )

    print("=" * 82 + "\n")
    conn.close()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Quản lý Link Shopee Affiliate, Kho SKU & Đối soát Chuyển đổi cho 3 Page Bán Hàng"
    )
    parser.add_argument(
        "--extract-aff-id",
        type=str,
        default=None,
        help="Truyền 1 link rút gọn s.shopee.vn/... bất kỳ của bạn để tự động lấy và lưu SHOPEE_AFFILIATE_ID",
    )
    parser.add_argument(
        "--set-aff-id",
        type=str,
        default=None,
        help="Lưu trực tiếp mã SHOPEE_AFFILIATE_ID (VD: 173xxxxxx) vào .env",
    )
    parser.add_argument("--add-sku", type=str, default=None, help="Mã định danh ngắn của sản phẩm (VD: quat_imi_5000)")
    parser.add_argument("--name", type=str, default=None, help="Tên hiển thị của sản phẩm")
    parser.add_argument("--url", type=str, default=None, help="Link gốc sản phẩm trên Shopee")
    parser.add_argument("--price", type=int, default=0, help="Giá bán sản phẩm (VNĐ)")
    parser.add_argument("--commission", type=str, default="12% (Xtra)", help="Mức hoa hồng dự kiến")
    parser.add_argument("--format", type=str, default="reel_ai", help="Định dạng nội dung (reel_ai / img_1x1)")
    parser.add_argument("--slot", type=str, default="", help="Khung giờ đăng (VD: 20261021_1145)")
    parser.add_argument("--hook", type=str, default="hook_before_after", help="Góc Hook 3s đầu")
    parser.add_argument(
        "--import-report",
        type=str,
        default=None,
        help="Đường dẫn tới file CSV Báo Cáo Chuyển Đổi tải từ affiliate.shopee.vn",
    )
    parser.add_argument(
        "--scan-fb-sales-pages",
        action="store_true",
        help="Quét các bài đăng và bình luận ghim hiện tại trên 3 Page Bán Hàng",
    )
    parser.add_argument(
        "--upgrade-live-fb-comments",
        action="store_true",
        help="Tự động gắn mã SHOPEE_AFFILIATE_ID và Sub_ID vào toàn bộ 6 Pinned Comment đang chạy trên 3 Fanpage",
    )
    parser.add_argument("--status", action="store_true", help="Hiển thị bảng tổng hợp SKU & Link của 3 Page")

    args = parser.parse_args()

    if args.upgrade_live_fb_comments:
        return upgrade_live_fb_comments()

    if args.extract_aff_id:
        aff_id = extract_affiliate_id_from_shortlink(args.extract_aff_id)
        if aff_id:
            save_env_key("SHOPEE_AFFILIATE_ID", aff_id)
            refresh_all_links_with_aff_id(aff_id)
            print(f"✅ Đã giải mã thành công và lưu `SHOPEE_AFFILIATE_ID={aff_id}` vào `.env`!")
            return print_dashboard_summary()
        print(
            "⚠️ Không tìm thấy `affiliate_id` trong URL chuyển hướng. "
            "Hãy đảm bảo đây là link rút gọn tạo từ tài khoản Shopee Affiliate của bạn, hoặc dùng `--set-aff-id <mã_số>`."
        )
        return 1

    if args.set_aff_id:
        clean_id = re.sub(r"^an_", "", args.set_aff_id.strip())
        save_env_key("SHOPEE_AFFILIATE_ID", clean_id)
        refresh_all_links_with_aff_id(clean_id)
        print(f"✅ Đã lưu `SHOPEE_AFFILIATE_ID={clean_id}` vào `.env`!")
        return print_dashboard_summary()

    if args.scan_fb_sales_pages:
        return scan_fb_sales_pages()

    if args.add_sku and args.url:
        res = add_product_and_generate_3page_links(
            sku_code=args.add_sku,
            name=args.name or args.add_sku,
            raw_url=args.url,
            price_vnd=args.price,
            commission=args.commission,
            content_format=args.format,
            date_slot=args.slot,
            hook_angle=args.hook,
        )
        print(f"✅ Đã thêm SKU `{res['sku_code']}` ({res['name']}) và tự động tạo bộ 3 Link cho 3 Page!")
        print(f"📄 File Batch CSV chuẩn `affiliate.shopee.vn/offer/custom_link`: {res['batch_csv_path']}")
        return print_dashboard_summary()

    if args.import_report:
        return import_shopee_conversion_report(Path(args.import_report))

    return print_dashboard_summary()


if __name__ == "__main__":
    sys.exit(main())
