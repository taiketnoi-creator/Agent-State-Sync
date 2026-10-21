#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local 0-Token FFmpeg 9:16 Short Video Renderer (Upgraded with Short-Video-Factory Batch Mixing)
Capabilities:
1. Multi-Clip & Keyframe Stitching (`filter_complex` concat for >= 4 scenes: Hook, Pain, Demo, CTA).
2. Folder-Level Storyboard Batch Mixing (`--scenes-dir` or directory `media_path` per scene + `--batch-count`).
3. Studio Audio Mixing (`voiceover` at -3dB + `bgm` auto-ducked at -18dB, synced to voice/scene duration).
4. Automatic `.srt` Subtitle Burn-in with Windows path escaping.
"""

import argparse
import json
import os
import random
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".avi"}
MEDIA_EXTS = IMAGE_EXTS | VIDEO_EXTS


def check_ffmpeg() -> Optional[str]:
    try:
        res = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
        return res.stdout.splitlines()[0]
    except Exception:
        return None


def probe_duration(media_path: str) -> Optional[float]:
    if not media_path or not os.path.exists(media_path):
        return None
    try:
        res = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                media_path,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        val = float(res.stdout.strip())
        return val if val > 0 else None
    except Exception:
        return None


def escape_ffmpeg_sub_path(path_str: str) -> str:
    abs_p = os.path.abspath(path_str).replace("\\", "/")
    return abs_p.replace(":", "\\:")


def resolve_scene_media(media_path: str, variant_idx: int = 0, randomize: bool = False) -> Optional[str]:
    """
    Supports both direct file path and Folder-level Storyboard Pool (Short-Video-Factory style).
    If media_path is a folder containing multiple clips, selects one deterministically or randomly.
    """
    if not media_path or not os.path.exists(media_path):
        return None
    p = Path(media_path)
    if p.is_file():
        return str(p)
    if p.is_dir():
        candidates = sorted([f for f in p.iterdir() if f.is_file() and f.suffix.lower() in MEDIA_EXTS])
        if not candidates:
            return None
        if randomize:
            return str(random.choice(candidates))
        return str(candidates[variant_idx % len(candidates)])
    return None


def discover_scenes_from_dir(scenes_dir: str, total_duration: float = 24.0) -> List[Dict[str, Any]]:
    """
    Scans a storyboard directory (`--scenes-dir`).
    - If subdirectories exist (e.g., 01_hook/, 02_pain/, 03_demo/, 04_cta/), each subdir is a scene pool.
    - Otherwise, each media file in scenes_dir is treated as a sequential scene.
    """
    root = Path(scenes_dir)
    if not root.exists():
        return []

    subdirs = sorted([d for d in root.iterdir() if d.is_dir()])
    scenes: List[Dict[str, Any]] = []
    if subdirs:
        per_scene = round(total_duration / len(subdirs), 2)
        for d in subdirs:
            scenes.append({"id": d.name, "media_path": str(d), "duration": per_scene})
    else:
        files = sorted([f for f in root.iterdir() if f.is_file() and f.suffix.lower() in MEDIA_EXTS])
        if files:
            per_scene = round(total_duration / len(files), 2)
            for f in files:
                scenes.append({"id": f.stem, "media_path": str(f), "duration": per_scene})
    return scenes


def build_ffmpeg_command(
    scenes: List[Dict[str, Any]],
    output_path: str,
    voiceover: str = "",
    bgm: str = "",
    subtitles_srt: str = "",
    variant_idx: int = 0,
    randomize: bool = False,
) -> List[str]:
    cmd = ["ffmpeg", "-y"]

    resolved_scenes: List[Dict[str, Any]] = []
    for s in scenes:
        m_file = resolve_scene_media(s.get("media_path", ""), variant_idx=variant_idx, randomize=randomize)
        dur = float(s.get("duration", 5.0) or 5.0)
        if m_file:
            resolved_scenes.append({"file": m_file, "duration": dur, "id": s.get("id", "")})

    # Measure voiceover duration if present
    vo_exists = bool(voiceover and os.path.exists(voiceover))
    bgm_exists = bool(bgm and os.path.exists(bgm))
    srt_exists = bool(subtitles_srt and os.path.exists(subtitles_srt))

    vo_duration = probe_duration(voiceover) if vo_exists else None
    raw_total_duration = sum(s["duration"] for s in resolved_scenes) if resolved_scenes else (
        sum(float(s.get("duration", 5.0)) for s in scenes) or (vo_duration or 15.0)
    )

    # Auto-scale scene durations proportionally if voiceover is longer/shorter and auto_sync is desired
    if resolved_scenes and vo_duration and abs(vo_duration - raw_total_duration) > 0.5:
        scale_factor = vo_duration / raw_total_duration
        for s in resolved_scenes:
            s["duration"] = round(max(1.5, s["duration"] * scale_factor), 2)
        total_duration = sum(s["duration"] for s in resolved_scenes)
    else:
        total_duration = raw_total_duration

    filter_parts: List[str] = []
    input_idx = 0

    if not resolved_scenes:
        # Fallback: clean 9:16 slate-950 preview video
        cmd.extend([
            "-f", "lavfi", "-i", f"color=c=0x0f172a:s=1080x1920:d={total_duration}:r=30",
        ])
        filter_parts.append(f"[0:v]format=yuv420p[vcat]")
        input_idx = 1
    else:
        concat_inputs = []
        for s in resolved_scenes:
            ext = Path(s["file"]).suffix.lower()
            dur = s["duration"]
            if ext in IMAGE_EXTS:
                cmd.extend(["-loop", "1", "-t", str(dur), "-i", s["file"]])
            else:
                # Loop input video if clip is shorter than target scene duration, then trim to exact scene duration
                cmd.extend(["-stream_loop", "-1", "-t", str(dur), "-i", s["file"]])

            filter_parts.append(
                f"[{input_idx}:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
                f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x0f172a,"
                f"fps=30,setsar=1,format=yuv420p[v{input_idx}]"
            )
            concat_inputs.append(f"[v{input_idx}]")
            input_idx += 1

        if len(concat_inputs) == 1:
            filter_parts.append(f"{concat_inputs[0]}null[vcat]")
        else:
            filter_parts.append(f"{''.join(concat_inputs)}concat=n={len(concat_inputs)}:v=1:a=0[vcat]")

    # Optional Subtitle burn-in on [vcat]
    if srt_exists:
        esc_srt = escape_ffmpeg_sub_path(subtitles_srt)
        filter_parts.append(
            f"[vcat]subtitles='{esc_srt}':force_style='FontName=Arial,FontSize=16,"
            f"PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=2,Shadow=0,MarginV=65'[vout]"
        )
        final_v_label = "[vout]"
    else:
        final_v_label = "[vcat]"

    # Audio inputs & Studio Mastering levels (Voiceover -3dB, BGM -18dB)
    vo_idx = None
    bgm_idx = None
    if vo_exists:
        cmd.extend(["-i", voiceover])
        vo_idx = input_idx
        input_idx += 1
    if bgm_exists:
        cmd.extend(["-stream_loop", "-1", "-t", str(total_duration), "-i", bgm])
        bgm_idx = input_idx
        input_idx += 1

    final_a_label = None
    if vo_idx is not None and bgm_idx is not None:
        filter_parts.append(f"[{vo_idx}:a]volume=-3dB[avo]")
        filter_parts.append(f"[{bgm_idx}:a]volume=-18dB[abgm]")
        filter_parts.append("[avo][abgm]amix=inputs=2:duration=first:dropout_transition=2[aout]")
        final_a_label = "[aout]"
    elif vo_idx is not None:
        filter_parts.append(f"[{vo_idx}:a]volume=-3dB[aout]")
        final_a_label = "[aout]"
    elif bgm_idx is not None:
        filter_parts.append(f"[{bgm_idx}:a]volume=-18dB[aout]")
        final_a_label = "[aout]"

    cmd.extend(["-filter_complex", ";".join(filter_parts)])
    cmd.extend(["-map", final_v_label])
    if final_a_label:
        cmd.extend(["-map", final_a_label, "-c:a", "aac", "-b:a", "192k"])

    cmd.extend([
        "-t", str(round(total_duration, 2)),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        output_path,
    ])
    return cmd


def render_job(
    manifest_path: Optional[str],
    output_path: str,
    scenes_dir: Optional[str] = None,
    voiceover_arg: str = "",
    bgm_arg: str = "",
    srt_arg: str = "",
    batch_count: int = 1,
    dry_run: bool = False,
) -> None:
    data: Dict[str, Any] = {}
    if manifest_path:
        if not os.path.exists(manifest_path):
            print(json.dumps({"status": "error", "message": f"Manifest file not found: {manifest_path}"}))
            sys.exit(1)
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    voiceover = voiceover_arg or data.get("voiceover_path", "")
    bgm = bgm_arg or data.get("bgm_path", "")
    subtitles = srt_arg or data.get("subtitles_srt", "")
    vo_dur = probe_duration(voiceover) or 24.0

    scenes = data.get("scenes", [])
    if scenes_dir:
        scenes = discover_scenes_from_dir(scenes_dir, total_duration=vo_dur)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    outputs_generated = []
    base_out = Path(output_path)

    for idx in range(max(1, batch_count)):
        if batch_count > 1:
            curr_out = str(base_out.with_name(f"{base_out.stem}_v{idx+1:02d}{base_out.suffix}"))
        else:
            curr_out = output_path

        cmd = build_ffmpeg_command(
            scenes=scenes,
            output_path=curr_out,
            voiceover=voiceover,
            bgm=bgm,
            subtitles_srt=subtitles,
            variant_idx=idx,
            randomize=(batch_count > 1 and idx > 0),
        )

        if dry_run:
            outputs_generated.append({"variant": idx + 1, "output": curr_out, "ffmpeg_cmd": " ".join(cmd)})
            continue

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            outputs_generated.append({"variant": idx + 1, "output_video": curr_out, "scenes_count": len(scenes)})
        else:
            print(json.dumps({"status": "error", "variant": idx + 1, "stderr_tail": res.stderr[-600:]}, ensure_ascii=False))
            sys.exit(1)

    status_label = "dry_run" if dry_run else "ok"
    if batch_count == 1 and not dry_run:
        print(json.dumps({
            "status": "ok",
            "output_video": output_path,
            "scenes_count": len(scenes),
            "mode": "folder_batch" if scenes_dir else "manifest",
        }, ensure_ascii=False))
    else:
        print(json.dumps({
            "status": status_label,
            "batch_count": batch_count,
            "scenes_count": len(scenes),
            "results": outputs_generated,
        }, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Local 0-Token FFmpeg 9:16 Short Video Factory Renderer")
    parser.add_argument("--manifest", help="Path to script/scene manifest JSON")
    parser.add_argument("--scenes-dir", help="Path to storyboard folder (01_hook/, 02_pain/, 03_demo/, 04_cta/)")
    parser.add_argument("--voiceover", default="", help="Optional override path to voiceover audio (.mp3/.wav)")
    parser.add_argument("--bgm", default="", help="Optional override path to BGM audio (.mp3/.wav)")
    parser.add_argument("--srt", default="", help="Optional override path to subtitles (.srt)")
    parser.add_argument("--batch-count", type=int, default=1, help="Number of video variations to batch-mix")
    parser.add_argument("--output", required=True, help="Output MP4 file path")
    parser.add_argument("--dry-run", action="store_true", help="Print FFmpeg command without executing")
    args = parser.parse_args()

    if not args.manifest and not args.scenes_dir:
        print(json.dumps({"status": "error", "message": "Provide either --manifest or --scenes-dir"}))
        sys.exit(1)

    render_job(
        manifest_path=args.manifest,
        output_path=args.output,
        scenes_dir=args.scenes_dir,
        voiceover_arg=args.voiceover,
        bgm_arg=args.bgm,
        srt_arg=args.srt,
        batch_count=args.batch_count,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
