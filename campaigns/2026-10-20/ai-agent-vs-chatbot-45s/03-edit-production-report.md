# BÁO CÁO SẢN XUẤT & NGHIỆM THU VIDEO REMOTION (`03-edit-production-report.md`)
## Chiến Dịch: AI Agent Tự Hành Khác Gì Chatbot Thông Thường?

- **Campaign ID:** `CAMP-20261020-ai-agent-vs-chatbot-45s`
- **Task ID:** `CAMP-20261020-W3-edit`
- **Phiên bản:** `v2` (Chuẩn Vàng 5 Golden Rules — `templates/remotion-cuongit-template`)
- **Kênh đích:** `#04: AI Players - Người chơi hệ AI`
- **Composition ID:** `AiAgentVsChatbotShort`
- **Độ phân giải & Tốc độ khung hình:** `1080x1920` (9:16 Vertical) @ `30fps`
- **Tổng thời lượng khóa cứng:** **`1.350 frames`** (`45.00 giây` chính xác)
- **Đường dẫn Source Code:** `f:\Ai Agent Setup\SubAgent\Subagent\templates\remotion-cuongit-template\src\AiAgentVsChatbotShort\`
- **Đường dẫn Video MP4 thành phẩm:** `f:\Ai Agent Setup\SubAgent\Subagent\campaigns\2026-10-20\ai-agent-vs-chatbot-45s\ai-agent-vs-chatbot-45s.mp4` (`102.1 MB`)
- **Đường dẫn 4 Frame QA:** `f:\Ai Agent Setup\SubAgent\Subagent\campaigns\2026-10-20\ai-agent-vs-chatbot-45s\qa-frames\` (`01-hook.jpg`, `02-problem.jpg`, `03-workflow.jpg`, `04-outro.jpg`)
- **Trạng thái Gate & QA bằng mắt:** **`PASS 100% (10.0/10)`**

---

## 1. Bảng Phân Bổ Frame & Đồng Bộ Audio Vbee V2 (`TOTAL_DURATION_FRAMES = 1350`)

| Phân Cảnh | Component | File Audio (`public/audio/AiAgentVsChatbot45s/`) | Thời Lượng Thoại (`durationSec`) | Tổng Frame Cảnh (`durationInFrames`) | Mốc Frame Cộng Dồn | Từ Khóa Nhấn (`#87ff00`) |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **Scene 1 (Hook)** | `Scene1Hook.tsx` | `scene1_hook.mp3` | `7.055s` | **228 frames** | `0 – 228` | `câu lệnh`, `trí tuệ`, `nhân tạo`, `sao chép`, `phần mềm` |
| **Scene 2 (Problem)** | `Scene2Problem.tsx` | `scene2_problem.mp3` | `7.160s` | **231 frames** | `228 – 459` | `hộp thoại`, `thông thường`, `văn bản`, `gợi ý`, `công cụ` |
| **Scene 3 (Concept 1)** | `Scene3Concept1.tsx` | `scene3_concept1.mp3` | `7.003s` | **227 frames** | `459 – 686` | `trợ lý`, `tự hành`, `kết nối`, `dữ liệu`, `phần mềm`, `thực thi` |
| **Scene 4 (Workflow)** | `Scene4Concept2.tsx` | `scene4_concept2.mp3` | `7.734s` | **249 frames** | `686 – 935` | `Quy trình`, `ba bước`, `mục tiêu`, `kế hoạch`, `công cụ`, `nghiệm thu`, `kết quả` |
| **Scene 5 (Impact)** | `Scene5Impact.tsx` | `scene5_impact.mp3` | `7.107s` | **230 frames** | `935 – 1165` | `tự động`, `hàng giờ`, `thủ công`, `đề bài`, `hệ thống`, `xuyên suốt` |
| **Scene 6 (Outro)** | `Scene6Outro.tsx` | `scene6_outro.mp3` | `4.521s` | **185 frames** | `1165 – 1350` | `Theo dõi`, `làm chủ`, `tự hành`, `thông minh` |
| **TỔNG CỘNG** | `AiAgentVsChatbotShort` | **6 files .mp3** | **`40.581s` thoại** | **`1.350 frames`** | **`00.00s – 45.00s`** | — |

---

## 2. Kiểm Định 5 Quy Tắc Vàng (`quy-chuan-remotion-cuongit-template.md`)

