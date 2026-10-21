# KHUNG LỘ TRÌNH ĐÀO TẠO TOÀN DIỆN AGENT-JAVIS (CURRICULUM)
*Hệ thống đào tạo chuẩn hóa 4 tầng dành cho Đội Subagent AI Affiliate Video Ngắn*

---

## TỔNG QUAN KIẾN TRÚC ĐÀO TẠO 4 TẦNG

Đội ngũ `Agent-Javis` vận hành theo mô hình phân tầng chặt chẽ, tối ưu hóa triệt để tài nguyên tính toán (Zero-Waste Context Firewall) và đảm bảo chất lượng chuyển đổi cao cho hệ thống tiếp thị liên kết Shopee thông qua video ngắn (Facebook Reels & YouTube Shorts).

```
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 4: CÔNG CỤ THỰC THI & TỰ ĐỘNG HÓA 0-TOKEN                         │
│ 4 Skills + 2 MCP Servers + 4 Local Python Scripts                      │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │
┌───────────────────────────────────┴────────────────────────────────────┐
│ TẦNG 3: 10 HỌC PHẦN CHUYÊN BIỆT THEO VAI TRÒ (5 – 11 BƯỚC)            │
│ mama + 9 Subagents (mkt, content, edit, voice, da-kenh, v.v.)         │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │
┌───────────────────────────────────┴────────────────────────────────────┐
│ TẦNG 2: KHO QUY CHUẨN KHOA HỌC & CÁC KÝ ỨC ĐÃ KIỂM CHỨNG (VALIDATED)     │
│ Brand Guidelines + Playbook Kịch Bản + knowledge/bo-nao-thu-2/INDEX.md │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │
┌───────────────────────────────────┴────────────────────────────────────┐
│ TẦNG 1: 6 TÀI LIỆU THỰC CHIẾN CỐT LÕI (CORE FOUNDATIONAL GUIDES)        │
│ Quy chuẩn nền tảng về sản xuất, phân phối, tương tác & an toàn pháp lý│
└────────────────────────────────────────────────────────────────────────┘
```

---

## TẦNG 1: 6 TÀI LIỆU THỰC CHIẾN CỐT LÕI (CORE FOUNDATIONAL GUIDES)

Bộ 6 tài liệu nền tảng tại thư mục gốc `training/` định hình tư duy thực chiến, cung cấp các quy tắc không thể phá vỡ cho toàn bộ đội ngũ:

| STT | Tài liệu | Đường dẫn | Trọng tâm thực chiến cốt lõi |
| :---: | :--- | :--- | :--- |
| 1 | **Thực hành Video AI Affiliate** | [ai-affiliate-video-practice.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/training/ai-affiliate-video-practice.md) | Sổ cái 7 ngày kiểm thử SKU (`7-day SKU test ledger`); quy trình 5 bước từ sản phẩm thô đến video kiểm chứng; tiêu chí dừng/tiếp tục (`KEEP / ITERATE / STOP`). |
| 2 | **Khởi tạo Facebook Page AI** | [facebook-page-launch.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/training/facebook-page-launch.md) | Bộ khung thiết lập 20 Fanpage vệ tinh; bảo mật tài khoản; tối ưu thông tin Fanpage chuẩn SEO; quy chuẩn ảnh bìa/avatar không vi phạm bản quyền. |
| 3 | **Nuôi dưỡng Cộng đồng Facebook** | [facebook-page-community-nurture.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/training/facebook-page-community-nurture.md) | Kịch bản 5 nhóm phản hồi tự động (`Canned Responses`); nghệ thuật ghim bình luận kèm link Shopee; quy tắc xử lý khiếu nại và bình luận tiêu cực. |
| 4 | **Tạo Video AI Bán Hàng** | [video-ai-ban-hang.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/training/video-ai-ban-hang.md) | Công thức tâm lý học hành vi mua sắm bốc đồng (*impulse buy*); kỹ thuật đẩy cao điểm khao khát; cách lồng ghép sản phẩm tự nhiên vào đời sống thường ngày. |
| 5 | **Quy chuẩn Remotion Explainer Template** | [quy-chuan-remotion-cuongit-template.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/knowledge/quy-chuan-remotion-cuongit-template.md) | Kiến trúc Video-as-Code React + TailwindCSS v4 từ repo remotion-cuongit-template; 6 phân cảnh Hook-Pain-Solution-Workflow-Benefits-CTA, BrandHeader, SubtitleBox 1 dòng, spring physics, đồng bộ frame audio. |
| 6 | **Tình báo Cạnh tranh Sạch** | [competitive-intelligence-clean-operations.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/training/competitive-intelligence-clean-operations.md) | Phương pháp do thám mẫu video thắng của đối thủ mà không copy nguyên bản; phân tích góc tiếp cận sáng tạo; tuân thủ bản quyền và chính sách nền tảng. |

---

## TẦNG 2: KHO QUY CHUẨN THƯƠNG HIỆU & CÁC KÝ ỨC ĐÃ KIỂM CHỨNG (VALIDATED)

