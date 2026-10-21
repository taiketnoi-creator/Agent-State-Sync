# Nhật Ký Thay Đổi & Nâng Cấp Phần Mềm / Ứng Dụng (Software & System Changelog)

> **Mục đích:** Ghi lại mọi thay đổi, cài đặt mới hoặc nâng cấp về phần mềm, công cụ CLI, MCP Server, cấu trúc Database, n8n Workflows và bộ Skills. Khi chuyển sang máy khác, nhìn vào bảng này sẽ biết ngay máy mới cần cập nhật thêm công cụ hay cấu hình nào để đồng bộ 100% với máy chính.

---

## [1.6.0] — 2026-10-21: Hệ Thống Tự Động Hóa Link & Đối Soát Shopee Affiliate Cá Nhân (`shopee_link_manager.py`) & Cẩm Nang Đa Kênh 2026

### 1. Công Cụ Tự Động Lấy Link, Quản Lý Kho SKU & Đối Soát Chuyển Đổi Shopee Affiliate (`tools/shopee_link_manager.py`)
- **Giải mã & Khóa cứng `SHOPEE_AFFILIATE_ID = 17395830088`:** Tự động bóc tách mã Publisher ID cá nhân từ 1 link rút gọn mẫu (`https://s.shopee.vn/6q1eCGjYkW`) và tạo link qua cổng Universal Redirect chính thức của Shopee (`https://s.shopee.vn/an_redir?origin_link=...&affiliate_id=17395830088&sub_id=...`).
- **Mở rộng SQLite `aff_system.db`:** Thêm 2 bảng mới `shopee_page_links` (lưu ma trận link 5 tầng `Sub_ID` cho 3 Page Bán Hàng: `ktx`, `deadline`, `phongtro`) và `shopee_conversions` (nhập và phân tích báo cáo CSV từ `affiliate.shopee.vn`).
- **Tự động nâng cấp Pinned Comment trên Facebook (`--upgrade-live-fb-comments`):** Quét và cập nhật trực tiếp toàn bộ 6/6 Pinned Comment đang chạy trên 3 Fanpage Bán Hàng sang link Affiliate chính chủ gắn `Sub_ID` riêng.
- **Xuất Batch CSV (`campaigns/shopee-links/shopee_custom_link_batch.csv`):** Tương thích 100% với công cụ *Chuyển đổi link hàng loạt* trên `affiliate.shopee.vn/offer/custom_link`.

### 2. Cẩm Nang Đa Kênh AI Affiliate 2026 (`FB Reels` + `YouTube Shorts/Shopping` + `Threads`)
- Lưu trữ tại `campaigns/2026-10-21/multi-channel-ai-affiliate-research/` (`01-fb-reels-ai-video-archetypes.md` & `02-youtube-shorts-and-threads-playbook.md`) và Bộ Não Thứ 2 (`MEM-20261021-multi-channel-ai-affiliate-playbook.md`).

---

## [1.5.0] — 2026-10-21: Bộ Công Cụ Tự Động Hóa Video AI Bán Hàng Số Lượng Lớn (SLL) Đa Sản Phẩm (`veo_step4_auto.py` & `build_step4_step5_auto.py`)

### 1. Quy Chuẩn Vàng & Prompt Google Flow v2 Cho Video AI Bán Hàng SLL (`Sandwich A-Roll ↔ B-Roll 8 Nhịp`)
- **`knowledge/quy-chuan-video-ai-ban-hang-sll.md` & `MEM-20261020-video-ai-ban-hang-sll-playbook.md`:**
  - Chuẩn hóa cấu trúc 8 nhịp đan xen `A-Roll (MC) ↔ B-Roll (Cận cảnh sản phẩm/kết quả)` giúp chống nhàm chán và áp dụng linh hoạt cho mọi ngành hàng (Gia dụng, Điện tử, Mỹ phẩm, Thời trang, Sức khỏe).
  - Khắc phục triệt để 4 lỗi AI thường gặp: Cấm AI vẽ chữ tiếng Việt lên nút bấm/poster cuối; khóa cứng `Rigid product geometry` chống biến dạng sản phẩm; dùng 1 trục Voiceover liền mạch chống khoảng lặng chết; tự động đè 3 lớp PNG trong suốt (`CHÚ Ý!`, `Logo góc phải`, `Khiên Vàng Bảo Hành 3D`) + phụ đề `.ass` 1 dòng chuẩn Brand-Kit (`#87FF00` & Trắng).