1. **Quy tắc 1 — Hệ Màu Chữ Tiêu Đề `#87ff00` & Tài Nguyên `public/brand-kit/`:**
   - Tiêu đề chính (`Headline` cả 6 Scene), thanh tiến trình, điểm nhấn chủ đạo và từ khóa phụ đề khóa cứng mã màu `#87ff00`.
   - Hình nền nạp trực tiếp từ `staticFile("brand-kit/bg/BG-video-motion.jpg")`, giữ nguyên sắc xanh cobalt điện tử nguyên bản (không phủ lớp đen), kèm chuyển động thở Ken Burns nhẹ và 2 quầng sáng `radial-gradient` trôi nổi.
   - BGM `brand-kit/bgm/1.The Violins.mp3` phát xuyên suốt ở `volume={0.10}` (-18dB); SFX chuyển cảnh `apple-pay-sound.mp3` (`volume={0.26}`) đầu các cảnh 2–6; SFX bật thẻ `discord-notification.mp3` (`volume={0.22}`) tại frame 25 của mỗi cảnh.
2. **Quy tắc 2 — Khung Thẻ Kính Trong Suốt (`Transparent Frosted Glass` — Cấm Khung Đen):**
   - Toàn bộ thẻ bao ngoài dùng `rounded-3xl border border-white/30 bg-white/[0.08] p-8 shadow-[0_16px_50px_rgba(0,0,0,0.25)] backdrop-blur-md`.
   - Thẻ con bên trong dùng `rounded-2xl border border-white/25 bg-white/[0.10] backdrop-blur-sm`. Tuyệt đối không có bất kỳ khối nền đen đặc nào che nền xanh.
3. **Quy tắc 3 — Motion Minh Họa Liên Tục Theo `frame` Ở Cả 6 Cảnh:**
   - **Scene 1:** Sóng radar tỏa rộng liên tục quanh Bot AI (`0.85 -> 1.55`), khiên `ShieldAlert` lắc nhịp nhàng, 2 thanh đo áp lực làm tay co giãn liên tục.
   - **Scene 2:** Icon `Cpu` co giãn + xoay nhẹ, nhãn `THỤ ĐỘNG 🛑` nghiêng lắc, thanh chỉ số `Trả lời văn bản` nhảy số trực tiếp (`~85-95%`) đối lập 2 thanh `0%`.
   - **Scene 3:** Kính lúp `Search` quét quỹ đạo tròn trên trung tâm `AI AGENT` (`#87ff00`), 2 mũi tên `ArrowRight` trượt ngang liên tục truyền dữ liệu từ `Kho Dữ Liệu Nội Bộ` sang `Phần Mềm Ngoài`.
   - **Scene 4:** Kích hoạt tuần tự 3 bước (`activeRange: [10,85]`, `[85,165]`, `[165,249]`), tự động sáng viền `#87ff00`, phóng nhẹ `scale(1.025)` và chạy thanh tiến trình từ `0% -> 100%`.
   - **Scene 5:** Cột trái `CHATBOT CŨ` rung cảnh báo nhẹ, cột phải `AI AGENT` bay lơ lửng kèm bộ đếm `TỰ ĐỘNG` tăng từ `0% -> 100%`.
   - **Scene 6:** Tên lửa `Rocket` bay lơ lửng trên nền `#87ff00`, chuông `BellRing` rung lắc, ngôi sao `Sparkles` xoay tròn (`frame * 4deg`) và nút CTA co giãn nhịp thở.
4. **Quy tắc 4 — Phụ Đề 1 Dòng (`whitespace-nowrap`) Trượt Nguyên Cụm & Bảo Vệ Từ Ghép:**
   - Không khung bao, trượt nguyên cụm từ dưới lên (`translateY: 36px -> 0px`), khóa cứng 1 dòng `whitespace-nowrap`.
   - Nạp đầy đủ 35 cụm `phrases` từ `01-content-script.md` (v2) và bổ sung trọn bộ 42 từ ghép 2 âm tiết mới vào `COMPOUND_PAIRS` trong `SubtitleBox.tsx`.
5. **Quy tắc 5 — Sub-heading Scene 6 Gọn 1 Dòng & Thẩm Định 4 Frame QA Bằng Mắt:**
   - Sub-heading Scene 6 `Làm Chủ Hệ Thống AI Agent Tự Hành Thông Minh Nhất` (`text-[27px] whitespace-nowrap`) nằm gọn tuyệt đối trên 1 dòng.