### 1. Kho quy chuẩn cốt lõi (`knowledge/`)
- [brand_guidelines.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/knowledge/brand_guidelines.md): Bộ quy trình vận hành thương hiệu & định vị kênh. Khóa cứng trần giá < 300.000đ, Whitelist sản phẩm, Blacklist hàng cấm, và quy tắc cấm URL trên caption Facebook Reels.
- [playbook-kich-ban-video-ngan.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/knowledge/playbook-kich-ban-video-ngan.md): Sổ tay sáng tạo kịch bản 15–35s với 4 nhịp chuyển động (`Hook → Pain → Demo → CTA`).

### 2. Các Ký ức thực chiến `VALIDATED` tại `knowledge/bo-nao-thu-2/INDEX.md`
Tất cả tri thức nền tảng đã qua kiểm chứng bằng số liệu thực tế được lưu trữ dài hạn:

| ID Ký Ức | Tiêu đề | Phân loại | Thẻ từ khóa | Nguồn & Ngữ cảnh |
| :--- | :--- | :---: | :--- | :--- |
| `MEM-20261012-page-network-pilot` | Mạng lưới 20 Page AI Affiliate và thứ tự pilot | `decision` | `ai-affiliate`, `facebook-page`, `pilot` | CEO phê duyệt mô hình mạng lưới Page vệ tinh phân tầng theo ngách. |
| `MEM-20261012-short-video-script-playbook` | Playbook kịch bản video ngắn có giá trị thực | `lesson` | `content`, `script`, `hook`, `storyboard` | Đúc kết công thức 4 nhịp: Hook 3s không chào hỏi, nhịp thoại ngắn gọn ≤ 85 từ. |
| `MEM-20261012-niche-product-research` | Phương pháp nghiên cứu niche và SKU AI Affiliate | `lesson` | `mkt`, `niche`, `sku`, `research` | Tiêu chí lọc sản phẩm: Shopee Mall/Yêu thích, rating ≥ 4.7 sao, > 500 bán, Before/After 3–5s. |
| `MEM-20261013-facebook-page-community-nurture` | Community nurture cho Facebook Page mới | `lesson` | `cham-soc-kenh`, `community`, `nurture` | Quy chuẩn ghim link Shopee tại bình luận đầu tiên trong 5 phút đầu, trực cmt 24h. |
| `MEM-20261014-ai-page-comment-hook-playbook` | Playbook 2 bài/ngày kéo bình luận cho Page AI | `decision` | `ai-players`, `hook`, `comment`, `cta` | Chiến lược đăng bài kéo tương tác vào 2 khung giờ vàng cố định 11h45 và 20h00. |

---

## TẦNG 3: 10 HỌC PHẦN CHUYÊN BIỆT THEO VAI TRÒ (5 – 11 BƯỚC)

Mỗi vị trí trong đội hình sở hữu một chương trình đào tạo độc lập tại `training/<vai-tro>/`, đảm bảo hoàn thành bài kiểm tra và đạt điểm số tốt nghiệp tối thiểu **≥ 9.0/10**:

| Subagent | Vai trò chính | Số bước đào tạo | File quy chuẩn gốc | Model khuyến nghị | Ngưỡng tốt nghiệp |
| :--- | :--- | :---: | :--- | :---: | :---: |
| **`mama`** | Chief of Staff (Tổng quản điều phối) | 5 bước | [mama.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/mama.md) | `inherit` (Gemini 4) | ≥ 9.5 / 10 |
| **`mkt`** | Nghiên cứu thị trường & Săn SKU | 7 bước | [mkt.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/mkt.md) | `inherit` (Gemini 4) | ≥ 9.0 / 10 |
| **`content`** | Biên kịch video ngắn chuyển đổi cao | 5 bước | [content.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/content.md) | `inherit` (Gemini 4) | ≥ 9.0 / 10 |
| **`edit`** | Đạo diễn hình ảnh & Dựng video | 11 bước | [edit.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/edit.md) | `inherit` (Gemini 4) | ≥ 9.0 / 10 |
| **`voice`** | Đạo diễn âm thanh, Voiceover & ASMR | 5 bước | [voice.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/voice.md) | `flash` | ≥ 9.0 / 10 |
| **`content-da-kenh`** | Chuyên viên phân phối đa nền tảng | 5 bước | [content-da-kenh.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/content-da-kenh.md) | `flash` | ≥ 9.0 / 10 |
| **`quan-ly-kenh`** | Lịch phát hành & Quản trị kênh | 5 bước | [quan-ly-kenh.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/quan-ly-kenh.md) | `flash` | ≥ 9.0 / 10 |
| **`cham-soc-kenh`** | Quản trị tương tác & Ghim link affiliate | 5 bước | [cham-soc-kenh.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/cham-soc-kenh.md) | `flash` | ≥ 9.0 / 10 |
| **`hieu-suat`** | Phân tích phễu chuyển đổi & Đề xuất test | 5 bước | [hieu-suat.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/hieu-suat.md) | `flash` | ≥ 9.0 / 10 |
| **`bo-nao-thu-2`** | Quản trị viên tri thức & Zero-PII | 5 bước | [bo-nao-thu-2.md](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/bo-nao-thu-2.md) | `flash` | ≥ 9.5 / 10 |

