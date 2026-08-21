# 13 — THE ROOM: 360° free-space human telepresence, rules suspended

**Status:** active design brief. Written 2026-08-21.
**Scope note:** `thedream.md` rules 4 (no window), 6 (ten centimetres) and 8 (no projector,
no screen, no retroreflector, no room modification) are **deliberately suspended** for this
document by the project owner. Everything else — no headset, no glasses, life-size, photoreal,
free-space, 360° — is retained. This describes a *different product* from `docs/11_THE_CUBE.md`
(TAYF-C35), which remains the rules-compliant design. Both are kept.

**Business, legal, logistics and the full cost stack are in `docs/16_BUSINESS_LEGAL_AND_LOGISTICS.md`.**

**Read `docs/14_TELEHUMAN_AND_THE_PATENT_GAP.md` alongside this.** It corrects §11's moat claim,
and it records that Queen's University built the broadcast version of this architecture in 2018
(TeleHuman 2): 275 projectors needed for 360°, 45 affordable, 59° delivered, onto an acrylic
cylinder at 10 FPS. That is the empirical price of not pupil-steering, and it corroborates §3.

**Audience:** another AI picking this up cold. All formulas are given so you can re-derive
rather than trust. Every number here is derived in-document except where marked `[UNVERIFIED]`.

---

## 1. The one law that governs everything

An image point floating in mid-air is only visible from directions the display's aperture
actually occupies. This is the clipping theorem (Smalley et al., *Nature* **553**, 486, 2018)
and it has no exception except matter at the image point.

Precisely: an optic of aperture width `D` at distance `z` from the image point `P` makes light
converge to `P` and diverge past it. The diverging light fills a cone whose half-angle is
`arctan(D / 2z)`. So a single aperture serves an angular wedge

```
α ≈ D / z          (radians, small-angle)
```

To be seen from all around, the wedges must tile the full circle:

```
Σ αᵢ ≥ 2π     ⟹     Σ Dᵢ ≥ 2π·z
```

**This is the whole design constraint in one line.** With the optics at `z = 2.5 m` from the
image, you need `2π × 2.5 = 15.7 metres of aperture width` arranged around the volume.
The number of engines is

```
N = 2π·z / D
```

Note `N` does **not** depend on how far away the viewer stands — only on the aperture-to-image
distance and the aperture size. Three independent derivations (angular wedges, viewer-ring
patch width, and étendue in §3) all land on the same `N`, which is a good sign the number is real.

### 1.1 The lever this exposes

`N ∝ z / D`. You reduce the machine by **moving the optics closer and making them wider**, not
by making the room bigger. Consequences:

| Form | z | D | N engines | Aperture band |
|---|---|---|---|---|
| Large room | 3.5 m | 0.25 m | 88 | 22 m |
| Standard room | 2.5 m | 0.25 m | **63** | 15.7 m |
| Booth / pod | 1.5 m | 0.40 m | **24** | 9.4 m |
| Tight pod | 1.2 m | 0.50 m | **15** | 7.5 m |

**The correct product is a booth, not a room.** A 3 m diameter pod needs ~24 engines; a 7 m room
needs ~88. Same physics, 4× the cost. This falls straight out of the math and should drive the
industrial design.

**Design point, fixed 2026-08-21 by `docs/15`:** the perceptual analysis independently drives
`z` down to the same place the geometry does, and pins the viewer distance too. Use
**z = 1.2–1.5 m, D = 0.5 m → N = 15–19 engines**, with the viewer at **R ≈ 1.3 m**. That R is
the *robust* window — it satisfies the design conditions for every depth-of-field figure between
0.20 D and 0.50 D, so the pod dimensions do not depend on which one is right.

### 1.2 Vertical coverage

Same law in elevation. A band of optic of height `h` at distance `z` covers `β ≈ h/z`. For
±20° of vertical parallax (enough for standing/sitting difference and for a child and an adult
to both look right): `h = 0.70 × z`. At `z = 2.5 m`, `h = 1.75 m`.

**Total passive optic area** = `15.7 m × 1.75 m ≈ 27 m²` for the room, `≈ 6.6 m²` for the pod.

---

## 2. Architecture that follows

