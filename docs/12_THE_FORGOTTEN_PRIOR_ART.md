# 12 — The Forgotten Prior Art

**Reference date: 2026-08-16.** Findings from a six-territory search (`wf_b44f376c-fac`) into places this repository had never looked: pre-1996 literature, patents rather than papers, non-English venues, non-plasma air emission, and matter-at-the-point schemes. Five of six territories reported.

This document exists because `research/deepseek_research.md` **§Section 5 is empty** — the online/vendor/patent research pass was killed mid-run and never wrote a line. That hole is why every price in the BOM says `[UNVERIFIED]`, and it is what this search was filling.

---

## 1. The headline: a 1988 cube that did what `thedream.md` asks

### US 4,881,068 — Korevaar & Spivey, ThermoTrex Corporation, San Diego
**Filed 1988-03-08 · Granted 1989-11-14 · Expired, free to practice**
`[PUBLISHED — USPTO facsimile pages 1, 6, 7 read directly; all figures verbatim from cols. 1–4]`

A **300 × 300 × 300 mm sealed glass cube** of rubidium vapour at 3 × 10¹³ cm⁻³ (Rb heated to ~130 °C). Two beams cross at 90° inside it:

| Beam | Transition | Visible alone? |
|---|---|---|
| **780 nm, 1.2 W** | 5s½ → 5p³⁄₂ | **No** — infrared |
| **572 nm, 0.8 W** | 5p³⁄₂ → 7d⁵⁄₂ | **No** — nothing to excite |
| **Both, at the crossing** | 7d⁵⁄₂ → 5p³⁄₂, 73% branch | **Yes — 572.411 nm yellow, isotropic into 4π** |

The *lines* stay dark. Only the 1 mm³ **intersection** glows.

| Parameter | Value |
|---|---|
| Image volume | **200 × 200 × 200 mm** |
| Voxels | **10⁶** (100 × 100 × 100) |
| Viewing | **360°, isotropic** |
| Scanning | Acousto-optic — **zero moving parts** |
| Optical power | **~2 W**, diode/dye lasers |
| Mechanism class | **(a)** — real light originating at the point |

**This is the closest anything in any literature has come to `thedream.md`**, and nobody in this repository had seen it. It appears in no doc, no BOM, no prior-art table.

Journal version: I. I. Kim, E. Korevaar & H. Hakakha (Western Research Corporation), which reports a floating cube and a rotating globe scanned above 15 Hz `[PUBLISHED — abstract; full text not obtained, exact mW figures UNVERIFIED]`.

### 1.1 It died of 1988 electronics, and the patent says so

> *"A scanning rate of 15 times/sec would look continuous to the eye, and should be achievable with the imminent development of faster scanners, or with a display reduction to 64×64×64 spots."*
> — US 4,881,068, col. 3, ll. 38–42 `[PUBLISHED, verbatim]`

They achieved **4 scans/second** against the **15** needed. Langhans' 2003 review confirms it: *"The limited speed of the mechanical scanners used in the apparatus lead to a low complexity of the three dimensional images"* `[PUBLISHED, verbatim]`.

**1.5 × 10⁷ voxels/s is about one-eighth of a 1080p60 pixel rate.** That is trivial for a 2026 raster scanner with direct diode modulation. **The stated cause of death no longer exists.**

### 1.2 Brightness — better than expected

Derived from the patent's own photon count `[DERIVED from PUBLISHED, col. 3 ll. 30–35]`:

```
8.7e9 visible photons/voxel/visit × 15 visits/s ÷ 2.9e18 photons/J × 0.94 × 673 lm/W
  = 2.86e-5 lm per voxel
  × 1e6 voxels = 28.6 lm total
  ÷ (0.13 m² head surface × 4π sr) = 17.5 cd/m²
```

**~5× too dim for a normally lit room. Not 100×.** That is a gap engineering closes, not a wall.

### 1.3 Why it still fails `thedream.md`

**The rubidium must live in a sealed cell heated to ~130 °C.** The vapour is colourless when off, so it passes **rule 1** — but a sealed cell is a container, a container is a window, and **rule 4** forbids windows. You would be looking *into* a hot glass tank, not at something in your room.

**This is the deepest result of the whole search**, and it generalises: see §3.

