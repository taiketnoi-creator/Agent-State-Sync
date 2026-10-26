# Lịch Sử Công Việc & Bàn Giao Trò Chuyện Dự Án (Work & Conversation History)

> **Quy tắc cập nhật:** Cuối mỗi phiên làm việc quan trọng, ghi lại tóm tắt ngắn gọn theo cấu trúc: **Bối cảnh & Quyết định của CEO -> Các hạng mục đã hoàn thành -> Trạng thái các mục tiêu (`OPEN` / `IN_PROGRESS` / `DONE`) -> Việc cần làm ngay ở phiên tiếp theo**. Nhờ đó, khi chuyển sang máy khác, AI đọc file này là hiểu ngay mạch trò chuyện trước đó mà không cần đồng bộ dữ liệu nặng.

---

## Phiên Làm Việc: 2026-10-19 — Chuyển Đổi Kiến Trúc Tối Ưu Token & Đồng Bộ Siêu Nhẹ Trên Gemini 4

### 1. Tóm Tắt Nội Dung Trò Chuyện & Quyết Định Của CEO
- **Mục tiêu cốt lõi:** Áp dụng hệ thống tự động hóa Subagent vào mảng **Xây dựng hệ thống bán hàng Affiliate** và **Làm Video AI xây dựng thương hiệu & bán hàng**.
- **Quyết định công nghệ & hạ tầng:**
  - Sử dụng hoàn toàn **Gemini 4** để điều phối và vận hành hệ thống Subagent (không sử dụng Ollama local).
  - Kết hợp **Docker / n8n** đã cài sẵn trên máy Windows cùng **FFmpeg**, **SQLite** và **Skills** để xử lý các tác vụ lặp lại với chi phí **0 token**.
  - Tích hợp toàn bộ đội 10 Subagent hiện có từ Codex tại `Subagent` (**Đội Agent Javis**) sang vận hành trực tiếp trên Antigravity (Gemini 4).
  - **Thay đổi chiến lược đồng bộ GitHub:** Tách một Repo mới siêu nhẹ (`Agent-State-Sync`) chỉ lưu **Lịch sử công việc/trò chuyện**, **Nhật ký thay đổi/nâng cấp phần mềm**, và **File cấu trúc tổng quan (`PROJECT-BLUEPRINT.md`)**. Không đẩy database, video hay thư viện nặng lên GitHub vì các máy đều đã cài sẵn cơ sở dữ liệu ở local.

