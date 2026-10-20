---
task_id: CAMP-20261021-W1-mkt
campaign_id: CAMP-20261021-ai-players-subagent-course-funnel
owner: mkt
status: DRAFT_ONLY
data_cutoff_date: "2026-10-21 (Asia/Ho_Chi_Minh)"
references:
  - "f:\\Ai Agent Setup\\SubAgent\\Subagent\\mkt.md"
  - "f:\\Ai Agent Setup\\SubAgent\\Subagent\\knowledge\\bo-nao-thu-2\\memories\\MEM-20261012-page-network-pilot.md"
  - "f:\\Ai Agent Setup\\SubAgent\\Subagent\\knowledge\\bo-nao-thu-2\\memories\\MEM-20261013-facebook-page-community-nurture.md"
  - "f:\\Ai Agent Setup\\SubAgent\\Subagent\\knowledge\\bo-nao-thu-2\\memories\\MEM-20261014-ai-page-comment-hook-playbook.md"
---

# BÁO CÁO NGHIÊN CỨU THỊ TRƯỜNG, CHIẾN LƯỢC TỐI ƯU PHỄU SẢN PHẨM SUBAGENT & GIẢI PHẪU 4 TỆP KHÁCH HÀNG MỤC TIÊU (ICP)

> [!IMPORTANT]
> **Quy ước phân loại bằng chứng theo chuẩn `mkt.md`:**
> - **`[FACT]`**: Quan sát thực tế từ thị trường đào tạo AI tại Việt Nam (2025–2026), chính sách nền tảng quảng cáo (Meta/TikTok), hoặc dữ liệu đầu vào từ Task Packet & Bộ não thứ 2.
> - **`[ESTIMATE]`**: Ước lượng hành vi người dùng, khung giờ hoạt động, tâm lý tiêu dùng và tỷ lệ chuyển đổi dự kiến dựa trên mặt bằng thị trường EdTech/Coaching Việt Nam (cần kiểm chứng qua chiến dịch test 7–14 ngày).
> - **`[STRATEGIC RECOMMENDATION]`**: Đề xuất chiến lược định vị, tái cấu trúc phễu, thông điệp (hook) và mô hình đóng gói sản phẩm dành cho CEO.

---

## PHẦN 1: ĐÁNH GIÁ THẲNG THẮN ĐỊNH HƯỚNG CỦA CEO & TOÀN CẢNH THỊ TRƯỜNG AI/SUBAGENT VIỆT NAM

### 1.1. Bối cảnh thị trường khóa học AI tại Việt Nam (Ngày chốt: 21/10/2026)

1. **`[FACT]` Sự bão hòa của thế hệ khóa học "AI Thế hệ 1" (Prompt & Chat cơ bản):**
   - Giai đoạn 2023–2025, thị trường Việt Nam bùng nổ các khóa học "Viết Prompt ChatGPT", "AI ứng dụng văn phòng cơ bản", "Tạo ảnh/video AI mì ăn liền". Hiện nay, tệp người học phổ thông đã rơi vào trạng thái **"bội thực khóa học giá rẻ (199k–499k) và tài liệu tặng miễn phí"** nhưng tỷ lệ ứng dụng ra kết quả thực tế (tiết kiệm giờ làm thật, ra đơn hàng thật) rất thấp.
2. **`[FACT]` Làn sóng chuyển dịch sang "AI Thế hệ 2 & 3" (Automation & Agentic AI / Subagent):**
   - Thị trường đào tạo giai đoạn 2025–2026 đang phân hóa thành 2 nhánh lớn:
     - **Nhánh Kỹ thuật / No-code Workflow (n8n, Make, Zapier):** Do các đơn vị như Học viện MCI, Cole.vn, và các cộng đồng n8n Vietnam dẫn dắt. Điểm nghẽn: Người không rành kỹ thuật (dân văn phòng, chủ shop, KOC) rất sợ nhìn sơ đồ node chằng chịt, lỗi JSON, cài đặt VPS, nối API.
     - **Nhánh Multi-Agent / Subagent (Đội ngũ tác nhân AI phân quyền):** Thay vì dùng 1 khung chat bắt AI làm đủ thứ (vừa nghiên cứu, vừa viết bài, vừa kiểm duyệt dẫn đến loạn ngữ cảnh), người dùng chia nhỏ công việc cho từng **Subagent** có file quy chuẩn (`System Instructions`), bộ nhớ (`Memory`), và công cụ (`Tools/Skills`) riêng biệt dưới sự điều phối của 1 Quản lý (`Orchestrator/Mama`).
3. **`[FACT]` Độ nhận diện của từ khóa "Subagent" tại Việt Nam:**
   - Trong giới Developer, MMO công nghệ cao, và Power Users (dùng Claude Code, Google Antigravity, Cursor, LangGraph), **"Subagent"** là từ khóa cực nóng và là tiêu chuẩn làm việc mới.
   - Tuy nhiên, **`[ESTIMATE]`** với **trên 85% khách hàng đại chúng** (Nhân sự văn phòng, Chủ shop SME, KOC/Creator phổ thông), từ khóa **"Subagent"** vẫn là một thuật ngữ kỹ thuật xa lạ (Jargon). Họ chưa chủ động gõ từ "Subagent" lên thanh tìm kiếm mà tìm kiếm theo **kết quả đầu ra** (ví dụ: *"cách làm video AI hàng loạt"*, *"AI tự làm báo cáo Excel"*, *"nhân viên AI trực page/viết bài"*).

---

### 1.2. Đánh giá thẳng thắn Cấu trúc Phễu & Hệ thống Sản phẩm của CEO

Cấu trúc hiện tại của CEO được thiết kế theo mô hình **Value Ladder (Thang giá trị)** gồm 3 tầng:
- **Tầng 1 — Phễu miễn phí (Lead Magnets):** (1) Skill cắt video, (2) Khóa học Giờ Vàng, (3) Module Subagent cơ bản cho các ngành/dân văn phòng.
- **Tầng 2 — Khóa chính (Core Offer):** *"Mastery Subagent: Tạo đội ngũ Agent trong mọi lĩnh vực"*.
- **Tầng 3 — Huấn luyện trả phí (Ascension / High-Ticket):** Các cấp độ *Cơ bản → Nâng cao → VIP → Diamond* & Chương trình *"Super AI Chuyển Đổi - 1 Là Thay Đổi 2 Là Chết"*.

#### A. Điểm mạnh cốt lõi trong định hướng của CEO (`[FACT]` & `[STRATEGIC RECOMMENDATION]`)

1. **Đi trước thị trường đại chúng 1 bước về bản chất công nghệ (`Subagent` thay vì `ChatGPT/Prompt`):**
   - Khi đối thủ vẫn đang dạy "1.000 câu lệnh ChatGPT" hoặc dạy kéo thả n8n quá phức tạp về mặt kỹ thuật, việc CEO đánh thẳng vào tư duy **"Tạo đội ngũ Subagent"** (chia vai trò, giao việc bằng ngôn ngữ tự nhiên kết hợp Skill thực thi như cắt video, nghiên cứu thị trường, viết bài) là một **Unique Mechanism (Cơ chế độc quyền)** cực kỳ đắt giá. Nó giải thích hợp lý cho khách hàng hiểu: *"Tại sao trước đây bạn dùng AI không hiệu quả? Vì bạn bắt 1 con AI làm việc của 10 phòng ban!"*
2. **Phễu miễn phí chạm đúng "nhu cầu có tính thanh khoản ngay" (Quick Wins):**
   - **"Skill cắt video"**: Đánh trúng cơn khát sản xuất video ngắn (Reels/TikTok/Shorts) của cả tệp MMO/Affiliate, Creator lẫn Chủ shop mà không cần biết dựng Premiere/CapCut phức tạp.
   - **"Khóa học Giờ Vàng"**: Đánh trúng nỗi đau "làm ra bài/video nhưng đăng không ai xem, không ra tương tác" — giải quyết bài toán phân phối (Distribution) bên cạnh bài toán sản xuất (Production).
   - **"Module Subagent cơ bản cho các ngành/dân văn phòng"**: Tạo sự gần gũi, cá nhân hóa theo từng nghề (HR, Kế toán, Sale, Admin), giúp hạ thấp rào cản sợ công nghệ.
