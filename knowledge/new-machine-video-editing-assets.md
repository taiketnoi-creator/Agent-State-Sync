# Chuẩn bị máy mới cho edit video

Tài liệu này quy định những thứ cần đồng bộ để mở project trên máy mới mà không lỗi font, mất nhạc hoặc lệch bố cục.

## 1. Font chữ dùng cho phong cách AI Players

Ưu tiên font có giấy phép rõ ràng, hỗ trợ tiếng Việt và được cài cùng một bộ trên mọi máy:

- **Be Vietnam Pro**: font chính cho caption, nội dung tiếng Việt.
- **Montserrat**: tiêu đề mạnh, số thứ tự, CTA.
- **Inter**: chữ phụ, chú thích nhỏ và giao diện.
- **Space Grotesk**: chỉ dùng làm font nhấn cho tiêu đề công nghệ.

Quy tắc: không đổi font tùy ý giữa các máy. Nếu project dùng font khác, ghi tên chính xác và nguồn tải vào manifest trước khi edit tiếp.

## 2. Nhạc nền và âm thanh

- Chỉ dùng nhạc có quyền sử dụng cho Facebook/Reels/TikTok hoặc nhạc tự tạo.
- Lưu file âm thanh ngoài Git nếu dung lượng lớn; Git chỉ lưu manifest, giấy phép và metadata.
- Nên chuẩn hóa thư mục:

```text
assets/audio/
  music/       # nhạc nền đã được phép sử dụng
  sfx/         # whoosh, click, pop, transition
  voice/       # voice-over đã duyệt
  audio-manifest.md
```

- Mỗi track trong `audio-manifest.md` cần có: tên file, nguồn, giấy phép, thời lượng, BPM (nếu biết), mood và dự án sử dụng.
- Không dùng nhạc tải ngẫu nhiên từ YouTube/TikTok nếu chưa kiểm tra quyền; có thể bị tắt tiếng hoặc hạn chế phân phối.

## 3. Cách chuyển sang máy mới

1. Clone project từ Git.
2. Cài Node.js, Python, FFmpeg và phần mềm edit đang dùng.
3. Cài các font trong mục 1 từ nguồn chính thức, sau đó khởi động lại ứng dụng edit.
4. Tải thư mục asset nặng từ kho lưu trữ dùng chung (Google Drive/OneDrive/ổ backup), không lấy từ Git.
5. Đặt asset đúng cấu trúc thư mục của project; không đổi tên file nếu project đang tham chiếu đường dẫn đó.
6. Đọc `audio-manifest.md`, chỉ tải các track cần cho video đang dựng.
7. Mở project mẫu, render thử 5–10 giây để kiểm tra font, tiếng Việt, voice và nhạc.
8. Nếu render đúng, ghi nhận máy đã sẵn sàng; nếu thiếu asset, cập nhật manifest thay vì chép file tùy tiện.

## 4. Những gì đưa lên Git và những gì không

**Đưa lên Git:**

- Font manifest: tên, phiên bản, nguồn và giấy phép.
- Audio manifest: tên file, nguồn, giấy phép và mã checksum nếu cần.
- File project, preset, template, script render và hướng dẫn.
- Asset nhẹ cần thiết để preview.

**Không đưa lên Git:**

- Video render, file WAV/MP3 lớn, voice thô, footage gốc, cache và thư mục export.
- File tải từ nguồn không rõ giấy phép.
- `.env`, token, tài khoản hoặc dữ liệu riêng tư.

## 5. Checklist trước khi bàn giao máy

- [ ] Đã cài đủ font và kiểm tra tiếng Việt.
- [ ] Đã có FFmpeg và phần mềm edit.
- [ ] Đã tải asset/audio cần thiết từ kho dùng chung.
- [ ] Manifest ghi đủ nguồn và giấy phép.
- [ ] Render thử không lỗi missing font/missing media.
- [ ] Không có video nặng hoặc dữ liệu riêng tư bị stage vào Git.