### 2. Những Việc Đã Hoàn Thành Trong Phiên (`DONE`)
- [x] Thiết kế kiến trúc **"Hybrid Zero-Waste"** giúp giảm 70–90% lượng token tiêu thụ khi chạy Subagent (dùng Subagent làm *Context Firewall*, chỉ trả báo cáo tóm tắt 5–15 dòng, lưu dữ liệu chi tiết xuống SQLite và file local).
- [x] Xây dựng MCP Server cục bộ `aff-n8n-sqlite` (`aff_n8n_sqlite_mcp.py`) kết nối trực tiếp **SQLite (`aff_system.db`)** và **Webhook n8n (`http://localhost:5678`)**, cấu hình chuẩn UTF-8 tiếng Việt trên Windows.
- [x] Kết nối tích hợp thêm `facebook-page` MCP Server (`~/.codex/mcp/facebook-mcp-server/server.py`) vào `~/.gemini/config/mcp_config.json`.
- [x] Kích hoạt cấu hình `.agents/GEMINI.md` và gắn đủ 4 bộ Skills (`ai-affiliate-page-operator`, `product-video-editor`, `ai-video-factory`, `n8n-automation-bridge`) vào `Subagent/.agents/skills/`.
- [x] Định nghĩa đầy đủ 9 Subagent chuyên biệt của đội `Agent-Javis` (`mkt`, `content`, `edit`, `voice`, `content-da-kenh`, `quan-ly-kenh`, `cham-soc-kenh`, `hieu-suat`, `bo-nao-thu-2`) dưới sự điều phối của `mama` (Gemini 4).
- [x] Nâng cấp cơ chế **Smart Model Tiering & Batch Execution** trong `.agents/GEMINI.md` theo phê duyệt của CEO: giữ `mama`, `mkt`, `content`, `edit` chạy `inherit` (Gemini 4) và chuyển 6 Subagent hậu cần (`voice`, `content-da-kenh`, `quan-ly-kenh`, `cham-soc-kenh`, `hieu-suat`, `bo-nao-thu-2`) sang `flash` kèm gộp lệnh song song để tiết kiệm tối đa Quota Gemini 4.
- [x] Kiểm toán toàn diện 10 Agent và hoàn tất **4 nâng cấp đồng bộ đưa toàn đội lên chuẩn ≥ 9.2/10**:
  1. Cập nhật Frontmatter (`inherit` / `flash`) và tích hợp quy trình gọi trực tiếp MCP (`aff-n8n-sqlite`, `facebook-page`) vào cả 10 file `.md` gốc; viết lại `knowledge/quick-task-facebook-page-publish-comment.md` chuẩn MCP 100%.
  2. Xây dựng trọn bộ 5 bài đào tạo cho `training/bo-nao-thu-2/` (`01-brand-ingestion.md` -> `05-retest.md`), bổ sung Rubric 10 điểm & Few-shot vào `bo-nao-thu-2.md`, và khởi tạo lộ trình tổng `training/CURRICULUM.md`.
  3. Lập trình và kiểm thử 3 công cụ tự động 0-token trong `tools/`: `validate_script_linter.py` (đếm từ ≤85, chặn câu chào 3s đầu), `generate_voice_tts.py` (xuất `.mp3` tiếng Việt tốc độ 1.12x qua `edge-tts`), `calculate_affiliate_funnel.py` (tính phễu 3 lớp & xuất quyết định `KEEP/ITERATE/STOP`).
- [x] Trang bị cơ chế **Báo Cáo Khởi Động Phiên Tự Động Đa Máy (`tools/mama_boot_check.py` & Hook `SessionStart`)**: Tự động pull trạng thái mới nhất từ GitHub, tính `%` tiến độ mục tiêu và kiểm tra kết nối trực tiếp Facebook Page, n8n, SQLite, FFmpeg/Edge-TTS ngay khi bắt đầu chat ở bất kỳ máy nào.
- [x] Khởi tạo Repo đồng bộ siêu nhẹ tại `Agent-State-Sync` và kết nối remote GitHub `https://github.com/taiketnoi-creator/Agent-State-Sync.git` kèm cơ chế tự động đồng bộ hai chiều sau mỗi lượt trò chuyện (`on_stop_sync.py` & `generate_snapshot.py`).

### 3. Chỉ Mục Tri Thức Hiện Có Từ Bộ Não Thứ 2 (`VALIDATED`)
*(Tham chiếu tại `knowledge/bo-nao-thu-2/INDEX.md`)*
- `MEM-20261012-page-network-pilot`: Mạng lưới 20 Page AI Affiliate và thứ tự pilot.
- `MEM-20261012-short-video-script-playbook`: Playbook kịch bản video ngắn có giá trị thực.
- `MEM-20261012-niche-product-research`: Phương pháp nghiên cứu niche và SKU AI Affiliate.
- `MEM-20261013-facebook-page-community-nurture`: Community nurture cho Facebook Page mới.
- `MEM-20261013-video-slide-composition-lessons`: Bài học thực chiến về bố cục và mật độ hình ảnh cho video slide.
- `MEM-20261014-ai-page-comment-hook-playbook`: Playbook 2 bài/ngày kéo bình luận cho Page AI.
- `MEM-20261020-remotion-brandkit-golden-rules`: Bộ 5 Quy Tắc Vàng dựng Video Remotion Brand-Kit (`#87ff00`, kính trong suốt, motion liên tục, sub trượt 1 dòng không khung).
- `MEM-20261020-video-ai-ban-hang-sll-playbook`: Quy chuẩn giải phẫu & nhân bản Video AI Bán Hàng SLL đa sản phẩm (Sandwich `A-Roll ↔ B-Roll` 8 nhịp + Google Flow + FFmpeg/Remotion).

