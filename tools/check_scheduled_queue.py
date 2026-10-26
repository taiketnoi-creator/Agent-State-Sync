import datetime
import json
import requests
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

v = json.load(open(r"C:\Users\guicci\.codex\mcp\facebook-mcp-server\pages_vault.json", encoding="utf-8"))
token = next(p["access_token"] for p in v["pages"] if p["id"] == "1022527194267367")

r = requests.get(
    f"https://graph.facebook.com/v22.0/1022527194267367/scheduled_posts?fields=id,scheduled_publish_time,message,attachments{{media_type}}&limit=100&access_token={token}"
).json()
items = r.get("data", [])
print(f"Total scheduled posts remaining: {len(items)}")
items.sort(key=lambda x: x.get("scheduled_publish_time", 0))
for p in items:
    ts = p.get("scheduled_publish_time", 0)
    dt_str = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    mtype = p.get("attachments", {}).get("data", [{}])[0].get("media_type", "unknown")
    msg = (p.get("message") or "").replace("\n", " ")[:65]
    print(f"{dt_str} [{mtype:5s}] {p.get('id')}: {msg}")
