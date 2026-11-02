"""
Nâng cấp Văn Phòng Ảo 3D (tools/ai-office) hỗ trợ:
1. Truy cập Online trên Điện thoại qua Cloudflare Tunnel + Mã PIN (?k=8899)
2. Tối ưu toàn diện Giao Diện Mobile (<= 768px):
   - Nhãn 3D trên đầu nhân vật siêu gọn 1 dòng (ẩn thanh tiến độ & chữ thừa khi rảnh) + nút 🏷️ Ẩn/Hiện nhãn
   - Cụm phím điều hướng D-Pad 4 hướng (▲ ▼ ◄ ►) + Zoom (➕ / ➖) + Chuyển chế độ 1 ngón Xoay / Kéo sàn mượt mà
   - Tách biệt hoàn toàn thanh công cụ đáy (#toolbar & #cam3d-dock) không bao giờ đè nhau
   - Khung Chat Mobile Fullscreen (100dvh) với thanh chọn nhanh 11 Agent cuộn ngang & đóng/mở danh sách cuộc trò chuyện
"""
from pathlib import Path

BASE = Path(__file__).resolve().parent
SERVER_TS = BASE / "src" / "server.ts"
INDEX_HTML = BASE / "public" / "index.html"
MAIN_JS = BASE / "public" / "js" / "main.js"
OFFICE3D_JS = BASE / "public" / "js" / "scene" / "office3d.js"


def patch_server_ts():
    s = SERVER_TS.read_text(encoding="utf-8")
    changed = False
    if "const HOST = process.env.OFFICE_HOST ?? '0.0.0.0';" not in s:
        s = s.replace(
            "const HOST = '127.0.0.1';",
            "const HOST = process.env.OFFICE_HOST ?? '0.0.0.0';\nconst MOBILE_PIN = process.env.OFFICE_PIN ?? '8899';",
        )
        changed = True
    if "url.searchParams.get('k') === MOBILE_PIN" not in s:
        s = s.replace(
            "const authed = (req: IncomingMessage, url: URL) =>\n  req.headers['x-office-token'] === SESSION_TOKEN || url.searchParams.get('token') === SESSION_TOKEN;",
            "const authed = (req: IncomingMessage, url: URL) =>\n  req.headers['x-office-token'] === SESSION_TOKEN || url.searchParams.get('token') === SESSION_TOKEN || url.searchParams.get('k') === MOBILE_PIN;",
        )
        changed = True
    if "const isLocal = isLoopback(req.socket.remoteAddress);" not in s:
        old_block = """  if (!isLoopback(req.socket.remoteAddress)) {
    res.writeHead(403).end('Chỉ cho phép truy cập nội bộ');
    return;
  }"""
        new_block = """  const isLocal = isLoopback(req.socket.remoteAddress);
  if (!isLocal) {
    const cookies = String(req.headers.cookie || '');
    const hasPinCookie = cookies.includes(`office_pin=${MOBILE_PIN}`);
    const queryPin = url.searchParams.get('k');
    const isVendorOrAsset = url.pathname.startsWith('/vendor/') || url.pathname.startsWith('/assets/') || url.pathname.startsWith('/js/') || url.pathname === '/favicon.ico';
    if (queryPin === MOBILE_PIN) {
      res.setHeader('Set-Cookie', `office_pin=${MOBILE_PIN}; Path=/; Max-Age=2592000; SameSite=Lax`);
    } else if (!hasPinCookie && !authed(req, url) && !isVendorOrAsset) {
      res.writeHead(401, { 'Content-Type': 'text/html; charset=utf-8' }).end(`<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Văn Phòng 3D Agent-Javis · Mobile Login</title><style>body{margin:0;height:100vh;display:flex;align-items:center;justify-content:center;background:#090b10;color:#eef2f6;font-family:system-ui,sans-serif;padding:20px}form{background:#121722;border:1px solid rgba(255,255,255,0.15);padding:24px;border-radius:16px;width:min(340px,100%);text-align:center;box-shadow:0 16px 40px rgba(0,0,0,0.6)}h2{margin:0 0 8px;color:#10b981;font-size:18px}p{margin:0 0 16px;font-size:13px;color:#94a3b8}input{width:100%;box-sizing:border-box;padding:12px;border-radius:10px;border:1px solid rgba(255,255,255,0.2);background:#090b10;color:#fff;font-size:18px;text-align:center;letter-spacing:6px;margin-bottom:14px}button{width:100%;padding:12px;border-radius:10px;border:none;background:linear-gradient(135deg,#10b981,#059669);color:#04130d;font-weight:700;font-size:15px;cursor:pointer}</style></head><body><form method="GET" action="/"><h2 style="display:flex;align-items:center;justify-content:center;gap:6px">🏢 Văn Phòng 3D Agent-Javis</h2><p>Nhập mã PIN CEO để mở trên Điện Thoại</p><input type="password" name="k" placeholder="••••" inputmode="numeric" required autofocus /><button type="submit">Mở Văn Phòng 3D</button></form></body></html>`);
      return;
    }
  }"""
        if old_block in s:
            s = s.replace(old_block, new_block)
            changed = True
    if changed:
        SERVER_TS.write_text(s, encoding="utf-8")
        print("Patched server.ts")


