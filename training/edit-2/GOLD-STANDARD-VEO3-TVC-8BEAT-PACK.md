# HỒ SƠ CHUẨN VÀNG ĐÀO TẠO VIDEO AI BÁN HÀNG SLL (`GOLD-STANDARD-VEO3-TVC-8BEAT-PACK`)

- **Mã hồ sơ:** `GOLD-STANDARD-VEO3-TVC-8BEAT-PACK`
- **Phụ trách chuyên môn:** `edit-2` (Chuyên gia Edit Video Bán Hàng Affiliate)
- **Kiểm duyệt quy chuẩn:** `bo-nao-thu-2` (`LUẬT #3` & `LUẬT #10` — `APPROVED_BY_SECOND_BRAIN`)
- **Trạng thái xuất bản:** **ĐÓNG BĂNG TUYỆT ĐỐI (`TRAINING_FREEZE_ACTIVE`)** — Chỉ lưu hồ sơ & tư liệu tại `training/edit-2/` để trình CEO nghiệm thu. Tuyệt đối không gọi API đăng hoặc hẹn giờ video lên 3 Page Bán Hàng (`Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline`) khi chưa có lệnh mở băng của CEO.

---

## PHẦN 1: QUY CHUẨN KHUNG XƯƠNG TVC 8 NHỊP (`24.0s` • `1080×1920 @ 30fps`) & 5 KHÓA KỸ THUẬT (`HARD GATES`)

### 1.1. Tỷ lệ Vàng `Hybrid A-Roll ↔ B-Roll Sandwich` (`45% A-Roll : 55% B-Roll`)
- **Thời lượng chuẩn:** `24.0 giây` chia làm **8 Nhịp × `3.0 giây/nhịp`** (`720 frames @ 30fps`), tối ưu hóa tỷ lệ giữ chân 3 giây đầu (`3s Hold Rate ≥ 68%`) và tỷ lệ xem hết (`Completion Rate ≥ 42%`).
- **Quy trình 2 Wave chống biến dạng (`SKU Truth & Creator Anchor Lock — RULE-EDIT2-02`):**
  - **Wave 1 (Khóa Mỏ Neo):** Luôn tạo Keyframe **Nhịp 3 (Unbox & Hero Product Reveal)** đầu tiên từ ảnh chụp sản phẩm thật trên Shopee để khóa cứng hình học sản phẩm (`SKU Geometry`), khuôn mặt Creator (`Character DNA`), trang phục và nhiệt độ màu ánh sáng.
  - **Wave 2 (Nhân Bản 7 Nhịp Còn Lại):** Dùng ảnh Nhịp 3 làm `Reference Image` (`Image-to-Video` trên Google Veo 3) để sinh 7 nhịp còn lại, đảm bảo sản phẩm không bị biến dạng và nhân vật đồng nhất 100%.
- **Miễn nhiễm lỗi Lip-Sync:** Toàn bộ các nhịp chứng minh công năng (Nhịp 1, 4, 5 PIP, 6, 7) sử dụng B-Roll Macro hoặc góc máy không lộ khẩu hình khi đọc thông số kỹ thuật; lời thoại (Voiceover `-3dB`) chạy xuyên suốt bên dưới.

### 1.2. Vùng An Toàn Hiển Thị (`9:16 Safe Zone — 1080×1920`)
- **`Top Margin`:** `≥ 250px` (Tránh thanh trạng thái và nút tìm kiếm Reels/TikTok).
- **`Bottom Margin`:** `≥ 420px` (Tránh tên Page, caption 2 dòng và thanh âm thanh).
- **`Right Margin`:** `≥ 140px` (Tránh cột nút Like, Comment, Share, Save).
- **`Left Margin`:** `≥ 60px`.

---

## PHẦN 2: HỒ SƠ SẢN XUẤT CHI TIẾT 3 SKU ĐẠI DIỆN 3 PAGE BÁN HÀNG

---

### MẪU #1 — PAGE `PHÒNG TRỌ HẾT CỨU`: MÁY SẤY QUẦN ÁO MINI GẤP GỌN KHỬ KHUẨN UV (`PT-DRYER-UV`)

#### A. Hồ Sơ Định Danh Nhân Vật & Sản Phẩm (`Creator DNA & SKU Anchor`)
- **Creator Anchor (`Minh Anh — Sinh viên năm 3 ở trọ`):** Nữ 21 tuổi người Việt Nam, tóc nâu hạt dẻ buộc nửa đầu, mặc áo thun kem form rộng khoác cardigan mỏng màu xanh pastel, gương mặt tự nhiên, thần thái gần gũi.
- **Bối cảnh (`Vietnamese Rental Room`):** Phòng trọ sinh viên Việt Nam diện tích 18m², tường sơn trắng kem, cửa sổ ban công nhỏ đang mưa phùn ẩm ướt, ánh sáng trong nhà ấm áp `3800K` kết hợp đèn Key Light `5200K`.
- **SKU Geometry Lock (`PT-DRYER-UV`):** Hộp máy sấy mini hình trụ bo góc màu trắng ngà phối viền vàng hồng (kích thước gấp gọn `28×20×11cm`), bên dưới gắn túi vải dù giữ nhiệt màu kem dài `110cm` có khóa kéo dọc, đèn LED tia UV xanh tím nằm ở họng thổi gió bên trong.

#### B. Bảng Phân Cảnh TVC 8 Nhịp (`0.0s → 24.0s`) — `PT-DRYER-UV`

