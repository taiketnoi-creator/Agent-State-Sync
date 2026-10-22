# Bộ Quy Tắc Vàng Dựng Video Giải Thích / Video Slide (`templates/remotion-cuongit-template`)

> **Trạng thái:** `VALIDATED — GOLDEN STANDARD (Đã huấn luyện & nghiệm thu thực chiến 100% cùng CEO ngày 2026-10-20)`  
> **Phạm vi áp dụng:** Toàn bộ Video Explainer, Tin tức AI, Giải mã công nghệ và Quy trình AI trên hệ thống **Agent-Javis** (đặc biệt là kênh **#04: AI Players — Người chơi hệ AI**).  
> **Mẫu chuẩn tham chiếu trực tiếp (Golden Reference Implementation):**  
> - Source code chuẩn: `templates/remotion-cuongit-template/src/AiHallucinationShort/` & `src/brandTheme.ts`  
> - Video thành phẩm mẫu: `campaigns/2026-10-20/ai-hallucination-45s/ai-hallucination-45s.mp4` (`43.58s` / `1.306 frames @ 30fps`)

---

## 🏆 5 QUY TẮC VÀNG BẮT BUỘC (5 GOLDEN RULES — HARD GATES)

Mọi video dựng bằng `templates/remotion-cuongit-template` **BẮT BUỘC tuân thủ tuyệt đối 5 quy tắc sau**, sai bất kỳ mục nào sẽ bị đánh `HOLD/REJECT` ngay lập tức:

### Quy tắc 1: Hệ Màu Chữ Tiêu Đề `#87ff00` & Tài Nguyên `public/brand-kit/` (`brandTheme.ts`)
1. **Màu chữ tiêu đề chính (`Headline` ở cả 6 Scene) & Điểm nhấn chủ đạo:**
   - **BẮT BUỘC khóa cứng mã màu `#87ff00`** (`style={{ color: "#87ff00" }}` / `backgroundColor: "#87ff00"`).
   - Các màu chữ khác giữ nguyên độ tương phản cao trên nền xanh: chữ mô tả phụ `#FFFFFF` / `text-white/90`, chữ trong thẻ Card `#FFFFFF` & `text-white/85`.
   - Sub-heading trong các thẻ Card (đặc biệt ở Scene 6 Outro) phải căn chỉnh cỡ chữ (`text-[27px] whitespace-nowrap`) để nằm gọn trên 1 dòng, **tuyệt đối không để rớt 1 chữ lẻ xuống dòng thứ 2**.
2. **Hình nền (`BG`) & Tối ưu Dung lượng / Tốc độ Render (`CRF 23`):**
   - Nạp trực tiếp từ `staticFile("brand-kit/bg/BG-video-motion.jpg")`.
   - **CẤM phủ lớp nền đen làm tối màu xanh nguyên bản của ảnh nền.**
   - **Giữ ảnh nền `BG-video-motion.jpg` cố định sắc nét (`className="h-full w-full object-cover"`, CẤM áp dụng `scale/translate` lên ảnh nền có hạt grain vì sẽ làm phình bitrate H.264 lên gấp 10 lần và làm chậm `backdrop-blur-md`).** Chỉ cho 2 quầng sáng (`radial-gradient` màu `rgba(135,255,0,0.14)` và `rgba(56,189,248,0.18)`) trôi nổi phía trên ảnh nền kết hợp `Config.setCrf(23)` và `Config.setConcurrency("50%")` trong `remotion.config.ts` để dung lượng MP4 luôn nhẹ **`~5–10 MB`** và tốc độ render nhanh gấp 2–3 lần.
3. **Nhạc nền (`BGM`) & Hiệu ứng âm thanh (`SFX`):**
   - **BGM:** Phát xuyên suốt `staticFile("brand-kit/bgm/1.The Violins.mp3")` ở mức âm lượng `volume={0.10}` (-18dB) để tôn giọng đọc.
   - **SFX Chuyển cảnh:** Chèn `staticFile("brand-kit/sfx/apple-pay-sound.mp3")` (`volume={0.26}`) ở đầu mỗi phân cảnh mới (Scene 2, 3, 4, 5, 6).
   - **SFX Bật Thẻ Card:** Chèn `staticFile("brand-kit/sfx/discord-notification.mp3")` (`volume={0.22}`) bọc trong `<Sequence from={25} durationInFrames={45}>` khi khối UI Card chính xuất hiện.

---

### Quy tắc 2: Khung Thẻ Kính Trong Suốt (`Transparent Frosted Glass` — Cấm Khung Đen)
1. **TUYỆT ĐỐI CẤM:** Dùng các khung nền đen đặc hoặc xám tối (`bg-slate-900/90`, `bg-slate-950`, `bg-rose-950/40`, `bg-emerald-950/40`, `bg-amber-950/40`) làm che khuất nền xanh `BG-video-motion.jpg`.
2. **Chuẩn Khung Kính Trong Suốt Bắt Buộc:**
   - **Thẻ bao ngoài (Main Container Card):** `rounded-3xl border border-white/30 bg-white/[0.08] p-8 shadow-[0_16px_50px_rgba(0,0,0,0.25)] backdrop-blur-md`
   - **Thẻ con bên trong (Inner Item Card):** `rounded-2xl border border-white/25 bg-white/[0.10] px-6 py-5 backdrop-blur-sm`
   - **Huy hiệu Kênh Phía Trên (`BrandHeader` tại `top: 150px`) & Top Badge:** `rounded-full border border-white/30 bg-white/10 px-8 py-3.5 shadow-[0_8px_30px_rgba(0,0,0,0.25)] backdrop-blur-md`

---

### Quy tắc 3: CẤM Lặp Lại Bố Cục & Element — Bắt Buộc 100% Độc Bản Toàn Diện Cho Từng Video (`Zero-Clone Bespoke Architecture — Hard Gate Bắt Buộc`)
1. **LUẬT CỨNG TỪ CEO (2026-10-22): KHÔNG VIDEO NÀO ĐƯỢC GIỐNG VIDEO NÀO TỪ ELEMENT, BỐ CỤC, ANIMATION ĐẾN TEXT!**
   - **Phần cố định duy nhất (`Brand Shell`):** Nền xanh `BG-video-motion.jpg` + 2 quầng sáng Neon, mã màu điểm nhấn `#87ff00`, chất liệu kính trong suốt (không khung đen), `BrandHeader`, `SubtitleBox` 1 dòng ở đáy (`bottom-56`), BGM & SFX, giọng Vbee `-3dB`.
   - **TUYỆT ĐỐI CẤM dùng chung 1 Component/Template tham số hóa (`Dynamic Template` nhận JSON props) cho nhiều video khác nhau!**
   - **BẮT BUỘC mỗi video mới phải được `edit` code thành 1 thư mục Composition độc lập (`src/<TenVideoRieng>/` gồm `Scene1.tsx .. Scene6.tsx`)** với:
     + **100% Khác Biệt Về Element Đồ Họa (`Bespoke Graphic Elements`):** Mỗi video phải tự vẽ SVG / UI / 3D / Biểu đồ / Mockup hoàn toàn mới theo đúng câu chuyện của kịch bản đó (không tái sử dụng lại khối thẻ hay hình vẽ của bất kỳ video nào trước đó).
     + **100% Khác Biệt Về Cách Bố Cục (`Varied Macro & Micro Layouts`):** Thay đổi vị trí đặt tiêu đề (trên / dưới / lệch trái / lệch phải / lồng trong đồ họa), thay đổi cấu trúc không gian (bất đối xứng, tròn đồng tâm, phân tầng tam giác, trục thời gian ngang, khung thiết bị dọc, sơ đồ cây, v.v.).
     + **100% Khác Biệt Về Chuyển Động (`Unique Animation Choreography`):** Mỗi video và mỗi phân cảnh phải có quỹ đạo chuyển động riêng (quay kim đồng hồ, quét tia laser, lật 3D perspective, con trỏ chuột di chuyển & click sóng âm, hạt dữ liệu chạy dọc đường cong Bezier, v.v.).
     + **100% Khác Biệt Về Trình Bày Text (`Typography & Callout Hierarchy`):** Cách trình bày chữ, nhãn badge, con số thống kê phải biến hóa theo đúng thiết kế của video đó.
2. **Kho 10+ Khuôn Mẫu Thị Giác Sáng Tạo (`Creative Visual Archetypes`) để `edit` biến hóa linh hoạt:**
   - **Bản đồ & Mạng lưới (Orbital Map / Node Constellation):** Vòng quỹ đạo xoay 360°, các điểm nút (Nodes) nối bằng tia laser SVG (`strokeDashoffset` chạy liên tục), sóng định vị tỏa tròn.
   - **Lưới Bento Đa Chiều (`2x2 Bento Grid` / `Asymmetric Masonry`):** Chia 4 ô vuông hoặc 1 ô lớn + 2 ô nhỏ bất đối xứng; cảnh đầu zoom/sáng ô 1–2, cảnh sau chuyển tâm điểm sang ô 3–4.
   - **Cửa Sổ Code & Terminal Sống (`Live Code Terminal / Matrix Stream`):** Khung trình biên dịch có các dòng lệnh `#87ff00` tự gõ theo `frame`, con trỏ nhấp nháy và đồng hồ đo tốc độ xử lý.
   - **Máy Quét Sinh Học & Sóng Điện Tâm Đồ (`SVG Waveform / ECG / DNA Scanner`):** Đường sóng SVG uốn lượn theo hàm `Math.sin(frame)` kết hợp tia laser ngang (`translateY`) quét dọc thẻ phân tích.
   - **Buồng Lái HUD & Radar Tự Hành (`LIDAR / Cockpit HUD`):** Quạt quét radar hình nón xoay tròn (`conic-gradient`), vòng thước ngắm cơ khí xoay ngược chiều nhau (`rotate(frame)` & `rotate(-frame)`).
   - **Trục Thời Gian Nén (`Time-Compression Slider` / `Speedometer Gauge`):** Đồng hồ kim quay nhanh hoặc thanh đối chiếu nén thời gian (ví dụ: thanh dài `10 Năm` co rút lại thành tia chớp `Vài Ngày ⚡`).
   - **Cấu Trúc Phân Tử / Lõi Năng Lượng (`Rotating Helix / Reactor Core`):** Các hạt cầu chuyển động xoắn kép hoặc xoay quanh lõi trung tâm theo pha `Math.sin` / `Math.cos`.
   - **Hiệu Ứng Chuyển Động Đa Dạng (`Varied Entrance & Micro-Animations`):** Kết hợp xoay 3D (`perspective(1000px) rotateX/rotateY`), lật thẻ (`flip`), trượt chéo, vẽ đường viền SVG (`strokeDasharray`), phóng tâm chấn (`elastic scale`), thay vì cảnh nào cũng chỉ trượt từ dưới lên giống nhau.

---

### Quy tắc 4: Phụ Đề 1 Dòng Trượt Từ Dưới Lên — Không Khung Bao & Không Cắt Từ Ghép (`SubtitleBox.tsx`)
1. **Không Khung Bao Quanh Sub:**
   - **Bỏ hoàn toàn khung pill nền đen và icon loa `🎙️`.**
   - Chữ hiển thị trực tiếp trên nền video với `font-black`, màu trắng `#FFFFFF`, tự động tô sáng từ khóa quan trọng bằng màu **`#87ff00`**, và đổ bóng sắc nét:
     `textShadow: "0 6px 22px rgba(0, 0, 0, 0.9), 0 2px 6px rgba(0, 0, 0, 0.98)"`
2. **Hiệu Ứng Trượt Nguyên Cụm Từ Dưới Lên (`Whole-Phrase Slide-Up`):**
   - Mỗi cụm phụ đề trượt đồng nhất từ dưới lên (`translateY: 36px -> 0px` bằng `spring({ damping: 15, stiffness: 170, mass: 0.55 })`).
   - **CẤM** làm hiệu ứng hiện trễ từng chữ khiến đầu câu chỉ hiện 1 chữ lẻ loi.
3. **Khóa Cứng 1 Dòng Duy Nhất (`whitespace-nowrap`) & Ngắt Đúng Cụm Nghĩa Tiếng Việt:**
   - **CẤM dùng `flex-wrap`** làm rớt 1–2 chữ cuối xuống dòng thứ 2. Sử dụng `whitespace-nowrap` kết hợp tự động co cỡ chữ thông minh (`36px` – `44px` tùy độ dài cụm).
   - **Bắt buộc khai báo mảng `phrases: string[]` trong `audioData.ts`** (mỗi cụm 3–7 từ, ngắt đúng dấu phẩy `,`, dấu chấm `.`, hoặc từ nối tự nhiên) **VÀ** tích hợp bộ từ điển `COMPOUND_PAIRS` trong `SubtitleBox.tsx` để **tuyệt đối không bao giờ cắt đôi từ ghép 2 âm tiết tiếng Việt** (*"trả lời"*, *"thông tin"*, *"tài liệu"*, *"quy trình"*, *"kiểm soát"*, *"xác suất"*...).
   - Thời lượng hiển thị từng cụm được tính tỷ lệ thuận với số từ trong cụm cộng thêm hệ số nghỉ `+0.5` tại các dấu câu (`, . : ; ! ?`).

---

### Quy tắc 5: Giọng Đọc Vbee AIVoice Thuần Việt, Định Mức Số Từ Chuẩn 1 Vòng & Studio Mastering (`tools/generate_voice_tts.py`)
1. **Định mức số từ khóa cứng theo tốc độ đọc Vbee (`~4.5 từ/giây` — Chạy 1 vòng duy nhất không phải sửa Gate 2):**
   - Video **30 giây:** Tổng **130 – 140 từ** (mỗi cảnh 20 – 24 từ).
   - Video **45 giây:** Tổng **195 – 205 từ** (Cảnh 1–5: 33 – 36 từ/cảnh; Cảnh 6 Outro: 25 – 28 từ; cộng đệm nghỉ `+16 frames` cho Cảnh 1–5 và `+49 frames` cho Cảnh 6 để đạt đúng `1.350 frames = 45.00s`).
   - Video **60 giây:** Tổng **260 – 275 từ** (mỗi cảnh 42 – 46 từ).
2. **Lời thoại 100% Tiếng Việt tự nhiên:**
   - Không viết tắt tiếng Anh gạch nối (như `U-S-B-C`, `M-C-P`) trong lời thoại gửi cho Vbee để tránh lỗi đánh vần sai.
   - Luôn chạy qua từ điển phiên âm `TECH_PHONETIC_RULES` trong `tools/generate_voice_tts.py`.
3. **Giữ nguyên nhịp thở tự nhiên (Không dùng `silenceremove` cắt giữa câu):**
   - Chỉ chuẩn hóa EQ ấm giọng và khóa đỉnh âm lượng `-3dB`, tuyệt đối không dùng bộ lọc `silenceremove` cắt cụt âm đuôi của Vbee.
4. **Kiểm tra nghe trực tiếp trước khi Render:**
   - Sau khi sinh 6 file `.mp3` cho 6 cảnh, bắt buộc dùng `read_file` nghe kiểm tra trực tiếp để xác nhận giọng đọc mượt 100% rồi mới đo `ffprobe` và render video.

---

## 🛠️ Lệnh Render Chuẩn Trên Máy Windows

```powershell
$env:PATH = "C:\Program Files\Adobe\Adobe Creative Cloud Experience\libs;" + $env:PATH
Set-Location "d:\Phiên bản Ai agent\Subagent\templates\remotion-cuongit-template"
node .\node_modules\@remotion\cli\remotion-cli.js render <CompositionId> "d:\Phiên bản Ai agent\Subagent\campaigns\<YYYY-MM-DD>\<campaign-slug>\<video-name>.mp4"
```
Sau khi render xong, bắt buộc trích xuất 4 frame QA (`01-hook.jpg`, `02-problem.jpg`, `03-workflow.jpg`, `04-outro.jpg`) bằng `ffmpeg` và dùng `read_file` kiểm tra trực tiếp bằng mắt trước khi bàn giao cho CEO.
