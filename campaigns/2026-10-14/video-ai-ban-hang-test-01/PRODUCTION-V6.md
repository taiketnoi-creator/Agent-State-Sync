# Production report — Video AI Bán Hàng V7

## Trạng thái

- Video: `READY_FOR_REVIEW`
- Xuất bản affiliate: `HOLD_MISSING_SKU_LINK`
- File local: `remotion/out/video-ai-ban-hang-aff-hoan-chinh-v7.mp4`

Video đã hoàn chỉnh về hình, voice, nhạc, SFX, kinetic text và CTA. Chưa được đăng kèm giỏ hàng/bình luận affiliate cho tới khi link trỏ đúng mẫu nồi xuất hiện trong video và listing được kiểm tra lại.

## Product truth và claim ledger

| ID | Nội dung | Trạng thái | Cách xử lý |
|---|---|---|---|
| P01 | Nồi điện mini màu kem, núm xoay, nắp rời | `VISUAL_ONLY` | Chỉ mô tả hình đang thấy; chưa gắn SKU/thương hiệu |
| C01 | Dung tích, công suất, lớp chống dính và bảo hành là bốn mục nên kiểm tra | `SELECTION_GUIDE` | Không khẳng định thông số của sản phẩm trong hình |
| C02 | Phù hợp với người tan làm muộn/bếp nhỏ | `CONTEXTUAL_FIT` | Diễn đạt như tình huống minh họa, không cam kết hiệu quả |
| C03 | Giá, dung tích, công suất, bảo hành cụ thể | `BLOCKED_BY_EVIDENCE` | Không xuất hiện trong video |

## Timeline

| Thời gian | Nhịp | Hình/text |
|---|---|---|
| 0–3s | Hook | Tan làm muộn, bếp trọ chật; “Vẫn muốn ăn nóng?” |
| 3–6s | Recognition | Ngại bày cả bếp; “Đói thì làm gì?” |
| 6–9s | Hero | Nồi điện mini xuất hiện rõ |
| 9–13s | Demo | Mở nắp/thao tác sản phẩm; “Cho vào • Xoay núm • Nấu” |
| 13–16s | Objection | “Nhỏ gọn chưa đủ • Đừng vội chốt đơn” |
| 16–19s | Trust | Checklist bốn tiêu chí chọn sản phẩm |
| 19–22s | CTA | “Xem đánh giá • Link ghim bình luận” |

## Asset manifest

| Asset | Loại | Vai trò | Quyền/trạng thái |
|---|---|---|---|
| `01-context.mp4` | generated video | Hook/bối cảnh | Nguồn nội bộ của campaign |
| `02-hero.mp4` | generated video | Hero/CTA | Nguồn nội bộ của campaign |
| `03-demo.mp4` | generated video | Demo/objection | Nguồn nội bộ của campaign |
| `04-payoff.mp4` | generated video | Trust/payoff | Nguồn nội bộ của campaign |
| `google-ad-voice.wav` | Google AI Studio / Gemini TTS | Voice-over chính, speaker Tavi | Nguồn nội bộ của campaign |
| `The-Violins.mp3` | user-supplied | Nhạc nền 10% | Cần người dùng bảo đảm quyền đăng nền tảng |
| `apple-pay-sound.mp3` | user-supplied | SFX 30% | Cần người dùng bảo đảm quyền đăng nền tảng |

## QA

- 1080×1920, 30 fps, 22,02 giây; H.264 + AAC stereo.
- Footage chuyển động chiếm 100%; có bốn clip nguồn độc lập; không dùng slideshow.
- Một Google voice `Tavi`; footage bị mute; không chồng voice và không có đoạn im lặng từ 1 giây.
- Loudness `-15,3 LUFS`; true peak `-3,6 dBTP`.
- Hook, Demo, Trust và CTA đã render frame để kiểm tra safe zone, dấu tiếng Việt và độ tương phản.
- Có disclosure `Minh họa bằng AI • Link có thể tạo hoa hồng`; không có logo/watermark `AI Players`.
- CTA không nêu giá, voucher, tồn kho hoặc thông số chưa xác minh.

## Gate trước khi đăng

1. Gắn đúng link/SKU có hình dáng và biến thể khớp video.
2. Kiểm tra listing, shop, giá, tồn kho, bảo hành và review mới tại thời điểm đăng.
3. Xác nhận quyền sử dụng nhạc và SFX trên nền tảng mục tiêu.
4. Nếu SKU không khớp, thay footage hoặc CTA; không dùng video như bằng chứng thử nghiệm sản phẩm thật.
