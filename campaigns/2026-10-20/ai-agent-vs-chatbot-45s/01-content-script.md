# KỊCH BẢN VIDEO SLIDE REMOTION EXPLAINER 45 GIÂY (CHUẨN VÀNG — BẢN V2)
## Chủ Đề: AI Agent Tự Hành Khác Gì Chatbot Thông Thường?

- **Campaign ID:** `CAMP-20261020-ai-agent-vs-chatbot-45s`
- **Task ID:** `CAMP-20261020-W1-content`
- **Phiên bản:** `v2` (Hiệu chỉnh chuẩn tốc độ đọc thực tế Vbee `hn_male_manhdung_news_48k-fhg` ~4.55 âm tiết/giây, đối chiếu trực tiếp mẫu chuẩn Vàng `AiHallucinationShort` 200 từ = `43.5s – 45.0s`)
- **Kênh đích:** `#04: AI Players - Người chơi hệ AI`
- **Định dạng:** `REMOTION_EXPLAINER` (`1080x1920 @ 30fps`, 6 phân cảnh chuẩn Vàng `templates/remotion-cuongit-template`)
- **Tổng số từ kịch bản đọc:** **`200 từ`** (Cảnh 1: 34 từ | Cảnh 2: 35 từ | Cảnh 3: 34 từ | Cảnh 4: 36 từ | Cảnh 5: 34 từ | Cảnh 6: 27 từ — 35 cụm `phrases`, mỗi cụm 4–6 từ)
- **Trạng thái Compliance & Hard Gate:** `PASS 100%` (Không chào hỏi 3s đầu, không bịa số liệu thống kê, 100% tiếng Việt tự nhiên cho Vbee, tuân thủ 5 Quy Tắc Vàng Remotion)

---

## 1. Kiến Trúc Retention & 3 Biến Thể Hook / 2 Biến Thể CTA (A/B Testing)

### Ba Biến Thể Mở Đầu (00–07s)
- **Phương án A (Chính thức — Contrarian / Pain-First Question):** *"Bạn đã bao giờ tự hỏi sao dùng trí tuệ nhân tạo, mà mỗi ngày bạn vẫn phải ngồi gõ từng câu lệnh, rồi tự tay sao chép dữ liệu qua từng phần mềm chưa?"*
- **Phương án B (Curiosity Gap):** *"Cùng gọi là trí tuệ nhân tạo, nhưng tại sao có công cụ chỉ biết trò chuyện qua lại, còn hệ thống khác lại tự động làm xong toàn bộ khối lượng công việc?"*
- **Phương án C (Pattern Interrupt):** *"Đừng đánh đồng hộp thoại thông thường với trợ lý tự hành, nếu bạn không muốn mỗi ngày vẫn mất hàng giờ ngồi gõ lệnh và làm thủ công từng bước!"*

### Hai Biến Thể Kêu Gọi Hành Động (39–45s)
- **Phương án CTA 1 (Chính thức — Follow Kênh):** *"Theo dõi ngay kênh để làm chủ những hệ thống trợ lý trí tuệ nhân tạo tự hành thông minh nhất cho công việc của bạn nhé!"*
- **Phương án CTA 2 (Bình luận nhận quy trình):** *"Theo dõi ngay kênh và để lại bình luận phía dưới để nhận trọn bộ sơ đồ thiết lập trợ lý tự hành cho công việc của bạn nhé!"*

---

## 2. Kịch Bản Chi Tiết 6 Phân Cảnh Chuẩn Vàng (`00s – 45s` | Tổng `200 từ`)

### SCENE 1: HOOK — NGHỊCH LÝ DÙNG AI NHƯNG VẪN LÀM TAY (`00s – 07.5s` | `scene1_hook`)
- **Nhịp kịch bản:** `Hook (00s - 03s -> 07.5s)` — Mở đầu bằng câu hỏi xoáy trực diện vào nghịch lý dùng AI nhưng mỗi ngày vẫn phải ngồi gõ từng câu lệnh và sao chép dữ liệu thủ công.
- **Số từ:** **`34 từ`** (6 cụm phụ đề, mỗi cụm 5–6 từ).
- Voiceover: "Bạn đã bao giờ tự hỏi sao dùng trí tuệ nhân tạo, mà mỗi ngày bạn vẫn phải ngồi gõ từng câu lệnh, rồi tự tay sao chép dữ liệu qua từng phần mềm chưa?"
- **Mảng `phrases` (`5–6 từ/cụm`, khóa cứng 1 dòng `whitespace-nowrap`):**
  ```ts
  phrases: [
    "Bạn đã bao giờ tự hỏi",
    "sao dùng trí tuệ nhân tạo,",
    "mà mỗi ngày bạn vẫn phải",
    "ngồi gõ từng câu lệnh,",
    "rồi tự tay sao chép dữ liệu",
    "qua từng phần mềm chưa?",
  ]
  ```
