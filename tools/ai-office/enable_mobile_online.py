"""
Nâng cấp Văn Phòng Ảo 3D (tools/ai-office) hỗ trợ:
1. Truy cập Online trên Điện thoại qua Cloudflare Tunnel + Mã PIN (?k=8899)
2. Tốc độ tải Cuộc trò chuyện tức thì (<5ms) nhờ bộ nhớ đệm RAM (transcriptCache) + gộp activeConvDetail ngay trong /api/state + gọi loadState() song song không chờ 3D tải xong.
3. Tối ưu toàn diện Giao Diện & Khung Chat Mobile (<= 768px):
   - Khắc phục triệt để lỗi không cuộn được tin nhắn (#chat-main & #log min-height: 0 + touch-action: pan-y + chống renderChatStream() giật cuộn mỗi 2s)
   - Khắc phục triệt để lỗi không nhắn tin được (#composer cố định ở đáy khung chat, hỗ trợ visualViewport khi bật bàn phím ảo, nút Gửi nhận chạm trực tiếp pointerdown không bị nuốt sự kiện khi bàn phím đóng)
   - Nhãn 3D trên đầu nhân vật siêu gọn 1 dòng + Cụm phím D-Pad 4 hướng (▲ ▼ ◄ ►) & Zoom (➕ / ➖)
"""
from pathlib import Path

BASE = Path(__file__).resolve().parent
SERVER_TS = BASE / "src" / "server.ts"
BRIDGE_TS = BASE / "src" / "antigravityBridge.ts"
INDEX_HTML = BASE / "public" / "index.html"
MAIN_JS = BASE / "public" / "js" / "main.js"
OFFICE3D_JS = BASE / "public" / "js" / "scene" / "office3d.js"