### 4. Trạng Thái Các Hạng Mục Tiếp Theo (`OPEN` / `IN_PROGRESS` / `DONE`)
- `[DONE]` Kết nối remote URL GitHub (`https://github.com/taiketnoi-creator/Agent-State-Sync.git`) cho thư mục `Agent-State-Sync` và đẩy bản đồng bộ siêu nhẹ lên GitHub.
- `[DONE]` Nâng cấp workflow `aff_video_autopost_workflow.json` lên v2 (chuẩn Brand Guidelines: FB Reels không chèn link caption + Pinned Comment gắn UTM, YT Shorts < 60 ký tự, giờ vàng 11h45/20h00), kích hoạt `local_n8n_webhook_hub.py` trên `http://localhost:5678` và kiểm tra kết nối thực tế cả 3 cổng Webhook (`aff-video-publish`, `aff-product-alert`, `aff-analytics-sync`) đạt `HTTP 200 OK`.
- `[DONE]` Tinh gọn Subagent `edit`: Xóa bỏ Nhóm 3 (`REAL-01..05` & `product-video-editor`) và Nhóm 4 (`07-ai-channel-ip-system.md` & `08-no-people-visual-style.md` không phục vụ bán hàng); kích hoạt `node` v24.13.0, `pnpm` 11.0.8 và cài đặt đầy đủ `node_modules` Remotion 4.0 cho 2 định dạng video chủ lực (**Video AI Bán Hàng** & **Video Slide**).
- `[DONE]` Kết nối thành công **5 Fanpage Facebook** (`Ký Túc Xá Có Biến`, `Hội Deadline`, `Phòng Trọ Hết Cứu`, `AI Players - Người chơi hệ AI`, `IFN`) vào kho bảo mật `pages_vault.json` & `.env` thông qua `tools/fb_multi_page_sync.py` (tự động lấy toàn bộ `PAGE_ID` & `PAGE_ACCESS_TOKEN` từ 1 `FACEBOOK_USER_TOKEN`).
- `[DONE]` Nâng cấp công cụ giọng đọc `tools/generate_voice_tts.py` lên **v2.0**: Tích hợp **Vbee AIVoice** + **Viettel AI TTS** + **Ánh xạ tự động 5 giọng Bắc/Nam theo 5 Fanpage (`--page 1..5`)** + Bộ lọc hậu kỳ **FFmpeg Studio Mastering** (cắt khoảng nghỉ thừa `> 0.22s`, nâng ấm/sáng giọng và khóa chuẩn `-3dB`).
- `[DONE]` Xóa sạch toàn bộ dữ liệu/khuôn mẫu Video Slide Cobalt–Lime cũ và **thay thế hoàn toàn bằng `templates/remotion-cuongit-template`** kèm Skill chính thức `.agents/skills/remotion-topic-explainer` và quy chuẩn `knowledge/quy-chuan-remotion-cuongit-template.md`.
- `[DONE]` Kết nối và kích hoạt thành công giọng đọc **Vbee AIVoice + FFmpeg Studio Mastering** trong `tools/generate_voice_tts.py` v2.0.
- `[DONE]` Sản xuất và render thành công video giải thích AI mới trên **`remotion-cuongit-template` (`McpExplainer` — 36.43s, điểm Rubric 9.7/10)**.
- `[DONE]` Rà soát 10 kho mã nguồn mở sản xuất Media AI và tích hợp 2 nâng cấp gọn nhẹ (`social-media-research` & `ffmpeg_render.py` multi-scene batch mixing).
- `[DONE]` Huấn luyện, nghiệm thu thực chiến và đóng gói **Bộ 5 Quy Tắc Vàng Dựng Video Remotion Brand-Kit (`MEM-20261020-remotion-brandkit-golden-rules`)**.
- `[DONE]` Sản xuất và render hoàn chỉnh Video Slide AI 45 giây chuẩn 5 Quy Tắc Vàng trên máy ở nhà (`Admin-PC`): **"AI Agent Tự Hành Khác Gì Chatbot Thông Thường?"** (`AiAgentVsChatbotShort` — điểm Rubric **10.0/10**).
- `[DONE]` Tối ưu hóa tốc độ Render Remotion (`Concurrency 50%` / `8x`) & giảm 86.5% dung lượng MP4 (`102.1 MB -> 13.83 MB`).
- `[DONE]` Sản xuất và render hoàn chỉnh Video Slide AI 45 giây theo kịch bản trực tiếp của CEO: **"Bản Đồ AI Hiện Tại (4 Trụ Cột) & Bước Ngoặt AI Tự Hành / Robotics"** (`AiMapPillarsShort` — điểm Rubric **10.0/10**).
- `[DONE]` Xây dựng công cụ `tools/fb_publish_video_reel.py` và thực thi lệnh `APPROVED_TO_PUBLISH` lên Fanpage **AI Players - Người chơi hệ AI** (`1022527194267367`).
- `[DONE]` Chuẩn hóa **Luật Chống Trùng Lặp Bố Cục (`Anti-Clone Layout Diversity Gate`)** cho Page `AI Players - Người chơi hệ AI`.
- `[DONE]` Khóa cứng **1 Phong Cách Thiết Kế Ảnh Duy Nhất (`Editorial Macro & 3-Detail Grid` — Khổ Vuông `1:1` `1080×1080`)** theo mẫu `sales-style-master-macro-grid.jpg` cho cả 3 Page Bán Hàng Affiliate.
- `[DONE]` Thiết lập cơ chế **Tự Động Dọn Kho Hình Ảnh & Video Local Sau 7 Ngày (`tools/cleanup_old_media.py`)**.
- `[DONE]` Xây dựng và kích hoạt **Lịch Báo Cáo Tổng Hợp 09h00 Sáng Hàng Ngày (`tools/mama_daily_9am_report.py`)**.
- `[DONE]` Thực thi **Đề xuất #1 — Phá Băng Tương Tác Chéo Tự Động (`tools/fb_cross_page_seeder.py`)** trên toàn bộ **13/13 bài đăng của 4 Fanpage**.
- `[DONE]` Giải phẫu kỹ thuật & đóng gói **Quy Chuẩn Vàng Sản Xuất Video AI Bán Hàng Số Lượng Lớn (SLL) Đa Sản Phẩm** (`knowledge/quy-chuan-video-ai-ban-hang-sll.md`).
- `[DONE]` Triển khai thực chiến trọn gói **Bước 1 $\rightarrow$ Bước 5 Tự Động 100%** cho sản phẩm **Quạt cầm tay mini phản lực iMI 120 mức gió Pin 5000mAh**.
- `[DONE]` Nghiên cứu, thiết kế và lưu vào Bộ não thứ 2 (`MEM-20261021-ai-players-subagent-course-funnel-strategy.md`) trọn bộ **Chiến lược Thương hiệu & Hệ thống Phễu Khóa học Subagent (Wave 1 + Wave 2) cho Page `AI Players - Người chơi hệ AI`**.
- `[DONE]` Nâng cấp `Agent-State-Sync/generate_snapshot.py` và `tools/mama_boot_check.py` tự động đồng bộ hai chiều toàn bộ thư mục `knowledge/bo-nao-thu-2/` và các file `.md` chiến dịch giữa máy nhà và máy công ty qua GitHub.
- `[DONE]` Xây dựng công cụ tự động hóa Link & Đối soát Shopee Affiliate Cá Nhân (`tools/shopee_link_manager.py`), khóa cứng mã **`SHOPEE_AFFILIATE_ID=17395830088`**.
- `[DONE]` Nghiên cứu chuyên sâu & đóng gói **Cẩm nang Đa kênh AI Affiliate 2026 (Facebook Reels + YouTube Shorts/Shopping + Threads)**.
- **[DONE] [2026-10-22 09:14] Tương tác chéo 4 Page & Seeding Hội nhóm 4 ngách (Ca Sáng 22/10 — Máy văn phòng `guicci`):** Hoàn tất tự động **33 Likes + 24 Bình luận thực chiến + 11 Group mới xin gia nhập** kèm 24 ảnh nghiệm thu gửi thẳng về Telegram.
- **[DONE] [2026-10-22 09:42] Khóa Tường Lửa Tệp Khán Giả (`MEM-20261022-audience-cluster-firewall-ai-vs-sales-pages`):** Tách biệt hoàn toàn tương tác giữa Page Công nghệ `AI Players` và Cụm 3 Page Bán Hàng (`Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline`).
- **[DONE] [2026-10-22 11:13] Kích hoạt Động Cơ Tự Động Chạy Ngầm Khi Mở Máy & Báo Cáo 6 Mốc Giờ Cố Định (`mama_auto_scheduler_engine.py` + `register_all_schedules.ps1`).**

