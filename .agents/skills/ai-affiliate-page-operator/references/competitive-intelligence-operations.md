# Training: Competitive Intelligence và vận hành Affiliate sạch

## Mục lục

1. Mục tiêu và ranh giới
2. Điều đáng học từ đội vận hành “black”
3. Ma trận bán hàng
4. Bộ công cụ theo chức năng
5. Quy trình nghiên cứu đối thủ
6. Quy trình spy → hypothesis → test
7. Tracking và kinh tế
8. Tổ chức đội agent
9. Nhịp vận hành
10. Luật ra quyết định
11. Mẫu bàn giao

## 1. Mục tiêu và ranh giới

Học khả năng vận hành, không học gian lận. Mục tiêu của agent là biến quan sát thị trường thành giả thuyết có thể kiểm tra, tạo creative nguyên bản, đo đơn hợp lệ và bảo vệ tài khoản/page.

### Được phép học và áp dụng

- Nghiên cứu offer và nhu cầu có cấu trúc.
- Phân loại creative theo audience, pain, hook, format và CTA.
- Theo dõi dữ liệu từng video và từng SKU.
- Test một biến chính mỗi lần.
- Tự động hoá thu thập dữ liệu được phép truy cập và báo cáo nội bộ.
- Dừng thử nghiệm yếu, nhân rộng thử nghiệm có đơn hợp lệ.
- Dùng tracker/redirect minh bạch để đo lường khi nền tảng và chương trình affiliate cho phép.

### Không được hướng dẫn hoặc thực hiện

- Tạo/mua tài khoản giả hoặc quay lại sau khi bị đình chỉ.
- Mua, đánh cắp hoặc sử dụng cookie, token, session, tài khoản hay “key” không được cấp phép.
- Bot traffic, click, follow, comment, review, lead, đơn hoặc tương tác giả.
- Cookie stuffing, click flooding/injection hoặc chiếm last-click không tạo giá trị.
- Cloaking, che đích đến, hiển thị nội dung khác cho hệ thống kiểm duyệt.
- Spam group, comment, inbox hoặc đăng lặp hàng loạt.
- Giả trải nghiệm, testimonial, báo chí, chuyên gia hoặc người dùng.
- Clone người nổi tiếng, giọng nói, mascot, footage hoặc creative của bên khác.
- Né chính sách, CAPTCHA, giới hạn truy cập hoặc hệ thống phát hiện gian lận.

Nếu yêu cầu chạm vào danh sách cấm, từ chối phần đó và chuyển sang phương án sạch tương ứng.

## 2. Điều đáng học từ đội vận hành “black”

Không giả định kết quả họ công bố là thật. Screenshot doanh thu có thể bỏ qua chi phí, hoàn hàng, tài khoản chết hoặc attribution bị chiếm.

Trích xuất năm năng lực hợp pháp:

1. **Offer-first:** nghiên cứu nhu cầu và economics trước khi sản xuất.
2. **Creative library:** lưu creative theo cấu trúc, không lưu một đống link rời rạc.
3. **Fast testing:** tạo nhiều giả thuyết nhỏ, không đặt cược vào một video.
4. **Granular tracking:** biết chính xác video, hook, CTA và SKU tạo kết quả.
5. **Stop/scale discipline:** cắt theo dữ liệu; nhân bản insight, không sao chép nguyên creative.

Luôn phân biệt:

- `Quan sát`: dữ liệu thấy được từ nguồn.
- `Suy luận`: giả thuyết dựa trên quan sát.
- `Bằng chứng chuyển đổi`: click, đơn hợp lệ, hoa hồng thực nhận từ dữ liệu của page.

## 3. Ma trận bán hàng

Mô hình mỗi thử nghiệm bằng:

> Audience × Pain × Occasion × Offer × Creative × CTA × Channel

| Trục | Câu hỏi | Ví dụ |
|---|---|---|
| Audience | Ai có khả năng mua? | Sinh viên ở trọ |
| Pain | Vấn đề cụ thể nào? | Giường tầng nóng |
| Occasion | Vì sao mua lúc này? | Đầu mùa nóng |
| Offer | SKU, giá, hoa hồng, shop? | Quạt kẹp bàn 149K |
| Creative | Kể theo format nào? | Sitcom AI, checklist |
| CTA | Một hành động gì? | Kiểm tra độ dày thành giường |
| Channel | Phân phối ở đâu? | Facebook Reels |

Mỗi hàng trong ma trận là một hypothesis. Mỗi video chỉ thay một trục chính để biết nguyên nhân thắng/thua.

### Mẫu hàng thử nghiệm

```text
test_id:
audience:
pain:
occasion:
offer_id:
creative_format:
hook:
cta:
channel:
main_variable_changed:
expected_signal:
stop_condition:
```

## 4. Bộ công cụ theo chức năng

Chọn tool theo câu hỏi cần trả lời, không chọn vì cộng đồng gọi là “tool win”.

