#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fb_publish_video_reel.py — Công cụ 0-Token Đăng Video Reels (`video_reels` / `videos`) + Lên Lịch Giờ Vàng + Tạo Comment #1 lên Facebook Page.
Hỗ trợ:
1. Đăng trực tiếp Facebook Reels (`/{page_id}/video_reels` 3-phase upload) hoặc lên lịch (`--schedule-time "YYYY-MM-DD HH:MM"` giờ VN +07:00).
2. Tự động fallback sang `https://graph-video.facebook.com/v22.0/{page_id}/videos` nếu endpoint `video_reels` hạn chế quyền hoặc khi hẹn giờ.
3. Tự động đăng bình luận đầu tiên (`Comment #1`) ngay dưới Reel/Video vừa xuất bản.
"""

import argparse
import datetime
import json
import mimetypes
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

FB_MCP_DIR = Path.home() / ".codex" / "mcp" / "facebook-mcp-server"
ENV_PATH = FB_MCP_DIR / ".env"
VAULT_PATH = FB_MCP_DIR / "pages_vault.json"
GRAPH_VERSION = "v22.0"
VN_TZ = datetime.timezone(datetime.timedelta(hours=7))


def get_page_credentials(page_selector: str | None = None) -> tuple[str, str, str]:
    if page_selector and VAULT_PATH.exists():
        vault = json.loads(VAULT_PATH.read_text(encoding="utf-8", errors="ignore"))
        pages = vault.get("pages", [])
        if page_selector.isdigit() and 1 <= int(page_selector) <= len(pages):
            p = pages[int(page_selector) - 1]
            return p["id"], p["access_token"], p["name"]
        sel_low = page_selector.strip().lower()
        for p in pages:
            if p["id"] == page_selector.strip() or sel_low in p["name"].lower():
                return p["id"], p["access_token"], p["name"]

    env_data = {}
    if ENV_PATH.exists():
        for raw in ENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env_data[k.strip()] = v.strip().strip('"').strip("'")
    pid = env_data.get("FACEBOOK_PAGE_ID", "")
    tok = env_data.get("FACEBOOK_ACCESS_TOKEN", "")
    return pid, tok, "Active Page"


def parse_vn_schedule_time(time_str: str | None) -> int | None:
    if not time_str:
        return None
    time_str = time_str.strip()
    if time_str.isdigit():
        return int(time_str)
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
        try:
            dt = datetime.datetime.strptime(time_str, fmt).replace(tzinfo=VN_TZ)
            return int(dt.timestamp())
        except ValueError:
            continue
    raise ValueError(f"Không nhận diện được định dạng thời gian: {time_str} (Dùng YYYY-MM-DD HH:MM)")


def upload_via_reels_api(
    page_id: str,
    page_token: str,
    video_path: Path,
    title: str,
    description: str,
    schedule_ts: int | None = None,
) -> dict:
    """Thực hiện 3 bước chuẩn của Facebook Reels Publishing API (`/{page_id}/video_reels`)."""
    # Bước 1: Khởi tạo phiên upload
    start_url = f"https://graph.facebook.com/{GRAPH_VERSION}/{page_id}/video_reels"
    start_data = json.dumps({"upload_phase": "start", "access_token": page_token}).encode("utf-8")
    req_start = urllib.request.Request(
        start_url,
        data=start_data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req_start, timeout=30.0) as resp:
            start_res = json.loads(resp.read().decode("utf-8", errors="ignore"))
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode("utf-8", errors="ignore"), "phase": "start", "status_code": e.code}

    video_id = start_res.get("video_id")
    upload_url = start_res.get("upload_url")
    if not video_id or not upload_url:
        return {"error": f"Thiếu video_id hoặc upload_url: {start_res}", "phase": "start"}

    # Bước 2: Đẩy binary file lên rupload.facebook.com
    video_bytes = video_path.read_bytes()
    req_upload = urllib.request.Request(
        upload_url,
        data=video_bytes,
        headers={
            "Authorization": f"OAuth {page_token}",
            "offset": "0",
            "file_size": str(len(video_bytes)),
            "Content-Type": "application/octet-stream",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req_upload, timeout=180.0) as resp:
            upload_res = json.loads(resp.read().decode("utf-8", errors="ignore"))
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode("utf-8", errors="ignore"), "phase": "upload", "status_code": e.code}

    # Bước 3: Kết thúc & Publish (hoặc Schedule) Reel
    finish_params = {
        "access_token": page_token,
        "video_id": video_id,
        "upload_phase": "finish",
        "description": description,
    }
    if title:
        finish_params["title"] = title
    if schedule_ts:
        finish_params["video_state"] = "SCHEDULED"
        finish_params["scheduled_publish_time"] = str(schedule_ts)
    else:
        finish_params["video_state"] = "PUBLISHED"

    finish_data = urllib.parse.urlencode(finish_params).encode("utf-8")
    req_finish = urllib.request.Request(start_url, data=finish_data, method="POST")
    try:
        with urllib.request.urlopen(req_finish, timeout=60.0) as resp:
            finish_res = json.loads(resp.read().decode("utf-8", errors="ignore"))
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode("utf-8", errors="ignore"), "phase": "finish", "status_code": e.code}

    return {
        "success": True,
        "endpoint": "video_reels",
        "video_id": video_id,
        "post_id": finish_res.get("post_id", video_id),
        "upload_res": upload_res,
        "finish_res": finish_res,
    }


def upload_via_videos_api(
    page_id: str,
    page_token: str,
    video_path: Path,
    title: str,
    description: str,
    schedule_ts: int | None = None,
) -> dict:
    """Fallback đăng qua `https://graph-video.facebook.com/v22.0/{page_id}/videos` (hỗ trợ cả xuất bản ngay & hẹn giờ)."""
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    mime_type = mimetypes.guess_type(video_path.name)[0] or "video/mp4"
    video_bytes = video_path.read_bytes()

    fields = [
        ("access_token", page_token),
        ("description", description),
    ]
    if title:
        fields.append(("title", title))
    if schedule_ts:
        fields.append(("published", "false"))
        fields.append(("scheduled_publish_time", str(schedule_ts)))
    else:
        fields.append(("published", "true"))

    body = bytearray()
    for field_name, field_val in fields:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{field_name}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{field_val}\r\n".encode("utf-8"))

    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(
        f'Content-Disposition: form-data; name="source"; filename="{video_path.name}"\r\n'.encode("utf-8")
    )
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    body.extend(video_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    url = f"https://graph-video.facebook.com/{GRAPH_VERSION}/{page_id}/videos"
    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180.0) as resp:
            res = json.loads(resp.read().decode("utf-8", errors="ignore"))
            vid = res.get("id", "")
            return {
                "success": True,
                "endpoint": "videos",
                "video_id": vid,
                "post_id": res.get("post_id", vid),
                "raw": res,
            }
    except urllib.error.HTTPError as e:
        err_text = e.read().decode("utf-8", errors="ignore")
        return {"error": err_text, "endpoint": "videos", "status_code": e.code}


def post_comment_with_retry(target_ids: list[str], page_token: str, message: str, retries: int = 4) -> dict:
    """Đợi Facebook xử lý Reel/Video vài giây rồi đăng Comment #1."""
    last_err = {}
    for attempt in range(retries):
        for tid in target_ids:
            if not tid:
                continue
            url = f"https://graph.facebook.com/{GRAPH_VERSION}/{tid}/comments"
            data = urllib.parse.urlencode({"message": message, "access_token": page_token}).encode("utf-8")
            req = urllib.request.Request(url, data=data, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=20.0) as resp:
                    return json.loads(resp.read().decode("utf-8", errors="ignore"))
            except urllib.error.HTTPError as e:
                last_err = {"error": e.read().decode("utf-8", errors="ignore"), "status_code": e.code}
        if attempt < retries - 1:
            time.sleep(4.0)
    return last_err


