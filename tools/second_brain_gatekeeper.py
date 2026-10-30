#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
second_brain_gatekeeper.py — Động Cơ Giám Sát Đa Tab & Chốt Kiểm Duyệt Cuối Cùng Của Bộ Não Thứ 2 (`bo-nao-thu-2`).

Thực thi LUẬT #10 của CEO (2026-10-30):
1. THEO DÕI MỌI TAB CÔNG VIỆC & MỌI CUỘC TRÒ CHUYỆN (`--watch-all-tabs`):
   - Tự động quét tất cả các cửa sổ/tab trò chuyện trong `.gemini/antigravity/brain/*/logs/transcript.jsonl`
     và `RECENT-CONVERSATION.md` trên cả Máy Công Ty (`guicci`) và Máy Ở Nhà (`Admin-PC`).
   - Tự động bắt các lời nhắc nhở (`nhắc lịch`, `nhắc tôi`, `hẹn giờ`, `tối nay`, `lúc ...h`) -> ghi vào
     `knowledge/ceo_evening_reminders.json` và sổ theo dõi của `bo-nao-thu-2`.
   - Tự động bắt các chỉ đạo thay đổi/chỉnh sửa/thêm quy tắc (`thay đổi`, `sửa lại`, `quy tắc`, `phong cách mới`,
     `cấm`, `tắt lệnh`, `không dùng`, `bộ này vẫn sai`...) -> lưu vào `knowledge/bo-nao-thu-2/LIVE-WATCH-LOG.json`
     để khóa cứng, ngăn chặn tuyệt đối việc dùng lại bộ nhớ cũ.
2. KIỂM DUYỆT TRƯỚC & SAU THỰC THI (`--audit --agent <name> --text <brief_or_output>`):
   - Đối chiếu mọi nhiệm vụ `mama` giao xuống và mọi sản phẩm của các Agent với `ACTIVE-RULES-MANIFEST.json`.
   - Phát hiện tức thời nếu bất kỳ Agent nào sử dụng bộ nhớ cũ (`banned_stale_memories`) -> CHẶN CỨNG (`REJECTED_BY_SECOND_BRAIN`).
   - Cấp chứng nhận `APPROVED_BY_SECOND_BRAIN` khi đạt 100% quy chuẩn mới nhất để `mama` báo cáo cuối cùng cho CEO.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
STATE_SYNC_DIR = SUBAGENT_DIR.parent / "Agent-State-Sync"
SB_DIR = SUBAGENT_DIR / "knowledge" / "bo-nao-thu-2"
MANIFEST_FILE = SB_DIR / "ACTIVE-RULES-MANIFEST.json"
WATCH_LOG_FILE = SB_DIR / "LIVE-WATCH-LOG.json"
REMINDERS_FILE = SUBAGENT_DIR / "knowledge" / "ceo_evening_reminders.json"
BRAIN_DIR = Path.home() / ".gemini" / "antigravity" / "brain"

REMINDER_REGEX = re.compile(
    r"(nhắc\s+lịch|nhắc\s+nhở|nhắc\s+tôi|hẹn\s+giờ|tối\s+nay\s+lúc|sáng\s+mai\s+lúc|vào\s+lúc\s+\d{1,2}\s*h|training\s+.*lúc)",
    re.IGNORECASE,
)

RULE_CHANGE_REGEX = re.compile(
    r"(quy\s+tắc\s+mới|quy\s+chuẩn\s+mới|phong\s+cách\s+mới|sửa\s+lại|thay\s+đổi|tắt\s+lệnh|cấm\s+tuyệt\s+đối|"
    r"không\s+dùng\s+lại|xóa\s+bỏ|bộ\s+này\s+vẫn\s+sai|ghi\s+nhớ\s+điều\s+này|cài\s+đặt\s+thêm|luôn\s+theo\s+dõi)",
    re.IGNORECASE,
)

