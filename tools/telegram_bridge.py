#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
telegram_bridge.py — Cầu nối điều khiển 2 chiều qua Telegram cho Mama (Chief of Staff) & Đội 9 Subagent.
Hỗ trợ:
1. Tầng Lệnh Nhanh 0-Token (xử lý tức thì bằng Python):
   /start, /status, /pages, /switch, /tasks, /sync, /help
2. Tầng Giao Việc Tự Do (Natural Language Task):
   - Lưu yêu cầu vào bảng `telegram_tasks` trong SQLite (`aff_system.db`).
   - Khi chạy ở chế độ `--listen-and-wake` (Background Task của Antigravity), ngay khi có lệnh giao việc mới
     từ CEO trên Telegram, script phản hồi xác nhận trên Telegram rồi kết thúc với mã 0 để kích hoạt
     cơ chế Reactive Wakeup đánh thức `mama` (Gemini 4) dậy xử lý ngay lập tức!
3. Gửi báo cáo kết quả & hình ảnh đính kèm về lại khung chat Telegram của CEO (`--reply`, `--send`).
"""

import argparse
import datetime
import json
import mimetypes
import os
import sqlite3
import subprocess
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

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
STATE_SYNC_DIR = SUBAGENT_DIR.parent / "Agent-State-Sync"
FB_MCP_DIR = Path.home() / ".codex" / "mcp" / "facebook-mcp-server"
ENV_PATH = FB_MCP_DIR / ".env"


def parse_env_file(env_path: Path) -> dict:
    data = {}
    if not env_path.exists():
        return data
    try:
        for raw_line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass
    return data


def set_env_key(env_path: Path, key: str, value: str) -> None:
    env_path.parent.mkdir(parents=True, exist_ok=True)
    lines = env_path.read_text(encoding="utf-8", errors="ignore").splitlines() if env_path.exists() else []
    updated = False
    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={value}")
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        new_lines.append(f"{key}={value}")
    env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def get_db_path() -> Path:
    candidates = [
        Path.home() / ".gemini" / "antigravity" / "scratch" / "ai-aff-video-system" / "data" / "aff_system.db",
        SUBAGENT_DIR / "database" / "aff_system.db",
        SUBAGENT_DIR / "data" / "aff_system.db",
    ]
    for p in candidates:
        if p.exists():
            return p
    default_db = SUBAGENT_DIR / "database" / "aff_system.db"
    default_db.parent.mkdir(parents=True, exist_ok=True)
    return default_db


def init_db() -> sqlite3.Connection:
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS telegram_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            user_name TEXT,
            message_id INTEGER,
            task_text TEXT NOT NULL,
            status TEXT DEFAULT 'PENDING',
            created_at TEXT,
            reply_text TEXT,
            completed_at TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS telegram_state (
            k TEXT PRIMARY KEY,
            v TEXT
        )
        """
    )
    conn.commit()
    return conn


def get_state(conn: sqlite3.Connection, key: str, default: str = "") -> str:
    cur = conn.execute("SELECT v FROM telegram_state WHERE k = ?", (key,))
    row = cur.fetchone()
    return row["v"] if row else default


def set_state(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        "INSERT INTO telegram_state (k, v) VALUES (?, ?) ON CONFLICT(k) DO UPDATE SET v = excluded.v",
        (key, str(value)),
    )
    conn.commit()


def get_bot_config() -> tuple[str, str]:
    env = parse_env_file(ENV_PATH)
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or env.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID") or env.get("TELEGRAM_CHAT_ID", "")
    if not token:
        raise RuntimeError(f"Chưa tìm thấy TELEGRAM_BOT_TOKEN trong {ENV_PATH}")
    return token, str(chat_id).strip()


def tg_api(token: str, method: str, payload: dict | None = None, timeout: float = 25.0) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    if payload is None:
        req = urllib.request.Request(url, method="GET")
    else:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=raw,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="ignore"))


def tg_send_message(token: str, chat_id: str | int, text: str, reply_to: int | None = None) -> dict:
    payload = {
        "chat_id": str(chat_id),
        "text": text[:4000],
        "disable_web_page_preview": True,
    }
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    try:
        return tg_api(token, "sendMessage", payload, timeout=15.0)
    except Exception as e:
        return {"ok": False, "error": str(e)}