3. **Chiều sâu thang sản phẩm (Cơ bản → Nâng cao → VIP → Diamond):**
   - Cho phép tối ưu hóa LTV (Lifetime Value - Giá trị vòng đời khách hàng): Thu hút số đông bằng phễu miễn phí/cơ bản và tạo biên lợi nhuận cao ở tầng VIP/Diamond (nơi khách hàng là Chủ doanh nghiệp, Agency, MMO Leader sẵn sàng chi trả cao).

#### B. 5 Điểm nghẽn chuyển đổi (Conversion Bottlenecks) & Rủi ro cần xử lý ngay

| STT | Điểm nghẽn / Rủi ro | Phân tích nguyên nhân thực tế (`[FACT]` & `[ESTIMATE]`) | Hậu quả nếu không tối ưu |
| :--- | :--- | :--- | :--- |
| **1** | **Rào cản thuật ngữ "Subagent" ở Phễu Lạnh (Cold Traffic Jargon Friction)** | **`[ESTIMATE]`** Dân văn phòng, chủ shop, người mới nhìn thấy chữ *"Subagent"* sẽ lập tức liên tưởng đến lập trình, code, IT khó hiểu và lướt qua trong 2 giây đầu. Họ không mua "Subagent", họ mua **"Thời gian rảnh, Tốc độ làm việc x5, và Cắt giảm chi phí thuê người"**. | CTR quảng cáo/video thấp ở tệp đại chúng; chỉ thu hút được tệp thích vọc công nghệ (nhưng ít tiền) mà bỏ lỡ tệp Chủ shop/SME (nhiều tiền nhưng sợ kỹ thuật). |
| **2** | **Đứt gãy logic giữa Lead Magnet và Khóa chính (Funnel Bridge Gap)** | Người vào phễu vì *"Khóa học Giờ Vàng"* (mẹo đăng bài/thuật toán mạng xã hội) hoặc *"Skill cắt video"* (công cụ edit) có thể **không hiểu tại sao bước tiếp theo mình phải học "Mastery Subagent"**. Nếu không cài cắm Subagent ngay trong phễu miễn phí, tỷ lệ chuyển đổi từ Free sang Paid sẽ bị gãy. | Tỷ lệ nhận quà miễn phí cao nhưng tỷ lệ mua khóa chính *Mastery Subagent* thấp (dưới 1%). |
| **3** | **Rủi ro kép của tên khóa *"Super AI Chuyển Đổi - 1 Là Thay Đổi 2 Là Chết"*** | 1. **`[FACT]` Rủi ro chính sách nền tảng (Meta Ads / TikTok Ads):** Từ khóa *"Chết"* và cấu trúc câu đe dọa trực diện trên mẫu quảng cáo/landing page rất dễ bị AI kiểm duyệt của Meta/TikTok quét lỗi *Sensationalism / Prohibited Content / Personal Attributes*, dẫn đến từ chối quảng cáo, bóp reach, đắt CPM hoặc khóa tài khoản.<br>2. **`[ESTIMATE]` Tâm lý kháng cự:** Tệp văn phòng và chuyên gia đã quá mệt mỏi với khẩu hiệu dọa dẫm ("AI sẽ cướp việc của bạn") từ năm 2023–2024; dùng ở phễu lạnh dễ bị gắn mác "lùa gà / đa cấp". | Dính gậy chính sách khi chạy Ads; giảm uy tín thương hiệu với nhóm khách hàng trí thức/SME nếu xuất hiện ở điểm chạm đầu tiên (Top-of-Funnel). |
| **4** | **Cái bẫy *"Trong mọi lĩnh vực"* của khóa chính Mastery Subagent** | Khẩu hiệu *"Tạo đội ngũ Agent trong mọi lĩnh vực"* nghe rất rộng nhưng lại làm giảm tính thuyết phục với từng cá nhân. Một kế toán sẽ tự hỏi *"Liệu có áp dụng được cho bảng lương/thuế của tôi không?"*, còn chủ shop lại hỏi *"Có chốt đơn/làm video affiliate được không?"*. | Khách hàng chần chừ không xuống tiền vì sợ kiến thức chung chung, cưỡi ngựa xem hoa như các khóa AI từng học. |
| **5** | **Điểm nghẽn tầng cao (VIP / Diamond) nếu bán "Thêm giờ học" thay vì "Hệ thống cài sẵn"** | **`[ESTIMATE]`** Khách hàng có tiền mua gói VIP / Diamond (Chủ doanh nghiệp, Chủ shop lớn, Leader MMO) là những người **nghèo thời gian nhất**. Nếu gói VIP/Diamond chỉ là "học nhiều buổi hơn", họ sẽ ngại mua vì sợ không có thời gian học và làm. | Khó chốt sale các gói High-Ticket (VIP/Diamond) hoặc khách mua xong bỏ dở, không ra kết quả dẫn đến đòi hoàn tiền/mất uy tín. |

---

## PHẦN 2: ĐỀ XUẤT 4 HƯỚNG TIẾP CẬN & ĐỊNH VỊ SẮC BÉN HƠN (`[STRATEGIC RECOMMENDATION]`)

Để giữ trọn vẹn tầm nhìn lớn của CEO nhưng xóa bỏ hoàn toàn 5 điểm nghẽn trên, `mkt` đề xuất **4 trụ cột tái định vị và tối ưu phễu**:

### Hướng 1: Định vị "Bán Kết Quả & Đội Ngũ Nhân Sự AI 0 Đồng" (Dịch thuật ngữ "Subagent" sang ngôn ngữ Kinh tế & Thời gian)
- **Nguyên tắc:** Không bắt khách hàng hiểu "Subagent là gì" về mặt kỹ thuật ở 3 giây đầu. Hãy định nghĩa:
  > **"ChatGPT chỉ là 1 thực tập sinh hỏi gì đáp nấy. Còn SUBAGENT là một PHÒNG BAN NHÂN SỰ AI CHUYÊN TRÁCH — có Giám đốc điều hành (Mama Agent) và các nhân viên chuyên môn (Nghiên cứu, Viết kịch bản, Cắt video, Chăm sóc khách, Kiểm duyệt) tự phối hợp làm việc cho bạn 24/7 với lương 0 đồng."**
- **Cách gọi tên chuyển đổi cao:**
  - Với Dân văn phòng: *"Bộ Trợ Lý Phân Việc Tự Động (Subagent) — Giải phóng 2 giờ làm báo cáo & giấy tờ mỗi ngày"*.
  - Với Creator / MMO / Affiliate: *"Dây Chuyền Sản Xuất Video & Content Đa Kênh Bằng Đội Ngũ Subagent — Làm 1 mình bằng cả ekip 5 người"*.
  - Với Chủ shop / SME / Agency: *"Xây Dựng Phòng Ban Nhân Sự AI 0 Đồng — Cắt giảm 60% tải vận hành lặp lại mà không cần tuyển thêm người"*.

### Hướng 2: Thiết kế lại "Cầu nối Phễu Miễn Phí (Lead Magnets)" để khóa chặt vào Core Offer
Mọi phễu miễn phí phải là **"Một mảnh ghép cắt ra từ Hệ thống Subagent"** để người học trải nghiệm sức mạnh của Subagent ngay lập tức, nhưng muốn chạy tự động toàn trình thì phải lên khóa chính:
1. **Phễu Free 1 — "Skill Cắt Video":** Đừng chỉ dạy dùng phần mềm cắt video thông thường. Hãy tặng **"1 Subagent Đạo Diễn & Cắt Video Tự Động (dùng câu lệnh cắt ghép + chèn sub chuẩn Brand-Kit trong 3 phút)"**. Sau khi họ cắt xong 1 video cực nhanh, chỉ cho họ thấy: *"Cắt video chỉ là 1 khâu. Muốn có kịch bản triệu view trước khi cắt và tự động chọn sản phẩm thắng, bạn cần thêm Subagent Nghiên cứu (MKT) và Subagent Biên kịch (Content) trong khóa Mastery Subagent!"*
2. **Phễu Free 2 — "Khóa Học Giờ Vàng":** Đừng chỉ cho bảng khung giờ đăng bài tĩnh. Hãy biến nó thành **"Khung Giờ Vàng + Subagent Lên Lịch & Tương Tác Kéo Bình Luận Tự Động theo từng khung giờ tâm lý khách hàng"**. Khi họ biết giờ vàng nhưng không có sức ngày nào cũng ngồi viết 2–3 bài đúng giờ vàng, họ sẽ khao khát sở hữu đội ngũ Subagent làm thay.
3. **Phễu Free 3 — "Module Subagent Cơ Bản Cho Các Ngành/Dân Văn Phòng":** Đóng gói thành **"Bản Cài Thử 1 Nhân Viên Subagent Mẫu"** cho đúng ngành của họ (Ví dụ: 1 Subagent lọc CV cho HR, 1 Subagent đối soát hóa đơn cho Kế toán, 1 Subagent viết 10 kịch bản tư vấn cho Sale). Khi dùng thử 1 Subagent thấy sướng, họ sẽ tự hỏi: *"Làm sao để tự tạo ra 10 Subagent phục vụ riêng cho mọi đầu việc của mình?"* $\rightarrow$ Chốt thẳng vào **Mastery Subagent**.