```
        ┌──────────── ceiling ring: N steered engines ────────────┐
        │                                                          │
   [HOE band]                                                 [HOE band]
   passive relay          ╭───────────────╮                  passive relay
   1.75 m tall            │  free-space   │                  1.75 m tall
   covering 360°          │  image volume │                  covering 360°
                          │  1 m ⌀ × 2 m  │
        │                 ╰───────────────╯                         │
        └──────────── floor: tracking cameras, IR ──────────────────┘
```

- **Engines** (`N` of them): each produces a wavefront that converges to real focus points in
  mid-air. Not a normal projector — a normal projector has one flat focal plane. You need
  either a phase SLM computing a hologram, or a fast binary modulator (DMD) plus a fast
  focus-changing element sweeping depth planes. §7 covers the choice.
- **Passive band**: a holographic optical element or relay film on the walls that turns each
  engine's output into the correct converging wavefront at its assigned azimuth. Passive optics
  are ~100× cheaper per square metre than active ones — put all the *area* in passive and all
  the *modulation* in a small number of active engines.
- **Tracking**: IR head/eye tracking of every person in the room, ≥120 Hz, <5 ms latency.
- **Render node**: local GPU. Renders each present eye's view of the remote person.

---

## 3. The information budget (étendue), and why tracking is the whole game

Étendue `G = A · Ω` (area × solid angle) is conserved and is the true currency.

**Brute force — broadcast to everywhere at once:**
- Apparent emitting area of a person `A ≈ 0.9 m²` (projected silhouette, not full skin area)
- Solid angle for 360° azimuth × 40° elevation: `Ω = 2π · 2sin(20°) = 4.3 sr`
- Required `G = 0.9 × 4.3 = 3.9 m²·sr`
- One 1080p phase SLM delivers `G ≈ (15 mm)² × 0.2 sr = 4.5×10⁻⁵ m²·sr`
- **Ratio ≈ 87,000 SLMs.** Dead.

**With pupil tracking — send light only where eyes actually are:**
- 4 people × 2 eyes = 8 pupils. Eyebox 50 × 50 mm each (tolerates tracking error and small
  head motion between updates), at 2.5 m: `Ω_eye = 2.5×10⁻³ / 2.5² = 4×10⁻⁴ sr`
- Total `Ω = 8 × 4×10⁻⁴ = 3.2×10⁻³ sr`
- Required `G = 0.9 × 3.2×10⁻³ = 2.9×10⁻³ m²·sr`
- **Ratio ≈ 64 SLMs.**

**Tracking buys a factor of ~1,350× in étendue.** It converts an impossible machine into a
merely expensive one, and it independently reproduces the `N = 63` from §1. This is the single
most important engineering decision in the whole system: *never broadcast, always steer.*

### 3.1 Pixel and data rate

Per eye view: person's silhouette at 1 mm resolution ≈ `9×10⁵` points ≈ 1 Mpix.
8 eyes × 1 Mpix × 90 Hz = **720 Mpix/s**, roughly three 4K120 streams. One modern workstation
GPU renders this for a Gaussian-splat or parametric avatar.

Brute force for comparison: 720 azimuthal views (0.5° spacing) × 1 Mpix × 90 Hz =
`6.5×10¹⁰ pix/s ≈ 1.6 Tb/s`. A rack of GPUs. Again: ~100× penalty for not tracking.

**Critical:** this is the *local render* rate. It is not the network rate. See §8.

---

## 4. The light budget — and the surprising result that light is free

Luminous flux needed to make an apparent surface of area `A` glow at luminance `L` into solid
angle `Ω`:

```
Φ = L · A · Ω
```

Target `L = 250 cd/m²` (about a computer monitor; a person lit in a normal room reflects
50–100 cd/m², so 250 reads as clearly present).

**Tracked delivery:** `Φ = 250 × 0.9 × 3.2×10⁻³ = 0.72 lm` delivered to all eight eyes.

End-to-end optical efficiency: phase SLM diffraction ~40%, HOE ~70%, relay ~80%, apodisation
and fill ~50% → ~11%. Be pessimistic and call it 5%.

```
Source flux = 0.72 / 0.05 = 14 lumens
```

**Fourteen lumens.** A phone flashlight is ~50 lm. Even at 0.5% efficiency it is 144 lm.

Brute-force broadcast for comparison: `Φ = 250 × 0.9 × 4.3 = 968 lm` at the image, `≈ 19,400 lm`
of source at 5% — two cinema projectors. Also not crazy.

