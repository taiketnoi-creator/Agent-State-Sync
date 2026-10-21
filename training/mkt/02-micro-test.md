# 02 — Micro-test

## Đề bài

Đề xuất 3 sản phẩm ngách gia dụng mini tiềm năng trên Shopee cho sinh viên/dân văn phòng mùa ẩm mốc/mùa mưa, phù hợp làm video AI giải trí ngắn.

Ngày chốt: 10/10/2026, Asia/Ho_Chi_Minh. Đây là nghiên cứu công khai, không truy cập tài khoản affiliate.

## Tín hiệu mùa vụ

Trung tâm Dự báo KTTV Quốc gia cho biết tháng 10/2026 nhiệt độ cả nước phổ biến cao hơn trung bình nhiều năm; vùng núi Bắc Bộ có lượng mưa cao hơn 5–20%, đồng thời vẫn cần đề phòng bão/áp thấp nhiệt đới. Tín hiệu này hỗ trợ nhu cầu mưa/ẩm theo khu vực, không chứng minh search volume toàn quốc. [Nguồn NCHMF](https://nchmf.gov.vn/kttv/vi-VN/1/ban-tin-du-bao-khi-hau-thoi-han-thang-tren-pham-vi-toan-quoc-thang-10-2026-post54310.html).

## Xếp hạng bảo thủ

Công thức: Nhu cầu 25 + Trend 20 + Commission 20 + Cạnh tranh nghịch đảo 15 + Visual 10 + Seller 10 = 100. Commission không quan sát được nhận 0/20; điểm là phép đánh giá nội bộ, không phải dữ liệu thị trường.

| Hạng | Ngách whitelist | Dữ liệu Shopee quan sát | Điểm | Confidence | Quyết định |
|---|---|---|---:|---|---|
| 1 | Túi nén chân không | Mstar Home Store: 20.000đ, 4,8 sao, 70k+ đã bán; trang được hiển thị là Shopee Mall | 70/100 | Cao cho listing, trung bình cho cơ hội | `RECOMMEND` để test nội dung; commission/search volume `UNKNOWN` |
| 2 | Ô che mưa tự động ngược | Listing tại shop Sơn Liễu: 107.000đ, 4,7 sao, 3k+ đã bán | 65/100 | Trung bình; badge shop `UNKNOWN` | `TEST`, chưa nâng `RECOMMEND` trước khi xác minh badge/tồn kho trong ngày chạy |
| 3 | Máy hút bụi mini cầm tay | 69.000–299.000đ, 4,8 sao, 670 đã bán; listing ghi shop đang tạm nghỉ | 51/100 | Thấp cho listing, trung bình cho ngách | `REJECT` listing hiện tại; giữ ngách để tìm listing thay thế đạt chuẩn |

Nguồn Shopee: [túi nén Mstar](https://shopee.vn/baqs0zyyo_), [ô gấp ngược](https://shopee.vn/shop/166703737), [máy hút bụi mini](https://shopee.vn/M%C3%A1y-H%C3%BAt-B%E1%BB%A5i-C%E1%BA%A7m-Tay-Mini-Kh%C3%B4ng-D%C3%A2y-v%C3%A0-C%C3%B3-D%C3%A2y-Cho-%C3%94-T%C3%B4-v%C3%A0-Gia-%C4%90%C3%ACnh-4.8-205-%C4%90%C3%A1nh-Gi%C3%A1-670-%C4%90%C3%A3-B%C3%A1n-i.1029359098.23772960481).

## Handoff Top 3

### 1. Túi nén chân không

- Insight: phòng trọ/tủ nhỏ, quần áo và chăn chiếm chỗ; người dùng lo đồ bị ẩm/bụi.
- Visual: Before tủ phình bung → ép túi xẹp trong cận cảnh → After tủ đóng gọn trong 3–5 giây.
- Mua ngay: mùa mưa/đổi mùa làm nhu cầu cất đồ rõ hơn; giá quan sát thấp.
- Phản đối: túi rò khí, cần bơm, kích thước không phù hợp. Không claim “chống mốc tuyệt đối”.
- Giả thuyết: visual ép xẹp ASMR tăng giữ chân so với mở đầu bằng lời nói.

### 2. Ô gấp ngược

- Insight: mang ô ướt vào văn phòng/lớp làm nhỏ nước lên sàn, balo và người bên cạnh.
- Visual: Before gấp ô thường nước bắn → After gấp ngược, mặt ướt cuộn vào trong.
- Mua ngay: mưa phát sinh bất tiện tức thì; giá quan sát 107.000đ.
- Phản đối: nặng, cồng kềnh, cơ cấu nhanh hỏng; cần kiểm tra thực tế, không claim “chống gió tuyệt đối”.
- Giả thuyết: tình huống “mang cả cơn mưa vào văn phòng” tạo hook tốt hơn demo trung tính.

### 3. Máy hút bụi mini

- Insight: vụn bánh/bụi bàn phím và khe bàn khó lau nhanh trong giờ làm/học.
- Visual: Before rắc vụn rõ màu → một đường hút → After bề mặt sạch; tránh phóng đại lực hút.
- Mua ngay: gọn, có thể demo tức thì; nhưng listing quan sát đang tạm nghỉ.
- Phản đối: lực hút, tiếng ồn, pin và độ bền; phải kiểm tra đúng SKU.
- Giả thuyết: demo một đường hút trên nền tương phản tăng CTR; chỉ chạy sau khi thay listing đạt chuẩn.

## Sản phẩm hấp dẫn nhưng loại

Máy hút bụi mini được giữ ở cấp **ngách** nhưng listing đang tạm nghỉ nên không được khuyến nghị bán. Đây là ví dụ bắt buộc tách “ngách có tiềm năng” khỏi “listing đủ điều kiện”.

## Test nhỏ 7 ngày

Chỉ test túi nén và ô sau khi xác minh listing. Mỗi ngách 2 video, chỉ thay hook; giữ thời lượng, CTA và khung đăng. KPI: 3-second hold, completion, outbound CTR; guardrail: comment phản ánh sai tính năng/giá; dừng nếu listing hết hàng hoặc giá vượt 300.000đ.