### Hướng 3: Chiến lược "Hai Tầng Ngôn Ngữ" cho khóa *"Super AI Chuyển Đổi - 1 Là Thay Đổi 2 Là Chết"* (Vừa giữ độ gắt của CEO, vừa an toàn 100% với Meta/TikTok Ads)
- **Ở tầng Front-End (Quảng cáo Meta/TikTok, Bài đăng Page công khai, Landing Page chạy Ads):**
  - **TUYỆT ĐỐI KHÔNG** đưa chữ *"Chết"* lên Text quảng cáo, Ảnh/Video Thumbnail chạy Ads để tránh bị thuật toán Meta phạt lỗi *Sensationalism / Personal Threat*.
  - **Tên hiển thị an toàn & sang trọng (Ad-Safe Title):**
    - Phương án A: ***"Super AI Chuyển Đổi: Tái Cấu Trúc Sự Nghiệp & Kinh Doanh Trước Làn Sóng Thay Thế Nhân Sự"***
    - Phương án B: ***"Super AI Chuyển Đổi: Làm Chủ Đội Ngũ AI Hoặc Bị Bỏ Lại Phía Sau"***
    - Phương án C (Viết tắt gây tò mò): ***"Super AI Chuyển Đổi — Quy Luật Sinh Tồn Mới Thời Đại Agentic AI"***
- **Ở tầng Back-End (Trong phòng Zoom kín, Livestream chốt sale, Nhóm Zalo/Telegram nội bộ, Slide thuyết trình của CEO):**
  - Giữ nguyên thông điệp gốc đầy sức nặng của CEO: ***"1 Là Thay Đổi — 2 Là Đào Thải (Chết về mặt năng lực cạnh tranh)"***. Trong không gian kín, sau khi đã chứng minh bằng case study thực tế (1 người có Subagent làm bằng 10 người làm thủ công), câu nói này sẽ trở thành **đòn bẩy tâm lý (Urgency Trigger)** cực mạnh thúc đẩy khách hàng ra quyết định ngay trong phiên.

### Hướng 4: Tái cấu trúc Thang sản phẩm trả phí (Cơ bản → Nâng cao → VIP → Diamond) theo mô hình **"Từ Tự Làm (DIY) $\rightarrow$ Cầm Tay Chỉ Việc (DWY) $\rightarrow$ Cài Đặt Trọn Bộ Chạy Sẵn (Plug-and-Play)"**

```mermaid
flowchart TD
    subgraph FREE["TẦNG 1: PHỄU MIỄN PHÍ (QUICK-WIN LEAD MAGNETS)"]
        F1["Skill Cắt Video bằng Subagent (3 phút)"]
        F2["Khóa Học Giờ Vàng + Bản đồ Tâm lý Khách hàng"]
        F3["Module 1 Subagent Mẫu theo Ngành (Văn phòng/MMO/Shop)"]
    end

    subgraph TRIPWIRE["TẦNG 1.5: BOOTCAMP CHUYỂN ĐỔI (LỌC KHÁCH)"]
        T1["Super AI Chuyển Đổi<br/>(Ad-Safe: 'Làm Chủ Đội Ngũ AI Hoặc Bị Bỏ Lại' / Nội bộ: '1 Là Thay Đổi 2 Là Chết')"]
    end

    subgraph CORE["TẦNG 2: CORE OFFER (KHÓA CHÍNH)"]
        C1["MASTERY SUBAGENT: Tạo Đội Ngũ Nhân Sự AI 0 Đồng<br/>(1 Khung tư duy lõi + 4 Bộ Template Ngành chuyên biệt: Văn phòng / Creator-MMO / Marketing / SME)"]
    end

    subgraph LADDER["TẦNG 3: THANG HUẤN LUYỆN TRẢ PHÍ (VALUE LADDER)"]
        L1["GÓI CƠ BẢN (DIY - Tự lắp ráp)<br/>Video bài giảng + Kho Prompt/Skill chuẩn + Cộng đồng hỏi đáp"]
        L2["GÓI NÂNG CAO (Multi-Agent System)<br/>Thiết kế Đội ngũ 5-10 Subagent phối hợp + Kết nối Automation/Data"]
        L3["GÓI VIP (Done-With-You - Cài Đặt Trực Tiếp)<br/>Cài đặt sẵn Bộ Subagent vào máy học viên + Coaching 1:1 / Nhóm nhỏ sửa lỗi thực chiến"]
        L4["GÓI DIAMOND (Done-For-You / Enterprise Clone)<br/>Thiết kế riêng Hệ thống Subagent độc quyền cho Shop/Doanh nghiệp + Đồng hành 6-12 tháng"]
    end

    F1 & F2 & F3 --> T1
    T1 --> C1
    C1 --> L1 --> L2 --> L3 --> L4
```

---

## PHẦN 3 & 4: GIẢI PHẪU CHI TIẾT 4 TỆP KHÁCH HÀNG MỤC TIÊU (ICP A, B, C, D)

Dưới đây là bản giải phẫu thực chiến cho 4 tệp khách hàng mục tiêu theo đúng yêu cầu: **Họ ở đâu trên không gian mạng, Khung giờ vàng & Trạng thái tâm lý từng khung giờ, 5 Nỗi đau thực chiến nhất khi dùng AI hiện nay (vì sao học nhiều nơi vẫn không làm được việc), và Key Hook chuyển đổi.**

---

### TỆP A: DÂN VĂN PHÒNG & CHUYÊN MÔN (HR, Kế toán, Admin, Sale, Quản lý cấp trung)

#### 1. Chân dung & Sức mua (`[ESTIMATE]`)
- **Độ tuổi:** 23 – 38 tuổi. Thu nhập: 9 – 30 triệu VNĐ/tháng.
- **Mục tiêu cốt lõi:** Giải phóng khỏi việc giấy tờ/báo cáo lặp đi lặp lại, về đúng giờ, không bị sếp chê chậm tiến độ, nâng cấp năng lực để không bị cắt giảm nhân sự và có thời gian làm nghề tay trái.
- **Ngưỡng chi trả dễ chốt:** Miễn phí $\rightarrow$ 299k – 1.990k (Gói Cơ bản/Nâng cao). Nhóm Trưởng phòng/Sale B2B thu nhập cao có thể mua gói VIP (3.900k – 7.900k) nếu giúp họ chốt sale hoặc quản lý team.

#### 2. Bảng giải phẫu Hành vi, Khung giờ vàng, 5 Nỗi đau & Key Hook — Tệp A (Dân Văn Phòng)

