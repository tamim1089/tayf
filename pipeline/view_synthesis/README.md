# View Synthesis Module

Implements `research/notes.md` §20's core idea: **few physical optical views → neural interpolation → many apparent views**. This may be the single highest-leverage software component for making a physically sparse optical engine (the realistic outcome of `hardware/optical-engine.md`'s hackathon and even north-star tracks) perceptually convincing.

## The research question this module exists to answer

What is the minimum number of physical optical channels required when neural rendering fills the angular gaps between them? This is not answered yet — it depends on the optical engine chosen (`hardware/optical-engine.md`) and the perceptual threshold work in `experiments/perceptual-quality/README.md`. This module is built to be tested against that question empirically, not designed around an assumed answer.

## Position in the pipeline

```
pipeline/avatar/  --(animated canonical Gaussian avatar, full 3D)-->
pipeline/view_synthesis/  --(sparse set of rendered/physical views + interpolation)-->
hardware/optical-engine.md's driver
```

Sits between avatar animation and the optical-engine driver: takes the fully-animated 3D avatar state and produces exactly the angular/spatial optical information the chosen optical engine can physically emit — not more (wasted compute), not less (visible gaps).

## Candidate approach

1. Render the animated Gaussian avatar (`pipeline/avatar/README.md`) from N physical view directions matching the optical engine's actual output channels (N is engine-specific — e.g. a light-field panel's native view count, or a laser-plasma engine's per-scan-pass angular sampling).
2. For any angular gap the optical engine cannot physically address but the observer-tracking system (`docs/calibration.md`) indicates is relevant, use neural view interpolation between the nearest physical views rather than an additional real render pass — the interpolation network operates in angle-space, not in full 3D reconstruction space, keeping this stage cheap relative to `pipeline/avatar/README.md`'s animation cost.
3. Apply `docs/theory.md`'s perceptual allocation principle here too: interpolation quality budget goes to face/hands/eyes first.

## Starting point found (Aug 2026 literature sweep)

Don't build this from scratch. **arXiv 2506.08064** ("A Real-time 3D Desktop Display") is an already-working, open-source pipeline (altiro3D) doing exactly this module's job end-to-end: webcam → MiDaS monocular depth → view synthesis (their "FAST" or "REAL" geometric algorithm) → quilt assembly → Looking Glass Portrait output, and it explicitly names video conferencing as a target use case. Their own measured bottleneck is the depth-estimation CNN (>50% of runtime on a laptop GPU), not view synthesis itself — useful to know before optimizing the wrong stage. For driving the panel at higher view counts/framerates once this module needs to scale beyond that baseline, CoherentRaster (arXiv 2605.04509) and LFDPR (arXiv 2601.19901) are real-time Gaussian-splat/point rendering methods validated on actual light-field-panel hardware — see `experiments/light-field/README.md` for full detail on all three. Fork and accelerate 2506.08064's pipeline rather than designing this module independently.

## Open items

1. No implementation exists yet — next step is forking arXiv 2506.08064's open-source pipeline once `hardware/optical-engine.md`'s hackathon-track panel is sourced (task #9), since the physical view count/geometry it needs to target is engine-specific.
2. The minimum-physical-channels research question is untested; first real experiment belongs in `experiments/angular-resolution/README.md`.
3. 2506.08064's own bottleneck (monocular depth CNN inference) needs re-benchmarking on TAYF's actual Jetson-class edge SoC, not assumed from their laptop-GPU numbers.
