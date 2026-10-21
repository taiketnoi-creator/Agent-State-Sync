# Playbook video dọc: dark tech, motion text và screen demo

## Nguồn phân tích và phạm vi

Playbook này được rút ra từ video tham chiếu dọc 720×1280, 30 fps, dài khoảng 76,6 giây. Đây là hướng dẫn **tái tạo ngôn ngữ hình ảnh**, không khẳng định công cụ gốc, font chính xác hay sao chép nội dung/nhận diện thương hiệu của video tham chiếu.

Phù hợp với video giải thích công cụ AI, giới thiệu tính năng, tutorial ngắn hoặc công nghệ/design. Dựng bằng Remotion, CSS/SVG và asset hợp lệ.

## Ý tưởng bố cục chủ đạo

Canvas được chia thành ba vùng cố định:

```text
0–15%     Brand/watermark nhỏ, ít gây chú ý
15–60%    Thông điệp chính: headline, card, demo hoặc danh sách
60–100%  Caption đồng bộ voice; phần đáy chừa vùng an toàn
```

Mỗi cảnh chỉ có **một điểm nhìn chính**. Chữ lớn, card hoặc screenshot không cạnh tranh với caption. Khoảng trống rộng là một phần của phong cách, không phải vùng cần lấp đầy.

## Hệ thiết kế ở canvas 720×1280

### Background

- Nền gần đen: `#0B0D0F` đến `#111416`.
- Gradient lạnh rất nhẹ: tím than/xanh đen ở vùng rìa; không có texture nổi rõ.
- Màu chữ chính: trắng 90–96% opacity.
- Màu chữ phụ: xám `#A4A4A8` đến `#B9B9BD`.
- Màu nhấn theo ngữ cảnh: đỏ san hô cho vấn đề (`#FF4D55`), cyan cho từ khoá/động từ (`#00C7E8`), tím cho tiêu đề tính năng (`#A855F7`), vàng cam cho tên sản phẩm (`#F7B733`).
- Một cảnh chỉ nên có một màu nhấn chính; cyan có thể dùng như màu karaoke xuyên suốt.

### Vùng an toàn và vị trí

| Thành phần | X/Y tương đối | Kích cỡ gợi ý | Quy tắc |
|---|---|---:|---|
| Logo/watermark | giữa trục X, Y 58–112 px | cao 30–42 px | opacity thấp, luôn cùng vị trí |
| Eyebrow/chapter | giữa hoặc trái, Y 300–420 px | 20–26 px | viết ngắn, có chấm/bullet nhấn |
| Headline | giữa khung, Y 400–600 px | 40–58 px | bold 700–800, 1–3 dòng |
| Line divider | giữa khung, dưới headline 24–34 px | rộng 56–160 px | mảnh 1–2 px, màu accent thấp |
| Screenshot/card | từ X=48 đến 672, Y 300–900 px | rộng tối đa 624 px | bo 16–20 px, không che caption |
| Danh sách tính năng | trái X=48–72, Y 480–850 px | title 28–34 px; body 18–24 px | canh trái, spacing 28–40 px |
| Caption karaoke | giữa, Y 1030–1160 px | 25–33 px | tối đa 2 dòng, chừa mép 48 px |

Các số là mốc tái tạo, không phải pixel bất biến. Khi scale sang 1080×1920, nhân mọi giá trị với 1,5.

### Font

- Sans hình học đậm, bo tròn vừa phải: **Be Vietnam Pro** là lựa chọn chuẩn tiếng Việt; có thể dùng Inter nếu render dấu tốt.
- Headline/list title: 700–800; body/caption: 500–700.
- Dòng lệnh: JetBrains Mono hoặc IBM Plex Mono, 24–30 px.
- Tăng line-height cho tiếng Việt: headline 1.12–1.20; caption 1.2–1.3.
- Không dùng chữ viền, gradient chữ phức tạp hoặc quá ba weight trong một cảnh.

## Mẫu layout cần dùng

### A. Hook vấn đề

```text
[logo nhỏ, top-center]

      [câu hỏi 2 dòng, trắng; 1 cụm đỏ]
                 [từ khoá vấn đề rất lớn, đỏ glow]
      [mô tả hậu quả xám, underline ngắn]

             [caption karaoke đáy]
```