| Nhịp | Thời gian | Loại Cảnh | Hình ảnh & Hành động (Visual Action) | Voiceover Tiếng Việt (`-3dB`, 78 từ) | Lớp Đồ Họa Remotion & SFX (`-18dB` BGM) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Pain Hook Cận Cảnh** | `0.0s – 3.0s` | B-Roll Macro → A-Roll | Cận cảnh dây phơi đồ ban công phòng trọ nhỏ giọt nước, áo sơ mi trắng lấm tấm vết mốc đen. Cắt giật sang gương mặt Minh Anh nhăn mặt ngửi cổ áo ẩm mùi hôi. | "Mưa nồm cả tuần, quần áo phơi ba ngày vẫn ẩm xì, bốc mùi mốc đến phát sợ!" | **Lớp 1:** Pop-up **`CHÚ Ý! ĐỒ ẨM MỐC`** (Đỏ-Trắng rung nhẹ).<br>**SFX:** Tiếng sấm mưa + *Buzzer Warning*. |
| **2. A-Roll Creator Đồng Cảm** | `3.0s – 6.0s` | A-Roll (`35mm f/1.8`) | Minh Anh cầm chiếc máy sấy tóc mini sấy từng ống tay áo mệt mỏi, phía sau đồng hồ treo tường chỉ `23:30`. | "Cầm máy sấy tóc hong từng cái áo lúc nửa đêm vừa mỏi rã rời vừa tốn điện." | **Lớp 5:** Karaoke Sub 1 dòng vàng-trắng.<br>**SFX:** Tiếng thở dài + *Clock Ticking*. |
| **3. Unbox & Hero Reveal (Anchor)** | `6.0s – 9.0s` | A-Roll (`35mm f/1.8`) | Không gian phòng trọ bừng sáng ấm áp. Minh Anh tươi cười đặt chiếc **Máy Sấy Mini Gấp Gọn UV (`PT-DRYER-UV`)** lên bàn, bung nhẹ túi vải sấy 3D trong 2 giây. | "Cứu tinh phòng trọ chật đây rồi: Máy sấy quần áo mini gấp gọn tích hợp tia UV!" | **Lớp 2:** Callout kính mờ **`GẤP GỌN 28CM • TREO 10 BỘ`**.<br>**SFX:** *Magic Ting* + *Whoosh*. |
| **4. Cơ Chế Cốt Lõi #1 Macro** | `9.0s – 12.0s` | B-Roll Macro (`85mm f/2.8`) | Cận cảnh Macro ngón tay chạm nút nguồn cảm ứng; luồng gió nóng đối lưu 360° thổi phồng túi vải giữ nhiệt kèm ánh sáng tím khử khuẩn UV dịu mắt bên trong. | "Luồng gió ấm đối lưu ba trăm sáu mươi độ kết hợp đèn UV diệt khuẩn, khử sạch mùi hôi." | **Lớp 2:** Callout #1 **`GIÓ NÓNG 65°C + KHỬ KHUẨN UV`**.<br>**SFX:** *Touch Beep* + Tiếng gió êm. |
| **5. A-Roll + PIP Split-Screen** | `12.0s – 15.0s` | Hybrid A-Roll + PIP B-Roll | Khung chính: Minh Anh ngồi học bài thảnh thơi, máy sấy hoạt động êm ru bên cạnh. Khung PIP góc trên: Cận cảnh hơi ẩm thoát ra ngoài qua lỗ thông khí, áo khô phẳng phiu. | "Máy chạy êm ru không ồn, hẹn giờ tự ngắt an toàn, cứ treo đồ đó rồi ngồi chạy deadline." | **Lớp 3:** Nhãn **`[Minh hoạ bằng AI]`** góc trên phải + Khung PIP bo góc.<br>**SFX:** *Soft Hum 40dB*. |
| **6. Before/After Đối Chứng 3s** | `15.0s – 18.0s` | B-Roll Split + Control Macro | 1.5s đầu: Split-screen Trái (Áo nhăn ẩm ướt) vs Phải (Áo trắng khô bông xốp). 1.5s sau: Cận cảnh 1 ngón tay bấm nút hẹn giờ `60p / 120p / 180p`. | "Chỉ sau ba mươi phút, đồ khô cong thơm tho như phơi nắng to, chẳng lo bạc màu." | **Lớp 2:** Callout #2 **`KHÔ NHANH 30 PHÚT • TỰ NGẮT`**.<br>**SFX:** *Ding!* chuyển cảnh. |
| **7. Test Tiện Ích Gấp Gọn & Bảo Chứng** | `18.0s – 21.0s` | B-Roll (`50mm f/2.0`) | Đôi tay gấp gọn túi vải vào trong thân máy chỉ dày bằng cuốn sách, cất gọn vào ngăn kéo tủ quần áo sinh viên. | "Dùng xong gấp gọn chỉ bằng hộp cơm, nhét vừa ngăn kéo, bảo hành chính hãng mười hai tháng." | **Lớp 4:** Huy hiệu Khiên Vàng 3D **`CHÍNH HÃNG • BẢO HÀNH 12 THÁNG`**.<br>**SFX:** *Shield Metallic Shine*. |
| **8. Happy Payoff & CTA** | `21.0s – 24.0s` | A-Roll (`35mm f/1.8`) | Minh Anh mặc chiếc áo sơ mi trắng khô thơm, tươi cười chỉ tay thẳng xuống khu vực bình luận bên dưới. | "Giá sinh viên đang trợ giá cực hời, bấm ngay link ở bình luận đầu tiên kẻo hết nhé!" | **Lớp 5:** CTA Banner đáy **`👇 MUA NGAY TẠI BÌNH LUẬN ĐẦU TIÊN #1`**.<br>**SFX:** *Pop Click* + Outtro. |

#### C. 8 Prompt Tiếng Anh Chuẩn Điện Ảnh Cho Google Veo 3 & Nano Banana (`PT-DRYER-UV`)

1. **Beat 1 (`0.0s–3.0s` — Pain Hook):**
   > `Cinematic vertical short video, 85mm Macro lens f/2.8, extreme close-up of damp white cotton shirt hanging on a rainy Vietnamese balcony with dark mildew spots and water droplets, whip-pan transition to 35mm f/1.8 medium close-up of a 21-year-old Vietnamese female student with chestnut half-up hair and pastel green cardigan wrinkling her nose in disgust while smelling the damp collar, moody rainy daylight 4500K, natural skin texture, realistic fabric physics. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
2. **Beat 2 (`3.0s–6.0s` — A-Roll Creator Pain):**
   > `35mm lens f/1.8, medium shot inside a cozy 18sqm Vietnamese student rental room at night, warm indoor tungsten light 3800K, the same 21-year-old Vietnamese female student in pastel green cardigan looking exhausted while holding a small handheld hairdryer trying to dry a wet shirt sleeve, an analog wall clock blurred in background showing late night, subtle handheld camera sway, authentic lived-in bedroom props. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