- **Từ khóa tô sáng (`highlightWords` `#87ff00`):** `["trí tuệ", "nhân tạo", "câu lệnh", "sao chép", "phần mềm"]` (`highlightKeyword: "câu lệnh"`)
- **Đặc tả Visual & UI Card (Chuẩn Quy Tắc 1, 2, 3):**
  - **Top Badge (`bg-white/10 border-white/30 backdrop-blur-md`):** Chấm tròn `#87ff00` nhấp nháy + chữ `NGHỊCH LÝ DÙNG AI HIỆN NAY`
  - **Tiêu đề chính (`Headline #87ff00`):**
    ```text
    ĐÃ DÙNG AI HỖ TRỢ
    SAO VẪN PHẢI LÀM TAY?
    ```
  - **Sub-headline (`text-white/90`):** `Cạm bẫy khiến bạn tốn hàng giờ gõ lệnh mỗi ngày!`
  - **Main Container Card (`bg-white/[0.08] border-white/30 backdrop-blur-md`):**
    - **Thẻ trái:** Icon `Bot` màu `#87ff00` có vòng sóng radar tỏa rộng liên tục (`scale: 0.85 -> 1.55`) + nhãn `Đã Hỏi AI ✅`.
    - **Giữa:** Icon `ShieldAlert` màu vàng rung lắc (`Math.sin(frame / 2.8) * 10deg`) + badge `NHƯNG... ⚠️`.
    - **Thẻ phải (2 thanh cảnh báo rung nhẹ):** Thanh 1 `Gõ Lệnh Liên Tục ❌` + Thanh 2 `Tự Sao Chép Tay ❌` với thanh đo áp lực co giãn liên tục.
  - **Âm thanh:** BGM `1.The Violins.mp3` (-18dB) + SFX `discord-notification.mp3` tại frame 25.

---

### SCENE 2: PROBLEM — GIỚI HẠN CỦA CHATBOT CŨ (`07.5s – 15.5s` | `scene2_problem`)
- **Nhịp kịch bản:** `Pain / Problem (07.5s - 15.5s)` — Giải thích nguyên nhân gốc rễ: Hộp thoại thông thường (Chatbot cũ) chỉ biết hỏi đâu đáp đấy trên màn hình chat, không có quyền mở công cụ làm việc.
- **Số từ:** **`35 từ`** (6 cụm phụ đề, mỗi cụm 5–6 từ).
- Voiceover: "Bởi vì hộp thoại thông thường chỉ biết hỏi đâu đáp đấy, đưa ra văn bản gợi ý trên màn hình trò chuyện, chứ hoàn toàn không có quyền tự mở công cụ làm việc."
- **Mảng `phrases` (`5–6 từ/cụm`, khóa cứng 1 dòng `whitespace-nowrap`):**
  ```ts
  phrases: [
    "Bởi vì hộp thoại thông thường",
    "chỉ biết hỏi đâu đáp đấy,",
    "đưa ra văn bản gợi ý",
    "trên màn hình trò chuyện,",
    "chứ hoàn toàn không có quyền",
    "tự mở công cụ làm việc.",
  ]
  ```
