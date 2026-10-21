# QUY CHUẨN THIẾT KẾ ẢNH BÀI ĐĂNG PAGE AI (`AI PLAYERS - NGƯỜI CHƠI HỆ AI`)
*Hệ thống nhận diện thị giác Cobalt–Lime 3D Textured Illustration (100% Khổ Vuông 1:1 — Giữ Hệ Màu & Chất Liệu, Đa Dạng Hóa Bố Cục Tuyệt Đối)*

---

## 1. Nguyên Tắc Cốt Lõi Đã Khóa Cứng Bởi CEO (`Hard Gates`)

1. **GIỮ ĐỒNG NHẤT HỆ MÀU & CHẤT LIỆU 3D, NHƯNG BỐ CỤC PHẢI KHÁC NHAU (`ANTI-CLONE LAYOUT DIVERSITY GATE`):**
   - **CẤM TUYỆT ĐỐI** việc dùng đi dùng lại 1–2 khuôn bố cục giống hệt nhau (ví dụ: bài nào cũng chữ căn giữa ở trên + nút pill ở giữa + vật thể tròn ở dưới, hoặc bài nào cũng chia 4 ô 2×2 giống nhau).
   - **Cái cần giữ cố định (`Brand DNA`):** Hệ màu **Xanh Dương Cobalt Điện Tử (`#03185E` $\rightarrow$ `#1452F0`) + Xanh Chuối Neon (`#A8FF00`) + Trắng Tinh (`#FFFFFF`) & Xanh Băng (`#C7DCFF`)**, chất liệu **Đồ họa 3D phủ hạt nhiễu mịn (`3D Stipple/Grain Textured Illustration`)**, khổ vuông `1:1`, **100% không dùng ảnh mặt người**.
   - **Cái bắt buộc phải thay đổi ở mỗi bài (`Layout & Composition`):** Vị trí đặt chữ, cấu trúc chia vùng, góc máy 3D (`isometric`, `top-down`, `split-screen`, `close-up macro`, `bento asymmetric`) và cách trình bày thông tin phải biến hóa theo đúng nội dung từng bài. Không được có 2 bài liên tiếp trên Page trùng kiểu bố cục.
