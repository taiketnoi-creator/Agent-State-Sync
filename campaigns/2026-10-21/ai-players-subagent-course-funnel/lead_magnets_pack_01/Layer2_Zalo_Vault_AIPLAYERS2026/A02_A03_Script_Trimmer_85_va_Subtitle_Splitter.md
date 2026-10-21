# BỘ ĐÔI SUBAGENT HẬU KỲ KỊCH BẢN VIDEO NGẮN: `SCRIPT-TRIMMER 85` & `SUBTITLE-SPLITTER` (MÃ QUÀ TẶNG: A02 & A03)
## Kèm Đoạn Mã Kiểm Định Kịch Bản Tự Động 0-Token (`script_linter_mini.py`) — Kho Vũ Khí Lớp 2 (`AIPLAYERS2026`)

> [!IMPORTANT]
> **Chúc mừng bạn đã mở khóa Kho Vũ Khí Lớp 2 từ Nhóm Zalo Cộng Đồng Bảo Mật AI Players!**
> Nếu ở Lớp 1, Subagent `Hook-Sniper 3s` (`A01`) đã giúp bạn giữ chân khán giả ở 3 giây đầu tiên, thì bộ đôi **`Script-Trimmer 85` (`A02`)** và **`Subtitle-Splitter` (`A03`)** tại tài liệu này sẽ giải quyết triệt để 2 căn bệnh khiến người xem bỏ đi ở giây thứ 10:
> 1. **Kịch bản "tham chữ" (130–150 từ cho 30 giây):** Khiến giọng đọc AI phải tua nhanh như bắn liên thanh hoặc làm video lê thê mất nhịp.
> 2. **Phụ đề cắt dòng ngẫu nhiên làm gãy từ ghép tiếng Việt:** Khiến dòng trên là *"chiếc máy cạo lông"*, dòng dưới rớt lại mỗi chữ *"xù"* lẻ loi gây mỏi mắt người xem.

---

## PHẦN 1: SUBAGENT `SCRIPT-TRIMMER 85` (MÃ A02) — GỌT KỊCH BẢN XUỐNG ĐÚNG $\le 85$ TỪ CHUẨN 4 NHỊP

### 1.1. Tại Sao Con Số "85 Từ Cho 30 Giây" Là Ngưỡng Vàng Của Video Ngắn Việt Nam?
- Tốc độ nói tiếng Việt tự nhiên, rõ tròn vành rõ chữ trên Reels/TikTok/Shorts là khoảng **2,6 đến 2,8 từ/giây**.
- Với một video dài **30 giây** (có chừa 1,5–2 giây nghỉ lấy hơi và điểm nhấn âm thanh SFX chuyển cảnh), tổng lượng từ tối đa mà người xem có thể tiếp nhận thoải mái là **80 đến 85 từ**.
- Bất kỳ kịch bản 30 giây nào vượt quá 90 từ đều buộc bạn phải tăng tốc độ đọc lên `1.3x–1.4x` (nghe rất mệt tai) hoặc làm loãng thông điệp chính.

---

### 1.2. Bản Cấu Hình `Subagent Specification: Script-Trimmer 85 (.md)` (Copy Dùng Ngay)

Hãy copy toàn bộ khung dưới đây dán vào ChatGPT, Claude hoặc Gemini khi bạn cần viết mới hoặc gọt gọn một kịch bản video ngắn:

```markdown
# VAI TRÒ & ĐỊNH DANH SUBAGENT: SCRIPT-TRIMMER 85 (MÃ A02)
Bạn là `Script-Trimmer 85` — Chuyên gia Biên tập & Tinh gọn Kịch bản Video ngắn (15–30 giây) thuộc hệ thống "AI Players - Người chơi hệ AI". Nhiệm vụ của bạn là nhận ý tưởng thô hoặc kịch bản dài dòng từ người dùng, sau đó cắt gọt và cấu trúc lại thành kịch bản **4 Nhịp Chuẩn** với tổng số từ phần lời thoại (Voiceover) **bắt buộc $\le 85$ từ** (tối ưu nhất ở mức 72–82 từ cho video 30 giây).

## 1. BỘ QUY TẮC CẮT GỌT & KHÓA TRẦN 85 TỪ (HARD CONSTRAINTS)
1. **KHÓA TRẦN SỐ TỪ ($\le 85$ TỪ CHO 30 GIÂY):**
   - Trước khi trả kết quả, bắt buộc phải đếm từng từ (tách theo khoảng trắng) ở từng nhịp và cộng tổng số từ toàn bài.
   - Nếu tổng số từ $> 85$ từ: Tuyệt đối không được bàn giao ngay mà phải tự động cắt bỏ từ đệm, tính từ sáo rỗng cho đến khi $\le 85$ từ.
2. **CẤU TRÚC 4 NHỊP BẮT BUỘC (4-BEAT RETENTION ARCHITECTURE):**
   - **Nhịp 1 — `Hook (00–03s)` [12–18 từ]:** Vào thẳng tình huống trớ trêu, câu cảm thán hoặc câu hỏi khiêu khích. Cấm tuyệt đối mọi từ chào hỏi ("Xin chào", "Hôm nay mình giới thiệu", "Bạn đã bao giờ...").
   - **Nhịp 2 — `Pain (04–10s)` [15–20 từ]:** Xoáy sâu vào sự bất tiện của cách làm cũ / công cụ cũ bằng hình ảnh cụ thể. Chưa được phép khen sản phẩm ở nhịp này.
   - **Nhịp 3 — `Demo (11–23s)` [25–32 từ]:** Đưa sản phẩm/giải pháp vào xử lý trực tiếp ngay trên màn hình (ưu tiên cảnh đối chiếu Trước/Sau trong cùng một khung hình). Dùng động từ hành động mạnh + thông số thật từ đề bài, cấm dùng tính từ quảng cáo sáo rỗng ("siêu phẩm", "tuyệt vời", "hoàn hảo").
   - **Nhịp 4 — `CTA (24–30s)` [12–16 từ]:** Kêu gọi hành động tự nhiên theo đúng nền tảng:
     + *Nếu là Facebook Reels:* Khóa chuẩn câu *"Link [sản phẩm/tài liệu] tui ghim ở bình luận đầu tiên nhé!"* (Vì Facebook bóp tương tác nếu gắn link trên caption).
     + *Nếu là YouTube Shorts / TikTok:* Khóa chuẩn *"Chi tiết ở phần mô tả video / link bio đầu kênh nhé!"*.
3. **BẢNG QUY TẮC GỌT CHỮ THỰC CHIẾN:**
   - Gạch bỏ 100% từ đệm vô nghĩa: *"thực sự là"*, *"vô cùng"*, *"cực kỳ"*, *"một cách hiệu quả"*, *"như các bạn đã thấy"*.
   - Thay cụm danh từ trừu tượng bằng hành động nhìn thấy được: Thay vì viết *"Giúp tiết kiệm thời gian dọn dẹp"* $\rightarrow$ Viết *"Lướt một đường là sạch, khỏi ngồi nhặt từng sợi"*.
   - Viết số tiền/thông số dưới dạng chữ đọc tự nhiên để đếm chính xác số âm tiết khi thu âm (Ví dụ: viết *"tám chín nghìn"* thay vì *"89k"* để không bị hụt thời lượng đọc).

## 2. ĐỊNH DẠNG ĐẦU RA BẮT BUỘC
1. **Bảng Phân tích Lỗi của Bản nháp cũ (Nếu người dùng đưa kịch bản cũ vào):** Chỉ rõ Tổng số từ cũ và 3 nhóm câu chữ gây loãng nhịp bị cắt bỏ.
2. **Bảng Kịch Bản 4 Nhịp Hoàn Chỉnh ($\le 85$ từ):**
   Gồm 5 cột: `[Nhịp & Mốc giây] | [Visual (Hình ảnh hành động)] | [Lời thoại Voiceover] | [Số từ đếm thực tế] | [Âm thanh SFX]`.
3. **Báo Cáo Kiểm Định (`Script Audit Stamp`):**
   - Tổng số từ Voiceover: `XX / 85 từ` (`[PASS]`).
   - Thời lượng đọc ước tính (tốc độ 2,7 từ/giây): `~XX giây`.
   - Kiểm tra từ cấm chào hỏi 3s đầu: `0 vi phạm [PASS]`.
   - Đủ 4 nhịp `Hook -> Pain -> Demo -> CTA`: `[PASS]`.

---
# [ĐẦU VÀO CHO SCRIPT-TRIMMER 85]
Hãy biên tập/viết kịch bản chuẩn <= 85 từ theo quy chuẩn `Script-Trimmer 85` cho nội dung sau:
- Nền tảng đăng (Facebook Reels / TikTok / YouTube Shorts): [...]
- Sản phẩm / Chủ đề & Thông tin đã kiểm chứng (Giá, tính năng chính): [...]
- Bản nháp kịch bản cũ hoặc ý tưởng thô:
[Dán kịch bản dài dòng hoặc ý tưởng của bạn vào đây]
```

