---
name: talking-head-editor
description: >-
  Dựng và hậu kỳ video thể loại Talking Head (Video người thật hoặc AI Avatar nói chuyện trực diện 9:16) bằng Remotion (React + @remotion/captions) hoặc HyperFrames (HTML/JS + FFmpeg). Tự động định vị A-Roll chính giữa màn hình, đồng bộ âm thanh với phụ đề .srt/.json tạo hiệu ứng chữ chạy Karaoke từng từ (word-by-word highlight) chuẩn xác tới từng mili-giây, và chèn B-Roll (ảnh/video minh họa) đè lên video gốc theo mốc thời gian (timestamps) dòng lệnh không lệch khung hình.
---

# Talking Head Video Editor Skill (Remotion & HyperFrames)

Skill này chuẩn hóa quy trình dựng video **Thể loại Talking Head (Người thật hoặc AI Avatar nói chuyện)** kết hợp **Phụ đề Karaoke chạy từng từ (Word-by-Word Highlight)** và **Chèn B-Roll tự động theo mốc thời gian (`timestamps`)** bằng mã nguồn **Remotion (React)** hoặc **HyperFrames (HTML/JS + FFmpeg)**.

---

## 1. Kiến Trúc 3 Lớp Của Video Talking Head Chuẩn Chuyển Đổi (`1080×1920 @ 30fps`)

1. **Lớp 1 — Luồng A-Roll Người Nói (Centered Speaker Layer):**
   - Định vị video người nói (hoặc AI Avatar như HeyGen / Kling / Veo) ở **chính giữa màn hình** (`object-position: center`, giữ vùng mắt ở đường 1/3 trên `y ≈ 520–680px`).
   - Khi có B-Roll xuất hiện ở chế độ `pip-card` hoặc `split-top`, luồng người nói vẫn giữ kết nối thị giác hoặc tự động thu nhỏ thành **Picture-in-Picture (PiP Avatar Bubble)** ở góc dưới để không làm đứt mạch cảm xúc.
2. **Lớp 2 — Lớp B-Roll Đè Theo Mốc Thời Gian (`Frame-Accurate B-Roll Overlay`):**
   - Nhập danh sách B-Roll qua dòng lệnh (`--broll "startSec-endSec:path:mode:label"`) hoặc file `manifest.json`.
   - Mốc thời gian giây (`startSec`, `endSec`) được quy đổi cứng sang chỉ số khung hình:
     $$\text{startFrame} = \text{round}(\text{startSec} \times \text{fps}), \quad \text{durationInFrames} = \text{round}((\text{endSec} - \text{startSec}) \times \text{fps})$$
   - Hỗ trợ 3 chế độ hiển thị B-Roll:
     - `fullscreen`: B-Roll phủ toàn màn hình (kèm hiệu ứng Zoom nhẹ *Ken Burns* để chống tĩnh), giữ âm thanh A-Roll xuyên suốt.
     - `pip-card`: B-Roll hiện trong khung kính Glassmorphism ở nửa trên màn hình (`top: 220px`), vẫn nhìn thấy người nói bên dưới.
     - `split-top`: Chia đôi màn hình 50/50 (nửa trên là B-Roll minh họa, nửa dưới là người nói).
3. **Lớp 3 — Phụ Đề Karaoke Chạy Từng Từ (`Word-by-Word Karaoke Captions`):**
   - Tự động chuyển đổi file `.srt` hoặc sinh trực tiếp từ `edge-tts` (`WordBoundary`) sang mảng JSON `WordToken[]` (`text`, `startMs`, `endMs`).
   - Bảo vệ từ ghép tiếng Việt (ví dụ: `"trí tuệ"`, `"nhân tạo"`, `"hệ thống"`, `"chuyển đổi"`) để chữ nhảy theo cụm từ có nghĩa.
   - Từ đang đọc tại thời điểm $t = (\text{frame} / \text{fps}) \times 1000\text{ ms}$ sẽ tự động **bật sáng màu `#87FF00` (Neon Lime)**, phóng nhẹ `scale(1.12)` bằng lò xo `spring()` và đổ bóng phát sáng, trong khi các từ đã đọc mang màu trắng `#FFFFFF` và từ sắp đọc mờ `rgba(255,255,255,0.45)`.

---

## 2. Cách 1: Dựng Tự Động Bằng Dòng Lệnh CLI (`talking_head_cli.py`)

Công cụ CLI tại `.agents/skills/talking-head-editor/scripts/talking_head_cli.py` cho phép dựng video Talking Head hoàn chỉnh chỉ bằng 1 dòng lệnh duy nhất:

### 2.1. Chạy với Engine Remotion (React + `@remotion/captions`)
```powershell
python ".agents/skills/talking-head-editor/scripts/talking_head_cli.py" `
  --aroll "campaigns/sample/speaker_aroll.mp4" `
  --srt "campaigns/sample/subtitles.srt" `
  --broll "02.0-05.5:campaigns/sample/broll_1.jpg:pip-card:Bằng chứng thực tế,08.0-12.0:campaigns/sample/broll_2.mp4:fullscreen:Demo trực tiếp" `
  --engine remotion `
  --output "campaigns/sample/talking_head_final.mp4"
```

### 2.2. Chạy với Engine HyperFrames (HTML5/JS Frame-Deterministic + FFmpeg Karaoke `\kf`)
```powershell
python ".agents/skills/talking-head-editor/scripts/talking_head_cli.py" `
  --aroll "campaigns/sample/speaker_aroll.mp4" `
  --srt "campaigns/sample/subtitles.srt" `
  --broll "02.0-05.5:campaigns/sample/broll_1.jpg:pip-card:Bằng chứng thực tế,08.0-12.0:campaigns/sample/broll_2.mp4:fullscreen:Demo trực tiếp" `
  --engine hyperframes `
  --output "campaigns/sample/talking_head_hyperframes.mp4"
```

### 2.3. Sinh Tự Động Phụ Đề Karaoke `.srt` + `.json` Word-Level Từ Văn Bản
Nếu chỉ có file lời thoại `.txt` và muốn tạo giọng đọc kèm phụ đề từng từ (millisecond-accurate):
```powershell
python ".agents/skills/talking-head-editor/scripts/talking_head_cli.py" `
  --generate-tts-text "Tại sao 90 phần trăm người làm video AI đều thất bại ở 3 giây đầu tiên? Bí mật nằm ở nhịp cắt B-roll và phụ đề Karaoke." `
  --srt "campaigns/sample/subtitles.srt" `
  --json-out "campaigns/sample/karaoke_words.json"
```

---

## 3. Cách 2: Tuỳ Biến Trực Tiếp Trong Mã Nguồn Remotion (`templates/remotion-cuongit-template/src/TalkingHeadShort/`)

Khi cần thiết kế giao diện Talking Head độc bản cho từng chiến dịch trong `templates/remotion-cuongit-template`:

1. **Component gốc:** [`TalkingHeadShort.tsx`](file:///d:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/templates/remotion-cuongit-template/src/TalkingHeadShort/TalkingHeadShort.tsx)
2. **Lớp phụ đề Karaoke:** [`KaraokeCaptionLayer.tsx`](file:///d:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/templates/remotion-cuongit-template/src/TalkingHeadShort/KaraokeCaptionLayer.tsx)
3. **Lớp B-Roll theo Timestamp:** [`BRollOverlayLayer.tsx`](file:///d:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/templates/remotion-cuongit-template/src/TalkingHeadShort/BRollOverlayLayer.tsx)

### Cấu trúc Props JSON (`TalkingHeadProps`)
```json
{
  "arollSrc": "talking-head/speaker_demo.mp4",
  "channelBadge": "⚡ AI PLAYERS",
  "headlineHook": "BÍ MẬT VIDEO TALKING HEAD TRIỆU VIEW",
  "words": [
    { "text": "Tại sao", "startMs": 0, "endMs": 420 },
    { "text": "video", "startMs": 420, "endMs": 750 },
    { "text": "Talking Head", "startMs": 750, "endMs": 1350 },
    { "text": "giữ chân", "startMs": 1350, "endMs": 1820 },
    { "text": "khán giả?", "startMs": 1820, "endMs": 2400 }
  ],
  "brolls": [
    {
      "id": "broll_1",
      "startSec": 2.0,
      "endSec": 5.0,
      "src": "talking-head/broll_chart.png",
      "mediaType": "image",
      "layout": "pip-card",
      "label": "📊 TỶ LỆ GIỮ CHÂN +68%",
      "zoomEffect": "ken-burns-in"
    }
  ]
}
```

---

## 4. Tiêu Chuẩn Nghiệm Thu (Hard Gate Cho Subagent `edit`)

- **Zero Frame Drift:** B-Roll phải mở và đóng khớp 100% với `startSec` và `endSec` đã khai báo (quy đổi qua `Math.round(sec * fps)`).
- **Karaoke Sync $\le 50\text{ms}$:** Từ đang phát âm phải sáng màu `#87FF00` đúng nhịp giọng nói, không hiển thị quá 6–8 từ trên 1 dòng để dễ đọc trên màn hình điện thoại.
- **Bảo Vệ Khuôn Mặt A-Roll:** Ở chế độ `pip-card`, khung B-Roll không được che miệng người nói; phụ đề Karaoke luôn đặt ở vùng an toàn (`bottom: 240px–340px`).
