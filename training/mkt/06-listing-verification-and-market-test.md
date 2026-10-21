# Training thực chiến MKT — Xác minh listing và kiểm chứng thị trường

## Mục tiêu

Sau module này, `mkt` phải có khả năng biến một ngách tiềm năng thành shortlist SKU có bằng chứng, bàn giao được cho `content` mà không bịa giá, badge, hoa hồng, search volume hoặc tình trạng shop.

Kết quả tốt nghiệp: đạt tối thiểu **9,5/10**, không vi phạm hard gate và không có lỗi nghiêm trọng về SKU/listing.

## 1. Phân biệt bốn lớp quyết định

Không gộp các khái niệm sau:

1. **Ngách tiềm năng:** có pain point và khả năng tạo nhiều nội dung.
2. **Sản phẩm tiềm năng:** loại sản phẩm có demo trực quan và phù hợp tệp người xem.
3. **SKU đủ điều kiện test:** đúng biến thể, giá/rating/lượt bán/tồn kho đạt hard gate; dữ liệu thiếu được ghi `UNKNOWN`.
4. **Listing được recommend:** ngoài điều kiện test còn phải xác minh shop/badge, claim và dữ liệu kinh tế cần thiết.

Một ngách tốt không cứu được một listing hết hàng, shop tạm nghỉ hoặc sai SKU. Trước khi có đơn hợp lệ lặp lại, không gọi SKU là `winner`.

## 2. Giao thức xác minh listing sáu bước

### Bước 1 — Khóa đúng SKU

- Ghi tên sản phẩm, phân loại/biến thể định quảng bá và URL trực tiếp.
- Không lấy giá thấp nhất của dải biến thể nếu SKU trong video có giá khác.
- Dải mục tiêu: `39.000–250.000đ`; hard ceiling của đúng SKU: dưới `300.000đ`.

### Bước 2 — Chụp trạng thái biến động

Ghi tại cùng một thời điểm:

- Giá niêm yết và giá sau voucher nếu quan sát được.
- Rating, lượt bán, tồn kho/trạng thái còn bán.
- Tên shop, điểm shop và badge Mall/Yêu Thích/Yêu Thích+ nếu nhìn thấy.
- Ngày giờ chốt và múi giờ `Asia/Ho_Chi_Minh`.

Không quan sát được trường nào thì ghi `UNKNOWN`; không suy luận từ rating hoặc lượt bán để thay badge.

### Bước 3 — Kiểm tra rủi ro mua hàng

- Đọc review xấu gần đây nếu có: sai mô tả, yếu, ồn, rò, nóng, dễ hỏng, đóng gói kém.
- Kiểm tra phí ship, voucher, lựa chọn biến thể và nguy cơ người xem bấm nhầm SKU.
- Ghi ít nhất hai phản đối mua hàng và cách kiểm chứng; không tự viết câu trả lời quảng cáo.

### Bước 4 — Kiểm tra claim và khả năng demo

- Mỗi lợi ích phải gắn với nguồn từ listing/tài liệu hợp lệ hoặc để trạng thái `NEEDS_EVIDENCE`.
- Cấm claim tuyệt đối, claim sức khỏe hoặc claim hiệu năng chưa được chứng minh.
- Phải mô tả được Before/After hiểu trong 3–5 giây mà không dùng ảnh AI làm bằng chứng thật.

### Bước 5 — Kiểm tra kinh tế bảo thủ

- Commission, search volume, CTR và CVR không quan sát được phải ghi `UNKNOWN` hoặc `GIẢ ĐỊNH`.
- Không dùng dữ liệu giả định để nâng listing lên `RECOMMEND`.
- Nếu có dữ liệu, ước tính doanh thu/hoa hồng trên 1.000 view bằng công thức:

```text
1.000 × CTR × CVR sau click × giá SKU × tỷ lệ hoa hồng
```

- Ghi riêng giá trị kỳ vọng, phí ship/voucher và rủi ro huỷ/hoàn.

### Bước 6 — Ra quyết định

- `RECOMMEND`: đủ mọi hard gate, badge/shop được xác minh và bằng chứng phù hợp mức claim.
- `TEST`: đúng whitelist, SKU/giá/rating/lượt bán/tồn kho đạt nhưng còn trường quan trọng `UNKNOWN`.
- `REJECT`: blacklist, sai giá, hết hàng, shop tạm nghỉ, listing không khớp video hoặc claim/rủi ro không kiểm soát được.

## 3. Evidence sheet bắt buộc

Mỗi listing bàn giao phải có:

