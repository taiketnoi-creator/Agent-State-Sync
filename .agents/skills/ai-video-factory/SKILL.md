---
name: ai-video-factory
description: >-
  Use this skill when generating high-converting short video scripts (TikTok/Reels/Shorts), maintaining AI brand character consistency, or rendering vertical 9:16 videos locally using FFmpeg (with multi-clip stitching and folder-level batch mixing).
---

# Nhà Máy Sản Xuất Video AI Xây Dựng Thương Hiệu & Bán Hàng (0-Token Local Render)

Skill này chuẩn hóa quy trình từ **Lên kịch bản -> Giữ đồng nhất nhân vật thương hiệu (Character Consistency) -> Trộn phân cảnh & Hậu kỳ tự động hàng loạt bằng FFmpeg (Tích hợp logic `short-video-factory`)**.

## 1. Cấu Trúc Kịch Bản Video Bán Hàng 30 Giây (High-Retention Formula)

Mỗi kịch bản lưu tại `output/scripts/<slug>.json` phải tuân thủ cấu trúc 4 nhịp:
1. **0s – 3s (Pattern Interrupt & Visual Hook):** Câu hỏi xoáy thẳng vào nỗi đau hoặc hình ảnh đối lập gây sốc. Tuyệt đối không chào hỏi rườm rà.
2. **3s – 10s (Agitation & Story):** Đồng cảm với vấn đề của người xem thông qua góc nhìn của nhân vật đại diện thương hiệu (`data/brand_persona.json`).
3. **10s – 23s (Solution & Proof):** Trình diễn 2–3 lợi ích đắt giá nhất của sản phẩm (tập trung vào kết quả thực tế Before/After thay vì thông số kỹ thuật khô khan).
4. **23s – 30s (Urgency & CTA):** Lời kêu gọi hành động rõ ràng (nhấn bình luận ghim / giỏ hàng góc trái) kèm lý do phải hành động ngay.

## 2. Quy Tắc Giữ Đồng Nhất Nhân Vật Thương Hiệu (Brand Character Consistency)

Khi sinh prompt tạo ảnh/video cho các cảnh (`scenes`), luôn lấy chuỗi `character_anchor_prompt` và `visual_style` từ file `data/brand_persona.json` ghép vào đầu mỗi prompt cảnh:
- **Công thức Prompt chuẩn:**
  `[character_anchor_prompt], [hành động/biểu cảm trong cảnh], [bối cảnh & sản phẩm], [visual_style], vertical 9:16 aspect ratio, photorealistic lighting`

## 3. Tự Động Dựng & Trộn Video 9:16 Hàng Loạt Bằng FFmpeg (`ffmpeg_render.py`)

Script `ffmpeg_render.py` hỗ trợ **nối đa phân cảnh (`filter_complex` concat $\ge 4$ cảnh)**, **tự động co giãn khớp thời lượng giọng đọc Vbee (`ffprobe`)**, **chuẩn hóa âm lượng phòng thu** (Voiceover `-3dB`, nhạc nền BGM tự động hạ xuống `-18dB`), **đóng cứng phụ đề `.srt`**, và **trộn hàng loạt theo thư mục phân cảnh (`--scenes-dir` + `--batch-count`)**:

### Cách 1: Dựng từ file Manifest chuẩn (`--manifest`)
```powershell
python ".agents/skills/ai-video-factory/scripts/ffmpeg_render.py" --manifest "output/scripts/sample_job.json" --output "output/videos/sample_final.mp4"
```

### Cách 2: Trộn phân cảnh hàng loạt theo thư mục (`--scenes-dir` — Short Video Factory Mode)
Chỉ cần bỏ các clip Veo/Kling hoặc ảnh keyframe vào các thư mục con (`01_hook/`, `02_pain/`, `03_demo/`, `04_cta/`), script sẽ tự động bốc từng cảnh, ghép khớp với file Voiceover và xuất ra nhiều biến thể (`--batch-count`):
```powershell
python ".agents/skills/ai-video-factory/scripts/ffmpeg_render.py" --scenes-dir "campaigns/2026-10-20/today-launch/scenes" --voiceover "campaigns/2026-10-20/today-launch/voice.mp3" --srt "campaigns/2026-10-20/today-launch/subtitles.srt" --batch-count 2 --output "output/videos/ktx_batch.mp4"
```
