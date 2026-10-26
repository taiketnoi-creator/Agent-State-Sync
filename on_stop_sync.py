from datetime import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SYNC_DIR = os.path.dirname(os.path.abspath(__file__))
SUBAGENT_DIR = os.path.join(os.path.dirname(SYNC_DIR), "Subagent")
RECENT_LOG_PATH = os.path.join(SYNC_DIR, "RECENT-CONVERSATION.md")
SUBAGENT_RECENT_LOG_PATH = os.path.join(SUBAGENT_DIR, "RECENT-CONVERSATION.md")


def resolve_transcript_path(payload: dict) -> tuple[str, str]:
    conv_id = payload.get("conversationId", "")
    t_path = payload.get("transcriptPath", "")
    if t_path and os.path.exists(t_path):
        return conv_id or "active", t_path
    brain_root = Path.home() / ".gemini" / "antigravity" / "brain"
    if conv_id:
        candidate = brain_root / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
        if candidate.exists():
            return conv_id, str(candidate)
    if brain_root.exists():
        candidates = list(brain_root.glob("*/.system_generated/logs/transcript.jsonl"))
        candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        for c in candidates[:8]:
            try:
                head_txt = c.read_text(encoding="utf-8", errors="ignore")[:25000]
                if "Subagent" in head_txt or "mama" in head_txt.lower() or "page ai" in head_txt.lower():
                    return c.parent.parent.parent.name, str(c)
            except Exception:
                continue
    return conv_id or "unknown", ""


def extract_recent_turns(transcript_path, max_turns=12):
    if not transcript_path or not os.path.exists(transcript_path):
        return []
    turns = []
    try:
        with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                stype = obj.get("type", "")
                content = (obj.get("content") or "").strip()
                created = obj.get("created_at", "")[:19].replace("T", " ")
                if stype == "USER_INPUT" and content:
                    clean = re.sub(r"<ADDITIONAL_METADATA>.*?</ADDITIONAL_METADATA>", "", content, flags=re.DOTALL)
                    clean = re.sub(r"<USER_SETTINGS_CHANGE>.*?</USER_SETTINGS_CHANGE>", "", clean, flags=re.DOTALL)
                    clean = clean.replace("<USER_REQUEST>", "").replace("</USER_REQUEST>", "").strip()
                    if clean:
                        turns.append(("USER", created, clean[:500]))
                elif stype == "PLANNER_RESPONSE" and content:
                    turns.append(("AGENT", created, content[:700]))
    except Exception:
        return []
    return turns[-max_turns:]


def update_recent_conversation(payload):
    conv_id, t_path = resolve_transcript_path(payload)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    turns = extract_recent_turns(t_path, max_turns=12)
    if not turns:
        return

    lines = [
        "# Lịch Sử Trò Chuyện Tự Động Gần Nhất (Auto-Updated After Every Turn)",
        "",
        f"- **Phiên (Conversation ID):** `{conv_id}`",
        f"- **Cập nhật tự động lúc:** `{now_str}`",
        "",
        "---",
        "",
    ]
    for role, ts, text in turns:
        icon = "👤 **CEO**" if role == "USER" else "🤖 **Mama (Gemini 4)**"
        lines.append(f"### {icon} ({ts})")
        lines.append(text)
        lines.append("")

    text_out = "\n".join(lines)
    for path in (RECENT_LOG_PATH, SUBAGENT_RECENT_LOG_PATH):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text_out)


def trigger_background_git_sync():
    cmd = (
        f'powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File '
        f'"{os.path.join(SYNC_DIR, "sync-light.ps1")}" -Mode finish '
        f'-Message "Auto-sync sau luot tro chuyen"'
    )
    creationflags = getattr(subprocess, "DETACHED_PROCESS", 0x00000008) | getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
    try:
        subprocess.Popen(
            cmd,
            cwd=SYNC_DIR,
            shell=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
            creationflags=creationflags,
        )
    except Exception:
        pass


def main():
    payload = {}
    try:
        update_recent_conversation(payload)
        trigger_background_git_sync()
    except Exception:
        pass

    sys.stdout.write(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
