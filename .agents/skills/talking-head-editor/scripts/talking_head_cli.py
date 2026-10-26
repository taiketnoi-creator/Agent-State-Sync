#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Talking Head Video Editor CLI (Remotion & HyperFrames Engines)
--------------------------------------------------------------
1. Định vị luồng video người nói (A-Roll) ở chính giữa màn hình (9:16 1080x1920).
2. Tự động đồng bộ file âm thanh / phụ đề (.srt hoặc .json) thành hiệu ứng chữ chạy
   từng từ (Karaoke Word-by-Word Highlight) bám sát giọng nói.
3. Chèn hình ảnh / video B-Roll đè lên luồng video gốc tại đúng mốc thời gian (timestamps)
   định sẵn từ dòng lệnh mà không bị lệch khung hình (Zero Frame Drift).
"""

import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
REMOTION_DIR = WORKSPACE_ROOT / "templates" / "remotion-cuongit-template"
PUBLIC_TEMP_DIR = REMOTION_DIR / "public" / "talking-head-runtime"

VIETNAMESE_COMPOUNDS = {
    "trí tuệ", "nhân tạo", "hệ thống", "tự động", "chuyển đổi", "khách hàng",
    "màn hình", "chính giữa", "phụ đề", "giọng nói", "khung hình", "thời gian",
    "dòng lệnh", "hình ảnh", "minh họa", "thực tế", "công nghệ", "doanh nghiệp",
    "ứng dụng", "tính năng", "mã nguồn", "bản chất", "người nói", "video ngắn",
}


def parse_srt_time_to_ms(time_str: str) -> int:
    """Convert '00:00:02,450' or '00:00:02.450' to milliseconds."""
    time_str = time_str.strip().replace(".", ",")
    match = re.match(r"(\d+):(\d+):(\d+),(\d+)", time_str)
    if not match:
        return 0
    h, m, s, ms = map(int, match.groups())
    return ((h * 3600) + (m * 60) + s) * 1000 + ms


def group_vietnamese_compounds(raw_words: List[str]) -> List[str]:
    """Group common 2-syllable Vietnamese compound words for natural Karaoke flow."""
    grouped: List[str] = []
    i = 0
    while i < len(raw_words):
        if i + 1 < len(raw_words):
            w1_clean = re.sub(r"[^\w]", "", raw_words[i].lower())
            w2_clean = re.sub(r"[^\w]", "", raw_words[i + 1].lower())
            pair = f"{w1_clean} {w2_clean}"
            if pair in VIETNAMESE_COMPOUNDS:
                grouped.append(f"{raw_words[i]} {raw_words[i + 1]}")
                i += 2
                continue
        grouped.append(raw_words[i])
        i += 1
    return grouped


def parse_srt_to_karaoke_words(srt_path: Path) -> List[Dict[str, Any]]:
    """
    Parse an .srt file into word-level Karaoke tokens with syllable-weighted
    millisecond timestamps (startMs, endMs).
    """
    content = srt_path.read_text(encoding="utf-8", errors="ignore")
    blocks = re.split(r"\n\s*\n", content.strip())
    words_out: List[Dict[str, Any]] = []

    for block in blocks:
        lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
        if len(lines) < 2:
            continue
        time_line_idx = 0
        for idx, line in enumerate(lines):
            if "-->" in line:
                time_line_idx = idx
                break
        else:
            continue

        time_parts = lines[time_line_idx].split("-->")
        start_ms = parse_srt_time_to_ms(time_parts[0])
        end_ms = parse_srt_time_to_ms(time_parts[1])
        text_body = " ".join(lines[time_line_idx + 1 :]).strip()
        if not text_body or end_ms <= start_ms:
            continue

        raw_tokens = [w for w in text_body.split() if w]
        tokens = group_vietnamese_compounds(raw_tokens)
        if not tokens:
            continue

        # Weight duration by character/syllable length + punctuation pause
        weights = []
        for tok in tokens:
            base_weight = max(1, len(tok.split())) * 1.0 + len(tok) * 0.12
            if tok.endswith((",", ";", ":")):
                base_weight += 0.45
            elif tok.endswith((".", "!", "?", "…")):
                base_weight += 0.65
            weights.append(base_weight)

        total_weight = sum(weights)
        total_dur = end_ms - start_ms
        cursor = float(start_ms)

        for tok, w in zip(tokens, weights):
            dur = (w / total_weight) * total_dur
            w_start = int(round(cursor))
            w_end = int(round(cursor + dur))
            words_out.append({
                "text": tok,
                "startMs": w_start,
                "endMs": max(w_start + 40, w_end),
            })
            cursor += dur

    return words_out


async def generate_tts_with_word_boundaries(
    text: str,
    voice: str,
    rate: str,
    audio_out: Path,
    srt_out: Optional[Path],
    json_out: Optional[Path],
) -> List[Dict[str, Any]]:
    """Generate TTS audio + millisecond-accurate word boundaries using edge-tts."""
    import edge_tts

    communicate = edge_tts.Communicate(text, voice, rate=rate)
    submaker = edge_tts.SubMaker()
    word_tokens: List[Dict[str, Any]] = []

    audio_out.parent.mkdir(parents=True, exist_ok=True)
    with open(audio_out, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                offset_ms = int(chunk["offset"] / 10000)
                duration_ms = int(chunk["duration"] / 10000)
                word_tokens.append({
                    "text": chunk["text"],
                    "startMs": offset_ms,
                    "endMs": offset_ms + max(50, duration_ms),
                })
                submaker.feed(chunk)

    if srt_out:
        srt_out.parent.mkdir(parents=True, exist_ok=True)
        srt_out.write_text(submaker.get_srt(), encoding="utf-8")

    # Fallback if stream only returned sentence boundaries or no boundaries
    if not word_tokens and srt_out and srt_out.exists() and srt_out.stat().st_size > 10:
        word_tokens = parse_srt_to_karaoke_words(srt_out)

    if not word_tokens:
        dur_ms = int(round(probe_duration_seconds(audio_out) * 1000))
        synthetic_srt = f"1\n00:00:00,000 --> 00:00:{dur_ms // 1000:02d},{dur_ms % 1000:03d}\n{text.strip()}\n"
        if srt_out:
            srt_out.parent.mkdir(parents=True, exist_ok=True)
            srt_out.write_text(synthetic_srt, encoding="utf-8")
            word_tokens = parse_srt_to_karaoke_words(srt_out)
        else:
            tmp_srt = audio_out.with_suffix(".tmp.srt")
            tmp_srt.write_text(synthetic_srt, encoding="utf-8")
            word_tokens = parse_srt_to_karaoke_words(tmp_srt)
            tmp_srt.unlink(missing_ok=True)

    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(
            json.dumps(word_tokens, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return word_tokens


def parse_broll_cli_spec(broll_spec: str) -> List[Dict[str, Any]]:
    """
    Parse CLI B-Roll specification string:
    Format: "startSec-endSec:filePath[:layout[:label]]" separated by comma ','
    Example: "2.0-5.5:assets/broll1.jpg:pip-card:Bằng chứng 1,8.0-11.0:assets/clip2.mp4:fullscreen:Demo"
    """
    if not broll_spec or not broll_spec.strip():
        return []

    cues: List[Dict[str, Any]] = []
    entries = [e.strip() for e in broll_spec.split(",") if e.strip()]

    for idx, entry in enumerate(entries, start=1):
        # Match start-end:rest
        m = re.match(r"^(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*:\s*(.+)$", entry)
        if not m:
            raise ValueError(
                f"Invalid B-Roll spec '{entry}'. Expected 'startSec-endSec:path[:layout[:label]]'"
            )
        start_sec = float(m.group(1))
        end_sec = float(m.group(2))
        rest = m.group(3)

        # Handle Windows drive letters like D:\path\file.jpg:pip-card:Label
        if re.match(r"^[A-Za-z]:[\\/]", rest):
            drive_prefix = rest[:2]
            parts = rest[2:].split(":")
            parts[0] = drive_prefix + parts[0]
        else:
            parts = rest.split(":")

        file_path = parts[0].strip()
        layout = parts[1].strip() if len(parts) > 1 and parts[1].strip() else "pip-card"
        label = parts[2].strip() if len(parts) > 2 and parts[2].strip() else ""

        ext = Path(file_path).suffix.lower()
        media_type = "video" if ext in {".mp4", ".mov", ".webm", ".mkv"} else "image"

        cues.append({
            "id": f"broll_{idx:02d}",
            "startSec": start_sec,
            "endSec": end_sec,
            "src": file_path,
            "mediaType": media_type,
            "layout": layout if layout in {"fullscreen", "pip-card", "split-top"} else "pip-card",
            "label": label,
            "zoomEffect": "ken-burns-in" if idx % 2 == 1 else "ken-burns-out",
        })
    return cues


def probe_duration_seconds(media_path: Path) -> float:
    """Use ffprobe to get exact media duration in seconds."""
    if not media_path or not media_path.exists():
        return 10.0
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
        return 10.0


def build_ass_karaoke_subtitles(words: List[Dict[str, Any]], ass_path: Path) -> None:
    """
    Generate an ASS subtitle file with \\kf Karaoke tags synchronized to millisecond
    word timestamps for HyperFrames / FFmpeg high-speed rendering.
    """
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Karaoke,Arial,58,&H0000FF87,&H00FFFFFF,&H00140A05,&H96140A05,-1,0,0,0,100,100,0,0,1,4,2,2,60,60,290,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    def ms_to_ass_time(ms: int) -> str:
        total_cs = max(0, int(round(ms / 10.0)))
        cs = total_cs % 100
        total_s = total_cs // 100
        s = total_s % 60
        total_m = total_s // 60
        m = total_m % 60
        h = total_m // 60
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    # Group words into chunks of up to 5 words or 1.6s
    chunks: List[List[Dict[str, Any]]] = []
    cur_chunk: List[Dict[str, Any]] = []
    for w in words:
        if not cur_chunk:
            cur_chunk.append(w)
            continue
        if len(cur_chunk) >= 5 or (w["endMs"] - cur_chunk[0]["startMs"]) > 1700:
            chunks.append(cur_chunk)
            cur_chunk = [w]
        else:
            cur_chunk.append(w)
    if cur_chunk:
        chunks.append(cur_chunk)

    events = []
    for chunk in chunks:
        c_start = chunk[0]["startMs"]
        c_end = chunk[-1]["endMs"]
        karaoke_parts = []
        cursor_ms = c_start
        for w in chunk:
            gap_cs = max(0, int(round((w["startMs"] - cursor_ms) / 10.0)))
            if gap_cs > 0:
                karaoke_parts.append(f"{{\\k{gap_cs}}}")
            dur_cs = max(5, int(round((w["endMs"] - w["startMs"]) / 10.0)))
            karaoke_parts.append(f"{{\\kf{dur_cs}}}{w['text']}")
            cursor_ms = w["endMs"]
        line_text = " ".join(karaoke_parts)
        events.append(
            f"Dialogue: 0,{ms_to_ass_time(c_start)},{ms_to_ass_time(c_end)},Karaoke,,0,0,0,,{line_text}"
        )

    ass_path.parent.mkdir(parents=True, exist_ok=True)
    ass_path.write_text(header + "\n".join(events) + "\n", encoding="utf-8")


def generate_hyperframes_html(
    output_html: Path,
    aroll_src: str,
    words: List[Dict[str, Any]],
    brolls: List[Dict[str, Any]],
    fps: int = 30,
) -> None:
    """
    Generate a deterministic HTML5/JS HyperFrames player with window.seekToFrame(frame)
    for browser/WebCodecs inspection or headless frame capture.
    """
    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <title>HyperFrames Talking Head Studio (1080x1920 @ {fps}fps)</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #050814; display: flex; justify-content: center; align-items: center; min-height: 100vh; font-family: 'Inter', sans-serif; }}
    #stage {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #050814; }}
    #aroll {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center center; z-index: 1; }}
    #broll-container {{ position: absolute; inset: 0; z-index: 20; pointer-events: none; }}
    .broll-pip {{ position: absolute; top: 230px; left: 64px; right: 64px; height: 580px; border-radius: 36px; overflow: hidden; border: 3px solid #87FF00; box-shadow: 0 28px 65px rgba(0,0,0,0.75); }}
    .broll-fullscreen {{ position: absolute; inset: 0; }}
    .broll-media {{ width: 100%; height: 100%; object-fit: cover; }}
    #karaoke-box {{ position: absolute; bottom: 270px; left: 56px; right: 56px; z-index: 40; display: flex; justify-content: center; }}
    .caption-pill {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 12px 16px; padding: 20px 36px; border-radius: 28px; background: rgba(8,12,24,0.78); backdrop-filter: blur(16px); border: 1.5px solid rgba(255,255,255,0.24); }}
    .word {{ font-size: 52px; font-weight: 900; color: rgba(255,255,255,0.45); transition: transform 0.05s ease; }}
    .word.past {{ color: #FFFFFF; }}
    .word.active {{ color: #87FF00; transform: scale(1.14); text-shadow: 0 0 24px rgba(135,255,0,0.8); }}
  </style>
</head>
<body>
  <div id="stage">
    <video id="aroll" src="{aroll_src}" playsinline></video>
    <div id="broll-container"></div>
    <div id="karaoke-box"><div id="caption-pill" class="caption-pill"></div></div>
  </div>
  <script>
    const FPS = {fps};
    const WORDS = {json.dumps(words, ensure_ascii=False)};
    const BROLLS = {json.dumps(brolls, ensure_ascii=False)};

    window.seekToFrame = function(frame) {{
      const timeSec = frame / FPS;
      const timeMs = timeSec * 1000;
      const aroll = document.getElementById('aroll');
      if (aroll && Math.abs(aroll.currentTime - timeSec) > 0.04) {{
        aroll.currentTime = timeSec;
      }}
      // Render active B-Roll
      const brollContainer = document.getElementById('broll-container');
      const activeBroll = BROLLS.find(b => timeSec >= b.startSec && timeSec < b.endSec);
      if (activeBroll) {{
        const cls = activeBroll.layout === 'fullscreen' ? 'broll-fullscreen' : 'broll-pip';
        brollContainer.innerHTML = `<div class="${{cls}}"><img class="broll-media" src="${{activeBroll.src}}" /></div>`;
      }} else {{
        brollContainer.innerHTML = '';
      }}
      // Render Karaoke Words
      const pill = document.getElementById('caption-pill');
      const visibleWords = WORDS.filter(w => Math.abs(w.startMs - timeMs) <= 1400);
      pill.innerHTML = visibleWords.map(w => {{
        const state = (timeMs >= w.startMs && timeMs < w.endMs) ? 'active' : (timeMs >= w.endMs ? 'past' : '');
        return `<span class="word ${{state}}">${{w.text}}</span>`;
      }}).join('');
    }};
  </script>
</body>
</html>"""
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(html, encoding="utf-8")