def tg_send_photo(token: str, chat_id: str | int, photo_path: str, caption: str = "") -> dict:
    p = Path(photo_path)
    if not p.exists():
        return tg_send_message(token, chat_id, f"{caption}\n\n⚠️ (Không tìm thấy file ảnh: {photo_path})")

    boundary = f"----MamaBoundary{uuid.uuid4().hex}"
    body = bytearray()

    def add_field(name: str, val: str):
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{val}\r\n".encode("utf-8"))

    add_field("chat_id", str(chat_id))
    if caption:
        add_field("caption", caption[:1000])

    mime_type = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(
        f'Content-Disposition: form-data; name="photo"; filename="{p.name}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8")
    )
    body.extend(p.read_bytes())
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30.0) as resp:
        return json.loads(resp.read().decode("utf-8", errors="ignore"))


def setup_bot_commands(token: str) -> dict:
    commands = [
        {"command": "start", "description": "Kết nối & khóa bảo mật tài khoản Sếp với Mama"},
        {"command": "status", "description": "Báo cáo khởi động phiên & Tiến độ dự án (0-token)"},
        {"command": "pages", "description": "Xem danh sách 5 Fanpage & lượt theo dõi"},
        {"command": "switch", "description": "Đổi Fanpage đang kích hoạt (VD: /switch 1)"},
        {"command": "tasks", "description": "Xem danh sách việc đã giao cho Mama & trạng thái"},
        {"command": "sync", "description": "Đồng bộ lịch sử công việc lên GitHub ngay"},
        {"command": "help", "description": "Hướng dẫn giao việc cho Mama & đội 9 Subagent"},
    ]
    return tg_api(token, "setMyCommands", {"commands": commands}, timeout=10.0)


def format_pages_list() -> str:
    vault_path = FB_MCP_DIR / "pages_vault.json"
    env = parse_env_file(ENV_PATH)
    active_id = env.get("FACEBOOK_PAGE_ID", "")
    if not vault_path.exists():
        return f"📄 Active Page ID hiện tại: {active_id or 'Chưa cấu hình'}"
    try:
        vdata = json.loads(vault_path.read_text(encoding="utf-8", errors="ignore"))
        pages = vdata.get("pages", [])
        lines = ["📊 DANH SÁCH FANPAGE TRONG KHO CỦA SẾP:\n"]
        for idx, p in enumerate(pages, 1):
            pid = str(p.get("id", ""))
            name = p.get("name", "Unknown")
            fans = p.get("fan_count", 0)
            marker = "✅ [ĐANG ACTIVE]" if pid == active_id else "⚪"
            lines.append(f"{idx}. {marker} {name}\n   • ID: {pid} | Follows: {fans}")
        lines.append("\n💡 Gõ `/switch <số thứ tự>` (VD: `/switch 1`) để chuyển Fanpage active.")
        return "\n".join(lines)
    except Exception as e:
        return f"⚠️ Lỗi đọc kho Fanpage: {e}"


def handle_switch_page(arg: str) -> str:
    vault_path = FB_MCP_DIR / "pages_vault.json"
    if not vault_path.exists():
        return "⚠️ Chưa có file pages_vault.json."
    vdata = json.loads(vault_path.read_text(encoding="utf-8", errors="ignore"))
    pages = vdata.get("pages", [])
    arg = arg.strip()
    if not arg:
        return "⚠️ Vui lòng nhập số thứ tự Page. Ví dụ: `/switch 1`\n\n" + format_pages_list()

    chosen = None
    if arg.isdigit() and 1 <= int(arg) <= len(pages):
        chosen = pages[int(arg) - 1]
    else:
        for p in pages:
            if str(p.get("id")) == arg or arg.lower() in str(p.get("name", "")).lower():
                chosen = p
                break
    if not chosen:
        return f"❌ Không tìm thấy Fanpage khớp với '{arg}'.\n\n" + format_pages_list()

    set_env_key(ENV_PATH, "FACEBOOK_PAGE_ID", str(chosen["id"]))
    if chosen.get("access_token"):
        set_env_key(ENV_PATH, "FACEBOOK_ACCESS_TOKEN", str(chosen["access_token"]))
    return (
        f"✅ Đã chuyển Active Page sang:\n"
        f"🌟 {chosen.get('name')} (ID: {chosen.get('id')} | Follows: {chosen.get('fan_count', 0)})"
    )