**Conclusion: this display is not power-limited.** It is aperture-limited and étendue-limited.
Anyone who tells you a free-space 360° display needs enormous power is thinking of laser plasma
in air (which does, because air has no energy ladder to exploit — see `docs/12`). Refractive
real-image displays do not have that problem. Correct this misconception wherever it appears.

---

## 5. The ghost problem, and the one honest fix

There is **no matter at the image point**, so nothing blocks light. The image is purely additive.
You will see the wall through the person's chest, and the back of their head through their face.
This is not an engineering gap; it is a consequence of the physics and every matter-free
volumetric display in history has it (Downing 1996, Korevaar 1988, Smalley 2018, Ochiai 2015).

Contrast ratio as seen by a viewer:

```
C = (L_image + L_background) / L_background
```

A white wall in a 300 lux room sits at `≈ 300 × 0.8 / π = 76 cd/m²`. At `L_image = 250`,
`C = 4.3:1`. Visible and solid-ish, but translucent.

**The one real fix, and it only works because we already broke rule 8:** the walls are already
being modified. Make the wall band *actively dark* — an LCD shutter layer, e-ink, or simply a
matte black baffle behind the aperture band. Drop `L_background` to `2 cd/m²` and

```
C = (250 + 2) / 2 = 126:1
```

which reads as opaque. This is the theatre trick: a dark surround makes an additive image look
solid. It is why every convincing hologram demo you have ever seen is shot in a dark room.

**Design consequence: the pod must have controlled lighting.** Not pitch black — the *viewers*
can be lit, because their eyes adapt locally — but the background behind the image volume must
be dark from every viewing direction. In a cylindrical pod this is easy: the far wall is always
part of the aperture band, and the band can be black between its optical zones.

---

## 6. The one thing this beats every screen and every headset at

> ### ⚠ THIS SECTION LED WITH THE WRONG CUE. Corrected 2026-08-21.
> Kept rather than deleted, per `research/METHODOLOGY.md` rule 4.
> Model: `eng/03_PHYSICS/depth_cues.py`. Tests: `test_depth_cues.py` (20 tests).
>
> **Accommodation is the weakest depth cue the eye has.** Both cues scale
> identically with subject depth `t` and viewing distance `R` —
> `accommodation = t/R²` diopters, `disparity = b·t/R²` radians — so the ratio of
> their suprathreshold margins is a **constant, independent of distance and
> subject size**:
>
> ```
> stereo_margin / accommodation_margin  =  b · 2·DOF_HALF / θ_threshold  =  268×
> ```
>
> 804× at a 10″ stereoacuity threshold, 134× at a generous 60″. **Stereopsis
> outperforms accommodation as a depth sense by two to three orders of magnitude,
> everywhere.** At the design point a body is `0.62×` threshold to focus — flat —
> and `168×` threshold to stereopsis.
>
> So the claim below is not just weak, it is close to backwards. A display that
> gets disparity right and focus wrong is ~268× nearer correct than one that does
> the reverse — which is exactly why headsets work at all despite VAC, and why VAC
> is a **comfort** problem, not a **depth** problem. "Look past it and see it blur"
> is real but is a *subtle* effect, and `docs/15` shows it is unavailable at all
> beyond R ≈ 2 m.
>
> **What the pitch should actually lead with, in order of defensibility:**
> 1. **Multi-viewer.** A real image at a real location serves *every* viewer
>    correctly at once. A tracked stereo screen — including HP Dimension, which is
>    explicitly one-on-one — serves exactly one. `depth_cues.py` identifies this as
>    the **only** cue a tracked stereo screen cannot match. It is the irreducible claim.
> 2. **No eyewear, no headset.**
> 3. **No substrate** — no bezel, frame, or surface texture betraying the plane.
> 4. **Walk-around** past any screen's viewing cone.
> 5. *Then* comfort: no VAC, so no fatigue over a long call.
>
> Against a **2D** screen the free-space image also wins enormously on disparity
> (44–670× threshold). Against a **stereo** screen it does not. State which
> competitor you mean.

Because the light genuinely converges to a point at a real depth, **the eye focuses there.**
Accommodation and vergence agree. There is no vergence-accommodation conflict, which is the
root cause of headset fatigue and of the uncanny flatness of every 2D telepresence screen ever
built, including a very good one like Project Starline.

