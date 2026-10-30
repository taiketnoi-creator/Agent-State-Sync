// Ứng dụng Văn phòng ảo 3D Agent-Javis:
// - Đồng bộ trực tiếp Đa Cuộc Trò Chuyện chuẩn Antigravity IDE (Thinking, Tool Calls, Markdown)
// - Bấm vào nhân vật 3D để giao việc trực tiếp + Hàng đợi tuần tự (Queue #1, #2, #3...)
// - Hiệu ứng truyền thông tin 3D (Mama <-> Subagent <-> Bộ Não Thứ 2) + Nhân vật đi bộ trò chuyện
import { Office3D, QUALITY } from './scene/office3d.js';

const TOKEN = document.querySelector('meta[name="office-token"]').content;
const PROVIDER_LABEL = {
  'claude-code': 'Claude Code',
  'codex': 'Agent-Javis / Antigravity',
  'anthropic-chat': 'Claude API',
  'openai-chat': 'OpenAI API',
  'observer': 'Quan sát phiên',
};
const STATUS_LABEL = {
  idle: 'Rảnh • Sẵn sàng',
  queued: 'Chờ việc trong hàng đợi',
  working: 'Đang thực thi',
  waiting: 'Xin duyệt quyền',
  error: 'Lỗi',
  offline: 'Offline',
};
const SHAPES = {
  zone: 'Khu cụm bàn',
  lounge: 'Lounge trung tâm',
  room: 'Phòng họp kính',
  cafe: 'Khu cà phê (giờ nghỉ)',
  game: 'Khu giải trí (giờ nghỉ)',
};
const AMENITY = new Set(['cafe', 'game']);
const THEMES = {
  docs: 'Văn bản',
  code: 'Code',
  design: 'Thiết kế',
  charts: 'Biểu đồ',
  media: 'Mạng xã hội',
  video: 'Dựng phim',
};

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const hhmm = (ts) => {
  const d = new Date(ts);
  return isNaN(d.getTime()) ? '' : d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
};
const ago = (ts) => {
  const m = Math.round((Date.now() - ts) / 60000);
  return m < 1 ? 'vừa xong' : m < 60 ? `${m} phút trước` : m < 1440 ? `${Math.round(m / 60)} giờ trước` : `${Math.round(m / 1440)} ngày trước`;
};

function toast(msg, ms = 3200) {
  const t = $('#toast');
  t.textContent = msg;
  t.style.display = 'block';
  clearTimeout(toast._t);
  toast._t = setTimeout(() => t.style.display = 'none', ms);
}

