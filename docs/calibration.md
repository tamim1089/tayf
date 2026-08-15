# Spatial Registration and Calibration

> ### ⚠ SUPERSEDED IN PART — read [`docs/10_TAYF_UNIVERSAL_ENGINEERING.md`](10_TAYF_UNIVERSAL_ENGINEERING.md) first
>
> This document predates the current design and is kept as a **detail source and historical record**, not as a specification. Where it disagrees with document 10, document 10 wins. Specifically superseded:
> - **The device is not a 10 cm cube.** It is a family of flat apertures (20 cm slab → A4 folio → 50 cm disc → chair → mirror), sized by the aperture law. Depth is dead weight; every form is a slab.
> - **The engine is static AIRR optics**, selected. Free-space plasma, acoustic and photophoretic routes were all evaluated and ruled out with quantitative reasons (doc 10 §9).
> - **The "~85% / ~15%" framing is retired.** It described a problem that no longer exists in that shape.
> - **Viewing angle is 170°**, measured (Yamamoto 2017, `10.11370/isj.56.341`) — not the ±20–30° stated in earlier revisions, which belongs to a different mechanism.
> - **Transport is delta + int8 at 0.104 Mbps**, measured — not fp16 + LZ4, whose assumed 0.6× ratio was tested and found to *expand* the payload.


Even though the display is free-space, the system must know *where* the apparent remote person is supposed to exist and *from which directions* they're being observed. This doc defines the coordinate system and the calibration flow that `hardware/optical-engine.md`'s renderer and `pipeline/avatar/README.md`'s animation stage both depend on.

## Coordinate frames

- **Cube coordinate system** — origin at the optical engine's nominal emission center, axes fixed to the physical enclosure (`hardware/enclosure.md`).
- **Capture volume frame** — the user-adjustable box set via `app/README.md`'s boundary-setting flow, expressed relative to the cube frame.
- **Remote human placement frame** — where the reconstructed avatar is anchored in the receiving cube's local space; by default coincides with the capture volume frame's "chair position" so the remote person appears to occupy roughly where the local user would expect a visitor to sit.
- **Observer frame** — the viewer's estimated head/eye position relative to the cube frame, needed to evaluate `L(x, y, z, θ, φ, t)` (`docs/theory.md`) for the directions that actually matter right now.

## Viewpoint dependency — observer position estimation

The renderer needs to know where the human observer is to decide which angular slice of the light field to prioritize (`docs/theory.md`'s "limited light" principle only pays off if the system knows which directions are occupied). Candidate methods, in order of implementation cost:

1. **Single-observer assumption** (hackathon-track default) — assume a fixed nominal viewing position in front of the cube; no active tracking. Cheapest, matches a light-field/AIP panel's inherent limited-angle design (`hardware/optical-engine.md`).
2. **Camera-based head/eye tracking** — reuse the same camera array doing local capture (`hardware/camera-rig.md`) to also track the local observer, since the observer of the *remote* avatar is the same person the local cube is capturing for transmission. This is close to free given the camera array already exists.
3. **Depth-based tracking** — only relevant if a depth sensor is added to the BOM (`hardware/bom.md`), not currently planned for the hackathon track.
4. **Multi-observer support** — explicitly deferred; the north-star optical engine (`hardware/optical-engine.md`) would need to serve multiple simultaneous angular slices, which materially increases the optical engine's required channel count. Not attempted before single-observer works.

## Calibration flow (one-time, per physical cube)

1. **Optical-engine geometric calibration** — map the optical engine's internal addressing (panel pixels, or eventual voxel/scan coordinates) to the cube coordinate frame. Panel-specific; deferred until `hardware/optical-engine.md`'s hackathon-track panel is sourced.
2. **Camera-to-cube extrinsics** — standard multi-camera extrinsic calibration (checkerboard or equivalent) once `hardware/camera-rig.md`'s physical layout is fixed.
3. **Capture-volume-to-avatar-placement mapping** — verify that a person captured within the app-set boundary reconstructs at the expected position/scale in the remote cube's frame.

## Open items

1. Nothing here has been implemented — this is the coordinate/flow specification other modules (`hardware/optical-engine.md`'s renderer, `pipeline/avatar/README.md`'s animation stage) are written against.
2. Observer-tracking accuracy requirements aren't quantified yet — depends on the hackathon-track optical engine's actual angular sensitivity, unknown until that panel is sourced (`hardware/bom.md`).