def render_with_remotion(
    aroll_path: Optional[Path],
    audio_path: Optional[Path],
    words: List[Dict[str, Any]],
    brolls: List[Dict[str, Any]],
    output_mp4: Path,
    channel_badge: str,
    headline_hook: str,
    fps: int = 30,
) -> None:
    """Stage assets into Remotion public folder and render TalkingHeadShort."""
    PUBLIC_TEMP_DIR.mkdir(parents=True, exist_ok=True)

    rel_aroll = ""
    duration_sec = 10.0
    if aroll_path and aroll_path.exists():
        dst_aroll = PUBLIC_TEMP_DIR / aroll_path.name
        shutil.copy2(aroll_path, dst_aroll)
        rel_aroll = f"talking-head-runtime/{aroll_path.name}"
        duration_sec = probe_duration_seconds(aroll_path)

    rel_audio = ""
    if audio_path and audio_path.exists():
        dst_audio = PUBLIC_TEMP_DIR / audio_path.name
        shutil.copy2(audio_path, dst_audio)
        rel_audio = f"talking-head-runtime/{audio_path.name}"
        if not rel_aroll:
            duration_sec = probe_duration_seconds(audio_path)

    if words:
        last_word_sec = (words[-1]["endMs"] / 1000.0) + 0.5
        duration_sec = max(duration_sec, last_word_sec)

    staged_brolls = []
    for cue in brolls:
        src_path = Path(cue["src"])
        if not src_path.is_absolute():
            src_path = (WORKSPACE_ROOT / src_path).resolve()
        if src_path.exists():
            dst_broll = PUBLIC_TEMP_DIR / f"{cue['id']}_{src_path.name}"
            shutil.copy2(src_path, dst_broll)
            cue_copy = dict(cue)
            cue_copy["src"] = f"talking-head-runtime/{dst_broll.name}"
            staged_brolls.append(cue_copy)
        else:
            print(f"[WARN] B-Roll file not found: {src_path}")

    duration_frames = max(60, int(round(duration_sec * fps)))
    props = {
        "arollSrc": rel_aroll,
        "audioSrc": rel_audio,
        "durationInFrames": duration_frames,
        "channelBadge": channel_badge,
        "headlineHook": headline_hook,
        "words": words,
        "brolls": staged_brolls,
    }

    props_file = PUBLIC_TEMP_DIR / "talking_head_props.json"
    props_file.write_text(json.dumps(props, ensure_ascii=False, indent=2), encoding="utf-8")

    output_mp4 = output_mp4.resolve()
    output_mp4.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "pnpm",
        "exec",
        "remotion",
        "render",
        "TalkingHeadShort",
        str(output_mp4),
        f"--props={props_file}",
    ]
    print(f"[Remotion] Rendering TalkingHeadShort ({duration_frames} frames @ {fps}fps)...")
    subprocess.run(cmd, cwd=str(REMOTION_DIR), shell=(os.name == "nt"), check=True)
    print(f"[OK] Rendered Talking Head video: {output_mp4}")


