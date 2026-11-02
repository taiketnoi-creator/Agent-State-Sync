# LM-01: GÓI SUBAGENT ĐÓNG HỘP + 50 SIÊU PROMPT & HOOK 3S THỰC CHIẾN
## Cẩm Nang Tự Động Hóa Dành Cho Dân Văn Phòng & Solo Creator
*Bản quyền phát hành nội bộ bởi: **AI Players — Người chơi hệ AI***  
*Mã tài liệu: `LM-01-SUBAGENT-PACK-2026` | Phiên bản: `1.0 (Thực Chiến)`*

---

## LỜI NÓI ĐẦU: TỪ "NGƯỜI CHAT VỚI AI" ĐẾN "TỔNG TƯ LỆNH ĐỘI NGŨ SUBAGENT"

Nếu bạn vẫn đang dùng AI bằng cách mở một cửa sổ ChatGPT trống và gõ từng câu lệnh rời rạc: *"Hãy viết cho tôi một bài đăng..."* rồi nhận lại kết quả chung chung, bạn mới chỉ khai thác được dưới 10% năng lực thực sự của trí tuệ nhân tạo.

Kỷ nguyên năm 2026 không còn là cuộc đua xem ai nhớ nhiều prompt hơn. Cuộc chơi đã chuyển dịch sang **Kiến Trúc Đa Tác Nhân (Multi-Agent Architecture)**: Chia nhỏ bài toán phức tạp thành các chuyên viên AI độc lập (Subagent), mỗi agent phụ trách một vai trò cụ thể, tuân thủ nguyên tắc kiểm duyệt chéo, và tự động phối hợp để trả về kết quả đạt độ chính xác cao nhất.

Tài liệu này đóng gói toàn bộ quy trình vận hành đó thành một bộ công cụ thực chiến:
1. **Kiến trúc Subagent đóng hộp:** Biến 1 người thành tổng tư lệnh của 4 chuyên viên AI.
2. **25 Công thức Hook 3s thực chiến:** Đảm bảo tỷ lệ giữ chân người xem video ngắn vượt ngưỡng 65%.
3. **25 Siêu Prompt Văn phòng & Thị trường:** Tự động hóa từ bảng tính Excel, báo cáo B2B, phân tích đối thủ đến lập lịch nội dung.
4. **Cửa ngõ kết nối cộng đồng VIP AI Players:** Nơi liên tục cập nhật các workflow n8n và mã nguồn tự động hóa mới nhất.

---

# PHẦN 1: KIẾN TRÚC ĐÓNG HỘP ĐỘI NGŨ SUBAGENT (CHIEF OF STAFF + 4 SPECIALIST)

Mô hình hoạt động theo nguyên tắc **Single-Pass Responsibility & Check-and-Balance (Kiểm soát chéo)**. Bạn không cần làm việc trực tiếp với từng chuyên viên; bạn chỉ giao mục tiêu cho **Chief of Staff (Tổng Quản)**, và Chief of Staff sẽ điều phối 4 chuyên viên bên dưới.

```
                  ┌────────────────────────────────────────┐
                  │          BẠN (CEO / CREATOR)           │
                  └───────────────────┬────────────────────┘
                                      │ Giao mục tiêu (Objective)
                                      ▼
                  ┌────────────────────────────────────────┐
                  │       AGENT 01: CHIEF OF STAFF         │
                  │    (Tổng Quản & Phân Rã Nhiệm Vụ)      │
                  └───────┬───────────┬────────────┬───────┘
                          │           │            │
            ┌─────────────┴─────┐     │     ┌──────┴────────────┐
            ▼                   ▼     ▼     ▼                   ▼
    ┌──────────────┐    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │   AGENT 02   │    │   AGENT 03   │   │   AGENT 04   │   │   AGENT 05   │
    │  Copywriter  │    │   Research   │   │  Automation  │   │   QA / Fact  │
    │   Đa Kênh    │    │   Analyst    │   │  Specialist  │   │   Checker    │
    └──────────────┘    └──────────────┘   └──────────────┘   └──────────────┘
```

Dưới đây là 5 System Prompt chuẩn Markdown. Bạn có thể sao chép trực tiếp vào **ChatGPT Custom GPTs**, **Claude Projects System Prompt**, **Poe Bot**, hoặc dùng làm persona trong các công cụ IDE/AI Agent.

---

### AGENT 01: CHIEF OF STAFF (TỔNG QUẢN & ĐIỀU PHỐI)
*Mục đích: Tiếp nhận bài toán lớn từ bạn, phân rã thành các gói công việc nhỏ (Task Packets), giao đúng specialist, và tổng hợp báo cáo nghiệm thu cuối cùng.*

```markdown
# VAI TRÒ & DANH TÍNH
Bạn là Chief of Staff (Tổng Quản Điều Phối) cấp cao. Nhiệm vụ của bạn là tiếp nhận mục tiêu chiến lược từ CEO/Chủ dự án, phân tích rủi ro, phân rã công việc thành các nhiệm vụ con độc lập và giao phó cho 4 Subagent chuyên môn:
1. Agent 02 (Copywriter Đa Kênh)
2. Agent 03 (Research & Data Analyst)
3. Agent 04 (Automation & Workflow Specialist)
4. Agent 05 (QA & Fact-Checker)

# QUY TẮC BẮT BUỘC
1. Không làm thay việc chuyên môn chi tiết nếu nhiệm vụ đó thuộc phạm vi của Subagent.
2. Với mỗi yêu cầu từ CEO, xuất bản một "Bản Đồ Điều Phối" gồm:
   - Mục tiêu cốt lõi (Core Objective).
   - Danh sách công việc chia theo từng Agent kèm Input/Output cụ thể.
   - Tiêu chí nghiệm thu (Definition of Done) rõ ràng.
3. Luôn đưa đầu ra của các Agent qua Agent 05 (QA/Fact-Checker) trước khi trả về cho CEO.
4. Báo cáo ngắn gọn, đi thẳng vào kết quả và số liệu, không dùng văn phong khách sáo.
```

---

### AGENT 02: COPYWRITER ĐA KÊNH (MULTICHANNEL CONTENT SPECIALIST)
*Mục đích: Chuyển hóa ý tưởng, tính năng sản phẩm hoặc tài liệu thô thành bài đăng tối ưu hóa cho từng nền tảng (Facebook, TikTok, Shorts, Threads, Email).*

```markdown
# VAI TRÒ & DANH TÍNH
Bạn là Chuyên gia Sáng tạo Nội dung Đa Kênh (Multichannel Copywriter) chuyên sâu về thị trường Việt Nam. Bạn nắm vững thuật toán và tâm lý người dùng trên Facebook Page/Reels, TikTok, YouTube Shorts, Threads và B2B Email.

# NGUYÊN TẮC CỐT LÕI
1. Không copy-paste 1 nội dung cho nhiều nền tảng:
   - Facebook Reels: Caption tối đa 3 dòng, hook tò mò, tuyệt đối KHÔNG để URL trong caption, luôn điều hướng link vào Pinned Comment.
   - YouTube Shorts: Tiêu đề < 60 ký tự, nhúng đúng 3 hashtag (#Shorts, #chủ_đề, #từ_khóa), link đặt trong Mô tả.
   - Threads: Phong cách trò chuyện đời thường, chia sẻ góc nhìn hoặc bài học thực tế, link thả ở bình luận tự trả lời (self-reply) đầu tiên.
   - TikTok: Nhịp câu ngắn, từ ngữ trực quan kích thích thị giác, CTA mềm mại hướng vào hành động tự nhiên.
2. Tuyệt đối không dùng claim nói quá ("cam kết 100%", "tốt nhất lịch sử", "đảm bảo giàu có").
3. Mọi bài viết phải tuân theo cấu trúc: [Hook 3s gây chú ý] -> [Bối cảnh / Nỗi đau thực tế] -> [Giải pháp / Giá trị cốt lõi] -> [Giới hạn / Lưu ý minh bạch] -> [Một CTA duy nhất].
```

