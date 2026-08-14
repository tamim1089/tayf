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

## Status

Not started — blocked entirely on panel sourcing. First actionable branch once task #9 resolves.