- Câu hỏi: 28–34 px, tối đa 2 dòng.
- Từ khoá: 58–72 px, bold 800, glow đỏ mềm 20–32 px.
- Chỉ từ khoá chính được rất lớn; phần còn lại phải nhường cấp bậc.

### B. Claim/giới thiệu sản phẩm

```text
[logo]

       [eyebrow nhỏ, màu accent]
       [headline lớn 1–2 dòng; từ khoá đổi màu]
       [divider ngắn]

                  [caption karaoke]
```

Nên để nhiều khoảng trống dưới headline; điều này tạo cảm giác premium và dẫn mắt xuống caption.

### C. Demo website/sản phẩm

```text
[logo]

       [screenshot website bo góc, gần full chiều rộng]

               [caption karaoke, đáy]
```

- Screenshot thật là nhân vật chính. Không đặt headline dài chồng lên nó.
- Dùng crop/zoom nhẹ để người xem đọc được vùng quan trọng; không kéo méo tỉ lệ.

### D. Danh sách “N tính năng”

```text
[logo]

[headline tím lớn]
[divider chạy ngang mảnh]

[icon] [tên tính năng đậm]
       [mô tả phụ xám]
... lặp lại 3–5 lần

[code command card, nếu có]

              [caption karaoke]
```

- Headline 40–48 px, canh trái X≈48–72.
- Mỗi item có icon 36–44 px, nền icon bo 10–12 px; text bắt đầu sau icon 14–18 px.
- Tên item 26–32 px bold; mô tả 18–22 px, xám.
- Chỉ reveal từng item; không hiện toàn bộ ngay từ đầu.

## Motion sử dụng

Motion trong phong cách này không phải là “hiệu ứng cho đẹp”. Nó phân phối sự chú ý theo nhịp voice.

### 1. Reveal theo lớp (layered reveal)

Thứ tự tiêu chuẩn: logo đã có sẵn/opacity thấp → eyebrow → headline → keyword lớn → mô tả/divider → caption. Mỗi lớp cách nhau 4–10 frame.

Gợi ý Remotion (30 fps):

```ts
const p = spring({frame: frame - delay, fps: 30, config: {damping: 18, stiffness: 130}});
const opacity = interpolate(p, [0, 1], [0, 1]);
const y = interpolate(p, [0, 1], [18, 0]);
const scale = interpolate(p, [0, 1], [0.97, 1]);
```

Áp dụng cho headline/card. Không dùng `spring` nảy quá mạnh; cảm giác cần chắc, mềm và có chủ đích.

### 2. Word highlight / karaoke caption

Caption phía đáy hiện theo từng cụm hoặc từng từ đồng bộ voice. Từ đang đọc chuyển từ xám 40–55% opacity sang trắng/cyan, không cần thay vị trí.

```text
trước khi đọc: xám mờ
đang đọc: cyan hoặc trắng sáng, opacity 100%
đã đọc: trắng 80–90% hoặc xám sáng
```

Đây là **motion text quan trọng nhất** của video: nó dẫn mắt xuống caption nhưng không kéo người xem khỏi visual chính.

Yêu cầu dữ liệu: cần timestamp theo từng từ/cụm từ từ TTS hoặc transcript alignment. Không đoán timing bằng cách chia đều mọi chữ.

### 3. Keyword emphasis

Từ khoá trong headline đổi màu theo nghĩa: đỏ = vấn đề; cyan = hành động/kết quả; tím = nhóm tính năng; vàng = tên sản phẩm. Nó xuất hiện sau phần chữ còn lại khoảng 3–6 frame, có scale `0.92 → 1` và glow nhẹ nếu là từ cảnh báo/vấn đề.

Không animate mọi từ. Một cảnh tối đa 1–2 keyword emphasis.

### 4. Stagger list

Danh sách tính năng hiện từng item theo chiều trên xuống. Mỗi item trễ 5–8 frame:

```text
icon fade + scale 0.90 → 1
title fade + x 14 → 0
body fade sau title 2–4 frame
```

Danh sách giữ yên sau khi hiện. Không trượt liên tục hoặc bounce vì sẽ làm khó đọc.

