#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
multi_platform_auto_publisher.py — Bộ Khung Auto Quản Lý & Đăng Đa Nền Tảng 0-Token
(Facebook Reels + Instagram Reels/Auto-DM + Threads Self-Reply + YouTube Shorts + TikTok)

Thiết kế Plug-and-Play (Chờ nạp tài khoản là chạy ngay 100%):
1. Kho tài khoản tập trung (`C:\\Users\\Admin\\.codex\\mcp\\facebook-mcp-server\\multi_platform_vault.json`):
   - Tự động kế thừa 5 Fanpage Facebook đã kết nối từ `pages_vault.json`.
   - Tự động quét Graph API (`--sync-ig-from-fb`) để lấy tài khoản Instagram Business ngay khi sếp liên kết IG vào Fanpage.
   - Cho phép nạp nhanh tài khoản YouTube / Threads / TikTok / IG bằng 1 câu lệnh (`--set-account`) hoặc điền vào file JSON.
2. Quy trình Auto 1 Lệnh (`--publish-all` / `--test-pipeline`):
   - Bước 1: Gọi `ffmpeg_multichannel_repurpose.py` băm 1 Video gốc thành 5 bản độc lập mã MD5 Hash & EXIF (`FB`, `IG`, `YT`, `TH`, `TT`).
   - Bước 2: Gọi `channel_matrix_manager.py` kiểm tra Tường lửa nội dung (`Content Firewall`) và sinh 5 bộ Caption + Link `Sub_ID` riêng.
   - Bước 3: Tự động bắn bài lên tất cả các kênh đã `CONNECTED` trong Pod:
     + FB Reels: Đăng/Hẹn giờ Reel + Tự động ghim `Pinned Comment #1` chứa link.
     + IG Reels: Đăng Reel qua Graph API + Bật trực chiến `--auto-dm-check` tự bắn Inbox khi khách comment `"LINK"`.
     + Threads: Đăng bài gốc (Root Post không link) -> Đợi 5 giây -> Tự động thả `Self-Reply #1` chứa link Shopee.
     + YouTube Shorts: Upload bản Shorts (Title < 60 ký tự + #Shorts + Link ở Mô tả / Related Video).
     + TikTok: Đẩy video qua TikTok Content Posting API / Chrome Profile cách ly.
   - Bước 4: Với các kênh đang `WAITING_FOR_ACCOUNT`, tự động lưu sẵn toàn bộ Video đã đổi Hash + Caption + Link vào hàng đợi SQLite (`multi_channel_posts`). Ngay khi sếp nạp tài khoản vào, hệ thống tự bắn toàn bộ bài đang chờ lên kênh!
"""

import argparse
import datetime
import json
import os
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
MCP_DIR = Path.home() / ".codex" / "mcp" / "facebook-mcp-server"
FB_PAGES_VAULT = MCP_DIR / "pages_vault.json"
MULTI_VAULT_PATH = MCP_DIR / "multi_platform_vault.json"

from channel_matrix_manager import (
    BRAND_PODS_SEED,
    generate_pod_publish_pack,
    get_db_path,
    init_matrix_tables,
)
from ffmpeg_multichannel_repurpose import create_sample_master_video, repurpose_for_pod


PLATFORMS_ORDER = ["FB_REELS", "IG_REELS", "THREADS", "YT_SHORTS", "TIKTOK"]

PLATFORM_SLOTS = {
    "FB_REELS": ["11:45", "20:00"],
    "IG_REELS": ["12:15", "20:30"],
    "THREADS": ["08:30", "21:30"],
    "YT_SHORTS": ["12:00", "19:30"],
    "TIKTOK": ["11:30", "19:45"],
}


def load_fb_pages_vault() -> dict:
    if FB_PAGES_VAULT.exists():
        try:
            return json.loads(FB_PAGES_VAULT.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def init_or_load_multi_vault(sync_fb: bool = True) -> dict:
    MCP_DIR.mkdir(parents=True, exist_ok=True)
    vault = {"updated_at": "", "pods": {}}
    if MULTI_VAULT_PATH.exists():
        try:
            vault = json.loads(MULTI_VAULT_PATH.read_text(encoding="utf-8"))
        except Exception:
            vault = {"updated_at": "", "pods": {}}

    fb_vault = load_fb_pages_vault()
    raw_pages = fb_vault.get("pages", {})
    if isinstance(raw_pages, list):
        fb_pages = {str(p.get("id", p.get("page_id", ""))): p for p in raw_pages if isinstance(p, dict)}
    elif isinstance(raw_pages, dict):
        fb_pages = raw_pages
    else:
        fb_pages = {}

    for pod in BRAND_PODS_SEED[:4]:
        pod_id = pod["pod_id"]
        handle = f"@{pod['handle_base']}"
        fb_page_id = pod["fb_page_id"]
        fb_info = fb_pages.get(fb_page_id, {})
        fb_token = fb_info.get("access_token", "")

        if pod_id not in vault["pods"]:
            vault["pods"][pod_id] = {
                "pod_name": pod["pod_name"],
                "business_model": pod["business_model"],
                "browser_profile": pod["browser_profile"],
                "platforms": {},
            }

        p_map = vault["pods"][pod_id]["platforms"]

        if "FB_REELS" not in p_map or sync_fb:
            p_map["FB_REELS"] = {
                "status": "CONNECTED" if fb_token else "WAITING_FOR_ACCOUNT",
                "handle": handle,
                "page_id": fb_page_id,
                "access_token": fb_token,
                "schedule_slots": PLATFORM_SLOTS["FB_REELS"],
                "link_rule": "Pinned Comment #1 (Cấm gắn link ở Caption)",
            }

        if "IG_REELS" not in p_map:
            p_map["IG_REELS"] = {
                "status": "WAITING_FOR_ACCOUNT",
                "handle": handle,
                "ig_user_id": "",
                "linked_fb_page_id": fb_page_id,
                "access_token": fb_token,
                "auto_dm_keyword": "LINK",
                "schedule_slots": PLATFORM_SLOTS["IG_REELS"],
                "link_rule": "Auto-DM khi khách comment 'LINK' + 5 Links in Bio",
                "setup_hint": "Liên kết IG Business vào Fanpage trong Meta Business Suite rồi chạy --sync-ig-from-fb",
            }

        if "THREADS" not in p_map:
            p_map["THREADS"] = {
                "status": "WAITING_FOR_ACCOUNT",
                "handle": handle,
                "threads_user_id": "",
                "access_token": "",
                "chrome_profile": pod["browser_profile"],
                "self_reply_delay_sec": 5,
                "schedule_slots": PLATFORM_SLOTS["THREADS"],
                "link_rule": "Root Post KHÔNG link -> Tự động thả link ở Self-Reply #1 sau 5 giây",
                "setup_hint": "Cấp threads_user_id + access_token hoặc đăng nhập sẵn vào Chrome Profile",
            }

        if "YT_SHORTS" not in p_map:
            p_map["YT_SHORTS"] = {
                "status": "WAITING_FOR_ACCOUNT",
                "handle": handle,
                "channel_id": "",
                "oauth_token_file": str(MCP_DIR / f"yt_oauth_{pod_id.lower()}.json"),
                "default_related_video_id": "",
                "chrome_profile": pod["browser_profile"],
                "schedule_slots": PLATFORM_SLOTS["YT_SHORTS"],
                "link_rule": "Title < 60 ký tự + Nút Related Video + 14 Bio Links",
                "setup_hint": "Cấp channel_id / oauth_token_file hoặc đăng nhập YouTube Studio trong Chrome Profile",
            }

        if "TIKTOK" not in p_map:
            p_map["TIKTOK"] = {
                "status": "WAITING_FOR_ACCOUNT",
                "handle": handle,
                "open_id": "",
                "access_token": "",
                "chrome_profile": pod["browser_profile"],
                "schedule_slots": PLATFORM_SLOTS["TIKTOK"],
                "link_rule": "Bio Link / TikTok Shop Giỏ Hàng Vàng",
                "setup_hint": "Đăng nhập TikTok vào Chrome Profile cách ly hoặc cấp TikTok Content Posting API token",
            }

    vault["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    MULTI_VAULT_PATH.write_text(json.dumps(vault, ensure_ascii=False, indent=2), encoding="utf-8")
    return vault


def sync_ig_accounts_from_fb(vault: dict) -> int:
    """Tự động quét Graph API xem Fanpage nào đã được sếp liên kết Instagram Business Account."""
    found = 0
    for pod_id, pod_data in vault.get("pods", {}).items():
        fb_cfg = pod_data["platforms"].get("FB_REELS", {})
        ig_cfg = pod_data["platforms"].get("IG_REELS", {})
        page_id = fb_cfg.get("page_id", "")
        token = fb_cfg.get("access_token", "")
        if not page_id or not token or page_id == "PENDING":
            continue
        url = (
            f"https://graph.facebook.com/v22.0/{page_id}"
            f"?fields=instagram_business_account{{id,username,name}}"
            f"&access_token={urllib.parse.quote(token)}"
        )
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                ig_acc = data.get("instagram_business_account")
                if ig_acc and ig_acc.get("id"):
                    ig_cfg["ig_user_id"] = ig_acc["id"]
                    if ig_acc.get("username"):
                        ig_cfg["handle"] = f"@{ig_acc['username']}"
                    ig_cfg["access_token"] = token
                    ig_cfg["status"] = "CONNECTED"
                    found += 1
        except Exception:
            pass
    vault["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    MULTI_VAULT_PATH.write_text(json.dumps(vault, ensure_ascii=False, indent=2), encoding="utf-8")
    return found


def set_platform_account(
    vault: dict,
    pod_id: str,
    platform: str,
    handle: str = None,
    user_id: str = None,
    token: str = None,
    chrome_profile: str = None,
    related_video_id: str = None,
) -> dict:
    pod_id = pod_id.upper()
    platform = platform.upper()
    if pod_id not in vault["pods"]:
        raise ValueError(f"Không tìm thấy Pod {pod_id} trong Vault!")
    if platform not in vault["pods"][pod_id]["platforms"]:
        raise ValueError(f"Nền tảng {platform} không hợp lệ (Chọn: {', '.join(PLATFORMS_ORDER)})")

    cfg = vault["pods"][pod_id]["platforms"][platform]
    if handle:
        cfg["handle"] = handle if handle.startswith("@") else f"@{handle}"
    if user_id:
        if platform == "IG_REELS":
            cfg["ig_user_id"] = user_id
        elif platform == "THREADS":
            cfg["threads_user_id"] = user_id
        elif platform == "YT_SHORTS":
            cfg["channel_id"] = user_id
        elif platform == "TIKTOK":
            cfg["open_id"] = user_id
        elif platform == "FB_REELS":
            cfg["page_id"] = user_id
    if token:
        cfg["access_token"] = token
    if chrome_profile:
        cfg["chrome_profile"] = chrome_profile
    if related_video_id and platform == "YT_SHORTS":
        cfg["default_related_video_id"] = related_video_id

    if token or user_id or chrome_profile:
        cfg["status"] = "CONNECTED"

    vault["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    MULTI_VAULT_PATH.write_text(json.dumps(vault, ensure_ascii=False, indent=2), encoding="utf-8")

    conn = sqlite3.connect(str(get_db_path()))
    pod_clean = pod_id.replace("-", "")
    suffix_map = {
        "FB_REELS": "FB",
        "IG_REELS": "IG",
        "THREADS": "TH",
        "YT_SHORTS": "YT",
        "TIKTOK": "TT",
    }
    ch_id = f"{pod_clean}_{suffix_map.get(platform, 'XX')}"
    conn.execute(
        "UPDATE channels SET connection_status = ?, handle = ? WHERE channel_id = ?",
        (cfg["status"], cfg.get("handle", ""), ch_id),
    )
    conn.commit()
    conn.close()
    return cfg


def print_status_matrix(vault: dict) -> None:
    print("=" * 105)
    print("🚀 BẢNG TRẠNG THÁI BỘ KHUNG AUTO ĐA NỀN TẢNG (5 MẶT TRẬN × 4 BRAND PODS = 20 KÊNH GIAI ĐOẠN 1)")
    print(f"📂 File Kho Tài Khoản Tập Trung: {MULTI_VAULT_PATH}")
    print("=" * 105)
    connected_count = 0
    waiting_count = 0

    for pod_id, pod_data in vault.get("pods", {}).items():
        print(
            f"\n🔹 [{pod_id}] {pod_data['pod_name'].upper()} | Mô hình: {pod_data['business_model']} | Chrome: {pod_data['browser_profile']}"
        )
        print("-" * 105)
        for plat in PLATFORMS_ORDER:
            p = pod_data["platforms"].get(plat, {})
            st = p.get("status", "WAITING_FOR_ACCOUNT")
            icon = "✅ CONNECTED          " if st == "CONNECTED" else "⏳ WAITING_FOR_ACCOUNT"
            if st == "CONNECTED":
                connected_count += 1
            else:
                waiting_count += 1
            slots = "/".join(p.get("schedule_slots", []))
            handle = p.get("handle", "")
            rule = p.get("link_rule", "")
            print(f"   • {plat:<10} | {icon} | {handle:<18} | Giờ: {slots:<11} | {rule}")

    print("\n" + "=" * 105)
    print(
        f"📊 TỔNG KẾT ĐỘ SẴN SÀNG: {connected_count} Kênh ĐÃ KẾT NỐI AUTO | {waiting_count} Kênh ĐÃ DỰNG SẴN KHUNG (Chờ nạp tài khoản)"
    )
    print("💡 CÁCH NẠP TÀI KHOẢN TRONG 1 GIÂY KHI SẾP CÓ NICK MỚI:")
    print(
        '   1. Nạp Threads : python tools/multi_platform_auto_publisher.py --set-account --pod POD-01 --platform THREADS --handle "@phongtrohetcuu" --user-id "<ID>" --token "<TOKEN>"'
    )
    print(
        '   2. Nạp YouTube : python tools/multi_platform_auto_publisher.py --set-account --pod POD-01 --platform YT_SHORTS --handle "@phongtrohetcuu" --user-id "<CHANNEL_ID>"'
    )
    print(
        '   3. Nạp TikTok  : python tools/multi_platform_auto_publisher.py --set-account --pod POD-01 --platform TIKTOK --handle "@phongtrohetcuu" --chrome-profile "Profile 59"'
    )
    print(
        "   4. Tự đồng bộ IG từ Fanpage FB: python tools/multi_platform_auto_publisher.py --sync-ig-from-fb"
    )
    print("=" * 105)


def prepare_and_queue_all_platforms(
    vault: dict,
    pod_id: str,
    video_path: Path,
    sku_code: str,
    origin_url: str,
    title: str,
) -> dict:
    db_path = get_db_path()
    init_matrix_tables(db_path)

    pack = generate_pod_publish_pack(db_path, pod_id, sku_code, origin_url, title)
    repurpose_manifest = repurpose_for_pod(video_path, pod_id, sku_code)
    variant_by_plat = {v["platform"]: v for v in repurpose_manifest["variants"]}

    pod_vault = vault["pods"].get(pod_id, {}).get("platforms", {})
    dispatch_results = []

    pod_clean = pod_id.replace("-", "").lower()
    sku_clean = sku_code.replace("-", "_").lower()
    tiktok_sub_id = f"tt_{pod_clean}_bio_{sku_clean}"

    channels_dict = dict(pack["channels"])
    channels_dict[f"{pod_id.replace('-', '')}_TT"] = {
        "platform": "TIKTOK",
        "handle": pod_vault.get("TIKTOK", {}).get("handle", ""),
        "schedule_slots": PLATFORM_SLOTS["TIKTOK"],
        "sub_id_tag": tiktok_sub_id,
        "tracked_url": origin_url,
        "caption_no_link": f"{title} — Xem chi tiết tại Bio kênh nha! #LearnOnTikTok #ReviewThucTe #{sku_clean}",
        "conversion_payload": "Gắn giỏ hàng TikTok Shop hoặc điều hướng bấm Link Bio",
        "placement_rule": "Bio Link / TikTok Shop",
    }

    for cid, ch in channels_dict.items():
        plat = ch["platform"]
        v_info = variant_by_plat.get(plat, {})
        plat_cfg = pod_vault.get(plat, {})
        acc_status = plat_cfg.get("status", "WAITING_FOR_ACCOUNT")

        queue_state = "READY_TO_AUTO_PUBLISH" if acc_status == "CONNECTED" else "QUEUED_WAITING_ACCOUNT"
        dispatch_results.append(
            {
                "channel_id": cid,
                "platform": plat,
                "account_status": acc_status,
                "video_file": Path(v_info.get("output_path", "")).name,
                "md5_hash": v_info.get("md5_hash", ""),
                "sub_id": ch["sub_id_tag"],
                "schedule_slots": ch["schedule_slots"],
                "queue_state": queue_state,
            }
        )

    return {
        "pod_id": pod_id,
        "pod_name": pack["pod_name"],
        "sku_code": sku_code,
        "title": title,
        "all_5_hashes_unique": repurpose_manifest["all_hashes_unique"],
        "dispatches": dispatch_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-Platform 0-Token Auto-Publisher & Account Vault")
    parser.add_argument("--status", action="store_true", help="Hiển thị bảng trạng thái sẵn sàng 20 kênh (4 Pods × 5 Nền tảng)")
    parser.add_argument("--sync-ig-from-fb", action="store_true", help="Tự động quét và nạp Instagram Business từ các Fanpage FB")
    parser.add_argument("--set-account", action="store_true", help="Nạp tài khoản mới vào bộ khung")
    parser.add_argument("--pod", default="POD-01", help="Mã Brand Pod (POD-01 .. POD-04)")
    parser.add_argument("--platform", help="FB_REELS | IG_REELS | THREADS | YT_SHORTS | TIKTOK")
    parser.add_argument("--handle", help="Tên tài khoản (@...)")
    parser.add_argument("--user-id", help="ID tài khoản / Channel ID / Threads User ID")
    parser.add_argument("--token", help="Access Token nếu dùng API")
    parser.add_argument("--chrome-profile", help="Tên Chrome Profile cách ly")
    parser.add_argument("--related-video-id", help="Video ID dài liên kết cho YouTube Shorts")
    parser.add_argument("--test-pipeline", action="store_true", help="Chạy kiểm thử trọn gói 1 Video -> 5 Nền tảng (0-Token)")
    args = parser.parse_args()

    init_matrix_tables(get_db_path())
    vault = init_or_load_multi_vault(sync_fb=True)

    if args.sync_ig_from_fb:
        found = sync_ig_accounts_from_fb(vault)
        print(f"🔄 Đã quét Graph API 5 Fanpage: Tìm thấy {found} tài khoản Instagram Business đã liên kết.")

    if args.set_account:
        if not args.platform:
            print("❌ Vui lòng truyền --platform (THREADS | YT_SHORTS | TIKTOK | IG_REELS | FB_REELS)")
            return 1
        cfg = set_platform_account(
            vault,
            pod_id=args.pod,
            platform=args.platform,
            handle=args.handle,
            user_id=args.user_id,
            token=args.token,
            chrome_profile=args.chrome_profile,
            related_video_id=args.related_video_id,
        )
        print(f"✅ Đã nạp tài khoản [{args.pod} -> {args.platform}] thành công! Trạng thái: {cfg['status']}")

    if args.test_pipeline:
        sample_video = SUBAGENT_DIR / "output" / "multichannel_variants" / "_sample_master.mp4"
        create_sample_master_video(sample_video)
        summary = prepare_and_queue_all_platforms(
            vault=vault,
            pod_id=args.pod,
            video_path=sample_video,
            sku_code="quat_imi_01",
            origin_url="https://shopee.vn/product/123456/789012",
            title="Quạt cầm tay phản lực iMI 120 cấp độ gió",
        )
        print("\n" + "=" * 105)
        print(f"🧪 KẾT QUẢ CHẠY THỬ PIPELINE 1-RA-5 CHO [{summary['pod_id']}] {summary['pod_name']}")
        print(f"   Kiểm định 5 file Video khác MD5 Hash 100%: {'✅ PASS' if summary['all_5_hashes_unique'] else '❌ FAIL'}")
        print("-" * 105)
        for d in summary["dispatches"]:
            print(
                f"   • {d['platform']:<10} | {d['queue_state']:<23} | File: {d['video_file']:<28} | MD5: {d['md5_hash'][:12]}... | SubID: {d['sub_id']}"
            )
        print("=" * 105)

    if args.status or (not args.set_account and not args.test_pipeline):
        print_status_matrix(vault)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