~~This is the demo-able, felt, non-technical difference. A viewer can look *past* the image and
see it blur, exactly as with a real object. Nothing on a screen does that. **Lead the pitch with
this**, not with "360°" — a customer cannot tell 360° from a good 2D screen in a photograph, but
they can feel focus in three seconds standing in front of it.~~

---

## 7. The key open engineering decision: the engine

> ### ⚠ THIS ENTIRE SECTION RESTED ON A WRONG PREMISE. Corrected 2026-08-21.
> It is kept rather than deleted, per `research/METHODOLOGY.md` rule 4.
>
> **The premise:** *"quantised depth (30 planes over a 1 m deep volume = 33 mm steps)."*
> That sizes the depth planes **geometrically**. The eye does not resolve depth in
> millimetres — it resolves it in **diopters**, and at pod distance one depth-of-field slab
> is *metres* thick:
>
> | R | one DoF slab (±0.3 D) | thickness | a whole body spans |
> |---|---|---|---|
> | 1.0 m | 0.77 → 1.43 m | 659 mm | 0.659 D |
> | 1.2 m | 0.88 → 1.87 m | 993 mm | 0.444 D |
> | 1.5 m | 1.03 → 2.73 m | 1693 mm | 0.278 D |
>
> **A whole person fits inside a single accommodation slab at every pod distance.** The
> correct plane count is **1** at the design point and never more than **3** anywhere in the
> usable range — not 24–32.
>
> Therefore, and all of it void:
> - the **2,700 Hz** plane-switch requirement,
> - the deformable-mirror and TAG-lens pricing that followed from it,
> - the ranking of the focus element as **risk 1** in §13,
> - and option **(b)**'s entire "swept focus" framing below.
>
> **What replaces it: fixed-focus engines.** No varifocal, no PB/FLC stack, no swept element.
> The BOM line disappears rather than shrinking. Derivation, code, and the design window in
> **`docs/15_THE_ACCOMMODATION_BUDGET.md`**; model at `eng/03_PHYSICS/accommodation.py`;
> values pinned in `eng/08_VERIFY/tests/test_accommodation.py` (31 tests).
>
> **The new risk 1** is not a build risk at all: whether the accommodation cue is *perceptible*
> at conversational distance. See doc 15 §4 and the §13 correction.

You need each engine to place real focus points at *arbitrary depths*, refreshed at 90 Hz.
A normal projector has one focal plane and cannot do this. Two candidates:

**(a) Phase SLM / computer-generated holography.**
LCoS phase modulator, compute a hologram whose reconstruction is the point cloud.
- Pro: full 3D per frame, arbitrary depth, continuous.
- Con: cost ($5k–15k each `[UNVERIFIED — get current Holoeye / Meadowlark quotes]`), speckle,
  low diffraction efficiency, and CGH compute cost. 63 × $10k = $630k of modulators alone. Dead
  at that price for a product; fine for the science prototype.

**(b) Fast binary modulator + swept focus (multi-focal-plane).** ~~*Recommended.*~~
**VOID — the swept element is not needed at all. See the correction box at the top of §7.**
The text below is kept as the record of the wrong reasoning; **do not build from it.** The
correct engine is (b) with the focus element simply removed: **DMD + fixed-focus relay.**

> ~~DMD at 10–20 kHz binary, plus a focus-tunable element (Optotune-class liquid lens ~1 kHz, or a
> deformable mirror, faster) sweeping 24–32 depth planes per frame.~~
> - ~~Required plane-switch rate: `30 planes × 90 Hz = 2,700 Hz`. Liquid lenses are marginal here;
>   deformable mirrors and acousto-optic lenses clear it. **This is the highest-risk component
>   and should be bench-tested first.**~~
- Pro: DMD engines are a commodity (~$1,000–1,500 in small volume), no speckle if LED-pumped,
  high efficiency. **This still holds, and is now cheaper without the focus element (~$900).**
- ~~Con: quantised depth (30 planes over a 1 m deep volume = 33 mm steps — coarse; depth-blending
  between adjacent planes is the standard fix and works).~~ **This "con" was the error: 33 mm is
  a geometric step, and the eye's step at 1.2 m is ~1000 mm.**

