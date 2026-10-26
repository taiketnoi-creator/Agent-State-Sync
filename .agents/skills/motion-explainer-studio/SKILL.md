---
name: motion-explainer-studio
description: >-
  Thiết kế và kết xuất video Thể loại Motion Explainer (Đồ họa chuyển động giải thích khái niệm phức tạp, kiến trúc công nghệ, toán học, thuật AI, mật mã học) bằng Motion Canvas (TypeScript: @motion-canvas/core, @motion-canvas/2d với hiệu ứng bo góc, zoom và camera tracking mượt mà) và Manim (Python: manim v0.22.0 tự động vẽ và biến đổi hình khối lập phương, ma trận, vector, đồ thị hàm số không cần keyframe thủ công).
---

# Motion Explainer Studio Skill (Motion Canvas & Manim)

Skill này trang bị cho Subagent `edit` 2 bộ engine đồ họa chuyển động (Procedural Motion Graphics) mạnh nhất hiện nay để giải thích các khái niệm phức tạp mà không cần đặt keyframe thủ công:

| Tiêu chí | 1. Motion Canvas (`TypeScript`) | 2. Manim (`Python - Manim Community v0.22`) |
| :--- | :--- | :--- |
| **Thế mạnh cốt lõi** | Video giải thích doanh nghiệp, kiến trúc hệ thống AI/Cloud, giới thiệu tính năng ứng dụng (SaaS UI), luồng dữ liệu bo góc. | Video giải thích học thuật, toán học, vật lý, mật mã học, ma trận (Matrix), đồ thị hàm số và biến đổi hình khối 2D/3D. |
| **Cơ chế chuyển động** | Generator (`function* (view)`) + `yield* all(...)`, `chain(...)`, điều khiển **Camera Tracking & Zoom (`camera().centerOn`, `camera().zoom`)** mượt mà bằng dòng lệnh. | Biến đổi hình học toán học (`ReplacementTransform`, `TransformMatchingShapes`, `ValueTracker`, `MovingCameraScene`, `ThreeDScene`). |
| **Thư mục / Công cụ** | [`templates/motion-canvas-template/`](file:///d:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/templates/motion-canvas-template) | [`.agents/skills/motion-explainer-studio/scripts/manim_explainer_cli.py`](file:///d:/Phi%C3%AAn%20b%E1%BA%A3n%20Ai%20agent/Subagent/.agents/skills/motion-explainer-studio/scripts/manim_explainer_cli.py) |

---

## 1. Nhánh 1: Dựng Video Giải Thích Công Nghệ / SaaS Bằng Motion Canvas (`TypeScript`)

### 1.1. Cấu Trúc Code Chuẩn Motion Canvas (`@motion-canvas/2d`)
Sử dụng cú pháp Generator `function* (view)` kết hợp `<Camera>` để tự động lia máy (pan) và phóng đại (zoom) theo từng khối kiến trúc:

```tsx
import { Camera, Circle, Line, Node, Rect, Txt, makeScene2D } from "@motion-canvas/2d";
import { Vector2, all, createRef, easeInOutCubic, easeOutBack } from "@motion-canvas/core";

export default makeScene2D(function* (view) {
  view.fill("#050814");
  const camera = createRef<Camera>();
  const cardA = createRef<Rect>();
  const cardB = createRef<Rect>();
  const connector = createRef<Line>();

  view.add(
    <Camera ref={camera}>
      <Node>
        <Line ref={connector} points={[new Vector2(0, -350), new Vector2(0, 350)]} stroke={"#87FF00"} lineWidth={8} end={0} />
        <Rect ref={cardA} y={-350} width={640} height={200} radius={36} fill={"#0F172A"} stroke={"#87FF00"} lineWidth={4} scale={0}>
          <Txt text={"API GATEWAY"} fill={"#87FF00"} fontSize={40} fontWeight={900} />
        </Rect>
        <Rect ref={cardB} y={350} width={640} height={200} radius={36} fill={"#0F172A"} stroke={"#38BDF8"} lineWidth={4} scale={0}>
          <Txt text={"VECTOR DATABASE"} fill={"#38BDF8"} fontSize={40} fontWeight={900} />
        </Rect>
      </Node>
    </Camera>
  );

  // 1. Bật khối A và zoom camera vào khối A
  yield* all(
    cardA().scale(1, 0.5, easeOutBack),
    camera().centerOn(cardA(), 0.6, easeInOutCubic),
    camera().zoom(1.3, 0.6, easeInOutCubic)
  );

  // 2. Vẽ đường nối và lia camera mượt xuống khối B
  yield* all(
    connector().end(1, 0.65, easeInOutCubic),
    cardB().scale(1, 0.5, easeOutBack),
    camera().centerOn(cardB(), 0.7, easeInOutCubic)
  );

  // 3. Thu phóng camera về toàn cảnh
  yield* all(
    camera().centerOn(new Vector2(0, 0), 0.8, easeInOutCubic),
    camera().zoom(1.0, 0.8, easeInOutCubic)
  );
});
```

### 1.2. Khởi Chạy Motion Canvas Studio
```powershell
Set-Location "d:\Phiên bản Ai agent\Subagent\templates\motion-canvas-template"
pnpm dev
```

---

## 2. Nhánh 2: Dựng Video Giải Thích Toán Học / Thuật Toán / Mật Mã Học Bằng Manim (`Python`)

Manim (`manim==0.22.0`) đã được cài đặt sẵn trong môi trường Python của dự án, hỗ trợ kết xuất cả khổ dọc **9:16 (`1080×1920`)** cho Reels/Shorts/TikTok và khổ ngang **16:9 (`1920×1080`)**.

### 2.1. Chạy Trực Tiếp Qua CLI (`manim_explainer_cli.py`)
Script `.agents/skills/motion-explainer-studio/scripts/manim_explainer_cli.py` cung cấp sẵn 3 mẫu Scene chuẩn (`FunctionGraphMorphScene`, `MatrixNeuralTransformScene`, `CryptoCube3DScene`) và hỗ trợ tự động ghép giọng đọc tiếng Việt (`--voiceover` hoặc `--tts-text`):

```powershell
# Render video giải thích Đồ thị Hàm số & Biến đổi Hình học (Khổ dọc 9:16 1080x1920)
python ".agents/skills/motion-explainer-studio/scripts/manim_explainer_cli.py" `
  --scene FunctionGraphMorphScene `
  --aspect 9:16 `
  --quality m `
  --output "output/manim_function_morph_9x16.mp4"

# Render video giải thích Ma trận Trọng số AI & Mạng Nơ-ron kèm thuyết minh tiếng Việt
python ".agents/skills/motion-explainer-studio/scripts/manim_explainer_cli.py" `
  --scene MatrixNeuralTransformScene `
  --aspect 9:16 `
  --tts-text "Bên trong trí tuệ nhân tạo, mọi câu chữ đều được biến đổi thành ma trận số học và đi qua phép nhân vector trong không gian đa chiều." `
  --output "output/manim_matrix_ai_9x16.mp4"
```

### 2.2. Các Phép Biến Đổi Cốt Lõi Của Manim Cần Nhớ
- **Vẽ tự động nét mượt:** `self.play(Create(mobject), Write(text))`
- **Biến hình liên tục giữa 2 hình khối bất kỳ (Morphing):** `self.play(ReplacementTransform(square, circle), run_time=1.2)`
- **Đồ thị hàm số động theo thời gian (`ValueTracker`):** Dùng `always_redraw(lambda: axes.plot(...))` kết hợp `self.play(tracker.animate.set_value(...))` để đường cong uốn lượn mượt mà.
- **Khối 3D & Camera xoay không gian (`ThreeDScene`):** Dùng `ThreeDCube`, `Surface`, `self.move_camera(phi=65*DEGREES, theta=-45*DEGREES)`.

---

## 3. Quy Tắc Phối Hợp Giữa Motion Canvas, Manim và Remotion

- Khi cần **giải thích cơ chế thuật toán, ma trận, hàm số, vector embedding hoặc mật mã học**: Dùng `manim_explainer_cli.py` xuất clip `.mp4` nền tối (`#050814`), sau đó có thể dùng trực tiếp hoặc đưa vào làm phân cảnh trung tâm trong Remotion/FFmpeg.
- Khi cần **tracking camera mượt qua sơ đồ hệ thống bo góc, luồng API, kiến trúc Microservices/Subagent**: Dùng `templates/motion-canvas-template` (`@motion-canvas/2d`).
