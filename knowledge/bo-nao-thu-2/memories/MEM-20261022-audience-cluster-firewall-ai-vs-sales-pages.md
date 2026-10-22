# MEM-20261022-audience-cluster-firewall-ai-vs-sales-pages — Luật Cứng Của CEO: Chỉ Tương Tác Các Group Hội Nhóm Cùng Tệp, Cấm Tuyệt Đối Tương Tác Chéo Giữa Các Page Với Nhau

- **ID:** `MEM-20261022-audience-cluster-firewall-ai-vs-sales-pages`
- **Loại:** `decision`
- **Trạng thái:** `VALIDATED`
- **Ngày chốt & Cập nhật:** `2026-10-22 19:01 (GMT+7)`
- **Nguồn:** Lệnh trực tiếp từ CEO qua Telegram (`Task #19`: *"Mama cập nhật thông tin chỉ tương tác các gr hội nhóm cùng tệp, k tương tác chéo các page vs nhau"*)
- **Phạm vi áp dụng:** `mama`, `cham-soc-kenh`, `quan-ly-kenh`, và toàn bộ công cụ tự động hóa Facebook (`tools/fb_*.py`, `tools/mama_auto_scheduler_engine.py`, `tools/mama_daily_group_and_eod.py`).

---

## 1. Quy Tắc Bắt Buộc (Hard Gate — Zero Cross-Page Seeding)

1. **CẤM TUYỆT ĐỐI tương tác chéo giữa bất kỳ Fanpage nào trong hệ thống với nhau (`0% Cross-Page Comment / Reply / Like`):**
   - Không dùng `AI Players` sang bình luận ở 3 Page bán hàng và ngược lại.
   - **Không dùng 3 Page bán hàng (`Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline`) đi bình luận hay thả Like chéo qua lại trên bài của nhau.**
   - Mỗi Fanpage chỉ thực hiện đúng **2 hành động trên chính Page của mình**:
     1. Tự gắn **`Pinned Comment #1`** của chính Page đó (chứa link Shopee Affiliate gắn `Sub_ID` hoặc link Nhóm Zalo Cộng Đồng).
     2. Chăm sóc và phản hồi 100% bình luận của **khách hàng thật bên ngoài** trên bài đăng của Page đó.

2. **CHỈ đi tương tác tại các Group / Hội nhóm Facebook CÙNG TỆP khách hàng của từng ngách (`Niche Group Seeding`):**
   - **Ngách 1 (`AI Players - Người chơi hệ AI`):** Chỉ tương tác trong các Group Cộng đồng AI Việt Nam, n8n & Automation, Claude/ChatGPT ứng dụng công việc, Vibe Coding.
   - **Ngách 2 (`Phòng Trọ Hết Cứu`):** Chỉ tương tác trong các Group Nghiện Decor Phòng Trọ, Cải tạo phòng nhỏ, Nấu ăn phòng trọ,Mẹo vặt nhà trọ.
   - **Ngách 3 (`Ký Túc Xá Có Biến`):** Chỉ tương tác trong các Group Sinh viên KTX (ĐHQG, Bách Khoa, NEU...), Đồ dùng tân sinh viên, Góc học tập sinh viên.
   - **Ngách 4 (`Hội Deadline`):** Chỉ tương tác trong các Group Vietnam Desk Setup, Chuyện Công Sở, Ghế công thái học & Đau mỏi cổ vai gáy, Dân văn phòng.

## 2. Chế Tài Kỹ Thuật Đã Khóa Trong Code
- Đã vô hiệu hóa vĩnh viễn mọi hàm bình luận chéo giữa các Page trong `tools/fb_cross_page_seeder.py` và `tools/fb_morning_2210_seeder.py` (thay bằng bộ quét tự động xóa sạch mọi bình luận chéo giữa các Page nếu phát hiện và chỉ trả lời khách hàng thật).
- Đã xóa sạch toàn bộ bình luận chéo cũ giữa các Page trên cả 4 Fanpage qua Facebook Graph API.
