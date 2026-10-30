#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_and_schedule_remaining_18_golden_reels.py
1. Chạy cổng khóa cứng `verify_zero_clone_tsx()` (nếu phát hiện bất kỳ 2 video nào trùng cấu trúc JSX/SVG -> DỪNG NGAY).
2. Bundle Remotion project (`build-bespoke-21-vault`) với 18 Composition Độc Bản 100% (`Reel07..21` & `Reel01..03`).
3. Cuốn chiếu từng video: Nếu đã có MP4 chuẩn -> Upload/Schedule ngay lập tức lên Fanpage AI Players (`1022527194267367`) kèm Pinned Comment #1; nếu chưa có MP4 -> Render (`--concurrency=2 --crf=23`) -> Trích xuất ảnh QA -> Upload/Schedule ngay.
4. Cập nhật bảng 21-Video QA Thumbnail Grid (`bespoke_21_reels_qa_grid.jpg`).
"""

import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from zero_repost_gate import verify_zero_clone_tsx
from fix_and_publish_21_reels_now import (
    BUNDLE_DIR,
    CAMPAIGN_DIR,
    FFMPEG_EXE,
    GRAPH_VERSION,
    NODE_EXE,
    OUT_MANIFEST,
    REMOTION_DIR,
    SPEC_D1_D2,
    SPEC_D3_D7,
    SRC_DIR,
    SSL_CTX,
    THUMBS_DIR,
    VIDEOS_DIR,
    ZALO_GROUP_URL,
    ZALO_PASSCODE,
    bundle_remotion,
    get_ai_players_credentials,
    parse_vn_schedule_time,
    post_comment_on_video,
    upload_video_to_meta,
)


def generate_qa_grid(all_items: list) -> Path:
    from PIL import Image, ImageDraw

    cols = 3
    rows = 7
    cell_w, cell_h = 360, 640
    grid = Image.new("RGB", (cols * cell_w, rows * cell_h), (10, 15, 30))
    draw = ImageDraw.Draw(grid)

    for idx, item in enumerate(all_items):
        rid = item["id"]
        r = idx // cols
        c = idx % cols
        x0 = c * cell_w
        y0 = r * cell_h

        thumb_s1 = THUMBS_DIR / f"golden_{rid}_s1.jpg"
        thumb_s3 = THUMBS_DIR / f"golden_{rid}_s3.jpg"
        chosen = thumb_s3 if (rid == "reel05" and thumb_s3.is_file()) else thumb_s1
        if chosen.is_file():
            try:
                im = Image.open(chosen).convert("RGB").resize((cell_w - 8, cell_h - 8))
                grid.paste(im, (x0 + 4, y0 + 4))
            except Exception:
                pass
        draw.rectangle([x0 + 2, y0 + 2, x0 + cell_w - 2, y0 + cell_h - 2], outline=(135, 255, 0), width=2)
        draw.rectangle([x0 + 8, y0 + 8, x0 + 255, y0 + 44], fill=(8, 12, 28))
        draw.text((x0 + 14, y0 + 14), f"{rid.upper()} | {item['schedule_vn']}", fill=(135, 255, 0))

    grid_path = CAMPAIGN_DIR / "bespoke_21_reels_qa_grid.jpg"
    grid.save(grid_path, quality=92)
    return grid_path


def main():
    render_only = "--render-only" in sys.argv
    skip_bundle = "--skip-bundle" in sys.argv

    # BƯỚC 0: CỔNG KHÓA CỨNG ZERO-CLONE
    ok_zc, msg_zc = verify_zero_clone_tsx(SRC_DIR)
    if not ok_zc:
        print(f"❌ DỪNG KHẨN CẤP: {msg_zc}", flush=True)
        sys.exit(1)
    print(f"🛡️ {msg_zc}", flush=True)

    d12 = json.loads(SPEC_D1_D2.read_text(encoding="utf-8"))
    d37 = json.loads(SPEC_D3_D7.read_text(encoding="utf-8"))

    # Thứ tự ưu tiên: Reel07..Reel21 rồi tới Reel01..Reel03 (Tổng 18 Reels)
    remaining_18 = d37 + [x for x in d12 if x["id"] in ("reel01", "reel02", "reel03")]
    slot_schedule = [
        "2026-10-30 08:15", "2026-10-30 11:45", "2026-10-30 16:30", "2026-10-30 20:00",
        "2026-10-31 11:45", "2026-10-31 16:30", "2026-10-31 20:00",
        "2026-11-01 11:45", "2026-11-01 16:30", "2026-11-01 20:00",
        "2026-11-02 11:45", "2026-11-02 16:30", "2026-11-02 20:00",
        "2026-11-03 11:45", "2026-11-03 16:30", "2026-11-03 20:00",
        "2026-11-04 11:45", "2026-11-04 16:30",
    ]
    for idx_slot, it in enumerate(remaining_18):
        if idx_slot < len(slot_schedule):
            it["schedule_vn"] = slot_schedule[idx_slot]

    all_21 = d12 + d37

    if not skip_bundle:
        bundle_remotion()

    page_id, page_token, page_name = get_ai_players_credentials()
    print(f"🔑 Kết nối Fanpage: {page_name} ({page_id})", flush=True)

    sched_url = f"https://graph.facebook.com/{GRAPH_VERSION}/{page_id}/scheduled_posts?fields=id,message,scheduled_publish_time&limit=100&access_token={urllib.parse.quote(page_token)}"
    with urllib.request.urlopen(urllib.request.Request(sched_url), timeout=25, context=SSL_CTX) as resp:
        sched_posts = json.loads(resp.read().decode("utf-8")).get("data", [])

    pub_url = f"https://graph.facebook.com/{GRAPH_VERSION}/{page_id}/videos?fields=id,title,description&limit=35&access_token={urllib.parse.quote(page_token)}"
    with urllib.request.urlopen(urllib.request.Request(pub_url), timeout=25, context=SSL_CTX) as resp:
        existing_vids = json.loads(resp.read().decode("utf-8")).get("data", [])

    cli_js = str(REMOTION_DIR / "node_modules" / "@remotion" / "cli" / "remotion-cli.js")
    done_count = 0

    for idx_r, item in enumerate(remaining_18, 1):
        rid = item["id"]
        comp_id = item["comp_id"]
        kw = item["keyword"]
        mp4 = VIDEOS_DIR / f"{rid}_{comp_id}.mp4"

        if not mp4.is_file() or mp4.stat().st_size < 1_000_000:
            t0 = time.time()
            print(f"\n🎬 [{idx_r:02d}/18 - {rid}] Đang render `{comp_id}` -> {mp4.name} ...", flush=True)
            proc = subprocess.run(
                [NODE_EXE, cli_js, "render", str(BUNDLE_DIR), comp_id, str(mp4), "--concurrency=2", "--crf=23", "--overwrite"],
                cwd=str(REMOTION_DIR),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
            )
            elapsed = round(time.time() - t0, 1)
            if proc.returncode != 0 or not mp4.is_file():
                print(f"❌ [{rid}] Lỗi render `{comp_id}`:\n{(proc.stderr or proc.stdout)[-800:]}", flush=True)
                continue
            mb = round(mp4.stat().st_size / (1024 * 1024), 2)
            print(f"✅ [{rid}] Render xong `{comp_id}` trong {elapsed}s ({mb} MB)", flush=True)
        else:
            mb = round(mp4.stat().st_size / (1024 * 1024), 2)
            print(f"⏩ [{idx_r:02d}/18 - {rid}] Đã có MP4 ({mb} MB): {mp4.name}", flush=True)

        # Trích xuất ảnh QA
        for tag, ss in [("s1", "00:00:03"), ("s3", "00:00:18"), ("s6", "00:00:40")]:
            jpg = THUMBS_DIR / f"golden_{rid}_{tag}.jpg"
            if not jpg.is_file():
                subprocess.run(
                    [FFMPEG_EXE, "-y", "-ss", ss, "-i", str(mp4), "-vframes", "1", "-q:v", "2", str(jpg)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

        if render_only:
            continue

        # Kiểm tra xem đã có trên Page chưa
        already_on_page = any(kw in (p.get("message") or "") for p in sched_posts) or any(
            kw in (v.get("description") or "") for v in existing_vids
        )
        if already_on_page:
            print(f"⏩ [{rid}] Đã tồn tại trên Page, bỏ qua upload.", flush=True)
            done_count += 1
            continue

        sched_ts = parse_vn_schedule_time(item["schedule_vn"])
        now_ts = int(time.time())
        pinned_comment = (
            f"🎁 [TÀI LIỆU & BỘ CÔNG CỤ MIỄN PHÍ — MÃ: {kw}]\n"
            f"👉 Tham gia ngay Nhóm Zalo Cộng Đồng VIP \"AI Players — Thực Chiến Subagent\" để lấy trọn bộ Sơ đồ Kiến trúc, File .MD & Bộ 30 Quà tặng đóng hộp:\n"
            f"🔗 Link vào nhóm ngay: {ZALO_GROUP_URL}\n"
            f"🔑 Mã duyệt tự động (Passcode): {ZALO_PASSCODE}\n\n"
            f"💡 Anh em vào nhóm bấm lên Tin nhắn ghim trên cùng là tải về máy dùng được ngay trong 3 phút nhé!"
        )

        if sched_ts <= now_ts + 720:
            print(f"🚀 [{idx_r:02d}/18 - {rid}] Đang đăng LIVE `{comp_id}` (khung {item['schedule_vn']})...", flush=True)
            up = upload_video_to_meta(page_id, page_token, mp4, item["title"], item["caption"], published=True)
            mode_status = "LIVE_PUBLISHED"
        else:
            print(f"☁️ [{idx_r:02d}/18 - {rid}] Đang tải lên & hẹn giờ `{comp_id}` ({item['schedule_vn']})...", flush=True)
            up = upload_video_to_meta(page_id, page_token, mp4, item["title"], item["caption"], published=False, schedule_ts=sched_ts)
            mode_status = "SCHEDULED"

        if "error" in up:
            print(f"❌ [{rid}] Lỗi upload Meta: {up['error']}", flush=True)
            continue

        vid = up["video_id"]
        pid = up["post_id"]
        cmt = post_comment_on_video(page_id, vid, pid, page_token, pinned_comment)
        cmt_id = cmt.get("id", "")
        item["fb_video_id"] = vid
        item["fb_comment_id"] = cmt_id
        item["status"] = mode_status
        done_count += 1
        OUT_MANIFEST.write_text(json.dumps(all_21, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ [{idx_r:02d}/18 - {rid}] Hoàn tất ({mode_status} - {item['schedule_vn']})! video_id={vid} | comment_id={cmt_id}", flush=True)

    grid_path = generate_qa_grid(all_21)
    OUT_MANIFEST.write_text(json.dumps(all_21, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n🎉 HOÀN TẤT XUẤT BẢN & HẸN GIỜ {done_count}/18 REELS ĐỘC BẢN! QA Grid: {grid_path}", flush=True)


if __name__ == "__main__":
    main()
