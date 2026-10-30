# Bộ Quy Tắc Vàng Dựng Video Giải Thích / Video Slide (`templates/remotion-cuongit-template`)

> **Trạng thái:** `VALIDATED — GOLDEN STANDARD (Đã huấn luyện & khóa cứng 5 Chốt chặn Zero-Clone ngày 2026-10-30)`  
> **Phạm vi áp dụng:** Toàn bộ Video Explainer, Tin tức AI, Giải mã công nghệ và Quy trình AI trên hệ thống **Agent-Javis** (đặc biệt là kênh **#04: AI Players — Người chơi hệ AI**).  
> **Mẫu chuẩn tham chiếu trực tiếp (Golden Reference Implementation):**  
> - Generator chuẩn 18 Kiến trúc Độc bản: `tools/build_18_truly_bespoke_zero_clone_reels.py`  
> - Cổng khóa cứng cấu trúc AST/JSX/SVG: `tools/zero_repost_gate.py --check-zero-clone` (`verify_zero_clone_tsx()`)

---

## 🏆 5 QUY TẮC VÀNG BẮT BUỘC (5 GOLDEN RULES — HARD GATES)

Mọi video dựng bằng `templates/remotion-cuongit-template` **BẮT BUỘC tuân thủ tuyệt đối 5 quy tắc sau**, sai bất kỳ mục nào sẽ bị đánh `HOLD/REJECT` ngay lập tức:

### Quy tắc 1: Hệ Màu Chữ Tiêu Đề `#87ff00` & Tài Nguyên `public/brand-kit/` (`brandTheme.ts`)
1. **Màu chữ tiêu đề chính (`Headline` ở cả 6 Scene) & Điểm nhấn chủ đạo:**
   - **BẮT BUỘC khóa cứng mã màu `#87ff00`** (`style={{ color: "#87ff00" }}` / `backgroundColor: "#87ff00"`).
   - Các màu chữ khác giữ nguyên độ tương phản cao trên nền xanh: chữ mô tả phụ `#FFFFFF` / `text-white/90`, chữ trong thẻ Card `#FFFFFF` & `text-white/85`.
   - Sub-heading trong các thẻ Card (đặc biệt ở Scene 6 Outro) phải căn chỉnh cỡ chữ (`text-[27px] whitespace-nowrap`) để nằm gọn trên 1 dòng, **tuyệt đối không để rớt 1 chữ lẻ xuống dòng thứ 2**.
2. **Hình nền (`BG`) & Tối ưu Dung lượng / Tốc độ Render (`CRF 23`, `--concurrency=2`):**
   - Nạp trực tiếp từ `staticFile("brand-kit/bg/BG-video-motion.jpg")`.
   - **CẤM phủ lớp nền đen làm tối màu xanh nguyên bản của ảnh nền.**
   - **Giữ ảnh nền `BG-video-motion.jpg` cố định sắc nét (`className="h-full w-full object-cover"`).** Chỉ cho 2 quầng sáng (`radial-gradient` màu `rgba(135,255,0,0.14)` và `rgba(56,189,248,0.18)`) trôi nổi phía trên ảnh nền kết hợp `--crf=23 --concurrency=2` để dung lượng MP4 luôn nhẹ **`~8–11 MB`** và CPU luôn mát.
3. **Nhạc nền (`BGM`) & Hiệu ứng âm thanh (`SFX`):**
   - **BGM:** Phát xuyên suốt `staticFile("brand-kit/bgm/1.The Violins.mp3")` ở mức âm lượng `volume={0.10}` (-18dB) để tôn giọng đọc.
   - **SFX Chuyển cảnh:** Chèn `staticFile("brand-kit/sfx/apple-pay-sound.mp3")` (`volume={0.26}`) ở đầu mỗi phân cảnh mới (Scene 2, 3, 4, 5, 6).
   - **SFX Bật Thẻ Card:** Chèn `staticFile("brand-kit/sfx/discord-notification.mp3")` (`volume={0.22}`) bọc trong `<Sequence from={25} durationInFrames={45}>` khi khối UI Card chính xuất hiện.

---

### Quy tắc 2: Khung Thẻ Kính Trong Suốt (`Transparent Frosted Glass` — Cấm Khung Đen) & Căn Trục Dọc Hài Hòa
1. **TUYỆT ĐỐI CẤM:** Dùng các khung nền đen đặc hoặc xám tối (`bg-slate-900/90`, `bg-slate-950`, `bg-rose-950/40`, `bg-emerald-950/40`, `bg-amber-950/40`) làm che khuất nền xanh `BG-video-motion.jpg`.
2. **Chuẩn Khung Kính Trong Suốt Bắt Buộc:**
   - **Thẻ bao ngoài (Main Container Card):** `rounded-[36px] border border-white/30 bg-white/[0.08] p-7 shadow-[0_16px_50px_rgba(0,0,0,0.25)] backdrop-blur-md`
   - **Thẻ con bên trong (Inner Item Card):** `rounded-2xl border border-white/25 bg-white/[0.10] p-5 backdrop-blur-sm`
   - **Huy hiệu Kênh Phía Trên (`BrandHeader` tại `top: 150px`):** `rounded-full border border-white/30 bg-white/10 px-8 py-3.5 shadow-[0_8px_30px_rgba(0,0,0,0.25)] backdrop-blur-md`
3. **Quy Tắc Căn Trục Dọc Hài Hòa (`justify-center gap-7 pt-[230px] pb-[435px]`):**
   - **CẤM dùng `justify-between`** trên toàn chiều cao `AbsoluteFill` (gây khoảng trống xanh mênh mông ở giữa màn hình và ép khối chữ đáy đè sát vào `SubtitleBox` tại `bottom-[380px]`).
   - **BẮT BUỘC dùng `flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white`** để các khối liên kết chặt chẽ ở tâm khung hình và cách dòng phụ đề đáy tối thiểu `60–80px`.

---

### Quy tắc 3: CẤM Lặp Lại Bố Cục & Element — 5 Chốt Chặn Kỹ Thuật Chống Nhân Bản (`Zero-Clone Bespoke Architecture — Hard Gate Bắt Buộc`)
1. **Chốt chặn #1 — Cấm tuyệt đối dùng chung Template Component hoặc Vòng lặp Chia dư `idx % N` (`idx % 3`, `idx % 2`):**
   - Cấm tạo component `DynamicShort` nhận JSON props.
   - **Cấm tuyệt đối** viết script Python xoay vòng một vài hàm builder (`builders[idx % 3]`) cho nhiều video. Mỗi video bắt buộc có hàm thiết kế `Scene1..Scene5` định danh `1-đối-1` theo đúng chủ đề kịch bản đó (`tools/build_18_truly_bespoke_zero_clone_reels.py`).
2. **Chốt chặn #2 — Đa dạng hóa 100% Bố cục Vĩ mô (`Macro Layout`) & Vị trí đặt Tiêu đề (`Header Placement`):**
   - **CẤM** đặt tiêu đề căn giữa ở đỉnh màn hình (`items-center text-center`) + 1 hộp chữ nhật bo góc ở giữa lặp đi lặp lại giữa các video!
   - Mỗi video phải thay đổi rõ rệt vị trí Tiêu đề & Kiểu chia không gian:
     + *Visual-First Top + Bottom-Left Header* (Đồ họa ở trên, Tiêu đề viền dọc `#87ff00` lệch trái ở dưới).
     + *Asymmetric Vertical Columns* (`col-span-5` Buồng thiết bị dọc bên trái + `col-span-7` Tiêu đề nghiêng căn phải & thẻ dữ liệu bên phải).
     + *3-Tier Sandwich Bridge* (Mảnh ghép đứt gãy ở đỉnh + Thanh cầu nối Tiêu đề `#87ff00` ở giữa + Đồ thị 3D ở đáy).
     + *Giant Metric Callout Split* (Khối chỉ số khổng lồ `300ms`, `5X`, `-50%` góc trên-trái + Tiêu đề căn phải + Sơ đồ Laser/Băng chuyền ở dưới).
     + *Top Code Terminal/IDE Window + Bottom Bracketed Title* (`[BUỒNG THỰC THI MÃ]`).
     + *Floating Search Bar + Stepped Indented Title + Open 3D XYZ Coordinate Space*.
     + *Twin Golden Anchor Pillars (`98%` & `99%`) Flanking Title + U-Shaped Attention Curve*.
     + *3-Column Olympic Podium / Dual-Track Horizontal Drag Race / Optical Triangle Prism Splitter / Tilted Mechanical Balance Scale / Inverted 3-Tier Funnel Pyramid*.
3. **Chốt chặn #3 — Cổng Khóa Cứng Tự Động AST/JSX/SVG (`verify_zero_clone_tsx()`):**
   - Ngay sau khi sinh hoặc sửa code `src/Reel*/Scene*.tsx`, bắt buộc chạy:
     `python "tools/zero_repost_gate.py" --check-zero-clone`
   - Nếu có bất kỳ 2 video nào trùng khung xương thẻ JSX/class bố cục hoặc trùng đường vẽ SVG `<path>`, lệnh sẽ báo `❌ CHẶN CỨNG [Zero-Clone Gate]` và dừng quy trình ngay lập tức.
4. **Chốt chặn #4 — Chụp nhanh `remotion still` (~25s) & Kiểm duyệt Mắt (`read_file` trên `QA Grid`) TRƯỚC khi Render `.mp4`:**
   - Tuyệt đối không render hàng loạt file `.mp4` hoặc đẩy thẳng lên Meta Graph API khi chưa chạy `remotion still --frame=75`, ghép vào `bespoke_21_reels_qa_grid.jpg` và dùng `read_file` tự kiểm tra bằng mắt.

---

### Quy tắc 4: Phụ Đề 1 Dòng Trượt Từ Dưới Lên — Không Khung Bao & Không Cắt Từ Ghép (`SubtitleBox.tsx`)
1. **Không Khung Bao Quanh Sub:**
   - **Bỏ hoàn toàn khung pill nền đen và icon loa `🎙️`.**
   - Chữ hiển thị trực tiếp trên nền video tại `bottom-[380px]` với `font-black`, màu trắng `#FFFFFF`, tự động tô sáng từ khóa quan trọng bằng màu **`#87ff00`**, và đổ bóng sắc nét.
2. **Hiệu Ứng Trượt Nguyên Cụm Từ Dưới Lên (`Whole-Phrase Slide-Up`) & Bảo Vệ Từ Ghép (`whitespace-nowrap`):**
   - Mỗi cụm phụ đề trượt đồng nhất từ dưới lên (`translateY: 36px -> 0px` bằng `spring`).
   - Sử dụng `whitespace-nowrap` kết hợp bộ từ điển `COMPOUND_PAIRS` trong `SubtitleBox.tsx` để không bao giờ cắt đôi từ ghép 2 âm tiết tiếng Việt.

---

### Quy tắc 5: Giọng Đọc Vbee AIVoice Thuần Việt & Studio Mastering (`tools/generate_voice_tts.py`)
1. **Định mức số từ khóa cứng theo tốc độ đọc Vbee (`~4.5 từ/giây`):**
   - Video **45 giây:** Tổng **195 – 205 từ** (Cảnh 1–5: 33 – 36 từ/cảnh; Cảnh 6 Outro: 25 – 28 từ).
2. **Lời thoại 100% Tiếng Việt tự nhiên & Khóa đỉnh âm lượng `-3dB`.**

---

## 🛠️ Quy Trình Kiểm Duyệt & Lệnh Render Chuẩn Trên Máy Windows

```powershell
# Bước 1: Kiểm tra cổng cấu trúc Zero-Clone (BẮT BUỘC PASS 100%)
python "d:\Phiên bản Ai agent\Subagent\tools\zero_repost_gate.py" --check-zero-clone

# Bước 2: Chụp ảnh tĩnh QA & Kiểm duyệt mắt trước khi render MP4
# Bước 3: Render MP4 với giới hạn CPU mát (--concurrency=2 --crf=23)
python "d:\Phiên bản Ai agent\Subagent\tools\render_and_schedule_remaining_18_golden_reels.py"
```
