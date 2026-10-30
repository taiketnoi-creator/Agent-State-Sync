// Cầu nối đồng bộ trực tiếp các cuộc trò chuyện thật của Antigravity (~/.gemini/antigravity/brain)
// + Quản lý đa cuộc trò chuyện (thêm, xóa, chuyển đổi, xem Thinking & Tool Calls giống hệt Antigravity IDE)
import { existsSync, readdirSync, statSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

export interface AntiToolCall {
  id: string;
  name: string;
  summary: string;
  status: 'done' | 'running';
}

export interface AntiStep {
  index: number;
  role: 'user' | 'assistant' | 'system';
  createdAt: string;
  content: string;
  thinking?: string;
  toolCalls?: AntiToolCall[];
  agentId?: string;
  agentName?: string;
}

export interface AntiConversation {
  id: string;
  title: string;
  subtitle: string;
  currentActivity: string;
  status: 'working' | 'idle' | 'queued';
  progressPct: number;
  agentId: string;
  agentName: string;
  source: 'antigravity-ide' | 'office-3d';
  updatedAt: number;
  stepCount: number;
  steps?: AntiStep[];
}

const BRAIN_DIR = join(homedir(), '.gemini', 'antigravity', 'brain');
const STATE_FILE = 'data/conversations_state.json';

interface LocalConvState {
  deletedIds: string[];
  customConversations: AntiConversation[];
  customSteps: Record<string, AntiStep[]>;
  titleOverrides: Record<string, string>;
}

function loadState(): LocalConvState {
  mkdirSync('data', { recursive: true });
  if (!existsSync(STATE_FILE)) {
    return { deletedIds: [], customConversations: [], customSteps: {}, titleOverrides: {} };
  }
  try {
    const raw = JSON.parse(readFileSync(STATE_FILE, 'utf8'));
    return {
      deletedIds: Array.isArray(raw.deletedIds) ? raw.deletedIds : [],
      customConversations: Array.isArray(raw.customConversations) ? raw.customConversations : [],
      customSteps: raw.customSteps && typeof raw.customSteps === 'object' ? raw.customSteps : {},
      titleOverrides: raw.titleOverrides && typeof raw.titleOverrides === 'object' ? raw.titleOverrides : {},
    };
  } catch {
    return { deletedIds: [], customConversations: [], customSteps: {}, titleOverrides: {} };
  }
}

function saveState(st: LocalConvState) {
  mkdirSync('data', { recursive: true });
  writeFileSync(STATE_FILE, JSON.stringify(st, null, 2), 'utf8');
}

function cleanUserText(raw: string): string {
  if (!raw) return '';
  let s = raw;
  s = s.replace(/<ADDITIONAL_METADATA>[\s\S]*?<\/ADDITIONAL_METADATA>/g, '');
  s = s.replace(/<USER_SETTINGS_CHANGE>[\s\S]*?<\/USER_SETTINGS_CHANGE>/g, '');
  s = s.replace(/<SYSTEM_MESSAGE>[\s\S]*?<\/SYSTEM_MESSAGE>/g, '');
  const m = s.match(/<USER_REQUEST>([\s\S]*?)<\/USER_REQUEST>/);
  if (m) s = m[1];
  s = s.replace(/<\/?USER_REQUEST>/g, '').trim();
  return s;
}

function summarizeToolCall(tc: any): AntiToolCall {
  const name = tc?.name || tc?.function?.name || 'tool';
  let args: any = tc?.args || tc?.arguments || tc?.function?.arguments || {};
  if (typeof args === 'string') {
    try { args = JSON.parse(args); } catch { args = {}; }
  }
  let summary = name;
  if (name === 'run_command') summary = args.toolSummary || `Chạy lệnh: ${(args.CommandLine || '').slice(0, 60)}`;
  else if (name === 'read_file') summary = `Đọc file: ${(args.Path || '').split(/[\\/]/).pop() || args.Path || ''}`;
  else if (name === 'write_file') summary = `Ghi file: ${(args.Path || '').split(/[\\/]/).pop() || args.Path || ''}`;
  else if (name === 'edit_file') summary = `Sửa file: ${(args.Path || '').split(/[\\/]/).pop() || args.Path || ''}`;
  else if (name === 'invoke_subagent') summary = `Gọi Subagent: ${args.TypeName || ''} (${args.Role || ''})`;
  else if (name === 'manage_task') summary = `Quản lý tiến trình: ${args.Action || ''}`;
  else if (name === 'search_web') summary = `Tìm kiếm Web: ${args.query || ''}`;
  return {
    id: tc?.id || Math.random().toString(36).slice(2, 9),
    name,
    summary,
    status: 'done',
  };
}

function detectAgentFromTranscript(steps: AntiStep[], rawHead: string): { id: string; name: string } {
  const joined = (rawHead + ' ' + steps.map(s => s.content).join(' ')).toLowerCase();
  if (joined.includes('báo cáo điểm danh — bộ não thứ 2') || joined.includes('bo-nao-thu-2')) {
    if (!joined.includes('báo cáo khởi động phiên của mama')) return { id: 'bo-nao-thu-2', name: 'Bộ Não Thứ 2' };
  }
  if (joined.includes('đã hoàn tất đọc [edit-2.md]')) return { id: 'edit-2', name: 'Edit-2 (Video Bán Hàng)' };
  if (joined.includes('editorial macro & 3-detail grid') && !joined.includes('mama')) return { id: 'edit', name: 'Edit (Đồ Họa)' };
  return { id: 'mama', name: 'Mama (Chief of Staff)' };
}

export function parseAntigravityTranscript(convId: string, fullSteps = false): AntiConversation | null {
  const logPath = join(BRAIN_DIR, convId, '.system_generated', 'logs', 'transcript.jsonl');
  if (!existsSync(logPath)) return null;
  let st: ReturnType<typeof statSync>;
  try { st = statSync(logPath); } catch { return null; }

  let raw = '';
  try { raw = readFileSync(logPath, 'utf8'); } catch { return null; }
  const lines = raw.split('\n').filter(l => l.trim().length > 0);
  if (!lines.length) return null;

  const steps: AntiStep[] = [];
  let firstUserPrompt = '';
  let lastActivity = 'Sẵn sàng';
  let lastRole: 'user' | 'assistant' | 'tool' = 'assistant';

  for (let i = 0; i < lines.length; i++) {
    let obj: any;
    try { obj = JSON.parse(lines[i]); } catch { continue; }
    const type = obj.type || '';
    const createdAt = obj.created_at || new Date(st.mtimeMs).toISOString();

    if (type === 'USER_INPUT') {
      const text = cleanUserText(obj.content || '');
      if (!text) continue;
      if (!firstUserPrompt) firstUserPrompt = text;
      lastActivity = `CEO: ${text.slice(0, 75)}`;
      lastRole = 'user';
      steps.push({
        index: steps.length,
        role: 'user',
        createdAt,
        content: text,
      });
    } else if (type === 'PLANNER_RESPONSE') {
      const content = (obj.content || '').trim();
      const thinking = (obj.thinking || '').trim();
      const rawCalls = Array.isArray(obj.tool_calls) ? obj.tool_calls : [];
      const toolCalls = rawCalls.map(summarizeToolCall);

      if (toolCalls.length > 0) {
        lastActivity = `🔧 ${toolCalls[toolCalls.length - 1].summary}`;
        lastRole = 'tool';
      }
      if (content) {
        lastActivity = content.replace(/[#*`>-]/g, '').trim().slice(0, 85);
        lastRole = 'assistant';
      } else if (thinking && !toolCalls.length) {
        lastActivity = `💭 Đang suy nghĩ: ${thinking.slice(0, 70)}...`;
      }

      if (content || thinking || toolCalls.length > 0) {
        steps.push({
          index: steps.length,
          role: 'assistant',
          createdAt,
          content,
          thinking: thinking || undefined,
          toolCalls: toolCalls.length ? toolCalls : undefined,
        });
      }
    }
  }

  if (!steps.length) return null;
  const agentInfo = detectAgentFromTranscript(steps, raw.slice(0, 2000));
  const isRecentWorking = (Date.now() - st.mtimeMs < 15000) && lastRole !== 'assistant';
  const state = loadState();
  const customExtraSteps = state.customSteps[convId] ?? [];
  const allSteps = [...steps, ...customExtraSteps];

  const rawTitle = state.titleOverrides[convId] || firstUserPrompt || `${agentInfo.name} · Phiên ${convId.slice(0, 6)}`;
  const title = rawTitle.replace(/\s+/g, ' ').slice(0, 68) + (rawTitle.length > 68 ? '…' : '');

  return {
    id: convId,
    title,
    subtitle: `${agentInfo.name} · ${allSteps.length} bước`,
    currentActivity: customExtraSteps.length
      ? customExtraSteps[customExtraSteps.length - 1].content.slice(0, 85)
      : lastActivity,
    status: isRecentWorking ? 'working' : 'idle',
    progressPct: isRecentWorking ? Math.min(95, 35 + (allSteps.length * 7) % 55) : 100,
    agentId: agentInfo.id,
    agentName: agentInfo.name,
    source: 'antigravity-ide',
    updatedAt: st.mtimeMs,
    stepCount: allSteps.length,
    steps: fullSteps ? allSteps.slice(-80) : undefined,
  };
}

export function listAllConversations(limit = 25): AntiConversation[] {
  const st = loadState();
  const deleted = new Set(st.deletedIds);
  const out: AntiConversation[] = [];

  // 1. Custom conversations created directly inside 3D Office
  for (const c of st.customConversations) {
    if (deleted.has(c.id)) continue;
    const cSteps = st.customSteps[c.id] ?? [];
    out.push({
      ...c,
      stepCount: cSteps.length,
      currentActivity: cSteps.length
        ? cSteps[cSteps.length - 1].content.replace(/[#*`]/g, '').slice(0, 85)
        : c.currentActivity,
    });
  }

  // 2. Real Antigravity IDE conversations from ~/.gemini/antigravity/brain
  if (existsSync(BRAIN_DIR)) {
    try {
      const dirs = readdirSync(BRAIN_DIR, { withFileTypes: true })
        .filter(d => d.isDirectory() && d.name !== 'tempmediaStorage' && !deleted.has(d.name));
      const sorted = dirs
        .map(d => {
          const p = join(BRAIN_DIR, d.name, '.system_generated', 'logs', 'transcript.jsonl');
          try { return { id: d.name, mtime: statSync(p).mtimeMs }; } catch { return null; }
        })
        .filter((x): x is { id: string; mtime: number } => !!x)
        .sort((a, b) => b.mtime - a.mtime)
        .slice(0, limit);

      for (const item of sorted) {
        const parsed = parseAntigravityTranscript(item.id, false);
        if (parsed) out.push(parsed);
      }
    } catch { /* ignore */ }
  }

  out.sort((a, b) => b.updatedAt - a.updatedAt);
  return out.slice(0, limit);
}

export function getConversationDetail(convId: string): AntiConversation | null {
  const st = loadState();
  if (st.deletedIds.includes(convId)) return null;
  const custom = st.customConversations.find(c => c.id === convId);
  if (custom) {
    const steps = st.customSteps[convId] ?? [];
    return { ...custom, stepCount: steps.length, steps };
  }
  return parseAntigravityTranscript(convId, true);
}

export function createOfficeConversation(input: { title?: string; agentId?: string; agentName?: string }): AntiConversation {
  const st = loadState();
  const id = 'conv-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 6);
  const agentId = input.agentId || 'mama';
  const agentName = input.agentName || 'Mama (Chief of Staff)';
  const title = (input.title || `Cuộc trò chuyện mới với ${agentName}`).trim();
  const conv: AntiConversation = {
    id,
    title,
    subtitle: `${agentName} · Văn phòng 3D`,
    currentActivity: 'Vừa khởi tạo • Sẵn sàng nhận lệnh',
    status: 'idle',
    progressPct: 0,
    agentId,
    agentName,
    source: 'office-3d',
    updatedAt: Date.now(),
    stepCount: 0,
    steps: [],
  };
  st.customConversations.unshift(conv);
  st.customSteps[id] = [
    {
      index: 0,
      role: 'assistant',
      createdAt: new Date().toISOString(),
      agentId,
      agentName,
      thinking: `Khởi tạo phiên làm việc trực tiếp cho ${agentName}. Đã nạp 10 Luật Cứng và kết nối Cổng Kiểm Duyệt Bộ Não Thứ 2 (Luật #10).`,
      content: `Xin chào CEO! Tôi là **${agentName}**. Cuộc trò chuyện này được đồng bộ trực tiếp trên Văn phòng 3D Agent-Javis.\n\nCEO có thể giao việc trực tiếp tại đây hoặc bấm vào bất kỳ nhân vật 3D nào trên mặt sàn. Nếu nhân sự đang bận, công việc mới sẽ tự động xếp vào **Hàng đợi tuần tự (Queue)** để xử lý lần lượt!`,
    },
  ];
  saveState(st);
  return { ...conv, steps: st.customSteps[id], stepCount: 1 };
}

export function appendConversationStep(convId: string, step: Omit<AntiStep, 'index' | 'createdAt'>, statusUpdate?: { status?: 'working' | 'idle' | 'queued'; pct?: number; activity?: string; titleIfNew?: string }) {
  const st = loadState();
  const list = st.customSteps[convId] ?? (st.customSteps[convId] = []);
  const fullStep: AntiStep = {
    ...step,
    index: list.length,
    createdAt: new Date().toISOString(),
  };
  list.push(fullStep);

  const custom = st.customConversations.find(c => c.id === convId);
  if (custom) {
    custom.updatedAt = Date.now();
    if (statusUpdate?.titleIfNew && custom.title.startsWith('Cuộc trò chuyện mới')) {
      custom.title = statusUpdate.titleIfNew.slice(0, 68);
    }
    if (statusUpdate?.status) custom.status = statusUpdate.status;
    if (statusUpdate?.pct !== undefined) custom.progressPct = statusUpdate.pct;
    if (statusUpdate?.activity) custom.currentActivity = statusUpdate.activity;
  } else if (statusUpdate?.titleIfNew && !st.titleOverrides[convId]) {
    st.titleOverrides[convId] = statusUpdate.titleIfNew.slice(0, 68);
  }
  saveState(st);
  return fullStep;
}

export function deleteConversation(convId: string): boolean {
  const st = loadState();
  if (!st.deletedIds.includes(convId)) st.deletedIds.push(convId);
  st.customConversations = st.customConversations.filter(c => c.id !== convId);
  delete st.customSteps[convId];
  saveState(st);
  return true;
}
