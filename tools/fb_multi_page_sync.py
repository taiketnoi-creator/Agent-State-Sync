#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fb_multi_page_sync.py — Công cụ Tự Động Lấy & Chuyển Đổi Nhiều Fanpage Facebook (0-Token).

Giải quyết bài toán quản lý dàn 5–20+ Fanpage mà KHÔNG cần copy tay từng Page ID & Token:
1. Chỉ cần 1 mã `FACEBOOK_USER_TOKEN` (User Access Token hoặc System User Token).
2. Tự động gọi Graph API `/me/accounts` lấy danh sách TOÀN BỘ Fanpage (kèm Page ID + Page Access Token riêng của từng Page).
3. Lưu toàn bộ vào kho bảo mật local `~/.codex/mcp/facebook-mcp-server/pages_vault.json` (đã khóa trong `.gitignore`).
4. Cho phép chuyển đổi Page đang hoạt động (`--use <số thứ tự / tên / ID>`) hoặc tự động nạp Page đầu tiên vào `.env`.

Cách dùng:
  - Quét & lưu toàn bộ Page từ FACEBOOK_USER_TOKEN trong .env:
      python tools/fb_multi_page_sync.py --sync
  - Xem danh sách các Page đã lưu trong kho:
      python tools/fb_multi_page_sync.py --list
  - Chuyển sang một Page khác (theo số thứ tự 1, 2... hoặc tên/ID):
      python tools/fb_multi_page_sync.py --use 1
      python tools/fb_multi_page_sync.py --use "AI Players"
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

FB_MCP_DIR = Path.home() / ".codex" / "mcp" / "facebook-mcp-server"
ENV_PATH = FB_MCP_DIR / ".env"
VAULT_PATH = FB_MCP_DIR / "pages_vault.json"
GRAPH_VERSION = "v22.0"


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


def update_env_active_page(page_id: str, page_token: str, page_name: str = "") -> None:
    env_data = parse_env(ENV_PATH)
    user_token = env_data.get(
        "FACEBOOK_USER_TOKEN",
        "DIEN_USER_TOKEN_VAO_DAY_DE_TU_DONG_LAY_TAT_CA_PAGE",
    )
    vbee_app = env_data.get("VBEE_APP_ID", "DIEN_VBEE_APP_ID_VAO_DAY")
    vbee_tok = env_data.get("VBEE_BEARER_TOKEN", "DIEN_VBEE_BEARER_TOKEN_VAO_DAY")
    viettel_tok = env_data.get("VIETTEL_TTS_TOKEN", "DIEN_VIETTEL_TTS_TOKEN_VAO_DAY")
    content = (
        "# ============================================================================\n"
        "# 1. CẤU HÌNH KẾT NỐI FACEBOOK PAGE CHO MCP SERVER (Bảo mật local)\n"
        "# ============================================================================\n"
        f"# Page đang kích hoạt: {page_name} (ID: {page_id})\n"
        f"FACEBOOK_USER_TOKEN={user_token}\n"
        f"FACEBOOK_PAGE_ID={page_id}\n"
        f"FACEBOOK_ACCESS_TOKEN={page_token}\n\n"
        "# ============================================================================\n"
        "# 2. CẤU HÌNH GIỌNG ĐỌC VBEE AIVOICE / VIETTEL AI TTS (Chọn 1 trong 2 hoặc cả 2)\n"
        "# ============================================================================\n"
        f"VBEE_APP_ID={vbee_app}\n"
        f"VBEE_BEARER_TOKEN={vbee_tok}\n"
        f"VIETTEL_TTS_TOKEN={viettel_tok}\n"
    )
    FB_MCP_DIR.mkdir(parents=True, exist_ok=True)
    ENV_PATH.write_text(content, encoding="utf-8")


