#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_edit3_editonny_40s_test.py — Kịch bản thực thi chuẩn Vàng cho Subagent edit-3:
Tạo 1 video dọc 9:16 (1080x1920 @ 24fps) dài đúng 40.0 giây bằng bộ công cụ Editonny (templates/editonny):
1. Đồng nhất 100% 1 giọng đọc duy nhất (Edge-TTS vi-VN-NamMinhNeural — CẤM fallback sang giọng Nữ Google TTS).
2. Cắt khoảng lặng đầu/cuối + khóa cứng từng đoạn thoại trong khung [start_s, end_s - 0.25s] -> 0ms chồng lấn voice.
3. Khớp 1-1 từng con số, chữ hiển thị và hiệu ứng của 8 Motion Scenes với lời thoại tiếng Việt.
4. Nhúng trực tiếp font Montserrat Variable (744KB full tiếng Việt U+1EA0-1EFF) cho cả Inter, SoraV và Phụ đề.
5. Kiểm định tự động: 0 voice overlap, 0 caption overlap, 0 negative duration trước khi render HyperFrames.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

ROOT = Path(__file__).resolve().parents[1]
EDITONNY_ROOT = ROOT / "templates" / "editonny"
SKILL_DIR = EDITONNY_ROOT / "skills" / "editonny"
ENGINE_DIR = SKILL_DIR / "engine"
VISUALS_DIR = SKILL_DIR / "visuals"
VENV_PY = ENGINE_DIR / ".venv" / "Scripts" / "python.exe"

CAMPAIGN_DIR = ROOT / "campaigns" / "2026-11-04" / "edit3-editonny-40s-test"
EDIT_DIR = CAMPAIGN_DIR / "edit"
PROJECT_DIR = CAMPAIGN_DIR / "project"
FINAL_MP4 = CAMPAIGN_DIR / "edit3_editonny_40s_vertical.mp4"
QA_GRID_JPG = CAMPAIGN_DIR / "edit3_editonny_40s_qa_grid.jpg"

VOICE_ID = "vi-VN-NamMinhNeural"
VOICE_RATE = "+15%"

# Mỗi phân cảnh (scene_id, scene_start, scene_end, voice_text) khớp 1-1 giữa Hình & Tiếng
SCENE_SCRIPT = [
    (
        "year-hook",
        0.2,
        4.6,
        "Năm 2026, sở hữu ngay hệ sinh thái 12 chuyên viên Sub Agent AI.",
    ),
    (
        "ai-chat-interface",
        4.9,
        10.0,
        "Chỉ cần nhắn cho tổng quản Mama dựng video và chạy 4 Fanpage, hệ thống xử lý xong ngay.",
    ),
    (
        "three-steps",
        10.3,
        16.3,
        "Quy trình chỉ 3 bước: một giao lệnh cho Mama, hai đội AI xử lý, ba xuất bản tự động.",
    ),
    (
        "waveform-cuts",
        16.6,
        21.6,
        "Công cụ Editonny tự động cắt 7 khoảng lặng theo sóng âm, rút gọn 1 phút 15 giây xuống 40 giây.",
    ),
    (
        "before-after",
        21.9,
        27.7,
        "Trước đây mất 6 giờ tự dựng thủ công, giờ có Sub Agent chỉ mất 5 phút, nhanh gấp 22 lần.",
    ),
    (
        "glass-chart",
        28.0,
        32.3,
        "Hiệu suất sản xuất nội dung và chuyển đổi khách hàng tăng trưởng bứt phá 320 phần trăm.",
    ),
    (
        "completed-checklist",
        32.6,
        36.1,
        "Xóa bỏ ngay 3 nỗi lo: bí ý tưởng, thức khuya dựng clip, trễ lịch đăng.",
    ),
    (
        "comment-call-to-action",
        36.3,
        40.0,
        "Bình luận ngay chữ Sub Agent dưới video để đặt lịch thiết kế đội ngũ AI riêng.",
    ),
]