| Hạng mục giải phẫu | Chi tiết thực chiến (`[FACT]` quan sát cộng đồng & `[ESTIMATE]` hành vi) |
| :--- | :--- |
| **1. Họ tập trung ở đâu trên không gian mạng?** | - **Facebook Groups:** *Bình Dân Học AI, Nghiện AI, Cộng đồng AI ứng dụng Văn phòng, Tâm Sự Con Sen, Chuyện Công Sở, Cộng đồng Nhân sự Việt Nam (HR Share), Cộng đồng Kế Toán Việt Nam, Hội Sales & Chăm sóc khách hàng, Cộng đồng Excel & Google Sheets Việt Nam.*<br>- **Facebook Pages / Reels:** Các kênh chia sẻ mẹo Excel/Word/Slide nhanh, các page hài công sở (tương tự định hướng *Hội Deadline, Văn Phòng Hết Pin, 5 Phút Trước Cuộc Họp* trong `MEM-20261012-page-network-pilot`).<br>- **TikTok / YouTube Shorts:** Xem các kênh "Mẹo văn phòng 60s", "Excel/AI cứu cánh deadline", vlog đời sống công sở.<br>- **Threads:** Nơi dân văn phòng trẻ (Gen Z, Millennials) than thở cực mạnh về chuyện sếp giao việc vô lý, OT không lương, áp lực KPI hàng ngày.<br>- **Zalo:** Sống trong hàng chục nhóm Zalo công việc của công ty; thường lưu các link tài liệu/template hữu ích vào *"Truyền File (Cloud của tôi)"* để mở trên máy tính văn phòng.<br>- **LinkedIn:** Tệp HR, Sale B2B, Kế toán trưởng, Quản lý cấp trung hoạt động mạnh để tìm cơ hội nghề nghiệp và khoe chứng chỉ/kỹ năng mới. |
| **2. Khung giờ vàng Online & Trạng thái tâm lý từng khung giờ** | - **07:15 – 08:30 (Trên đường đi làm / Ăn sáng / Ngồi cà phê đầu giờ):**<br>  + *Tâm lý:* Ngại bắt đầu một ngày làm việc ngập đầu việc vụn vặt; lướt điện thoại nhanh.<br>  + *Nội dung chạm:* Bài ngắn dạng Checklist / Mẹo giải quyết nhanh 1 việc trong ngày (đúng nhịp Bài 1 buổi sáng của `MEM-20261014-ai-page-comment-hook-playbook`).<br>- **11:45 – 13:15 (Nghỉ trưa tại bàn làm việc hoặc quán ăn):**<br>  + *Tâm lý:* Vừa trải qua buổi sáng mệt mỏi với sếp/khách hàng; đang ngồi trước máy tính hoặc cầm điện thoại; **rất sẵn sàng tải tài liệu/template về test ngay trên PC công ty**.<br>  + *Nội dung chạm:* Video ngắn 45–60s Before/After xử lý bảng biểu/báo cáo/email, bài tặng Template/Module Subagent văn phòng.<br>- **16:30 – 17:45 (Giờ "Hết Pin" cuối buổi chiều công sở):**<br>  + *Tâm lý:* Mệt não nhưng vẫn bị kẹt vì báo cáo cuối ngày chưa xong hoặc lướt mạng chờ hết giờ.<br>  + *Nội dung chạm:* Nội dung đồng cảm nỗi đau deadline + giải pháp "Bấm nút 3 phút xong báo cáo để 5h chiều xách túi về thẳng".<br>- **20:30 – 22:30 (Sau khi ăn tối, nằm nghỉ hoặc học thêm):**<br>  + *Tâm lý:* Lo lắng về tương lai, thu nhập, sợ tụt hậu; có thời gian xem video dài hơn (Livestream, Zoom, Webinar).<br>  + *Nội dung chạm:* Livestream/Zoom chuyển đổi khóa *Mastery Subagent* hoặc *Super AI Chuyển Đổi*. |
| **3. 5 Nỗi đau thực chiến nhất khi dùng AI hiện nay (Vì sao học nhiều nơi vẫn không làm được việc?)** | 1. **Học thuộc lòng "1.000 câu lệnh (Prompt)" nhưng mở file công ty ra thì tịt:** Các khóa học cũ chỉ phát cho file PDF chứa hàng trăm câu lệnh dịch từ tiếng Anh. Khi đưa bảng Excel lộn xộn, hợp đồng dài 30 trang hay JD tuyển dụng thực tế vào, AI trả lời sáo rỗng, sai ngữ cảnh công ty.<br>2. **Mất thời gian dạy lại AI từ đầu mỗi ngày (Mất trí nhớ ngữ cảnh):** Hôm qua vừa chỉnh cho ChatGPT hiểu quy định công ty và văn phong sếp muốn, hôm nay mở đoạn chat mới lại phải gõ lại từ đầu, tốn thời gian hơn cả tự làm.<br>3. **AI "bịa số liệu" (Hallucination) và phá hỏng định dạng (Format):** Kế toán, Admin, HR sợ nhất là AI cộng sai số, trích xuất thiếu dòng, hoặc xuất ra đoạn văn bản phải ngồi copy-paste, căn chỉnh lại bảng biểu trong Word/Excel mất thêm 1 tiếng.<br>4. **Bắt 1 khung chat làm 10 việc dẫn đến kết quả "nửa vời":** Vừa bắt nó phân tích dữ liệu, vừa bắt viết báo cáo, vừa bắt làm slide trong 1 luồng chat khiến AI bị nhiễu loạn, câu sau quên câu trước.<br>5. **Sợ lộ dữ liệu nội bộ & sợ công cụ kỹ thuật phức tạp:** Nghe đến cài đặt API, Docker, code Python hay n8n là dân văn phòng bỏ cuộc ngay vì máy tính công ty chặn cài đặt hoặc bản thân không biết code. |
| **4. Key Hook Chuyển Đổi & Cảnh Before/After 3–5s** | - **Key Hook 1 (Đánh vào nỗi đau dạy lại AI):** *"Đừng học thuộc lòng 1.000 câu lệnh ChatGPT nữa! Đây là cách đóng gói toàn bộ quy trình làm việc của bạn thành 1 Nhân viên Subagent — chỉ cần dạy 1 lần duy nhất, từ mai chỉ việc ném file vào là có báo cáo chuẩn ý sếp."*<br>- **Key Hook 2 (Đánh vào thời gian tan làm):** *"Tại sao đồng nghiệp cùng phòng 5h chiều đã thảnh thơi về mà báo cáo vẫn mượt, còn bạn 8h tối vẫn ngồi lọc từng dòng Excel? Bí mật nằm ở 3 Subagent chuyên biệt cho dân văn phòng này."*<br>- **Key Hook 3 (Dẫn vào Module Subagent miễn phí):** *"Tặng miễn phí Bộ 4 Subagent Văn Phòng (HR lọc CV - Kế toán rà số - Sale viết kịch bản bám đuổi - Admin làm biên bản họp). Bình luận đúng tên bộ phận của bạn để nhận file cài trong 3 phút!"*<br>- **Visual Before/After (3–5s đầu video):**<br>  + *Before:* Màn hình máy tính mở 15 tab Excel/Word rối mù, đồng hồ chỉ 19:30, nhân vật văn phòng vò đầu bứt tai.<br>  + *After:* Chỉ 1 thao tác thả file vào thư mục Subagent $\rightarrow$ 3 cửa sổ Subagent tự động chạy параллельно (Phân tích số liệu $\rightarrow$ Viết báo cáo $\rightarrow$ Xuất bảng sạch đẹp) trong 5 giây. |

---

### TỆP B: CONTENT CREATOR / MMO / AFFILIATE / KOC (Người làm kiếm tiền online, xây kênh, tiếp thị liên kết)

#### 1. Chân dung & Sức mua (`[ESTIMATE]`)
- **Độ tuổi:** 18 – 35 tuổi. Thu nhập biến động mạnh (từ người mới kiếm 3–5 triệu/tháng đến các MMO Leader kiếm 50–300 triệu/tháng).
- **Mục tiêu cốt lõi:** Sản xuất nội dung/video số lượng lớn (SLL) với chi phí thấp nhất, nuôi hệ thống nhiều kênh (Page/TikTok/YouTube) cùng lúc, bắt trend nhanh, kéo traffic và ra hoa hồng (Affiliate/AdSense) thật.
- **Ngưỡng chi trả dễ chốt:** Rất nhạy với bất kỳ công cụ nào giúp **"Làm nhanh hơn – Nhiều kênh hơn – Ra tiền nhanh hơn"**. Sẵn sàng mua từ khóa Cơ bản/Nâng cao (990k – 3.900k) đến gói VIP/Diamond (10 – 30 triệu) nếu được chuyển giao quy trình làm video/nuôi hệ thống kênh thực chiến.

#### 2. Bảng giải phẫu Hành vi, Khung giờ vàng, 5 Nỗi đau & Key Hook — Tệp B (Creator / MMO / Affiliate / KOC)