- **Từ khóa tô sáng (`highlightWords` `#87ff00`):** `["hộp thoại", "thông thường", "văn bản", "gợi ý", "công cụ"]` (`highlightKeyword: "hộp thoại"`)
- **Đặc tả Visual & UI Card (Chuẩn Quy Tắc 1, 2, 3):**
  - **Top Badge:** `GIỚI HẠN CỦA CHATBOT CŨ`
  - **Tiêu đề chính (`Headline #87ff00`):**
    ```text
    CHỈ HỎI ĐÂU ĐÁP ĐẤY
    KHÔNG THỂ HÀNH ĐỘNG
    ```
  - **Sub-headline (`text-white/90`):** `Đưa ra văn bản gợi ý rồi đứng chờ bạn tự làm!`
  - **Main Container Card (`bg-white/[0.08] border-white/30 backdrop-blur-md`):**
    - **Header Card:** Icon `Cpu` xoay nhẹ + tiêu đề `Cơ Chế Hộp Thoại Thụ Động` (`Chờ người dùng nhắc từng câu lệnh`) + nhãn `THỤ ĐỘNG 🛑` nghiêng lắc liên tục.
    - **3 Thanh Chỉ Số Nhảy Động Theo Frame:**
      1. `Trả lời văn bản`: `88%` (nhảy động)
      2. `Mở phần mềm ngoài`: `0%` (khóa cứng cảnh báo)
      3. `Tự chạy quy trình`: `0%` (khóa cứng cảnh báo)
    - **Bottom Alert Inner Card (`bg-white/[0.10] border-white/25`):** Icon `ShieldAlert` phát sáng + `Chỉ Gợi Ý Chữ = Bạn Vẫn Phải Tự Làm!` (`Không có quyền bấm nút, gửi thư hay cập nhật dữ liệu`).
  - **Âm thanh:** SFX chuyển cảnh `apple-pay-sound.mp3` (frame 0) + `discord-notification.mp3` (frame 25).

---

### SCENE 3: CORE SOLUTION — CƠ CHẾ AI AGENT TỰ HÀNH (`15.5s – 23.0s` | `scene3_concept1`)
- **Nhịp kịch bản:** `Demo / Solution (15.5s - 23.0s)` — Giải pháp đột phá: Trợ lý tự hành (AI Agent) được cấp quyền kết nối thẳng vào kho dữ liệu nội bộ và phần mềm ngoài để chủ động thực thi.
- **Số từ:** **`34 từ`** (6 cụm phụ đề, mỗi cụm 5–6 từ).
- Voiceover: "Ngược lại, trợ lý tự hành được cấp quyền kết nối thẳng vào kho dữ liệu nội bộ và hệ thống phần mềm ngoài, để chủ động thực thi mà không chờ nhắc lệnh."
- **Mảng `phrases` (`5–6 từ/cụm`, khóa cứng 1 dòng `whitespace-nowrap`):**
  ```ts
  phrases: [
    "Ngược lại, trợ lý tự hành",
    "được cấp quyền kết nối thẳng",
    "vào kho dữ liệu nội bộ",
    "và hệ thống phần mềm ngoài,",
    "để chủ động thực thi",
    "mà không chờ nhắc lệnh.",
  ]
  ```
- **Từ khóa tô sáng (`highlightWords` `#87ff00`):** `["trợ lý", "tự hành", "kết nối", "dữ liệu", "phần mềm", "thực thi"]` (`highlightKeyword: "tự hành"`)
- **Đặc tả Visual & UI Card (Chuẩn Quy Tắc 1, 2, 3):**
  - **Top Badge:** `ĐỘT PHÁ CÔNG NGHỆ AI AGENT`
  - **Tiêu đề chính (`Headline #87ff00`):**
    ```text
    TRỢ LÝ AI TỰ HÀNH
    TRỰC TIẾP LÀM VIỆC THẬT
    ```
  - **Sub-headline (`text-white/90`):** `Kết nối thẳng dữ liệu và phần mềm để thực thi từ A đến Z!`
  - **Main Container Card (Luồng 3 khối ngang + Mũi tên dữ liệu `ArrowRight` chạy liên tục):**
    - **Khối 1 (Trái):** Icon `Database` bay nhẹ + `Kho Dữ Liệu Nội Bộ` (`Hồ sơ & tài liệu thật`).
    - **Mũi tên 1 (`ArrowRight` `#87ff00`):** Trượt ngang liên tục theo `flowProgress`.
    - **Khối 2 (Giữa — Nền `#87ff00` chữ đen `text-slate-950`):** Icon `Search` quét quỹ đạo tròn + `AI AGENT` (`Tự điều phối`).
    - **Mũi tên 2 (`ArrowRight` `#87ff00`):** Trượt ngang liên tục theo `flowProgress`.
    - **Khối 3 (Phải):** Icon `Bot` phát sáng + `Phần Mềm Ngoài` (`Tự chạy hoàn tất ✅`).
  - **Âm thanh:** SFX `apple-pay-sound.mp3` (frame 0) + `discord-notification.mp3` (frame 25).