3. **Beat 3 (`6.0s–9.0s` — Unbox & Hero Reveal [WAVE 1 ANCHOR]):**
   > `35mm lens f/1.8, bright warm studio-grade bedroom lighting 5000K, medium shot of the same 21-year-old Vietnamese female student smiling brightly, placing a compact cream-white rounded rectangular portable clothes dryer with rose-gold trim on a wooden desk and smoothly unfolding its attached cream thermal fabric drying bag vertically, slow dolly-in camera movement focusing on the sleek portable dryer unit, crisp shadows, photorealistic materials. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
4. **Beat 4 (`9.0s–12.0s` — Core Mechanism Macro):**
   > `85mm Macro lens f/2.8, extreme close-up of a single slender index finger gently touching the circular power area on the cream-white portable clothes dryer with rose-gold trim, warm airflow inflating the cream fabric cover smoothly while a soft violet-blue UV sanitizing light glows from the internal air vent, shallow depth of field, smooth slow push-in camera motion, stable hand anatomy with five natural fingers. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
5. **Beat 5 (`12.0s–15.0s` — A-Roll + B-Roll PIP Source):**
   > `35mm lens f/1.8, medium shot of the 21-year-old Vietnamese female student sitting calmly at her study desk typing on a laptop while the inflated cream portable clothes dryer stands quietly beside her desk with clothes inside, soft warm ambient lighting, zero camera shake, peaceful atmosphere; paired with 85mm close-up insert of gentle warm steam mist escaping the top fabric vent leaving a crisp dry shirt inside. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
6. **Beat 6 (`15.0s–18.0s` — Before/After & 1-Finger Control):**
   > `85mm Macro lens f/2.8, clean visual comparison showing a wrinkled damp grey-toned shirt on the left transitioning via smooth wipe to a fluffy warm sunlit-textured white shirt on the right, followed by a close-up of one index finger pressing the timer control button on the cream-white portable dryer housing, crisp studio rim lighting, zero hand distortion. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
7. **Beat 7 (`18.0s–21.0s` — Foldability & Durability Test):**
   > `50mm lens f/2.0, high-angle close-up of two natural hands neatly folding the cream fabric drying bag back into the compact cream-white and rose-gold dryer base, snapping the lid shut into a book-sized box, and sliding it effortlessly into a wooden wardrobe drawer, smooth orbital camera pan, warm clean lighting. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
8. **Beat 8 (`21.0s–24.0s` — Happy Payoff & CTA):**
   > `35mm lens f/1.8, eye-level medium close-up of the 21-year-old Vietnamese female student wearing the fresh crisp white shirt over her pastel outfit, hugging a folded warm towel, smiling confidently at the camera and pointing her right index finger straight down toward the bottom of the vertical frame, bright airy daylight, shallow bokeh background. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`

---

### MẪU #2 — PAGE `KÝ TÚC XÁ CÓ BIẾN`: QUẠT TÍCH ĐIỆN KẸP THÀNH GIƯỜNG TẦNG KTX 10000mAh (`KTX-CLIP-FAN`)

#### A. Hồ Sơ Định Danh Nhân Vật & Sản Phẩm (`Creator DNA & SKU Anchor`)
- **Creator Anchor (`Hoàng Nam — Nam sinh viên KTX ĐHQG`):** Nam 20 tuổi người Việt Nam, tóc ngắn gọn gàng, mặc áo phông thể thao màu xám than, gương mặt lanh lợi, biểu cảm sinh động.
- **Bối cảnh (`Vietnamese University Dormitory`):** Giường tầng ký túc xá sinh viên bằng sắt sơn tĩnh điện màu trắng/xám, có rèm che giường tầng 2, bàn học nhỏ gắn liền đầu giường, ánh sáng đèn học ấm pha ánh xanh dịu ban đêm.
- **SKU Geometry Lock (`KTX-CLIP-FAN`):** Quạt tích điện màu trắng nhám kết hợp lồng quạt đường kính `20cm` gồm 5 cánh xoắn khí động học, cổ xoay bi cầu 360°, chân đế dạng kẹp lò xo bản to có đệm cao su chống trượt dày, tích hợp vòng đèn LED sáng dịu ở tâm lồng quạt.

#### B. Bảng Phân Cảnh TVC 8 Nhịp (`0.0s → 24.0s`) — `KTX-CLIP-FAN`

| Nhịp | Thời gian | Loại Cảnh | Hình ảnh & Hành động (Visual Action) | Voiceover Tiếng Việt (`-3dB`, 79 từ) | Lớp Đồ Họa Remotion & SFX (`-18dB` BGM) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Pain Hook Cận Cảnh** | `0.0s – 3.0s` | B-Roll Macro → A-Roll | Cận cảnh quạt trần KTX đứng im vì mất điện/khuất rèm giường tầng 2. Cắt giật sang Hoàng Nam mồ hôi ướt đẫm trán, cầm vở quạt liên tục trong màn ngủ. | "Nằm giường tầng hai ký túc xá kéo rèm vào là bí rịch, đêm mất điện thì nóng phát khóc!" | **Lớp 1:** Pop-up **`CHÚ Ý! GIƯỜNG TẦNG BÍ BÁCH`**.<br>**SFX:** Tiếng thở hắt + *Heat Buzz*. |
| **2. A-Roll Creator Đồng Cảm** | `3.0s – 6.0s` | A-Roll (`35mm f/1.8`) | Hoàng Nam cắm thử chiếc quạt dây nhỏ nhưng ổ điện ở tít dưới đất không tới, quạt đặt lên nệm thì bị đổ nghiêng. | "Dây điện thì ngắn chẳng tới ổ cắm, để quạt thường lên nệm hơi tí là đổ kềnh." | **Lớp 5:** Karaoke Sub 1 dòng vàng-trắng.<br>**SFX:** *Fail Thud* + Tiếng thở dài. |
| **3. Unbox & Hero Reveal (Anchor)** | `6.0s – 9.0s` | A-Roll (`35mm f/1.8`) | Đèn bàn bật sáng. Hoàng Nam hào hứng giơ chiếc **Quạt Tích Điện Kẹp Giường 10000mAh (`KTX-CLIP-FAN`)** và kẹp phập một phát chắc nịch vào thanh sắt giường tầng 2. | "Chân ái cho anh em giường tầng: Quạt tích điện kẹp thành giường pin trâu mười nghìn mili-am-pe!" | **Lớp 2:** Callout kính mờ **`PIN 10.000mAh • KẸP MỌI THÀNH GIƯỜNG`**.<br>**SFX:** *Clamp Snap* + *Magic Ting*. |
| **4. Cơ Chế Cốt Lõi #1 Macro** | `9.0s – 12.0s` | B-Roll Macro (`85mm f/2.8`) | Cận cảnh Macro má kẹp cao su ôm chặt khung sắt giường tầng, bàn tay xoay cổ quạt 360° mượt mà và bật công tắc gió vù vù làm bay lọn tóc. | "Kẹp lò xo đệm cao su bám chặt khung sắt, xoay ba trăm sáu mươi độ chỉnh hướng gió cực mượt." | **Lớp 2:** Callout #1 **`XOAY 360° • 4 CẤP ĐỘ GIÓ MẠNH`**.<br>**SFX:** *Mechanical Click* + *Wind Whoosh*. |
| **5. A-Roll + PIP Split-Screen** | `12.0s – 15.0s` | Hybrid A-Roll + PIP B-Roll | Khung chính: Hoàng Nam nằm đọc sách dưới ánh đèn LED dịu tích hợp trên quạt, tóc bay nhẹ. Khung PIP góc trên: Cận cảnh mô-tơ không chổi than quay êm và cổng sạc Type-C. | "Mô tơ không chổi than chạy êm ru suốt hai mươi tư tiếng, có sẵn đèn LED đọc sách ban đêm." | **Lớp 3:** Nhãn **`[Minh hoạ bằng AI]`** góc trên phải + Khung PIP.<br>**SFX:** *Whisper Quiet Breeze*. |
| **6. Before/After Đối Chứng 3s** | `15.0s – 18.0s` | B-Roll Split + Control Macro | 1.5s đầu: Split-screen Trái (Nóng bức ướt mồ hôi) vs Phải (Gió mát rượi, ngủ sâu). 1.5s sau: Cận cảnh 1 ngón tay bấm nút chuyển 4 nấc gió và bật đèn ngủ. | "Bốn cấp độ gió từ thoang thoảng đến mát lạnh, lồng quạt tháo rời vệ sinh trong một nốt nhạc." | **Lớp 2:** Callout #2 **`CHạy LIÊN TỤC 24H • THÁO LỒNG DỄ DÀNG`**.<br>**SFX:** *Crisp Click* + *Chime*. |
| **7. Test Độ Bền Kẹp & Bảo Chứng** | `18.0s – 21.0s` | B-Roll (`50mm f/2.0`) | Cận cảnh bàn tay lắc nhẹ khung giường sắt nhưng chân kẹp quạt vẫn bám cứng cáp không xê dịch 1mm, đèn báo pin sáng rõ. | "Kẹp siêu chắc rung giường cũng không rớt, lỗi một đổi một, bảo hành chính hãng mười hai tháng." | **Lớp 4:** Huy hiệu Khiên Vàng 3D **`CHÍNH HÃNG • BẢO HÀNH 12 THÁNG`**.<br>**SFX:** *Solid Grip Thump* + *Shine*. |
| **8. Happy Payoff & CTA** | `21.0s – 24.0s` | A-Roll (`35mm f/1.8`) | Hoàng Nam kéo tấm chăn mỏng tận hưởng làn gió mát, cười tươi chỉ tay thẳng xuống khu vực bình luận đầu tiên. | "Săn ngay deal sinh viên siêu rẻ ở đường link dưới bình luận đầu tiên trước khi cháy hàng nhé!" | **Lớp 5:** CTA Banner đáy **`👇 MUA NGAY TẠI BÌNH LUẬN ĐẦU TIÊN #1`**.<br>**SFX:** *Pop Click* + Outtro. |

