# Video AI Bán Hàng — Test 05

Bản dựng Remotion sửa lại voice và toàn bộ ngôn ngữ motion text theo nhịp direct-response.

## Voice

- Voice mới tạo trực tiếp bằng Google AI Studio, model Gemini TTS, speaker `Tavi`.
- Ba block cùng một speaker, phong cách quảng cáo nhanh, sáng và giàu năng lượng.
- File dùng trong bản dựng: `public/audio/google-ad-voice.wav`, dài 20,8 giây.
- Không dùng gTTS; audio native của footage được mute để không chồng giọng.
- Toàn bộ footage là B-roll/thao tác không có nhân vật mấp máy nói, tránh lệch lip-sync với Google voice-over.

## Hình và text

- Tổng thời lượng 22 giây, bốn shot hard-cut; mỗi shot có zoom nhẹ và flash cut.
- Text chính đặt ở vùng giữa khung hình, tối đa hai dòng, không dùng caption dạng đoạn văn.
- Motion text dùng punch-in, snap scale, directional wipe và micro-shake trong 4–12 frame.
- Cấu trúc: Hook → thao tác → objection → bốn tiêu chí → CTA.
- Không chèn `AI Players`, logo dự án hoặc watermark.

## Render

```powershell
node node_modules/@remotion/cli/remotion-cli.js render src/remotion-entry.tsx VideoAiBanHang out/video-ai-ban-hang-test-05-google-voice-kinetic.mp4
```

`node_modules/` không được lưu lâu dài trong workspace. Khi cần render lại, cài dependency từ `pnpm-lock.yaml`; giữ `out/video-ai-ban-hang-test-05-google-voice-kinetic.mp4` làm bản thành phẩm hiện hành.

## Bản affiliate hoàn chỉnh V7

- Composition: `VideoAiBanHangV6`, 1080×1920, 30 fps, 22 giây.
- Sáu nhịp dựng: tình huống 0–6s → hero 6–9s → demo 9–13s → objection 13–16s → trust 16–19s → CTA 19–22s.
- Footage chuyển động chiếm 100% thời lượng; dùng bốn clip nguồn độc lập, không có slideshow.
- Giữ một Google voice `Tavi`; nhạc 10%, SFX 30%; mute toàn bộ audio footage.
- Text dùng DTPhudu/DarleySans, snap/punch nhanh, đặt lower-middle và không dùng branding `AI Players`.
- Disclosure hiển thị xuyên suốt: `Minh họa bằng AI • Link có thể tạo hoa hồng`.
- CTA Facebook: `Xem đánh giá • Link ghim bình luận`.
- File xuất: `out/video-ai-ban-hang-aff-hoan-chinh-v7.mp4`.

Video chỉ được đăng khi link/bình luận ghim trỏ đúng mẫu sản phẩm xuất hiện trong video và thông tin listing đã được kiểm tra lại.

## QA bắt buộc

- 1080×1920, 30 fps, khoảng 22 giây.
- Kiểm tra Google voice là audio chính, nhạc nền 8%, SFX 30%.
- Kiểm tra frame Hook, giữa và CTA: chữ cân giữa, không che sản phẩm, không tràn vùng an toàn.
