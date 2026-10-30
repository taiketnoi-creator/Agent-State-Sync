#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cleanup_cloned_vault_posts.py — Xóa toàn bộ các bài ảnh bị bê nguyên mẫu MagentX (có chữ Zoom / 2 buổi / logo Higgsfield)
trên Fanpage AI Players (1022527194267367) để thay bằng ảnh thiết kế độc bản đúng phong cách.
"""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
VAULT_DIR = SUBAGENT_DIR / "campaigns" / "2026-10-26" / "ai-players-weekly-vault"
RESULTS_PATH = VAULT_DIR / "meta_schedule_results.json"
VAULT_PATH = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / "pages_vault.json"
AI_PAGE_ID = "1022527194267367"
GRAPH_VERSION = "v22.0"


def get_token() -> str:
    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
    for p in vault.get("pages", []):
        if str(p.get("id")) == AI_PAGE_ID:
            return p.get("access_token", "")
    return ""


def delete_object(token: str, obj_id: str) -> bool:
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{obj_id}?access_token={token}"
    req = urllib.request.Request(url, method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=20.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return bool(data.get("success", True))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="ignore")
        # Try with page_id prefix if bare photo id failed
        if "_" not in obj_id:
            return delete_object(token, f"{AI_PAGE_ID}_{obj_id}")
        print(f"  ⚠️ Không xóa được {obj_id}: {err[:120]}")
        return False


def main():
    token = get_token()
    if not token:
        print("❌ Không tìm thấy token!")
        return

    deleted = 0
    if RESULTS_PATH.exists():
        data = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
        items = data.get("items", [])
        print(f"🔍 Đang thu hồi {len(items)} bài ảnh bê nguyên mẫu từ meta_schedule_results.json...")
        for it in items:
            pid = str(it.get("post_id", ""))
            code = it.get("code", "")
            if pid:
                ok = delete_object(token, pid)
                if ok:
                    deleted += 1
                    print(f"  🗑️ Đã xóa {code} ({pid})")

    # Quét thêm scheduled_posts để đảm bảo không sót bài ảnh lỗi nào
    sched_url = f"https://graph.facebook.com/{GRAPH_VERSION}/{AI_PAGE_ID}/scheduled_posts?fields=id,message,scheduled_publish_time&access_token={token}&limit=100"
    try:
        with urllib.request.urlopen(sched_url, timeout=20.0) as resp:
            sdata = json.loads(resp.read().decode("utf-8"))
            print(f"📊 Số bài còn trong scheduled_posts sau khi dọn: {len(sdata.get('data', []))}")
            for p in sdata.get("data", []):
                print("  - Giữ lại (Video Reel):", p.get("id"), p.get("message", "")[:50].replace("\n", " "))
    except Exception as e:
        print("Lỗi kiểm tra scheduled_posts:", e)

    print(f"\n✅ Đã thu hồi sạch {deleted} bài ảnh bê nguyên mẫu!")


if __name__ == "__main__":
    main()
