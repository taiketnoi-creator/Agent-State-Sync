from __future__ import annotations

import argparse
from pathlib import Path

import cv2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--contact-sheet", action="store_true")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(str(args.video))
    if not capture.isOpened():
        raise SystemExit(f"Cannot open video: {args.video}")

    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = float(capture.get(cv2.CAP_PROP_FPS) or 0)
    duration = frame_count / fps if fps else 0
    if frame_count <= 0 or fps <= 0:
        raise SystemExit("Video metadata is unavailable")

    sample_count = max(2, args.count)
    positions = [round(i * (frame_count - 1) / (sample_count - 1)) for i in range(sample_count)]
    saved_frames = []
    for index, frame_number in enumerate(positions):
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ok, frame = capture.read()
        if not ok:
            continue
        timestamp = frame_number / fps
        filename = args.output / f"frame-{index:02d}-{timestamp:06.2f}s.jpg"
        cv2.imwrite(str(filename), frame, [cv2.IMWRITE_JPEG_QUALITY, 94])
        saved_frames.append((frame, timestamp))

    if args.contact_sheet and saved_frames:
        columns = 4
        thumb_width = 270
        thumb_height = 480
        rows = (len(saved_frames) + columns - 1) // columns
        sheet = cv2.copyMakeBorder(
            cv2.resize(saved_frames[0][0], (thumb_width, thumb_height)),
            0,
            thumb_height * rows - thumb_height,
            0,
            thumb_width * columns - thumb_width,
            cv2.BORDER_CONSTANT,
            value=(22, 22, 22),
        )
        for index, (frame, timestamp) in enumerate(saved_frames):
            row, column = divmod(index, columns)
            thumb = cv2.resize(frame, (thumb_width, thumb_height))
            cv2.putText(
                thumb,
                f"{timestamp:05.2f}s",
                (12, 34),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            y0, x0 = row * thumb_height, column * thumb_width
            sheet[y0 : y0 + thumb_height, x0 : x0 + thumb_width] = thumb
        cv2.imwrite(str(args.output / "contact-sheet.jpg"), sheet, [cv2.IMWRITE_JPEG_QUALITY, 92])

    capture.release()
    print(f"duration={duration:.2f}s fps={fps:.3f} frames={frame_count} output={args.output}")


if __name__ == "__main__":
    main()
