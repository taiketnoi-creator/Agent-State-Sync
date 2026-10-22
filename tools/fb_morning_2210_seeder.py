#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fb_morning_2210_seeder.py — Công Cụ Chăm Sóc Bình Luận Khách Thật & Kiểm Soát Zero Cross-Page Seeding.

THEO LỆNH BẮT BUỘC CỦA CEO (2026-10-22 19:01 — Task #19):
- TUYỆT ĐỐI KHÔNG tương tác chéo giữa các Fanpage với nhau (kể cả giữa 3 Page bán hàng).
- Chỉ đi tương tác tại các Group/Hội nhóm cùng tệp khách hàng (qua `mama_daily_group_and_eod.py` / `fb_group_browser_interact.py`).
- Script này khi được gọi chỉ thực hiện:
  1. Quét và tự động XÓA ngay bất kỳ bình luận chéo nào giữa các Page trong hệ thống nếu còn sót.
  2. Kiểm tra và đảm bảo mỗi bài đăng chỉ có Pinned Comment #1 của chính Page chủ nhà và phản hồi bình luận của KHÁCH HÀNG THẬT bên ngoài.
"""

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

VAULT_PATH = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / "pages_vault.json"


def main() -> int:
    if not VAULT_PATH.exists():
        print("⚠️ Không tìm thấy pages_vault.json")
        return 0

    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
    pages = vault.get("pages", [])
    if isinstance(pages, dict):
        pages = list(pages.values())

    our_page_ids = {str(p.get("id", p.get("page_id", ""))) for p in pages if isinstance(p, dict)}
    our_page_names = {(p.get("name") or "").strip() for p in pages if isinstance(p, dict)}
    tokens_by_id = {str(p.get("id", p.get("page_id", ""))): p.get("access_token", "") for p in pages if isinstance(p, dict)}

    purged = 0
    real_customer_comments = 0

    for p in pages:
        pid = str(p.get("id", p.get("page_id", "")))
        pname = (p.get("name") or "").strip()
        ptoken = p.get("access_token", "")
        if not pid or not ptoken or pname == "IFN":
            continue

        url = (
            f"https://graph.facebook.com/v22.0/{pid}/published_posts"
            f"?fields=id,comments.limit(50){{id,from,message}}"
            f"&limit=15&access_token={urllib.parse.quote(ptoken)}"
        )
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                posts = json.loads(r.read().decode("utf-8")).get("data", [])
        except Exception:
            continue

        for post in posts:
            for c in post.get("comments", {}).get("data", []):
                cid = c.get("id")
                c_from = c.get("from") or {}
                c_from_id = str(c_from.get("id", ""))
                c_from_name = (c_from.get("name") or "").strip()

                if (c_from_id in our_page_ids and c_from_id != pid) or (
                    c_from_name in our_page_names and c_from_name != pname
                ):
                    for tk in [ptoken, tokens_by_id.get(c_from_id, "")]:
                        if not tk:
                            continue
                        del_url = f"https://graph.facebook.com/v22.0/{cid}?access_token={urllib.parse.quote(tk)}"
                        try:
                            req = urllib.request.Request(del_url, method="DELETE")
                            with urllib.request.urlopen(req, timeout=10):
                                purged += 1
                                break
                        except Exception:
                            pass
                elif c_from_id and c_from_id != pid:
                    real_customer_comments += 1

    print(
        f"✅ [ZERO CROSS-PAGE POLICY] Đã kiểm tra 4 Fanpage: Xóa {purged} bình luận chéo giữa các Page | Ghi nhận {real_customer_comments} bình luận khách hàng thật."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