async function api(path, method = 'GET', body) {
  const r = await fetch('/api' + path, {
    method,
    headers: { 'content-type': 'application/json', 'x-office-token': TOKEN },
    body: body ? JSON.stringify(body) : undefined,
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.error || r.statusText);
  return j;
}

/** Render Markdown nhẹ chuẩn Antigravity IDE */
function renderMarkdown(md) {
  if (!md) return '';
  let s = esc(md);
  s = s.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (_m, _lang, code) => `<pre><code>${code.trim()}</code></pre>`);
  s = s.replace(/`([^`\n]+)`/g, '<code>$1</code>');
  s = s.replace(/^####\s+(.+)$/gm, '<h4>$1</h4>');
  s = s.replace(/^###\s+(.+)$/gm, '<h3>$1</h3>');
  s = s.replace(/^##\s+(.+)$/gm, '<h3>$1</h3>');
  s = s.replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
  s = s.replace(/^\s*[-*]\s+(.+)$/gm, '<li>$1</li>');
  s = s.replace(/(<li>[\s\S]*?<\/li>)/g, '<ul>$1</ul>');
  s = s.replace(/<\/ul>\s*<ul>/g, '');
  s = s.replace(/\n{2,}/g, '<br><br>').replace(/\n/g, '<br>');
  return s;
}

// ---------------- Tệp đính kèm (dán ảnh, kéo thả, chọn tệp)
const fmtSize = (n) => n >= 1048576 ? (n / 1048576).toFixed(1) + 'MB' : Math.max(1, Math.round(n / 1024)) + 'KB';
const extOf = (n) => (String(n).split('.').pop() || '').slice(0, 4);
const MAX_FILES = 10, MAX_SIZE = 25 * 1024 * 1024;

function makeTray({ list: listEl, input, dropZone, fileInput, button }) {
  const items = [];
  const render = () => {
    listEl.innerHTML = items.map((it, i) => `
      <div class="att ${it.status === 'uploading' ? 'uploading' : ''} ${it.status === 'error' ? 'err' : ''}" title="${esc(it.name)}">
        ${it.preview ? `<img src="${it.preview}" alt="" />` : `<div class="ficon">${esc(extOf(it.name))}</div>`}
        <div class="nm">${esc(it.name)}<small>${it.status === 'uploading' ? 'đang tải lên…' : it.status === 'error' ? 'lỗi tải lên' : fmtSize(it.size)}</small></div>
        <button class="x" type="button" data-rm="${i}" title="Bỏ tệp">×</button>
      </div>`).join('');
  };
  listEl.addEventListener('click', e => {
    const b = e.target.closest('[data-rm]'); if (!b) return;
    const [it] = items.splice(+b.dataset.rm, 1);
    if (it?.preview) URL.revokeObjectURL(it.preview);
    render();
  });
  async function add(files) {
    for (const f of files) {
      if (items.length >= MAX_FILES) { toast(`Tối đa ${MAX_FILES} tệp mỗi việc`); break; }
      if (f.size > MAX_SIZE) { toast(`${f.name} quá lớn (tối đa 25MB)`); continue; }
      let name = f.name || 'tep';
      if (/^image\.(png|jpe?g|gif|webp)$/i.test(name) || !f.name) {
        const d = new Date(); const p = (n) => String(n).padStart(2, '0');
        name = `anh-dan-${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}.${(f.type.split('/')[1] || 'png').replace('jpeg', 'jpg')}`;
      }
      const it = { name, size: f.size, mime: f.type, status: 'uploading', preview: f.type.startsWith('image/') ? URL.createObjectURL(f) : null };
      items.push(it); render();
      try {
        const r = await fetch('/api/uploads', {
          method: 'POST', body: f,
          headers: { 'x-office-token': TOKEN, 'content-type': 'application/octet-stream', 'x-filename': encodeURIComponent(name), 'x-mime': f.type || '' },
        });
        const j = await r.json().catch(() => ({}));
        if (!r.ok) throw new Error(j.error || r.statusText);
        it.id = j.id; it.status = 'ok';
      } catch (err) {
        it.status = 'error';
        toast(`Không tải lên được ${name}: ${err.message}`);
      }
      render();
    }
  }
  input.addEventListener('paste', e => {
    const files = [...(e.clipboardData?.files ?? [])];
    if (!files.length) return;
    if (!e.clipboardData.getData('text/plain')) e.preventDefault();
    add(files);
  });
  let depth = 0;
  const hasFiles = (e) => [...(e.dataTransfer?.types ?? [])].includes('Files');
  dropZone.addEventListener('dragenter', e => { if (!hasFiles(e)) return; e.preventDefault(); depth++; dropZone.classList.add('dragging'); });
  dropZone.addEventListener('dragover', e => { if (hasFiles(e)) e.preventDefault(); });
  dropZone.addEventListener('dragleave', () => { if (--depth <= 0) { depth = 0; dropZone.classList.remove('dragging'); } });
  dropZone.addEventListener('drop', e => {
    if (!hasFiles(e)) return; e.preventDefault(); depth = 0; dropZone.classList.remove('dragging');
    add([...e.dataTransfer.files]);
  });
  button.onclick = () => fileInput.click();
  fileInput.onchange = () => { add([...fileInput.files]); fileInput.value = ''; };
  return {
    busy: () => items.some(it => it.status === 'uploading'),
    ids: () => items.filter(it => it.status === 'ok').map(it => it.id),
    count: () => items.filter(it => it.status === 'ok').length,
    clear: () => { items.forEach(it => it.preview && URL.revokeObjectURL(it.preview)); items.length = 0; render(); },
  };
}

// ---------------- Trạng thái toàn cục
const state = {
  departments: [],
  agents: [],
  permissions: [],
  feed: [],
  providers: [],
  conversations: [],
  activeConvId: null,
  activeConvDetail: null,
};

let selectedId = 'mama';
const agentById = (id) => state.agents.find(a => a.id === id);
const deptById = (id) => state.departments.find(d => d.id === id);

// ---------------- Cảnh 3D
const params = new URLSearchParams(location.search);
const office = new Office3D($('#stage'), {
  onPick: (id) => onPickAgent3D(id),
  onProgress: (msg) => { $('#loading-text').textContent = msg; },
  onDeptMoved: async (dept) => {
    try {
      await api(`/departments/${encodeURIComponent(dept.id)}`, 'PUT', {
        name: dept.name, color: dept.color, x: dept.x, z: dept.z, w: dept.w, d: dept.d, style: dept.style,
      });
      toast(`🏗️ Đã di chuyển phòng ban "${dept.name}" tới tọa độ (${dept.x}, ${dept.z})`);
    } catch (e) {
      toast(`Lỗi lưu vị trí phòng ban: ${e.message}`);
    }
  },
  onCameraChange: ({ mode, autoRotate }) => {
    $('#mode-orbit')?.classList.toggle('active', mode === 'orbit');
    $('#mode-pan')?.classList.toggle('active', mode === 'pan');
    $('#mode-dept')?.classList.toggle('active', mode === 'move_dept');
    $('#btn-spin360')?.classList.toggle('active-Spin', !!autoRotate);
  },
});
if (params.get('q') && QUALITY[params.get('q')]) office.quality = params.get('q');
if (params.get('auto') === '0') office.autoQuality = false;
if (params.get('nghi') === 'nhanh') office.leisureSpeed = 10;
office.onLeisure = () => renderHud();
office.onQualityAuto = (q) => { renderQuality(); toast(`Đã tự động tối ưu chất lượng 3D sang "${QUALITY[q]}"`); };

function renderQuality() { $('#btn-quality').textContent = `Chất lượng: ${QUALITY[office.quality]}`; }
$('#btn-quality').onclick = () => {
  const order = ['high', 'medium', 'low'];
  office.autoQuality = false;
  office.applyQuality(order[(order.indexOf(office.quality) + 1) % 3]);
  renderQuality();
};
$('#btn-overview').onclick = () => office.overview();

$('#btn-collab-wave').onclick = async () => {
  try {
    await api('/collab-wave', 'POST', { topic: 'Triển khai Chiến dịch 4 Page & Kiểm duyệt Luật #10' });
    toast('⚡ Mama đang truyền lệnh xuống các Subagent & Bộ Não Thứ 2 trên sàn 3D!');
  } catch (e) { toast(e.message); }
};

// ---------------- HUD & Feed
function renderHud() {
  const working = state.agents.filter(a => a.status === 'working' || a.status === 'waiting');
  const lead = working.find(a => a.status === 'waiting') ?? working[0];
  if (lead) {
    const dept = deptById(lead.departmentId)?.name ?? '';
    $('#hud-title').textContent = `${lead.name} (${lead.progressPct || 35}%)`;
    $('#hud-sub').textContent = lead.activityText || lead.currentTask?.prompt?.slice(0, 100) || `${dept} · đang thực thi`;
  } else {
    $('#hud-title').textContent = `Đội 11 Agent-Javis Sẵn Sàng`;
    $('#hud-sub').textContent = 'Bấm vào nhân vật 3D bất kỳ để giao việc trực tiếp hoặc mở 💬 Antigravity Chat.';
  }
  const q = state.agents.reduce((s, a) => s + (a.queued || 0), 0);
  const lc = office.leisureCounts?.() ?? { cafe: 0, game: 0 };
  const rest = [lc.cafe && `${lc.cafe} uống cà phê`, lc.game && `${lc.game} giải trí`].filter(Boolean).join(', ');
  $('#hud-count').textContent = `${working.length} đang làm việc` + (q ? ` · ${q} việc xếp hàng` : '') + ` · ${state.agents.length} nhân sự 3D` + (rest ? ` · ${rest}` : '') + ` · ${state.conversations.length} cuộc trò chuyện`;
}

function renderFeed() {
  const fresh = state.feed.filter(e => Date.now() - e.ts < 180000);
  $('#feed').innerHTML = fresh.slice(-4).map(e => {
    const a = agentById(e.agentId);
    return `<div>${hhmm(e.ts)} · <b>${esc(a?.name ?? e.agentId)}</b>: ${esc(e.text.slice(0, 110))}</div>`;
  }).join('');
}
setInterval(renderFeed, 15000);

// ============================================================================
// QUẢN LÝ ĐA CUỘC TRÒ CHUYỆN CHUẨN ANTIGRAVITY IDE & HÀNG ĐỢI TUẦN TỰ
// ============================================================================
function shortAgo(ts) {
  const m = Math.max(1, Math.round((Date.now() - ts) / 60000));
  if (m < 60) return `${m}m`;
  const h = Math.round(m / 60);
  if (h < 24) return `${h}h`;
  return `${Math.round(h / 24)}d`;
}

function renderConversationSidebar() {
  const listEl = $('#conv-list');
  if (!listEl) return;
  if (!state.conversations.length) {
    listEl.innerHTML = `<div class="muted" style="padding:12px 14px">Chưa có cuộc trò chuyện nào.</div>`;
  } else {
    listEl.innerHTML = state.conversations.map(c => {
      const isAct = c.id === state.activeConvId;
      const dotCls = c.status === 'working' ? 'working' : '';
      return `
        <div class="agy-tab-item conv-item ${isAct ? 'active' : ''}" data-cid="${esc(c.id)}" title="${esc(c.title)} — ${esc(c.currentActivity || '')}">
          <span class="t-dot ${dotCls}"></span>
          <span class="t-title">${esc(c.title)}</span>
          <span class="t-time">${shortAgo(c.updatedAt)}</span>
          <button class="c-del" type="button" data-del-cid="${esc(c.id)}" title="Xoá cuộc trò chuyện này">×</button>
        </div>`;
    }).join('');
  }

  // Render 11 nhân sự nhanh ở đáy Sidebar
  const pillsEl = $('#agent-quick-pills');
  if (pillsEl) {
    pillsEl.innerHTML = state.agents.map(a => {
      const short = a.name.replace(/\s*\(.*?\)\s*/g, '').trim();
      const dotCls = a.status === 'working' ? 'working' : a.queued > 0 ? 'queued' : '';
      const badge = a.status === 'working' ? ` ${a.progressPct || 35}%` : a.queued > 0 ? ` #${a.queued}` : '';
      return `<div class="a-pill ${a.id === selectedId ? 'selected' : ''}" data-aid="${esc(a.id)}" title="${esc(a.name)} — ${esc(a.role)}">
        <span class="dot ${dotCls}"></span><span>${esc(short)}${esc(badge)}</span>
      </div>`;
    }).join('');
  }

  // Cập nhật dropdown chọn nhân vật 3D nhận việc
  const selEl = $('#p-target-agent');
  if (selEl) {
    selEl.innerHTML = state.agents.map(a => {
      const stText = a.status === 'working' ? ` [Đang làm ${a.progressPct || 35}% — sẽ xếp hàng đợi]` : a.queued > 0 ? ` [Đang chờ ${a.queued} việc]` : ' [Sẵn sàng]';
      return `<option value="${esc(a.id)}" ${a.id === selectedId ? 'selected' : ''}>${esc(a.name)}${esc(stText)}</option>`;
    }).join('');
  }
}