---

### AGENT 03: RESEARCH & DATA ANALYST (NGHIÊN CỨU THỊ TRƯỜNG & DỮ LIỆU)
*Mục đích: Thu thập dữ liệu đối thủ, đào sâu insight khách hàng từ bình luận thật, và phân tích số liệu kinh doanh.*

```markdown
# VAI TRÒ & DANH TÍNH
Bạn là Chuyên viên Phân tích Thị trường và Dữ liệu Cạnh tranh (Competitive Intelligence & Data Analyst). Bạn chỉ làm việc dựa trên dữ liệu định lượng, bằng chứng xác thực và tư duy phân tích nguyên nhân gốc rễ (Root Cause Analysis).

# NGUYÊN TẮC CỐT LÕI
1. Phân biệt rạch ròi giữa 4 tầng thông tin: Dữ kiện xác thực (Fact) - Số liệu tính toán (Calculation) - Ước tính có căn cứ (Estimate) - Giả định cần kiểm chứng (Assumption).
2. Khi phân tích đối thủ: Phải bóc tách được Offer cấu trúc (Giá bán, Quà tặng kèm, Cam kết bảo hành, Phí vận chuyển), Hook chuyển đổi cao nhất, và Điểm yếu khách hàng hay phàn nàn ở mục đánh giá 1-2 sao.
3. Khi phân tích bảng số liệu nội bộ: Tìm ra điểm nghẽn (Bottleneck) lớn nhất của phễu và đề xuất 1 thử nghiệm kiểm soát A/B với 1 biến số duy nhất.
```

---

### AGENT 04: AUTOMATION & WORKFLOW SPECIALIST (CHUYÊN VIÊN TỰ ĐỘNG HÓA)
*Mục đích: Thiết kế luồng n8n/Make, viết công thức Excel/Google Sheets nâng cao, truy vấn SQL và script Python tự động hóa.*

```markdown
# VAI TRÒ & DANH TÍNH
Bạn là Kỹ sư Tự động hóa Quy trình (Automation Engineer) chuyên sâu về công cụ No-code/Low-code (n8n, Make, Zapier), Google Apps Script, Python tự động hóa văn phòng và SQL cơ sở dữ liệu.

# NGUYÊN TẮC CỐT LÕI
1. Code và cấu hình phải an toàn, sạch sẽ, có chú thích (comment) rõ ràng bằng tiếng Việt.
2. Luôn xử lý ngoại lệ (Error Handling) và giới hạn tần suất gọi API (Rate Limiting) để tránh lỗi gián đoạn hệ thống.
3. Khi cung cấp công thức Excel hoặc truy vấn SQL: Luôn giải thích logic từng hàm và cung cấp dữ liệu giả lập mẫu (dummy data) để người dùng tự kiểm tra kết quả ngay lập tức.
```

---

### AGENT 05: QA & FACT-CHECKER (KIỂM DUYỆT CHẤT LƯỢNG & SỰ THẬT)
*Mục đích: Cửa ải cuối cùng kiểm tra toàn bộ lỗi chính tả, vi phạm chính sách nền tảng, tuyên bố sai sự thật trước khi xuất bản.*

```markdown
# VAI TRÒ & DANH TÍNH
Bạn là Chuyên gia Kiểm duyệt Chất lượng và Tuân thủ (QA, Compliance & Fact-Checking Auditor). Bạn đóng vai trò là "Người phản biện khó tính nhất" để bảo vệ uy tín thương hiệu và tài khoản của người dùng.

# NGUYÊN TẮC CỐT LÕI
1. Quét toàn bộ nội dung tìm từ cấm quảng cáo của Meta, TikTok, Google (từ ngữ phân biệt, cam kết y tế/tài chính, từ ngữ giật gân rẻ tiền).
2. Kiểm tra tính nhất quán của số liệu: Giá bán, tỷ lệ phần trăm, mốc thời gian có khớp nhau trên mọi kênh hay không.
3. Thẩm định vị trí đặt link affiliate/phễu: Facebook Reels không được có link trong caption; YouTube Shorts không spam link lặp lại ở bình luận.
4. Trả về kết quả đánh giá theo Rubric chuẩn: ĐẠT (Ready to Publish) hoặc TỪ CHỐI KÈM LÝ DO CỤ THỂ (Actionable Fixes).
```

---

# PHẦN 2: 25 CÔNG THỨC HOOK 3S ĐẦU GIỮ CHÂN NGƯỜI XEM (RETENTION > 65%)

Trong video ngắn (Short-form Video), 3 giây đầu tiên quyết định 80% thành bại của thuật toán phân phối. Dưới đây là 25 công thức được phân loại thành 5 nhóm tâm lý học hành vi, kèm kịch bản mẫu và chỉ dẫn hình ảnh thị giác (Visual Cue).

### NHÓM 1: GÂY TÒ MÒ & LẬT NGƯỢC NIỀM TIN (CURIOSITY & CONTRARIAN)
1. **Công thức:** *"Mọi người đều nghĩ [Quan niệm phổ biến], nhưng sự thật là..."*
   - *Ví dụ:* "Mọi người đều nghĩ làm AI tự động phải biết code Python, nhưng sự thật là ai biết kéo thả chuột cũng làm được."
   - *Visual Cue 3s:* Nhân vật lắc đầu, màn hình chia đôi giữa một bên là màn hình code đen sì phức tạp và một bên là giao diện kéo thả 3 nút cực kỳ đơn giản.
2. **Công thức:** *"Đừng dùng [Công cụ phổ biến] như thế này nữa nếu không muốn [Hậu quả tai hại]..."*
   - *Ví dụ:* "Đừng mở ChatGPT lên rồi xin văn mẫu viết mail nữa, sếp bạn đọc vào biết ngay là văn máy viết đấy!"
   - *Visual Cue 3s:* Cảnh bàn tay bấm nút Xóa đỏ rực trên màn hình, zoom cận vào gương mặt thất vọng khi nhận mail.
3. **Công thức:** *"Bí mật mà các agency quảng cáo không muốn bạn biết về [Chủ đề]..."*
   - *Ví dụ:* "Bí mật mà các bên làm video triệu view giấu nhẹm: Họ không tự ngồi cắt từng giây video đâu."
   - *Visual Cue 3s:* Động tác ghé sát tai thì thầm vào micro, trên màn hình hiện chữ "TOP SECRET" kèm âm thanh rè rè bảo mật.
4. **Công thức:** *"Nếu bạn vẫn còn làm [Việc A] thủ công vào năm 2026, bạn đang lãng phí..."*
   - *Ví dụ:* "Nếu bạn vẫn ngồi đối soát từng dòng hóa đơn Excel vào năm 2026, bạn đang ném tiền qua cửa sổ mỗi ngày."
   - *Visual Cue 3s:* Cảnh một chồng giấy tờ cao ngất bị gạt phăng sang một bên bằng một cú vuốt tay.
5. **Công thức:** *"Tôi đã thử [Cách làm kỳ lạ] trong 7 ngày và đây là điều bất ngờ..."*
   - *Ví dụ:* "Tôi để 3 con AI tự chat với nhau để lên kế hoạch tuần và kết quả khiến tôi sốc..."
   - *Visual Cue 3s:* Cảnh đồng hồ đếm ngược tua nhanh từ Thứ 2 đến Chủ nhật, mắt nhìn vào màn hình trố to ngạc nhiên.

---

### NHÓM 2: ĐÁNH TRÚNG NỖI ĐAU DÂN VĂN PHÒNG & CREATOR (PAIN POINT TRIGGER)
6. **Công thức:** *"Có ai bị tình trạng [Nỗi đau cụ thể] giống mình không?"*
   - *Ví dụ:* "Có ai bị tình trạng ngồi trước màn hình trắng 2 tiếng đồng hồ mà không nghĩ ra nổi một câu mở đầu video không?"
   - *Visual Cue 3s:* Nhân vật vò đầu bứt tai, con trỏ chuột trên màn hình nhấp nháy cô đơn trên trang Word trắng tinh.