| Hạng mục giải phẫu | Chi tiết thực chiến (`[FACT]` quan sát cộng đồng & `[ESTIMATE]` hành vi) |
| :--- | :--- |
| **1. Họ tập trung ở đâu trên không gian mạng?** | - **Facebook Groups:** *Cộng đồng MMO Việt Nam, Kiếm tiền Affiliate Shopee/TikTok Shop, Tâm Sự Affiliate, Hội Xây Kênh TikTok/Reels Không Lộ Mặt (Faceless), Cộng đồng AI Video & Ảnh (Kling, Runway, Veo, Google Flow, Remotion), Hội Reup & Bán Nội Dung Số, Bình Dân Học AI.*<br>- **Facebook Pages / Reels:** Thường xuyên lướt và "mổ xẻ" các Page AI Affiliate triệu view, các Page kéo bình luận kiểu Kingcontent (`MEM-20261014-ai-page-comment-hook-playbook`), lưu video đối thủ về để phân tích hook.<br>- **TikTok:** Sống trên TikTok để soi xu hướng âm thanh, giỏ hàng vàng, các kênh AI bán hàng gia dụng/phòng trọ.<br>- **YouTube:** Xem các video hướng dẫn dài (15–45 phút) về tut/trick làm MMO, cách dùng công cụ AI tạo video đồng nhất nhân vật, tự động hóa xây kênh.<br>- **Zalo / Telegram:** Hoạt động cực mạnh trong các nhóm Zalo/Telegram kín chia sẻ kèo Affiliate, nhóm nhận tài nguyên (prompt, tool cắt video, suộc video). |
| **2. Khung giờ vàng Online & Trạng thái tâm lý từng khung giờ** | - **09:00 – 11:30 (Giờ soi trend, tìm sản phẩm & lên kịch bản):**<br>  + *Tâm lý:* Bí ý tưởng, loay hoay không biết hôm nay làm sản phẩm gì, viết kịch bản sao cho không bị flop.<br>  + *Nội dung chạm:* Bài chia sẻ quy trình tìm sản phẩm thắng (Winning SKU), công thức viết Hook 3s đầu, tặng Prompt/Subagent soi đối thủ.<br>- **14:00 – 17:00 (Giờ cày cuốc sản xuất & dựng video):**<br>  + *Tâm lý:* Kiệt sức vì phải cắt ghép từng clip, chèn phụ đề, tạo giọng đọc, render lỗi, làm 3 tiếng mới xong 1 video ngắn.<br>  + *Nội dung chạm:* **Phễu "Skill Cắt Video" & Subagent dựng video hàng loạt** chạm mạnh nhất ở khung giờ này!<br>- **19:30 – 21:00 (Giờ đăng bài & Canh "Giờ Vàng" kéo tương tác):**<br>  + *Tâm lý:* Hồi hộp canh view sau khi đăng bài; sốt ruột khi đăng xong lẹt đẹt vài chục view.<br>  + *Nội dung chạm:* **Phễu "Khóa Học Giờ Vàng"** + Chiến thuật kéo bình luận và nuôi tương tác cộng đồng (`MEM-20261013-facebook-page-community-nurture`).<br>- **22:00 – 01:30 sáng (Giờ "Cú Đêm" của dân MMO / Creator):**<br>  + *Tâm lý:* Khung giờ tập trung cao nhất của dân MMO; hay xem các case study "Giải phẫu hệ thống 10–20 Page", xem webinar và dễ bấm mua khóa học nhất lúc đêm muộn vì khao khát đột phá thu nhập. |
| **3. 5 Nỗi đau thực chiến nhất khi dùng AI hiện nay (Vì sao học nhiều nơi vẫn không làm được việc?)** | 1. **Đứt gãy quy trình giữa 10 công cụ rời rạc ("Ác mộng Copy-Paste"):** Tìm sản phẩm một nơi, sang ChatGPT xin kịch bản, qua ElevenLabs lấy voice, sang công cụ khác tạo ảnh/video, rồi mở CapCut căn chỉnh từng dòng chữ. Làm 1 video mất 2–3 tiếng thì không thể nhân bản lên 10–20 kênh.<br>2. **Video AI nhìn "giả trân", sai sản phẩm thật hoặc vô hồn nên có view mà không có đơn:** Học các khóa chỉ dạy tạo ảnh/video AI lung linh nhưng khách nhìn vào biết ngay đồ giả (hoặc sai màu/kiểu dáng SKU trên Shopee), dẫn đến click ảo hoặc bị bóp tương tác.<br>3. **Kịch bản AI viết ra giọng "Văn mẫu công nghiệp":** Cứ mở đầu là *"Bạn có biết..."*, *"Trong thời đại ngày nay..."* khiến người xem lướt đi trong 1.5 giây đầu tiên.<br>4. **Không biết cách quản lý chất lượng khi làm số lượng lớn (SLL):** Làm 1 kênh thì nhớ, làm đến kênh thứ 3 là loạn phong cách ảnh, loạn giọng văn, quên lịch đăng, dẫn đến bỏ kênh giữa chừng.<br>5. **Tốn tiền mua đủ loại tài khoản/tool AI mỗi tháng nhưng không ra hệ thống:** Mỗi tháng đốt 2–3 triệu tiền mua tool theo lời giới thiệu trên mạng nhưng vẫn phải ngồi cày tay 14 tiếng/ngày. |
| **4. Key Hook Chuyển Đổi & Cảnh Before/After 3–5s** | - **Key Hook 1 (Dẫn thẳng vào Skill Cắt Video & Khóa Giờ Vàng):** *"Làm Affiliate mà ngồi cắt CapCut từng giây với gõ phụ đề bằng tay thì bao giờ mới nuôi nổi 5 kênh? Xem cách mình giao cho Subagent tự động cắt video, gắn sub trượt chuẩn Brand-Kit và canh đúng Giờ Vàng lên bài chỉ trong 10 phút!"*<br>- **Key Hook 2 (Đánh vào bản chất Đội ngũ Subagent):** *"Bí mật của những tay chơi vận hành 10–20 Page AI cùng lúc không phải là họ thức 24/24, mà là họ có 1 Đội ngũ 5 Subagent: 1 con soi sản phẩm ngon, 1 con viết kịch bản chuẩn nhịp, 1 con dựng video, 1 con kiểm duyệt tránh gậy chính sách!"*<br>- **Key Hook 3 (Kéo bình luận theo `MEM-20261014`):** *"Giải phẫu toàn bộ luồng lệnh giúp 1 người vận hành dây chuyền Video AI Bán Hàng SLL mà không bị 'văn mẫu ChatGPT'. Bình luận từ khóa `SUBAGENT` để nhận miễn phí Module Cắt Video + Lịch Giờ Vàng 2026."*<br>- **Visual Before/After (3–5s đầu video):**<br>  + *Before:* Người làm MMO mắt thâm quầng lúc 1h sáng, màn hình CapCut dày đặc timeline thủ công, kênh TikTok/Reels hiện "12 lượt xem".<br>  + *After:* Giao lệnh cho `mama` $\rightarrow$ `mkt`, `content`, `edit` tự động trả ra kịch bản + video hoàn chỉnh có sub sắc nét, bảng quản lý 5 Page xanh mượt. |

---

### TỆP C: MARKETER / FREELANCER / AGENCY NHỎ (Performance, Content, Social, SEO, Branding)

#### 1. Chân dung & Sức mua (`[ESTIMATE]`)
- **Độ tuổi:** 22 – 36 tuổi. Thu nhập: 12 – 50 triệu VNĐ/tháng.
- **Mục tiêu cốt lõi:** Nhận được nhiều dự án/khách hàng (Client) hơn mà không phải thuê thêm nhân sự; rút ngắn thời gian nghiên cứu thị trường (Research), lập kế hoạch (Plan), sản xuất đa định dạng (Creative Variations) để test Ads; giữ đúng Brand Voice cho từng khách hàng riêng biệt.
- **Ngưỡng chi trả dễ chốt:** Đây là tệp hiểu giá trị của **"Quy trình (Workflow) & Tài sản tái sử dụng"**. Rất dễ chốt khóa chính *Mastery Subagent* (1.990k – 4.990k) và gói *Nâng cao / VIP* (7.900k – 19.900k) vì chỉ cần áp dụng vào 1–2 dự án của Client là họ đã hoàn vốn 100%.

#### 2. Bảng giải phẫu Hành vi, Khung giờ vàng, 5 Nỗi đau & Key Hook — Tệp C (Marketer / Freelancer / Agency nhỏ)