$('#conv-list').addEventListener('click', async (e) => {
  const delBtn = e.target.closest('[data-del-cid]');
  if (delBtn) {
    e.stopPropagation();
    const cid = delBtn.dataset.delCid;
    if (!confirm('Xoá cuộc trò chuyện này khỏi danh sách?')) return;
    try {
      await api(`/conversations/${encodeURIComponent(cid)}`, 'DELETE');
      state.conversations = state.conversations.filter(c => c.id !== cid);
      if (state.activeConvId === cid) {
        state.activeConvId = state.conversations[0]?.id ?? null;
        if (state.activeConvId) await selectConversation(state.activeConvId);
        else { state.activeConvDetail = null; renderChatStream(); }
      }
      renderConversationSidebar();
      toast('Đã xoá cuộc trò chuyện');
    } catch (err) { toast(err.message); }
    return;
  }
  const item = e.target.closest('[data-cid]');
  if (item) await selectConversation(item.dataset.cid);
});

$('#agent-quick-pills').addEventListener('click', (e) => {
  const pill = e.target.closest('[data-aid]');
  if (!pill) return;
  selectAgentTarget(pill.dataset.aid, true);
});

$('#p-target-agent').addEventListener('change', (e) => {
  selectAgentTarget(e.target.value, false);
});

$('#btn-new-conv').onclick = async () => {
  try {
    const conv = await api('/conversations', 'POST', { agentId: selectedId || 'mama' });
    state.conversations.unshift(conv);
    await selectConversation(conv.id);
    $('#p-input').focus();
    toast(`Đã tạo cuộc trò chuyện mới với ${conv.agentName}`);
  } catch (e) { toast(e.message); }
};

async function selectConversation(convId) {
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
}

function selectAgentTarget(agentId, flyCamera = false) {
  if (!agentById(agentId)) return;
  selectedId = agentId;
  office.select(agentId);
  if (flyCamera) office.flyTo(agentId);
  renderConversationSidebar();
  renderPanelHeaderAndQueue();
}

/** Khi CEO bấm trực tiếp vào nhân vật 3D trên mặt sàn */
async function onPickAgent3D(agentId) {
  selectedId = agentId;
  office.select(agentId);
  $('#panel').classList.add('open');
  document.body.classList.add('panel-open');

  // Tìm cuộc trò chuyện gần nhất của Agent này hoặc giữ cuộc trò chuyện hiện tại nhưng đổi mục tiêu giao việc sang Agent vừa bấm
  const agentConv = state.conversations.find(c => c.agentId === agentId);
  if (agentConv) {
    await selectConversation(agentConv.id);
  } else if (!state.activeConvId && state.conversations.length) {
    await selectConversation(state.conversations[0].id);
  }
  selectAgentTarget(agentId, false);
  const a = agentById(agentId);
  if (a) {
    toast(`🎯 Đang chọn ${a.name} — ${a.status === 'working' ? `Đang bận (${a.progressPct || 35}%), việc mới sẽ tự động xếp vào hàng đợi!` : 'Sẵn sàng nhận việc ngay!'}`);
  }
  $('#p-input').focus();
}

