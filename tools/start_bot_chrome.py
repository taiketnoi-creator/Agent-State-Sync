#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
start_bot_chrome.py — Tự động khởi chạy ngầm Chrome Bot độc lập (.chrome-fb-bot) tại cổng 9222.
Cam kết 100% Zero-Taskkill:
- Tuyệt đối không đóng hay can thiệp vào Chrome cá nhân của CEO.
- Khởi tạo tiến trình độc lập qua WMI Win32_Process (tách khỏi Job Object tạm thời) để luôn sống bền vững.
- Khóa cứng --profile-directory=Default nơi đã lưu phiên đăng nhập Facebook của Bot.
"""

import json
import pathlib
import subprocess
import sys
import time
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

SUBAGENT_DIR = pathlib.Path(__file__).resolve().parent.parent
BOT_DIR = SUBAGENT_DIR / ".chrome-fb-bot"
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def get_cdp_version_info(timeout: float = 2.0) -> dict:
    try:
        with urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except Exception:
        return {}


def ensure_bot_chrome_online(timeout_sec: float = 12.0) -> str:
    """
    Đảm bảo Chrome Bot độc lập tại cổng 9222 luôn ONLINE và trả về webSocketDebuggerUrl.
    Nếu cổng 9222 chưa mở, tự động khởi chạy ngầm không cần CEO mở file .bat.
    """
    info = get_cdp_version_info(timeout=1.8)
    if info.get("webSocketDebuggerUrl"):
        return info["webSocketDebuggerUrl"]

    BOT_DIR.mkdir(parents=True, exist_ok=True)
    if not pathlib.Path(CHROME_EXE).exists():
        return ""

    # Ưu tiên khởi tạo qua WMI Win32_Process để tiến trình sống độc lập hoàn toàn
    cmd_str = (
        f'"{CHROME_EXE}" '
        f'--user-data-dir="{BOT_DIR}" '
        f'--profile-directory="Default" '
        f'--remote-debugging-port=9222 '
        f'--no-first-run '
        f'--no-default-browser-check '
        f'https://www.facebook.com'
    )
    launched = False
    try:
        ps_cmd = [
            "powershell",
            "-NoProfile",
            "-WindowStyle",
            "Hidden",
            "-Command",
            f"Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{{CommandLine='{cmd_str}'}} | Out-Null",
        ]
        subprocess.run(ps_cmd, timeout=6, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        launched = True
    except Exception:
        launched = False

    if not launched:
        try:
            subprocess.Popen(
                [
                    CHROME_EXE,
                    f"--user-data-dir={BOT_DIR}",
                    "--profile-directory=Default",
                    "--remote-debugging-port=9222",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "https://www.facebook.com",
                ],
                creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            return ""

    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        time.sleep(1.0)
        info = get_cdp_version_info(timeout=1.5)
        if info.get("webSocketDebuggerUrl"):
            return info["webSocketDebuggerUrl"]

    return ""


def main():
    info = get_cdp_version_info(timeout=1.5)
    if info.get("webSocketDebuggerUrl"):
        print("✅ Chrome Bot đã chạy sẵn trên cổng 9222:", info.get("Browser"))
        return

    print("🚀 Đang tự động khởi động Chrome Bot độc lập (.chrome-fb-bot | Default)...")
    ws_url = ensure_bot_chrome_online(timeout_sec=12.0)
    if ws_url:
        info = get_cdp_version_info(timeout=2.0)
        print("🎉 KẾT NỐI THÀNH CÔNG! Port 9222 is ONLINE.")
        print("   Browser:", info.get("Browser"))
        print("   WS URL:", ws_url)
    else:
        print("❌ Lỗi: Không thể mở cổng 9222 sau 12 giây.")
        sys.exit(1)


if __name__ == "__main__":
    main()
