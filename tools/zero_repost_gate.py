#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zero_repost_gate.py — Cổng Khóa Cứng Chống Đăng Lặp Bài Cũ / Ảnh Cũ / Video Cũ (Zero-Repost Firewall)
và Cổng Khóa Cứng Chống Nhân Bản Bố Cục Video (`verify_zero_clone_tsx`).
"""

import argparse
import hashlib
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
REGISTRY_PATH = SUBAGENT_DIR / "campaigns" / "daily-reports" / "published_history_registry.json"
VAULT_PATH = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / "pages_vault.json"

FOUR_PAGE_IDS = [
    "1022527194267367",  # AI Players - Người chơi hệ AI
    "1442323328956326",  # Phòng Trọ Hết Cứu
    "1421270697727753",  # Ký Túc Xá Có Biến
    "1407231352464711",  # Hội Deadline
]

PERMANENT_BANNED_FILENAMES = [
    "sales-phongtro-1145-style02.jpg",
    "sales-phongtro-1145-style02.png",
    "sales-phongtro-2030-style01.jpg",
    "sales-phongtro-2030-style01.png",
    "sales-ktx-1145-style02.jpg",
    "sales-ktx-1145-style02.png",
    "sales-ktx-2100-style01.jpg",
    "sales-ktx-2100-style01.png",
    "sales-deadline-1145-style02.jpg",
    "sales-deadline-1145-style02.png",
    "sales-deadline-2000-style01.jpg",
    "sales-deadline-2000-style01.png",
    "mcp-ai-explainer-40s.mp4",
    "ai-hallucination-45s.mp4",
    "ai-agent-vs-chatbot-45s.mp4",
    "ai-map-pillars-45s.mp4",
    "openrouter_mindmap_explainer.mp4",
    "ai-square-01-lead-prompt50.jpg",
    "ai-square-02-lead-hethong.jpg",
    "ai-square-03-github-f5-tts.jpg",
    "ai-square-04-github-browser-use.jpg",
    "ai-square-05-github-awesome-llm.jpg",
    "ai-square-06-discussion-poll.jpg",
    "day1_img1_1415_repo.png",
    "day1_img2_1545_voice.png",
    "day1_img3_1715_prompt50.png",
    "day1_img4_1845_khobau.png",
    "day1_img5_2015_hethong.png",
    "day1_img6_2145_poll.png",
]


def normalize_caption_fingerprint(text: str) -> str:
    if not text:
        return ""
    first_non_empty = ""
    for line in text.splitlines():
        s = line.strip()
        if s:
            first_non_empty = s
            break
    cleaned = re.sub(r"[^\w\s]", "", first_non_empty.lower(), flags=re.UNICODE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:75]


def compute_file_sha256(file_path: Path) -> str:
    if not file_path or not file_path.exists() or not file_path.is_file():
        return ""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_registry() -> dict:
    if REGISTRY_PATH.exists():
        try:
            data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("banned_filenames", [])
                data.setdefault("published_sha256", {})
                data.setdefault("published_caption_fingerprints", {})
                for fn in PERMANENT_BANNED_FILENAMES:
                    if fn not in data["banned_filenames"]:
                        data["banned_filenames"].append(fn)
                return data
        except Exception:
            pass
    return {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "banned_filenames": list(PERMANENT_BANNED_FILENAMES),
        "published_sha256": {},
        "published_caption_fingerprints": {},
    }


def save_registry(data: dict) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    REGISTRY_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def check_live_graph_duplicate(page_id: str, caption: str, title: str = "") -> tuple[bool, str]:
    if not VAULT_PATH.exists():
        return True, "OK"
    fp_cap = normalize_caption_fingerprint(caption)
    fp_title = normalize_caption_fingerprint(title)
    if len(fp_cap) < 12 and len(fp_title) < 12:
        return True, "OK"

    try:
        vault = json.loads(VAULT_PATH.read_text(encoding="utf-8", errors="ignore"))
        pages = {str(p["id"]): p for p in vault.get("pages", [])}
        if str(page_id) not in pages:
            return True, "OK"
        tok = pages[str(page_id)]["access_token"]
        ctx = ssl._create_unverified_context()

        endpoints = [
            ("scheduled_posts", "message"),
            ("published_posts", "message"),
            ("videos", "title,description"),
        ]
        for ep, fields in endpoints:
            url = (
                f"https://graph.facebook.com/v22.0/{page_id}/{ep}"
                f"?fields=id,{fields},created_time,scheduled_publish_time&limit=35&access_token={urllib.parse.quote(tok)}"
            )
            try:
                with urllib.request.urlopen(url, context=ctx, timeout=10) as resp:
                    items = json.loads(resp.read().decode("utf-8", errors="ignore")).get("data", [])
                    for item in items:
                        for f in fields.split(","):
                            val = item.get(f, "") or ""
                            fp_remote = normalize_caption_fingerprint(val)
                            if fp_remote and len(fp_remote) >= 12:
                                if (fp_cap and fp_remote == fp_cap) or (fp_title and fp_remote == fp_title):
                                    return (
                                        False,
                                        f"CHẶN CỨNG [Live Graph API Duplicate]: Nội dung '{fp_remote[:45]}...' đã tồn tại trên Page ({ep} id={item.get('id')})!",
                                    )
            except Exception:
                pass
    except Exception:
        pass
    return True, "OK"


def verify_fresh_content(page_id: str, media_path: Path | str | None, caption: str, title: str = "") -> tuple[bool, str]:
    reg = load_registry()
    if media_path:
        p = Path(media_path)
        if p.name in reg.get("banned_filenames", []):
            return False, f"CHẶN CỨNG [Zero-Repost]: File '{p.name}' nằm trong danh sách media cũ đã từng đăng!"
        if p.exists():
            sha = compute_file_sha256(p)
            if sha and sha in reg.get("published_sha256", {}):
                prev_info = reg["published_sha256"][sha]
                return False, f"CHẶN CỨNG [Zero-Repost]: Mã băm SHA256 của file '{p.name}' trùng khớp với file đã đăng ({prev_info})!"

    for text_check in (caption, title):
        fp = normalize_caption_fingerprint(text_check)
        if fp and len(fp) >= 12:
            if fp in reg.get("published_caption_fingerprints", {}):
                prev_post = reg["published_caption_fingerprints"][fp]
                return False, f"CHẶN CỨNG [Zero-Repost]: Nội dung mở đầu '{fp[:45]}...' trùng với bài đã đăng ({prev_post})!"

    is_live_ok, live_reason = check_live_graph_duplicate(str(page_id), caption, title)
    if not is_live_ok:
        return False, live_reason

    return True, "OK"


def record_published_content(page_id: str, media_path: Path | str | None, caption: str, post_id: str = "") -> None:
    reg = load_registry()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if media_path:
        p = Path(media_path)
        if p.name not in reg["banned_filenames"]:
            reg["banned_filenames"].append(p.name)
        if p.exists():
            sha = compute_file_sha256(p)
            if sha:
                reg["published_sha256"][sha] = f"{p.name} | page={page_id} | post={post_id} | {now_str}"

    fp = normalize_caption_fingerprint(caption)
    if fp and len(fp) >= 12:
        reg["published_caption_fingerprints"][fp] = f"page={page_id} | post={post_id} | {now_str}"

    save_registry(reg)


def sync_historical_posts_and_local_media() -> dict:
    reg = load_registry()
    ctx = ssl._create_unverified_context()

    camp_root = SUBAGENT_DIR / "campaigns"
    local_hashed = 0
    if camp_root.exists():
        for date_dir in sorted(camp_root.iterdir()):
            if not date_dir.is_dir():
                continue
            if date_dir.name in ("2026-10-20", "2026-10-21", "2026-10-22", "2026-10-23", "2026-10-24", "2026-10-25"):
                for media_file in date_dir.rglob("*"):
                    if media_file.is_file() and media_file.suffix.lower() in (".jpg", ".jpeg", ".png", ".mp4"):
                        sha = compute_file_sha256(media_file)
                        if sha and sha not in reg["published_sha256"]:
                            reg["published_sha256"][sha] = f"legacy_campaign:{date_dir.name}/{media_file.name}"
                            local_hashed += 1
                        if media_file.name not in reg["banned_filenames"]:
                            reg["banned_filenames"].append(media_file.name)

    graph_posts_recorded = 0
    if VAULT_PATH.exists():
        try:
            vault = json.loads(VAULT_PATH.read_text(encoding="utf-8", errors="ignore"))
            pages = {str(p["id"]): p for p in vault.get("pages", [])}
            for pid in FOUR_PAGE_IDS:
                if pid not in pages:
                    continue
                tok = pages[pid]["access_token"]
                for ep, field_name in [("published_posts", "message"), ("videos", "description")]:
                    url = (
                        f"https://graph.facebook.com/v22.0/{pid}/{ep}"
                        f"?fields=id,{field_name},created_time&limit=50&access_token={urllib.parse.quote(tok)}"
                    )
                    try:
                        with urllib.request.urlopen(url, context=ctx, timeout=15) as resp:
                            items = json.loads(resp.read().decode("utf-8", errors="ignore")).get("data", [])
                            for item in items:
                                msg = item.get(field_name, "") or ""
                                fp = normalize_caption_fingerprint(msg)
                                if fp and len(fp) >= 12 and fp not in reg["published_caption_fingerprints"]:
                                    reg["published_caption_fingerprints"][fp] = (
                                        f"page={pid} | id={item.get('id')} | created={item.get('created_time')}"
                                    )
                                    graph_posts_recorded += 1
                    except Exception:
                        pass
        except Exception:
            pass

    save_registry(reg)
    return {
        "banned_filenames_count": len(reg["banned_filenames"]),
        "published_sha256_count": len(reg["published_sha256"]),
        "published_caption_fingerprints_count": len(reg["published_caption_fingerprints"]),
        "newly_hashed_local": local_hashed,
        "newly_recorded_graph": graph_posts_recorded,
    }


def verify_zero_clone_tsx(src_dir: Path | str | None = None) -> tuple[bool, str]:
    """
    Cổng Khóa Cứng Chống Nhân Bản Video (`MEM-20261022-zero-clone-bespoke-video-rule.md`):
    Quét toàn bộ thư mục `src/Reel*/Scene1.tsx .. Scene5.tsx`.
    Bóc tách khung xương JSX + SVG + Macro Layout (bỏ qua text tiếng Việt) để kiểm tra:
    1. Không có bất kỳ 2 video nào có cùng cấu trúc thẻ JSX/SVG ở Scene1..Scene5 (chống `idx % N` xoay vòng hàm).
    2. Không được phép dùng lặp lại cùng 1 chuỗi SVG `<path d="...">` hoặc cấu trúc khung bao giữa 2 video.
    """
    if src_dir is None:
        src_dir = SUBAGENT_DIR / "templates" / "remotion-cuongit-template" / "src"
    src_path = Path(src_dir)
    if not src_path.exists():
        return False, f"Không tìm thấy thư mục nguồn Remotion: {src_path}"

    reel_dirs = sorted([d for d in src_path.iterdir() if d.is_dir() and d.name.startswith("Reel")])
    if len(reel_dirs) < 2:
        return True, "OK"

    for scene_num in range(1, 6):
        seen_skeletons: dict[str, str] = {}
        seen_svg_paths: dict[str, str] = {}
        for rdir in reel_dirs:
            sfile = rdir / f"Scene{scene_num}.tsx"
            if not sfile.exists():
                return False, f"CHẶN CỨNG [Zero-Clone]: Thiếu file {rdir.name}/Scene{scene_num}.tsx"
            code = sfile.read_text(encoding="utf-8", errors="ignore")

            tags_and_classes = re.findall(
                r"<(svg|path|circle|rect|polygon|line|ellipse|g|h1|h2|table)\b|className=\"([^\"]+)\"",
                code,
            )
            norm_tokens = []
            for tag, cls in tags_and_classes:
                if tag:
                    norm_tokens.append(f"<{tag}>")
                elif cls:
                    layout_cls = [
                        c
                        for c in cls.split()
                        if any(
                            k in c
                            for k in (
                                "grid",
                                "flex",
                                "col-span",
                                "row-span",
                                "rotate",
                                "rounded",
                                "border-l",
                                "border-r",
                                "border-t",
                                "border-b",
                                "items-",
                                "justify-",
                                "w-",
                                "h-",
                                "max-w-",
                            )
                        )
                    ]
                    norm_tokens.append(".".join(layout_cls))
            skeleton_str = "|".join(norm_tokens)
            skel_hash = hashlib.sha256(skeleton_str.encode("utf-8")).hexdigest()[:16]

            if skel_hash in seen_skeletons:
                prev_comp = seen_skeletons[skel_hash]
                return (
                    False,
                    f"CHẶN CỨNG [Zero-Clone Gate]: `{rdir.name}/Scene{scene_num}.tsx` trùng khớp khung xương bố cục/SVG với `{prev_comp}/Scene{scene_num}.tsx` (hash={skel_hash})! Cấm dùng chung hàm template!",
                )
            seen_skeletons[skel_hash] = rdir.name

            svg_ds = [d.strip() for d in re.findall(r'\bd="([^"]{25,})"', code)]
            if svg_ds:
                svg_sig = hashlib.sha256("||".join(svg_ds).encode("utf-8")).hexdigest()[:16]
                if svg_sig in seen_svg_paths:
                    prev_svg_comp = seen_svg_paths[svg_sig]
                    return (
                        False,
                        f"CHẶN CỨNG [Zero-Clone Gate]: `{rdir.name}/Scene{scene_num}.tsx` dùng lại hình vẽ SVG `<path>` giống hệt `{prev_svg_comp}/Scene{scene_num}.tsx`!",
                    )
                seen_svg_paths[svg_sig] = rdir.name

    return True, f"PASSED Zero-Clone Structural Gate ({len(reel_dirs)} compositions verified 100% unique across Scene1..Scene5)"


def verify_zero_clone_images(image_dir: Path | str | None = None, max_similarity: float = 0.58) -> tuple[bool, str]:
    """
    Cổng Khóa Cứng Chống Thiết Kế Ảnh Na Ná Nhau (`LUẬT #1 — Zero-Clone Bespoke Image Gate`):
    Chia mỗi ảnh `1080×1080` thành lưới `8×8` (64 phân vùng không gian) để đo:
    1. Phân bố khối màu chủ đạo (Lime, Pink, Cyan, Amber, Emerald, Violet, White, Dark) ở từng phân vùng.
    2. Phân bố mật độ tương phản / cạnh hình học (Structural Edge Density) ở từng phân vùng.
    Nếu bất kỳ 2 ảnh nào có độ tương đồng bố cục không gian > `max_similarity` (ví dụ dùng chung khuôn Template 1..5),
    lập tức CHẶN CỨNG và báo tên 2 file vi phạm!
    """
    from PIL import Image

    if image_dir is None:
        image_dir = SUBAGENT_DIR / "campaigns" / "2026-10-26" / "ai-players-weekly-vault" / "images"
    img_path_dir = Path(image_dir)
    if not img_path_dir.exists():
        return False, f"Không tìm thấy thư mục ảnh: {img_path_dir}"

    img_files = sorted(
        [f for f in img_path_dir.iterdir() if f.is_file() and f.suffix.lower() in (".jpg", ".jpeg", ".png")]
    )
    if len(img_files) < 2:
        return True, f"OK ({len(img_files)} image)"

    def _classify_zone_signature(im: Image.Image) -> list[str]:
        small = im.convert("RGB").resize((64, 64), Image.Resampling.BILINEAR)
        px = small.load()
        sig = []
        # 8x8 zones, each zone is 8x8 pixels in the 64x64 thumbnail
        for gy in range(8):
            for gx in range(8):
                r_sum = g_sum = b_sum = 0
                bright_cnt = 0
                for y in range(gy * 8, (gy + 1) * 8):
                    for x in range(gx * 8, (gx + 1) * 8):
                        r, g, b = px[x, y]
                        r_sum += r
                        g_sum += g
                        b_sum += b
                        if (r + g + b) > 380:
                            bright_cnt += 1
                r_avg, g_avg, b_avg = r_sum // 64, g_sum // 64, b_sum // 64
                lum = (r_avg + g_avg + b_avg) // 3
                if lum < 38:
                    c_tag = "DARK"
                elif g_avg > 170 and r_avg > 140 and b_avg < 90:
                    c_tag = "LIME"
                elif r_avg > 170 and b_avg > 70 and g_avg < 100:
                    c_tag = "PINK"
                elif b_avg > 160 and g_avg > 140 and r_avg < 90:
                    c_tag = "CYAN"
                elif r_avg > 180 and g_avg > 110 and b_avg < 70:
                    c_tag = "AMBER"
                elif g_avg > 150 and r_avg < 90 and b_avg < 120:
                    c_tag = "EMERALD"
                elif b_avg > 160 and r_avg > 110 and g_avg < 110:
                    c_tag = "VIOLET"
                elif lum > 175:
                    c_tag = "WHITE"
                else:
                    c_tag = f"MID_{r_avg//64}_{g_avg//64}_{b_avg//64}"
                b_bucket = "HI" if bright_cnt > 24 else ("MD" if bright_cnt > 6 else "LO")
                sig.append(f"{c_tag}:{b_bucket}")
        return sig

    signatures: list[tuple[str, list[str]]] = []
    for f in img_files:
        with Image.open(f) as im:
            signatures.append((f.name, _classify_zone_signature(im)))

    for i in range(len(signatures)):
        name_a, sig_a = signatures[i]
        for j in range(i + 1, len(signatures)):
            name_b, sig_b = signatures[j]
            # Count matching non-DARK zones vs total active zones
            active_zones = 0
            matching_active = 0
            for za, zb in zip(sig_a, sig_b):
                if za == "DARK:LO" and zb == "DARK:LO":
                    continue
                active_zones += 1
                if za == zb:
                    matching_active += 1
            sim = (matching_active / active_zones) if active_zones > 0 else 1.0
            if sim > max_similarity:
                return (
                    False,
                    f"CHẶN CỨNG [Zero-Clone Image Gate]: Ảnh `{name_a}` và `{name_b}` có bố cục không gian/màu sắc giống nhau tới {sim*100:.1f}% (vượt ngưỡng {max_similarity*100:.0f}%)! Cấm dùng chung khuôn thiết kế!",
                )

    return True, f"PASSED Zero-Clone Image Gate ({len(img_files)} ảnh độc bản 100%, không có 2 thiết kế nào giống nhau!)"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sync", action="store_true", help="Quét Graph API & kho cũ để khóa sổ Zero-Repost")
    parser.add_argument("--check-zero-clone", action="store_true", help="Kiểm tra cứng cấu trúc Zero-Clone của toàn bộ Reel Compositions")
    parser.add_argument("--check-zero-clone-images", type=str, nargs="?", const="", help="Kiểm tra cứng Zero-Clone cho thư mục ảnh bài đăng")
    args = parser.parse_args()

    if args.check_zero_clone:
        ok, msg = verify_zero_clone_tsx()
        print(("✅ " if ok else "❌ ") + msg)
        sys.exit(0 if ok else 1)

    if args.check_zero_clone_images is not None:
        target_dir = args.check_zero_clone_images if args.check_zero_clone_images else None
        ok, msg = verify_zero_clone_images(target_dir)
        print(("✅ " if ok else "❌ ") + msg)
        sys.exit(0 if ok else 1)

    if args.sync:
        stats = sync_historical_posts_and_local_media()
        print("✅ ĐÃ KHÓA SỔ ZERO-REPOST GATE THÀNH CÔNG:", json.dumps(stats, ensure_ascii=False))
    else:
        reg = load_registry()
        print(
            json.dumps(
                {
                    "banned_filenames_count": len(reg.get("banned_filenames", [])),
                    "published_sha256_count": len(reg.get("published_sha256", {})),
                    "published_caption_fingerprints_count": len(reg.get("published_caption_fingerprints", {})),
                },
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    main()