def patch_office3d_js():
    s = OFFICE3D_JS.read_text(encoding="utf-8")

    # 1. Upgrade setNavMode + add panByScreen & cycleHudMode
    old_nav = """  /** Đổi chế độ cầm nắm chuột trái: 'orbit' (Xoay 360°) | 'pan' (Cầm nắm kéo sàn) | 'move_dept' (Cầm nắm kéo phòng ban) */
  setNavMode(mode = 'orbit') {
    this.navMode = mode;
    if (mode === 'pan') {
      this.controls.mouseButtons.LEFT = THREE.MOUSE.PAN;
      this.controls.mouseButtons.RIGHT = THREE.MOUSE.ROTATE;
    } else {
      this.controls.mouseButtons.LEFT = THREE.MOUSE.ROTATE;
      this.controls.mouseButtons.RIGHT = THREE.MOUSE.PAN;
    }
    const el = this.renderer?.domElement;
    if (el) {
      el.style.cursor = mode === 'pan' ? 'grab' : mode === 'move_dept' ? 'move' : 'grab';
    }
    this.onCameraChange?.({ mode: this.navMode, autoRotate: this.controls.autoRotate });
  }"""

    new_nav = """  /** Đổi chế độ cầm nắm chuột trái / cảm ứng 1 ngón: 'orbit' (Xoay 360°) | 'pan' (Cầm nắm kéo sàn) | 'move_dept' (Cầm nắm kéo phòng ban) */
  setNavMode(mode = 'orbit') {
    this.navMode = mode;
    if (mode === 'pan') {
      this.controls.mouseButtons.LEFT = THREE.MOUSE.PAN;
      this.controls.mouseButtons.RIGHT = THREE.MOUSE.ROTATE;
      if (this.controls.touches) {
        this.controls.touches.ONE = THREE.TOUCH.PAN;
        this.controls.touches.TWO = THREE.TOUCH.DOLLY_ROTATE;
      }
    } else {
      this.controls.mouseButtons.LEFT = THREE.MOUSE.ROTATE;
      this.controls.mouseButtons.RIGHT = THREE.MOUSE.PAN;
      if (this.controls.touches) {
        this.controls.touches.ONE = THREE.TOUCH.ROTATE;
        this.controls.touches.TWO = THREE.TOUCH.DOLLY_PAN;
      }
    }
    const el = this.renderer?.domElement;
    if (el) {
      el.style.cursor = mode === 'pan' ? 'grab' : mode === 'move_dept' ? 'move' : 'grab';
    }
    this.onCameraChange?.({ mode: this.navMode, autoRotate: this.controls.autoRotate });
  }

  /** Di chuyển (Pan) mặt sàn theo hướng màn hình (D-Pad Mobile: dx trái/phải, dz tiến/lùi) */
  panByScreen(dx = 0, dz = 0, dur = 0.2) {
    const forward = new THREE.Vector3();
    this.camera.getWorldDirection(forward);
    forward.y = 0;
    if (forward.lengthSq() < 0.001) forward.set(0, 0, -1);
    forward.normalize();
    const right = new THREE.Vector3().crossVectors(forward, new THREE.Vector3(0, 1, 0)).normalize();
    const distScale = Math.max(1.1, this.camera.position.distanceTo(this.controls.target) * 0.13);
    const delta = new THREE.Vector3()
      .addScaledVector(right, dx * distScale)
      .addScaledVector(forward, dz * distScale);
    const halfW = FLOOR.w * 0.65, halfD = FLOOR.d * 0.65;
    const nextTarget = this.controls.target.clone().add(delta);
    nextTarget.x = Math.max(-halfW, Math.min(halfW, nextTarget.x));
    nextTarget.z = Math.max(-halfD, Math.min(halfD, nextTarget.z));
    const actualDelta = nextTarget.clone().sub(this.controls.target);
    const nextPos = this.camera.position.clone().add(actualDelta);
    if (dur <= 0.05) {
      this.camera.position.copy(nextPos);
      this.controls.target.copy(nextTarget);
      this.controls.update();
    } else {
      this.animateCamera(nextPos, nextTarget, dur);
    }
  }

  /** Chuyển đổi chế độ hiển thị nhãn tên 3D: 'auto' (Gọn) | 'minimal' (Chỉ hiện người bận) | 'hidden' (Ẩn hết) */
  cycleHudMode() {
    const order = ['auto', 'minimal', 'hidden'];
    const cur = this.hudDisplayMode || 'auto';
    this.hudDisplayMode = order[(order.indexOf(cur) + 1) % order.length];
    if (this.hudLayer) {
      this.hudLayer.dataset.hudMode = this.hudDisplayMode;
    }
    return this.hudDisplayMode;
  }"""

    s_norm = s.replace("\r\n", "\n")
    if old_nav in s_norm:
        s_norm = s_norm.replace(old_nav, new_nav)

    # 2. Upgrade resize() for better portrait mobile framing
    old_resize = """    const scale = this.camera.aspect < 1.25 ? Math.min(2.1, 1.25 / this.camera.aspect) : 1;"""
    new_resize = """    const scale = this.camera.aspect < 1.25 ? Math.min(1.58, 1.15 / this.camera.aspect) : 1;"""
    if old_resize in s_norm:
        s_norm = s_norm.replace(old_resize, new_resize)

    # 3. Upgrade updateDomHud() so mobile uses compact collision boxes (minW=64, minH=22) instead of 128x50
    old_hud = """    // Chống đè thẻ (Screen-space collision repulsion 3 vòng lặp)
    const minW = 128, minH = 50;"""
    new_hud = """    // Chống đè thẻ (Screen-space collision repulsion: trên mobile thu gọn kích thước thẻ để không đẩy tràn màn hình)
    const isMob = w <= 768;
    const minW = isMob ? 64 : 128, minH = isMob ? 22 : 50;"""
    if old_hud in s_norm:
        s_norm = s_norm.replace(old_hud, new_hud)

    OFFICE3D_JS.write_text(s_norm, encoding="utf-8")
    print("Patched office3d.js")


