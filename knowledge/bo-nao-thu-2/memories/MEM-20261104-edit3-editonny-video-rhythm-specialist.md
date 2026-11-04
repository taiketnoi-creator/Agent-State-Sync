---
id: MEM-20261104-edit3-editonny-video-rhythm-specialist
title: "Quy chuẩn Subagent edit-3 — Chuyên gia Editonny (Cắt nhịp giọng nói, Phụ đề từng từ, Bám mặt 9:16 & 145 Cảnh Đồ Họa HyperFrames)"
created_at: "2026-11-04T10:45:00+07:00"
updated_at: "2026-11-04T10:45:00+07:00"
status: ACTIVE
priority: CRITICAL
source: "CEO Thành Tài — Mệnh lệnh tạo Subagent edit-3 & cài đặt chuyên biệt dự án https://github.com/soumatheusgomes/editonny ngày 04/11/2026"
tags:
  - edit-3
  - editonny
  - hyperframes
  - faster-whisper
  - motion-scenes
  - talking-head
  - video-rhythm
---

# Quy Chuẩn Subagent `edit-3` (`Editonny Local Video Rhythm, Speech-Cut, Captions & 145 Motion Scenes Specialist`)

## 1. Vị Trí Cài Đặt & Môi Trường Đã Khóa Cứng Trên Hệ Thống

- **File định nghĩa Subagent:**
  - `d:\Phiên bản Ai agent\Subagent\edit-3.md`
  - `d:\Phiên bản Ai agent\Subagent\.agents\plugins\agent-javis\agents\edit-3.md` (Đã đăng ký Native Subagent `edit-3` trên Antigravity)
- **Thư mục mã nguồn & Engine `editonny` (`v1.1.0`):**
  - Kho gốc: `d:\Phiên bản Ai agent\Subagent\templates\editonny`
  - Skill liên kết: `d:\Phiên bản Ai agent\Subagent\.agents\skills\editonny`
  - CLI điều khiển chính: `d:\Phiên bản Ai agent\Subagent\templates\editonny\skills\editonny\scripts\editonny.py`
  - Môi trường Python Engine (`uv` khóa cứng): `d:\Phiên bản Ai agent\Subagent\templates\editonny\skills\editonny\engine\.venv\Scripts\python.exe` (CPython 3.11.15 + `faster-whisper==1.2.1`, `opencv-python-headless==5.0.0.93`, `onnxruntime==1.23.2`, `pillow==13.0.0`, `numpy==2.4.6`, `av==18.1.0`)
  - Thư viện Cảnh Đồ Họa (`Visual Catalog`): **145 cảnh HTML/GSAP/Three.js** tại `skills/editonny/visuals/scenes/*.html` + **79 video gốc kiểm chứng SHA-256** (`79/79 valid videos`).
  - Trình kết xuất (`Renderer`): `npx --yes hyperframes@0.8.179` (`C:\Users\guicci\.local\bin\npx.cmd`).

## 2. Phân Vai Rõ Ràng Giữa 3 Subagent Dựng Hình (`edit` vs `edit-2` vs `edit-3`)

1. **`edit`**: Chuyên thiết kế Ảnh vuông `1:1` Độc Bản `Zero-Clone` + dựng Remotion Reels `9:16` (`21 Bespoke Reels`) cho Page `AI Players` và Ảnh vuông `1:1` `Minimal Pop-Bold Typography` cho 3 Page Bán Hàng.
2. **`edit-2`**: Chuyên sản xuất Video AI Bán Hàng thương mại 8 Nhịp (`Hybrid A-Roll <-> B-Roll Sandwich`), viết Prompt tiếng Anh cho Nano Banana / Google Veo 3 và đóng gói 5 lớp đồ họa thương mại.
3. **`edit-3`**: Chuyên vận hành bộ công cụ **`editonny`** để:
   - Cắt gọt video người thật nói chuyện / AI Avatar / screencast theo **nhịp giọng nói & biên độ âm thanh (`waveform_cut.py`, `tighten_cut.py`, `breaths.py`)**, tự động cắt khoảng lặng, câu nói vấp, câu lặp.
   - Bóc băng giọng nói chuẩn từng từ bằng **Faster-Whisper (`transcribe.py` -> `pack_transcripts.py` -> `align_words.py`)** và đóng phụ đề từng từ (`captions.py` + kiểm tra OCR chống tràn lề).
   - Bám khuôn mặt tự động (`track_faces.py` + `face_layout.py`) khi chuyển đổi khung hình `9:16` (`1080x1920`), `16:9`, `4:5`, `1:1` với 3 phong cách (`paper`, `night`, `amber`) và 6 bố cục (`fullscreen`, `evidence`, `frame`, `greenScreen`, `contain`, `compare`).
   - Chèn **145 cảnh đồ họa chuyển động (`visuals/apply.py`)** và **79 video minh họa gốc** tại đúng các điểm cắt (`--cut`) hoặc mốc thời gian (`--start`), chuẩn hóa âm thanh `-14 LUFS` / `-1.5 dBTP` và kiểm định qua `verify.py` + `quality_gate.py`.

## 3. Quy Trình 8 Bước Chuẩn Khi Gọi `edit-3`

1. `editonny.py doctor` & `editonny.py inspect <source.mp4> --json`
2. `editonny.py workspace init --edit <EDIT_DIR> --project <PROJECT_DIR> --source <source.mp4>`
3. `editonny.py helper transcribe.py` $\rightarrow$ `pack_transcripts.py` $\rightarrow$ `waveform_cut.py` $\rightarrow$ `tighten_cut.py` $\rightarrow$ `render_cut.py`
4. `editonny.py new <PROJECT_DIR> --edit <EDIT_DIR> --style night|paper|amber`
5. `editonny.py catalog "<từ khóa>"` $\rightarrow$ `editonny.py scene --project <PROJECT_DIR> --use <scene-id> --cut <giây>`
6. `python build.py prepare` $\rightarrow$ `python build.py compose`
7. `python build.py hf lint` $\rightarrow$ `python build.py hf check` $\rightarrow$ `python build.py hf snapshot`
8. `python build.py hf render --fps 30 --output renders/final.mp4` $\rightarrow$ `editonny.py helper verify.py` & `quality_gate.py`