---

## 2. A correction to this repository's own derived law

`docs/11` and the reasoning behind it assert:

> *"Only a NONLINEAR (intensity^n) process localises light to a point, which is why every free-space voxel scheme needs high intensity."*

**True for air. False for doped matter, and the correction is good news.**

Localisation requires an **AND**, not an intensity power law. Two beams at **different wavelengths** driving a **resonant ladder** localise identically, at:

| System | Excitation density | Source |
|---|---|---|
| Lippert 2017 | **0.40 mW/cm² (385 nm) + 2.0 mW/cm² (525 nm)** | `[PUBLISHED]` |
| Gu 2023 — working 5 × 5 × 5 cm free-floating-voxel display | **10.4 + 10.1 mW/cm²**, quartz chamber | `[PUBLISHED]` |
| Qi 2024 — volumetric writing | **< 4 mW CW total** | `[PUBLISHED]` |

Against air breakdown at **~10¹³ W/cm²** — that is **twelve orders of magnitude**.

> **Air needs brute force only because air has no ladder.** Air's transparency and air's refusal to glow are the same fact. The plasma exclusion does **not** generalise to doped media.

**Lineage:** Zito & Schraeder, *Applied Optics* 2(12) 1323 (1963), `10.1364/AO.2.001323` — mercury vapour, explicitly *"for the production of an isolated source of visible radiation in three-dimensional space"*. Then Lewis, Verber & McGhee, *"A true three-dimensional display"*, IEEE Trans. Electron Devices 18(9) 724 (1971), `10.1109/T-ED.1971.17273` — a 2 cm CaF₂:Er cube. Then Downing et al., *Science* 273:1185 (1996) — doped glass. Then Korevaar (§1).

---

## 3. The rule that actually kills the matter-at-the-point family

Not rule 1. **Rule 4.**

Every low-power matter-at-the-point scheme that has ever worked puts the matter in a **container**:

| System | Container |
|---|---|
| Lewis 1971 | CaF₂:Er crystal cube |
| Downing 1996 | doped glass |
| Korevaar 1988 | sealed heated Rb cell |
| Lippert 2017 | cuvette |
| Gu 2023 | quartz chamber |

**This repository has been treating rule 1 (nothing carrying the image) as the discriminator. It is not — rule 4 (not behind a window) is.** The only candidate in the family with no container is a free airborne aerosol, which is why that one ranks first despite being unpublished.

### 3.1 The unpublished configuration

**Ultra-sparse airborne upconverting nanoparticles**, ~10³/cm³, excited only where two invisible IR beams cross. **No published demonstration in air exists** `[searched; nearest analogue is Liu et al., Applied Optics 47(34):6416 (2008), a transparent colloid — still a container]`.

Two derived numbers, and the second is the killer:

- **Invisibility is NOT the constraint.** At n = 10⁹/m³ and d = 50 nm, extinction is **3.0 × 10⁻⁹ /m — about 4,000× below clean air's own Rayleigh coefficient.** The cloud would be optically undetectable. `[DERIVED]`
- **Particle size is.** Each surface particle must emit 3.7 µW, which over its own surface at d = 506 nm is a radiant exitance of **4.6 × 10⁶ W/m² — exactly a 3000 K blackbody. Any smaller particle must out-radiate a tungsten filament and vaporises.** `[DERIVED]`

**d ≥ 506 nm is a hard floor**, and a 506 nm particle is no longer invisible in the numbers above.

---

## 4. The finding that changes what we build

### US 5,782,547 (Videotronic Systems, 1996→1998) and US 4,671,625 (Noble, 1983)
**Both expired. Free to practice.** `[PUBLISHED — claims read verbatim on FreePatentsOnline]`

A single large **Fresnel lens forms the front face of the enclosure**. A small luminous panel sits behind it, beyond the focal point. A **real, magnified image is projected into open air in front of the lens.** One optic, one pass, no retroreflector.

- **Claim 32** recites the minimal form: Fresnel forming the front surface, image projected beyond it, open to ambient room light with no shroud
- **Claims 9 and 19** recite a further lens *"to increase the apparent size of the first spatial object"* — **a granted claim to magnifying a free-space aerial object**

### 4.1 This corrects `docs/11` §1.1

