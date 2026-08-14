# Perceptual Quality — Track D

Owns `docs/theory.md`'s Track D question: how little optical information does a human observer actually need to perceive convincing remote presence? This is the thinnest-covered track in `research/deepseek_research.md` relative to its importance to the whole project — most of the corpus so far documents *how to build* optical/representation systems, not *how much of them the human visual system actually requires*. This branch is where that gap gets closed empirically rather than left as an assumption.

## Why this is not optional polish

`docs/theory.md`'s engineering hypothesis is that convincing telepresence requires substantially less optical complexity than complete volumetric fidelity — but that hypothesis is currently unverified. Every other experimental branch (`voxel-display/`, `light-field/`, `angular-resolution/`) needs this branch's thresholds to know when to stop optimizing a dimension that no longer moves perceived quality.

## Protocol

1. **Identity similarity** — does the observer recognize *this specific person*, not just "a person," across representation-fidelity levels (`pipeline/avatar/README.md`'s compression settings).
2. **Depth perception** — measured depth-judgment accuracy against the optical engine's actual output (`hardware/optical-engine.md`), not assumed from the mechanism's theoretical capability.
3. **3D stability / motion realism** — does the reconstruction "boil," jitter, or flicker during natural motion, and at what point does that break presence.
4. **View consistency** — does the image stay coherent as the observer moves within the supported viewing cone (`docs/calibration.md`'s single-observer assumption's actual angular tolerance).
5. **Viewer preference** — direct comparative ratings across configurations (voxel density, view count, avatar compression level) to find the actual quality/cost knee points other branches should target.

## Relationship to other branches

Every quantitative "how much X do we need" question elsewhere in `experiments/` (angular-resolution's channel count, voxel-display's voxel density, bandwidth's compression aggressiveness) should ultimately be answered against this branch's thresholds, not against engineering convenience alone.

## Status

Not started. This is the branch most likely to be neglected under hackathon time pressure because it doesn't look like "building the thing" — flagging explicitly that skipping it means every other branch is optimizing against a guess, not a measured target.