$('#btn-chat-toggle').onclick = async () => {
  const isOpen = $('#panel').classList.contains('open');
  if (isOpen) {
    closePanel();
  } else {
    $('#panel').classList.add('open');
    document.body.classList.add('panel-open');
    if (!state.activeConvId && state.conversations.length) {
      await selectConversation(state.conversations[0].id);
    } else if (state.activeConvId) {
      await selectConversation(state.activeConvId);
    }
  }
};

function closePanel() {
  $('#panel').classList.remove('open');
  document.body.classList.remove('panel-open');
  office.select(null);
}

function renderPanelHeaderAndQueue() {
  const a = agentById(selectedId) ?? state.agents[0];
  const conv = state.activeConvDetail;
  $('#p-conv-title').textContent = conv ? conv.title : (a ? a.name : 'Antigravity Chat');

  if (a) {
    const chips = [
      `<span class="chip status-${a.status}">🎯 ${esc(a.name)}: ${STATUS_LABEL[a.status] ?? a.status}${a.status === 'working' ? ` (${a.progressPct || 35}%)` : ''}</span>`,
      `<span class="chip">${esc(deptById(a.departmentId)?.name ?? '')}</span>`,
    ];
    if (a.queued > 0) {
      chips.push(`<span class="chip status-queued">⏳ ${a.queued} việc trong hàng đợi</span>`);
    }
    if (conv?.source === 'antigravity-ide') {
      chips.push(`<span class="chip" style="color:#a5b4fc;border-color:rgba(99,102,241,0.45)">🔗 Đồng bộ trực tiếp Antigravity IDE</span>`);
    }
    $('#p-chips').innerHTML = chips.join('');

    // Cập nhật Thanh Tiến Độ & Hàng Đợi Tuần Tự (Task Queue)
    const qb = $('#queue-banner');
    const qTasks = a.queuedTasks ?? [];
    if (a.status === 'working' || a.status === 'waiting' || qTasks.length > 0) {
      qb.classList.add('visible');
      const pct = a.status === 'working' ? Math.max(8, a.progressPct || 35) : 0;
      $('#q-active-text').textContent = a.status === 'working'
        ? `${a.activityText || '⚡ Đang thực thi'}${a.currentTask?.prompt ? ` — "${a.currentTask.prompt.slice(0, 58)}"` : ''}`
        : `⏳ Đang chuẩn bị chạy hàng đợi (${qTasks.length} việc chờ)…`;
      $('#q-active-pct').textContent = a.status === 'working' ? `${pct}%` : `Chờ #${qTasks.length}`;
      $('#q-bar-fill').style.width = `${pct}%`;

      $('#q-list').innerHTML = qTasks.map(qt => `
        <div class="q-item">
          <span><b>Hàng đợi #${qt.position}:</b> ${esc(qt.prompt.slice(0, 68))}</span>
          <div style="display:flex;gap:4px">
            ${qt.position > 1 ? `<button type="button" data-q-up="${esc(qt.id)}" title="Đẩy lên ưu tiên #1">↑ Ưu tiên</button>` : ''}
            <button type="button" data-q-del="${esc(qt.id)}" title="Huỷ việc này khỏi hàng đợi">× Huỷ</button>
          </div>
        </div>`).join('');
    } else {
      qb.classList.remove('visible');
    }

    $('#p-queue-hint').textContent = a.status === 'working'
      ? `⏳ ${a.name} đang bận (${a.progressPct || 35}%) → Gửi lệnh sẽ xếp vào Hàng đợi #${(a.queued || 0) + 1}`
      : `🟢 ${a.name} đang rảnh → Gửi lệnh sẽ thực thi ngay lập tức`;
  }
  renderPerms();
}

$('#q-list').addEventListener('click', async (e) => {
  const upBtn = e.target.closest('[data-q-up]');
  if (upBtn) {
    try { await api(`/queue/${encodeURIComponent(upBtn.dataset.qUp)}/promote`, 'POST'); await loadState(); toast('Đã đẩy công việc lên đầu hàng đợi'); }
    catch (err) { toast(err.message); }
    return;
  }
  const delBtn = e.target.closest('[data-q-del]');
  if (delBtn) {
    try { await api(`/queue/${encodeURIComponent(delBtn.dataset.qDel)}`, 'DELETE'); await loadState(); toast('Đã xoá công việc khỏi hàng đợi'); }
    catch (err) { toast(err.message); }
  }
});

function renderChatStream() {
  const log = $('#log');
  if (!log) return;
  const conv = state.activeConvDetail;
  if (!conv || !conv.steps || !conv.steps.length) {
    log.innerHTML = `<div class="muted" style="text-align:center;margin:auto;padding:24px">
      Chưa có tin nhắn nào trong cuộc trò chuyện này.<br>Hãy nhập yêu cầu bên dưới để giao việc cho <b>${esc(agentById(selectedId)?.name ?? 'Mama')}</b>!
    </div>`;
    return;
  }

  log.innerHTML = conv.steps.map(st => {
    const timeStr = hhmm(st.createdAt);
    if (st.role === 'user') {
      return `
        <div class="anti-msg-user">
          <div class="u-meta"><span>👤 CEO</span><span>${esc(timeStr)}</span></div>
          <div>${esc(st.content)}</div>
        </div>`;
    }
    const agName = st.agentName || conv.agentName || 'Mama (Gemini 4)';
    const thinkBlock = st.thinking
      ? `<details class="anti-thinking">
          <summary>💭 Quá trình suy nghĩ &amp; kiểm tra quy tắc (${Math.max(1, Math.round(st.thinking.length / 85))}s)</summary>
          <div class="think-body">${esc(st.thinking)}</div>
        </details>`
      : '';
    const toolsBlock = st.toolCalls && st.toolCalls.length
      ? `<div class="anti-tools">${st.toolCalls.map(tc => `
          <div class="anti-tool-pill">
            <span class="ok">✓</span>
            <span><b>${esc(tc.name)}</b> · ${esc(tc.summary)}</span>
          </div>`).join('')}</div>`
      : '';
    const contentBlock = st.content
      ? `<div class="anti-content">${renderMarkdown(st.content)}</div>`
      : '';
    return `
      <div class="anti-msg-agent">
        <div class="anti-agent-head">
          <b>🤖 ${esc(agName)}</b>
          <span>${esc(timeStr)}</span>
        </div>
        ${thinkBlock}
        ${toolsBlock}
        ${contentBlock}
      </div>`;
  }).join('');

  log.scrollTop = log.scrollHeight;
}