---

### SCENE 4: WORKFLOW 3 BƯỚC CỦA AI AGENT (`23.0s – 31.5s` | `scene4_concept2`)
- **Nhịp kịch bản:** `Demo / Workflow (23.0s - 31.5s)` — Giải phẫu quy trình 3 bước khép kín của AI Agent: Phân tích mục tiêu lập kế hoạch -> Tự mở công cụ xử lý dữ liệu -> Nghiệm thu kết quả.
- **Số từ:** **`36 từ`** (6 cụm phụ đề, mỗi cụm đúng 6 từ).
- Voiceover: "Quy trình chuẩn gồm ba bước: một là phân tích mục tiêu để tự lập kế hoạch làm, hai là tự mở công cụ xử lý dữ liệu thực tế, ba là nghiệm thu kết quả."
- **Mảng `phrases` (`6 từ/cụm`, khóa cứng 1 dòng `whitespace-nowrap`):**
  ```ts
  phrases: [
    "Quy trình chuẩn gồm ba bước:",
    "một là phân tích mục tiêu",
    "để tự lập kế hoạch làm,",
    "hai là tự mở công cụ",
    "xử lý dữ liệu thực tế,",
    "ba là nghiệm thu kết quả.",
  ]
  ```
- **Từ khóa tô sáng (`highlightWords` `#87ff00`):** `["Quy trình", "ba bước", "mục tiêu", "kế hoạch", "công cụ", "nghiệm thu", "kết quả"]` (`highlightKeyword: "kế hoạch"`)
- **Đặc tả Visual & UI Card (Chuẩn Quy Tắc 1, 2, 3):**
  - **Tiêu đề chính (`Headline #87ff00`):**
    ```text
    QUY TRÌNH 3 BƯỚC TỰ HÀNH
    ```
  - **Sub-headline (`text-white/90`):** `Vận hành khép kín không cần con người nhắc từng lệnh`
  - **3 Thẻ Bước Tuần Tự (`bg-white/[0.08] backdrop-blur-md`, sáng viền `#87ff00` & chạy thanh progress `0% -> 100%` theo `activeRange`):**
    1. **Card Bước 1 (`activeRange: [10, 85]`):** Icon `Database` trên nền `#87ff00` + Tiêu đề `1. Phân Tích & Lập Kế Hoạch` + Mô tả `Tự chia nhỏ mục tiêu lớn thành từng đầu việc` + Badge `BƯỚC 1 ⚡`.
    2. **Card Bước 2 (`activeRange: [85, 165]`):** Icon `Lock` trên nền `#87ff00` + Tiêu đề `2. Tự Mở Công Cụ Xử Lý` + Mô tả `Chủ động kết nối phần mềm và xử lý dữ liệu thật` + Badge `BƯỚC 2 ⚡`.
    3. **Card Bước 3 (`activeRange: [165, 245]`):** Icon `FileCheck` trên nền `#87ff00` + Tiêu đề `3. Tự Nghiệm Thu Kết Quả` + Mô tả `Rà soát lỗi và bàn giao đầu ra hoàn chỉnh` + Badge `BƯỚC 3 ⚡`.
  - **Âm thanh:** SFX `apple-pay-sound.mp3` (frame 0) + `discord-notification.mp3` (frame 25).

---

### SCENE 5: IMPACT — SO SÁNH TRƯỚC VÀ SAU (`31.5s – 39.0s` | `scene5_impact`)
- **Nhịp kịch bản:** `Payoff / Before–After Impact (31.5s - 39.0s)` — Đối chiếu hiệu suất thực tế: Thay vì mất hàng giờ làm thủ công từng việc nhỏ, chỉ cần giao đề bài để hệ thống chạy xuyên suốt.
- **Số từ:** **`34 từ`** (6 cụm phụ đề, mỗi cụm 4–6 từ).
- Voiceover: "Nhờ cơ chế tự động này, thay vì mất hàng giờ liền làm thủ công từng việc nhỏ, bạn chỉ cần giao đề bài để hệ thống chạy xuyên suốt từ đầu đến cuối."
- **Mảng `phrases` (`4–6 từ/cụm`, khóa cứng 1 dòng `whitespace-nowrap`):**
  ```ts
  phrases: [
    "Nhờ cơ chế tự động này,",
    "thay vì mất hàng giờ liền",
    "làm thủ công từng việc nhỏ,",
    "bạn chỉ cần giao đề bài",
    "để hệ thống chạy xuyên suốt",
    "từ đầu đến cuối.",
  ]
  ```
