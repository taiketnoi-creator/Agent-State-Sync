# Training liên agent — Competitive Intelligence và nghiên cứu niche/SKU sạch

Ngày học: 2026-10-13  
Nguồn: `competitive-intelligence-operations.md`, `niche-product-research.md` thuộc skill `ai-affiliate-page-operator`  
Agent áp dụng: `mkt`, `content`, `hieu-suat`, `mama`  
Trạng thái: **LEARNED — PENDING_PRACTICAL_TEST**

## Mục tiêu

Biến quan sát thị trường và đối thủ thành giả thuyết có thể kiểm tra, tạo creative nguyên bản, đo đến đơn hợp lệ và ra quyết định stop/scale mà không gian lận, sao chép hoặc bịa bằng chứng.

## 1. Ranh giới bắt buộc

### Được phép

- Nghiên cứu nguồn công khai, offer, pain, hook, format, CTA và pattern creative.
- Tự động hóa việc thu thập dữ liệu mà đội có quyền truy cập và báo cáo nội bộ.
- Dùng Creative Intelligence Card, scorecard niche/SKU và experiment ledger.
- Tạo creative AI nguyên bản từ insight/pattern đã quan sát.
- Theo dõi `view → retention → click → order → valid order → valid commission`.

### Tự động FAIL

- Tài khoản giả, cookie/token/session/key trái phép hoặc quay lại sau đình chỉ.
- Bot traffic, follow, comment, review, lead, click hay đơn giả.
- Cookie stuffing, click injection/flooding, cloaking hoặc né kiểm duyệt.
- Spam group/comment/inbox hoặc đăng lặp hàng loạt.
- Clone người nổi tiếng, giọng, mascot, footage, hook nhận diện hoặc creative hoàn chỉnh của người khác.
- Giả trải nghiệm, testimonial, báo chí, chuyên gia hoặc dùng minh họa AI làm proof sản phẩm.

Khi một yêu cầu chạm danh sách cấm, agent phải từ chối phần đó và đề xuất phương án nghiên cứu/test sạch.

## 2. Mô hình giả thuyết bán hàng

Mỗi test là một hàng trong ma trận:

```text
Audience × Pain × Occasion × Offer × Creative × CTA × Channel
```

Mỗi video chỉ thay một biến chính. Mỗi hàng phải có:

```text
test_id, audience, pain, occasion, offer_id, creative_format,
hook, cta, channel, main_variable_changed, expected_signal, stop_condition
```

Luôn tách ba lớp:

- `OBSERVED`: dữ liệu nhìn thấy, có nguồn và ngày.
- `INFERENCE`: giả thuyết rút ra từ quan sát.
- `CONVERSION_EVIDENCE`: click, đơn hợp lệ và hoa hồng quan sát từ page.

Không dùng view, like, số đã bán, ads chạy lâu, Trends tăng hoặc commission cao để kết luận winner.

## 3. Competitive Intelligence 30 mẫu

Mỗi vòng nghiên cứu đầy đủ thu thập:

- 10 video organic.
- 10 TikTok ads/creative.
- 10 Meta ads/creative.

Mỗi mẫu phải điền Creative Intelligence Card:

```text
source_url, observed_at, platform, advertiser/page, product/category,
audience, pain, hook_0_2s, opening_visual, format, main_benefit,
proof_or_demo, objection_handled, cta, first/last_observed,
visible_variants, what_to_learn, what_not_to_copy, confidence
```

Đếm pattern bằng số mẫu, sau đó chuyển thành hypothesis. Không gọi pattern là công thức thắng. Không tải/reup asset khi chưa có quyền.

## 4. Nghiên cứu niche và SKU

Niche phải theo công thức: `nhóm người + bối cảnh sống + chuỗi vấn đề lặp lại`.

- So sánh tối thiểu 3 niche bằng scorecard 35 điểm: vấn đề lặp lại, dễ minh họa, độ sâu SKU, mùa vụ, giá, rủi ro claim và khả năng làm series.
- Ưu tiên pilot từ 28/35 nhưng vẫn phải test.
- Với SKU, so sánh ít nhất 3 listing, đọc tối thiểu 20 review mới và ưu tiên review 1–3 sao.
- Chấm SKU 50 điểm: pain, demo, listing/shop, 10 góc content, economics, rủi ro claim/hoàn.
- Hard gate trong `mkt.md` luôn chạy trước scorecard; điểm cao không cứu listing vi phạm.