function renderPerms() {
  const list = state.permissions.filter(p => p.agentId === selectedId);
  $('#perms').innerHTML = list.map(p => `
    <div class="perm"><b>Xin quyền: ${esc(p.tool)}</b>
      <pre>${esc(JSON.stringify(p.input, null, 2).slice(0, 1500))}</pre>
      <button class="btn small primary" data-perm="${p.id}" data-allow="1">Cho phép</button>
      <button class="btn small danger" data-perm="${p.id}" data-allow="0">Từ chối</button>
    </div>`).join('');
}
$('#perms').addEventListener('click', async e => {
  const b = e.target.closest('[data-perm]'); if (!b) return;
  b.disabled = true;
  await api(`/permissions/${b.dataset.perm}`, 'POST', { allow: b.dataset.allow === '1' }).catch(err => toast(err.message));
});

const panelTray = makeTray({ list: $('#p-atts'), input: $('#p-input'), dropZone: $('#composer'), fileInput: $('#p-file'), button: $('#p-attach') });

async function sendTask() {
  const prompt = $('#p-input').value.trim();
  const targetAgent = $('#p-target-agent')?.value || selectedId || 'mama';
  if (!prompt && !panelTray.count()) return;
  if (panelTray.busy()) return toast('Đợi tải tệp lên xong rồi gửi nhé');

  $('#p-send').disabled = true;
  try {
    let convId = state.activeConvId;
    if (!convId) {
      const created = await api('/conversations', 'POST', { agentId: targetAgent, title: prompt.slice(0, 60) });
      state.conversations.unshift(created);
      convId = created.id;
      state.activeConvId = convId;
    }
    $('#p-input').value = '';
    const attIds = panelTray.ids();
    panelTray.clear();

    const res = await api(`/conversations/${encodeURIComponent(convId)}/messages`, 'POST', {
      agentId: targetAgent,
      prompt,
      attachments: attIds,
    });
    if (res.conv) {
      state.activeConvDetail = res.conv;
      renderChatStream();
    }
    await loadState();
  } catch (err) {
    toast(err.message);
  } finally {
    $('#p-send').disabled = false;
  }
}

$('#p-send').onclick = sendTask;
$('#p-input').addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendTask();
  }
});
$('#p-close').onclick = closePanel;
$('#p-focus').onclick = () => selectedId && office.flyTo(selectedId);
$('#p-stop').onclick = () => api(`/agents/${selectedId}/stop`, 'POST').then(r => toast(`Đã dừng${r.cancelledQueued ? `, huỷ ${r.cancelledQueued} việc chờ` : ''}`)).catch(e => toast(e.message));
$('#p-edit').onclick = () => agentForm(agentById(selectedId));

// ---------------- Modal
function openModal(html) { $('#modal-box').innerHTML = html; $('#modal').classList.add('open'); }
function closeModal() { $('#modal').classList.remove('open'); }
$('#modal').addEventListener('click', e => { if (e.target.id === 'modal' || e.target.dataset.close !== undefined) closeModal(); });
const opt = (v, cur, label = v) => `<option value="${esc(v)}" ${v === cur ? 'selected' : ''}>${esc(label)}</option>`;

function agentForm(a = {}, isEdit = !!a.id && !!agentById(a.id)) {
  openModal(`
    <h3>${isEdit ? 'Sửa nhân viên' : 'Tuyển nhân viên mới'}</h3>
    <form id="agent-form">
      <div class="row2">
        <div class="field"><label>Tên hiển thị</label><input name="name" required value="${esc(a.name)}" /></div>
        <div class="field"><label>Phòng ban</label><select name="departmentId">${state.departments.filter(d => !AMENITY.has(d.style?.shape)).map(d => opt(d.id, a.departmentId, d.name)).join('')}</select></div>
      </div>
      <div class="field"><label>Vai trò</label><input name="role" value="${esc(a.role)}" /></div>
      <div class="row2">
        <div class="field"><label>Loại nhân viên</label><select name="provider">${state.providers.map(p => opt(p, a.provider ?? 'codex', PROVIDER_LABEL[p])).join('')}</select></div>
        <div class="field"><label>Model</label><input name="model" value="${esc(a.model)}" placeholder="Gemini 4 / Inherit" /></div>
      </div>
      <div class="field"><label>Thư mục làm việc (cwd)</label><input name="cwd" value="${esc(a.cwd)}" /></div>
      <div class="field"><label>Hướng dẫn riêng (system prompt)</label><textarea name="systemPrompt">${esc(a.systemPrompt)}</textarea></div>
      <div class="modal-actions"><button type="button" class="btn" data-close>Huỷ</button><button class="btn primary">${isEdit ? 'Lưu' : 'Tuyển'}</button></div>
    </form>`);
  const form = $('#agent-form');
  form.onsubmit = async e => {
    e.preventDefault();
    const body = Object.fromEntries(new FormData(form));
    try {
      if (isEdit) await api(`/agents/${a.id}`, 'PATCH', body);
      else await api('/agents', 'POST', body);
      closeModal();
      await loadState();
    } catch (err) { toast(err.message); }
  };
}

