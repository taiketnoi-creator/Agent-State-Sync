from datetime import datetime
import json
import os
import platform
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


def extract_turns_from_transcript(transcript_path: str, max_turns: int = 8) -> tuple[str, list]:
    """Return (last_timestamp, list of (role, ts, text)) for a main user conversation."""
    if not transcript_path or not os.path.exists(transcript_path):
        return "", []
    turns = []
    has_direct_user_request = False
    last_ts = ""
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
                    if "<USER_REQUEST>" in content:
                        has_direct_user_request = True
                    clean = re.sub(r"<ADDITIONAL_METADATA>.*?</ADDITIONAL_METADATA>", "", content, flags=re.DOTALL)
                    clean = re.sub(r"<USER_SETTINGS_CHANGE>.*?</USER_SETTINGS_CHANGE>", "", clean, flags=re.DOTALL)
                    clean = clean.replace("<USER_REQUEST>", "").replace("</USER_REQUEST>", "").strip()
                    if clean:
                        turns.append(("USER", created, clean[:600]))
                        if created > last_ts:
                            last_ts = created
                elif stype == "PLANNER_RESPONSE" and content:
                    turns.append(("AGENT", created, content[:900]))
                    if created > last_ts:
                        last_ts = created
    except Exception:
        return "", []
    if not has_direct_user_request:
        return "", []
    return last_ts, turns[-max_turns:]


def collect_local_conversations(payload: dict, max_sessions: int = 3) -> list[dict]:
    """Scan local Antigravity brain directory for the most recent CEO conversations across all open tabs."""
    brain_root = Path.home() / ".gemini" / "antigravity" / "brain"
    host = platform.node()
    sessions = []
    seen_ids = set()

    # 1. Check payload conversation first if provided
    p_cid = payload.get("conversationId", "")
    p_path = payload.get("transcriptPath", "")
    if p_cid and not p_path and brain_root.exists():
        cand = brain_root / p_cid / ".system_generated" / "logs" / "transcript.jsonl"
        if cand.exists():
            p_path = str(cand)
    if p_path and os.path.exists(p_path):
        last_ts, turns = extract_turns_from_transcript(p_path, max_turns=8)
        if turns:
            cid = p_cid or Path(p_path).parent.parent.parent.name
            seen_ids.add(cid)
            sessions.append({"conv_id": cid, "host": host, "last_ts": last_ts, "turns": turns})

    # 2. Scan all recent transcripts in brain_root
    if brain_root.exists():
        candidates = list(brain_root.glob("*/.system_generated/logs/transcript.jsonl"))
        candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        for c in candidates[:15]:
            cid = c.parent.parent.parent.name
            if cid in seen_ids:
                continue
            last_ts, turns = extract_turns_from_transcript(str(c), max_turns=8)
            if turns:
                seen_ids.add(cid)
                sessions.append({"conv_id": cid, "host": host, "last_ts": last_ts, "turns": turns})
            if len(sessions) >= max_sessions:
                break

    sessions.sort(key=lambda s: s["last_ts"], reverse=True)
    return sessions[:max_sessions]


def parse_existing_other_host_sections(current_host: str) -> list[str]:
    """Preserve conversation blocks recorded by OTHER machines (e.g. guicci vs Admin-PC) so cross-machine history is never lost."""
    source_path = RECENT_LOG_PATH if os.path.exists(RECENT_LOG_PATH) else SUBAGENT_RECENT_LOG_PATH
    if not os.path.exists(source_path):
        return []
    try:
        text = Path(source_path).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    blocks = re.split(r"(?=^## 💻 Phiên Trò Chuyện: )", text, flags=re.MULTILINE)
    kept = []
    for b in blocks:
        if not b.startswith("## 💻 Phiên Trò Chuyện: "):
            continue
        if f"| Máy: `{current_host}`" not in b:
            kept.append(b.strip())
    return kept[:2]


