#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import shutil
from pathlib import Path

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = SUBAGENT_DIR / "campaigns" / "2026-10-26" / "ai-players-weekly-vault" / "images"
TEST_DIR = Path(r"c:\Users\guicci\Downloads\vid\test_ai_players")
ART_DIR = Path(r"C:\Users\guicci\.gemini\antigravity\brain\6e438316-f5a0-4933-a2dd-bc3802a26c0d\bespoke_check")

TEST_DIR.mkdir(parents=True, exist_ok=True)
ART_DIR.mkdir(parents=True, exist_ok=True)

MAPPING = {
    "day1_img1_1415_repo.jpg": "test1_browser_use_showcase.jpg",
    "day2_img1_0830_artifacts.jpg": "test2_claude_artifacts.jpg",
    "day3_img5_1815_mcpserver.jpg": "test3_mcp_protocol.jpg",
    "day4_img1_0830_cursor.jpg": "test4_cursor_windsurf.jpg",
    "day1_img2_1545_voice.jpg": "test5_benchmark_matrix.jpg",
    "day2_img6_2115_n8nhub.jpg": "test6_n8n_bento_steps.jpg",
    "day1_img6_2145_abcd.jpg": "test7_community_poll.jpg",
    "day1_img5_2045_hethong.jpg": "test8_system_blueprint.jpg",
    "day1_img3_1715_prompt50.jpg": "test9_playbook_vault.jpg",
    "day7_img5_1815_eodreport.jpg": "test10_weekly_telemetry.jpg",
}

for src_name, dst_name in MAPPING.items():
    src = IMAGES_DIR / src_name
    if src.exists():
        shutil.copy2(src, TEST_DIR / dst_name)
        shutil.copy2(src, ART_DIR / src_name)
print("Copied 10 bespoke showcase samples to Downloads\\vid\\test_ai_players and artifact dir!")