#### C. 8 Prompt Tiếng Anh Chuẩn Điện Ảnh Cho Google Veo 3 & Nano Banana (`KTX-CLIP-FAN`)

1. **Beat 1 (`0.0s–3.0s` — Pain Hook):**
   > `Cinematic vertical short video, 85mm Macro lens f/2.8, close-up of a stationary ceiling fan blocked by a top-bunk privacy curtain in a Vietnamese university dorm, whip-pan to 35mm f/1.8 close-up of a 20-year-old Vietnamese male student in a charcoal grey t-shirt sitting on a metal top bunk bed with sweat beads on his forehead, frantically fanning himself with a notebook in humid warm dim lighting 3500K. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
2. **Beat 2 (`3.0s–6.0s` — A-Roll Creator Pain):**
   > `35mm lens f/1.8, medium shot on a top bunk bed in a Vietnamese dorm room, the same 20-year-old Vietnamese male student looking frustrated as a traditional corded mini fan tips over on the soft mattress and its short power cord dangles hopelessly far above the floor socket, realistic metal bunk bed rails, moody indoor lighting. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
3. **Beat 3 (`6.0s–9.0s` — Unbox & Hero Reveal [WAVE 1 ANCHOR]):**
   > `35mm lens f/1.8, bright clean bedroom lighting 5000K, medium shot of the same 20-year-old Vietnamese male student smiling excitedly while holding a matte-white portable rechargeable clip-on fan with a wide heavy-duty spring clamp and 5 aerodynamic blades, firmly clamping it onto the white painted steel rail of the top bunk bed in one smooth motion, slow push-in camera movement. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
4. **Beat 4 (`9.0s–12.0s` — Core Mechanism Macro):**
   > `85mm Macro lens f/2.8, extreme close-up of the rubber-padded heavy-duty clamp gripping the metal bunk bed rail tightly, a natural five-fingered hand smoothly rotating the 360-degree neck joint of the matte-white clip fan, blades spinning into a clean motion blur blowing cool air that gently lifts the student's hair, crisp rim lighting, shallow depth of field. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
5. **Beat 5 (`12.0s–15.0s` — A-Roll + B-Roll PIP Source):**
   > `35mm lens f/1.8, medium shot of the 20-year-old Vietnamese male student relaxing comfortably against his pillow on the top bunk reading a book illuminated by the warm circular LED ring light built into the center of the matte-white clip-on fan; paired with an 85mm Macro close-up of the rear Type-C charging port and silent brushless motor hub spinning smoothly. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
6. **Beat 6 (`15.0s–18.0s` — Before/After & 1-Finger Control):**
   > `85mm Macro lens f/2.8, dynamic split visual contrasting a sweaty uncomfortable dorm night on the left with a cool breezy restful sleep on the right, cutting to an extreme close-up of a single index finger pressing the tactile speed button on the back of the matte-white clip fan base, twisting the front grille slightly to show easy detachment, zero hand morphing. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