def patch_index_html():
    s = INDEX_HTML.read_text(encoding="utf-8").replace("\r\n", "\n")

    # 1. Inject Mobile D-Pad & Zoom controls + Label toggle button into HTML if not yet present
    if 'id="mob-nav-pad"' not in s:
        target_dock = '  <div id="hud3d-layer"></div>'
        mob_pad_html = """  <div id="hud3d-layer"></div>

  <!-- CỤM PHÍM ĐIỀU HƯỚNG DI CHUYỂN 4 HƯỚNG (D-PAD) & ZOOM CHUYÊN DỤNG CHO MOBILE -->
  <div id="mob-nav-pad" aria-label="Điều hướng 3D Mobile">
    <div class="mob-zoom-col">
      <button type="button" class="mob-pad-btn" id="mob-zoom-in" title="Phóng to (Zoom In)">➕</button>
      <button type="button" class="mob-pad-btn" id="mob-zoom-out" title="Thu nhỏ (Zoom Out)">➖</button>
      <button type="button" class="mob-pad-btn" id="btn-hud-toggle" title="Ẩn / Hiện gọn nhãn tên nhân vật 3D">🏷️</button>
    </div>
    <div class="mob-dpad-grid">
      <button type="button" class="mob-pad-btn d-up" id="mob-pan-up" title="Di chuyển tiến lên">▲</button>
      <button type="button" class="mob-pad-btn d-left" id="mob-pan-left" title="Di chuyển sang trái">◄</button>
      <button type="button" class="mob-pad-btn d-center" id="mob-home" title="Về toàn cảnh trung tâm">🎯</button>
      <button type="button" class="mob-pad-btn d-right" id="mob-pan-right" title="Di chuyển sang phải">►</button>
      <button type="button" class="mob-pad-btn d-down" id="mob-pan-down" title="Di chuyển lùi xuống">▼</button>
    </div>
  </div>"""
        s = s.replace(target_dock, mob_pad_html, 1)

    # 2. Add mobile conversation drawer toggle button inside #chat-header
    if 'id="btn-mob-convs"' not in s:
        s = s.replace(
            '<button class="btn small ghost" id="btn-chat-theme" title="Chuyển đổi giao diện Chat Sáng / Tối">☀️ Sáng</button>',
            '<button class="btn small ghost" id="btn-mob-convs" title="Danh sách Cuộc trò chuyện & 11 Agent">📂 DS Chat</button>\n            <button class="btn small ghost" id="btn-chat-theme" title="Chuyển đổi giao diện Chat Sáng / Tối">☀️ Sáng</button>',
        )

    # 3. Replace MOBILE_RESPONSIVE_TUNNEL_CSS block with comprehensive mobile stylesheet
    start_marker = "  /* MOBILE_RESPONSIVE_TUNNEL_CSS */"
    end_marker = "</style>"
    if start_marker in s and end_marker in s:
        idx1 = s.index(start_marker)
        idx2 = s.index(end_marker, idx1)
        new_mobile_css = """  /* MOBILE_RESPONSIVE_TUNNEL_CSS */
  #mob-nav-pad {
    display: none;
  }
  #btn-mob-convs {
    display: none;
  }
  /* Chế độ ẩn/rút gọn nhãn 3D trên cả Desktop & Mobile */
  #hud3d-layer[data-hud-mode="hidden"] .agent-hud3d {
    display: none !important;
  }
  #hud3d-layer[data-hud-mode="minimal"] .agent-hud3d:not(.st-working):not(.st-waiting):not(.is-selected) {
    display: none !important;
  }

  @media (max-width: 768px) {
    .desktop-only { display: none !important; }
    #stage { inset: 0 !important; border-radius: 0 !important; border: none !important; }

    /* 1. HUD Trên Cùng Siêu Gọn */
    #hud {
      top: 6px !important; left: 6px !important; right: 6px !important;
      max-width: none !important; padding: 7px 11px !important;
      border-radius: 12px !important;
      background: rgba(9, 12, 20, 0.86) !important;
    }
    #hud .eyebrow { font-size: 9.5px !important; letter-spacing: 0.08em !important; }
    #hud h1 { font-size: 13.5px !important; margin: 2px 0 !important; }
    #hud p { display: none !important; }
    #hud .count { font-size: 11px !important; line-height: 1.3 !important; }

    /* 2. Nhãn Tên 3D Trên Đầu Nhân Vật: Thu Gọn Thành Viên Thuốc 1 Dòng, Không Che Sàn 3D */
    .agent-hud3d {
      gap: 2px !important;
    }
    .hud3d-card {
      min-width: 0 !important;
      max-width: 108px !important;
      padding: 2px 7px !important;
      border-radius: 99px !important;
      background: rgba(9, 13, 22, 0.82) !important;
      border: 1px solid rgba(255, 255, 255, 0.2) !important;
      box-shadow: 0 3px 8px rgba(0, 0, 0, 0.5) !important;
    }
    .hud3d-top { gap: 4px !important; }
    .hud3d-dot { width: 6px !important; height: 6px !important; }
    .hud3d-name { font-size: 10.5px !important; font-weight: 600 !important; }
    /* Khi rảnh (idle) trên mobile: ẩn chữ SẴN SÀNG, ẩn dòng phụ, ẩn thanh bar */
    .agent-hud3d:not(.st-working):not(.st-waiting):not(.is-selected) .hud3d-pct,
    .agent-hud3d:not(.st-working):not(.st-waiting):not(.is-selected) .hud3d-act,
    .agent-hud3d:not(.st-working):not(.st-waiting):not(.is-selected) .hud3d-bar {
      display: none !important;
    }
    .agent-hud3d.st-working .hud3d-card,
    .agent-hud3d.is-selected .hud3d-card {
      border-radius: 9px !important;
      max-width: 148px !important;
      padding: 4px 8px !important;
    }
    .hud3d-bubble {
      max-width: 175px !important;
      font-size: 10px !important;
      padding: 3px 7px !important;
    }

    /* 3. Cụm Phím Điều Hướng Di Chuyển D-Pad 4 Hướng & Zoom Nổi Bên Phải */
    #mob-nav-pad {
      position: absolute;
      right: 8px;
      bottom: 96px;
      z-index: 9;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      pointer-events: auto;
    }
    .mob-zoom-col {
      display: flex;
      flex-direction: column;
      gap: 5px;
      background: rgba(11, 15, 24, 0.84);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 12px;
      padding: 4px;
      backdrop-filter: blur(10px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.55);
    }
    .mob-dpad-grid {
      display: grid;
      grid-template-columns: repeat(3, 32px);
      grid-template-rows: repeat(3, 32px);
      gap: 3px;
      background: rgba(11, 15, 24, 0.84);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 14px;
      padding: 5px;
      backdrop-filter: blur(10px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
    }
    .mob-pad-btn {
      width: 32px;
      height: 32px;
      border-radius: 9px;
      border: 1px solid rgba(255, 255, 255, 0.12);
      background: rgba(255, 255, 255, 0.07);
      color: #f8fafc;
      font-size: 13px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      user-select: none;
      -webkit-user-select: none;
      touch-action: manipulation;
      padding: 0;
    }
    .mob-pad-btn:active {
      background: #10b981;
      color: #04130d;
      border-color: #34d399;
      transform: scale(0.94);
    }
    .mob-dpad-grid .d-up { grid-column: 2; grid-row: 1; }
    .mob-dpad-grid .d-left { grid-column: 1; grid-row: 2; }
    .mob-dpad-grid .d-center { grid-column: 2; grid-row: 2; background: rgba(16, 185, 129, 0.18); border-color: rgba(16, 185, 129, 0.45); }
    .mob-dpad-grid .d-right { grid-column: 3; grid-row: 2; }
    .mob-dpad-grid .d-down { grid-column: 2; grid-row: 3; }

    /* 4. Hai Thanh Công Cụ Đáy Tách Biệt Hoàn Toàn (Không Bao Giờ Chồng Lên Nhau) */
    #toolbar {
      top: auto !important;
      bottom: 48px !important;
      left: 6px !important;
      right: 6px !important;
      max-width: none !important;
      display: flex !important;
      flex-wrap: nowrap !important;
      overflow-x: auto !important;
      justify-content: center !important;
      gap: 5px !important;
      padding: 2px 0 !important;
      z-index: 8 !important;
    }
    #toolbar .btn {
      padding: 6px 10px !important;
      font-size: 11.5px !important;
      border-radius: 10px !important;
      flex-shrink: 0 !important;
    }
    #cam3d-dock {
      left: 6px !important;
      right: 6px !important;
      bottom: 6px !important;
      transform: none !important;
      width: auto !important;
      max-width: none !important;
      overflow-x: auto !important;
      justify-content: flex-start !important;
      padding: 5px 8px !important;
      gap: 5px !important;
      border-radius: 12px !important;
    }
    #cam3d-dock .dock-btn {
      padding: 5px 9px !important;
      font-size: 11px !important;
      flex-shrink: 0 !important;
    }
    #cam3d-dock .zoom-wrap {
      display: none !important; /* Đã có nút Zoom ➕/➖ bên phải vừa tay ngón cái */
    }
    #hint, #feed { display: none !important; }

    /* 5. Khung Chat Mobile Fullscreen Chuẩn App (100dvh, Ưu Tiên 85% Chiều Cao Cho Tin Nhắn) */
    #panel {
      position: fixed !important;
      inset: 0 !important;
      top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
      width: 100vw !important;
      height: 100dvh !important;
      min-width: 0 !important;
      min-height: 0 !important;
      max-width: none !important;
      max-height: none !important;
      border-radius: 0 !important;
      border: none !important;
      flex-direction: column !important;
      z-index: 30 !important;
    }
    .chat-resizer, #conv-splitter { display: none !important; }
    #btn-mob-convs {
      display: inline-flex !important;
      background: rgba(99, 102, 241, 0.16) !important;
      border-color: rgba(99, 102, 241, 0.45) !important;
      color: #c7d2fe !important;
      font-weight: 600 !important;
    }
    /* Mặc định thu gọn danh sách cuộc trò chuyện trên mobile để nhường chỗ đọc chat, bấm 📂 DS Chat mới mở ra */
    #conv-sidebar {
      width: 100% !important;
      min-width: 0 !important;
      max-height: 210px !important;
      border-right: none !important;
      border-bottom: 1px solid var(--line) !important;
      display: none !important;
      flex-shrink: 0 !important;
    }
    #panel.mob-convs-open #conv-sidebar {
      display: flex !important;
    }
    .sidebar-head { padding: 8px 12px 4px !important; }
    .agy-folder-row { display: none !important; }
    #conv-list {
      max-height: 115px !important;
      overflow-y: auto !important;
      padding: 4px 8px !important;
    }
    /* Hiển thị dải chọn nhanh 11 Agent cuộn ngang trong DS Chat trên Mobile */
    .sidebar-agents {
      display: block !important;
      padding: 6px 10px !important;
    }
    .sidebar-agents-title { display: none !important; }
    #agent-quick-pills {
      display: flex !important;
      flex-wrap: nowrap !important;
      overflow-x: auto !important;
      gap: 5px !important;
      padding-bottom: 2px !important;
    }
    .a-pill { flex-shrink: 0 !important; padding: 4px 9px !important; font-size: 11px !important; }

    #chat-header {
      padding: 8px 10px !important;
      min-height: 44px !important;
      flex-shrink: 0 !important;
    }
    .ch-row1 {
      gap: 6px !important;
    }
    #p-conv-title {
      font-size: 13px !important;
      max-width: 44vw !important;
    }
    #p-close {
      background: rgba(239, 68, 68, 0.16) !important;
      border-color: rgba(239, 68, 68, 0.45) !important;
      color: #fca5a5 !important;
      font-weight: 700 !important;
      padding: 5px 10px !important;
    }
    #log {
      padding: 12px 12px !important;
      gap: 12px !important;
      flex: 1 1 auto !important;
    }
    .anti-msg-user {
      max-width: 90% !important;
      font-size: 13px !important;
      padding: 9px 12px !important;
    }
    .anti-content {
      font-size: 13px !important;
      line-height: 1.55 !important;
    }
    /* Hiển thị thanh chọn Agent nhận lệnh ngay trên ô nhập chat Mobile */
    .composer-target-bar {
      display: flex !important;
      padding: 0 2px 4px !important;
      font-size: 11px !important;
    }
    #p-queue-hint { display: none !important; }
    #composer {
      padding: 8px 10px 12px !important;
      flex-shrink: 0 !important;
    }
    #composer textarea {
      height: 38px !important;
      font-size: 14px !important; /* >= 14px chống iOS Safari tự zoom khi gõ */
    }
    body.panel-open #toolbar,
    body.panel-open #cam3d-dock,
    body.panel-open #mob-nav-pad,
    body.panel-open #hud {
      display: none !important;
    }
  }
"""
        s = s[:idx1] + new_mobile_css + s[idx2:]

    INDEX_HTML.write_text(
        s.replace('<script type="module" src="/js/main.js"></script>', '<script type="module" src="/js/main.js?v=mob3"></script>'),
        encoding="utf-8",
    )
    print("Patched index.html")