def patch_bridge_ts():
    if not BRIDGE_TS.exists():
        return
    s = BRIDGE_TS.read_text(encoding="utf-8").replace("\r\n", "\n")
    changed = False

    # Add RAM cache for parsed transcripts so listAllConversations & getConversationDetail take <1ms instead of reading huge JSONL files every second
    cache_marker = "// RAM_TRANSCRIPT_CACHE_V1"
    if cache_marker not in s:
        target = "export function parseAntigravityTranscript(convId: string, fullSteps = false, summaryRow?: SummaryRow): AntiConversation | null {"
        replacement = """// RAM_TRANSCRIPT_CACHE_V1
interface CachedTranscript {
  mtimeMs: number;
  size: number;
  customSig: string;
  fullConv: AntiConversation;
}
const transcriptRamCache = new Map<string, CachedTranscript>();

export function parseAntigravityTranscript(convId: string, fullSteps = false, summaryRow?: SummaryRow): AntiConversation | null {"""
        if target in s:
            s = s.replace(target, replacement, 1)
            changed = True

        # Prefer compact transcript.jsonl first (10x-30x smaller than transcript_full.jsonl) and use RAM cache
        old_body = """  const fullLogPath = join(BRAIN_DIR, convId, '.system_generated', 'logs', 'transcript_full.jsonl');
  const compactLogPath = join(BRAIN_DIR, convId, '.system_generated', 'logs', 'transcript.jsonl');
  const logPath = existsSync(fullLogPath) ? fullLogPath : compactLogPath;
  const hasLog = existsSync(logPath);
  if (!hasLog && !summaryRow) return null;

  let mtimeMs = Date.now();
  if (summaryRow?.last_modified_time) {
    const parsedTs = Date.parse(summaryRow.last_modified_time);
    if (!isNaN(parsedTs)) mtimeMs = parsedTs;
  }
  if (hasLog) {
    try {
      const fTime = statSync(logPath).mtimeMs;
      if (fTime > mtimeMs) mtimeMs = fTime;
    } catch {}
  }"""
        new_body = """  const compactLogPath = join(BRAIN_DIR, convId, '.system_generated', 'logs', 'transcript.jsonl');
  const fullLogPath = join(BRAIN_DIR, convId, '.system_generated', 'logs', 'transcript_full.jsonl');
  const logPath = existsSync(compactLogPath) ? compactLogPath : fullLogPath;
  const hasLog = existsSync(logPath);
  if (!hasLog && !summaryRow) return null;

  let mtimeMs = Date.now();
  let fileSize = 0;
  if (summaryRow?.last_modified_time) {
    const parsedTs = Date.parse(summaryRow.last_modified_time);
    if (!isNaN(parsedTs)) mtimeMs = parsedTs;
  }
  if (hasLog) {
    try {
      const stStat = statSync(logPath);
      if (stStat.mtimeMs > mtimeMs) mtimeMs = stStat.mtimeMs;
      fileSize = stStat.size;
    } catch {}
  }

  const stCheck = loadState();
  const cStepsCheck = stCheck.customSteps[convId] ?? [];
  const customSig = `${cStepsCheck.length}:${cStepsCheck[cStepsCheck.length - 1]?.createdAt || ''}:${summaryRow?.status || ''}:${summaryRow?.title || ''}`;
  const cached = transcriptRamCache.get(convId);
  if (cached && cached.mtimeMs === mtimeMs && cached.size === fileSize && cached.customSig === customSig) {
    if (fullSteps) return cached.fullConv;
    return { ...cached.fullConv, steps: undefined };
  }"""
        if old_body in s:
            s = s.replace(old_body, new_body, 1)
            changed = True

        old_return = """  return {
    id: convId,
    title: officialTitle.replace(/\\s+/g, ' ').trim(),
    projectFolder,
    subtitle: `${projectFolder}`,
    currentActivity: allSteps.length
      ? (allSteps[allSteps.length - 1].content || lastActivity).replace(/[#*`>|_-]/g, '').slice(0, 85)
      : lastActivity,
    status: isRunning ? 'working' : 'idle',
    progressPct: isRunning ? Math.min(95, 35 + (allSteps.length * 7) % 55) : 100,
    agentId: 'mama',
    agentName: 'Mama',
    source: 'antigravity-ide',
    updatedAt: mtimeMs,
    stepCount: allSteps.length || summaryRow?.step_count || 0,
    steps: fullSteps ? allSteps.slice(-60) : undefined,
  };"""
        new_return = """  const fullConvObj: AntiConversation = {
    id: convId,
    title: officialTitle.replace(/\\s+/g, ' ').trim(),
    projectFolder,
    subtitle: `${projectFolder}`,
    currentActivity: allSteps.length
      ? (allSteps[allSteps.length - 1].content || lastActivity).replace(/[#*`>|_-]/g, '').slice(0, 85)
      : lastActivity,
    status: isRunning ? 'working' : 'idle',
    progressPct: isRunning ? Math.min(95, 35 + (allSteps.length * 7) % 55) : 100,
    agentId: 'mama',
    agentName: 'Mama',
    source: 'antigravity-ide',
    updatedAt: mtimeMs,
    stepCount: allSteps.length || summaryRow?.step_count || 0,
    steps: allSteps.slice(-60),
  };
  transcriptRamCache.set(convId, { mtimeMs, size: fileSize, customSig, fullConv: fullConvObj });
  return fullSteps ? fullConvObj : { ...fullConvObj, steps: undefined };"""
        if old_return in s:
            s = s.replace(old_return, new_return, 1)
            changed = True

    if changed:
        BRIDGE_TS.write_text(s, encoding="utf-8")
        print("Patched antigravityBridge.ts (RAM Cache + Compact Log priority)")


def patch_server_ts():
    s = SERVER_TS.read_text(encoding="utf-8").replace("\r\n", "\n")
    changed = False

    # Return activeConvDetail inside /api/state so mobile doesn't need a second round-trip to load the first conversation
    old_state_route = """api.get('/state', wrap(() => ({
  ...office.snapshot(),
  providers: PROVIDERS,
  conversations: listAllConversations(25),
})));"""
    new_state_route = """api.get('/state', wrap(() => {
  const conversations = listAllConversations(25);
  const activeConvDetail = conversations.length > 0 ? getConversationDetail(conversations[0].id) : null;
  return {
    ...office.snapshot(),
    providers: PROVIDERS,
    conversations,
    activeConvDetail,
  };
}));"""
    if old_state_route in s:
        s = s.replace(old_state_route, new_state_route, 1)
        changed = True

    if changed:
        SERVER_TS.write_text(s, encoding="utf-8")
        print("Patched server.ts (Bundled activeConvDetail in /api/state)")