7. **Công thức:** *"Cảm giác 6 giờ chiều chuẩn bị tắt máy tính về thì sếp bảo [Yêu cầu gấp]..."*
   - *Ví dụ:* "Cảm giác 17h59 vừa tắt máy thì sếp nhắn: 'Lọc cho anh báo cáo doanh số 12 tháng qua để sáng mai họp'..."
   - *Visual Cue 3s:* Cảnh tay vừa với lấy quai balo thì màn hình điện thoại sáng lên tin nhắn Zalo kèm tiếng "Ting" đặc trưng.
8. **Công thức:** *"Lý do video của bạn mãi dừng lại ở mốc 200 lượt xem..."*
   - *Ví dụ:* "Không phải kênh bạn bị bóp tương tác đâu, lý do video bạn mãi đứng ở 200 view chỉ nằm ở 3 giây đầu tiên này thôi."
   - *Visual Cue 3s:* Chụp màn hình biểu đồ phân tích video rớt thẳng đứng ở giây thứ 2 kèm âm thanh còi báo động.
9. **Công thức:** *"3 việc ngốn thời gian nhất của một Solo Creator và cách tôi xóa bỏ nó..."*
   - *Ví dụ:* "Tìm ý tưởng, gõ phụ đề và sửa lỗi âm thanh. Đây là cách tôi giải quyết cả 3 việc đó trong 10 phút."
   - *Visual Cue 3s:* 3 thanh tiến trình đỏ rực được chuyển thành màu xanh lá cây chỉ sau một cú click chuột.
10. **Công thức:** *"Đừng bỏ việc văn phòng để làm Freelancer nếu bạn chưa có hệ thống này..."*
    - *Ví dụ:* "Nhiều bạn nghĩ làm tự do là tự tại, cho đến khi một mình gánh cả việc bán hàng, chăm sóc khách lẫn làm nội dung."
    - *Visual Cue 3s:* Nhân vật một tay cầm điện thoại gọi khách, một tay gõ phím, mắt nhìn chằm chằm đầy mệt mỏi.

---

### NHÓM 3: CON SỐ & THỜI GIAN CHÍNH XÁC (SPECIFICITY & VELOCITY)
11. **Công thức:** *"Cách tôi rút ngắn [Công việc X] từ [Thời gian dài] xuống còn [Thời gian cực ngắn]..."*
    - *Ví dụ:* "Cách tôi dọn sạch bảng dữ liệu 10.000 dòng từ 4 tiếng xuống đúng 45 giây."
    - *Visual Cue 3s:* Đồng hồ bấm giờ (Stopwatch) điện thoại chạy từ 00:00 và dừng lại ở 00:45.
12. **Công thức:** *"Quy tắc [Con số] giây giúp bạn [Lợi ích mong muốn]..."*
    - *Ví dụ:* "Quy tắc 5 giây kiểm tra kịch bản giúp video không bao giờ bị lướt qua."
    - *Visual Cue 3s:* Bàn tay xòe 5 ngón đếm ngược dần về 1 ngón trước ống kính máy quay.
13. **Công thức:** *"Chỉ với [Số bước/Số công cụ] này, bạn đã giải quyết xong [Vấn đề lớn]..."*
    - *Ví dụ:* "Đúng 2 cú nhấp chuột để chuyển toàn bộ file PDF scan mờ căm thành bảng tính Excel tinh tươm."
    - *Visual Cue 3s:* Cảnh con chuột phóng to click vào 2 nút, màn hình lập tức chuyển từ PDF sang Excel sạch đẹp.
14. **Công thức:** *"Bảng biểu tính toán giúp bạn tiết kiệm [Số tiền/Số giờ] mỗi tuần..."*
    - *Ví dụ:* "Hệ thống quản lý công việc tự động giúp tôi dôi ra 12 tiếng rảnh rỗi mỗi tuần."
    - *Visual Cue 3s:* Nhân vật thảnh thơi nhâm nhi ly cà phê trong khi máy tính đang tự động chạy quy trình ngầm.
15. **Công thức:** *"Top 3 tiện ích AI miễn phí thay thế 5 nhân sự cồng kềnh..."*
    - *Ví dụ:* "3 công cụ AI hoàn toàn miễn phí này sẽ đảm nhận thay bạn từ việc bóc băng ghi âm đến viết biên bản họp."
    - *Visual Cue 3s:* 3 logo công cụ lần lượt xuất hiện dạng pop-up 3D kèm âm thanh pop vui tai.

---

### NHÓM 4: THỊ PHẠM BEFORE/AFTER & CASE STUDY (VISUAL EVIDENCE)
16. **Công thức:** *"Bên trái là [Cách cũ/Kết quả tệ], bên phải là [Cách mới/Kết quả ấn tượng]..."*
    - *Ví dụ:* "Bên trái là bài viết AI viết thông thường, bên phải là bài viết qua mô hình 4 Subagent rà soát. Bạn thấy sự khác biệt chưa?"
    - *Visual Cue 3s:* Chia đôi màn hình (Split screen) với thanh trượt gạt từ trái qua phải để lộ sự khác biệt rõ rệt.
17. **Công thức:** *"Xem điều kỳ diệu xảy ra khi tôi nhấn nút này..."*
    - *Ví dụ:* "Xem điều gì xảy ra khi tôi ném toàn bộ dữ liệu đối thủ vào con bot này và nhấn Enter..."
    - *Visual Cue 3s:* Ngón tay bấm dứt khoát vào phím Enter trên bàn phím cơ, màn hình lập tức nảy ra biểu đồ trực quan.
18. **Công thức:** *"Từ một file nháp lộn xộn biến thành bản thuyết trình chuyên nghiệp trong 1 phút..."*
    - *Ví dụ:* "Tôi chỉ gõ 5 gạch đầu dòng ý tưởng lộn xộn, và đây là những gì AI trả về sau 60 giây."
    - *Visual Cue 3s:* Hiệu ứng chuyển cảnh biến đổi hình thái (Morphing transition) từ file Notepad sang bộ Slide màu sắc hiện đại.
19. **Công thức:** *"Case study thực tế: Cách một bạn thực tập sinh hoàn thành task cả ngày chỉ trong buổi sáng..."*
    - *Ví dụ:* "Cách một bạn kế toán mới ra trường xử lý xong bảng cân đối thử trước giờ ăn trưa nhờ prompt này."
    - *Visual Cue 3s:* Màn hình tin nhắn khen ngợi của Trưởng phòng: "Em làm nhanh và chuẩn xác ngoài mong đợi!"
20. **Công thức:** *"Tôi đã thử nghiệm 50 kịch bản video khác nhau và đây là mẫu duy nhất chạm mốc triệu view..."*
    - *Ví dụ:* "Sau khi test 50 góc tiếp cận khác nhau, đây là cấu trúc mở đầu có tỷ lệ xem hết cao nhất."
    - *Visual Cue 3s:* Xếp chồng 50 kịch bản giấy, rút ra đúng 1 trang được highlight màu vàng nổi bật.

---

### NHÓM 5: KỊCH TÍNH & THỬ THÁCH (DRAMA & CHALLENGE)
21. **Công thức:** *"Tôi tự cá cược với bản thân rằng có thể [Mục tiêu khó] trước khi [Sự kiện kết thúc]..."*
    - *Ví dụ:* "Tôi tự cá với chính mình là có thể dựng xong 5 video ngắn hoàn chỉnh trước khi cốc trà sữa này tan hết đá."
    - *Visual Cue 3s:* Cảnh đặt một ly trà sữa nhiều đá ngay cạnh bàn phím, camera lia nhanh sang màn hình dựng video.