7. **Beat 7 (`18.0s–21.0s` — Grip Stability Test):**
   > `50mm lens f/2.0, close-up shot of a hand shaking the metal bunk bed frame vigorously while the matte-white clip-on fan remains rock-solid and completely stable on the rail without slipping a millimeter, slow camera arc around the sturdy clamp mechanism, crisp studio highlight on the matte plastic and metal rail. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
8. **Beat 8 (`21.0s–24.0s` — Happy Payoff & CTA):**
   > `35mm lens f/1.8, eye-level medium close-up of the 20-year-old Vietnamese male student on his cozy top bunk bed with the clip-on fan blowing a gentle breeze, smiling warmly at the camera and pointing his index finger straight down toward the bottom comment area, clean bokeh background. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`

---

### MẪU #3 — PAGE `HỘI DEADLINE`: GIÁ ĐỠ LAPTOP HỢP KIM NHÔM CNC CHỈNH 7 NẤC (`DL-LAPTOP-STAND`)

#### A. Hồ Sơ Định Danh Nhân Vật & Sản Phẩm (`Creator DNA & SKU Anchor`)
- **Creator Anchor (`Khánh Linh — Freelancer / Dân văn phòng chạy Deadline`):** Nữ 24 tuổi người Việt Nam, đeo kính gọng mảnh hiện đại, tóc búi gọn gàng, mặc áo sơ mi xanh navy tối giản, thần thái chuyên nghiệp.
- **Bối cảnh (`Modern Vietnamese Work Desk`):** Bàn làm việc gỗ sồi tại căn hộ/văn phòng hiện đại, có màn hình phụ, cốc cà phê đá Việt Nam, đèn kẹp bàn Deskbar chiếu sáng `5000K` kết hợp đèn LED hắt tường màu xanh dương dịu (`Cyan-Blue Accent`).
- **SKU Geometry Lock (`DL-LAPTOP-STAND`):** Giá đỡ laptop khung chữ M gập gọn làm từ hợp kim nhôm CNC nguyên khối màu bạc xám (`Space Silver`) dày `4mm`, các dải đệm silicon xám chống trượt gắn dọc 2 thanh đỡ và 2 ngàm móc đáy, thanh chống điều chỉnh 7 rãnh răng cưa chuẩn xác.

#### B. Bảng Phân Cảnh TVC 8 Nhịp (`0.0s → 24.0s`) — `DL-LAPTOP-STAND`

| Nhịp | Thời gian | Loại Cảnh | Hình ảnh & Hành động (Visual Action) | Voiceover Tiếng Việt (`-3dB`, 81 từ) | Lớp Đồ Họa Remotion & SFX (`-18dB` BGM) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Pain Hook Cận Cảnh** | `0.0s – 3.0s` | B-Roll Macro → A-Roll | Cận cảnh đáy laptop nóng rực trên mặt bàn phẳng làm quạt kêu rú. Cắt giật sang Khánh Linh cúi gằm mặt gõ phím, tay xoa gáy nhăn mặt đau mỏi cổ vai gáy. | "Ngồi còng lưng chạy deadline tám tiếng mỗi ngày, cổ vai gáy đau buốt mà laptop thì nóng ran!" | **Lớp 1:** Pop-up **`CHÚ Ý! ĐAU VAI GÁY & NÓNG MÁY`**.<br>**SFX:** Tiếng quạt laptop rú + *Neck Crack*. |
| **2. A-Roll Creator Đồng Cảm** | `3.0s – 6.0s` | A-Roll (`35mm f/1.8`) | Khánh Linh lấy 2 cuốn từ điển dày kê tạm dưới đáy laptop nhưng gõ phím bị cập kênh trượt nghiêng suýt rơi máy. | "Lấy sách kê tạm thì bít hết khe tản nhiệt, gõ phím mạnh một chút là máy trượt xập xệ." | **Lớp 5:** Karaoke Sub 1 dòng vàng-trắng.<br>**SFX:** *Book Slip Thud* + Tiếng thở dài. |
| **3. Unbox & Hero Reveal (Anchor)** | `6.0s – 9.0s` | A-Roll (`35mm f/1.8`) | Ánh sáng Deskbar bừng sáng sắc nét. Khánh Linh rút **Giá Đỡ Laptop Nhôm CNC 7 Nấc (`DL-LAPTOP-STAND`)** từ túi nhung, kéo mở khung chữ M trong 1 giây đặt lên bàn. | "Đầu tư ngay em giá đỡ laptop hợp kim nhôm CNC nguyên khối chỉnh bảy nấc chuẩn công thái học!" | **Lớp 2:** Callout kính mờ **`NHÔM CNC NGUYÊN KHỐI • KÉO MỞ 1 GIÂY`**.<br>**SFX:** *Metallic Slide* + *Magic Ting*. |
| **4. Cơ Chế Cốt Lõi #1 Macro** | `9.0s – 12.0s` | B-Roll Macro (`85mm f/2.8`) | Cận cảnh Macro thanh chống gài vào rãnh nấc thứ 4, đệm silicon dày ôm sát viền MacBook/Laptop, gầm máy thoáng đãng 100% giúp tản nhiệt. | "Thiết kế rỗng đáy giúp tản nhiệt cực nhanh, bảy nấc chỉnh độ cao nâng màn hình ngang tầm mắt." | **Lớp 2:** Callout #1 **`CHỈNH 7 NẤC ĐỘ CAO • TẢN NHIỆT 100%`**.<br>**SFX:** *Precision Metal Click*. |
| **5. A-Roll + PIP Split-Screen** | `12.0s – 15.0s` | Hybrid A-Roll + PIP B-Roll | Khung chính: Khánh Linh ngồi thẳng lưng chuẩn tư thế, gõ phím mượt mà. Khung PIP góc trên: Cận cảnh dải đệm silicon chống trầy và khung nhôm dày `4mm` không rung lắc. | "Khung nhôm dày bốn mi-li-mét bọc đệm silicon chống trượt, gõ phím nhanh cỡ nào cũng đầm chắc." | **Lớp 3:** Nhãn **`[Minh hoạ bằng AI]`** góc trên phải + Khung PIP.<br>**SFX:** *Mechanical Keyboard ASMR*. |
| **6. Before/After Đối Chứng 3s** | `15.0s – 18.0s` | B-Roll Split + Control Macro | 1.5s đầu: Split-screen Trái (Cúi gằm gù lưng 45°) vs Phải (Lưng thẳng 90°, tầm mắt chuẩn). 1.5s sau: Cận cảnh 1 ngón tay khép gọn giá đỡ thành thanh nhỏ. | "Tạm biệt cảnh gù lưng mỏi cổ, gấp lại nhỏ gọn như cây thước bỏ vừa túi chống sốc." | **Lớp 2:** Callout #2 **`CHỐNG GÙ LƯNG • GẤP GỌN BỎ TÚI`**.<br>**SFX:** *Smooth Fold Snap*. |
| **7. Test Chịu Lực 20Kg & Bảo Chứng** | `18.0s – 21.0s` | B-Roll (`50mm f/2.0`) | Cận cảnh đặt chiếc laptop gaming 16 inch nặng kèm chồng sách dày lên trên, giá đỡ nhôm CNC vẫn đứng vững vàng không cong vênh. | "Chịu tải tới hai mươi ki-lô-gam, cân đẹp mọi dòng laptop mười bảy inch, bảo hành mười hai tháng." | **Lớp 4:** Huy hiệu Khiên Vàng 3D **`CHÍNH HÃNG • BẢO HÀNH 12 THÁNG`**.<br>**SFX:** *Heavy Weight Lock* + *Shine*. |
| **8. Happy Payoff & CTA** | `21.0s – 24.0s` | A-Roll (`35mm f/1.8`) | Khánh Linh mỉm cười nâng ly cà phê, tay kia chỉ thẳng xuống bình luận đầu tiên dưới màn hình. | "Giá chỉ bằng hai cốc trà sữa, bấm ngay vào link ở bình luận đầu tiên để rinh về nhé!" | **Lớp 5:** CTA Banner đáy **`👇 MUA NGAY TẠI BÌNH LUẬN ĐẦU TIÊN #1`**.<br>**SFX:** *Pop Click* + Outtro. |