// Giao brief nhanh
$('#btn-brief').onclick = () => {
  const lead = agentById(selectedId) ?? state.agents[0];
  if (!lead) return;
  openModal(`
    <h3>Giao brief nhanh (Tự động xếp hàng đợi nếu Agent đang bận)</h3>
    <form id="brief-form">
      <div class="field"><label>Nhân sự 3D nhận việc</label><select name="to">${state.agents.map(a => `<option value="${a.id}" ${a.id === lead.id ? 'selected' : ''}>${esc(a.name)} — ${a.status === 'working' ? `Đang làm (${a.progressPct || 35}%)` : 'Sẵn sàng'}</option>`).join('')}</select></div>
      <div class="field brief-drop" id="brief-drop"><label>Nội dung công việc</label><textarea name="prompt" style="min-height:120px" placeholder="VD: Nghiên cứu 3 SKU mới cho Page Phòng Trọ Hết Cứu và chuyển sang Content viết kịch bản Hook 3s..."></textarea>
        <div class="drop-hint">Thả tệp vào để đính kèm</div></div>
      <div class="atts" id="brief-atts" style="margin:-4px 0 10px"></div>
      <input type="file" id="brief-file" multiple hidden />
      <div class="modal-actions"><button type="button" class="btn" id="brief-attach" style="margin-right:auto">Đính kèm tệp</button><button type="button" class="btn" data-close>Huỷ</button><button class="btn primary">Giao việc</button></div>
    </form>`);
  const f0 = $('#brief-form');
  const tray = makeTray({ list: $('#brief-atts'), input: f0.prompt, dropZone: $('#brief-drop'), fileInput: $('#brief-file'), button: $('#brief-attach') });
  f0.onsubmit = async e => {
    e.preventDefault();
    const f = e.target;
    if (tray.busy()) return toast('Đợi tải tệp lên xong rồi giao nhé');
    try {
      const targetId = f.to.value;
      let convId = state.activeConvId;
      if (!convId) {
        const c = await api('/conversations', 'POST', { agentId: targetId, title: f.prompt.value.slice(0, 60) });
        convId = c.id;
        state.activeConvId = convId;
      }
      await api(`/conversations/${encodeURIComponent(convId)}/messages`, 'POST', {
        agentId: targetId,
        prompt: f.prompt.value,
        attachments: tray.ids(),
      });
      closeModal();
      await onPickAgent3D(targetId);
    } catch (err) { toast(err.message); }
  };
};

// Sửa bố cục phòng ban
$('#btn-depts').onclick = () => {
  const list = state.departments;
  openModal(`
    <h3>Phòng ban 3D</h3>
    <form id="dept-form">
      <div class="field"><label>Chọn phòng</label><select name="id">${list.map(d => opt(d.id, list[0]?.id, d.name)).join('')}${opt('__new', '', '+ Thêm phòng mới')}</select></div>
      <div id="dept-fields"></div>
      <div class="modal-actions"><button type="button" class="btn" data-close>Đóng</button><button class="btn primary">Lưu</button></div>
    </form>`);
  const form = $('#dept-form');
  const fill = () => {
    const d = deptById(form.id.value) ?? { id: '', name: '', color: '#10b981', x: 0, z: 9, w: 6, d: 4, style: { shape: 'zone', screenTheme: 'docs' } };
    const st = d.style ?? {};
    $('#dept-fields').innerHTML = `
      ${form.id.value === '__new' ? `<div class="field"><label>Mã (không dấu)</label><input name="newId" required pattern="[a-z0-9-]+" /></div>` : ''}
      <div class="row2">
        <div class="field"><label>Tên</label><input name="name" required value="${esc(d.name)}" /></div>
        <div class="field"><label>Chữ trên sàn</label><input name="label" value="${esc(st.label ?? '')}" placeholder="${esc(d.name)}" /></div>
      </div>
      <div class="row2">
        <div class="field"><label>Kiểu khu vực</label><select name="shape">${Object.entries(SHAPES).map(([k, v]) => opt(k, st.shape ?? 'zone', v)).join('')}</select></div>
        <div class="field"><label>Màn hình hiển thị</label><select name="screenTheme">${Object.entries(THEMES).map(([k, v]) => opt(k, st.screenTheme ?? 'docs', v)).join('')}</select></div>
      </div>
      <div class="row4">
        <div class="field"><label>Tâm x</label><input name="x" type="number" step="0.1" value="${d.x}" /></div>
        <div class="field"><label>Tâm z</label><input name="z" type="number" step="0.1" value="${d.z}" /></div>
        <div class="field"><label>Rộng</label><input name="w" type="number" step="0.1" min="2" value="${d.w}" /></div>
        <div class="field"><label>Sâu</label><input name="d" type="number" step="0.1" min="2" value="${d.d}" /></div>
      </div>
      <div class="field"><label>Màu thảm</label><input name="color" type="color" value="${esc(d.color)}" /></div>`;
  };
  form.id.onchange = fill; fill();
  form.onsubmit = async e => {
    e.preventDefault();
    const f = Object.fromEntries(new FormData(form));
    const id = f.id === '__new' ? f.newId : f.id;
    const prev = deptById(id)?.style ?? {};
    const body = { id, name: f.name, color: f.color, x: +f.x, z: +f.z, w: +f.w, d: +f.d, style: { ...prev, shape: f.shape, screenTheme: f.screenTheme, label: f.label || undefined, seed: prev.seed ?? Math.floor(Math.random() * 1000) } };
    try { await api('/departments', 'POST', body); toast('Đã lưu phòng ban'); closeModal(); }
    catch (err) { toast(err.message); }
  };
};

// ---------------- Dữ liệu & WebSocket Real-time
async function loadState() {
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
}

function connect() {
  const ws = new WebSocket(`${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}/ws?token=${TOKEN}`);
  ws.onopen = () => loadState().then(() => { $('#loading').classList.add('done'); }).catch(e => toast(e.message));
  ws.onmessage = (m) => {
    const { type, payload } = JSON.parse(m.data);
    if (type === 'status') {
      const a = agentById(payload.agentId);
      if (a) {
        a.status = payload.status;
        if (payload.pct !== undefined) a.progressPct = payload.pct;
        if (payload.activityText) a.activityText = payload.activityText;
        if (payload.queued !== undefined) a.queued = payload.queued;
        office.setAgentProgress(a.id, { pct: a.progressPct, activityText: a.activityText, queued: a.queued, status: a.status });
        renderHud();
        renderConversationSidebar();
        renderPanelHeaderAndQueue();
      }
      clearTimeout(connect._t);
      connect._t = setTimeout(() => loadState().catch(() => {}), 350);
    } else if (type === 'progress') {
      const a = agentById(payload.agentId);
      if (a) {
        a.progressPct = payload.pct;
        a.activityText = payload.activityText;
        office.setAgentProgress(a.id, { pct: payload.pct, activityText: payload.activityText, status: payload.status });
        renderHud();
        renderConversationSidebar();
        renderPanelHeaderAndQueue();
      }
    } else if (type === 'collab') {
      office.courier(payload.fromId, payload.toId, payload.topic || '', payload.kind || 'delegate');
      const va = office.agents.get(payload.fromId), vb = office.agents.get(payload.toId);
      if (va && vb && !va.person.trip && va.where === 'home') {
        office.walkToColleague(va, vb, `💬 ${payload.topic || 'Trao đổi công việc'}`, `💬 Đã nhận thông tin!`);
      }
    } else if (type === 'event') {
      if (['task', 'result', 'error', 'permission'].includes(payload.kind)) {
        state.feed.push(payload);
        state.feed = state.feed.slice(-30);
        renderFeed();
      }
      if (payload.kind === 'task' && payload.data?.fromAgentId) {
        office.courier(payload.data.fromAgentId, payload.agentId, payload.text.slice(0, 42), 'delegate');
      }
    } else if (type === 'conversations-changed') {
      api('/conversations').then(res => {
        const list = res.conversations || res;
        state.conversations = list;
        renderConversationSidebar();
        if (state.activeConvId) {
          api(`/conversations/${encodeURIComponent(state.activeConvId)}`).then(d => {
            state.activeConvDetail = d;
            renderChatStream();
            renderPanelHeaderAndQueue();
          }).catch(() => {});
        }
      }).catch(() => {});
    } else if (type === 'permission') {
      state.permissions.push(payload);
      if (payload.agentId === selectedId) renderPerms();
      const a = agentById(payload.agentId);
      toast(`${a?.name ?? payload.agentId} xin quyền dùng ${payload.tool}`);
    } else if (type === 'permission-resolved') {
      state.permissions = state.permissions.filter(p => p.id !== payload.id);
      renderPerms();
    } else if (type === 'changed') {
      loadState().catch(() => {});
    }
  };
  ws.onclose = () => {
    $('#hud-title').textContent = 'Đang kết nối lại máy chủ 3D…';
    setTimeout(connect, 1800);
  };
}

