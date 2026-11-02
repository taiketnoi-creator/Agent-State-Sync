#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ensure_ai_office_running.py — Tự động khởi chạy ngầm Văn Phòng Ảo 3D (http://localhost:4800)
+ Cloudflare Mobile HTTPS Tunnel (*.trycloudflare.com/?k=8899) trên cả 2 máy (Công ty & Ở nhà)
mà KHÔNG CẦN CEO phải gõ câu lệnh trong Antigravity.

Cơ chế kích hoạt tự động 3 tầng:
1. Windows Startup (`AgentJavis_AutoBoot_OnStartup.vbs`) & Task Scheduler (`AtLogOn`): Tự chạy ngay khi bật máy.
2. Antigravity IDE / VS Code (`.vscode/tasks.json` -> `runOn: folderOpen` + `%APPDATA%\\Antigravity\\User\\settings.json` -> `task.allowAutomaticTasks: on`): Tự chạy ngay khi mở phần mềm Antigravity.
3. Hook `SessionStart` (`tools/mama_boot_check.py`): Tự kiểm tra, cài đặt Startup trên máy mới và khởi chạy nếu chưa bật.
"""

import argparse
import datetime as dt
import json
import os
import platform
import re
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
STATE_SYNC_DIR = SUBAGENT_DIR.parent / "Agent-State-Sync"
OFFICE_DIR = SUBAGENT_DIR / "tools" / "ai-office"
DATA_DIR = OFFICE_DIR / "data"
LIVE_STATE_FILE = DATA_DIR / "live_tunnel_state.json"
TUNNEL_LOG_FILE = DATA_DIR / "cloudflared_tunnel.log"
SERVER_LOG_FILE = DATA_DIR / "office_autostart.log"
CLOUDFLARED_EXE = OFFICE_DIR / "tools" / "cloudflared.exe"
CLOUDFLARED_URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
PORT = 4800
REMOTE_PIN = "8899"
CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0
DETACHED_PROCESS = 0x00000008 if os.name == "nt" else 0


def is_port_open(port: int = PORT, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.8)
        return s.connect_ex((host, port)) == 0


def get_lan_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def find_node_exe() -> str:
    candidates = [
        r"C:\Program Files\nodejs\node.exe",
        r"C:\Program Files\Adobe\Adobe Creative Cloud Experience\libs\node.exe",
        os.path.expandvars(r"%ProgramFiles%\nodejs\node.exe"),
        os.path.expandvars(r"%APPDATA%\nvm\current\node.exe"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return "node"


def ensure_patches_applied() -> None:
    patch_script = OFFICE_DIR / "enable_mobile_online.py"
    if patch_script.exists():
        try:
            subprocess.run(
                [sys.executable, str(patch_script)],
                cwd=str(OFFICE_DIR),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=8,
                creationflags=CREATE_NO_WINDOW,
            )
        except Exception:
            pass


def start_office_server_if_needed() -> bool:
    """Khởi chạy máy chủ Văn Phòng Ảo 3D ở cổng 4800 nếu chưa chạy. Trả về True nếu vừa khởi động mới."""
    if is_port_open(PORT):
        return False

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ensure_patches_applied()

    node_exe = find_node_exe()
    tsx_cli = OFFICE_DIR / "node_modules" / "tsx" / "dist" / "cli.mjs"
    if tsx_cli.exists():
        cmd = [node_exe, str(tsx_cli), "src/server.ts"]
    else:
        cmd = [node_exe, "--experimental-transform-types", "src/server.ts"]

    env = os.environ.copy()
    node_dir = str(Path(node_exe).parent) if os.path.exists(node_exe) else ""
    if node_dir:
        env["PATH"] = f"{node_dir};{env.get('PATH', '')}"

    out_f = open(SERVER_LOG_FILE, "a", encoding="utf-8", errors="ignore")
    subprocess.Popen(
        cmd,
        cwd=str(OFFICE_DIR),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=out_f,
        stderr=out_f,
        creationflags=CREATE_NO_WINDOW | DETACHED_PROCESS,
    )

    for _ in range(16):
        time.sleep(0.4)
        if is_port_open(PORT):
            return True
    return is_port_open(PORT)


def is_cloudflared_running() -> bool:
    if os.name != "nt":
        return False
    try:
        out = subprocess.check_output(
            ["tasklist", "/FI", "IMAGENAME eq cloudflared.exe", "/NH"],
            stderr=subprocess.DEVNULL,
            text=True,
            creationflags=CREATE_NO_WINDOW,
            timeout=3,
        )
        return "cloudflared.exe" in out.lower()
    except Exception:
        return False


def ensure_cloudflared_binary() -> bool:
    if CLOUDFLARED_EXE.exists() and CLOUDFLARED_EXE.stat().st_size > 5_000_000:
        return True
    try:
        CLOUDFLARED_EXE.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(CLOUDFLARED_URL, str(CLOUDFLARED_EXE))
        return CLOUDFLARED_EXE.exists()
    except Exception:
        return False


def extract_tunnel_url_from_log() -> str:
    for log_candidate in [
        TUNNEL_LOG_FILE,
        *sorted(
            (Path.home() / ".gemini" / "antigravity" / "brain").glob("*/.system_generated/tasks/*.log"),
            key=lambda p: p.stat().st_mtime if p.exists() else 0,
            reverse=True,
        )[:15],
    ]:
        if not log_candidate.exists():
            continue
        try:
            txt = log_candidate.read_text(encoding="utf-8", errors="ignore")
            matches = re.findall(r"https://[a-z0-9-]+\.trycloudflare\.com", txt)
            if matches:
                return matches[-1]
        except Exception:
            pass
    return ""


def start_tunnel_if_needed() -> tuple[str, bool]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if is_cloudflared_running():
        existing_url = extract_tunnel_url_from_log()
        if not existing_url and LIVE_STATE_FILE.exists():
            try:
                existing_url = json.loads(LIVE_STATE_FILE.read_text(encoding="utf-8")).get("tunnel_url", "")
            except Exception:
                pass
        if existing_url:
            return existing_url, False

    if not ensure_cloudflared_binary():
        return "", False

    try:
        TUNNEL_LOG_FILE.write_text("", encoding="utf-8")
    except Exception:
        pass

    log_f = open(TUNNEL_LOG_FILE, "a", encoding="utf-8", errors="ignore")
    subprocess.Popen(
        [
            str(CLOUDFLARED_EXE),
            "tunnel",
            "--url",
            f"http://localhost:{PORT}",
            "--no-autoupdate",
            "--logfile",
            str(TUNNEL_LOG_FILE),
        ],
        cwd=str(OFFICE_DIR),
        stdin=subprocess.DEVNULL,
        stdout=log_f,
        stderr=log_f,
        creationflags=CREATE_NO_WINDOW | DETACHED_PROCESS,
    )

    tunnel_url = ""
    for _ in range(25):
        time.sleep(0.5)
        tunnel_url = extract_tunnel_url_from_log()
        if tunnel_url:
            break

    return tunnel_url, bool(tunnel_url)


def install_windows_startup_and_vscode_hook() -> None:
    """
    Đảm bảo trên cả 2 máy (Công ty & Ở nhà):
    1. `%APPDATA%\\Antigravity\\User\\settings.json` luôn bật `"task.allowAutomaticTasks": "on"`.
    2. `AgentJavis_AutoBoot_OnStartup.vbs` trong Windows Startup tự bật Văn Phòng Ảo 3D ngay khi khởi động máy.
    3. `generate_snapshot.py` và `mama_boot_check.py` tích hợp sẵn tự khởi chạy 3D Office.
    """
    if os.name == "nt":
        appdata = Path(os.environ.get("APPDATA", ""))
        for ide_name in ("Antigravity", "Code", "Windsurf"):
            settings_path = appdata / ide_name / "User" / "settings.json"
            if settings_path.parent.exists():
                try:
                    data = json.loads(settings_path.read_text(encoding="utf-8")) if settings_path.exists() else {}
                    if data.get("task.allowAutomaticTasks") != "on":
                        data["task.allowAutomaticTasks"] = "on"
                        settings_path.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")
                except Exception:
                    pass

        try:
            startup_dir = appdata / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
            if startup_dir.exists():
                vbs_path = startup_dir / "AgentJavis_AutoBoot_OnStartup.vbs"
                py_exe = sys.executable
                engine_script = SUBAGENT_DIR / "tools" / "mama_auto_scheduler_engine.py"
                self_script = Path(__file__).resolve()
                vbs_content = (
                    'Set WshShell = CreateObject("WScript.Shell")\n'
                    f'WshShell.CurrentDirectory = "{SUBAGENT_DIR}"\n'
                    f'WshShell.Run """{py_exe}"" ""{self_script}"" --open-browser --notify-telegram", 0, False\n'
                    f'WshShell.Run """{py_exe}"" ""{engine_script}"" --mode boot-or-9am", 0, False\n'
                )
                vbs_path.write_text(vbs_content, encoding="utf-8")
        except Exception:
            pass

    # Tích hợp vào generate_snapshot.py để đồng bộ .vscode/tasks.json & .vscode/settings.json sang Máy Nhà
    gs_path = STATE_SYNC_DIR / "generate_snapshot.py"
    if gs_path.exists():
        try:
            gtxt = gs_path.read_text(encoding="utf-8")
            if ".vscode" not in gtxt:
                gtxt = gtxt.replace(
                    'os.path.join(".agents", "hooks.json"),',
                    'os.path.join(".agents", "hooks.json"),\n    os.path.join(".vscode", "tasks.json"),\n    os.path.join(".vscode", "settings.json"),',
                )
                gs_path.write_text(gtxt, encoding="utf-8")
        except Exception:
            pass

    # Tích hợp vào mama_boot_check.py để Hook SessionStart tự bật Văn Phòng Ảo 3D trên cả 2 máy
    mb_path = SUBAGENT_DIR / "tools" / "mama_boot_check.py"
    if mb_path.exists():
        try:
            mtxt = mb_path.read_text(encoding="utf-8")
            if "ensure_ai_office_booted" not in mtxt:
                func_block = (
                    "\n\ndef ensure_ai_office_booted() -> str:\n"
                    "    import socket\n"
                    "    office_script = SUBAGENT_DIR / 'tools' / 'ensure_ai_office_running.py'\n"
                    "    state_file = SUBAGENT_DIR / 'tools' / 'ai-office' / 'data' / 'live_tunnel_state.json'\n"
                    "    port_open = False\n"
                    "    try:\n"
                    "        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:\n"
                    "            s.settimeout(0.5)\n"
                    "            port_open = (s.connect_ex(('127.0.0.1', 4800)) == 0)\n"
                    "    except Exception:\n"
                    "        pass\n"
                    "    if office_script.exists():\n"
                    "        try:\n"
                    "            creationflags = 0x08000000 if os.name == 'nt' else 0\n"
                    "            subprocess.Popen(\n"
                    "                [sys.executable, str(office_script), '--install-startup', '--open-browser', '--notify-telegram', '--quiet'],\n"
                    "                cwd=str(SUBAGENT_DIR),\n"
                    "                stdin=subprocess.DEVNULL,\n"
                    "                stdout=subprocess.DEVNULL,\n"
                    "                stderr=subprocess.DEVNULL,\n"
                    "                close_fds=True,\n"
                    "                creationflags=creationflags,\n"
                    "            )\n"
                    "        except Exception:\n"
                    "            pass\n"
                    "    mobile_url = ''\n"
                    "    if state_file.exists():\n"
                    "        try:\n"
                    "            mobile_url = json.loads(state_file.read_text(encoding='utf-8')).get('mobile_url', '')\n"
                    "        except Exception:\n"
                    "            pass\n"
                    "    if port_open:\n"
                    "        extra = f' | Mobile: `{mobile_url}`' if mobile_url else ''\n"
                    "        return f'✅ ĐANG CHẠY NGẦM (`http://localhost:4800`{extra} — Tự bật khi mở máy/Antigravity)'\n"
                    "    return '🚀 ĐÃ TỰ KÍCH HOẠT NGẦM (`http://localhost:4800` + Cloudflare Mobile Tunnel `?k=8899`)'\n"
                )
                mtxt = mtxt.replace(
                    "def build_markdown_report(auto_pull: bool = True) -> str:",
                    func_block + "\n\ndef build_markdown_report(auto_pull: bool = True) -> str:",
                )
                mtxt = mtxt.replace(
                    "f_sched = ex.submit(ensure_daily_auto_scheduler_booted)",
                    "f_sched = ex.submit(ensure_daily_auto_scheduler_booted)\n        f_office = ex.submit(ensure_ai_office_booted)",
                )
                mtxt = mtxt.replace(
                    "scheduler_status = f_sched.result()",
                    "scheduler_status = f_sched.result()\n        office_status = f_office.result()",
                )
                mtxt = mtxt.replace(
                    "| **Lịch Chạy Ngầm 4 Page (`Auto-Scheduler`)** | {scheduler_status} |",
                    "| **Văn Phòng Ảo 3D (`Port 4800 & Mobile`)** | {office_status} |\n   | **Lịch Chạy Ngầm 4 Page (`Auto-Scheduler`)** | {scheduler_status} |",
                )
                mb_path.write_text(mtxt, encoding="utf-8")
        except Exception:
            pass