`docs/11` states **"image size = source panel size"** as the governing theorem. **That is true of AIRR only.** The M = 1 isometry argument holds for a beamsplitter plus corner-cube array, and for nothing else.

> **The real law is the APERTURE, not the panel.**

Consequences, all `[DERIVED]`:

| | AIRR (doc 11 spec) | Fresnel |
|---|---|---|
| Panel needed for a 300 mm image | **305 mm** (15-inch) | **100–150 mm** |
| Retroreflector | required | **none** |
| Transmission | **25%** (double-pass theorem) | **~85%** (single pass) |
| Rule-8 judgment call | needed | **retired** |
| Front optic | beamsplitter + RR | **350 mm f/1 acrylic Fresnel, $20–40** |

**The image ceiling is unchanged** — a 350 mm front face still caps the image at ~350 mm, because the aperture is the aperture. What changes is everything behind it.

**The cost is the viewing cone**, which for a 350 mm aperture at 45 mm float works out to ~151°. **That is now a measurement, not an assumption**, and it belongs on the C0 bench beside the retroreflector.

### 4.2 The unification this forces

`docs/11` carries the 170° viewing angle, the image-size ceiling, and the depth-budget equation as **three separate facts**. They are **one fact**: the aperture's angular size seen from the image point.

---

## 5. What this retires from `docs/11`

### 5.1 §4.2(a) is wrong as argued

`docs/11` §4.2(a) claims magnifying AIRR fails because *"an 800 mm image needs an 800 mm lens."* **That is false** — a projector lens is not as big as its screen. Replace with the correct law, derived in `wf_081aee9d-43a`:

> **`a_min = D·p/(D−W)`** — the minimum viewing distance at which the whole image is visible.
> **When `W ≥ D`, no solution exists at any distance.**

Shoulders (460 mm) and height (800 mm) both exceed D = 350 mm, so **no viewing distance exists**. Same wall, correct reason. Validated against a published prototype (Sakane 2025: D = 1000 mm, W = 360 mm, p = 3700 mm → a_min = 5.8 m; experiment run at 10/15/20 m).

### 5.2 The falsification condition is tested and NOT met

`docs/11` §6 item 2 stakes the verdict on whether any published system shows an aerial image exceeding its largest optic. **Two independent tests, both negative:**

| System | Largest optic | Image | Ratio |
|---|---|---|---|
| Sakane 2023, *Optical Review* 30:657–663 | Fresnel **1400 × 1050 mm** | **360 × 360 mm** | optic is **3.9×** larger |
| Okawa, Yokose & Naemura (U. Tokyo, VRSJ 2018) | Fresnel **650 × 550 mm** | 155 × 185 mm plate → **4× larger image** | optic still larger |

The U. Tokyo paper is the one published system in **any language** that explicitly sets out to *"display an aerial image larger than the imaging element."* It succeeds 4× over — and **its own Japanese conclusion is that only the lens behind the image must be large.** That is `docs/11` §4.2(a)'s corrected statement, independently derived and experimentally verified by a different group **seven years earlier, in a venue with no English index.**

### 5.3 Measured LeAIRR numbers, replacing estimates

`[PUBLISHED — Sakane 2023, Opt. Rev. 30:657–663, Table 1 and §3]`

| | |
|---|---|
| Aerial image | *"about 360 mm × 360 mm … 3-times as large as the light source"*, β = 3 |
| Measured aerial luminance | **13 and 20 cd/m²** from a **2700 cd/m²** source |
| Viewing angle | **"about 3 degrees"** as built; authors' best case with adequate BS and RR: **24.5°** |
| Vanishing distance | 7.0 m |

**Magnification destroys the single best property AIRR has** (170° → 3–24.5°), in the authors' own words. `docs/11` §6 item 3's UNVERIFIED quote is now **confirmed verbatim** from Takiyama 2025, *J. SID* 33:472–481 §4: *"the viewing angle and size of the proposed optical system are limited by the size of the convex lens."*

### 5.4 The M = 1 theorem has a named exception

