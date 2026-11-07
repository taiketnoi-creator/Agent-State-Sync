#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_capture_fb_login_and_run_shift.py — Mở cửa sổ Chrome Bot (.chrome-fb-bot --visible) ngoài Desktop thật
để CEO đăng nhập 1 lần; ngay khi phát hiện cookie `c_user` + `xs` đăng nhập thành công:
1. Tự động trích xuất & mã hóa Cookie vào `knowledge/fb_bot_session_vault.json` (đồng bộ 2 máy).
2. Tự động đóng cửa sổ hiển thị (`stop_bot_chrome()`) để trả lại màn hình gọn sạch cho CEO.
3. Tự động kích hoạt ngay Ca Tương Tác Group + Reels + Reply Người Dùng Thật ở chế độ chạy ngầm 100% (`--headless=new`).
"""

import subprocess
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SUBAGENT_DIR / "tools"))

from start_bot_chrome import (
    ensure_bot_chrome_online,
    export_bot_session_vault,
    stop_bot_chrome,
    sync_bot_state_between_machines,
)


def main():
    stop_bot_chrome()
    time.sleep(1.0)
    ws_url = ensure_bot_chrome_online(timeout_sec=15.0, headless=False)
    if not ws_url:
        print("❌ Lỗi: Không mở được cửa sổ .chrome-fb-bot cổng 9222", flush=True)
        return

    print(f"✅ Đã mở cửa sổ Chrome Bot hiển thị ({ws_url}). Mời CEO đăng nhập Facebook...", flush=True)
    from playwright.sync_api import sync_playwright

    logged_in = False
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_url, timeout=15000)
        ctx = browser.contexts[0]
        pg = ctx.pages[-1] if ctx.pages else ctx.new_page()
        try:
            pg.goto("https://www.facebook.com/login/", timeout=25000)
        except Exception:
            pass

        deadline = time.time() + 900
        while time.time() < deadline:
            try:
                cookies = ctx.cookies("https://www.facebook.com")
                has_c_user = any(c.get("name") == "c_user" for c in cookies)
                has_xs = any(c.get("name") == "xs" for c in cookies)
                cur_url = pg.url.lower()
                if has_c_user and has_xs and "login" not in cur_url and "checkpoint" not in cur_url:
                    export_bot_session_vault(cookies)
                    logged_in = True
                    print("✅ ĐÃ PHÁT HIỆN ĐĂNG NHẬP THÀNH CÔNG & LƯU COOKIE MÃ HÓA VÀO VAULT!", flush=True)
                    break
            except Exception:
                pass
            time.sleep(2.0)

    if logged_in:
        stop_bot_chrome()
        sync_bot_state_between_machines(direction="push")
        print("🚀 Đã đóng cửa sổ hiển thị, đồng bộ 2 máy và kích hoạt chạy ngầm Ca Tương Tác Group!", flush=True)
        time.sleep(1.0)
        subprocess.Popen(
            [
                sys.executable,
                str(SUBAGENT_DIR / "tools" / "mama_daily_group_and_eod.py"),
                "--shift",
                "2",
                "--urls-per-niche",
                "4",
                "--cmts-per-url",
                "3",
                "--send-telegram",
            ],
            cwd=str(SUBAGENT_DIR),
        )


if __name__ == "__main__":
    main()
