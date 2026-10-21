# Hướng dẫn sử dụng đội Subagent E-commerce & Affiliate

## 1. Mục đích

Bộ này điều phối quy trình từ nghiên cứu sản phẩm, viết kịch bản, dựng visual/audio, copy đa kênh, phát hành, chăm sóc comment đến đo lường hiệu suất. `mama` là cổng điều phối duy nhất; các agent khác chỉ làm đúng phạm vi được giao.

## 2. Cấu trúc gói

```text
agents/
  mama.md
  mkt.md
  content.md
  edit.md
  voice.md
  content-da-kenh.md
  quan-ly-kenh.md
  cham-soc-kenh.md
  hieu-suat.md
  bo-nao-thu-2.md
training/
knowledge/
  brand_guidelines.md
  bo-nao-thu-2/
HUONG-DAN-SU-DUNG.md
CHANGELOG.md
```

Nếu runtime đọc file ở thư mục gốc, giữ nguyên tên file; nếu runtime yêu cầu `.codex/agents/`, copy hoặc mount thư mục `agents/` theo đúng registry của runtime.

## 3. Việc phải chuẩn bị trước khi chạy

### Brand và dữ liệu

- Đặt bản chính `brand_guidelines.md` vào `knowledge/`.
- Bổ sung brand voice, danh mục whitelist/blacklist, claim cấm, thị trường, timezone và quy tắc disclosure affiliate.
- Chuẩn bị thư mục campaign riêng, không ghi đè source hoặc output chiến dịch khác.

### Runtime và model/tool

- Xác nhận runtime đọc YAML frontmatter và gọi được `mama`.
- Đăng ký model/tool đúng theo registry thực tế; không giả định tên model trong file luôn khả dụng.
- Kiểm tra các tool tối thiểu: `Read`, `Write`, `WebSearch`, `Bash` và cơ chế gọi agent con nếu có.
- Chạy dry-run trước khi cho phép hành động bên ngoài.

### Kết nối nền tảng

Không đặt token/password trong Markdown, git hoặc prompt. Lưu bằng secret manager/environment variables của runtime.

- **Facebook/Meta:** Page ID, quyền đăng Reels, quyền đọc/đăng comment và ghim comment nếu API/connector hỗ trợ; xác nhận Page đúng thương hiệu.
- **YouTube:** channel ID, OAuth scope tối thiểu cho upload/schedule/read analytics; xác nhận channel và timezone.
- **Shopee Affiliate:** affiliate account/shortlink service, link tracking/UTM, quy tắc disclosure và attribution window; test link không chứa secret.
- **Kho asset:** quyền đọc/ghi thư mục video, audio, thumbnail và manifest; không cấp quyền xóa mặc định.

Kết nối chỉ được coi là đạt khi có một **sandbox/dry-run** thành công: tạo được draft metadata, kiểm tra link placeholder và đọc được trạng thái giả lập mà chưa public.

## 4. Quyền mặc định và approval gate

Mặc định mọi agent ở `DRAFT_ONLY`.

- Không tự đăng, schedule, ghim/xóa comment, đổi bio/link, chi tiền, boost bài hoặc thay ngân sách.
- Chỉ chuyển sang `APPROVED_TO_PUBLISH` khi CEO/người được ủy quyền xác nhận rõ campaign, nền tảng, asset version, link và lịch.
- Sau publish phải ghi ops log; không nói “đã đăng/đã ghim” nếu chưa có bằng chứng từ connector.

## 5. Cách bắt đầu một yêu cầu

Gọi `mama` bằng brief tự nhiên:

```text
mama, hãy lập chiến dịch affiliate đồ tiện ích mùa mưa cho sinh viên.
Mục tiêu: 10 video trong 1 tuần trên Facebook Reels và YouTube Shorts.
Ngân sách: chưa chạy paid media.
Trạng thái: draft-only, chưa publish.
```

`mama` phải hỏi lại trước khi giao việc. CEO cần xác nhận tối thiểu:

1. Mục tiêu chính: view, CTR, đơn hàng, commission hay mục tiêu khác?
2. Sản phẩm/thị trường/tệp khách và nền tảng nào trong phạm vi?
3. Kết quả bàn giao cụ thể là gì, số lượng bao nhiêu, deadline nào?
4. Ngân sách, giá trần và ràng buộc thương hiệu/pháp lý?
5. Dữ liệu/asset/link nào đã có, dữ liệu nào còn thiếu?
6. Chỉ tạo draft hay được phép schedule/publish/ghim comment?
7. KPI, attribution window và điều kiện dừng/scale là gì?

Nếu brief đã đủ, `mama` vẫn phải gửi một **Confirmation Summary** ngắn để CEO xác nhận trước khi mở wave đầu tiên.

## 6. Luồng vận hành chuẩn

```text
mama intake & confirmation
→ mkt
→ Gate 1
→ content
→ Gate 2
→ edit
→ voice + content-da-kenh
→ Gate 4
→ quan-ly-kenh
→ cham-soc-kenh
→ CEO approval
→ publish/schedule
→ hieu-suat
```

Mỗi handoff phải có `campaign_id`, `asset_id`, `input_version`, owner, output path, acceptance criteria, deadline và `do_not`.

## 6.1 Bộ não thứ 2 — ký ức dài hạn

`bo-nao-thu-2` trực thuộc `mama`, không phải cổng điều phối độc lập. Dùng để lưu ý tưởng, quyết định, kết quả thử nghiệm và bài học có thể tái sử dụng.

```text
Bộ não thứ 2, ghi nhớ điều này:
Video có hook Before/After trong 2 giây đầu giữ người xem tốt hơn ở nhóm sinh viên.
Ngữ cảnh/nguồn: báo cáo campaign CAMP-20261012-A, mẫu 8 video.
Phạm vi áp dụng: TikTok Việt Nam, nhóm 18–24; cần kiểm chứng thêm.
```

Mỗi ký ức được lưu riêng tại `knowledge/bo-nao-thu-2/memories/`, có trạng thái và nguồn. Chỉ `VALIDATED` được đề xuất cho planning; `UNVERIFIED` chỉ là giả thuyết để test. Không ghi secrets/PII. Mama duyệt mọi việc nâng ký ức thành training hoặc quy tắc toàn đội.

## 7. Checklist trước khi cho chạy thật

- [ ] Brand guideline đúng phiên bản đã được nạp.
- [ ] Model/tool/connector đã được dry-run trên máy hiện tại.
- [ ] Facebook Page và YouTube channel đúng tài khoản.
- [ ] Shopee link/shortlink đã xác minh và có disclosure.
- [ ] Asset/video/audio/copy đã qua quality gate.
- [ ] Caption Facebook không chứa URL; YouTube route đúng description/bio.
- [ ] Pinned comment draft có link đúng version.
- [ ] Lịch dùng timezone Asia/Ho_Chi_Minh, đúng slot đã duyệt.
- [ ] Không có credential/PII trong artifact.
- [ ] CEO đã duyệt trạng thái `APPROVED_TO_PUBLISH`.

## 8. Khi chuyển sang máy khác

1. Copy toàn bộ `agents/`, `training/`, `knowledge/`, hướng dẫn và changelog.
2. Cài/đăng ký runtime, model và tool theo registry máy mới.
3. Nạp secrets bằng secret manager; không copy file token.
4. Chạy `mama` ở chế độ dry-run.
5. Kiểm tra `Confirmation Summary`, một task packet mẫu và một draft calendar trước khi kết nối publish thật.

