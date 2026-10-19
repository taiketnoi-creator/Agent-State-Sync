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
- [x] Khởi tạo Repo đồng bộ siêu nhẹ tại `D:\Phiên bản Ai agent\Agent-State-Sync`.

### 3. Chỉ Mục Tri Thức Hiện Có Từ Bộ Não Thứ 2 (`VALIDATED`)
*(Tham chiếu tại `D:\Phiên bản Ai agent\Subagent\knowledge\bo-nao-thu-2\INDEX.md`)*
- `MEM-20261012-page-network-pilot`: Mạng lưới 20 Page AI Affiliate và thứ tự pilot.
- `MEM-20261012-short-video-script-playbook`: Playbook kịch bản video ngắn có giá trị thực.
- `MEM-20261012-niche-product-research`: Phương pháp nghiên cứu niche và SKU AI Affiliate.
- `MEM-20261013-facebook-page-community-nurture`: Community nurture cho Facebook Page mới.
- `MEM-20261013-video-slide-composition-lessons`: Bài học thực chiến về bố cục và mật độ hình ảnh cho video slide.
- `MEM-20261014-ai-page-comment-hook-playbook`: Playbook 2 bài/ngày kéo bình luận cho Page AI.

### 4. Trạng Thái Các Hạng Mục Tiếp Theo (`OPEN` / `IN_PROGRESS`)
- `[OPEN]` Kết nối remote URL GitHub mới cho thư mục `D:\Phiên bản Ai agent\Agent-State-Sync` để đẩy bản đồng bộ siêu nhẹ đầu tiên.
- `[OPEN]` Import workflow mẫu `aff_video_autopost_workflow.json` vào n8n Docker local và kiểm tra kết nối Webhook thực tế.
- `[OPEN]` Chạy chiến dịch thực tế tiếp theo với đội Subagent (`mama` -> `mkt` -> `content` -> `edit` -> `voice` -> `quan-ly-kenh`).
