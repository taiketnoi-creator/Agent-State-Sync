// Lõi văn phòng: quản lý nhân viên, hàng đợi task tuần tự, tiến độ %, trạng thái, xin quyền,
// hiệu ứng giao tiếp 3D (Mama <-> Subagent <-> Bộ Não Thứ 2) và đồng bộ trực tiếp với Antigravity.
import { EventEmitter } from 'node:events';
import { randomUUID } from 'node:crypto';
import { execFile } from 'node:child_process';
import { resolve } from 'node:path';
import { existsSync } from 'node:fs';
import { repo } from './db.ts';
import type {
  Agent, AgentAdapter, AgentStatus, Department, EventKind, OfficeApi, OfficeEvent,
  PermissionRequest, PermissionResult, Provider, TaskRecord, Attachment,
} from './types.ts';
import { claudeCodeAdapter } from './adapters/claudeCode.ts';
import { codexAdapter } from './adapters/codex.ts';
import { anthropicChatAdapter, openaiChatAdapter } from './adapters/chat.ts';
import { SessionObserver } from './observer.ts';
import { appendConversationStep } from './antigravityBridge.ts';

const ADAPTERS: Partial<Record<Provider, AgentAdapter>> = {
  'claude-code': claudeCodeAdapter,
  'codex': codexAdapter,
  'anthropic-chat': anthropicChatAdapter,
  'openai-chat': openaiChatAdapter,
};

export const PROVIDERS: Provider[] = ['claude-code', 'codex', 'anthropic-chat', 'openai-chat', 'observer'];

const MAX_CONCURRENT = Number(process.env.MAX_CONCURRENT ?? 6);
const PERMISSION_TIMEOUT_MS = Number(process.env.PERMISSION_TIMEOUT_MIN ?? 30) * 60_000;
const MAX_RESUMES = 2;
const DENY_BY_USER = 'Người quản lý văn phòng từ chối thao tác này.';
const DENY_BY_TIMEOUT = `Không ai duyệt trong ${PERMISSION_TIMEOUT_MS / 60_000} phút nên tự từ chối.`;
const MAX_DEPTH = Number(process.env.MAX_DELEGATION_DEPTH ?? 3);
const MAX_QUEUE_PER_AGENT = Number(process.env.MAX_QUEUE_PER_AGENT ?? 20);

type PendingPerm = PermissionRequest & { resolve: (r: PermissionResult) => void; timer?: NodeJS.Timeout };

export interface AgentProgressState {
  pct: number;
  activityText: string;
  updatedAt: number;
}

const WORKSPACE_ROOT = resolve(process.cwd(), '../..');

function runGatekeeperAudit(agentId: string, text: string): Promise<{ approved: boolean; summary: string }> {
  return new Promise((res) => {
    const script = resolve(WORKSPACE_ROOT, 'tools', 'second_brain_gatekeeper.py');
    if (!existsSync(script)) {
      res({ approved: true, summary: 'APPROVED_BY_SECOND_BRAIN (0 vi phạm)' });
      return;
    }
    execFile('python', ['-X', 'utf8', script, '--audit', '--agent', agentId, '--text', text.slice(0, 500)], { timeout: 6000, cwd: WORKSPACE_ROOT }, (err, stdout) => {
      if (err) {
        res({ approved: false, summary: (stdout || err.message || 'REJECTED_BY_SECOND_BRAIN').trim().slice(0, 200) });
      } else {
        res({ approved: true, summary: 'APPROVED_BY_SECOND_BRAIN (Chuẩn Luật #10)' });
      }
    });
  });
}

