#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bot_chrome_web_remote.py — Giao diện điều khiển trực tiếp `.chrome-fb-bot` (cổng 9222)
ngay trong khung Browser bên phải của Antigravity tại địa chỉ: http://localhost:9224
- Chống popup `Comment C | Quote Ctrl+L` bằng `user-select: none`.
- Hỗ trợ cả 3 cách nhập:
  1. Nút bấm mở hộp thoại `prompt()`原生 (không bao giờ bị chặn chuột).
  2. Ô nhập Email / Mật khẩu trực tiếp trên thanh điều khiển.
  3. Click trực tiếp vào ảnh màn hình Facebook và gõ bàn phím trực tiếp.
"""
import base64
import http.server
import json
import subprocess
import sys
import threading
import time
import urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SUBAGENT_DIR / "tools"))

from start_bot_chrome import (
    ensure_bot_chrome_online,
    export_bot_session_vault,
    stop_bot_chrome,
    sync_bot_state_between_machines,
)

HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Chrome Bot 9222 — Đăng Nhập Facebook</title>
<style>
  * { box-sizing: border-box; user-select: none; -webkit-user-select: none; }
  input.txt { user-select: text !important; -webkit-user-select: text !important; }
  body { margin: 0; background: #0f172a; color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
  .bar { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; padding: 12px 14px; background: #1e293b; border-bottom: 2px solid #334155; font-size: 13px; z-index: 20; }
  .status { padding: 6px 12px; border-radius: 6px; font-weight: 800; background: #f59e0b; color: #000; }
  .status.ok { background: #10b981; color: #000; }
  input.txt { padding: 8px 12px; border-radius: 6px; border: 2px solid #60a5fa; background: #020617; color: #fff; font-size: 14px; outline: none; }
  input.txt:focus { border-color: #10b981; box-shadow: 0 0 0 2px rgba(16,185,129,0.35); }
  button { padding: 8px 14px; border-radius: 6px; border: none; background: #2563eb; color: #fff; font-weight: 700; font-size: 13.5px; cursor: pointer; }
  button.green { background: #10b981; color: #000; font-size: 14px; }
  button.amber { background: #f59e0b; color: #000; font-size: 14px; }
  button:hover { filter: brightness(1.08); }
  .stage { flex: 1; display: flex; align-items: center; justify-content: center; overflow: auto; position: relative; background: #020617; }
  img#screen { max-width: 100%; max-height: 100%; cursor: pointer; border: 1px solid #334155; -webkit-user-drag: none; }
</style>
</head>
<body>
  <div class="bar">
    <span id="badge" class="status">CHỜ ĐĂNG NHẬP (:9222)</span>
    <button class="amber" onclick="promptLogin()">🔑 BẤM ĐÂY NHẬP NHANH (KHÔNG KẸT CHUỘT)</button>
    <input id="emailBox" class="txt" style="width:185px;" type="text" placeholder="Email / Số điện thoại..." autocomplete="off" />
    <input id="passBox" class="txt" style="width:155px;" type="password" placeholder="Mật khẩu..." autocomplete="off" />
    <button class="green" onclick="doLogin()">🚀 Đăng Nhập</button>
    <button onclick="prompt2FA()">🔢 Nhập Mã 2FA / Gõ chữ</button>
  </div>
  <div class="stage">
    <img id="screen" src="" onclick="onImgClick(event)" draggable="false" />
  </div>
<script>
const img = document.getElementById('screen');
const badge = document.getElementById('badge');

function refresh() {
  fetch('/state?t=' + Date.now()).then(r => r.json()).then(d => {
    if (d.logged_in) {
      badge.textContent = '✅ ĐÃ ĐĂNG NHẬP & LƯU VAULT (c_user=' + d.c_user + ')';
      badge.className = 'status ok';
    } else if (d.status_msg) {
      badge.textContent = d.status_msg;
    }
    if (d.jpg_b64) {
      img.src = 'data:image/jpeg;base64,' + d.jpg_b64;
    }
  }).catch(() => {});
}
setInterval(refresh, 750);
refresh();

function onImgClick(e) {
  const rect = img.getBoundingClientRect();
  const x = Math.round((e.clientX - rect.left) * (1440 / rect.width));
  const y = Math.round((e.clientY - rect.top) * (900 / rect.height));
  fetch('/click?x=' + x + '&y=' + y).then(() => setTimeout(refresh, 300));
}

function promptLogin() {
  const u = window.prompt('Bước 1/2 — Nhập Email hoặc Số điện thoại Facebook:');
  if (!u || !u.trim()) return;
  const p = window.prompt('Bước 2/2 — Nhập Mật khẩu Facebook:');
  if (!p) return;
  badge.textContent = '⏳ Đang điền tài khoản & bấm Đăng nhập...';
  fetch('/fill_login?u=' + encodeURIComponent(u.trim()) + '&p=' + encodeURIComponent(p))
    .then(() => setTimeout(refresh, 1000));
}

function prompt2FA() {
  const val = window.prompt('Nhập mã xác thực 2FA (hoặc nội dung cần gõ vào ô đang chọn):');
  if (!val) return;
  fetch('/type?text=' + encodeURIComponent(val)).then(() => setTimeout(refresh, 400));
}

function doLogin() {
  const u = document.getElementById('emailBox').value.trim();
  const p = document.getElementById('passBox').value;
  if (!u || !p) {
    promptLogin();
    return;
  }
  badge.textContent = '⏳ Đang điền tài khoản & bấm Đăng nhập...';
  fetch('/fill_login?u=' + encodeURIComponent(u) + '&p=' + encodeURIComponent(p)).then(() => {
    document.getElementById('passBox').value = '';
    setTimeout(refresh, 1000);
  });
}

document.getElementById('passBox').addEventListener('keydown', e => {
  if (e.key === 'Enter') doLogin();
});

// Nếu CEO click vào ảnh màn hình Facebook rồi gõ bàn phím trực tiếp, chuyển tiếp phím sang trình duyệt Bot
window.addEventListener('keydown', e => {
  const tag = (document.activeElement && document.activeElement.tagName) || '';
  if (tag === 'INPUT' || tag === 'TEXTAREA') return;
  if (e.ctrlKey || e.altKey || e.metaKey) return;
  if (e.key.length === 1 || e.key === 'Backspace' || e.key === 'Enter' || e.key === 'Tab') {
    e.preventDefault();
    fetch('/key?k=' + encodeURIComponent(e.key)).then(() => setTimeout(refresh, 250));
  }
});
</script>
</body>
</html>
"""

