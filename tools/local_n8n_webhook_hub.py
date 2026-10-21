import datetime
import json
import os
import re
import sqlite3
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRATCH_BASE = r"C:\Users\guicci\.gemini\antigravity\scratch\ai-aff-video-system"
DB_PATH = os.environ.get("AFF_DB_PATH", os.path.join(SCRATCH_BASE, "data", "aff_system.db"))
QUEUE_DIR = os.path.join(SCRATCH_BASE, "output", "publish_queue")
PORT = int(os.environ.get("N8N_PORT", "5678"))


def process_video_publish(body: dict) -> tuple[int, dict]:
    video_path = str(body.get("video_path", "")).strip()
    if not video_path:
        return 400, {
            "status": "REJECTED_MISSING_VIDEO_PATH",
            "error": "Field 'video_path' is required by Gate: Validate Video & Payload"
        }

    job_id = body.get("job_id", "auto")
    product_id = body.get("product_id", 1)
    raw_url = str(body.get("aff_url", "")).strip()
    sep = "&" if "?" in raw_url else "?"
    fb_utm = f"{raw_url}{sep}utm_source=fb_reels&utm_medium=pinned_comment&utm_campaign=job_{job_id}" if raw_url else ""
    yt_utm = f"{raw_url}{sep}utm_source=yt_shorts&utm_medium=description&utm_campaign=job_{job_id}" if raw_url else ""

    raw_caption = str(body.get("caption") or body.get("title") or "Đồ tiện ích thông minh đáng thử")
    clean_caption = re.sub(r"https?://\S+", "", raw_caption).strip()
    fb_caption = f"{clean_caption}\n\n👉 Link sản phẩm tui ghim ở bình luận đầu tiên nha!"
    fb_pinned = (
        f"🔥 Chốt đơn chính hãng giá hời tại đây nha các bác: {fb_utm}"
        if fb_utm
        else "🔥 Link sản phẩm đang cập nhật ở bình luận đầu tiên nha!"
    )

    base_title = str(body.get("title") or "Món đồ tiện ích cứu cánh mỗi ngày")[:35].strip()
    yt_title = f"{base_title} #Shorts #TienIch #Review"
    yt_desc = f"{clean_caption}\n\n👉 Chi tiết món này tui để ở phần Mô tả video và Link bio đầu kênh nhé: {yt_utm}".strip()

    slot = "20:00" if str(body.get("schedule_slot")) == "20:00" else "11:45"
    approval_gate = str(body.get("approval_status") or "DRAFT_ONLY")
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    result = {
        "status": "READY_FOR_PUBLISH_QUEUE",
        "job_id": job_id,
        "product_id": product_id,
        "video_path": video_path,
        "schedule_slot": slot,
        "approval_gate": approval_gate,
        "channels": {
            "facebook_reels": {
                "caption_no_link": fb_caption,
                "pinned_comment_with_link": fb_pinned,
                "tracked_aff_url": fb_utm
            },
            "youtube_shorts": {
                "title_under_60_chars": yt_title,
                "title_length": len(yt_title),
                "description": yt_desc,
                "tracked_aff_url": yt_utm
            }
        },
        "processed_at": now_iso
    }

    os.makedirs(QUEUE_DIR, exist_ok=True)
    queue_file = os.path.join(QUEUE_DIR, f"job_{job_id}_publish_pack.json")
    with open(queue_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    result["queue_manifest_path"] = queue_file

    if os.path.exists(DB_PATH) and str(job_id).isdigit():
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute(
                "UPDATE video_jobs SET status = ? WHERE id = ?",
                ("queued_for_publish" if approval_gate == "DRAFT_ONLY" else "published", int(job_id))
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

    return 200, result


def process_product_alert(body: dict) -> tuple[int, dict]:
    name = body.get("name", "Unknown SKU")
    score = body.get("score", 0)
    commission = body.get("commission", "N/A")
    hook = body.get("hook_angle", "")
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return 200, {
        "status": "PRODUCT_ALERT_LOGGED",
        "product_name": name,
        "score": score,
        "commission": commission,
        "hook_angle": hook,
        "alert_message": f"🎯 [WINNING SKU] {name} (Score: {score}/100 | HH: {commission}) - Hook: {hook}",
        "processed_at": now_iso
    }


def process_analytics_sync(body: dict) -> tuple[int, dict]:
    views = int(body.get("views", 0) or 0)
    clicks = int(body.get("clicks", 0) or 0)
    orders = int(body.get("orders", 0) or 0)
    ctr = round((clicks / views) * 100, 2) if views > 0 else 0.0
    cvr = round((orders / clicks) * 100, 2) if clicks > 0 else 0.0
    if orders > 0 and ctr >= 1.5:
        decision = "KEEP_AND_SCALE"
    elif views >= 1000 and ctr < 0.8:
        decision = "ITERATE_HOOK_CTA"
    else:
        decision = "MONITOR"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return 200, {
        "status": "ANALYTICS_SYNCED",
        "job_id": body.get("job_id", 0),
        "metrics": {
            "views": views,
            "clicks": clicks,
            "orders": orders,
            "ctr_pct": ctr,
            "cvr_pct": cvr
        },
        "recommendation": decision,
        "processed_at": now_iso
    }


class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def _send_json(self, code: int, payload: dict):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path.startswith("/healthz") or self.path == "/":
            self._send_json(200, {
                "status": "ok",
                "engine": "n8n-local-webhook-hub-v2",
                "port": PORT,
                "active_webhooks": [
                    "/webhook/aff-video-publish",
                    "/webhook/aff-product-alert",
                    "/webhook/aff-analytics-sync"
                ]
            })
        else:
            self._send_json(404, {"error": f"Unknown GET endpoint: {self.path}"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw_body = self.rfile.read(length).decode("utf-8", errors="replace") if length > 0 else "{}"
        try:
            body = json.loads(raw_body)
            if isinstance(body, dict) and "body" in body and isinstance(body["body"], dict):
                body = body["body"]
        except Exception:
            body = {"raw": raw_body}

        clean_path = self.path.split("?")[0].rstrip("/")
        slug = clean_path.split("/")[-1]

        if slug == "aff-video-publish":
            code, resp = process_video_publish(body)
        elif slug == "aff-product-alert":
            code, resp = process_product_alert(body)
        elif slug == "aff-analytics-sync":
            code, resp = process_analytics_sync(body)
        else:
            code, resp = 200, {
                "status": "CUSTOM_WEBHOOK_RECEIVED",
                "webhook_slug": slug,
                "received": body
            }

        self._send_json(code, resp)


def run_server():
    server = HTTPServer(("127.0.0.1", PORT), WebhookHandler)
    print(f"n8n Local Webhook Hub v2 listening on http://localhost:{PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    run_server()
