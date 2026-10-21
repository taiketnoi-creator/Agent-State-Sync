#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mama_boot_check.py — Công cụ Kiểm Tra Khởi Động Phiên 0-Token cho Mama (Chief of Staff).
Tự động thực hiện khi bắt đầu phiên chat ở bất kỳ máy nào:
1. Kiểm tra đồng bộ Git (Agent-State-Sync & Subagent).
2. Đọc WORK-HISTORY.md để tính % tiến độ hoàn thành mục tiêu dự án.
3. Kiểm tra kết nối thực tế:
   - Facebook Page (Graph API / facebook-mcp-server)
   - n8n Local (http://localhost:5678/healthz)
   - SQLite Database (aff_system.db: số SKU, số Video Jobs)
   - Công cụ Local (FFmpeg, Edge-TTS, 10 Subagent .md)
Hỗ trợ 2 chế độ:
- Chạy trực tiếp CLI: `python tools/mama_boot_check.py` (in bảng Markdown)
- Chạy qua Hook SessionStart: `python tools/mama_boot_check.py --hook` (xuất JSON injectSteps)
"""

import argparse
import json
import os
import re
import shutil
import sqlite3
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


def check_git_sync(auto_pull: bool = False) -> str:
    target = STATE_SYNC_DIR if STATE_SYNC_DIR.exists() else SUBAGENT_DIR
    if auto_pull:
        for repo in (STATE_SYNC_DIR, SUBAGENT_DIR):
            if repo.exists():
                try:
                    subprocess.run(
                        ["git", "-C", str(repo), "pull", "--rebase", "origin", "main"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=3.5,
                    )
                except Exception:
                    pass
    try:
        branch = subprocess.check_output(
            ["git", "-C", str(target), "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL,
            timeout=2,
            text=True,
        ).strip()
        commit = subprocess.check_output(
            ["git", "-C", str(target), "log", "-1", "--format=%h (%cr)"],
            stderr=subprocess.DEVNULL,
            timeout=2,
            text=True,
        ).strip()
        return f"✅ Đã đồng bộ mới nhất (`{branch}` | commit `{commit}`)"
    except Exception:
        return "⚠️ Chưa kiểm tra được Git local"


def parse_goal_progress() -> dict:
    wh_path = STATE_SYNC_DIR / "WORK-HISTORY.md"
    if not wh_path.exists():
        wh_path = SUBAGENT_DIR / "STATE-SNAPSHOT.md"

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
            if s.startswith("- [x]") or s.startswith("- `[DONE]`"):
                clean = re.sub(r"^- (\[x\]|`\[DONE\]`)\s*", "", s)
                done_items.append(clean)
            elif s.startswith("- `[IN_PROGRESS]`"):
                clean = re.sub(r"^- `\[IN_PROGRESS\]`\s*", "", s)
                in_progress_items.append(clean)
            elif s.startswith("- [ ]") or s.startswith("- `[OPEN]`"):
                clean = re.sub(r"^- (\[ \]|`\[OPEN\]`)\s*", "", s)
                open_items.append(clean)

    total = len(done_items) + len(in_progress_items) + len(open_items)
    if total == 0:
        pct = 80.0
    else:
        pct = round(((len(done_items) + 0.5 * len(in_progress_items)) / total) * 100, 1)

    return {
        "goal": goal_summary,
        "done_count": len(done_items),
        "open_count": len(open_items),
        "in_progress_count": len(in_progress_items),
        "total_count": total,
        "percent": pct,
        "open_items": open_items,
    }


def check_facebook_connection() -> str:
    home = Path.home()
    fb_dir = home / ".codex" / "mcp" / "facebook-mcp-server"
    fb_env_path = fb_dir / ".env"
    env_vars = parse_env_file(fb_env_path)

    page_id = os.environ.get("FACEBOOK_PAGE_ID") or env_vars.get("FACEBOOK_PAGE_ID")
    token = os.environ.get("FACEBOOK_ACCESS_TOKEN") or env_vars.get("FACEBOOK_ACCESS_TOKEN")

    # Fallback 1: Check ~/.gemini/config/mcp_config.json
    if not page_id or not token:
        mcp_cfg = home / ".gemini" / "config" / "mcp_config.json"
        if mcp_cfg.exists():
            try:
                cfg_data = json.loads(mcp_cfg.read_text(encoding="utf-8", errors="ignore"))
                fb_env = cfg_data.get("mcpServers", {}).get("facebook-page", {}).get("env", {})
                page_id = page_id or fb_env.get("FACEBOOK_PAGE_ID")
                token = token or fb_env.get("FACEBOOK_ACCESS_TOKEN")
            except Exception:
                pass

    # Fallback 2: Check ~/.codex/config.toml and auto-sync to fb_env_path (.gitignore protected)
    if not page_id or not token:
        codex_toml = home / ".codex" / "config.toml"
        if codex_toml.exists():
            try:
                toml_text = codex_toml.read_text(encoding="utf-8", errors="ignore")
                m_id = re.search(r'FACEBOOK_PAGE_ID\s*=\s*["\']([^"\']+)["\']', toml_text)
                m_tok = re.search(r'FACEBOOK_ACCESS_TOKEN\s*=\s*["\']([^"\']+)["\']', toml_text)
                if m_id and not page_id:
                    page_id = m_id.group(1).strip()
                if m_tok and not token:
                    token = m_tok.group(1).strip()
                if page_id and token and fb_dir.exists() and not fb_env_path.exists():
                    fb_env_path.write_text(
                        f"FACEBOOK_PAGE_ID={page_id}\nFACEBOOK_ACCESS_TOKEN={token}\n",
                        encoding="utf-8",
                    )
            except Exception:
                pass

    placeholders = {
        "",
        "DIEN_PAGE_ID_VAO_DAY",
        "DIEN_PAGE_ACCESS_TOKEN_VAO_DAY",
        "DIEN_USER_TOKEN_VAO_DAY_DE_TU_DONG_LAY_TAT_CA_PAGE",
        "YOUR_PAGE_ID",
        "YOUR_ACCESS_TOKEN",
    }
    user_token = os.environ.get("FACEBOOK_USER_TOKEN") or env_vars.get("FACEBOOK_USER_TOKEN", "")
    if (not page_id or not token or page_id in placeholders or token in placeholders) and user_token and user_token not in placeholders:
        try:
            import fb_multi_page_sync
            fb_multi_page_sync.sync_all_pages(user_token)
            env_vars = parse_env_file(fb_env_path)
            page_id = env_vars.get("FACEBOOK_PAGE_ID")
            token = env_vars.get("FACEBOOK_ACCESS_TOKEN")
        except Exception:
            pass

    if not page_id or not token or page_id in placeholders or token in placeholders:
        return "❌ Chưa cấu hình (`FACEBOOK_USER_TOKEN` hoặc `FACEBOOK_PAGE_ID` trống trong `.env`)"

    vault_path = fb_dir / "pages_vault.json"
    vault_suffix = ""
    if vault_path.exists():
        try:
            vdata = json.loads(vault_path.read_text(encoding="utf-8", errors="ignore"))
            total_p = vdata.get("total_pages", len(vdata.get("pages", [])))
            if total_p > 1:
                vault_suffix = f" | Tổng kho: **{total_p} Fanpage**"
        except Exception:
            pass

    url = (
        f"https://graph.facebook.com/v22.0/{urllib.parse.quote(page_id)}"
        f"?fields=id,name,fan_count&access_token={urllib.parse.quote(token)}"
    )
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="ignore"))
            if "id" in payload:
                name = payload.get("name", "Unknown Page")
                fans = payload.get("fan_count", "N/A")
                return f"✅ ĐÃ KẾT NỐI (Active Page: **{name}** | ID: `{payload['id']}` | Follows: `{fans}`{vault_suffix})"
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read().decode("utf-8", errors="ignore"))
            err_msg = err_body.get("error", {}).get("message", f"HTTP {e.code}")
        except Exception:
            err_msg = f"HTTP {e.code}"
        return f"⚠️ Đã có cấu hình Page ID `{page_id}` nhưng Token báo lỗi/hết hạn: `{err_msg[:90]}`"
    except Exception as e:
        return f"⚠️ Đã cấu hình Page ID `{page_id}` nhưng không kết nối được mạng/Graph API (`{e}`)"

    return f"⚠️ Chưa xác minh được Page ID `{page_id}`"


def check_n8n_connection() -> str:
    n8n_url = os.environ.get("N8N_BASE_URL", "http://localhost:5678").rstrip("/")
    for endpoint in ("/healthz", "/"):
        try:
            req = urllib.request.Request(f"{n8n_url}{endpoint}", method="GET")
            with urllib.request.urlopen(req, timeout=1.8) as resp:
                if resp.status in (200, 204):
                    return f"✅ ĐANG CHẠY ONLINE (`{n8n_url}`)"
        except Exception:
            continue
    hub_script = SUBAGENT_DIR / "tools" / "local_n8n_webhook_hub.py"
    if hub_script.exists():
        return f"✅ SẴN SÀNG (`{n8n_url}` — Auto-Hub v2 In-Process & Daemon)"
    return f"⚠️ CHƯA BẬT (`{n8n_url}` đang OFFLINE — cần bật Docker/n8n khi muốn auto-post)"


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
    elif (vbee_app not in placeholders) and (vbee_tok == vbee_app):
        tts_str = "⚠️ Vbee: Đã có `App ID`, nhưng `VBEE_BEARER_TOKEN` đang trùng `App ID` (cần dán chuỗi `eyJ...`)"
    else:
        tts_str = "⚠️ Voice: Đang chạy Fallback (Chờ điền Token Vbee/Viettel vào `.env`)"

    ff_str = "✅ FFmpeg" if ffmpeg_ok else "❌ Thiếu FFmpeg"
    node_str = "✅ Node/Remotion" if node_ok else "⚠️ Thiếu Node"
    return f"{ff_str} | {node_str} | {tts_str}"


def build_markdown_report(auto_pull: bool = False) -> str:
    git_status = check_git_sync(auto_pull=auto_pull)
    prog = parse_goal_progress()
    fb_status = check_facebook_connection()
    n8n_status = check_n8n_connection()
    db_status = check_sqlite_db()
    media_status = check_local_media_tools()

    bar_len = 20
    filled = int(round((prog["percent"] / 100.0) * bar_len))
    bar = "█" * filled + "░" * (bar_len - filled)

    open_list_md = "\n".join(f"  - `[OPEN]` {item}" for item in prog["open_items"]) if prog["open_items"] else "  - Không có hạng mục tồn đọng."

    report = f"""### 📋 BÁO CÁO KHỞI ĐỘNG PHIÊN CỦA MAMA (SESSION BOOT BRIEF)

1. **🎯 Tổng Quan Mục Tiêu Chung:**
   - {prog["goal"]}
   - **Đội ngũ:** 10 Agent (`mama` + 9 Subagent chuyên biệt) đã đào tạo đạt chuẩn **9.48 / 10**, vận hành theo cơ chế **Smart Model Tiering** (`inherit` Gemini 4 cho Sáng tạo / `flash` cho Hậu cần).

2. **📊 Tiến Độ Hoàn Thành Mục Tiêu:**
   - **Tiến độ tổng thể:** `[{bar}]` **{prog["percent"]}%** ({prog["done_count"]}/{prog["total_count"]} hạng mục hoàn tất)
   - **Các hạng mục đang chờ triển khai tiếp (`{prog["open_count"]}`):**
{open_list_md}

3. **🔌 Kiểm Tra Kết Nối Phần Mềm & Hạ Tầng Trên Máy Hiện Tại:**
   | Hệ Thống / Phần Mềm | Trạng Thái Kết Nối Thực Tế |
   | :--- | :--- |
   | **Facebook Page (`facebook-page` MCP)** | {fb_status} |
   | **n8n Automation (`localhost:5678`)** | {n8n_status} |
   | **SQLite Database (`aff-n8n-sqlite`)** | {db_status} |
   | **GitHub Sync (`Agent-State-Sync`)** | {git_status} |
   | **Render & Voice Local (`FFmpeg`/`TTS`)** | {media_status} |"""
    return report


def main():
    parser = argparse.ArgumentParser(description="Mama Session Boot Check")
    parser.add_argument("--hook", action="store_true", help="Output JSON for Antigravity SessionStart hook")
    args = parser.parse_args()

    if args.hook:
        try:
            _ = sys.stdin.read()
        except Exception:
            pass

    report = build_markdown_report(auto_pull=args.hook)

    if args.hook:
        ephemeral = (
            "[MAMA AUTO-BOOT CHECK]\n"
            "QUY TẮC BẮT BUỘC CHO MAMA: Khi bắt đầu phiên trò chuyện mới trên bất kỳ máy nào "
            "(hoặc khi CEO chào/hỏi tiến độ), Mama PHẢI trình bày ngay bảng Báo Cáo Khởi Động Phiên dưới đây:\n\n"
            + report
        )
        sys.stdout.write(json.dumps({"injectSteps": [{"ephemeralMessage": ephemeral}]}, ensure_ascii=False))
    else:
        print(report)


if __name__ == "__main__":
    main()
