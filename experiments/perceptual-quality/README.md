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

**Conditions.** Four displays, three comparisons, all against the aerial image. The condition
set is derived from the cue truth-table in `eng/03_PHYSICS/depth_cues.py`, not chosen by hand:

| | Display | Cues it gets right | Role |
|---|---|---|---|
| **A** | free-space real image at R | all except opacity | the product |
| **real** | physical object at the same X | all | **calibration** — what does our rig cost us? |
| **flat2d** | 2D screen physically at X | accommodation only | what does free space buy over 2D? |
| **farscreen** | 2D screen at the backdrop, angularly matched | none of the depth cues | the HP Dimension / Beam baseline |

`cues_distinguishing()` says A-vs-real should differ **only in opacity**, so any other
discrimination there measures *our optics* — ghosting, luminance mismatch, aberration. It is the
calibration cell and it caps how far any other cell can be trusted.

**Sweep** R = 0.7 / 1.3 / 2.5 m — strongest cues, the design point, and where accommodation is
predicted dead. Cut from six distances because `pq1_design.py` showed six needed **173 min per
subject**. Move the viewer, not the rig, so image-to-backdrop stays fixed.

**Sizing — computed, not guessed.** Run `python3 experiments/perceptual-quality/pq1_design.py`.
9 cells, Holm-corrected α = 0.0056:

- **21 subjects × 222 trials ≈ 44 min each, one sitting. 15.5 subject-hours total.**
- Cells predicted at ceiling (flat2d, farscreen — disparity is 44–670× threshold): 15 trials
  per cell, 8 subjects would do.
- The calibration cell wants a **null**, and a non-significant t-test is *absence of evidence,
  not evidence of absence*. It is tested for **equivalence (TOST, margin ±0.10)**, which needs
  21 subjects and 44 trials — the most demanding cell in the study, deliberately.

**Pre-registered before any data.** Primary: across-subject one-sided t vs 0.5 per cell, Holm.
Secondary: per-subject exact binomial. Report effect sizes and CIs for every cell including
nulls. **Fixed n, no peeking, no adding subjects after looking.**

**Prediction to falsify (from the model, not from hope):** A-vs-flat2d strongly discriminated at
*every* distance, because disparity stays 44× threshold even at 2.5 m — the distance sweep tests
the *accommodation* prediction, not the disparity one. A-vs-real near chance. If A-vs-flat2d is
at chance, the cue model is wrong and that is the most informative outcome available.

**Decision:** A > flat2d and A ≈ real → build the wedge. A ≈ flat2d → the free-space image is
buying nothing a screen at the same place cannot, **pivot**, and count it a win found for ~$215.
A ≉ real → fix the rig before believing any other cell.

**Rig:** full buildable spec, confound analysis and parts list in **`BENCH.md`** (~$215). Static —
no DMD, no tracking, no multiplane. The source **must be a physical 3D object, not a screen**: an
AIRR relay images whatever you feed it, so a flat source gives a flat aerial image and the
experiment tests nothing. Shares the bench with the η_RR measurement in
`experiments/aerial-imaging/README.md`, which must be taken **first** because it sets the
comparator dimming.

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
