# Quy Trình Tự Động: Đăng Bài & Bình Luận Cho Facebook Page Qua MCP Server

## 1. Mục Tiêu

Hoàn tất chu trình phân phối nội dung trên Facebook Page thông qua hệ thống **MCP Server local** (`facebook-page` và `aff-n8n-sqlite`):
1. Chuẩn bị nội dung và trích xuất link Affiliate Shopee đã rút gọn từ SQLite.
2. Đăng bài hoặc lên lịch phát hành đúng khung giờ vàng qua MCP `facebook-page`.
3. Lấy `post_id` trả về và tự động tạo Pinned Comment chứa link Affiliate Shopee.
4. Quản lý tương tác và tự động lọc/kiểm duyệt bình luận tiêu cực.
5. Bảo toàn cổng kiểm soát an toàn tuyệt đối (`DRAFT_ONLY` vs `APPROVED_TO_PUBLISH`).

---

## 2. Cổng Kiểm Soát An Toàn Bắt Buộc (Safety Gate)

> [!IMPORTANT]
> **QUY TẮC AN TOÀN PUBLISH:**
> - Mọi kế hoạch nội dung, lịch đăng và bình luận mặc định ở trạng thái `DRAFT_ONLY`.
> - **CHỈ THỰC HIỆN ĐĂNG THẬT / LÊN LỊCH THẬT** khi có chỉ thị rõ ràng kèm trạng thái `APPROVED_TO_PUBLISH` từ CEO.
> - Tuyệt đối không đăng quá **2 video/ngày/kênh**.
> - Khung giờ lên lịch cố định: **11h45 trưa** hoặc **20h00 tối** (Asia/Ho_Chi_Minh).

---

## 3. Chuỗi Thực Hiện Chuẩn (5 Bước Tự Động Hóa 0-Token)

### Bước 1: Chuẩn bị nội dung & Lấy link Affiliate từ SQLite
- **Kiểm tra asset & copy:**
  + Video dọc 9:16 hoặc ảnh/carousel đã qua QA kỹ thuật (`edit`), voiceover/audio chuẩn (`voice`).
  + Caption chuẩn quy tắc Facebook Reels (`content-da-kenh`): không chứa URL trong caption, tối đa 3 dòng, kết thúc bắt buộc bằng câu:
    > *"Link tui ghim ở bình luận đầu tiên nhé!"*
- **Truy vấn link Affiliate:**
  + Gọi MCP `aff-n8n-sqlite:sqlite_query` để lấy link rút gọn kèm mã tracking (`sub_id`) từ bảng `products` trong database SQLite local:
    ```sql
    SELECT product_name, promo_price, affiliate_link, shopee_url FROM products WHERE id = :product_id;
    ```

### Bước 2: Đăng bài hoặc Lên lịch bài viết qua MCP `facebook-page`
- **Tùy chọn A — Lên lịch bài viết (Ưu tiên):**
  + Gọi MCP tool `facebook-page:schedule_post`:
    * `message`: Nội dung caption đã chuẩn hóa (kèm disclosure AI/Affiliate nếu có).
    * `scheduled_publish_time`: Timestamp Unix của khung giờ vàng gần nhất (11h45 hoặc 20h00).
  + Kiểm tra danh sách đã lên lịch qua `facebook-page:get_scheduled_posts`.
- **Tùy chọn B — Đăng ngay (Khi có lệnh phê duyệt đăng gấp):**
  + Đối với bài viết chữ, link hoặc video Reel: Gọi MCP tool `facebook-page:post_to_facebook` với `message` và `link` (nếu là bài chia sẻ) hoặc media upload.
  + Đối với bài ảnh đơn / album: Gọi MCP tool `facebook-page:post_image_to_facebook`.
- **Ghi nhận phản hồi:**
  + Nhận và lưu lại mã định danh bài viết: `post_id` (dạng `PageID_PostID`).

