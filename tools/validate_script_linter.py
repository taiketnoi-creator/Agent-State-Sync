#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_script_linter.py
-------------------------
0-Token Script Linter cho Kịch Bản Video Ngắn AI Affiliate (Agent-Javis).
Kiểm tra tự động các chuẩn bắt buộc:
  1. Giới hạn số từ thoại: <= 85 từ cho video 30s (tỷ lệ chuẩn ~2.8 từ/giây).
  2. Cấm tuyệt đối câu chào hỏi ở 3s đầu (Hook): "xin chào", "chào mọi người", "hello cả nhà"...
  3. Cấu trúc chuẩn 4 nhịp: Hook -> Pain Point -> Demo/Solution -> CTA.

Sử dụng:
  python tools/validate_script_linter.py --file <path_to_script.md> [--duration 30] [--json]
  python tools/validate_script_linter.py --text "Nội dung kịch bản..." [--duration 30] [--json]
"""

import sys
import os
import re
import json
import argparse

# Đảm bảo in tiếng Việt mượt mà trên console Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

BANNED_GREETINGS = [
    "xin chào",
    "chào mọi người",
    "chào các bạn",
    "chào cả nhà",
    "hello cả nhà",
    "hello mọi người",
    "hi các bạn",
    "hé lô",
    "chào bạn",
    "chào tất cả",
    "alo alo",
    "hi mọi người",
    "xin chao",
    "chao moi nguoi",
    "hello ca nha"
]

FOUR_BEATS_PATTERNS = {
    "Hook": [r"\bhook\b", r"\b0[0-3]s\b", r"\b[0-3]s\b", r"mở đầu", r"3s đầu"],
    "Pain": [r"\bpain\b", r"nỗi đau", r"ức chế", r"bất tiện", r"vấn đề", r"khó chịu", r"phiền phức", r"0[4-9]s", r"1[0-2]s"],
    "Demo": [r"\bdemo\b", r"\bsolution\b", r"giải pháp", r"trình diễn", r"before", r"after", r"hướng dẫn", r"sử dụng", r"1[3-9]s", r"2[0-5]s"],
    "CTA": [r"\bcta\b", r"call to action", r"kêu gọi", r"link", r"bình luận", r"giỏ hàng", r"bio", r"2[5-9]s", r"30s"]
}


def extract_voiceover(text: str) -> str:
    """
    Trích xuất phần lời thoại (Voiceover) từ kịch bản nếu có cấu trúc phân đoạn.
    Nếu không có phân đoạn Thoại/Voiceover, làm sạch markdown và stage directions.
    """
    # Tìm các mẫu: Thoại: "..." hoặc Voiceover: "..." hoặc Lời thoại: "..."
    voice_matches = re.findall(
        r'(?:thoại|voiceover|lời thoại|voice)\s*:\s*["“]?([^"\n”\r]+)["”]?',
        text,
        re.IGNORECASE
    )
    if voice_matches:
        return " ".join(voice_matches)

    # Nếu không có định dạng 'Thoại:', lọc bỏ các chỉ dẫn hình ảnh [00s-03s], (Visual: ...)
    cleaned = re.sub(r'\[\s*\d+s?\s*[-–]\s*\d+s?\s*\]', ' ', text)
    cleaned = re.sub(r'\((?:visual|hình ảnh|cảnh|hành động)[^)]*\)', ' ', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'#+\s+[^\n]+', ' ', cleaned)  # Bỏ tiêu đề markdown
    cleaned = re.sub(r'[-*]\s+', ' ', cleaned)      # Bỏ bullet points
    return cleaned


def count_words(text: str) -> int:
    """Đếm số từ tiếng Việt sau khi làm sạch ký tự đặc biệt."""
    # Bỏ markdown tags, dấu câu
    clean = re.sub(r'[^\w\s]', ' ', text, flags=re.UNICODE)
    words = [w for w in clean.split() if w.strip()]
    return len(words)


def check_banned_greetings(full_text: str, voice_text: str) -> list:
    """
    Kiểm tra xem 3s đầu (hoặc 15 từ đầu tiên của lời thoại/kịch bản) có chứa lời chào bị cấm không.
    """
    detected = []
    # Lấy 20 từ đầu tiên của voice_text hoặc full_text
    words = voice_text.split() if voice_text else full_text.split()
    opening_text = " ".join(words[:25]).lower()

    for phrase in BANNED_GREETINGS:
        if phrase in opening_text:
            detected.append(phrase)

    return detected


def check_four_beats(text: str) -> dict:
    """Kiểm tra sự hiện diện của 4 nhịp kịch bản: Hook, Pain, Demo, CTA."""
    results = {}
    lower_text = text.lower()
    for beat, patterns in FOUR_BEATS_PATTERNS.items():
        found = False
        for pat in patterns:
            if re.search(pat, lower_text):
                found = True
                break
        results[beat] = found
    return results


def lint_script(content: str, target_duration: int = 30) -> dict:
    """
    Thực hiện toàn bộ quy trình linting kịch bản.
    """
    voiceover = extract_voiceover(content)
    word_count = count_words(voiceover)
    
    # Tính trần số từ cho thời lượng target (chuẩn 30s <= 85 từ -> 2.83 từ/s)
    max_words = int(target_duration * (85 / 30.0))
    
    # 1. Kiểm tra độ dài từ
    word_count_pass = word_count <= max_words
    
    # 2. Kiểm tra câu chào ở Hook 3s đầu
    banned_found = check_banned_greetings(content, voiceover)
    greeting_pass = len(banned_found) == 0
    
    # 3. Kiểm tra 4 nhịp
    beats_status = check_four_beats(content)
    beats_pass = all(beats_status.values())
    
    overall_pass = word_count_pass and greeting_pass and beats_pass
    
    # Ước tính thời lượng nói (với tốc độ 2.8 từ/giây của MC affiliate)
    estimated_duration_sec = round(word_count / 2.8, 1) if word_count > 0 else 0.0

    return {
        "status": "PASS" if overall_pass else "FAIL",
        "target_duration_sec": target_duration,
        "max_words_allowed": max_words,
        "actual_words": word_count,
        "estimated_duration_sec": estimated_duration_sec,
        "checks": {
            "word_count": {
                "passed": word_count_pass,
                "message": f"Số từ {word_count}/{max_words} từ cho video {target_duration}s"
            },
            "no_banned_greetings": {
                "passed": greeting_pass,
                "detected": banned_found,
                "message": "Không chào hỏi ở 3s đầu" if greeting_pass else f"Phát hiện câu chào cấm: {banned_found}"
            },
            "four_beats_structure": {
                "passed": beats_pass,
                "beats": beats_status,
                "message": "Đủ 4 nhịp (Hook, Pain, Demo, CTA)" if beats_pass else f"Thiếu nhịp: {[k for k, v in beats_status.items() if not v]}"
            }
        },
        "voiceover_preview": voiceover.strip()[:150] + ("..." if len(voiceover.strip()) > 150 else "")
    }


def main():
    parser = argparse.ArgumentParser(
        description="0-Token Script Linter cho Kịch Bản Video Ngắn AI Affiliate (Agent-Javis)"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", "-f", type=str, help="Đường dẫn đến file kịch bản (.md hoặc .txt)")
    group.add_argument("--text", "-t", type=str, help="Nội dung kịch bản dạng chuỗi truyền trực tiếp")
    parser.add_argument("--duration", "-d", type=int, default=30, help="Thời lượng mục tiêu theo giây (mặc định 30s)")
    parser.add_argument("--json", action="store_true", help="Xuất kết quả định dạng JSON sạch")

    args = parser.parse_args()

    content = ""
    if args.file:
        if not os.path.exists(args.file):
            print(f"Lỗi: Không tìm thấy file tại '{args.file}'", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = args.text

    result = lint_script(content, target_duration=args.duration)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n==================================================")
        print("    AGENT-JAVIS SCRIPT LINTER (0-TOKEN CHECK)    ")
        print("==================================================")
        status_symbol = "✔ PASS" if result["status"] == "PASS" else "✖ FAIL"
        print(f"Trạng thái tổng quan: [{status_symbol}]")
        print(f"Thời lượng mục tiêu:  {result['target_duration_sec']}s (Trần: <= {result['max_words_allowed']} từ)")
        print(f"Số từ thoại thực tế: {result['actual_words']} từ (~{result['estimated_duration_sec']}s nói)")
        print("--------------------------------------------------")
        print("Chi tiết các bài kiểm tra:")
        
        c1 = result["checks"]["word_count"]
        print(f" 1. Giới hạn số từ:       [{'PASS' if c1['passed'] else 'FAIL'}] {c1['message']}")
        
        c2 = result["checks"]["no_banned_greetings"]
        print(f" 2. Chặn câu chào Hook:  [{'PASS' if c2['passed'] else 'FAIL'}] {c2['message']}")
        
        c3 = result["checks"]["four_beats_structure"]
        beats_str = ", ".join([f"{k}: {'OK' if v else 'THIẾU'}" for k, v in c3["beats"].items()])
        print(f" 3. Đủ 4 nhịp kịch bản:  [{'PASS' if c3['passed'] else 'FAIL'}] ({beats_str})")
        
        print("--------------------------------------------------")
        print(f"Trích đoạn thoại:\n\"{result['voiceover_preview']}\"")
        print("==================================================\n")

    sys.exit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
