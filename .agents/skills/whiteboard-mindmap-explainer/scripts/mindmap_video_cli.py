#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Whiteboard Mindmap Explainer CLI
--------------------------------
Tự động sản xuất video hoạt hình Sơ Đồ Tư Duy Bảng Trắng Vô Cực (Infinite Canvas Mindmap)
kết hợp Nhân Vật Pixel Mascot Cầm Bút Tô Mực Thật (Ghost Outline -> Live Ink Drawing)
theo đúng phong cách "Hệ sinh thái Anthropic / Kỹ Sư 4.0".
"""

import argparse
import asyncio
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
REMOTION_DIR = WORKSPACE_ROOT / "templates" / "remotion-cuongit-template"
PUBLIC_MINDMAP_DIR = REMOTION_DIR / "public" / "mindmap-runtime"


def probe_duration_seconds(media_path: Path) -> float:
    if not media_path.exists():
        return 3.5
    try:
        res = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(media_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return float(res.stdout.strip())
    except Exception:
        return 3.5


async def synthesize_segments_and_concat(
    segments: List[Dict[str, str]],
    voice: str,
    rate: str,
    work_dir: Path,
    final_mp3: Path,
) -> List[float]:
    """
    Synthesize each narration segment via tools/generate_voice_tts.py (Vbee / Viettel / Edge
    with FFmpeg Studio Mastering -3dB), measure exact duration in seconds,
    and concatenate into a single seamless voiceover track.
    """
    work_dir.mkdir(parents=True, exist_ok=True)
    durations: List[float] = []
    part_files: List[Path] = []
    tts_tool = WORKSPACE_ROOT / "tools" / "generate_voice_tts.py"

    for idx, seg in enumerate(segments):
        part_mp3 = work_dir / f"seg_{idx:02d}_{seg['id']}.mp3"
        if not (part_mp3.exists() and part_mp3.stat().st_size > 1000):
            subprocess.run(
                [
                    sys.executable,
                    str(tts_tool),
                    "--page", "4",
                    "--text", seg["text"],
                    "--output", str(part_mp3),
                ],
                check=True,
            )
        dur = probe_duration_seconds(part_mp3)
        durations.append(dur)
        part_files.append(part_mp3)

    concat_list = work_dir / "concat_list.txt"
    lines = [f"file '{p.resolve().as_posix()}'" for p in part_files]
    concat_list.write_text("\n".join(lines), encoding="utf-8")

    final_mp3.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list),
            "-c:a", "libmp3lame",
            "-q:a", "2",
            str(final_mp3),
        ],
        check=True,
        capture_output=True,
    )
    return durations


def get_default_preset_spec() -> Dict[str, Any]:
    """Return a default 4-branch AI Ecosystem Mindmap spec with narration segments."""
    return {
        "rootTitle": "Anthropic",
        "stickyHookText": "Chỉ một\nnhánh nhỏ!",
        "stickyFinaleTop": "model\n→ app\n→ agent làm cùng bạn",
        "stickyFinaleBottom": "Bạn đang dùng\nnhánh nào?",
        "hookNarration": "Nhắc tới Anthropic, nhiều người chỉ nghĩ tới khung chat Claude.",
        "rootOverviewNarration": "Nhưng đó mới là một nhánh nhỏ thôi nha! Để mình vẽ cả cái cây cho bạn xem từng nhánh một.",
        "finaleNarration": "Nhìn cả cái cây này mới thấy khung chat chỉ là một chiếc lá. Còn bạn đang dùng nhánh nào rồi? Comment cho mình biết nha!",
        "branches": [
            {
                "id": "claude_app",
                "title": "Claude app",
                "color": "#C85A3C",
                "x": -680,
                "y": -380,
                "anchorPosition": "bottom",
                "narration": "Nhánh đầu tiên, Claude App, có trên web, máy tính và điện thoại. Đây là cửa chính để bạn chat, nghiên cứu, đọc tài liệu với gói Free, Pro và Max.",
                "blocks": [
                    {
                        "type": "icon-row",
                        "items": [
                            {"icon": "🌐", "label": "web"},
                            {"icon": "💻", "label": "máy tính"},
                            {"icon": "📱", "label": "điện thoại"},
                        ],
                    },
                    {
                        "type": "checklist",
                        "items": [
                            {"icon": "💬", "label": "Chat"},
                            {"icon": "📚", "label": "Nghiên cứu"},
                            {"icon": "📄", "label": "Đọc tài liệu"},
                            {"icon": "🎙️", "label": "Giọng nói"},
                        ],
                    },
                    {
                        "type": "pills",
                        "items": [{"label": "Free"}, {"label": "Pro"}, {"label": "Max"}],
                    },
                    {
                        "type": "summary-note",
                        "items": [{"label": "= cửa chính vào Claude"}],
                    },
                ],
            },
            {
                "id": "cowork",
                "title": "Cowork",
                "color": "#5C7A45",
                "x": -220,
                "y": -640,
                "anchorPosition": "bottom",
                "narration": "Nhánh thứ hai, Cowork. Ở đây bạn không hỏi nữa mà giao việc. Claude tự lên kế hoạch, dùng file, mở trình duyệt rồi nộp kết quả ngay cả khi bạn tắt máy.",
                "blocks": [
                    {
                        "type": "flow-steps",
                        "items": [
                            {"icon": "📅", "label": "kế hoạch"},
                            {"icon": "📄", "label": "file"},
                            {"icon": "🌐", "label": "trình duyệt"},
                            {"icon": "📈", "label": "kết quả"},
                        ],
                    },
                    {
                        "type": "icon-row",
                        "items": [
                            {"icon": "🌐", "label": "web"},
                            {"icon": "📱", "label": "điện thoại"},
                        ],
                    },
                    {
                        "type": "strikethrough-replace",
                        "oldWord": "hỏi",
                        "newWord": "giao việc",
                        "items": [{"label": "tắt máy, vẫn làm tiếp"}],
                    },
                ],
            },
            {
                "id": "claude_code",
                "title": "Claude Code",
                "subtitle": "cho dân lập trình",
                "color": "#B84B30",
                "x": 460,
                "y": -580,
                "anchorPosition": "bottom",
                "narration": "Nhánh thứ ba, Claude Code cho dân lập trình. Bạn giao một task, nó đọc cả project, sửa code, chạy test, lỗi thì tự sửa và có cả Code Review.",
                "blocks": [
                    {
                        "type": "cycle-loop",
                        "centerLabel": "task",
                        "items": [
                            {"label": "đọc project"},
                            {"label": "sửa code"},
                            {"label": "chạy test"},
                            {"label": "tự sửa"},
                        ],
                    },
                    {
                        "type": "pills",
                        "items": [
                            {"label": "terminal"},
                            {"label": "IDE"},
                            {"label": "Desktop"},
                            {"label": "web"},
                            {"label": "Slack"},
                        ],
                    },
                    {
                        "type": "summary-note",
                        "items": [{"icon": "✅", "label": "Code Review"}],
                    },
                ],
            },
            {
                "id": "models",
                "title": "Models",
                "color": "#1E1E1E",
                "x": -580,
                "y": 480,
                "anchorPosition": "top",
                "narration": "Lõi bên dưới là các Model: Haiku nhanh rẻ, Sonnet cân bằng hàng ngày, Opus cho việc khó, Fable mạnh nhất mở rộng và Mythos cho nhóm bảo mật.",
                "blocks": [
                    {
                        "type": "staircase-bars",
                        "items": [
                            {"label": "Haiku", "subLabel": "nhanh, rẻ", "heightRatio": 0.28},
                            {"label": "Sonnet", "subLabel": "hàng ngày", "heightRatio": 0.45},
                            {"label": "Opus", "subLabel": "việc khó", "heightRatio": 0.64},
                            {"label": "Fable", "subLabel": "mạnh nhất", "heightRatio": 0.82},
                            {"label": "Mythos", "subLabel": "nhóm bảo mật", "heightRatio": 1.0, "highlight": True},
                        ],
                    },
                    {
                        "type": "summary-note",
                        "items": [{"label": "mọi nhánh đều chạy trên đây"}],
                    },
                ],
            },
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Whiteboard Mindmap Explainer CLI")
    parser.add_argument("--config", type=str, default="", help="Path to custom JSON mindmap spec")
    parser.add_argument("--preset", type=str, default="ai-agent-ecosystem", help="Built-in preset name")
    parser.add_argument("--voice", type=str, default="vi-VN-NamMinhNeural")
    parser.add_argument("--rate", type=str, default="+14%")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--output", type=str, required=True, help="Output MP4 file path")
    args = parser.parse_args()

    if args.config and Path(args.config).exists():
        spec = json.loads(Path(args.config).read_text(encoding="utf-8"))
    else:
        spec = get_default_preset_spec()

    PUBLIC_MINDMAP_DIR.mkdir(parents=True, exist_ok=True)
    segments: List[Dict[str, str]] = [
        {"id": "hook", "text": spec.get("hookNarration", "Nhiều người chỉ biết tới một nhánh nhỏ.")},
        {"id": "root", "text": spec.get("rootOverviewNarration", "Để mình vẽ cả cái cây cho bạn xem.")},
    ]
    for b in spec["branches"]:
        segments.append({"id": b["id"], "text": b.get("narration", b["title"])})
    segments.append({"id": "finale", "text": spec.get("finaleNarration", "Bạn đang dùng nhánh nào?")})

    final_mp3 = PUBLIC_MINDMAP_DIR / "mindmap_master_voice.mp3"
    print(f"[Mindmap TTS] Synthesizing {len(segments)} narration segments ({args.voice})...")
    durations = asyncio.run(
        synthesize_segments_and_concat(
            segments=segments,
            voice=args.voice,
            rate=args.rate,
            work_dir=PUBLIC_MINDMAP_DIR / "parts",
            final_mp3=final_mp3,
        )
    )

    hook_end = round(durations[0], 2)
    root_end = round(hook_end + durations[1], 2)
    cursor = root_end

    branches_out = []
    for idx, b in enumerate(spec["branches"]):
        b_dur = durations[2 + idx]
        b_copy = dict(b)
        b_copy["startSec"] = round(cursor, 2)
        b_copy["endSec"] = round(cursor + b_dur, 2)
        b_copy.pop("narration", None)
        branches_out.append(b_copy)
        cursor += b_dur

    finale_start = round(cursor, 2)
    total_sec = cursor + durations[-1] + 0.6
    total_frames = max(90, int(round(total_sec * args.fps)))

    props = {
        "rootTitle": spec["rootTitle"],
        "hookTitle": spec.get("hookTitle", "Đa Mô Hình AI"),
        "hookPills": spec.get("hookPills", ["GPT-4 • Mượt", "DeepSeek • Lý luận", "Claude 3.5 • Code"]),
        "hookPainText": spec.get("hookPainText", "Quá nhiều tài khoản + Đống API key phức tạp!"),
        "stickyHookText": spec["stickyHookText"],
        "stickyFinaleTop": spec["stickyFinaleTop"],
        "stickyFinaleBottom": spec["stickyFinaleBottom"],
        "audioSrc": "mindmap-runtime/mindmap_master_voice.mp3",
        "bgmSrc": spec.get("bgmSrc", "brand-kit/bgm/1.The Violins.mp3"),
        "durationInFrames": total_frames,
        "hookEndSec": hook_end,
        "rootOverviewEndSec": root_end,
        "finaleStartSec": finale_start,
        "branches": branches_out,
    }

    props_path = PUBLIC_MINDMAP_DIR / "mindmap_props.json"
    props_path.write_text(json.dumps(props, ensure_ascii=False, indent=2), encoding="utf-8")

    out_mp4 = Path(args.output).resolve()
    out_mp4.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "pnpm",
        "exec",
        "remotion",
        "render",
        "WhiteboardMindmapShort",
        str(out_mp4),
        f"--props={props_path}",
    ]
    print(f"[Remotion Mindmap] Rendering {total_frames} frames ({total_sec:.1f}s) -> {out_mp4}...")
    subprocess.run(cmd, cwd=str(REMOTION_DIR), shell=(os.name == "nt"), check=True)
    print(f"[OK] Rendered Whiteboard Mindmap Explainer video: {out_mp4}")


if __name__ == "__main__":
    main()
