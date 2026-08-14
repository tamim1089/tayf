# Camera Rig Design

**Status: open, not finalized.** This is currently the top blocking hardware decision after the optical engine choice.

## Capture volume

Target: a single seated adult in a chair, roughly 0.6m × 0.6m × 1.2m volume in front of the cube, cube placed at approximately chest-to-eye height on a side table or the chair's own armrest per the original concept ("place it on a chair"). Boundaries are user-adjustable via `app/` at session start — the phone app sets the capture box, not a fixed hardware FOV.

## Why multiple cameras, not one

Monocular pose/face/hand estimators (GVHMR/HaMeR/SMIRK-class, per `pipeline/capture/README.md`) can run from a single RGB stream, but a single fixed camera on a 10cm cube sitting beside a chair will lose the far side of the body to self-occlusion during natural movement (turning, leaning, gesturing). A 3-4 camera array tiled across two adjacent cube faces gives enough angular coverage to keep the subject's face and both hands in at least one view through normal conversational motion, without requiring room-scale capture infrastructure.

## Candidate layout

- 2 cameras front face (stereo baseline ~6-8cm — the practical limit inside a 10cm enclosure once the optical engine and edge SoC claim their volume), angled slightly outward for wider combined coverage than a single wide-FOV lens would give at equal resolution.
- 1-2 cameras on an adjacent face for oblique/profile coverage, reducing occlusion loss during head turns.

## FOV math (first pass, to refine once sensor is chosen)

For a subject at ~1.0-1.5m from the cube (typical chair-to-side-table distance) and a target capture volume ~0.6m wide, each camera needs roughly 40-50° effective horizontal FOV per lens to keep the full seated envelope in frame at the near end of that range, with margin for the user-adjustable boundary to shrink the working volume rather than requiring the optics to zoom.

## Sync

Hardware-triggered sync (shared trigger line from the edge SoC or a small sync IC) across all sensors — required for the pose estimators to treat multi-view frames as time-coincident; software-only sync (timestamp matching) is not acceptable given the sub-100ms end-to-end latency budget the rest of the pipeline already achieves (Mon3tr: ~80ms).

## Open items

1. Confirm exact sensor FOV/resolution once `hardware/bom.md`'s vendor pass is rerun — this doc's angles are working assumptions, not measured.
2. Validate occlusion coverage empirically once the remote RTX 5060 dev rig has *any* camera hardware attached — nothing here has been tested against real capture.
3. Reconcile camera placement with `hardware/enclosure.md`'s physical layout (camera modules compete for cube-face real estate with the optical engine panel).
