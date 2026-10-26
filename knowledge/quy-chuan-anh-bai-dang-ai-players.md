# QUY CHUẨN THIẾT KẾ ẢNH BÀI ĐĂNG PAGE AI (`AI PLAYERS - NGƯỜI CHƠI HỆ AI`)
*Hệ thống Nhận diện Thị giác Cyber-Grid Carbon–Lime–Pink (`Downloads\vid` Style — 100% Khổ Vuông `1:1` `1080×1080` Render Qua Headless Chrome Engine)*

---

## 1. Nguyên Tắc Cốt Lõi Đã Khóa Cứng Bởi CEO (`Hard Gates — Cập nhật 26/10/2026`)

1. **100% CHUẨN STYLE `Downloads\vid` (`ref_1` $\rightarrow$ `ref_8`) QUA ENGINE `tools/render_vid_style_card.py`:**
   - **CẤM TUYỆT ĐỐI** dùng code Python `Pillow` (`draw.rectangle`) vẽ hộp 2D đen phẳng lì vô hồn.
   - **CẤM TUYỆT ĐỐI** quay lại phong cách nền xanh Cobalt cũ.
   - Toàn bộ ảnh bài đăng vuông `1:1` (`1080×1080`) trên Page `AI Players` phải kết xuất qua Headless Chrome/Edge HTML5 + CSS3 + SVG Engine tại [render_vid_style_card.py](file:///f:/Ai%20Agent%20Setup/SubAgent/Subagent/tools/render_vid_style_card.py) và [generate_weekly_vid_vault.py](file:///f:/Ai%20Agent%20Setup/SubAgent/Subagent/tools/generate_weekly_vid_vault.py).
2. **KHÓA VIEWPORT `1080×1080` KHÔNG MẤT VIỀN DƯỚI (`Zero-Cutoff Guarantee`):**
   - Khung trình duyệt Headless luôn cộng biên dư (`--window-size=1200,1250`) trước khi crop chính xác `(0, 0, 1080, 1080)` để bảo toàn 100% thẻ đáy và ngàm góc Cyber Brackets.
3. **CHỐNG TRÙNG LẶP (`Zero-Repost & Anti-Clone Layout Gate`):**
   - Trong 6 bài ảnh/ngày (`08:30`, `10:15`, `13:30`, `15:15`, `18:15`, `21:15`), bắt buộc luân phiên **5 Kiến trúc Layout (`Template 1` $\rightarrow$ `Template 5`)** để không có 2 bài liên tiếp trùng bố cục; cấm tuyệt đối lấy lại bài/ảnh cũ đã đăng những ngày trước.

---

## 2. Hệ Màu, Chất Liệu & Chi Tiết Đồ Họa Đặc Trưng (`Vid-Style DNA`)

1. **Bảng Màu Độc Quyền (`Carbon Checkered Grid + Electric Neon Lime + Hot Pink + Crisp White`):**
   - **Nền chính (`Background`):** Đen Carbon sâu (`#07080a`) phủ **họa tiết caro chìm (`#111317` checkered grid `72×72px`)** và quầng sáng trung tâm (`radial-gradient`).
   - **Màu Nhấn Chủ Đạo 1 (`Electric Neon Lime`):** Xanh chuối neon rực (`#CCFF00`) dùng cho thẻ lớn, số thứ tự `01–04`, khung đường hầm 3D, nút CTA pill và logo hoa thị 8 hướng (`Asterisk Logo`).
   - **Màu Nhấn Chủ Đạo 2 (`Cyber Hot Pink`):** Hồng neon (`#FF2A6D`) dùng cho nhãn nghiêng (`Skewed Parallelogram Badge -14deg` kèm ngôi sao `✦`), highlight từ khóa quan trọng, thanh tiến độ `SOLD OUT` và ngàm góc `Corner Brackets`.
   - **Màu Chữ (`Typography`):** Trắng tinh (`#FFFFFF`) và Đen tuyền (`#000000` trên nền `#CCFF00`), sử dụng bộ font **`Montserrat 800/900`**, **`Chakra Petch 900`** và **`Inter`**.
2. **Chi Tiết Đồ Họa Nhận Diện (`Signature Graphic Elements`):**
   - **Tiêu đề đóng ngoặc vuông đa sắc:** `[ <span style="color:#CCFF00">FOU</span>NDA<span style="color:#FF2A6D">TION</span> ]`
   - **Biểu tượng App 3D bóng kính (`Glossy 3D Squircle App Icon`)** kèm con trỏ chuột vector `↖` (`CURSOR_SVG`).
   - **Đường hầm lưới phối cảnh 3D (`3D Neon Cyber Perspective Grid Tunnel`)** kèm vòng quỹ đạo ngôi sao.
   - **Logo Hoa Thị 8 Hướng (`8-Directional Asterisk Star Logo` `#CCFF00`)** & Logo `zoom` tích hợp.

---

## 3. Năm (05) Kiến Trúc Bố Cục Chuẩn `Downloads\vid` (`5 Master Templates`)

| Mã Template | Hàm Render Trong `render_vid_style_card.py` | Cấu Trúc Thị Giác Đặc Trưng | Loại Bài Phù Hợp Nhất |
| :--- | :--- | :--- | :--- |
| **Template #1** | `render_template_hero_showcase()` | **Nửa trên:** Nhãn hồng nghiêng `✦ Thực hành với` + Thẻ lớn màu `#CCFF00` chứa tên Tool in đậm + Icon App 3D bóng kính & con trỏ chuột.<br>**Nửa dưới:** Nhãn hồng `✦ Với model` + Khung đường hầm lưới 3D Neon phát sáng tên Model (`SEEDANCE 2.5`, `STAGEHAND 2.0`...). | Giới thiệu Công cụ AI mới, Repo GitHub Hot, Model AI mới ra mắt. |
| **Template #2** | `render_template_curriculum_breakdown()` | **Header:** Nhãn hồng nghiêng bên trái + Pill hồng bên phải (`4 skills` / `4 tiêu chí`).<br>**Body:** Bảng 4 hàng kẻ chỉ mảnh `#CCFF00` dọc/ngang; cột trái là số khổng lồ `01` $\rightarrow$ `04` màu `#CCFF00`, cột phải là Tiêu đề trắng in hoa + Mô tả có highlight từ khóa màu hồng `#FF2A6D`. | Phân tích 4 Kỹ năng, Giáo án, So sánh 4 tiêu chí thực chiến, Checklist 4 bước. |
| **Template #3** | `render_template_feature_matrix()` | **Đỉnh:** Pill hồng `Level 01` + Tiêu đề lớn đóng ngoặc vuông `[ ... ]` phối 3 màu Chuối–Trắng–Hồng + Dòng thông tin Zoom.<br>**Giữa:** Ma trận `2×2` gồm 4 ô Pill viền mảnh chứa Icon `#CCFF00` (`key`, `book`, `flow`, `num`) + tiêu đề Trắng/Hồng.<br>**Đáy:** Logo Hoa thị 8 hướng `#CCFF00` + Cụm tiêu đề kết luận 2 dòng Trắng/Hồng. | Tổng quan Hệ thống, Bản đồ Model, Ma trận 4 tính năng / 4 mảnh ghép. |
| **Template #4** | `render_template_offer_card()` | Khung thẻ viền bo tròn có **dải đỉnh màu `#CCFF00`** + 4 ngàm góc hồng `Corner Brackets`: Nhãn hồng + Tiêu đề `[ ... ]` + Pill chuối hướng dẫn + **3 ô thẻ thông số ngang** + Pill thời gian + Nút CTA lớn màu `#CCFF00` có con trỏ chuột bấm vào. | Bài Tặng Quà (Lead Magnet: Sổ tay Prompt, Ebook, Template), Lịch sự kiện / Workshop. |
| **Template #5** | `render_template_urgency_slots()` | **Đỉnh:** Nhãn hồng + Chữ khổng lồ phát sáng trắng **`SOLD OUT`** (hoặc tiêu đề cảnh báo).<br>**Giữa:** 2–3 thanh tiến độ (`Progress Bars` màu hồng `#FF2A6D` báo `%` vị trí/chỉ số) + Nút Pill hồng lớn ở tâm.<br>**Đáy:** Khung viền `#CCFF00` chứa chữ lớn bên trái (`LV2` / `10X`) + Ưu đãi Trắng/Hồng ở giữa + Logo Hoa thị `#CCFF00` bên phải. | Bài Khan hiếm, Thống kê tỷ lệ đào thải/ứng dụng AI, Kêu gọi hành động khẩn cấp. |
