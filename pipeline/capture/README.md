# Capture Module

Responsibility: turn 3-4 synchronized camera streams (`hardware/camera-rig.md`) into a `pipeline/schema.py` `DrivingState` packet, per frame.

## Estimators (candidate stack, per research/deepseek_research.md Track 2)

- **Body pose:** GVHMR-class monocular estimator → `DrivingState.body_pose` (75 dims).
- **Facial expression:** SMIRK-class estimator → `DrivingState.face_expression` (50 dims).
- **Hand pose:** HaMeR-class estimator → `DrivingState.hand_pose` (90 dims, both hands).

Mon3tr (arXiv 2601.07518) runs these three in parallel on PC-class hardware at 71-377fps individually, synchronizing to ~58fps overall (13.78ms worker execution, 2.13ms sync, 1.27ms smoothing). Those numbers are not yet validated on the Jetson-class edge SoC TAYF targets — first real benchmarking task once hardware arrives.

## Segmentation / matting

BiRefNet (MIT) for foreground/background separation within the user-set capture boundary from `app/README.md`, before pose estimation — keeps the estimators focused on the subject, not the room behind them.

## Inputs

Synchronized frames from the hardware-triggered camera array (`hardware/camera-rig.md`), timestamp-matched via the shared trigger line (`firmware/README.md`).

## Outputs

One `pipeline/schema.py::DrivingState` per frame, handed to `pipeline/transport/`.

## Open items

1. No benchmarking has been done on target embedded hardware — everything above is projected from PC-class published numbers.
2. Capture-boundary enforcement (cropping to the user-set box from the phone app) needs a concrete implementation once `app/README.md`'s pairing/boundary flow is built.
