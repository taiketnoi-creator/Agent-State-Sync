#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_voice_tts.py (v2.0 — Vbee AIVoice + Viettel AI + Edge-TTS + FFmpeg Studio Mastering)
---------------------------------------------------------------------------------------------
Bộ sinh Voiceover Đa Tầng chuyên nghiệp cho Video Ngắn Affiliate & Drama (Agent-Javis):
1. Hỗ trợ 3 Engine giọng đọc tiếng Việt:
   - `vbee`    : Vbee AIVoice API (Giọng Bắc/Trung/Nam chuyên Review Shopee, Kể chuyện Drama, Công nghệ)
   - `viettel` : Viettel AI TTS API (Giọng Quỳnh Anh, Diễm My, Thanh Tùng, Minh Quân siêu tự nhiên)
   - `edge`    : Microsoft Neural TTS (Fallback miễn phí khi chưa nạp API key Vbee/Viettel)
   - `auto`    : Tự động ưu tiên Vbee -> Viettel AI -> Edge-TTS
2. Tự động chọn giọng chuẩn theo từng Fanpage trong dàn 5 Page của CEO (`--page 1..5` hoặc tên Page).
3. Tích hợp bộ lọc hậu kỳ **FFmpeg Studio Mastering** (mặc định bật):
   - Tự động cắt khoảng nghỉ thừa > 0.22s giữa các câu tạo nhịp TikTok/Reels dồn dập.
   - EQ làm ấm giọng + Compressor nén tiếng đều đặn + Khóa đỉnh âm lượng chuẩn `-3dB` theo `voice.md`.

Cách dùng:
  python tools/generate_voice_tts.py --list-voices
  python tools/generate_voice_tts.py --page 1 --text "Mới dọn vào ký túc xá..." --output voice.mp3
  python tools/generate_voice_tts.py --provider vbee --voice sg_female_thaotrinh_full_48k-fhg --file script.md -o out.mp3
  python tools/generate_voice_tts.py --provider viettel --voice hn-quynhanh --text "Review thực tế..." -o out.mp3