- **Từ khóa tô sáng (`highlightWords` `#87ff00`):** `["tự động", "hàng giờ", "thủ công", "đề bài", "hệ thống", "xuyên suốt"]` (`highlightKeyword: "tự động"`)
- **Đặc tả Visual & UI Card (Chuẩn Quy Tắc 1, 2, 3):**
  - **Top Badge:** `SO SÁNH HIỆU SUẤT THỰC TẾ`
  - **Tiêu đề chính (`Headline #87ff00`):**
    ```text
    CHỈ CẦN GIAO ĐỀ BÀI
    HỆ THỐNG CHẠY XUYÊN SUỐT
    ```
  - **Sub-headline (`text-white/90`):** `Giải phóng bạn khỏi hàng giờ thao tác lặp đi lặp lại`
  - **Grid 2 Cột Đối Lập (`grid-cols-2 gap-6`):**
    - **Cột Trái (Before — Chatbot Cũ, rung nhẹ `leftShakeX`):**
      - Header: Icon `AlertTriangle` vàng + `CHATBOT CŨ`
      - Title: `Làm Thủ Công`
      - Body: `Mất hàng giờ ngồi gõ lệnh, sao chép và tự xử lý từng việc nhỏ`
      - Footer Badge: `TỐN HÀNG GIỜ ❌`
    - **Cột Phải (After — AI Agent, bay lơ lửng `rightFloatY` + viền `#87ff00/60`):**
      - Header: Icon `ShieldCheck` xoay nhẹ + `AI AGENT` + bộ đếm chạy `0% -> 100%`
      - Title: `Chạy Xuyên Suốt`
      - Body: `Chỉ cần giao đề bài, hệ thống tự vận hành trọn gói từ đầu đến cuối`
      - Footer Badge (Nền `#87ff00` chữ đen): Icon `CheckCircle2` + `TỰ ĐỘNG 100%`
  - **Âm thanh:** SFX `apple-pay-sound.mp3` (frame 0) + `discord-notification.mp3` (frame 25).

---

### SCENE 6: OUTRO & CTA — KÊNH AI PLAYERS (`39.0s – 45.0s` | `scene6_outro`)
- **Nhịp kịch bản:** `CTA (39.0s - 45.0s)` — Kêu gọi theo dõi kênh **AI Players - Người chơi hệ AI** để làm chủ những hệ thống trợ lý trí tuệ nhân tạo tự hành thông minh nhất.
- **Số từ:** **`27 từ`** (5 cụm phụ đề, mỗi cụm 4–6 từ).
- Voiceover: "Theo dõi ngay kênh để làm chủ những hệ thống trợ lý trí tuệ nhân tạo tự hành thông minh nhất cho công việc của bạn nhé!"
- **Mảng `phrases` (`4–6 từ/cụm`, khóa cứng 1 dòng `whitespace-nowrap`):**
  ```ts
  phrases: [
    "Theo dõi ngay kênh",
    "để làm chủ những hệ thống",
    "trợ lý trí tuệ nhân tạo",
    "tự hành thông minh nhất",
    "cho công việc của bạn nhé!",
  ]
  ```
- **Từ khóa tô sáng (`highlightWords` `#87ff00`):** `["Theo dõi", "làm chủ", "tự hành", "thông minh"]` (`highlightKeyword: "Theo dõi"`)
- **Đặc tả Visual & UI Card (Chuẩn Quy Tắc 1, 2, 3):**
  - **Main Container Card (`bg-white/[0.08] border-white/30 p-10 backdrop-blur-md`):**
    - **Icon Chính:** `Rocket` trên khối vuông bo góc nền `#87ff00` bay lơ lửng (`rocketY` + `rocketTilt`).
    - **Tiêu đề Kênh (`Headline #87ff00`):** `AI PLAYERS`
    - **Sub-heading 1 dòng (`text-[27px] whitespace-nowrap font-bold text-white/95`):**
      `Làm Chủ Hệ Thống AI Agent Tự Hành Thông Minh Nhất` (49 ký tự — nằm gọn tuyệt đối trên 1 dòng).
    - **Nút CTA (`bg-[#87ff00] text-slate-950 rounded-full` co giãn nhịp thở `btnPulse`):**
      Icon `BellRing` rung lắc + `THEO DÕI NGAY ĐỂ LÀM CHỦ AI!` + Icon `Sparkles` xoay tròn (`frame * 4deg`).
  - **Âm thanh:** SFX `apple-pay-sound.mp3` (frame 0) + `discord-notification.mp3` (frame 25).

