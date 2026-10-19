# Lịch Sử Công Việc & Bàn Giao Trò Chuyện Dự Án (Work & Conversation History)

> **Quy tắc cập nhật:** Cuối mỗi phiên làm việc quan trọng, ghi lại tóm tắt ngắn gọn theo cấu trúc: **Bối cảnh & Quyết định của CEO -> Các hạng mục đã hoàn thành -> Trạng thái các mục tiêu (`OPEN` / `IN_PROGRESS` / `DONE`) -> Việc cần làm ngay ở phiên tiếp theo**. Nhờ đó, khi chuyển sang máy khác, AI đọc file này là hiểu ngay mạch trò chuyện trước đó mà không cần đồng bộ dữ liệu nặng.

---

## Phiên Làm Việc: 2026-10-19 — Chuyển Đổi Kiến Trúc Tối Ưu Token & Đồng Bộ Siêu Nhẹ Trên Gemini 4

### 1. Tóm Tắt Nội Dung Trò Chuyện & Quyết Định Của CEO
- **Mục tiêu cốt lõi:** Áp dụng hệ thống tự động hóa Subagent vào mảng **Xây dựng hệ thống bán hàng Affiliate** và **Làm Video AI xây dựng thương hiệu & bán hàng**.
- **Quyết định công nghệ & hạ tầng:**
  - Sử dụng hoàn toàn **Gemini 4** để điều phối và vận hành hệ thống Subagent (không sử dụng Ollama local).
  - Kết hợp **Docker / n8n** đã cài sẵn trên máy Windows cùng **FFmpeg**, **SQLite** và **Skills** để xử lý các tác vụ lặp lại với chi phí **0 token**.
  - Tích hợp toàn bộ đội 10 Subagent hiện có từ Codex tại `D:\Phiên bản Ai agent\Subagent` (**Đội Agent Javis**) sang vận hành trực tiếp trên Antigravity (Gemini 4).
  - **Thay đổi chiến lược đồng bộ GitHub:** Tách một Repo mới siêu nhẹ (`D:\Phiên bản Ai agent\Agent-State-Sync`) chỉ lưu **Lịch sử công việc/trò chuyện**, **Nhật ký thay đổi/nâng cấp phần mềm**, và **File cấu trúc tổng quan (`PROJECT-BLUEPRINT.md`)**. Không đẩy database, video hay thư viện nặng lên GitHub vì các máy đều đã cài sẵn cơ sở dữ liệu ở local.

