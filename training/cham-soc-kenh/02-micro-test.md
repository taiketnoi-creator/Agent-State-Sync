# Micro-test — cham-soc-kenh

## Input

Viết một Pinned Top Comment cho video “Máy cạo lông xù”, ba biến thể trả lời cho:

1. “Xin link shop uy tín”
2. “Có cạo rách áo không b?”
3. “Ship về tỉnh bao nhiêu ngày?”

Liệt kê 5 từ khóa moderation. Dùng placeholder `[SHOPEE_AFFILIATE_LINK]`; không bịa Mall, giá hoặc ship.

## Expected output

- Phần 1: pinned comment.
- Phần 2: response variants, tối thiểu 3 variants cho mỗi intent.
- Phần 3: moderation keywords và hành động theo ngữ cảnh.

## Gold response constraints

- Nêu ưu điểm/giới hạn nhẹ nhàng trước CTA.
- Câu hỏi ship phải hướng người xem kiểm tra ETA trên listing.
- Câu hỏi “rách áo” không được cam kết tuyệt đối.
- Keyword `lừa đảo` chỉ là tín hiệu review; khiếu nại hợp lệ chuyển người thật.