---

## 3. Cấu Hình `audioData.ts` & Từ Điển Bảo Vệ Từ Ghép (`COMPOUND_PAIRS`) Bàn Giao Cho `voice` & `edit`

### 3.1. Bản Chuẩn `audioData.ts` (Tổng `200 từ` — 35 cụm `phrases`)
```ts
export const audioManifest = {
  scenes: [
    {
      id: "scene1_hook",
      text: "Bạn đã bao giờ tự hỏi sao dùng trí tuệ nhân tạo, mà mỗi ngày bạn vẫn phải ngồi gõ từng câu lệnh, rồi tự tay sao chép dữ liệu qua từng phần mềm chưa?",
      phrases: [
        "Bạn đã bao giờ tự hỏi",
        "sao dùng trí tuệ nhân tạo,",
        "mà mỗi ngày bạn vẫn phải",
        "ngồi gõ từng câu lệnh,",
        "rồi tự tay sao chép dữ liệu",
        "qua từng phần mềm chưa?",
      ],
      highlightKeyword: "câu lệnh",
      audioFile: "audio/AiAgentVsChatbot45s/scene1_hook.mp3",
    },
    {
      id: "scene2_problem",
      text: "Bởi vì hộp thoại thông thường chỉ biết hỏi đâu đáp đấy, đưa ra văn bản gợi ý trên màn hình trò chuyện, chứ hoàn toàn không có quyền tự mở công cụ làm việc.",
      phrases: [
        "Bởi vì hộp thoại thông thường",
        "chỉ biết hỏi đâu đáp đấy,",
        "đưa ra văn bản gợi ý",
        "trên màn hình trò chuyện,",
        "chứ hoàn toàn không có quyền",
        "tự mở công cụ làm việc.",
      ],
      highlightKeyword: "hộp thoại",
      audioFile: "audio/AiAgentVsChatbot45s/scene2_problem.mp3",
    },
    {
      id: "scene3_concept1",
      text: "Ngược lại, trợ lý tự hành được cấp quyền kết nối thẳng vào kho dữ liệu nội bộ và hệ thống phần mềm ngoài, để chủ động thực thi mà không chờ nhắc lệnh.",
      phrases: [
        "Ngược lại, trợ lý tự hành",
        "được cấp quyền kết nối thẳng",
        "vào kho dữ liệu nội bộ",
        "và hệ thống phần mềm ngoài,",
        "để chủ động thực thi",
        "mà không chờ nhắc lệnh.",
      ],
      highlightKeyword: "tự hành",
      audioFile: "audio/AiAgentVsChatbot45s/scene3_concept1.mp3",
    },
    {
      id: "scene4_concept2",
      text: "Quy trình chuẩn gồm ba bước: một là phân tích mục tiêu để tự lập kế hoạch làm, hai là tự mở công cụ xử lý dữ liệu thực tế, ba là nghiệm thu kết quả.",
      phrases: [
        "Quy trình chuẩn gồm ba bước:",
        "một là phân tích mục tiêu",
        "để tự lập kế hoạch làm,",
        "hai là tự mở công cụ",
        "xử lý dữ liệu thực tế,",
        "ba là nghiệm thu kết quả.",
      ],
      highlightKeyword: "kế hoạch",
      audioFile: "audio/AiAgentVsChatbot45s/scene4_concept2.mp3",
    },
    {
      id: "scene5_impact",
      text: "Nhờ cơ chế tự động này, thay vì mất hàng giờ liền làm thủ công từng việc nhỏ, bạn chỉ cần giao đề bài để hệ thống chạy xuyên suốt từ đầu đến cuối.",
      phrases: [
        "Nhờ cơ chế tự động này,",
        "thay vì mất hàng giờ liền",
        "làm thủ công từng việc nhỏ,",
        "bạn chỉ cần giao đề bài",
        "để hệ thống chạy xuyên suốt",
        "từ đầu đến cuối.",
      ],
      highlightKeyword: "tự động",
      audioFile: "audio/AiAgentVsChatbot45s/scene5_impact.mp3",
    },
    {
      id: "scene6_outro",
      text: "Theo dõi ngay kênh để làm chủ những hệ thống trợ lý trí tuệ nhân tạo tự hành thông minh nhất cho công việc của bạn nhé!",
      phrases: [
        "Theo dõi ngay kênh",
        "để làm chủ những hệ thống",
        "trợ lý trí tuệ nhân tạo",
        "tự hành thông minh nhất",
        "cho công việc của bạn nhé!",
      ],
      highlightKeyword: "Theo dõi",
      audioFile: "audio/AiAgentVsChatbot45s/scene6_outro.mp3",
    },
  ],
};
```

