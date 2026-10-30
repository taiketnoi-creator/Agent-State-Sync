# Quy tắc Mama — Gặp vấn đề phải kèm giải pháp & Chuẩn Báo Cáo Telegram Ngắn Gọn

Áp dụng cho mọi nhiệm vụ của Mama và các agent khi vận hành 4 Fanpage trên cả Máy Công Ty (`guicci`) và Máy Ở Nhà (`Admin-PC`).

## 1. Gặp vấn đề phải kèm giải pháp
Khi bất kỳ bước nào bị lỗi, thiếu quyền, thiếu dữ liệu hoặc không thể hoàn tất:
1. Nêu rõ vấn đề và nguyên nhân đã xác minh.
2. Nêu ảnh hưởng đến mục tiêu, deadline hoặc chất lượng.
3. Đưa ra ít nhất một phương án xử lý khả thi, ưu tiên phương án ít rủi ro nhất.
4. Tiếp tục các phần độc lập có thể làm an toàn; không dừng toàn bộ kế hoạch chỉ vì một nhánh lỗi.

## 2. Quy chuẩn Văn Phong Báo Cáo Telegram (`Ultra-Concise Mobile Format`)
- **Độ dài tối đa:** **4–8 dòng** cho mỗi tin nhắn báo cáo trên Telegram (`compact_telegram_text()` trong `tools/telegram_bridge.py`).
- **Đi thẳng vào số liệu thực tế:** Chỉ nêu kết quả cốt lõi (`Bài đăng 24h`, `Kho hẹn giờ`, `Like / Comment`, `Kết quả ca tương tác`).
- **3 Điều Cấm Tuyệt Đối trên Telegram:**
  1. **CẤM** gửi bảng kẻ ngang Markdown (`| Fanpage | ... | :--- |`) gây vỡ khung trên điện thoại.
  2. **CẤM** liệt kê dài dòng danh sách tiêu đề 20–30 bài hẹn giờ hoặc viết đoạn văn nhận xét/khuyến nghị rườm rà.
  3. **CẤM** gửi 2 tin nhắn báo cáo trùng lặp liên tiếp trong cùng 1 mốc giờ (`mama_auto_scheduler_engine.py`).
