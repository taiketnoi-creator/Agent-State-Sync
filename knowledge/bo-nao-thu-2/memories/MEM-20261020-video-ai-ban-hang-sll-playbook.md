# MEM-20261020-video-ai-ban-hang-sll-playbook — Quy Chuẩn Sản Xuất Video AI Bán Hàng SLL Đa Sản Phẩm (Phong Cách TVC Hybrid A-Roll + B-Roll)

- **ID:** `MEM-20261020-video-ai-ban-hang-sll-playbook`
- **Loại:** `decision`
- **Trạng thái:** `VALIDATED`
- **Ngày chốt:** `2026-10-20`
- **Nguồn phê duyệt:** CEO phê duyệt qua phân tích thực chiến video mẫu `C:\Users\Admin\Downloads\Video Ai\video AI đồ gia dụng.mp4` (`UNIE USC308` — `41.84s`)
- **Tài liệu quy chuẩn chi tiết:** `knowledge/quy-chuan-video-ai-ban-hang-sll.md`
- **Phạm vi áp dụng:** Toàn bộ chiến dịch **Video AI Bán Hàng Số Lượng Lớn (`VIDEO_AI_BAN_HANG` SLL)** áp dụng cho nhiều sản phẩm/ngành hàng khác nhau trên hệ thống `Agent-Javis` và `Google Flow`.

---

## Nội Dung Quyết Định Cốt Lõi

1. **Khung Xương 8 Nhịp Chuẩn TVC Thương Mại (`Hybrid A-Roll ↔ B-Roll Sandwich`):**
   - Không làm video chỉ có nhân vật đứng nói đơn điệu. Mọi video bán hàng cho bất kỳ sản phẩm nào đều tuân theo cấu trúc 8 nhịp (`32–42 giây`):
     - **Nhịp 1 (`00.0–01.5s` | Shock Hook):** 0.5s cận cảnh nỗi đau/sự cố cắt nhanh sang 1.0s gương mặt MC nhăn trán + Chữ Pop-up **`CHÚ Ý!`** viền đen-đỏ.
     - **Nhịp 2 (`01.5–07.0s` | Pain & Time Pressure):** MC xử lý công việc thủ công mệt mỏi, phía sau có đạo cụ áp lực thời gian (đồng hồ treo tường).
     - **Nhịp 3 (`07.0–13.5s` | Hero Product Reveal):** Không gian sáng hiện đại, MC tươi cười chỉ tay vào sản phẩm chính trên bàn, zoom cận sản phẩm.
     - **Nhịp 4 (`13.5–17.0s` | B-Roll Action 1):** Cận cảnh mở nắp / bật máy / kích hoạt cơ chế sản phẩm.
     - **Nhịp 5 (`17.0–23.5s` | B-Roll Result 2):** 2 cảnh cận cảnh liên tiếp chứng minh kết quả đầu ra hoàn hảo + gắn cố định Logo góc trên phải.
     - **Nhịp 6 (`23.5–31.0s` | B-Roll Control 3):** Cận cảnh ngón tay bấm nút điều khiển / thao tác 1 chạm dễ dàng.
     - **Nhịp 7 (`31.0–35.0s` | Trust & Warranty Shield):** Zoom cận sản phẩm + bật **Huy hiệu Khiên Vàng 3D (`BẢO HÀNH CHÍNH HÃNG / CAM KẾT CHẤT LƯỢNG`)** giữa màn hình.
     - **Nhịp 8 (`35.0–41.0s` | Happy Payoff & CTA):** Nhân vật/gia đình tận hưởng thành quả thảnh thơi + Thanh CTA điều hướng bình luận ghim/giỏ hàng.

2. **Khắc Phục Triệt Để 4 Lỗi AI Của Video Mẫu:**
   - **Cấm dùng AI vẽ chữ tiếng Việt lên nút bấm hoặc vẽ màn hình End-Card cuối video** (tránh lỗi chữ vô nghĩa như cuối video mẫu). Toàn bộ chữ `CHÚ Ý!`, Callout tính năng, Khiên Bảo Hành 3D, Phụ đề 1 dòng và Thanh CTA cuối phải đóng bằng lớp hậu kỳ **Remotion / FFmpeg / CapCut Template**.
   - **Chống biến dạng sản phẩm (`SKU Drift`):** Mọi cảnh có sản phẩm trong Google Flow đều phải truyền `Ảnh Sản Phẩm Gốc` làm Reference và khóa `Rigid product geometry, exact lid/body from reference, zero morphing`.
   - **Xử lý âm thanh mượt 100%:** Cắt bỏ khoảng lặng đầu/cuối từng clip hoặc dùng 1 track Voiceover chủ đạo (`tools/generate_voice_tts.py` — Vbee Studio Mastering `-3dB`) đè lên chuỗi B-Roll.

3. **Cơ Chế Nhân Bản Số Lượng Lớn (SLL) Cho Nhiều Sản Phẩm:**
   - **Nhân bản chiều sâu (1 SKU $\rightarrow$ 12–20 Video):** Tạo 1 bộ nguyên liệu trên Google Flow (`4 Hook/Pain` + `2 Hero` + `4 B-Roll dùng chung` + `2 CTA`), sau đó dùng `ffmpeg_render.py --scenes-dir --batch-count 12` tự động đảo tổ hợp và thay giọng đọc Vbee Bắc/Nam.
   - **Nhân bản chiều rộng (Đa sản phẩm):** Giữ cố định `Hồ sơ Creator` và `Khuôn mẫu Hậu kỳ 8 Nhịp`, chỉ thay `Ảnh Sản Phẩm Mới + 3 Thông số thật + Bảng ánh xạ ngành hàng`.