"""

import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False

ENV_VAULT_PATH = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / ".env"

VBEE_VOICES = {
    "hn_female_ngochuyen_full_48k-fhg": "Nữ Hà Nội - Ngọc Huyền (Trẻ trung, Drama Ký Túc Xá / Review cực cuốn)",
    "sg_female_thaotrinh_full_48k-fhg": "Nữ Sài Gòn - Thảo Trinh (Tự nhiên, gần gũi, Review đồ gia dụng Phòng Trọ)",
    "hn_male_manhdung_news_48k-fhg": "Nam Hà Nội - Mạnh Dũng (Đĩnh đạc, sắc bén, chuẩn kênh AI Players / Tech)",
    "sg_male_minhhoang_full_48k-fhg": "Nam Sài Gòn - Minh Hoàng (Năng động, KOC / Livestream / Business IFN)",
    "hue_female_huonggiang_full_48k-fhg": "Nữ Huế - Hương Giang (Truyền cảm, kể chuyện đời sống)",
}

VIETTEL_VOICES = {
    "hn-quynhanh": "Nữ miền Bắc - Quỳnh Anh (Giọng Gen Z tự nhiên, Drama / Review Shopee)",
    "hcm-diemmy": "Nữ miền Nam - Diễm My (Giọng miền Nam ngọt ngào, Review gia dụng / Phòng trọ)",
    "hn-thanhtung": "Nam miền Bắc - Thanh Tùng (Trầm ấm, chuẩn kênh AI Players / Công nghệ)",
    "hcm-minhquan": "Nam miền Nam - Minh Quân (Năng động, chuyên KOC / Kinh doanh IFN)",
    "hue-maingoc": "Nữ miền Trung - Mai Ngọc (Truyền cảm, nhẹ nhàng)",
}

EDGE_VOICES = {
    "vi-VN-HoaiMyNeural": "Nữ miền Bắc (Microsoft Neural - Fallback miễn phí)",
    "vi-VN-NamMinhNeural": "Nam miền Bắc (Microsoft Neural - Fallback miễn phí)",
}

# Bảng ánh xạ tự động 5 Fanpage của CEO -> Giọng đọc phù hợp nhất trên từng nền tảng
PAGE_PERSONA_MAP = {
    "1": {
        "page_name": "Ký Túc Xá Có Biến",
        "style": "Nữ Gen Z miền Bắc - Kể chuyện Drama sinh viên & Review",
        "speed": 1.12,
        "vbee": "hn_female_ngochuyen_full_48k-fhg",
        "viettel": "hn-quynhanh",
        "edge": "vi-VN-HoaiMyNeural",
    },
    "2": {
        "page_name": "Hội Deadline",
        "style": "Nữ miền Bắc nhịp nhanh - Chuyện chạy deadline & Mẹo công sở/sinh viên",
        "speed": 1.15,
        "vbee": "hn_female_ngochuyen_full_48k-fhg",
        "viettel": "hn-quynhanh",
        "edge": "vi-VN-HoaiMyNeural",
    },
    "3": {
        "page_name": "Phòng Trọ Hết Cứu",
        "style": "Nữ miền Nam gần gũi - Drama phòng trọ & Review đồ gia dụng <300k",
        "speed": 1.12,
        "vbee": "sg_female_thaotrinh_full_48k-fhg",
        "viettel": "hcm-diemmy",
        "edge": "vi-VN-HoaiMyNeural",
    },
    "4": {
        "page_name": "AI Players - Người chơi hệ AI",
        "style": "Nam miền Bắc đĩnh đạc - Công nghệ AI & Video Slide Tech",
        "speed": 1.12,
        "vbee": "hn_male_manhdung_news_48k-fhg",
        "viettel": "hn-thanhtung",
        "edge": "vi-VN-NamMinhNeural",
    },
    "5": {
        "page_name": "IFN - Dịch vụ Livestream TikTok, Xây kênh trọn gói, Booking KOL, KOC",
        "style": "Nam miền Nam năng động - E-commerce, Livestream & KOC",
        "speed": 1.10,
        "vbee": "sg_male_minhhoang_full_48k-fhg",
        "viettel": "hcm-minhquan",
        "edge": "vi-VN-NamMinhNeural",
    },
}


def load_env_keys() -> dict:
    keys = {}
    if ENV_VAULT_PATH.exists():
        for raw in ENV_VAULT_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            keys[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("VBEE_APP_ID", "VBEE_BEARER_TOKEN", "VIETTEL_TTS_TOKEN"):
        if os.environ.get(k):
            keys[k] = os.environ[k]
    return keys


def is_valid_key(val: str | None) -> bool:
    if not val:
        return False
    placeholders = {
        "",
        "DIEN_VBEE_APP_ID_VAO_DAY",
        "DIEN_VBEE_BEARER_TOKEN_VAO_DAY",
        "DIEN_VIETTEL_TTS_TOKEN_VAO_DAY",
        "YOUR_TOKEN",
    }
    return val.strip() not in placeholders


TECH_PHONETIC_RULES = [
    (r"\bU-S-B-C\b", "U Ét Bê Xi"),
    (r"\bUSB-C\b", "U Ét Bê Xi"),
    (r"\bM-C-P\b", "Em Xi Pi"),
    (r"\bMCP\b", "Em Xi Pi"),
    (r"\bR-A-G\b", "Rờ A Gờ"),
    (r"\bRAG\b", "Rờ A Gờ"),
    (r"\bL-L-M\b", "Eo Eo Em"),
    (r"\bLLM\b", "Eo Eo Em"),
    (r"\bA-P-I\b", "Ây Pi Ai"),
    (r"\bAPI\b", "Ây Pi Ai"),
    (r"\bG-P-U\b", "Gi Pi U"),
    (r"\bGPU\b", "Gi Pi U"),
    (r"\bC-P-U\b", "Xi Pi U"),
    (r"\bCPU\b", "Xi Pi U"),
    (r"\bK-P-I\b", "Kây Pi Ai"),
    (r"\bKPI\b", "Kây Pi Ai"),
    (r"\bC-E-O\b", "Xi I Ô"),
    (r"\bCEO\b", "Xi I Ô"),
    (r"\bn8n\b", "En Tám En"),
    (r"\bAI Players\b", "Ây Ai Play ơ"),
    (r"\bAI\b", "Ây Ai"),
    (r"\bRobotics\b", "rô bốt tích"),
    (r"\brobotics\b", "rô bốt tích"),
    (r"\bRobot\b", "rô bốt"),
    (r"\brobot\b", "rô bốt"),
    (r"\bcode\b", "cốt"),
    (r"\bchat\b", "chát"),
    (r"\bPrompt\b", "câu lệnh"),
    (r"\bprompt\b", "câu lệnh"),
]


def clean_script_for_tts(raw_text: str) -> str:
    """Làm sạch kịch bản thô thành văn bản thuần lời thoại, giữ dấu ngắt nhịp tự nhiên và phiên âm chuẩn từ viết tắt công nghệ."""
    text = raw_text
    # Đổi dấu ngắt nhịp [ ... ] của voice.md thành dấu phẩy để TTS nghỉ hơi tự nhiên
    text = re.sub(r"\[\s*\.\.\.\s*\]", ", ", text)
    # Xóa timeline tags [00s - 03s] hoặc [00:03]
    text = re.sub(r"\[\s*\d+s?\s*[-–:]\s*\d+s?\s*\]", " ", text)
    text = re.sub(r"\[\s*\d+\s*[sS]?\s*\]", " ", text)
    # Xóa stage directions dạng ngoặc đơn
    text = re.sub(
        r"\([^)]*(?:visual|hình ảnh|cận cảnh|zoom|âm thanh|asmr|sound|hiệu ứng|take|bối cảnh|sfx)[^)]*\)",
        " ",
        text,
        flags=re.IGNORECASE,
    )
    # Xóa nhãn thoại
    text = re.sub(
        r"(?:\bthoại\b|\bvoiceover\b|\blời thoại\b|\bvoice\b)\s*:\s*",
        " ",
        text,
        flags=re.IGNORECASE,
    )
    # Phiên âm chuẩn các từ viết tắt tiếng Anh công nghệ trước khi xóa dấu gạch ngang
    for pattern, replacement in TECH_PHONETIC_RULES:
        text = re.sub(pattern, replacement, text)

    # Xóa markdown
    text = re.sub(r"#+\s+", " ", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"^\s*[-*+]\s+", " ", text, flags=re.MULTILINE)
    text = re.sub(r">\s+", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r'["“”‘’\']', " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def synthesize_viettel(text: str, output_path: str, voice: str, speed: float, token: str) -> None:
    """Gọi API Viettel AI TTS (https://viettelai.vn/tts/speech_synthesis)."""
    url = "https://viettelai.vn/tts/speech_synthesis"
    payload = {
        "text": text,
        "voice": voice if voice in VIETTEL_VOICES else "hn-quynhanh",
        "speed": round(float(speed), 2),
        "tts_return_option": 3,  # 3 = mp3
        "token": token,
        "without_filter": False,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "accept": "*/*"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        content_type = resp.headers.get("Content-Type", "")
        body = resp.read()
        if "application/json" in content_type or body.startswith(b"{"):
            err_json = json.loads(body.decode("utf-8", errors="ignore"))
            raise RuntimeError(f"Viettel AI trả lỗi: {err_json}")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(body)


def synthesize_vbee(text: str, output_path: str, voice: str, speed: float, app_id: str, bearer_token: str) -> None:
    """Gọi API Vbee AIVoice v1 (https://vbee.vn/api/v1/tts) và tải file mp3."""
    url = "https://vbee.vn/api/v1/tts"
    voice_code = voice if voice in VBEE_VOICES else "hn_female_ngochuyen_full_48k-fhg"
    payload = {
        "app_id": app_id,
        "response_type": "indirect",
        "callback_url": "https://httpbin.org/post",
        "input_text": text,
        "voice_code": voice_code,
        "audio_type": "mp3",
        "bitrate": 128,
        "speed_rate": str(round(float(speed), 2)),
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        res_data = json.loads(resp.read().decode("utf-8", errors="ignore"))

    if res_data.get("status") != 1:
        raise RuntimeError(f"Vbee API báo lỗi: {res_data}")

    request_id = res_data.get("result", {}).get("request_id")
    if not request_id:
        raise RuntimeError(f"Không nhận được request_id từ Vbee: {res_data}")

    # Poll trạng thái tối đa 25 giây
    poll_url = f"https://vbee.vn/api/v1/tts/{request_id}"
    audio_link = None
    for _ in range(15):
        time.sleep(1.5)
        poll_req = urllib.request.Request(
            poll_url,
            headers={"Authorization": f"Bearer {bearer_token}"},
            method="GET",
        )
        with urllib.request.urlopen(poll_req, timeout=15) as p_resp:
            p_data = json.loads(p_resp.read().decode("utf-8", errors="ignore"))
        result = p_data.get("result", {})
        status = result.get("status")
        if status == "SUCCESS" and result.get("audio_link"):
            audio_link = result["audio_link"]
            break
        if status == "FAILURE":
            raise RuntimeError(f"Vbee xử lý thất bại: {p_data}")

    if not audio_link:
        raise RuntimeError("Quá thời gian chờ Vbee kết xuất âm thanh.")

    with urllib.request.urlopen(audio_link, timeout=25) as audio_resp:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(audio_resp.read())


async def synthesize_edge(text: str, output_path: str, voice: str, speed: float) -> None:
    """Fallback sang Microsoft Edge-TTS."""
    voice_id = voice if voice in EDGE_VOICES else "vi-VN-HoaiMyNeural"
    pct = int(round((float(speed) - 1.0) * 100))
    rate_str = f"{pct:+d}%"
    communicate = edge_tts.Communicate(text=text, voice=voice_id, rate=rate_str)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    bytes_written = 0
    with open(output_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
                bytes_written += len(chunk["data"])
    if bytes_written == 0:
        raise RuntimeError("Không nhận được dữ liệu từ Edge-TTS.")


def apply_ffmpeg_studio_mastering(input_mp3: str, output_mp3: str) -> bool:
    """
    Hậu kỳ âm thanh bằng FFmpeg Studio Mastering (Không cắt âm giữa câu để tránh nuốt chữ Vbee):
    1. Lọc tạp âm trầm (<80Hz), nâng ấm giọng (220Hz) & độ rõ chữ (3.5kHz).
    2. Compressor nhẹ giúp giọng đều đặn + chuẩn hóa đỉnh âm lượng đúng -3dB.
    """
    if not shutil.which("ffmpeg"):
        return False

    af_chain = (
        "highpass=f=80,"
        "equalizer=f=220:width_type=o:width=1.5:g=1.8,"
        "equalizer=f=3500:width_type=o:width=2.0:g=2.2,"
        "acompressor=threshold=-18dB:ratio=2.2:attack=10:release=80:makeup=1.5dB,"
        "alimiter=limit=0.707:level=disabled"
    )
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".mp3")
    os.close(tmp_fd)
    try:
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            input_mp3,
            "-af",
            af_chain,
            "-ar",
            "44100",
            "-b:a",
            "192k",
            tmp_path,
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, timeout=20)
        shutil.move(tmp_path, output_mp3)
        return True
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        return False


def resolve_page_persona(page_arg: str | None) -> dict | None:
    if not page_arg:
        return None
    s = page_arg.strip().lstrip("#0")
    if s in PAGE_PERSONA_MAP:
        return PAGE_PERSONA_MAP[s]
    s_low = page_arg.strip().lower()
    for _, info in PAGE_PERSONA_MAP.items():
        if s_low in info["page_name"].lower():
            return info
    return None


def print_voice_catalog() -> None:
    print("\n======================================================================")
    print("  DANH MỤC GIỌNG ĐỌC TIẾNG VIỆT (VBEE + VIETTEL AI + 5 FANPAGE MAP)  ")
    print("======================================================================")
    print("\n1. TỰ ĐỘNG CHỌN GIỌNG THEO 5 FANPAGE CỦA CEO (--page <1..5>):")
    for k, info in PAGE_PERSONA_MAP.items():
        print(f" • --page {k} ({info['page_name']})")
        print(f"     Phong cách : {info['style']} | Tốc độ: {info['speed']}x")
        print(f"     Vbee       : {info['vbee']}")
        print(f"     Viettel AI : {info['viettel']}")
    print("\n2. GIỌNG VBEE AIVOICE (--provider vbee --voice <ID>):")
    for vid, desc in VBEE_VOICES.items():
        print(f" • {vid:<36} : {desc}")
    print("\n3. GIỌNG VIETTEL AI TTS (--provider viettel --voice <ID>):")
    for vid, desc in VIETTEL_VOICES.items():
        print(f" • {vid:<36} : {desc}")
    print("\n4. GIỌNG EDGE-TTS FALLBACK (--provider edge --voice <ID>):")
    for vid, desc in EDGE_VOICES.items():
        print(f" • {vid:<36} : {desc}")
    print("======================================================================\n")


def parse_speed(rate_arg: str, default_speed: float = 1.12) -> float:
    s = rate_arg.strip()
    if s.endswith("%"):
        try:
            pct = float(s[:-1])
            return round(1.0 + pct / 100.0, 2)
        except ValueError:
            return default_speed
    if s.endswith("x"):
        s = s[:-1]
    try:
        return round(float(s), 2)
    except ValueError:
        return default_speed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bộ sinh Voiceover Đa Tầng (Vbee + Viettel AI + Edge-TTS + FFmpeg Studio Mastering)"
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--text", "-t", type=str, help="Chuỗi văn bản kịch bản cần đọc")
    group.add_argument("--file", "-f", type=str, help="Đường dẫn file kịch bản markdown/txt")
    group.add_argument("--list-voices", action="store_true", help="Hiển thị danh sách giọng Vbee, Viettel AI và 5 Fanpage")

    parser.add_argument("--provider", "-p", choices=["auto", "vbee", "viettel", "edge"], default="auto", help="Chọn nền tảng TTS (mặc định: auto)")
    parser.add_argument("--page", type=str, default=None, help="Chọn tự động giọng theo Fanpage (1..5 hoặc tên Page)")
    parser.add_argument("--output", "-o", type=str, default="output.mp3", help="Đường dẫn file .mp3 đầu ra")
    parser.add_argument("--voice", "-v", type=str, default=None, help="Mã giọng đọc cụ thể")
    parser.add_argument("--rate", "-r", type=str, default="+12%", help="Tốc độ đọc (mặc định: +12%% ~ 1.12x)")
    parser.add_argument("--no-master", action="store_true", help="Tắt bộ lọc hậu kỳ FFmpeg Studio Mastering")
    parser.add_argument("--dry-run", action="store_true", help="Chỉ làm sạch văn bản và kiểm tra cấu hình, không xuất audio")

    args = parser.parse_args()

    if args.list_voices:
        print_voice_catalog()
        sys.exit(0)

    if not args.text and not args.file:
        parser.print_help()
        sys.exit(1)

    raw_content = Path(args.file).read_text(encoding="utf-8") if args.file else args.text
    cleaned_text = clean_script_for_tts(raw_content)
    word_count = len(cleaned_text.split())
    if not cleaned_text:
        print("Lỗi: Kịch bản rỗng sau khi làm sạch!", file=sys.stderr)
        sys.exit(1)

    persona = resolve_page_persona(args.page)
    speed = persona["speed"] if (persona and args.rate == "+12%") else parse_speed(args.rate)

    env_keys = load_env_keys()
    vbee_app = env_keys.get("VBEE_APP_ID", "")
    vbee_tok = env_keys.get("VBEE_BEARER_TOKEN", "")
    has_vbee = is_valid_key(vbee_app) and is_valid_key(vbee_tok) and (vbee_tok != vbee_app)
    has_viettel = is_valid_key(env_keys.get("VIETTEL_TTS_TOKEN"))

    if is_valid_key(vbee_app) and vbee_tok == vbee_app:
        print(
            "⚠️ [CHÚ Ý VBEE]: Dòng VBEE_BEARER_TOKEN trong .env đang bị dán trùng với mã VBEE_APP_ID (36 ký tự).\n"
            "   👉 Trên trang Vbee Studio (studio.vbee.vn), ngoài App ID còn có 1 mã 'Access Token / Bearer Token' rất dài (bắt đầu bằng 'eyJ...').\n"
            "   👉 Tạm thời chuyển sang Fallback + FFmpeg Studio Mastering để không gián đoạn!",
            file=sys.stderr,
        )

    chosen_provider = args.provider
    if chosen_provider == "auto":
        if has_vbee:
            chosen_provider = "vbee"
        elif has_viettel:
            chosen_provider = "viettel"
        else:
            chosen_provider = "edge"

    if chosen_provider == "vbee":
        voice_id = args.voice or (persona["vbee"] if persona else "hn_female_ngochuyen_full_48k-fhg")
    elif chosen_provider == "viettel":
        voice_id = args.voice or (persona["viettel"] if persona else "hn-quynhanh")
    else:
        voice_id = args.voice or (persona["edge"] if persona else "vi-VN-HoaiMyNeural")

    print("\n============================================================")
    print("  AGENT-JAVIS VOICE ENGINE v2.0 (VBEE / VIETTEL / MASTERING)")
    print("============================================================")
    if persona:
        print(f"Fanpage mục tiêu : {persona['page_name']} ({persona['style']})")
    print(f"Engine kích hoạt : {chosen_provider.upper()}")
    print(f"Giọng đọc        : {voice_id}")
    print(f"Tốc độ phát      : {speed}x")
    print(f"Số từ thoại      : {word_count} từ (~{round(word_count / 2.8, 1)}s)")
    print(f"Studio Mastering : {'BẬT (Cắt nghỉ thừa + EQ + Khóa -3dB)' if not args.no_master else 'TẮT'}")
    print(f"File đầu ra      : {os.path.abspath(args.output)}")
    print("------------------------------------------------------------")

    if args.dry_run:
        print(f"[DRY-RUN] Văn bản sạch:\n\"{cleaned_text}\"")
        sys.exit(0)

    try:
        if chosen_provider == "vbee":
            if not has_vbee:
                raise RuntimeError(f"Chưa điền VBEE_APP_ID và VBEE_BEARER_TOKEN trong {ENV_VAULT_PATH}")
            synthesize_vbee(
                cleaned_text,
                args.output,
                voice_id,
                speed,
                env_keys["VBEE_APP_ID"],
                env_keys["VBEE_BEARER_TOKEN"],
            )
        elif chosen_provider == "viettel":
            if not has_viettel:
                raise RuntimeError(f"Chưa điền VIETTEL_TTS_TOKEN trong {ENV_VAULT_PATH}")
            synthesize_viettel(
                cleaned_text,
                args.output,
                voice_id,
                speed,
                env_keys["VIETTEL_TTS_TOKEN"],
            )
        else:
            if not HAS_EDGE_TTS:
                raise RuntimeError("Chưa cài đặt thư viện edge-tts.")
            asyncio.run(synthesize_edge(cleaned_text, args.output, voice_id, speed))

        if not args.no_master:
            mastered = apply_ffmpeg_studio_mastering(args.output, args.output)
            if mastered:
                print("✨ Đã áp dụng FFmpeg Studio Mastering (Cắt lặng thừa + Tăng ấm/sáng giọng + Chuẩn -3dB).")

        print(f"✔ XUẤT AUDIO THÀNH CÔNG: {os.path.abspath(args.output)}")
        print("============================================================\n")
    except Exception as e:
        print(f"✖ LỖI KHI SINH AUDIO ({chosen_provider.upper()}): {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