// Tự động đồng bộ danh sách cuộc trò chuyện Antigravity IDE mỗi 5 giây
setInterval(() => {
  if (document.hidden) return;
  api('/conversations').then(res => {
    const list = res.conversations || res;
    const oldSig = state.conversations.map(c => `${c.id}:${c.stepCount}:${c.updatedAt}`).join('|');
    const newSig = list.map(c => `${c.id}:${c.stepCount}:${c.updatedAt}`).join('|');
    if (oldSig !== newSig) {
      state.conversations = list;
      renderConversationSidebar();
      if (state.activeConvId) {
        api(`/conversations/${encodeURIComponent(state.activeConvId)}`).then(d => {
          state.activeConvDetail = d;
          renderChatStream();
        }).catch(() => {});
      }
    }
  }).catch(() => {});
}, 5000);

await Promise.all([
  document.fonts.load('600 64px "Be Vietnam Pro"'),
  document.fonts.load('400 14px "Be Vietnam Pro"'),
]).catch(() => {});

// ============================================================================
// ĐIỀU KHIỂN 3D NỔI: CẦM NẮM KÉO SÀN, KÉO ĐỔI CHỖ PHÒNG BAN, ZOOM & XOAY 360°
// ============================================================================
$('#mode-orbit').onclick = () => {
  office.setNavMode('orbit');
  toast('🔄 Chế độ Xoay 360°: Kéo chuột trái để xoay 360°, chuột phải để kéo sàn.');
};
$('#mode-pan').onclick = () => {
  office.setNavMode('pan');
  toast('✋ Chế độ Cầm Nắm Kéo Sàn: Kéo chuột trái để cầm nắm dịch chuyển toàn bộ mặt sàn.');
};
$('#mode-dept').onclick = () => {
  const next = office.navMode === 'move_dept' ? 'orbit' : 'move_dept';
  office.setNavMode(next);
  if (next === 'move_dept') {
    toast('🏗️ Chế độ Kéo Phòng Ban: Bấm giữ chuột trái vào thảm phòng ban bất kỳ và kéo sang vị trí mới!');
  }
};
$('#btn-spin360').onclick = () => {
  const on = office.toggleAutoRotate360();
  toast(on ? '🎡 Đang tự động xoay 360° quanh vị trí hiện tại!' : '⏹ Đã dừng tự động xoay 360°.');
};
$('#btn-eye360').onclick = () => {
  office.eyeLevelView();
  toast('👁️ Đã hạ góc nhìn ngang tầm mắt — kéo chuột để ngắm 360° quanh phòng!');
};
$('#btn-zoom-in').onclick = () => {
  office.zoomBy(0.76);
  setTimeout(syncZoomSlider, 380);
};
$('#btn-zoom-out').onclick = () => {
  office.zoomBy(1.28);
  setTimeout(syncZoomSlider, 380);
};
const zoomSlider = $('#zoom-slider');
function syncZoomSlider() {
  if (!zoomSlider || !office.camera) return;
  const d = Math.round(office.getZoomDistance());
  // Đảo chiều thanh trượt: kéo sang phải (giá trị cao) = phóng to (khoảng cách gần)
  zoomSlider.value = String(Math.max(2, Math.min(75, 77 - d)));
}
if (zoomSlider) {
  zoomSlider.addEventListener('input', () => {
    const val = Number(zoomSlider.value);
    const targetDist = Math.max(1.5, 77 - val);
    office.setZoomDistance(targetDist);
  });
}
setInterval(syncZoomSlider, 800);

