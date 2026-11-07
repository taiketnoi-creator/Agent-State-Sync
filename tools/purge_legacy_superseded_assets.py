#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
purge_legacy_superseded_assets.py — Công cụ Xóa Sạch Tư Liệu, Ảnh/Video Cũ & Script Lỗi Thời
(Thực thi Luật #9 của CEO: Khi có thay đổi/quy chuẩn mới, xóa bỏ hoàn toàn tư liệu và code cũ
để không một Agent hay Script nào có thể lấy nhầm nội dung cũ ra tái sử dụng).
"""

import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_SELF_SUBAGENT = Path(__file__).resolve().parent.parent
_SELF_SYNC = _SELF_SUBAGENT.parent / "Agent-State-Sync"

WORKSPACES = [
    _SELF_SUBAGENT,
    _SELF_SYNC,
    Path(r"d:\Phiên bản Ai agent\Subagent"),
    Path(r"d:\Phiên bản Ai agent\Agent-State-Sync"),
    Path(r"f:\Ai Agent Setup\SubAgent\Subagent"),
    Path(r"f:\Ai Agent Setup\SubAgent\Agent-State-Sync"),
]

# 1. Các thư mục chiến dịch & mẫu ảnh/video cũ đã bị thay thế bởi quy chuẩn mới
OBSOLETE_DIRS = [
    "assets/ai-players-image-styles",  # Style Cobalt cũ & ảnh mặt người đã bị cấm
    "campaigns/2026-10-10",
    "campaigns/2026-10-12",
    "campaigns/2026-10-13",
    "campaigns/2026-10-14",
    "campaigns/2026-10-15",
    "campaigns/2026-10-20",
    "campaigns/2026-10-21",
    "campaigns/2026-10-22",
    "campaigns/2026-10-23",
    "campaigns/2026-10-24",
    "campaigns/2026-10-26",  # Toàn bộ lô bespoke21 cũ (Reel01..Reel21) đã xuất bản 27/10-30/10
    "campaigns/2026-11-04/ai-players-subagent-agency-vault/golden_video_slides",  # Lô re-render Reel01..17 cũ bị cấm
    "campaigns/2026-11-04/ai-players-subagent-agency-vault/reels",
    "templates/remotion-cuongit-template/build-bespoke-21-vault",
    "templates/remotion-cuongit-template/public/audio/bespoke26",
    "templates/remotion-cuongit-template/src/AiHallucinationShort",
    "templates/remotion-cuongit-template/src/DevOpsSysadmin",
    "templates/remotion-cuongit-template/src/DockerExplainer",
    "templates/remotion-cuongit-template/src/McpShort",
    "templates/remotion-cuongit-template/src/WhiteboardMindmap",
    "templates/remotion-cuongit-template/src/Reel01DeepResearch",
    "templates/remotion-cuongit-template/src/Reel02ZeroShotVoice",
    "templates/remotion-cuongit-template/src/Reel03GraphRagMatrix",
    "templates/remotion-cuongit-template/src/Reel04StructuredJson",
    "templates/remotion-cuongit-template/src/Reel05VisionOcrParser",
    "templates/remotion-cuongit-template/src/Reel06PromptCaching",
    "templates/remotion-cuongit-template/src/Reel07VoiceToAction",
    "templates/remotion-cuongit-template/src/Reel08CodeSandboxExec",
    "templates/remotion-cuongit-template/src/Reel09SelfHealingWorkflow",
    "templates/remotion-cuongit-template/src/Reel10CompetitorAdSpy",
    "templates/remotion-cuongit-template/src/Reel11SmallLanguageModel",
    "templates/remotion-cuongit-template/src/Reel12SemanticSearchVector",
    "templates/remotion-cuongit-template/src/Reel13PromptInjectionShield",
    "templates/remotion-cuongit-template/src/Reel14SyntheticDataGen",
    "templates/remotion-cuongit-template/src/Reel15BatchApiOvernight",
    "templates/remotion-cuongit-template/src/Reel16SpeculativeDecoding",
    "templates/remotion-cuongit-template/src/Reel17CustomerIntentRouter",
    "templates/remotion-cuongit-template/src/Reel18AutomatedAbTesting",
    "templates/remotion-cuongit-template/src/Reel19LongContextNeedle",
    "templates/remotion-cuongit-template/src/Reel20ZeroTouchOnboarding",
    "templates/remotion-cuongit-template/src/Reel21AutonomousKpiAudit",
]

# 2. Các file lẻ (ảnh style cũ, tài liệu cũ, script sinh video trùng khuôn cũ) cần xóa vĩnh viễn
OBSOLETE_FILES = [
    "assets/sales-pages-image-styles/sales-style-01-organic-cutout-card.jpg",
    "knowledge/personal-brand-visual-reference.md",
    "tools/render_and_schedule_6_subagent_golden_video_slides.py",
    "tools/render_and_schedule_remaining_18_golden_reels.py",
    "tools/fix_and_publish_21_reels_now.py",
    "tools/build_18_truly_bespoke_zero_clone_reels.py",
    "tools/rebuild_remaining_18_golden_reels_data.py",
    "tools/generate_day1_day2_new_voices.py",
    "tools/delete_19_clone_reels.py",
    "tools/audit_21_reels_completeness.py",
    "tools/check_reels_status.py",
    "tools/build_ai_players_subagent_agency_reels.py",
    "tools/rebuild_remaining_18_golden_reels.py",
    "tools/apply_golden_bespoke_fix_all_21.py",
    "tools/assemble_weekly_ai_players_vault.py",
    "tools/build_ai_players_4day_vault.py",
    "tools/build_remaining_8_weekly_reels.py",
    "tools/build_weekly_ai_players_vault.py",
    "tools/deploy_fresh_today_ai_players.py",
    "tools/fb_morning_2210_seeder.py",
    "tools/publish_today_3_verified_reels.py",
    "tools/publish_wave3_and_full_seed.py",
    "tools/render_and_schedule_ai_vault.py",
    "tools/render_and_schedule_weekly_19_reels.py",
    "tools/render_campaign_cards.py",
    "tools/render_qa_and_schedule_21_bespoke_reels.py",
    "tools/render_test_batch.py",
    "tools/render_today_3_from_bundle.py",
    "tools/rerender_tpl1.py",
    "tools/schedule_ai_players_queue.py",
    "tools/schedule_today_ai_players.py",
    "tools/schedule_weekly_batch.py",
    "tools/test_bespoke_6cards.py",
    "tools/test_vp.py",
    "tools/generate_weekly_vid_vault.py",
    "tools/send_clean_page_report_tele.py",
    "campaigns/2026-10-30/test_samples/sample_t1_hero.jpg",
    "campaigns/2026-10-30/test_samples/sample_t2_curriculum.jpg",
    "campaigns/2026-10-30/test_samples/sample_t3_feature_matrix.jpg",
    "campaigns/2026-10-30/test_samples/sample_t4_offer_card.jpg",
    "campaigns/2026-10-30/test_samples/sample_t5_urgency.jpg",
    "campaigns/2026-11-04/ai-players-subagent-agency-vault/subagent_agency_6_reels_manifest.json",
]


def clean_root_tsx(ws: Path) -> bool:
    root_tsx = ws / "templates" / "remotion-cuongit-template" / "src" / "Root.tsx"
    if not root_tsx.exists():
        return False
    lines = root_tsx.read_text(encoding="utf-8").splitlines()
    banned_tokens = (
        "DockerExplainer",
        "DevOpsSysadmin",
        "McpExplainer",
        "McpShort",
        "WhiteboardMindmap",
        "AiHallucination",
        "Reel01",
        "Reel02",
        "Reel03",
        "Reel04",
        "Reel05",
        "Reel06",
        "Reel07",
        "Reel08",
        "Reel09",
        "Reel10",
        "Reel11",
        "Reel12",
        "Reel13",
        "Reel14",
        "Reel15",
        "Reel16",
        "Reel17",
        "Reel18",
        "Reel19",
        "Reel20",
        "Reel21",
    )
    new_lines = [ln for ln in lines if not any(tok in ln for tok in banned_tokens)]
    if len(new_lines) != len(lines):
        root_tsx.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        return True
    return False


def main():
    removed_dirs = 0
    removed_files = 0
    seen = set()
    for ws in WORKSPACES:
        if not ws.exists() or str(ws.resolve()) in seen:
            continue
        seen.add(str(ws.resolve()))
        for rel_d in OBSOLETE_DIRS:
            dpath = ws / rel_d
            if dpath.exists() and dpath.is_dir():
                shutil.rmtree(dpath, ignore_errors=True)
                removed_dirs += 1
                print(f"🗑️ [DIR] Đã xóa thư mục cũ: {dpath}")
        for rel_f in OBSOLETE_FILES:
            fpath = ws / rel_f
            if fpath.exists() and fpath.is_file():
                try:
                    fpath.unlink()
                    removed_files += 1
                    print(f"🗑️ [FILE] Đã xóa tệp cũ: {fpath}")
                except Exception as e:
                    print(f"⚠️ Không xóa được {fpath}: {e}")
        if clean_root_tsx(ws):
            print(f"✨ Đã dọn sạch các Composition cũ khỏi {ws.name}/src/Root.tsx")

    print(f"\n✅ HOÀN TẤT DỌN SẠCH TƯ LIỆU CŨ: Đã xóa {removed_dirs} thư mục cũ & {removed_files} tệp/script lỗi thời.")


if __name__ == "__main__":
    main()
