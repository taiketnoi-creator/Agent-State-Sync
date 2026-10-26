#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motion Explainer Studio — Manim Python CLI Engine (v0.22.0)
-----------------------------------------------------------
Tự động vẽ và biến đổi các hình khối lập phương 3D, ma trận, vector và đồ thị hàm số
theo thời gian một cách mượt mà mà không cần đặt keyframe thủ công.
Hỗ trợ cả khổ dọc 9:16 (1080x1920 cho Reels/Shorts/TikTok) và khổ ngang 16:9 (1920x1080),
kèm tính năng tự động lồng tiếng Việt (edge-tts) và đóng gói MP4 hoàn chỉnh.
"""

import argparse
import asyncio
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from manim import (
     BLUE_C,
     Create,
     DEGREES,
     DOWN,
     FadeIn,
     FadeOut,
     GREEN_B,
     LEFT,
     ORIGIN,
     PI,
     RIGHT,
     UP,
     WHITE,
     YELLOW,
     Arrow,
     Axes,
     Circle,
     Cube,
     Dot,
     IntegerMatrix,
     LaggedStart,
     Line,
     MovingCameraScene,
     NumberPlane,
     RegularPolygon,
     ReplacementTransform,
     RoundedRectangle,
     Square,
     Text,
     ThreeDAxes,
     ThreeDScene,
     VGroup,
     ValueTracker,
     Write,
     always_redraw,
     config,
     rate_functions,
)

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
BRAND_BG = "#050814"
BRAND_LIME = "#87FF00"
BRAND_CYAN = "#38BDF8"


class FunctionGraphMorphScene(MovingCameraScene):
    """
    Scene 1: Biến đổi Hình khối Hình học (Tam giác -> Lục giác -> Đường tròn)
    & Đồ thị Hàm số Sóng điều biến theo thời gian (ValueTracker) kèm Camera Zoom.
    """

    def construct(self) -> None:
        self.camera.background_color = BRAND_BG

        # Header title
        title = Text("BIẾN ĐỔI HÌNH HỌC & HÀM SỐ", font="Arial", weight="BOLD", font_size=34, color=BRAND_LIME)
        subtitle = Text("Procedural Math Animation — Zero Manual Keyframes", font="Arial", font_size=20, color=WHITE)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.6)
        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.6)

        # Phase 1: Shape Morphing (Square -> Hexagon -> Circle)
        sq = Square(side_length=2.4, color=BRAND_CYAN, stroke_width=6).shift(UP * 1.8)
        sq.set_fill(BRAND_CYAN, opacity=0.18)
        hex_shape = RegularPolygon(n=6, radius=1.4, color=BRAND_LIME, stroke_width=6).shift(UP * 1.8)
        hex_shape.set_fill(BRAND_LIME, opacity=0.22)
        circle = Circle(radius=1.4, color=YELLOW, stroke_width=6).shift(UP * 1.8)
        circle.set_fill(YELLOW, opacity=0.22)

        self.play(Create(sq), run_time=0.6)
        self.play(ReplacementTransform(sq, hex_shape, rate_func=rate_functions.ease_in_out_cubic), run_time=0.8)
        self.play(ReplacementTransform(hex_shape, circle, rate_func=rate_functions.ease_in_out_cubic), run_time=0.8)

        # Phase 2: Dynamic Function Graph with ValueTracker
        axes = Axes(
            x_range=[-PI, PI, PI / 2],
            y_range=[-1.6, 1.6, 0.8],
            x_length=6.4,
            y_length=3.6,
            axis_config={"color": "#475569", "stroke_width": 3},
            tips=False,
        ).shift(DOWN * 2.1)

        freq_tracker = ValueTracker(1.0)
        amp_tracker = ValueTracker(0.8)

        wave_graph = always_redraw(
            lambda: axes.plot(
                lambda x: amp_tracker.get_value() * math.sin(freq_tracker.get_value() * x) * math.cos(0.5 * x),
                color=BRAND_LIME,
                stroke_width=6,
            )
        )

        moving_dot = always_redraw(
            lambda: Dot(
                axes.c2p(
                    1.2,
                    amp_tracker.get_value() * math.sin(freq_tracker.get_value() * 1.2) * math.cos(0.6),
                ),
                color=BRAND_CYAN,
                radius=0.12,
            )
        )

        self.play(Create(axes), Create(wave_graph), FadeIn(moving_dot), run_time=0.8)
        self.play(
            freq_tracker.animate.set_value(3.2),
            amp_tracker.animate.set_value(1.45),
            circle.animate.scale(0.82).set_color(BRAND_LIME),
            run_time=1.8,
            rate_func=rate_functions.ease_in_out_sine,
        )

        # Phase 3: Smooth Camera Zoom onto the wave peak
        self.play(
            self.camera.frame.animate.scale(0.75).move_to(axes.get_center()),
            run_time=0.9,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(
            self.camera.frame.animate.scale(1 / 0.75).move_to(ORIGIN),
            run_time=0.8,
            rate_func=rate_functions.ease_in_out_cubic,
        )


class MatrixNeuralTransformScene(MovingCameraScene):
    """
    Scene 2: Giải thích Ma trận Trọng số (Weight Matrix) & Biến đổi Không gian Vector
    trong AI / Mật mã học.
    """

    def construct(self) -> None:
        self.camera.background_color = BRAND_BG

        title = Text("MA TRẬN TRỌNG SỐ & BIẾN ĐỔI VECTOR", font="Arial", weight="BOLD", font_size=32, color=BRAND_LIME)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=0.7)

        # Input Vector X, Weight Matrix W, Output Vector Y
        mat_w = IntegerMatrix([[2, -1], [1, 3]], v_buff=0.7, h_buff=0.9).scale(0.85).shift(UP * 2.2 + LEFT * 1.5)
        mat_w.set_color(BRAND_CYAN)
        vec_x = IntegerMatrix([[4], [2]], v_buff=0.7).scale(0.85).next_to(mat_w, RIGHT, buff=0.45)
        vec_x.set_color(WHITE)
        arrow = Arrow(LEFT * 0.3, RIGHT * 0.5, color=BRAND_LIME, buff=0.1).next_to(vec_x, RIGHT, buff=0.3)
        vec_y = IntegerMatrix([[6], [10]], v_buff=0.7).scale(0.85).next_to(arrow, RIGHT, buff=0.3)
        vec_y.set_color(BRAND_LIME)

        self.play(FadeIn(mat_w, shift=UP * 0.2), FadeIn(vec_x, shift=UP * 0.2), run_time=0.7)
        self.play(Create(arrow), FadeIn(vec_y, scale=1.2), run_time=0.7)

        # Linear transformation grid below
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5.6,
            y_length=5.6,
            background_line_style={"stroke_color": "#38BDF8", "stroke_width": 2, "stroke_opacity": 0.45},
        ).shift(DOWN * 1.9)

        basis_i = Arrow(plane.c2p(0, 0), plane.c2p(1, 0), buff=0, color=BRAND_LIME, stroke_width=6)
        basis_j = Arrow(plane.c2p(0, 0), plane.c2p(0, 1), buff=0, color=YELLOW, stroke_width=6)
        grid_group = VGroup(plane, basis_i, basis_j)

        self.play(Create(plane), Create(basis_i), Create(basis_j), run_time=0.8)
        self.play(
            grid_group.animate.apply_matrix([[1.3, 0.35], [-0.25, 1.15]], about_point=plane.get_center()),
            run_time=1.6,
            rate_func=rate_functions.ease_in_out_cubic,
        )


class CryptoCube3DScene(ThreeDScene):
    """
    Scene 3: Khối Lập Phương 3D (Hypercube / Cryptography Block) xoay trong không gian 3 chiều.
    """

    def construct(self) -> None:
        self.camera.background_color = BRAND_BG
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3], x_length=6, y_length=6, z_length=6)
        outer_cube = Cube(side_length=2.6, fill_opacity=0.15, fill_color=BRAND_CYAN, stroke_color=BRAND_LIME, stroke_width=3)
        inner_cube = Cube(side_length=1.3, fill_opacity=0.35, fill_color=BRAND_LIME, stroke_color=WHITE, stroke_width=2)

        self.play(Create(axes), Create(outer_cube), Create(inner_cube), run_time=1.0)
        self.begin_ambient_camera_rotation(rate=0.45)
        self.play(
            outer_cube.animate.rotate(PI / 2, axis=UP),
            inner_cube.animate.rotate(-PI / 2, axis=RIGHT).scale(1.25),
            run_time=2.2,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.stop_ambient_camera_rotation()


SCENE_MAP = {
    "FunctionGraphMorphScene": FunctionGraphMorphScene,
    "MatrixNeuralTransformScene": MatrixNeuralTransformScene,
    "CryptoCube3DScene": CryptoCube3DScene,
}


async def synthesize_tts(text: str, voice: str, out_mp3: Path) -> None:
    import edge_tts

    out_mp3.parent.mkdir(parents=True, exist_ok=True)
    comm = edge_tts.Communicate(text, voice, rate="+12%")
    await comm.save(str(out_mp3))


def main() -> None:
    parser = argparse.ArgumentParser(description="Manim Motion Explainer Studio CLI")
    parser.add_argument(
        "--scene",
        choices=list(SCENE_MAP.keys()),
        default="FunctionGraphMorphScene",
        help="Built-in Manim Explainer Scene to render",
    )
    parser.add_argument(
        "--script-file",
        type=str,
        default="",
        help="Optional custom Python file containing a Manim Scene",
    )
    parser.add_argument(
        "--scene-class",
        type=str,
        default="",
        help="Scene class name when using --script-file",
    )
    parser.add_argument(
        "--aspect",
        choices=["9:16", "16:9"],
        default="9:16",
        help="Video aspect ratio: 9:16 (vertical 1080x1920) or 16:9 (horizontal 1920x1080)",
    )
    parser.add_argument(
        "--quality",
        choices=["l", "m", "h"],
        default="m",
        help="Render quality: l (480p15), m (720p30), h (1080p60)",
    )
    parser.add_argument("--tts-text", type=str, default="", help="Optional Vietnamese narration text to mux")
    parser.add_argument("--voiceover", type=str, default="", help="Optional existing voiceover MP3/WAV to mux")
    parser.add_argument("--output", type=str, required=True, help="Final output MP4 path")
    args = parser.parse_args()

    out_path = Path(args.output).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    media_dir = out_path.parent / "_manim_build"

    if args.aspect == "9:16":
        if args.quality == "l":
            res_arg = "540,960"
            fps = 30
        elif args.quality == "m":
            res_arg = "720,1280"
            fps = 30
        else:
            res_arg = "1080,1920"
            fps = 30
    else:
        if args.quality == "l":
            res_arg = "854,480"
            fps = 30
        elif args.quality == "m":
            res_arg = "1280,720"
            fps = 30
        else:
            res_arg = "1920,1080"
            fps = 30

    target_py = Path(args.script_file).resolve() if args.script_file else Path(__file__).resolve()
    target_scene = args.scene_class if (args.script_file and args.scene_class) else args.scene

    raw_video_out = out_path.with_suffix(".raw.mp4") if (args.tts_text or args.voiceover) else out_path

    cmd = [
        sys.executable,
        "-m",
        "manim",
        "render",
        str(target_py),
        target_scene,
        "-r",
        res_arg,
        "--fps",
        str(fps),
        "--media_dir",
        str(media_dir),
        "-o",
        str(raw_video_out),
    ]
    print(f"[Manim] Rendering {target_scene} ({res_arg} @ {fps}fps)...")
    subprocess.run(cmd, check=True)

    # Locate the rendered file if Manim placed it inside media_dir
    if not raw_video_out.exists():
        found = list(media_dir.rglob(raw_video_out.name))
        if found:
            shutil.copy2(found[0], raw_video_out)

    # Optional Voiceover Muxing
    voice_path: Optional[Path] = None
    if args.voiceover and Path(args.voiceover).exists():
        voice_path = Path(args.voiceover).resolve()
    elif args.tts_text:
        voice_path = out_path.with_suffix(".tts.mp3")
        asyncio.run(synthesize_tts(args.tts_text, "vi-VN-NamMinhNeural", voice_path))

    if voice_path and voice_path.exists() and raw_video_out != out_path:
        mux_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(raw_video_out),
            "-i",
            str(voice_path),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(out_path),
        ]
        subprocess.run(mux_cmd, check=True)
        raw_video_out.unlink(missing_ok=True)

    print(f"[OK] Manim Motion Explainer rendered at: {out_path}")


if __name__ == "__main__":
    main()
