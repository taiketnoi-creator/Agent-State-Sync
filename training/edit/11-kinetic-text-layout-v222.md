# Training 11 — Kinetic text layout từ `v222.mp4`

## Phạm vi học

Chỉ học cách bố trí, phối màu và chuyển động của text. Không sao chép nhân vật, nội dung nói, bối cảnh, âm thanh hoặc nhận diện của video nguồn.

Nguồn phân tích: `C:\Users\guicci\Downloads\v222.mp4`, dài khoảng 14,37 giây, khung dọc 9:16. Frame đã được kiểm tra tại các mốc từ 0,00 đến 14,33 giây.

## 1. Hệ thống phân cấp chữ

- Mỗi cụm chỉ có một thông điệp chính, thường dài 2–4 từ.
- Từ khóa chính dùng sans-serif condensed, viết hoa, nét rất đậm; tham chiếu nhóm font Anton/Impact/Druk Condensed, không bắt buộc đúng font nguồn.
- Dòng dẫn hoặc số năm dùng display serif tương phản cao, nghiêng nhẹ; tham chiếu nhóm Didot/Bodoni Italic.
- Có thể dùng chữ outline cỡ lớn ở lớp sau để tạo chiều sâu, nhưng độ tương phản thấp hơn dòng chính.
- Không dùng caption dài chạy liên tục. Text xuất hiện như title card ngắn, bám theo nhịp nói.

## 2. Bố cục 9:16

- Cụm chữ đặt ở lower-middle: tâm cụm nằm khoảng 58–72% chiều cao khung.
- Chiều rộng cụm chính khoảng 72–86% khung; tối đa 2 dòng cho headline.
- Căn giữa; line-height chặt khoảng 0,82–0,95 lần cỡ chữ để khối chữ liền và mạnh.
- Giữ safe zone tối thiểu 7% hai cạnh, 9% đáy và tránh che mắt/miệng nhân vật.
- Có thể chồng hai họ font: serif mảnh ở phía trên hoặc xuyên nhẹ qua lớp sau; sans đậm nằm trước và là lớp đọc chính.
- Khi nhân vật/đạo cụ chiếm giữa khung, chữ dịch xuống vùng ngực/bụng, không đặt cố định một vị trí cho mọi shot.

## 3. Màu sắc và độ nổi

- Màu nhấn chính: lime điện gần `#D9FF00` đến `#E6FF18`.
- Màu phụ: trắng `#FFFFFF`; đỏ bão hòa dùng rất ít cho icon/shape chuyển ý.
- Chữ lime dùng outer glow mềm cùng tông, không viền đen dày; glow chỉ đủ tách khỏi nền tối.
- Chữ trắng có shadow/glow xám nhẹ. Chữ outline dùng stroke trắng mảnh, fill trong suốt hoặc xám rất tối.
- Mỗi card chỉ ưu tiên một màu nhấn; tránh đổi màu từng từ kiểu karaoke.

## 4. Nhịp xuất hiện và transition

- Reveal theo tầng, không bật cả cụm cùng lúc: dòng 1 vào trước, dòng 2 theo sau khoảng 4–10 frame.
- Chuyển động vào ưu tiên: opacity `0→1`, scale `0,88→1,04→1`, và translateY `24–50px→0` trong khoảng 8–14 frame ở 30 fps.
- Từ khóa có thể overshoot nhẹ rồi settle; không bounce nhiều lần.
- Dòng serif dùng fade + trượt ngang/đứng nhẹ, chậm hơn sans đậm để tạo tương phản nhịp.
- Outline nền xuất hiện sau headline 2–5 frame, opacity thấp; không cạnh tranh với lớp chính.
- Khi thay thông điệp, cụm cũ mờ/scale xuống trong 6–10 frame; shot mới có thể dùng motion blur hoặc whip/zoom rất ngắn để che cut.
- Có khoảng thở không text giữa các cụm; không phủ chữ xuyên toàn bộ video.
- Icon/shape chuyển ý được phép xoay hoặc morph đơn giản, nhưng không thay thế khả năng đọc của headline.

## 5. Mẫu animation đề xuất

```text
Headline line 1: 0–10f, opacity 0→1, y 42→0, scale 0.90→1.03→1.00
Headline line 2: 5–15f, opacity 0→1, y 34→0, scale 0.94→1.00
Serif kicker: 0–14f, opacity 0→1, x -20→0
Outline echo: 8–18f, opacity 0→0.35, y 18→0
Hold: tối thiểu 24–40f tùy độ dài cụm
Exit: 6–10f, opacity 1→0, scale 1→0.96, y 0→-18
```

## 6. Những điều không được học theo máy móc

- Không dùng cùng một cỡ chữ khổng lồ cho mọi câu.
- Không để glow quá mạnh làm mất nét chữ hoặc bệt dấu tiếng Việt.
- Không chồng serif và sans nếu nội dung dài hoặc nền đã phức tạp.
- Không đặt chữ lên mặt, mắt, miệng hoặc chi tiết sản phẩm cần chứng minh.
- Không sao chép nguyên văn title, icon, font thương mại hoặc hiệu ứng nhận diện của video nguồn.

## 7. Checklist QA

- [ ] Một frame chỉ có một điểm đọc chính.
- [ ] Đọc được khi thu nhỏ còn 360×640.
- [ ] Dấu tiếng Việt không chạm/cắt do line-height quá chặt.
- [ ] Lime/white đủ tương phản với nền ở mọi shot.
- [ ] Reveal có phân tầng 4–10 frame, không bật đồng loạt.
- [ ] Text giữ đủ lâu để đọc xong trước khi thoát.
- [ ] Có frame không text để hình và lời thoại được thở.
- [ ] Không che khuôn mặt hoặc sản phẩm trọng tâm.

## Trạng thái

`VALIDATED_REFERENCE` — dùng làm tham chiếu cho agent Edit khi brief yêu cầu kinetic title, không tự thay thế brand kit hiện hành của AI Players.
