# Kiểm toán Hiệu Suất — 4 Page, 30/10/2026

Trạng thái: **READY_FOR_REVIEW — kiểm toán snapshot hoàn tất; phễu chuyển đổi chưa đủ bằng chứng**.
Owner: Hiệu Suất (Analytics). Căn cứ: `hieu-suat.md`, `quan-ly-kenh.md:63–64`, quy tắc null và đối soát nguồn.
Đây là báo cáo hiệu chỉnh mới; giữ nguyên dữ liệu nguồn và báo cáo lịch sử. Không thay đổi job production, lịch đăng, attribution hay chiến dịch.

## 1. Nguồn và phạm vi xác minh

- Snapshot: `campaigns/daily-reports/.metrics_cache.json`, timestamp `1793325627.0573406`, tương ứng **09:00:27 ngày 30/10/2026, UTC+7**. Hash SHA-256 nằm trong `analytics-audit-v1.json` cùng thư mục.
- Đối chiếu `campaigns/daily-reports/report-2026-10-30.md`, mã `tools/mama_daily_9am_report.py` và milestone `milestone_boot-or-9am_0900.md`.
- Chỉ tái tính từ snapshot tại máy; không phải lần gọi Meta/Shopee mới. Công cụ Meta Insights/Shopee/SQLite MCP nêu trong vai trò không hiện có trong phiên này.
- `aff_system.db` tại gốc repository: **0 byte, không có bảng** khi mở chỉ đọc. Không có bằng chứng đơn/hoa hồng trong DB này; không suy ra toàn hệ thống không có đơn. Không đọc kho credential hay hồ sơ trình duyệt.
- Snapshot không lưu danh sách published post ID, comment ID, tác giả ID, phân trang, metric Insights hoặc giao dịch Shopee. Vì thế số bài/likes bên dưới là **số được báo cáo**, chưa được tái xác minh từ API thô.

## 2. Sửa định mức: 15 bài/ngày

Theo quy chuẩn hiện hành: AI Players **6 ảnh + 3 Reels = 9**; mỗi page bán hàng **2 ảnh**, tổng **9 + 3 × 2 = 15**. Không cộng bài scheduled vào published.

| Page | Bài được báo cáo trong 24h | Định mức | Tỷ lệ hiệu chỉnh | Scheduled được lấy mẫu | Likes lifetime trên mẫu bài |
|---|---:|---:|---:|---:|---:|
| AI Players | 7 | 9 | 77,78% | 25 | 2 / 25 bài |
| Phòng Trọ Hết Cứu | 0 | 2 | 0% | 0 | 38 / 14 bài |
| Ký Túc Xá Có Biến | 0 | 2 | 0% | 0 | 32 / 12 bài |
| Hội Deadline | 0 | 2 | 0% | 0 | 35 / 13 bài |
| Tổng | 7 | 15 | **46,67%** | 25 | 107 / 64 bài |

`Tỷ lệ khối lượng = tổng published / tổng định mức × 100`. Báo cáo cũ dùng 7/14 = 50%; hiệu chỉnh giảm **3,33 điểm phần trăm**. Còn thiếu 8 bài so với định mức số lượng, chưa xác nhận đủ cơ cấu ảnh/Reels. Không lấy trung bình đơn giản tỷ lệ của bốn page.

Cửa sổ snapshot là **29/10 09:00:27 → 30/10 09:00:27 UTC+7**. Đây là tiến độ 24h lăn, không phải tiến độ cả ngày 30/10. KPI ngày phải dùng `[00:00, 00:00 ngày kế tiếp)` theo UTC+7, cuối ngày mới chốt mẫu số 15; giữa ngày có thể so với số slot đã đến hạn, ghi nhãn riêng.

25 bài chờ đăng là mẫu hàng đợi, không chứng minh toàn bộ lịch đã đủ: API chỉ lấy `limit=25` và không phân trang. Danh sách này bắt đầu từ **31/10 08:30**, không chứng minh có coverage cho phần còn lại ngày 30/10. Ba page bán hàng báo queue 0, phù hợp milestone khóa vì thiếu gói SKU mới; không dùng lại bài cũ để lấp KPI.

## 3. Bình luận khách, bình luận Page và ghim

**Thu hồi tính xác thực của nhãn “2 Cmt khách” tại AI Players.** Hai mẫu trong `user_comments_samples` đều mang tên **AI Players - Người chơi hệ AI**. Đây là bằng chứng nhãn sai/đáng ngờ, chưa đủ comment ID/from.id để chốt chính xác tổng khách thật. Giá trị hiệu chỉnh cho cả bốn page: **khách đã xác minh = null**, không thay bằng 0.

Lỗi ở bộ tạo báo cáo hiện tại:

- `fetch_page_metrics` coi một comment có emoji/link hoặc comment đầu của Page là ghim, sau đó lấy tổng comment trừ tối đa 1. Các phản hồi tiếp theo của Page bị tính sang khách.
- Nếu tổng comment ≥1, code tự nhận đã có ghim dù không xác định tác giả hay trạng thái ghim. Vì vậy **7/7 ghim chưa được chứng minh**; `0/0` của ba page bán hàng phải là **N/A**, không đánh dấu đạt.
- Like/share/comment cộng trên toàn bộ tối đa 25 bài/page được lấy mẫu; không lọc riêng bài 24h. Tương tác này là lifetime trên mẫu bài, cũng không phải số tương tác phát sinh trong 24h.

Quy tắc thay thế trong `tools/audit_four_page_metrics.py::classify_comments`:

1. Khử trùng theo comment ID, phân loại bằng `from.id`. Mọi ID của **cả 4 Page** là `page`; nhân sự/tài khoản vận hành trong danh sách được xác nhận là `internal`.
2. ID còn lại chỉ là `audience_candidate`; cần lọc spam và nội dung liên quan trước khi gọi là khách đủ điều kiện. Tên hiển thị/link/emoji không xác nhận danh tính.
3. Thiếu ID comment/tác giả → `unknown`; thiếu trang dữ liệu hoặc reply → ghi coverage chưa đủ. Không suy ra phần chưa tải là khách.
4. Tách comment gốc/reply, unique người bình luận và số comment; không cộng lẫn số người với lượt.
5. Page đăng comment chứa đúng link chỉ xác minh **link hiện diện**. Ghim cần bằng chứng trạng thái ghim từ nguồn hỗ trợ hoặc kiểm tra giao diện có mốc thời gian. Không suy ra ghim chỉ từ vị trí trả về.

## 4. Bằng chứng chuyển đổi và dữ liệu còn thiếu

| Chỉ số | AI Players | Phòng Trọ | Ký Túc Xá | Hội Deadline | Bằng chứng cần bổ sung |
|---|---|---|---|---|---|
| Starts / View 3s / retention | null | N/A với ảnh | N/A với ảnh | N/A với ảnh | Insights từng video, tên metric và định nghĩa mẫu số, mốc 24h/72h |
| Comment khách đã xác minh | null | null | null | null | Comment ID/from.id, reply, thời gian, đầy đủ phân trang, danh sách actor nội bộ |
| Outbound link clicks | null | null | null | null | Export Insights đúng loại click ra link; tách click mở ảnh, profile và all-clicks |
| Click Shopee theo sub_id | null | null | null | null | Export affiliate, ngày/múi giờ, sub_id và định nghĩa click/unique click |
| Đơn hợp lệ / hủy / hoàn / từ chối | null | null | null | null | Export giao dịch, khóa order/line khử trùng, trạng thái, SKU, thời điểm chốt |
| Hoa hồng chờ / duyệt / đã trả | null | null | null | null | Export đối soát, trạng thái commission, điều chỉnh và tiền tệ VND |

AI Players dẫn tài liệu/cộng đồng: cần đo lead vào phễu riêng. Chỉ dùng đơn Shopee cho AI Players khi có chiến dịch affiliate thực tế và mapping đã xác nhận; không gán doanh thu của ba page bán hàng sang AI Players. Không dùng likes làm bằng chứng click/đơn.

Gói bằng chứng tối thiểu, mỗi bản export có `source_file`, SHA-256, `extracted_at`, `period_start/end`, timezone và định nghĩa metric:

- Meta: `page_id, post_id, published_at, format, metric_name, metric_value, metric_period`, trạng thái phân trang, mốc tuổi bài 24h/72h. ID bình luận dùng nội bộ; báo cáo chỉ xuất tổng, không thông tin cá nhân.
- Mapping: `page_id → post_id → creative_id → campaign_id → sub_id → SKU/listing`, route link và thời gian hiệu lực. Bổ sung cửa sổ attribution, quy tắc gán đơn/click, độ trễ và đơn ngoài cửa sổ.
- Shopee: click theo sub_id; giao dịch tối thiểu có `order_key, line_key, status, ordered_at, validated_at, sub_id, sku, GMV, pending/approved/paid_commission, currency`. Khóa giao dịch cần ẩn danh; không thu PII người mua.
- Đối soát: dedup line trước, đếm distinct order cho số đơn; tổng commission theo line/trạng thái, tránh cộng lại snapshot của cùng giao dịch. Tách GMV, hoa hồng, payout nền tảng, chi phí quảng cáo và sản xuất.

Meta outbound clicks và Shopee clicks là hai nguồn khác nhau: báo chênh lệch và coverage, không ép chúng bằng nhau. Chỉ tính tỷ lệ khi cohort, cửa sổ đo và mapping tương thích.

## 5. Công thức và giới hạn