### 2. Những Việc Đã Hoàn Thành Trong Phiên (`DONE`)
- [x] Thiết kế kiến trúc **"Hybrid Zero-Waste"** giúp giảm 70–90% lượng token tiêu thụ khi chạy Subagent (dùng Subagent làm *Context Firewall*, chỉ trả báo cáo tóm tắt 5–15 dòng, lưu dữ liệu chi tiết xuống SQLite và file local).
- [x] Xây dựng MCP Server cục bộ `aff-n8n-sqlite` (`aff_n8n_sqlite_mcp.py`) kết nối trực tiếp **SQLite (`aff_system.db`)** và **Webhook n8n (`http://localhost:5678`)**, cấu hình chuẩn UTF-8 tiếng Việt trên Windows.
- [x] Kết nối tích hợp thêm `facebook-page` MCP Server (`C:\Users\guicci\.codex\mcp\facebook-mcp-server\server.py`) vào `C:\Users\guicci\.gemini\config\mcp_config.json`.
- [x] Kích hoạt cấu hình `.agents/GEMINI.md` và gắn đủ 4 bộ Skills (`ai-affiliate-page-operator`, `product-video-editor`, `ai-video-factory`, `n8n-automation-bridge`) vào `D:\Phiên bản Ai agent\Subagent\.agents\skills\`.
- [x] Định nghĩa đầy đủ 9 Subagent chuyên biệt của đội `Agent-Javis` (`mkt`, `content`, `edit`, `voice`, `content-da-kenh`, `quan-ly-kenh`, `cham-soc-kenh`, `hieu-suat`, `bo-nao-thu-2`) dưới sự điều phối của `mama` (Gemini 4).
- [x] Nâng cấp cơ chế **Smart Model Tiering & Batch Execution** trong `.agents/GEMINI.md` theo phê duyệt của CEO: giữ `mama`, `mkt`, `content`, `edit` chạy `inherit` (Gemini 4) và chuyển 6 Subagent hậu cần (`voice`, `content-da-kenh`, `quan-ly-kenh`, `cham-soc-kenh`, `hieu-suat`, `bo-nao-thu-2`) sang `flash` kèm gộp lệnh song song để tiết kiệm tối đa Quota Gemini 4.
- [x] Kiểm toán toàn diện 10 Agent và hoàn tất **4 nâng cấp đồng bộ đưa toàn đội lên chuẩn ≥ 9.2/10**:
  1. Cập nhật Frontmatter (`inherit` / `flash`) và tích hợp quy trình gọi trực tiếp MCP (`aff-n8n-sqlite`, `facebook-page`) vào cả 10 file `.md` gốc; viết lại `knowledge/quick-task-facebook-page-publish-comment.md` chuẩn MCP 100%.
  2. Xây dựng trọn bộ 5 bài đào tạo cho `training/bo-nao-thu-2/` (`01-brand-ingestion.md` -> `05-retest.md`), bổ sung Rubric 10 điểm & Few-shot vào `bo-nao-thu-2.md`, và khởi tạo lộ trình tổng `training/CURRICULUM.md`.
  3. Lập trình và kiểm thử 3 công cụ tự động 0-token trong `tools/`: `validate_script_linter.py` (đếm từ ≤85, chặn câu chào 3s đầu), `generate_voice_tts.py` (xuất `.mp3` tiếng Việt tốc độ 1.12x qua `edge-tts`), `calculate_affiliate_funnel.py` (tính phễu 3 lớp & xuất quyết định `KEEP/ITERATE/STOP`).
- [x] Trang bị cơ chế **Báo Cáo Khởi Động Phiên Tự Động Đa Máy (`tools/mama_boot_check.py` & Hook `SessionStart`)**: Tự động pull trạng thái mới nhất từ GitHub, tính `%` tiến độ mục tiêu và kiểm tra kết nối trực tiếp Facebook Page, n8n, SQLite, FFmpeg/Edge-TTS ngay khi bắt đầu chat ở bất kỳ máy nào.
- [x] Khởi tạo Repo đồng bộ siêu nhẹ tại `D:\Phiên bản Ai agent\Agent-State-Sync` và kết nối remote GitHub `https://github.com/taiketnoi-creator/Agent-State-Sync.git` kèm cơ chế tự động đồng bộ hai chiều sau mỗi lượt trò chuyện (`on_stop_sync.py` & `generate_snapshot.py`).

### 3. Chỉ Mục Tri Thức Hiện Có Từ Bộ Não Thứ 2 (`VALIDATED`)
*(Tham chiếu tại `D:\Phiên bản Ai agent\Subagent\knowledge\bo-nao-thu-2\INDEX.md`)*
- `MEM-20261012-page-network-pilot`: Mạng lưới 20 Page AI Affiliate và thứ tự pilot.
- `MEM-20261012-short-video-script-playbook`: Playbook kịch bản video ngắn có giá trị thực.
- `MEM-20261012-niche-product-research`: Phương pháp nghiên cứu niche và SKU AI Affiliate.
- `MEM-20261013-facebook-page-community-nurture`: Community nurture cho Facebook Page mới.
- `MEM-20261013-video-slide-composition-lessons`: Bài học thực chiến về bố cục và mật độ hình ảnh cho video slide.
- `MEM-20261014-ai-page-comment-hook-playbook`: Playbook 2 bài/ngày kéo bình luận cho Page AI.

### 4. Trạng Thái Các Hạng Mục Tiếp Theo (`OPEN` / `IN_PROGRESS` / `DONE`)
- `[DONE]` Kết nối remote URL GitHub (`https://github.com/taiketnoi-creator/Agent-State-Sync.git`) cho thư mục `D:\Phiên bản Ai agent\Agent-State-Sync` và đẩy bản đồng bộ siêu nhẹ lên GitHub.
- `[OPEN]` Import workflow mẫu `aff_video_autopost_workflow.json` vào n8n Docker local và kiểm tra kết nối Webhook thực tế.
- `[OPEN]` Chạy chiến dịch thực tế tiếp theo với đội Subagent (`mama` -> `mkt` -> `content` -> `edit` -> `voice` -> `quan-ly-kenh`).
