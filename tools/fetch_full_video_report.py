#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_full_video_report.py — Trích xuất toàn bộ dữ liệu & chỉ số tương tác thực tế của tất cả Video/Reels trên 4 Fanpage.
"""
import sys
import json
import pathlib
import urllib.request
import urllib.error
import datetime as dt

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

VAULT = pathlib.Path.home() / ".codex/mcp/facebook-mcp-server/pages_vault.json"
data = json.loads(VAULT.read_text(encoding="utf-8"))

report = []

for item in data.get("pages", []):
    pid = item.get("id")
    name = item.get("name")
    token = item.get("access_token")
    if not token or pid == "591875884001523":
        continue

    page_data = {
        "page_id": pid,
        "page_name": name,
        "videos": []
    }

    url = f"https://graph.facebook.com/v20.0/{pid}/videos?fields=id,title,description,created_time,length,views&limit=50&access_token={token}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            v_list = json.loads(resp.read().decode("utf-8")).get("data", [])
    except Exception as e:
        print(f"Error fetching videos for {name}: {e}")
        continue

    for v in v_list:
        vid_id = v.get("id")
        title = v.get("title") or (v.get("description") or "").split("\n")[0]
        length = round(v.get("length", 0), 1)
        created_time = v.get("created_time")
        views = v.get("views", 0)

        # 1. Fetch likes and comments summary
        detail_url = f"https://graph.facebook.com/v20.0/{vid_id}?fields=likes.summary(true),comments.summary(true)&access_token={token}"
        likes_cnt = 0
        likers = []
        cmts_cnt = 0
        cmts_list = []
        try:
            with urllib.request.urlopen(detail_url) as resp:
                d_res = json.loads(resp.read().decode("utf-8"))
                likes_summary = d_res.get("likes", {}).get("summary", {})
                likes_cnt = likes_summary.get("total_count", 0)
                likers = [x.get("name") for x in d_res.get("likes", {}).get("data", [])]

                cmts_summary = d_res.get("comments", {}).get("summary", {})
                cmts_cnt = cmts_summary.get("total_count", 0)
                for c in d_res.get("comments", {}).get("data", []):
                    sender = c.get("from", {}).get("name", "Unknown")
                    msg = c.get("message", "")
                    cmts_list.append({"from": sender, "message": msg[:100]})
        except Exception as e:
            pass

        # 2. Fetch video insights
        insights_url = f"https://graph.facebook.com/v20.0/{vid_id}/video_insights?access_token={token}"
        avg_watch_time_s = 0.0
        total_watch_time_s = 0.0
        plays_count = views
        retention = {}
        try:
            with urllib.request.urlopen(insights_url) as resp:
                i_res = json.loads(resp.read().decode("utf-8")).get("data", [])
                for metric in i_res:
                    m_name = metric.get("name")
                    val = metric.get("values", [{}])[0].get("value")
                    if m_name == "post_video_avg_time_watched" and val:
                        avg_watch_time_s = round(val / 1000.0, 1)
                    elif m_name == "post_video_view_time" and val:
                        total_watch_time_s = round(val / 1000.0, 1)
                    elif m_name in ("blue_reels_play_count", "fb_reels_total_plays") and val:
                        plays_count = max(plays_count, int(val))
                    elif m_name == "post_video_retention_graph" and isinstance(val, dict):
                        # Sample retention at key points
                        retention = {
                            "0s": f"{round(val.get('0', 0)*100)}%",
                            "3s": f"{round(val.get('3', 0)*100)}%",
                            "10s": f"{round(val.get('10', 0)*100)}%",
                            "15s": f"{round(val.get('15', 0)*100)}%",
                        }
        except Exception as e:
            pass

        page_data["videos"].append({
            "id": vid_id,
            "title": title,
            "created_time": created_time,
            "length_s": length,
            "views": views,
            "plays_count": plays_count,
            "likes_count": likes_cnt,
            "likers": likers,
            "comments_count": cmts_cnt,
            "comments": cmts_list,
            "avg_watch_time_s": avg_watch_time_s,
            "total_watch_time_s": total_watch_time_s,
            "retention": retention,
        })

    report.append(page_data)

print(json.dumps(report, ensure_ascii=False, indent=2))
