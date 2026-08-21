# 09 — Device Designs: the six forms the aperture law permits

**Reference date: 2026-08-16.** Follows from `docs/01_SYSTEM_MASTER_SPEC.md` §4.3b. This document exists because the project spent two days holding rule 6 (10 cm) fixed and rejecting every design that didn't fit it — including the ones that work. Relaxing rule 6 and holding the other nine produces buildable hardware immediately.

---

## 1. The law that sets every dimension

For an image in the viewer's own space (nearer than the device), light must reach the eye through the exit aperture:

**W_image ≤ D_aperture**

So **the aperture size decides the image size, and nothing else does.** Every design below is that sentence applied to a different viewing geometry. There is no cleverness available — pick the subject you want to show, and the aperture follows.

| Subject at life size | Minimum aperture |
|---|---|
| Head | 25 cm |
| Head + neck | 32 cm |
| Head + shoulders (bust) | 50 cm |
| Seated upper body | 80 cm |
| Standing full body | 170 cm |

**An aperture is an emitting *area*, not a solid volume.** Depth is set only by how far in front the image floats — not by the image size. This is why every design here is a slab rather than a box.

---

## 2. THE FINDING: zero moving parts

**The retroreflective (AIRR) and Pepper's-ghost routes contain no mechanism whatsoever.** The optics are static sheets of glass and film. The only dynamic element in the entire device is the pixels changing on a flat display panel — the same component in a phone.

This is a decisive practical advantage, and it is unique to this family:

| Approach | Moving parts | Consequence |
|---|---|---|
| Laser-plasma voxels | Galvo mirrors scanning at kHz | Wear, alignment drift, noise, cost |
| Acoustic trap (MATD) | A bead flown at 8.75 m/s | Bead loss, air-current sensitivity, 6-particle ceiling |
| Photophoretic trap | Galvos + focus-tunable lens | Class-4 laser, alignment, particle handling |
| Swept volume (Voxon) | A physically spinning screen | Noise, vibration, sealed housing, service life |
| **AIRR / Pepper's plate** | **None** | **Silent, no wear, no calibration drift, no consumables** |

Consequences worth stating explicitly:

- **Silent.** No fan for scanner electronics, no rotor, no ultrasound. It can sit beside a conversation.
- **No wear-out mechanism.** Service life is the display panel's, not a bearing's.
- **No alignment drift.** Static optics bonded once at assembly; nothing to recalibrate in the field.
- **No consumables.** No beads to reload, no medium to replenish, nothing to inhale.
- **Trivially safe.** No laser above indicator level, no plasma, no high-intensity ultrasound. Rule 10 is satisfied by construction rather than by engineering controls.
- **Cheap to manufacture.** Sheet optics and a commodity panel.

**This is why the design family survives while everything else in this project died.** It isn't better physics — it's the same aperture law — but it asks nothing of mechanism.

---

## 3. How AIRR actually works (and how it differs from Pepper's ghost)

Both are static. They are **not** interchangeable, and the difference decides rule 4.

**Pepper's ghost** — display + one angled beamsplitter. The viewer sees a **virtual** image, apparently *behind* the glass. Cheap at any size, wide viewing angle. **Fails rule 4**: the person is on the far side of a plane, not in your space.

**AIRR (Aerial Imaging by Retro-Reflection)** — display + beamsplitter + retroreflector sheet. Light from the display reflects off the beamsplitter onto the retroreflector, which returns it along its incoming path; it passes through the beamsplitter and **converges to a real image floating in front of the device, in the viewer's own space.** Unit magnification. **Satisfies rule 4.**

Three static elements, no mechanism:

1. **Source panel** — commodity LCD/OLED
2. **Beamsplitter** — half-mirror glass or film at 45°
3. **Retroreflector** — microstructured corner-cube or bead sheet (static, but a specialist part)

### Honest caveats

- **Optical efficiency is poor.** The beamsplitter costs ~50% on each pass, so ~75% of source light is lost before the image forms. The source panel must be bright. This is a power-budget item, not a blocker.
- **Viewing cone — CORRECTED 2026-08-16, and it is far better than this document previously claimed.** Yamamoto, *J. Imaging Soc. Japan* **56**(4) 341–351 (2017), DOI `10.11370/isj.56.341` — **open access on J-Stage, not paywalled** — measures **170° left–right** for AIRR, and reports >2.2× gain for polarised AIRR plus image position independent of retroreflector shape and placement. **[PUBLISHED]**
  The ~±20–30° figure previously stated here was wrong: it belongs to **ASKA3D / MMAP micro-mirror-array plates**, a *different* aerial-imaging mechanism (measured ~40°, DOI `10.3390/jimaging11050150`). Conflating AIRR with MMAP is an error this document made and now corrects. **AIRR is materially the better choice**, and at 170° the product is much closer to a walk-around image than the "conversational cone only" framing used throughout earlier revisions.
