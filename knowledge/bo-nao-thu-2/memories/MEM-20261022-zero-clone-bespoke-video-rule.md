# MEM-20261022-zero-clone-bespoke-video-rule

- **ID:** `MEM-20261022-zero-clone-bespoke-video-rule`
- **Tiêu đề:** Luật Bắt Buộc Của CEO: Không Video Nào Giống Video Nào — 5 Chốt Chặn Cứng Chống Nhân Bản Bố Cục & Element (`Zero-Clone Bespoke Gate`)
- **Loại:** `decision`
- **Trạng thái:** `VALIDATED`
- **Ngày ghi nhận:** `2026-10-22` (Cập nhật khóa cứng 5 Chốt chặn Kỹ thuật ngày `2026-10-30`)
- **Nguồn:** Lệnh trực tiếp từ CEO (`"cập nhật nguyên tắc này cho edit nhé, đừng tạo nhầm 1 lần nào nữa"`)
- **Phạm vi áp dụng:** Toàn bộ các video sản xuất từ nay về sau (`mama`, `edit`, `content`, `edit.md`, `.agents/plugins/agent-javis/agents/edit.md` và `knowledge/quy-chuan-remotion-cuongit-template.md`)

## 5 Chốt Chặn Kỹ Thuật Bắt Buộc (Cấm Tái Phạm Dưới Mọi Hình Thức)

1. **Chốt chặn #1 — Cấm tuyệt đối dùng chung Template Component hoặc Vòng lặp Chia dư `idx % N` (`idx % 3`, `idx % 2`):**
   - Cấm tạo một component `DynamicShort` dùng chung nhận mảng JSON.
   - **Cấm tuyệt đối** viết script Python xoay vòng một vài hàm builder (`builders[idx % 3]`) cho nhiều video khiến các video lặp lại cùng 1 hình vẽ radar, sóng âm hay 2 hộp song song.
   - Mỗi video phải là 1 Composition độc lập (`src/<UniqueVideoSlug>/Scene1..Scene6.tsx`) với hàm thiết kế định danh `1-đối-1` theo đúng chủ đề kịch bản đó (chuẩn tham chiếu: `tools/build_18_truly_bespoke_zero_clone_reels.py`).

2. **Chốt chặn #2 — Đa dạng hóa 100% Bố cục Vĩ mô (`Macro Layout`) & Vị trí đặt Tiêu đề (`Header Placement`):**
   - **Cấm** đặt tiêu đề căn giữa ở đỉnh màn hình (`items-center text-center`) + 1 khung chữ nhật bo góc ở giữa lặp đi lặp lại giữa các video!
   - Bắt buộc biến hóa vị trí Tiêu đề & Kiểu chia khung hình giữa các video:
     + *Visual-First Top + Bottom-Left Header* (Đồ họa ở trên, Tiêu đề viền dọc `#87ff00` lệch trái ở dưới).
     + *Asymmetric Vertical Columns* (`col-span-5` Buồng thu âm/Thiết bị dọc bên trái + `col-span-7` Tiêu đề nghiêng căn phải & thẻ dữ liệu bên phải).
     + *3-Tier Sandwich Bridge* (Mảnh ghép đứt gãy ở đỉnh + Thanh cầu nối Tiêu đề `#87ff00` ở giữa + Đồ thị mạng lưới 3D ở đáy).
     + *Giant Metric Callout Split* (Khối chỉ số khổng lồ `300ms`, `5X`, `-50%` góc trên-trái + Tiêu đề căn phải + Sơ đồ Laser/Băng chuyền ở dưới).
     + *Top Code Terminal/IDE Window + Bottom Bracketed Title* (`[BUỒNG THỰC THI MÃ]`).
     + *Floating Search Bar + Stepped Indented Title + Open 3D XYZ Coordinate Space*.
     + *Twin Golden Anchor Pillars (`98%` & `99%`) Flanking Title + U-Shaped Attention Curve*.
     + *3-Column Olympic Podium / Dual-Track Horizontal Drag Race / Optical Triangle Prism Splitter / Tilted Mechanical Balance Scale / Inverted 3-Tier Funnel Pyramid*.

3. **Chốt chặn #3 — Căn trục dọc Hài hòa (`justify-center gap-7 pt-[230px] pb-[435px]`):**
   - **Cấm** dùng `justify-between` trên toàn chiều cao `AbsoluteFill` (gây khoảng trống xanh mênh mông ở giữa màn hình và đẩy khối chữ đáy đè sát vào `SubtitleBox` tại `bottom-[380px]`).
   - Bắt buộc dùng `flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px]` để các khối liên kết chặt chẽ ở tâm khung hình và cách dòng phụ đề đáy tối thiểu `60–80px`.

4. **Chốt chặn #4 — Cổng Kiểm tra Cấu trúc Tự động AST/JSX/SVG (`verify_zero_clone_tsx()`):**
   - Trước mọi lần bundle/render, bắt buộc chạy `python "tools/zero_repost_gate.py" --check-zero-clone`.
   - Hàm `verify_zero_clone_tsx()` tự động bóc tách khung xương thẻ JSX/class bố cục và chữ ký đường vẽ `<path d="...">` trên toàn bộ `src/Reel*/Scene1..Scene5.tsx`. Nếu phát hiện bất kỳ 2 video nào trùng cấu trúc hoặc dùng lại đường vẽ SVG, hệ thống lập tức báo lỗi đỏ `CHẶN CỨNG [Zero-Clone Gate]` và dừng quy trình.

5. **Chốt chặn #5 — Kết xuất Ảnh tĩnh `remotion still` (~25s) & Kiểm duyệt Mắt (`read_file` trên `QA Grid`) TRƯỚC khi Render `.mp4`:**
   - Tuyệt đối không render hàng loạt file `.mp4` hoặc đẩy thẳng lên Meta Graph API khi chưa dùng `remotion still --frame=75` kết xuất ảnh mẫu ghép vào `bespoke_21_reels_qa_grid.jpg` và dùng `read_file` tự kiểm tra trực quan bằng mắt.
