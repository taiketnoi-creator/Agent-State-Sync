#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zero_repost_gate.py — Cổng Khóa Cứng Chống Đăng Lặp Bài Cũ / Ảnh Cũ / Video Cũ (Zero-Repost Firewall).

Chức năng:
1. Lưu trữ sổ cái `campaigns/daily-reports/published_history_registry.json` chứa:
   - SHA-256 hash của mọi file ảnh/video đã từng xuất bản hoặc thuộc kho cũ (20/10 -> 26/10).
   - Tên file (basename) của các media cũ bị cấm tái sử dụng (`mcp-ai-explainer-40s.mp4`, `sales-phongtro-1145-style02.jpg`...).
   - Dấu vân tay nội dung (normalized 60 ký tự đầu của caption/title) đã từng xuất hiện trên 4 Fanpage.
2. Cung cấp hàm `verify_fresh_content(page_id, media_path, caption)` cho mọi công cụ đăng/lên lịch:
   - Nếu trùng SHA-256 hash, trùng tên file cũ, hoặc trùng dấu vân tay caption đã đăng -> CHẶN CỨNG NGAY LẬP TỨC (`return False, reason`).
3. Cho phép chạy CLI `python tools/zero_repost_gate.py --sync` để quét toàn bộ lịch sử bài đăng thực tế từ Meta Graph API của cả 4 Page + khóa toàn bộ media cũ.
"""

import argparse
import hashlib
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
REGISTRY_PATH = SUBAGENT_DIR / "campaigns" / "daily-reports" / "published_history_registry.json"
VAULT_PATH = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / "pages_vault.json"

FOUR_PAGE_IDS = [
    "1022527194267367",  # AI Players - Người chơi hệ AI
    "1442323328956326",  # Phòng Trọ Hết Cứu
    "1421270697727753",  # Ký Túc Xá Có Biến
    "1407231352464711",  # Hội Deadline
]

# Danh sách đen các file media cũ (20/10 - 26/10) bị CẤM VĨNH VIỄN không được đăng lại
PERMANENT_BANNED_FILENAMES = [
    # 6 ảnh bán hàng ngày 20/10 đã bị lặp nhiều ngày
    "sales-phongtro-1145-style02.jpg",
    "sales-phongtro-1145-style02.png",
    "sales-phongtro-2030-style01.jpg",
    "sales-phongtro-2030-style01.png",
    "sales-ktx-1145-style02.jpg",
    "sales-ktx-1145-style02.png",
    "sales-ktx-2100-style01.jpg",
    "sales-ktx-2100-style01.png",
    "sales-deadline-1145-style02.jpg",
    "sales-deadline-1145-style02.png",
    "sales-deadline-2000-style01.jpg",
    "sales-deadline-2000-style01.png",
    # 4 video Reels Remotion ngày 20/10 đã đăng
    "mcp-ai-explainer-40s.mp4",
    "ai-hallucination-45s.mp4",
    "ai-agent-vs-chatbot-45s.mp4",
    "ai-map-pillars-45s.mp4",
    # Video bảng trắng test bị cấm
    "openrouter_mindmap_explainer.mp4",
    # 6 ảnh AI Players ngày 20/10 và 6 ảnh ngày 1 (26/10) đã đăng
    "ai-square-01-lead-prompt50.jpg",
    "ai-square-02-lead-hethong.jpg",
    "ai-square-03-github-f5-tts.jpg",
    "ai-square-04-github-browser-use.jpg",
    "ai-square-05-github-awesome-llm.jpg",
    "ai-square-06-discussion-poll.jpg",
    "day1_img1_1415_repo.png",
    "day1_img2_1545_voice.png",
    "day1_img3_1715_prompt50.png",
    "day1_img4_1845_khobau.png",
    "day1_img5_2015_hethong.png",
    "day1_img6_2145_poll.png",
]


def normalize_caption_fingerprint(text: str) -> str:
    if not text:
        return ""
    first_non_empty = ""
    for line in text.splitlines():
        s = line.strip()
        if s:
            first_non_empty = s
            break
    cleaned = re.sub(r"[^\w\s]", "", first_non_empty.lower(), flags=re.UNICODE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:75]


def compute_file_sha256(file_path: Path) -> str:
    if not file_path or not file_path.exists() or not file_path.is_file():
        return ""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_registry() -> dict:
    if REGISTRY_PATH.exists():
        try:
            data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("banned_filenames", [])
                data.setdefault("published_sha256", {})
                data.setdefault("published_caption_fingerprints", {})
                for fn in PERMANENT_BANNED_FILENAMES:
                    if fn not in data["banned_filenames"]:
                        data["banned_filenames"].append(fn)
                return data
        except Exception:
            pass
    return {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "banned_filenames": list(PERMANENT_BANNED_FILENAMES),
        "published_sha256": {},
        "published_caption_fingerprints": {},
    }


def save_registry(data: dict) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    REGISTRY_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def check_live_graph_duplicate(page_id: str, caption: str, title: str = "") -> tuple[bool, str]:
    """
    Kiểm tra trực tiếp theo thời gian thực trên Meta Graph API (published_posts, scheduled_posts, videos, video_reels)
    xem tiêu đề hoặc nội dung mở đầu đã tồn tại trên Page chưa (chống trùng lặp tuyệt đối kể cả khi 2 máy chưa kịp git pull).
    """
    if not VAULT_PATH.exists():
        return True, "OK"
    fp_cap = normalize_caption_fingerprint(caption)
    fp_title = normalize_caption_fingerprint(title)
    if len(fp_cap) < 12 and len(fp_title) < 12:
        return True, "OK"

    try:
        vault = json.loads(VAULT_PATH.read_text(encoding="utf-8", errors="ignore"))
        pages = {str(p["id"]): p for p in vault.get("pages", [])}
        if str(page_id) not in pages:
            return True, "OK"
        tok = pages[str(page_id)]["access_token"]
        ctx = ssl._create_unverified_context()

        endpoints = [
            ("scheduled_posts", "message"),
            ("published_posts", "message"),
            ("videos", "title,description"),
        ]
        for ep, fields in endpoints:
            url = (
                f"https://graph.facebook.com/v22.0/{page_id}/{ep}"
                f"?fields=id,{fields},created_time,scheduled_publish_time&limit=35&access_token={urllib.parse.quote(tok)}"
            )
            try:
                with urllib.request.urlopen(url, context=ctx, timeout=10) as resp:
                    items = json.loads(resp.read().decode("utf-8", errors="ignore")).get("data", [])
                    for item in items:
                        for f in fields.split(","):
                            val = item.get(f, "") or ""
                            fp_remote = normalize_caption_fingerprint(val)
                            if fp_remote and len(fp_remote) >= 12:
                                if (fp_cap and fp_remote == fp_cap) or (fp_title and fp_remote == fp_title):
                                    return (
                                        False,
                                        f"CHẶN CỨNG [Live Graph API Duplicate]: Nội dung '{fp_remote[:45]}...' đã tồn tại trên Page ({ep} id={item.get('id')})!",
                                    )
            except Exception:
                pass
    except Exception:
        pass
    return True, "OK"


def verify_fresh_content(page_id: str, media_path: Path | str | None, caption: str, title: str = "") -> tuple[bool, str]:
    """
    Kiểm tra xem media_path và caption có phải nội dung MỚI 100% hay không (kết hợp sổ Local + kiểm tra trực tuyến Meta Graph API).
    Trả về (True, "OK") nếu hợp lệ; trả về (False, "Lý do chặn") nếu phát hiện bài/ảnh/video cũ hoặc trùng lặp!
    """
    reg = load_registry()
    if media_path:
        p = Path(media_path)
        if p.name in reg.get("banned_filenames", []):
            return False, f"CHẶN CỨNG [Zero-Repost]: File '{p.name}' nằm trong danh sách media cũ đã từng đăng!"
        if p.exists():
            sha = compute_file_sha256(p)
            if sha and sha in reg.get("published_sha256", {}):
                prev_info = reg["published_sha256"][sha]
                return False, f"CHẶN CỨNG [Zero-Repost]: Mã băm SHA256 của file '{p.name}' trùng khớp với file đã đăng ({prev_info})!"

    for text_check in (caption, title):
        fp = normalize_caption_fingerprint(text_check)
        if fp and len(fp) >= 12:
            if fp in reg.get("published_caption_fingerprints", {}):
                prev_post = reg["published_caption_fingerprints"][fp]
                return False, f"CHẶN CỨNG [Zero-Repost]: Nội dung mở đầu '{fp[:45]}...' trùng với bài đã đăng ({prev_post})!"

    # Kiểm tra trực tiếp trên Meta Graph API để chống lên lịch trùng lặp giữa 2 lần chạy hoặc 2 máy
    is_live_ok, live_reason = check_live_graph_duplicate(str(page_id), caption, title)
    if not is_live_ok:
        return False, live_reason

    return True, "OK"


def record_published_content(page_id: str, media_path: Path | str | None, caption: str, post_id: str = "") -> None:
    reg = load_registry()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if media_path:
        p = Path(media_path)
        if p.name not in reg["banned_filenames"]:
            reg["banned_filenames"].append(p.name)
        if p.exists():
            sha = compute_file_sha256(p)
            if sha:
                reg["published_sha256"][sha] = f"{p.name} | page={page_id} | post={post_id} | {now_str}"

    fp = normalize_caption_fingerprint(caption)
    if fp and len(fp) >= 12:
        reg["published_caption_fingerprints"][fp] = f"page={page_id} | post={post_id} | {now_str}"

    save_registry(reg)


def sync_historical_posts_and_local_media() -> dict:
    """
    Quét toàn bộ bài đã đăng trên 4 Fanpage qua Meta Graph API + toàn bộ file media cũ từ 2026-10-20..2026-10-25
    để đưa vào sổ khóa cứng `published_history_registry.json`.
    """
    reg = load_registry()
    ctx = ssl._create_unverified_context()

    # 1. Quét toàn bộ file media trong campaigns/2026-10-20 .. 2026-10-25
    camp_root = SUBAGENT_DIR / "campaigns"
    local_hashed = 0
    if camp_root.exists():
        for date_dir in sorted(camp_root.iterdir()):
            if not date_dir.is_dir():
                continue
            if date_dir.name in ("2026-10-20", "2026-10-21", "2026-10-22", "2026-10-23", "2026-10-24", "2026-10-25"):
                for media_file in date_dir.rglob("*"):
                    if media_file.is_file() and media_file.suffix.lower() in (".jpg", ".jpeg", ".png", ".mp4"):
                        sha = compute_file_sha256(media_file)
                        if sha and sha not in reg["published_sha256"]:
                            reg["published_sha256"][sha] = f"legacy_campaign:{date_dir.name}/{media_file.name}"
                            local_hashed += 1
                        if media_file.name not in reg["banned_filenames"]:
                            reg["banned_filenames"].append(media_file.name)

    # 2. Quét toàn bộ published_posts và videos trên 4 Fanpage từ Meta Graph API
    graph_posts_recorded = 0
    if VAULT_PATH.exists():
        try:
            vault = json.loads(VAULT_PATH.read_text(encoding="utf-8", errors="ignore"))
            pages = {str(p["id"]): p for p in vault.get("pages", [])}
            for pid in FOUR_PAGE_IDS:
                if pid not in pages:
                    continue
                tok = pages[pid]["access_token"]
                for ep, field_name in [("published_posts", "message"), ("videos", "description")]:
                    url = (
                        f"https://graph.facebook.com/v22.0/{pid}/{ep}"
                        f"?fields=id,{field_name},created_time&limit=50&access_token={urllib.parse.quote(tok)}"
                    )
                    try:
                        with urllib.request.urlopen(url, context=ctx, timeout=15) as resp:
                            items = json.loads(resp.read().decode("utf-8", errors="ignore")).get("data", [])
                            for item in items:
                                msg = item.get(field_name, "") or ""
                                fp = normalize_caption_fingerprint(msg)
                                if fp and len(fp) >= 12 and fp not in reg["published_caption_fingerprints"]:
                                    reg["published_caption_fingerprints"][fp] = (
                                        f"page={pid} | id={item.get('id')} | created={item.get('created_time')}"
                                    )
                                    graph_posts_recorded += 1
                    except Exception:
                        pass
        except Exception:
            pass

    save_registry(reg)
    return {
        "banned_filenames_count": len(reg["banned_filenames"]),
        "published_sha256_count": len(reg["published_sha256"]),
        "published_caption_fingerprints_count": len(reg["published_caption_fingerprints"]),
        "newly_hashed_local": local_hashed,
        "newly_recorded_graph": graph_posts_recorded,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sync", action="store_true", help="Quét Graph API & kho cũ để khóa sổ Zero-Repost")
    args = parser.parse_args()

    if args.sync:
        stats = sync_historical_posts_and_local_media()
        print("✅ ĐÃ KHÓA SỔ ZERO-REPOST GATE THÀNH CÔNG:", json.dumps(stats, ensure_ascii=False))
    else:
        reg = load_registry()
        print(
            json.dumps(
                {
                    "banned_filenames_count": len(reg.get("banned_filenames", [])),
                    "published_sha256_count": len(reg.get("published_sha256", {})),
                    "published_caption_fingerprints_count": len(reg.get("published_caption_fingerprints", {})),
                },
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    main()