- **`FLOW_BUILD_PROMPT.md` (`PROMPT 6`):**
  - Bổ sung Prompt nâng cấp ứng dụng Google Flow lên cấu trúc 8 nhịp `A-Roll + B-Roll` và thêm nút xuất `Raw Scenes Pack (SLL)` để trộn hàng loạt bằng FFmpeg.

### 2. Công Cụ Tự Động Hóa Bước 4 & Bước 5 Không Cần Đụng Tay (`tools/veo_step4_auto.py` & `build_step4_step5_auto.py`)
- **`tools/veo_step4_auto.py`:** Tự động gửi 8 ảnh Keyframe `9:16` kèm Prompt chuyển động vào Google Veo API (`veo-2.0-generate-001` / `veo-3.0-generate-preview`) khi có `GEMINI_API_KEY`, hoặc tự động fallback sang trình dựng chuyển động FFmpeg 30fps local.
- **`campaigns/2026-10-21/quat-cam-tay-imi-5000mah/build_step4_step5_auto.py`:**
  - Tự động vẽ 3 lớp đồ họa PNG trong suốt `1080×1920` bằng `.NET System.Drawing` (không cần cài thư viện ngoài).
  - Tự động render 8 clip chuyển động `raw_scenes/scene_01..08.mp4` khớp từng phần trăm giây với `voiceover_v1.mp3`.
  - Tự động đóng gói video thương mại hoàn chỉnh `outputs/quat_cam_tay_imi_v1_commercial.mp4` (`39.89s`, `1080×1920 @ 30fps`) gồm: Sticker `CHÚ Ý!` + Logo `iMI • 120 SPEED` + Khiên `CHÍNH HÃNG iMI - PIN TRÂU 5000mAh - BẢO HÀNH UY TÍN` + Phụ đề `.ass` 1 dòng + Voiceover + Nhạc nền `-18dB` + SFX.

---

## [1.4.0] — 2026-10-21: Tự Động Dọn Kho Hình Ảnh & Video Local Sau 7 Ngày (`cleanup_old_media.py`) & Xuất Bản Ảnh Local (`fb_publish_image_post.py`)

### 1. Công Cụ Tự Động Dọn Kho Media Local Quá Hạn 7 Ngày (`tools/cleanup_old_media.py` & `tools/run_cleanup_7d.bat`)
- **Mục tiêu:** Tự động xóa toàn bộ hình ảnh (`.jpg`, `.png`, `.webp`), video (`.mp4`, `.mov`), âm thanh (`.mp3`, `.wav`) và thư mục build tạm (`remotion/`, `images/`, `assets/`, `qa-frames/`, `out/`, `node_modules/`) trong `campaigns/<YYYY-MM-DD>/` và `templates/remotion-cuongit-template/out/` khi đã quá **7 ngày** (`--days 7`), giữ cho ổ cứng local luôn nhẹ và sạch.
- **Bảo vệ an toàn tuyệt đối:**
  - Giữ lại các file nhật ký `.md` siêu nhẹ (vài KB) trong `campaigns/<YYYY-MM-DD>/` để bảo toàn lịch sử Post ID và kịch bản.
  - Không bao giờ chạm tới thư mục tài nguyên gốc `assets/` (chứa mẫu chuẩn `ai-players-image-styles/` và `sales-pages-image-styles/`), `brand-kit/`, `knowledge/`, `training/`, `tools/` và `aff_system.db`.
- **Kích hoạt 3 lớp lịch tự động:**
  1. **Hook Khởi Động Phiên (`tools/mama_boot_check.py`):** Tự động quét và dọn media quá hạn > 7 ngày mỗi khi mở Antigravity và hiển thị dung lượng kho `campaigns/` ngay trong bảng Báo Cáo Khởi Động Phiên.
  2. **Windows Task Scheduler (`AgentJavis_MediaCleanup_7Days`):** Chạy ngầm hàng ngày lúc `09:00 AM` (kèm cờ `StartWhenAvailable` tự chạy bù ngay khi bật máy).
  3. **Antigravity Standing Cron (`0 9 * * *`):** Chạy định kỳ mỗi ngày khi Antigravity đang mở.

