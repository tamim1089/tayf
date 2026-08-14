# Branch B — Directional Light-Field / Holographic Reconstruction

Corresponds to `hardware/optical-engine.md`'s hackathon track (light-field/retroreflective AIP panel). This is the highest-priority experimental branch — it's the one the Sep 13 demo actually depends on.

## Research questions

1. How many discrete views does the observer need before the display reads as convincingly 3D rather than a flat image with parallax artifacts?
2. Can directional control alone (no literal voxels in air) produce a convincing sense of depth for a moving, talking human, not just static test geometry?
3. How compact can the emitter/panel become while holding view count and resolution — directly informs whether the sourced panel can plausibly shrink toward 10cm in a later revision?
4. Can `pipeline/view_synthesis/README.md`'s neural interpolation fill missing angles well enough that a cheaper, lower-native-view-count panel performs like a denser one?

## Protocol (experiments 1-4 from `experiments/README.md`, this branch's version)

1. Single point/simple geometry rendered through the chosen light-field/AIP panel — measure achieved apparent depth and view count actually resolved (vs. panel's nominal spec).
2. Rotating object — measure whether rotation reads as physically consistent from a fixed observer position, or whether view-transition artifacts (banding, ghosting between adjacent views) are visible.
3. Observer walks across the panel's viewing cone — measure the angular range over which the image stays coherent (this bounds the "single-observer assumption" in `docs/calibration.md`).
4. Face/hand test target (experiment 5 from `experiments/README.md`) — first point at which this branch's protocol requires the real `pipeline/` avatar stack rather than synthetic test geometry.

## Prerequisites before this branch can start

- Panel sourced (`hardware/bom.md`, task #9 — the single blocking hardware decision for the whole project).

## Rendering pipeline is now de-risked (Aug 2026 literature sweep)

Three independent papers found in `hardware/optical-engine.md`'s literature-update pass answer this branch's "can consumer hardware drive a real many-view panel at practical framerates" question in the affirmative, with real hardware validation, not just simulation:

- **CoherentRaster** (arXiv 2605.04509) — real-time 3D Gaussian Splatting for light-field displays via subpixel-level rasterization; up to 87.7fps at 2K on a consumer GPU (~15x faster than naive per-view 3DGS), directly compatible with `pipeline/avatar/README.md`'s Gaussian-splat avatar representation.
- **LFDPR** (arXiv 2601.19901) — texture-based point rendering validated on an actual physical tilted-lens light-field-display prototype (the same device class as the hackathon-track panel), up to 8x faster than standard multiview rendering.
- **Real-time radiance-field rendering on commercial LFDs** (arXiv 2508.18540) — 228fps for 45-view quilts on a single RTX 5090, running on an actual commercial Looking-Glass-class panel; supports both Gaussian-splat and voxel avatar representations.

More directly actionable: **arXiv 2506.08064** ("A Real-time 3D Desktop Display") is an already-working, open-source (altiro3D) pipeline — single USB webcam → MiDaS monocular depth → view synthesis → Looking Glass Portrait — that explicitly names video conferencing as its target use case. It runs at only 10Hz on a laptop GPU (below smooth-video threshold, monocular-depth artifacts, no image-quality evaluation), so it's a starting point to fork and accelerate, not a finished solution — but it validates that this branch's entire pipeline, end to end, is buildable today rather than requiring new research. See `pipeline/view_synthesis/README.md` for how this changes that module's starting point.

## Status

Not started — blocked entirely on panel sourcing. First actionable branch once task #9 resolves. When it does, `arXiv 2506.08064`'s open-source pipeline is the recommended starting point to fork rather than building the capture→view-synthesis→panel path from scratch.