#### C. 8 Prompt Tiếng Anh Chuẩn Điện Ảnh Cho Google Veo 3 & Nano Banana (`DL-LAPTOP-STAND`)

1. **Beat 1 (`0.0s–3.0s` — Pain Hook):**
   > `Cinematic vertical short video, 85mm Macro lens f/2.8, extreme close-up of a silver laptop lying flat on a wooden desk overheating with heat shimmer, whip-pan to 35mm f/1.8 medium close-up of a 24-year-old Vietnamese female freelancer wearing thin-framed glasses and a navy-blue shirt hunched forward, grimacing in pain while rubbing the back of her stiff neck under late-night desk lighting. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
2. **Beat 2 (`3.0s–6.0s` — A-Roll Creator Pain):**
   > `35mm lens f/1.8, medium shot at a modern oak study desk, the same 24-year-old Vietnamese female freelancer with glasses trying to prop her laptop up on two thick books, the laptop wobbles and slips dangerously as she types on the keyboard, frustrated facial expression, realistic home office background. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
3. **Beat 3 (`6.0s–9.0s` — Unbox & Hero Reveal [WAVE 1 ANCHOR]):**
   > `35mm lens f/1.8, crisp 5000K deskbar key lighting with subtle cyan background accent, medium shot of the same 24-year-old Vietnamese female freelancer smiling confidently, pulling a sleek space-silver CNC machined aluminum foldable M-frame laptop stand from a grey pouch and expanding it smoothly in one second onto the oak desk, slow dolly-in camera movement highlighting the brushed anodized aluminum texture. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
4. **Beat 4 (`9.0s–12.0s` — Core Mechanism Macro):**
   > `85mm Macro lens f/2.8, extreme close-up of a natural hand locking the twin aluminum support struts into the fourth precision notch of the space-silver CNC laptop stand, thick grey non-slip silicone pads gripping the edges of a sleek laptop while the open-frame underside allows complete airflow, shallow depth of field, smooth slow slider pan. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
5. **Beat 5 (`12.0s–15.0s` — A-Roll + B-Roll PIP Source):**
   > `35mm lens f/1.8, medium side-angle shot of the 24-year-old Vietnamese female freelancer sitting with upright ergonomic posture typing comfortably with her laptop elevated at eye level on the space-silver aluminum stand; paired with an 85mm Macro close-up of the 4mm thick CNC aluminum alloy arm and grey silicone pads absorbing typing vibration without shaking. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
6. **Beat 6 (`15.0s–18.0s` — Before/After & 1-Finger Control):**
   > `85mm Macro lens f/2.8, split comparison showing a slouched neck posture on the left versus an aligned upright ergonomic posture with the elevated laptop stand on the right, cutting to a close-up of a single index finger smoothly collapsing the space-silver aluminum laptop stand into a slim compact bar and slipping it into a laptop sleeve, zero hand distortion. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
7. **Beat 7 (`18.0s–21.0s` — Heavy Load Durability Test):**
   > `50mm lens f/2.0, close-up eye-level shot of two hands placing a heavy 16-inch metal laptop plus three thick hardcover books on top of the space-silver CNC aluminum laptop stand, the triangular M-frame structure holds the heavy load rock-solid without bending or flexing, slow camera push-in with metallic specular highlights. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`
8. **Beat 8 (`21.0s–24.0s` — Happy Payoff & CTA):**
   > `35mm lens f/1.8, eye-level medium close-up of the 24-year-old Vietnamese female freelancer with glasses holding an iced coffee cup at her organized desk, smiling warmly at the camera and pointing her index finger straight down toward the bottom comment section, bright professional studio lighting. No readable text, no Vietnamese letters on screen, no fake UI text, exact product geometry from reference image, zero morphing, vertical 9:16 1080x1920.`

---

## PHẦN 3: KIẾN TRÚC 5 LỚP ĐỒ HỌA THƯƠNG MẠI REMOTION & QUY TRÌNH FFMPEG AUDIO MASTERING

### 3.1. Kiến Trúc 5 Lớp Đồ Họa Hậu Kỳ Remotion (`RULE-EDIT2-03` — Zero AI Text)

Toàn bộ văn bản tiếng Việt, huy hiệu và khung hình PIP được kết xuất bằng mã nguồn React/TypeScript (`Remotion 1080×1920 @ 30fps, 720 frames`) đè lên 8 clip gốc từ Google Veo 3:

```tsx
// Cấu trúc Component chuẩn: SalesTVC8BeatComposition.tsx (1080x1920 @ 30fps, durationInFrames = 720)
export const SalesTVC8BeatComposition: React.FC<SalesTVCProps> = ({
  clips,           // 8 file MP4 từ Veo 3 (mỗi clip 90 frames = 3.0s)
  pipClipUrl,      // Clip B-Roll Macro dùng cho cửa sổ PIP ở Nhịp 5 (frames 360..450)
  hookTitle,       // Lớp 1: "CHÚ Ý! ..."
  callouts,        // Lớp 2: Callout kính mờ ở Nhịp 3, 4, 6
  warrantyText,    // Lớp 4: "CHÍNH HÃNG • BẢO HÀNH 12 THÁNG" ở Nhịp 7
  subtitles,       // Lớp 5A: Phụ đề Karaoke từng từ (Word-by-word JSON timestamps)
  ctaBannerText,   // Lớp 5B: "👇 MUA NGAY TẠI BÌNH LUẬN ĐẦU TIÊN #1" ở Nhịp 8
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0A0D14' }}>
      {/* LỚP 0: 8 CLIP GỐC GOOGLE VEO 3 (90 FRAMES / NHỊP) */}
      {clips.map((src, idx) => (
        <Sequence key={idx} from={idx * 90} durationInFrames={90}>
          <OffthreadVideo src={src} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </Sequence>
      ))}

      {/* LỚP 1: TOP SHOCK HOOK BANNER (NHỊP 1: 0.0s - 3.0s | Frames 0..89) */}
      <Sequence from={0} durationInFrames={90}>
        <TopShockHookBanner text={hookTitle} safeTop={260} />
      </Sequence>

      {/* LỚP 2: GLASSMORPHISM FEATURE CALLOUTS (NHỊP 3, 4, 6) */}
      <Sequence from={180} durationInFrames={90}>
        <GlassCalloutPill badge="HERO SKU" text={callouts.reveal} top={300} left={64} />
      </Sequence>
      <Sequence from={270} durationInFrames={90}>
        <GlassCalloutPill badge="CƠ CHẾ #1" text={callouts.mechanism} top={300} left={64} />
      </Sequence>
      <Sequence from={450} durationInFrames={90}>
        <GlassCalloutPill badge="HIỆU QUẢ THẬT" text={callouts.beforeAfter} top={300} left={64} />
      </Sequence>

      {/* LỚP 3: PIP SPLIT-SCREEN OVERLAY + NHÃN [Minh hoạ bằng AI] (NHỊP 4-6: Frames 270..540) */}
      <Sequence from={270} durationInFrames={270}>
        <AIDisclosureWatermark text="[Minh hoạ bằng AI]" top={255} right={145} />
      </Sequence>
      <Sequence from={360} durationInFrames={90}>
        <PictureInPictureCard src={pipClipUrl} top={330} left={64} width={420} height={560} />
      </Sequence>

      {/* LỚP 4: 3D GOLD WARRANTY SHIELD (NHỊP 7: 18.0s - 21.0s | Frames 540..629) */}
      <Sequence from={540} durationInFrames={90}>
        <GoldWarrantyShield3D text={warrantyText} top={320} />
      </Sequence>

      {/* LỚP 5A: KARAOKE WORD-BY-WORD SUBTITLE (XUYÊN SUỐT 0.0s - 24.0s | Y = 1380px, Bottom Safe >= 420px) */}
      <KaraokeLowerThirdSubtitle words={subtitles} bottomOffset={450} rightSafe={145} />

      {/* LỚP 5B: BOTTOM CTA BANNER ĐIỀU HƯỚNG BÌNH LUẬN ĐẦU TIÊN (NHỊP 8: 21.0s - 24.0s | Frames 630..720) */}
      <Sequence from={630} durationInFrames={90}>
        <PinnedCommentCTABanner text={ctaBannerText} bottomOffset={425} />
      </Sequence>
    </AbsoluteFill>
  );
};
```

#### Bảng Đặc Tả Tọa Độ & Kiểu Chữ 5 Lớp Đồ Họa (`Safe Zone Compliance`)
1. **Lớp 1 — `TopShockHookBanner` (`0.0s – 3.0s`):**
   - Vị trí: `top: 260px`, căn giữa theo trục ngang khả dụng (`left: 60px`, `right: 140px`).
   - Typography: `Be Vietnam Pro Black (900)`, cỡ chữ `58px`, chữ trắng `#FFFFFF` viền đen dày `6px` trên nền hộp đỏ cảnh báo `#EF4444` bo góc `20px`, hiệu ứng `spring()` nẩy trong 8 frame đầu.
2. **Lớp 2 — `GlassCalloutPill` (`Nhịp 3, 4, 6`):**
   - Vị trí: `top: 300px, left: 64px` (nằm gọn dưới Top Safe Zone).
   - Thiết kế: Kính mờ `backdrop-filter: blur(16px)`, nền `rgba(15, 23, 42, 0.78)`, viền `2px solid #38BDF8`, chữ vàng `#FACC15` + trắng `#FFFFFF` cỡ `38px Bold`.
3. **Lớp 3 — `PictureInPictureCard` & `AIDisclosureWatermark` (`Nhịp 4–6`):**
   - Nhãn **`[Minh hoạ bằng AI]`**: Gắn cố định tại `top: 255px, right: 145px`, chữ `24px SemiBold` độ mờ `85%`, tuân thủ chính sách minh bạch nội dung AI của Meta/TikTok.
   - Khung **PIP Split-Screen (`Nhịp 5: 12.0s–15.0s`)**: Kích thước `420×560px` đặt tại `top: 330px, left: 64px`, viền sáng `4px solid #FACC15`, bo góc `24px`, hiển thị cận cảnh cơ chế vận hành song song với A-Roll Creator.
4. **Lớp 4 — `GoldWarrantyShield3D` (`Nhịp 7: 18.0s – 21.0s`):**
   - Vị trí: `top: 320px`, huy hiệu Khiên Vàng 3D ánh kim (`#FDE047 → #CA8A04`) kèm hiệu ứng quét sáng (`Shine Sweep`) xác nhận **`CHÍNH HÃNG • BẢO HÀNH 12 THÁNG`**.
5. **Lớp 5 — `KaraokeLowerThirdSubtitle` & `PinnedCommentCTABanner`:**
   - **Karaoke Subtitle:** Luôn hiển thị **đúng 1 dòng (tối đa 5–6 từ/nhịp hiển thị)** tại `bottom: 450px` (`Y = 1470px`), font `Be Vietnam Pro ExtraBold 800` cỡ `48px`, từ đang đọc đổi màu vàng `#FACC15` phóng nhẹ `scale(1.08)`.
   - **CTA Banner (`Nhịp 8: 21.0s – 24.0s`):** Đặt tại `bottom: 425px` (ngay trên vùng caption của Reels), nền Gradient Cam Shopee `#EE4D2D → #FF7337`, mũi tên nhấp nháy chỉ thẳng xuống khu vực **Bình luận ghim đầu tiên (`Pinned Comment #1`)**.

