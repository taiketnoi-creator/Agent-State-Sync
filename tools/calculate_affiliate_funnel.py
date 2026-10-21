#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calculate_affiliate_funnel.py
-----------------------------
Công cụ phân tích phễu chuyển đổi Affiliate Video Ngắn (0-Token) cho Agent-Javis.
Hỗ trợ 2 chế độ:
  1. Truyền chỉ số trực tiếp qua CLI (--views, --hook-3s, --watch-50, --clicks, --orders, --revenue)
  2. Đọc trực tiếp từ cơ sở dữ liệu SQLite (--db, mặc định: database/aff_system.db)

Tự động áp dụng Giao thức chẩn đoán 3 lớp của `hieu-suat.md`:
  - Lớp 1: Hook / Nội dung / Retention
  - Lớp 2: CTA / Link visibility
  - Lớp 3: Giá sản phẩm, phí ship, tồn kho & Shop listing
Đưa ra kết luận KEEP / ITERATE / STOP và heading chuẩn:
  ## Hành động cụ thể cho video kế tiếp (Actionable Next Step)

Sử dụng:
  python tools/calculate_affiliate_funnel.py --views 100000 --clicks 5 --orders 0
  python tools/calculate_affiliate_funnel.py --views 50000 --hook-3s 32000 --watch-50 15000 --clicks 450 --orders 18 --revenue 350000
  python tools/calculate_affiliate_funnel.py --db database/aff_system.db --job-id 1