Trước dữ liệu chuyển đổi, chỉ gọi SKU là `ứng viên test`.

## 5. Creative nguyên bản

`content` chỉ học cơ chế chú ý, pain, proof, objection và CTA; không paraphrase sát hook hay tái tạo nhận diện đối thủ.

Mỗi SKU phải có 10 góc thực sự khác nhau, ví dụ:

1. Tình huống pain.
2. Demo minh họa.
3. Checklist chọn mua.
4. Ai không nên mua.
5. So sánh lựa chọn.
6. Nhược điểm/phản biện.
7. Setup/cách dùng.
8. Đánh đổi theo giá.
9. Xử lý objection.
10. Trả lời bình luận.

Claim thiếu nguồn trả `BLOCKED_BY_EVIDENCE`. Cảnh AI có khả năng bị hiểu là thật phải gắn disclosure; affiliate disclosure và đúng link/SKU là gate bắt buộc.

## 6. Test 3–3–3 và tracking

- Vòng 1: 3 video thay pain/hook.
- Vòng 2: 3 video thay cách trình bày SKU.
- Vòng 3: 3 video thay CTA trên góc tốt nhất.

Mỗi video chỉ thay một biến chính. Đọc dữ liệu tại cùng cửa sổ 24h/72h và cùng attribution window.

Tracking tối thiểu:

```text
page_id, video_id, test_id, product_id, shop_id,
audience, pain, occasion, format, hook, cta, published_at,
views_24h, views_72h, retention_signal, clicks, orders,
valid_orders, cancelled_orders, returned_orders, commission
```

Không thay null bằng 0. Dữ liệu nhỏ phải ghi `directional only`.

## 7. Unit economics và baseline

```text
CTR = clicks / views
CVR = orders / clicks
Valid order rate = valid_orders / orders
Commission per 1,000 views = commission / views × 1,000
Commission per 100 clicks = commission / clicks × 100
```

Forecast phải ghi `GIẢ ĐỊNH`; khi có dữ liệu thật phải thay CTR, CVR, valid-order rate và refund rate. So sánh mặc định với median 10 video gần nhất của cùng page, ưu tiên cùng cohort.

## 8. Luật chẩn đoán và ra quyết định

- Retention thấp: sửa hook/shot đầu.
- View tốt, click thấp: sửa pain–offer bridge hoặc CTA.
- Click tốt, đơn thấp: audit giá thực trả, phí ship, voucher, review, shop, tồn kho, biến thể, listing và tracking.
- Có đơn nhưng valid-order rate thấp: pause, thay SKU/shop hoặc sửa kỳ vọng/claim.
- Không có tín hiệu sau đủ 9 video: stop SKU và ghi bài học.
- Chỉ scale 5–10 biến thể khi đơn hợp lệ lặp lại qua nhiều video/ngày, commission/1.000 view vượt median, huỷ/hoàn không phá economics, compliance pass và vẫn tạo được creative nguyên bản.

Nhân bản insight, không sao chép creative.

## 9. Phân vai và review độc lập

- `mkt`: niche/SKU scorecard, 30 Creative Intelligence Cards, evidence sheet, product brief, claim ledger và ba hypothesis.
- `content`: 10 hook nguyên bản, 10 góc/SKU, script theo claim đã duyệt và disclosure.
- `hieu-suat`: measurement plan, báo cáo 24h/72h, unit economics, baseline, bottleneck và `STOP / REVISE / CONTINUE / SCALE`.
- `mama`: khóa dependency, chỉ định compliance reviewer và không cho cùng một agent tự nghiên cứu, tự sản xuất rồi tự tuyên bố winner.

## 10. Bài thi thực chiến

1. Chọn và chấm 3 niche.
2. Thu thập 30 Creative Intelligence Cards.
3. Xác minh 5 listing thật; đọc tối thiểu 20 review mới cho mỗi SKU vào vòng sâu.
4. Chọn tối đa 3 SKU sạch; hoàn thành claim ledger và 10 góc/SKU.
5. Lập ba hypothesis và test 3–3–3.
6. Báo cáo 24h/72h và quyết định theo valid orders/economics.

Trạng thái chỉ chuyển sang `PRACTICAL_PASS` khi không có compliance fail, không bịa dữ liệu và quyết định winner/scale dựa trên đơn hợp lệ.

