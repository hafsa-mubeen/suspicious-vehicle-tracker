# Detection Evaluation Summary

## Setup

- Model: YOLOv8s (pretrained on COCO, no MOT fine-tuning)
- Sequence: MOT17-04-FRCNN (1050 frames, ~30k pedestrian annotations)
- Hardware: NVIDIA T4 GPU (Kaggle)
- Date: Day 3

## Confidence threshold sweep

| Metric           | conf=0.40 | conf=0.25 (chosen) |
|------------------|-----------|--------------------|
| True positives   | 18,063    | 22,294             |
| False positives  | 1,296     | 2,550              |
| False negatives  | 21,746    | 17,515             |
| Precision        | 0.933     | 0.897              |
| Recall           | 0.454     | **0.560**          |
| mAP@0.5          | 0.436     | **0.520**          |
| Average FPS      | 71.9      | **78.6**           |

## Operating point

We use **conf=0.25** as the project default. The 10.6-point recall gain
substantially outweighs the 3.6-point precision drop, and downstream pipeline
components (tracker + two-signal rule engine) tolerate spurious detections far
better than missed ones — a missed person is irrecoverable, while a false
positive typically fails the dwell + motion stagnation criteria within seconds.

## Honest caveats

- MOT17-04 is a dense pedestrian street, harder than typical CCTV.
- COCO-trained detectors systematically miss heavily-occluded and very small
  people; MOT-fine-tuned variants report ~0.75 recall but at considerable
  training cost. We deliberately skipped fine-tuning.
- MOT17 has only pedestrian annotations, so bicycle and motorcycle accuracy is
  evaluated qualitatively on real CCTV demo clips (Day 4).