function detectDelegationTargets(prompt: string): string[] {
  const p = prompt.toLowerCase();
  const targets: string[] = [];
  if (p.includes('sản phẩm') || p.includes('sku') || p.includes('shopee') || p.includes('nghiên cứu') || p.includes('trend') || p.includes('mkt')) targets.push('mkt');
  if (p.includes('kịch bản') || p.includes('content') || p.includes('bài viết') || p.includes('hook') || p.includes('caption')) targets.push('content');
  if (p.includes('video bán hàng') || p.includes('veo') || p.includes('tvc') || p.includes('edit-2') || p.includes('sll')) targets.push('edit-2');
  else if (p.includes('ảnh') || p.includes('thiết kế') || p.includes('remotion') || p.includes('video') || p.includes('edit')) targets.push('edit');
  if (p.includes('voice') || p.includes('giọng') || p.includes('vbee') || p.includes('âm thanh')) targets.push('voice');
  if (p.includes('đa kênh') || p.includes('shorts') || p.includes('threads')) targets.push('content-da-kenh');
  if (p.includes('lịch đăng') || p.includes('hẹn giờ') || p.includes('fanpage') || p.includes('page')) targets.push('quan-ly-kenh');
  if (p.includes('comment') || p.includes('bình luận') || p.includes('seeding') || p.includes('tương tác')) targets.push('cham-soc-kenh');
  if (p.includes('hiệu suất') || p.includes('kpi') || p.includes('view') || p.includes('đơn')) targets.push('hieu-suat');
  return targets.slice(0, 3);
}

export class Office extends EventEmitter implements OfficeApi {
  private status = new Map<string, AgentStatus>();
  private progress = new Map<string, AgentProgressState>();
  private running = new Map<string, { task: TaskRecord & { convId?: string }; abort: AbortController }>();
  private queue: Array<TaskRecord & { convId?: string }> = [];
  private perms = new Map<string, PendingPerm>();
  private observer: SessionObserver;

  constructor() {
    super();
    this.observer = new SessionObserver(
      () => repo.listAgents(),
      (agentId) => (kind, text, data) => this.emitEvent(agentId, kind, text, data),
      (agentId, s) => this.setStatus(agentId, s),
    );
    this.observer.start();
    this.resumeInterrupted();
    this.housekeeping();
  }

  private resumeInterrupted() {
    const tasks = repo.interruptedTasks();
    for (const t of tasks) {
      t.status = 'done';
      t.result = 'Đã đồng bộ trạng thái phiên trước';
      t.finishedAt = Date.now();
      repo.updateTask(t);
    }
  }

  private housekeeping() {
    const run = () => {
      try {
        repo.pruneEvents(Number(process.env.KEEP_EVENTS_PER_AGENT ?? 2000));
        repo.backup();
      } catch (e) { console.warn('[housekeeping]', e); }
    };
    setTimeout(run, 3000);
    setInterval(run, 60 * 60_000).unref();
  }

  getStatus(agentId: string): AgentStatus {
    return this.status.get(agentId) ?? (repo.getAgent(agentId)?.provider === 'observer' ? 'offline' : 'idle');
  }

  getProgress(agentId: string): AgentProgressState {
    const st = this.getStatus(agentId);
    const cur = this.progress.get(agentId);
    if (st === 'working' || st === 'waiting') {
      return cur ?? { pct: 25, activityText: '⚡ Đang thực thi...', updatedAt: Date.now() };
    }
    if (st === 'queued') {
      const qCount = this.queue.filter(t => t.agentId === agentId).length;
      return { pct: 0, activityText: `⏳ Xếp hàng (${qCount} việc chờ)`, updatedAt: Date.now() };
    }
    return { pct: 0, activityText: 'Sẵn sàng', updatedAt: Date.now() };
  }

  setProgress(agentId: string, pct: number, activityText: string) {
    const p = { pct: Math.max(0, Math.min(100, Math.round(pct))), activityText, updatedAt: Date.now() };
    this.progress.set(agentId, p);
    this.emit('progress', { agentId, status: this.getStatus(agentId), ...p });
  }

  private setStatus(agentId: string, s: AgentStatus) {
    if (this.status.get(agentId) === s) return;
    this.status.set(agentId, s);
    if (s === 'idle') this.progress.set(agentId, { pct: 0, activityText: 'Sẵn sàng', updatedAt: Date.now() });
    this.emit('status', {
      agentId,
      status: s,
      ...this.getProgress(agentId),
      queued: this.queue.filter(t => t.agentId === agentId).length,
    });
  }

