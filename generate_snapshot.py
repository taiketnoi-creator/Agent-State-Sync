from datetime import datetime
import json
import os
import platform
import shutil
import sqlite3
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DB_PATH = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "scratch", "ai-aff-video-system", "data", "aff_system.db")
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
]


def sync_file_pair(p_sub: str, p_sync: str):
    os.makedirs(os.path.dirname(p_sub), exist_ok=True)
    os.makedirs(os.path.dirname(p_sync), exist_ok=True)
    if os.path.exists(p_sub) and os.path.exists(p_sync):
        if os.path.getmtime(p_sub) > os.path.getmtime(p_sync) + 0.5:
            shutil.copy2(p_sub, p_sync)
        elif os.path.getmtime(p_sync) > os.path.getmtime(p_sub) + 0.5:
            shutil.copy2(p_sync, p_sub)
    elif os.path.exists(p_sync) and not os.path.exists(p_sub):
        shutil.copy2(p_sync, p_sub)
    elif os.path.exists(p_sub) and not os.path.exists(p_sync):
        shutil.copy2(p_sub, p_sync)


def sync_tree_by_ext(rel_root: str, exts=(".md",)):
    """Mirror lightweight text/code files under rel_root between Subagent and Agent-State-Sync."""
    sub_root = os.path.join(SUBAGENT_DIR, rel_root)
    sync_root = os.path.join(SYNC_DIR, rel_root)
    rel_paths = set()
    for base in (sub_root, sync_root):
        if not os.path.exists(base):
            continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [
                d for d in dirs
                if d not in ("__pycache__", "node_modules", ".git", "out", "assets", "images", "raw_scenes", "outputs", "keyframes_v1", "qa-frames")
            ]
            for f in files:
                if f.lower().endswith(exts):
                    full_p = os.path.join(root, f)
                    rel_p = os.path.relpath(full_p, base)
                    rel_paths.add(rel_p)
    for rel_p in sorted(rel_paths):
        sync_file_pair(os.path.join(sub_root, rel_p), os.path.join(sync_root, rel_p))


def sync_bidirectional():
    """Keep lightweight state files, 10 Agent definitions, training, knowledge, skills, tools, and campaign .md docs mirrored."""
    for fname in SYNC_FILES:
        p_sub = os.path.join(SUBAGENT_DIR, fname)
        p_sync = os.path.join(SYNC_DIR, fname)
        sync_file_pair(p_sub, p_sync)
    sync_tree_by_ext("training", (".md", ".json"))
    sync_tree_by_ext("knowledge", (".md", ".json"))
    sync_tree_by_ext(os.path.join(".agents", "skills"), (".md", ".py", ".json"))
    sync_tree_by_ext("tools", (".py", ".bat", ".ps1"))
    sync_tree_by_ext("campaigns", (".md", ".csv"))


def main():
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
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id, name, niche, score, commission, status FROM products ORDER BY id DESC LIMIT 10")
        db_data["products"] = [dict(r) for r in cur.fetchall()]
        cur.execute("SELECT id, title, status, platforms FROM video_jobs ORDER BY id DESC LIMIT 10")
        db_data["video_jobs"] = [dict(r) for r in cur.fetchall()]
        conn.close()

    camp_lines = "\n".join(f"- `{c}`" for c in campaigns) if campaigns else "- *(Chưa có chiến dịch)*"
    json_block = json.dumps(db_data, ensure_ascii=False, indent=2)

    md = f"""# Bản Chụp Trạng Thái Tự Động (Lightweight State Snapshot)

- **Cập nhật lần cuối:** `{now_str}`
- **Máy thực hiện:** `{host}`

## 1. Các Thư Mục Chiến Dịch Hiện Có (`D:\\Phiên bản Ai agent\\Subagent\\campaigns`)
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

    sync_bidirectional()
    print("Updated STATE-SNAPSHOT.md and mirrored state files between Subagent and Agent-State-Sync.")


if __name__ == "__main__":
    main()