def sync_all_pages(user_token: str | None = None) -> int:
    env_data = parse_env(ENV_PATH)
    token = user_token or env_data.get("FACEBOOK_USER_TOKEN", "")
    placeholders = {
        "",
        "DIEN_USER_TOKEN_VAO_DAY_DE_TU_DONG_LAY_TAT_CA_PAGE",
        "YOUR_USER_TOKEN",
    }
    if token in placeholders:
        print(
            "❌ Chưa có FACEBOOK_USER_TOKEN trong file .env!\n"
            f"👉 Hãy dán 1 mã User Access Token vào dòng FACEBOOK_USER_TOKEN=... trong file: {ENV_PATH}"
        )
        return 1

    pages = []
    next_url = (
        f"https://graph.facebook.com/{GRAPH_VERSION}/me/accounts"
        f"?fields=id,name,access_token,category,fan_count&limit=100&access_token={urllib.parse.quote(token)}"
    )

    try:
        while next_url:
            req = urllib.request.Request(next_url, method="GET")
            with urllib.request.urlopen(req, timeout=8.0) as resp:
                payload = json.loads(resp.read().decode("utf-8", errors="ignore"))
                for item in payload.get("data", []):
                    if "id" in item and "access_token" in item:
                        pages.append(
                            {
                                "id": item["id"],
                                "name": item.get("name", "Unnamed Page"),
                                "category": item.get("category", ""),
                                "fan_count": item.get("fan_count", 0),
                                "access_token": item["access_token"],
                            }
                        )
                next_url = payload.get("paging", {}).get("next")
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode("utf-8", errors="ignore"))
            msg = err.get("error", {}).get("message", f"HTTP {e.code}")
        except Exception:
            msg = f"HTTP {e.code}"
        print(f"❌ Lỗi từ Facebook Graph API: {msg}")
        return 1
    except Exception as e:
        print(f"❌ Không thể kết nối tới Facebook Graph API: {e}")
        return 1

    if not pages:
        print(
            "⚠️ Token hợp lệ nhưng không tìm thấy Fanpage nào! "
            "Hãy kiểm tra xem bạn đã tích chọn các quyền `pages_show_list`, `pages_manage_posts`, `pages_read_engagement` và chọn đúng các Page khi tạo Token chưa."
        )
        return 1

    vault_data = {
        "active_page_id": pages[0]["id"],
        "active_page_name": pages[0]["name"],
        "total_pages": len(pages),
        "pages": pages,
    }
    FB_MCP_DIR.mkdir(parents=True, exist_ok=True)
    VAULT_PATH.write_text(json.dumps(vault_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # Mặc định kích hoạt Page đầu tiên vào .env
    update_env_active_page(pages[0]["id"], pages[0]["access_token"], pages[0]["name"])

    print(f"✅ ĐÃ TỰ ĐỘNG LẤY THÀNH CÔNG {len(pages)} FANPAGE VÀO KHO BẢO MẬT LOCAL!")
    print("-" * 70)
    for idx, p in enumerate(pages, start=1):
        active_mark = "👉 [ĐANG ACTIVE]" if idx == 1 else "   "
        print(f"{active_mark} #{idx:02d} | {p['name']} | ID: {p['id']} | Follows: {p.get('fan_count', 0)}")
    print("-" * 70)
    print("💡 Muốn chuyển sang Page khác, chạy: python tools/fb_multi_page_sync.py --use <số_thứ_tự_hoặc_tên_page>")
    return 0


def list_saved_pages() -> int:
    if not VAULT_PATH.exists():
        print("ℹ️ Chưa có kho `pages_vault.json`. Hãy chạy `python tools/fb_multi_page_sync.py --sync` trước.")
        return 0
    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8", errors="ignore"))
    active_id = vault.get("active_page_id", "")
    pages = vault.get("pages", [])
    print(f"📋 DANH SÁCH {len(pages)} FANPAGE ĐÃ LƯU TRONG KHO LOCAL:")
    print("-" * 70)
    for idx, p in enumerate(pages, start=1):
        mark = "👉 [ACTIVE]" if p["id"] == active_id else "          "
        print(f"{mark} #{idx:02d} | {p['name']} | ID: {p['id']} | Follows: {p.get('fan_count', 0)}")
    print("-" * 70)
    return 0


def switch_active_page(selector: str) -> int:
    if not VAULT_PATH.exists():
        print("❌ Chưa có kho `pages_vault.json`. Hãy chạy `--sync` trước.")
        return 1
    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8", errors="ignore"))
    pages = vault.get("pages", [])
    if not pages:
        print("❌ Kho Fanpage đang trống.")
        return 1

    chosen = None
    # 1. Theo số thứ tự (1-based)
    if selector.isdigit() and 1 <= int(selector) <= len(pages):
        chosen = pages[int(selector) - 1]
    else:
        # 2. Theo Page ID chính xác hoặc tên Page (không phân biệt hoa thường)
        sel_low = selector.strip().lower()
        for p in pages:
            if p["id"] == selector.strip() or sel_low in p["name"].lower():
                chosen = p
                break

    if not chosen:
        print(f"❌ Không tìm thấy Fanpage khớp với '{selector}'. Chạy `--list` để xem danh sách.")
        return 1

    vault["active_page_id"] = chosen["id"]
    vault["active_page_name"] = chosen["name"]
    VAULT_PATH.write_text(json.dumps(vault, ensure_ascii=False, indent=2), encoding="utf-8")
    update_env_active_page(chosen["id"], chosen["access_token"], chosen["name"])
    print(f"✅ Đã chuyển Page hoạt động sang: **{chosen['name']}** (ID: `{chosen['id']}`)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Quản lý & đồng bộ tự động nhiều Fanpage Facebook")
    parser.add_argument("--sync", action="store_true", help="Tự động lấy toàn bộ Page ID & Page Token từ FACEBOOK_USER_TOKEN")
    parser.add_argument("--token", type=str, default=None, help="Truyền trực tiếp User Access Token khi chạy --sync")
    parser.add_argument("--list", action="store_true", help="Hiển thị danh sách các Fanpage đã lưu")
    parser.add_argument("--use", type=str, default=None, help="Chuyển đổi Fanpage đang kích hoạt (theo STT, Tên hoặc Page ID)")
    args = parser.parse_args()

    if args.sync:
        return sync_all_pages(args.token)
    if args.use:
        return switch_active_page(args.use)
    return list_saved_pages()


if __name__ == "__main__":
    sys.exit(main())
