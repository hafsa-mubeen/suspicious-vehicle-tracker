"""
Sanity check: run detector on a frame from a demo clip.
Usage:
    python scripts/test_clip_detection.py clips/clip_01_atm_loitering.mp4
    python scripts/test_clip_detection.py clips/clip_01_atm_loitering.mp4 --t 60
"""

import sys
import argparse
from pathlib import Path
import cv2

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.detection.detector import Detector


def main(clip_path: str, frame_offset_seconds: float = 30.0):
    cap = cv2.VideoCapture(clip_path)
    if not cap.isOpened():
        print(f"ERROR: Could not open {clip_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0

    print(f"Clip: {clip_path}")
    print(f"  FPS: {fps:.2f}")
    print(f"  Total frames: {total_frames}")
    print(f"  Duration: {duration:.1f}s")

    target_frame = int(frame_offset_seconds * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
    ret, frame = cap.read()
    if not ret:
        print(f"ERROR: Could not read frame at {frame_offset_seconds}s")
        return

    print(f"\nGrabbed frame at {frame_offset_seconds}s (frame #{target_frame})")
    print(f"  Frame shape: {frame.shape}")

    print("\nRunning YOLOv8s detection...")
    detector = Detector(weights="yolov8s.pt", conf_threshold=0.25, device="cpu")
    detections = detector.detect(frame)

    print(f"\nDetected {len(detections)} target-class objects:")
    for d in detections:
        x, y, w, h = d["bbox"]
        print(f"  - {d['class']:12s} conf={d['confidence']:.2f}  bbox=({x:.0f},{y:.0f},{w:.0f},{h:.0f})")

    annotated = frame.copy()
    for d in detections:
        x, y, w, h = d["bbox"]
        x1, y1 = int(x), int(y)
        x2, y2 = int(x + w), int(y + h)
        color = (0, 255, 0) if d["class"] == "person" else (255, 0, 0)
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
        label = f"{d['class']} {d['confidence']:.2f}"
        cv2.putText(annotated, label, (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    output_path = Path("_scratch") / f"sanity_{Path(clip_path).stem}_t{int(frame_offset_seconds)}.jpg"
    output_path.parent.mkdir(exist_ok=True)
    cv2.imwrite(str(output_path), annotated)
    print(f"\nAnnotated frame saved to: {output_path}")

    cap.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("clip_path", help="Path to the .mp4 clip")
    parser.add_argument("--t", type=float, default=30.0, help="Frame offset in seconds (default 30)")
    args = parser.parse_args()
    main(args.clip_path, args.t)