def main() -> int:
    parser = argparse.ArgumentParser(description="Đăng Video Reel local hoặc Lên lịch Giờ Vàng lên Facebook Page")
    parser.add_argument("--page", type=str, default="AI Players", help="Tên, STT hoặc ID Fanpage")
    parser.add_argument("--video", type=str, required=True, help="Đường dẫn file .mp4 local")
    parser.add_argument("--title", type=str, default="", help="Tiêu đề Reel / Video")
    parser.add_argument("--caption-file", type=str, default=None, help="File văn bản chứa caption")
    parser.add_argument("--caption", type=str, default=None, help="Chuỗi caption trực tiếp")
    parser.add_argument("--comment-file", type=str, default=None, help="File văn bản chứa Comment #1")
    parser.add_argument("--comment", type=str, default=None, help="Chuỗi Comment #1 trực tiếp")
    parser.add_argument(
        "--schedule-time",
        type=str,
        default=None,
        help="Thời gian hẹn giờ đăng (Giờ VN: 'YYYY-MM-DD HH:MM' hoặc Unix timestamp). Để trống = Đăng ngay.",
    )
    args = parser.parse_args()

    video_path = Path(args.video)
    if not video_path.is_file():
        print(f"❌ Không tìm thấy file video: {video_path}")
        return 1

    caption = args.caption or ""
    if args.caption_file:
        caption = Path(args.caption_file).read_text(encoding="utf-8").strip()

    first_comment = args.comment or ""
    if args.comment_file:
        first_comment = Path(args.comment_file).read_text(encoding="utf-8").strip()

    schedule_ts = parse_vn_schedule_time(args.schedule_time)

    page_id, page_token, page_name = get_page_credentials(args.page)
    if not page_id or not page_token:
        print("❌ Chưa có thông tin xác thực Page.")
        return 1

    # Ưu tiên gọi API Reels chính thức (`/{page_id}/video_reels`), nếu lỗi thì fallback sang `/{page_id}/videos`
    res = upload_via_reels_api(page_id, page_token, video_path, args.title, caption, schedule_ts)
    if "error" in res:
        res = upload_via_videos_api(page_id, page_token, video_path, args.title, caption, schedule_ts)

    if "error" in res:
        print(f"❌ Lỗi đăng video lên {page_name}: {res['error']}")
        return 1

    video_id = res.get("video_id", "")
    post_id = res.get("post_id", video_id)
    cmt_res = {}
    if first_comment and not schedule_ts:
        cmt_res = post_comment_with_retry([video_id, post_id, f"{page_id}_{video_id}"], page_token, first_comment)

    output = {
        "status": "SCHEDULED" if schedule_ts else "PUBLISHED",
        "endpoint": res.get("endpoint"),
        "page_name": page_name,
        "page_id": page_id,
        "video_file": str(video_path),
        "video_id": video_id,
        "post_id": post_id,
        "reel_url": f"https://www.facebook.com/reel/{video_id}",
        "watch_url": f"https://www.facebook.com/{page_id}/videos/{video_id}",
        "scheduled_publish_time_unix": schedule_ts,
        "scheduled_publish_time_vn": (
            datetime.datetime.fromtimestamp(schedule_ts, tz=VN_TZ).strftime("%Y-%m-%d %H:%M:%S (+07:00)")
            if schedule_ts
            else None
        ),
        "first_comment_id": cmt_res.get("id", None),
        "first_comment_error": cmt_res.get("error", None),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
