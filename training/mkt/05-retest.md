# 05 — Re-test sau cập nhật prompt

## Đề bài

Đề xuất 3 sản phẩm ngách cho dân văn phòng mùa nắng nóng/mùa hè.

Ngày chốt listing: 10/10/2026, Asia/Ho_Chi_Minh. “Mùa hè” là ngữ cảnh test; không tuyên bố đây là xu hướng tuần hiện tại. Commission và search volume đều `UNKNOWN` vì không có phiên affiliate.

## Kết quả

| Hạng | Ngách whitelist | Listing quan sát | Hard gate | Visual 3–5 giây | Điểm bảo thủ | Quyết định |
|---|---|---|---|---|---:|---|
| 1 | Quạt tích điện mini | 150.000đ; 4,7 sao; 2k+ đã bán; shop 4,9 | Giá/rating/lượt bán đạt; badge `UNKNOWN` | Before nhân vật quạt giấy, tóc bết → After bật quạt, dải giấy/tóc chuyển động | 68/100 | `TEST` chờ xác minh badge và commission |
| 2 | Bình nước thể thao có vạch giờ nhắc uống | 69.000đ; 4,9 sao; 10k+ đã bán | Giá/rating/lượt bán đạt; badge `UNKNOWN` | Before nhiều vạch giờ chưa uống → timelapse uống theo vạch → After bình cạn | 67/100 | `TEST` chờ xác minh badge và vật liệu đúng SKU |
| 3 | Khay làm đá thông minh nhấn nút | 56.000đ; 4,8 sao; 2k+ đã bán; shop 4,8 | Giá/rating/lượt bán đạt; badge `UNKNOWN` | Before vặn khay, đá rơi tung → After nhấn nút, đá rơi gọn vào hộp | 66/100 | `TEST` chờ xác minh badge và commission |

Nguồn Shopee: [quạt mini SmartGood](https://shopee.vn/quattichdienmini_smartgood?tab=5), [bình nước có vạch giờ](https://shopee.vn/thucuc18.6), [khay đá nhấn nút](https://shopee.vn/ts_mart_gdtm).

## Handoff ngắn cho Scriptwriter

- **Quạt mini:** pain point nóng lúc mất điện/chỗ ngồi bí; hook visual “quạt hồ sơ đến bay deadline”; phản đối cần kiểm tra tiếng ồn, pin, lực gió; không dùng “mát tức thì” như fact nếu chưa test.
- **Bình nước:** pain point quên uống khi họp/chạy deadline; hook visual các mốc giờ “đuổi theo” nhân vật; phản đối cồng kềnh/rò nước; không claim sức khỏe.
- **Khay đá:** pain point bẻ khay làm đá văng khắp bếp; hook slapstick rồi chuyển sang nút nhấn; phản đối chiếm tủ/lấy đá không trơn; không claim vật liệu an toàn nếu chưa có chứng từ.

## Kiểm tra tái phạm

- Không có listing hết hàng/tạm nghỉ trong shortlist quan sát.
- Không suy diễn badge: cả ba ghi `UNKNOWN` và chỉ `TEST`.
- Không bịa commission/search volume; thành phần commission nhận 0 điểm.
- Không dùng dải giá “từ” để che SKU vượt trần.
- Cả ba đúng whitelist, dưới 300.000đ, ≥4,7 sao, >500 lượt bán và có Before/After 3–5 giây.

## Tự chấm lại theo rubric chính thức

| Tiêu chí chính thức | Tối đa | Điểm | Nhận xét |
|---|---:|---:|---|
| Whitelist/Blacklist | 3,0 | 3,0 | Quạt mini, bình nước nhắc uống và khay đá đều đúng whitelist; không chạm blacklist |
| Giá và shop | 2,5 | 2,0 | Cả ba trong 39.000–250.000đ, ≥4,7 sao và >500 lượt bán; chưa xác minh badge Mall/Yêu Thích nên không chấm trọn |
| Before/After | 2,5 | 2,5 | Mỗi sản phẩm giải quyết một bất tiện rõ trong 3–5 giây và dễ tạo visual AI |
| Insight khách Việt | 2,0 | 2,0 | Nóng tại bàn làm việc, quên uống khi chạy deadline và lấy đá văng là pain point cụ thể của dân văn phòng Việt |
| **Tổng chính thức** | **10,0** | **9,5 — PASS** | Không tái phạm lỗi vòng đầu |

## Điểm lịch sử

Điểm **9,6/10** theo rubric cũ chỉ để truy vết. Điểm tốt nghiệp có hiệu lực là **9,5/10 theo rubric chính thức**.

Phần 0,5 điểm chưa đạt tuyệt đối do badge Mall/Yêu Thích chưa được quan sát trong dữ liệu công khai. Agent xử lý đúng bằng cách giữ trạng thái `TEST`, không bịa badge và không `RECOMMEND` quá mức.
