#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fb_cross_page_seeder.py — ĐÃ KHÓA VĨNH VIỄN TƯƠNG TÁC CHÉO GIỮA CÁC PAGE THEO LỆNH CỦA CEO (2026-10-22).

Quy tắc bắt buộc từ CEO (Task #19):
- Chỉ tương tác các Group / Hội nhóm cùng tệp khách hàng (`tools/mama_daily_group_and_eod.py` & `tools/fb_group_browser_interact.py`).
- TUYỆT ĐỐI KHÔNG tương tác chéo giữa các Page với nhau (`0% Cross-Page Seeding`).
- Khi chạy file này, hệ thống sẽ chuyển hướng sang `fb_morning_2210_seeder.py` để quét và dọn sạch bất kỳ bình luận chéo nào giữa các Page.
"""

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    target = Path(__file__).resolve().parent / "fb_morning_2210_seeder.py"
    raise SystemExit(subprocess.call([sys.executable, str(target)]))
