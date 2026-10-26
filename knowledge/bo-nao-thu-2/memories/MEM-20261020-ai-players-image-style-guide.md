---
id: MEM-20261020-ai-players-image-style-guide
title: "Quy chuẩn Thiết Kế Ảnh Bài Đăng Page AI Players Theo Phong Cách Cyber-Grid Carbon–Lime–Pink (Downloads\\vid Style — 5 Templates Render Qua Headless Chrome)"
type: decision
status: VALIDATED
confidence: high
source: "CEO huấn luyện & phê duyệt bộ mẫu Downloads\\vid (ref_1 -> ref_8) chiều 2026-10-26"
created_at: 2026-10-20
updated_at: 2026-10-26
owner: bo-nao-thu-2
tags: [ai-players, image-style, vid-style, carbon-lime-pink, headless-chrome, render-vid-style-card, anti-clone, edit]
scope: "Áp dụng bắt buộc 100% cho toàn bộ ảnh bài đăng vuông 1:1 (1080x1080) trên Page AI Players - Người chơi hệ AI."
---

## Nội dung quyết định đã xác thực (Cập nhật chuẩn `Downloads\vid` chiều 2026-10-26)

CEO đã huấn luyện và chuyển đổi 100% phong cách ảnh bài đăng của Page `AI Players - Người chơi hệ AI` sang chuẩn **`Downloads\vid` (`ref_1` $\rightarrow$ `ref_8`)**, kết xuất trực tiếp bằng Headless Chrome HTML/CSS/SVG Engine tại `tools/render_vid_style_card.py` và `tools/generate_weekly_vid_vault.py`:

1. **Hệ màu & Chất liệu (`Cyber-Grid Carbon • Neon Lime • Hot Pink • Crisp White`):**
   - **Nền chính (`Background`):** Đen Carbon sâu (`#07080a`) phủ lưới caro chìm (`#111317` checkered grid `72×72px`) + quầng sáng trung tâm.
   - **Bảng màu chủ đạo:** Xanh Chuối Điện Tử (`#CCFF00`), Hồng Neon (`#FF2A6D`), Trắng Tinh (`#FFFFFF`) và Đen Tuyền (`#000000`).
   - **Typography & Badge:** Font `Montserrat 800/900` + `Chakra Petch 900` + `Inter`; nhãn nghiêng màu hồng `#FF2A6D` (`skewX(-14deg)`) đính sao `✦`; tiêu đề đóng ngoặc vuông `[ ... ]` phối 3 màu Chuối–Trắng–Hồng; logo hoa thị 8 hướng `#CCFF00` và con trỏ chuột vector `↖`.
2. **5 Kiến Trúc Bố Cục Chuẩn `Downloads\vid` Luân Phiên (`5 Master Templates`):**
   - **Template #1 (`Hero Showcase — Tool Lime Card + Neon Grid Tunnel`):** Thẻ lớn `#CCFF00` kèm Icon App 3D bóng kính ở trên + Đường hầm lưới phối cảnh 3D Neon chứa tên Model phát sáng ở dưới.
   - **Template #2 (`Curriculum 4-Item Breakdown`):** Bảng 4 hàng kẻ chỉ mảnh `#CCFF00` với cột số thứ tự khổng lồ `01–04` màu `#CCFF00` bên trái và nội dung có từ khóa highlight màu hồng `#FF2A6D` bên phải.
   - **Template #3 (`2×2 Feature Matrix & Asterisk Branding`):** Tiêu đề đóng ngoặc vuông `[ ... ]` + Ma trận `2×2` gồm 4 ô Pill viền mảnh chứa Icon `#CCFF00` + Footer gắn Logo Hoa thị 8 hướng.
   - **Template #4 (`Offer / Lead Magnet Card`):** Khung thẻ có dải đỉnh `#CCFF00`, 4 ngàm góc hồng `Corner Brackets`, 3 ô thẻ thông số ngang và nút CTA lớn `#CCFF00` kèm con trỏ chuột.
   - **Template #5 (`Urgency / Sold Out Slots`):** Tiêu đề lớn phát sáng trắng + các thanh tiến độ (`Progress Bars` màu hồng `#FF2A6D`) + nút Pill hồng trung tâm + thẻ ưu đãi viền `#CCFF00` ở đáy.
3. **Lệnh cấm tuyệt đối:**
   - Cấm dùng `Pillow` (`draw.rectangle`) vẽ hộp 2D thô cứng; cấm dùng lại phong cách nền xanh Cobalt cũ; cấm cắt mất viền dưới ảnh (`Zero-Cutoff 1080×1080`).
