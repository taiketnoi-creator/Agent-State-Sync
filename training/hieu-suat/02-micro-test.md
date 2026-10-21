# Bước 2 — Micro-test

## Đề bài

Video đạt 100.000 view nhưng chỉ có 5 click vào link Shopee và 0 đơn hàng. Phân tích 3 nguyên nhân khả dĩ nhất và đề xuất phương án khắc phục ngay cho video tiếp theo.

## Kiểm tra dữ liệu và tính toán

- View-to-click CTR = `5 clicks / 100.000 views × 100 = 0,005%`.
- Click-to-order CVR = `0 valid orders / 5 clicks × 100 = 0%`.
- Mẫu sau click chỉ có 5 clicks, quá nhỏ để kết luận đáng tin cậy rằng landing page có CVR kém. Kết luận CVR hiện tại chỉ mang tính `directional only`.
- Chưa có 3-second view rate, retention curve, completion rate, CTA timestamp, click source, giá thực trả, phí ship, rating, tồn kho và tracking breakdown.

## Ba nguyên nhân ưu tiên

### 1. View cao nhưng traffic có thể không đủ chất lượng mua

- **Bằng chứng cần kiểm tra:** retention curve tại 3s/10s/điểm demo; tỷ lệ người còn xem tại thời điểm CTA; nguồn traffic và completion rate.
- **Lý do:** hook giải trí có thể kéo view rộng nhưng pain point/demo không đủ khớp nhu cầu mua của người Việt 18–35.
- **Hành động:** đưa pain point và Before/After vào sớm hơn, giữ nguyên CTA và listing để cô lập biến.
- **KPI xác nhận:** retention tại thời điểm demo và tỷ lệ người còn xem lúc CTA tăng; sau đó CTR tăng trên cùng attribution window.

### 2. CTA hoặc khả năng nhìn thấy link quá yếu

- **Bằng chứng cần kiểm tra:** CTA timestamp, wording, số người còn xem lúc CTA, vị trí link đúng chuẩn nền tảng, khả năng mở link và click event.
- **Lý do:** CTR 0,005% cho thấy điểm nghẽn quan sát được nằm trước hoặc tại click; CTA mơ hồ hay link khó thấy là giả thuyết ưu tiên.
- **Hành động:** thử một CTA duy nhất nêu lợi ích cụ thể và chỉ rõ vị trí link; với Facebook hướng tới comment ghim, với YouTube hướng tới mô tả/bio.
- **KPI xác nhận:** view-to-click CTR của phiên bản mới so với control, cùng sản phẩm, cùng khung giờ và attribution window.

### 3. Offer/listing có thể không đủ hấp dẫn, nhưng chưa đủ click để kết luận

- **Bằng chứng cần kiểm tra:** giá thực trả, voucher, phí ship, rating/lượt bán, review gần đây, tồn kho/biến thể, độ khớp video–listing và tracking.
- **Lý do:** mức giá cao, phí ship hoặc shop kém uy tín có thể làm người xem không click hoặc không mua; tuy nhiên chỉ 5 clicks nên chưa thể quy 0 đơn chắc chắn cho landing page.
- **Hành động:** kiểm tra listing và tracking trước; chỉ test listing/shop khác khi phát hiện ma sát rõ, không thay cùng lúc với CTA trong một A/B test.
- **KPI xác nhận:** outbound click hợp lệ, add-to-cart nếu có và click-to-order CVR trên cỡ mẫu đủ lớn.

## Hành động cụ thể cho video kế tiếp (Actionable Next Step)

Giữ nguyên sản phẩm, listing và phần lớn creative; chỉ thay CTA thành một câu nêu lợi ích + chỉ đúng vị trí link, đặt khi retention còn đủ cao. So sánh view-to-click CTR với control trên cùng điều kiện; đồng thời kiểm tra tracking và listing ngoài bài test để loại trừ lỗi kỹ thuật.