**Recommendation for a first build: (b) with fixed focus.** 15 × $900 ≈ $13.5k, against
63 × $10k of phase SLMs. The gap widened in our favour once the varifocal came out.

**Explicitly rejected: scanned beam.** A galvo/MEMS scanner draws ~10⁶–10⁷ points/s. You need
`8 eyes × 10⁶ points × 90 Hz = 7.2×10⁸ points/s`. Scanning loses by two orders of magnitude.
You need a *parallel* modulator. Do not revisit this.

---

## 8. Capture, network, and the latency trick that makes it work over distance

**Capture:** you cannot photograph a person from 360° with a few cameras. The realistic path is
a **pre-enrolled photoreal avatar** (3D Gaussian splat or parametric body model), driven live by
4–6 cameras in the sender's pod. The avatar carries the 360° appearance; the live cameras carry
only pose, expression, and hands.

**Network:** you transmit *avatar parameters*, not pixels. Order 2–10 Mb/s. Any 5G or fibre link
carries it. The 720 Mpix/s of §3.1 is generated **locally at the receiver**, never transmitted.

**The trick — decouple the two latencies:**

| Loop | Path | Budget | Consequence if violated |
|---|---|---|---|
| Parallax loop | local head tracker → local GPU → local engines | **< 20 ms** | image swims, breaks presence, nausea |
| Conversation loop | remote capture → network → local render | < 250 ms | awkward pauses, but tolerable |

Head motion is served entirely locally, so the parallax loop **never touches the network**.
Dubai↔London at ~120 ms one-way affects only the conversation loop, where humans already
tolerate it. This is why the architecture survives intercontinental distance and why a
naive "stream the light field" design does not.

Parallax budget breakdown: tracking 5 ms + render 11 ms (90 Hz) + display 4 ms ≈ 20 ms. Tight
but these are ordinary VR numbers; the industry hits them routinely.

---

## 9. Safety

Non-negotiable, and it will gate the product before any customer sees it.

- Beams **converge in mid-air and keep going into the room**, where people's eyes are. Every
  accessible point must be Class 1 under IEC 60825-1. `[UNVERIFIED — exact AEL must be computed
  per wavelength and pulse structure by a qualified assessor, not from memory.]`
- This strongly favours **LED or incoherent sources over lasers** even at a brightness cost.
  §4 shows you have ~1,000× of light headroom, so spend it on safety. Use LEDs.
- Tracking failure must fail *dark*, not fail *bright*. Watchdog on the tracker; kill emission
  on loss of lock.
- Depth-plane sweeping produces temporal structure — check flicker against photosensitive
  epilepsy guidance (IEC 61966 / ITU-R BT.1702 class review). `[UNVERIFIED]`

---

## 10. Bill of materials and cost (order-of-magnitude, pod configuration, N = 24)

| Item | Qty | Unit | Total |
|---|---|---|---|
| DMD engine + LED + ~~varifocal~~ **fixed-focus relay** + drive | ~~24~~ **15** | $900 | **$13,500** |
| HOE / relay band, 6.6 m² | 1 | $2,000/m² proto | $13,200 |
| Render node (2× workstation GPU + host) | 1 | — | $18,000 |
| Tracking (6× IR camera + illuminators + host) | 1 | — | $6,000 |
| Pod structure, blackout, acoustics, power, thermal | 1 | — | $25,000 |
| Calibration rig, cabling, integration labour | 1 | — | $30,000 |
| **Prototype BOM** | | | ~~≈ $128,000~~ **≈ $101,000** |
| **Volume BOM (100 units, HOE at $300/m², engine at $450)** | | | ~~≈ $55,000~~ **≈ $42,000** |

> **Corrected 2026-08-21 (`docs/15`).** The engine line was priced with a swept-focus element
> that §7 has since shown is not needed — a person fits in one depth-of-field slab at pod
> distance, so the engines are **fixed focus**. `N` also drops from 24 to **15** at the design
> point `z = 1.2 m, D = 0.5 m`. Both changes cut cost; neither was a negotiation with a vendor.
> The external review that flagged this line as the BOM's serious error was right that it was
> wrong, and wrong about the direction — repricing the varifocal was not the fix, **deleting it
> was.** Power falls with it: 15 × ~40 W + GPUs ~600 W + tracking ~200 W ≈ **1.4 kW**.