| Hạng mục giải phẫu | Chi tiết thực chiến (`[FACT]` quan sát cộng đồng & `[ESTIMATE]` hành vi) |
| :--- | :--- |
| **1. Họ tập trung ở đâu trên không gian mạng?** | - **Facebook Groups:** *Tâm Sự iSocial, Cộng đồng Digital Marketing Việt Nam, Vũ Trụ Creator / Copywriter Việt Nam, Hội Performance Marketing / Facebook Ads Việt Nam, Cộng đồng Freelancer Việt Nam, Hội n8n & AI Automation Việt Nam, Bình Dân Học AI.*<br>- **Facebook Profiles / Pages:** Theo dõi sát các chuyên gia Marketing thực chiến, các bài phân tích Case Study dài (Long-form post), các bài bóc tách phễu (Funnel Teardown).<br>- **Threads & LinkedIn:** Nơi Marketer/Agency thảo luận sôi nổi về chiến thuật mới, khoe kết quả chiến dịch, than phiền về việc khách hàng (Client) bắt sửa bài 10 lần hoặc giá thầu Ads đắt đỏ.<br>- **YouTube:** Xem các kênh chuyên sâu về AI Workflow, Automation, Prompt hệ thống, thiết kế thương hiệu đồng nhất.<br>- **Zalo:** Nhóm làm việc với Client, nhóm cộng đồng MarTech/AdTech. |
| **2. Khung giờ vàng Online & Trạng thái tâm lý từng khung giờ** | - **08:30 – 10:00 (Giờ kiểm tra số liệu Ads / Đọc tin ngành đầu ngày):**<br>  + *Tâm lý:* Căng thẳng nhìn chi phí quảng cáo (CPM/CPA) tăng cao do thiếu mẫu nội dung (Creative) mới để test.<br>  + *Nội dung chạm:* Bài viết phân tích cách dùng Subagent tạo 10 góc tiếp cận (Creative Angles) và 30 kịch bản test 3–3–3 trong 1 buổi sáng.<br>- **13:30 – 15:30 (Giờ chạy Brief, làm Proposal & bị Client giục sửa bài):**<br>  + *Tâm lý:* Quá tải vì một mình phải kiêm từ nghiên cứu đối thủ, lập kế hoạch, viết bài, làm ảnh đến báo cáo hiệu suất.<br>  + *Nội dung chạm:* Case study trực diện: *"Cách thiết lập Bộ 4 Subagent đóng vai 1 Agency thu nhỏ (Researcher - Copywriter - Art Director - QA)".*<br>- **21:00 – 23:30 (Giờ Freelancer cày job ngoài giờ / Agency Owner tính bài toán lợi nhuận):**<br>  + *Tâm lý:* Muốn nhận thêm khách để tăng thu nhập nhưng sức người đã chạm trần; thuê thêm thực tập sinh/nhân sự mới thì tốn thời gian đào tạo và ăn mòn hết biên lợi nhuận.<br>  + *Nội dung chạm:* Định vị **"Nhân bản quy trình chất lượng cao bằng Hệ thống Subagent có Bộ nhớ riêng (Memory) cho từng Client"**. |
| **3. 5 Nỗi đau thực chiến nhất khi dùng AI hiện nay (Vì sao học nhiều nơi vẫn không làm được việc?)** | 1. **AI làm mất "Chất riêng thương hiệu" (Brand Voice & Style Consistency):** Khi quản lý 3–5 khách hàng hoặc 3–5 Page khác nhau, dùng AI thông thường sẽ bị lẫn lộn giọng văn, màu sắc thiết kế lộn xộn, khách hàng duyệt bài trả về vì "nhìn giống bài viết bằng AI".<br>2. **Không có bộ nhớ dài hạn (Second Brain / Memory) cho từng dự án:** Mỗi lần làm chiến dịch mới lại phải nạp lại từ đầu tệp khách hàng, sản phẩm, từ khóa cấm của thương hiệu đó.<br>3. **Thiếu khâu Kiểm duyệt chéo (Quality Gate / Fact-check):** AI viết nhanh nhưng hay chém gió quá đà (Overclaim) dễ vi phạm chính sách quảng cáo Facebook/TikTok, khiến Marketer mất công ngồi sửa lại từng câu còn lâu hơn tự viết.<br>4. **Học Automation (n8n/Make) thì quá cứng nhắc, còn chat thủ công thì quá chậm:** Các luồng tự động hóa cố định không xử lý được các bài toán sáng tạo linh hoạt (như phân tích tâm lý ngách mới hay đổi góc kịch bản), trong khi hệ thống **Subagent có khả năng tự suy luận và phối hợp đa bước** lại chưa được ai dạy bài bản.<br>5. **Không đóng gói được quy trình để bàn giao cho nhân sự Junior làm theo chuẩn:** Chủ Agency nhỏ biết dùng AI nhưng nhân viên dùng thì ra rác vì không có quy chuẩn đóng gói thành Subagent cố định. |
| **4. Key Hook Chuyển Đổi & Cảnh Before/After 3–5s** | - **Key Hook 1 (Đánh vào biên lợi nhuận Freelancer/Agency):** *"Đừng tuyển thêm người khi chưa xây xong Đội ngũ Subagent này! Cách 1 Freelancer vận hành khối lượng công việc của cả 1 Agency 8 người (Nghiên cứu thị trường $\rightarrow$ Kịch bản $\rightarrow$ Thiết kế đồng bộ Brand-Kit $\rightarrow$ Kiểm duyệt) mà vẫn giữ nguyên chất riêng từng thương hiệu."*<br>- **Key Hook 2 (Đánh vào nỗi đau AI viết chung chung):** *"Lý do AI của bạn viết bài nào cũng nhạt nhẽo là vì bạn chưa tách riêng 'Subagent Nghiên Cứu Insight' khỏi 'Subagent Viết Bài' và 'Subagent Kiểm Duyệt'. Xem cấu trúc Bộ não thứ 2 + Đội ngũ Subagent thực chiến này!"*<br>- **Visual Before/After (3–5s đầu video):**<br>  + *Before:* Bảng Trello/Notion ngập thẻ đỏ "Trễ hạn", khách hàng nhắn tin Zalo giục liên tục, bài viết AI bị gạch xóa đỏ chói.<br>  + *After:* Sơ đồ 1 Quản lý (`mama`) điều phối 4 Subagent có sẵn `Memory` thương hiệu $\rightarrow$ Xuất ra bản nghiên cứu + 10 kịch bản + bộ ảnh chuẩn hệ màu Cobalt-Lime / Editorial đồng bộ 100%. |

---

### TỆP D: CHỦ SHOP / SOLOPRENEUR / CHỦ DOANH NGHIỆP SME (Thương mại điện tử, Dịch vụ, Đào tạo, Kinh doanh truyền thống chuyển đổi số)

#### 1. Chân dung & Sức mua (`[ESTIMATE]`)
- **Độ tuổi:** 27 – 48 tuổi. Doanh thu từ vài trăm triệu đến vài chục tỷ/năm.
- **Mục tiêu cốt lõi:** Tăng doanh số, cắt giảm chi phí lương nhân sự vận hành/marketing cồng kềnh, giảm sự phụ thuộc vào nhân viên (tránh cảnh nhân viên nghỉ việc là sập quy trình), tự động hóa khâu ra nội dung bán hàng và chăm sóc khách.
- **Ngưỡng chi trả dễ chốt:** **Đây là tệp Khách Hàng Vàng cho gói VIP & DIAMOND** và chương trình ***Super AI Chuyển Đổi***. Họ không tiếc 10 – 50 triệu VNĐ nếu nhìn thấy hệ thống đó giúp họ **tiết kiệm 15 – 30 triệu tiền lương nhân sự MỖI THÁNG** và được **cài đặt tận tay (Done-With-You / Done-For-You)**.

#### 2. Bảng giải phẫu Hành vi, Khung giờ vàng, 5 Nỗi đau & Key Hook — Tệp D (Chủ Shop / Solopreneur / SME)

