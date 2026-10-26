#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
schedule_weekly_batch.py — Tự Động Lên Lịch Bài Viết Hàng Loạt Từ Kho Tuần Lên Facebook Graph API
Hỗ trợ đặt lịch an toàn theo chuẩn Meta v22.0 (scheduled_publish_time >= 600s).
"""

import argparse
import datetime as dt
import json
import mimetypes
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
VAULT_DIR = SUBAGENT_DIR / "campaigns" / "2026-10-26" / "ai-players-weekly-vault"
MANIFEST_PATH = VAULT_DIR / "master_vault_manifest.json"
VAULT_PATH = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / "pages_vault.json"
VN_TZ = dt.timezone(dt.timedelta(hours=7))
AI_PAGE_ID = "1022527194267367"
GRAPH_VERSION = "v22.0"


def get_token() -> str:
    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
    for p in vault.get("pages", []):
        if str(p.get("id")) == AI_PAGE_ID:
            return p.get("access_token", "")
    return ""


def schedule_photo(token: str, img_path: Path, caption: str, sched_ts: int) -> dict:
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{AI_PAGE_ID}/photos"
    boundary = f"----AgentJavisBoundary{uuid.uuid4().hex}"
    body = bytearray()

    def add_field(name: str, value: str):
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{value}\r\n".encode("utf-8"))

    add_field("access_token", token)
    add_field("message", caption)
    add_field("published", "false")
    add_field("scheduled_publish_time", str(sched_ts))

    mime_type = mimetypes.guess_type(str(img_path))[0] or "image/jpeg"
    file_bytes = img_path.read_bytes()

    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="source"; filename="{img_path.name}"\r\n'.encode("utf-8"))
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    body.extend(file_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=40.0) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        return {"error": err_msg, "code": e.code}


def get_existing_scheduled_slots(token: str) -> set:
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{AI_PAGE_ID}/scheduled_posts?fields=id,scheduled_publish_time&access_token={token}&limit=100"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            slots = set()
            for p in data.get("data", []):
                ts = p.get("scheduled_publish_time", 0)
                if ts:
                    dt_str = dt.datetime.fromtimestamp(ts, tz=VN_TZ).strftime("%Y-%m-%d %H:%M")
                    slots.add(dt_str)
            return slots
    except Exception as e:
        print(f"⚠️ Không thể quét lịch hiện tại: {e}")
        return set()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=str, default="2", help="Danh sách ngày cần nạp lịch (ví dụ '2' hoặc '2,3')")
    args = parser.parse_args()

    token = get_token()
    if not token:
        print("❌ Không tìm thấy Access Token của Fanpage AI Players!")
        return

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    existing_slots = get_existing_scheduled_slots(token)
    print(f"📊 Đang có {len(existing_slots)} mốc giờ đã được hẹn trên Page AI.")

    target_days = [int(d.strip()) for d in args.days.split(",") if d.strip().isdigit()]

    now_ts = int(time.time())
    success_count = 0

    for day_data in manifest.get("image_matrix", []):
        day_num = day_data["day"]
        if day_num not in target_days:
            continue
        date_str = day_data["date"]
        print(f"\n📅 Bắt đầu xử lý Ngày {day_num} ({date_str}):")

        for post in day_data.get("posts", []):
            slot = post["slot"]
            slot_str = f"{date_str} {slot}"
            if slot_str in existing_slots:
                print(f"  ⏩ Bỏ qua {slot_str}: Đã có bài được hẹn giờ trước đó.")
                continue

            target_dt = dt.datetime.strptime(slot_str, "%Y-%m-%d %H:%M").replace(tzinfo=VN_TZ)
            sched_ts = int(target_dt.timestamp())

            if sched_ts <= now_ts + 600:
                print(f"  ⚠️ Bỏ qua {slot_str}: Thời gian hẹn trong quá khứ hoặc dưới 10 phút.")
                continue

            img_path = SUBAGENT_DIR / post["image_file_assembled"]
            cap_path = SUBAGENT_DIR / post["caption_file"]

            if not img_path.exists() or not cap_path.exists():
                print(f"  ❌ Thiếu tệp ảnh hoặc caption cho {slot_str}")
                continue

            caption = cap_path.read_text(encoding="utf-8")
            res = schedule_photo(token, img_path, caption, sched_ts)

            if "id" in res:
                post_id = res["id"]
                post["post_id"] = post_id
                post["status"] = "SCHEDULED_ON_META"
                print(f"  ✅ Đã hẹn giờ thành công {slot_str} -> Post ID: {post_id}")
                success_count += 1
                existing_slots.add(slot_str)
                time.sleep(1.5)  # Tránh rate limit
            else:
                print(f"  ❌ Lỗi khi hẹn giờ {slot_str}: {res}")

    # Ghi nhận kết quả vào manifest
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n🎉 Hoàn thành nạp lịch batch! Đã lên lịch thành công thêm {success_count} bài.")


if __name__ == "__main__":
    main()
