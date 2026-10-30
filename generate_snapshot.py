import argparse
from datetime import datetime
import hashlib
import json
import os
import platform
import shutil
import sqlite3
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DB_PATH = os.path.join(
    os.path.expanduser("~"),
    ".gemini",
    "antigravity",
    "scratch",
    "ai-aff-video-system",
    "data",
    "aff_system.db",
)
SYNC_DIR = os.path.dirname(os.path.abspath(__file__))
SUBAGENT_DIR = os.path.join(os.path.dirname(SYNC_DIR), "Subagent")

SYNC_FILES = [
    "PROJECT-BLUEPRINT.md",
    "WORK-HISTORY.md",
    "SOFTWARE-CHANGELOG.md",
    "RECENT-CONVERSATION.md",
    "STATE-SNAPSHOT.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "HUONG-DAN-SU-DUNG.md",
    "HUONG-DAN-CAI-DAT-MAY-MOI.md",
    "skills-manifest.md",
    "mama.md",
    "mkt.md",
    "content.md",
    "edit.md",
    "voice.md",
    "content-da-kenh.md",
    "quan-ly-kenh.md",
    "cham-soc-kenh.md",
    "hieu-suat.md",
    "bo-nao-thu-2.md",
    "sync-light.ps1",
    "on_stop_sync.py",
    os.path.join(".agents", "GEMINI.md"),
    os.path.join(".agents", "hooks.json"),
]


def _file_sha256(path: str) -> str:
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""


def sync_file_pair(p_sub: str, p_sync: str, direction: str = "auto"):
    """
    direction:
      - 'pull': Git (Agent-State-Sync) is source of truth -> copy p_sync to p_sub whenever different.
      - 'push': Workspace (Subagent) is source of truth -> copy p_sub to p_sync whenever different.
      - 'auto': Compare mtime when hashes differ.
    """
    os.makedirs(os.path.dirname(p_sub), exist_ok=True)
    os.makedirs(os.path.dirname(p_sync), exist_ok=True)

    sub_exists = os.path.exists(p_sub)
    sync_exists = os.path.exists(p_sync)

    if sub_exists and sync_exists:
        if _file_sha256(p_sub) == _file_sha256(p_sync):
            return
        if direction == "pull":
            shutil.copy2(p_sync, p_sub)
        elif direction == "push":
            shutil.copy2(p_sub, p_sync)
        else:
            if os.path.getmtime(p_sub) > os.path.getmtime(p_sync) + 0.5:
                shutil.copy2(p_sub, p_sync)
            elif os.path.getmtime(p_sync) > os.path.getmtime(p_sub) + 0.5:
                shutil.copy2(p_sync, p_sub)
            else:
                shutil.copy2(p_sub, p_sync)
    elif sync_exists and not sub_exists:
        shutil.copy2(p_sync, p_sub)
    elif sub_exists and not sync_exists:
        shutil.copy2(p_sub, p_sync)


def sync_tree_by_ext(rel_root: str, exts=(".md",), direction: str = "auto", allow_test_samples: bool = False):
    """Mirror lightweight text/code files under rel_root between Subagent and Agent-State-Sync."""
    sub_root = os.path.join(SUBAGENT_DIR, rel_root)
    sync_root = os.path.join(SYNC_DIR, rel_root)
    rel_paths = set()
    skip_dirs = {
        "__pycache__",
        "node_modules",
        ".git",
        "out",
        "assets",
        "images",
        "raw_scenes",
        "outputs",
        "keyframes_v1",
        "qa-frames",
        "videos",
    }
    for base in (sub_root, sync_root):
        if not os.path.exists(base):
            continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            is_test_samples = allow_test_samples and os.path.basename(root).lower() == "test_samples"
            for f in files:
                fl = f.lower()
                if exts is None or fl.endswith(exts) or (is_test_samples and fl.endswith((".jpg", ".png"))):
                    full_p = os.path.join(root, f)
                    rel_p = os.path.relpath(full_p, base)
                    rel_paths.add(rel_p)
    for rel_p in sorted(rel_paths):
        sync_file_pair(os.path.join(sub_root, rel_p), os.path.join(sync_root, rel_p), direction=direction)