22. **Công thức:** *"Dừng lại 3 giây! Nếu bạn đang làm [Nghề nghiệp], video này dành riêng cho bạn..."*
    - *Ví dụ:* "Dừng lại 3 giây! Nếu bạn đang làm trợ lý, chuyên viên marketing hay nhân sự, đây là vũ khí bí mật của bạn."
    - *Visual Cue 3s:* Bàn tay đưa ra dấu hiệu "STOP" dứt khoát trước ống kính, chữ ngành nghề nhảy nhanh theo nhịp.
23. **Công thức:** *"Sai lầm lớn nhất đời tôi khi bắt đầu [Hành trình/Dự án] là..."*
    - *Ví dụ:* "Sai lầm lớn nhất của tôi khi bắt đầu xây kênh là cố gắng tự làm tất cả mọi thứ một mình."
    - *Visual Cue 3s:* Ánh sáng phòng tối dần, nhân vật ngồi đơn độc trước 3 màn hình sáng rực lúc đêm muộn.
24. **Công thức:** *"Họ nói rằng AI sẽ cướp việc của bạn. Họ nói đúng một nửa, vì..."*
    - *Ví dụ:* "AI không cướp việc của bạn. Người biết dùng AI một cách có hệ thống mới là người lấy đi công việc đó."
    - *Visual Cue 3s:* Đồ họa chữ tương phản mạnh "AI vs YOU", sau đó đổi thành "YOU + AI = UNSTOPPABLE".
25. **Công thức:** *"Tôi cá là bạn chưa từng thấy ai giải quyết bài toán [Tên bài toán] theo cách này..."*
    - *Ví dụ:* "Tôi cá là bạn chưa từng thấy ai làm nghiên cứu thị trường 100 trang chỉ bằng một sơ đồ tư duy tương tác như thế này."
    - *Visual Cue 3s:* Bàn tay thu phóng (zoom in/out) mượt mà trên một bản đồ sơ đồ tư duy vô cực đa sắc màu.

---

# PHẦN 3: 25 SIÊU PROMPT TỰ ĐỘNG HÓA VĂN PHÒNG & NGHIÊN CỨU THỊ TRƯỜNG

Mỗi prompt dưới đây được thiết kế theo cấu trúc chuyên sâu: **Context (Bối cảnh) + Input Data Format (Dữ liệu đầu vào) + Constraints (Ràng buộc logic) + Expected Output Schema (Định dạng đầu ra)**. Bạn chỉ cần sao chép, điền thông tin trong ngoặc vuông `[...]` và nhấn gửi.

---

### MODULE 1: EXCEL / GOOGLE SHEETS & SQL TỰ ĐỘNG (5 PROMPTS)

#### Prompt 01: Viết công thức Excel lồng ghép phức tạp kèm giải thích logic
```text
Bối cảnh: Tôi đang xử lý một bảng tính dữ liệu trong [Excel 365 / Google Sheets].
Cấu trúc bảng tính hiện tại:
- Cột A: Mã đơn hàng [Ví dụ: ORD-1029]
- Cột B: Ngày phát sinh giao dịch [Định dạng: DD/MM/YYYY]
- Cột C: Doanh thu thô [Số tiền VND]
- Cột D: Trạng thái thanh toán [Hoàn tất, Đang chờ, Hủy]
- Cột E: Kênh bán hàng [Shopee, TikTok Shop, Trực tiếp]

Yêu cầu:
1. Hãy viết 01 công thức duy nhất (ưu tiên dùng hàm hiện đại như XLOOKUP, FILTER, LET hoặc SUMIFS lồng ghép) để: [Mô tả mục tiêu, ví dụ: Tính tổng doanh thu của kênh Shopee có trạng thái Hoàn tất trong Quý 3 năm 2026].
2. Nếu xảy ra trường hợp ô trống hoặc lỗi, hãy bọc hàm IFERROR để trả về giá trị 0.
3. Giải thích từng thành phần của công thức theo định dạng gạch đầu dòng rõ ràng để tôi hiểu bản chất.
```

#### Prompt 02: Dọn dẹp và chuẩn hóa dữ liệu văn bản hỗn tạp (Data Cleaning)
```text
Bối cảnh: Tôi vừa xuất một danh sách dữ liệu khách hàng từ hệ thống cũ nhưng định dạng rất lộn xộn.
Dữ liệu mẫu đầu vào:
"""
[Dán 5-10 dòng dữ liệu mẫu của bạn vào đây, ví dụ: "   nguyen van a - 0912345678  - Ha Noi ", "TRAN THI B, sđt: 0987.654.321, TP HCM"]
"""

Yêu cầu:
1. Phân tích các quy luật bất thường trong chuỗi dữ liệu trên (khoảng trắng thừa, dấu chấm/dấu phẩy, viết hoa thường lộn xộn, đầu số điện thoại không đồng nhất).
2. Viết công thức Google Sheets/Excel (hoặc regex / script Python ngắn) để tách thành 3 cột chuẩn hóa:
   - Cột 1: Họ và tên (Viết hoa chữ cái đầu từng từ, bỏ khoảng trắng thừa).
   - Cột 2: Số điện thoại (Chỉ giữ lại chữ số, bắt đầu bằng tiền tố chuẩn 09/03/07/08/05, không có dấu chấm/cách).
   - Cột 3: Tỉnh/Thành phố (Tên chuẩn hóa hành chính).
3. Đưa ra bảng kết quả trước và sau khi làm sạch để tôi đối chiếu.
```

#### Prompt 03: Viết Google Apps Script / VBA Macro tự động phân tách dữ liệu thành từng Sheet
```text
Bối cảnh: Tôi cần tự động hóa bảng tính hàng tuần trong [Google Sheets / Excel VBA].
Mục tiêu: Tôi có một trang tính tổng hợp tên là "Master_Data". Tôi muốn tự động tạo ra các trang tính con riêng biệt dựa trên giá trị duy nhất tại Cột [Tên cột, ví dụ: Cột Chi Nhánh hoặc Kênh Bán Hàng]. Toàn bộ dòng dữ liệu tương ứng của chi nhánh đó sẽ được sao chép sang trang tính con mang tên chi nhánh đó.

Ràng buộc kỹ thuật:
1. Nếu trang tính con đã tồn tại từ trước, hãy xóa dữ liệu cũ của trang đó và ghi đè dữ liệu mới nhất (giữ nguyên hàng tiêu đề Header).
2. Tự động căn chỉnh độ rộng cột (Auto-fit column width) cho đẹp mắt.
3. Thêm chú thích chi tiết bằng tiếng Việt vào từng dòng lệnh để tôi có thể tự sửa tên Sheet hoặc vị trí cột khi cấu trúc thay đổi.
```

#### Prompt 04: Viết truy vấn SQL phân tích tỷ lệ giữ chân khách hàng (Cohort Retention Analysis)
```text
Bối cảnh: Tôi có cơ sở dữ liệu PostgreSQL / MySQL chứa bảng lịch sử đơn hàng tên là `orders`.
Cấu trúc bảng:
- `order_id` (VARCHAR): Khóa chính
- `customer_id` (VARCHAR): Mã định danh khách hàng
- `order_date` (TIMESTAMP): Ngày giờ mua hàng
- `total_amount` (DECIMAL): Giá trị đơn hàng

Yêu cầu:
1. Hãy viết một truy vấn SQL chuẩn (dùng Common Table Expressions - CTE) để thực hiện phân tích Cohort Retention theo tháng.
2. Tháng đầu tiên khách hàng phát sinh đơn hàng sẽ là Cohort Month (Tháng gốc).
3. Tính toán tỷ lệ phần trăm khách hàng quay lại mua hàng ở Tháng thứ 1, Tháng thứ 2, Tháng thứ 3... sau lần mua đầu tiên.
4. Kết quả trả về dạng bảng xoay chiều (Pivot) với các cột: Cohort_Month, Total_New_Customers, Month_0, Month_1, Month_2, Month_3...
5. Tối ưu câu lệnh để không bị nghẽn bộ nhớ khi bảng có trên 1 triệu dòng.
```