STATE = {
    "jpg_b64": "",
    "logged_in": False,
    "c_user": "",
    "exported": False,
    "status_msg": "CHỜ ĐĂNG NHẬP (:9222)",
}
CMD_QUEUE = []


def worker_loop():
    ws = ensure_bot_chrome_online(timeout_sec=14.0, headless=True)
    if not ws:
        STATE["status_msg"] = "❌ LỖI MỞ CHROME 9222"
        return
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(ws, timeout=12000)
        ctx = b.contexts[0]
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        pg.set_viewport_size({"width": 1440, "height": 900})
        if "facebook.com" not in pg.url:
            try:
                pg.goto("https://www.facebook.com/login/", timeout=22000)
            except Exception:
                pass
        while True:
            while CMD_QUEUE:
                cmd = CMD_QUEUE.pop(0)
                try:
                    op = cmd.get("op")
                    if op == "click":
                        pg.mouse.click(cmd["x"], cmd["y"])
                    elif op == "fill_login":
                        STATE["status_msg"] = "⏳ Đang điền Email & Mật khẩu..."
                        em = pg.locator('input[name="email"]').first
                        pw = pg.locator('input[name="pass"]').first
                        if em.count() == 0:
                            ctx.clear_cookies()
                            pg.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
                            pg.goto("https://www.facebook.com/login/", timeout=18000)
                            time.sleep(1.2)
                            em = pg.locator('input[name="email"]').first
                            pw = pg.locator('input[name="pass"]').first
                        em.click(timeout=3000)
                        em.fill(cmd["u"], timeout=3000)
                        time.sleep(0.2)
                        pw.click(timeout=3000)
                        pw.fill(cmd["p"], timeout=3000)
                        time.sleep(0.3)
                        pg.evaluate("() => { const s = document.querySelector('input[type=submit]'); if (s) s.click(); }")
                        STATE["status_msg"] = "⏳ Đã gửi thông tin đăng nhập, đang chờ Facebook phản hồi..."
                    elif op == "type":
                        pg.keyboard.insert_text(cmd["text"])
                        time.sleep(0.2)
                        pg.keyboard.press("Enter")
                    elif op == "key":
                        k = cmd["k"]
                        if len(k) == 1:
                            pg.keyboard.insert_text(k)
                        else:
                            pg.keyboard.press(k)
                except Exception as exc:
                    STATE["status_msg"] = f"⚠️ Lỗi thao tác: {str(exc)[:40]}"
            try:
                raw = pg.screenshot(type="jpeg", quality=72)
                STATE["jpg_b64"] = base64.b64encode(raw).decode("ascii")
                cks = ctx.cookies("https://www.facebook.com")
                cmap = {c["name"]: c["value"] for c in cks}
                if "c_user" in cmap and cmap["c_user"] and "xs" in cmap and cmap["xs"]:
                    STATE["logged_in"] = True
                    STATE["c_user"] = cmap["c_user"]
                    if not STATE["exported"]:
                        export_bot_session_vault(cks)
                        sync_bot_state_between_machines(direction="push")
                        STATE["exported"] = True
                        STATE["status_msg"] = f"✅ ĐÃ LƯU VAULT (c_user={cmap['c_user']})"
            except Exception:
                pass
            time.sleep(0.55)


class ThreadedHTTPServer(http.server.ThreadingHTTPServer):
    allow_reuse_address = True


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        if parsed.path == "/":
            body = HTML_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        elif parsed.path == "/state":
            body = json.dumps(STATE).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        elif parsed.path == "/click":
            x = int(qs.get("x", [720])[0])
            y = int(qs.get("y", [450])[0])
            CMD_QUEUE.append({"op": "click", "x": x, "y": y})
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        elif parsed.path == "/fill_login":
            u = qs.get("u", [""])[0]
            p = qs.get("p", [""])[0]
            CMD_QUEUE.append({"op": "fill_login", "u": u, "p": p})
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        elif parsed.path == "/type":
            txt = qs.get("text", [""])[0]
            CMD_QUEUE.append({"op": "type", "text": txt})
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        elif parsed.path == "/key":
            k = qs.get("k", [""])[0]
            if k:
                CMD_QUEUE.append({"op": "key", "k": k})
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    t = threading.Thread(target=worker_loop, daemon=True)
    t.start()
    srv = ThreadedHTTPServer(("127.0.0.1", 9224), Handler)
    print("WEB REMOTE v3 READY AT: http://localhost:9224", flush=True)
    srv.serve_forever()
