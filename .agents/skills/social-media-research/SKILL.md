---
name: social-media-research
description: >-
  Bộ kỹ năng nghiên cứu mạng xã hội thực chiến (tích hợp từ ScrapeCreators/social-media-research-skills) dành cho mkt và content: Săn bài/video viral vượt chuẩn (Outlier Post Finder), Đào bình luận lấy ngôn ngữ khách hàng (Comment Mining), Mổ xẻ kịch bản & Hook 3s từ lời thoại (Transcript Intelligence), và Giải phẫu quảng cáo đối thủ (Ad Library Teardown).
---

# Bộ Kỹ Năng Nghiên Cứu Mạng Xã Hội & Đối Thủ (`social-media-research`)

Skill này được tích hợp và Việt hóa từ kho mã nguồn mở **`ScrapeCreators/social-media-research-skills`**, trang bị cho **`mkt`** và **`content`** 4 quy trình phân tích dữ liệu mạng xã hội dựa trên bằng chứng thực tế (Evidence-backed Social Intelligence), hỗ trợ cả **Chế độ Local 0-Token** (kết hợp `facebook-page` MCP / dữ liệu JSON) và **Chế độ ScrapeCreators API** (nếu cấu hình `SCRAPECREATORS_API_KEY`).

---

## 1. Khi Nào Sử Dụng Skill Này?

- **`mkt` (Nghiên cứu thị trường & Săn SKU):**
  - Tìm các video/bài đăng có hiệu suất đột biến (**Outlier Posts**) so với mức trung vị (median) của kênh đối thủ.
  - Khai thác bình luận thật (**Comment Mining**) để tìm rào cản mua hàng, câu hỏi lặp đi lặp lại, và nỗi đau thực tế của khách hàng (Voice of Customer).
  - Giải phẫu quảng cáo đang chạy trên Meta Ad Library / TikTok (**Ad Library Teardown**) để tìm khoảng trống thị trường (Angle Gap).
- **`content` & `cham-soc-kenh` (Kịch bản & Chốt đơn):**
  - Bóc tách lời thoại video (**Transcript Intelligence**) để lấy nguyên văn câu **Hook 3 giây đầu**, cấu trúc dẫn chuyện và CTA chuyển đổi cao.
  - Chuyển hóa các câu hỏi/phàn nàn phổ biến nhất trong phần bình luận thành kịch bản xử lý từ chối và bộ **5 Canned Responses**.

---

## 2. Bốn Quy Trình Cốt Lõi (Core Research Workflows)

### 2.1. Săn Bài Đăng / Video Đột Biến (`Outlier Post Finder`)
Không đánh giá một video chỉ dựa trên lượt xem thô (vì kênh lớn tự nhiên có nhiều view hơn kênh nhỏ). Bắt buộc tính **Độ bứt phá so với mức nền (Baseline Lift)** của chính kênh đó:
1. Thu thập tối thiểu `10–20` bài đăng/video gần nhất của kênh.
2. Tính **Trung vị (`Median`)** của lượt xem (`median_views`) và tương tác (`median_engagement`) — dùng `median` thay vì `mean` để không bị 1 bài siêu viral làm lệch chuẩn.
3. Chấm điểm độ đột biến (`Lift Score`):
   $$\text{View Lift} = \frac{\text{Post Views}}{\text{Median Views}}, \quad \text{Engagement Lift} = \frac{\text{Post Engagement}}{\text{Median Engagement}}$$
   - **🔥 Huge Outlier ($\ge 5.0\times$ baseline):** Công thức Hook + Chủ đề đại thắng, ưu tiên mổ xẻ ngay.
   - **⚡ Strong Outlier ($2.0\times - 4.9\times$ baseline):** Góc tiếp cận tốt, đáng đưa vào Swipe File.
   - **📈 Mild Outlier ($1.5\times - 1.9\times$ baseline):** Tín hiệu khả quan.

