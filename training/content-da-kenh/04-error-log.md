# Bước 4 — Error Log

## Lỗi thực tế trong micro-test

`NONE` — Không phát hiện lỗi đặt link, độ dài, hashtag hoặc claim trong output được chấm.

## Danh sách lỗi chuẩn phải chặn

| Mã | Lỗi | Mức trừ | Cách chặn đã đưa vào prompt |
|---|---|---:|---|
| MC-01 | Đặt URL trực tiếp trong caption Facebook Reels | -3,0 | Cấm URL trong caption; link chỉ ở bình luận ghim. |
| MC-02 | Caption Facebook dài như bài blog | -2,0 | Giới hạn tối đa 3 dòng. |
| MC-03 | Claim “Cam kết áo mới 100% sau 1 lần cạo” | -2,0 | Cấm claim tuyệt đối/quá đà; chỉ dùng mô tả quan sát được. |
| MC-04 | Tiêu đề YouTube từ 60 ký tự trở lên hoặc sai bộ hashtag | Theo rubric | Bắt buộc dưới 60 ký tự và đúng 3 hashtag cốt lõi. |
| MC-05 | Bịa link affiliate thật | Vi phạm nguyên tắc chung | Dùng `[SHOPEE_AFFILIATE_LINK]` tới khi có URL đã xác minh. |

## Chẩn đoán

- Lỗi do quên luật: `NONE`.
- Lỗi do thiếu tool: `NONE`.
- Lỗi do prompt chưa chặt: chưa xuất hiện trong micro-test, nhưng bốn constraint định dạng đã được bổ sung để giảm khả năng sai ở lượt sau.

## Câu sáo rỗng/claim cấm ghi nhận

- Không có câu sáo rỗng thực tế trong micro-test.
- Mẫu bị cấm dùng về sau: “Cam kết áo mới 100% sau 1 lần cạo”.