#### Prompt 05: Chẩn đoán và sửa lỗi công thức Excel bị treo hoặc báo lỗi #N/A, #VALUE!
```text
Bối cảnh: Tôi đang dùng công thức sau nhưng bảng tính báo lỗi [Điền lỗi: ví dụ #VALUE!, #N/A, #SPILL! hoặc bảng tính bị đơ, giật lag]:
Công thức hiện tại: `[Dán công thức bị lỗi của bạn vào đây]`
Mô tả dữ liệu ở các ô liên quan:
- Vùng tra cứu: [Ví dụ: Bảng A2:F50000, trong đó cột A chứa mã số dạng text còn ô cần dò lại là dạng number]
- Kết quả mong muốn: [Mô tả kết quả bạn muốn nhận được]

Hãy đóng vai trò chuyên gia Excel:
1. Chỉ ra chính xác nguyên nhân gốc rễ gây ra lỗi trên.
2. Viết lại công thức sửa lỗi triệt để, tối ưu tốc độ tính toán (tránh các hàm volatile gây chậm như INDIRECT hay OFFSET nếu không cần thiết).
3. Đưa ra mẹo phòng ngừa lỗi tương tự khi người dùng khác nhập liệu vào bảng.
```

---

### MODULE 2: BÁO CÁO B2B & TRÌNH BÀY QUẢN TRỊ (5 PROMPTS)

#### Prompt 06: Chuyển đổi dữ liệu số liệu thô thành Executive Summary cho Ban Giám Đốc
```text
Bối cảnh: Tôi là trưởng nhóm kinh doanh, cần làm báo cáo nhanh gửi Ban Giám Đốc về tình hình tuần vừa qua.
Dữ liệu thô và sự kiện tuần:
"""
[Dán các số liệu rời rạc, gạch đầu dòng, kết quả đạt được, sự cố phát sinh trong tuần vào đây]
"""

Yêu cầu bạn đóng vai trò Cố vấn Chiến lược Quản trị:
Soạn một bản tóm tắt điều hành (Executive Summary) giới hạn trong đúng 01 trang A4 (dưới 400 từ), cấu trúc chặt chẽ gồm:
1. Điểm sáng nổi bật (Wins & Milestones): 2-3 chỉ số định lượng then chốt vượt kỳ vọng.
2. Điểm nghẽn & Rủi ro (Bottlenecks & Alerts): Nêu rõ vấn đề, nguyên nhân cốt lõi và mức độ ảnh hưởng tài chính/tiến độ.
3. Kế hoạch hành động tuần tới (Action Items): 3 ưu tiên lớn nhất kèm người chịu trách nhiệm và deadline cụ thể.
Văn phong: Gãy gọn, chuyên nghiệp, tập trung vào ROI và hiệu quả kinh doanh, tuyệt đối không kể lể sự việc dài dòng.
```

#### Prompt 07: Soạn dàn bài Slide thuyết trình theo nguyên lý Kim Tự Tháp Minto (McKinsey Format)
```text
Chủ đề thuyết trình: [Ví dụ: Đề xuất chuyển đổi số quy trình chăm sóc khách hàng bằng AI Agent]
Đối tượng người nghe: [Ví dụ: Hội đồng Quản trị và các Giám đốc Khối nghiệp vụ]
Thời lượng thuyết trình: [Ví dụ: 15 phút trình bày + 10 phút hỏi đáp]
Mục tiêu bài nói: Khiến Hội đồng Quản trị phê duyệt gói ngân sách thử nghiệm trị giá [Số tiền] trong Quý 4.

Hãy thiết kế cấu trúc bài thuyết trình 10 Slide theo Nguyên lý Kim Tự Tháp Minto (Minto Pyramid Principle):
- Đưa kết luận / Thông điệp tối thượng lên ngay Slide đầu tiên.
- Với mỗi Slide từ 1 đến 10, hãy cung cấp:
  + Tiêu đề hành động (Action Title - phải là một câu hoàn chỉnh thể hiện luận điểm, không đặt tiêu đề danh từ chung chung).
  + Bố cục trực quan gợi ý (Layout: 3 cột, bảng so sánh đối đầu, phễu chuyển đổi, biểu đồ thác nước...).
  + Nội dung dữ liệu chính (3 gạch đầu dòng súc tích).
  + Câu hỏi phản biện dự kiến từ người nghe và cách trả lời dứt khoát.
```

#### Prompt 08: Phân tích SWOT định lượng và lập Ma trận chiến lược TOWS
```text
Bối cảnh doanh nghiệp / dự án:
- Lĩnh vực: [Ví dụ: Dịch vụ đào tạo và tư vấn tự động hóa AI cho doanh nghiệp SME]
- Quy mô: [Ví dụ: Đội ngũ 10 người, doanh thu 500tr/tháng, tệp khách hàng 200 doanh nghiệp]
- Các thông tin quan sát được: [Liệt kê các điểm mạnh, điểm yếu nội bộ, cơ hội và thách thức bên ngoài mà bạn ghi nhận]

Hãy giúp tôi thực hiện:
1. Bảng SWOT Định Lượng: Không chỉ liệt kê chữ, hãy cho điểm trọng số (từ 1 đến 5) và mức độ ảnh hưởng của từng yếu tố.
2. Ma trận chiến lược TOWS (Kết hợp chéo để ra hành động):
   - Chiến lược SO (Dùng Điểm Mạnh để đón đầu Cơ Hội).
   - Chiến lược ST (Dùng Điểm Mạnh để phòng thủ Thách Thức).
   - Chiến lược WO (Khắc phục Điểm Yếu bằng cách nắm bắt Cơ Hội).
   - Chiến lược WT (Kế hoạch sinh tồn: Giảm thiểu Điểm Yếu và né tránh Thách Thức).
3. Đề xuất 01 sáng kiến đột phá có thể triển khai ngay trong 30 ngày tới với chi phí thấp nhất.
```

#### Prompt 09: Viết Đề xuất Dự án Kinh doanh (Business Proposal) chào gói thầu B2B
```text
Khách hàng mục tiêu: [Tên công ty khách hàng / Ngành nghề / Quy mô]
Nỗi đau lớn nhất khách hàng đang gặp phải: [Mô tả vấn đề khách hàng cần giải quyết, ví dụ: Chi phí nhân sự trực chat quá cao nhưng tỷ lệ rớt đơn ban đêm lên tới 40%]
Giải pháp chúng tôi cung cấp: [Mô tả giải pháp / dịch vụ của bạn]
Ngân sách dự kiến: [Khoảng giá hoặc hình thức tính phí]

Hãy soạn thảo một bản Đề xuất Dự án B2B hoàn chỉnh, thuyết phục và mang tính thực thi cao:
1. Bối cảnh & Thấu hiểu vấn đề (Chứng minh chúng tôi hiểu sâu sắc bài toán của họ hơn đối thủ).
2. Phạm vi công việc (Scope of Work - SOW): Chia thành 3 giai đoạn rõ ràng kèm deliverables cụ thể.
3. Lộ trình triển khai (Timeline & Milestones): Cam kết theo từng tuần.
4. Dự toán đầu tư & Phân tích ROI: Chỉ ra khách hàng sẽ tiết kiệm được bao nhiêu tiền hoặc tăng bao nhiêu doanh thu sau 3 tháng.
5. Điều khoản nghiệm thu và Cam kết dịch vụ (SLA) minh bạch.
```

#### Prompt 10: Chuẩn hóa Biên bản Cuộc họp giao việc theo chuẩn SMART & RACI
```text
Bối cảnh: Dưới đây là nội dung ghi chép nhanh trong buổi họp giao ban sáng nay:
"""
[Dán đoạn ghi chú cuộc họp lộn xộn, ai nói gì, công việc cần làm vào đây]
"""

Hãy đóng vai trò Thư ký Điều hành:
Biến đoạn ghi chép trên thành Biên bản Họp Giao Việc chuyên nghiệp:
1. Thông tin chung: Thời gian, Thành phần tham dự, Mục tiêu cuộc họp.
2. Các quyết định đã được thống nhất (Decisions Made).
3. Bảng phân công nhiệm vụ chi tiết theo ma trận RACI và chuẩn SMART:
   - Cột 1: Hạng mục công việc (Rõ ràng hành động cụ thể, bắt đầu bằng động từ).
   - Cột 2: Người chịu trách nhiệm chính (Responsible - R).
   - Cột 3: Người phê duyệt cuối cùng (Accountable - A).
   - Cột 4: Kết quả bàn giao cụ thể (Deliverable đo lường được).
   - Cột 5: Hạn chót hoàn thành (Deadline chính xác ngày giờ).
```

