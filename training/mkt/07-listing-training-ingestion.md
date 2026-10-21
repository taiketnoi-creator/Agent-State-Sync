# Biên bản học MKT — Xác minh listing và kiểm chứng thị trường

Ngày học: 2026-10-13  
Tài liệu: `training/mkt/06-listing-verification-and-market-test.md`  
Trạng thái: **LEARNED — PENDING_PRACTICAL_TEST**

## Nội dung MKT đã tiếp thu

- Phân biệt rõ bốn cấp: ngách tiềm năng → sản phẩm tiềm năng → SKU đủ điều kiện `TEST` → listing đủ điều kiện `RECOMMEND`.
- Khóa đúng URL và biến thể quảng bá; không lấy giá rẻ nhất của SKU khác để đại diện.
- Mọi dữ liệu biến động phải có nguồn, timestamp và đúng SKU. Không quan sát được phải ghi `UNKNOWN`.
- Chỉ `RECOMMEND` khi vượt toàn bộ hard gate và đã xác minh shop/badge, claim và trạng thái listing.
- Ảnh AI hoặc demo hư cấu chỉ là minh họa, không được dùng làm bằng chứng hiệu quả sản phẩm.
- Chưa có đơn hợp lệ lặp lại thì không gọi SKU là `winner`.
- Chỉ bàn giao cho `content` khi evidence sheet, product brief và claim ledger đã hoàn chỉnh.

## Workflow MKT cam kết áp dụng

1. Nhận whitelist, tệp khách, khoảng giá, nền tảng và ngày chốt.
2. Khóa đúng SKU và URL trực tiếp.
3. Chốt cùng thời điểm: giá, rating, lượt bán, tồn kho, shop và badge.
4. Đọc review xấu; kiểm tra phí ship, voucher và rủi ro chọn nhầm biến thể.
5. Kiểm tra claim, Before/After 3–5 giây và độ hợp lệ của nguồn.
6. Kiểm tra kinh tế bảo thủ; mọi CTR, CVR, commission hoặc search volume chưa quan sát phải ghi `UNKNOWN`/`GIẢ ĐỊNH`.
7. Hoàn thành evidence sheet rồi phân loại `RECOMMEND / TEST / REJECT`.
8. Với SKU đủ điều kiện, bàn giao product brief, 10 góc nội dung và claim ledger cho `content`.
9. SKU `TEST` chạy vòng 7 ngày, mỗi lần chỉ thay một biến; đọc kết quả tại 24h/72h và áp dụng stop rule.

## Lỗi tự động FAIL đã ghi nhớ

- Bịa hoặc suy diễn badge, commission, search volume, giá hay tồn kho.
- Dùng giá biến thể rẻ nhất đại diện cho SKU quảng bá khác.
- `RECOMMEND` listing hết hàng, shop tạm nghỉ hoặc thiếu hard gate.
- Dùng hình AI/demo hư cấu làm proof sản phẩm.
- Gọi SKU là winner khi chưa có đơn hợp lệ lặp lại.

## Cách xử lý các quy tắc song song

- Bài xác minh listing dùng ngưỡng tốt nghiệp **≥9,5/10**, cao hơn ngưỡng chung 9,0/10.
- Test 7 ngày là vòng đầu; chỉ kéo dài đến 14 ngày khi dữ liệu chưa đủ và phải ghi lý do.
- Opportunity Score, Affiliate Product Scorecard và các scorecard niche/SKU bổ trợ nhau; **hard gate luôn có quyền loại trước**, điểm cao không cứu được listing vi phạm.

## Bài thi thực chiến tiếp theo

MKT phải xác minh 5 listing thật trong cùng một ngách, hoàn thành evidence sheet và claim ledger, phân loại có bằng chứng, rồi bàn giao tối đa 3 SKU sạch cho `content`. Kết quả chỉ chuyển sang `PRACTICAL_PASS` khi đạt ≥9,5/10 và không có lỗi tự động FAIL.

