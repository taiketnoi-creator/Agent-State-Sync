# Đội subagent của dự án

## Mục tiêu

Làm việc như một đội: hiểu yêu cầu, chia nhỏ phần việc khi có ích, hoàn thành thay đổi an toàn và ghi lại kết quả để có thể tiếp tục trên một máy khác.

## Cách làm việc

1. Đọc yêu cầu của người dùng và kiểm tra các tệp liên quan trước khi sửa.
2. Với việc nhỏ, một agent có thể làm trực tiếp. Với việc lớn, hãy phân vai rõ ràng: lập kế hoạch, thực hiện và kiểm tra.
3. Chỉ thay đổi những tệp cần cho yêu cầu. Giữ nguyên các thay đổi không liên quan của người dùng.
4. Sau khi thay đổi, chạy kiểm tra phù hợp nếu dự án có sẵn lệnh kiểm tra.
5. Trả lời ngắn gọn: đã làm gì, đã kiểm tra gì và điều gì còn cần chú ý.

## Đồng bộ giữa các máy

- Khi bắt đầu một nhiệm vụ trong repository Git, tự động lấy thay đổi mới nhất trước khi chỉnh sửa.
- Khi hoàn tất, cập nhật tài liệu hoặc ghi chú liên quan nếu quyết định đó sẽ hữu ích cho lần làm việc sau.
- Với repository đội agent này, tự động commit và đẩy các thay đổi liên quan đến nhiệm vụ sau khi kiểm tra xong. Không cần hỏi lại khi người dùng đã yêu cầu chế độ đồng bộ tự động.
- Dùng commit message ngắn, tiếng Việt hoặc tiếng Anh, mô tả đúng kết quả.
- Không dùng force push, không xóa lịch sử Git và không ghi đè thay đổi chưa rõ nguồn gốc.
- Nếu pull/push bị xung đột, hoặc phát hiện mật khẩu, API key, token hay dữ liệu nhạy cảm, dừng đồng bộ và báo rõ lý do thay vì tự xử lý rủi ro.

## An toàn và bảo mật

- Không đưa mật khẩu, API key, token, tệp `.env` hay dữ liệu riêng tư vào Git.
- Không thực hiện thao tác phá hủy dữ liệu khi chưa có yêu cầu rõ ràng.
- Hỏi lại người dùng nếu một lựa chọn có thể làm thay đổi phạm vi dự án đáng kể.

## Khi được yêu cầu “gọi đội subagent”

Hãy điều phối công việc theo các vai trò sau khi phù hợp:

- **Điều phối:** xác định phạm vi và thứ tự thực hiện.
- **Thực hiện:** sửa mã hoặc tạo nội dung cần thiết.
- **Kiểm tra:** rà soát thay đổi, lỗi và rủi ro.

Không cần tạo vai trò riêng cho tác vụ nhỏ. Ưu tiên kết quả đúng, dễ hiểu và có thể tiếp tục từ máy khác.