| Tầng | Công cụ/nguồn | Mục đích | Không chứng minh được |
|---|---|---|---|
| Demand | Google Trends Việt Nam | Mùa vụ, mức quan tâm tương đối | Doanh số tuyệt đối |
| Creative | TikTok Creative Center | Top Ads, Top Products, keywords, pattern | Lợi nhuận của SKU |
| Competitor | Meta Ad Library | Ads đang chạy, góc và biến thể | ROAS hoặc đơn |
| Product | TikTok Shop, Shopee | Giá, review, câu hỏi, shop, listing | Số bán hiển thị không đủ xác minh winner |
| Market | YouNet ECI, Metric, EcomHeat | Tăng trưởng ngành và thương hiệu | Hiệu quả từng SKU của page |
| Voice of customer | Groups, comments, Q&A | Pain, objection, ngôn ngữ khách | Đại diện toàn thị trường |
| Tracking | Affiliate dashboard + bảng dữ liệu | Click, đơn, huỷ/hoàn, hoa hồng | Attribution ngoài phạm vi nền tảng |
| Production | AI video, voice, caption, asset library | Tạo creative nguyên bản nhanh | Bằng chứng trải nghiệm thật |

Đánh giá tool trả phí theo: nguồn dữ liệu, độ mới, phạm vi Việt Nam, quyền truy cập, export, attribution, bảo mật, điều khoản sử dụng và chi phí. Không mua key crack, tài khoản chia sẻ không rõ nguồn, cookie hoặc session.

Nguồn chính thức tham khảo:

- TikTok Creative Center: https://ads.tiktok.com/resources/help/article/creative-center?redirected=2
- Meta Ad Library: https://www.facebook.com/ads/library/
- Google Trends FAQ: https://support.google.com/trends/answer/4365533?hl=en
- Google Ads — chống né hệ thống/cloaking: https://support.google.com/adspolicy/answer/15938075?hl=en
- Meta Community Guidelines — chống spam/tương tác/review giả: https://www.facebook.com/help/477434105621119?locale=en_GB
- FTC affiliate disclosure: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking

Khi thực thi, tìm và dùng phiên bản chính sách mới nhất.

## 5. Quy trình nghiên cứu đối thủ

Thu thập mẫu từ nguồn công khai và hợp lệ. Không tải/reup asset nếu không có quyền.

### Mẫu Creative Intelligence Card

```text
source_url:
observed_at:
platform:
advertiser/page:
product/category:
audience:
pain:
hook_0_2s:
opening_visual:
format:
main_benefit:
proof_or_demo:
objection_handled:
cta:
first/last observed date if available:
visible variants:
what_to_learn:
what_not_to_copy:
confidence: low / medium / high
```

### Tín hiệu đáng quan sát

- Cùng một offer có nhiều hook/creative.
- Creative xuất hiện qua nhiều lần kiểm tra.
- Vấn đề và đối tượng được nói rõ trong 2 giây đầu.
- Bình luận hỏi giá, kích thước, cách dùng, lựa chọn biến thể hoặc link.
- Nhiều creator/shop độc lập cùng khai thác một pain.

Không kết luận quảng cáo có lời chỉ vì chạy lâu. Đó chỉ là tín hiệu để tạo hypothesis.

### Báo cáo 30 mẫu mỗi vòng

- 10 video organic.
- 10 TikTok ads/creative.
- 10 Meta ads/creative.

Phân loại cả 30 theo cùng schema. Tìm pattern lặp lại, không chọn theo cảm tính.

## 6. Quy trình spy → hypothesis → test

### Bước 1 — Thu thập

Ghi nguồn, ngày quan sát, format, hook, pain, offer và CTA. Không chỉ lưu view/like.

### Bước 2 — Phát hiện pattern

Ví dụ quan sát:

- 12/30 mẫu mở bằng căn phòng bừa.
- 9/30 dùng before/after.
- 7/30 dùng CTA kiểm tra kích thước.
- 6/30 nói một nhược điểm.

Không gọi đây là “công thức thắng”. Chuyển thành hypothesis:

> Tệp phòng trọ có thể phản ứng tốt với pain trực quan và CTA giúp tránh mua sai.

### Bước 3 — Tạo creative nguyên bản

- Dùng nhân vật và bối cảnh AI riêng.
- Viết lời thoại mới.
- Chỉ dùng claim đã xác minh.
- Gắn disclosure AI và affiliate.
- Không giả demo thật khi chỉ là minh hoạ.

### Bước 4 — Test 3–3–3

- 3 video test pain/hook.
- 3 video test cách trình bày SKU.
- 3 video test CTA.

Mỗi video thay một biến chính. Ghi 24h và 72h trong cửa sổ so sánh thống nhất.

### Bước 5 — Đọc phễu

> View → retention → click → đơn → đơn hợp lệ → hoa hồng

Không scale từ view hoặc like khi chưa có tín hiệu gần doanh thu.

## 7. Tracking và kinh tế

Lưu tối thiểu:

```text
page_id
video_id
test_id
product_id
shop_id
audience
pain
occasion
format
hook
cta
published_at
views_24h
views_72h
retention_signal
clicks
orders
valid_orders
cancelled_orders
returned_orders
commission
```

