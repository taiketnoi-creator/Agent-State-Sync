---
id: MEM-20261020-sales-pages-image-style-guide
title: "Quy chuẩn Thiết Kế Ảnh 3 Page Bán Hàng Affiliate — Khổ Vuông 1:1 Chuẩn Minimal Pop-Bold Typography (Ít Chữ, Chữ Chính Dày Đậm, 3D Pop-Color Pill Badge)"
type: decision
status: VALIDATED
confidence: high
source: "CEO phê duyệt & khóa cứng chuẩn Minimal Pop-Bold Typography — 2026-10-30"
created_at: 2026-10-20
updated_at: 2026-10-30
owner: bo-nao-thu-2
tags: [sales-pages, image-style, square-1x1, minimal-pop-bold, editorial-macro-grid, headless-chrome, affiliate, edit]
scope: "Áp dụng bắt buộc 100% cho ảnh bài đăng sản phẩm trên 3 Page bán hàng Affiliate: Phòng Trọ Hết Cứu, Ký Túc Xá Có Biến, Hội Deadline."
---

## Nội dung quyết định đã xác thực (Cập nhật Chuẩn Minimal Pop-Bold 2026-10-30)

CEO quyết định **nâng cấp và khóa cứng quy chuẩn thiết kế ảnh bài đăng** cho cả 3 Page Bán Hàng Affiliate (`Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline`) với tỷ lệ Vuông `1:1` (`1080×1080 px`) theo triết lý: **ÍT CHỮ TỐI ĐA — CHỮ CHÍNH DÀY DẶN — MÀU SẮC BẮT MẮT — ẢNH SẢN PHẨM THÔNG THOÁNG 100%**:

1. **Nguyên Tắc Cốt Lõi (Hard Gates):**
   - **Ít Chữ Tối Đa — Cấm Nhồi Nhét Text Gây Rối Mắt (`Zero Text Clutter`):**
     + Tuyệt đối không nhồi nhét hàng loạt spec pills, danh sách `01 - 02 - 03`, nhãn `#01/#02/#03` hay mô tả 2 dòng dài dưới 3 ô chi tiết.
     + Toàn bộ vùng giữa ảnh và vùng dưới vòng tròn Macro phải **để trống 100%** cho ảnh chụp sản phẩm studio tỏa sáng.
   - **Chữ Chính Dày Dặn & Màu Sắc Bắt Mắt (`Minimal Pop-Bold Headline`):**
     + Kết xuất bằng Headless Chrome HTML/CSS Engine (`tools/render_sales_bold_editorial.py`).
     + Góc trên trái **chỉ hiển thị đúng 2 dòng Tiêu Đề Chính cỡ đại** (`48px–68px`, Font `Be Vietnam Pro Black 900` cực dày):
       - *Dòng 1:* Chữ in hoa siêu dày màu nhấn có viền đậm `#111827` & bóng đổ khối 3D.
       - *Dòng 2:* Bọc trong **Khối Hộp Màu Nổi 3D (`3D Pop-Color Pill Badge`)** với bảng màu rực rỡ (`#FF3D00`, `#0066FF`, `#00A859`, `#FF6B00`, `#6D28D9`, `#E11D48`, `#0284C7`).
     + Dưới 3 ô vuông chi tiết ở đáy (`y=994px`): Chỉ gắn **đúng 1 nhãn Pill ngắn gọn 2–3 từ (`19px`, `Black 900`)** sát mép dưới mỗi ô, không viết câu dài.

2. **Ảnh Mẫu Chuẩn Vàng & Cổng Kiểm Duyệt:**
   - Ảnh mẫu tham chiếu: `assets/sales-pages-image-styles/sales-style-master-macro-grid-bold-v2.jpg`.
   - Bảng QA Grid kiểm duyệt: `campaigns/2026-10-30/sales-weekend-vault/sales_weekend_9_qa_grid.jpg`.
   - Bắt buộc kiểm tra trực quan bằng mắt (`read_file` trên QA Grid) trước khi lên lịch đăng.

3. **Lịch Đăng & Chuyển Đổi:**
   - Khung giờ vàng cố định: **`11h45 trưa`** và **`20h00 tối`** (2 bài/page/ngày = 6 bài/ngày).
   - Cuối Caption bắt buộc có 1 câu hỏi lựa chọn A/B ngắn gọn để kéo bình luận thật, điều hướng link Shopee tại **Bình luận đầu tiên (`Pinned Comment #1`)**.
