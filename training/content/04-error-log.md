# Error Log — Viral Scriptwriter

## Kết quả trên micro-test

| Lỗi kiểm tra | Mức trừ | Có xuất hiện? | Bằng chứng / xử lý |
|---|---:|---|---|
| Mở bằng “Xin chào…” hoặc “Hôm nay mình giới thiệu…” | -3.0 | Không | Hook bắt đầu bằng “Trời ơi…” và đi thẳng vào tình huống. |
| Thoại quá dài, không đọc kịp trong 30 giây | -2.0 | Không | Tổng 80 từ, dưới trần huấn luyện 85 từ. |
| Lộ bán hàng từ giây thứ 5 | -2.0 | Không | Giây 4–10 chỉ mô tả nỗi đau; sản phẩm vào từ giây 11. |

## Câu sáo rỗng thực sự xuất hiện

`NONE` — không ghi nhận câu kiểu “sản phẩm tuyệt vời”, “không thể bỏ lỡ”, “chất lượng hàng đầu” hoặc lời chào quảng cáo trong bài test.

## Rủi ro cần khóa dù chưa phát sinh lỗi

- Prompt cũ chưa có trần số từ rõ ràng cho video 30 giây.
- Prompt cũ chưa cấm bằng câu lệnh dứt khoát các lời chào trong 3 giây đầu.
- Prompt cũ chưa mã hóa CTA khác nhau giữa Facebook và YouTube.

Phân loại nguyên nhân: `PROMPT_GAP`, không phải thiếu tool. Các khoảng trống này đã được khóa trong `content.md`.