def handle_sync_git() -> str:
    sync_script = STATE_SYNC_DIR / "sync-light.ps1"
    if sync_script.exists():
        try:
            out = subprocess.check_output(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(sync_script)],
                stderr=subprocess.STDOUT,
                timeout=30,
                text=True,
                encoding="utf-8",
                errors="ignore",
            )
            return f"✅ Đã chạy đồng bộ GitHub (Agent-State-Sync) thành công!\n\n{out.strip()[-600:]}"
        except Exception as e:
            return f"⚠️ Lỗi khi chạy sync-light.ps1: {e}"
    return "⚠️ Không tìm thấy thư mục Agent-State-Sync trên máy này."


def handle_status_report() -> str:
    try:
        sys.path.insert(0, str(SUBAGENT_DIR / "tools"))
        import mama_boot_check
        report = mama_boot_check.build_markdown_report(auto_pull=False)
        # Clean markdown table slightly for mobile Telegram readability
        return report
    except Exception as e:
        return f"⚠️ Lỗi khi chạy mama_boot_check: {e}"


def handle_tasks_list(conn: sqlite3.Connection) -> str:
    cur = conn.execute(
        "SELECT id, task_text, status, created_at FROM telegram_tasks ORDER BY id DESC LIMIT 8"
    )
    rows = cur.fetchall()
    if not rows:
        return "📭 Hiện chưa có nhiệm vụ nào trong hàng đợi Telegram."
    lines = ["📋 8 NHIỆM VỤ GẦN NHẤT TRÊN TELEGRAM:\n"]
    for r in rows:
        icon = "⏳" if r["status"] == "PENDING" else ("🔄" if r["status"] == "IN_PROGRESS" else "✅")
        lines.append(f"#{r['id']} {icon} [{r['status']}] ({r['created_at'][:16]})\n   👉 {r['task_text'][:120]}")
    return "\n\n".join(lines)


def build_help_text() -> str:
    return (
        "🤖 HƯỚNG DẪN ĐIỀU KHIỂN MAMA & ĐỘI 9 SUBAGENT QUA TELEGRAM\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "⚡ 1. LỆNH NHANH 0-TOKEN (Phản hồi tức thì 1 giây):\n"
        "• /status — Xem Báo cáo khởi động phiên & Tiến độ dự án\n"
        "• /pages — Xem danh sách 5 Fanpage & lượt Follow\n"
        "• /switch <số> — Đổi Fanpage đang điều khiển (VD: /switch 1)\n"
        "• /tasks — Xem tiến độ các việc đã giao cho Mama\n"
        "• /sync — Đồng bộ lịch sử công việc lên GitHub\n"
        "• /help — Xem bảng hướng dẫn này\n\n"
        "🧠 2. GIAO VIỆC TỰ DO CHO MAMA (Chat tiếng Việt tự nhiên):\n"
        "Sếp chỉ cần nhắn thẳng yêu cầu vào khung chat này (không cần gõ dấu /), ví dụ:\n"
        "• \"Mama ơi, viết 1 bài tặng bộ Prompt văn phòng kèm tạo ảnh 1:1 rồi gửi qua đây cho anh duyệt\"\n"
        "• \"Đăng bài mở màn thu phễu lên page AI Players và ghim comment đầu tiên\"\n"
        "• \"Tìm cho anh 3 sản phẩm gia dụng thông minh dưới 200k để làm video AI\"\n\n"
        "👉 Ngay khi Sếp nhắn, Mama (Gemini 4) trên máy tính sẽ tự động thức dậy, điều phối 9 Subagent thực thi và gửi báo cáo + ảnh/link về thẳng đây cho Sếp!"
    )


