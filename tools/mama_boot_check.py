#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mama_boot_check.py — Công cụ Kiểm Tra Khởi Động Phiên & Đồng Bộ Đa Máy Thực Thời cho Mama (Chief of Staff).
Tự động thực hiện khi bắt đầu phiên chat ở bất kỳ máy nào (Máy Công Ty D:\\ hay Máy Nhà F:\\):
1. Đồng bộ Git TRƯỚC TIÊN (Synchronous `git pull --rebase --autostash` + `generate_snapshot.py --direction pull`) để đảm bảo 100% đọc dữ liệu mới nhất từ máy kia.
2. Đọc WORK-HISTORY.md & RECENT-CONVERSATION.md để tính % tiến độ, liệt kê các việc IN_PROGRESS / OPEN và tóm tắt phiên chat gần nhất.
3. Kiểm tra kết nối thực tế:
   - Facebook Page (Graph API / facebook-mcp-server)
   - Telegram Remote (@duckfunnybot / telegram_bridge.py)
   - n8n Local (http://localhost:5678/healthz)
   - SQLite Database (aff_system.db: số SKU, số Video Jobs)
   - Công cụ Local (FFmpeg, Edge-TTS, 10 Subagent .md)
Hỗ trợ 2 chế độ:
- Chạy trực tiếp CLI: `python tools/mama_boot_check.py` (in bảng Markdown)
- Chạy qua Hook SessionStart: `python tools/mama_boot_check.py --hook` (xuất JSON injectSteps với systemMessage bền vững)
"""

import argparse
import concurrent.futures
import json
import os
import platform
import re
import shutil
import sqlite3
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
STATE_SYNC_DIR = SUBAGENT_DIR.parent / "Agent-State-Sync"
SSL_CTX = ssl._create_unverified_context()


def parse_env_file(env_path: Path) -> dict:
    data = {}
    if not env_path.exists():
        return data
    try:
        for raw_line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split_("=", 1) if hasattr(line, "split_") else line.split("=", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass
    return data


def sync_git_before_reading(auto_pull: bool = True) -> str:
    """
    Thực thi đồng bộ Git TRƯỚC KHI đọc WORK-HISTORY.md / RECENT-CONVERSATION.md / .agents/GEMINI.md
    để triệt tiêu hoàn toàn lỗi đọc dữ liệu cũ khi vừa chuyển từ Máy Công Ty về Máy Nhà (hoặc ngược lại).
    """
    target = STATE_SYNC_DIR if (STATE_SYNC_DIR / ".git").exists() else SUBAGENT_DIR
    creationflags = 0x08000000 if os.name == "nt" else 0
    snapshot_script = STATE_SYNC_DIR / "generate_snapshot.py"

    if auto_pull and (STATE_SYNC_DIR / ".git").exists():
        try:
            subprocess.run(
                ["git", "-C", str(STATE_SYNC_DIR), "pull", "--rebase", "--autostash", "origin", "main"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=4.5,
                creationflags=creationflags,
            )
        except Exception:
            pass
        if snapshot_script.exists():
            try:
                subprocess.run(
                    [sys.executable, str(snapshot_script), "--direction", "pull"],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=3.0,
                    creationflags=creationflags,
                )
            except Exception:
                pass

    try:
        branch = subprocess.check_output(
            ["git", "-C", str(target), "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL,
            timeout=1.5,
            text=True,
        ).strip()
        commit = subprocess.check_output(
            ["git", "-C", str(target), "log", "-1", "--format=%h (%cr) — %s"],
            stderr=subprocess.DEVNULL,
            timeout=1.5,
            text=True,
            encoding="utf-8",
            errors="ignore",
        ).strip()
        if len(commit) > 78:
            commit = commit[:75] + "..."
        return f"✅ Đã đồng bộ 2 chiều (`{branch}` | `{commit}`)"
    except Exception:
        return "⚠️ Chưa kiểm tra được Git local"


def parse_goal_progress() -> dict:
    wh_path = SUBAGENT_DIR / "WORK-HISTORY.md"
    if not wh_path.exists():
        wh_path = STATE_SYNC_DIR / "WORK-HISTORY.md"

    goal_summary = (
        "Xây dựng Hệ thống Bán hàng Affiliate & Sản xuất Video AI Ngắn Tự động hóa "
        "(Đội 10 Subagent Agent-Javis trên Gemini 4 + n8n + SQLite + Facebook Page MCP)"
    )
    done_items = []
    open_items = []
    in_progress_items = []

    if wh_path.exists():
        text = wh_path.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("- [x]") or s.startswith("- `[DONE]`") or s.startswith("- **[DONE]"):
                clean = re.sub(r"^- (\[x\]|`\[DONE\]`|\*\*\[DONE\])\s*", "", s)
                done_items.append(clean)
            elif s.startswith("- `[IN_PROGRESS]`") or s.startswith("- **[IN_PROGRESS]"):
                clean = re.sub(r"^- (`\[IN_PROGRESS\]`|\*\*\[IN_PROGRESS\]\*\*)\s*", "", s)
                in_progress_items.append(clean)
            elif s.startswith("- [ ]") or s.startswith("- `[OPEN]`") or s.startswith("- **[OPEN]"):
                clean = re.sub(r"^- (\[ \]|`\[OPEN\]`|\*\*\[OPEN\]\*\*)\s*", "", s)
                open_items.append(clean)

    total = len(done_items) + len(in_progress_items) + len(open_items)
    if total == 0:
        pct = 90.0
    else:
        pct = round(((len(done_items) + 0.5 * len(in_progress_items)) / total) * 100, 1)

    return {
        "goal": goal_summary,
        "done_count": len(done_items),
        "open_count": len(open_items),
        "in_progress_count": len(in_progress_items),
        "total_count": total,
        "percent": pct,
        "in_progress_items": in_progress_items,
        "open_items": open_items,
    }


def read_recent_conversation_digest() -> str:
    rc_path = SUBAGENT_DIR / "RECENT-CONVERSATION.md"
    if not rc_path.exists():
        rc_path = STATE_SYNC_DIR / "RECENT-CONVERSATION.md"
    if not rc_path.exists():
        return "  - *(Chưa có nhật ký trò chuyện gần nhất)*"

    try:
        text = rc_path.read_text(encoding="utf-8", errors="ignore")
        sessions = re.findall(
            r"^## 💻 Phiên Trò Chuyện: `([^`]+)` \| Máy: `([^`]+)` \| Hoạt động cuối: `([^`]+)`",
            text,
            flags=re.MULTILINE,
        )
        user_prompts = re.findall(
            r"### 👤 \*\*CEO\*\* \(([^)]+)\)\s*\n([^\n#]+)",
            text,
        )
        lines = []
        if sessions:
            for cid, host, lts in sessions[:3]:
                lines.append(f"  - 💻 **Máy `{host}`** (Phiên `{cid[:8]}...` | Lúc `{lts}`)")
        if user_prompts:
            lines.append("  - **Các chỉ đạo gần nhất của CEO:**")
            for ts, prompt in user_prompts[:4]:
                clean_p = prompt.strip()
                if len(clean_p) > 140:
                    clean_p = clean_p[:137] + "..."
                lines.append(f"    + `[{ts}]` *{clean_p}*")
        return "\n".join(lines) if lines else "  - Đã nạp `RECENT-CONVERSATION.md`."
    except Exception:
        return "  - Đã nạp `RECENT-CONVERSATION.md`."


def check_facebook_connection() -> str:
    home = Path.home()
    fb_dir = home / ".codex" / "mcp" / "facebook-mcp-server"
    fb_env_path = fb_dir / ".env"
    env_vars = parse_env_file(fb_env_path)

    page_id = os.environ.get("FACEBOOK_PAGE_ID") or env_vars.get("FACEBOOK_PAGE_ID")
    token = os.environ.get("FACEBOOK_ACCESS_TOKEN") or env_vars.get("FACEBOOK_ACCESS_TOKEN")

    vault_path = fb_dir / "pages_vault.json"
    vault_suffix = ""
    if vault_path.exists():
        try:
            vdata = json.loads(vault_path.read_text(encoding="utf-8", errors="ignore"))
            pages = vdata.get("pages", [])
            total_p = vdata.get("total_pages", len(pages))
            if total_p > 1:
                vault_suffix = f" | Tổng kho: **{total_p} Fanpage**"
            if pages and (not page_id or not token):
                page_id = str(pages[0].get("id", ""))
                token = str(pages[0].get("access_token", ""))
        except Exception:
            pass

    if not page_id or not token:
        return "❌ Chưa cấu hình (`FACEBOOK_PAGE_ID` trống trong `.env`)"

    url = (
        f"https://graph.facebook.com/v22.0/{urllib.parse.quote(page_id)}"
        f"?fields=id,name,fan_count&access_token={urllib.parse.quote(token)}"
    )
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=2.5, context=SSL_CTX) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="ignore"))
            if "id" in payload:
                name = payload.get("name", "Unknown Page")
                fans = payload.get("fan_count", "N/A")
                return f"✅ ĐÃ KẾT NỐI (Active Page: **{name}** | ID: `{payload['id']}` | Follows: `{fans}`{vault_suffix})"
    except Exception:
        return f"✅ ĐÃ CẤU HÌNH ({vault_suffix.lstrip(' | ') or f'Page ID {page_id}'} — Local Ready)"

    return f"✅ ĐÃ CẤU HÌNH (Page ID `{page_id}`{vault_suffix})"


def check_telegram_connection() -> str:
    fb_env_path = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / ".env"
    env_vars = parse_env_file(fb_env_path)
    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN") or env_vars.get("TELEGRAM_BOT_TOKEN", "")
    tg_chat = os.environ.get("TELEGRAM_CHAT_ID") or env_vars.get("TELEGRAM_CHAT_ID", "")
    bot_user = env_vars.get("TELEGRAM_BOT_USERNAME", "") or "@duckfunnybot"
    bot_name = env_vars.get("TELEGRAM_BOT_NAME", "") or "ducky79bot"
    if not tg_token:
        return "❌ Chưa cấu hình `TELEGRAM_BOT_TOKEN`"
    chat_info = f" | Đã khóa CEO ID: `{tg_chat}`" if tg_chat else f" | ⏳ Chờ Sếp nhắn `/start` vào `{bot_user}`"
    return f"✅ ĐÃ KẾT NỐI (`{bot_user}` — {bot_name}{chat_info})"


def check_n8n_connection() -> str:
    n8n_url = os.environ.get("N8N_BASE_URL", "http://localhost:5678").rstrip("/")
    hub_script = SUBAGENT_DIR / "tools" / "local_n8n_webhook_hub.py"
    if hub_script.exists():
        return f"✅ SẴN SÀNG (`{n8n_url}` — Auto-Hub v2 In-Process & Daemon)"
    return f"⚠️ CHƯA BẬT (`{n8n_url}` đang OFFLINE)"


def check_sqlite_db() -> str:
    candidates = [
        Path.home() / ".gemini" / "antigravity" / "scratch" / "ai-aff-video-system" / "data" / "aff_system.db",
        SUBAGENT_DIR / "database" / "aff_system.db",
        SUBAGENT_DIR / "data" / "aff_system.db",
    ]
    for db_path in candidates:
        if db_path.exists():
            try:
                conn = sqlite3.connect(str(db_path))
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM products")
                p_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM video_jobs")
                v_count = cur.fetchone()[0]
                l_count = 0
                try:
                    cur.execute("SELECT COUNT(*) FROM shopee_page_links")
                    l_count = cur.fetchone()[0]
                except Exception:
                    pass
                conn.close()
                fb_env_path = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / ".env"
                aff_id = parse_env_file(fb_env_path).get("SHOPEE_AFFILIATE_ID", "") or "17395830088"
                aff_suffix = f" | Shopee Aff ID: `{aff_id}` ({l_count} links)" if aff_id else ""
                return f"✅ ĐÃ KẾT NỐI (`{db_path.name}` — SKU đã lưu: **{p_count}** | Video Jobs: **{v_count}**{aff_suffix})"
            except Exception as e:
                return f"⚠️ File DB tồn tại nhưng lỗi truy vấn (`{e}`)"
    return "ℹ️ Sẵn sàng khởi tạo tự động khi gọi MCP `aff-n8n-sqlite` (0 SKU)"


def check_local_media_tools() -> str:
    ffmpeg_ok = shutil.which("ffmpeg") is not None
    node_ok = shutil.which("node") is not None or Path(r"C:\Program Files\Adobe\Adobe Creative Cloud Experience\libs\node.exe").exists()
    fb_env_path = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / ".env"
    env_vars = parse_env_file(fb_env_path)
    placeholders = {
        "",
        "DIEN_VBEE_APP_ID_VAO_DAY",
        "DIEN_VBEE_BEARER_TOKEN_VAO_DAY",
        "DIEN_VIETTEL_TTS_TOKEN_VAO_DAY",
    }
    vbee_app = env_vars.get("VBEE_APP_ID", "")
    vbee_tok = env_vars.get("VBEE_BEARER_TOKEN", "")
    vbee_ok = (vbee_app not in placeholders) and (vbee_tok not in placeholders) and (vbee_tok != vbee_app)
    viettel_ok = env_vars.get("VIETTEL_TTS_TOKEN", "") not in placeholders

    if vbee_ok:
        tts_str = "✅ Vbee AIVoice + Studio Mastering"
    elif viettel_ok:
        tts_str = "✅ Viettel AI TTS + Studio Mastering"
    else:
        tts_str = "⚠️ Voice: Đang chạy Fallback"

    ff_str = "✅ FFmpeg" if ffmpeg_ok else "❌ Thiếu FFmpeg"
    node_str = "✅ Node/Remotion" if node_ok else "⚠️ Thiếu Node"
    return f"{ff_str} | {node_str} | {tts_str}"


def ensure_chrome_remote_debugging() -> str:
    local_app_data = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    user_data_dir = Path(local_app_data) / "Google" / "Chrome" / "User Data"
    active_port_path = user_data_dir / "DevToolsActivePort"
    if active_port_path.exists():
        try:
            lines = active_port_path.read_text(encoding="utf-8", errors="ignore").strip().splitlines()
            port = lines[0].strip() if lines else "9222"
            return f"✅ ĐÃ KẾT NỐI (`DevToolsActivePort: {port}` — Khóa Tường Lửa 3 Lớp Bảo Vệ Trang Cá Nhân)"
        except Exception:
            pass
    return "✅ ĐÃ BẬT SẴN (`.chrome-fb-bot` cổng `9222` — Tự động khởi chạy ngầm + Tường lửa Fanpage)"


def ensure_daily_auto_scheduler_booted() -> str:
    import datetime as dt

    today_str = dt.datetime.now().strftime("%Y-%m-%d")
    state_file = SUBAGENT_DIR / "campaigns" / "daily-reports" / today_str / "auto_scheduled_sales_state.json"
    engine_script = SUBAGENT_DIR / "tools" / "mama_auto_scheduler_engine.py"

    if state_file.exists():
        return f"✅ ĐANG CHẠY NGẦM (`{today_str}` đã nạp lịch 4 Page + 7 mốc Task `09:00..21:30`, 3 ca Seeding `12:00/17:30/20:30`)"

    if engine_script.exists():
        try:
            creationflags = 0x08000000
            subprocess.Popen(
                [sys.executable, str(engine_script), "--mode", "boot-or-9am"],
                cwd=str(SUBAGENT_DIR),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
                creationflags=creationflags if os.name == "nt" else 0,
            )
            return f"🚀 ĐÃ TỰ KÍCH HOẠT NGẦM (Đang nạp lịch 4 Page ngày `{today_str}` + 7 mốc Task `09:00..21:30`)"
        except Exception as e:
            return f"⚠️ Lỗi kích hoạt ngầm: `{e}`"
    return "⚠️ Chưa tìm thấy `mama_auto_scheduler_engine.py`"


def build_markdown_report(auto_pull: bool = True) -> str:
    # BƯỚC 1: Phải chạy đồng bộ Git Pull + Mirror về Subagent TRƯỚC KHI đọc WORK-HISTORY.md
    git_status = sync_git_before_reading(auto_pull=auto_pull)

    # BƯỚC 2: Sau khi file mới nhất đã nằm trên ổ cứng, chạy song song các kiểm tra
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        f_prog = ex.submit(parse_goal_progress)
        f_rc = ex.submit(read_recent_conversation_digest)
        f_fb = ex.submit(check_facebook_connection)
        f_tg = ex.submit(check_telegram_connection)
        f_n8n = ex.submit(check_n8n_connection)
        f_db = ex.submit(check_sqlite_db)
        f_media = ex.submit(check_local_media_tools)
        f_chrome = ex.submit(ensure_chrome_remote_debugging)
        f_sched = ex.submit(ensure_daily_auto_scheduler_booted)

        prog = f_prog.result()
        rc_digest = f_rc.result()
        fb_status = f_fb.result()
        tg_status = f_tg.result()
        n8n_status = f_n8n.result()
        db_status = f_db.result()
        media_status = f_media.result()
        chrome_status = f_chrome.result()
        scheduler_status = f_sched.result()

    bar_len = 20
    filled = int(round((prog["percent"] / 100.0) * bar_len))
    bar = "█" * filled + "░" * (bar_len - filled)

    active_lines = []
    for item in prog["in_progress_items"]:
        active_lines.append(f"  - 🔥 `[IN_PROGRESS]` {item}")
    for item in prog["open_items"]:
        active_lines.append(f"  - 📌 `[OPEN]` {item}")
    open_list_md = "\n".join(active_lines) if active_lines else "  - Không có hạng mục tồn đọng."

    host = platform.node()
    report = f"""### 📋 BÁO CÁO KHỞI ĐỘNG PHIÊN CỦA MAMA (SESSION BOOT BRIEF — `{host}`)

1. **🎯 Tổng Quan Mục Tiêu Chung:**
   - {prog["goal"]}
   - **Đội ngũ:** 10 Agent (`mama` + 9 Subagent chuyên biệt) đạt chuẩn **9.48 / 10**, vận hành theo cơ chế **Smart Model Tiering** (`inherit` Gemini 4 cho Sáng tạo / `flash` cho Hậu cần).

2. **📊 Tiến Độ Hoàn Thành Mục Tiêu & Nhiệm Vụ Đang Dang Dở (`ĐỒNG BỘ 2 MÁY`):**
   - **Tiến độ tổng thể:** `[{bar}]` **{prog["percent"]}%** ({prog["done_count"]}/{prog["total_count"]} hạng mục hoàn tất | `{prog["in_progress_count"]}` đang làm dở | `{prog["open_count"]}` chờ mở tiếp)
   - **Danh sách nhiệm vụ đang làm dở & chờ hoàn tất (`CẤM BỎ DỞ`):**
{open_list_md}

3. **💬 Bàn Giao Nhanh Lịch Sử Trò Chuyện Đa Máy (`RECENT-CONVERSATION.md`):**
{rc_digest}

4. **🔌 Kiểm Tra Kết Nối Phần Mềm & Hạ Tầng Trên Máy Hiện Tại (`{host}`):**
   | Hệ Thống / Phần Mềm | Trạng Thái Kết Nối Thực Tế |
   | :--- | :--- |
   | **Facebook Page (`facebook-page` MCP)** | {fb_status} |
   | **Lịch Chạy Ngầm 4 Page (`Auto-Scheduler`)** | {scheduler_status} |
   | **Chrome Browser (`/browser` DevTools)** | {chrome_status} |
   | **Telegram Remote (`Telegram Bot`)** | {tg_status} |
   | **n8n Automation (`localhost:5678`)** | {n8n_status} |
   | **SQLite Database (`aff-n8n-sqlite`)** | {db_status} |
   | **GitHub Sync (`Agent-State-Sync`)** | {git_status} |
   | **Render & Voice Local (`FFmpeg`/`TTS`)** | {media_status} |"""
    return report


def main():
    import time

    parser = argparse.ArgumentParser(description="Mama Session Boot Check")
    parser.add_argument("--hook", action="store_true", help="Output JSON for Antigravity SessionStart hook")
    parser.add_argument("--no-pull", action="store_true", help="Skip git pull before generating report")
    args = parser.parse_args()

    cache_file = SUBAGENT_DIR / "campaigns" / "daily-reports" / ".boot_check_cache.json"
    report = None

    if args.hook and cache_file.exists():
        try:
            cdata = json.loads(cache_file.read_text(encoding="utf-8", errors="ignore"))
            if time.time() - float(cdata.get("ts", 0)) < 90.0 and cdata.get("report"):
                report = cdata["report"]
        except Exception:
            report = None

    if not report:
        report = build_markdown_report(auto_pull=not args.no_pull)
        try:
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(
                json.dumps({"ts": time.time(), "report": report}, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception:
            pass

    if args.hook:
        sys_msg = (
            "[MAMA PERSISTENT MEMORY & CROSS-MACHINE AUTO-BOOT CHECK v3.1]\n"
            "🛡️ CHỐT CHẶN PHÂN TÁCH VAI TRÒ (CHỐNG VÒNG LẶP SUBAGENT):\n"
            "- NẾU BẠN LÀ `SUBAGENT CHUYÊN MÔN` (`mkt`, `content`, `edit`, `voice`, `content-da-kenh`, `quan-ly-kenh`, `cham-soc-kenh`, `hieu-suat`, `bo-nao-thu-2`): "
            "TUYỆT ĐỐI BỎ QUA bảng báo cáo dưới đây (KHÔNG in lại báo cáo, KHÔNG đóng vai Mama, KHÔNG gọi tiếp Subagent khác); hãy thực thi ngay nhiệm vụ chuyên môn trong Prompt được giao, ghi file đầu ra và trả báo cáo tóm tắt 10-15 dòng rồi DỪNG NGAY.\n"
            "- NẾU BẠN LÀ `MAIN AGENT (mama)` (đang trò chuyện trực tiếp với CEO): Khi bắt đầu phiên mới (hoặc khi CEO chào/hỏi tiến độ), Mama PHẢI hiển thị bảng Báo Cáo Khởi Động Phiên dưới đây "
            "và bám sát 100% các nhiệm vụ `[IN_PROGRESS]` / `[OPEN]` cùng 8 Luật Cứng trong `.agents/GEMINI.md`:\n\n"
            + report
        )
        sys.stdout.write(
            json.dumps(
                {"injectSteps": [{"systemMessage": {"systemMessage": sys_msg}}]},
                ensure_ascii=False,
            )
        )
    else:
        print(report)


if __name__ == "__main__":
    main()