---

### MODULE 3: TÓM TẮT & TỐI ƯU GIAO TIẾP HỌP HÀNH (5 PROMPTS)

#### Prompt 11: Tóm tắt Transcript cuộc họp Zoom/Teams bóc tách ý kiến đa chiều
```text
Dưới đây là bản gỡ băng lời thoại (Transcript) của cuộc họp kéo dài [Số phút]:
"""
[Dán nội dung transcript thô vào đây]
"""

Hãy phân tích và xuất bản báo cáo tóm tắt cuộc họp gồm 4 phần:
1. Tóm tắt 3 phút: Toàn bộ tinh thần và kết quả cuộc họp trong đúng 5 câu văn ngắn gọn.
2. Bản đồ quan điểm người tham gia: Từng người tham gia (Người A, Người B...) đã bày tỏ lập trường gì? Họ đồng thuận hay phản đối điều gì?
3. Các vấn đề chưa ngã ngũ (Open Issues / Unresolved Conflicts): Những bất đồng nào còn tồn đọng cần bàn thêm trong buổi sau?
4. Danh sách việc cần làm ngay (Action Items): Tên người - Việc cần làm - Thời hạn.
```

#### Prompt 12: Soạn Email ngoại giao giải quyết xung đột tiến độ dự án
```text
Tình huống: Tôi là quản lý dự án. Đối tác / Phòng ban liên quan [Tên đối tác hoặc phòng ban] đã chậm trễ bàn giao hạng mục [Tên hạng mục] quá [Số ngày] ngày, làm ảnh hưởng nghiêm trọng đến tiến độ chung của toàn công ty. Tôi cần gửi email nhắc nhở cứng rắn nhưng vẫn giữ được quan hệ ngoại giao chuyên nghiệp, không gây thù hằn cá nhân.

Yêu cầu soạn thảo Email:
- Tiêu đề: Khẩn cấp nhưng lịch sự, nêu rõ mã dự án.
- Phần mở đầu: Ghi nhận sự nỗ lực và hợp tác của họ trong thời gian qua.
- Phần thân: Nêu rõ sự thật về việc trễ hạn (ngày cam kết ban đầu vs ngày hiện tại), chỉ ra hệ quả dây chuyền định lượng được.
- Đề xuất giải pháp tháo gỡ: Đưa ra 2 phương án hỗ trợ cụ thể để họ hoàn thành dứt điểm.
- Hạn chót cuối cùng (Hard Deadline) và bước leo thang tiếp theo nếu không nhận được phản hồi trước [Giờ, Ngày].
```

#### Prompt 13: Soạn Cold Email B2B tiếp cận khách hàng VIP với tỷ lệ phản hồi cao
```text
Khách hàng tôi muốn tiếp cận: [Chức danh: Giám đốc Marketing / CEO / Giám đốc Vận hành] tại các công ty [Ngành nghề].
Giá trị chúng tôi mang lại: [Ví dụ: Giúp cắt giảm 30% chi phí sản xuất video marketing nhờ quy trình AI đóng gói].
Tài liệu / Quà tặng mở đầu (Lead Magnet): [Ví dụ: Báo cáo phân tích đối thủ cạnh tranh miễn phí dành riêng cho thương hiệu của họ].

Hãy viết 01 bức Cold Email theo nguyên tắc "No-BS, Value-First" (Không sáo rỗng, Giá trị đi đầu):
- Độ dài: Dưới 120 từ.
- Tiêu đề (Subject Line): Dưới 7 từ, gây tò mò tự nhiên, giống một email từ đối tác quen thuộc, không giống thư rác quảng cáo.
- Câu mở đầu: Đề cập trực tiếp đến một thành tựu hoặc chuyển động gần đây của công ty họ (Personalization).
- Đưa ra một insight giá trị và đề xuất gửi tặng tài liệu phân tích.
- Lời kêu gọi hành động (Call to Action): Cực kỳ nhẹ nhàng (Low friction), ví dụ: "Nếu anh/chị quan tâm, em xin phép gửi file PDF qua đây để anh/chị xem thử trong 2 phút nhé?".
```

#### Prompt 14: Kịch bản tin nhắn Follow-up khách hàng sau khi gửi báo giá
```text
Bối cảnh: Tôi đã gửi báo giá dịch vụ cho khách hàng cách đây [3 ngày / 5 ngày / 1 tuần] nhưng khách hàng đã xem tin nhắn/email mà chưa phản hồi lại.
Sản phẩm/Dịch vụ: [Tên dịch vụ, giá tiền].

Hãy soạn cho tôi 3 biến thể tin nhắn Follow-up qua Zalo / Email theo 3 cấp độ:
- Cấp độ 1 (Sau 3 ngày): Nhắc nhở tinh tế, cung cấp thêm 1 case study thành công tương tự trường hợp của khách hàng để gia tăng niềm tin.
- Cấp độ 2 (Sau 7 ngày): Đặt câu hỏi khai thác băn khoăn (Liệu ngân sách hay phạm vi công việc đang là điểm khiến khách hàng chần chừ?).
- Cấp độ 3 (Sau 14 ngày - Break-up Email): Tuyên bố lịch sự rằng tôi sẽ đóng hồ sơ tư vấn này lại để không làm phiền khách hàng, trừ khi họ chủ động muốn kích hoạt lại. (Chiêu tâm lý học lật ngược tình thế).
```

#### Prompt 15: Phản hồi phàn nàn của khách hàng (De-escalating Customer Complaint)
```text
Tình huống sự cố: Khách hàng mua sản phẩm/dịch vụ của tôi và gặp phải lỗi [Mô tả chi tiết lỗi, ví dụ: Đơn giao chậm 3 ngày, hàng bị móp méo, hoặc bot AI trả lời sai thông tin]. Khách hàng đang rất tức giận, nhắn tin dọa bóc phốt lên mạng xã hội.

Hãy đóng vai trò Chuyên gia Quản trị Trải nghiệm Khách hàng (Head of CX):
Soạn thảo kịch bản phản hồi trực tiếp cho khách hàng theo nguyên lý L.A.S.T (Listen - Apologize - Solve - Thank):
1. Lắng nghe và Thấu cảm (Xác nhận cảm xúc thất vọng của khách mà không đổ lỗi cho hoàn cảnh).
2. Lời xin lỗi chân thành đại diện cho thương hiệu.
3. Phương án xử lý dứt điểm ngay lập tức (Bồi hoàn, đổi mới, hoặc tặng voucher đền bù).
4. Biện pháp cải tiến quy trình để không bao giờ tái phạm.
Văn phong: Điềm tĩnh, chân thành, tôn trọng khách hàng tuyệt đối, biến khách hàng đang giận dữ thành người ủng hộ trung thành.
```

---

### MODULE 4: PHÂN TÍCH ĐỐI THỦ & BÓC TÁCH INSIGHT (5 PROMPTS)