def load_live_state() -> dict:
    if LIVE_STATE_FILE.exists():
        try:
            return json.loads(LIVE_STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_live_state(state: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LIVE_STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def notify_telegram_if_new_tunnel(tunnel_url: str, lan_ip: str) -> None:
    if not tunnel_url:
        return
    state = load_live_state()
    if state.get("last_notified_tunnel_url") == tunnel_url:
        return

    tele_script = SUBAGENT_DIR / "tools" / "telegram_bridge.py"
    if not tele_script.exists():
        return

    host_name = platform.node()
    msg = (
        f"🏢 VĂN PHÒNG ẢO 3D ĐÃ TỰ ĐỘNG BẬT ({host_name})\n"
        f"🔗 Mở trên Điện thoại (4G/Wi-Fi): {tunnel_url}/?k={REMOTE_PIN}\n"
        f"📶 Mạng LAN nội bộ: http://{lan_ip}:{PORT}/?k={REMOTE_PIN}\n"
        f"💻 Trên máy tính: http://localhost:{PORT} (Mã PIN: {REMOTE_PIN})"
    )
    try:
        subprocess.run(
            [sys.executable, str(tele_script), "--send", msg],
            cwd=str(SUBAGENT_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
            creationflags=CREATE_NO_WINDOW,
        )
        state["last_notified_tunnel_url"] = tunnel_url
        save_live_state(state)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="Auto-start 3D AI Virtual Office & Mobile Tunnel")
    parser.add_argument("--open-browser", action="store_true", help="Tự mở tab trình duyệt http://localhost:4800 (chống mở lặp)")
    parser.add_argument("--notify-telegram", action="store_true", help="Gửi link Mobile Tunnel mới về Telegram CEO")
    parser.add_argument("--install-startup", action="store_true", help="Cài đặt tự chạy khi mở máy Windows & Antigravity")
    parser.add_argument("--quiet", action="store_true", help="Chỉ xuất JSON gọn")
    args = parser.parse_args()

    if args.install_startup:
        install_windows_startup_and_vscode_hook()

    server_started = start_office_server_if_needed()
    tunnel_url, tunnel_started = start_tunnel_if_needed()
    lan_ip = get_lan_ip()

    state = load_live_state()
    today_str = dt.date.today().isoformat()
    browser_already_opened_today = state.get("browser_opened_date") == today_str and not server_started

    state.update({
        "updated_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "machine": platform.node(),
        "local_url": f"http://localhost:{PORT}",
        "lan_url": f"http://{lan_ip}:{PORT}/?k={REMOTE_PIN}",
        "tunnel_url": tunnel_url,
        "mobile_url": f"{tunnel_url}/?k={REMOTE_PIN}" if tunnel_url else f"http://{lan_ip}:{PORT}/?k={REMOTE_PIN}",
        "pin": REMOTE_PIN,
        "port_open": is_port_open(PORT),
    })
    save_live_state(state)

    if args.open_browser and state["port_open"] and (server_started or not browser_already_opened_today):
        try:
            webbrowser.open(f"http://localhost:{PORT}")
            state["browser_opened_date"] = today_str
            save_live_state(state)
        except Exception:
            pass

    if (args.notify_telegram or tunnel_started) and tunnel_url:
        notify_telegram_if_new_tunnel(tunnel_url, lan_ip)

    if args.quiet:
        print(json.dumps(state, ensure_ascii=False))
    else:
        print(
            f"✅ AI Office 3D: http://localhost:{PORT} | "
            f"Mobile: {state['mobile_url']} | "
            f"LAN: {state['lan_url']}"
        )


if __name__ == "__main__":
    main()