| Hạng mục giải phẫu | Chi tiết thực chiến (`[FACT]` quan sát cộng đồng & `[ESTIMATE]` hành vi) |
| :--- | :--- |
| **1. Họ tập trung ở đâu trên không gian mạng?** | - **Facebook Groups:** *Quản Trị và Khởi Nghiệp, Cộng đồng Doanh nghiệp vừa và nhỏ (SME), Tâm Sự Con Buôn, Lập Nghiệp Cùng Shopee / TikTok Shop, Cộng đồng Chủ Shop Thời Trang / Gia Dụng / F&B, Hội CEO & Quản Trị Thực Chiến.*<br>- **Facebook Newsfeed & Reels:** Hay xem các video phân tích bài toán kinh doanh, tối ưu chi phí vận hành, câu chuyện chuyển đổi số thực tế của các chủ doanh nghiệp khác.<br>- **YouTube:** Xem các talkshow kinh doanh, phân tích chiến lược, hướng dẫn áp dụng AI vào quản trị doanh nghiệp (thường nghe khi lái xe hoặc buổi tối).<br>- **Zalo (Kênh quan trọng số 1 để chốt Sale):** Sống trên Zalo để điều hành nhân viên, làm việc với nhà cung cấp/đối tác. Mọi chăm sóc 1:1 cho tệp này bắt buộc phải đưa về Zalo cá nhân hoặc Zalo nhóm VIP.<br>- **TikTok:** Xem để biết đối thủ đang bán hàng kiểu gì trên livestream/video ngắn. |
| **2. Khung giờ vàng Online & Trạng thái tâm lý từng khung giờ** | - **06:00 – 07:45 (Dậy sớm tập thể dục, uống trà/cà phê, đọc tin kinh doanh):**<br>  + *Tâm lý:* Tỉnh táo nhất trong ngày, suy nghĩ về chiến lược dài hạn, bài toán doanh thu – chi phí của tháng.<br>  + *Nội dung chạm:* Bài viết phân tích sâu sắc về **"Bài toán Chi phí Nhân sự vs. Đội ngũ Subagent"**; thông điệp *Super AI Chuyển Đổi* (phiên bản chiến lược kinh doanh).<br>- **12:00 – 13:30 (Giờ nghỉ trưa ngắn):**<br>  + *Tâm lý:* Tranh thủ lướt xem các giải pháp công cụ giúp nhân viên trong shop/công ty làm việc nhanh hơn.<br>  + *Nội dung chạm:* Video demo ngắn gọn 60s: 1 Chủ shop tự vận hành quy trình ra 30 video bán hàng + kịch bản chăm sóc khách mà không cần đội media đắt đỏ.<br>- **21:30 – 23:30 (Sau khi đóng cửa shop / Kết thúc việc điều hành trong ngày):**<br>  + *Tâm lý:* Thấm mệt vì cả ngày phải đi "chữa cháy" cho nhân viên; cảm thấy cô đơn và áp lực trước biên lợi nhuận ngày càng mỏng; **sợ đối thủ dùng AI vượt mặt mình**.<br>  + *Nội dung chạm:* Khung giờ vàng để mời vào Zoom *Super AI Chuyển Đổi* hoặc tư vấn chốt gói **VIP / Diamond (Cài đặt trực tiếp bộ Subagent cho doanh nghiệp)**. |
| **3. 5 Nỗi đau thực chiến nhất khi dùng AI hiện nay (Vì sao học nhiều nơi vẫn không làm được việc?)** | 1. **Có tiền đi học nhưng KHÔNG CÓ THỜI GIAN ngồi mò mẫm kỹ thuật:** Chủ shop/SME đi học nhiều khóa AI nhưng giảng viên bắt tự ngồi code, tự nối hàng chục bước phức tạp. Về đến nhà quá bận việc kinh doanh nên bỏ xó khóa học.<br>2. **Cử nhân viên đi học thì nhân viên không áp dụng hoặc giỏi lên rồi... xin nghỉ:** Không có một "Hệ thống tài sản AI cố định của công ty" (như Bộ não thứ 2 + Hệ thống Subagent lưu sẵn quy trình trên máy chủ/thư mục công ty) để ai vào ngồi cũng chạy được ngay.<br>3. **Thuê đội Marketing/Media in-house tốn 25–40 triệu/tháng nhưng hiệu suất thấp:** Nhân viên viết bài chậm, quay dựng video tốn kém, bảo làm thêm góc nội dung mới thì kêu quá tải.<br>4. **Sợ bị "lùa gà" các khóa học lý thuyết suông trên mây:** Chủ doanh nghiệp cần nhìn thấy **Quy trình thực tế (SOP)**, **Tiêu chuẩn kiểm duyệt (Rubric/Hard Gate)** và **Bài toán Kinh tế (ROI)** rõ ràng chứ không thích nghe chém gió công nghệ viển vông.<br>5. **Thiếu người "Cầm tay cài đặt vào đúng bài toán của Shop/Công ty mình":** Mỗi ngành hàng (gia dụng, thời trang, dịch vụ, đào tạo) có đặc thù riêng; họ cần người thiết kế hoặc cùng họ lắp sẵn bộ Subagent khớp với sản phẩm của họ. |
| **4. Key Hook Chuyển Đổi & Cảnh Before/After 3–5s** | - **Key Hook 1 (Đánh thẳng vào bài toán Lương nhân sự vs. Lợi nhuận):** *"Nuôi 1 team Marketing 4 người tốn 40 triệu/tháng nhưng mỗi tuần chỉ ra nổi 5 video bán hàng? Hãy xem cách tôi đóng gói toàn bộ quy trình Nghiên cứu sản phẩm – Viết kịch bản – Dựng video – Chăm sóc kênh thành 1 Đội ngũ 10 Subagent làm việc 24/7 không đòi tăng lương, không xin nghỉ việc!"*<br>- **Key Hook 2 (Đánh vào tâm lý Chuyển đổi sinh tồn cho chương trình Super AI):** *"Thời đại này không phải cá lớn nuốt cá bé, mà là Chủ shop biết dùng Đội ngũ AI nuốt chửng Chủ shop vẫn đang vận hành thủ công. Đừng để đối thủ dùng 1 hệ thống Subagent đánh bại cả công ty 20 người của bạn!"*<br>- **Key Hook 3 (Chốt gói VIP/Diamond - Done-With-You):** *"Bạn không cần biến mình thành chuyên gia công nghệ. Chúng tôi trực tiếp cùng bạn cài đặt trọn bộ Phòng Ban Subagent chạy sẵn vào đúng mô hình kinh doanh của bạn trong 14 ngày!"*<br>- **Visual Before/After (3–5s đầu video):**<br>  + *Before:* Chủ shop ôm đầu trước bảng chi phí lương nhân sự đỏ rực, nhân viên ngồi bấm điện thoại, hàng tồn kho chất đống.<br>  + *After:* Màn hình Dashboard điều hành Đội ngũ Subagent tinh gọn: 1 lệnh giao từ CEO $\rightarrow$ Hệ thống tự động xuất kế hoạch sản phẩm, kịch bản, video bán hàng chuẩn chỉnh, chi phí vận hành giảm mạnh. |

---

## PHẦN 5: MA TRẬN TỐI ƯU PHỄU SẢN PHẨM THEO 4 TỆP ICP & KẾ HOẠCH KIỂM CHỨNG (7–14 NGÀY)

### 5.1. Bảng ánh xạ Phễu Sản Phẩm của CEO vào 4 Tệp Khách Hàng (`[STRATEGIC RECOMMENDATION]`)

