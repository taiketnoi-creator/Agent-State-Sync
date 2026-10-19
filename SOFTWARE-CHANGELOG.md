# Nhật Ký Thay Đổi & Nâng Cấp Phần Mềm / Ứng Dụng (Software & System Changelog)

> **Mục đích:** Ghi lại mọi thay đổi, cài đặt mới hoặc nâng cấp về phần mềm, công cụ CLI, MCP Server, cấu trúc Database, n8n Workflows và bộ Skills. Khi chuyển sang máy khác, nhìn vào bảng này sẽ biết ngay máy mới cần cập nhật thêm công cụ hay cấu hình nào để đồng bộ 100% với máy chính.

---

## [1.1.0] — 2026-10-19: Hoàn Thiện Đào Tạo 10 Agent (≥ 9.2/10), Tích Hợp MCP Trực Tiếp & Bộ 3 Công Cụ Python 0-Token

### 1. Bộ 3 Công Cụ Tự Động Hóa Local 0-Token Mới (`D:\Phiên bản Ai agent\Subagent\tools\`)
- **`tools/validate_script_linter.py`:** Tự động kiểm tra kịch bản của `content` (đếm từ ≤ 85 từ cho video 30s, phát hiện câu chào bị cấm trong 3s đầu, kiểm tra đủ 4 nhịp `Hook → Pain → Demo → CTA`).
- **`tools/generate_voice_tts.py`:** Kết nối `edge-tts` tạo file `.mp3` giọng đọc tiếng Việt (`vi-VN-HoaiMyNeural` / `vi-VN-NamMinhNeural`, tốc độ `+12%` tương đương `1.12x`), tự động lọc bỏ ký hiệu đánh dấu nhịp đọc `[ ... ]`.
- **`tools/calculate_affiliate_funnel.py`:** Tự động tính chỉ số phễu 3 lớp (Hook 3s, Hold 50%, CTR, CVR, RPM) từ CLI hoặc SQLite `aff_system.db` và xuất chẩn đoán `KEEP / ITERATE / STOP` kèm `Actionable Next Step`.

### 2. Đồng Bộ Hóa Giáo Trình & Hồ Sơ 10 Agent
- **`training/CURRICULUM.md`:** Khởi tạo lộ trình đào tạo tổng 4 tầng cho toàn đội `Agent-Javis`.
- **`training/bo-nao-thu-2/`:** Bổ sung trọn bộ 5 bài huấn luyện (`01-brand-ingestion.md` -> `05-retest.md`) và nâng cấp `bo-nao-thu-2.md` (Rubric 10 điểm + Few-shot thực tế).
- **Cập nhật 10 file `.md` gốc & `knowledge/quick-task-facebook-page-publish-comment.md`:** Chuẩn hóa Frontmatter (`inherit` cho nhóm Sáng tạo, `flash` cho nhóm Hậu cần) và gắn trực tiếp cú pháp gọi MCP (`aff-n8n-sqlite` & `facebook-page`), loại bỏ hoàn toàn quy trình Windsor.ai cũ.

---

## [1.0.0] — 2026-10-19: Nâng Cấp Lên Kiến Trúc Gemini 4 + MCP (SQLite & n8n) + Đồng Bộ Siêu Nhẹ

### 1. Nâng Cấp Hệ Thống Điều Phối & AI Runtime
- **Model vận hành chính:** Chuyển sang sử dụng **Gemini 4** trên Antigravity (thay thế cấu hình model cũ trong frontmatter Codex và không dùng Ollama).
- **Cấu hình `.agents/GEMINI.md`:** Bổ sung tại `D:\Phiên bản Ai agent\Subagent\.agents\GEMINI.md` và `C:\Users\guicci\.gemini\antigravity\scratch\ai-aff-video-system\.agents\GEMINI.md` với cơ chế *Context Firewall* (giảm 80–90% token mỗi lượt).
- **Lifecycle Hooks (`hooks.json`):**
  - Thêm hook `SessionStart` (`session_start.py`) tự động đọc thống kê nhanh từ SQLite.
  - Thêm hook `PreToolUse` (`pre_command_guard.py`) chặn các lệnh xóa/format nguy hiểm.