### 5. Screenshot/camera motion

- Screenshot vào bằng fade + scale `0.96 → 1` trong 10–14 frame.
- Trong thời gian giữ cảnh, có thể zoom rất chậm `1.00 → 1.025` hoặc pan tối đa 16–24 px.
- Khi chuyển vùng giao diện, hard cut sạch hoặc crossfade 6–10 frame. Tránh zoom nhanh gây cảm giác chóng mặt.

### 6. Divider và glow

- Divider có thể reveal theo `scaleX: 0 → 1`, transform origin ở giữa hoặc trái, trong 6–10 frame.
- Glow tăng opacity từ 0 lên 30–45%; không pulse liên tục.

## Chuyển cảnh giữa scene

- Ưu tiên fade-to-dark/crossfade 6–12 frame.
- Nếu đổi chủ đề, cho scene cũ giảm opacity và scale xuống `0.985`, scene mới vào `1.015 → 1`.
- Demo website có thể hard cut để tạo nhịp “bằng chứng thật”.
- Không dùng spin, cube, glitch, whip-pan, lens flare hay wipe màu toàn màn hình trừ khi brief yêu cầu chủ đích.

## Nhịp dựng

- Một claim/slide text: 2,5–5 giây.
- Cảnh demo: 3–8 giây tuỳ lượng thông tin cần đọc.
- Danh sách 5 mục: 7–12 giây, mỗi item có thời gian đọc tối thiểu 0,7–1,0 giây sau khi xuất hiện.
- Caption và visual phải có ít nhất một thay đổi đáng chú ý mỗi 1–2,5 giây; thay đổi có thể là từ karaoke mới, item mới, zoom nhẹ hoặc screenshot mới.

## Quy tắc sản xuất cho agent

1. Chọn một layout A/B/C/D cho mỗi scene trước khi viết motion.
2. Lập hierarchy text: headline → supporting text → caption. Không để caption to hơn headline.
3. Chỉ dùng accent cho từ mang nghĩa; không tô nhiều màu để trang trí.
4. Lưu `wordTimings` hoặc `phraseTimings` cùng scene để render karaoke chính xác.
5. Screenshot/demo phải là ảnh thật có quyền dùng và đã che token, email, dữ liệu cá nhân.
6. Xem preview ở tốc độ bình thường trên màn hình điện thoại. Nếu phải dừng mới đọc được, giảm chữ hoặc tăng thời lượng.

## Mẫu dữ liệu scene

```json
{
  "type": "feature-list",
  "durationInFrames": 270,
  "accent": "purple",
  "headline": "5 TÍNH NĂNG ĐỘT PHÁ",
  "items": [
    {"icon": "palette", "title": "Khoá nhất quán màu sắc", "body": "xuyên suốt toàn trang"},
    {"icon": "ban", "title": "Bằng lệnh cấm nghiêm ngặt", "body": "không còn SVG thủ công lộn xộn"}
  ],
  "caption": "Bộ khung chuyển động chuẩn, mượt như lụa.",
  "phraseTimings": [
    {"text": "Bộ khung", "start": 166, "end": 188, "accent": false},
    {"text": "chuyển động chuẩn", "start": 189, "end": 225, "accent": true},
    {"text": "mượt như lụa", "start": 226, "end": 265, "accent": false}
  ]
}
```

## Checklist trước render

- [ ] Canvas 720×1280 hoặc 1080×1920, 30 fps.
- [ ] Logo ở cùng vùng top-center, không gây nhiễu.
- [ ] Mỗi scene có một điểm nhìn chính và đủ khoảng trống.
- [ ] Text có thứ bậc; headline, body và caption không cạnh tranh.
- [ ] Caption không vượt vùng an toàn đáy và timing khớp TTS.
- [ ] Motion dùng fade/translate/scale nhẹ; không có bounce hoặc transition phô trương.
- [ ] List reveal lần lượt; screenshot không méo, không chứa dữ liệu nhạy cảm.
- [ ] Màu accent được dùng có ý nghĩa và độ tương phản đạt mức dễ đọc.
- [ ] Đã xem preview trên kích thước điện thoại trước khi xuất bản.
