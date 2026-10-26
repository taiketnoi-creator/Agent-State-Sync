#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
on_stop_sync_bridge.py — Cầu nối không phụ thuộc ổ đĩa (Drive-Agnostic Bridge) cho Hook Stop.
Tự động định vị `../Agent-State-Sync/on_stop_sync.py` dù Workspace nằm ở:
- Máy Công Ty (`D:\\Phiên bản Ai agent\\Subagent`)
- Máy Ở Nhà (`F:\\Ai Agent Setup\\SubAgent\\Subagent`)
"""

import os
import runpy
import sys
from pathlib import Path

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
STATE_SYNC_SCRIPT = SUBAGENT_DIR.parent / "Agent-State-Sync" / "on_stop_sync.py"

if __name__ == "__main__":
    if STATE_SYNC_SCRIPT.exists():
        sys.path.insert(0, str(STATE_SYNC_SCRIPT.parent))
        runpy.run_path(str(STATE_SYNC_SCRIPT), run_name="__main__")
    else:
        sys.stdout.write('{"decision": "allow"}')
