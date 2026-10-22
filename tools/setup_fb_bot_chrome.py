#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import shutil
import sqlite3
import subprocess
import time
import urllib.request
from pathlib import Path

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
UD = Path.home() / "AppData/Local/Google/Chrome/User Data"
BOT_DIR = SUBAGENT_DIR / ".chrome-fb-bot"


def find_fb_profile() -> Path:
    for p in ["Profile 1", "Profile 9", "Default", "Profile 3", "Profile 5", "Profile 6", "Profile 8", "Profile 10"]:
        ck = UD / p / "Network" / "Cookies"
        if not ck.exists():
            continue
        tmp = SUBAGENT_DIR / "output" / "_tmp_ck.db"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        try:
            # Copy via esentutl or raw read if locked
            shutil.copyfile(ck, tmp)
            conn = sqlite3.connect(str(tmp))
            cnt = conn.execute("SELECT count(1) FROM cookies WHERE host_key LIKE '%facebook.com%' AND name='c_user'").fetchone()[0]
            conn.close()
            if cnt > 0:
                print(f"Found Facebook c_user in {p}")
                return UD / p
        except Exception as e:
            print(f"{p}: {e}")
    return UD / "Profile 1"


def sync_to_bot_dir():
    src_prof = find_fb_profile()
    BOT_DIR.mkdir(parents=True, exist_ok=True)
    default_dst = BOT_DIR / "Default"
    default_dst.mkdir(parents=True, exist_ok=True)

    # Copy Local State so DPAPI key matches
    local_state = UD / "Local State"
    if local_state.exists():
        shutil.copyfile(local_state, BOT_DIR / "Local State")

    # Copy Preferences & Network/Cookies
    for rel in ["Preferences", "Secure Preferences", "Network/Cookies", "Network/Cookies-journal"]:
        s = src_prof / rel
        d = default_dst / rel
        if s.exists():
            d.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copyfile(s, d)
            except Exception as e:
                print(f"Skip {rel}: {e}")

    print(f"Synced {src_prof.name} -> {BOT_DIR}")


if __name__ == "__main__":
    sync_to_bot_dir()
