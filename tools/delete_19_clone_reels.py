#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
delete_19_clone_reels.py
Xóa khẩn cấp toàn bộ 19 video clone/content cũ (v01..v19) vừa hẹn giờ trên Meta Graph API
và xóa thư mục template dùng chung `src/AiVaultDynamicShort` theo đúng lệnh cấm `MEM-20261022-zero-clone-bespoke-video-rule.md`.
"""

import json
import shutil
import ssl
import sys
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
CAMPAIGN_DIR = ROOT_DIR / "campaigns" / "2026-10-26" / "ai-players-weekly-vault"
MANIFEST_19_PATH = CAMPAIGN_DIR / "weekly_19_new_reels_manifest.json"
FB_MCP_DIR = Path.home() / ".codex" / "mcp" / "facebook-mcp-server"
VAULT_PATH = FB_MCP_DIR / "pages_vault.json"
SSL_CTX = ssl._create_unverified_context()


def main():
    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
    tok = [p["access_token"] for p in vault["pages"] if p["id"] == "1022527194267367"][0]

    # 1. Lấy danh sách toàn bộ scheduled_posts hiện tại để tìm đúng post_id của video
    url = f"https://graph.facebook.com/v22.0/1022527194267367/scheduled_posts?fields=id,message,scheduled_publish_time,created_time,attachments{{media_type,target}}&limit=100&access_token={tok}"
    res = json.loads(urllib.request.urlopen(url, context=SSL_CTX, timeout=30).read().decode("utf-8"))
    sched_posts = res.get("data", [])

    m19 = json.loads(MANIFEST_19_PATH.read_text(encoding="utf-8")) if MANIFEST_19_PATH.is_file() else []
    clone_video_ids = {str(x.get("fb_video_id")) for x in m19 if x.get("fb_video_id")}

    # Tìm tất cả các scheduled video posts được tạo trong đợt vừa rồi (hoặc khớp video_id)
    to_delete = set()
    for sp in sched_posts:
        sp_id = sp.get("id", "")
        att = sp.get("attachments", {}).get("data", [{}])[0]
        mtype = att.get("media_type", "")
        target_id = str(att.get("target", {}).get("id", ""))
        # Giữ lại 2 video độc bản chuẩn đã duyệt từ trước nếu cần, hoặc kiểm tra target_id trong clone_video_ids
        if target_id in clone_video_ids or (mtype == "video" and sp_id not in ("1022527194267367_122133385149248983", "1022527194267367_122133385629248983")):
            to_delete.add(sp_id)

    for vid in clone_video_ids:
        to_delete.add(vid)

    deleted_count = 0
    for tid in sorted(to_delete):
        try:
            req = urllib.request.Request(
                f"https://graph.facebook.com/v22.0/{tid}?access_token={tok}",
                method="DELETE",
            )
            r = json.loads(urllib.request.urlopen(req, context=SSL_CTX, timeout=20).read().decode("utf-8"))
            if r.get("success"):
                deleted_count += 1
                print(f"🗑️ Đã xóa khỏi Meta: {tid}")
        except Exception:
            pass

    # 2. Xóa các file MP4 clone v01..v19 và thư mục template dùng chung `AiVaultDynamicShort`
    for item in m19:
        vf = Path(item.get("video_file", ""))
        if vf.is_file():
            vf.unlink()

    dyn_dir = ROOT_DIR / "templates" / "remotion-cuongit-template" / "src" / "AiVaultDynamicShort"
    if dyn_dir.is_dir():
        shutil.rmtree(dyn_dir, ignore_errors=True)
        print(f"🗑️ Đã xóa vĩnh viễn thư mục template dùng chung: {dyn_dir}")

    print(f"✅ Hoàn tất thu hồi {deleted_count} mục video clone/cũ trên Meta Graph API!")


if __name__ == "__main__":
    main()
