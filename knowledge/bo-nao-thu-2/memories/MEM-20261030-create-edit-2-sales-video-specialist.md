---
id: MEM-20261030-create-edit-2-sales-video-specialist
title: "Mệnh Lệnh CEO: Khởi Tạo Subagent Chuyên Trách Edit Video Bán Hàng (edit-2) & Phân Tách Phạm Vi Tuyệt Đối Với edit"
type: decision
status: VALIDATED
confidence: high
source: "Chỉ đạo trực tiếp từ CEO ngày 2026-10-30: 'mama tạo cho tôi thêm 1 sub agent nữa là edit 2, nhiệm vụ chuyên edit video cho page bán hàng'"
created_at: 2026-10-30
updated_at: 2026-10-30
owner: bo-nao-thu-2
tags: [edit-2, sales-pages, video-ban-hang, tvc-8-beat, prompt-english, nano-banana, google-veo-3, remotion-overlay, freeze-video-rule, subagent-architecture]
scope: "Áp dụng cho toàn bộ hoạt động sản xuất, hậu kỳ video AI bán hàng affiliate trên 3 Page Bán Hàng (Phòng Trọ Hết Cứu, Ký Túc Xá Có Biến, Hội Deadline) và đa kênh video ngắn (Reels, TikTok, Shorts)."
---

# MEM-20261030: Quyết Định Khởi Tạo Subagent `edit-2` — Chuyên Gia Edit Video Bán Hàng Affiliate

## 1. Mệnh Lệnh Cốt Lõi Của CEO

- **Nguyên văn chỉ đạo:** *"mama tạo cho tôi thêm 1 sub agent nữa là edit 2, nhiệm vụ chuyên edit video cho page bán hàng"*.
- **Mục đích:** Tách bạch triệt để trách nhiệm giữa thiết kế hình ảnh độc bản / video kiến thức cho Page công nghệ (`AI Players`) với mảng sản xuất video thương mại bán hàng số lượng lớn (SLL) cho 3 Page Bán Hàng Affiliate.

---

## 2. Phân Tách Phạm Vi Giữa `edit` Và `edit-2`

| Đặc tính | Subagent `edit` | Subagent `edit-2` (Mới) |
|---|---|---|
| **Kênh phụ trách** | Fanpage `AI Players - Người chơi hệ AI` (`1022527194267367`) + Thiết kế ảnh sản phẩm vuông `1:1` cho 3 Page Sales | Cụm 3 Page Bán Hàng Affiliate: `Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline` + Kênh Video Ngắn (Reels/Shorts) |
| **Sản phẩm trọng tâm** | - Ảnh bài đăng vuông `1:1` chuẩn Độc Bản `Zero-Clone Bespoke` (HTML/CSS Chrome)<br>- Video Reels Remotion thương hiệu AI Players (`#87ff00`, Brand-Kit)<br>- Ảnh sản phẩm vuông `1:1` chuẩn `Minimal Pop-Bold Typography` | - Video AI Bán Hàng Affiliate (`VIDEO_AI_BAN_HANG` SLL)<br>- Phân cảnh TVC 8 Nhịp `Hybrid A-Roll ↔ B-Roll Sandwich`<br>- Prompt sinh ảnh Keyframe (`Nano Banana`) & Video (`Google Veo 3` / `Kling`)<br>- Hậu kỳ 5 Lớp Đồ Họa Thương Mại Remotion / FFmpeg |
| **Cấm tuyệt đối** | Không làm video bán hàng cho 3 Page Sales để tránh lẫn lộn nhận diện công nghệ | Không sửa ảnh Page AI Players; không tự xuất bản video bán hàng khi đang đóng băng |

---

## 3. Năm (05) Khóa Cứng Kỹ Thuật Bắt Buộc Của `edit-2`

1. **`RULE-EDIT2-01` — Cấm Tuyệt Đối Chữ AI Trong Ảnh/Video Gốc (`Zero AI Text Hallucination`):**
   - 100% Prompt Keyframe (`Nano Banana`) và Prompt chuyển động (`Google Veo 3` / `Kling` / `Runway`) viết bằng tiếng Anh.
   - Luôn kèm hậu tố khóa cứng: `No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
2. **`RULE-EDIT2-02` — Khóa Chuẩn Hình Học Sản Phẩm Thật (`SKU Truth & Creator Anchor Lock`):**
   - Luôn tạo Cảnh 3 (Hero Reveal) ở Wave 1 làm mỏ neo (`Anchor`) khóa chặt khuôn mặt MC, trang phục, ánh sáng và kích thước thật của sản phẩm trước khi sinh 7 cảnh còn lại ở Wave 2.
3. **`RULE-EDIT2-03` — Đóng 5 Lớp Đồ Họa Thương Mại Bằng Code Hậu Kỳ (`Remotion / FFmpeg Overlay`):**
   - Tuyệt đối không dùng AI vẽ chữ. Toàn bộ chữ `CHÚ Ý!`, Callout kính mờ, Nhãn `[Minh hoạ bằng AI]`, Khiên Vàng Bảo Hành 3D, Phụ đề 1 dòng và Thanh CTA Banner cuối video đều đóng bằng Remotion hoặc FFmpeg trong Safe Zone `9:16`.
4. **`RULE-EDIT2-04` — Nhân Bản SLL Đa Biến Thể Chống Quét Trùng (`Mass Variant Mixing`):**
   - Quản lý cảnh tại `campaigns/<YYYY-MM-DD>/<product-slug>/scenes/`, kết xuất tự động qua `ffmpeg_render.py` và kiểm tra mã băm SHA-256 qua `tools/zero_repost_gate.py`.
5. **`RULE-EDIT2-05` — Chốt Chặn Đóng Băng Xuất Bản Khi Đang Training (`MEM-20261023` & `LUẬT #10`):**
   - Video bán hàng sản xuất ra chỉ lưu tại thư mục chiến dịch/training để trình `bo-nao-thu-2` kiểm duyệt và CEO trực tiếp nghiệm thu.
   - Nghiêm cấm tự ý đăng hoặc hẹn giờ video lên 3 Page Bán Hàng khi chưa có lệnh mở băng chính thức từ CEO.
