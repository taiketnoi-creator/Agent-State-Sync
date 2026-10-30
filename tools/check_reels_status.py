#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
CAMPAIGN_DIR = ROOT_DIR / "campaigns" / "2026-10-26" / "ai-players-weekly-vault"
VIDEOS_DIR = CAMPAIGN_DIR / "videos_bespoke21"
MANIFEST = CAMPAIGN_DIR / "bespoke_21_weekly_reels_manifest.json"
VAULT_PATH = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / "pages_vault.json"
AI_PAGE_ID = "1022527194267367"

mp4s = sorted(VIDEOS_DIR.glob("*.mp4")) if VIDEOS_DIR.exists() else []
print(f"🎬 MP4 files in {VIDEOS_DIR}: {len(mp4s)}")
for m in mp4s:
    print(f"  - {m.name} ({round(m.stat().st_size / (1024*1024), 2)} MB)")

if MANIFEST.exists():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    print(f"\n📋 Manifest entries: {len(data)}")
    for it in data:
        print(f"  - {it.get('id')} ({it.get('comp_id')}): status={it.get('status')}, sched={it.get('schedule_vn')}, fb_video_id={it.get('fb_video_id')}")
else:
    print("\n⚠️ No bespoke_21_weekly_reels_manifest.json found!")

# Check Facebook Page published videos & scheduled posts
vault = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
token = next(p["access_token"] for p in vault["pages"] if str(p["id"]) == AI_PAGE_ID)

url_vids = f"https://graph.facebook.com/v22.0/{AI_PAGE_ID}/videos?fields=id,title,description,created_time,published&limit=20&access_token={token}"
try:
    with urllib.request.urlopen(url_vids, timeout=20.0) as resp:
        vdata = json.loads(resp.read().decode("utf-8"))
        print(f"\n📺 Videos on Page AI Players ({len(vdata.get('data', []))}):")
        for v in vdata.get("data", [])[:10]:
            print(f"  - ID={v.get('id')} | published={v.get('published')} | created={v.get('created_time')} | title={str(v.get('title', ''))[:45]}")
except Exception as e:
    print("Error fetching videos:", e)