def patch_main_js():
    s = MAIN_JS.read_text(encoding="utf-8").replace("\r\n", "\n")
    s = s.replace("from './scene/office3d.js';", "from './scene/office3d.js?v=mob3';")

    # 1. Prevent desktop saved rect from overriding mobile fullscreen panel
    old_restore = """  // Khôi phục kích thước đã lưu
  try {
    const saved = JSON.parse(localStorage.getItem('office.chatRect') || 'null');
    if (saved) {"""
    new_restore = """  // Khôi phục kích thước đã lưu (chỉ áp dụng trên màn hình Desktop > 768px)
  try {
    const saved = window.innerWidth > 768 ? JSON.parse(localStorage.getItem('office.chatRect') || 'null') : null;
    if (saved) {"""
    if old_restore in s:
        s = s.replace(old_restore, new_restore)

    # 2. Add mobile D-Pad, Zoom, HUD label toggle, and Mobile Sidebar toggle handlers
    marker = "/* MOBILE_NAV_HANDLERS_V2 */"
    if marker not in s:
        handlers_code = """
/* MOBILE_NAV_HANDLERS_V2 */
(function initMobileControls() {
  const bindHoldPan = (selector, dx, dz) => {
    const btn = $(selector);
    if (!btn) return;
    let timer = null;
    const step = () => office.panByScreen(dx, dz, 0.16);
    const stop = () => { if (timer) { clearInterval(timer); timer = null; } };
    btn.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      step();
      stop();
      timer = setInterval(step, 140);
    });
    btn.addEventListener('pointerup', stop);
    btn.addEventListener('pointercancel', stop);
    btn.addEventListener('pointerleave', stop);
  };

  bindHoldPan('#mob-pan-up', 0, 1);
  bindHoldPan('#mob-pan-down', 0, -1);
  bindHoldPan('#mob-pan-left', -1, 0);
  bindHoldPan('#mob-pan-right', 1, 0);

  $('#mob-home')?.addEventListener('click', () => {
    office.overview();
    toast('🎯 Đã đưa camera về Toàn cảnh trung tâm');
  });
  $('#mob-zoom-in')?.addEventListener('click', () => {
    office.zoomBy(0.75);
    setTimeout(syncZoomSlider, 350);
  });
  $('#mob-zoom-out')?.addEventListener('click', () => {
    office.zoomBy(1.3);
    setTimeout(syncZoomSlider, 350);
  });
  $('#btn-hud-toggle')?.addEventListener('click', () => {
    const mode = office.cycleHudMode();
    const labelMap = {
      auto: '🏷️ Nhãn 3D: Thu gọn thông minh',
      minimal: '🏷️ Nhãn 3D: Chỉ hiện Agent đang bận',
      hidden: '🏷️ Nhãn 3D: Đã ẩn toàn bộ để ngắm 3D',
    };
    toast(labelMap[mode] || 'Đã đổi chế độ nhãn 3D');
  });
  $('#btn-mob-convs')?.addEventListener('click', (e) => {
    e.stopPropagation();
    const p = $('#panel');
    if (!p) return;
    const open = p.classList.toggle('mob-convs-open');
    $('#btn-mob-convs').textContent = open ? '🔼 Thu gọn DS' : '📂 DS Chat';
  });
})();
"""
        s = s.replace("await office.init();", handlers_code + "\nawait office.init();")

    MAIN_JS.write_text(s, encoding="utf-8")
    print("Patched main.js")


if __name__ == "__main__":
    patch_server_ts()
    patch_office3d_js()
    patch_index_html()
    patch_main_js()
    print("MOBILE_UI_UPGRADE_COMPLETE")
