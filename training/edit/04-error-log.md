# Bước 4 — Error Log

## Lỗi thực tế trong micro-test

Không phát hiện lỗi bị trừ điểm trong output micro-test. Không tạo lỗi giả để hợp thức hóa quá trình huấn luyện.

| Mã | Lỗi chuẩn cần kiểm tra | Mức trừ | Có xuất hiện? | Bằng chứng / xử lý |
|---|---|---:|---|---|
| AV-01 | Chèn thoại tiếng Việt vào Motion Prompt | -3.0 | Không | Toàn bộ nội dung trong ba khối Motion Prompt là tiếng Anh. |
| AV-02 | Thiếu timeline theo giây | -2.0 | Không | Mỗi prompt có ba khoảng thời gian rõ ràng. |
| AV-03 | Mô tả chung chung, thiếu shot/angle/light | -2.0 | Không | Mỗi cảnh có cỡ cảnh, góc máy, camera behavior và ánh sáng cụ thể. |
| AV-04 | Thiếu lệnh chống méo | Theo rubric product fidelity | Không | Exact rigid lock xuất hiện trong từng cảnh. |
| AV-05 | Dùng người nổi tiếng/nhân vật bản quyền | Theo rubric compliance | Không | Chỉ dùng fictional/generic subject và negative constraints rõ ràng. |

## Rủi ro cấu hình được khóa

Trước cập nhật, file agent chưa bắt buộc Motion Prompt phải 100% tiếng Anh và chưa bắt buộc exact rigid lock. Đây là **khoảng trống cấu hình**, không phải lỗi của output micro-test. Đã khóa bằng hard rule, rubric 10 điểm và few-shot chuẩn trong `edit.md`.

## Danh sách câu sáo rỗng

Không có. Không dùng mô tả kiểu `A man shaving fabric`; mỗi prompt đều có ngôn ngữ điện ảnh và hành động theo thời gian.

## Sự cố thực tế 2026-10-14 — Nhầm Video Slide thành Video AI Bán Hàng

| Mã | Lỗi | Mức độ | Bằng chứng | Xử lý bắt buộc |
|---|---|---|---|---|
| VAI-SALE-01 | Dùng ba ảnh AI tĩnh, pan/zoom và motion text trong Remotion rồi gắn nhãn Video AI Bán Hàng | Critical / format fail | `campaigns/2026-10-14/video-ai-ban-hang-test-01/` | Hạ kết quả thành `FAILED_FORMAT / MOTION_STORYBOARD`; thêm gate 4 clip + 80% footage động; thiếu Veo/image-to-video phải trả `BLOCKED_MISSING_MOTION_ASSETS`. |

Nguyên nhân gốc: có quy tắc “chia clip Veo” nhưng chưa có preflight định lượng để xác nhận loại asset trước khi dựng. Render đúng độ phân giải, có voice, caption và âm thanh không thể bù cho việc sai format. Lỗi này không được phép tái diễn.
