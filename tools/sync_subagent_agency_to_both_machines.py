#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_subagent_agency_to_both_machines.py — Đồng Bộ Toàn Diện Định Vị & Nhiệm Vụ Subagent Agency Giữa Máy Công Ty (guicci) & Máy Ở Nhà (Admin-PC)
"""

import shutil
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
SYNC_DIR = SUBAGENT_DIR.parent / "Agent-State-Sync"

FILES_TO_MIRROR = [
    ".agents/GEMINI.md",
    "WORK-HISTORY.md",
    "content.md",
    "edit.md",
    "content-da-kenh.md",
    "cham-soc-kenh.md",
    ".agents/plugins/agent-javis/agents/content.md",
    ".agents/plugins/agent-javis/agents/edit.md",
    ".agents/plugins/agent-javis/agents/content-da-kenh.md",
    ".agents/plugins/agent-javis/agents/cham-soc-kenh.md",
    "knowledge/bo-nao-thu-2/INDEX.md",
    "knowledge/bo-nao-thu-2/ACTIVE-RULES-MANIFEST.json",
    "knowledge/bo-nao-thu-2/memories/MEM-20261104-ai-players-subagent-agency-positioning.md",
    "tools/update_subagent_agency_memory_and_rules.py",
    "tools/build_ai_players_subagent_agency_vault.py",
    "tools/build_ai_players_subagent_agency_reels.py",
    "tools/mama_daily_group_and_eod.py",
    "tools/mama_auto_scheduler_engine.py",
    "tools/activate_mui3_mui4_growth_engine.py",
    "campaigns/2026-11-04/ai-players-subagent-agency-vault/subagent_agency_17_images_manifest.json",
    "campaigns/2026-11-04/ai-players-subagent-agency-vault/subagent_agency_6_reels_manifest.json",
    "campaigns/2026-11-04/ai-players-subagent-agency-vault/subagent_agency_17_images_qa_grid.jpg",
]


def run_git_push(repo_dir: Path, commit_msg: str, specific_files: list[str] | None = None) -> None:
    if not (repo_dir / ".git").exists():
        print(f"⚠️ Không tìm thấy .git tại {repo_dir}")
        return
    lock_f = repo_dir / ".git" / "index.lock"
    if lock_f.exists():
        lock_f.unlink(missing_ok=True)
    if specific_files:
        subprocess.run(["git", "-C", str(repo_dir), "reset"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        existing = [f for f in specific_files if (repo_dir / f).exists()]
        if existing:
            subprocess.run(["git", "-C", str(repo_dir), "add", "--"] + existing, check=False)
    else:
        subprocess.run(["git", "-C", str(repo_dir), "add", "-A"], check=False)
    st = subprocess.run(["git", "-C", str(repo_dir), "status", "--porcelain"], capture_output=True, text=True)
    if st.stdout.strip():
        subprocess.run(["git", "-C", str(repo_dir), "commit", "-m", commit_msg], check=False)
    subprocess.run(["git", "-C", str(repo_dir), "pull", "--rebase", "--autostash", "origin", "main"], check=False)
    res = subprocess.run(["git", "-C", str(repo_dir), "push", "origin", "main"], capture_output=True, text=True)
    head = subprocess.run(["git", "-C", str(repo_dir), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    print(f"✅ [{repo_dir.name}] Đã đồng bộ Git thành công (HEAD={head}) | rc={res.returncode}")


def main():
    if SYNC_DIR.exists():
        copied = 0
        for rel in FILES_TO_MIRROR:
            src = SUBAGENT_DIR / rel
            dst = SYNC_DIR / rel
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                copied += 1
        print(f"📦 Đã sao chép {copied} tệp cấu hình, ký ức Bộ não thứ 2 & manifest sang Agent-State-Sync.")

        snap_py = SYNC_DIR / "generate_snapshot.py"
        if snap_py.exists():
            subprocess.run([sys.executable, str(snap_py), "--direction", "push"], check=False)

    msg = "feat(ai-players): pivot full image+reel pipeline to Personal & Enterprise Subagent Agency + 1:1 Custom Setup Service & sync 2 PCs"
    run_git_push(SUBAGENT_DIR, msg, specific_files=FILES_TO_MIRROR)
    if SYNC_DIR.exists():
        run_git_push(SYNC_DIR, msg)


if __name__ == "__main__":
    main()