### Bước 3: Đăng Pinned Comment gắn Link Affiliate
- Sau khi có `post_id`, ngay lập tức gọi MCP tool `facebook-page:reply_to_comment` (hoặc tạo bình luận cấp 1 dưới `post_id`):
  + **Nội dung Pinned Comment chuẩn:**
    > *"Link sản phẩm tui ghim ở đây nhé: [AFFILIATE_LINK] (Lưu ý: Link affiliate, giá và khuyến mãi có thể thay đổi tùy thời điểm mua hàng nha mọi người!)"*
  + **Quy chuẩn:**
    * Link phải là link Shopee Affiliate hợp lệ lấy từ bảng `products`.
    * Phải có disclosure minh bạch về tiếp thị liên kết.
    * Ghim bình luận lên đầu bài viết để người xem dễ thấy nhất.

### Bước 4: Tự động Kiểm duyệt & Quản trị Tương tác (Moderation)
- Định kỳ theo ca hoặc sau khi đăng:
  1. Quét bình luận mới bằng MCP `facebook-page:get_post_comments`.
  2. Phản hồi các thắc mắc thông thường ("Bao nhiêu tiền?", "Dùng bền không?") bằng MCP `facebook-page:reply_to_comment` từ bộ Canned Responses đã duyệt.
  3. Lọc bình luận tiêu cực, chửi bới, xúc phạm qua MCP `facebook-page:filter_negative_comments`.
  4. Ẩn bình luận spam, lừa đảo, chèn link lạ qua MCP `facebook-page:hide_comment` hoặc `bulk_hide_comments`.
  5. Khi gặp bình luận khiếu nại chất lượng hàng, yêu cầu hoàn tiền hoặc nghi hàng giả: Gắn cờ `NEEDS_HUMAN` và báo ngay cho CEO/Mama, tuyệt đối không tự ý xóa bình luận của khách hàng thật.

### Bước 5: Báo cáo nhanh & Ghi nhận SQLite
- Gọi tool MCP `aff-n8n-sqlite:aff_save_video_job` để cập nhật trạng thái video job thành `PUBLISHED` kèm `post_id` và URL bài viết.
- Xuất báo cáo ngắn gọn tối đa 5 dòng cho Mama/CEO:
  * Page & Chiến dịch.
  * `post_id` & Link bài viết trực tiếp.
  * Trạng thái Pinned Comment (đã đăng kèm link Shopee).
  * Khung giờ đăng / lên lịch.

---

## 4. Xử Lý Sự Cố & Rollback (Incident Handling)

| Sự cố | Nguyên nhân | Hướng xử lý |
| :--- | :--- | :--- |
| MCP báo lỗi Token Facebook hết hạn | Page Access Token bị thu hồi hoặc hết hạn | Báo Mama/CEO làm mới Token trong cấu hình MCP `facebook-page`, giữ bài viết ở `READY_FOR_REVIEW`, không thử lại liên tục. |
| Không lấy được `post_id` | Mạng chập chờn hoặc API phản hồi chậm | Dùng `facebook-page:get_page_posts` để truy vấn danh sách 5 bài gần nhất tìm bài vừa tạo; nếu thấy thì lấy `post_id` tiếp tục bước comment; nếu không có mới retry 1 lần. |
| Chưa có link Shopee Affiliate đã rút gọn | Chưa chạy webhook n8n hoặc thiếu SKU | Tạm hoãn bình luận, giữ ở `PUBLISHED_COMMENT_PENDING`, kích hoạt `n8n_trigger_webhook` (`/webhook/aff-link-shorten`) để lấy link trước khi ghim. |
| Phát hiện sai sót trong caption | Lỗi chính tả hoặc nhầm giá | Dùng tool MCP `facebook-page:update_post` để sửa lại caption ngay lập tức. Nếu lỗi nghiêm trọng vi phạm chính sách: Dùng `delete_post` để gỡ bỏ. |

---

## 5. Checklist Vận Hành 30 Giây

- [ ] Trạng thái đã được CEO phê duyệt: `APPROVED_TO_PUBLISH`.
- [ ] Caption tuân thủ: 0 link trong caption, kết đúng câu *"Link tui ghim ở bình luận đầu tiên nhé!"*.
- [ ] Link Shopee Affiliate đã được kiểm chứng từ SQLite local (`aff-n8n-sqlite`).
- [ ] Đăng/Lên lịch thành công qua MCP `facebook-page`, nhận `post_id`.
- [ ] Đã đăng Pinned Comment chứa link Shopee Affiliate dưới `post_id`.
- [ ] Đã cập nhật trạng thái vào SQLite local (`aff_save_video_job`).
