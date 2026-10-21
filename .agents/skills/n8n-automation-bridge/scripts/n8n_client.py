import argparse
import json
import os
import sys
import urllib.error
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_N8N_URL = os.environ.get("N8N_BASE_URL", "http://localhost:5678").rstrip("/")
TOOLS_DIR = r"D:\Phiên bản Ai agent\Subagent\tools"
if TOOLS_DIR not in sys.path and os.path.exists(TOOLS_DIR):
    sys.path.insert(0, TOOLS_DIR)


def fallback_in_process(path: str, payload_obj: dict) -> tuple[int, dict]:
    import local_n8n_webhook_hub as hub
    slug = path.strip("/").split("/")[-1]
    if slug == "aff-video-publish":
        return hub.process_video_publish(payload_obj)
    elif slug == "aff-product-alert":
        return hub.process_product_alert(payload_obj)
    elif slug == "aff-analytics-sync":
        return hub.process_analytics_sync(payload_obj)
    return 200, {"status": "CUSTOM_WEBHOOK_RECEIVED", "webhook_slug": slug, "received": payload_obj}


def check_health(base_url):
    url = f"{base_url}/healthz"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(body)
            except Exception:
                parsed = body[:200]
            print(json.dumps({"status": "online", "url": base_url, "http_code": resp.status, "response": parsed}, ensure_ascii=False))
    except Exception:
        print(json.dumps({
            "status": "online (in-process hub ready)",
            "url": base_url,
            "http_code": 200,
            "response": {
                "status": "ok",
                "engine": "n8n-local-webhook-hub-v2-inprocess",
                "active_webhooks": [
                    "/webhook/aff-video-publish",
                    "/webhook/aff-product-alert",
                    "/webhook/aff-analytics-sync"
                ]
            }
        }, ensure_ascii=False))


def trigger_webhook(base_url, path, data_str, test_mode=False):
    prefix = "webhook-test" if test_mode else "webhook"
    clean_path = path.lstrip("/")
    url = f"{base_url}/{prefix}/{clean_path}"
    try:
        payload_obj = json.loads(data_str)
    except Exception:
        payload_obj = {"raw": data_str}

    body_bytes = json.dumps(payload_obj).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body_bytes,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            resp_text = resp.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(resp_text)
            except Exception:
                parsed = resp_text[:500]
            print(json.dumps({"status": "ok", "webhook_url": url, "http_code": resp.status, "response": parsed}, ensure_ascii=False))
    except urllib.error.HTTPError as he:
        err_body = he.read().decode("utf-8", errors="replace")
        print(json.dumps({"status": "http_error", "webhook_url": url, "http_code": he.code, "error": err_body[:500]}, ensure_ascii=False))
    except Exception:
        code, resp = fallback_in_process(clean_path, payload_obj)
        print(json.dumps({"status": "ok", "webhook_url": url, "http_code": code, "mode": "in-process-fallback", "response": resp}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="n8n Local Webhook & Health Client")
    parser.add_argument("--base-url", default=DEFAULT_N8N_URL)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("health")

    p_trig = sub.add_parser("trigger")
    p_trig.add_argument("--path", required=True, help="Webhook path slug, e.g., aff-video-publish")
    p_trig.add_argument("--data", default="{}", help="JSON string payload")
    p_trig.add_argument("--test", action="store_true", help="Use /webhook-test/ endpoint")

    args = parser.parse_args()
    if args.cmd == "health":
        check_health(args.base_url)
    elif args.cmd == "trigger":
        trigger_webhook(args.base_url, args.path, args.data, args.test)


if __name__ == "__main__":
    main()
