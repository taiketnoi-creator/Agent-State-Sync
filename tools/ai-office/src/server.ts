// HTTP + WebSocket server cho văn phòng ảo 3D Agent-Javis (Đồng bộ Antigravity IDE)
import './log.ts';
import 'dotenv/config';
import express, { type Request, type Response, type NextFunction } from 'express';
import { createServer } from 'node:http';
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { randomBytes } from 'node:crypto';
import { WebSocketServer, type WebSocket } from 'ws';
import { Office, PROVIDERS } from './office.ts';
import { repo } from './db.ts';
import { discoverSessions } from './observer.ts';
import { pricing } from './pricing.ts';
import { saveUpload, getUpload, isImage, MAX_UPLOAD } from './attachments.ts';
import {
  listAllConversations,
  getConversationDetail,
  createOfficeConversation,
  deleteConversation,
} from './antigravityBridge.ts';
import type { Department } from './types.ts';

const PORT = Number(process.env.PORT ?? 4800);
const HOST = process.env.HOST ?? '127.0.0.1';
const TOKEN = process.env.OFFICE_TOKEN || randomBytes(16).toString('hex');
const ALLOWED_HOSTS = new Set([`localhost:${PORT}`, `127.0.0.1:${PORT}`, `[::1]:${PORT}`, ...(process.env.ALLOWED_HOSTS?.split(',') ?? [])]);
const WORKSPACE_ROOT = resolve(process.cwd(), '../..').replace(/\\/g, '/');

const resolveAgentCwd = (rawCwd?: string | null) => {
  if (!rawCwd || rawCwd === '../..' || !existsSync(rawCwd)) return WORKSPACE_ROOT;
  return rawCwd;
};

// ---------- Seed & đồng bộ phòng ban / nhân viên chuẩn Agent-Javis
const office = new Office();
if (existsSync('office.config.json')) {
  const cfg = JSON.parse(readFileSync('office.config.json', 'utf8')) as { departments: Department[]; agents?: any[] };
  const existingDepts = repo.listDepartments();
  if (existingDepts.length === 0) {
    cfg.departments.forEach(d => repo.upsertDepartment(d));
    for (const a of cfg.agents ?? []) office.createAgent({ ...a, cwd: resolveAgentCwd(a.cwd) });
    console.log(`Đã tạo ${cfg.departments.length} phòng ban, ${cfg.agents?.length ?? 0} nhân viên Agent-Javis`);
  } else {
    for (const d of cfg.departments) {
      repo.upsertDepartment(d);
    }
    const existingAgents = repo.listAgents();
    let added = 0, updated = 0;
    for (const a of cfg.agents ?? []) {
      const targetCwd = resolveAgentCwd(a.cwd);
      const cur = existingAgents.find(x => x.id === a.id);
      if (!cur) {
        office.createAgent({ ...a, cwd: targetCwd });
        added++;
      } else if (cur.role !== a.role || cur.systemPrompt !== a.systemPrompt || cur.departmentId !== a.departmentId || cur.cwd !== targetCwd || cur.name !== a.name) {
        office.updateAgent(a.id, {
          name: a.name,
          role: a.role,
          departmentId: a.departmentId,
          systemPrompt: a.systemPrompt,
          cwd: targetCwd,
        });
        updated++;
      }
    }
    if (added || updated) console.log(`Đã đồng bộ cấu hình Agent-Javis: +${added} nhân sự mới, cập nhật ${updated} nhân sự`);
  }
}

const app = express();
app.use(express.json({ limit: '2mb' }));

const hostGuard = (req: Request, res: Response, next: NextFunction) => {
  if (!ALLOWED_HOSTS.has(req.headers.host ?? '')) return res.status(403).send('Host không được phép');
  next();
};
app.use(hostGuard);

const indexHtml = () => readFileSync('public/index.html', 'utf8').replace('__OFFICE_TOKEN__', TOKEN);
app.get('/', (_req, res) => res.type('html').send(indexHtml()));
app.get('/models/manifest.json', (_req, res, next) => existsSync('public/models/manifest.json') ? next() : res.json({}));
app.use(express.static('public', { index: false }));
app.use('/vendor/three', express.static('node_modules/three'));
app.use('/vendor/fonts', express.static('node_modules/@fontsource'));

app.get('/files/:id/:name', (req, res) => {
  if (req.query.t !== TOKEN) return res.status(401).send('Sai token');
  const a = getUpload(String(req.params.id));
  if (!a) return res.status(404).send('Không còn tệp này');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Content-Security-Policy', 'sandbox');
  res.type(isImage(a) ? a.mime : 'application/octet-stream');
  res.setHeader('Content-Disposition', `${isImage(a) ? 'inline' : 'attachment'}; filename*=UTF-8''${encodeURIComponent(a.name)}`);
  res.sendFile(a.path);
});

