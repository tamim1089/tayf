# 15 — The Accommodation Budget

**Reference date: 2026-08-21.** Corrects `docs/13_THE_ROOM.md` §7, §10 and §13, deletes the
project's most expensive component, and replaces the top risk with a cheaper and more dangerous
one.

**Model:** `eng/03_PHYSICS/accommodation.py` — run it, don't trust this page.
**Tests:** `eng/08_VERIFY/tests/test_accommodation.py` — 31 pinned values.

---

## 1. The error, and why it was easy to make

Doc 13 §7 sized the depth planes like this: *a 1 m deep volume, 30 planes, 33 mm steps*. That
is a **geometric** division of space. It led directly to a 2,700 Hz plane-switch requirement,
to deformable mirrors at $10k–50k each, and to the focus element being ranked risk 1.

The eye does not resolve depth in millimetres. It resolves depth in **diopters** — reciprocal
metres — and the reciprocal is brutal. Depth resolution collapses with distance as `1/R²`.

Let `t` be a subject's front-to-back depth and `R` the viewer's distance to its centre:

```
span(R, t) = 1/(R − t/2) − 1/(R + t/2)     ≈  t / R²
```

| R | head (t=0.25) | shoulders (t=0.35) | body (t=0.60) |
|---|---|---|---|
| 0.50 m | 1.067 D | 1.595 D | 3.750 D |
| 0.70 m | 0.527 D | 0.762 D | 1.500 D |
| 1.00 m | 0.254 D | 0.361 D | 0.659 D |
| **1.20 m** | **0.176 D** | **0.248 D** | **0.444 D** |
| 1.50 m | 0.112 D | 0.158 D | 0.278 D |
| 2.50 m | 0.040 D | 0.056 D | 0.097 D |

Against a human depth of field of roughly **±0.30 D**, i.e. 0.60 D total `[ASSUMED — see §5]`,
one slab is not millimetres thick:

| R | slab | thickness |
|---|---|---|
| 0.70 m | 0.58 → 0.89 m | 308 mm |
| 1.00 m | 0.77 → 1.43 m | 659 mm |
| 1.20 m | 0.88 → 1.87 m | 993 mm |
| 1.50 m | 1.03 → 2.73 m | **1693 mm** |
| 2.50 m | 1.43 → 10.0 m | 8571 mm |

**A whole person fits inside a single accommodation slab at every pod distance.**

## 2. What that deletes

`planes_needed(R, t) = ⌈span / 0.6 D⌉`, floored at 1:

| R | head | shoulders | body |
|---|---|---|---|
| 0.70 m | 1 | 2 | **3** |
| 1.00 m | 1 | 1 | 2 |
| **1.20 m** | **1** | **1** | **1** |
| 1.50 m | 1 | 1 | 1 |
| 2.50 m | 1 | 1 | 1 |

**One plane at the design point. Never more than three anywhere. Doc 13 said 24–32.**

Consequently, and all void: the 2,700 Hz requirement, the deformable-mirror pricing, the
TAG-lens and PB/FLC-stack investigation, and the entire "which swept-focus element" question
that dominated the last two design rounds. **The engines are fixed focus.** The BOM line does
not shrink — it disappears (`docs/13` §10, corrected).

The external review that flagged the varifocal as the BOM's serious error was right that the
number was wrong and wrong about the direction. Repricing the component was not the fix.

## 3. The window nobody would have guessed

Two constraints pull in opposite directions:

- **Too close.** `span ∝ t/R²`, so at R = 0.70 m a body spans 1.5 D and needs **3** planes.
- **Too far.** The cue that differentiates a free-space image from a screen is the diopter gap
  to the nearest surface *behind* it, `1/R − 1/wall`. That falls as `1/R`, and past
  **R ≈ 2.0 m** it drops below threshold — the free-space advantage is then not subtle, it is
  **physically absent**.

Both are satisfied only in a band. `design_window()` returns, for a full body with the pod wall
2z behind the image:

| pod radius z | R window | engines `N = 2πz/D` at D = 0.5 m |
|---|---|---|
| 1.2 m | **1.05 – 1.85 m** | **15** |
| 1.5 m | 1.05 – 2.00 m | 19 |