"""

import sys
import os
import json
import sqlite3
import argparse
from typing import Optional, Dict, Any

# Đảm bảo in tiếng Việt mượt mà trên console Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


DEFAULT_DB_CANDIDATES = [
    os.path.join("database", "aff_system.db"),
    os.path.join("data", "aff_system.db"),
    os.path.expanduser(r"~\.gemini\antigravity\scratch\ai-aff-video-system\data\aff_system.db")
]


def calculate_metrics(
    views: int,
    hook_3s: Optional[int] = None,
    watch_50: Optional[int] = None,
    clicks: int = 0,
    orders: int = 0,
    revenue: float = 0.0
) -> Dict[str, Any]:
    """Tính toán chi tiết các tỷ lệ chuyển đổi và đối soát mẫu số."""
    if views <= 0:
        return {"error": "Số lượt xem (views) phải lớn hơn 0"}

    # 1. 3-Second Hook Rate
    hook_rate_pct = None
    if hook_3s is not None:
        hook_rate_pct = round((hook_3s / views) * 100.0, 2)

    # 2. 50% Hold Rate
    hold_rate_pct = None
    if watch_50 is not None:
        hold_rate_pct = round((watch_50 / views) * 100.0, 2)

    # 3. View-to-Click CTR (%)
    ctr_pct = round((clicks / views) * 100.0, 4)

    # 4. Click-to-Order CVR (%)
    cvr_pct = None
    directional_only = False
    if clicks > 0:
        cvr_pct = round((orders / clicks) * 100.0, 2)
        if clicks < 30:
            directional_only = True
    else:
        cvr_pct = 0.0

    # 5. View-to-Order CVR (%)
    view_to_order_pct = round((orders / views) * 100.0, 4)

    # 6. Revenue / Commission per 1,000 views (RPM)
    rpm = round((revenue / views) * 1000.0, 2) if revenue > 0 else 0.0

    # 7. EPC (Earnings Per Click)
    epc = round(revenue / clicks, 2) if clicks > 0 and revenue > 0 else 0.0

    return {
        "views": views,
        "hook_3s": hook_3s,
        "watch_50": watch_50,
        "clicks": clicks,
        "orders": orders,
        "revenue": revenue,
        "hook_rate_pct": hook_rate_pct,
        "hold_rate_pct": hold_rate_pct,
        "ctr_pct": ctr_pct,
        "cvr_pct": cvr_pct,
        "view_to_order_pct": view_to_order_pct,
        "directional_only": directional_only,
        "rpm": rpm,
        "epc": epc
    }


def diagnose_funnel(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Áp dụng Giao thức chẩn đoán 3 lớp của hieu-suat.md
    """
    views = metrics["views"]
    clicks = metrics["clicks"]
    orders = metrics["orders"]
    ctr = metrics["ctr_pct"]
    cvr = metrics["cvr_pct"]
    hook_rate = metrics["hook_rate_pct"]
    is_directional = metrics["directional_only"]

    diagnosis_layers = []
    decision = "ITERATE"
    actionable_next_step = ""

    # LỚP 1: HOOK / NỘI DUNG / RETENTION
    if hook_rate is not None and hook_rate < 35.0:
        diagnosis_layers.append({
            "layer": 1,
            "name": "Hook & Nội Dung Đầu Video (3s Hook Rate)",
            "finding": f"3-second Hook Rate yếu ({hook_rate}% < 35.0%). Khán giả lướt qua ngay trong 3s đầu.",
            "evidence": f"Chỉ {metrics['hook_3s']:,} / {views:,} người xem dừng lại quá 3s.",
            "action": "Đổi visual 0-3s sang cú sốc tương phản Before/After, đưa nỗi đau ức chế lên giây 0, bỏ toàn bộ lời dẫn."
        })
    elif ctr < 0.05 and views >= 10000:
        diagnosis_layers.append({
            "layer": 1,
            "name": "Ý Định Mua Của Traffic (Audience Intent)",
            "finding": f"Lượng view lớn ({views:,}) nhưng CTR cực thấp ({ctr}%). Traffic rộng nhưng không có ý định mua.",
            "evidence": "Khoảng cách lớn giữa lượt xem giải trí và hành vi click link.",
            "action": "Đưa sản phẩm và Before/After vào sớm hơn trước giây thứ 10; tránh làm nội dung quá xa rời công năng sản phẩm."
        })

    # LỚP 2: CTA & LINK VISIBILITY
    if ctr < 0.15:
        diagnosis_layers.append({
            "layer": 2,
            "name": "Lời Kêu Gọi Hành Động & Vị Trí Đặt Link (CTA Visibility)",
            "finding": f"View-to-Click CTR đạt {ctr}% (dưới ngưỡng kỳ vọng 0.3% - 0.8%). Lời kêu gọi hành động hoặc vị trí đặt link chưa đủ rõ.",
            "evidence": f"Chỉ phát sinh {clicks} clicks trên {views:,} lượt xem.",
            "action": "Chỉ định vị trí link rõ ràng theo từng nền tảng (Reels: 'Link tui ghim ở bình luận đầu tiên'; Shorts: 'Link bio đầu kênh'); đưa CTA xuất hiện sớm hơn trước khi retention rơi tự do."
        })

    # LỚP 3: GIÁ, SHOP LISTING & MA SÁT TRÊN LANDING PAGE
    if is_directional:
        diagnosis_layers.append({
            "layer": 3,
            "name": "Độ Tin Cậy Mẫu Click & Listing Shopee",
            "finding": f"Chỉ có {clicks} clicks (mẫu < 30 clicks). Tỷ lệ CVR {cvr}% chỉ mang tính định hướng (directional only).",
            "evidence": "Chưa đủ cỡ mẫu thống kê để kết luận giá hay shop là nguyên nhân gây rớt đơn hàng.",
            "action": "Tập trung giải quyết nghẽn ở Lớp 1 và Lớp 2 để kéo tối thiểu 30-50 clicks trước khi thay đổi giá hay đổi shop listing."
        })
    elif clicks >= 30 and cvr < 1.0:
        diagnosis_layers.append({
            "layer": 3,
            "name": "Giá, Phí Ship, Rating & Listing Shopee",
            "finding": f"CTR tốt nhưng CVR thấp ({cvr}% < 1.0% với {clicks} clicks). Người xem bấm vào Shopee nhưng không chốt mua.",
            "evidence": f"{clicks} clicks nhưng chỉ có {orders} đơn hàng thành công.",
            "action": "Kiểm tra giá thực tế theo biến thể, phí ship (nếu > 30k sinh viên sẽ bỏ giỏ), tồn kho, voucher giảm giá và đánh giá 1 sao gần đây của shop."
        })

    # RA QUYẾT ĐỊNH KEEP / ITERATE / STOP & ACTIONABLE NEXT STEP
    if orders >= 10 and ctr >= 0.4 and (cvr is not None and cvr >= 2.0):
        decision = "KEEP"
        actionable_next_step = (
            "Tiếp tục nhân bản creative chiến thắng: Giữ nguyên Hook và cấu trúc kịch bản, "
            "thử nghiệm 2 biến thể âm thanh/ASMR khác nhau và lên lịch phát sóng vào khung giờ vàng kế tiếp."
        )
    elif views >= 50000 and clicks < 10 and orders == 0:
        decision = "ITERATE"
        actionable_next_step = (
            "Giữ nguyên sản phẩm và visual chính, chỉ thay CTA bằng một câu nêu rõ lợi ích "
            "+ chỉ đúng vị trí link ('Link tui ghim ở bình luận đầu tiên nha!'), "
            "đưa CTA vào lúc retention còn đủ cao; theo dõi view-to-click CTR trên cùng attribution window trước khi thay thêm biến khác."
        )
    elif views < 5000 and orders == 0:
        decision = "ITERATE"
        actionable_next_step = (
            "Tập trung cải thiện 3s Hook đầu tiên: Thay thế câu mở đầu bằng tình huống Before/After gây cấn "
            "hoặc một câu hỏi trực diện nỗi đau thường nhật của học sinh/sinh viên."
        )
    else:
        decision = "ITERATE"
        actionable_next_step = (
            "Chọn duy nhất một biến chính để tối ưu (Hook visual hoặc CTA wording). "
            "Giữ cố định các thông số còn lại và theo dõi chỉ số phễu trong chu kỳ 24h - 72h tiếp theo."
        )

    return {
        "decision": decision,
        "diagnosis_layers": diagnosis_layers,
        "actionable_next_step": actionable_next_step
    }


