# Bước 3 — Scorecard

## Rubric chính thức

| Tiêu chí | Trọng số | Kết quả kiểm tra | Điểm |
|---|---:|---|---:|
| Ngôn ngữ điện ảnh chuẩn; Motion Prompt không lẫn tiếng Việt | 3.0 | Cả ba prompt dùng tiếng Anh; có shot size, angle/movement, lighting và lens language. | 3.0 |
| Timeline giây chi tiết | 2.5 | Mọi prompt chia hành động thành các mốc giây liên tiếp, không chồng lấn. | 2.5 |
| Khóa chống méo sản phẩm | 2.5 | Cả ba cảnh có exact rigid lock và negative constraints riêng cho shot. | 2.5 |
| Không vi phạm người nổi tiếng/bản quyền | 2.0 | Chỉ dùng nhân vật hư cấu/không định danh; cấm celebrity likeness và copyrighted character. | 2.0 |
| **Tổng** | **10.0** | **Đạt ngưỡng >= 9.0** | **10.0** |

## Kiểm tra riêng từng cảnh

| Cảnh | Prompt tiếng Anh | Timeline | Shot/angle/light | Exact rigid lock | Deepfake/copyright | Kết quả |
|---|---|---|---|---|---|---|
| Hook áo xù lông | Đạt | Đạt | Đạt | Đạt | Đạt | PASS |
| Macro ASMR | Đạt | Đạt | Đạt | Đạt | Đạt | PASS |
| Before/After | Đạt | Đạt | Đạt | Đạt | Đạt | PASS |

**Điểm micro-test trước cập nhật prompt:** `10.0/10 — PASS`.

Ghi chú: agent đã đáp ứng đề bài nhờ chỉ thị test đầy đủ. Việc cập nhật file cấu hình vẫn cần thiết để biến các yêu cầu này thành luật mặc định cho những lần gọi sau, kể cả khi brief không nhắc lại.