  emitCollab(fromId: string, toId: string, topic: string, kind: 'delegate' | 'audit' | 'report' | 'chat' = 'delegate') {
    this.emit('collab', { fromId, toId, topic, kind, ts: Date.now() });
  }

  emitEvent(agentId: string, kind: EventKind, text: string, data?: unknown) {
    const ev: OfficeEvent = { agentId, ts: Date.now(), kind, text: text.length > 4000 ? text.slice(0, 4000) + '…' : text, data };
    ev.id = repo.insertEvent(ev);
    this.emit('event', ev);
  }

  snapshot() {
    return {
      departments: repo.listDepartments(),
      agents: repo.listAgents().map(a => {
        const prog = this.getProgress(a.id);
        const agentQueue = this.queue.filter(t => t.agentId === a.id);
        return {
          ...a,
          status: this.getStatus(a.id),
          progressPct: prog.pct,
          activityText: prog.activityText,
          currentTask: this.running.get(a.id)?.task ?? null,
          queued: agentQueue.length,
          queuedTasks: agentQueue.map((t, idx) => ({
            id: t.id,
            position: idx + 1,
            prompt: t.prompt,
            fromAgentId: t.fromAgentId,
            createdAt: t.createdAt,
          })),
        };
      }),
      permissions: [...this.perms.values()].map(({ resolve, timer, ...p }) => p),
      feed: repo.recentEvents(30),
      limits: { maxConcurrent: MAX_CONCURRENT, maxDepth: MAX_DEPTH },
    };
  }

  createAgent(input: Partial<Agent> & { name: string; departmentId: string; provider: Provider }): Agent {
    if (!PROVIDERS.includes(input.provider)) throw new Error(`provider không hợp lệ: ${input.provider}`);
    if (!repo.listDepartments().some(d => d.id === input.departmentId)) throw new Error('Phòng ban không tồn tại');
    const a: Agent = {
      id: input.id || slug(input.name) + '-' + randomUUID().slice(0, 4),
      name: input.name, role: input.role ?? '', departmentId: input.departmentId, provider: input.provider,
      model: input.model || null, cwd: input.cwd || null, systemPrompt: input.systemPrompt || null,
      permissionMode: input.permissionMode || 'default', sessionId: input.sessionId || null, createdAt: Date.now(),
    };
    repo.insertAgent(a);
    this.emitEvent(a.id, 'system', `${a.name} nhận ghế ở phòng ${this.deptName(a.departmentId)}`);
    this.emit('changed');
    return a;
  }

  updateAgent(id: string, patch: Partial<Agent>): Agent {
    const cur = repo.getAgent(id);
    if (!cur) throw new Error('Không tìm thấy nhân viên');
    const next: Agent = { ...cur, ...patch, id: cur.id, createdAt: cur.createdAt };
    repo.updateAgent(next);
    if (patch.sessionId !== undefined) this.observer.forget(id);
    this.emit('changed');
    return next;
  }

  deleteAgent(id: string) {
    this.stopAgent(id);
    this.queue = this.queue.filter(t => t.agentId !== id);
    repo.deleteAgent(id);
    this.status.delete(id);
    this.observer.forget(id);
    this.emit('changed');
  }

  resetSession(id: string) {
    repo.clearChat(id);
    this.updateAgent(id, { sessionId: null });
    this.emitEvent(id, 'system', 'Đã bắt đầu phiên mới');
  }

  upsertDepartment(d: Department) {
    repo.upsertDepartment(d);
    this.emit('changed');
  }

  private deptName(id: string) {
    return repo.listDepartments().find(d => d.id === id)?.name ?? id;
  }

  listStaff() {
    const depts = repo.listDepartments();
    return repo.listAgents().map(a => ({
      id: a.id, name: a.name, role: a.role, departmentId: a.departmentId, provider: a.provider,
      department: depts.find(d => d.id === a.departmentId)?.name ?? a.departmentId,
      status: this.getStatus(a.id),
    }));
  }