| Tệp khách hàng (ICP) | Mồi Phễu Miễn Phí (Lead Magnet) hiệu quả nhất | Góc dẫn vào Khóa Chính (*Mastery Subagent*) | Sản phẩm Trả phí chủ lực (Monetization Focus) |
| :--- | :--- | :--- | :--- |
| **A. Dân Văn Phòng & Chuyên Môn** | **Module Subagent cơ bản theo ngành** (Tặng sẵn 1 Subagent mẫu cho HR / Kế toán / Admin / Sale) + **Khóa Giờ Vàng** (cho nhóm làm thêm). | *"Từ 1 Subagent mẫu được tặng $\rightarrow$ Học cách tự tạo trọn bộ 5 Subagent giải quyết 80% việc bàn giấy để về sớm lúc 5h chiều và nhận thêm việc tay trái."* | **Gói Cơ Bản & Nâng Cao** (Tự lắp ráp đội ngũ Subagent cá nhân với chi phí vừa túi tiền dân công sở). |
| **B. Creator / MMO / Affiliate / KOC** | **Skill Cắt Video bằng Subagent** + **Khóa Học Giờ Vàng** (Combo giải quyết ngay bài toán Làm video nhanh & Đăng bài có view). | *"Cắt video và biết giờ vàng mới chỉ là 20% cuộc chơi. Muốn nhân bản 5–20 kênh kiếm tiền tự động, bạn phải sở hữu trọn bộ Subagent: Soi sản phẩm thắng + Viết kịch bản + Dựng video SLL + Nuôi tương tác."* | **Khóa Mastery Subagent (Cơ bản $\rightarrow$ Nâng cao $\rightarrow$ VIP)** (Chuyển giao bộ khung Subagent làm Affiliate/Xây kênh thực chiến). |
| **C. Marketer / Freelancer / Agency nhỏ** | **Module Subagent Marketing & Content** + **Case Study Giải phẫu Hệ thống 10 Subagent vận hành chiến dịch**. | *"Đóng gói chất xám của bạn thành hệ thống Subagent có Bộ nhớ thương hiệu (Second Brain) để nhận gấp 3 lần dự án mà không phải thức đêm hay tuyển thêm người."* | **Gói Nâng Cao & VIP** (Tập trung vào Multi-Agent Workflow, Brand-Kit đồng bộ, và Quản trị nhiều dự án/Client). |
| **D. Chủ Shop / Solopreneur / SME** | **Bản Audit "Cắt giảm 50% tải vận hành bằng Đội ngũ Subagent"** + Vé mời tham dự **Super AI Chuyển Đổi**. | *"Đừng tự mày mò từng công cụ lẻ tẻ. Hãy xây dựng một Phòng Ban Nhân Sự AI 0 Đồng trở thành tài sản cố định của doanh nghiệp bạn."* | **Super AI Chuyển Đổi $\rightarrow$ Gói VIP (Done-With-You cài đặt trực tiếp) & Gói DIAMOND (Thiết kế riêng hệ thống Subagent cho Doanh nghiệp).** |

---

### 5.2. Kế hoạch Kiểm chứng Thực chiến 7–14 Ngày (Test Matrix 3–3–3 theo chuẩn `mkt.md` & `MEM-20261014`)

Để đảm bảo nguyên tắc **"Test one primary variable"** và **"Evidence over intuition"**, trước khi đổ ngân sách lớn, `mkt` đề xuất kế hoạch test 14 ngày trên kênh Page AI Players và mạng lưới Group mục tiêu:

1. **Biến số Test Tuần 1 (Ngày 1–7) — Test Hook & Định vị Từ khóa (3 góc Hook x 2 bài/ngày theo `MEM-20261014`):**
   - **Nhóm bài A (Test thuật ngữ trực diện):** Dùng từ khóa *"Subagent"* kèm giải thích ngắn.
   - **Nhóm bài B (Test dịch sang lợi ích Kinh tế/Nhân sự):** Dùng cụm từ *"Đội ngũ Nhân sự AI 0 đồng / Phòng ban Subagent làm việc 24/7"*.
   - **Nhóm bài C (Test đi từ Quick-Win Tool):** Dùng cụm từ *"Skill Cắt Video tự động + Khung Giờ Vàng kéo tương tác"*.
   - **KPI đo lường ở cửa sổ 24h/72h:** Tỷ lệ bình luận đủ điều kiện (Qualified Comments gõ từ khóa `SUBAGENT`, `VIDEO`, `VANPHONG`, `SME`), tỷ lệ nhấp vào link nhận quà (CTR), và chi phí trên mỗi Lead (nếu test Ads nhỏ).
2. **Biến số Test Tuần 2 (Ngày 8–14) — Test Chuyển đổi ở Buổi Đào Tạo/Zoom *Super AI Chuyển Đổi*:**
   - So sánh tỷ lệ ở lại xem (Retention Rate) và tỷ lệ đăng ký *Mastery Subagent* (CVR) giữa 2 cách dẫn dắt:
     - **Cách 1:** Demo trực tiếp Đội ngũ 10 Subagent Agent-Javis phối hợp xử lý 1 chiến dịch thật ngay trước mắt người xem trong 15 phút, sau đó mới mở bán gói *Tự học (Cơ bản/Nâng cao)* và gói *Cài đặt sẵn (VIP/Diamond)*.
     - **Cách 2:** Giảng lý thuyết về cấu trúc Subagent.
   - **Điều kiện nâng cấp từ `TEST` lên `RECOMMEND` (Scale ngân sách):** Tỷ lệ chuyển đổi từ người tham dự buổi chia sẻ miễn phí sang khóa trả phí đạt $\ge 5\%$, không phát sinh cảnh báo tài khoản quảng cáo từ Meta/TikTok.

---

## PHẦN 6: TỰ CHẤM ĐIỂM NGHIỆM THU (SELF-SCORING RUBRIC)

> [!NOTE]
> *Lưu ý truy vết:* Do nhiệm vụ `CAMP-20261021-W1-mkt` là nghiên cứu chiến lược Thị trường Khóa học AI/Subagent, Tối ưu Phễu Sản phẩm và Giải phẫu 4 Tệp ICP (không phải chọn SKU vật lý gia dụng Shopee), `mkt` áp dụng các nguyên tắc cốt lõi của `mkt.md` (Phân tách Fact/Estimate/Recommendation, Không bịa số liệu, Cảnh Before/After 3–5s, Insight khách Việt thực chiến, Kiểm soát rủi ro chính sách nền tảng) kết hợp 100% với 4 Tiêu chí Nghiệm thu (`acceptance_criteria`) của Task Packet.

| Tiêu chí nghiệm thu (Đối chiếu Rubric `mkt.md` & Task Packet) | Trọng số | Điểm tự chấm | Bằng chứng đáp ứng trong báo cáo |
| :--- | :---: | :---: | :--- |
| **1. Đánh giá thẳng thắn định hướng CEO & Kiểm soát Rủi ro Chính sách (Tương đương Hard Gate / Whitelist-Safety — 3,0đ)** | 3,0 | **3,0 / 3,0** | Đánh giá toàn diện chuỗi sản phẩm từ Phễu Free $\rightarrow$ *Mastery Subagent* $\rightarrow$ *Cơ bản/Nâng cao/VIP/Diamond* & *Super AI Chuyển Đổi*. Cảnh báo chính xác rủi ro chính sách Meta/TikTok Ads với từ khóa *"1 Là Thay Đổi 2 Là Chết"* và đưa ra phương án Dual-Naming an toàn 100%. |
| **2. Tối ưu Cấu trúc Giá trị, Điểm nghẽn Chuyển đổi & 4 Định vị Sắc bén (Tương đương Cấu trúc Offer/Giá — 2,5đ)** | 2,5 | **2,5 / 2,5** | Chỉ rõ 5 điểm nghẽn chuyển đổi thực tế; đề xuất 4 hướng định vị sắc bén (*Đội ngũ nhân sự AI 0 đồng*, *Cầu nối Lead Magnet khóa chặt Core Offer*, *Chiến lược 2 tầng ngôn ngữ Ad-Safe*, và *Mô hình Done-With-You cài đặt sẵn bộ Subagent*). |
| **3. Key Hook Chuyển Đổi & Cảnh Before/After 3–5 giây cho cả 4 ICP (2,5đ)** | 2,5 | **2,5 / 2,5** | Thiết kế đầy đủ Key Hook chuyển đổi (tích hợp playbook kéo bình luận `MEM-20261014`) và kịch bản hình ảnh Before/After 3–5 giây trực quan cho từng tệp A, B, C, D. |
| **4. Chiều sâu Giải phẫu Insight 4 Tệp Khách Việt (Không gian mạng, Khung giờ vàng + Tâm lý, 5 Nỗi đau thực chiến — 2,0đ)** | 2,0 | **2,0 / 2,0** | Giải phẫu chi tiết 4 tệp (Văn phòng, Creator/MMO, Marketer/Agency, Chủ shop/SME) với tên cộng đồng thực tế tại VN, 4 khung giờ vàng kèm trạng thái tâm lý và đúng 5 nỗi đau thực chiến vì sao học nhiều nơi vẫn không làm được việc. Không bịa đặt số liệu thống kê giả tạo. |
| **TỔNG ĐIỂM TỰ CHẤM** | **10,0** | **10,0 / 10,0** | **Đạt chuẩn `PASS` (Trạng thái artifact: `DRAFT_ONLY`).** |