const api = express.Router();
api.use((req, res, next) => {
  if (req.headers['x-office-token'] !== TOKEN) return res.status(401).json({ error: 'Sai token' });
  next();
});
const wrap = (fn: (req: Request, res: Response) => unknown) => (req: Request, res: Response) => {
  try { const r = fn(req, res); if (r !== undefined && !res.headersSent) res.json(r); }
  catch (e: any) { res.status(400).json({ error: e.message }); }
};
const id = (req: Request) => String(req.params.id);

api.get('/state', wrap(() => ({
  ...office.snapshot(),
  providers: PROVIDERS,
  conversations: listAllConversations(25),
})));

// ---- Quản lý Đa Cuộc Trò Chuyện chuẩn Antigravity IDE
api.get('/conversations', wrap(() => listAllConversations(30)));
api.get('/conversations/:id', wrap(req => {
  const c = getConversationDetail(id(req));
  if (!c) throw new Error('Không tìm thấy cuộc trò chuyện');
  return c;
}));
api.post('/conversations', wrap(req => {
  const agentId = String(req.body.agentId || 'mama');
  const agent = repo.getAgent(agentId);
  const conv = createOfficeConversation({
    title: req.body.title,
    agentId,
    agentName: agent?.name || 'Mama (Chief of Staff)',
  });
  broadcast('conversations-changed', null);
  return conv;
}));
api.delete('/conversations/:id', wrap(req => {
  deleteConversation(id(req));
  broadcast('conversations-changed', null);
  return { ok: true };
}));
api.post('/conversations/:id/messages', wrap(req => {
  const convId = id(req);
  const targetAgentId = String(req.body.agentId || 'mama');
  const prompt = String(req.body.prompt || '');
  const ids: unknown[] = Array.isArray(req.body.attachments) ? req.body.attachments : [];
  const atts = ids.map(x => getUpload(String(x)));
  if (atts.some(a => !a)) throw new Error('Có tệp đính kèm không còn trên máy, hãy đính kèm lại');
  const task = office.assignTask(targetAgentId, prompt, undefined, undefined, atts as any, convId);
  broadcast('conversations-changed', { convId });
  return { task, conv: getConversationDetail(convId) };
}));

// ---- Quản lý Nhân viên & Hàng đợi Task
api.post('/agents', wrap(req => office.createAgent(req.body)));
api.patch('/agents/:id', wrap(req => office.updateAgent(id(req), req.body)));
api.delete('/agents/:id', wrap(req => { office.deleteAgent(id(req)); return { ok: true }; }));
api.get('/agents/:id/events', wrap(req => repo.listEvents(id(req), Number(req.query.limit ?? 200))));
api.get('/agents/:id/tasks', wrap(req => repo.listTasks(id(req))));
api.post('/agents/:id/tasks', wrap(req => {
  const ids: unknown[] = Array.isArray(req.body.attachments) ? req.body.attachments : [];
  const atts = ids.map(x => getUpload(String(x)));
  if (atts.some(a => !a)) throw new Error('Có tệp đính kèm không còn trên máy, hãy đính kèm lại');
  const convId = req.body.convId ? String(req.body.convId) : undefined;
  return office.assignTask(id(req), String(req.body.prompt ?? ''), undefined, undefined, atts as any, convId);
}));

api.delete('/queue/:id', wrap(req => ({ ok: office.cancelSingleQueuedTask(id(req)) })));
api.post('/queue/:id/promote', wrap(req => ({ ok: office.promoteQueuedTask(id(req)) })));

api.post('/collab-wave', wrap(req => {
  const topic = String(req.body?.topic || 'Đồng bộ Chiến dịch 4 Page & Kiểm duyệt Luật #10');
  const chain: Array<[string, string, string, 'delegate' | 'audit' | 'report']> = [
    ['mama', 'mkt', `Săn SKU Whitelist: ${topic.slice(0, 28)}`, 'delegate'],
    ['mama', 'content', 'Soạn kịch bản Hook 3s & Caption A/B', 'delegate'],
    ['mama', 'edit', 'Render Ảnh Zero-Clone 1:1 & Bespoke Reel', 'delegate'],
    ['mama', 'edit-2', 'Chuẩn bị TVC 8 Nhịp Sandwich A-Roll/B-Roll', 'delegate'],
    ['edit', 'bo-nao-thu-2', 'Kiểm duyệt chống trùng lặp (Luật #10)', 'audit'],
    ['bo-nao-thu-2', 'mama', 'APPROVED_BY_SECOND_BRAIN ✓', 'report'],
  ];
  chain.forEach(([from, to, msg, kind], idx) => {
    setTimeout(() => office.emitCollab(from, to, msg, kind), idx * 650);
  });
  return { ok: true, count: chain.length };
}));