Installed sale price at 3–4× volume BOM: **$180k–$250k per pod**, and the product is sold in
**pairs** (a call needs two ends), so **$360k–$500k per relationship**.

Power: 24 engines × ~40 W + GPUs ~600 W + tracking/host ~200 W ≈ **1.8 kW**. One 20 A circuit.
Not a facilities problem. Thermal: 1.8 kW into a small pod *is* a facilities problem — budget
active cooling and quiet fans (a telepresence pod that roars is unsellable).

---

## 11. Business

**Category:** installed immersive telepresence, not consumer electronics. Nobody buys this for
their living room. The correct comparable is Cisco TelePresence (2006, ~$300k/room, sold
thousands into enterprise) — proof that a six-figure video-call room is a real market when the
experience clears a bar. Also relevant: Google Project Starline (screen-based, 2-person, no 360),
Proto Inc. (Pepper's-ghost box, ~$65k `[UNVERIFIED]`), Light Field Lab SolidLight (panel, not
free-space 360 `[UNVERIFIED]`), ARHT Media. **None of them do free-space 360° with correct
accommodation.** That is the whitespace.

**Buyers, ranked by willingness to pay:**
1. **Sovereign / diplomatic** — a head of state who will not fly. GCC governments buy this at
   list price and do not negotiate. Highest price, longest cycle, best logo.
2. **Energy / heavy industry remote expert** — one senior engineer serving many sites. Hard ROI:
   compare against travel cost and downtime hours. Easiest business case to write.
3. **Telemedicine specialist consults** — a specialist "present" at a regional hospital.
   Regulatory friction, but enormous volume if cleared.
4. **Luxury retail and flagship brand** — a designer or celebrity appearing in-store. Marketing
   budget, fast decisions, low technical scrutiny. **Best beachhead: they buy on wow.**
5. Museums, theme parks, memorials.

**MENA / GSMA angle (this is a GSMA MENA Ignite entry, so this matters):** a pod needs local edge
compute and a low-jitter link. That is exactly the anchor use case regional telcos (e&, du, STC,
Zain, Ooredoo) are hunting for to justify 5G SA and edge investment. Sell the pod *through* the
carrier: they provide colo, the network slice with QoS, and the enterprise relationship; you
provide hardware and software and take a revenue share. This is a materially easier
go-to-market for a solo founder than selling $250k boxes direct, and it is the pitch the judges
are primed to hear.

**Revenue model:** hardware sale (or 36-month lease) + per-pod SaaS ($2–4k/month for avatar
enrolment, calibration drift correction, updates) + per-minute session fee on high-value calls.
Recurring revenue is what makes it fundable; the hardware is the wedge.

**Moat:** four claimed pieces —
1. the HOE design that maps `N` engines onto 360° of aperture band,
2. the pupil-steering *scheduling* algorithm (which engine serves which eye, and the handoff as
   people walk — this is a hard real-time assignment problem and the hardest thing to copy),
3. the multi-plane depth-blending calibration that keeps 24 independently-aimed engines
   geometrically coherent to sub-millimetre,
4. the avatar enrolment pipeline.

> ### ⚠ Items 2 and 4 are anticipated. Corrected 2026-08-21 — see `docs/14` §5.
> The clause *"Items 1–3 are patentable"* originally stood here and **is false.** It is kept
> rather than deleted, per `research/METHODOLOGY.md` rule 4.
>
> - **Item 2 is anticipated by US11474597B2** (Google LLC, priority 2019-11-01, **active to
>   2040**): eye-tracked multiview display that *"renders a specific view for each detected eye
>   based on that eye's location"* and emits it *"only in the viewing zone where that eye was
>   detected."* This repository had **already found and verified it** at `docs/05` §3.4 row 28,
>   whose own reading states the anticipation in bold. This section was written without
>   consulting it — a process failure, recorded rather than quietly patched.
> - **Item 4 is anticipated** by Mon3tr (arXiv 2601.07518), per `docs/05` §3.8.
> - **Items 1 and 3 survive**, item 3 narrowed to multi-engine geometric coherence — depth
>   blending itself is standard in multifocal near-eye displays.
> - Anticipation blocks *patenting* item 2, not *using* it. Whether US11474597B2's angular-pixel-
>   array limitation excludes a ring of steered projectors is a claim-construction question for an
>   attorney. **Do not read "we can probably use it" as "we can own it."**

