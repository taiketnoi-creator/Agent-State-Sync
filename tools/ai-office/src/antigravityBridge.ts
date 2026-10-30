// Cầu nối đồng bộ trực tiếp 2 chiều với Antigravity IDE (conversation_summaries.db + transcript_full.jsonl + agentapi.bat)
// - Gom tất cả các bước PLANNER_RESPONSE trong cùng 1 lượt trả lời thành 1 câu trả lời sạch duy nhất giống hệt Antigravity IDE
// - Đọc transcript_full.jsonl để không bao giờ bị cắt cụt bảng biểu hay báo cáo dài
// - Chuyển tiếp tin nhắn trực tiếp sang Antigravity IDE qua agentapi.bat
import { existsSync, statSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { spawn } from 'node:child_process';
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
const AGENTAPI_BAT = join(AGY_DIR, 'bin', 'agentapi.bat');
const STATE_FILE = 'data/conversations_state.json';
const AGY_ENV_FILE = 'data/antigravity_env.json';

// Lưu lại biến môi trường kết nối Antigravity Language Server khi server chạy từ trong Antigravity
export function captureAntigravityEnv() {
  mkdirSync('data', { recursive: true });
  if (process.env.ANTIGRAVITY_LS_ADDRESS && process.env.ANTIGRAVITY_CSRF_TOKEN) {
    const envSnapshot: Record<string, string> = {};
    for (const [k, v] of Object.entries(process.env)) {
      if (v && (k.startsWith('ANTIGRAVITY_') || k.startsWith('AGY_'))) {
        envSnapshot[k] = v;
      }
    }
    try { writeFileSync(AGY_ENV_FILE, JSON.stringify(envSnapshot, null, 2), 'utf8'); } catch {}
  } else if (existsSync(AGY_ENV_FILE)) {
    try {
      const saved = JSON.parse(readFileSync(AGY_ENV_FILE, 'utf8'));
      for (const [k, v] of Object.entries(saved)) {
        if (typeof v === 'string' && !process.env[k]) process.env[k] = v;
      }
    } catch {}
  }
}
captureAntigravityEnv();

/** Chuyển tiếp tin nhắn từ http://localhost:4800/ thẳng vào Antigravity IDE qua agentapi.bat */
export function forwardToAntigravityIde(convId: string, prompt: string): Promise<boolean> {
  return new Promise((resolve) => {
    captureAntigravityEnv();
    if (!existsSync(AGENTAPI_BAT) || !convId || convId.startsWith('conv-')) {
      resolve(false);
      return;
    }
    try {
      const child = spawn('cmd.exe', ['/c', AGENTAPI_BAT, 'send-message', convId, prompt], {
        env: { ...process.env },
        windowsHide: true,
      });
      const timer = setTimeout(() => {
        try { child.kill(); } catch {}
        resolve(false);
      }, 4000);
      child.on('close', (code) => {
        clearTimeout(timer);
        resolve(code === 0);
      });
      child.on('error', () => {
        clearTimeout(timer);
        resolve(false);
      });
    } catch {
      resolve(false);
    }
  });
}

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
  } finally {
    try { db?.close(); } catch {}
  }
  return map;
}

function cleanUserText(raw: string): string {
  if (!raw) return '';
  let s = raw;
  s = s.replace(/<CONTEXT_SUMMARY>[\s\S]*?<\/CONTEXT_SUMMARY>/g, '');
  s = s.replace(/<ADDITIONAL_METADATA>[\s\S]*?<\/ADDITIONAL_METADATA>/g, '');
  s = s.replace(/<USER_SETTINGS_CHANGE>[\s\S]*?<\/USER_SETTINGS_CHANGE>/g, '');
  s = s.replace(/<SYSTEM_MESSAGE>[\s\S]*?<\/SYSTEM_MESSAGE>/g, '');
  s = s.replace(/The following is a <SYSTEM_MESSAGE>[\s\S]*/g, '');
  const m = s.match(/<USER_REQUEST>([\s\S]*?)<\/USER_REQUEST>/);
  if (m) s = m[1];
  s = s.replace(/<\/?USER_REQUEST>/g, '').trim();
  if (s.startsWith('Error: The stream was interrupted')) return '';
  return s;
}

function summarizeToolCall(tc: any): AntiToolCall {
  const name = tc?.name || tc?.function?.name || 'tool';
  let args: any = tc?.args || tc?.arguments || tc?.function?.arguments || {};
  if (typeof args === 'string') {
    try { args = JSON.parse(args); } catch { args = {}; }
  }
  let summary = name;
  if (name === 'run_command') summary = args.toolSummary || (args.CommandLine || '').slice(0, 55);
  else if (name === 'read_file') summary = (args.Path || '').split(/[\\/]/).pop() || 'read_file';
  else if (name === 'write_file') summary = (args.Path || '').split(/[\\/]/).pop() || 'write_file';
  else if (name === 'edit_file') summary = (args.Path || '').split(/[\\/]/).pop() || 'edit_file';
  else if (name === 'invoke_subagent') summary = `${args.TypeName || ''} (${args.Role || ''})`;
  else if (name === 'manage_task') summary = `${args.Action || ''}`;
  return {
    id: tc?.id || Math.random().toString(36).slice(2, 9),
    name,
    summary,
    status: 'done',
  };
}