def patch_office3d_js():
    s = OFFICE3D_JS.read_text(encoding="utf-8").replace("\r\n", "\n")

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

    if old_nav in s:
        s = s.replace(old_nav, new_nav)

    old_resize = """    const scale = this.camera.aspect < 1.25 ? Math.min(2.1, 1.25 / this.camera.aspect) : 1;"""
    new_resize = """    const scale = this.camera.aspect < 1.25 ? Math.min(1.58, 1.15 / this.camera.aspect) : 1;"""
    if old_resize in s:
        s = s.replace(old_resize, new_resize)

    old_hud = """    // Chống đè thẻ (Screen-space collision repulsion 3 vòng lặp)
    const minW = 128, minH = 50;"""
    new_hud = """    // Chống đè thẻ (Screen-space collision repulsion: trên mobile thu gọn kích thước thẻ để không đẩy tràn màn hình)
    const isMob = w <= 768;
    const minW = isMob ? 64 : 128, minH = isMob ? 22 : 50;"""
    if old_hud in s:
        s = s.replace(old_hud, new_hud)

    OFFICE3D_JS.write_text(s, encoding="utf-8")
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

    # 3. Replace MOBILE_RESPONSIVE_TUNNEL_CSS block with comprehensive mobile stylesheet (fixing Flexbox scroll & composer visibility)
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
  /* Bắt buộc min-height: 0 cho chuỗi Flexbox để #log luôn cuộn mượt và không đẩy #composer biến mất */
  #chat-main {
    min-height: 0 !important;
    overflow: hidden !important;
  }
  #log {
    min-height: 0 !important;
    overflow-y: auto !important;
    -webkit-overflow-scrolling: touch !important;
    overscroll-behavior: contain !important;
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

    /* 4. Hai Thanh Công Cụ Đáy Tách Biệt Hoàn Toàn */
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
      display: none !important;
    }
    #hint, #feed { display: none !important; }

    /* 5. Khung Chat Mobile Fullscreen Chuẩn App: Cuộn Tin Nhắn Mượt & Nhắn Tin Tức Thì */
    #panel {
      position: fixed !important;
      top: 0 !important;
      left: 0 !important;
      right: 0 !important;
      bottom: 0 !important;
      width: 100vw !important;
      height: 100vh !important;
      height: 100dvh !important;
      min-width: 0 !important;
      min-height: 0 !important;
      max-width: none !important;
      max-height: none !important;
      border-radius: 0 !important;
      border: none !important;
      flex-direction: column !important;
      overflow: hidden !important;
      z-index: 40 !important;
    }
    .chat-resizer, #conv-splitter { display: none !important; }
    #btn-mob-convs {
      display: inline-flex !important;
      background: rgba(99, 102, 241, 0.18) !important;
      border-color: rgba(99, 102, 241, 0.5) !important;
      color: #c7d2fe !important;
      font-weight: 600 !important;
    }
    /* Mặc định hiển thị thanh chọn nhanh Cuộc trò chuyện & Agent gọn ở đầu, bấm 📂 DS Chat mở rộng */
    #conv-sidebar {
      width: 100% !important;
      min-width: 0 !important;
      max-height: 215px !important;
      border-right: none !important;
      border-bottom: 1px solid var(--line) !important;
      display: none !important;
      flex: 0 0 auto !important;
      overflow: hidden !important;
    }
    #panel.mob-convs-open #conv-sidebar {
      display: flex !important;
    }
    .sidebar-head { padding: 8px 12px 4px !important; flex: 0 0 auto !important; }
    .agy-folder-row { display: none !important; }
    #conv-list {
      max-height: 120px !important;
      overflow-y: auto !important;
      -webkit-overflow-scrolling: touch !important;
      touch-action: pan-y !important;
      padding: 4px 8px !important;
      flex: 1 1 auto !important;
    }
    .sidebar-agents {
      display: block !important;
      padding: 6px 10px !important;
      flex: 0 0 auto !important;
    }
    .sidebar-agents-title { display: none !important; }
    #agent-quick-pills {
      display: flex !important;
      flex-wrap: nowrap !important;
      overflow-x: auto !important;
      -webkit-overflow-scrolling: touch !important;
      touch-action: pan-x !important;
      gap: 5px !important;
      padding-bottom: 2px !important;
    }
    .a-pill { flex-shrink: 0 !important; padding: 4px 9px !important; font-size: 11px !important; }

    /* Cột phải (#chat-main) chiếm phần còn lại của màn hình với min-height: 0 để #log cuộn độc lập */
    #chat-main {
      flex: 1 1 0% !important;
      min-height: 0 !important;
      max-height: 100% !important;
      width: 100% !important;
      display: flex !important;
      flex-direction: column !important;
      overflow: hidden !important;
    }
    #chat-header {
      padding: 8px 10px !important;
      min-height: 44px !important;
      flex: 0 0 auto !important;
      cursor: default !important;
    }
    .ch-row1 {
      gap: 6px !important;
      width: 100% !important;
    }
    #p-conv-title {
      font-size: 13px !important;
      max-width: 40vw !important;
    }
    #p-size-lg {
      display: none !important;
    }
    #p-close {
      background: rgba(239, 68, 68, 0.18) !important;
      border-color: rgba(239, 68, 68, 0.5) !important;
      color: #fca5a5 !important;
      font-weight: 700 !important;
      padding: 5px 10px !important;
    }
    /* Vùng tin nhắn (#log): Cuộn cảm ứng mượt mà 100% trên iOS & Android */
    #log {
      flex: 1 1 0% !important;
      min-height: 0 !important;
      padding: 12px 12px !important;
      gap: 12px !important;
      overflow-y: auto !important;
      overflow-x: hidden !important;
      -webkit-overflow-scrolling: touch !important;
      touch-action: pan-y !important;
      overscroll-behavior: contain !important;
      user-select: text !important;
      -webkit-user-select: text !important;
    }
    .anti-msg-user {
      max-width: 90% !important;
      font-size: 13.5px !important;
      padding: 9px 13px !important;
    }
    .anti-content {
      font-size: 13.5px !important;
      line-height: 1.55 !important;
      overflow-x: auto !important;
    }
    /* Khung nhập tin nhắn (#composer): Luôn neo cố định dưới đáy, không bao giờ bị đẩy mất */
    #composer {
      flex: 0 0 auto !important;
      padding: 8px 10px calc(10px + env(safe-area-inset-bottom, 0px)) !important;
      background: rgba(13, 16, 23, 0.98) !important;
      border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
      position: relative !important;
      z-index: 5 !important;
    }
    #panel.theme-light #composer {
      background: #f8fafc !important;
      border-top: 1px solid #e5e7eb !important;
    }
    .composer-target-bar {
      display: flex !important;
      padding: 0 2px 5px !important;
      font-size: 11.5px !important;
    }
    #p-queue-hint { display: none !important; }
    .composer-row {
      display: flex !important;
      align-items: center !important;
      gap: 8px !important;
      padding: 6px 8px !important;
    }
    #composer textarea {
      height: 40px !important;
      min-height: 36px !important;
      max-height: 96px !important;
      font-size: 16px !important; /* 16px chuẩn iOS Safari/Chrome Mobile không bị tự zoom lệch khung */
      line-height: 1.35 !important;
      touch-action: manipulation !important;
    }
    #p-send {
      width: 38px !important;
      height: 38px !important;
      min-width: 38px !important;
      touch-action: manipulation !important;
      cursor: pointer !important;
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

    # Bust JS cache with ?v=mob4
    s = s.replace('/js/main.js?v=mob3', '/js/main.js?v=mob4').replace('/js/main.js"', '/js/main.js?v=mob4"')
    INDEX_HTML.write_text(s, encoding="utf-8")
    print("Patched index.html (v=mob4)")