### 2. Bổ Sung & Nâng Cấp MCP Servers (`~/.gemini/config/mcp_config.json`)
- **MỚI — `aff-n8n-sqlite` (`aff_n8n_sqlite_mcp.py`):**
  - Chạy trên Python 3.11 (`uv` managed Python) với cờ `PYTHONUTF8=1`.
  - Tự động khởi tạo SQLite `data/aff_system.db` với 4 bảng: `products`, `brand_personas`, `video_jobs`, `n8n_logs`.
  - Cung cấp 5 công cụ MCP: `system_dashboard_summary`, `sqlite_query`, `aff_upsert_product`, `aff_save_video_job`, `n8n_trigger_webhook`.
- **TÍCH HỢP — `facebook-page` (`facebook-mcp-server`):**
  - Kết nối server MCP từ `C:\Users\<user>\.codex\mcp\facebook-mcp-server\server.py` (Python 3.12 venv) vào cấu hình MCP chung của Antigravity.

### 3. Nâng Cấp Bộ Skills (`D:\Phiên bản Ai agent\Subagent\.agents\skills\`)
- **`ai-affiliate-page-operator`**: Đồng bộ từ `.codex/skills/` sang `.agents/skills/` để Antigravity tự động nhận diện.
- **`product-video-editor`**: Đóng gói chuẩn hóa vào `.agents/skills/product-video-editor/`.
- **MỚI — `ai-video-factory`**: Thêm quy tắc đồng nhất nhân vật (`brand_persona.json`) và script `ffmpeg_render.py` dựng video dọc `9:16` (`1080x1920`) bằng FFmpeg local tốn 0 token.
- **MỚI — `n8n-automation-bridge`**: Thêm script `n8n_client.py` kiểm tra health/kích hoạt Webhook n8n và file mẫu `aff_video_autopost_workflow.json`.

### 4. Phiên Bản Phần Mềm & Công Cụ Local Chuẩn Đã Xác Minh
| Phần mềm / Công cụ | Phiên bản / Đường dẫn chuẩn | Ghi chú khi cài trên máy khác |
| :--- | :--- | :--- |
| **FFmpeg** | `9.0.2-full_build` | Dùng cho `product-video-editor` và `ffmpeg_render.py` |
| **Python (uv)** | `cpython-3.11.15` (`~\AppData\Roaming\uv\python\...`) | Chạy MCP `aff-n8n-sqlite`, Hooks và CLI scripts |
| **Python (FB MCP venv)** | `Python 3.12.14` (`~\.codex\mcp\facebook-mcp-server\.venv`) | Chạy `facebook-page` MCP server |
| **Git** | `C:\Program Files\Git\cmd\git.exe` | Đồng bộ repo siêu nhẹ `Agent-State-Sync` |
| **Docker / n8n** | Localhost Port `5678` (`http://localhost:5678`) | Nhận Webhook từ Subagent `quan-ly-kenh` / `n8n-ops` |

---

## Lịch Sử Trước Đây (Kế thừa từ `D:\Phiên bản Ai agent\Subagent\CHANGELOG.md`)
- **[0.12.0] (2026-10-12):** Chuẩn hóa visual system slide-tech (cobalt, lime neon, trắng) và font Be Vietnam Pro.
- **[0.9.0] – [0.11.0] (2026-10-12):** Đào tạo `edit` theo chuẩn Remotion JSON, TTS và Page Brief 30 ngày cho `AI Players`.
- **[0.6.0] – [0.8.0] (2026-10-12):** Bổ sung curriculum `training/ai-affiliate-video-practice.md` và `training/facebook-page-launch.md`.
- **[0.5.0] (2026-10-12):** Bổ sung subagent `bo-nao-thu-2` và kho ký ức `knowledge/bo-nao-thu-2/`.
- **[0.1.0] – [0.4.0] (2026-10-08 -> 2026-10-10):** Khởi tạo đội Subagent `mama`, `mkt`, `content`, `edit`, `voice`, `content-da-kenh`, `quan-ly-kenh`, `cham-soc-kenh`, `hieu-suat`.
