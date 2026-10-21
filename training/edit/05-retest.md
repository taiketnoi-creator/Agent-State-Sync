# Bước 6 — Re-test: Giá đỡ điện thoại xoay 360 độ

## Đề bài

Tạo prompt AI video cho phân cảnh cận cảnh chiếc điện thoại gắn trên giá đỡ hợp kim nhôm xoay 360 độ trên mặt bàn làm việc hiện đại.

- **Cỡ cảnh:** Extreme macro close-up chuyển sang hero close-up.
- **Góc máy:** Low three-quarter macro angle; slow counter-orbit.
- **Rigid lock:** `Rigid product geometry, preserved scale, stable macro lighting, natural hand kinematics, zero morphing`.

## Motion Prompt

```text
[00-02s] Extreme macro close-up of a generic unbranded smartphone secured upright in a brushed aluminum 360-degree rotating stand on a modern dark-walnut desk. Low three-quarter camera angle, 100 mm macro lens look, shallow depth of field, soft cool key light and a narrow rim light producing crisp metallic reflections along the hinge and base.
[02-05s] An anonymous hand gently turns the stand clockwise through 180 degrees while the phone remains centered, upright, and firmly seated. The camera performs a slow counter-orbit at constant distance, revealing the stable circular base and brushed aluminum texture without changing focal length.
[05-07s] The hand leaves frame and the stand completes the rotation to 360 degrees, settling without bounce or wobble. Keep the phone dimensions, hinge geometry, and reflections consistent throughout.
[07-09s] Hold a clean hero close-up as the metal edge catches one crisp highlight and the blank phone screen remains free of text, logos, and interface elements.
Rigid product geometry, preserved scale, stable macro lighting, natural hand kinematics, zero morphing. No warped phone, no bending aluminum, no duplicated hinge, no floating base, no changing screen ratio, no extra fingers, no unstable reflections, no logo, no readable text, no celebrity likeness, no copyrighted character.
```

## Chấm điểm

| Tiêu chí | Điểm tối đa | Kết quả | Điểm |
|---|---:|---|---:|
| Ngôn ngữ điện ảnh; prompt 100% tiếng Anh | 3.0 | Có macro shot, góc máy, counter-orbit, lens, DOF và crisp metallic reflections; không lẫn tiếng Việt. | 3.0 |
| Timeline chi tiết | 2.5 | Bốn mốc liên tiếp `[00-02s]` đến `[07-09s]`. | 2.5 |
| Zero morphing/product fidelity | 2.5 | Có exact rigid lock và negative constraints theo vật thể. | 2.5 |
| Deepfake/bản quyền | 2.0 | Không người nổi tiếng, logo hoặc nhân vật bản quyền. | 2.0 |
| **Tổng** | **10.0** | **PASS** | **10.0** |

**Số vòng sửa:** `0` — bản đầu đạt chuẩn.  
**Kết quả sau cập nhật prompt:** `10.0/10 — PASS`.