Tính:

```text
CTR = clicks / views
CVR = orders / clicks
Valid order rate = valid_orders / orders
Commission per 1,000 views = commission / views × 1,000
Commission per 100 clicks = commission / clicks × 100
```

Ví dụ giả định:

```text
1.000 views × 2% CTR × 5% CVR × 199.000đ × 10% commission
= 19.900đ commission/1.000 views
```

Nếu valid order rate là 70%, giá trị kỳ vọng còn `13.930đ/1.000 views`. Gắn nhãn `GIẢ ĐỊNH` cho đến khi thay bằng dữ liệu quan sát.

## 8. Tổ chức đội agent

### Market Intelligence Agent

Đầu ra:

- Ba nhu cầu đáng chú ý.
- Ba offer đáng test.
- Nguồn, ngày kiểm tra, scorecard và rủi ro.

### Creative Intelligence Agent

Đầu ra:

- 30 Creative Intelligence Cards.
- Năm pattern lặp lại.
- Mười hook nguyên bản.
- Ba hypothesis có thể test.

### Product Auditor

Đầu ra:

- So sánh ít nhất ba listing.
- Tóm tắt tối thiểu 20 review mới.
- Ba claim đã xác minh và hai giới hạn.
- Rủi ro huỷ/hoàn.

### AI Content Producer

Đầu ra:

- Script, shot list, prompt, caption, CTA, disclosure và asset manifest.

### Performance Analyst

Đầu ra:

- Báo cáo 24h/72h.
- So với median 10 video gần nhất.
- Chẩn đoán bottleneck và quyết định tiếp theo.

### Compliance Reviewer

Đầu ra Pass/Fail:

- Claim và nguồn.
- Disclosure.
- Bản quyền/IP.
- AI impersonation/testimonial.
- Spam/fake activity/cloaking/evasion.

Không để cùng một agent tự nghiên cứu, tự sản xuất và tự kết luận thắng mà không có bước review độc lập.

## 9. Nhịp vận hành

### Hàng ngày

| Thời điểm | Hoạt động |
|---|---|
| Sáng | Thu thập trend, ads, review, giá và thay đổi listing |
| Trưa | Chấm offer, viết hypothesis, duyệt claim |
| Chiều | Tạo 2–4 creative AI nguyên bản |
| Tối | Đăng, phản hồi bình luận, ghi objection |
| Sau 24h | Đọc hook, retention và click |
| Sau 72h | Đọc đơn hợp lệ, huỷ/hoàn và commission |

### Hàng tuần

- Loại thử nghiệm không có tín hiệu sau đủ vòng test.
- Giữ các hypothesis còn cần dữ liệu.
- Nhân 5–10 biến thể cho winner đã xác minh.
- Cập nhật kho creative, scorecard và bài học thất bại.
- Audit compliance và quyền asset.

Không áp dụng máy móc tỷ lệ scale/cut cố định khi lượng dữ liệu nhỏ.

## 10. Luật ra quyết định

So sánh với median 10 video gần nhất của cùng page:

- View/retention thấp: sửa hook hoặc shot đầu.
- View tốt, click thấp: sửa pain–offer bridge hoặc CTA.
- Click tốt, đơn thấp: kiểm tra shop, giá, review, vận chuyển, listing.
- Có đơn, valid order rate thấp: dừng hoặc thay SKU/shop; sửa kỳ vọng.
- Đơn hợp lệ lặp lại và commission/1.000 view vượt median: tạo 5–10 biến thể.
- Không có tín hiệu sau chín video: dừng SKU và ghi bài học.

Chỉ gọi `winner` khi:

1. Có đơn hợp lệ từ nhiều video hoặc nhiều ngày.
2. Commission/1.000 view vượt đường cơ sở của page.
3. Huỷ/hoàn không phá economics.
4. Có thể tiếp tục tạo creative nguyên bản, đúng claim.

## 11. Mẫu bàn giao

### Competitive Intelligence Report

```text
Research window:
Sources and access dates:
Category / audience:
Number of samples:
Observed patterns with counts:
Unverified inferences:
Three testable hypotheses:
Ten original hooks:
Three offers to test:
Policy/IP risks:
Actions for next 72 hours:
```

### Experiment Report

```text
test_id:
matrix row:
main variable changed:
24h and 72h data:
CTR / CVR / valid order rate:
commission per 1,000 views:
comparison to page median:
diagnosis:
decision: stop / revise / continue / scale
next three actions:
```

### Compliance Gate

```text
Authorized data/tool access: PASS/FAIL
No fake accounts/traffic/engagement/orders/reviews: PASS/FAIL
No cookie stuffing/click injection/cloaking: PASS/FAIL
Original or licensed creative: PASS/FAIL
Claims sourced: PASS/FAIL
AI and affiliate disclosure: PASS/FAIL
Correct destination/product link: PASS/FAIL
```

Do not publish, automate, or scale when any compliance gate is `FAIL`.
