# 14 — TeleHuman, Vertegaal's patents, and a correction to doc 13

**Reference date: 2026-08-21.** Triggered by a single question — *does a company doing this
exist?* — which surfaced **TeleHuman 2** (Queen's University, CHI 2018): a ring of projectors
around a human-sized retroreflective cylinder. That is, to within the choice of relay optic,
**the architecture derived from scratch in `docs/13_THE_ROOM.md` five hours earlier.**

This document does three things: enumerates Roel Vertegaal's patent estate, reads the TeleHuman 2
paper for its real numbers, and **corrects a false claim in doc 13 §11.**

---

## 1. The headline, in three lines

1. **Vertegaal never patented it.** 16 patent-family members, not one on TeleHuman, TeleHuman 2,
   LightBee, or any cylindrical/light-field/telepresence display. The architecture is published,
   unpatented, and therefore free to practise — but also **unpatentable by anyone, including us.**
2. **TeleHuman 2 as built was not 360°.** The rail was designed for **275 projectors**; budget
   allowed **45**; the delivered system gave **59° of parallax at ~10 FPS**. The 360° figure in
   every press write-up is the design target, not the result.
3. **The moat claim in doc 13 §11 is wrong.** Pupil-steered per-eye view emission is claimed by
   **Google US11474597B2, granted, in force to 2040** — which this repository had *already found*
   and filed at `docs/05` §3.4 before doc 13 was written. See §5.

---

## 2. Vertegaal's patent estate — complete enumeration

Source: Google Patents structured query, `inventor="Roel Vertegaal"`, 2026-08-21.
16 unique family members. `[V]` on the enumeration (numbers, dates, assignees read off the
record); claim text not read for each, so tier is `[R]` on individual scope.

| Family | Members | Priority | Assignee | Subject |
|---|---|---|---|---|
| Attentive interfaces | US8672482B2, US20130188032A1, CA2423142C, HK1158334A, WO2004084054A2 | 2003-03-21 | Queen's University at Kingston | Communication between humans and devices |
| Calibration-free eye tracking | US7963652B2, EP1691670B1 | 2003-11-14 | Queen's University at Kingston | Eye tracking without calibration |
| Flexible displays | US8466873B2, US20170224140A1, HK1176419A | 2006-03-30 | Roel Vertegaal | Interaction techniques for flexible displays |
| Computing apparatus | WO2014106748A2 | 2013-01-04 | Plastic Logic Limited | Flexible computing device |
| Flexible + microlens 3D | US20200166967A1 | 2015-03-17 | Queen's University at Kingston | Flexible display w/ convex microlens array producing a flexible 3D light field |
| Haptics | CA2923867A1 | 2015-03-17 | Roel Vertegaal | Haptic rendering, flexible device |
| Vision correction | US20180252935A1 | 2017-03-03 | **Evolution Optiks Limited** | Vision-correction light field display + barrier |
| Gaze estimation | US12271519B2, WO2022267810A1 | 2021-06 | **Huawei Technologies** | Eye tracking, 2D on-screen gaze estimation |

**Nothing on cylindrical light-field telepresence.** Verified four ways, all returning zero:

| Probe | Result |
|---|---|
| `assignee="Queen's University at Kingston"` + `"cylindrical display"` | **0** |
| `assignee="Queen's University at Kingston"` + `telepresence` | **0** |
| `assignee="Queen's University at Kingston"` + `"light field"` | **0** |
| Full 16-item inventor enumeration, read by title | **0 relevant** |

This is a negative result across four independent probes, which is the standard
`research/METHODOLOGY.md` requires before a negative is recorded as a finding rather than as an
absence of searching. It is still a negative: an unpublished or differently-titled filing would
not appear.

### 2.1 The one that did get patented, by the student

**Daniel Gotsch**, first author of TeleHuman 2, has **22 patents — all assigned to Evolution
Optiks Limited**, on light-field displays and **pupil tracking**, for **vision correction**.
The lab published the telepresence work and patented the eyesight work. Worth knowing when
assessing what Vertegaal's circle considered commercially defensible.

---

## 3. TeleHuman 2, as actually built

`[PUBLISHED — CHI 2018 paper text extracted and read directly. Gotsch, Zhang, Merritt, Vertegaal,
"TeleHuman2: A Cylindrical Light Field Teleconferencing System for Life-size 3D Human
Telepresence."]`

**Display**
- Hollow acrylic tube, **195 cm tall × 75 cm diameter**, 5 mm wall
- Coated with retroreflective sheeting, **1.3° retroreflective viewing angle** — brightness drops
  below 50% beyond 1.3° from the projector axis. This is what separates the stereo pair: only
  eyes within 1.3° of a projector see that projector's image.
- Second layer: **Brightview 1D vertical diffuser**, so the projector ring can sit above head
  height. **No vertical parallax by design.**

**Projectors**
- Circular rail with slots for **275 projectors**, one per **1.3°** (275 × 1.3° = 357.5° ≈ 360°)
- **PicoPro laser pico projectors** — 720p, **32 lm each**, laser-scanned so **no focusing needed**
- **45 installed.** 45 × 1.3° = 58.5° ≈ **59° of parallax delivered**
- One **Odroid C1+** per projector as its render engine; 15 Odroids per Gigabit switch
- **~10 FPS rendering**

**Capture**
- Remote subject stands in a circle of radius 180 cm, **1 ZED stereo camera per 20°**
- 2×2K stereo at **15 fps**, one GTX 1080 per camera, depth via CUDA
- **3 ZED cameras built** → 59° of capture, matching the 59° of display
- Images scaled to 1280×720, JPEG, UDP broadcast; relief-mapping shader rotates each view ±10°

**Every number cross-checks:** 45 projectors × 1.3° = 59° display; 3 cameras × 20° = 60° capture.
The system is internally consistent and consistently one-sixth of a circle.

### 3.1 What this tells us that the press coverage does not

- **The image is on the cylinder.** A retroreflective coating on a 75 cm acrylic tube is a
  *screen*. Accommodation is fixed at the tube surface. TeleHuman 2 has 360°-capable geometry,
  life size, and no headset — and **still puts the light on a surface.** The free-space
  accommodation argument in `docs/13` §6 survives contact with it intact.
- **The cost of not steering.** TeleHuman 2 emits one view per 1.3° to *everywhere at once*.
  That is precisely the broadcast architecture `docs/13` §3 prices at ~1,350× the étendue of a
  pupil-steered one. **275 projectors is the empirical value of not tracking.** Doc 13's central
  engineering claim now has an independent experimental price tag attached, which is better
  evidence than the derivation alone.
- **Why it never became a company.** 275 pico projectors + 275 single-board computers + 18 stereo
  cameras + 18 GPU hosts, to deliver 10 FPS onto an acrylic tube. The budget ran out at 45.
  This is not a market-timing failure or a go-to-market failure. It is a **unit-cost** failure,
  and it is the same failure `docs/13` §1.1 is trying to engineer around by shrinking `z` and
  widening `D`.
- **Follow-up:** *LightBee* (CHI 2019) reused the same 45-projector ring against a retroreflective
  cylinder mounted on a **quadcopter**. `[R — search-record level, paper not read.]`

---

## 4. Freedom to operate — what actually threatens us, and what does not

Two patents surfaced during this search that bear on `docs/13`. Both claim texts read verbatim.

### 4.1 US9813673B2 — Smits, "Holographic video capture and telepresence system" — **NOT a threat**
Filed 2017-01-20, granted 2017-11-07, assignee Gerard Dirk Smits. `[V — claim 1 read verbatim.]`

Claim 1 requires *"a head mounted projection display apparatus that includes: a frame that is
adapted to wrap around a portion of a head of a user."* **It is a headset-based capture patent.**
TAYF has no headset at either end by definition. Does not read on us. Recorded so nobody has to
look at it twice.

### 4.2 US11385712B2 — Evolution Optiks, "Pupil tracking system and method…" — **narrow, but design around it**
Priority 2019-04-01 (CA 3,038,584), granted 2022-07-12. `[V — claim 1 read verbatim.]`

Claim 1 is **not** a general claim on pupil-steered light fields. It claims one specific
jitter-suppression algorithm: acquire pupil location sequentially, compute pupil **velocity**,
compare against a **designated threshold**, hold the viewing-zone geometry fixed while velocity
is below threshold, and re-render the zone only when velocity exceeds it.

**Why this matters to us anyway:** velocity-threshold hysteresis is the *obvious* first fix for a
jittery pupil tracker, and doc 13 §2 puts a tracker at the centre of the system. If we implement
"hold the zone until the eye moves fast enough," we land inside this claim. Use a different
stabilisation — Kalman/one-euro filtering on position, or zone updates on a fixed cadence
independent of velocity — and document the choice at the time it is made.

---

## 5. ⚠ CORRECTION TO `docs/13_THE_ROOM.md` §11

Doc 13 lists as moat item 2:

> *"the pupil-steering **scheduling** algorithm (which engine serves which eye, and the handoff as
> people walk — this is a hard real-time assignment problem and the hardest thing to copy)"*

