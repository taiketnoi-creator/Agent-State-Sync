#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import time
import urllib.request
import json
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

bot_dir = pathlib.Path.home() / ".chrome-fb-bot"
bot_dir.mkdir(parents=True, exist_ok=True)

chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# First check if 9222 is already running
try:
    with urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=1.5) as resp:
        info = json.loads(resp.read().decode())
        print("✅ Chrome Bot đã chạy sẵn trên cổng 9222:", info.get("Browser"))
        sys.exit(0)
except Exception:
    pass

cmd = [
    chrome_exe,
    f"--user-data-dir={bot_dir}",
    "--remote-debugging-port=9222",
    "--no-first-run",
    "--no-default-browser-check",
    "https://www.facebook.com"
]

proc = subprocess.Popen(cmd, creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
print(f"🚀 Đã khởi động Chrome Bot độc lập (PID: {proc.pid}). Đang kiểm tra kết nối...")
time.sleep(3)

try:
    with urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=3.0) as resp:
        info = json.loads(resp.read().decode())
        print("🎉 KẾT NỐI THÀNH CÔNG! Port 9222 is ONLINE.")
        print("   Browser:", info.get("Browser"))
except Exception as e:
    print("❌ Lỗi kết nối 9222:", e)
