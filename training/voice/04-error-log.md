# Voice — Error log

## Lỗi kiểm tra cần chặn

1. Văn bản thô không có pause/emphasis: trừ 3.0 điểm; nguyên nhân là bỏ qua chuẩn TTS.
2. Nhồi quá nhiều SFX cùng lúc: trừ 2.5 điểm; nguyên nhân là không giới hạn cue density.
3. Không ghi tốc độ đọc 1.1x/1.15x: trừ 1.5 điểm; nguyên nhân là thiếu thông số voice.

## Kết quả micro-test

Không phát hiện lỗi thực tế trong bản đạt 10/10; các lỗi trên được giữ như regression checks cho lần chạy sau.