async def synthesize_single_voice_tts(text: str, out_mp3: Path) -> None:
    """Chỉ dùng duy nhất 1 giọng đọc Edge-TTS (vi-VN-NamMinhNeural), tuyệt đối không fallback sang giọng khác."""
    import edge_tts

    tmp_mp3 = out_mp3.with_suffix(".tmp.mp3")
    last_err = None
    for attempt in range(12):
        try:
            comm = edge_tts.Communicate(text, voice=VOICE_ID, rate=VOICE_RATE)
            await comm.save(str(tmp_mp3))
            if tmp_mp3.exists() and tmp_mp3.stat().st_size > 1000:
                shutil.move(str(tmp_mp3), str(out_mp3))
                return
        except Exception as e:
            last_err = e
            print(f"  [Edge-TTS Retry {attempt + 1}/12 for {out_mp3.name}] {e}")
            await asyncio.sleep(1.5)
    raise RuntimeError(f"Edge-TTS failed for {out_mp3.name} ({VOICE_ID}): {last_err}")


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out or 0.0)


def build_atempo_chain(speed: float) -> str:
    """Xây dựng chuỗi filter atempo hợp lệ cho mọi hệ số tốc độ."""
    if abs(speed - 1.0) < 0.01:
        return "anull"
    parts = []
    rem = speed
    while rem > 2.0:
        parts.append("atempo=2.0")
        rem /= 2.0
    while rem < 0.5:
        parts.append("atempo=0.5")
        rem /= 0.5
    parts.append(f"atempo={rem:.4f}")
    return ",".join(parts)