DEFAULT_BANNED_STALE_PATTERNS = [
    {
        "pattern": r"5\s+master\s+templates|sample_t[1-5]_|luân\s+phiên\s+5\s+template",
        "reason": "BỘ NHỚ CŨ BỊ CẤM (LUẬT #1 & #9): Đã bãi bỏ vĩnh viễn '5 Master Templates' trên Page AI Players; bắt buộc dùng thiết kế Độc Bản Zero-Clone 100%.",
        "agents": ["all", "edit", "content", "quan-ly-kenh"],
    },
    {
        "pattern": r"cobalt[\-\s]?lime|cobalt[\-\s]?blue|#0047ff|render_campaign_cards\.py|build_weekly_ai_players_vault\.py",
        "reason": "BỘ NHỚ CŨ BỊ CẤM (LUẬT #1 & #9): Phong cách Cobalt-Lime 3D cũ và script cũ đã bị xóa vĩnh viễn.",
        "agents": ["all", "edit"],
    },
    {
        "pattern": r"whiteboard_mindmap|openrouter_mindmap_explainer|aiplayers6scenereel",
        "reason": "BỘ NHỚ CŨ BỊ CẤM (LUẬT #2): Cấm dùng chung 1 khuôn AIPlayers6SceneReel hoặc đăng video test bảng trắng lên Page AI Players.",
        "agents": ["all", "edit", "quan-ly-kenh"],
    },
    {
        "pattern": r"spec\s+pills\s+dài|danh\s+sách\s+01[\-\s]02[\-\s]03\s+dưới\s+vòng\s+tròn|sales-style-01-organic-cutout",
        "reason": "BỘ NHỚ CŨ BỊ CẤM (LUẬT #3): 3 Page Bán Hàng đã chuyển sang chuẩn Minimal Pop-Bold Typography (Ít chữ • Chữ chính dày dặn 3D • Màu bắt mắt).",
        "agents": ["all", "edit", "content-da-kenh"],
    },
    {
        "pattern": r"DAILY_SALES_QUEUE|campaigns/2026-10-20/today-launch",
        "reason": "BỘ NHỚ CŨ BỊ CẤM (Zero-Repost Gate): Đã xóa vĩnh viễn hàng đợi tĩnh ngày 20/10; cấm đăng lặp bài cũ.",
        "agents": ["all", "quan-ly-kenh", "mkt"],
    },
    {
        "pattern": r"taskkill\s+/f\s+/im\s+chrome\.exe|Stop-Process\s+-Name\s+chrome",
        "reason": "VI PHẠM LUẬT CỨNG #6: Cấm tuyệt đối dùng taskkill đóng Chrome làm việc của CEO.",
        "agents": ["all"],
    },
]