A **varifocal mirror is a curved mirror**, so `docs/11` §1.1's isometry theorem does not apply to it. Traub states it himself in US 3,493,290 (filed 1966): *"the greater the distance of the image from the mirror, the greater will be…"* — and his **Figure 3 is explicitly labelled "(Real image)"**, disclosing a real-image, in-front-of-aperture variant in 1966, at a stated cost of *"a reduction of the intensity of the image illumination by a factor of four."*

**That factor of 4 is the same 25% double-pass penalty `docs/11` §2.4 derives for AIRR — the same tax, a different mechanism.** The SpaceGraph commercialisation (BBN/Genisco, 1981, $120,000) used the virtual-image form, which is a window.

---

## 6. Worth one afternoon, after C2

### Aerial Depth-Fused 3D (aerial DFD)
Terashima, Yamamoto & Suyama, *Optical Review* (2019), `10.1007/s10043-018-0473-9` — **the same lab that invented AIRR.**

Two aerial images at different depths, overlapped along the line of sight, fuse into a single percept whose apparent depth moves **continuously** with the luminance ratio between them. No glasses, no tracking, **no moving parts**.

**TAYF-C35 currently shows a flat aerial plane** — `docs/11` §3.2 admits no depth cue beyond the float. Aerial DFD adds real perceived depth for the cost of a second panel and a second beamsplitter pass.

**The number that must be dug out:** maximum fusible separation between the two aerial planes, in mm, at ~0.5 m. A 2016 paper titled *"Enlargement of Continuous Perceived Depth Region in DFD"* implies the native range is small.

---

## 7. Open leads, ranked

| # | Lead | Why it matters | Cost to close |
|---|---|---|---|
| 1 | **Schwarz & Blundell, *Optical Engineering* 32(11):2818 (1993), `10.1117/12.148130`** — *"Considerations regarding voxel brightness in volumetric displays utilizing two-step excitation processes"* | The one paper that appears to state the general **brightness law** rather than one system's measurement. If the derived `1/N` duty-cycle bound is right, it applies to **laser-plasma, photophoretic traps, and every scanned-point scheme** — and it decides whether the Rb revival is a 5× or a 400× shortfall | **One interlibrary loan** |
| 2 | **Kim, Korevaar & Hakakha 1996** full text | Laser power per voxel, voxel cd/m², cell temperature, max scan rate | Document delivery |
| 3 | **Interman Corporation portfolio** (WO2024/190160, WO2024/157731, US20260227596, WO2023/238561) | An **active Japanese aerial-imaging assignee this repo never found**, with pending US claims on **foldable and portable** aerial image devices, published as recently as **2026-08-06**. `docs/05` §10 item 8 names exactly this gap. Their WO2024/190160 pairs two retro-transmissive plates *"to achieve a large-screen aerial image"* | Portfolio walk before any product decision |
| 4 | **MW-LIBS** — microwave-assisted laser breakdown (Ikeda et al., *Spectrochim. Acta B* 2016) | **~100× emission enhancement**, plasma lifetime 50 → 500 µs. Larger than the 25–250× gap that excluded plasma. Probably does not rescue it — the rejection was *thermal*, and microwaves substitute watts rather than removing them — but the numbers are new and the mechanism was never considered | Full text, extract **total** (laser + microwave) energy per luminous voxel |

---

## 8. Negative results worth keeping

**Non-plasma air emission is conclusively dead**, and for a reason worth recording:

> Excited room air converts **~7 × 10⁻⁵** of deposited energy into photons, and those photons are **300–430 nm**. Luminous efficacy: **~5 × 10⁻⁶ lm per watt deposited.** A dim-but-visible floating head therefore needs of order **10⁵–10⁶ W** dumped continuously into the room's air. `[DERIVED]`

**That number is independent of how you excite it** — laser, electron beam, ion beam, discharge, microwave — because it is a property of nitrogen.

And the counter-intuitive part: **this is worse than plasma, not better.** A hot plasma is a grey-body continuum radiator with real visible output. Every non-breakdown scheme gives up the continuum and keeps only UV fluorescence, at 10⁻⁴ photopic overlap. **There is no non-plasma escape hatch in air.**

**No granted patent claim anywhere** — Google Patents CPC/IPC sweeps, PATENTSCOPE including JP/KR/CN national collections with Japanese full text, FreePatentsOnline — **to an in-front aerial image larger than the device that forms it.** That is a real negative result, from a real search.