def render_with_hyperframes(
    aroll_path: Optional[Path],
    audio_path: Optional[Path],
    words: List[Dict[str, Any]],
    brolls: List[Dict[str, Any]],
    output_mp4: Path,
    fps: int = 30,
) -> None:
    """
    Generate HyperFrames HTML/JS scene + render MP4 via FFmpeg deterministic
    timestamped B-Roll overlay (enable='between(t,start,end)') and ASS Karaoke subtitles.
    """
    output_mp4 = output_mp4.resolve()
    output_mp4.parent.mkdir(parents=True, exist_ok=True)

    html_out = output_mp4.with_suffix(".hyperframes.html")
    generate_hyperframes_html(
        html_out,
        aroll_src=str(aroll_path) if aroll_path else "",
        words=words,
        brolls=brolls,
        fps=fps,
    )
    print(f"[HyperFrames] Saved HTML5/JS frame-accurate stage: {html_out}")

    ass_path = output_mp4.with_suffix(".karaoke.ass")
    build_ass_karaoke_subtitles(words, ass_path)

    duration_sec = 8.0
    if aroll_path and aroll_path.exists():
        duration_sec = probe_duration_seconds(aroll_path)
    elif audio_path and audio_path.exists():
        duration_sec = probe_duration_seconds(audio_path)
    elif words:
        duration_sec = (words[-1]["endMs"] / 1000.0) + 0.5

    inputs = []
    if aroll_path and aroll_path.exists():
        inputs.extend(["-i", str(aroll_path)])
    else:
        inputs.extend([
            "-f", "lavfi",
            "-i", f"color=c=#081026:s=1080x1920:r={fps}:d={duration_sec:.2f}",
        ])

    valid_brolls = []
    for cue in brolls:
        p = Path(cue["src"])
        if not p.is_absolute():
            p = (WORKSPACE_ROOT / p).resolve()
        if p.exists():
            cue_copy = dict(cue)
            cue_copy["abs_path"] = p
            valid_brolls.append(cue_copy)
            if cue["mediaType"] == "image":
                inputs.extend(["-loop", "1", "-t", f"{duration_sec:.2f}", "-i", str(p)])
            else:
                inputs.extend(["-i", str(p)])

    filter_parts = [
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:(iw-1080)/2:(ih-1920)/2,setsar=1[base0]"
    ]
    last_label = "base0"

    for idx, cue in enumerate(valid_brolls, start=1):
        b_label = f"broll{idx}"
        out_label = f"base{idx}"
        s_sec = cue["startSec"]
        e_sec = cue["endSec"]
        if cue["layout"] == "fullscreen":
            filter_parts.append(
                f"[{idx}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[{b_label}];"
                f"[{last_label}][{b_label}]overlay=0:0:enable='between(t,{s_sec:.3f},{e_sec:.3f})'[{out_label}]"
            )
        elif cue["layout"] == "split-top":
            filter_parts.append(
                f"[{idx}:v]scale=1080:940:force_original_aspect_ratio=increase,crop=1080:940,setsar=1[{b_label}];"
                f"[{last_label}][{b_label}]overlay=0:0:enable='between(t,{s_sec:.3f},{e_sec:.3f})'[{out_label}]"
            )
        else:
            # pip-card centered at top (952x580 at x=64, y=230)
            filter_parts.append(
                f"[{idx}:v]scale=952:580:force_original_aspect_ratio=increase,crop=952:580,setsar=1[{b_label}];"
                f"[{last_label}][{b_label}]overlay=64:230:enable='between(t,{s_sec:.3f},{e_sec:.3f})'[{out_label}]"
            )
        last_label = out_label

    # Escape ASS path for FFmpeg subtitles filter on Windows
    ass_escaped = str(ass_path).replace("\\", "/").replace(":", "\\:")
    filter_parts.append(f"[{last_label}]ass='{ass_escaped}'[vfinal]")

    cmd = ["ffmpeg", "-y"] + inputs
    if audio_path and audio_path.exists() and not (aroll_path and aroll_path.exists()):
        cmd.extend(["-i", str(audio_path)])
        audio_input_idx = 1 + len(valid_brolls)
        cmd.extend([
            "-filter_complex", ";".join(filter_parts),
            "-map", "[vfinal]",
            "-map", f"{audio_input_idx}:a",
        ])
    elif aroll_path and aroll_path.exists():
        cmd.extend([
            "-filter_complex", ";".join(filter_parts),
            "-map", "[vfinal]",
            "-map", "0:a?",
        ])
    else:
        cmd.extend([
            "-filter_complex", ";".join(filter_parts),
            "-map", "[vfinal]",
        ])

    cmd.extend([
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-crf", "21",
        "-preset", "fast",
        "-t", f"{duration_sec:.2f}",
        str(output_mp4),
    ])
    print(f"[HyperFrames/FFmpeg] Rendering video with timestamped B-Roll & Karaoke ASS...")
    subprocess.run(cmd, check=True)
    print(f"[OK] Rendered HyperFrames Talking Head video: {output_mp4}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Talking Head Video Editor CLI (Remotion & HyperFrames)"
    )
    parser.add_argument("--aroll", type=str, default="", help="Path to A-Roll speaker video (.mp4)")
    parser.add_argument("--audio", type=str, default="", help="Optional separate voiceover audio (.mp3/.wav)")
    parser.add_argument("--srt", type=str, default="", help="Path to .srt subtitle file")
    parser.add_argument("--words-json", type=str, default="", help="Path to word-level .json file")
    parser.add_argument(
        "--broll",
        type=str,
        default="",
        help="Comma-separated B-Roll specs: 'startSec-endSec:filePath[:layout[:label]]'",
    )
    parser.add_argument(
        "--engine",
        choices=["remotion", "hyperframes"],
        default="remotion",
        help="Rendering engine: remotion (React) or hyperframes (HTML/JS + FFmpeg)",
    )
    parser.add_argument("--channel-badge", type=str, default="⚡ AI PLAYERS")
    parser.add_argument("--headline-hook", type=str, default="")
    parser.add_argument("--generate-tts-text", type=str, default="", help="Generate TTS + Karaoke subtitles from text")
    parser.add_argument("--tts-voice", type=str, default="vi-VN-NamMinhNeural")
    parser.add_argument("--tts-rate", type=str, default="+12%")
    parser.add_argument("--json-out", type=str, default="", help="Save generated word-level JSON tokens")
    parser.add_argument("--output", type=str, default="", help="Output MP4 path")
    args = parser.parse_args()

    words: List[Dict[str, Any]] = []
    audio_path = Path(args.audio) if args.audio else None
    srt_path = Path(args.srt) if args.srt else None
    json_out_path = Path(args.json_out) if args.json_out else None

    if args.generate_tts_text:
        if not audio_path:
            audio_path = WORKSPACE_ROOT / "output" / "talking_head_tts.mp3"
        if not srt_path:
            srt_path = audio_path.with_suffix(".srt")
        words = asyncio.run(
            generate_tts_with_word_boundaries(
                text=args.generate_tts_text,
                voice=args.tts_voice,
                rate=args.tts_rate,
                audio_out=audio_path,
                srt_out=srt_path,
                json_out=json_out_path,
            )
        )
        print(f"[OK] Generated TTS audio ({audio_path}) + {len(words)} word-level Karaoke tokens.")

    if not words and args.words_json and Path(args.words_json).exists():
        words = json.loads(Path(args.words_json).read_text(encoding="utf-8"))
    elif not words and srt_path and srt_path.exists():
        words = parse_srt_to_karaoke_words(srt_path)
        if json_out_path:
            json_out_path.parent.mkdir(parents=True, exist_ok=True)
            json_out_path.write_text(json.dumps(words, ensure_ascii=False, indent=2), encoding="utf-8")

    brolls = parse_broll_cli_spec(args.broll)

    if not args.output:
        return

    aroll_path = Path(args.aroll) if args.aroll else None
    output_mp4 = Path(args.output)

    if args.engine == "remotion":
        render_with_remotion(
            aroll_path=aroll_path,
            audio_path=audio_path,
            words=words,
            brolls=brolls,
            output_mp4=output_mp4,
            channel_badge=args.channel_badge,
            headline_hook=args.headline_hook,
        )
    else:
        render_with_hyperframes(
            aroll_path=aroll_path,
            audio_path=audio_path,
            words=words,
            brolls=brolls,
            output_mp4=output_mp4,
        )


if __name__ == "__main__":
    main()