**This is anticipated and the repository already knew it.** `docs/05` §3.4 row 28, tier **[V]**:

> **US11474597B2 — Google LLC** (Pulli, Wetzstein, Spicer, Jones, Maila, Economou), filed
> 2020-11-02, priority 2019-11-01, **active, expires 2040-11-02**: multiview autostereoscopic
> display with an angular-pixel array and an eye tracker; the processing system **renders a
> specific view for each detected eye based on that eye's location** and drives the angular pixels
> to display that view **only in the viewing zone where that eye was detected.**

Doc 05 §3.4's own reading already states the conclusion in bold — *"Concept B's candidate novelty
… is anticipated by US11474597B2 on its face"* — and doc 13 was written without consulting it.
That is a process failure, not a physics failure, and it is recorded here rather than quietly
edited per `research/METHODOLOGY.md` rule 4.

**What survives as defensible, corrected:**

| Doc 13 §11 moat item | Verdict |
|---|---|
| 1. HOE band mapping N engines onto 360° of aperture | **Survives.** No art found. Also the hardest thing in the build (§6). |
| 2. Pupil-steering scheduling | **Dead as claimed.** Anticipated by US11474597B2 (Google, to 2040). |
| 3. Multi-plane depth-blending calibration across N independently-aimed engines | **Survives, narrowed.** Novelty is in the *multi-engine geometric coherence*, not in depth blending, which is standard in multifocal near-eye displays. |
| 4. Avatar enrolment pipeline | **Dead.** Anticipated by Mon3tr (arXiv 2601.07518), per `docs/05` §3.8. |