---

## Phiên Làm Việc: 2026-10-23 — Nâng Cấp Tương Tác Video Ngang (16:9) & Dọc/Reels (9:16) Cùng Tệp & Khóa Cứng Quy Tắc Zero-Taskkill Bảo Vệ Chrome CEO

### 1. Tóm Tắt Quyết Định & Chỉ Đạo Cốt Lõi Của CEO
- **Bổ sung tương tác Video:** Bổ sung tương tác **cả Video Ngang (16:9) và Video Dọc (Reels 9:16)** tại các hội nhóm và luồng cùng tệp cho cả 4 ngách (`ai`, `phongtro`, `ktx`, `deadline`).
- **Bộ lọc thông minh Bài Mới + Nhiều Like/Comment:** Lọc đúng các bài/video **Mới đăng (`vừa xong`, `phút`, `giờ`, `1-3 ngày`) có lượng Like và Bình luận cao nhất** trên feed.
- **LỆNH CẤM NGHIÊM NGẶT TỪ CEO:** **TUYỆT ĐỐI CẤM LÀM VĂNG / ĐÓNG / KHỞI ĐỘNG LẠI CHROME CỦA CEO** (`taskkill /F /IM chrome.exe` bị cấm vĩnh viễn dưới mọi hình thức).

### 2. Các Hạng Mục Đã Hoàn Thành (`DONE`)
- [x] **Xóa bỏ 100% lệnh `taskkill` và đóng Chrome** trong toàn bộ codebase tools.
- [x] **Nâng cấp `mama_daily_group_and_eod.py` v2.0 (Video Ngang + Video Dọc/Reels + Chấm Điểm DOM).**
- [x] **Nâng cấp Bảng Điều Khiển Tương Tác 1-Click (`tools/fb_group_browser_interact.py` & `campaigns/daily-reports/group_seeding_cockpit.html`).**
- **[DONE] [2026-10-23 23:25] Khóa Cứng Quy Tắc CEO: 3 Page Bán Hàng Chỉ Đăng Ảnh 1:1 Kèm Link Shopee Affiliate — Đóng Băng Tuyệt Đối Video Bán Hàng Cho Đến Khi Training Đạt Chuẩn.**
- `[DONE]` **[2026-10-24] Cài đặt & tích hợp 2 Skill dựng video mới theo yêu cầu CEO (`talking-head-editor` & `motion-explainer-studio`).**
- `[DONE]` **[2026-10-24] Thiết kế bộ đôi Banner 3D Shopee Sale Key Visual cho `@KingToolShop_bot` (Khắc phục 100% lỗi chữ AI méo/ảo giác).**