### 3.1 And it survives the assumption

`DOF_HALF` is the one `[ASSUMED]` number holding this up, so it is swept rather than trusted:

| DOF_HALF | R window |
|---|---|
| 0.20 D | 1.30 – 2.65 m |
| 0.25 D | 1.15 – 2.25 m |
| 0.30 D | 1.05 – 2.00 m |
| 0.40 D | 0.95 – 1.60 m |
| 0.50 D | 0.85 – 1.35 m |

The window **never closes**, and the intersection of all of them is non-empty:

> ### R = 1.30 – 1.35 m works for every depth-of-field figure in the range.

`robust_window()`. This is the practical answer to resting a product on an unverified number:
**pick a design point inside the intersection and the geometry cannot be invalidated** by
whatever the bench measures. The measurement can change the *size* of the effect. It cannot
move the pod. Design point: **R ≈ 1.3 m, z = 1.2 m, N = 15.**

## 4. The risk this creates, which is worse than the one it removed

If the subject fits in one focal slab, the within-subject focus cue is gone — you will **not**
see the nose in front of the ears.

### 4.0 ⚠ But "free space ≈ a flat screen" was wrong — added 2026-08-21

The first draft of this section concluded that free space is therefore not differentiated from
a flat screen at the same distance. **That skipped stereopsis, and stereopsis is the cue that
actually carries depth.** `eng/03_PHYSICS/depth_cues.py`:

Both cues scale identically — `accommodation = t/R²` diopters, `disparity = b·t/R²` radians —
so the ratio of their suprathreshold margins is a **constant, independent of `R` and `t`**:

```
stereo_margin / accommodation_margin  =  b · 2·DOF_HALF / θ_threshold  =  268×
```

(804× at a 10″ threshold, 134× at a generous 60″.) At the design point a body is **0.62×**
threshold to accommodation and **168×** threshold to stereopsis.

| R | body: accommodation | body: stereopsis |
|---|---|---|
| 0.7 m | 2.50× | 670× |
| **1.3 m** | **0.62×** | **168×** |
| 2.5 m | 0.16× | 44× |

**So the correct statement is:** against a **2D** screen, free space wins decisively — on
disparity, by 44–670×. Against a **stereo** screen serving one tracked viewer, it wins on
neither focus nor disparity. The honest hierarchy of what free space uniquely buys:

1. **Multi-viewer** — the only cue `depth_cues.py` finds that a tracked stereo screen cannot
   match, because such a screen serves exactly one viewer by construction. HP Dimension is
   explicitly one-on-one. **This is the irreducible claim and the pitch should lead with it.**
2. **No eyewear.**
3. **No substrate** — no bezel, frame, or surface texture betraying the plane.
4. **Walk-around** past any screen's cone.
5. **Comfort** — no VAC over a long call. Comfort, not depth.