The steering *idea* remains free to **use** — anticipation blocks patenting it, and US11474597B2's
claim is tied to an angular-pixel array rather than a ring of steered projectors, so an
infringement read is a separate and unfinished question. **Do not treat "we can probably use it"
as "we can own it."**

---

## 6. What this changes in the plan

1. **The wedge test is unaffected and still the right next move.** TeleHuman 2 used laser pico
   projectors *specifically because they need no focusing* — which is precisely the property doc 13
   must destroy, since a fixed-focus scanned beam cannot place a real focus point at a chosen
   depth. Their component choice is direct evidence that the focus mechanism is the hard part.
   **Bench-test the focus element first, exactly as planned.**
2. **The pitch changes.** "Nobody has built this" is false and a judge may know it. The true and
   stronger claim is: *"Queen's University built the broadcast version in 2018. It needed 275
   projectors to reach 360°, they could afford 45, and it painted onto an acrylic tube at 10 FPS.
   We are building the steered version, which needs 24 and puts the light in the air."*
3. **File nothing on steering.** Redirect any patent budget to the HOE band and multi-engine
   calibration (§5 rows 1 and 3).
4. **Open item:** resolve whether US11474597B2's angular-pixel-array limitation excludes a ring of
   steered projectors. That is a claim-construction question for a patent attorney, not for this
   repository.

---

## 7. Citations

`[PUBLISHED]` Gotsch, Zhang, Merritt, Vertegaal, "TeleHuman2: A Cylindrical Light Field
Teleconferencing System for Life-size 3D Human Telepresence," **CHI 2018** — full text extracted
and read; all §3 numbers transcribed directly.
`[V]` Google Patents structured query, `inventor="Roel Vertegaal"`, 16 results, 2026-08-21.
`[V]` US9813673B2 — claim 1 read verbatim.
`[V]` US11385712B2 — claim 1 read verbatim.
`[V, inherited]` US11474597B2 — verified in `docs/05` §3.4 row 28, not re-verified here.
`[R]` LightBee, CHI 2019 — search-record level only, paper not read.
`[R]` Voxon VX2 (256 mm ⌀ × 256 mm), VX2-XL (512 × 256 mm); Holoconnects Holobox (transparent LCD
over a custom light box, per vendor's own copy); Proto; Light Field Lab SolidLight (panel, video-
wall market) — all vendor-page level, none independently verified.