**Search first, and start from what is already in this repo:** `docs/05` §3.4 (observer-tracked
emission — the cluster that matters most) and §3.8 (academic anticipation), then `docs/14`
(TeleHuman 2 and Vertegaal's estate), then Korevaar & Spivey US 4,881,068 (`docs/12`), the USC ICT
360° light-field patents (Jones/Debevec/Bolas), Light Field Lab, and Sony's spatial-reality family.

---

## 12. The hackathon-scale demo — one wedge of the circle

You cannot build 24 engines before a deadline. You do not need to. The physics is **linear in
wedges**: `N = 2π·z/D` means one engine is exactly `1/N` of the product, with nothing hidden.

**Build one wedge:** one DMD engine + one varifocal + one HOE segment + one tracked viewer,
producing a floating life-size head with correct parallax and correct focus over a ~15–20° arc.
Cost ≈ $4,000. Time ≈ 6 weeks.

Then the claim you make on stage is honest, checkable, and strong:
> *"This is one of twenty-four identical wedges. The arc you are standing in is the product.
> The other twenty-three are the same part, bought twenty-three more times. Here is the equation
> that says so."*

That is a far better pitch than a rendering, because a judge can walk into the arc, look past
the head, watch it blur, and know it is not a screen.

---

## 13. Risks, ranked by what actually kills the project

1. ~~**Varifocal plane-switch rate (2,700 Hz).**~~ **RETIRED 2026-08-21 — the requirement was
   an artefact, see §7.** Replaced as risk 1 by: **is the accommodation cue perceptible at all?**
   Once the subject fits in one focal slab, free space is not differentiated from a flat screen
   *placed at the same distance* — what remains is the absent substrate, the walk-around, and
   multi-viewer geometry. `experiments/perceptual-quality/README.md` already records the
   published warning (arXiv 2401.02171: a flat 2D cutout scored co-presence **5.2 vs 5.3**
   against a full 3D avatar while beating it on fidelity 5.1 vs 3.7, p<.001). This is an
   *existence* risk, not a build risk, and it is the cheapest thing on this list to settle —
   ~$300 and two weeks. Do it before anything else. Protocol in `docs/15` §4.
2. **360° coverage cost.** `N = 2π·z/D` is unforgiving. Every centimetre you can shrink the pod
   or widen the aperture is money. Industrial design and optics must be co-designed, not
   sequenced.
3. **Ghost transparency.** Cannot be fixed, only managed with a dark surround (§5). If a
   customer requires an opaque person in a lit room, walk away from the deal.
4. **Eye safety certification.** Can kill the product at the last gate. Use LEDs, engage an
   IEC 60825-1 assessor early, design fail-dark.
5. **Multi-viewer handoff.** Two people crossing paths swap which engine serves which eye.
   Get the flicker/glitch behaviour right or the illusion collapses exactly when the room is busy.
6. **Avatar uncanny valley.** A geometrically perfect display of a slightly-wrong face is worse
   than a good 2D video call. Budget as much for the avatar as for the optics.
7. **Two-ended chicken-and-egg.** A pod is worthless alone. Sell in pairs, or seed hub pods in
   carrier facilities so a single-pod customer still has someone to call.

---

## 14. What a receiving AI must verify before relying on this

- Every formula in §1, §3, §4 is derived here — re-derive them, do not trust them.
- `[UNVERIFIED]` price points: Holoeye/Meadowlark SLM, Optotune/deformable-mirror switch rates,
  HOE $/m² at volume, Proto Inc. and Light Field Lab pricing and specs.
- `[UNVERIFIED]` IEC 60825-1 AEL figures and flicker guidance — must come from the standard or
  a qualified assessor, never from a language model's memory.
- Confirmed and safe to cite: Smalley et al., *Nature* **553**, 486 (2018); Jones, McDowall,
  Yamada, Bolas, Debevec, "Rendering for an Interactive 360° Light Field Display," SIGGRAPH 2007;
  Downing et al., *Science* **273**, 1185 (1996); Korevaar & Spivey, US 4,881,068 (expired);
  Yamamoto, AIRR, DOI 10.11370/isj.56.341.
- Project rule, inherited: **verify a citation or mark it UNVERIFIED.** This project was burned
  by fabricated references early. Do not repeat that.