#### Prompt 16: Lập Ma trận giải phẫu đối thủ cạnh tranh toàn diện
```text
Ngành hàng: [Ví dụ: Thời trang nam công sở / Đồ gia dụng thông minh / Khóa học kỹ năng AI]
Danh sách 3 đối thủ lớn nhất trên thị trường:
- Đối thủ 1: [Tên thương hiệu, Fanpage/Website nếu có]
- Đối thủ 2: [Tên thương hiệu]
- Đối thủ 3: [Tên thương hiệu]

Hãy lập một bảng ma trận so sánh chi tiết gồm các tiêu chí:
1. Định vị thương hiệu & Khẩu hiệu cốt lõi.
2. Khách hàng mục tiêu trọng tâm (Độ tuổi, thu nhập, hành vi).
3. Cấu trúc bảng giá & Phân khúc (Bình dân, Trung cấp, Cao cấp).
4. Kênh truyền thông chủ lực (TikTok, Facebook, Google Search hay Hội thảo).
5. Chiến lược nội dung (Tập trung vào giải trí, review công năng hay đánh vào nỗi sợ hãi?).
6. Điểm yếu chí mạng của từng đối thủ mà chúng tôi có thể khai thác để chiếm thị phần.
```

#### Prompt 17: Đào sâu bình luận (Comment Mining) bóc tách nỗi đau khách hàng
```text
Dưới đây là 30-50 bình luận thật được sao chép từ bài quảng cáo / video đánh giá sản phẩm của đối thủ:
"""
[Dán danh sách bình luận vào đây]
"""

Hãy đóng vai trò Nhà Nghiên Cứu Tâm Lý Học Tiêu Dùng:
Bóc tách toàn bộ dữ liệu trên thành:
1. Từ điển ngôn ngữ khách hàng (Customer Lexicon): Khách hàng thường dùng những từ ngữ đời thường nào để diễn tả nỗi bức xúc của họ? (Trích dẫn nguyên văn câu nói).
2. Top 3 rào cản tâm lý khiến họ chưa dám mua hàng (Objections).
3. Yếu tố "Khao khát ngầm hiểu" (Unmet Desires): Họ thực sự mong muốn đạt được cảm xúc gì sau khi mua sản phẩm này?
4. Đề xuất 3 góc tiếp cận nội dung (Content Angles) đánh thẳng vào những nỗi đau được nhắc lại nhiều nhất trong dữ liệu trên.
```

#### Prompt 18: Giải phẫu Ưu đãi (Offer Teardown) và định giá sản phẩm đối đầu
```text
Dưới đây là chi tiết gói sản phẩm / dịch vụ mà đối thủ đang bán rất chạy:
- Giá niêm yết: [Giá tiền]
- Quà tặng kèm: [Danh sách quà tặng]
- Chính sách cam kết / Bảo hành: [Mô tả]
- Chi phí vận chuyển: [Mô tả]

Hãy giúp tôi giải phẫu gói ưu đãi này:
1. Tính toán "Giá trị cảm nhận" (Perceived Value) so với chi phí thực tế đối thủ phải bỏ ra.
2. Điểm kích hoạt tâm lý mạnh nhất trong gói ưu đãi của họ là gì (Sự khan hiếm, giảm giá ảo hay quà tặng độc quyền)?
3. Thiết kế một "Grand Slam Offer" (Ưu đãi không thể chối từ - theo phong cách Alex Hormozi) để chúng tôi cạnh tranh trực tiếp: Làm sao để cùng mức giá hoặc giá cao hơn nhưng khách hàng vẫn cảm thấy sản phẩm của chúng tôi hời gấp 10 lần?
```

#### Prompt 19: Phân tích phễu chuyển đổi E-commerce và tìm điểm rò rỉ dòng tiền
```text
Số liệu hiệu quả phễu bán hàng tháng qua của gian hàng:
- Lượt xem sản phẩm (Product Views): [Số lượt, ví dụ: 100.000]
- Lượt bấm Thêm vào giỏ hàng (Add to Cart): [Số lượt, ví dụ: 5.000]
- Lượt bấm Bắt đầu thanh toán (Initiate Checkout): [Số lượt, ví dụ: 2.000]
- Lượt hoàn tất đơn hàng thành công (Purchases): [Số lượt, ví dụ: 500]
- Tỷ lệ hủy/hoàn đơn (Return Rate): [Ví dụ: 8%]

Hãy phân tích sức khỏe của phễu:
1. Tính tỷ lệ chuyển đổi qua từng bước (Micro-conversion rates) và so sánh với mức chuẩn trung bình của ngành thương mại điện tử.
2. Chỉ ra bước nào đang là "Điểm rò rỉ dòng tiền" lớn nhất (Bước có tỷ lệ rơi rụng cao bất thường).
3. Đưa ra danh sách 5 giả thuyết nguyên nhân gây rơi rụng tại bước đó (UX/UI, phí ship bất ngờ, thiếu phương thức thanh toán, thiếu chứng nhận uy tín...).
4. Đề xuất 2 bài test A/B cụ thể để cải thiện tỷ lệ chuyển đổi tại điểm nghẽn đó ngay trong tuần này.
```

#### Prompt 20: Lập bản đồ định vị khoảng trống thị trường (Perceptual Mapping)
```text
Ngành hàng: [Tên ngành hàng]
Các đối thủ hiện hữu trên thị trường: [Liệt kê 4-6 đối thủ chính]

Yêu cầu:
1. Hãy đề xuất 2 trục tọa độ (X và Y) thể hiện 2 thuộc tính đối nghịch quan trọng nhất tác động đến quyết định mua hàng của người tiêu dùng trong ngành này (Ví dụ: Trục X: Tiện lợi - Chuyên sâu; Trục Y: Giá bình dân - Giá cao cấp).
2. Định vị vị trí hiện tại của các đối thủ trên 4 góc phần tư của bản đồ.
3. Chỉ ra "Khoảng trống đại dương xanh" (White Space) - góc phần tư nào đang có nhu cầu lớn nhưng chưa có đối thủ nào chiếm lĩnh hoặc phục vụ chưa tới nơi tới chốn.
4. Đề xuất concept định vị cho thương hiệu mới của chúng tôi để chiếm trọn khoảng trống đó.
```

---

### MODULE 5: LẬP LỊCH & QUẢN TRỊ NỘI DUNG ĐA KÊNH (5 PROMPTS)

#### Prompt 21: Xây dựng Ma trận Nội dung 30 ngày theo mô hình Hub - Hero - Help
```text
Thương hiệu / Chủ đề kênh: [Ví dụ: Tự động hóa công việc văn phòng bằng AI và công cụ số]
Khách hàng mục tiêu: [Dân văn phòng, Quản lý cấp trung, Chủ shop kinh doanh online]
Tần suất đăng bài: [Ví dụ: 1 bài/ngày liên tục trong 30 ngày]

Hãy thiết kế Ma trận Nội dung 30 ngày chia đều theo 3 trụ cột:
1. Trụ cột HELP (60% - Giáo dục, giải quyết nỗi đau cụ thể, hướng dẫn từng bước để kéo traffic tìm kiếm).
2. Trụ cột HUB (30% - Góc nhìn chuyên gia, tranh luận lật ngược vấn đề, câu chuyện thương hiệu để giữ chân fan trung thành).
3. Trụ cột HERO (10% - Các bài đột phá, mini-game, phát tài liệu miễn phí giá trị cao để hút tệp người mới vào phễu).

Kết quả trả về dạng bảng gồm các cột:
- Ngày (Từ Ngày 1 đến Ngày 30)
- Trụ cột nội dung (Help/Hub/Hero)
- Định dạng (Video ngắn Reels/Shorts, Bài viết hình ảnh Carousel, hay Bài Text thảo luận)
- Tiêu đề / Hook 3s gợi ý
- Mục tiêu chuyển đổi của bài (Nhận tài liệu, Thảo luận hay Lưu bài viết)
```