- Hook 3s = `video_3s_views / video_starts × 100`; nếu nguồn chỉ có impressions thì đặt tên riêng `3s views / impressions`, không so trộn. Ảnh: N/A.
- Comment rate = `qualified_external_comments / 3s_views × 100`; là tỷ lệ lượt trên lượt. Unique commenter rate phải dùng mẫu số unique viewer tương thích.
- View-to-click = `attributed_outbound_clicks / views × 100`; CTR theo impression phải ghi tên khác. Click từ comment cần tracking riêng; không lấy click tất cả trên bài thay thế.
- CVR = `distinct valid orders / Shopee attributed clicks × 100`; valid-order rate = `valid orders / total distinct orders × 100`.
- EPC = `approved commission / Shopee attributed clicks`; commission/100 clicks = `100 × EPC`; commission/1.000 views = `approved commission / views × 1000`.
- Thiếu tử/mẫu hoặc mẫu số 0 → **null/N/A**. Commission đã trả báo riêng; chưa có cost thì không tính ROI/ROAS.
- View → comment → click → đơn là khung chẩn đoán. Không có tracking cấp cohort thì không khẳng định người click đã bình luận; không nhân các tỷ lệ như một chuỗi chuyển đổi cá nhân.

## 6. Quyết định và hành động

**Cả 4 page: ITERATE phần đo lường; chưa đủ cơ sở KEEP/STOP creative hoặc SKU.** Không có quyết định tắt/scale, không suy đoán hook yếu từ việc thiếu dữ liệu.

- Hook/retention: chưa có curve và View 3s, nên chưa xác định điểm rơi. Owner Quản Lý Kênh cung cấp metric cùng tuổi bài; Analytics đối chiếu median 10 video gần nhất cùng page/cohort, ghi directional nếu thiếu baseline/mẫu.
- CTA/link: chưa có click/link coverage và xác nhận ghim. Owner Quản Lý Kênh + Chăm Sóc Kênh cung cấp dữ liệu tác giả comment, trạng thái link/ghim, route tracking. Không dùng tương tác nội bộ chứng minh nhu cầu khách.
- Giá/listing/shop: chưa có đơn và thông tin giá thực trả, ship, voucher, tồn kho/biến thể, rating/review tại thời điểm test. Cần MKT cung cấp khi có click hợp lệ; chưa quy lỗi cho listing hoặc video.

Đọc creative/click tại 24h, đơn và economics tại 72h kèm trạng thái đối soát còn trễ. KEEP khi chất lượng nội dung và conversion được xác nhận trên cohort tương thích; ITERATE một biến khi bottleneck có bằng chứng; STOP chỉ khi kết quả đủ tin cậy hoặc có lỗi compliance/listing đã xác minh. Không dùng một ngưỡng tỷ lệ tùy ý để tuyên bố winner.

### Hành động cụ thể cho video kế tiếp (Actionable Next Step)

Ưu tiên hoàn thiện tracking cho **một video AI Players mới được duyệt**: giữ nội dung, CTA và slot đã duyệt; bổ sung mapping post/link và mốc Insights 24h/72h. KPI chính là tỷ lệ trường bắt buộc có bằng chứng **100%**; guardrail không lẫn Page/internal vào khách và không gán đơn không có sub_id. Chưa thử đồng thời hook và CTA. Khi đủ baseline mới thiết kế test một biến hook 0–3s, chốt cỡ mẫu từ baseline/MDE trước khi chạy; thiếu mẫu thì kéo dài, không chốt winner.

## 7. Bàn giao kỹ thuật và kiểm tra

- `analytics-audit-v1.json`: số liệu hiệu chỉnh, hash nguồn và null rõ ràng. Công cụ chỉ đọc snapshot và chỉ tạo output mới, không ghi đè.
- Tái chạy: `python -B tools/audit_four_page_metrics.py --cache campaigns/daily-reports/.metrics_cache.json --output campaigns/daily-reports/2026-10-30/analytics-audit-v2.json`.
- Kiểm thử: `python -B -m unittest discover -s tools -p test_audit_four_page_metrics.py -v` — **4/4 đạt** (định mức, null, danh tính/bình luận trùng, page trùng).
- **Tồn tại cần xử lý ở job production:** `tools/mama_daily_9am_report.py` vẫn dùng định mức 8, logic trừ một comment, tự suy ra ghim và phần trăm ghim hardcode 100%. Không lấy báo cáo cũ làm số đã kiểm toán. Theo blast radius của `hieu-suat.md`, nhiệm vụ này tạo báo cáo/công cụ mới, không sửa job của owner khác.
- Git pull bị từ chối ghi `.git/FETCH_HEAD`; `.git` chỉ đọc trong phiên. Không thể commit/push từ đây. Giữ nguyên mọi thay đổi sẵn có và không chạy job báo cáo gốc vì job có tác dụng phụ dọn/xóa media.

Tự chấm: **9,0/10 về chất lượng kiểm toán và khả năng truy vết**, không phải chứng nhận hiệu suất kinh doanh. Hạn chế chính: chưa truy cập raw Meta/Shopee, chưa đối soát được comment/đơn/hoa hồng và chưa sửa bộ tạo báo cáo production.
