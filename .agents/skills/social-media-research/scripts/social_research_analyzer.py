#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Social Media Research Analyzer (Adapted from ScrapeCreators/social-media-research-skills)
Provides 0-Token deterministic local intelligence for `mkt`, `content`, and `cham-soc-kenh`:
1. Outlier Post Finder (--mode outlier): Calculates median baseline and view/engagement lift.
2. Comment Mining (--mode comments): Classifies Vietnamese & English comments into 6 VoC buckets.
3. Transcript Intelligence (--mode transcript): Extracts 3s Hook, Pain/Setup, Demo Proof, and CTA.
"""

import argparse
import json
import os
import re
import statistics
import sys
from typing import Any, Dict, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ============================================================================
# 1. OUTLIER POST FINDER (Median Baseline & Lift Scoring)
# ============================================================================

def analyze_outliers(posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not posts:
        return {"status": "error", "message": "Empty posts list"}

    views_list = [float(p.get("views", p.get("play_count", 0)) or 0) for p in posts]
    eng_list = []
    for p in posts:
        likes = float(p.get("likes", 0) or 0)
        comments = float(p.get("comments", 0) or 0)
        shares = float(p.get("shares", 0) or 0)
        saves = float(p.get("saves", 0) or 0)
        eng_list.append(likes + comments * 2.0 + shares * 3.0 + saves * 2.0)

    median_views = statistics.median(views_list) if views_list else 1.0
    median_eng = statistics.median(eng_list) if eng_list else 1.0
    median_views = max(median_views, 1.0)
    median_eng = max(median_eng, 1.0)

    confidence = "High" if len(posts) >= 20 else ("Medium" if len(posts) >= 10 else "Low")

    scored_posts = []
    for idx, p in enumerate(posts):
        views = views_list[idx]
        eng = eng_list[idx]
        view_lift = round(views / median_views, 2)
        eng_lift = round(eng / median_eng, 2)
        primary_lift = max(view_lift, eng_lift)

        if primary_lift >= 5.0:
            tier = "Huge Outlier (5x+)"
        elif primary_lift >= 2.0:
            tier = "Strong Outlier (2x-5x)"
        elif primary_lift >= 1.5:
            tier = "Mild Outlier (1.5x-2x)"
        else:
            tier = "Baseline (<1.5x)"

        title_or_caption = (p.get("title") or p.get("caption") or p.get("text") or "").strip()
        first_line_hook = title_or_caption.splitlines()[0][:120] if title_or_caption else ""

        scored_posts.append({
            "id": p.get("id", f"post_{idx+1}"),
            "url": p.get("url", ""),
            "platform": p.get("platform", "Social"),
            "views": int(views),
            "engagement_score": round(eng, 1),
            "view_lift": view_lift,
            "engagement_lift": eng_lift,
            "tier": tier,
            "hook_extract": first_line_hook,
        })

    scored_posts.sort(key=lambda x: (x["view_lift"], x["engagement_lift"]), reverse=True)
    outliers_only = [p for p in scored_posts if p["view_lift"] >= 1.5 or p["engagement_lift"] >= 1.5]

    return {
        "status": "ok",
        "mode": "outlier",
        "sample_size": len(posts),
        "confidence": confidence,
        "baseline": {
            "median_views": round(median_views, 1),
            "median_engagement_weighted": round(median_eng, 1),
        },
        "outliers_found": len(outliers_only),
        "top_outliers": scored_posts[:5],
        "hooks_to_steal": [p["hook_extract"] for p in outliers_only[:5] if p["hook_extract"]],
    }


# ============================================================================
# 2. COMMENT MINING (Vietnamese + English E-Commerce VoC Classifier)
# ============================================================================

VOC_PATTERNS = {
    "buying_intent": [
        r"\blink\b", r"xin link", r"mua ở đâu", r"giá sao", r"bao nhiêu tiền",
        r"giá bn", r"ib\b", r"inbox", r"chốt", r"đặt hàng", r"ship", r"giỏ hàng",
        r"còn hàng không", r"mua 2", r"combo",
    ],
    "objections": [
        r"sợ\b", r"nhảy át", r"tốn điện", r"nhanh hỏng", r"có bền không",
        r"hàng giả", r"lừa đảo", r"dùng được mấy bữa", r"bảo hành sao",
        r"ký túc xá cấm", r"ktx có dùng được", r"nóng không", r"dính nồi",
        r"ngắn quá", r"nhỏ quá",
    ],
    "pain_points": [
        r"bực mình", r"mệt mỏi", r"chùi muốn xỉu", r"khó vệ sinh", r"dầu mỡ",
        r"chật", r"nóng bức", r"đau lưng", r"mất thời gian", r"bừa bộn",
        r"loại cũ", r"mua nhầm", r"thất vọng",
    ],
    "questions": [
        r"\?", r"không shop", r"ko shop", r"không ạ", r"ko ạ", r"như thế nào",
        r"mấy lít", r"công suất", r"dùng sao", r"kích thước", r"rửa nước được không",
    ],
    "praise": [
        r"đáng tiền", r"xịn", r"ưng quá", r"tiện lợi", r"dùng êm", r"nhanh chín",
        r"đẹp lắm", r"10 điểm", r"cứu tinh", r"rẻ mà ngon",
    ],
}


def analyze_comments(comments: List[Any]) -> Dict[str, Any]:
    buckets: Dict[str, List[str]] = {k: [] for k in VOC_PATTERNS}
    buckets["other"] = []
    seen = set()
    cleaned_count = 0

    for item in comments:
        text = item.get("text", "") if isinstance(item, dict) else str(item)
        text_clean = re.sub(r"\s+", " ", text).strip()
        if len(text_clean) < 3:
            continue
        norm = text_clean.lower()
        if norm in seen:
            continue
        seen.add(norm)
        cleaned_count += 1

        matched = False
        for bucket, patterns in VOC_PATTERNS.items():
            if any(re.search(pat, norm) for pat in patterns):
                buckets[bucket].append(text_clean)
                matched = True
        if not matched:
            buckets["other"].append(text_clean)

    summary_counts = {k: len(v) for k, v in buckets.items()}
    recommended_canned_topics = []
    if buckets["buying_intent"]:
        recommended_canned_topics.append("Điều hướng link Shopee ở Bình Luận Ghim đầu tiên + mã Freeship")
    if buckets["objections"]:
        recommended_canned_topics.append("Giải tỏa rào cản (công suất an toàn KTX, chống dính, bảo hành đổi trả)")
    if buckets["questions"]:
        recommended_canned_topics.append("Trả lời thông số kỹ thuật ngắn gọn (dung tích, cách vệ sinh)")

    return {
        "status": "ok",
        "mode": "comments",
        "total_unique_comments": cleaned_count,
        "bucket_counts": summary_counts,
        "representative_quotes": {k: v[:5] for k, v in buckets.items() if v and k != "other"},
        "recommended_script_hooks_from_pain": (buckets["pain_points"] + buckets["objections"])[:4],
        "recommended_canned_response_topics": recommended_canned_topics,
    }


# ============================================================================
# 3. TRANSCRIPT INTELLIGENCE (Hook 3s & 4-Beat Short Script Segmentation)
# ============================================================================

def analyze_transcript(text: str) -> Dict[str, Any]:
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines() if ln.strip()]
    # Strip SRT sequence numbers and timestamps if input is an SRT file
    cleaned_lines = [
        ln for ln in lines
        if not re.match(r"^\d+$", ln) and not re.match(r"^\d{2}:\d{2}:\d{2}", ln)
    ]
    full_text = " ".join(cleaned_lines)
    sentences = [s.strip() for s in re.split(r"(?<=[.!?…])\s+", full_text) if s.strip()]
    if not sentences and cleaned_lines:
        sentences = cleaned_lines

    words = full_text.split()
    total_words = len(words)
    estimated_duration_sec = round(total_words / 2.8, 1)  # ~168 WPM Vietnamese short-form pace

    hook_3s = sentences[0] if sentences else ""
    cta_line = sentences[-1] if len(sentences) > 1 else ""
    middle = sentences[1:-1] if len(sentences) > 2 else []
    mid_split = max(1, len(middle) // 2) if middle else 0
    pain_setup = " ".join(middle[:mid_split]) if middle else ""
    demo_proof = " ".join(middle[mid_split:]) if middle else ""

    # Check Hard Gate compliance from content.md (no greeting in first 3s, <= 85 words for 30s)
    forbidden_greetings = ["xin chào", "hello", "chào mọi người", "hi mọi người", "hôm nay mình"]
    has_greeting_violation = any(g in hook_3s.lower() for g in forbidden_greetings)

    return {
        "status": "ok",
        "mode": "transcript",
        "total_words": total_words,
        "estimated_duration_sec": estimated_duration_sec,
        "hard_gate_check": {
            "word_limit_85_pass": total_words <= 85,
            "no_greeting_3s_pass": not has_greeting_violation,
        },
        "segmented_beats": {
            "00_03s_hook": hook_3s,
            "03_10s_pain_setup": pain_setup,
            "10_23s_demo_proof": demo_proof,
            "23_30s_cta": cta_line,
        },
    }


def run_demo() -> Dict[str, Any]:
    sample_posts = [
        {"id": "p1", "platform": "TikTok", "views": 12500, "likes": 420, "comments": 35, "shares": 18, "title": "Dọn bàn học ký túc xá cuối tuần"},
        {"id": "p2", "platform": "TikTok", "views": 14200, "likes": 510, "comments": 40, "shares": 22, "title": "Mẹo gấp quần áo gọn trong 5 phút"},
        {"id": "p3", "platform": "TikTok", "views": 11800, "likes": 390, "comments": 28, "shares": 15, "title": "Review giá đỡ điện thoại giá rẻ"},
        {"id": "p4", "platform": "TikTok", "views": 98500, "likes": 6400, "comments": 820, "shares": 1150, "title": "Nấu mì bằng ấm siêu tốc bị chập điện? Đừng đợi bảo vệ tịch thu mới tiếc!"},
    ]
    sample_comments = [
        "Ký túc xá dùng có bị nhảy át không shop ơi?",
        "Xin link mua nồi với ạ, đang sale còn bao nhiêu tiền?",
        "Loại cũ mình mua dính đáy nồi chùi muốn xỉu luôn",
        "Đã mua dùng 2 tháng, nấu lẩu mì cực nhanh mà dễ rửa lắm 10 điểm",
    ]
    sample_transcript = (
        "Nấu mì bằng ấm siêu tốc bị cúp điện cả phòng? "
        "Sinh viên ở ký túc xá thèm bữa lẩu nóng lúc nửa đêm mà sợ nhảy át thì nhìn đây. "
        "Chiếc nồi điện mini công suất 600W chống dính vân đá này chiên trứng không cần dầu, lau nhẹ 3 giây là sạch bóng. "
        "Bấm ngay vào link Shopee mình ghim ở bình luận đầu tiên trước khi hết voucher giảm giá nhé!"
    )
    return {
        "outlier_demo": analyze_outliers(sample_posts),
        "comment_mining_demo": analyze_comments(sample_comments),
        "transcript_demo": analyze_transcript(sample_transcript),
    }


def main():
    parser = argparse.ArgumentParser(description="Social Media Research Analyzer (Outlier / Comment Mining / Transcript)")
    parser.add_argument("--mode", choices=["outlier", "comments", "transcript", "demo"], default="demo")
    parser.add_argument("--input", help="Path to JSON or TXT input file")
    parser.add_argument("--output", help="Optional path to save JSON report")
    args = parser.parse_args()

    if args.mode == "demo":
        result = run_demo()
    else:
        if not args.input or not os.path.exists(args.input):
            print(json.dumps({"status": "error", "message": f"Input file not found: {args.input}"}, ensure_ascii=False))
            sys.exit(1)
        if args.mode in ("outlier", "comments"):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            result = analyze_outliers(data) if args.mode == "outlier" else analyze_comments(data)
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                text = f.read()
            result = analyze_transcript(text)

    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
    print(output_json)


if __name__ == "__main__":
    main()