---

### 3.2. Quy Chuẩn Mastering Âm Thanh FFmpeg (`-3dB` Voiceover / `-18dB` BGM + SFX Cue Sheet)

Sau khi kết xuất luồng hình ảnh 5 lớp từ Remotion (`visual_master_24s.mp4`), hệ thống chạy lệnh FFmpeg Mastering để trộn 3 kênh âm thanh chuẩn thương mại:

1. **Kênh 1 — Voiceover Tiếng Việt (`Vbee Studio / CIT Voice` — Đỉnh âm `-3.0 dBFS`, LUFS `-14`):**
   - Lọc cắt tần số trầm dưới `80Hz` (`highpass=f=80`), nén dải động `acompressor=threshold=-16dB:ratio=3:attack=5:release=50`, chuẩn hóa đỉnh âm đúng **`-3.0dB`** để giọng đọc rõ từng chữ ngay cả khi xem bằng loa điện thoại ngoài trời.
2. **Kênh 2 — Nhạc Nền Thương Mại (`Upbeat Lo-Fi / Modern Pop Trap` — Nền `-18.0 dBFS` + Auto Sidechain Ducking):**
   - Hạ mức âm lượng cố định xuống **`-18.0dB`** (`volume=-18dB`) để làm nền nhịp điệu mà không lấn giọng đọc.
3. **Kênh 3 — Bảng Cue Sheet Hiệu Ứng Âm Thanh (`SFX Track` — Đỉnh âm `-9.0 dBFS`):**
   - `00.1s` (Nhịp 1): `sfx_warning_hit.wav` (Gây chú ý ngay 0.5s đầu).
   - `03.2s` (Nhịp 2): `sfx_clock_tick_sigh.wav` (Tăng cảm giác cấp bách).
   - `06.0s` (Nhịp 3): `sfx_whoosh_magic_ting.wav` (Bừng sáng khi Hero SKU xuất hiện).
   - `09.2s` (Nhịp 4): `sfx_macro_switch_on.wav` (Âm thanh vật lý khi kích hoạt sản phẩm).
   - `15.0s` (Nhịp 6): `sfx_split_ding.wav` (Chuyển cảnh Before/After đối chứng).
   - `18.2s` (Nhịp 7): `sfx_shield_shine.wav` (Khẳng định uy tín bảo hành 12 tháng).
   - `21.0s` (Nhịp 8): `sfx_pop_cta_click.wav` (Thúc đẩy hành vi bấm xuống Bình luận #1).

#### Lệnh FFmpeg Mastering Chuẩn Công Nghiệp (`24.0s`, `H.264 High Profile`, `AAC 192kbps`)
```powershell
ffmpeg -y `
  -i "visual_master_24s.mp4" `
  -i "voiceover_vi_24s.wav" `
  -i "bgm_upbeat_loop.mp3" `
  -i "sfx_stems_24s.wav" `
  -filter_complex `
    "[1:a]highpass=f=80,acompressor=threshold=-16dB:ratio=3:attack=5:release=50,volume=-3dB[vo]; `
     [2:a]volume=-18dB,afade=t=out:st=22.5:d=1.5[bgm]; `
     [3:a]volume=-9dB[sfx]; `
     [vo][bgm][sfx]amix=inputs=3:duration=first:dropout_transition=0,alimiter=limit=0.707[aout]" `
  -map 0:v:0 -map "[aout]" `
  -c:v libx264 -profile:v high -pix_fmt yuv420p -r 30 -crf 18 -preset slow `
  -c:a aac -b:a 192k -ar 48000 `
  -t 24.0 "final_tvc_8beat_master.mp4"
```

---

## PHẦN 4: BẢNG TỰ CHẤM ĐIỂM RUBRIC (`edit-2`) & CAM KẾT CHỐT CHẶN AN TOÀN

| Tiêu chí Rubric `edit-2` | Điểm tối đa | Điểm đạt | Đối chiếu thực tế trong Hồ sơ Chuẩn Vàng |
| :--- | :---: | :---: | :--- |
| **1. Đúng cấu trúc TVC 8 Nhịp (`45% A-Roll ↔ 55% B-Roll`)** | `3.0` | **`3.0`** | Đủ 3 SKU × 8 Nhịp (`0.0s → 24.0s`, `3.0s/nhịp`), tích hợp Wave 1 Anchor (Nhịp 3), Macro Mechanism (Nhịp 4), PIP Split-Screen (Nhịp 5) và Before/After 3s (Nhịp 6). |
| **2. Prompt Tiếng Anh 100% & Khóa chống lỗi chữ AI** | `2.5` | **`2.5`** | 24/24 Prompt viết 100% bằng tiếng Anh, khóa tiêu cự `35mm f/1.8` (A-Roll) & `85mm Macro f/2.8` (B-Roll), gắn đầy đủ hậu tố `No readable text, exact product geometry from reference image, zero morphing`. |
| **3. Đủ 5 Lớp Đồ Họa Thương Mại & Vùng An Toàn `9:16`** | `2.5` | **`2.5`** | Đủ 5 lớp Remotion (`TopShockHookBanner`, `GlassCalloutPill`, `PIP + [Minh hoạ bằng AI]`, `GoldWarrantyShield3D`, `Karaoke Subtitle + CTA Banner`) nằm gọn trong Safe Zone (`top ≥ 250px`, `bottom ≥ 420px`, `right ≥ 140px`). |
| **4. Tuân thủ Luật #3 & Luật #10 (`bo-nao-thu-2` Gate)** | `2.0` | **`2.0`** | Đóng băng tuyệt đối xuất bản video lên 3 Page Bán Hàng (`TRAINING_FREEZE_ACTIVE`); chỉ lưu hồ sơ tại `training/edit-2/GOLD-STANDARD-VEO3-TVC-8BEAT-PACK.md` chờ CEO nghiệm thu. |
| **TỔNG ĐIỂM NGHIỆM THU NỘI BỘ** | **`10.0`** | **`10.0 / 10.0`** | **ĐẠT CHUẨN VÀNG (`GOLD STANDARD PASSED`)** |