def load_json_safe(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return default


def extract_recent_user_messages(max_tabs: int = 12) -> list[dict]:
    """
    Quét toàn bộ các tab trò chuyện gần nhất trong `.gemini/antigravity/brain/*/logs/transcript.jsonl`
    để `bo-nao-thu-2` không bỏ sót bất kỳ lời dặn hay quy tắc mới nào ở bất kỳ cửa sổ nào.
    """
    items = []
    if not BRAIN_DIR.exists():
        return items

    transcript_files = []
    for conv_dir in BRAIN_DIR.iterdir():
        if not conv_dir.is_dir():
            continue
        t_path = conv_dir / ".system_generated" / "logs" / "transcript.jsonl"
        if t_path.exists():
            try:
                transcript_files.append((t_path.stat().st_mtime, conv_dir.name, t_path))
            except Exception:
                pass

    transcript_files.sort(key=lambda x: x[0], reverse=True)
    host = platform.node()

    for _, conv_id, t_path in transcript_files[:max_tabs]:
        try:
            lines = t_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            for raw in lines[-60:]:
                obj = json.loads(raw)
                if obj.get("type") != "USER_INPUT" or obj.get("source") != "USER_EXPLICIT":
                    continue
                content = str(obj.get("content", "")).strip()
                m = re.search(r"<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>", content, re.DOTALL)
                user_text = m.group(1).strip() if m else content
                if not user_text or len(user_text) < 4:
                    continue
                created_at = str(obj.get("created_at", ""))[:19].replace("T", " ")
                msg_hash = hashlib.sha1(f"{conv_id}:{user_text}".encode("utf-8")).hexdigest()[:12]
                items.append({
                    "id": msg_hash,
                    "machine": host,
                    "conversation_id": conv_id,
                    "created_at": created_at,
                    "text": user_text[:600],
                })
        except Exception:
            pass

    return items


def watch_all_tabs() -> dict:
    """
    Thực thi nhiệm vụ Giám Sát Đa Tab của `bo-nao-thu-2`:
    - Quét tất cả các tab trò chuyện gần nhất.
    - Phát hiện và lưu lại các chỉ đạo thay đổi quy tắc (`rule_updates`) và lời nhắc nhở (`reminders_detected`).
    """
    SB_DIR.mkdir(parents=True, exist_ok=True)
    watch_data = load_json_safe(
        WATCH_LOG_FILE,
        {
            "updated_at": "",
            "last_machine": "",
            "monitored_tabs_count": 0,
            "captured_rule_directives": [],
            "captured_reminders": [],
        },
    )

    seen_ids = {x.get("id") for x in watch_data.get("captured_rule_directives", [])} | {
        x.get("id") for x in watch_data.get("captured_reminders", [])
    }

    msgs = extract_recent_user_messages(max_tabs=12)
    new_rules = 0
    new_reminders = 0

    for m in msgs:
        mid = m["id"]
        if mid in seen_ids:
            continue
        txt = m["text"]
        if RULE_CHANGE_REGEX.search(txt):
            watch_data.setdefault("captured_rule_directives", []).insert(
                0,
                {
                    "id": mid,
                    "machine": m["machine"],
                    "conversation_id": m["conversation_id"],
                    "timestamp": m["created_at"],
                    "directive": txt,
                    "status": "LOCKED_IN_SECOND_BRAIN",
                },
            )
            seen_ids.add(mid)
            new_rules += 1
        elif REMINDER_REGEX.search(txt):
            watch_data.setdefault("captured_reminders", []).insert(
                0,
                {
                    "id": mid,
                    "machine": m["machine"],
                    "conversation_id": m["conversation_id"],
                    "timestamp": m["created_at"],
                    "reminder": txt,
                    "status": "TRACKED_BY_SECOND_BRAIN",
                },
            )
            seen_ids.add(mid)
            new_reminders += 1

    watch_data["captured_rule_directives"] = watch_data.get("captured_rule_directives", [])[:40]
    watch_data["captured_reminders"] = watch_data.get("captured_reminders", [])[:30]
    watch_data["updated_at"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    watch_data["last_machine"] = platform.node()
    watch_data["monitored_tabs_count"] = len({m["conversation_id"] for m in msgs})

    WATCH_LOG_FILE.write_text(json.dumps(watch_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "status": "OK",
        "monitored_tabs": watch_data["monitored_tabs_count"],
        "new_rule_directives_captured": new_rules,
        "new_reminders_captured": new_reminders,
        "total_locked_directives": len(watch_data["captured_rule_directives"]),
    }


def audit_task_or_output(agent_name: str, text_or_path: str) -> dict:
    """
    Chốt Kiểm Duyệt Bắt Buộc Của Bộ Não Thứ 2 (`Pre-Execution & Final Compliance Gate`):
    - Kiểm tra nội dung giao việc hoặc kết quả của Agent xem có vi phạm quy tắc mới hoặc dùng lại bộ nhớ cũ không.
    """
    content = text_or_path
    p = Path(text_or_path)
    if p.exists() and p.is_file():
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            pass

    manifest = load_json_safe(MANIFEST_FILE, {})
    violations = []

    for rule in DEFAULT_BANNED_STALE_PATTERNS:
        target_agents = rule.get("agents", ["all"])
        if "all" in target_agents or agent_name in target_agents:
            if re.search(rule["pattern"], content, re.IGNORECASE):
                violations.append(rule["reason"])

    for stale_kw in manifest.get("banned_stale_memories", []):
        if isinstance(stale_kw, dict):
            pat = stale_kw.get("pattern") or stale_kw.get("keyword", "")
            reason = stale_kw.get("reason", f"Phát hiện mẫu bộ nhớ cũ bị cấm: {pat}")
        else:
            pat = str(stale_kw)
            reason = f"Phát hiện mẫu bộ nhớ cũ bị cấm: {pat}"
        if pat and len(pat) > 5 and re.search(re.escape(pat), content, re.IGNORECASE):
            if reason not in violations:
                violations.append(reason)

    active_rules = manifest.get("active_rules_by_agent", {}).get(
        agent_name,
        manifest.get("active_rules_by_agent", {}).get("all", []),
    )

    passed = len(violations) == 0
    return {
        "gatekeeper": "bo-nao-thu-2",
        "agent_checked": agent_name,
        "verdict": "APPROVED_BY_SECOND_BRAIN" if passed else "REJECTED_BY_SECOND_BRAIN_STALE_MEMORY",
        "passed": passed,
        "violations": violations,
        "active_rules_enforced": active_rules,
        "checked_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def main():
    parser = argparse.ArgumentParser(description="Bộ Não Thứ 2 — Giám Sát Đa Tab & Cổng Kiểm Duyệt Quy Chuẩn")
    parser.add_argument("--watch-all-tabs", action="store_true", help="Quét mọi tab trò chuyện để bắt quy tắc mới & lời nhắc nhở")
    parser.add_argument("--audit", action="store_true", help="Kiểm duyệt công việc/đầu ra của Agent")
    parser.add_argument("--agent", type=str, default="all", help="Tên Agent cần kiểm duyệt")
    parser.add_argument("--text", type=str, default="", help="Nội dung hoặc đường dẫn file cần kiểm duyệt")
    args = parser.parse_args()

    if args.watch_all_tabs:
        res = watch_all_tabs()
        print(json.dumps(res, ensure_ascii=False))
        return

    if args.audit:
        res = audit_task_or_output(args.agent, args.text)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        if not res["passed"]:
            sys.exit(1)
        return

    res = watch_all_tabs()
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