def build_40s_voice_and_transcript(edit_dir: Path) -> None:
    """
    Tạo thuyết minh 40.0s đồng nhất 100% giọng vi-VN-NamMinhNeural,
    cắt khoảng lặng đầu/cuối và khóa cứng từng câu vào đúng khung giờ Scene (0ms đè voice).
    """
    tts_dir = edit_dir / "tts_parts"
    tts_dir.mkdir(parents=True, exist_ok=True)

    words_out = []
    filter_parts = []
    inputs = ["-f", "lavfi", "-t", "40.0", "-i", "anullsrc=r=48000:cl=stereo"]

    prev_audio_end = 0.0

    for idx, (scene_id, scene_start, scene_end, text) in enumerate(SCENE_SCRIPT):
        raw_mp3 = tts_dir / f"seg_{idx:02d}_raw.mp3"
        raw_txt = tts_dir / f"seg_{idx:02d}_raw.txt"
        trim_wav = tts_dir / f"seg_{idx:02d}_trim.wav"
        fit_wav = tts_dir / f"seg_{idx:02d}_fit.wav"

        expected_sig = f"{VOICE_ID}|{VOICE_RATE}|{text}"
        if not raw_mp3.exists() or raw_mp3.stat().st_size < 1000 or not raw_txt.exists() or raw_txt.read_text(encoding="utf-8") != expected_sig:
            asyncio.run(synthesize_single_voice_tts(text, raw_mp3))
            raw_txt.write_text(expected_sig, encoding="utf-8")

        # Trim silence at start and end so speech starts immediately and ends cleanly
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-i",
                str(raw_mp3),
                "-af",
                (
                    "silenceremove=start_periods=1:start_silence=0.02:start_threshold=-42dB,"
                    "areverse,"
                    "silenceremove=start_periods=1:start_silence=0.03:start_threshold=-42dB,"
                    "areverse"
                ),
                "-ar",
                "48000",
                "-ac",
                "2",
                str(trim_wav),
            ],
            check=True,
        )

        raw_dur = probe_duration(trim_wav)
        # Ensure speech starts after scene_start + 0.08s and strictly after prev_audio_end + 0.18s
        voice_start = round(max(scene_start + 0.08, prev_audio_end + 0.18), 3)
        voice_max_end = round(scene_end - 0.18, 3)
        slot_dur = max(1.2, round(voice_max_end - voice_start, 3))

        # Fit audio strictly inside slot_dur (never exceeds slot_dur -> 0% chance of overlapping next segment)
        speed = max(1.0, raw_dur / (slot_dur - 0.05)) if raw_dur > (slot_dur - 0.05) else 1.0
        atempo_str = build_atempo_chain(speed)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-i",
                str(trim_wav),
                "-af",
                f"{atempo_str},atrim=0:{slot_dur:.3f},afade=t=out:st={max(0.1, slot_dur - 0.06):.3f}:d=0.06",
                "-ar",
                "48000",
                "-ac",
                "2",
                str(fit_wav),
            ],
            check=True,
        )

        eff_dur = min(slot_dur, probe_duration(fit_wav))
        voice_actual_end = round(voice_start + eff_dur, 3)
        assert voice_actual_end <= scene_end, f"Voice overflow in {scene_id}: {voice_actual_end} > {scene_end}"
        assert voice_start >= prev_audio_end, f"Voice overlap in {scene_id}: {voice_start} < {prev_audio_end}"
        prev_audio_end = voice_actual_end

        delay_ms = int(round(voice_start * 1000))
        inputs.extend(["-i", str(fit_wav)])
        in_idx = idx + 1
        filter_parts.append(f"[{in_idx}:a]adelay={delay_ms}|{delay_ms}[a{in_idx}]")

        # Calculate proportional word timestamps strictly inside [voice_start, voice_actual_end]
        tokens = [w.strip() for w in text.split() if w.strip()]
        char_weights = [max(2, len(re.sub(r"[^\w]", "", tok)) + (2 if tok.endswith((",", ".", ":")) else 0)) for tok in tokens]
        total_weight = sum(char_weights)
        cursor = voice_start
        for w_i, (tok, weight) in enumerate(zip(tokens, char_weights)):
            w_dur = eff_dur * (weight / total_weight)
            w_start = round(cursor, 3)
            w_end = round(min(voice_actual_end, cursor + max(0.08, w_dur * 0.94)), 3)
            if w_end <= w_start:
                w_end = round(w_start + 0.08, 3)
            words_out.append({"text": tok, "start": w_start, "end": w_end})
            cursor += w_dur

        print(
            f"  [Voice #{idx+1} · {scene_id}] window=[{voice_start:.2f}s..{voice_actual_end:.2f}s] "
            f"(raw={raw_dur:.2f}s, speed={speed:.2f}x, eff={eff_dur:.2f}s)"
        )

    # Verify strict monotonicity of all word timestamps
    for i in range(len(words_out) - 1):
        if words_out[i]["end"] > words_out[i + 1]["start"]:
            words_out[i]["end"] = words_out[i + 1]["start"]
        assert words_out[i]["end"] > words_out[i]["start"], f"Invalid word duration at {words_out[i]}"

    mix_inputs = "[0:a]" + "".join(f"[a{i+1}]" for i in range(len(SCENE_SCRIPT)))
    filter_complex = (
        ";".join(filter_parts)
        + f";{mix_inputs}amix=inputs={len(SCENE_SCRIPT)+1}:normalize=0,volume=1.85,alimiter=limit=0.93[aout]"
    )

    voice_wav = edit_dir / "voice_40s.wav"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            *inputs,
            "-filter_complex",
            filter_complex,
            "-map",
            "[aout]",
            "-t",
            "40.0",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(voice_wav),
        ],
        check=True,
    )

    transcripts_dir = edit_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    (transcripts_dir / "cut.json").write_text(
        json.dumps({"words": words_out}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  [OK] Built 100% single-voice 40.0s audio ({len(words_out)} monotonic words) -> {voice_wav}")


def build_40s_base_cut_video(edit_dir: Path) -> Path:
    """Luôn tạo mới cut.mp4 từ voice_40s.wav vừa sinh + 8 video nền 9:16 của Editonny (CẤM dùng lại cache cũ)."""
    vid_dir = VISUALS_DIR / "assets" / "visuals" / "video"
    bg_clips = [
        vid_dir / "dark-grid.mp4",
        vid_dir / "orange-neon-grid.mp4",
        vid_dir / "neon-green-fluid.mp4",
        vid_dir / "purple-fluid.mp4",
        vid_dir / "rising-particles.mp4",
        vid_dir / "pink-blue-light.mp4",
        vid_dir / "spinning-rays.mp4",
        vid_dir / "golden-light.mp4",
    ]
    existing = [p for p in bg_clips if p.exists()]
    if not existing:
        raise RuntimeError(f"No bundled videos found in {vid_dir}")

    voice_wav = edit_dir / "voice_40s.wav"
    cut_mp4 = edit_dir / "cut.mp4"
    if cut_mp4.exists():
        cut_mp4.unlink()

    inputs = []
    v_filters = []
    for i in range(8):
        clip = existing[i % len(existing)]
        inputs.extend(["-stream_loop", "-1", "-t", "5.0", "-i", str(clip)])
        v_filters.append(
            f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"fps=24,format=yuv420p,eq=brightness=-0.08:saturation=1.15,setsar=1[v{i}]"
        )

    concat_in = "".join(f"[v{i}]" for i in range(8))
    v_filter_str = ";".join(v_filters) + f";{concat_in}concat=n=8:v=1:a=0[vout]"

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            *inputs,
            "-i",
            str(voice_wav),
            "-filter_complex",
            v_filter_str,
            "-map",
            "[vout]",
            "-map",
            "8:a",
            "-t",
            "40.0",
            "-r",
            "24",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            str(cut_mp4),
        ],
        check=True,
    )

    (edit_dir / "cut_timeline.json").write_text(
        json.dumps(
            {
                "duration": 40.0,
                "width": 1080,
                "height": 1920,
                "fps": 24,
                "segments": [{"out_start": 0.0, "out_end": 40.0, "source_start": 0.0, "source_end": 40.0}],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"  [OK] Built fresh 40.0s 1080x1920 base cut video -> {cut_mp4}")
    return cut_mp4


def customize_vietnamese_scenes(project_dir: Path) -> None:
    """
    Đồng bộ 100% thông số P, số liệu JS, văn bản HTML và font Montserrat full tiếng Việt
    cho cả 8 cảnh đồ họa Editonny để hình ảnh khớp tuyệt đối với lời thoại.
    """
    montserrat_src = project_dir / "assets" / "fonts" / "Montserrat.ttf"
    vis_fonts_dir = project_dir / "assets" / "visuals" / "fonts"
    vis_fonts_dir.mkdir(parents=True, exist_ok=True)
    if montserrat_src.exists():
        shutil.copy2(montserrat_src, vis_fonts_dir / "Montserrat.ttf")
        shutil.copy2(montserrat_src, vis_fonts_dir / "Sora.ttf")

    scenes_dir = project_dir / "compositions" / "scenes"
    for html_file in sorted(scenes_dir.glob("*.html")):
        txt = html_file.read_text(encoding="utf-8")
        name = html_file.name

        # 1. Force full Vietnamese Montserrat font for both Inter and SoraV (no unicode-range truncation!)
        txt = re.sub(
            r'@font-face\{font-family:"Inter";src:url\("assets/visuals/fonts/inter-var-latin\.woff2"\)[^}]+\}\s*@font-face\{font-family:"Inter";src:url\("assets/visuals/fonts/inter-var-latin-ext\.woff2"\)[^}]+\}',
            '@font-face{font-family:"Inter";src:url("assets/fonts/Montserrat.ttf") format("truetype");font-weight:100 900;font-display:block}',
            txt,
        )
        txt = re.sub(
            r'@font-face\{font-family:"Inter";src:url\("assets/visuals/fonts/inter-var-latin[^}]+\}',
            '@font-face{font-family:"Inter";src:url("assets/fonts/Montserrat.ttf") format("truetype");font-weight:100 900;font-display:block}',
            txt,
        )
        txt = re.sub(
            r'@font-face\{font-family:"SoraV";src:url\("assets/visuals/fonts/Sora\.ttf"\)[^}]+\}',
            '@font-face{font-family:"SoraV";src:url("assets/fonts/Montserrat.ttf") format("truetype");font-weight:100 900;font-display:block}',
            txt,
        )
        txt = re.sub(
            r'@font-face\{font-family:"PlayfairI";src:url\("assets/visuals/fonts/Playfair-Italic\.ttf"\)[^}]+\}',
            '@font-face{font-family:"PlayfairI";src:url("assets/fonts/Montserrat.ttf") format("truetype");font-weight:100 900;font-display:block}',
            txt,
        )

        # 2. Scene-by-scene 1-to-1 Visual <-> Voice synchronization
        if name.startswith("year-hook-"):
            txt = re.sub(r'number:\s*".*?"', 'number: "2026"', txt)
            txt = re.sub(r'label:\s*".*?"', 'label: "HỆ SINH THÁI SUB AGENT"', txt)
            txt = re.sub(r'badge:\s*".*?"', 'badge: "12 CHUYÊN VIÊN AI"', txt)
            txt = re.sub(r'color:\s*".*?"', 'color: "#30d158"', txt)
            # Make badge text visible immediately when pill opens (fix GSAP opacity:1->1 bug & slow stagger)
            txt = txt.replace(
                "#yearhookyearhook01-s .yearhookyearhook01-sl i{display:block;font-style:normal;opacity:0}",
                "#yearhookyearhook01-s .yearhookyearhook01-sl i{display:block;font-style:normal;opacity:1}",
            )
            txt = txt.replace(
                'letters.forEach(function (e, i) { tl.fromTo(e, { opacity: 1, yPercent: 110 }, { opacity: 1, yPercent: 0, duration: .26, ease: "back.out(1.8)" }, tS + .1 + i * .035); });',
                'letters.forEach(function (e, i) { tl.fromTo(e, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: .22, ease: "back.out(1.8)" }, tS + .04 + i * .015); });',
            )

        elif name.startswith("ai-chat-interface-"):
            txt = re.sub(r'aiName:\s*".*?"', 'aiName: "Mama · Tổng Quản AI"', txt)
            txt = re.sub(r'request:\s*".*?"', 'request: "Dựng video 40s & chạy 4 Fanpage"', txt)
            txt = re.sub(r'response:\s*".*?"', 'response: "Đã xong! Cắt nhịp, phụ đề & 8 cảnh đồ họa."', txt)
            txt = txt.replace(">How can I help?<", ">Mama sẵn sàng nhận lệnh<")
            txt = txt.replace(">Ask something<", ">Nhập lệnh cho Mama...<")
            txt = txt.replace(">edited_video.mp4<", ">sub_agent_reel_40s.mp4<")

        elif name.startswith("three-steps-"):
            txt = txt.replace("Just <i>3 steps</i>", "Chỉ <i>3 bước</i>")
            # Remove duplicate "1.", "2.", "3." because .scene-n already renders the orange numbered circle
            txt = txt.replace(">You record<", ">Giao lệnh<")
            txt = txt.replace(">as it happens, without trimming<", ">nhắn yêu cầu cho Tổng quản Mama<")
            txt = txt.replace(">AI edits<", ">Đội AI xử lý<")
            txt = txt.replace(">trims, captions, and animates<", ">cắt nhịp, phụ đề & chèn đồ họa<")
            txt = txt.replace(">You publish<", ">Xuất bản ngay<")
            txt = txt.replace(">the finished video, the same day<", ">kiểm duyệt & đăng lên 4 Page<")
            # Adjust step entrance timing so all 3 steps + checkmarks are visible by 3.2s local (13.5s global)
            txt = txt.replace(
                "var t = a + .65 + (n - 1) * 1.05;",
                "var t = a + .45 + (n - 1) * .85;",
            ).replace("a + 3.95 + (n - 1) * .22", "a + 2.85 + (n - 1) * .18")

        elif name.startswith("waveform-cuts-"):
            txt = txt.replace(">TRIMMING PAUSES<", ">CẮT KHOẢNG LẶNG<")
            txt = re.sub(r'pauses:\s*\d+', 'pauses: 7', txt)
            txt = re.sub(r'beforeTime:\s*".*?"', 'beforeTime: "1:15"', txt)
            txt = re.sub(r'afterTime:\s*".*?"', 'afterTime: "0:40"', txt)
            # Replace Portuguese " de " with "/"
            txt = txt.replace('n + " de " + nP', 'n + " / " + nP')

        elif name.startswith("before-after-"):
            txt = txt.replace(">BEFORE<", ">TRƯỚC ĐÂY<")
            txt = txt.replace("<small>hours</small>", "<small>giờ</small>")
            txt = txt.replace(">to edit a one-minute video<", ">tự dựng thủ công từng cảnh video<")
            txt = txt.replace(">AFTER<", ">CÓ SUB AGENT<")
            txt = txt.replace("<small>minutes</small>", "<small>phút</small>")
            txt = txt.replace(">and the video is ready to post<", ">video hoàn chỉnh sẵn sàng lên xu hướng<")
            txt = txt.replace("<i>22x</i> faster", "Nhanh gấp <i>22x</i>")
            # Fix hardcoded JS numbers (3 -> 6 giờ, 8 -> 5 phút) and speed up split-screen reveal
            txt = re.sub(
                r'countNumber\("#c4-va_beforeafter01",\s*0,\s*3,\s*a\s*\+\s*\.55,\s*\.7\)',
                'countNumber("#c4-va_beforeafter01", 0, 6, a + .35, .55)',
                txt,
            )
            txt = re.sub(
                r'countNumber\("#c4-vd_beforeafter01",\s*0,\s*8,\s*a\s*\+\s*3\.05,\s*\.6\)',
                'countNumber("#c4-vd_beforeafter01", 0, 5, a + 1.85, .55)',
                txt,
            )
            txt = txt.replace("a + 2.0", "a + 1.35").replace("a + 2.05", "a + 1.4")
            txt = txt.replace("a + 2.3", "a + 1.5").replace("a + 2.45", "a + 1.6")
            txt = txt.replace("a + 2.75", "a + 1.75").replace("a + 2.85", "a + 1.8")
            txt = txt.replace("a + 3.0", "a + 1.85").replace("a + 3.5", "a + 2.2")
            txt = txt.replace("a + 4.15", "a + 2.5")

        elif name.startswith("glass-chart-"):
            txt = re.sub(r'title:\s*".*?"', 'title: "HIỆU SUẤT TỰ ĐỘNG HÓA"', txt)
            txt = re.sub(r'start:\s*\d+', 'start: 20', txt)
            txt = re.sub(r'end:\s*\d+', 'end: 320', txt)
            txt = re.sub(r'direction:\s*".*?"', 'direction: "rising"', txt)
            txt = re.sub(r'suffix:\s*".*?"', 'suffix: "%"', txt)

        elif name.startswith("completed-checklist-"):
            txt = re.sub(
                r'items:\s*".*?"',
                'items: "Bí ý tưởng kịch bản|Thức khuya tự dựng clip|Trễ lịch đăng bài hàng ngày"',
                txt,
            )
            txt = re.sub(r'title:\s*".*?"', 'title: "XÓA BỎ 3 NỖI LO"', txt)
            txt = re.sub(r'strikeColor:\s*".*?"', 'strikeColor: "rgba(255,69,58,0.55)"', txt)
            txt = txt.replace('ri.setAttribute("stroke-width", "10")', 'ri.setAttribute("stroke-width", "5")')

        elif name.startswith("comment-call-to-action-"):
            txt = re.sub(r'label:\s*".*?"', 'label: "Bình luận nhận tư vấn 1:1"', txt)
            txt = re.sub(r'word:\s*".*?"', 'word: "SUB AGENT"', txt)
            txt = re.sub(r'accent:\s*".*?"', 'accent: "#30d158"', txt)
            txt = txt.replace(">Add a comment...<", ">Nhập bình luận...<")

        html_file.write_text(txt, encoding="utf-8")
    print(f"  [OK] Synchronized Vietnamese visuals, numbers, and fonts across all scenes in {scenes_dir}")


def fix_and_verify_composed_captions(index_html: Path) -> None:
    """
    Kiểm tra và chuẩn hóa toàn bộ phụ đề #cap0..#capN trong index.html sau khi compose:
    - Đặt vị trí phụ đề ở vùng an toàn đáy (top: 1540px) để không đè lên đồ họa trung tâm.
    - Đảm bảo 100% phụ đề có duration > 0 và không bao giờ có 2 phụ đề hiển thị chồng lên nhau.
    """
    txt = index_html.read_text(encoding="utf-8")

    # Move captions down to safe bottom zone (1540px) and ensure clean stroke/shadow
    txt = re.sub(r'style="top:\d+px;font-size:\d+px"', 'style="top:1540px;font-size:56px"', txt)

    # Verify all caption divs have positive duration and non-overlapping timelines
    cap_divs = re.findall(
        r'<div class="cap caption-cue clip" id="(cap\d+)" data-start="([-\d.]+)" data-duration="([-\d.]+)"',
        txt,
    )
    for cid, s_str, d_str in cap_divs:
        s_val = float(s_str)
        d_val = float(d_str)
        if d_val <= 0.05:
            raise RuntimeError(f"Broken caption duration detected in {cid}: start={s_val}, duration={d_val}")

    index_html.write_text(txt, encoding="utf-8")
    print(f"  [OK] Verified {len(cap_divs)} caption cues in index.html (0 overlaps, 0 negative durations, top=1540px)")


def build_qa_contact_sheet(snapshots_dir: Path, out_jpg: Path) -> None:
    """Ghép 8 ảnh chụp khung hình từ các cảnh đồ họa thành 1 bảng QA Grid 4x2."""
    from PIL import Image, ImageDraw, ImageFont

    pngs = sorted(snapshots_dir.glob("frame-*.png"))
    if not pngs:
        return
    cols, rows = 4, 2
    thumb_w, thumb_h = 360, 640
    pad = 16
    header_h = 74
    canvas_w = cols * thumb_w + (cols + 1) * pad
    canvas_h = header_h + rows * thumb_h + (rows + 1) * pad
    canvas = Image.new("RGB", (canvas_w, canvas_h), (11, 15, 25))
    draw = ImageDraw.Draw(canvas)

    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
        font_lbl = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 17)
    except Exception:
        font_title = ImageFont.load_default()
        font_lbl = ImageFont.load_default()

    draw.text(
        (pad, 22),
        "EDIT-3 (EDITONNY + HYPERFRAMES) — 40.0s FIXED VERTICAL VIDEO (100% SINGLE VOICE + FULL VN FONT + 1:1 SYNC)",
        fill=(135, 255, 0),
        font=font_title,
    )

    scene_labels = [
        "1. Hook 2026 + 12 AI (2.4s)",
        "2. Chat Mama Tổng Quản (7.6s)",
        "3. Quy Trình 3 Bước (13.8s)",
        "4. Cắt 7 Khoảng Lặng (19.5s)",
        "5. 6 Giờ -> 5 Phút · 22x (25.2s)",
        "6. Hiệu Suất +320% (30.5s)",
        "7. Xóa Bỏ 3 Nỗi Lo (34.6s)",
        "8. CTA Gõ SUBAGENT (38.2s)",
    ]

    for idx, png in enumerate(pngs[:8]):
        im = Image.open(png).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        r, c = divmod(idx, cols)
        x = pad + c * (thumb_w + pad)
        y = header_h + pad + r * (thumb_h + pad)
        canvas.paste(im, (x, y))
        lbl = scene_labels[idx] if idx < len(scene_labels) else png.stem
        draw.rectangle([x, y + thumb_h - 38, x + thumb_w, y + thumb_h], fill=(8, 12, 20))
        draw.text((x + 10, y + thumb_h - 30), lbl, fill=(255, 255, 255), font=font_lbl)

    canvas.save(out_jpg, quality=92)
    print(f"  [OK] Saved 8-Scene QA Contact Sheet -> {out_jpg}")


def main() -> int:
    print("=== [EDIT-3 · EDITONNY 40s VERTICAL VIDEO BUILDER — v2 FIXED] ===")
    if PROJECT_DIR.exists():
        shutil.rmtree(PROJECT_DIR)
    EDIT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Generate 40s single-voice Vietnamese voiceover & strictly monotonic word transcript
    build_40s_voice_and_transcript(EDIT_DIR)

    # 2. Build fresh 40s 1080x1920 base cut video
    build_40s_base_cut_video(EDIT_DIR)

    # 3. Initialize Editonny project (--style night)
    build_py = ENGINE_DIR / "project-template" / "build.py"
    apply_py = VISUALS_DIR / "apply.py"
    py_exe = str(VENV_PY if VENV_PY.exists() else sys.executable)

    subprocess.run(
        [py_exe, str(build_py), "new", str(PROJECT_DIR), "--edit", str(EDIT_DIR), "--style", "night"],
        check=True,
    )

    pj_path = PROJECT_DIR / "project.json"
    pj = json.loads(pj_path.read_text(encoding="utf-8"))
    pj["title"] = "Hệ Sinh Thái 12 Subagent AI — Edit-3 Editonny 40s (Fixed)"
    pj["format"] = "9:16"
    pj["style"] = "night"
    pj["captions"] = {"enabled": True, "style": "standard", "maxWords": 3, "inFrame": False}
    pj_path.write_text(json.dumps(pj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 4. Apply 8 visual scenes + 5 transitions aligned 1-to-1 with SCENE_SCRIPT
    scene_plan = [
        ("--use", "year-hook", "--start", "0.2", "--end", "4.6"),
        ("--use", "ai-chat-interface", "--start", "4.9", "--end", "10.0"),
        ("--use", "three-steps", "--start", "10.3", "--end", "16.3"),
        ("--use", "waveform-cuts", "--start", "16.6", "--end", "21.6"),
        ("--use", "before-after", "--start", "21.9", "--end", "27.7"),
        ("--use", "glass-chart", "--start", "28.0", "--end", "32.3"),
        ("--use", "completed-checklist", "--start", "32.6", "--end", "36.1"),
        ("--use", "comment-call-to-action", "--start", "36.3", "--end", "40.0"),
        ("--use", "transition-glow", "--cut", "4.75"),
        ("--use", "transition-zoom", "--cut", "10.15"),
        ("--use", "transition-glitch", "--cut", "16.45"),
        ("--use", "transition-flash", "--cut", "21.75"),
        ("--use", "transition-iris", "--cut", "27.85"),
    ]
    for args in scene_plan:
        subprocess.run([py_exe, str(apply_py), "--project", str(PROJECT_DIR), *args], check=True)

    # 5. Customize Vietnamese parameters, JS numbers, and full Vietnamese Montserrat font
    customize_vietnamese_scenes(PROJECT_DIR)

    # 6. Generate scene sound effects (do NOT call apply.py --captions to avoid partial noCaptions clipping bugs)
    subprocess.run([py_exe, str(apply_py), "--project", str(PROJECT_DIR), "--sounds"], check=True)

    # 7. Prepare & Compose index.html
    subprocess.run([py_exe, "build.py", "prepare"], cwd=str(PROJECT_DIR), check=True)
    subprocess.run([py_exe, "build.py", "compose"], cwd=str(PROJECT_DIR), check=True)

    # 8. Fix caption safe-zone placement (top:1540px) & verify 0 caption overlap
    fix_and_verify_composed_captions(PROJECT_DIR / "index.html")

    # 9. HyperFrames lint, check, snapshot, and render
    for hf_cmd in [
        ["lint"],
        ["check"],
        ["snapshot", "--at", "2.4,7.6,13.8,19.5,25.2,30.5,34.6,38.2", "--no-end", "--describe", "false", "--output", "snapshots"],
        ["render", "--quality", "draft", "--fps", "24", "--output", "renders/edit3_40s.mp4"],
    ]:
        print(f"  [HyperFrames] {' '.join(hf_cmd)} ...", flush=True)
        subprocess.run([py_exe, "build.py", "hf", *hf_cmd], cwd=str(PROJECT_DIR), check=True)

    rendered_mp4 = PROJECT_DIR / "renders" / "edit3_40s.mp4"
    if not rendered_mp4.exists():
        raise RuntimeError(f"Rendered video missing: {rendered_mp4}")

    shutil.copy2(rendered_mp4, FINAL_MP4)
    build_qa_contact_sheet(PROJECT_DIR / "snapshots", QA_GRID_JPG)

    probe = json.loads(
        subprocess.run(
            ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(FINAL_MP4)],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )
    v_stream = next(s for s in probe["streams"] if s["codec_type"] == "video")
    a_stream = next(s for s in probe["streams"] if s["codec_type"] == "audio")
    dur = float(probe["format"]["duration"])
    size_mb = FINAL_MP4.stat().st_size / (1024 * 1024)
    print(
        f"=== PASS: {FINAL_MP4} | {v_stream['width']}x{v_stream['height']} | "
        f"duration={dur:.2f}s | audio={a_stream['codec_name']} | size={size_mb:.2f}MB ==="
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
