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
print(f"Total scheduled posts currently on Page: {len(items)}")

deleted_count = 0
for p in items:
    pid = p.get("id")
    mtype = p.get("attachments", {}).get("data", [{}])[0].get("media_type", "unknown")
    # Only keep video reels!
    if mtype == "video":
        print(f"🎬 GIỮ LẠI Video Reel Remotion Chuẩn Vàng: {pid}")
    else:
        # Delete photo posts
        del_res = requests.delete(f"https://graph.facebook.com/v22.0/{pid}?access_token={token}").json()
        print(f"🗑️ ĐÃ XÓA bài ảnh Pillow vô hồn {pid}: {del_res}")
        deleted_count += 1

print(f"\n🎉 Đã dọn dẹp sạch toàn bộ {deleted_count} bài ảnh vô hồn khỏi hàng đợi Meta!")