def query_from_sqlite(db_path: str, job_id: Optional[int] = None) -> Dict[str, Any]:
    """Đọc dữ liệu video/metrics từ SQLite database."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Không tìm thấy database tại '{db_path}'")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Kiểm tra xem có bảng video_metrics hoặc video_jobs không
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cursor.fetchall()]

    metrics_data = None
    if "video_metrics" in tables:
        if job_id:
            cursor.execute("SELECT views, hook_3s, watch_50, clicks, orders, revenue FROM video_metrics WHERE job_id = ? LIMIT 1", (job_id,))
        else:
            cursor.execute("SELECT views, hook_3s, watch_50, clicks, orders, revenue FROM video_metrics ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            metrics_data = {
                "views": row[0],
                "hook_3s": row[1],
                "watch_50": row[2],
                "clicks": row[3],
                "orders": row[4],
                "revenue": row[5]
            }

    if not metrics_data and "video_jobs" in tables:
        # Lấy thông tin job gần nhất
        if job_id:
            cursor.execute("SELECT id, title, hook_3s FROM video_jobs WHERE id = ?", (job_id,))
        else:
            cursor.execute("SELECT id, title, hook_3s FROM video_jobs ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            print(f"[INFO] Đọc từ video_jobs ID={row[0]}: '{row[1]}'")

    conn.close()

    if not metrics_data:
        raise ValueError(f"Chưa có bản ghi số liệu hiệu suất nào trong database '{db_path}'")

    return metrics_data


def main():
    parser = argparse.ArgumentParser(
        description="Công cụ phân tích phễu chuyển đổi Affiliate Video Ngắn (0-Token) cho Agent-Javis"
    )
    # Nhóm 1: Nhập tay qua CLI
    cli_group = parser.add_argument_group("Nhập chỉ số qua CLI")
    cli_group.add_argument("--views", type=int, help="Tổng số lượt xem (views)")
    cli_group.add_argument("--hook-3s", type=int, default=None, help="Lượt xem giữ chân qua 3 giây đầu")
    cli_group.add_argument("--watch-50", type=int, default=None, help="Lượt xem đạt trên 50%% thời lượng")
    cli_group.add_argument("--clicks", type=int, default=0, help="Số lượt nhấp link Shopee (clicks)")
    cli_group.add_argument("--orders", type=int, default=0, help="Số đơn hàng hợp lệ phát sinh (orders)")
    cli_group.add_argument("--revenue", type=float, default=0.0, help="Tổng hoa hồng / doanh thu ước tính (VND)")

    # Nhóm 2: Đọc từ Database
    db_group = parser.add_argument_group("Đọc từ Database SQLite")
    db_group.add_argument("--db", type=str, default=None, help="Đường dẫn file database SQLite")
    db_group.add_argument("--job-id", type=int, default=None, help="ID của video job cần phân tích")

    parser.add_argument("--json", action="store_true", help="Xuất kết quả định dạng JSON")

    args = parser.parse_args()

    # Xác định nguồn dữ liệu
    views = args.views
    hook_3s = args.hook_3s
    watch_50 = args.watch_50
    clicks = args.clicks
    orders = args.orders
    revenue = args.revenue

    if views is None:
        # Thử tìm SQLite database
        db_path = args.db
        if not db_path:
            for cand in DEFAULT_DB_CANDIDATES:
                if os.path.exists(cand):
                    db_path = cand
                    break

        if db_path and os.path.exists(db_path):
            try:
                db_metrics = query_from_sqlite(db_path, args.job_id)
                views = db_metrics["views"]
                hook_3s = db_metrics.get("hook_3s")
                watch_50 = db_metrics.get("watch_50")
                clicks = db_metrics.get("clicks", 0)
                orders = db_metrics.get("orders", 0)
                revenue = db_metrics.get("revenue", 0.0)
            except Exception as e:
                print(f"[CẢNH BÁO] Không thể đọc từ SQLite: {e}. Vui lòng truyền chỉ số qua CLI.", file=sys.stderr)
                parser.print_help()
                sys.exit(1)
        else:
            # Nếu không có cả CLI và DB
            print("Lỗi: Vui lòng cung cấp chỉ số qua CLI (--views, --clicks, --orders) hoặc chỉ định file SQLite (--db)!", file=sys.stderr)
            parser.print_help()
            sys.exit(1)

    metrics = calculate_metrics(
        views=views,
        hook_3s=hook_3s,
        watch_50=watch_50,
        clicks=clicks,
        orders=orders,
        revenue=revenue
    )

    if "error" in metrics:
        print(f"Lỗi: {metrics['error']}", file=sys.stderr)
        sys.exit(1)

    diagnosis = diagnose_funnel(metrics)

    output_payload = {
        "metrics": metrics,
        "diagnosis": diagnosis
    }

    if args.json:
        print(json.dumps(output_payload, ensure_ascii=False, indent=2))
    else:
        print("\n==================================================")
        print("    BÁO CÁO PHÂN TÍCH PHỄU CHUYỂN ĐỔI AFFILIATE   ")
        print("           (AGENT-JAVIS PERFORMANCE)             ")
        print("==================================================")
        print(f"Lượt xem (Views):            {metrics['views']:,}")
        if metrics['hook_3s'] is not None:
            print(f"Giữ chân 3s (Hook Rate):     {metrics['hook_3s']:,} ({metrics['hook_rate_pct']}%)")
        if metrics['watch_50'] is not None:
            print(f"Giữ chân 50% (Hold Rate):    {metrics['watch_50']:,} ({metrics['hold_rate_pct']}%)")
        print(f"Lượt click Shopee (Clicks):  {metrics['clicks']:,} (CTR: {metrics['ctr_pct']}%)")
        print(f"Đơn hàng hợp lệ (Orders):    {metrics['orders']:,}")
        
        cvr_display = f"{metrics['cvr_pct']}%"
        if metrics['directional_only']:
            cvr_display += "  [CẢNH BÁO: directional only (mẫu < 30 clicks)]"
        print(f"Tỷ lệ chốt đơn (CVR):        {cvr_display}")
        
        if metrics['revenue'] > 0:
            print(f"Hoa hồng ước tính:           {metrics['revenue']:,.0f} đ (RPM: {metrics['rpm']} đ / 1k views)")

        print("--------------------------------------------------")
        print(f"QUYẾT ĐỊNH VẬN HÀNH:        [{diagnosis['decision']}]")
        print("--------------------------------------------------")
        print("CHẨN ĐOÁN 3 LỚP (DIAGNOSIS):")
        for layer in diagnosis["diagnosis_layers"]:
            print(f"\n[Lớp {layer['layer']}] {layer['name']}")
            print(f" • Nhận định: {layer['finding']}")
            print(f" • Bằng chứng: {layer['evidence']}")
            print(f" • Hành động:  {layer['action']}")

        print("\n--------------------------------------------------")
        print("## Hành động cụ thể cho video kế tiếp (Actionable Next Step)")
        print(diagnosis["actionable_next_step"])
        print("==================================================\n")


if __name__ == "__main__":
    main()
