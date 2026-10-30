#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
REMOTION_DIR = ROOT_DIR / "templates" / "remotion-cuongit-template"
SRC_DIR = REMOTION_DIR / "src"
PUBLIC_DIR = REMOTION_DIR / "public"
CAMPAIGN_DIR = ROOT_DIR / "campaigns" / "2026-10-26" / "ai-players-weekly-vault"

d12 = json.loads((CAMPAIGN_DIR / "bespoke_day1_day2_spec.json").read_text(encoding="utf-8"))
d37 = json.loads((CAMPAIGN_DIR / "bespoke_day3_to_day7_spec.json").read_text(encoding="utf-8"))
all_items = d12 + d37

for it in all_items:
    rid = it["id"]
    cid = it["comp_id"]
    cdir = SRC_DIR / cid
    idx_ok = (cdir / "index.tsx").exists()
    scenes_ok = all((cdir / f"Scene{i}.tsx").exists() for i in range(1, 7))
    aud_dir = PUBLIC_DIR / "audio" / "bespoke26" / rid
    mp3_count = len(list(aud_dir.glob("*.mp3"))) if aud_dir.exists() else 0
    print(f"{rid} | {cid:28s} | sched={it['schedule_vn']} | tsx={idx_ok and scenes_ok} | mp3={mp3_count}/6")