def listen_loop(wake_on_task: bool = True, max_seconds: int = 3600) -> int:
    token, allowed_chat_id = get_bot_config()
    conn = init_db()
    offset = int(get_state(conn, "last_update_id", "0") or "0")
    start_ts = time.time()

    while (time.time() - start_ts) < max_seconds:
        try:
            resp = tg_api(
                token,
                "getUpdates",
                {"offset": offset, "timeout": 20, "allowed_updates": ["message"]},
                timeout=28.0,
            )
        except Exception:
            time.sleep(2)
            continue

        if not resp.get("ok"):
            time.sleep(2)
            continue

        for upd in resp.get("result", []):
            upd_id = int(upd["update_id"])
            offset = upd_id + 1
            set_state(conn, "last_update_id", str(offset))

            msg = upd.get("message") or {}
            chat = msg.get("chat") or {}
            chat_id = str(chat.get("id", "")).strip()
            if not chat_id:
                continue

            sender = msg.get("from") or {}
            user_name = (
                f"{sender.get('first_name', '')} {sender.get('last_name', '')}".strip()
                or sender.get("username", "CEO")
            )
            text = (msg.get("text") or msg.get("caption") or "").strip()
            msg_id = msg.get("message_id")

            if not text:
                continue

            # Auto-bind first user as CEO if TELEGRAM_CHAT_ID is empty
            if not allowed_chat_id:
                allowed_chat_id = chat_id
                set_env_key(ENV_PATH, "TELEGRAM_CHAT_ID", allowed_chat_id)
                set_state(conn, "ceo_chat_id", allowed_chat_id)
                set_state(conn, "ceo_name", user_name)
                welcome = (
                    f"🎉 KẾT NỐI THÀNH CÔNG VỚI SẾP {user_name.upper()}!\n"
                    f"🔒 Đã khóa bảo mật độc quyền cho tài khoản Telegram ID: {allowed_chat_id}\n\n"
                    + build_help_text()
                )
                tg_send_message(token, chat_id, welcome, reply_to=msg_id)
                if text.lower().startswith("/start"):
                    print(
                        json.dumps(
                            {
                                "event": "CEO_CONNECTED",
                                "chat_id": allowed_chat_id,
                                "user_name": user_name,
                                "text": text,
                            },
                            ensure_ascii=False,
                        ),
                        flush=True,
                    )
                    if wake_on_task:
                        return 0
                    continue

            # Security check
            if chat_id != allowed_chat_id:
                tg_send_message(
                    token,
                    chat_id,
                    "⛔ Bot này đã được khóa bảo mật độc quyền cho CEO. Truy cập bị từ chối.",
                    reply_to=msg_id,
                )
                continue

            low = text.lower()

            # 0-Token Instant Commands
            if low in ("/start", "start"):
                tg_send_message(
                    token,
                    chat_id,
                    f"👋 Chào Sếp {user_name}! Mama & Đội 9 Subagent đang trực chiến.\n\n" + build_help_text(),
                    reply_to=msg_id,
                )
                continue

            if low in ("/help", "help", "hướng dẫn", "huong dan"):
                tg_send_message(token, chat_id, build_help_text(), reply_to=msg_id)
                continue

            if low in ("/status", "status", "báo cáo", "bao cao", "tiến độ", "tien do"):
                report = handle_status_report()
                tg_send_message(token, chat_id, report, reply_to=msg_id)
                continue

            if low in ("/pages", "pages", "fanpage"):
                tg_send_message(token, chat_id, format_pages_list(), reply_to=msg_id)
                continue

            if low.startswith("/switch"):
                arg = text[len("/switch") :].strip()
                tg_send_message(token, chat_id, handle_switch_page(arg), reply_to=msg_id)
                continue

            if low in ("/sync", "sync", "đồng bộ", "dong bo"):
                tg_send_message(token, chat_id, "🔄 Đang đồng bộ trạng thái lên GitHub...", reply_to=msg_id)
                res = handle_sync_git()
                tg_send_message(token, chat_id, res, reply_to=msg_id)
                continue

            if low in ("/tasks", "tasks", "nhiệm vụ", "nhiem vu"):
                tg_send_message(token, chat_id, handle_tasks_list(conn), reply_to=msg_id)
                continue

            # Natural language task for Mama & 9 Subagents
            clean_task = text[len("/task") :].strip() if low.startswith("/task") else text
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur = conn.execute(
                """
                INSERT INTO telegram_tasks (chat_id, user_name, message_id, task_text, status, created_at)
                VALUES (?, ?, ?, ?, 'PENDING', ?)
                """,
                (chat_id, user_name, msg_id, clean_task, now_str),
            )
            task_id = cur.lastrowid
            conn.commit()

            ack = (
                f"🫡 Mama đã nhận lệnh #{task_id} của Sếp!\n"
                f"📝 Nội dung: \"{clean_task}\"\n"
                f"⚡ Đang đánh thức phiên Mama (Gemini 4) + Đội 9 Subagent thực thi và sẽ báo cáo kết quả ngay tại đây..."
            )
            tg_send_message(token, chat_id, ack, reply_to=msg_id)

            wake_payload = {
                "event": "NEW_TELEGRAM_TASK",
                "task_id": task_id,
                "chat_id": chat_id,
                "user_name": user_name,
                "message_id": msg_id,
                "task_text": clean_task,
                "created_at": now_str,
            }
            print(json.dumps(wake_payload, ensure_ascii=False), flush=True)
            if wake_on_task:
                return 0

    return 0