This also re-reads **arXiv 2401.02171** more favourably than §4 first did. Its "flat 2D cutout"
was *correctly placed in 3D space* in an AR headset, so it carried correct placement disparity
and lacked only *within-object* volumetric structure. The finding is therefore "internal
volumetric geometry is unnecessary; correct spatial placement is what matters" — which is
independent support for exactly what doc 15 derived from diopters, and is a threat to
volumetric *fidelity*, not to TAYF's architecture. `[Read at repository-note level from
`experiments/perceptual-quality/README.md`, not from the paper. Verify before quoting.]`

Whether that is worth a 15-engine ring is an empirical question, and the literature already
carries a warning. `experiments/perceptual-quality/README.md` records **arXiv 2401.02171**: a
life-size, correctly-placed **flat 2D cutout** produced co-presence statistically
indistinguishable from a full 3D avatar (**5.2 vs 5.3** on a 7-point scale) while *beating* it
on fidelity (**5.1 vs 3.7, p<.001**).

**Risk 1 is therefore no longer a build risk.** It is: *can anyone tell?*

### 4.1 The experiment — three conditions, one afternoon of subjects

Same content, matched luminance, bezels masked, at R = 0.7 / 1.0 / 1.3 / 1.5 / 2.0 / 2.5 m,
far wall ≥ 3 m:

| | Condition | What it isolates |
|---|---|---|
| **A** | free-space real image at R | the product |
| **B** | flat screen at the same location R | is it the *distance*, or the *free space*? |
| **C** | flat screen at the far wall, perspective-correct | the HP Dimension / Beam baseline |

Naive subjects, n ≥ 12, none told the hypothesis. Two-alternative forced choice A-vs-B and
A-vs-C at each R, plus a presence rating. Log every field in `experiments/README.md`'s
research-notebook template.

**What each outcome buys:**

- **A > B** → the value is genuinely free-space. Build the wedge.
- **A ≈ B > C** → the value is *an image at the right distance*, obtainable far more cheaply
  than a 15-engine ring. **Pivot** — and this is a good outcome, found for $300 instead of
  $128,000.
- **A ≈ B ≈ C** → 2401.02171 was right about the general case. Stop.

**Prediction to falsify:** discrimination should be strong at R ≤ 1.5 m and collapse to chance
by R = 2.5 m, where `background_cue < DOF_HALF`. If it is at chance *everywhere*, the cue
is not the mechanism and no pod geometry rescues it.

**Bench note:** build it static — no DMD, no tracking, no multiplane. A beamsplitter plus
retroreflective sheet (AIRR, `docs/11` §2.3, M = 1) or a concave mirror imaging a 50–80 mm
bright object is enough. Measure **η_RR** at the same bench while it is set up; it is flagged in
`experiments/aerial-imaging/README.md` as never measured anywhere and every brightness figure
in this project depends on it, including `docs/13` §4's assumed 5% efficiency.

## 5. Status of every number here

| Quantity | Status |
|---|---|
| `span = 1/(R−t/2) − 1/(R+t/2)` and `≈ t/R²` | **[DERIVED]** — geometric optics, re-derivable |
| `dof_slab`, `planes_needed`, `background_cue`, `N = 2πz/D` | **[DERIVED]** — code + 31 tests |
| Design window, robust window | **[DERIVED]** — `design_window()`, `robust_window()` |
| **`DOF_HALF = ±0.30 D`** | **[ASSUMED]** — literature-typical for a ~3 mm pupil, **not verified against a primary source in this repository.** Swept 0.20–0.50 D; conclusions hold across the range. |
| Plane spacing of one full DoF | **[ASSUMED]** — consistent with multifocal-display practice (0.6–0.9 D with depth blending); not verified here |
| `t` = 0.25 / 0.35 / 0.60 m | **[ASSUMED]** — anthropometric estimates, not from a table |
| arXiv 2401.02171 figures | **[PUBLISHED]** — inherited from `experiments/perceptual-quality/README.md`, not re-read here |

## 6. Scope — which architectures this correction touches

`research/METHODOLOGY.md` rule 3: a constraint must be scoped to the architecture it applies to.

| Architecture | Affected? |
|---|---|
| `docs/13` THE ROOM — refractive real-image engines | **Yes.** Swept focus deleted; engines fixed focus; N = 15 at the design point. |
| `docs/02` §11.5 Layout E — laser-plasma voxel engine | **No.** Its axial focus modulator places the *laser focus* so air ionises at the intended voxel — a generation requirement, not a perceptual one. It stays. *(An earlier revision of this document's rollout flagged that component for removal. The flag was wrong; recorded here and at `docs/02` §11.5 per rule 4.)* |
| `docs/11` TAYF-C35 — AIRR cube | **Not yet checked.** AIRR is a single-plane relay with no focus element, so there is probably nothing to remove, but the *viewing distance* analysis in §3 may bear on where a C35 should sit. Open. |

The distinction that matters: doc 15 removes focus elements whose job is **placing accommodation
planes for the eye**. It says nothing about focus elements whose job is **putting energy at a
point in space**. Confusing the two would be the same class of error this document exists to fix.

**The honest summary:** the *relative* conclusions — one plane not thirty, a window that exists,
a design point that survives the sweep — follow from geometry and are robust. The *absolute*
threshold for whether a human notices is an assumption, and §4.1 is the experiment that
replaces it with a measurement.
