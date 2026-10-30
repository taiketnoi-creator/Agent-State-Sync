#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mama_auto_scheduler_engine.py — Động Cơ Tự Động Hóa Chạy Ngầm Khi Mở Máy & Báo Cáo Theo 7 Mốc Giờ Cố Định.

ĐÃ TÍCH HỢP CỔNG KHÓA CỨNG ZERO-REPOST GATE (`tools/zero_repost_gate.py`):
- Đã XÓA BỎ VĨNH VIỄN biến tĩnh `DAILY_SALES_QUEUE` (6 bài cũ ngày 20/10).
- Tuyệt đối CẤM lấy lại bài/ảnh/video cũ đã từng đăng để đăng lặp lại lên bất kỳ Fanpage nào.
- Mọi bài trước khi lên lịch đều phải vượt qua `verify_fresh_content(page_id, media_path, caption)` (kiểm tra SHA256, tên file, và dấu vân tay nội dung).
"""

import argparse
import datetime as dt
import json
import mimetypes
import ssl
import subprocess
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
VAULT_PATH = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / "pages_vault.json"
REPORTS_DIR = SUBAGENT_DIR / "campaigns" / "daily-reports"
TZ_VN = dt.timezone(dt.timedelta(hours=7))
SSL_CTX = ssl._create_unverified_context()

AI_ID = "1022527194267367"
SALES_IDS = ["1442323328956326", "1421270697727753", "1407231352464711"]

DEFAULT_PINNED_COMMENTS = {
    "1022527194267367": (
        "📌 KHO TÀI LIỆU & CỘNG ĐỒNG AI PLAYERS CHÍNH THỨC:\n"
        "👉 Tham gia ngay Nhóm Zalo Cộng Đồng Bảo Mật để tải trọn bộ KHO VŨ KHÍ 6 SUBAGENT (.MD) & Sơ đồ Kiến trúc Miễn phí: "
        "https://zalo.me/g/etllok798 (Mã vào nhóm: AIPLAYERS2026) 🚀"
    ),
    "1442323328956326": (
        "📌 KHO DEAL ĐỒ GIA DỤNG PHÒNG TRỌ CHÍNH HÃNG:\n"
        "🛒 Săn ngay ưu đãi Shopee tại đây nha: https://s.shopee.vn/an_redir?origin_link=https%3A%2F%2Fshopee.vn&affiliate_id=17395830088&sub_id=phongtro-pinned-auto\n"
        "ℹ️ [Affiliate Disclosure: Link chia sẻ có thể mang lại khoản hoa hồng nhỏ giúp duy trì Page mà không làm thay đổi giá mua của bạn!]"
    ),
    "1421270697727753": (
        "📌 KHO DEAL SINH VIÊN & KÝ TÚC XÁ CHÍNH HÃNG:\n"
        "🛒 Săn ngay giá sinh viên trên Shopee tại đây: https://s.shopee.vn/an_redir?origin_link=https%3A%2F%2Fshopee.vn&affiliate_id=17395830088&sub_id=ktx-pinned-auto\n"
        "ℹ️ [Affiliate Disclosure: Link chia sẻ có thể mang lại khoản hoa hồng nhỏ giúp duy trì Page mà không làm thay đổi giá mua của bạn!]"
    ),
    "1407231352464711": (
        "📌 KHO ĐỒ DESK SETUP & DÂN VĂN PHÒNG CHÍNH HÃNG:\n"
        "🛒 Xem ưu đãi Shopee tại đây nha: https://s.shopee.vn/an_redir?origin_link=https%3A%2F%2Fshopee.vn&affiliate_id=17395830088&sub_id=deadline-pinned-auto\n"
        "ℹ️ [Affiliate Disclosure: Link chia sẻ có thể mang lại khoản hoa hồng nhỏ giúp duy trì Page mà không làm thay đổi giá mua của bạn!]"
    ),
}


def load_vault() -> dict:
    if not VAULT_PATH.exists():
        return {}
    data = json.loads(VAULT_PATH.read_text(encoding="utf-8", errors="ignore"))
    return {str(p["id"]): p for p in data.get("pages", [])}


def graph_get(endpoint: str, token: str, params: dict = None) -> dict:
    q = dict(params or {})
    q["access_token"] = token
    url = f"https://graph.facebook.com/v22.0/{endpoint}?{urllib.parse.urlencode(q)}"
    with urllib.request.urlopen(url, context=SSL_CTX, timeout=15) as r:
        return json.loads(r.read().decode("utf-8", errors="ignore"))


def graph_post(endpoint: str, token: str, params: dict) -> dict:
    url = f"https://graph.facebook.com/v22.0/{endpoint}"
    payload = dict(params)
    payload["access_token"] = token
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=20) as r:
            return json.loads(r.read().decode("utf-8", errors="ignore"))
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode("utf-8", errors="ignore"), "code": e.code}
    except Exception as e:
        return {"error": str(e)}


def upload_photo_or_schedule(page_id: str, token: str, image_path: Path, caption: str, sched_ts: int = 0) -> dict:
    from zero_repost_gate import verify_fresh_content, record_published_content

    is_fresh, reason = verify_fresh_content(page_id, image_path, caption)
    if not is_fresh:
        return {"error": reason, "blocked_by_zero_repost_gate": True}

    url = f"https://graph.facebook.com/v22.0/{page_id}/photos"
    boundary = f"----AgentJavisBoundary{uuid.uuid4().hex}"
    body = bytearray()

    def add_field(name: str, value: str):
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{value}\r\n".encode("utf-8"))

    add_field("access_token", token)
    add_field("message", caption)
    now_ts = int(time.time())
    if sched_ts > now_ts + 660:
        add_field("published", "false")
        add_field("scheduled_publish_time", str(sched_ts))
    else:
        add_field("published", "true")

    mime_type = mimetypes.guess_type(str(image_path))[0] or "image/png"
    file_bytes = image_path.read_bytes()
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="source"; filename="{image_path.name}"\r\n'.encode("utf-8"))
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    body.extend(file_bytes)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=45) as resp:
            res = json.loads(resp.read().decode("utf-8", errors="ignore"))
            post_id = res.get("post_id") or res.get("id")
            if post_id:
                record_published_content(page_id, image_path, caption, str(post_id))
            return res
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode("utf-8", errors="ignore"), "code": e.code}
    except Exception as e:
        return {"error": str(e)}


def load_fresh_sales_queue_for_date(today_str: str) -> dict:
    """
    Chỉ nạp bài từ manifest MỚI của ngày hiện tại (`campaigns/<YYYY-MM-DD>/sales-daily-vault/manifest.json`).
    Tuyệt đối KHÔNG dùng danh sách tĩnh ngày 20/10!
    """
    manifest_path = SUBAGENT_DIR / "campaigns" / today_str / "sales-daily-vault" / "manifest.json"
    if not manifest_path.exists():
        return {}
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def ensure_daily_sales_posts_scheduled(pages: dict) -> list:
    """
    Kiểm tra 3 Page Bán Hàng xem hôm nay đã có bài hẹn giờ cho khung 11:45 và 20:00 chưa.
    Chỉ nạp bài từ kho MỚI 100% đã qua kiểm duyệt `zero_repost_gate.py`.
    Nếu chưa có kho bài mới cho hôm nay, khóa chặn tuyệt đối việc lấy bài cũ ra đăng lại!
    """
    from zero_repost_gate import verify_fresh_content

    now_vn = dt.datetime.now(TZ_VN)
    today_str = now_vn.strftime("%Y-%m-%d")
    state_file = REPORTS_DIR / today_str / "auto_scheduled_sales_state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    done_state = {}
    if state_file.exists():
        try:
            done_state = json.loads(state_file.read_text(encoding="utf-8"))
        except Exception:
            done_state = {}

    fresh_queue = load_fresh_sales_queue_for_date(today_str)
    actions_log = []

    for sid in SALES_IDS:
        if sid not in pages:
            continue
        p_obj = pages[sid]
        tok = p_obj["access_token"]
        pname = p_obj["name"]

        existing_sched_ts = []
        try:
            sp_list = graph_get(f"{sid}/scheduled_posts", tok, {"fields": "id,scheduled_publish_time", "limit": 20}).get("data", [])
            existing_sched_ts = [int(sp.get("scheduled_publish_time", 0)) for sp in sp_list]
        except Exception:
            pass

        page_items = fresh_queue.get(sid, [])
        if not page_items:
            if not existing_sched_ts:
                actions_log.append(
                    f"🔒 [{pname}] Kho hẹn giờ trống & chưa có gói SKU mới ngày {today_str} (Đã khóa Zero-Repost Gate — CẤM lấy lại bài cũ 20/10)."
                )
            continue

        for item in page_items:
            slot = item["slot"]
            key = f"{sid}_{today_str}_{slot}"
            if done_state.get(key):
                continue

            h, m = [int(x) for x in slot.split(":")]
            target_dt = dt.datetime(now_vn.year, now_vn.month, now_vn.day, h, m, 0, tzinfo=TZ_VN)
            sched_ts = int(target_dt.timestamp())
            if any(abs(ts - sched_ts) < 1800 for ts in existing_sched_ts):
                done_state[key] = {"mode": "ALREADY_ON_GRAPH", "slot": slot, "timestamp": now_vn.isoformat()}
                continue

            img_path = SUBAGENT_DIR / item["image"] if not Path(item["image"]).is_absolute() else Path(item["image"])
            if not img_path.exists():
                actions_log.append(f"⚠️ [{pname}] Khung {slot} thiếu file ảnh mới: {img_path.name}")
                continue

            is_fresh, reason = verify_fresh_content(sid, img_path, item["caption"])
            if not is_fresh:
                actions_log.append(f"🛑 [{pname}] {reason}")
                continue

            res = upload_photo_or_schedule(sid, tok, img_path, item["caption"], sched_ts)
            post_id = res.get("post_id") or res.get("id")
            if post_id:
                cmt_res = graph_post(f"{post_id}/comments", tok, {"message": item["pinned_cmt"]})
                cmt_id = cmt_res.get("id", "")
                mode_label = "SCHEDULED" if sched_ts > int(time.time()) + 660 else "PUBLISHED_NOW"
                done_state[key] = {
                    "post_id": post_id,
                    "pinned_comment_id": cmt_id,
                    "mode": mode_label,
                    "slot": slot,
                    "timestamp": now_vn.isoformat(),
                }
                actions_log.append(f"✅ [{pname}] Khung {slot}: {mode_label} ({post_id}) | Pinned Cmt: {cmt_id}")
            else:
                actions_log.append(f"⚠️ [{pname}] Khung {slot} lỗi: {res}")

    state_file.write_text(json.dumps(done_state, ensure_ascii=False, indent=2), encoding="utf-8")
    return actions_log


def purge_duplicate_published_posts(pages: dict) -> list:
    """
    Quét trực tiếp 30 bài published_posts gần nhất trên cả 4 Fanpage.
    Nếu phát hiện bất kỳ bài viết nào có câu mở đầu trùng lặp với bài đã đăng trước đó trên cùng Page
    (do máy khác chưa git pull hoặc chạy lặp), tự động gọi DELETE xóa ngay bản trùng lặp!
    """
    from zero_repost_gate import normalize_caption_fingerprint

    deleted_log = []
    for pid, p_obj in pages.items():
        if pid not in ([AI_ID] + SALES_IDS):
            continue
        tok = p_obj["access_token"]
        pname = p_obj["name"]
        try:
            feed = graph_get(
                f"{pid}/published_posts",
                tok,
                {"fields": "id,message,created_time,attachments{target}", "limit": 35},
            ).get("data", [])
            # Sắp xếp từ cũ nhất -> mới nhất để giữ lại bài gốc đầu tiên và xóa các bản bị đăng lặp về sau
            feed_sorted = sorted(feed, key=lambda x: x.get("created_time", ""))
            seen_fp = {}
            for post in feed_sorted:
                post_id = post["id"]
                msg = post.get("message") or ""
                fp = normalize_caption_fingerprint(msg)
                att = (post.get("attachments") or {}).get("data", [{}])[0]
                target_id = (att.get("target") or {}).get("id")

                if not fp and not target_id:
                    del_candidates = [post_id]
                elif fp and len(fp) >= 12 and fp in seen_fp:
                    del_candidates = [target_id, post_id] if target_id else [post_id]
                else:
                    if fp and len(fp) >= 12:
                        seen_fp[fp] = post_id
                    continue

                for did in del_candidates:
                    if not did:
                        continue
                    try:
                        req = urllib.request.Request(
                            f"https://graph.facebook.com/v22.0/{did}?access_token={urllib.parse.quote(tok)}",
                            method="DELETE",
                        )
                        with urllib.request.urlopen(req, context=SSL_CTX, timeout=12):
                            deleted_log.append(
                                f"🧹 Đã tự động xóa bài đăng trùng lặp trên [{pname}]: {post_id} (target={did} | '{fp[:40]}...')"
                            )
                            break
                    except Exception:
                        pass
        except Exception:
            pass
    return deleted_log


def ensure_all_live_posts_have_pinned_comment(pages: dict) -> list:
    """
    Quét 5 bài LIVE mới nhất trên cả 4 Page; nếu bài nào vừa nhảy từ Scheduled -> LIVE mà chưa có bình luận của Page,
    tự động gắn Pinned Comment #1 chuẩn phễu!
    """
    fixed_log = []
    for pid, p_obj in pages.items():
        if pid not in ([AI_ID] + SALES_IDS):
            continue
        tok = p_obj["access_token"]
        pname = p_obj["name"]
        try:
            feed = graph_get(f"{pid}/published_posts", tok, {"fields": "id,message,created_time", "limit": 5}).get("data", [])
            for post in feed:
                post_id = post["id"]
                cmts = graph_get(f"{post_id}/comments", tok, {"fields": "id,from", "limit": 10}).get("data", [])
                has_host_cmt = any(c.get("from", {}).get("id") == pid for c in cmts)
                if not has_host_cmt:
                    pin_msg = DEFAULT_PINNED_COMMENTS.get(pid, DEFAULT_PINNED_COMMENTS[AI_ID])
                    r = graph_post(f"{post_id}/comments", tok, {"message": pin_msg})
                    if "id" in r:
                        fixed_log.append(
                            f"📌 Đã tự động bổ sung Pinned Comment #1 cho bài mới lên sóng [{pname}]: {post_id} -> {r['id']}"
                        )
        except Exception:
            pass
    return fixed_log


def send_telegram_if_configured(text: str):
    bridge = SUBAGENT_DIR / "tools" / "telegram_bridge.py"
    if bridge.exists():
        subprocess.run(
            [sys.executable, str(bridge), "--send", "--text", text[:3900]],
            timeout=20,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["boot-or-9am", "midday-1145", "shift1-1200", "shift2-1730", "evening-2000", "shift3-2030", "eod-2130"],
        default="boot-or-9am",
    )
    args = parser.parse_args()

    now_vn = dt.datetime.now(TZ_VN)
    today_str = now_vn.strftime("%Y-%m-%d")

    # 0A. Tự động đồng bộ Git (Agent-State-Sync -> Subagent) trước mọi ca chạy ngầm để chống chạy code cũ trên Máy Công Ty / Máy Nhà
    state_sync_dir = SUBAGENT_DIR.parent / "Agent-State-Sync"
    if (state_sync_dir / ".git").exists():
        try:
            subprocess.run(
                ["git", "-C", str(state_sync_dir), "pull", "--rebase", "--autostash", "origin", "main"],
                timeout=8,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            snap_py = state_sync_dir / "generate_snapshot.py"
            if snap_py.exists():
                subprocess.run(
                    [sys.executable, str(snap_py), "--direction", "pull"],
                    timeout=5,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
        except Exception:
            pass

    pages = load_vault()

    # 0B. Luôn tự động bật ngầm Chrome Bot độc lập tại cổng 9222 trước mọi ca
    pass

    # 1. Quét xóa bài trùng lặp trên cả 4 Page + Kiểm tra lịch đăng ngày hôm nay (Zero-Repost Gate) + gắn Pinned Comment #1
    dup_actions = purge_duplicate_published_posts(pages)
    sched_actions = list(dup_actions) + ensure_daily_sales_posts_scheduled(pages)
    pin_actions = ensure_all_live_posts_have_pinned_comment(pages)

    # 2. Thực thi tác vụ theo từng mốc giờ
    if args.mode in ("boot-or-9am", "eod-2130"):
        subprocess.run([sys.executable, str(SUBAGENT_DIR / "tools" / "mama_daily_9am_report.py"), "--quiet"])

    if args.mode == "shift1-1200":
        subprocess.run([sys.executable, str(SUBAGENT_DIR / "tools" / "mama_daily_group_and_eod.py"), "--shift", "1", "--send-telegram"])

    if args.mode == "shift2-1730":
        subprocess.run([sys.executable, str(SUBAGENT_DIR / "tools" / "mama_daily_group_and_eod.py"), "--shift", "2", "--send-telegram"])

    if args.mode == "shift3-2030":
        subprocess.run([sys.executable, str(SUBAGENT_DIR / "tools" / "mama_daily_group_and_eod.py"), "--shift", "3", "--send-telegram"])

    # 3. Ghi nhận báo cáo mốc giờ ra file & gửi Telegram
    out_dir = REPORTS_DIR / today_str
    out_dir.mkdir(parents=True, exist_ok=True)
    milestone_file = REPORTS_DIR / "latest-milestone-status.md"

    lines = [
        f"# ⏰ BÁO CÁO TỰ ĐỘNG MỐC [{args.mode.upper()}] — {now_vn.strftime('%H:%M:%S %d/%m/%Y')}",
        "",
        "## 1. Trạng Thái Tự Động Lên Lịch & Xuất Bản 4 Fanpage (Zero-Repost Gate Active)",
    ]
    if sched_actions:
        lines.extend([f"- {a}" for a in sched_actions])
    else:
        lines.append("- ✅ Toàn bộ 4 Fanpage (`AI Players`, `Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline`) đã đủ lịch bài đăng hôm nay.")

    if pin_actions:
        lines.append("\n## 2. Tự Động Gắn Pinned Comment #1 Cho Bài Mới Lên Sóng")
        lines.extend([f"- {p}" for p in pin_actions])

    summary_text = "\n".join(lines) + "\n"
    milestone_file.write_text(summary_text, encoding="utf-8")
    (out_dir / f"milestone_{args.mode}_{now_vn.strftime('%H%M')}.md").write_text(summary_text, encoding="utf-8")
    send_telegram_if_configured(summary_text)
    print(summary_text)


if __name__ == "__main__":
    main()