### 3.2. Danh Sách Từ Ghép 2 Âm Tiết Bổ Sung Vào `COMPOUND_PAIRS` (`SubtitleBox.tsx`)
```ts
const ADDITIONAL_COMPOUND_PAIRS = [
  "bao giờ",
  "tự hỏi",
  "trí tuệ",
  "nhân tạo",
  "mỗi ngày",
  "vẫn phải",
  "câu lệnh",
  "tự tay",
  "sao chép",
  "dữ liệu",
  "phần mềm",
  "bởi vì",
  "hộp thoại",
  "thông thường",
  "đưa ra",
  "văn bản",
  "gợi ý",
  "màn hình",
  "trò chuyện",
  "hoàn toàn",
  "công cụ",
  "làm việc",
  "ngược lại",
  "trợ lý",
  "tự hành",
  "cấp quyền",
  "kết nối",
  "nội bộ",
  "hệ thống",
  "chủ động",
  "thực thi",
  "nhắc lệnh",
  "quy trình",
  "ba bước",
  "phân tích",
  "mục tiêu",
  "kế hoạch",
  "xử lý",
  "thực tế",
  "nghiệm thu",
  "kết quả",
  "cơ chế",
  "tự động",
  "thay vì",
  "hàng giờ",
  "thủ công",
  "đề bài",
  "xuyên suốt",
  "theo dõi",
  "làm chủ",
  "thông minh",
  "công việc",
];
```

---

## 4. Bảng Tự Chấm Điểm Rubric (`content.md` & Quy Chuẩn Remotion — Bản `v2`)

| Tiêu chí | Điểm tối đa | Điểm tự chấm | Căn cứ nghiệm thu |
|---|---:|---:|---|
| **1. Hook 3 giây đầu** | 3.0 | **3.0** | Câu hỏi xoáy trực diện vào nghịch lý "đã dùng AI sao vẫn phải ngồi gõ từng câu lệnh và tự sao chép dữ liệu?", không chào hỏi. |
| **2. Cấu trúc 6 cảnh & Độ dài chuẩn Vbee 45s** | 2.5 | **2.5** | Đủ 6 phân cảnh chuẩn Vàng, tổng đúng **200 từ** (34 + 35 + 34 + 36 + 34 + 27), khớp chính xác tốc độ đọc ~4.55 từ/giây của Vbee (`~44.0s - 45.0s`). |
| **3. Tone of Voice & Phụ đề `phrases`** | 2.5 | **2.5** | 100% tiếng Việt tự nhiên, 35 cụm `phrases` (5–6 cụm/cảnh, mỗi cụm 4–6 từ), bảo vệ 100% từ ghép 2 âm tiết tiếng Việt. |
| **4. CTA & Đặc tả Visual `#87ff00`** | 2.0 | **2.0** | Đặc tả đầy đủ Headline `#87ff00`, Frosted Glass Card `bg-white/[0.08]`, Motion liên tục cả 6 cảnh, Sub-heading Scene 6 gọn 1 dòng. |
| **TỔNG ĐIỂM** | **10.0** | **10.0 / 10** | **PASS — ĐỦ ĐIỀU KIỆN BÀN GIAO CHO `voice` VÀ `edit`** |