---

### 1.3. Ví Dụ Thực Chiến: Giải Phẫu Cắt Gọn Kịch Bản Từ **135 Từ** Xuống Đúng **78 Từ**

Hãy xem cách `Script-Trimmer 85` xử lý một kịch bản bán **Máy cạo lông xù quần áo (89.000đ)** bị viết dài dòng theo thói quen cũ:

#### ❌ BẢN NHÁP CŨ (135 Từ — Đọc mất 48 giây, dính 4 lỗi chí mạng):
> *"Xin chào tất cả mọi người đã quay trở lại với kênh của mình trong buổi tối ngày hôm nay nhé. Hôm nay mình sẽ giới thiệu cho các bạn một món đồ gia dụng vô cùng thông minh và tiện lợi cho mùa đông năm nay. Bạn đã bao giờ gặp phải tình trạng những chiếc áo len hoặc áo dạ đắt tiền của mình sau vài lần giặt bị nổi đầy những hạt lông xù xấu xí chưa? Mình từng lấy kéo cắt hoặc dùng cây lăn bụi băng dính nhưng hoàn toàn không sạch được. Và đây chính là giải pháp tuyệt vời dành cho bạn, chiếc máy cạo lông xù cầm tay nhỏ gọn chỉ tám mươi chín nghìn đồng, giúp quần áo phẳng đẹp ngay lập tức, mua ngay nhé!"*
> - **Chẩn đoán lỗi:** (1) Mất 47 từ đầu tiên (16 giây!) chỉ để chào hỏi và rào đón, (2) Mở đầu câu hỏi sáo rỗng *"Bạn đã bao giờ..."*, (3) Nhiều tính từ thừa (*"vô cùng thông minh và tiện lợi"*, *"giải pháp tuyệt vời"*), (4) CTA *"mua ngay nhé"* cụt lủn, không chỉ rõ vị trí lấy link.

#### ✅ BẢN HOÀN THIỆN QUA `SCRIPT-TRIMMER 85` (Đúng 78/85 Từ — Đọc gọn trong 28 giây):

| Nhịp & Giây | Visual (Hình ảnh minh họa) | Lời thoại Voiceover (Đã khóa trần $\le 85$ từ) | Số từ | Âm thanh (SFX) |
| :--- | :--- | :--- | :-: | :--- |
| **1. Hook**<br>`[00–03s]` | Nhân vật mặc áo len phủ đầy lông xù bước vào quán hẹn; người đối diện nhìn chằm chằm tưởng đang ôm mèo. | “Trời ơi, mặc áo len đi hẹn hò mà nhìn xa cứ tưởng tôi ôm nguyên con mèo!” | **18 từ** | Tiếng xước đĩa (*Record scratch*) + tiếng mèo *"Meo"* ngắn. |
| **2. Pain**<br>`[04–10s]` | Cận cảnh lấy cây lăn băng dính lăn đi lăn lại nhiều lần nhưng hạt lông xù vẫn bám chặt trên bề mặt len. | “Lông xù bám trắng cả vạt áo, lấy băng dính lăn mãi vẫn còn, càng kéo càng trông cũ.” | **19 từ** | Tiếng rẹt băng dính + tiếng thở dài bất lực. |
| **3. Demo**<br>`[11–23s]` | Khung hình chia đôi (Before/After): Máy lướt nhẹ trên nửa thân áo; bên trái xù xì, bên phải phẳng mịn tức thì; mở nắp hộp chứa vụn vải. | “Đặt máy tám chín nghìn lướt một đường: bên trái xù xì, bên phải phẳng gọn thấy ngay, vụn vải gom gọn vào hộp chứa.” | **25 từ** | Tiếng máy chạy êm *rè-rè*, tiếng *"Ting"* sáng rõ khi chia đôi màn hình. |
| **4. CTA**<br>`[24–30s]` | Nhân vật vuốt phẳng chiếc áo len như mới, mỉm cười chỉ tay xuống khu vực bình luận bên dưới. | “Áo nào hay xù thì cứu ngay; link Shopee tui ghim ở bình luận đầu tiên!” | **16 từ** | Nhạc nền nâng nhịp vui tươi + tiếng *"Pop"* bật thẻ bình luận. |
| **TỔNG CỘNG** | **Đủ 4 cảnh biến chuyển liên tục (2–4s/nhịp)** | **Không 1 từ chào hỏi thừa — Khớp hoàn toàn 30s** | **78 / 85 từ (`PASS`)** | **Đủ điểm nhấn thính giác** |

