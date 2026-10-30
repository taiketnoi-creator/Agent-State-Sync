---
id: MEM-20261020-ai-players-image-style-guide
title: "Quy chuẩn Thiết Kế Ảnh Bài Đăng Page AI Players — Luật Cứng Zero-Clone Bespoke Image Design (Không Thiết Kế Nào Được Giống Nhau)"
type: decision
status: VALIDATED
confidence: high
source: "CEO chỉ đạo trực tiếp ngày 2026-10-30: Thiết lập quy tắc không thiết kế nào được giống nhau, xóa bỏ việc lặp lại 5 Master Templates"
created_at: 2026-10-20
updated_at: 2026-10-30
owner: bo-nao-thu-2
tags: [ai-players, image-style, zero-clone-image, bespoke-layout, headless-chrome, anti-clone, edit]
scope: "Áp dụng bắt buộc 100% cho toàn bộ ảnh bài đăng vuông 1:1 (1080x1080) trên Page AI Players - Người chơi hệ AI."
---

## Nội dung quyết định đã xác thực (Cập nhật Luật Cứng Zero-Clone 2026-10-30)

1. **XÓA BỎ VĨNH VIỄN Quy Tắc Cũ "Luân phiên 5 Master Templates":**
   - Nguyên nhân khiến ảnh trên Page `AI Players` bị na ná nhau trước đây là do xoay vòng 5 hàm template cố định (`Template 1..5`: Hộp Vàng + Đường Hầm, Bảng 4 hàng `01–04`, Lưới `2×2 + CORE`, Hộp `100% MIỄN PHÍ`, Thanh tiến độ).
   - Kể từ `2026-10-30`, **NGHIÊM CẤM TUYỆT ĐỐI** việc dùng chung bất kỳ hàm HTML/CSS template nào cho 2 bài đăng khác nhau!

2. **5 Chốt Chặn Cứng Cho Thiết Kế Ảnh Độc Bản (`100% Bespoke Per-Post Visual Architecture`):**
   - **Chốt chặn #1 — `1 Bài Ảnh = 1 Kiến Trúc Không Gian Độc Bản (Zero Shared Skeleton)`:**
     Mỗi bài đăng (`1080×1080`) bắt buộc được thiết kế bằng cấu trúc bố cục riêng biệt hoàn toàn:
     + *Bố cục Đối đầu Chéo góc (Diagonal VS Split Arena)*
     + *Bố cục Radar Đồng tâm 360° (Concentric Sonar & Orbital Nodes)*
     + *Bố cục Kim tự tháp Phân tầng 3D (3-Tier Isometric Hierarchy Pyramid)*
     + *Bố cục Màn hình IDE & Terminal Thực chiến (Dual-Pane Code & Live Output)*
     + *Bố cục Sơ đồ Phễu Chuyển đổi Dọc (3-Stage Conversion Funnel)*
     + *Bố cục Giải phẫu X-Ray 3 Lớp (3-Layer Deep Anatomy Stack)*
     + *Bố cục Bảng điều khiển Đồng hồ Đo (Cockpit Speedometer & Telemetry Gauges)*
     + *Bố cục Đường ống Dây chuyền Ngang (Horizontal Pipeline & Gatekeepers)*
     + *Bố cục Sơ đồ Tư duy Tỏa nhánh (Central Brain Radial Mindmap)*
     + *Bố cục Bục Vinh danh 3 Cột (3-Pillar Benchmark Podium)*
     + *Bố cục Lưới Tổ ong Lục giác (Hexagonal Mesh Network)*
     + *Bố cục Bản vẽ Kỹ thuật Blueprint (Engineering CAD Blueprint Grid)*
   - **Chốt chặn #2 — Đa Dạng Hóa Bảng Màu & Khí Quyển Nền (`Distinct Color & Atmosphere Themes`):**
     Cấm đóng khung mọi bài vào đúng 1 cặp màu Vàng Chanh `#D4FF00` + Hồng `#F42F6C` ở cùng một vị trí! Mỗi bài liền kề phải có phối màu chủ đạo & ánh sáng nền khác biệt rõ rệt:
     + *Theme A:* `Cyber Acid Lime (#D4FF00) & Deep Obsidian (#080A0F)`
     + *Theme B:* `Electric Cyan (#00F0FF) & Midnight Sapphire (#06101E)`
     + *Theme C:* `Neon Magenta (#FF2A85) & Royal Violet (#120824)`
     + *Theme D:* `Solar Amber (#FFB800) & Forged Carbon (#12100B)`
     + *Theme E:* `Emerald Matrix (#00FF88) & Dark Cyber Slate (#071410)`
     + *Theme F:* `Crimson Laser (#FF3355) & Titanium Gunmetal (#101218)`
   - **Chốt chặn #3 — Font Offline 100% (`brand-kit/fonts/local_ttf_fonts.css`) & Không Lỗi Tiếng Việt.**
   - **Chốt chặn #4 — Cổng Kiểm Định Tự Động `verify_zero_clone_images()` (`tools/zero_repost_gate.py`):**
     Bắt buộc chạy `python tools/zero_repost_gate.py --check-zero-clone-images` trước khi xuất bản. Cổng chia ảnh thành `8×8 = 64` vùng không gian để đo phân bố khối màu và hình học; nếu bất kỳ 2 ảnh nào giống nhau `> 58%` sẽ bị chặn cứng ngay lập tức.
   - **Chốt chặn #5 — Kiểm Duyệt Bằng Mắt Qua `QA Grid` (`read_file`) Trước Khi Lên Lịch.**