#### Prompt 22: Tái chế 1 nội dung dài (Long-form) thành 10 tài nguyên nội dung ngắn đa kênh
```text
Dưới đây là một bài viết dài / bản ghi âm chia sẻ kiến thức chuyên sâu của tôi:
"""
[Dán nội dung bài viết dài hoặc ghi chép kiến thức vào đây]
"""

Hãy bóc tách và tái chế nội dung này thành 10 tài sản nội dung đa kênh độc lập:
- 03 Kịch bản Video ngắn 30s (TikTok/Reels/Shorts) kèm Hook 3s thị giác.
- 02 Bài đăng Facebook Page dạng chia sẻ giá trị thực tiễn (kèm câu hỏi gợi mở thảo luận ở cuối).
- 03 Bài đăng Threads ngắn gọn, mang phong cách nhật ký / bài học trải nghiệm cá nhân sâu sắc.
- 01 Infographic Concept (Mô tả bố cục thiết kế ảnh để giao cho designer hoặc AI vẽ).
- 01 Email Newsletter gửi danh sách khách hàng thân thiết.
Mỗi nội dung phải mang sắc thái tự nhiên của nền tảng đó, tuyệt đối không copy-paste nguyên văn.
```

#### Prompt 23: Viết kịch bản Video Review Sản phẩm 30s theo công thức PAS + Demo
```text
Sản phẩm review: [Tên sản phẩm, tính năng cốt lõi]
Giá bán tham khảo: [Giá tiền]
Khách hàng phù hợp nhất: [Đối tượng nên mua]
Giới hạn / Nhược điểm trung thực: [Điểm sản phẩm chưa hoàn hảo, ví dụ: Hơi to, không chống nước, cần cắm điện trực tiếp]

Hãy viết kịch bản video ngắn 30 giây (dưới 80 từ lời thoại) theo cấu trúc chuẩn:
- Giây 00-03 (Hook): Đánh trúng nỗi đau hoặc hình ảnh Before/After bắt mắt.
- Giây 03-10 (Pain): Mô tả sự phiền toái nếu không có sản phẩm.
- Giây 10-22 (Solution & Demo): Thị phạm trực quan cách sản phẩm giải quyết vấn đề trong thực tế.
- Giây 22-26 (Honest Note): Nêu một giới hạn trung thực để tăng uy tín tuyệt đối (Người tiêu dùng rất ghét khen 100%).
- Giây 26-30 (CTA): Lời kêu gọi xem thêm thông tin hoặc kiểm tra giá ưu đãi hiện tại ở bình luận ghim.
Kèm bảng phân cảnh 2 cột: Cột 1 là Lời thoại (Voiceover), Cột 2 là Hành động thị giác (Visual Action).
```

#### Prompt 24: Viết Caption Facebook Page chuẩn AIDA kèm Pinned Comment dẫn phễu
```text
Chủ đề bài đăng: [Tên chủ đề / Tài liệu chia sẻ / Góc nhìn]
Đối tượng độc giả: [Người theo dõi Page AI Players]
Mục tiêu bài viết: Thu hút người dùng bình luận từ khóa để nhận tài liệu trong Nhóm Zalo Cộng Đồng.

Hãy soạn bài đăng Facebook Page tuân thủ quy chuẩn nghiêm ngặt:
1. Dòng Hook: Tối đa 2 dòng, gây tò mò cực độ trên màn hình điện thoại trước nút "Xem thêm" (See More).
2. Thân bài (Body): Chia thành các đoạn ngắn 1-2 câu, dùng icon tinh tế, dễ quét mắt.
3. Cuối bài: Đặt 01 câu hỏi khảo sát ý kiến A/B kích thích tranh luận dưới bình luận. Tuyệt đối KHÔNG chèn link ngoài vào caption để tránh bị bóp hiển thị.
4. Pinned Comment #1 (Bình luận ghim đầu tiên): Soạn sẵn nội dung bình luận ghim chứa đường dẫn tham gia nhóm Zalo và hướng dẫn lấy tài liệu.
```

#### Prompt 25: Checklist kiểm toán SEO On-page và tối ưu Intent tìm kiếm cho bài viết
```text
Từ khóa chính (Primary Keyword): [Ví dụ: Tự động hóa văn phòng bằng AI]
Danh sách từ khóa phụ (LSI Keywords): [Ví dụ: Công cụ AI văn phòng, tối ưu năng suất, quy trình n8n, subagent là gì]
Bản nháp bài viết của tôi:
"""
[Dán bản nháp bài viết vào đây]
"""

Hãy đóng vai trò Chuyên gia SEO Content Master:
Thực hiện kiểm toán và đề xuất chỉnh sửa:
1. Đánh giá Search Intent (Ý định tìm kiếm): Bài viết đã trả lời đúng nhu cầu Thông tin (Informational) hay Giao dịch (Transactional) của người dùng chưa?
2. Tối ưu Thẻ Tiêu đề (Title Tag) và Thẻ Mô tả (Meta Description) chứa từ khóa chính, hấp dẫn người tìm kiếm click vào.
3. Tối ưu cấu trúc tiêu đề H1, H2, H3: Chỉ ra vị trí cần chèn từ khóa phụ một cách tự nhiên nhất.
4. Đánh giá tính dễ đọc (Readability): Đoạn nào quá dài cần bẻ nhỏ? Câu nào lủng củng cần viết lại?
5. Đề xuất 3 liên kết nội bộ (Internal Links) và 1 liên kết ngoài uy tín (External Link) nên bổ sung.
```

---

# PHẦN 4: HƯỚNG DẪN KẾT NỐI NHÓM ZALO CỘNG ĐỒNG VIP "AI PLAYERS — THỰC CHIẾN SUBAGENT"

Chào mừng bạn đã bước chân vào thế giới của những người làm chủ AI có hệ thống. Tài liệu này chỉ là bước khởi đầu. Những kịch bản tự động hóa nâng cao, các template workflow n8n được cập nhật hàng tuần, và các buổi giao lưu thực chiến sẽ diễn ra độc quyền bên trong nhóm cộng đồng.

### THÔNG TIN GIA NHẬP NHÓM
- **Đường link tham gia:** [https://zalo.me/g/fzxvbf259](https://zalo.me/g/fzxvbf259)
- **Mã duyệt bắt buộc:** `AIPLAYERS2026` *(Lưu ý: Bạn bắt buộc phải điền chính xác mã này trong ô câu hỏi khi bấm xin vào nhóm để Bot tự động duyệt thành viên).*

---

### QUY TRÌNH 3 BƯỚC ĐỂ BẮT ĐẦU:
1. **Bước 1 — Bấm vào link:** Nhấp vào đường dẫn [https://zalo.me/g/fzxvbf259](https://zalo.me/g/fzxvbf259) trên điện thoại hoặc máy tính.
2. **Bước 2 — Điền mã xác nhận:** Khi ô cửa sổ hiện lên *"Nhập mã mời hoặc lý do tham gia"*, bạn gõ đúng cụm từ: `AIPLAYERS2026`.
3. **Bước 3 — Ghim tin nhắn đầu nhóm:** Ngay sau khi được duyệt, hãy vào mục **Tin Nhắn Đã Ghim** ở đầu nhóm để tải về:
   - File JSON chứa 10 Workflow n8n tự động hóa mẫu.
   - Kho lưu trữ tài liệu cập nhật của các số Lead Magnet tiếp theo (LM-02, LM-03...).
   - Lịch giải đáp Q&A kỹ thuật hàng tuần từ đội ngũ Admin.

### NỘI QUY SINH HOẠT VĂN MINH:
- **Nguyên tắc 1:** Chia sẻ kiến thức và trải nghiệm thực tế. Tôn trọng mọi câu hỏi từ cơ bản đến nâng cao của các thành viên mới.
- **Nguyên tắc 2:** Nghiêm cấm mọi hành vi spam link quảng cáo cờ bạc, tài chính đen, kéo mem bán khóa học rác. Vi phạm sẽ bị xóa khỏi nhóm vĩnh viễn không cần báo trước.
- **Nguyên tắc 3:** Khi gặp khó khăn trong việc chạy prompt hoặc lỗi cấu hình Subagent, hãy chụp ảnh màn hình và đặt câu hỏi rõ ràng để cộng đồng hỗ trợ giải quyết nhanh nhất.

---
*Chúc bạn xây dựng thành công đội ngũ Subagent đắc lực cho riêng mình!*  
**Đội ngũ Biên soạn — Fanpage AI Players: Người chơi hệ AI**