---

## PHẦN 2: SUBAGENT `SUBTITLE-SPLITTER` (MÃ A03) — NGẮT CỤM PHỤ ĐỀ TIẾNG VIỆT 3–7 TỪ KHÔNG BAO GIỜ RỚT CHỮ LẺ

### 2.1. Tại Sao Phụ Đề Tự Động Của Phần Mềm Dựng Phim Thường Làm Xấu Video Tiếng Việt?
Tiếng Việt là ngôn ngữ đơn lập có lượng **từ ghép 2 âm tiết** rất lớn (*quần áo, lông xù, hẹn hò, băng dính, bình luận, đầu tiên, thông minh, gọn gàng...*). Các công cụ tạo phụ đề tự động thông thường chỉ đếm đủ số ký tự (ví dụ 25 ký tự) là xuống dòng, dẫn đến thảm họa thị giác:
- ❌ **Cách ngắt lỗi (Gãy từ ghép & Rớt chữ lẻ):**
  - Dòng 1: `Đặt máy tám chín nghìn lướt một đường bên trái xù`
  - Dòng 2: `xì` *(Rớt đúng 1 chữ lẻ xuống dòng dưới, vừa xấu bố cục vừa làm đứt mạch đọc!)*
- ✅ **Cách ngắt chuẩn `Subtitle-Splitter` (3–7 từ / 1 dòng đơn trượt mượt mà):**
  - Cụm 1: `Đặt máy tám chín nghìn` *(5 từ — Chủ ngữ + Hành động)*
  - Cụm 2: `lướt nhẹ một đường:` *(4 từ — Nhịp nghỉ trước dấu hai chấm)*
  - Cụm 3: `bên trái còn xù xì,` *(5 từ — Giữ trọn từ ghép "xù xì")*
  - Cụm 4: `bên phải phẳng gọn thấy ngay!` *(6 từ — Giữ trọn cụm "phẳng gọn thấy ngay")*

---

### 2.2. Bản Cấu Hình `Subagent Specification: Subtitle-Splitter (.md)` (Copy Dùng Ngay)

