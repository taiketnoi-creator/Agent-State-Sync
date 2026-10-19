# Quy Tắc Tự Động Tiếp Nhận & Bàn Giao Giữa Các Máy (Cross-Machine Continuity Protocol)

1. **Khi bắt đầu phiên làm việc mới:**
   - Đọc ngay 3 file trong thư mục này theo thứ tự:
     1. [PROJECT-BLUEPRINT.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Agent-State-Sync/PROJECT-BLUEPRINT.md) — Nắm cấu trúc tổng quan, vị trí đội Subagent (`D:\Phiên bản Ai agent\Subagent`), Database SQLite và MCP Servers.
     2. [WORK-HISTORY.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Agent-State-Sync/WORK-HISTORY.md) — Nắm mạch trò chuyện gần nhất, quyết định của CEO và các việc đang `OPEN` / `IN_PROGRESS`.
     3. [SOFTWARE-CHANGELOG.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Agent-State-Sync/SOFTWARE-CHANGELOG.md) & [STATE-SNAPSHOT.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Agent-State-Sync/STATE-SNAPSHOT.md) — Kiểm tra các nâng cấp phần mềm và danh sách sản phẩm/chiến dịch mới nhất.
2. **Khi kết thúc phiên hoặc khi CEO yêu cầu đồng bộ / đẩy lên GitHub:**
   - Ghi nối tiếp (append) tóm tắt cuộc trò chuyện, kết quả công việc vào `WORK-HISTORY.md`.
   - Nếu có thay đổi công cụ, phần mềm, MCP, Skills hay cấu trúc thư mục, cập nhật vào `SOFTWARE-CHANGELOG.md` và `PROJECT-BLUEPRINT.md`.
   - Chạy script `./sync-light.ps1 -Mode finish` để tự động chụp snapshot và đẩy lên GitHub.