### 2. Công Cụ Đăng Bài Ảnh Local & Bình Luận Đầu Tiên (`tools/fb_publish_image_post.py`)
- Upload trực tiếp ảnh `.jpg`/`.png` từ ổ cứng lên Facebook Graph API (`/{page_id}/photos`) cho bất kỳ Fanpage nào trong `pages_vault.json` và tự động ghim ngay `Pinned Comment #1` chứa link tài liệu/sản phẩm (`/{post_id}/comments`) với chi phí **0 token**.

---

## [1.3.0] — 2026-10-20: Tích Hợp Skill `social-media-research` & Nâng Cấp `ffmpeg_render.py` (Batch Storyboard Mixing)

### 1. Bộ Kỹ Năng Nghiên Cứu MXH Mới (`.agents/skills/social-media-research/`)
- Kế thừa và Việt hóa từ `ScrapeCreators/social-media-research-skills` với 4 quy trình chuẩn cho `mkt`, `content`, và `cham-soc-kenh`:
  - **Outlier Post Finder:** Chấm điểm độ bứt phá (`view_lift`, `engagement_lift`) so với trung vị (`median`) của kênh.
  - **Comment Mining:** Phân loại bình luận thực tế tiếng Việt/Anh vào 6 nhóm VoC (`buying_intent`, `objections`, `pain_points`, `questions`, `praise`, `other`).
  - **Transcript Intelligence:** Tự động tách lời thoại video thành 4 nhịp (`00-03s Hook`, `03-10s Pain`, `10-23s Demo Proof`, `23-30s CTA`) và kiểm tra Hard Gate (`<= 85 từ`, không chào hỏi 3s đầu).
  - **Script Local 0-Token:** `.agents/skills/social-media-research/scripts/social_research_analyzer.py`.

### 2. Nâng Cấp Trình Dựng Video FFmpeg (`.agents/skills/ai-video-factory/scripts/ffmpeg_render.py`)
- Tích hợp cơ chế **Folder-Level Storyboard Batch Mixing** từ `YILS-LIN/short-video-factory` (`--scenes-dir` + `--batch-count`).
- Nối mượt nhiều clip/ảnh phân cảnh bằng `filter_complex` (`concat=n=N:v=1:a=0`), tự động đo thời lượng giọng đọc qua `ffprobe`, trộn âm thanh chuẩn phòng thu (Voiceover `-3dB`, BGM `-18dB`) và đóng cứng phụ đề `.srt`.

---

## [1.2.0] — 2026-10-19: Nâng Cấp Hệ Thống Webhook n8n v2 & Local Zero-Token Webhook Hub (`localhost:5678`)

### 1. Nâng Cấp Workflow Đa Kênh `aff_video_autopost_workflow.json` (v2)
- **Tích hợp đủ 3 luồng Webhook chuẩn:** `/webhook/aff-video-publish`, `/webhook/aff-product-alert`, và `/webhook/aff-analytics-sync`.
- **Khóa cứng quy chuẩn Brand Guidelines 4.3:**
  - **Facebook Reels:** Tự động lọc bỏ link thô khỏi caption (chống bóp tương tác), gắn câu điều hướng *"👉 Link sản phẩm tui ghim ở bình luận đầu tiên nha!"* và sinh riêng `pinned_comment_with_link` chứa mã đo lường `?utm_source=fb_reels&utm_medium=pinned_comment&utm_campaign=job_<id>`.
  - **YouTube Shorts:** Tự động cắt tiêu đề `< 60 ký tự` kèm 3 hashtag chuẩn (`#Shorts #TienIch #Review`) và đưa link UTM vào phần mô tả.
  - **Khung giờ vàng:** Tự động gán lịch `11:45` hoặc `20:00` và kiểm tra trạng thái `approval_gate` (`DRAFT_ONLY` mặc định).

### 2. Bổ Sung `tools/local_n8n_webhook_hub.py` & Cơ Chế Tự Phục Hồi (Zero-Fail Fallback)
- **`tools/local_n8n_webhook_hub.py`:** Daemon HTTP siêu nhẹ chạy trực tiếp trên Python 3.11 tại `http://localhost:5678` (không cần bật Docker Desktop nặng máy), xử lý tức thì cả 3 cổng Webhook và xuất gói manifest ra `output/publish_queue/job_<id>_publish_pack.json`.
- **Tự khởi động & In-process Fallback:** Nâng cấp `aff_n8n_sqlite_mcp.py` (v1.1.0) và `n8n_client.py` tự động xử lý in-process nếu cổng `5678` chưa bật sau khi khởi động lại máy, đảm bảo không bao giờ lỗi `WinError 10061`.

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
