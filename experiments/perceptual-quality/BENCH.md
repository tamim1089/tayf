# PQ-1 Bench — buildable specification

Rig for `experiments/perceptual-quality/README.md` experiment PQ-1, which also
takes the η_RR measurement `experiments/aerial-imaging/README.md` has flagged as
never measured anywhere.

**Design point from the model:** `eng/03_PHYSICS/accommodation.py`,
`eng/03_PHYSICS/depth_cues.py`. **Statistics:** `pq1_design.py` (run it).
**Everything below is `[UNVERIFIED]` on price and `[DERIVED]` on geometry.**

---

## 1. Why an AIRR relay and not a display

The rig must produce a free-space image with **genuine binocular disparity**, not
a flat picture floating in air. `depth_cues.py` shows disparity is the cue that
actually separates free space from a 2D screen — 44–670× threshold, against
accommodation's 0.16–2.5×.

An AIRR relay images **whatever the source is**, at M = 1. Put a real 3D object
in as the source and the aerial image is a real 3D image with correct disparity
and parallax throughout its depth. Put a flat panel in and you get a flat image
and the experiment tests nothing.

> **The source object must be a physical 3D object, not a screen.** This is the
> single most important line in this document. An AIRR image of an LCD is a
> floating LCD picture, and comparing that against an LCD at the same location is
> a null by construction.

## 2. Optical layout

```
                                    ┌─ black velvet backdrop, ≥2.5 m ─┐
                                    │                                  │
   viewer ────── R ──────►  ✦ image at X          ╱ 45° beamsplitter   │
   (0.7 / 1.3 / 2.5 m)      (250 mm from BS)     ╱  200 × 200 mm       │
                                                ╱                      │
                                               ╱ ──── retroreflector ──┘
                                              ╱      200 × 200 mm
                              ┌──────────────╱
                              │  baffled source compartment
                              │  3D object, 60 mm, on a 250 mm arm
                              │  LED spot, PWM-dimmable
                              └──────────────
```

**Image position.** AIRR forms a real image mirror-symmetric about the
beamsplitter plane, so image-to-BS distance **equals** source-to-BS distance.
Set both to **250 mm**.

**Viewing cone.** Bounded by the beamsplitter's angular size at the image —
the same clipping law as `docs/13` §1:

```
half-angle = arctan((D/2) / d_BS)
```

| BS size D | half-angle at d_BS = 250 mm | full cone |
|---|---|---|
| 150 mm | 16.7° | 33° |
| **200 mm** | **21.8°** | **44°** |
| 300 mm | 31.0° | 62° |

200 mm is enough for a fixed-viewpoint 2AFC with margin, and leaves room for a
second observer at ±15° in the multi-viewer pilot. Larger is better and costs
more; do not go below 150 mm.

**To vary R, move the viewer, not the rig.** The image-to-backdrop distance then
stays fixed, so `background_cue(R) = 1/R − 1/(R + d_backdrop)` varies only in the
intended way. Mark three floor positions at 0.7 / 1.3 / 2.5 m.

## 3. The confounds this layout kills, and the one it does not

Every one of these was found by asking "what else differs between conditions?"
rather than by building first.

| Confound | Fix |
|---|---|
| Beamsplitter visible behind the aerial image but not behind a comparator | **Leave the BS and retroreflector in the path for every condition.** Comparators sit in front of the BS at X, so all conditions are viewed through the same glass against the same retroreflector. |
| Stray light from the lit source giving away the aerial condition | Baffle the source compartment; matte-black everything; check with the source lit and the BS masked — no glow may be visible. |
| A support stand under the physical comparators that the aerial image cannot have | **Support from directly behind, on the viewing axis**, with a thin black rod hidden by the object itself. This is why the main study is **fixed-viewpoint** — the trick fails off-axis. |
| Luminance mismatch (AIRR loses ~75% at the beamsplitter alone) | Measure the aerial luminance first (§5), then PWM-dim the comparators to match. **This is why η_RR must be measured before the psychophysics, not after.** |
| Subject learning the rig's sounds | Run the stepper on every trial including aerial-only ones, so the mechanism is acoustically identical in all conditions. |
| **Not fixed: the aerial image is additive and cannot occlude.** | Unfixable — it is the ghost limit (`docs/13` §5). It is the *only* cue `depth_cues.py` predicts should separate aerial from real, and is therefore measured rather than hidden. Use a dark backdrop so there is little behind the image to show through. |

