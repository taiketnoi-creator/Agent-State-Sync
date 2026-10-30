// Cầu nối đồng bộ trực tiếp các Tab Cuộc Trò Chuyện chính của Antigravity IDE (từ conversation_summaries.db & brain)
// - Chỉ lấy các Tab Trò Chuyện chính của CEO trong dự án Subagent (nesting_depth = 0, không trộn các phiên chạy ngầm của Subagent)
// - Lấy đúng Tiêu đề chính thức của Antigravity IDE ("Kiểm Tra Dự Án Văn Phòng 3D", "Git Pull Command Explanation", "Kiểm Tra Cấu Trúc Sub Agent"...)
import { existsSync, statSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { DatabaseSync } from 'node:sqlite';

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
  projectFolder: string;
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

const AGY_DIR = join(homedir(), '.gemini', 'antigravity');
const BRAIN_DIR = join(AGY_DIR, 'brain');
const SUMMARIES_DB = join(AGY_DIR, 'conversation_summaries.db');
const STATE_FILE = 'data/conversations_state.json';

interface SummaryRow {
  conversation_id: string;
  title: string;
  step_count: number;
  last_modified_time: string;
  workspace_uris: string;
  status: string;
  nesting_depth: number;
  parent_conversation_id: string;
  agent_name: string;
}

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

function extractFolderName(workspaceUris: string): string {
  if (!workspaceUris) return 'Khác';
  try {
    const arr = JSON.parse(workspaceUris);
    if (Array.isArray(arr) && arr.length > 0) {
      const decoded = decodeURIComponent(String(arr[0]));
      const parts = decoded.replace(/\\/g, '/').replace(/\/+$/, '').split('/');
      return parts[parts.length - 1] || 'Subagent';
    }
  } catch {}
  return 'Subagent';
}

/** Đọc danh sách các Tab Trò Chuyện chính (nesting_depth = 0) từ conversation_summaries.db của Antigravity */
function queryTopLevelAntigravitySummaries(): Map<string, SummaryRow> {
  const map = new Map<string, SummaryRow>();
  if (!existsSync(SUMMARIES_DB)) return map;
  let db: DatabaseSync | null = null;
  try {
    db = new DatabaseSync(SUMMARIES_DB, { readOnly: true });
    const rows = db.prepare(`
      SELECT conversation_id, title, step_count, last_modified_time, workspace_uris, status, nesting_depth, parent_conversation_id, agent_name
      FROM conversation_summaries
      WHERE nesting_depth = 0 AND parent_conversation_id = '' AND agent_name = ''
      ORDER BY last_modified_time DESC
    `).all() as unknown as SummaryRow[];
    for (const r of rows) {
      map.set(r.conversation_id, r);
    }
  } catch {
    // ignore lock errors
  } finally {
    try { db?.close(); } catch {}
  }
  return map;
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

export function parseAntigravityTranscript(convId: string, fullSteps = false, summaryRow?: SummaryRow): AntiConversation | null {
  const logPath = join(BRAIN_DIR, convId, '.system_generated', 'logs', 'transcript.jsonl');
  const hasLog = existsSync(logPath);
  if (!hasLog && !summaryRow) return null;

  let mtimeMs = Date.now();
  if (summaryRow?.last_modified_time) {
    const parsedTs = Date.parse(summaryRow.last_modified_time);
    if (!isNaN(parsedTs)) mtimeMs = parsedTs;
  } else if (hasLog) {
    try { mtimeMs = statSync(logPath).mtimeMs; } catch {}
  }

  const steps: AntiStep[] = [];
  let firstUserPrompt = '';
  let lastActivity = 'Sẵn sàng';
  let lastRole: 'user' | 'assistant' | 'tool' = 'assistant';

  if (hasLog) {
    let raw = '';
    try { raw = readFileSync(logPath, 'utf8'); } catch {}
    const lines = raw.split('\n').filter(l => l.trim().length > 0);
    for (let i = 0; i < lines.length; i++) {
      let obj: any;
      try { obj = JSON.parse(lines[i]); } catch { continue; }
      const type = obj.type || '';
      const createdAt = obj.created_at || new Date(mtimeMs).toISOString();

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
  }

  const state = loadState();
  const customExtraSteps = state.customSteps[convId] ?? [];
  const allSteps = [...steps, ...customExtraSteps];
  if (!allSteps.length && !summaryRow?.title) return null;

  const isRunning = summaryRow?.status === 'CASCADE_RUN_STATUS_RUNNING' || ((Date.now() - mtimeMs < 15000) && lastRole !== 'assistant');
  const officialTitle = state.titleOverrides[convId] || summaryRow?.title || firstUserPrompt || `Cuộc trò chuyện ${convId.slice(0, 6)}`;
  const projectFolder = summaryRow ? extractFolderName(summaryRow.workspace_uris) : 'Subagent';

  return {
    id: convId,
    title: officialTitle.replace(/\s+/g, ' ').trim(),
    projectFolder,
    subtitle: `${projectFolder} · ${allSteps.length || summaryRow?.step_count || 0} bước`,
    currentActivity: customExtraSteps.length
      ? customExtraSteps[customExtraSteps.length - 1].content.slice(0, 85)
      : lastActivity,
    status: isRunning ? 'working' : 'idle',
    progressPct: isRunning ? Math.min(95, 35 + (allSteps.length * 7) % 55) : 100,
    agentId: 'mama',
    agentName: 'Mama (Chief of Staff)',
    source: 'antigravity-ide',
    updatedAt: mtimeMs,
    stepCount: allSteps.length || summaryRow?.step_count || 0,
    steps: fullSteps ? allSteps.slice(-80) : undefined,
  };
}

export function listAllConversations(limit = 25): AntiConversation[] {
  const st = loadState();
  const deleted = new Set(st.deletedIds);
  const out: AntiConversation[] = [];

  // 1. Các Tab Trò Chuyện tạo mới trực tiếp trong Văn phòng 3D
  for (const c of st.customConversations) {
    if (deleted.has(c.id)) continue;
    const cSteps = st.customSteps[c.id] ?? [];
    out.push({
      ...c,
      projectFolder: c.projectFolder || 'Subagent',
      stepCount: cSteps.length,
      currentActivity: cSteps.length
        ? cSteps[cSteps.length - 1].content.replace(/[#*`]/g, '').slice(0, 85)
        : c.currentActivity,
    });
  }

  // 2. Các Tab Trò Chuyện chính của CEO từ conversation_summaries.db (Lọc đúng dự án Subagent, bỏ sạch Subagent runs)
  const summaryMap = queryTopLevelAntigravitySummaries();
  for (const [convId, row] of summaryMap.entries()) {
    if (deleted.has(convId)) continue;
    const folder = extractFolderName(row.workspace_uris);
    // Chỉ hiển thị đúng các Tab thuộc dự án Subagent giống hệt ảnh 2 của CEO
    if (folder.toLowerCase() !== 'subagent') continue;
    const parsed = parseAntigravityTranscript(convId, false, row);
    if (parsed) out.push(parsed);
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
    return { ...custom, projectFolder: custom.projectFolder || 'Subagent', stepCount: steps.length, steps };
  }
  const summaryMap = queryTopLevelAntigravitySummaries();
  return parseAntigravityTranscript(convId, true, summaryMap.get(convId));
}

export function createOfficeConversation(input: { title?: string; agentId?: string; agentName?: string }): AntiConversation {
  const st = loadState();
  const id = 'conv-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 6);
  const agentId = input.agentId || 'mama';
  const agentName = input.agentName || 'Mama (Chief of Staff)';
  const title = (input.title || `Cuộc trò chuyện mới`).trim();
  const conv: AntiConversation = {
    id,
    title,
    projectFolder: 'Subagent',
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
      content: `Xin chào CEO! Tôi là **${agentName}**. Cuộc trò chuyện này được đồng bộ trực tiếp trong thư mục **📁 Subagent**.\n\nCEO có thể giao việc trực tiếp tại đây hoặc bấm vào bất kỳ nhân vật 3D nào trên mặt sàn!`,
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
    custom.stepCount = list.length;
    if (statusUpdate?.status) custom.status = statusUpdate.status;
    if (statusUpdate?.pct !== undefined) custom.progressPct = statusUpdate.pct;
    if (statusUpdate?.activity) custom.currentActivity = statusUpdate.activity;
    if (statusUpdate?.titleIfNew && (custom.title.startsWith('Cuộc trò chuyện mới') || custom.title.length < 6)) {
      custom.title = statusUpdate.titleIfNew.slice(0, 62);
    }
  } else if (statusUpdate?.titleIfNew && !st.titleOverrides[convId]) {
    st.titleOverrides[convId] = statusUpdate.titleIfNew.slice(0, 62);
  }
  saveState(st);
}

export function deleteConversation(convId: string): boolean {
  const st = loadState();
  if (!st.deletedIds.includes(convId)) st.deletedIds.push(convId);
  st.customConversations = st.customConversations.filter(c => c.id !== convId);
  delete st.customSteps[convId];
  saveState(st);
  return true;
}