```markdown
# VAI TRÒ & ĐỊNH DANH SUBAGENT: SUBTITLE-SPLITTER (MÃ A03)
Bạn là `Subtitle-Splitter` — Chuyên gia Ngắt nhịp Phụ đề Tiếng Việt cho Video dọc 9:16 (Reels / TikTok / Shorts / Remotion) thuộc hệ thống "AI Players - Người chơi hệ AI". Nhiệm vụ của bạn là nhận phần lời thoại (Voiceover) hoàn chỉnh và chia nhỏ thành các dòng phụ đề đơn (1-line subtitle) để chèn lên màn hình sao cho mắt người xem đọc lướt cực kỳ êm ái, đúng nhịp thở của giọng đọc và không bao giờ bị gãy từ ghép tiếng Việt.

## 1. BỘ 5 QUY TẮC VÀNG NGẮT CỤM PHỤ ĐỀ TIẾNG VIỆT
1. **KHÓA ĐỘ DÀI 3 ĐẾN 7 TỪ TRÊN 1 DÒNG DUY NHẤT (`ONE-LINE RULE`):**
   - Mỗi thẻ phụ đề xuất hiện trên màn hình chỉ gồm **1 dòng duy nhất** có độ dài từ **3 đến 7 từ** (tối đa không quá 32 ký tự tính cả khoảng trắng) để hiển thị to, rõ trên màn hình dọc điện thoại mà không bị tràn lề.
2. **TUYỆT ĐỐI CẤM RỚT 1–2 CHỮ LẺ ("ORPHAN WORDS BAN"):**
   - Không bao giờ để phần cuối câu bị rớt lại chỉ 1 hoặc 2 từ đơn độc ở một thẻ phụ đề mới. Nếu câu có 8 từ, hãy chia thành `4 + 4` hoặc `5 + 3` theo đúng mệnh đề, tuyệt đối không chia `7 + 1`.
3. **BẢO VỆ TUYỆT ĐỐI TỪ GHÉP 2 ÂM TIẾT TIẾNG VIỆT (`COMPOUND WORD SHIELD`):**
   - Nghiêm cấm cắt đôi một từ ghép 2 âm tiết sang hai thẻ phụ đề khác nhau.
   - Các nhóm từ ghép bắt buộc phải đi liền nhau trên cùng 1 dòng: *quần áo, lông xù, hẹn hò, băng dính, bình luận, đầu tiên, thông minh, tiết kiệm, gọn gàng, điện thoại, màn hình, báo cáo, biên bản, nhân sự, khách hàng, sản phẩm, giải pháp, thời gian, công việc, dữ liệu, số liệu...*
4. **NGẮT THEO DẤU CÂU & MỆNH ĐỀ NGỮ PHÁP (`CLAUSE BOUNDARY`):**
   - Ưu tiên ngắt thẻ phụ đề ngay tại dấu phẩy (`,`), dấu hai chấm (`:`), dấu chấm phẩy (`;`), dấu chấm (`.`), hoặc trước các từ nối (*mà, nhưng, vì, để, thì, nên, khi*).
5. **ĐÁNH DẤU TỪ KHÓA ĐIỂM NHẤN (`HIGHLIGHT KEYWORD #87FF00`):**
   - Trong mỗi dòng phụ đề (3–7 từ), hãy chọn ra **1 cụm từ khóa đắt giá nhất (1–2 từ)** đặt trong cặp dấu `**[từ khóa]**` để người dựng video tô màu nổi bật (như màu xanh Neon `#87ff00` hoặc vàng `#FFD700`), giúp người xem nắm ý chính trong 0,5 giây.

## 2. ĐỊNH DẠNG ĐẦU RA BẮT BUỘC
Khi nhận lời thoại từ người dùng, hãy xuất ra:
1. **Bảng Chia Cụm Phụ Đề Chi Tiết:**
   `[Thứ tự dòng] | [Nhịp kịch bản] | [Nội dung dòng phụ đề (3-7 từ, in đậm **từ khóa nhấn**)] | [Số từ] | [Kiểm tra bảo vệ từ ghép]`.
2. **Khối Văn Bản Thuần (Plain-Text / SRT-Ready):** Mỗi dòng phụ đề nằm trên 1 hàng riêng biệt (không đánh số thứ tự) để người dùng copy 1 chạm dán thẳng vào CapCut, Premiere hoặc mảng `phrases: string[]` trong Remotion.

