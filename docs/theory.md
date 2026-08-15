# TAYF Theory — Core Hypotheses and the Optimization Framing

> ### ⚠ SUPERSEDED IN PART — read [`docs/10_TAYF_UNIVERSAL_ENGINEERING.md`](10_TAYF_UNIVERSAL_ENGINEERING.md) first
>
> This document predates the current design and is kept as a **detail source and historical record**, not as a specification. Where it disagrees with document 10, document 10 wins. Specifically superseded:
> - **The device is not a 10 cm cube.** It is a family of flat apertures (20 cm slab → A4 folio → 50 cm disc → chair → mirror), sized by the aperture law. Depth is dead weight; every form is a slab.
> - **The engine is static AIRR optics**, selected. Free-space plasma, acoustic and photophoretic routes were all evaluated and ruled out with quantitative reasons (doc 10 §9).
> - **The "~85% / ~15%" framing is retired.** It described a problem that no longer exists in that shape.
> - **Viewing angle is 170°**, measured (Yamamoto 2017, `10.11370/isj.56.341`) — not the ±20–30° stated in earlier revisions, which belongs to a different mechanism.
> - **Transport is delta + int8 at 0.104 Mbps**, measured — not fp16 + LZ4, whose assumed 0.6× ratio was tested and found to *expand* the payload.


Formalizes the theoretical framing from `research/notes.md` §3, §22, §50-56, §61-65. `docs/architecture.md` is the "what we're building" doc; this is the "why it should work" doc — read both together.

## The light-field formalism

The optical engine's target output is not "a 3D object" but a function:

**L(x, y, z, θ, φ, t)**

where `(x, y, z)` is spatial position, `(θ, φ)` is viewing direction, and `t` is time. The system does not need to physically illuminate every point equally in every direction — it needs to emit only the light necessary to produce the correct perceptual image from the viewing directions that are actually occupied by an observer. This is the "limited light" insight and it is the single most important cost-reduction lever available to the optical-engine design (`hardware/optical-engine.md`, `docs/calibration.md` for how `L` gets estimated at runtime).

## Why this is not "a projector"

A projector performs `image → photons → physical surface`. TAYF's optical stage performs `3D representation → controlled optical field → free-space image`. Photons need something to interact with to become visible; a conventional display has no free-space output mode. This is why the project's real research object is a *free-space optical engine* (`hardware/optical-engine.md`), not a display driver.

## Two decoupling moves that make the 10cm constraint tractable

1. **Representation vs. transmission.** Persistent identity (shape, face, skin, hair, clothing) is captured once; only dynamic state (pose, expression, gaze, hand articulation) is transmitted per frame (`pipeline/avatar/README.md`, `pipeline/schema.py`). This is a solved, measured decoupling (Mon3tr: 215 floats/frame, <0.2 Mbps).
2. **Physical optical volume vs. perceived image scale.** The cube does not need to physically contain a human-sized volumetric emitter. Optical magnification, aerial imaging, angular expansion, view synthesis, and holographic wavefront reconstruction can all decouple a small physical engine from a larger apparent result. This decoupling is *not* solved — it is the actual open research question (`hardware/optical-engine.md` §3.1's ranked mechanism table).

## The four research tracks

| Track | Question to solve | Status | Owning doc |
|---|---|---|---|
| A — Human Representation | What is the smallest representation that preserves identity, body motion, face, and hands? | Solved (Mon3tr, GETA-3DGS) | `pipeline/avatar/README.md` |
| B — Communication | What is the smallest dynamic state transmittable at conversational quality? | Solved (215 floats/frame, <0.2Mbps, ~80ms) | `pipeline/transport/README.md` |
| C — Free-Space Optics | How much spatial/angular optical information can a 10cm optical engine generate? | **Open** | `hardware/optical-engine.md` |
| D — Perception | How little optical information does a human observer actually need to perceive convincing presence? | Open, understudied. **Checked Aug 2026** (55-60 papers read): no clean numeric threshold found, but the single strongest lead in either research pass is real — see below | `docs/theory.md` (this doc) + `experiments/perceptual-quality/README.md` |

The breakthrough, if there is one, most likely comes from the interaction between C and D — not from either alone. A physically sparse optical engine (Track C's likely ceiling for years) becomes viable exactly to the extent that Track D's threshold for "convincing presence" is lower than "complete volumetric fidelity." This is why Track D is not optional academic polish — it is the lever that makes Track C's hard physics survivable on a useful timeline.

## The strongest lead so far on the engineering hypothesis

A dedicated literature check of Track D (arXiv 2401.02171, an AR-HMD telepresence study) found that a life-size, correctly-placed **flat 2D video cutout** — no volumetric geometry, no view-dependent parallax at all — produced co-presence statistically indistinguishable from a full rigged 3D avatar (5.2 vs 5.3 on a 7-point scale), while beating the 3D avatar's fidelity rating by a wide, significant margin (5.1 vs 3.7, p<.001). This is not proof the engineering hypothesis holds for TAYF specifically — the study used a single tracked viewpoint in a headset, not a free-space multi-viewer display, so it says nothing about whether TAYF's optical engine can skip parallax information for simultaneous viewers. But it is real, numerically clean evidence that *for single-viewer conversational presence*, spatial placement and photographic fidelity may matter more than volumetric structure — exactly the kind of result this hypothesis needs, tested at the wrong device class. `experiments/perceptual-quality/README.md` now queues a direct flat-2D-vs-volumetric test as its first experiment rather than starting from nothing.

## The three testable hypotheses

1. **Scientific hypothesis:** a remote human can be perceptually reconstructed in free space using a physically compact optical engine if the human is represented by a sufficiently efficient dynamic neural representation and the optical system emits only perceptually necessary spatial/angular information.
2. **Engineering hypothesis:** the optical complexity required for convincing human telepresence is substantially lower than the complexity required to reproduce a human's complete volumetric light field at uniform fidelity. This motivates perceptual rendering, adaptive quality, sparse optical channels, and neural view interpolation (`pipeline/view_synthesis/README.md`) over brute-force volumetric emission.
3. **Central optimization problem:** maximize perceived telepresence subject to cube volume ≤ 1000cm³, bandwidth ≤ ~0.3 Mbps, latency ≤ 150ms, power/thermal ≤ what a sealed enclosure can reject (`hardware/power-thermal.md`), and laser/optical safety constraints (`hardware/optical-engine.md` §safety). Every hardware and software decision in this repo is a constrained choice inside this optimization, not an independent one.

## Perceptual allocation

Not every part of a human needs equal representation fidelity. Allocate more of both the representation budget (`pipeline/schema.py`'s parameter budget) and the optical-engine's angular/spatial budget to face, eyes, mouth, and hands; allocate less to occluded regions, low-saliency clothing, and off-axis-from-current-viewpoint geometry. This is a standing design principle across `pipeline/avatar/README.md` and `hardware/optical-engine.md`, not a one-time optimization pass.

## What a first prototype should actually prove

Solve the optical engine before solving photorealistic human capture — a human is a bad first optical test target (skin, hair, cloth, expression, identity all compound the difficulty at once). The correct experimental order is point → line → plane → simple 3D object → rotating object → symbol/text → face → hand → head → upper body → full human, each stage isolating what's newly being tested. See `experiments/README.md` for the concrete protocol.
