#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cleanup_old_media.py — Công cụ Tự Động Dọn Kho Hình Ảnh & Video Local Quá Hạn (Mặc định: 7 ngày).

Cơ chế hoạt động:
1. Quét thư mục `campaigns/<YYYY-MM-DD>/`:
   - Tính tuổi chiến dịch dựa trên tên thư mục chuẩn `YYYY-MM-DD` (chính xác tuyệt đối kể cả khi vừa git clone/copy sang máy mới) hoặc `mtime` của file.
   - Xóa toàn bộ file media/binary nặng quá hạn (`>= days` ngày):
     + Video: .mp4, .mov, .mkv, .webm, .avi
     + Hình ảnh: .jpg, .jpeg, .png, .webp, .gif, .bmp
     + Âm thanh: .mp3, .wav, .m4a, .aac, .ogg, .flac
     + Font/Binary/Build tạm trong campaign: .ttf, .otf, .woff, .woff2, .zip, .tsx, .ts, .json, .yaml, .mjs
     + Thư mục con chứa media/build tạm trong campaign quá hạn: `images/`, `assets/`, `qa-frames/`, `out/`, `remotion/`, `node_modules/`
   - Giữ lại các file nhật ký `.md` siêu nhẹ (vài KB) để lưu lịch sử Post ID & kịch bản (trừ khi truyền `--purge-all`).
2. Quét thư mục tạm của Remotion Template (`templates/remotion-cuongit-template/out/` và `public/audio/<Topic>/` quá hạn 7 ngày):
   - TUYỆT ĐỐI BẢO VỆ: `assets/` gốc của dự án, `brand-kit/`, `fonts/` gốc, `knowledge/`, `training/`, `tools/`.
