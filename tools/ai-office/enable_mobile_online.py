#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
enable_mobile_online.py — Nâng cấp Văn Phòng Ảo 3D (localhost:4800) hỗ trợ truy cập Online
trên Điện thoại (4G/5G/Wi-Fi) qua Cloudflare Quick Tunnel + Khóa PIN CEO (8899) + Responsive Mobile UI.
"""

import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

OFFICE_DIR = pathlib.Path(__file__).resolve().parent
SERVER_TS = OFFICE_DIR / "src" / "server.ts"
INDEX_HTML = OFFICE_DIR / "public" / "index.html"
ENV_FILE = OFFICE_DIR / ".env"


def patch_env():
    if ENV_FILE.exists():
        txt = ENV_FILE.read_text(encoding="utf-8")
        txt = txt.replace("HOST=127.0.0.1", "HOST=0.0.0.0")
        if "REMOTE_PIN=" not in txt:
            txt = txt.rstrip() + "\nREMOTE_PIN=8899\n"
        ENV_FILE.write_text(txt, encoding="utf-8")


def patch_server_ts():
    s = SERVER_TS.read_text(encoding="utf-8")
    if "REMOTE_PIN" not in s:
        s = s.replace(
            "const HOST = process.env.HOST ?? '127.0.0.1';",
            "const HOST = process.env.HOST ?? '0.0.0.0';\nconst REMOTE_PIN = process.env.REMOTE_PIN || '8899';",
        )

    old_guard_lf = (
        "const hostGuard = (req: Request, res: Response, next: NextFunction) => {\n"
        "  if (!ALLOWED_HOSTS.has(req.headers.host ?? '')) return res.status(403).send('Host không được phép');\n"
        "  next();\n"
        "};"
    )
    old_guard_crlf = old_guard_lf.replace("\n", "\r\n")

    new_guard = """const hostGuard = (req: Request, res: Response, next: NextFunction) => {
  const host = req.headers.host ?? '';
  const isLocal = ALLOWED_HOSTS.has(host) && !req.headers['cf-connecting-ip'] && !req.headers['x-forwarded-for'];
  if (isLocal) return next();
  if (req.headers['x-office-token'] === TOKEN || req.query.t === TOKEN) return next();
  if (req.path.startsWith('/vendor/') || req.path.startsWith('/js/') || req.path.startsWith('/models/')) return next();
  const cookieStr = req.headers.cookie ?? '';
  const hasPinCookie = cookieStr.includes(`javis_mobile_pin=${REMOTE_PIN}`);
  if (req.query.k === REMOTE_PIN) {
    res.setHeader('Set-Cookie', `javis_mobile_pin=${REMOTE_PIN}; Path=/; Max-Age=2592000; HttpOnly; SameSite=Lax`);
    return next();
  }
  if (hasPinCookie) return next();
  return res.status(401).type('html').send(`<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Văn Phòng Ảo 3D · Xác Thực CEO</title><style>body{margin:0;height:100vh;display:flex;align-items:center;justify-content:center;background:#070a10;color:#f8fafc;font-family:system-ui,sans-serif}.box{background:#111827;border:2px solid #10b981;border-radius:20px;padding:28px;width:min(360px,90vw);text-align:center;box-shadow:0 20px 50px rgba(0,0,0,0.7)}input{width:100%;padding:12px;margin:16px 0;border-radius:12px;border:1px solid #334155;background:#090d16;color:#fff;font-size:20px;text-align:center;letter-spacing:6px;box-sizing:border-box}button{width:100%;padding:13px;border-radius:12px;border:none;background:#10b981;color:#04130d;font-weight:800;font-size:16px;cursor:pointer}</style></head><body><form class="box" method="GET" action="/"><div style="font-size:38px">🏢</div><h2 style="margin:10px 0 6px">Văn Phòng Ảo 3D Agent-Javis</h2><p style="color:#94a3b8;font-size:13.5px;margin:0">Nhập Mã PIN CEO để mở điều khiển từ điện thoại</p><input type="password" name="k" placeholder="••••" autofocus required><button type="submit">MỞ VĂN PHÒNG 3D</button></form></body></html>`);
};"""

    if old_guard_crlf in s:
        s = s.replace(old_guard_crlf, new_guard)
    elif old_guard_lf in s:
        s = s.replace(old_guard_lf, new_guard)

    s = s.replace(
        "if (url.pathname !== '/ws' || url.searchParams.get('token') !== TOKEN || !ALLOWED_HOSTS.has(req.headers.host ?? ''))",
        "if (url.pathname !== '/ws' || url.searchParams.get('token') !== TOKEN)",
    )
    s = s.replace(
        "server.listen(PORT, () => {",
        "server.listen(PORT, HOST, () => {",
    )
    SERVER_TS.write_text(s, encoding="utf-8")
    print("✅ Đã nâng cấp src/server.ts (Hỗ trợ Mobile Tunnel + PIN Gate 8899 + LAN 0.0.0.0)")


def patch_mobile_css():
    html = INDEX_HTML.read_text(encoding="utf-8")
    marker = "/* MOBILE_RESPONSIVE_TUNNEL_CSS */"
    if marker in html:
        print("ℹ️ index.html đã có CSS Mobile Responsive.")
        return

    mobile_css = """
  /* MOBILE_RESPONSIVE_TUNNEL_CSS */
  @media (max-width: 768px) {
    #stage { inset: 0; border-radius: 0; border: none; }
    #hud { top: 8px; left: 8px; right: 8px; max-width: none; padding: 9px 12px; }
    #hud h1 { font-size: 14px; }
    #hud p { display: none; }
    #toolbar {
      top: auto; bottom: 10px; left: 8px; right: 8px;
      max-width: none; justify-content: center; gap: 5px;
    }
    .btn { padding: 6px 9px; font-size: 11.5px; }
    #hint, #feed { display: none !important; }
    #panel {
      top: 6px !important; left: 6px !important; right: 6px !important; bottom: 6px !important;
      width: auto !important; height: auto !important;
      flex-direction: column !important;
    }
    #conv-sidebar {
      width: 100% !important; min-width: 100% !important;
      max-height: 155px; border-right: none; border-bottom: 1px solid var(--line);
    }
    #conv-splitter { display: none !important; }
    body.panel-open #toolbar { display: none; }
  }
</style>"""
    html = html.replace("</style>", mobile_css, 1)
    INDEX_HTML.write_text(html, encoding="utf-8")
    print("✅ Đã bổ sung giao diện Mobile Responsive cho public/index.html")


if __name__ == "__main__":
    patch_env()
    patch_server_ts()
    patch_mobile_css()