export function parseAntigravityTranscript(convId: string, fullSteps = false, summaryRow?: SummaryRow): AntiConversation | null {
  const fullLogPath = join(BRAIN_DIR, convId, '.system_generated', 'logs', 'transcript_full.jsonl');
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
  }

  // Gom các bước PLANNER_RESPONSE liên tiếp trong cùng 1 lượt (turn) thành 1 câu trả lời duy nhất giống hệt Antigravity IDE
  const mergedTurns: AntiStep[] = [];
  let firstUserPrompt = '';
  let lastActivity = 'Sẵn sàng';
  let lastRole: 'user' | 'assistant' | 'tool' = 'assistant';

  if (hasLog) {
    let raw = '';
    try { raw = readFileSync(logPath, 'utf8'); } catch {}
    const lines = raw.split('\n').filter(l => l.trim().length > 0);
    let pendingAssistant: AntiStep | null = null;

    for (let i = 0; i < lines.length; i++) {
      let obj: any;
      try { obj = JSON.parse(lines[i]); } catch { continue; }
      const type = obj.type || '';
      const createdAt = obj.created_at || new Date(mtimeMs).toISOString();

      if (type === 'USER_INPUT') {
        const text = cleanUserText(obj.content || '');
        if (!text) continue;
        if (pendingAssistant) {
          if (pendingAssistant.content || (pendingAssistant.toolCalls && pendingAssistant.toolCalls.length)) {
            mergedTurns.push(pendingAssistant);
          }
          pendingAssistant = null;
        }
        if (!firstUserPrompt) firstUserPrompt = text;
        lastActivity = text.slice(0, 75);
        lastRole = 'user';
        mergedTurns.push({
          index: mergedTurns.length,
          role: 'user',
          createdAt,
          content: text,
        });
      } else if (type === 'PLANNER_RESPONSE') {
        const content = (obj.content || '').trim();
        const thinking = (obj.thinking || '').trim();
        const rawCalls = Array.isArray(obj.tool_calls) ? obj.tool_calls : [];
        const toolCalls = rawCalls.map(summarizeToolCall);

        if (!pendingAssistant) {
          pendingAssistant = {
            index: mergedTurns.length,
            role: 'assistant',
            createdAt,
            content: '',
            thinking: '',
            toolCalls: [],
          };
        }
        pendingAssistant.createdAt = createdAt;
        if (toolCalls.length > 0) {
          pendingAssistant.toolCalls = [...(pendingAssistant.toolCalls || []), ...toolCalls];
          lastActivity = `Đang chạy: ${toolCalls[toolCalls.length - 1].summary}`;
          lastRole = 'tool';
        }
        if (thinking) {
          pendingAssistant.thinking = thinking;
        }
        if (content) {
          // Luôn lấy nội dung phản hồi cuối cùng đầy đủ nhất của lượt đó
          pendingAssistant.content = content;
          lastActivity = content.replace(/[#*`>|_-]/g, '').trim().slice(0, 85);
          lastRole = 'assistant';
        }
      }
    }
    if (pendingAssistant && (pendingAssistant.content || (pendingAssistant.toolCalls && pendingAssistant.toolCalls.length))) {
      mergedTurns.push(pendingAssistant);
    }
  }

  const state = loadState();
  const customExtraSteps = state.customSteps[convId] ?? [];
  // Lọc bỏ các bước custom trùng hoặc rỗng, và gộp mượt mà
  const allSteps = [...mergedTurns, ...customExtraSteps];
  if (!allSteps.length && !summaryRow?.title) return null;

  const isRunning = summaryRow?.status === 'CASCADE_RUN_STATUS_RUNNING' || ((Date.now() - mtimeMs < 12000) && lastRole !== 'assistant');
  const officialTitle = state.titleOverrides[convId] || summaryRow?.title || firstUserPrompt || `Cuộc trò chuyện ${convId.slice(0, 6)}`;
  const projectFolder = summaryRow ? extractFolderName(summaryRow.workspace_uris) : 'Subagent';

  return {
    id: convId,
    title: officialTitle.replace(/\s+/g, ' ').trim(),
    projectFolder,
    subtitle: `${projectFolder}`,
    currentActivity: customExtraSteps.length
      ? customExtraSteps[customExtraSteps.length - 1].content.replace(/[#*`>|_-]/g, '').slice(0, 85)
      : lastActivity,
    status: isRunning ? 'working' : 'idle',
    progressPct: isRunning ? Math.min(95, 35 + (allSteps.length * 7) % 55) : 100,
    agentId: 'mama',
    agentName: 'Mama',
    source: 'antigravity-ide',
    updatedAt: mtimeMs,
    stepCount: allSteps.length || summaryRow?.step_count || 0,
    steps: fullSteps ? allSteps.slice(-60) : undefined,
  };
}

export function listAllConversations(limit = 25): AntiConversation[] {
  const st = loadState();
  const deleted = new Set(st.deletedIds);
  const out: AntiConversation[] = [];

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

  const summaryMap = queryTopLevelAntigravitySummaries();
  for (const [convId, row] of summaryMap.entries()) {
    if (deleted.has(convId)) continue;
    const folder = extractFolderName(row.workspace_uris);
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
  const agentName = input.agentName || 'Mama';
  const title = (input.title || `Cuộc trò chuyện mới`).trim();
  const conv: AntiConversation = {
    id,
    title,
    projectFolder: 'Subagent',
    subtitle: `Subagent`,
    currentActivity: 'Sẵn sàng',
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
  st.customSteps[id] = [];
  saveState(st);
  return { ...conv, steps: [], stepCount: 0 };
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
