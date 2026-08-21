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

## Experiment PQ-1 — Free-space vs. flat screen (the go/no-go for `docs/13`)

**Added 2026-08-21.** This is the experiment this file's own literature check calls out as
missing (*"no paper tests a controlled sweep of free-space, multi-viewer, angular-view-count
against presence/identity ratings — that experiment remains this project's own to run"*). Full
derivation and rationale in `docs/15_THE_ACCOMMODATION_BUDGET.md` §4; geometry from
`eng/03_PHYSICS/accommodation.py`.

**Why it is now first, not last.** `docs/15` shows a whole person fits inside one depth-of-field
slab at pod distance, so the within-subject focus cue does not exist and free space is not
differentiated from a screen *placed at the same distance*. Whether the remaining differences —
no substrate, walk-around, multi-viewer geometry — are worth a 15-engine ring is the single
cheapest question that can end the project, and finding 1 above (2401.02171) says it may not be.

**Conditions.** Same content, matched luminance, bezels masked, far wall ≥ 3 m:

| | Condition | Isolates |
|---|---|---|
| A | free-space real image at R | the product |
| B | flat screen at the same location R | the *distance*, not the free space |
| C | flat screen at the far wall, perspective-correct | the HP Dimension / Beam baseline |

**Sweep** R = 0.7 / 1.0 / 1.3 / 1.5 / 2.0 / 2.5 m. R = 1.3 m is the robust design point
(`robust_window()`); R = 2.5 m is where the model predicts the cue vanishes.

**Subjects.** n ≥ 12, naive, none told the hypothesis. Two-alternative forced choice A-vs-B and
A-vs-C at each R, plus a presence rating. Also run the familiar-viewer condition queued in
finding 2 above if any subject knows the depicted person — that is TAYF's real deployment case
and a strictly harder bar.

**Prediction to falsify:** discrimination strong at R ≤ 1.5 m, collapsing to chance by
R = 2.5 m where `background_cue < DOF_HALF`. At chance *everywhere* means the cue is not the
mechanism and no pod geometry rescues it.

**Decision:** A > B → build the wedge. A ≈ B > C → pivot to a far cheaper product, and count
that a win found for ~$300. A ≈ B ≈ C → stop.

**Rig:** static — no DMD, no tracking, no multiplane. Shares a bench with the η_RR measurement
in `experiments/aerial-imaging/README.md`; build once, take both numbers.

## Relationship to other branches

Every quantitative "how much X do we need" question elsewhere in `experiments/` (angular-resolution's channel count, voxel-display's voxel density, bandwidth's compression aggressiveness) should ultimately be answered against this branch's thresholds, not against engineering convenience alone.

## Literature check, Aug 2026 (55-60 of 208 unread PERCEPTION-tagged papers read in depth)

No paper gives the clean numeric threshold this branch wants ("N views is enough," "X% fidelity suffices for identity recognition"). Five papers give real, directionally useful, numerically-grounded evidence — full write-ups in `research/deepseek_research.md` Track 4:

1. **2401.02171 (strongest finding)** — a life-size, correctly-placed **flat 2D video cutout** (no volumetric geometry, no parallax) produced AR-HMD co-presence statistically indistinguishable from a full 3D avatar (5.2 vs 5.3 on a 7-point scale) while beating it significantly on fidelity (5.1 vs 3.7, p<.001). Untested for TAYF's actual free-space multi-viewer case (the study used one tracked viewpoint), but this is the single most actionable lead this project has for the engineering hypothesis. **New queued experiment: add a "flat 2D vs. volumetric, single viewer" condition to this branch's protocol before assuming full parallax reproduction is required.**
2. **2509.17748** — realistic avatars raise identification but also raise eeriness and lower appeal; critically, people are hardest on avatars of *themselves or people they know* — TAYF's actual deployment scenario, not the anonymous-stranger case most digital-human papers validate against. **New queued experiment: test identity-similarity protocols against familiar-viewer conditions, not just stranger recognition — a strictly harder and more relevant bar.**
3. **2503.20308** — 82.6% of viewers preferred expressive-but-100ms-mistimed lip motion over precisely-timed-but-flat motion. Gives `pipeline/transport/README.md`'s ~80ms latency budget a validated safety margin (vs. the classical 50ms-lead/220ms-lag audiovisual-sync JND) and suggests spending budget on motion-amplitude fidelity before timing precision if a tradeoff is forced.
4. **2511.08032 / 2510.03874** — distortion axes are perceptually unequal: reconstruction-view sparsity causes sharp threshold-like collapse rather than graceful decline; temporal jitter and UV-map compression are well-tolerated relative to texture/geometry distortion. Real, numeric, but on the *capture-side* reconstruction-view axis, not TAYF's *emission-side* display-channel axis — do not conflate the two when citing this.
5. **2409.08577** — confirms displaying the *remote* party (not the local user's own avatar) is what drives presence — validates TAYF's basic architecture, no fidelity number.

**Conspicuously missing from the literature:** no paper tests a controlled sweep of free-space, multi-viewer, angular-view-count against presence/identity ratings — the exact Track C×D intersection this branch needs most. That experiment remains this project's own to run, not something to find in the literature.

## Status

**2026-08-21: PQ-1 above is now the project's next physical action**, ahead of every
optical build task — see `docs/15` §4 and `docs/13` §13 risk 1.

Not started as an in-house measurement, but no longer a blank slate — three concrete, literature-motivated hypotheses are queued above (flat-2D-vs-volumetric for single-viewer use; familiar-viewer identity recognition) as the first experiments to run rather than starting from scratch. This is still the branch most likely to be neglected under hackathon time pressure because it doesn't look like "building the thing" — flagging explicitly that skipping it means every other branch is optimizing against a guess, not a measured target.
