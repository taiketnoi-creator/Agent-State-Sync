# 04 — Error log và biện pháp khóa lỗi

| ID | Lỗi/thiếu sót | Tác động | Nguyên nhân | Khóa lỗi trong prompt |
|---|---|---|---|---|
| MR-01 | Có thể đưa listing shop tạm nghỉ vào Top 3 nếu chỉ nhìn ngách | Không thể chuyển đổi dù nội dung tốt | Prompt chưa chặt | Cấm `RECOMMEND` listing hết hàng/shop tạm nghỉ; chỉ giữ ngách ở `TEST` |
| MR-02 | Badge Mall/Yêu Thích không xác minh được ở mọi listing | “Shop uy tín” có thể bị nói quá | Thiếu tool/data công khai | Bắt buộc ghi `UNKNOWN`; không tự suy diễn badge |
| MR-03 | Commission và search volume không có trong phiên công khai | Dễ bịa hoặc tạo độ chính xác giả | Thiếu tool/data affiliate | Commission `UNKNOWN` nhận 0/20; không dùng điểm trung bình giả |
| MR-04 | Dải giá có thể trộn SKU hợp lệ và SKU vượt trần | Dùng giá “từ” gây hiểu lầm | Prompt chưa chặt | Khóa đúng SKU dưới 300k; dải có SKU ≥300k chỉ `TEST` |
| MR-05 | Quy trình gốc yêu cầu 5–10 sản phẩm trong khi micro-test yêu cầu đúng 3 | Có nguy cơ tự mở rộng phạm vi | Xung đột yêu cầu | Tuân lệnh hẹp hơn của Chief of Staff và ghi rõ ngoại lệ |
| MR-06 | Listing túi nén 20.000đ dưới dải giá mục tiêu 39.000–250.000đ | Biên doanh thu/giá trị đơn có thể không phù hợp dù vẫn dưới trần | Prompt chưa nêu sàn giá mục tiêu | Thêm dải mục tiêu 39.000–250.000đ; ngoài dải chỉ `TEST` với lý do rõ |
| MR-07 | Rating đạt nhưng badge Mall/Yêu Thích chưa được chứng minh vẫn có thể được hiểu là shop đạt chuẩn | Chấm quá tay mục Giá & shop | Rubric chính thức chặt hơn prompt cũ | Chỉ `RECOMMEND` khi badge đã quan sát; badge `UNKNOWN` tối đa `TEST` và không chấm trọn mục Giá & shop |

Không có lỗi thuộc nhóm “quên luật” trong micro-test. Các lỗi chính thuộc `thiếu tool-data` và `prompt chưa chặt`. MR-06 và MR-07 được phát hiện khi áp dụng rubric chính thức của CEO.