- **Unit magnification, for CONVENTIONAL AIRR.** Image size = source size, exactly — and this is a **theorem, not a measurement**: the composition of plane reflections is a Euclidean isometry, so `M = 1` by geometry. This is why aperture = image size for this family. **Two named exceptions exist** — LeAIRR and Fresnel-AIRR do magnify, at the cost of the viewing angle and an optic several times larger than the image (`docs/11` §4.1). `[Corrected 2026-08-21 per docs/11 §7.]`
- **Retroreflector cost scales with area.** Small formats are cheap; a 170 cm plate is not.
- **The precise folding arrangement for the portable unit is unresolved.** AIRR needs three surfaces in fixed relative geometry; collapsing that into a book-sized hinge is real mechanical design work, not yet done.
- **The AIRR primary literature is now READ — and it was never paywalled.** Yamamoto, *J. Imaging Soc. Japan* **56**(4) 341–351 (2017), DOI `10.11370/isj.56.341`, is open access on J-Stage. Two independent passes read it in full and verified quoted strings against the Japanese original. This closes what was, for two days, recorded as this project's largest unverified block — and it was closed by looking in the right place, not by getting institutional access. A cautionary result for `research/METHODOLOGY.md`.
- **What genuinely remains unmeasured is the absolute photometric transfer**: aerial-image cd/m² per source cd/m², i.e. the retroreflector return efficiency η_RR. Every source-luminance and panel-power figure in this project rests on it, and no published source states it. One afternoon with a spot luminance meter at V0 closes it. **[UNVERIFIED — the single highest-value measurement available]**

---

## 4. The six designs

All modelled at true scale in `models/build_models.py`; renders in `models/png/`.

### 06 — Folio (portable) ⭐ *the bag-sized answer*
**Aperture 30 × 21 cm (A4) · closed 30 × 21 × 7 cm · 4.4 L**
Shows a **life-size human head**. Folds to a hardback book; fits any laptop bag. A4 is the smallest bag-friendly aperture that still shows a face at true scale — which is what a video call frames anyway. A 45° plate lies flat when closed and stands when opened.

### 03 — Disc
**Aperture 50 cm dia · depth 12 cm · 24 L**
Life-size head and shoulders. Wall-mountable or on a slim stand. The cheapest fixed-installation entry point.

### 01 — Mirror
**Aperture 55 × 175 cm · depth 20 cm**
Life-size **standing** person. Off-state is a mirror — an object already present in homes at exactly the required dimensions, and already permitted to be a reflective surface. No screen aesthetic at all.

### 02 — Doorway
**Aperture 80 × 200 cm · depth 14 cm**
A person standing in the door frame. Uses pre-existing architecture as the aperture. Best for offices and shared spaces, where a doorway already means "a person might be there."

### 04 — Shop window
**Aperture 240 × 220 cm (existing glass) · 60 cm backstage**
Life-size person appearing on the pavement side of the glass. Retrofits infrastructure that already exists in every city: a large vertical sheet facing pedestrians, with power and a hidden backstage. Pepper's ghost is the right technology here — cheap per m² at scale.

### 05 — Command table
**Aperture 150 × 150 cm, HORIZONTAL · depth 35 cm**
Terrain and battlespace floating above the surface, viewable from all sides, no headsets.

**The geometry inversion:** a table-top plate *fails* for consumers because a seated viewer looks horizontally and sees it edge-on. It *works* here because operators stand and look **down**, so the plate faces them squarely. Same physics, opposite verdict, purely from viewing direction. Adjacent legitimate uses on identical hardware: mission rehearsal, training, remote expert assistance, forward telemedicine.

---

## 5. Technology selection

| Scale | Technology | Why |
|---|---|---|
| ≤1 m², consumer | **AIRR** | Real image in the viewer's space (rule 4); small area absorbs the retroreflector cost |
| 2–50 m², advertising | **Pepper's ghost** | Negligible cost per m²; virtual image acceptable when the viewer is a passer-by |
| Horizontal, multi-viewer | **Swept volume** | The one geometry where genuine 360° walk-around works |

---

## 6. What none of these solve

Stated plainly so the documentation cannot be mistaken for the dream being met:

- **A device is visible behind the person.** The image genuinely floats in open air with nothing at its location, but the emitting surface is in view. No geometry removes this — light must come from somewhere, and that somewhere must be as wide as the person.
- **Rule 6 is broken in every case.** The 10 cm cube shows a 10 cm object. That is the law, not a limitation of these designs.
- **Viewing cone is wide, not narrow** — 170° measured for AIRR (§3). The earlier ±20–30° claim confused AIRR with ASKA3D/MMAP plates (~40°) and is withdrawn.

What they do satisfy: **rules 1, 2, 3, 4, 5, 7, 8, 9 and 10 — nine of ten — with commodity parts, no moving components, and no safety envelope to engineer.**

---

## 7. Next actions

1. **Obtain the AIRR primary literature** (Optics Express, OSA Continuum, Optical Review) and replace every reasoned figure in §3 with a measured one. This is the largest open item in the document.
2. **Resolve the folio's three-surface fold** — the mechanical design that collapses AIRR's fixed geometry into a book-sized hinge.
3. **Source a retroreflector sheet and a beamsplitter** and build the disc (design 03) first — it is the simplest static configuration and validates the whole family.
4. **Measure real optical efficiency** against the ~75% loss predicted in §3, and size the source panel from the measurement rather than the estimate.