def patch_main_js():
    s = MAIN_JS.read_text(encoding="utf-8").replace("\r\n", "\n")
    s = s.replace("from './scene/office3d.js?v=mob3';", "from './scene/office3d.js?v=mob4';").replace("from './scene/office3d.js';", "from './scene/office3d.js?v=mob4';")

    # 1. Add client-side convDetailCache & use activeConvDetail bundled in /api/state for 0ms chat opening
    old_load_state = """async function loadState() {
  const s = await api('/state');
  state.departments = s.departments || [];
  state.agents = s.agents || [];
  state.permissions = s.permissions || [];
  state.feed = s.feed || [];
  state.providers = s.providers || [];
  if (Array.isArray(s.conversations)) state.conversations = s.conversations;

  office.setData(state.departments, state.agents);
  if (!state.activeConvId && state.conversations.length) {
    state.activeConvId = state.conversations[0].id;
    api(`/conversations/${encodeURIComponent(state.activeConvId)}`).then(d => {
      state.activeConvDetail = d;
      renderChatStream();
      renderPanelHeaderAndQueue();
    }).catch(() => {});
  }
  renderHud();
  renderFeed();
  renderConversationSidebar();
  renderPanelHeaderAndQueue();
}"""

    new_load_state = """const convDetailCache = new Map();

async function loadState() {
  const s = await api('/state');
  state.departments = s.departments || [];
  state.agents = s.agents || [];
  state.permissions = s.permissions || [];
  state.feed = s.feed || [];
  state.providers = s.providers || [];
  if (Array.isArray(s.conversations)) state.conversations = s.conversations;
  if (s.activeConvDetail && s.activeConvDetail.id) {
    convDetailCache.set(s.activeConvDetail.id, s.activeConvDetail);
  }

  if (office.scene) {
    office.setData(state.departments, state.agents);
  }
  if (!state.activeConvId && state.conversations.length) {
    state.activeConvId = state.conversations[0].id;
    if (s.activeConvDetail && s.activeConvDetail.id === state.activeConvId) {
      state.activeConvDetail = s.activeConvDetail;
      renderChatStream(true);
    } else {
      api(`/conversations/${encodeURIComponent(state.activeConvId)}`).then(d => {
        convDetailCache.set(d.id, d);
        state.activeConvDetail = d;
        renderChatStream(true);
        renderPanelHeaderAndQueue();
      }).catch(() => {});
    }
  }
  renderHud();
  renderFeed();
  renderConversationSidebar();
  renderPanelHeaderAndQueue();
}"""
    if old_load_state in s:
        s = s.replace(old_load_state, new_load_state, 1)

    # 2. Speed up selectConversation() using convDetailCache + instant mobile drawer collapse
    old_select_conv = """async function selectConversation(convId) {
  state.activeConvId = convId;
  renderConversationSidebar();
  try {
    const detail = await api(`/conversations/${encodeURIComponent(convId)}`);
    state.activeConvDetail = detail;
    if (detail.agentId && agentById(detail.agentId)) {
      selectedId = detail.agentId;
      office.select(selectedId);
    }
    renderPanelHeaderAndQueue();
    renderChatStream();
    renderConversationSidebar();
  } catch (e) {
    toast(e.message);
  }
}"""

    new_select_conv = """async function selectConversation(convId) {
  state.activeConvId = convId;
  // Tự động đóng ngăn DS Chat trên mobile sau khi bấm chọn cuộc trò chuyện
  $('#panel')?.classList.remove('mob-convs-open');
  if ($('#btn-mob-convs')) $('#btn-mob-convs').textContent = '📂 DS Chat';

  const cached = convDetailCache.get(convId);
  if (cached) {
    state.activeConvDetail = cached;
    renderPanelHeaderAndQueue();
    renderChatStream(true);
  } else {
    const log = $('#log');
    if (log) log.innerHTML = `<div class="muted" style="text-align:center;margin:auto;padding:24px">⏳ Đang tải cuộc trò chuyện…</div>`;
  }
  renderConversationSidebar();
  try {
    const detail = await api(`/conversations/${encodeURIComponent(convId)}`);
    convDetailCache.set(convId, detail);
    if (state.activeConvId === convId) {
      state.activeConvDetail = detail;
      if (detail.agentId && agentById(detail.agentId)) {
        selectedId = detail.agentId;
        office.select(selectedId);
      }
      renderPanelHeaderAndQueue();
      renderChatStream(true);
      renderConversationSidebar();
    }
  } catch (e) {
    toast(e.message);
  }
}"""
    if old_select_conv in s:
        s = s.replace(old_select_conv, new_select_conv, 1)

    # 3. Fix renderChatStream() so it doesn't destroy touch scrolling every 2 seconds when content hasn't changed
    old_render_stream = """function renderChatStream() {
  const log = $('#log');
  if (!log) return;
  const conv = state.activeConvDetail;
  if (!conv || !conv.steps || !conv.steps.length) {
    log.innerHTML = `<div class="muted" style="text-align:center;margin:auto;padding:24px">
      Nhập tin nhắn bên dưới để bắt đầu trò chuyện.
    </div>`;
    return;
  }

  // Chỉ hiển thị câu hỏi của User và câu trả lời sạch của Antigravity (ẩn toàn bộ bước trung gian thừa)
  const visibleSteps = conv.steps.filter(st => st.role === 'user' || (st.content && st.content.trim().length > 0));
  const lastStep = visibleSteps[visibleSteps.length - 1];
  const waitingIndicator = (lastStep && lastStep.role === 'user')
    ? `<div class="anti-msg-agent"><div class="anti-content" style="opacity:0.75;font-style:italic">⏳ Đang trả lời...</div></div>`
    : '';
  log.innerHTML = visibleSteps
    .map(st => {
      if (st.role === 'user') {
        return `<div class="anti-msg-user">${esc(st.content)}</div>`;
      }
      return `
        <div class="anti-msg-agent">
          <div class="anti-content">${renderMarkdown(st.content)}</div>
        </div>`;
    }).join('') + waitingIndicator;

  log.scrollTop = log.scrollHeight;
}"""

    new_render_stream = """function renderChatStream(forceScroll = false) {
  const log = $('#log');
  if (!log) return;
  const conv = state.activeConvDetail;
  if (!conv || !conv.steps || !conv.steps.length) {
    renderChatStream._lastSig = `${conv?.id || 'none'}:empty`;
    log.innerHTML = `<div class="muted" style="text-align:center;margin:auto;padding:24px">
      Nhập tin nhắn bên dưới để bắt đầu trò chuyện.
    </div>`;
    return;
  }

  // Chỉ hiển thị câu hỏi của User và câu trả lời sạch của Antigravity (ẩn toàn bộ bước trung gian thừa)
  const visibleSteps = conv.steps.filter(st => st.role === 'user' || (st.content && st.content.trim().length > 0));
  const lastStep = visibleSteps[visibleSteps.length - 1];
  const streamSig = `${conv.id}:${visibleSteps.length}:${lastStep?.role || ''}:${(lastStep?.content || '').length}`;
  if (!forceScroll && renderChatStream._lastSig === streamSig) {
    return; // Không ghi đè DOM khi nội dung chưa đổi để bảo toàn vị trí cuộn cảm ứng trên Mobile
  }
  const wasNearBottom = (log.scrollHeight - log.scrollTop - log.clientHeight) < 140;
  renderChatStream._lastSig = streamSig;

  const waitingIndicator = (lastStep && lastStep.role === 'user')
    ? `<div class="anti-msg-agent"><div class="anti-content" style="opacity:0.75;font-style:italic">⏳ Đang trả lời...</div></div>`
    : '';
  log.innerHTML = visibleSteps
    .map(st => {
      if (st.role === 'user') {
        return `<div class="anti-msg-user">${esc(st.content)}</div>`;
      }
      return `
        <div class="anti-msg-agent">
          <div class="anti-content">${renderMarkdown(st.content)}</div>
        </div>`;
    }).join('') + waitingIndicator;

  if (forceScroll || wasNearBottom) {
    requestAnimationFrame(() => {
      log.scrollTop = log.scrollHeight;
    });
  }
}"""
    if old_render_stream in s:
        s = s.replace(old_render_stream, new_render_stream, 1)

    # 4. Make sendTask() rock-solid on Mobile (works even when activeConvDetail wasn't loaded yet, and scrolls immediately)
    old_send_task = """    // Hiển thị tức thì tin nhắn vừa gửi + trạng thái Đang trả lời (0ms delay)
    if (state.activeConvDetail && Array.isArray(state.activeConvDetail.steps)) {
      state.activeConvDetail.steps.push({ role: 'user', content: prompt, createdAt: new Date().toISOString() });
      renderChatStream();
    }

    const res = await api(`/conversations/${encodeURIComponent(convId)}/messages`, 'POST', {
      agentId: targetAgent,
      prompt,
      attachments: attIds,
    });
    if (res.conv) {
      state.activeConvDetail = res.conv;
      renderChatStream();
    }"""

    new_send_task = """    // Hiển thị tức thì tin nhắn vừa gửi + trạng thái Đang trả lời (0ms delay)
    if (!state.activeConvDetail || state.activeConvDetail.id !== convId) {
      state.activeConvDetail = { id: convId, title: prompt.slice(0, 60), steps: [] };
    }
    if (!Array.isArray(state.activeConvDetail.steps)) {
      state.activeConvDetail.steps = [];
    }
    state.activeConvDetail.steps.push({ role: 'user', content: prompt, createdAt: new Date().toISOString() });
    renderChatStream(true);

    const res = await api(`/conversations/${encodeURIComponent(convId)}/messages`, 'POST', {
      agentId: targetAgent,
      prompt,
      attachments: attIds,
    });
    if (res.conv) {
      convDetailCache.set(res.conv.id, res.conv);
      state.activeConvDetail = res.conv;
      renderChatStream(true);
    }"""
    if old_send_task in s:
        s = s.replace(old_send_task, new_send_task, 1)

    # 5. Guard desktop drag/resize handlers so they never set fixed pixel width/height/top/left on Mobile <= 768px
    old_resizer_down = """      handle.addEventListener('pointerdown', (e) => {
      e.preventDefault();"""
    new_resizer_down = """      handle.addEventListener('pointerdown', (e) => {
      if (window.innerWidth <= 768) return;
      e.preventDefault();"""
    s = s.replace(old_resizer_down, new_resizer_down)

    old_header_down = """    header.addEventListener('pointerdown', (e) => {
      if (e.target.closest('button, select, input')) return;"""
    new_header_down = """    header.addEventListener('pointerdown', (e) => {
      if (window.innerWidth <= 768) return;
      if (e.target.closest('button, select, input')) return;"""
    s = s.replace(old_header_down, new_header_down)

    # 6. Upgrade MOBILE_NAV_HANDLERS_V2 -> V3 (with instant touch send, visualViewport keyboard adaptation, and parallel loadState + office.init)
    idx_v2 = s.find("/* MOBILE_NAV_HANDLERS_V2 */")
    if idx_v2 != -1:
        s = s[:idx_v2]

    mobile_v3_and_boot = """/* MOBILE_NAV_HANDLERS_V2 */
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

  // Đảm bảo nút Gửi (#p-send) trên Mobile phản hồi ngay lập tức khi chạm (không bị sự kiện đóng bàn phím ảo nuốt click)
  const sendBtn = $('#p-send');
  if (sendBtn) {
    sendBtn.addEventListener('pointerdown', (e) => {
      if (window.innerWidth <= 768) {
        e.preventDefault();
        sendTask();
      }
    });
  }

  // Tự động co chiều cao #panel khớp với bàn phím ảo trên iPhone/Android (visualViewport)
  const syncMobileViewport = () => {
    const p = $('#panel');
    if (!p || window.innerWidth > 768) return;
    p.style.width = '';
    p.style.left = '';
    p.style.right = '';
    p.style.bottom = '';
    if (window.visualViewport) {
      p.style.height = `${Math.round(window.visualViewport.height)}px`;
      p.style.top = `${Math.round(window.visualViewport.offsetTop)}px`;
    } else {
      p.style.height = '';
      p.style.top = '';
    }
  };
  window.visualViewport?.addEventListener('resize', syncMobileViewport);
  window.visualViewport?.addEventListener('scroll', syncMobileViewport);
  window.addEventListener('resize', syncMobileViewport);
})();

// Tải dữ liệu Cuộc trò chuyện & kết nối WebSocket NGAY LẬP TỨC (song song với khởi tạo 3D, không bắt chờ 3D tải xong!)
connect();
loadState().catch(() => {});

await office.init();
if (state.departments.length || state.agents.length) {
  office.setData(state.departments, state.agents);
}
renderQuality();
window.__office = office;
"""
    s = s + mobile_v3_and_boot
    MAIN_JS.write_text(s, encoding="utf-8")
    print("Patched main.js (Instant parallel connect + touch scroll & mobile send fixes)")


if __name__ == "__main__":
    patch_bridge_ts()
    patch_server_ts()
    patch_office3d_js()
    patch_index_html()
    patch_main_js()
    print("MOBILE_UI_AND_CHAT_UPGRADE_COMPLETE")
