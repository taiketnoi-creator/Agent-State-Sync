# Facebook MCP cho tác vụ Page hằng ngày

## Phân vai công cụ

- `facebook_page` (HagaiHen/facebook-mcp-server): đọc bài viết và bình luận, đăng bài/ảnh, trả lời bình luận, lên lịch và đọc chỉ số hằng ngày.
- Windsor.ai: chỉ dùng cho báo cáo tổng hợp cuối tháng.
- Trình duyệt đã đăng nhập: phương án dự phòng khi Graph API không hỗ trợ tác vụ hoặc quyền của Page chưa được Meta phê duyệt.

## Bản cài đã kiểm tra

- Nguồn: `https://github.com/HagaiHen/facebook-mcp-server`
- Commit: `61b2128555d7582b19daf772186c03bc051c1c05`
- Thư mục cài cục bộ: `C:\Users\<user>\.codex\mcp\facebook-mcp-server`
- Python: môi trường riêng `.venv`
- MCP SDK: ghim nhánh `1.x` (`mcp<2`) vì mã nguồn hiện tại chưa tương thích MCP SDK 2.x.
- Codex MCP name: `facebook_page`

## Bảo mật và quyền thao tác

- Không ghi `FACEBOOK_ACCESS_TOKEN` vào repository, tài liệu, prompt hoặc commit.
- Token và `FACEBOOK_PAGE_ID` phải được cấp riêng trên từng máy bằng biến môi trường cục bộ.
- Cấu hình mặc định yêu cầu phê duyệt đối với thao tác ghi.
- Các công cụ xóa bài, xóa bình luận hàng loạt và gửi DM đang bị vô hiệu hóa mặc định.
- Repo chỉ nhận một cặp Page ID/token cho mỗi tiến trình. Nếu quản lý nhiều Page, cần cấu hình một server/credential riêng cho từng Page.

## Trạng thái nghiệm thu 2026-10-15

- Cài mã nguồn và dependency: hoàn tất.
- Server STDIO khởi động: đạt.
- Codex đọc được 40 công cụ MCP: đạt.
- Kết nối Graph API với Page thật: chờ cấp `FACEBOOK_ACCESS_TOKEN` và `FACEBOOK_PAGE_ID` hợp lệ.
- Sau khi cấp biến môi trường, khởi động lại Codex rồi kiểm tra `facebook_page` trong danh sách MCP trước khi chạy tác vụ thật.

## Nguyên tắc vận hành

1. Đọc Page và bình luận trước khi tạo phản hồi.
2. Không spam, không bình luận hàng loạt giống nhau và không tạo tương tác giả.
3. Bài đăng, bình luận và lịch đăng phải đúng Page được giao.
4. Nếu API lỗi, báo mã lỗi và đưa ngay phương án: sửa quyền/token, đổi tác vụ sang trình duyệt, hoặc chờ giới hạn Meta được gỡ.
5. Không tự xóa nội dung hoặc gửi tin nhắn riêng khi chưa có chỉ đạo rõ ràng.