// ============================================================================
// TÙY CHỈNH KÉO DÃN KHUNG CHAT 8 HƯỚNG, KÉO VỊ TRÍ & CO GIÃN CỘT CUỘC TRÒ CHUYỆN
// ============================================================================
(function initResizableDraggableChat() {
  const panel = $('#panel');
  const sidebar = $('#conv-sidebar');
  const splitter = $('#conv-splitter');
  const header = $('#chat-header');
  if (!panel) return;

  // Khôi phục kích thước đã lưu
  try {
    const saved = JSON.parse(localStorage.getItem('office.chatRect') || 'null');
    if (saved) {
      if (saved.w) panel.style.width = `${ Math.min(window.innerWidth - 20, Math.max(420, saved.w)) }px`;
      if (saved.h) {
        panel.style.height = `${ Math.min(window.innerHeight - 20, Math.max(340, saved.h)) }px`;
        panel.style.bottom = 'auto';
      }
      if (saved.sidebarW && sidebar) {
        sidebar.style.width = `${ Math.min(440, Math.max(175, saved.sidebarW)) }px`;
        sidebar.style.minWidth = sidebar.style.width;
      }
    }
  } catch {}

  const saveRect = () => {
    try {
      const r = panel.getBoundingClientRect();
      const sw = sidebar ? sidebar.getBoundingClientRect().width : 245;
      localStorage.setItem('office.chatRect', JSON.stringify({ w: Math.round(r.width), h: Math.round(r.height), sidebarW: Math.round(sw) }));
    } catch {}
  };


  // Chuyển đổi giao diện Chat Sáng / Tối (Light / Dark Mode)
  const themeBtn = $('#btn-chat-theme');
  const applyChatTheme = (mode) => {
    const isLight = mode === 'light';
    panel.classList.toggle('theme-light', isLight);
    if (themeBtn) themeBtn.textContent = isLight ? '🌙 Tối' : '☀️ Sáng';
    try { localStorage.setItem('office.chatTheme', mode); } catch {}
  };
  try {
    const savedTheme = localStorage.getItem('office.chatTheme') || 'dark';
    applyChatTheme(savedTheme);
  } catch {}
  themeBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    const next = panel.classList.contains('theme-light') ? 'dark' : 'light';
    applyChatTheme(next);
  });

  // Nút chọn nhanh kích thước Gọn / Vừa / Rộng
  $('#p-size-sm')?.addEventListener('click', (e) => {
    e.stopPropagation();
    panel.style.top = '58px'; panel.style.right = '12px'; panel.style.left = 'auto'; panel.style.bottom = 'auto';
    panel.style.width = '540px'; panel.style.height = '540px';
    if (sidebar) { sidebar.style.width = '195px'; sidebar.style.minWidth = '195px'; }
    saveRect();
  });
  $('#p-size-md')?.addEventListener('click', (e) => {
    e.stopPropagation();
    panel.style.top = '12px'; panel.style.right = '12px'; panel.style.left = 'auto'; panel.style.bottom = '12px';
    panel.style.width = '780px'; panel.style.height = 'auto';
    if (sidebar) { sidebar.style.width = '245px'; sidebar.style.minWidth = '245px'; }
    saveRect();
  });
  $('#p-size-lg')?.addEventListener('click', (e) => {
    e.stopPropagation();
    panel.style.top = '10px'; panel.style.right = '10px'; panel.style.left = 'auto'; panel.style.bottom = '10px';
    panel.style.width = `${Math.round(window.innerWidth * 0.9)}px`; panel.style.height = 'auto';
    if (sidebar) { sidebar.style.width = '310px'; sidebar.style.minWidth = '310px'; }
    saveRect();
  });

  // Kéo dãn 8 hướng quanh viền khung chat
  panel.querySelectorAll('.chat-resizer').forEach(handle => {
    handle.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const dir = handle.dataset.dir || 'w';
      const startX = e.clientX;
      const startY = e.clientY;
      const rect = panel.getBoundingClientRect();
      panel.style.top = `${rect.top}px`;
      panel.style.left = `${rect.left}px`;
      panel.style.right = 'auto';
      panel.style.bottom = 'auto';
      panel.style.width = `${rect.width}px`;
      panel.style.height = `${rect.height}px`;

      const onMove = (ev) => {
        const dx = ev.clientX - startX;
        const dy = ev.clientY - startY;
        if (dir.includes('w')) {
          const nw = Math.max(420, Math.min(window.innerWidth - 20, rect.width - dx));
          const nl = rect.right - nw;
          if (nl >= 6) {
            panel.style.width = `${nw}px`;
            panel.style.left = `${nl}px`;
          }
        }
        if (dir.includes('e')) {
          const nw = Math.max(420, Math.min(window.innerWidth - rect.left - 8, rect.width + dx));
          panel.style.width = `${nw}px`;
        }
        if (dir.includes('n')) {
          const nh = Math.max(340, Math.min(window.innerHeight - 20, rect.height - dy));
          const nt = rect.bottom - nh;
          if (nt >= 6) {
            panel.style.height = `${nh}px`;
            panel.style.top = `${nt}px`;
          }
        }
        if (dir.includes('s')) {
          const nh = Math.max(340, Math.min(window.innerHeight - rect.top - 8, rect.height + dy));
          panel.style.height = `${nh}px`;
        }
      };
      const onUp = () => {
        window.removeEventListener('pointermove', onMove);
        window.removeEventListener('pointerup', onUp);
        saveRect();
      };
      window.addEventListener('pointermove', onMove);
      window.addEventListener('pointerup', onUp);
    });
  });

  // Kéo thanh tiêu đề để di chuyển vị trí khung chat trên màn hình
  if (header) {
    header.addEventListener('pointerdown', (e) => {
      if (e.target.closest('button, select, input')) return;
      const startX = e.clientX;
      const startY = e.clientY;
      const rect = panel.getBoundingClientRect();
      panel.style.left = `${rect.left}px`;
      panel.style.top = `${rect.top}px`;
      panel.style.right = 'auto';
      panel.style.bottom = 'auto';
      panel.style.width = `${rect.width}px`;
      panel.style.height = `${rect.height}px`;

      const onMove = (ev) => {
        const nl = Math.max(6, Math.min(window.innerWidth - rect.width - 6, rect.left + (ev.clientX - startX)));
        const nt = Math.max(6, Math.min(window.innerHeight - 80, rect.top + (ev.clientY - startY)));
        panel.style.left = `${nl}px`;
        panel.style.top = `${nt}px`;
      };
      const onUp = () => {
        window.removeEventListener('pointermove', onMove);
        window.removeEventListener('pointerup', onUp);
      };
      window.addEventListener('pointermove', onMove);
      window.addEventListener('pointerup', onUp);
    });
  }

  // Kéo vách ngăn giữa cột Cuộc Trò Chuyện và cột Chat Chính
  if (splitter && sidebar) {
    splitter.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      splitter.classList.add('dragging');
      const startX = e.clientX;
      const startW = sidebar.getBoundingClientRect().width;
      const onMove = (ev) => {
        const nw = Math.max(170, Math.min(460, startW + (ev.clientX - startX)));
        sidebar.style.width = `${nw}px`;
        sidebar.style.minWidth = `${nw}px`;
      };
      const onUp = () => {
        splitter.classList.remove('dragging');
        window.removeEventListener('pointermove', onMove);
        window.removeEventListener('pointerup', onUp);
        saveRect();
      };
      window.addEventListener('pointermove', onMove);
      window.addEventListener('pointerup', onUp);
    });
  }
})();

await office.init();
renderQuality();
window.__office = office;
connect();
