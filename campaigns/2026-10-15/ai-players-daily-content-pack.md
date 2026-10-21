# AI Players — gói nội dung ngày 15/10/2026

## Trạng thái vận hành

- Kênh: AI Players — Người chơi hệ AI.
- Nhịp đã duyệt: 2 Reel, 2 bài ảnh, 1 bài tin/trend và các lượt hỏi–đáp cộng đồng.
- Fallback hôm nay: dùng browser Facebook khi connector không hỗ trợ thao tác.
- Chưa đánh dấu xuất bản Reel/bài ảnh khi chưa có asset đã render và kiểm duyệt.

## Hai Reel — bản nháp chờ video render

### Reel 1 — giao việc cụ thể cho AI

- Hook màn hình: `Bạn không thiếu AI — bạn thiếu một việc cụ thể để giao.`
- Nội dung: lấy một việc lặp lại trong tuần, viết đầu vào, đầu ra và tiêu chí kiểm tra; thử trên dữ liệu mẫu trước khi dùng thật.
- CTA: `Bình luận VIỆC để nhận khung giao việc 5 dòng.`
- Disclosure: nội dung giáo dục; kết quả phụ thuộc công cụ, dữ liệu và bước kiểm tra của người dùng.

### Reel 2 — ghi chú thành checklist

- Hook màn hình: `Từ một đoạn ghi chú thành checklist có người phụ trách.`
- Nội dung: AI tách mục tiêu, bước làm, người phụ trách, hạn hoàn thành và điều kiện hoàn tất; người dùng duyệt trước khi giao việc.
- CTA: `Bình luận CHECKLIST nếu bạn muốn mẫu workflow.`
- Disclosure: không hứa tự động hóa tuyệt đối; luôn rà soát nội dung trước khi thực thi.

## Hai bài ảnh — bản nháp thiết kế

### Ảnh 1 — checklist workflow an toàn

- Tiêu đề: `5 dòng để giao việc cho AI rõ ràng hơn`
- Các dòng: Mục tiêu / Dữ liệu đầu vào / Đầu ra cần nhận / Giới hạn quyền / Cách kiểm tra.
- Caption: `Một prompt tốt chưa đủ. Hãy mô tả cả đầu vào, đầu ra và cách kiểm tra để workflow có thể lặp lại.`
- CTA: `Lưu bài và bình luận WORKFLOW để nhận ví dụ.`

### Ảnh 2 — AI không thay trách nhiệm

- Tiêu đề: `AI làm nhanh hơn, bạn vẫn là người duyệt cuối.`
- Ba điểm: kiểm tra nguồn / thử trên dữ liệu mẫu / duyệt trước khi ghi thay đổi.
- Caption: `Tự động hóa tốt luôn có điểm dừng để con người kiểm tra — đặc biệt với dữ liệu khách hàng, tài chính và nội dung công khai.`
- CTA: `Bạn đang đặt bước kiểm tra ở đâu trong quy trình?`

## Tin/trend — khung kiểm chứng trước khi đăng

- Góc: cập nhật xu hướng repo, MCP hoặc công cụ AI đang được cộng đồng quan tâm.
- Điều kiện đăng: chỉ dùng nguồn chính thức hoặc repo có lịch sử cập nhật rõ; ghi ngày truy cập, không khẳng định hiệu quả nếu chưa thử.
- CTA dự kiến: `Bạn muốn AI Players thử repo nào tiếp theo?`
- Trạng thái: `PENDING_SOURCE_VERIFICATION` — chưa đăng khi chưa có nguồn trend đã kiểm chứng trong ngày.

## Tương tác đã thực hiện hôm nay

- Đã trả lời bình luận MCP bằng vai trò AI Players, nhấn mạnh giới hạn quyền, dữ liệu mẫu và kiểm tra log.
- Đã trả lời bình luận CHECKLIST bằng vai trò AI Players, mời người dùng gửi ghi chú mẫu để chuyển thành workflow.
- Không trả lời các bình luận cũ ngoài cửa sổ chăm sóc hôm nay để tránh spam.

## Cổng duyệt

- `REEL_BLOCKED_ASSET`: chưa có MP4 AI Players đã render.
- `IMAGE_BLOCKED_ASSET`: chưa có hai file ảnh 1:1 đã duyệt.
- `TREND_PENDING_SOURCE_VERIFICATION`: chưa có nguồn trend kiểm chứng trong ngày.
