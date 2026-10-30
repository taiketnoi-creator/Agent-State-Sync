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

dirs = sorted([d.name for d in SRC_DIR.iterdir() if d.is_dir()])
print("Directories in src/:", dirs)

# Check if any mp4 exists anywhere in campaigns/2026-10-26
cdir = ROOT_DIR / "campaigns" / "2026-10-26"
mp4s = list(cdir.rglob("*.mp4")) if cdir.exists() else []
print("MP4s in campaigns/2026-10-26:", [str(m.relative_to(ROOT_DIR)) for m in mp4s])
