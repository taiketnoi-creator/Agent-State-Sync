# Video AI Bán Hàng — Veo native audio và nhịp direct-response

## Khi nào áp dụng

Áp dụng khi người dùng yêu cầu giọng đọc phải được Google/Veo tạo đồng thời với video. Đây là biến thể `VEO_NATIVE_AUDIO`, không được thay bằng gTTS hoặc một track voice hậu kỳ rồi báo là voice gốc của Veo.

## Hard gates

- Mỗi clip nguồn phải có cả stream video và stream audio.
- Prompt phải ghi `Native synchronized audio is mandatory`, mô tả giọng, tốc độ và câu thoại tiếng Việt chính xác.
- Không chèn branding, logo dự án, dòng `AI Players`, caption hoặc tiêu đề nếu người dùng không yêu cầu.
- Không dùng crossfade dài. Video bán hàng direct-response ưu tiên hard cut, whip-pan, snap zoom, punch-in và impact SFX.
- Hook phải xuất hiện trong 0–2 giây; CTA chỉ yêu cầu một hành động.
- Sau khi ghép, không được có khoảng im lặng liên tục từ 1 giây trở lên, trừ khi kịch bản chủ ý yêu cầu.
- Clip có logo ngoài ý muốn, chữ giả, nhãn méo hoặc text AI sinh phải bị loại và tạo lại; không che bằng một lớp branding khác.
- Nhân vật đang nói trên hình phải dùng audio native do Google/Veo tạo cùng cảnh để giữ lip-sync. Các clip có nhân vật nói phải khóa cùng một mô tả giọng, nhịp và tính cách; ưu tiên cùng character/reference xuyên suốt.
- Cảnh B-roll hoặc minh họa không lộ miệng có thể dùng voice-over, nhưng voice-over cũng phải được tạo bằng Google AI Studio/Gemini TTS và giữ cùng một speaker. Cấm dùng gTTS, giọng video slide hoặc voice chậm kiểu thuyết minh.
- Không trộn nhiều voice identity trong một video. Nếu chuyển toàn bộ sang một Google voice-over thống nhất thì chỉ dùng footage không thể hiện nhân vật đang nói và mute toàn bộ native audio.

## Nhịp mặc định

- Tổng thời lượng mục tiêu: 20–30 giây.
- 4–6 shot: hook → demo → trust → CTA.
- Cắt phần im lặng đầu/cuối clip dựa trên waveform hoặc `silencedetect`.
- Mỗi shot chỉ giữ đủ thời gian để hoàn tất câu thoại và hành động chính.
- Nhịp voice mặc định cho video bán hàng: sáng, rõ, nhanh và có lực; không kéo chữ, không đọc đều đều, không dùng sắc thái buồn ngủ.
- Mức âm thanh tham chiếu cho social: integrated loudness khoảng `-16 đến -14 LUFS`, true peak không vượt `-0,5 dB`.

## Prompt audio mẫu

```text
Native synchronized audio is mandatory. One energetic young Vietnamese female commercial voice speaks clearly and quickly in Vietnamese, exact words: “...” Strong direct-response delivery, about 1.15x normal pace. Add crisp whoosh and tactile product sounds, no music.
```

Luôn kèm negative constraints:

```text
No on-screen text, no subtitles, no captions, no letters, no product labels, no logos, no brands, no readable UI, no silent video, no slideshow.
```

## QA bắt buộc

1. Dò đủ audio stream trên từng clip bằng `ffprobe`.
2. Kiểm tra đầu–giữa–cuối từng cảnh để phát hiện chữ/logo giả, drift sản phẩm, lỗi tay và morphing.
3. Chạy kiểm tra khoảng lặng dài trên bản cuối.
4. Kiểm tra loudness và true peak.
5. Xem toàn bộ ở tốc độ thường để đánh giá cảm giác bán hàng, không chỉ kiểm tra kỹ thuật.
6. Nếu thấy miệng nhân vật chuyển động, xác nhận audio là native/lip-sync; nếu dùng Google voice-over hậu kỳ, thay shot đó bằng B-roll không lộ miệng.

## Bài học từ Test 02

Bản Test 02 có footage Veo thật nhưng vẫn thất bại về mục tiêu bán hàng vì dùng voice ngoài, crossfade chậm, lớp tiêu đề/caption dày và branding `AI Players`. Đạt chuẩn kỹ thuật không đồng nghĩa đạt direct-response. Bản sửa phải thay đổi cả nguồn voice, nhịp dựng và ngôn ngữ hình ảnh.
