# Avatar Module

Responsibility: (1) one-time offline enrollment building a personalized canonical Gaussian avatar, (2) per-frame animation of that avatar from an incoming `pipeline/schema.py::DrivingState`.

## Avatar model — license decision

**Use Anny (NAVER, Apache-2.0) or MHR (Meta's Momentum Human Rig), not SMPL-X.** SMPL-X is the de-facto research standard and is what most cited papers in `research/deepseek_research.md` actually use, but its license is non-commercial — unusable for anything beyond a research demo that never ships. This is project task "Commit to license-clean avatar model" and it needs to be resolved before capture-pipeline code is written against a specific rig, not after.

## Enrollment (offline, on the remote RTX 5060 — never on the deployed cube)

One-time per-user capture (~1-2 min video per Mon3tr's reference) builds a personalized 3D Gaussian avatar bound to the chosen parametric template. Mon3tr reports ~33s build time on non-embedded hardware; this step never runs on the deployed cube's edge SoC.

## Runtime animation (on-cube, both sender-side enrollment-adjacent and receiver-side rendering)

Given an incoming `DrivingState`, deform the canonical Gaussian set via linear-blend-skinning driven by `body_pose`, plus attribute corrections for expression (`face_expression`) and hand articulation (`hand_pose`). Compression of the *canonical* avatar itself (not the per-frame stream) can draw on GETA-3DGS (arXiv 2605.02086, ~5x storage reduction) or the prior-guided framework in arXiv 2510.10492 (<0.26 Mbps at 25fps for the combined canonical+driving representation).

## Open items

1. License decision (above) blocks writing real animation code against a specific rig's joint/blendshape topology.
2. On-device (Jetson-class) animation performance is unvalidated — same caveat as `pipeline/capture/README.md`.
3. Enrollment UX (how a first-time user gets their ~1-2 min capture) is not designed — belongs partly to `app/README.md`.