def update_recent_conversation(payload: dict):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    host = platform.node()
    local_sessions = collect_local_conversations(payload, max_sessions=3)
    other_host_blocks = parse_existing_other_host_sections(host)

    if not local_sessions and not other_host_blocks:
        return

    lines = [
        "# Lịch Sử Trò Chuyện Đa Máy & Đa Cửa Sổ Gần Nhất (Cross-Machine Auto-Sync)",
        "",
        f"- **Cập nhật tự động lúc:** `{now_str}`",
        f"- **Máy cập nhật cuối:** `{host}` (`{SUBAGENT_DIR}`)",
        "- **Cơ chế:** Tự động gom lịch sử từ tất cả các cửa sổ chat gần nhất của CEO trên cả **Máy Công Ty (`guicci`)** và **Máy Ở Nhà (`Admin-PC`)**.",
        "",
        "---",
        "",
    ]

    for sess in local_sessions:
        lines.append(
            f"## 💻 Phiên Trò Chuyện: `{sess['conv_id']}` | Máy: `{sess['host']}` | Hoạt động cuối: `{sess['last_ts']}`"
        )
        lines.append("")
        for role, ts, text in sess["turns"]:
            icon = "👤 **CEO**" if role == "USER" else "🤖 **Mama (Gemini 4)**"
            lines.append(f"### {icon} ({ts})")
            lines.append(text)
            lines.append("")
        lines.append("---")
        lines.append("")

    for block in other_host_blocks:
        lines.append(block)
        lines.append("")

    text_out = "\n".join(lines).strip() + "\n"
    for path in (RECENT_LOG_PATH, SUBAGENT_RECENT_LOG_PATH):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text_out)


def run_git_sync_worker():
    """Thực thi đồng bộ Git thuần Python (miễn nhiễm 100% với lỗi PowerShell NativeCommandError và chống đụng độ .git/index.lock)."""
    import time

    lock_path = os.path.join(SYNC_DIR, ".git_sync_lock.json")
    now_ts = time.time()
    try:
        if os.path.exists(lock_path):
            ldata = json.loads(Path(lock_path).read_text(encoding="utf-8", errors="ignore"))
            if now_ts - float(ldata.get("ts", 0)) < 15.0:
                return
        Path(lock_path).write_text(json.dumps({"ts": now_ts}), encoding="utf-8")
    except Exception:
        pass

    host = platform.node()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    snapshot_py = os.path.join(SYNC_DIR, "generate_snapshot.py")
    creationflags = 0x08000000 if os.name == "nt" else 0

    try:
        # 1. Đẩy các thay đổi mới từ Subagent -> Agent-State-Sync
        subprocess.run(
            [sys.executable, snapshot_py, "--direction", "push"],
            cwd=SYNC_DIR,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=20,
            creationflags=creationflags,
        )
        # 2. Add & Commit local trước
        subprocess.run(
            ["git", "-C", SYNC_DIR, "add", "-A"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
            creationflags=creationflags,
        )
        diff_res = subprocess.run(
            ["git", "-C", SYNC_DIR, "diff", "--cached", "--quiet"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
            creationflags=creationflags,
        )
        if diff_res.returncode != 0:
            subprocess.run(
                ["git", "-C", SYNC_DIR, "commit", "-m", f"Auto-sync ({host} @ {now_str})"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10,
                creationflags=creationflags,
            )
        # 3. Pull --rebase từ GitHub
        subprocess.run(
            ["git", "-C", SYNC_DIR, "pull", "--rebase", "--autostash", "origin", "main"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=20,
            creationflags=creationflags,
        )
        # 4. Đồng bộ các file mới kéo về ngược lại Subagent
        subprocess.run(
            [sys.executable, snapshot_py, "--direction", "pull"],
            cwd=SYNC_DIR,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=20,
            creationflags=creationflags,
        )
        # 5. Push lên GitHub
        subprocess.run(
            ["git", "-C", SYNC_DIR, "push", "-u", "origin", "main"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=20,
            creationflags=creationflags,
        )
    except Exception:
        pass


def trigger_background_git_sync():
    creationflags = getattr(subprocess, "DETACHED_PROCESS", 0x00000008) | getattr(
        subprocess, "CREATE_NO_WINDOW", 0x08000000
    )
    try:
        subprocess.Popen(
            [sys.executable, os.path.abspath(__file__), "--background-sync"],
            cwd=SYNC_DIR,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
            creationflags=creationflags,
        )
    except Exception:
        pass


def main():
    if "--background-sync" in sys.argv:
        run_git_sync_worker()
        return

    payload = {}
    try:
        if not sys.stdin.isatty():
            raw_in = sys.stdin.read().strip()
            if raw_in:
                payload = json.loads(raw_in)
    except Exception:
        payload = {}

    # Chỉ chạy đồng bộ Git khi phiên thực sự đã hoàn tất (fullyIdle != False)
    # nhằm tránh đụng độ .git/index.lock khi Mama đang chờ Subagent hoặc Background Task chạy song song.
    is_fully_idle = payload.get("fullyIdle", True)
    try:
        if is_fully_idle:
            update_recent_conversation(payload)
            trigger_background_git_sync()
    except Exception:
        pass

    sys.stdout.write(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