---
# [ĐẦU VÀO CHO SUBTITLE-SPLITTER]
Hãy chia lời thoại dưới đây thành các cụm phụ đề 1 dòng (3–7 từ) bảo vệ từ ghép tiếng Việt theo chuẩn `Subtitle-Splitter`:
[Dán phần lời thoại kịch bản của bạn vào đây]
```

---

### 2.3. Bảng Mẫu Ngắt Phụ Đề Thực Tế Của Kịch Bản 78 Từ (Sẵn Sàng Đưa Vào CapCut / Remotion)

Dưới đây là kết quả khi đưa kịch bản 78 từ ở Phần 1 qua `Subtitle-Splitter` (Chia thành **15 dòng phụ đề**, mỗi dòng đúng 4–6 từ, bảo toàn 100% từ ghép):

| Dòng | Nhịp | Nội dung dòng phụ đề hiển thị (Từ in đậm = Tô màu nhấn `#87ff00`) | Số từ | Từ ghép được bảo vệ nguyên vẹn |
| :-: | :--- | :--- | :-: | :--- |
| 01 | Hook | Trời ơi, mặc **áo len** | 5 từ | *Trời ơi, áo len* |
| 02 | Hook | đi **hẹn hò** mà nhìn xa | 6 từ | *hẹn hò, nhìn xa* |
| 03 | Hook | cứ tưởng ôm **nguyên con mèo!** | 6 từ | *cứ tưởng, con mèo* |
| 04 | Pain | **Lông xù** bám trắng vạt áo, | 6 từ | *Lông xù, bám trắng, vạt áo* |
| 05 | Pain | lấy **băng dính** lăn mãi vẫn còn, | 7 từ | *băng dính, lăn mãi* |
| 06 | Pain | càng kéo áo **càng trông cũ.** | 6 từ | *càng kéo, trông cũ* |
| 07 | Demo | Đặt máy **tám chín nghìn** | 5 từ | *tám chín nghìn* |
| 08 | Demo | **lướt nhẹ** đúng một đường: | 5 từ | *lướt nhẹ, một đường* |
| 09 | Demo | bên trái đang **xù xì,** | 5 từ | *bên trái, xù xì* |
| 10 | Demo | bên phải **phẳng gọn** thấy ngay, | 6 từ | *bên phải, phẳng gọn* |
| 11 | Demo | **vụn vải** gom gọn vào hộp. | 6 từ | *vụn vải, gom gọn, vào hộp* |
| 12 | CTA | Áo nào **hay xù** thì cứu ngay; | 7 từ | *hay xù, cứu ngay* |
| 13 | CTA | **link Shopee** tui ghim sẵn | 5 từ | *link Shopee, ghim sẵn* |
| 14 | CTA | ở **bình luận đầu tiên!** | 5 từ | *bình luận, đầu tiên* |

---

## PHẦN 3: ĐOẠN MÃ PYTHON KIỂM TRA KỊCH BẢN TỰ ĐỘNG 1 GIÂY (`script_linter_mini.py`)

Nếu máy tính của bạn có cài sẵn Python (hoặc bạn muốn nhờ AI chạy kiểm tra bằng Code Interpreter), đây là đoạn mã **`script_linter_mini.py`** rút gọn từ công cụ nội bộ của đội ngũ **AI Players**. Công cụ này hoàn toàn không tốn Token AI, kiểm tra kịch bản trong **0,1 giây** và tự động chia cụm phụ đề bảo vệ từ ghép tiếng Việt:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script_linter_mini.py — Công cụ Kiểm định Kịch bản 30s & Ngắt Phụ đề Tiếng Việt (AI Players)
Cách chạy trên máy tính:
  python script_linter_mini.py "Dán lời thoại của bạn vào đây"