---

## Phiên Làm Việc: 2026-10-26 & 2026-10-27 — Khóa Cổng Chống Đăng Lặp `Zero-Repost Gate`, Tường Lửa 3 Lớp Bảo Vệ Trang Cá Nhân & Đồng Bộ Đa Máy Thực Thời v3.0

### 1. Tóm Tắt Quyết Định & Chỉ Đạo Nóng Của CEO
- **Thu hồi bài đăng test sai lệch trên Page AI:** Phát hiện video vẽ tay bảng trắng test (`openrouter_mindmap_explainer.mp4`) bị đăng nhầm lên Page AI lúc 11:45 (lệch Brand Guidelines Remotion `#87ff00` kính trong suốt). Đã gỡ bỏ khẩn cấp ngay lập tức.
- **Khuôn mẫu thiết kế ảnh Page `AI Players`:** Đã xóa sạch 36 bài ảnh Pillow 2D xấu trên Meta; CEO đã đào tạo lại các thiết kế ảnh ở Máy Công Ty (`guicci`) sau `15:24` ngày `26/10` vì bản `render_vid_style_card.py` lúc `15:24` vẫn còn lỗi thiết kế nặng.
- **Khóa Cứng Cổng Chống Đăng Lặp Vĩnh Viễn (`Zero-Repost Gate` — `tools/zero_repost_gate.py`):** Cấm tuyệt đối việc lấy lại bài viết, ảnh hoặc video Reel cũ đã đăng để đăng lặp lại trên cả 4 Fanpage. Đã xóa bỏ `DAILY_SALES_QUEUE` tĩnh và 3 script đăng lặp bài cũ.
- **Tăng cường tương tác hội nhóm lên 3 ca/ngày (`12:00`, `17:30`, `20:30`) & Khóa Tường Lửa 3 Lớp Bảo Vệ Trang Cá Nhân:** Nghiêm cấm động vào trang cá nhân `Thành Tài` hoặc cửa sổ Messenger cá nhân; bắt buộc chuyển sang đúng 1 trong 4 Fanpage trước khi tương tác và chỉ gõ vào ô `Bình luận dưới tên <Tên Fanpage>`.
- **Xử lý dứt điểm lỗi không đồng bộ giữa Máy Công Ty (`guicci` — ổ `D:\`) và Máy Ở Nhà (`Admin-PC` — ổ `F:\`):** Xóa bỏ đường dẫn ổ đĩa cố định trong `.agents/hooks.json`, đồng bộ `git pull` + `--direction pull` trước khi đọc bộ nhớ đầu phiên, sửa lỗi PowerShell `$ErrorActionPreference = 'Stop'` làm đứt gãy tiến trình `git push` ngầm, mở khóa đồng bộ `assets/ai-players-image-styles/` và gom lịch sử của tất cả các cửa sổ chat từ cả 2 máy vào `RECENT-CONVERSATION.md`.

### 2. Các Hạng Mục Đã Hoàn Thành (`DONE`)
- [x] **Xử lý sự cố nóng trên Meta Graph API:** Đã xóa vĩnh viễn video bảng trắng đăng nhầm (`1022527194267367_122133373323248983`) và dọn sạch 100% 36 bài ảnh Pillow 2D lỗi khỏi hàng đợi hẹn giờ.
- [x] **Khóa cứng `Zero-Repost Gate` (`tools/zero_repost_gate.py` & `published_history_registry.json`):** Tự động băm SHA-256 ảnh/video và kiểm tra lịch sử đăng trước mọi lệnh xuất bản trên cả 4 Fanpage; xóa bỏ hoàn toàn `DAILY_SALES_QUEUE` tĩnh.
- [x] **Nâng cấp Động cơ Tương tác 3 ca/ngày (`12:00`, `17:30`, `20:30`) + Khóa Cứng Tường Lửa 3 Lớp Bảo Vệ Trang Cá Nhân (`mama_daily_group_and_eod.py` & `auto_seed_kingtool.py`):** Tự động khởi chạy trình duyệt Bot riêng `.chrome-fb-bot` cổng `9222`, tự động chuyển sang Fanpage (`ensure_fanpage_active()`), đóng mọi popup Messenger và chỉ bình luận dưới tên Fanpage.
- [x] **Nâng cấp Hệ Thống Đồng Bộ Đa Máy Thực Thời v3.0 (`.agents/hooks.json`, `tools/on_stop_sync_bridge.py`, `tools/mama_boot_check.py`, `on_stop_sync.py`, `generate_snapshot.py`, `sync-light.ps1`):** Tự động chạy trên cả ổ `D:\` (Máy Công Ty) và ổ `F:\` (Máy Nhà), ép `git pull` đồng bộ trước khi đọc bộ nhớ đầu phiên, phân tách `--direction pull/push` chống ghi đè ngược, đồng bộ cả thư mục `assets/ai-players-image-styles/` và gom lịch sử đa cửa sổ chat của cả 2 máy vào `RECENT-CONVERSATION.md`.

### 3. Các Hạng Mục Đang Thực Thi & Chờ Hoàn Tất (`IN_PROGRESS` / `OPEN` — Cấm Bỏ Dở)
- `[IN_PROGRESS]` **(Ưu tiên #1 — Đồng bộ bản sửa thiết kế ảnh mới của Page `AI Players` từ Máy Công Ty & Hoàn thiện Kho 1 Tuần):** (1) **Nhánh Ảnh (`42 Ảnh 1:1`):** Đồng bộ bản training sửa lỗi thiết kế ảnh từ Máy Công Ty (`guicci`) về kho chung và cập nhật lại ảnh hẹn giờ trên Page `AI Players`; (2) **Nhánh Video Reels (`3 Reels/ngày: 11:45, 16:30, 20:00`):** Giám sát render Remotion chuẩn 5 Quy Tắc Vàng cho 12 kịch bản mới trong `campaigns/2026-10-26/ai-players-4day-vault/` & chống trùng lặp qua `zero_repost_gate.py`.
- `[IN_PROGRESS]` **(Ưu tiên #2 — Kho Ảnh Mới Cho 3 Page Bán Hàng):** Săn SKU Whitelist mới và kết xuất lô ảnh vuông `1:1` mới chuẩn `Editorial Macro & 3-Detail Grid` + link Shopee Affiliate (`SHOPEE_AFFILIATE_ID=17395830088`) nạp vào hàng đợi `11:45` và `20:00` cho `Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline` (sau khi đã xóa `DAILY_SALES_QUEUE` cũ).
- `[IN_PROGRESS]` **(Ưu tiên #3 — Tương tác Hội nhóm 3 Ca `12:00`, `17:30`, `20:30`):** Vận hành ổn định 3 ca tương tác hàng ngày trên 4 ngách dưới danh nghĩa 4 Fanpage (với tường lửa 3 lớp bảo vệ trang cá nhân `Thành Tài`) và gửi ảnh nghiệm thu về Telegram.
- `[OPEN]` **(Ưu tiên #4 — Phễu Khóa học Subagent Page `AI Players`):** Sản xuất & đóng gói Món Quà số 1 từ kho 30 Lead Magnets (`Gói Subagent Đóng Hộp + Hook 3s / Văn Phòng`), cài đặt Nhóm Zalo Cộng Đồng Bảo Mật và lên bài thu phễu.
- `[OPEN]` **(Ưu tiên #5 — Đào tạo Video AI Bán Hàng SLL):** Kết nối Google Veo 3 để hoàn thiện quy trình sản xuất Video AI Bán Hàng SLL đạt chuẩn Vàng trình CEO nghiệm thu (trong thời gian này 3 Page Bán Hàng giữ nguyên 100% chỉ đăng Ảnh vuông 1:1).