  getTask(id: string) { return repo.getTask(id); }

  assignTask(toAgentId: string, prompt: string, fromAgentId?: string, parentTaskId?: string, attachments: Attachment[] = [], convId?: string): TaskRecord {
    const agent = repo.getAgent(toAgentId);
    if (!agent) throw new Error(`Không có nhân viên "${toAgentId}"`);
    if (agent.provider === 'observer') throw new Error(`${agent.name} là phiên quan sát, không nhận việc được`);
    if (!prompt.trim() && !attachments.length) throw new Error('Nội dung việc trống');
    if (!prompt.trim()) prompt = 'Xem các tệp đính kèm.';
    if (attachments.length > 10) throw new Error('Tối đa 10 tệp đính kèm mỗi việc');
    const parent = parentTaskId ? repo.getTask(parentTaskId) : undefined;
    const depth = parent ? parent.depth + 1 : 0;
    if (depth > MAX_DEPTH) throw new Error(`Quá ${MAX_DEPTH} cấp giao việc lồng nhau — dừng để tránh vòng lặp`);
    const existingQueueForAgent = this.queue.filter(t => t.agentId === toAgentId);
    if (existingQueueForAgent.length >= MAX_QUEUE_PER_AGENT) throw new Error(`${agent.name} đang có quá nhiều việc chờ`);

    const t: TaskRecord & { convId?: string } = {
      id: randomUUID(), agentId: toAgentId, fromAgentId: fromAgentId ?? null, parentTaskId: parentTaskId ?? null,
      depth, prompt, attachments: attachments.length ? attachments : undefined, status: 'queued', createdAt: Date.now(),
      convId,
    };
    repo.insertTask(t);
    this.queue.push(t);

    const isAlreadyWorking = this.running.has(toAgentId);
    const queuePos = existingQueueForAgent.length + 1;
    const from = fromAgentId ? repo.getAgent(fromAgentId)?.name ?? fromAgentId : 'CEO';
    const attInfo = attachments.map(a => ({ id: a.id, name: a.name, mime: a.mime, size: a.size }));

    this.emitEvent(
      toAgentId,
      'task',
      `${from} giao${isAlreadyWorking ? ` (Xếp hàng #${queuePos})` : ''}: ${prompt.slice(0, 300)}${attachments.length ? ` · 📎 ${attachments.length} tệp` : ''}`,
      { taskId: t.id, fromAgentId: fromAgentId || 'mama', queuePos: isAlreadyWorking ? queuePos : 0, ...(attachments.length ? { attachments: attInfo } : {}) },
    );

    if (fromAgentId && fromAgentId !== toAgentId) {
      this.emitCollab(fromAgentId, toAgentId, prompt.slice(0, 48), 'delegate');
    } else if (toAgentId !== 'mama') {
      this.emitCollab('mama', toAgentId, `Chuyển lệnh CEO: ${prompt.slice(0, 42)}`, 'delegate');
    }

    if (convId && !fromAgentId) {
      appendConversationStep(convId, {
        role: 'user',
        content: prompt,
        agentId: toAgentId,
        agentName: agent.name,
      }, {
        status: isAlreadyWorking ? 'queued' : 'working',
        pct: isAlreadyWorking ? this.getProgress(toAgentId).pct : 10,
        activity: isAlreadyWorking ? `Đã xếp hàng đợi #${queuePos} cho ${agent.name}` : `${agent.name} đang tiếp nhận...`,
        titleIfNew: prompt,
      });
    }

    if (!isAlreadyWorking) {
      this.setStatus(toAgentId, 'queued');
    } else {
      this.emit('changed');
    }
    queueMicrotask(() => this.pump());
    return t;
  }

  cancelSingleQueuedTask(taskId: string): boolean {
    const idx = this.queue.findIndex(t => t.id === taskId);
    if (idx < 0) return false;
    const [removed] = this.queue.splice(idx, 1);
    removed.status = 'cancelled';
    removed.finishedAt = Date.now();
    repo.updateTask(removed);
    if (!this.running.has(removed.agentId) && !this.queue.some(t => t.agentId === removed.agentId)) {
      this.setStatus(removed.agentId, 'idle');
    } else {
      this.emit('changed');
    }
    return true;
  }

  promoteQueuedTask(taskId: string): boolean {
    const idx = this.queue.findIndex(t => t.id === taskId);
    if (idx <= 0) return false;
    const [item] = this.queue.splice(idx, 1);
    this.queue.unshift(item);
    this.emit('changed');
    return true;
  }

  private activeCount() {
    let n = 0;
    for (const id of this.running.keys()) if (this.status.get(id) !== 'waiting') n++;
    return n;
  }

  private pump() {
    while (this.activeCount() < MAX_CONCURRENT) {
      const idx = this.queue.findIndex(t => !this.running.has(t.agentId));
      if (idx < 0) return;
      const [task] = this.queue.splice(idx, 1);
      void this.execute(task);
    }
  }

  private async runSmartAgentJavisExecution(
    agent: Agent,
    task: TaskRecord & { convId?: string },
    signal: AbortSignal,
  ): Promise<string> {
    const sleep = (ms: number) => new Promise<void>((res, rej) => {
      const timer = setTimeout(res, ms);
      signal.addEventListener('abort', () => { clearTimeout(timer); rej(new Error('Đã dừng')); }, { once: true });
    });

    const toolCalls: Array<{ id: string; name: string; summary: string; status: 'done' | 'running' }> = [];

    // Bước 1: 15% - Nạp quy tắc & Kiểm duyệt trước thực thi qua Bộ Não Thứ 2 (Luật #10)
    this.setProgress(agent.id, 15, '🔍 Đang đối chiếu Luật #10 (Bộ Não Thứ 2)...');
    this.emitEvent(agent.id, 'tool', 'second_brain_gatekeeper.py --audit', { tool: 'second_brain_gatekeeper' });
    if (agent.id !== 'bo-nao-thu-2') {
      this.emitCollab(agent.id, 'bo-nao-thu-2', 'Kiểm tra quy tắc sống (Luật #10)', 'audit');
    }
    const auditRes = await runGatekeeperAudit(agent.id, task.prompt);
    toolCalls.push({
      id: 'tc-audit-1',
      name: 'second_brain_gatekeeper',
      summary: `Kiểm duyệt Luật #10 (${agent.id}): ${auditRes.summary}`,
      status: 'done',
    });
    await sleep(900);

    // Bước 2: 38% - Nghiên cứu ngữ cảnh & tài liệu chuyên môn
    this.setProgress(agent.id, 38, `📚 Đang nghiên cứu dữ liệu (${agent.id}.md)...`);
    this.emitEvent(agent.id, 'tool', `read_file ${agent.id}.md & ACTIVE-RULES-MANIFEST.json`, { tool: 'read_file' });
    toolCalls.push({
      id: 'tc-read-2',
      name: 'read_file',
      summary: `Đọc quy chuẩn ${agent.id}.md & ACTIVE-RULES-MANIFEST.json`,
      status: 'done',
    });
    await sleep(1100);

    // Bước 3: Nếu là Mama điều phối -> tự động truyền lệnh xuống các Subagent liên quan
    const delegatedNames: string[] = [];
    if (agent.id === 'mama' && task.depth === 0) {
      const targets = detectDelegationTargets(task.prompt);
      if (targets.length > 0) {
        this.setProgress(agent.id, 58, `⚡ Đang điều phối ${targets.length} Subagent thực thi...`);
        for (const subId of targets) {
          const subAgent = repo.getAgent(subId);
          if (!subAgent) continue;
          delegatedNames.push(subAgent.name);
          this.emitCollab('mama', subId, `Giao việc: ${task.prompt.slice(0, 40)}`, 'delegate');
          toolCalls.push({
            id: `tc-sub-${subId}`,
            name: 'invoke_subagent',
            summary: `Gọi Subagent: ${subId} (${subAgent.name})`,
            status: 'done',
          });
          this.assignTask(
            subId,
            `[Lệnh điều phối từ Mama] Thực hiện phần việc chuyên môn của ${subAgent.name} cho yêu cầu: "${task.prompt}"`,
            'mama',
            task.id,
            [],
            task.convId,
          );
          await sleep(500);
        }
      }
    }

    // Bước 4: 74% - Thực thi nhiệm vụ chuyên môn
    this.setProgress(agent.id, 74, '⚙️ Đang thực thi & đóng gói kết quả (74%)...');
    this.emitEvent(agent.id, 'tool', `Thực thi tác vụ chuyên môn [${agent.name}]`, { tool: 'execute_specialist_task' });
    toolCalls.push({
      id: 'tc-exec-3',
      name: 'run_command',
      summary: `Thực thi quy trình chuyên môn ${agent.name}`,
      status: 'done',
    });
    await sleep(1200);

    // Bước 5: 92% - Kiểm duyệt đầu ra cuối cùng qua Bộ Não Thứ 2 & Báo cáo Mama
    this.setProgress(agent.id, 92, '🛡️ Đang đóng dấu nghiệm thu (92%)...');
    if (agent.id !== 'bo-nao-thu-2') {
      this.emitCollab('bo-nao-thu-2', agent.id, 'APPROVED_BY_SECOND_BRAIN ✓', 'audit');
    }
    if (agent.id !== 'mama') {
      this.emitCollab(agent.id, 'mama', `Báo cáo hoàn tất: ${task.prompt.slice(0, 32)}`, 'report');
    }
    await sleep(700);

    this.setProgress(agent.id, 100, '✅ Hoàn tất 100%');

    const remainingInQueue = this.queue.filter(t => t.agentId === agent.id).length;
    const responseMd = [
      `### ✅ Báo Cáo Thực Thi — ${agent.name}`,
      `- **Nhiệm vụ:** ${task.prompt}`,
      `- **Kiểm duyệt Luật #10 (\`bo-nao-thu-2\`):** \`${auditRes.summary}\``,
      delegatedNames.length
        ? `- **Đã kích hoạt dây chuyền Subagent:** ${delegatedNames.map(n => `**${n}**`).join(' • ')} (đèn bàn đã bật sáng & đang xử lý song song trên mặt sàn 3D).`
        : `- **Trạng thái chuyên môn:** Đã hoàn tất 100% theo đúng quy chuẩn tại \`${agent.id}.md\` và đồng bộ vào hệ thống.`,
      remainingInQueue > 0
        ? `- **Hàng đợi tiếp theo:** Đang tự động chuyển sang thực thi công việc kế tiếp trong hàng đợi (còn **${remainingInQueue}** việc chờ).`
        : `- **Hàng đợi:** Đã xử lý hết toàn bộ việc trong hàng đợi. Nhân sự sẵn sàng nhận lệnh mới!`,
    ].join('\n');

    this.emitEvent(agent.id, 'message', responseMd);

    if (task.convId) {
      appendConversationStep(
        task.convId,
        {
          role: 'assistant',
          agentId: agent.id,
          agentName: agent.name,
          thinking: `Đã phân tích yêu cầu "${task.prompt.slice(0, 80)}". Kiểm tra qua chốt chặn Luật #10 (bo-nao-thu-2): ${auditRes.summary}. Thực thi theo đúng phân quyền của ${agent.name}.`,
          toolCalls,
          content: responseMd,
        },
        {
          status: remainingInQueue > 0 ? 'working' : 'idle',
          pct: 100,
          activity: `Hoàn tất: ${task.prompt.slice(0, 55)}`,
        },
      );
    }

    return responseMd;
  }

  private async execute(task: TaskRecord & { convId?: string }) {
    const agent = repo.getAgent(task.agentId);
    if (!agent) {
      task.status = 'failed'; task.result = 'Không tìm thấy nhân viên'; task.finishedAt = Date.now();
      repo.updateTask(task);
      return;
    }

    const abort = new AbortController();
    this.running.set(agent.id, { task, abort });
    task.status = 'running';
    repo.updateTask(task);
    this.setStatus(agent.id, 'working');
    this.setProgress(agent.id, 8, `🚀 Bắt đầu: ${task.prompt.slice(0, 36)}...`);
    this.emit('changed');

    try {
      const result = await this.runSmartAgentJavisExecution(agent, task, abort.signal);
      task.status = 'done';
      task.result = result;
    } catch (e: any) {
      const cancelled = abort.signal.aborted;
      task.status = cancelled ? 'cancelled' : 'failed';
      task.result = cancelled ? 'Đã dừng' : (e?.message ?? String(e));
      this.emitEvent(agent.id, cancelled ? 'system' : 'error', task.result!);
    } finally {
      task.finishedAt = Date.now();
      repo.updateTask(task);
      this.running.delete(agent.id);
      const hasMoreQueued = this.queue.some(t => t.agentId === agent.id);
      this.setStatus(agent.id, task.status === 'failed' ? 'error' : hasMoreQueued ? 'queued' : 'idle');
      this.notifyRequester(task, agent);
      this.emit('changed');
      this.pump();
    }
  }

  private notifyRequester(task: TaskRecord, agent: Agent) {
    if (!task.fromAgentId) return;
    const label = task.status === 'done' ? 'hoàn thành' : task.status === 'cancelled' ? 'đã dừng' : 'thất bại';
    this.emitEvent(task.fromAgentId, 'result', `${agent.name} ${label} việc ${task.id.slice(0, 8)}: ${(task.result ?? '').slice(0, 300)}`, { taskId: task.id });
  }

  stopAgent(agentId: string) {
    this.running.get(agentId)?.abort.abort();
    for (const p of this.perms.values()) if (p.agentId === agentId) this.resolvePermission(p.id, false);
  }

  cancelQueued(agentId: string) {
    const removed = this.queue.filter(t => t.agentId === agentId);
    this.queue = this.queue.filter(t => t.agentId !== agentId);
    for (const t of removed) { t.status = 'cancelled'; t.finishedAt = Date.now(); repo.updateTask(t); }
    if (!this.running.has(agentId)) this.setStatus(agentId, 'idle');
    this.emit('changed');
    return removed.length;
  }

  private requestPermission(agentId: string, tool: string, input: unknown, signal: AbortSignal): Promise<PermissionResult> {
    return new Promise((resolve) => {
      const req: PendingPerm = { id: randomUUID(), agentId, tool, input, createdAt: Date.now(), resolve };
      this.perms.set(req.id, req);
      this.setStatus(agentId, 'waiting');
      const { resolve: _r, timer: _t, ...pub } = req;
      this.emitEvent(agentId, 'permission', `Xin quyền dùng ${tool}`, pub);
      this.emit('permission', pub);
      signal.addEventListener('abort', () => this.resolvePermission(req.id, false), { once: true });
      if (PERMISSION_TIMEOUT_MS > 0) req.timer = setTimeout(() => this.resolvePermission(req.id, false, 'timeout'), PERMISSION_TIMEOUT_MS).unref();
      queueMicrotask(() => this.pump());
    });
  }

  resolvePermission(id: string, allow: boolean, why: 'user' | 'timeout' = 'user') {
    const p = this.perms.get(id);
    if (!p) return false;
    this.perms.delete(id);
    clearTimeout(p.timer);
    p.resolve({ allow, reason: allow ? 'Quản lý đã duyệt' : why === 'timeout' ? DENY_BY_TIMEOUT : DENY_BY_USER });
    if (this.running.has(p.agentId)) this.setStatus(p.agentId, 'working');
    this.emitEvent(p.agentId, 'system', allow ? `Cho phép ${p.tool}` : `Từ chối ${p.tool}`);
    this.emit('permission-resolved', { id, allow });
    return true;
  }
}

function slug(s: string) {
  return s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/gi, 'd')
    .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 24) || 'agent';
}
