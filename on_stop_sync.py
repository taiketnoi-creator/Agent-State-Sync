from datetime import datetime
import json
import os
import re
import subprocess
import sys

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SYNC_DIR = r"D:\Phiên bản Ai agent\Agent-State-Sync"
SUBAGENT_DIR = r"D:\Phiên bản Ai agent\Subagent"
RECENT_LOG_PATH = os.path.join(SYNC_DIR, "RECENT-CONVERSATION.md")
SUBAGENT_RECENT_LOG_PATH = os.path.join(SUBAGENT_DIR, "RECENT-CONVERSATION.md")
SNAPSHOT_SCRIPT = os.path.join(SYNC_DIR, "generate_snapshot.py")

def extract_recent_turns(transcript_path, max_turns=10):
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
                    turns.append(("USER", created, clean[:400]))
                elif stype == "PLANNER_RESPONSE" and content:
                    turns.append(("AGENT", created, content[:600]))
    except Exception:
        return []
    return turns[-max_turns:]

def update_recent_conversation(payload):
    conv_id = payload.get("conversationId", "unknown")
    t_path = payload.get("transcriptPath", "")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    turns = extract_recent_turns(t_path, max_turns=12)
    lines = [
        "# Lịch Sử Trò Chuyện Tự Động Gần Nhất (Auto-Updated After Every Turn)",
        "",
        f"- **Phiên (Conversation ID):** `{conv_id}`",
        f"- **Cập nhật tự động lúc:** `{now_str}`",
        "",
        "---",
        ""
    ]
    if turns:
        for role, ts, text in turns:
            icon = "👤 **CEO**" if role == "USER" else "🤖 **Mama (Gemini 4)**"
            lines.append(f"### {icon} ({ts})")
            lines.append(text)
            lines.append("")
    else:
        lines.append("*(Đang đồng bộ từ phiên hiện tại)*")

    text_out = "\n".join(lines)
    for path in (RECENT_LOG_PATH, SUBAGENT_RECENT_LOG_PATH):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text_out)

def trigger_background_git_sync():
    # Spawn detached background process so the chat turn finishes in <50ms with zero lag
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
            creationflags=creationflags
        )
    except Exception:
        pass

def main():
    raw = ""
    try:
        raw = sys.stdin.read()
    except Exception:
        pass

    try:
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        payload = {}

    try:
        update_recent_conversation(payload)
        trigger_background_git_sync()
    except Exception:
        pass

    # Stop hook contract: return decision != "continue" so the agent stops normally
    sys.stdout.write(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