---

## 3. Kết Quả Thẩm Định 4 Frame QA Trực Tiếp Bằng Mắt (`view_file`)

| File Frame QA | Mốc Trích Xuất | Nội Dung Kiểm Tra Bằng Mắt | Kết Quả |
| :--- | :---: | :--- | :---: |
| `qa-frames/01-hook.jpg` | `00:00:04.2` | Header `AI PLAYERS`, Badge `NGHỊCH LÝ DÙNG AI HIỆN NAY`, Card kính trong suốt 3 khối (`Đã Hỏi AI ✅`, `NHƯNG... ⚠️`, `Gõ Lệnh Liên Tục ❌` / `Tự Sao Chép Tay ❌`), Headline `#87ff00` 2 dòng cân đối, phụ đề 1 dòng `"ngồi gõ từng câu lệnh,"` tô sáng `"câu lệnh"` màu `#87ff00`. | **PASS 100%** |
| `qa-frames/02-problem.jpg` | `00:00:08.5` | Badge `GIỚI HẠN CỦA CHATBOT CŨ`, Headline `#87ff00` `CHỈ HỎI ĐÂU ĐÁP ĐẤY / KHÔNG THỂ HÀNH ĐỘNG`, Card kính `Cơ Chế Hộp Thoại Thụ Động` + 3 thanh chỉ số (`90%`, `0%`, `0%`) + Alert box rõ nét, phụ đề 1 dòng `"Bởi vì hộp thoại thông thường"`. | **PASS 100%** |
| `qa-frames/03-workflow.jpg` | `00:00:26.2` | Headline `#87ff00` `QUY TRÌNH 3 BƯỚC TỰ HÀNH`, 3 Card bước trong suốt (`1. Phân Tích & Lập Kế Hoạch`, `2. Tự Mở Công Cụ Xử Lý` đang sáng viền `#87ff00`, `3. Tự Nghiệm Thu Kết Quả`), phụ đề 1 dòng `"để tự lập kế hoạch làm,"` tô sáng `"kế hoạch"`. | **PASS 100%** |
| `qa-frames/04-outro.jpg` | `00:00:39.4` | Card kính Outro với icon `Rocket` nền `#87ff00`, tiêu đề `AI PLAYERS` `#87ff00`, Sub-heading `Làm Chủ Hệ Thống AI Agent Tự Hành Thông Minh Nhất` nằm gọn 1 dòng duy nhất, nút CTA `#87ff00` sắc nét, phụ đề 1 dòng `"Theo dõi ngay kênh"`. | **PASS 100%** |

---

## 4. Bảng Tự Chấm Điểm Nghiệm Thu (`edit.md` & 5 Quy Tắc Vàng — 10 Điểm)

| Tiêu Chí | Điểm Tối Đa | Điểm Tự Chấm | Căn Cứ Nghiệm Thu |
| :--- | :---: | :---: | :--- |
| **1. Hệ màu `#87ff00`, Nền `BG-video-motion.jpg` & BGM/SFX** | 2.5 | **2.5** | Khóa cứng `#87ff00`, giữ nguyên nền xanh nguyên bản không phủ đen, đầy đủ BGM (-18dB) & 2 lớp SFX chuyển cảnh/bật thẻ. |
| **2. Khung thẻ kính trong suốt (`Frosted Glass`)** | 2.5 | **2.5** | 100% thẻ dùng `bg-white/[0.08] border-white/30 backdrop-blur-md`, không dùng khung nền tối/đen. |
| **3. Motion minh họa liên tục & Đồng bộ 1350 frames** | 2.5 | **2.5** | Cả 6 cảnh đều có chuyển động nội cảnh liên tục theo `frame`, khớp 100% thời lượng audio Vbee v2 (`1350 frames = 45.00s`). |
| **4. Phụ đề 1 dòng `whitespace-nowrap` & QA 4 Frames** | 2.5 | **2.5** | Phụ đề 1 dòng trượt nguyên cụm không khung bao, không rớt chữ lẻ ở tất cả các cảnh và Scene 6 Outro; đã kiểm tra trực tiếp 4 ảnh QA. |
| **TỔNG ĐIỂM** | **10.0** | **10.0 / 10** | **APPROVED — SẴN SÀNG BÀN GIAO CHO `mama`** |