def main():
    parser = argparse.ArgumentParser(description="Mama Telegram 2-Way Bridge")
    parser.add_argument("--setup-menu", action="store_true", help="Register bot commands menu on Telegram")
    parser.add_argument(
        "--listen-and-wake",
        action="store_true",
        help="Listen for Telegram messages; handle 0-token commands and exit(0) on new task to wake Mama",
    )
    parser.add_argument("--daemon", action="store_true", help="Run continuous background listener without exiting")
    parser.add_argument("--check-inbox", action="store_true", help="List all PENDING Telegram tasks")
    parser.add_argument("--reply", type=int, help="Reply to a specific task_id and mark it DONE")
    parser.add_argument("--send", type=str, help="Send a proactive message to CEO's Telegram")
    parser.add_argument("--text", type=str, help="Message text to send with --reply")
    parser.add_argument("--photo", type=str, help="Optional image file path to attach")
    args = parser.parse_args()

    token, allowed_chat_id = get_bot_config()
    conn = init_db()

    if args.setup_menu:
        me = tg_api(token, "getMe")
        cmd_res = setup_bot_commands(token)
        print(
            json.dumps(
                {
                    "bot": me.get("result", {}),
                    "commands_registered": cmd_res.get("ok", False),
                    "allowed_chat_id": allowed_chat_id or "WAITING_FOR_FIRST_MESSAGE",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.check_inbox:
        cur = conn.execute(
            "SELECT id, chat_id, user_name, message_id, task_text, status, created_at "
            "FROM telegram_tasks WHERE status = 'PENDING' ORDER BY id ASC"
        )
        rows = [dict(r) for r in cur.fetchall()]
        print(json.dumps({"pending_count": len(rows), "tasks": rows}, ensure_ascii=False, indent=2))
        return

    if args.reply is not None:
        if not args.text:
            print("❌ Cần truyền --text khi dùng --reply")
            sys.exit(1)
        cur = conn.execute("SELECT * FROM telegram_tasks WHERE id = ?", (args.reply,))
        row = cur.fetchone()
        target_chat = row["chat_id"] if row else allowed_chat_id
        reply_msg_id = row["message_id"] if row else None
        if not target_chat:
            print("❌ Chưa có chat_id của CEO (CEO cần nhắn /start vào bot trước).")
            sys.exit(1)

        if args.photo:
            res = tg_send_photo(token, target_chat, args.photo, caption=args.text)
            if len(args.text) > 1000:
                tg_send_message(token, target_chat, args.text, reply_to=reply_msg_id)
        else:
            res = tg_send_message(token, target_chat, args.text, reply_to=reply_msg_id)

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            "UPDATE telegram_tasks SET status = 'DONE', reply_text = ?, completed_at = ? WHERE id = ?",
            (args.text, now_str, args.reply),
        )
        conn.commit()
        print(json.dumps({"status": "REPLIED_AND_DONE", "task_id": args.reply, "telegram_ok": res.get("ok")}, ensure_ascii=False))
        return

    if args.send:
        if not allowed_chat_id:
            print("❌ Chưa có TELEGRAM_CHAT_ID (Sếp cần nhắn /start vào @thanh79bot trên Telegram trước).")
            sys.exit(1)
        if args.photo:
            res = tg_send_photo(token, allowed_chat_id, args.photo, caption=args.send)
        else:
            res = tg_send_message(token, allowed_chat_id, args.send)
        print(json.dumps({"status": "SENT", "telegram_ok": res.get("ok")}, ensure_ascii=False))
        return

    if args.listen_and_wake:
        sys.exit(listen_loop(wake_on_task=True, max_seconds=7200))

    if args.daemon:
        while True:
            listen_loop(wake_on_task=False, max_seconds=3600)


if __name__ == "__main__":
    main()
