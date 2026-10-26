#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import pathlib

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

p = pathlib.Path("campaigns/daily-reports/video_engagement_raw.json")
raw = p.read_bytes()
for enc in ("utf-8-sig", "utf-16", "utf-8"):
    try:
        data = json.loads(raw.decode(enc))
        break
    except Exception:
        pass

total_videos = sum(len(x["videos"]) for x in data)
total_views = sum(sum(v["views"] for v in x["videos"]) for x in data)
total_likes = sum(sum(v["likes_count"] for v in x["videos"]) for x in data)
total_cmts = sum(sum(v["comments_count"] for v in x["videos"]) for x in data)
total_watch_time = sum(sum(v["total_watch_time_s"] for v in x["videos"]) for x in data)

print(f"=== TỔNG QUAN TƯƠNG TÁC TOÀN BỘ VIDEO ({total_videos} Videos) ===")
print(f"👁️ Tổng lượt xem (Views): {total_views} lượt xem")
print(f"⏱️ Tổng thời gian xem (Watch Time): {round(total_watch_time/60, 1)} phút ({round(total_watch_time)}s)")
print(f"👍 Tổng lượt Thích/Reactions: {total_likes} lượt")
print(f"💬 Tổng lượt Bình luận (Comments): {total_cmts} bình luận")
print("=" * 60)

for page in data:
    pname = page["page_name"]
    vids = page["videos"]
    p_views = sum(v["views"] for v in vids)
    p_likes = sum(v["likes_count"] for v in vids)
    p_cmts = sum(v["comments_count"] for v in vids)
    print(f"\n📂 FANPAGE: {pname}")
    print(f"   • Số lượng video: {len(vids)} | Lượt xem: {p_views} | Likes: {p_likes} | Bình luận: {p_cmts}")
    for idx, v in enumerate(vids, 1):
        likers_str = ", ".join(v["likers"][:3]) if v["likers"] else "Chưa có"
        ret = v.get("retention", {})
        ret_str = f"0s: {ret.get('0s','-')}, 3s: {ret.get('3s','-')}, 10s: {ret.get('10s','-')}" if ret else "Chưa có data retention"
        print(f"   [{idx}] {v['title']}")
        print(f"       - Video ID: {v['id']} | Ngày đăng: {v['created_time'][:10]} | Thời lượng: {v['length_s']}s")
        print(f"       - Lượt xem (Views): {v['views']} | Xem TB: {v['avg_watch_time_s']}s | Tổng tg xem: {v['total_watch_time_s']}s")
        print(f"       - Tương tác: {v['likes_count']} Like ({likers_str}) | {v['comments_count']} Bình luận")
        print(f"       - Tỷ lệ giữ chân (Retention): {ret_str}")
        if v.get("comments"):
            for c in v["comments"][:2]:
                print(f"         💬 [{c['from']}]: {c['message'][:80]}...")