3. Ghi log kết quả dọn dẹp vào `campaigns/cleanup-history.log` và trả về thống kê dung lượng giải phóng.
"""

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
CAMPAIGNS_DIR = SUBAGENT_DIR / "campaigns"
REMOTION_DIR = SUBAGENT_DIR / "templates" / "remotion-cuongit-template"

MEDIA_EXTENSIONS = {
    # Video
    ".mp4", ".mov", ".mkv", ".webm", ".avi",
    # Image
    ".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp",
    # Audio
    ".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac",
    # Fonts & archives inside campaign folders
    ".ttf", ".otf", ".woff", ".woff2", ".zip", ".tar", ".gz",
}

HEAVY_CAMPAIGN_SUBDIRS = {
    "images",
    "assets",
    "qa-frames",
    "out",
    "remotion",
    "node_modules",
    ".remotion",
    "video",
    "audio",
}

DATE_DIR_PATTERN = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


def get_folder_size_bytes(path: Path) -> int:
    total = 0
    if not path.exists():
        return 0
    if path.is_file():
        try:
            return path.stat().st_size
        except OSError:
            return 0
    for root, _, files in os.walk(path):
        for f in files:
            fp = Path(root) / f
            try:
                total += fp.stat().st_size
            except OSError:
                pass
    return total


def format_bytes(num_bytes: int) -> str:
    mb = num_bytes / (1024 * 1024)
    if mb >= 1024:
        return f"{mb / 1024:.2f} GB"
    return f"{mb:.2f} MB"


def parse_campaign_date(folder_name: str):
    m = DATE_DIR_PATTERN.match(folder_name.strip())
    if not m:
        return None
    try:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def remove_empty_dirs(root_dir: Path):
    if not root_dir.exists() or not root_dir.is_dir():
        return
    for current_root, dirs, _ in os.walk(root_dir, topdown=False):
        for d in dirs:
            dp = Path(current_root) / d
            try:
                if dp.exists() and not any(dp.iterdir()):
                    dp.rmdir()
            except OSError:
                pass


def run_cleanup(
    days: int = 7,
    dry_run: bool = False,
    purge_all: bool = False,
    reference_date: dt.date = None,
) -> dict:
    today = reference_date or dt.date.today()
    cutoff_date = today - dt.timedelta(days=days)
    cutoff_ts = dt.datetime.combine(cutoff_date, dt.time.max).timestamp()

    deleted_files_count = 0
    deleted_dirs_count = 0
    freed_bytes = 0
    cleaned_campaigns = []
    details = []

    # 1. Quét thư mục campaigns/<YYYY-MM-DD>
    if CAMPAIGNS_DIR.exists():
        for entry in sorted(CAMPAIGNS_DIR.iterdir()):
            if not entry.is_dir():
                continue

            camp_date = parse_campaign_date(entry.name)
            is_expired_campaign = False
            if camp_date is not None:
                # Nếu chiến dịch có ngày <= cutoff_date (tức cách hôm nay >= days ngày)
                if camp_date <= cutoff_date:
                    is_expired_campaign = True
            else:
                try:
                    if entry.stat().st_mtime <= cutoff_ts:
                        is_expired_campaign = True
                except OSError:
                    pass

            if not is_expired_campaign:
                continue

            camp_freed = 0
            camp_files = 0

            if purge_all:
                sz = get_folder_size_bytes(entry)
                cnt = sum(1 for _ in entry.rglob("*") if _.is_file())
                if not dry_run:
                    shutil.rmtree(entry, ignore_errors=True)
                freed_bytes += sz
                deleted_files_count += cnt
                deleted_dirs_count += 1
                cleaned_campaigns.append(entry.name)
                details.append(f"Xóa toàn bộ campaign `{entry.name}` ({cnt} files, {format_bytes(sz)})")
                continue

            # Xóa các thư mục con nặng (remotion, images, assets, qa-frames, out, node_modules...)
            deleted_subpaths = []
            for sub in sorted(entry.rglob("*"), key=lambda p: len(p.parts)):
                if not sub.exists():
                    continue
                if any(parent in sub.parents for parent in deleted_subpaths):
                    continue
                if sub.is_dir() and sub.name.lower() in HEAVY_CAMPAIGN_SUBDIRS:
                    sz = get_folder_size_bytes(sub)
                    cnt = sum(1 for f in sub.rglob("*") if f.is_file())
                    if sz > 0 or cnt > 0:
                        deleted_subpaths.append(sub)
                        if not dry_run:
                            shutil.rmtree(sub, ignore_errors=True)
                        camp_freed += sz
                        camp_files += cnt
                        deleted_dirs_count += 1

            # Xóa các file media lẻ còn sót trong campaign quá hạn (giữ lại .md)
            for fpath in list(entry.rglob("*")):
                if not fpath.exists() or not fpath.is_file():
                    continue
                if any(parent in fpath.parents for parent in deleted_subpaths):
                    continue
                if fpath.suffix.lower() in MEDIA_EXTENSIONS:
                    try:
                        sz = fpath.stat().st_size
                    except OSError:
                        sz = 0
                    if not dry_run:
                        try:
                            fpath.unlink()
                        except OSError:
                            pass
                    camp_freed += sz
                    camp_files += 1

            if not dry_run:
                remove_empty_dirs(entry)

            if camp_freed > 0 or camp_files > 0:
                freed_bytes += camp_freed
                deleted_files_count += camp_files
                cleaned_campaigns.append(entry.name)
                details.append(
                    f"Campaign `{entry.name}` (ngày {camp_date}): đã dọn {camp_files} file media/build, giải phóng **{format_bytes(camp_freed)}** (giữ nguyên file `.md`)"
                )

    # 2. Quét thư mục tạm Remotion out/ (chỉ xóa file .mp4/.mov quá hạn >= days ngày)
    remotion_out = REMOTION_DIR / "out"
    if remotion_out.exists() and remotion_out.is_dir():
        for fpath in list(remotion_out.rglob("*")):
            if fpath.is_file() and fpath.suffix.lower() in MEDIA_EXTENSIONS:
                try:
                    mtime = fpath.stat().st_mtime
                    sz = fpath.stat().st_size
                except OSError:
                    continue
                if mtime <= cutoff_ts:
                    if not dry_run:
                        try:
                            fpath.unlink()
                        except OSError:
                            pass
                    freed_bytes += sz
                    deleted_files_count += 1
                    details.append(f"Remotion out `{fpath.name}`: giải phóng {format_bytes(sz)}")

    remaining_campaigns_bytes = get_folder_size_bytes(CAMPAIGNS_DIR)

    result = {
        "today": str(today),
        "retention_days": days,
        "cutoff_date": str(cutoff_date),
        "dry_run": dry_run,
        "deleted_files_count": deleted_files_count,
        "deleted_dirs_count": deleted_dirs_count,
        "freed_bytes": freed_bytes,
        "freed_human": format_bytes(freed_bytes),
        "cleaned_campaigns": cleaned_campaigns,
        "remaining_campaigns_bytes": remaining_campaigns_bytes,
        "remaining_campaigns_human": format_bytes(remaining_campaigns_bytes),
        "details": details,
    }

    if not dry_run and (deleted_files_count > 0 or deleted_dirs_count > 0):
        log_path = CAMPAIGNS_DIR / "cleanup-history.log"
        try:
            CAMPAIGNS_DIR.mkdir(parents=True, exist_ok=True)
            ts_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_line = (
                f"[{ts_str}] AUTO-CLEANUP (>{days}d, cutoff <={cutoff_date}): "
                f"cleaned={cleaned_campaigns}, files_deleted={deleted_files_count}, "
                f"freed={result['freed_human']}, remaining_campaigns={result['remaining_campaigns_human']}\n"
            )
            with open(log_path, "a", encoding="utf-8") as lf:
                lf.write(log_line)
        except Exception:
            pass

    return result


def main():
    parser = argparse.ArgumentParser(description="Auto-cleanup old campaign media & videos (>= 7 days)")
    parser.add_argument("--days", type=int, default=7, help="Retention period in days (default: 7)")
    parser.add_argument("--dry-run", action="store_true", help="Preview files to delete without deleting")
    parser.add_argument("--purge-all", action="store_true", help="Delete entire expired campaign folders including .md")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    args = parser.parse_args()

    res = run_cleanup(days=args.days, dry_run=args.dry_run, purge_all=args.purge_all)

    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return

    mode_str = "DRY-RUN (CHẠY THỬ)" if args.dry_run else "LIVE CLEANUP (ĐÃ DỌN DẸP)"
    print(f"=== 🧹 BÁO CÁO DỌN KHO MEDIA LOCAL ({mode_str}) ===")
    print(f"- Ngày hiện tại: {res['today']} | Ngưỡng giữ lại: {res['retention_days']} ngày (Xóa media từ ngày <= {res['cutoff_date']})")
    print(f"- Số file media/build đã xóa: {res['deleted_files_count']} files ({res['deleted_dirs_count']} thư mục media/build)")
    print(f"- Dung lượng ổ cứng giải phóng: {res['freed_human']}")
    print(f"- Dung lượng kho `campaigns/` hiện tại: {res['remaining_campaigns_human']}")
    if res["details"]:
        print("- Chi tiết:")
        for d in res["details"]:
            print(f"  + {d}")
    else:
        print("- Chi tiết: Không có media nào quá hạn 7 ngày cần xóa.")


if __name__ == "__main__":
    main()