def sync_bidirectional(direction: str = "auto"):
    """Keep lightweight state files, 10 Agent definitions, .agents/GEMINI.md, hooks.json, ALL training files, knowledge, skills, tools, style reference assets, and campaign docs mirrored."""
    for fname in SYNC_FILES:
        p_sub = os.path.join(SUBAGENT_DIR, fname)
        p_sync = os.path.join(SYNC_DIR, fname)
        sync_file_pair(p_sub, p_sync, direction=direction)
    sync_tree_by_ext("training", None, direction=direction)
    sync_tree_by_ext("knowledge", (".md", ".json"), direction=direction)
    sync_tree_by_ext(os.path.join(".agents", "skills"), (".md", ".py", ".json"), direction=direction)
    sync_tree_by_ext(os.path.join(".agents", "plugins"), (".md", ".json", ".svg"), direction=direction)
    sync_tree_by_ext("tools", (".py", ".bat", ".ps1", ".html", ".css", ".json", ".js"), direction=direction)
    sync_tree_by_ext(os.path.join("assets", "sales-pages-image-styles"), (".jpg", ".jpeg", ".png", ".webp", ".md", ".json"), direction=direction)
    sync_tree_by_ext("campaigns", (".md", ".csv", ".json", ".html"), direction=direction, allow_test_samples=True)


def main():
    parser = argparse.ArgumentParser(description="Bidirectional State Snapshot & File Mirror")
    parser.add_argument(
        "--direction",
        choices=["auto", "pull", "push"],
        default="auto",
        help="pull = Agent-State-Sync -> Subagent; push = Subagent -> Agent-State-Sync; auto = mtime",
    )
    args = parser.parse_args()

    # Sync files first according to direction so STATE-SNAPSHOT reflects latest state
    sync_bidirectional(direction=args.direction)

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    host = platform.node()

    camp_dir = os.path.join(SUBAGENT_DIR, "campaigns")
    campaigns = []
    if os.path.exists(camp_dir):
        campaigns = sorted([
            d for d in os.listdir(camp_dir)
            if os.path.isdir(os.path.join(camp_dir, d))
        ])

    db_data = {"products": [], "video_jobs": []}
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT id, name, niche, score, commission, status FROM products ORDER BY id DESC LIMIT 10")
            db_data["products"] = [dict(r) for r in cur.fetchall()]
            cur.execute("SELECT id, title, status, platforms FROM video_jobs ORDER BY id DESC LIMIT 10")
            db_data["video_jobs"] = [dict(r) for r in cur.fetchall()]
            conn.close()
        except Exception:
            pass

    camp_lines = "\n".join(f"- `{c}`" for c in campaigns) if campaigns else "- *(Chưa có chiến dịch)*"
    json_block = json.dumps(db_data, ensure_ascii=False, indent=2)

    md = f"""# Bản Chụp Trạng Thái Tự Động (Lightweight State Snapshot)

- **Cập nhật lần cuối:** `{now_str}`
- **Máy thực hiện:** `{host}` (`{SUBAGENT_DIR}`)

## 1. Các Thư Mục Chiến Dịch Hiện Có (`Subagent/campaigns`)
{camp_lines}

## 2. Tóm Tắt Dữ Liệu SQLite Local (Top 10 Mới Nhất — Không Cần Đẩy File `.db`)
```json
{json_block}
```
"""
    for target_dir in (SYNC_DIR, SUBAGENT_DIR):
        if os.path.exists(target_dir):
            with open(os.path.join(target_dir, "STATE-SNAPSHOT.md"), "w", encoding="utf-8") as f:
                f.write(md)

    print(f"Updated STATE-SNAPSHOT.md and mirrored state files (direction={args.direction}).")


if __name__ == "__main__":
    main()