## 4. Condition switching

`pq1_design.py` found that if a human has to move a screen between
presentations, switching dominates the trial and the study becomes infeasible.
So switching must be **mechanised and ~1 s**:

- A stepper-driven **3-position carousel** at X: `empty` (aerial), `figurine`
  (real), `panel` (flat2d). Rotating 120° takes about a second.
- The AIRR source LED is switched electronically, in anti-phase with the
  carousel.
- A microcontroller sequences the whole trial and logs timestamps, so trial
  order is randomised by software rather than by the experimenter — who must not
  know the condition either, if a second person is available to run subjects.

The `farscreen` condition is a fourth display at the backdrop, angularly matched,
always physically present and simply switched on.

## 5. η_RR measurement — do this first

Closes the open item in `experiments/aerial-imaging/README.md`.

```
η_RR = (aerial image luminance, cd/m²) / (source object luminance, cd/m²) / 0.25
```

The 0.25 divisor removes the beamsplitter's two-pass `r(1−r)` ceiling
(`docs/11` §2.4) so the number isolates the retroreflector.

1. Measure source-object luminance directly, LED at a fixed PWM setting.
2. Measure aerial-image luminance at the same PWM, on axis, at 0.7 m.
3. Repeat at ±5°, ±10°, ±20° to get the angular fall-off — AIRR's cone is
   quoted at 170° but that is a different geometry from ours.

**Instrument paths.** Borrowed spot luminance meter → `[MEASURED]`. Phone camera
in full manual mode (fixed ISO, shutter, WB), calibrated against a
known-luminance reference in the same frame → `[INDICATIVE]`. Record which was
used; `docs/13` §4's assumed 5% end-to-end efficiency depends on this number.

## 6. Parts

All prices `[UNVERIFIED]` — no vendor quotes obtained.

| Item | Spec | Est. |
|---|---|---|
| Beamsplitter | half-mirrored acrylic, 200 × 200 × 3 mm | $25 |
| Retroreflector | corner-cube or glass-bead sheeting, 200 × 200 mm | $15 |
| Source + comparator objects | **two identical** 3D-printed figurines, ~60 mm, matte | $20 |
| Comparator panel | 2.4–3.5″ IPS module, PWM-dimmable | $25 |
| Far screen | any spare monitor/tablet at the backdrop | $0 |
| Carousel | stepper + driver + 3-position arm | $45 |
| Controller | RP2040 or similar, sequencing + logging | $10 |
| Illumination | LED spot + constant-current PWM driver | $20 |
| Blackout | velvet / flock paper, ~2 m² | $25 |
| Structure | plywood or extrusion, fixings, baffles | $30 |
| **Total** | | **≈ $215** |

Photometry is borrowed or phone-based, so it adds nothing. This sits inside the
$150–400 band in the plan.

## 7. Build order

1. **Optics only** — source, BS, retroreflector. Confirm a visible aerial image
   at 250 mm. *If no image forms, nothing else matters; stop and fix alignment.*
2. **Blackout and baffles** — verify no glow with the source lit.
3. **η_RR** (§5). Sets the comparator dimming for step 5.
4. **Carousel and controller** — verify ~1 s switching and identical acoustics.
5. **Luminance matching** — dim comparators to the measured aerial luminance.
6. **Pilot, n = 2** (not naive — you and one other). Checks trial timing and that
   the task is answerable at all. **Not** data.
7. **Run**, per `pq1_design.py`: 21 subjects × 222 trials × ~44 min.

## 8. What this bench cannot answer

Stated so nobody over-reads the result:

- **Not the multi-viewer claim**, which `depth_cues.py` identifies as the
  irreducible advantage over a tracked stereo screen. The on-axis rod support
  and the 44° cone both break off-axis. A second observer at ±15° is a *pilot*,
  not a test.
- **Not life-size.** A 60 mm object at 1.3 m subtends 2.6°; a head subtends 11°.
  Angular size affects presence, so PQ-1 measures *discrimination*, not presence
  at product scale.
- **Not the wedge.** No DMD, no tracking, no engine ring. A PQ-1 pass licenses
  building the wedge; it does not de-risk it.
