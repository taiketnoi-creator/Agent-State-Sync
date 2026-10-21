#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fb_publish_image_post.py — Công cụ 0-Token Đăng Ảnh Local + Tạo Bình Luận Đầu Tiên (Pinned Comment #1) lên Facebook Page.
Sử dụng 100% thư viện chuẩn Python (urllib.request multipart/form-data), không phụ thuộc thư viện ngoài.
"""

import argparse
import json
import mimetypes
import sys
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


def post_local_photo(page_id: str, page_token: str, image_path: Path, caption: str) -> dict:
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    mime_type = mimetypes.guess_type(image_path.name)[0] or "image/jpeg"
    img_bytes = image_path.read_bytes()

    body = bytearray()
    for field_name, field_val in [("caption", caption), ("access_token", page_token)]:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{field_name}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{field_val}\r\n".encode("utf-8"))

    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(
        f'Content-Disposition: form-data; name="source"; filename="{image_path.name}"\r\n'.encode("utf-8")
    )
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    body.extend(img_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{page_id}/photos"
    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30.0) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except urllib.error.HTTPError as e:
        err_text = e.read().decode("utf-8", errors="ignore")
        return {"error": err_text, "status_code": e.code}


def post_comment(target_id: str, page_token: str, message: str) -> dict:
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{target_id}/comments"
    data = urllib.parse.urlencode({"message": message, "access_token": page_token}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20.0) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except urllib.error.HTTPError as e:
        err_text = e.read().decode("utf-8", errors="ignore")
        return {"error": err_text, "status_code": e.code}


def main() -> int:
    parser = argparse.ArgumentParser(description="Đăng bài ảnh local kèm Comment #1 lên Facebook Page")
    parser.add_argument("--page", type=str, default="AI Players", help="Tên, STT hoặc ID Fanpage")
    parser.add_argument("--image", type=str, required=True, help="Đường dẫn file ảnh local")
    parser.add_argument("--caption-file", type=str, default=None, help="File văn bản chứa caption")
    parser.add_argument("--caption", type=str, default=None, help="Chuỗi caption trực tiếp")
    parser.add_argument("--comment-file", type=str, default=None, help="File văn bản chứa Pinned Comment #1")
    parser.add_argument("--comment", type=str, default=None, help="Chuỗi Pinned Comment #1 trực tiếp")
    args = parser.parse_args()

    img_path = Path(args.image)
    if not img_path.is_file():
        print(f"❌ Không tìm thấy file ảnh: {img_path}")
        return 1

    caption = args.caption or ""
    if args.caption_file:
        caption = Path(args.caption_file).read_text(encoding="utf-8").strip()

    first_comment = args.comment or ""
    if args.comment_file:
        first_comment = Path(args.comment_file).read_text(encoding="utf-8").strip()

    page_id, page_token, page_name = get_page_credentials(args.page)
    if not page_id or not page_token:
        print("❌ Chưa có thông tin xác thực Page.")
        return 1

    res = post_local_photo(page_id, page_token, img_path, caption)
    if "error" in res:
        print(f"❌ Lỗi đăng ảnh lên {page_name}: {res['error']}")
        return 1

    photo_id = res.get("id", "")
    post_id = res.get("post_id", f"{page_id}_{photo_id}")
    cmt_res = {}
    if first_comment:
        cmt_res = post_comment(post_id, page_token, first_comment)
        if "error" in cmt_res and photo_id:
            cmt_res = post_comment(photo_id, page_token, first_comment)

    output = {
        "status": "PUBLISHED",
        "page_name": page_name,
        "page_id": page_id,
        "image": str(img_path),
        "photo_id": photo_id,
        "post_id": post_id,
        "post_url": f"https://www.facebook.com/{post_id}",
        "first_comment_id": cmt_res.get("id", None),
        "first_comment_error": cmt_res.get("error", None),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
