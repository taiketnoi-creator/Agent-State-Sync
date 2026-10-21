# BƯỚC 1: HỒ SƠ NGUYÊN LIỆU ĐẦU VÀO & KIỂM ĐỊNH (STEP 1 INPUT DOSSIER)
> **Chiến dịch:** `2026-10-21 / quat-cam-tay-imi-5000mah`  
> **Link gốc Shopee:** `https://shopee.vn/Quạt-cầm-tay-iMI-điều-chỉnh-120-mức-gió-mạnh-gió-mát-pin-5000mAh-sạc-USB-quạt-mini.-i.1613521954.29791579815`  
> **Shop ID:** `1613521954` | **Item ID:** `29791579815` | **Model ID:** `306574774720`  
> **Image ID gốc:** `sg-11134301-7repa-m8m4ux3y1lw5d9`

---

## 1. Bóc Tách Thông Tin Sản Phẩm Từ Link Shopee

- **Tên sản phẩm chuẩn:** Quạt cầm tay mini phản lực iMI (120 cấp độ gió, Pin 5000mAh, Màn hình LED, Sạc USB Type-C)
- **Ngành hàng (`product_category`):** `electronics_gadget` (Thiết bị điện tử / Gia dụng cá nhân mùa nóng)
- **Kích thước thực tế (`product_size`):** `small handheld` (Nhỏ gọn vừa lòng bàn tay, cao ~16cm, đường kính đầu quạt ~6cm)
- **Đặc điểm nhận diện vật lý (Dùng để khóa `product_desc_en` chống biến dạng):**
  - Thân hình trụ tròn màu **vàng champagne ánh bạc kim loại nhám (matte metallic champagne-silver)**.
  - Đầu quạt dạng **tuốc-bin phản lực tròn**, bên trong có **vòng đèn LED xanh dương (`blue LED ring`)** và tâm tròn màu đen nhám với 5 nan đỡ.
  - Cổ quạt phía trước có **màn hình LED kỹ thuật số hình bầu dục nằm ngang màu đen** hiển thị số **`120`** màu trắng.
  - Ngay dưới màn hình LED là **nút bấm kép hình viên thuốc (`+` / `-`)** cùng màu thân quạt; cạnh trái có khe/công tắc nhỏ màu đen.
- **4 Điểm Bán Hàng Cốt Lõi (USP):**
  1. **Công nghệ lốc xoáy 120 cấp độ gió (`120-speed hurricane technology`):** Gió thổi tập trung cực mạnh, thổi bay tóc và làm mát tức thì dưới trời nắng 38–40 độ.
  2. **Màn hình LED hiển thị thông minh:** Báo chính xác mức gió từ `01` đến `120` và dung lượng pin, chủ động sạc không lo tắt đột ngột.
  3. **Pin lớn `5000mAh` + Sạc USB Type-C:** Dùng liên tục nhiều giờ khi đi học, đi làm, du lịch, xếp hàng ngoài trời hoặc khi mất điện.
  4. **Thiết kế kim loại sang trọng, bỏ gọn túi xách:** Nhỏ mà có võ, cầm đầm tay, không cồng kềnh như quạt truyền thống.
- **Điều cấm nói (`Forbidden Claims`):**
  - Không nói "lạnh như điều hòa 16 độ", không cam kết thời lượng pin ảo quá thực tế (chỉ nói "pin lớn 5000mAh dùng bền bỉ cả buổi/cả ngày tùy mức gió"), không dùng từ tuyệt đối vi phạm chính sách ("tốt nhất thế giới", "rẻ nhất Việt Nam").

---

## 2. Kiểm Định Bộ 3 Ảnh Đầu Vào (Step 1 Input Validation)

| Thành phần | File gốc / File đã xử lý | Kết quả kiểm định Gemini Vision |
| :--- | :--- | :--- |
| **Ảnh gốc từ Shopee** | `inputs/product_shopee_main.jpg` | ⚠️ **Cảnh báo:** Ảnh gốc của Shop có bàn tay cầm, chữ quảng cáo tiếng Anh (`LED air volume digital display...`) và bóng kính `120` phóng to đè lên quạt. Nếu đưa trực tiếp vào AI sẽ bị lỗi dính chữ rác lên video. |
| **1. Ảnh Sản Phẩm Sạch (`Product Ref`)** | `inputs/product_clean_packshot.png` | ✅ **ĐẠT (10/10):** Đã tách bỏ toàn bộ chữ tiếng Anh, bóng kính `120` và bàn tay; giữ nguyên 100% hình khối quạt iMI màu vàng champagne, vòng LED xanh và màn hình `120` trên nền trắng chuẩn Studio. |
| **2. Ảnh Khuôn Mặt MC (`Face Ref`)** | `inputs/creator_face_ref.png` | ✅ **ĐẠT (10/10):** Nữ MC Việt Nam 25 tuổi, góc chính diện rõ nét, ánh sáng tự nhiên, biểu cảm tươi tắn, không đeo kính hay phụ kiện che mặt. |
| **3. Ảnh Dáng Người MC (`Body Ref`)** | `inputs/creator_body_ref.png` | ✅ **ĐẠT (10/10):** Cùng nhân vật Nữ MC, trang phục thanh lịch năng động (áo trắng/kem), phông nền sạch dễ tách ghép. |

---

## 3. Dữ Liệu Đầu Vào Chuẩn Hóa Để Dán Ngay Vào Bước 1 (Google Flow)

### A. Ô "Tên sản phẩm"
```text
Quạt cầm tay mini phản lực iMI 120 mức gió Pin 5000mAh
```

### B. Ô "Kịch bản thô / Thông tin sản phẩm"
```text
- Quạt cầm tay mini phản lực iMI thiết kế vỏ ánh kim màu vàng champagne sang trọng, nhỏ gọn vừa lòng bàn tay.
- Công nghệ lốc xoáy 120 cấp độ gió tùy chỉnh từ gió mát dịu đến gió phản lực cực mạnh thổi bay cái nóng mùa hè.
- Có màn hình LED kỹ thuật số thông minh hiển thị rõ cấp độ gió (tới mức 120) và phần trăm pin.
- Dung lượng pin lớn 5000mAh, sạc cổng USB Type-C tiện lợi qua sạc dự phòng hoặc laptop, mang đi học, đi làm, đi du lịch hay dùng lúc cúp điện đều cực tiện.
- Bảo hành đổi trả uy tín theo chính sách gian hàng.
```

### C. Ô "Điều cấm nói"
```text
Không nói lạnh sâu như điều hòa, không bịa thông số ngoài mô tả, không dùng từ tuyệt đối như số 1 thế giới, 100% vĩnh viễn.
```

### D. Khóa Mô Tả Tiếng Anh Chuẩn Cho Bước 2 (`product_desc_en` & `creator_desc_en`)
- **`product_desc_en`:**
  `A compact handheld turbo jet fan (iMI brand) with a matte metallic champagne-silver cylindrical handle, a circular turbine head featuring an inner glowing blue LED ring and a matte black circular center hub with five spokes, a small black horizontal oval LED display on the upper front neck glowing with white digits "120", and a pill-shaped "+ / -" rocker button directly below the screen. Pocket-sized, about 16cm tall, held comfortably in one hand. Rigid product geometry, zero morphing.`
- **`creator_desc_en`:**
  `A 25-year-old Vietnamese woman with fair natural skin, bright expressive eyes, warm smile, shoulder-length dark brown hair, wearing a smart-casual cream short-sleeve polo top, slim build, energetic TikTok reviewer vibe.`
