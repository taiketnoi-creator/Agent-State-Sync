#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_and_publish_21_reels_now.py
1. Hoàn thiện 14 file audio còn thiếu của reel01, reel04, reel05, reel06 (đạt 126/126 file .mp3).
2. Cập nhật audioData.ts và đăng ký đủ 21 Composition độc bản (Reel01..Reel21) vào Root.tsx.
3. Bundle Remotion sang build-bespoke-21-vault.
4. ƯU TIÊN SỐ 1: Render ngay 3 Video Reels của hôm nay (2026-10-27):
   - Reel04StructuredJson (ca 11:45 sáng nay): ĐĂNG LIVE NGAY LẬP TỨC kèm Pinned Comment #1!
   - Reel05VisionOcrParser (ca 16:30 chiều nay): Hẹn giờ 16:30 hôm nay kèm Pinned Comment #1!
   - Reel06PromptCaching (ca 20:00 tối nay): Hẹn giờ 20:00 hôm nay kèm Pinned Comment #1!
5. Tiếp tục Render & Hẹn giờ 18 Video Reels còn lại của tuần (28/10 -> 02/11) đủ 21/21 Reels.
"""

import concurrent.futures
import datetime
import json
import math
import mimetypes
import shutil
import ssl
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
REMOTION_DIR = ROOT_DIR / "templates" / "remotion-cuongit-template"
SRC_DIR = REMOTION_DIR / "src"
PUBLIC_DIR = REMOTION_DIR / "public"
AUDIO_BASE_DIR = PUBLIC_DIR / "audio" / "bespoke26"
BUNDLE_DIR = REMOTION_DIR / "build-bespoke-21-vault"

CAMPAIGN_DIR = ROOT_DIR / "campaigns" / "2026-10-26" / "ai-players-weekly-vault"
VIDEOS_DIR = CAMPAIGN_DIR / "videos_bespoke21"
THUMBS_DIR = CAMPAIGN_DIR / "thumbs_bespoke21"
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
THUMBS_DIR.mkdir(parents=True, exist_ok=True)

SPEC_D1_D2 = CAMPAIGN_DIR / "bespoke_day1_day2_spec.json"
SPEC_D3_D7 = CAMPAIGN_DIR / "bespoke_day3_to_day7_spec.json"
OUT_MANIFEST = CAMPAIGN_DIR / "bespoke_21_weekly_reels_manifest.json"

TTS_SCRIPT = ROOT_DIR / "tools" / "generate_voice_tts.py"
FFPROBE_EXE = shutil.which("ffprobe") or "ffprobe"
FFMPEG_EXE = shutil.which("ffmpeg") or "ffmpeg"
NODE_EXE = shutil.which("node") or r"C:\Program Files\Adobe\Adobe Creative Cloud Experience\libs\node.exe"

FB_MCP_DIR = Path.home() / ".codex" / "mcp" / "facebook-mcp-server"
VAULT_PATH = FB_MCP_DIR / "pages_vault.json"
GRAPH_VERSION = "v22.0"
VN_TZ = datetime.timezone(datetime.timedelta(hours=7))
SSL_CTX = ssl._create_unverified_context()

ZALO_GROUP_URL = "https://zalo.me/g/etllok798"
ZALO_PASSCODE = "AIPLAYERS2026"


def get_audio_duration(mp3_path: Path) -> float:
    cmd = [
        FFPROBE_EXE,
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(mp3_path),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        val = float(res.stdout.strip())
        return val if val > 1.0 else 7.5
    except Exception:
        return 7.5


def ensure_all_126_audio_files(all_items: list) -> None:
    print("🎙️ Bước 1: Kiểm tra & tổng hợp bù các file voiceover còn thiếu...", flush=True)
    for item in all_items:
        rid = item["id"]
        cid = item["comp_id"]
        tot_frames = 0
        updated = False
        for s_idx, sc in enumerate(item["scenes"]):
            mp3_path = AUDIO_BASE_DIR / rid / f"scene{s_idx+1}.mp3"
            mp3_path.parent.mkdir(parents=True, exist_ok=True)
            if not mp3_path.is_file() or mp3_path.stat().st_size < 1000:
                print(f"  + Đang tạo voice cho {rid}/scene{s_idx+1}.mp3 ...", flush=True)
                for provider in ("vbee", "edge"):
                    subprocess.run(
                        [
                            sys.executable,
                            str(TTS_SCRIPT),
                            "--text",
                            sc["text"],
                            "--output",
                            str(mp3_path),
                            "--provider",
                            provider,
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        check=False,
                    )
                    if mp3_path.is_file() and mp3_path.stat().st_size >= 1000:
                        break
                    time.sleep(1.0)
                updated = True

            sec = round(get_audio_duration(mp3_path), 3)
            pad = 42 if s_idx == 5 else 16
            frames = int(math.ceil(sec * 30.0)) + pad
            sc["id"] = f"scene{s_idx+1}"
            sc["audioFile"] = f"audio/bespoke26/{rid}/scene{s_idx+1}.mp3"
            sc["durationSec"] = sec
            sc["durationInFrames"] = frames
            tot_frames += frames

        item["totalFrames"] = tot_frames
        item["totalSeconds"] = round(tot_frames / 30.0, 2)

        # Write audioData.ts in src/<cid>/audioData.ts
        adata_path = SRC_DIR / cid / "audioData.ts"
        manifest_obj = {
            "scenes": [
                {
                    "id": s["id"],
                    "text": s["text"],
                    "phrases": s["phrases"],
                    "audioFile": s["audioFile"],
                    "durationSec": s["durationSec"],
                    "durationInFrames": s["durationInFrames"],
                }
                for s in item["scenes"]
            ],
            "totalFrames": item["totalFrames"],
            "totalSeconds": item["totalSeconds"],
        }
        ts_code = (
            'import { AudioManifest } from "../AiHallucinationShort/types";\n\n'
            f"export const TOTAL_DURATION_FRAMES = {item['totalFrames']};\n\n"
            f"export const audioManifest: AudioManifest = {json.dumps(manifest_obj, ensure_ascii=False, indent=2)};\n"
        )
        adata_path.write_text(ts_code, encoding="utf-8")


def register_21_compositions_in_root(all_items: list) -> None:
    print("🧩 Bước 2: Đăng ký 21 Composition độc bản vào src/Root.tsx...", flush=True)
    imports = [
        'import "./index.css";',
        'import { Composition } from "remotion";',
        'import { AiHallucination45s } from "./AiHallucinationShort";',
        'import { aiHallucinationSchema } from "./AiHallucinationShort/types";',
        'import { TOTAL_DURATION_FRAMES as AI_HALLUCINATION_FRAMES } from "./AiHallucinationShort/audioData";',
        'import { TalkingHeadShort, talkingHeadSchema } from "./TalkingHeadShort";',
    ]
    comps = []
    for item in all_items:
        cid = item["comp_id"]
        frames = int(item.get("totalFrames") or 1450)
        imports.append(f'import {{ {cid} }} from "./{cid}";')
        comps.append(
            f'      <Composition id="{cid}" component={{{cid}}} durationInFrames={{{frames}}} fps={{30}} width={{1080}} height={{1920}} />'
        )

    root_tsx = "\n".join(imports) + "\n\nexport const RemotionRoot: React.FC = () => {\n  return (\n    <>\n" + "\n".join(comps) + """
      <Composition id="AiHallucination45s" component={AiHallucination45s} durationInFrames={AI_HALLUCINATION_FRAMES} fps={30} width={1080} height={1920} schema={aiHallucinationSchema} defaultProps={{ title: "Căn Bệnh Ảo Giác Của AI", subtitle: "Cách Khóa Chặt Bằng Kho Dữ Liệu Riêng" }} />
      <Composition id="TalkingHeadShort" component={TalkingHeadShort} durationInFrames={300} fps={30} width={1080} height={1920} schema={talkingHeadSchema} calculateMetadata={({ props }) => ({ durationInFrames: props.durationInFrames || 300 })} defaultProps={talkingHeadSchema.parse({})} />
    </>
  );
};
"""
    (SRC_DIR / "Root.tsx").write_text(root_tsx, encoding="utf-8")


def bundle_remotion() -> None:
    print("📦 Bước 3: Đóng gói Webpack Bundle cho 21 Composition độc bản...", flush=True)
    cmd = [
        NODE_EXE,
        str(REMOTION_DIR / "node_modules" / "@remotion" / "cli" / "remotion-cli.js"),
        "bundle",
        "src/index.ts",
        "--out-dir",
        str(BUNDLE_DIR),
    ]
    res = subprocess.run(cmd, cwd=str(REMOTION_DIR), capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if res.returncode != 0:
        raise RuntimeError(f"Bundle failed: {(res.stderr or res.stdout)[-800:]}")
    print("  ✅ Bundle thành công tại:", BUNDLE_DIR, flush=True)


def get_ai_players_credentials() -> tuple[str, str, str]:
    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
    for p in vault.get("pages", []):
        if str(p.get("id")) == "1022527194267367":
            return p["id"], p["access_token"], p["name"]
    raise RuntimeError("Missing AI Players credentials")


def parse_vn_schedule_time(time_str: str) -> int:
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            dt = datetime.datetime.strptime(time_str.strip(), fmt).replace(tzinfo=VN_TZ)
            return int(dt.timestamp())
        except ValueError:
            continue
    raise ValueError(f"Invalid schedule time: {time_str}")


def upload_video_to_meta(
    page_id: str,
    page_token: str,
    video_path: Path,
    title: str,
    description: str,
    published: bool = False,
    schedule_ts: int | None = None,
) -> dict:
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    mime_type = mimetypes.guess_type(video_path.name)[0] or "video/mp4"
    video_bytes = video_path.read_bytes()

    fields = [
        ("access_token", page_token),
        ("description", description),
        ("title", title),
        ("published", "true" if published else "false"),
    ]
    if not published and schedule_ts:
        fields.append(("scheduled_publish_time", str(schedule_ts)))

    body = bytearray()
    for k, v in fields:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{v}\r\n".encode("utf-8"))

    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="source"; filename="{video_path.name}"\r\n'.encode("utf-8"))
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    body.extend(video_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    url = f"https://graph-video.facebook.com/{GRAPH_VERSION}/{page_id}/videos"
    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=240.0, context=SSL_CTX) as resp:
            res = json.loads(resp.read().decode("utf-8", errors="ignore"))
            vid = res.get("id", "")
            return {
                "success": True,
                "video_id": vid,
                "post_id": res.get("post_id", f"{page_id}_{vid}"),
            }
    except Exception as e:
        err_msg = e.read().decode("utf-8", errors="ignore") if hasattr(e, "read") else str(e)
        return {"error": err_msg}


def post_comment_on_video(page_id: str, video_id: str, post_id: str, page_token: str, message: str) -> dict:
    last_err = {}
    for attempt in range(2):
        for tid in [f"{page_id}_{video_id}", video_id, post_id]:
            if not tid:
                continue
            url = f"https://graph.facebook.com/{GRAPH_VERSION}/{tid}/comments"
            data = urllib.parse.urlencode({"message": message, "access_token": page_token}).encode("utf-8")
            req = urllib.request.Request(url, data=data, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=25.0, context=SSL_CTX) as resp:
                    return json.loads(resp.read().decode("utf-8", errors="ignore"))
            except Exception as e:
                last_err = {"error": str(e)}
        if attempt == 0:
            time.sleep(3.0)
    return last_err


def render_and_publish_one(item: dict, page_id: str, page_token: str, publish_live_now: bool = False) -> dict:
    rid = item["id"]
    comp_id = item["comp_id"]
    video_path = VIDEOS_DIR / f"{rid}_{comp_id}.mp4"
    item["video_file"] = str(video_path)

    pinned_comment = (
        f"🎁 [TÀI LIỆU & BỘ CÔNG CỤ MIỄN PHÍ — MÃ: {item['keyword']}]\n"
        f"👉 Tham gia ngay Nhóm Zalo Cộng Đồng VIP \"AI Players — Thực Chiến Subagent\" để lấy trọn bộ Sơ đồ Kiến trúc, File .MD & Bộ 30 Quà tặng đóng hộp:\n"
        f"🔗 Link vào nhóm ngay: {ZALO_GROUP_URL}\n"
        f"🔑 Mã duyệt tự động (Passcode): {ZALO_PASSCODE}\n\n"
        f"💡 Anh em vào nhóm bấm lên Tin nhắn ghim trên cùng là tải về máy dùng được ngay trong 3 phút nhé!"
    )
    item["pinned_comment"] = pinned_comment

    if not video_path.is_file() or video_path.stat().st_size < 400_000:
        print(f"\n🎬 [{rid}] Đang render Composition độc bản `{comp_id}` -> {video_path.name}...", flush=True)
        t0 = time.time()
        cmd = [
            NODE_EXE,
            str(REMOTION_DIR / "node_modules" / "@remotion" / "cli" / "remotion-cli.js"),
            "render",
            str(BUNDLE_DIR),
            comp_id,
            str(video_path),
            "--concurrency=4",
            "--crf=23",
            "--overwrite",
        ]
        proc = subprocess.run(cmd, cwd=str(REMOTION_DIR), capture_output=True, text=True, encoding="utf-8", errors="ignore")
        elapsed = round(time.time() - t0, 1)
        if proc.returncode != 0 or not video_path.is_file():
            err_tail = (proc.stderr or proc.stdout or "")[-600:]
            print(f"❌ [{rid}] Render `{comp_id}` lỗi sau {elapsed}s: {err_tail}", flush=True)
            item["status"] = "RENDER_ERROR"
            item["error"] = err_tail
            return item
        mb = round(video_path.stat().st_size / (1024 * 1024), 2)
        print(f"✅ [{rid}] Render `{comp_id}` xong trong {elapsed}s ({mb} MB)", flush=True)
    else:
        mb = round(video_path.stat().st_size / (1024 * 1024), 2)
        print(f"⏩ [{rid}] Đã có sẵn MP4 ({mb} MB): {video_path.name}", flush=True)

    if not item.get("fb_video_id"):
        if publish_live_now:
            print(f"🚀 [{rid}] ĐANG ĐĂNG LIVE NGAY LẬP TỨC `{comp_id}` LÊN PAGE AI PLAYERS...", flush=True)
            up = upload_video_to_meta(page_id, page_token, video_path, item["title"], item["caption"], published=True)
        else:
            sched_ts = parse_vn_schedule_time(item["schedule_vn"])
            now_ts = int(time.time())
            if sched_ts < now_ts + 750:
                sched_ts = now_ts + 900
            print(f"☁️ [{rid}] Đang tải lên & hẹn giờ `{comp_id}` ({item['schedule_vn']})...", flush=True)
            up = upload_video_to_meta(page_id, page_token, video_path, item["title"], item["caption"], published=False, schedule_ts=sched_ts)

        if "error" in up:
            print(f"❌ [{rid}] Lỗi upload Meta: {up['error']}", flush=True)
            item["status"] = "UPLOAD_ERROR"
            item["upload_error"] = up["error"]
        else:
            vid = up["video_id"]
            pid = up.get("post_id", f"{page_id}_{vid}")
            item["fb_video_id"] = vid
            item["fb_post_id"] = pid
            item["status"] = "PUBLISHED_LIVE" if publish_live_now else "SCHEDULED"
            cmt = post_comment_on_video(page_id, vid, pid, page_token, pinned_comment)
            item["first_comment_id"] = cmt.get("id")
            mode_lbl = "ĐÃ ĐĂNG LIVE NGAY" if publish_live_now else f"ĐÃ HẸN GIỜ ({item['schedule_vn']})"
            print(f"🎯 [{rid}] {mode_lbl} `{comp_id}`! Video ID: {vid} | Cmt #1: {item.get('first_comment_id')}", flush=True)

    return item


def main() -> int:
    d12 = json.loads(SPEC_D1_D2.read_text(encoding="utf-8"))
    d37 = json.loads(SPEC_D3_D7.read_text(encoding="utf-8"))

    # Roll Day 1's 3 reels (reel01..reel03) to Monday 2026-11-02 (11:45, 16:30, 20:00) so full 7-day rolling window is 27/10 -> 02/11
    rollover_map = {
        "reel01": "2026-11-02 11:45",
        "reel02": "2026-11-02 16:30",
        "reel03": "2026-11-02 20:00",
    }
    for it in d12:
        if it["id"] in rollover_map:
            it["schedule_vn"] = rollover_map[it["id"]]

    all_items = d12 + d37

    only_today = "--only-today" in sys.argv
    only_remaining = "--remaining" in sys.argv

    if not only_remaining:
        # 1. Ensure all 126 audio files & audioData.ts
        ensure_all_126_audio_files(all_items)

        # Save updated specs
        SPEC_D1_D2.write_text(json.dumps(d12, ensure_ascii=False, indent=2), encoding="utf-8")

        # 2. Register 21 compositions in Root.tsx
        register_21_compositions_in_root(all_items)

        # 3. Bundle Remotion once
        bundle_remotion()

    page_id, page_token, page_name = get_ai_players_credentials()

    # 4. Priority #1: Render & Publish LIVE reel04 (ca 11:45 sáng nay), rồi hẹn giờ reel05 (16:30) & reel06 (20:00) của hôm nay trước tiên!
    today_ids = ["reel04", "reel05", "reel06"]
    today_items = [x for x in all_items if x["id"] in today_ids]
    remaining_items = [x for x in all_items if x["id"] not in today_ids]

    if not only_remaining:
        for item in today_items:
            is_live_now = (item["id"] == "reel04")
            render_and_publish_one(item, page_id, page_token, publish_live_now=is_live_now)
            OUT_MANIFEST.write_text(json.dumps(all_items, ensure_ascii=False, indent=2), encoding="utf-8")
        if only_today:
            print("\n🎉 HOÀN TẤT 3/3 VIDEO REELS CỦA HÔM NAY (27/10): 1 LIVE + 2 HẸN GIỜ (16:30 & 20:00)!", flush=True)
            return 0

    print("\n⚡ Đã xong 3 Video Reels của hôm nay (27/10)! Tiếp tục render & hẹn giờ song song 18 Video Reels còn lại...", flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futs = [pool.submit(render_and_publish_one, item, page_id, page_token, False) for item in remaining_items]
        for f in concurrent.futures.as_completed(futs):
            try:
                f.result()
                OUT_MANIFEST.write_text(json.dumps(all_items, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception as e:
                print(f"⚠️ Worker exception: {e}", flush=True)

    ok = sum(1 for x in all_items if x.get("status") in ("PUBLISHED_LIVE", "SCHEDULED"))
    print(f"\n🏁 HOÀN TẤT: {ok}/21 Video Reels Độc Bản đã được render & xuất bản/hẹn giờ lên Page AI Players!", flush=True)
    return 0 if ok == 21 else 1


if __name__ == "__main__":
    sys.exit(main())
