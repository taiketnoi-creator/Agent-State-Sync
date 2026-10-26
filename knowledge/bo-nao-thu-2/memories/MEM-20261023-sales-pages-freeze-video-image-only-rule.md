# MEM-20261023-sales-pages-freeze-video-image-only-rule — Luật Cứng Của CEO: 3 Page Bán Hàng Hiện Tại Chỉ Đăng Ảnh 1:1 Kèm Link Affiliate; Đóng Băng Video Bán Hàng Cho Đến Khi Training Đạt Chuẩn

- **ID:** `MEM-20261023-sales-pages-freeze-video-image-only-rule`
- **Loại:** `decision`
- **Trạng thái:** `VALIDATED`
- **Thẻ:** `sales-pages, freeze-video, image-only, editorial-macro-grid, shopee-affiliate, quality-gate, training`
- **Nguồn:** Chỉ đạo trực tiếp của CEO — 2026-10-23
- **Chủ quản:** `bo-nao-thu-2`, `mama`, `quan-ly-kenh`, `edit`, `content`

---

## 1. Bối cảnh chỉ đạo của CEO

Trong phiên vận hành ngày 23/10/2026, CEO đã ra chỉ đạo chấn chỉnh dứt khoát về chính sách nội dung trên 3 Page Bán Hàng:
> *"chưa đăng video bán hàng mà, page bán hàng hiện tại chỉ đăng ảnh, video bán hàng cần traning thêm nên chưa ra dc video chuẩn để đăng, video bán hàng hiện sẽ chưa đăng nội dung gì cả 3 page chỉ đăng ảnh và gắn link thôi"*

Các video bán hàng xuất hiện trên Graph API trước đó là các bản render thử nghiệm kỹ thuật (từ các đợt test render công cụ ngày 17/10 & 21/10). Về mặt vận hành thực tế, **chưa có bất kỳ video bán hàng nào được CEO phê duyệt để phát hành chính thức**.

---

## 2. Quy Tắc Cốt Lõi Khóa Cứng (Strict Operating Rules)

### Điều 1: 3 Page Bán Hàng Hiện Tại CHỈ ĐĂNG ẢNH & GẮN LINK SHOPEE AFFILIATE
- Áp dụng trên cả 3 Fanpage Bán Hàng:
  1. **`Phòng Trọ Hết Cứu`** (`1442323328956326`)
  2. **`Ký Túc Xá Có Biến`** (`1421270697727753`)
  3. **`Hội Deadline`** (`1407231352464711`)
- **Hình thức đăng bài:** **100% là Ảnh Vuông 1:1** thiết kế theo chuẩn độc bản duy nhất:
  - Phong cách: **`Editorial Macro & 3-Detail Grid`** trên nền xám ấm studio `#F8F8F6` theo [quy-chuan-anh-bai-dang-page-ban-hang.md](file:///f:/Ai%20Agent%20Setup/SubAgent/Subagent/knowledge/quy-chuan-anh-bai-dang-page-ban-hang.md).
  - Khung giờ đăng cố định: Đúng 2 khung giờ vàng **`11:45` trưa** và **`20:00` tối**.
  - Pinned Comment #1: Bắt buộc gắn link Shopee Affiliate chuẩn (Sub-ID phân tách theo Page).

### Điều 2: ĐÓNG BĂNG TUYỆT ĐỐI NỘI DUNG VIDEO BÁN HÀNG
- **Tình trạng hiện tại:** Video AI bán hàng đang trong quá trình training nội bộ (cần hoàn thiện chuyển động AI Veo/Kling, đồng nhất hình ảnh sản phẩm 3D và cảnh Before/After 3–5s đạt Rubric $\ge 9.0/10$).
- **Lệnh cấm:**
  - **CẤM TUYỆT ĐỐI** tự động xuất bản (publish) hoặc hẹn giờ (schedule) bất kỳ video nào lên 3 Page bán hàng.
  - Mọi công cụ tự động (`mama_auto_scheduler_engine.py`, `fb_publish_video_reel.py`, `multi_platform_auto_publisher.py`) phải khóa chặt luồng video của 3 Page bán hàng, chỉ cho phép xuất bản bài viết dạng PHOTO.
  - Video bán hàng chỉ được phép kích hoạt đăng bài khi và chỉ khi có văn bản nghiệm thu phê duyệt chính thức bằng lệnh `APPROVED_TO_PUBLISH_SALES_VIDEO` từ CEO.

### Điều 3: Phân Định Rõ Ràng Phạm Vi Phát Hành Video
- **Page duy nhất được phép đăng Video:** **`AI Players - Người chơi hệ AI`** (`1022527194267367`).
  - Định dạng: Chỉ đăng **Video Explainer / Tech Short** dựng bằng **Remotion chuẩn Vàng** (`templates/remotion-cuongit-template/src/AiHallucinationShort/` theo [MEM-20261020-remotion-brandkit-golden-rules.md](file:///f:/Ai%20Agent%20Setup/SubAgent/Subagent/knowledge/bo-nao-thu-2/memories/MEM-20261020-remotion-brandkit-golden-rules.md)), phục vụ mục tiêu chia sẻ giá trị kiến thức và dẫn phễu Zalo Cộng Đồng 0 Đồng.
  - Không bán hàng trực tiếp trên Page `AI Players`.

---

## 3. Phân Công Trách Nhiệm Đội Subagent

1. **`mama` (Chief of Staff):**
   - Giám sát toàn bộ các script lập lịch và tự động hóa; loại bỏ hoàn toàn mọi cấu hình lên lịch video bán hàng trên 3 Page.
   - Báo cáo định kỳ chỉ tính toán và kiểm tra chỉ số bài đăng ẢNH + link Affiliate cho 3 Page bán hàng.
2. **`quan-ly-kenh` & `content`:**
   - Khi chuẩn bị nội dung cho 3 Page bán hàng, 100% chuẩn bị định dạng Ảnh 1:1 + Caption chuẩn + Pinned Comment #1 chứa link Shopee.
   - Không đưa video bán hàng vào hàng đợi `scheduled_posts`.
3. **`edit`:**
   - Tiếp tục tập trung nghiên cứu và training các mẫu Video AI Bán hàng trong môi trường thử nghiệm nội bộ (`output/testing/`), không đưa ra môi trường production.