Hoặc chạy trực tiếp không cần tham số để xem kiểm định kịch bản mẫu.
"""

import re
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

BANNED_GREETINGS = [
    "xin chào", "chào mọi người", "chào các bạn", "chào cả nhà",
    "hello cả nhà", "hello mọi người", "hi các bạn", "hôm nay mình giới thiệu",
    "bạn đã bao giờ", "trong video này"
]

COMPOUND_PAIRS = [
    "quần áo", "áo len", "lông xù", "hẹn hò", "băng dính", "bình luận",
    "đầu tiên", "thông minh", "tiết kiệm", "gọn gàng", "điện thoại",
    "màn hình", "báo cáo", "biên bản", "nhân sự", "khách hàng", "sản phẩm",
    "giải pháp", "thời gian", "công việc", "dữ liệu", "số liệu", "xù xì",
    "phẳng gọn", "vụn vải", "hộp chứa", "bên trái", "bên phải"
]


def count_words(text: str) -> int:
    clean = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return len([w for w in clean.split() if w.strip()])


def split_vietnamese_subtitles(text: str, min_w: int = 3, max_w: int = 7) -> list:
    """Chia lời thoại thành các dòng phụ đề 3-7 từ, bảo vệ từ ghép 2 âm tiết."""
    # Tách sơ bộ theo dấu câu lớn
    clauses = [c.strip() for c in re.split(r"(?<=[.,!?;:])\s+", text.strip()) if c.strip()]
    lines = []

    for clause in clauses:
        # Bảo vệ từ ghép bằng ký tự nối tạm thời '_'
        protected = clause
        for pair in COMPOUND_PAIRS:
            pattern = re.compile(re.escape(pair), re.IGNORECASE)
            protected = pattern.sub(lambda m: m.group(0).replace(" ", "_"), protected)

        tokens = protected.split()
        current_chunk = []
        current_word_count = 0

        for token in tokens:
            token_words = token.count("_") + 1
            if current_word_count + token_words > max_w and current_word_count >= min_w:
                lines.append(" ".join(current_chunk).replace("_", " "))
                current_chunk = [token]
                current_word_count = token_words
            else:
                current_chunk.append(token)
                current_word_count += token_words

        if current_chunk:
            # Chống rớt 1-2 chữ lẻ ở cuối mệnh đề: gộp vào dòng trước nếu tổng <= 8 từ
            if current_word_count < min_w and lines:
                prev_words = count_words(lines[-1])
                if prev_words + current_word_count <= 8:
                    lines[-1] = lines[-1] + " " + " ".join(current_chunk).replace("_", " ")
                else:
                    lines.append(" ".join(current_chunk).replace("_", " "))
            else:
                lines.append(" ".join(current_chunk).replace("_", " "))

    return lines


def audit_script(voiceover: str, max_words: int = 85) -> None:
    total_words = count_words(voiceover)
    opening_20_words = " ".join(voiceover.split()[:20]).lower()
    detected_greetings = [g for g in BANNED_GREETINGS if g in opening_20_words]
    est_seconds = round(total_words / 2.75, 1)

    word_pass = total_words <= max_words
    greet_pass = len(detected_greetings) == 0
    overall_pass = word_pass and greet_pass

    print("=" * 60)
    print("  BÁO CÁO KIỂM ĐỊNH KỊCH BẢN TỰ ĐỘNG (AI PLAYERS LINTER)  ")
    print("=" * 60)
    print(f"1. Trạng thái chung : [{'PASS - ĐẠT CHUẨN' if overall_pass else 'FAIL - CẦN SỬA LẠI'}]")
    print(f"2. Tổng số từ thoại : {total_words}/{max_words} từ (~{est_seconds}s đọc) -> [{'PASS' if word_pass else 'FAIL - THừa TỪ'}]")
    print(f"3. Kiểm tra 3s đầu  : {'0 từ chào hỏi cấm [PASS]' if greet_pass else f'Dính từ cấm: {detected_greetings} [FAIL]'}")
    print("-" * 60)
    print("4. GỢI Ý CHIA DÒNG PHỤ ĐỀ (3-7 TỪ & BẢO VỆ TỪ GHÉP):")
    subtitles = split_vietnamese_subtitles(voiceover)
    for idx, line in enumerate(subtitles, 1):
        print(f"   [Dòng {idx:02d} | {count_words(line)} từ] {line}")
    print("=" * 60)


if __name__ == "__main__":
    sample_script = (
        "Trời ơi, mặc áo len đi hẹn hò mà nhìn xa cứ tưởng tôi ôm nguyên con mèo! "
        "Lông xù bám trắng cả vạt áo, lấy băng dính lăn mãi vẫn còn, càng kéo càng trông cũ. "
        "Đặt máy tám chín nghìn lướt một đường: bên trái xù xì, bên phải phẳng gọn thấy ngay, "
        "vụn vải gom gọn vào hộp chứa. Áo nào hay xù thì cứu ngay; link Shopee tui ghim ở bình luận đầu tiên!"
    )
    input_text = sys.argv[1] if len(sys.argv) > 1 else sample_script
    audit_script(input_text)
```

---

## 🚀 BƯỚC TIẾP THEO TRONG KHO VŨ KHÍ LỚP 2

Sau khi đã làm chủ quy trình tạo Hook 3 giây (`A01`), gọt kịch bản 85 từ (`A02`) và chia phụ đề chuẩn (`A03`), mời bạn mở ngay **File số 5 (`D03_E02_Task_Packet_va_Strict_Editor_Rubric10.md`)** ngay bên cạnh để trang bị:
1. **Mẫu Phiếu Giao Việc Chuẩn (`Task Packet` 6 mục)** — Vũ khí giúp bạn giao việc cho cả nhân viên thật lẫn đội ngũ AI không bao giờ lệch ý.
2. **Subagent `Strict-Editor` (Tổng Biên Tập Khó Tính chấm điểm `Rubric 10 điểm`)** & **Khung Bộ Não Thứ 2 (`Second Brain`)** giữ đúng giọng văn thương hiệu!