api.post('/uploads', express.raw({ type: () => true, limit: MAX_UPLOAD }), wrap(req => {
  const name = decodeURIComponent(String(req.headers['x-filename'] ?? 'tep'));
  const a = saveUpload(name, String(req.headers['x-mime'] ?? ''), req.body as Buffer);
  return { id: a.id, name: a.name, mime: a.mime, size: a.size };
}));
api.post('/agents/:id/stop', wrap(req => { office.stopAgent(id(req)); return { cancelledQueued: office.cancelQueued(id(req)) }; }));
api.post('/agents/:id/reset', wrap(req => { office.resetSession(id(req)); return { ok: true }; }));
api.post('/departments', wrap(req => { office.upsertDepartment(req.body); return { ok: true }; }));
api.post('/permissions/:id', wrap(req => ({ ok: office.resolvePermission(id(req), !!req.body.allow) })));
api.get('/tasks', wrap(() => repo.listTasks(undefined, 100)));
api.get('/discover', wrap(() => discoverSessions(40)));

api.get('/usage', wrap(req => {
  const range = String(req.query.range ?? 'today');
  const start = new Date(); start.setHours(0, 0, 0, 0);
  const since = range === 'all' ? 0 : range === '30d' ? start.getTime() - 29 * 864e5 : range === '7d' ? start.getTime() - 6 * 864e5 : start.getTime();
  const rows = repo.usageSummary(since);
  const agents: Record<string, any> = {};
  for (const r of rows) {
    const a = agents[r.agentId] ??= { agentId: r.agentId, provider: r.provider, input: 0, output: 0, cacheRead: 0, cacheWrite: 0, costUsd: 0, unpriced: 0, reported: 0, tasks: 0, models: [] };
    for (const k of ['input', 'output', 'cacheRead', 'cacheWrite', 'costUsd', 'unpriced', 'reported', 'tasks'] as const) a[k] += r[k] ?? 0;
    a.models.push(r);
  }
  const list = Object.values(agents).sort((x: any, y: any) => y.costUsd - x.costUsd || (y.input + y.output) - (x.input + x.output));
  const total = list.reduce((t: any, a: any) => { for (const k of ['input', 'output', 'cacheRead', 'cacheWrite', 'costUsd', 'unpriced', 'tasks']) t[k] += a[k]; return t; },
    { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, costUsd: 0, unpriced: 0, tasks: 0 });
  return { range, since, agents: list, total, byDay: repo.usageByDay(since), usdToVnd: pricing().usdToVnd ?? null };
}));
app.use('/api', api);

// ---------- WebSocket: đẩy sự kiện real-time cho UI
const server = createServer(app);
const wss = new WebSocketServer({ noServer: true });
server.on('upgrade', (req, socket, head) => {
  const url = new URL(req.url ?? '/', 'http://x');
  if (url.pathname !== '/ws' || url.searchParams.get('token') !== TOKEN || !ALLOWED_HOSTS.has(req.headers.host ?? '')) {
    socket.destroy();
    return;
  }
  wss.handleUpgrade(req, socket, head, ws => wss.emit('connection', ws, req));
});

const broadcast = (type: string, payload: unknown) => {
  const msg = JSON.stringify({ type, payload });
  wss.clients.forEach((c: WebSocket) => { if (c.readyState === 1) c.send(msg); });
};
office.on('event', ev => broadcast('event', ev));
office.on('status', s => broadcast('status', s));
office.on('progress', p => broadcast('progress', p));
office.on('collab', c => broadcast('collab', c));
office.on('permission', p => broadcast('permission', p));
office.on('permission-resolved', p => broadcast('permission-resolved', p));
office.on('usage', u => broadcast('usage', u));
let changedTimer: NodeJS.Timeout | undefined;
office.on('changed', () => {
  clearTimeout(changedTimer);
  changedTimer = setTimeout(() => {
    broadcast('changed', null);
    broadcast('conversations-changed', null);
  }, 100);
});

server.on('error', (e: NodeJS.ErrnoException) => {
  if (e.code === 'EADDRINUSE') {
    console.error(`\nCổng ${PORT} đang được dùng: văn phòng có lẽ đã chạy sẵn ở một cửa sổ khác → mở http://localhost:${PORT}.`);
    process.exit(3);
  }
  console.error('[server]', e);
  process.exit(1);
});
let lastConvSignature = '';
setInterval(() => {
  if (wss.clients.size === 0) return;
  try {
    const convs = listAllConversations(10);
    const sig = convs.map(c => `${c.id}:${c.stepCount}:${c.updatedAt}:${c.currentActivity}`).join('|');
    if (lastConvSignature && sig !== lastConvSignature) {
      broadcast('conversations-changed', null);
    }
    lastConvSignature = sig;
  } catch {}
}, 1200).unref();

server.listen(PORT, () => {
  console.log(`\n🏢 Văn phòng ảo 3D Agent-Javis: http://localhost:${PORT}`);
});

process.on('SIGINT', () => { console.log('\nĐóng văn phòng…'); process.exit(0); });