### Cấu trúc tiêu chuẩn của mỗi học phần (Standard 5-Step Structure):
1. `01-brand-ingestion.md`: Nạp nhận thức thương hiệu, ranh giới quyền hạn (Least Privilege) và quy tắc cấm.
2. `02-micro-test.md`: Bài kiểm tra tình huống thực chiến sát thực tế vận hành.
3. `03-scorecard.md`: Bảng chấm điểm chi tiết theo Rubric 10 điểm cùng thang phạt lỗi âm.
4. `04-error-log.md`: Phân tích lỗi hồi quy và cơ chế khóa cứng (Regression Locks).
5. `05-retest.md`: Bài kiểm tra tái đánh giá sau khắc phục đạt kết quả tuyệt đối.
*(Riêng `mkt` có thêm 2 bước kiểm chứng listing thị trường; `edit` có thêm 6 bước chuyên sâu về Remotion, Motion Prompt và xử lý video dọc).*

---

## TẦNG 4: CÔNG CỤ THỰC THI & TỰ ĐỘNG HÓA 0-TOKEN

Tầng dưới cùng cung cấp năng lực hành động tự động trực tiếp trên máy local mà không tiêu tốn token của LLM:

### 1. 4 Bộ Skills Chuyên Nghiệp
- **`ai-affiliate-page-operator`**: Nghiên cứu thị trường, xây dựng ma trận offer-audience-creative, vận hành Page vệ tinh Facebook.
- **`ai-video-factory`**: Tạo kịch bản chuyển đổi cao, duy trì tính nhất quán của AI Character và render video 9:16 qua FFmpeg.
- **`n8n-automation-bridge`**: Kết nối tự động hóa với webhook n8n, đồng bộ lịch đăng bài và báo cáo qua Telegram.
- **`product-video-editor`**: Cắt ghép take tốt từ source thô, xoay góc 90 độ, chuẩn hóa video dọc 9:16 tắt âm thanh hiện trường.

### 2. 2 MCP Servers Tích Hợp
- **`aff-n8n-sqlite`**: Quản lý cơ sở dữ liệu SQLite (`products`, `brand_personas`, `video_jobs`, `n8n_logs`) và kích hoạt webhook n8n.
- **`facebook-page`**: Tương tác API Facebook Graph: đăng video Reels, ghim bình luận kèm link Shopee, đọc và phản hồi comment.

### 3. Bộ 4 Local Scripts Tự Động Hóa Trong `tools/`
- [extract_video_frames.py](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/tools/extract_video_frames.py): Trích xuất khung hình tự động từ file video để làm tư liệu visual phân tích.
- [validate_script_linter.py](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/tools/validate_script_linter.py): Linter kiểm tra kịch bản 0-token (đếm từ ≤ 85 từ / 30s, chặn câu chào hỏi 3s đầu, kiểm tra 4 nhịp `Hook → Pain → Demo → CTA`).
- [generate_voice_tts.py](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/tools/generate_voice_tts.py): Bộ sinh giọng đọc tự nhiên chuẩn tiếng Việt (Edge-TTS) với tốc độ +12% (1.12x), tự động lọc sạch ký hiệu cue trước khi xuất file `.mp3`.
- [calculate_affiliate_funnel.py](file:///D:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/tools/calculate_affiliate_funnel.py): Phân tích phễu chuyển đổi affiliate (Hook 3s, Hold 50%, CTR, CVR) và tự động kích hoạt **Giao thức chẩn đoán 3 lớp** để đưa ra `Actionable Next Step`.

---

## NGUYÊN TẮC VẬN HÀNH BẢO VỆ TOKEN & CHẤT LƯỢNG

1. **Zero-Waste Context Firewall**: Main Agent (`mama`) chỉ nạp tài liệu điều phối; công việc chuyên môn được ủy quyền cho từng Subagent chạy trong ngữ cảnh riêng biệt.
2. **Handoff qua File & Database**: Kết quả bàn giao được ghi nhận vào `campaigns/` hoặc SQLite; tin nhắn trao đổi giữa các agent chỉ tóm tắt 10–15 dòng kèm đường dẫn artifact.
3. **Phân Tầng Model Tự Động**: Tầng Sáng tạo & Duyệt Gate dùng `Gemini 4` (`Model="inherit"`), Tầng Hậu cần & Vận hành dùng `Model="flash"` để tối ưu 80% chi phí quota.
4. **Quy tắc Kiểm thử Một Biến (Single Variable Test)**: Mỗi lần tối ưu hóa video chỉ thay đổi 1 biến duy nhất (Hook visual, CTA wording hoặc vị trí đặt link) để xác định đúng nguyên nhân tác động.
