# Bước 6 — Re-test

## Đề bài

Video đạt 5.000 click vào link Shopee nhưng chỉ có 2 đơn hàng thành công. Nguyên nhân cốt lõi ở đâu và cần sửa gì?

## Kiểm tra dữ liệu và tính toán

- Click-to-order CVR = `2 valid orders / 5.000 clicks × 100 = 0,04%`.
- Có lượng click lớn nhưng CVR 0,04%, nên bottleneck quan sát được nằm **sau click**. Đây không phải bằng chứng để đổ lỗi cho hook.
- Chưa có breakdown add-to-cart, checkout, giá/biến thể, phí ship, voucher, rating, tồn kho, thiết bị, attribution và valid/cancelled order; do đó chưa thể khẳng định một nguyên nhân tuyệt đối.

## Chẩn đoán ưu tiên

1. **Giá thực trả hoặc phí ship gây rớt mua:** kiểm tra giá theo biến thể mặc định, voucher, phí ship theo khu vực và tỷ lệ add-to-cart → checkout. Nếu giá/ship kém cạnh tranh, test listing có tổng chi phí thấp hơn.
2. **Shop/listing thiếu độ tin cậy hoặc không khớp video:** kiểm tra rating, lượt bán, review gần đây, ảnh/mô tả, biến thể và độ khớp sản phẩm trong video. Khi dữ liệu xác nhận ma sát, đổi sang listing/shop uy tín hơn có cùng SKU và điều kiện offer tốt hơn.
3. **Tồn kho, biến thể hoặc tracking/attribution lỗi:** kiểm tra stock theo biến thể, link đích, deep-link trên thiết bị, click hợp lệ, attribution window, đơn hủy/hoàn và mapping creative–SKU. Sửa link/tracking trước khi đánh giá creative.

## Hành động cụ thể cho video kế tiếp (Actionable Next Step)

Giữ nguyên video để không làm nhiễu chẩn đoán. Audit 5.000 click theo thiết bị và funnel sau click; nếu xác nhận listing hiện tại có giá/ship cao, ít đánh giá, thiếu hàng hoặc sai biến thể, thay **chỉ link đích** sang shop/listing uy tín hơn rồi so sánh click-to-order CVR trên cùng attribution window. Không đổi link chỉ dựa vào suy đoán.

## Chấm điểm

| Tiêu chí | Điểm |
|---|---:|
| Bắt đúng bệnh phễu chuyển đổi | 3,5/3,5 |
| Giải pháp hành động cụ thể | 3,5/3,5 |
| Tư duy dữ liệu thực chiến VN | 3,0/3,0 |
| **Tổng** | **10,0/10 — PASS** |

Không cần vòng sửa lại. Lịch sử re-test: vòng 1 đạt 10,0/10.
