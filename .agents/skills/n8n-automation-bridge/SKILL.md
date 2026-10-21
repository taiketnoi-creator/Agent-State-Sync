---
name: n8n-automation-bridge
description: >-
  Use this skill when triggering n8n workflows via webhooks, publishing AI videos to social platforms (TikTok, Reels, Shorts, Facebook), syncing affiliate links, or checking n8n status.
---

# Cầu Nối Tự Động Hóa n8n (Zero-Token Event & Distribution Hub)

Skill này kết nối hệ thống Subagent với **n8n (Docker Local)** để đẩy toàn bộ các tác vụ lặp đi lặp lại (đăng bài đa kênh, rút gọn link Affiliate, thông báo Telegram/Zalo, đồng bộ Google Sheets) sang n8n xử lý với **0 token**.

## 1. Các Luồng Webhook Chuẩn Trên n8n

Mặc định n8n chạy tại `http://localhost:5678` (có thể cấu hình qua biến môi trường `N8N_BASE_URL`). Hệ thống sử dụng 3 endpoint webhook chính:

1. **`/webhook/aff-video-publish`**:
   - Nhận thông tin video thành phẩm (`video_path`, `caption`, `hashtags`, `aff_url`, `platforms`) để tự động lên lịch/đăng lên TikTok, YouTube Shorts, Instagram Reels, Facebook Reels.
2. **`/webhook/aff-product-alert`**:
   - Gửi thông báo sản phẩm Winning hoặc báo cáo trạng thái chiến dịch về Telegram / Zalo / Google Sheets.
3. **`/webhook/aff-analytics-sync`**:
   - Thu thập lượt xem, lượt click link Affiliate và doanh thu chuyển đổi để cập nhật ngược về bảng `products` và `video_jobs` trong SQLite.

## 2. Cách Kích Hoạt Từ Subagent

### Cách 1: Gọi trực tiếp qua MCP Tool (`aff-n8n-sqlite`)
Gọi công cụ `n8n_trigger_webhook` với các tham số:
- `webhook_path`: `"aff-video-publish"`
- `payload_json`: Chuỗi JSON chứa dữ liệu cần gửi.

### Cách 2: Gọi qua Script CLI (`n8n_client.py`)

```powershell
# Kiểm tra kết nối n8n local
& "C:\Users\guicci\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\python.exe" ".agents/skills/n8n-automation-bridge/scripts/n8n_client.py" health

# Kích hoạt webhook đăng video & đồng bộ link Affiliate
& "C:\Users\guicci\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\python.exe" ".agents/skills/n8n-automation-bridge/scripts/n8n_client.py" trigger --path "aff-video-publish" --data "{\"job_id\": 1, \"video_path\": \"output/videos/sample.mp4\", \"platforms\": [\"tiktok\", \"reels\", \"shorts\"]}"
```
