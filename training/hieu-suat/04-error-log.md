# Bước 4 — Error Log

## Lỗi thực sự phát hiện trong cấu hình trước huấn luyện

| ID | Lỗi/khoảng trống | Nguyên nhân | Cách khóa lỗi | Trạng thái |
|---|---|---|---|---|
| CA-001 | Chưa bắt buộc bóc tách rõ ba lớp `nội dung/retention → CTA/link → offer/shop/landing page`. | Prompt cũ cho phép phân loại rộng nhưng chưa có checklist cố định. | Thêm giao thức thất bại ba lớp vào prompt. | Đã khóa |
| CA-002 | Chưa bắt buộc kết thúc bằng một next step cụ thể với heading chuẩn. | Tiêu chuẩn cũ chỉ yêu cầu quyết định/test, chưa chuẩn hóa output. | Thêm heading exact và yêu cầu một biến chính, control, KPI. | Đã khóa |
| CA-003 | Chưa có rubric huấn luyện và few-shot chứa công thức/denominator. | Prompt chưa đóng gói benchmark kiểm định. | Thêm rubric 10 điểm và worked example có CTR/CVR. | Đã khóa |

## Lỗi thường gặp cần giám sát

- “Cần làm nội dung hay hơn” nhưng không chỉ ra metric, bằng chứng hoặc test: trừ 3,0 điểm.
- Không phân biệt lỗi video với lỗi giá/chất lượng/shop/landing page: trừ 2,5 điểm.

Hai lỗi thường gặp trên **không xuất hiện trong câu trả lời micro-test**, nên không được ghi là lỗi agent đã phạm. Không phát sinh danh sách câu sáo rỗng thực tế.