### 2.2. Đào Bình Luận Lấy Ngôn Ngữ Khách Hàng (`Comment Mining`)
Làm sạch bình luận rác/spam và phân loại bình luận thật vào **6 nhóm tín hiệu mua hàng**:
1. **`Buying Intent` (Tín hiệu chốt đơn):** Hỏi giá, xin link, hỏi phí ship, hỏi combo (*"xin link", "giá sao shop", "mua ở đâu"*).
2. **`Objections` (Rào cản / Nghi ngờ):** Sợ tốn điện, sợ hàng giả, nghi ngờ độ bền, ký túc xá cấm dùng (*"ký túc xá dùng có nhảy át không", "dùng mấy bữa có hỏng không"*).
3. **`Pain Points / Complaints` (Nỗi đau thực tế):** Phàn nàn về giải pháp cũ hoặc sản phẩm đối thủ (*"loại cũ dính đáy nồi chùi muốn xỉu"*).
4. **`Questions` (Thắc mắc tính năng):** Hỏi kích thước, dung tích, bảo hành, cách vệ sinh.
5. **`Praise / Proof` (Khen ngợi thực tế):** Điểm khách đã mua thích nhất (dùng làm Demo Proof ở giây `10–23s`).
6. **`Exact Customer Language` (Từ lóng / Cụm từ đắt giá):** Giữ nguyên văn cách khách hàng gọi tên vấn đề để đưa vào câu Hook 3s và Pinned Comment.

### 2.3. Mổ Xẻ Lời Thoại Video (`Transcript Intelligence`)
Khi có lời thoại (transcript / phụ đề `.srt`) của các video Outlier, bóc tách thành **6 lát cắt chuẩn**:
- **`[00-03s]` Exact Hook:** Câu mở đầu nguyên văn (Pattern Interrupt / Câu hỏi xoáy nỗi đau / Cảnh báo).
- **`[03-10s]` Pain & Setup:** Tình huống đồng cảm hoặc bối cảnh sử dụng (ví dụ: phòng trọ, ký túc xá, bàn làm việc).
- **`[10-23s]` Core Claim & Visual Proof:** Lợi ích cốt lõi và cảnh chứng minh Before/After.
- **`[23-30s]` Payoff & CTA:** Lời kêu gọi hành động và lý do phải bấm vào bình luận ghim / giỏ hàng ngay.

### 2.4. Giải Phẫu Quảng Cáo Đối Thủ (`Ad Library Teardown`)
Khi kiểm tra quảng cáo của đối thủ trên Meta Ad Library hoặc TikTok Creative Center:
- Không khẳng định một quảng cáo là "ra đơn khủng" chỉ vì nó đang bật; hãy tìm **các quảng cáo được chạy lặp lại nhiều biến thể hoặc duy trì dài ngày (Repeated / Long-running Ads)**.
- Gom cụm thông điệp theo: `Pain Point` $\rightarrow$ `Offer` $\rightarrow$ `Visual Concept` $\rightarrow$ Đề xuất **3 góc test mới (Gap Angles)** mà đối thủ đang bỏ trống.

---

## 3. Công Cụ Phân Tích Tự Động Local (`social_research_analyzer.py`)

Sử dụng script Python tích hợp sẵn để tự động chấm điểm Outlier, phân loại bình luận tiếng Việt/Anh và bóc tách cấu trúc Transcript mà không tốn token:

```powershell
# 1. Chấm điểm Outlier Posts từ file JSON dữ liệu bài đăng
python ".agents/skills/social-media-research/scripts/social_research_analyzer.py" --mode outlier --input "output/research/posts_sample.json"

# 2. Đào bình luận (Comment Mining) phân loại Buying Intent / Objections / Pain Points
python ".agents/skills/social-media-research/scripts/social_research_analyzer.py" --mode comments --input "output/research/comments_sample.json"

# 3. Mổ xẻ lời thoại (Transcript Intelligence) tách Hook 3s & kiểm tra nhịp kịch bản
python ".agents/skills/social-media-research/scripts/social_research_analyzer.py" --mode transcript --input "output/research/transcript_sample.txt"
```

> **Tích hợp API (Tùy chọn):** Nếu trong `.env` có khai báo `SCRAPECREATORS_API_KEY`, script có thể gọi trực tiếp các endpoint của ScrapeCreators (`/v3/tiktok/profile/videos`, `/v1/tiktok/video/comments`, `/v1/facebook/adLibrary/search/ads`) để kéo dữ liệu live trước khi phân tích.
