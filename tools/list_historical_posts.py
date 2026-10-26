import json
import requests
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

v = json.load(open(r"C:\Users\guicci\.codex\mcp\facebook-mcp-server\pages_vault.json", encoding="utf-8"))
token = next(p["access_token"] for p in v["pages"] if p["id"] == "1022527194267367")

r = requests.get(
    f"https://graph.facebook.com/v22.0/1022527194267367/posts?fields=id,created_time,message&limit=100&access_token={token}"
).json()
items = r.get("data", [])
print(f"Total historical posts: {len(items)}")
for i, p in enumerate(items):
    dt = p.get("created_time", "")[:10]
    msg = (p.get("message") or "").replace("\n", " ")[:70]
    print(f"{i+1:2d}. [{dt}] {p.get('id')}: {msg}")
