# MEM-20261022-zero-clone-bespoke-video-rule

- **ID:** `MEM-20261022-zero-clone-bespoke-video-rule`
- **Tiêu đề:** Luật Bắt Buộc Của CEO: Không Video Nào Giống Video Nào — Khác Biệt 100% Từ Element, Bố Cục, Animation Đến Text
- **Loại:** `decision`
- **Trạng thái:** `VALIDATED`
- **Ngày ghi nhận:** `2026-10-22`
- **Nguồn:** Lệnh trực tiếp từ CEO sau khi kiểm tra kho video ngày `2026-10-22`
- **Phạm vi áp dụng:** Toàn bộ các video sản xuất từ nay về sau (`mama`, `edit`, `content` và quy chuẩn Remotion `knowledge/quy-chuan-remotion-cuongit-template.md`)

## Nội dung quy tắc bắt buộc

1. **Tuyệt đối cấm dùng chung Template Component cho nhiều video:**
   - Cấm tạo một component `DynamicShort` dùng chung rồi truyền mảng dữ liệu JSON để đẻ hàng loạt video có khung thẻ chữ nhật bo góc, khoảng cách lề hoặc cấu trúc chữ lặp lại.
2. **Mỗi video kịch bản khác nhau bắt buộc là 1 Composition độc lập (`src/<UniqueVideoSlug>/`) với 6 file cảnh (`Scene1..Scene6.tsx`) thiết kế riêng 100%:**
   - **Element hoàn toàn khác nhau:** Mỗi video phải tự vẽ đồ họa SVG, thiết bị 3D/UI mockup, biểu đồ hình học, đồng hồ đo, sơ đồ mạng lưới hoặc vật thể minh họa độc bản theo đúng kịch bản; cấm tái sử dụng khung thẻ của video trước.
   - **Bố cục (Macro & Micro Layout) hoàn toàn khác nhau:** Vị trí đặt tiêu đề, vị trí đặt vật thể minh họa, tỷ lệ chia khung hình (Trái–Phải, Trên–Dưới, Chéo góc, Tâm điểm đồng tâm, Đa tầng chồng lớp...) phải thay đổi hoàn toàn giữa các video.
   - **Animation (Chuyển động) hoàn toàn khác nhau:** Mỗi video phải có ngôn ngữ chuyển động riêng (xoay 3D perspective, vẽ nét SVG `stroke-dashoffset`, sóng âm biến thiên, con trỏ chuột click + vòng sóng lan tỏa, lật thẻ origami, hạt bay theo quỹ đạo...).
   - **Text (Cách trình bày chữ & Typography Callout) hoàn toàn khác nhau:** Cách dàn chữ tiêu đề (nghiêng Italic, xếp bậc thang, tách khối Kicker/Number, chữ chạy ngang, chữ gắn trong nhãn tag, font weight/size hierarchy) của mỗi video phải được thiết kế mới 100%.
3. **Cổng kiểm duyệt của `mama`:**
   - Trước khi lên lịch hoặc báo cáo nghiệm thu, `mama` bắt buộc ghép ảnh Grid Thumbnail của các video và kiểm tra chéo: nếu có bất kỳ 2 video nào có khung thẻ, bố cục hoặc kiểu trình bày chữ na ná nhau thì lập tức đánh `BLOCKED` và bắt `edit` code lại từ đầu.
