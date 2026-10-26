---
name: whiteboard-mindmap-explainer
description: >-
  Giải phẫu và tự động sản xuất video hoạt hình Sơ Đồ Tư Duy Bảng Trắng Vô Cực (Infinite Canvas Mindmap + Pixel Mascot Live Drawing) giống hệt phong cách "Hệ sinh thái Anthropic / Kỹ Sư 4.0". Kết hợp nền giấy kem ấm (#F5F2EB), nét vẽ tay wobbly (Rough/Excalidraw style), cơ chế Ghost Dashed Outline -> Mascot cầm bút tô mực thật tới đâu hình/chữ hiện ra tới đó, Camera 2D Pan/Zoom xuyên suốt 1 bảng vẽ khổng lồ duy nhất và Zoom-Out toàn cảnh ở cuối video.
---

# Whiteboard Mindmap Explainer Skill (Infinite Canvas + Mascot Live Drawing)

Skill này được xây dựng từ kết quả **giải phẫu kỹ thuật từng khung hình (Frame-by-Frame Reverse Engineering)** của video mẫu `FDown.vn_Tai_video_Facebook_720p (HD)_205f.mp4` (*Giải thích Hệ sinh thái Anthropic / Claude*), cho phép tạo ra các video giải thích hệ sinh thái, bản đồ công cụ AI, lộ trình học tập hoặc phễu sản phẩm có **tỷ lệ giữ chân (Retention) và chia sẻ (Share/Save) cực cao**.

---

## 1. Giải Phẫu Kỹ Thuật Video Mẫu (Tại Sao Video Này Cuốn Hút?)

### 1.1. Kiến Trúc "1 Bảng Vẽ Vô Cực Duy Nhất" (`Single Infinite World Canvas`)
Khác với video chuyển cảnh slide thông thường, toàn bộ video diễn ra trên **một mặt phẳng tọa độ 2D khổng lồ duy nhất (`4200×4200px`)** màu giấy kem ấm (`#F5F2EB`). Người xem luôn có cảm giác về **không gian vật lý (Spatial Memory)**:
- **Tâm bản đồ `(0, 0)`:** Node gốc hình elip vẽ tay (`Anthropic`).
- **Các nhánh vệ tinh `(branchX, branchY)`:** Tỏa ra theo hình nan quạt xung quanh tâm, mỗi nhánh mang **1 mã màu đất (Earthy Pastel Ink)** riêng biệt:
  - Đỏ gạch Terracotta (`#C85A3C`), Xanh rêu Olive (`#5C7A45`), Đỏ cam Rust (`#B84B30`), Xanh thép Steel Blue (`#3F74A6`), Tím Plum (`#7C4D8B`), Vàng đất Ochre (`#A67C38`), Đen than (`#1E1E1E`), Nâu đồng (`#8C583A`), Xanh Navy (`#2E5B82`).

### 1.2. Kịch Bản Điều Hướng Camera 4 Nhịp (`4-Act Camera Choreography`)
1. **Nhịp 1 — Deceptive Close-Up Hook (`00:00 – 00:03`, `Zoom = 2.2x`):**
   - Camera mở đầu bằng góc cận cảnh tại **Nhánh số 1 (`Claude app`)**. Khán giả tưởng toàn bộ chủ đề chỉ có bấy nhiêu.
2. **Nhịp 2 — The "One Small Branch" Zoom-Out Twist (`00:03 – 00:07`, `Zoom = 1.0x`):**
   - Lời thoại: *"Nhưng đó mới là một nhánh nhỏ thôi nha! Để mình vẽ cả cái cây cho bạn xem..."*
   - Camera đột ngột **Zoom Out** về tâm `"Anthropic"`, một tờ giấy **Sticky Note màu vàng kem (`#F4E3B2`) dán nghiêng `-6°`** đập vào góc trên trái với chữ **"Chỉ một nhánh nhỏ!"**, đồng thời để lộ các đường nhánh xám mờ tỏa ra 8 hướng.
3. **Nhịp 3 — Branch-by-Branch Guided Tour (`00:07 – 02:02`, `Zoom = 1.8x`):**
   - Camera trượt mượt (`easeInOutCubic` trong `12–15 frames`) dọc theo dây nhánh từ tâm ra từng Node (`Nhánh 1 -> Nhánh 2 -> ... -> Nhánh N`).
   - Tại mỗi nhánh, tiêu đề nhánh nằm cố định ở cạnh dưới hoặc cạnh trên khung hình, nhường khoảng trống trung tâm cho nhân vật Mascot vẽ chi tiết nhánh đó.
4. **Nhịp 4 — Grand Finale Macro Zoom-Out & Sticky CTA (`02:02 – 02:13`, `Zoom = 0.28x`):**
   - Camera thu nhỏ hết cỡ để lộ **toàn bộ sơ đồ cây hoàn chỉnh** với hàng chục chi tiết vừa vẽ.
   - Đập 2 tờ **Sticky Note** tổng kết (`"model → app → agent làm cùng bạn"`) và câu hỏi kích thích bình luận (`"Bạn đang dùng nhánh nào?"`).

### 1.3. Cơ Chế "Bản Phác Nét Đứt → Mascot Tô Mực Thật" (`Ghost Blueprint → Live Mascot Ink`)
Đây là kỹ thuật giữ mắt người xem không rời màn hình:
- **Trạng thái 1 (`Ghost Blueprint`):** Trước khi nói tới, vòng tròn tiêu đề nhánh hiển thị dưới dạng **nét đứt màu xám mờ (`strokeDasharray="10 8"`, `opacity=0.35`)**.
- **Trạng thái 2 (`Mascot Tracing & Drawing`):** Nhân vật **Pixel Mascot 4 chân màu cam đất (`#D97757`) cầm cây bút nghiêng `32°`** chạy dọc theo đường viền hoặc dòng chữ:
  - Ngòi bút (`penTip`) lướt tới đâu, nét vẽ tay liền mạch (`Solid Hand-Drawn Wobbly Stroke`) và chữ/icon hiện ra tới đó (sử dụng `strokeDashoffset` cho đường nét và `clipPath: inset(0 ${100 - progress}% 0 0)` cho văn bản/icon).
  - Chân Mascot nhấp nhô liên tục (`walkCycle`) và thân nhún nhảy theo nhịp vẽ.

### 1.4. Bộ 7 Mẫu Đồ Họa Con Bên Trong Mỗi Nhánh (`7 Micro-Diagram Primitives`)
Mỗi nhánh không chỉ viết chữ đơn điệu mà kết hợp 2–3 mẫu đồ họa nhỏ:
1. **`strikethrough-replace` (Gạch từ cũ → Viết từ mới):** VD viết `"hỏi"` rồi lấy bút gạch đỏ `"~~hỏi~~"` và viết `"giao việc"` bên cạnh.
2. **`icon-row` (Hàng Icon ngang):** 3 icon vẽ nét mảnh xếp ngang (`[🌐 web]  [💻 máy tính]  [📱 điện thoại]`).
3. **`icon-checklist` (Danh sách Icon + Chữ dọc):** Các dòng có icon nhỏ đầu dòng (`💬 Chat`, `📚 Nghiên cứu`, `📄 Đọc tài liệu`).
4. **`pills` (Các vòng elip vẽ tay nhỏ xếp ngang):** `(Free)` `(Pro)` `(Max)`.
5. **`flow-horizontal` (Luồng mũi tên ngang):** `kế hoạch → file → trình duyệt → kết quả`.
6. **`cycle-loop` (Vòng tuần hoàn 4 bước quanh 1 nhân):** `đọc project ↻ sửa code ↻ chạy test ↻ tự sửa` xoay quanh `(task)`.
7. **`staircase-bars` & `stacked-boxes` (Biểu đồ cột bậc thang & Hộp xếp chồng ngang):** Dùng để so sánh cấp độ (`Haiku < Sonnet < Opus < Fable < Mythos`) hoặc liệt kê kiến trúc tầng (`API / SDK / Managed`).

---

## 2. Cách Sử Dụng Skill Để Tạo Video Tương Tự

### 2.1. Chạy Bằng Dòng Lệnh CLI (`mindmap_video_cli.py`)
Công cụ CLI tại [`.agents/skills/whiteboard-mindmap-explainer/scripts/mindmap_video_cli.py`](file:///d:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/.agents/skills/whiteboard-mindmap-explainer/scripts/mindmap_video_cli.py) tự động hóa từ file kịch bản JSON -> Sinh giọng đọc tiếng Việt theo từng phân cảnh -> Tính toán frame chuẩn xác -> Render video MP4 `1080×1920 @ 30fps`:

```powershell
# Render video mẫu Hệ sinh thái AI Subagent / Claude Mindmap
python ".agents/skills/whiteboard-mindmap-explainer/scripts/mindmap_video_cli.py" `
  --preset "ai-agent-ecosystem" `
  --output "output/whiteboard_mindmap_demo.mp4"

# Hoặc truyền file kịch bản JSON tuỳ chỉnh cho bất kỳ chủ đề nào
python ".agents/skills/whiteboard-mindmap-explainer/scripts/mindmap_video_cli.py" `
  --config "campaigns/my-topic/mindmap_spec.json" `
  --output "campaigns/my-topic/mindmap_video.mp4"
```

### 2.2. Cấu Trúc Mã Nguồn Remotion (`templates/remotion-cuongit-template/src/WhiteboardMindmap/`)
- [`WhiteboardMindmapShort.tsx`](file:///d:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/templates/remotion-cuongit-template/src/WhiteboardMindmap/WhiteboardMindmapShort.tsx): Component chính điều khiển `WorldCamera` (Pan/Zoom trên bảng vẽ `4200×4200`), tự động nối tia từ Root Node tới các Branch Node, hiển thị Ghost Outline -> Mascot Live Ink Drawing và Sticky Notes.
- [`PixelMascotArtist.tsx`](file:///d:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/templates/remotion-cuongit-template/src/WhiteboardMindmap/PixelMascotArtist.tsx): Nhân vật Pixel Mascot 4 chân cầm bút chì/bút dạ tự động bám sát tọa độ `(penX, penY)` của nét vẽ hiện tại.
- [`handDrawn.ts`](file:///d:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/templates/remotion-cuongit-template/src/WhiteboardMindmap/handDrawn.ts): Bộ hàm sinh đường SVG vẽ tay tự nhiên (`wobblyEllipse`, `wobblyRect`, `wobblyLine`, `wobblyArrow`).
- [`types.ts`](file:///d:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/templates/remotion-cuongit-template/src/WhiteboardMindmap/types.ts): Định nghĩa Schema JSON cho các nhánh và 7 Micro-Patterns.