2. **100% ĐỒ HỌA 3D KHÔNG NGƯỜI (`NO-PERSON 3D GRAPHIC ONLY`):**
   - Tuyệt đối không đưa ảnh mặt người / chân dung chuyên gia lên ảnh bài đăng.
   - Tham chiếu chất liệu & bảng màu từ 2 ảnh mẫu gốc:
     - [cobalt-lime-01-3d-hero-scene.jpg](file:///f:/Ai%20Agent%20Setup/SubAgent/Subagent/assets/ai-players-image-styles/cobalt-lime-01-3d-hero-scene.jpg)
     - [cobalt-lime-02-2x2-3d-icon-grid.jpg](file:///f:/Ai%20Agent%20Setup/SubAgent/Subagent/assets/ai-players-image-styles/cobalt-lime-02-2x2-3d-icon-grid.jpg)
3. **100% KHỔ VUÔNG `1:1` (`1080×1080`):**
   - Mọi ảnh xuất ra đều cố định ở tỷ lệ vuông `1:1`.

---

## 2. Hệ Màu & Chất Liệu Nhận Diện Cố Định (`Visual Style DNA`)

1. **Bảng Màu Độc Quyền (`Electric Cobalt Blue + Neon Lime + Crisp White`):**
   - **Nền chính (`Background`):** Xanh Dương Cobalt Điện Tử Sâu (`#03185E` $\rightarrow$ `#0A36BA` $\rightarrow$ `#1452F0`), phủ **hạt nhiễu mịn (`stipple/grain noise`)**.
   - **Màu Nhấn (`Neon Lime Accent`):** Xanh chuối neon phát sáng (`#A8FF00` / `#B8FF1A`).
   - **Màu Chữ & Khối 3D:** Trắng tinh (`#FFFFFF`) và Xanh băng nhạt (`#C7DCFF`).
2. **Chi Tiết Đồ Họa Đặc Trưng (Dùng linh hoạt, không rập khuôn vị trí):**
   - Khối 3D có độ nhám hạt (`textured 3D clay/glass/metal render`), thẻ kính mờ (`frosted glass cards`), tia sáng/hạt năng lượng xanh lime, vệt cọ sần hoặc lưới kỹ thuật mảnh.

---

## 3. 6 Kiến Trúc Bố Cục Khác Biệt Bắt Buộc Luân Phiên (`6 Distinct Layout Archetypes`)

Khi thiết kế bộ ảnh cho Page AI trong ngày (ví dụ 5–6 bài/ngày), `edit` và `image-generator` **bắt buộc gán mỗi bài một Kiến trúc Bố cục khác nhau hoàn toàn** trong 6 kiểu sau:

| Mã Bố Cục | Tên Kiến Trúc Thiết Kế | Mô Tả Cấu Trúc Thị Giác Khác Biệt | Phù Hợp Nhất Cho Loại Bài |
| :--- | :--- | :--- | :--- |
| **Layout #1** | **`3D Hero Scene + Energy Rings`** *(Góc nghiêng trung tâm)* | Tiêu đề lớn ở đỉnh; nửa dưới là **1 cụm thiết bị/cửa sổ 3D nghiêng góc** đặt trong vòng xoáy năng lượng Neon Lime. | Bài giới thiệu Công cụ / Repo điều khiển tự động (VD: `browser-use`). |
| **Layout #2** | **`VS Split-Screen Comparison`** *(Chia đôi màn hình đối đầu)* | Chia ảnh thành **2 nửa Trái – Phải (hoặc Chéo góc)** đối lập rõ rệt: Bên trái tông xanh tối trầm (Cách cũ / Tốn phí) `VS` Bên phải bừng sáng viền Neon Lime (Giải pháp AI / Open-Source 0đ). | Bài so sánh Công cụ Miễn phí vs Trả phí, hoặc Trước vs Sau khi dùng AI (VD: `F5-TTS 0đ vs Tool $99`). |
| **Layout #3** | **`Isometric 3D Pipeline Flowchart`** *(Sơ đồ dây chuyền 3D)* | Góc nhìn **Isometric từ trên chéo xuống**: 3–4 trạm/khối 3D nối liền nhau bằng **đường ống ánh sáng Neon Lime dẫn truyền theo hình chữ Z hoặc đường chéo** từ góc trên xuống góc dưới; tiêu đề đặt gọn ở góc. | Bài Hệ thống, Kiến trúc Đội quân AI, Workflow nhiều bước (VD: `Bản vẽ Đội quân Nhân sự AI 24/7`). |
| **Layout #4** | **`Asymmetric Left–Right Editorial`** *(Bố cục tạp chí bất đối xứng Trái–Phải)* | **Cột Trái (45%):** Tiêu đề lớn căn lề trái xếp dọc từ trên xuống + danh sách 3–4 gạch đầu dòng phát sáng + nút CTA góc dưới trái.<br>**Cột Phải (55%):** Một mô hình 3D dạng chồng sách/tháp tài liệu/cỗ máy lớn vươn dọc từ đáy lên sát đỉnh phải. | Bài Tặng Tài Liệu, Sổ Tay, Ebook, Bộ Prompt (VD: `Sổ tay 50 Siêu Prompt`). |
| **Layout #5** | **`Giant Centerpiece + Anatomy Callouts`** *(Giải phẫu vật thể khổng lồ ở tâm)* | Chính giữa ảnh là **1 vật thể 3D khổng lồ** (rương kho báu mở tung, lõi chip AI, khối Rubik công nghệ) tỏa sáng ra 4 phía; xung quanh là **4–5 thẻ nhãn nhỏ (`Callout Pointers`) có đường kẻ chấm chỉ thẳng vào từng bộ phận**; tiêu đề đặt vòm phía trên hoặc dưới đáy. | Bài Tổng hợp Kho tài nguyên, Giải phẫu cấu trúc, Top công cụ (VD: `Kho báu 30.000 sao GitHub`). |
| **Layout #6** | **`Bento Modular Grid (Asymmetric)`** *(Lưới Bento đa kích thước kiểu Apple)* | Thay vì 4 ô bằng nhau nhàm chán, chia thành **Bố cục Bento bất đối xứng** (VD: 1 thẻ ngang lớn trên cùng + 1 thẻ dọc cao bên trái + 2 thẻ vuông nhỏ bên phải), mỗi ô có đồ họa 3D và cỡ chữ riêng biệt. | Bài khảo sát `A / B / C / D`, Checklist 4 việc, Phân loại vai trò AI. |

---

## 4. Quy Trình Kiểm Duyệt Trước Khi Xuất Bản (`QA Hard Gate`)

1. **Kiểm tra chống trùng lặp (`Visual Diff Check`):** Đặt các ảnh trong cùng ngày cạnh nhau — nếu có 2 ảnh nào nhìn lướt qua có cùng vị trí đặt chữ + cùng kiểu khung/vòng xoáy, `edit` **bắt buộc phải vẽ lại** bằng một Layout khác trong bảng Mục 3.
2. **Chính tả Tiếng Việt 100%:** Kiểm tra kỹ từng dấu tiếng Việt trước khi bàn giao.