| Trường | Yêu cầu |
|---|---|
| `product_name` | Tên sản phẩm dễ hiểu |
| `sku_variant` | Đúng biến thể sẽ xuất hiện trong video |
| `listing_url` | URL trực tiếp |
| `checked_at` | Ngày giờ + múi giờ |
| `price_listed` | Giá quan sát của đúng SKU |
| `price_after_voucher` | Giá sau voucher hoặc `UNKNOWN` |
| `rating / sold` | Rating và lượt bán quan sát |
| `stock_status` | Còn bán/hết hàng/shop tạm nghỉ |
| `shop_name / shop_score` | Tên và điểm shop nếu có |
| `shop_badge` | Mall/Yêu Thích/Yêu Thích+ hoặc `UNKNOWN` |
| `commission / search_volume` | Giá trị quan sát hoặc `UNKNOWN` |
| `allowed_claims` | Claim có nguồn |
| `forbidden_or_unverified_claims` | Claim cấm/chưa đủ bằng chứng |
| `negative_review_signals` | Review xấu hoặc rủi ro phổ biến |
| `visual_3_5s` | Before/After có thể hiểu bằng hình |
| `decision` | `RECOMMEND / TEST / REJECT` + lý do |
| `confidence` | `low / medium / high` |

## 4. Product brief bàn giao cho Content

Chỉ bàn giao sau khi evidence sheet hoàn tất. Product brief gồm:

- Buyer và một vấn đề chính.
- Ba lợi ích có nguồn; hai giới hạn/phản đối.
- Một Before/After 3–5 giây.
- Tối thiểu 10 góc nội dung không trùng ý.
- Claim ledger: `APPROVED / NEEDS_EVIDENCE / FORBIDDEN`.
- SKU/link/ngày chốt và quyết định hiện tại.
- Điều kiện phải kiểm tra lại ngay trước khi publish: giá, tồn kho, biến thể và trạng thái shop.

`mkt` không viết thay kịch bản, caption hoặc prompt hình ảnh hoàn chỉnh.

## 5. Test thị trường 7 ngày

Với mỗi SKU ở trạng thái `TEST`:

1. Tạo hai video chỉ thay hook; giữ thời lượng, CTA, offer và lịch đăng.
2. Theo dõi `3-second hold`, completion, outbound CTR, click hợp lệ và comment phản đối.
3. Nếu có dữ liệu sau click, theo dõi add-to-cart, đơn hợp lệ, CVR, huỷ/hoàn và hoa hồng/1.000 view.
4. So sánh ở cửa sổ 24h và 72h với median 10 video gần nhất của chính page.
5. Dừng hoặc kiểm tra lại nếu listing hết hàng, giá đổi mạnh, sai biến thể, comment báo sai tính năng hoặc tỷ lệ huỷ/hoàn tăng.

Không thay nhiều biến trong cùng một vòng test. View cao không tự động biến SKU thành winner.

## 6. Bài tập tốt nghiệp

### Đề bài

Chọn một ngách phù hợp tệp người Việt 18–35 và tìm **5 listing thật**. Hoàn thành:

- Evidence sheet cho cả 5 listing.
- Phân loại `RECOMMEND / TEST / REJECT` có lý do.
- Chọn tối đa 3 SKU đủ điều kiện để bàn giao cho `content`.
- Product brief và claim ledger cho từng SKU được chọn.
- Kế hoạch test 7 ngày, mỗi SKU hai hook và chỉ thay một biến chính.

### Rubric 10 điểm

| Tiêu chí | Điểm tối đa |
|---|---:|
| Đúng SKU, giá, biến thể, tồn kho và timestamp | 2,5 |
| Xác minh shop/badge; mọi dữ liệu thiếu ghi `UNKNOWN` | 2,0 |
| Claim ledger, review xấu và phản đối mua hàng | 1,5 |
| Before/After 3–5 giây và tối thiểu 10 góc content | 1,5 |
| Quyết định `RECOMMEND / TEST / REJECT` tương xứng bằng chứng | 1,5 |
| Kế hoạch test 7 ngày chỉ thay một biến, KPI và stop rule rõ | 1,0 |
| **Tổng** | **10,0** |

Điều kiện PASS: `≥9,5/10` và không có lỗi nghiêm trọng.

### Lỗi nghiêm trọng — tự động FAIL

- Bịa hoặc suy diễn badge, commission, search volume, giá hay tình trạng tồn kho.
- Lấy giá của biến thể rẻ nhất để đại diện SKU khác.
- `RECOMMEND` listing hết hàng/shop tạm nghỉ hoặc thiếu hard gate.
- Dùng hình AI/demo hư cấu làm bằng chứng hiệu quả sản phẩm.
- Gọi SKU là winner khi chưa có đơn hợp lệ lặp lại.

## Checklist trước bàn giao

- [ ] URL và đúng SKU đã được khóa.
- [ ] Giá, rating, lượt bán, tồn kho và shop được chốt cùng thời điểm.
- [ ] Badge thiếu đã ghi `UNKNOWN`.
- [ ] Commission/search volume thiếu không bị ước lượng thành fact.
- [ ] Có claim ledger, review xấu và hai phản đối.
- [ ] Before/After hiểu trong 3–5 giây.
- [ ] Quyết định tương xứng với confidence.
- [ ] Có điều kiện re-check trước publish và stop rule sau publish.

