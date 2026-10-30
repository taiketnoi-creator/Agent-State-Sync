#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
start_bot_chrome.py — Trình quản lý vòng đời Chrome Bot độc lập (.chrome-fb-bot) tại cổng 9222.

Nâng cấp v3.0 (2026-10-30 — Theo lệnh CEO):
1. CHẠY NGẦM 100% (`--headless=new` + `CREATE_NO_WINDOW`):
   - Không bật cửa sổ Chrome lên màn hình, không hiện icon dưới thanh Taskbar gây vướng mắt CEO.
   - Chỉ khi truyền cờ `--visible` (dùng khi CEO muốn mở cửa sổ để đăng nhập tay) mới hiện giao diện.
2. TỰ ĐỘNG TẮT SẠCH SAU KHI TƯƠNG TÁC XONG (`stop_bot_chrome()`):
   - Gửi lệnh CDP `Browser.close` để lưu cookie an toàn rồi đóng trình duyệt.
   - Quét WMI lọc chính xác các tiến trình `chrome.exe` có `CommandLine` chứa `.chrome-fb-bot` để dọn sạch 100% RAM/CPU.
   - Cam kết 100% Zero-Taskkill: Tuyệt đối không đụng vào Chrome cá nhân của CEO (LUẬT #6).
3. ĐỒNG BỘ PHIÊN ĐĂNG NHẬP & LỊCH SỬ TƯƠNG TÁC GIỮA 2 MÁY (`guicci` Công Ty <-> `Admin-PC` Ở Nhà):
   - Giải quyết triệt để việc DPAPI của Windows khóa cứng file SQLite Cookies theo từng máy:
     Trích xuất Cookie Facebook đã giải mã qua CDP (`ctx.cookies()`), mã hóa đối xứng bằng khóa dẫn xuất từ
     `pages_vault.json` (nằm ngoài Git, an toàn bảo mật 100%) rồi lưu vào `knowledge/fb_bot_session_vault.json`.
   - Tự động `git pull` nạp Cookie mới nhất trước khi mở ca tương tác và `git push` đồng bộ lên `Agent-State-Sync`
     ngay sau khi tương tác xong và đóng Chrome Bot.
"""

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import pathlib
import platform
import subprocess
import sys
import time
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200
CREATE_NO_WINDOW = 0x08000000

SUBAGENT_DIR = pathlib.Path(__file__).resolve().parent.parent
STATE_SYNC_DIR = SUBAGENT_DIR.parent / "Agent-State-Sync"
BOT_DIR = SUBAGENT_DIR / ".chrome-fb-bot"
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
VAULT_PATH = pathlib.Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / "pages_vault.json"
SESSION_VAULT_FILE = SUBAGENT_DIR / "knowledge" / "fb_bot_session_vault.json"
INTERACTION_LEDGER_FILE = SUBAGENT_DIR / "campaigns" / "daily-reports" / "group_interaction_ledger.json"


def _derive_vault_key() -> bytes:
    """
    Tạo khóa mã hóa 32-byte từ `pages_vault.json` (có sẵn trên cả 2 máy nhưng không bao giờ nằm trên Git).
    Giúp mã hóa an toàn Cookie Facebook trong `knowledge/fb_bot_session_vault.json` khi đồng bộ qua Git.
    """
    secret_seed = "AgentJavis-FB-Bot-CrossMachine-Sync-2026"
    if VAULT_PATH.exists():
        try:
            data = json.loads(VAULT_PATH.read_text(encoding="utf-8", errors="ignore"))
            pages = sorted(data.get("pages", []), key=lambda x: str(x.get("id", "")))
            if pages:
                secret_seed += "|" + str(pages[0].get("id", "")) + "|" + str(pages[0].get("access_token", ""))[:32]
        except Exception:
            pass
    return hashlib.sha256(secret_seed.encode("utf-8")).digest()


def _xor_crypt(data: bytes, key: bytes) -> bytes:
    out = bytearray(len(data))
    klen = len(key)
    for i, b in enumerate(data):
        stream_byte = hashlib.sha256(key + i.to_bytes(4, "little")).digest()[0]
        out[i] = b ^ stream_byte
    return bytes(out)


def export_bot_session_vault(cookies: list, active_fanpage: str = "") -> bool:
    """
    Lưu danh sách Cookie Facebook (đã trích xuất qua CDP) vào `knowledge/fb_bot_session_vault.json` (mã hóa)
    để máy kia (`Admin-PC` hoặc `guicci`) tự động nạp vào `.chrome-fb-bot` khi chạy ca tiếp theo.
    """
    fb_cookies = [
        c for c in (cookies or [])
        if "facebook.com" in str(c.get("domain", ""))
    ]
    has_c_user = any(c.get("name") == "c_user" for c in fb_cookies)
    if not fb_cookies or not has_c_user:
        return False

    key = _derive_vault_key()
    raw_bytes = json.dumps(fb_cookies, ensure_ascii=False).encode("utf-8")
    enc_b64 = base64.b64encode(_xor_crypt(raw_bytes, key)).decode("ascii")

    payload = {
        "updated_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_machine": platform.node(),
        "active_fanpage": active_fanpage,
        "cookie_count": len(fb_cookies),
        "cookie_names": sorted(list({c.get("name", "") for c in fb_cookies})),
        "ciphertext_b64": enc_b64,
    }
    SESSION_VAULT_FILE.parent.mkdir(parents=True, exist_ok=True)
    SESSION_VAULT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return True


def import_bot_session_vault() -> list:
    """
    Giải mã danh sách Cookie Facebook từ `knowledge/fb_bot_session_vault.json` để nạp vào `.chrome-fb-bot`.
    """
    if not SESSION_VAULT_FILE.exists():
        return []
    try:
        payload = json.loads(SESSION_VAULT_FILE.read_text(encoding="utf-8"))
        enc_b64 = payload.get("ciphertext_b64", "")
        if not enc_b64:
            return []
        key = _derive_vault_key()
        raw_bytes = _xor_crypt(base64.b64decode(enc_b64), key)
        cookies = json.loads(raw_bytes.decode("utf-8"))
        if isinstance(cookies, list):
            return cookies
    except Exception:
        pass
    return []


def sync_bot_state_between_machines(direction: str = "pull") -> None:
    """
    Đồng bộ 2 chiều trạng thái Chrome Bot (`fb_bot_session_vault.json` + `group_interaction_ledger.json`)
    giữa Máy Công Ty (`guicci`) và Máy Ở Nhà (`Admin-PC`) qua kho `Agent-State-Sync`.
    """
    if not (STATE_SYNC_DIR / ".git").exists():
        return
    snap_py = STATE_SYNC_DIR / "generate_snapshot.py"
    try:
        if direction == "pull":
            subprocess.run(
                ["git", "-C", str(STATE_SYNC_DIR), "pull", "--rebase", "--autostash", "origin", "main"],
                timeout=12,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if snap_py.exists():
                subprocess.run(
                    [sys.executable, str(snap_py), "--direction", "pull"],
                    timeout=8,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
        elif direction == "push":
            if snap_py.exists():
                subprocess.run(
                    [sys.executable, str(snap_py), "--direction", "push"],
                    timeout=8,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            subprocess.run(
                ["git", "-C", str(STATE_SYNC_DIR), "add", "knowledge/fb_bot_session_vault.json", "campaigns/daily-reports/"],
                timeout=6,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            host = platform.node()
            now_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
            subprocess.run(
                ["git", "-C", str(STATE_SYNC_DIR), "commit", "-m", f"sync(fb-bot): update session vault & group ledger from {host} ({now_str})"],
                timeout=6,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["git", "-C", str(STATE_SYNC_DIR), "pull", "--rebase", "--autostash", "origin", "main"],
                timeout=12,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["git", "-C", str(STATE_SYNC_DIR), "push", "origin", "main"],
                timeout=15,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    except Exception:
        pass


def get_cdp_version_info(timeout: float = 2.0) -> dict:
    try:
        with urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except Exception:
        return {}


def ensure_bot_chrome_online(timeout_sec: float = 12.0, headless: bool = True) -> str:
    """
    Đảm bảo Chrome Bot độc lập tại cổng 9222 ONLINE và trả về webSocketDebuggerUrl.
    - Mặc định `headless=True`: Chạy ngầm 100% (`--headless=new`), KHÔNG hiện cửa sổ hay icon dưới Taskbar.
    - Tự động đồng bộ Cookie/Session mới nhất từ máy kia về trước khi khởi chạy.
    """
    info = get_cdp_version_info(timeout=1.5)
    if info.get("webSocketDebuggerUrl"):
        return info["webSocketDebuggerUrl"]

    BOT_DIR.mkdir(parents=True, exist_ok=True)
    if not pathlib.Path(CHROME_EXE).exists():
        return ""

    # Nếu máy hiện tại chưa có Cookie trong .chrome-fb-bot/Default, thử nạp bước đầu từ setup_fb_bot_chrome
    ck_path = BOT_DIR / "Default" / "Network" / "Cookies"
    if not ck_path.exists():
        try:
            from setup_fb_bot_chrome import sync_to_bot_dir
            sync_to_bot_dir()
        except Exception:
            pass

    chrome_args = [
        CHROME_EXE,
        f"--user-data-dir={BOT_DIR}",
        "--profile-directory=Default",
        "--remote-debugging-port=9222",
        "--window-size=1440,900",
        "--mute-audio",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-blink-features=AutomationControlled",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding",
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    ]
    if headless:
        chrome_args.insert(4, "--headless=new")

    chrome_args.append("https://www.facebook.com/")

    try:
        subprocess.Popen(
            chrome_args,
            creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return ""

    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        time.sleep(0.8)
        info = get_cdp_version_info(timeout=1.5)
        if info.get("webSocketDebuggerUrl"):
            return info["webSocketDebuggerUrl"]

    return ""


def stop_bot_chrome() -> dict:
    """
    Đóng hoàn toàn trình duyệt Chrome Bot (`.chrome-fb-bot` cổng 9222) ngay sau khi tương tác xong.
    TUYỆT ĐỐI KHÔNG đụng vào Chrome cá nhân của CEO:
    1. Gửi lệnh `Browser.close` qua CDP cổng 9222 để Chrome tự lưu Cookie và thoát êm.
    2. Chỉ dọn các tiến trình `chrome.exe` có `CommandLine` chứa `.chrome-fb-bot`.
    """
    closed_via_cdp = False
    info = get_cdp_version_info(timeout=1.2)
    ws_url = info.get("webSocketDebuggerUrl", "")
    if ws_url:
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(ws_url, timeout=4000)
                ctx = browser.contexts[0] if browser.contexts else browser.new_context()
                pg = ctx.pages[0] if ctx.pages else ctx.new_page()
                cdp = ctx.new_cdp_session(pg)
                cdp.send("Browser.close")
                closed_via_cdp = True
        except Exception:
            pass
        time.sleep(1.5)

    # Bước 2: Lọc chính xác bằng WMI các PID có CommandLine chứa `.chrome-fb-bot` (nếu còn sót)
    killed_pids = []
    try:
        ps_script = (
            "Get-CimInstance Win32_Process -Filter \"Name='chrome.exe'\" | "
            "Where-Object { $_.CommandLine -like '*.chrome-fb-bot*' } | "
            "ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue; $_.ProcessId }"
        )
        res = subprocess.run(
            ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=6,
            creationflags=CREATE_NO_WINDOW,
        )
        for line in (res.stdout or "").splitlines():
            line = line.strip()
            if line.isdigit():
                killed_pids.append(int(line))
    except Exception:
        pass

    return {
        "closed_via_cdp": closed_via_cdp,
        "terminated_bot_pids": killed_pids,
        "port_9222_still_open": bool(get_cdp_version_info(timeout=0.8).get("webSocketDebuggerUrl")),
    }


def main():
    parser = argparse.ArgumentParser(description="Quản lý Chrome Bot (.chrome-fb-bot) chạy ngầm & đồng bộ 2 máy")
    parser.add_argument("--visible", action="store_true", help="Mở cửa sổ hiển thị (chỉ dùng khi cần đăng nhập tay)")
    parser.add_argument("--stop", action="store_true", help="Tắt ngay Chrome Bot (.chrome-fb-bot) cổng 9222")
    parser.add_argument("--export-session", action="store_true", help="Trích xuất & mã hóa Cookie từ cổng 9222 vào Vault đồng bộ 2 máy")
    parser.add_argument("--check-login", action="store_true", help="Kiểm tra trạng thái đăng nhập Facebook & 4 Fanpage rồi tự đóng")
    args = parser.parse_args()

    if args.stop:
        res = stop_bot_chrome()
        print("🛑 Đã tắt Chrome Bot (.chrome-fb-bot):", json.dumps(res, ensure_ascii=False))
        return

    headless_mode = not args.visible
    mode_label = "CHẠY NGẦM 100% (--headless=new)" if headless_mode else "HIỂN THỊ CỬA SỔ (--visible)"
    print(f"🚀 Đang khởi động Chrome Bot (.chrome-fb-bot) ở chế độ [{mode_label}]...")
    ws_url = ensure_bot_chrome_online(timeout_sec=12.0, headless=headless_mode)
    if not ws_url:
        print("❌ Lỗi: Không thể mở cổng 9222.")
        sys.exit(1)

    info = get_cdp_version_info(timeout=2.0)
    print(f"✅ KẾT NỐI THÀNH CÔNG! Browser: {info.get('Browser')} | WS: {ws_url}")

    if args.export_session or args.check_login:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(ws_url, timeout=8000)
            ctx = browser.contexts[0]
            vc = import_bot_session_vault()
            if vc:
                ctx.add_cookies(vc)
            pg = ctx.pages[0] if ctx.pages else ctx.new_page()
            if args.check_login:
                pg.goto("https://www.facebook.com/", timeout=22000)
                time.sleep(3.0)
                has_login = pg.locator('input[name="email"], input[name="pass"]').count() > 0
                is_cp = "checkpoint" in pg.url.lower() or "two_step_verification" in pg.url.lower()
                acct_btn = pg.locator('[aria-label="Tài khoản, trang cá nhân của bạn"], [aria-label="Trang cá nhân của bạn"], [aria-label="Tài khoản"]').first
                menu_lines = []
                if acct_btn.count() > 0:
                    acct_btn.click(timeout=3000)
                    time.sleep(1.8)
                    dialogs = pg.locator('div[role="dialog"]')
                    for i in range(dialogs.count()):
                        d = dialogs.nth(i)
                        aria = d.get_attribute("aria-label") or ""
                        if "thông báo" not in aria.lower():
                            txt = d.inner_text(timeout=1500)
                            if txt.strip():
                                menu_lines = [ln.strip() for ln in txt.splitlines() if ln.strip()][:12]
                                break
                cookies = ctx.cookies("https://www.facebook.com")
                cmap = {c["name"]: c["value"] for c in cookies if "facebook.com" in c.get("domain", "")}
                print("🔎 KẾT QUẢ KIỂM TRA ĐĂNG NHẬP FACEBOOK:", json.dumps({
                    "logged_in_ok": (not has_login and not is_cp and "c_user" in cmap),
                    "has_login_form": has_login,
                    "is_checkpoint": is_cp,
                    "c_user": cmap.get("c_user", ""),
                    "i_user_fanpage_profile": cmap.get("i_user", ""),
                    "active_menu_lines": menu_lines,
                }, ensure_ascii=False, indent=2))
            cookies = ctx.cookies("https://www.facebook.com")
            ok = export_bot_session_vault(cookies)
            print(f"🔐 Export Session Vault ({len(cookies)} cookies): {'THÀNH CÔNG' if ok else 'CHƯA ĐĂNG NHẬP'}")
        if headless_mode:
            stop_res = stop_bot_chrome()
            print("🛑 Đã tự động đóng Chrome Bot:", json.dumps(stop_res, ensure_ascii=False))


if __name__ == "__main__":
    main()
