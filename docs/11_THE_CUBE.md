# 11 — THE CUBE

**Reference date: 2026-08-16.** Supersedes nothing; this is the first document in the repo that specifies a *cube* and states honestly what a cube can and cannot do. Follows the verdict in §1, which was reached by adversarial verification (workflow `wf_4371072e-a02`, two independent high-confidence analyses, one of which retrieved and read Yamamoto 2017 in the original Japanese rather than relying on this repo's summary).

---

## 1. The verdict, stated once, plainly

**A cube can show a life-size human head and neck floating in open air. A cube cannot show a body.**

At 350 mm it passes **nine of the ten rules in `thedream.md`**; the only physics failure is rule 6, the 10 cm size (§3.1).

Both halves of that sentence are load-bearing and neither is negotiable.

### 1.1 Why the head works

Conventional AIRR has **magnification exactly 1**, and this is a *theorem*, not a measurement:

> The beamsplitter is a plane. Each retroreflector element is three mutually orthogonal plane mirrors (a corner cube), or a bead returning light antiparallel along its own line. The net object→image transformation is **reflection in the beamsplitter plane**. A plane reflection is a Euclidean isometry: it preserves every distance. **An isometry has magnification exactly 1 by definition.** There is no adjustable parameter — you cannot tune a plane mirror to magnify. [DERIVED]

Confirmed by ray construction and by Yamamoto's own card-interception measurement (Fig. 2a–c: sharp, left-right-reversed characters only at the plane-symmetric position; blurred fore and aft). [MEASURED]

So: **image size = source panel size.** A human head is **25 cm** tall (face alone, 22 cm). A panel that size fits in a cube. Therefore a head fits in a cube.

### 1.2 Why the body does not

Same theorem, run the other way:

| Subject | Life size | Panel required | Cube required |
|---|---|---|---|
| Face | 22 cm | 22 cm | ~26 cm |
| **Head + hair** | **25 cm** | **25 cm** | **~30 cm** |
| Head + neck | 32 cm | 32 cm | ~38 cm |
| Seated upper body | 80 cm | 80 cm | ~95 cm |
| Standing body | 170 cm | 170 cm | ~200 cm |

**The empirical proof, and it is the inventor's own hardware:**

> Yamamoto's life-scale (等身大) aerial human display used a **96-inch LED panel — 192 × 144 cm, 240 cm diagonal, 6 mm pitch**, with a vinyl-sheet beamsplitter at 45° and a vertical micro-bead retroreflector. [MEASURED, Yamamoto 2017 §3.2, Fig. 10]

The person who invented AIRR, when he wanted a life-size human, built a life-size panel. That is the question answered from hardware rather than from argument.

### 1.3 The correction this document exists to record

On 2026-08-16 ~01:00 this project told its own author that *"a 20 cm slab shows your full upper body, life-size, floating in open air."*

**That was false.** An upper body is 80 cm; a 20 cm slab yields ~20 cm. The error is **4× linear, 16× in area.** It is recorded here rather than deleted, per `research/METHODOLOGY.md` rule 4.

---

## 2. The cube, specified

### 2.0 The one equation that sizes the cube

Image size and float distance draw from the **same depth budget**. The source panel's perpendicular setback from the beamsplitter *equals* the float, 1:1 [MEASURED, Yamamoto Fig. 2 + DERIVED from plane symmetry], and the beamsplitter's clear diagonal must satisfy `diagonal ≥ float·√2`. The working rule for a cube of side `S`:

> ### `image_height + float ≈ S`   and   `image_width ≤ S`

Spend depth on subject, you lose air. Spend it on air, you lose subject. **There is no third option, because M = 1 at every float distance** — pushing the image further out never gains width. [DERIVED]

### 2.1 The size ladder

| Cube | Largest image | Float | What you actually see | Verdict |
|---|---|---|---|---|
| 100 mm | 100 × 100 mm | ~0 | a fist | **Dead** — fails rule 3 as well as rule 6 |
| 200 mm | ~180 × 180 mm | ~20 mm | life-size face, chin to hairline | Works, but hugs the glass |
| 300 mm | 197 × 263 mm | ~45 mm | full head with hair | Comfortable |
| **350 mm** | **229 × 305 mm** | **~45 mm** | **head + neck** | **Selected** |
| 500 mm | 400 × 450 mm | ~50 mm | head, neck, top of chest | Shoulders still fail — a bust is 500 mm **wide** |

### 2.2 TAYF-C35 — the selected cube

| Parameter | Value | Tag |
|---|---|---|
| **External** | **350 × 350 × 350 mm** | [DERIVED] |
| **Aerial image** | **229 × 305 mm — life-size head and neck** | [DERIVED] |
| **Float** | **~45 mm in front of the front face** | [DERIVED] |
| Source panel | 15-inch 4:3 LCD, 304.8 × 228.6 mm, mounted **portrait** | [PUBLISHED — commodity industrial/kiosk part] |
| Beamsplitter | 350 × 495 mm plate at 45°, 2–3 mm, 50/50 front surface, AR or 0.5–1° wedge on the rear | [DERIVED] |
| Retroreflector | 350 × 350 mm micro-bead or prismatic sheet | [DERIVED] |
| Viewing angle | **170° horizontal**, set by panel directivity not by the optics | [MEASURED, Yamamoto 2017 §2.2/§3.1] |
| Moving parts | **Zero** | [PUBLISHED] |
| Magnification | 1.000, exactly | [DERIVED — isometry] |

**What 350 mm buys over 300 mm.** A 305 mm image instead of 263 mm — which crosses the line from *head* (250 mm) to *head + neck* (320 mm). This matters perceptually more than the 42 mm suggests: a head alone reads as a severed head hanging in space, while a head on a neck reads as **a person leaning into the room.** The neck is what makes it a person. [ESTIMATE — perceptual claim, untested]

**Why a 15-inch 4:3 panel.** Portrait orientation gives 229 mm wide × 305 mm tall. Head width is ~160 mm, so 229 mm leaves generous margin; 305 mm covers head (250 mm) plus most of the neck. 4:3 industrial and kiosk panels are commodity parts with real supply chains, and unlike laptop 16:9 panels their aspect ratio is close to what a portrait head actually needs. [DERIVED]

**The trade you can make at 350 mm.** Drop to a 12.9-inch panel and you get a 263 mm image at **87 mm float** — less subject, roughly double the air. If the C0 measurement shows the image reads as flat or glass-bound, this is the knob to turn. [DERIVED]

**Where 350 mm still fails, and it is not height.** Shoulders need **500 mm of width**, and the cube is 350 mm across. **Width fails before height does** — you could stretch the cube taller and still not get a bust. [DERIVED]

### 2.3 Optical layout

```
                    ┌─────────────────────────┐
                    │                         │
   retroreflector ──┤▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓          │
   350 × 350 mm     │▓             ╲          │
                    │▓              ╲  45°    │      ● aerial image
                    │▓               ╲ beam-  │     ╱ 229 × 305 mm
                    │▓                ╲splitter    ╱  HEAD + NECK
                    │▓                 ╲      │  ╱   floating in air
                    │▓                  ╲     │ ╱    ~45 mm out
                    │                    ╲    │╱
                    │  ┌──────────────┐   ╲   ●
                    │  │ 15" 4:3 LCD  │    ╲  │
                    │  │ portrait     │     ╲ │
                    │  └──────────────┘      ╲│
                    └─────────────────────────┘
                         350 mm cube            front aperture
```

Light path: panel → beamsplitter (50% reflects) → retroreflector (returns antiparallel) → beamsplitter (50% transmits) → **converges in free space** at the plane-symmetric position of the panel. The image is **real** — intercept it with a card and it lands sharply on the card, blurring fore and aft. [MEASURED, Yamamoto 2017 Fig. 2a–c]

### 2.4 What the two 50% passes cost

**25% maximum optical efficiency, and it is a theorem.** Light crosses the beamsplitter twice, and the two useful events are *reflect* then *transmit*. Any splitter ratio `r` gives `r(1−r)`, maximised at `r = 0.5` → **0.25**. No coating improves it. [DERIVED]

**The one legitimate escape: p-AIRR.** Polarise the source, put a quarter-wave retarder in front of the retroreflector, and use a polarising beamsplitter — the double pass rotates the polarisation so both events become near-lossless. Yamamoto measured **>2.2× gain** (1/2 s, F4.8, ISO400, 50 cm). [MEASURED, Fig. 8]

**Design consequence: use an LCD panel, not OLED.** LCD output is *already linearly polarised*, so p-AIRR costs one retarder film and zero light. This inverts the usual instinct to reach for OLED. Build it both ways and measure — it is the cheapest high-value experiment in the whole project. [DERIVED]

---

## 3. What the cube does, and what it does not

### 3.1 The Ten Rules, audited

Tested against `thedream.md` verbatim, not against a paraphrase.

| # | Rule (abridged) | TAYF-C35 | Reasoning |
|---|---|---|---|
| **1** | **Free-space** — no screen, panel, mist or surface *carrying* the image | ✅ **PASS** | The AIRR image is a **real image**; nothing exists at the image location. Proven by interception: a card held there shows it **sharp, blurred fore and aft** [MEASURED, Fig. 2a–c]. The LCD is the *source*, not the *carrier* |
| **2** | **No wearables** | ✅ **PASS** | Nothing worn, ever |
| **3** | **Life-size** — true human scale, not a figurine | ✅ **PASS** | M = 1 **exactly**, by theorem (§1.1). A 305 mm image is a head and neck at precisely true scale |
| **4** | **In the viewer's own space** — not behind a window, portal or aperture plane | ✅ **PASS** | AIRR forms the image **in front of** the aperture. This is the mode's defining property, not a tuning |
| **5** | **Photoreal** | ✅ **PASS** | A photoreal render on an LCD. Nothing in the optical path degrades identity |
| **6** | **Ten centimetres** | ❌ **FAIL** | 350 ≠ 100. And a true 100 mm cube gives a **100 mm image — a fist**, which would fail rule 3 as well |
| **7** | **Symmetric** — both ends capture and display | ✅ **PASS** | Cameras fit trivially in a 350 mm enclosure |
| **8** | **Self-contained** — nothing else to buy, install or mount; *"no retroreflector"* | ✅ **PASS**, with a judgment call | The rule **names the retroreflector explicitly**. AIRR uses one — **sealed inside the cube**. Read as "nothing **else** added to the room," a component inside the sealed device is not something bought, installed or mounted. **This reading is the author's call to make, and it is the only rule whose verdict turns on interpretation rather than physics** |
| **9** | **Any ordinary room, normal light** | ✅ **PASS** *(pending)* | *"bright enough to be observed clearly under ordinary lighting"* [PUBLISHED, Yamamoto §3.1] — but rests on `η_RR`, still unmeasured (§6.1) |
| **10** | **Safe and live, <150 ms** | ✅ **PASS** | No laser anywhere; passive glass and film. ~80 ms end-to-end transport (doc 10 §6) |

### **Nine of ten. Only rule 6 fails.**

**An observation worth recording:** none of the ten numbered rules requires a **whole body**. Rule 3 demands *true human scale*, which a life-size head and neck satisfies exactly. Only the preamble sentence — *"standing or sitting in the air"* — asks for a body. **The written rules are stricter about scale than about completeness**, and the cube passes the written rules. This is not a loophole being exploited; it is what the specification actually says, and it is recorded so the author can decide whether the preamble or the numbered list governs.

### 3.2 The honest description of the demo

A 35 cm cube sits on the table. A person's head and neck hang in the air about 4.5 cm in front of it, at true human scale, looking at you, talking, turning to follow you as you move — because your phone is tracking their head and theirs is tracking yours. You can put your hand where their cheek is. Nothing is worn. Nothing is projected onto anything.

**It is a head and neck. Not a bust, not a torso, not a body.** Anyone who sees it will immediately ask "can it do the whole person?" and the honest answer is "yes — at 200 cm, not 35."

### 3.3 Why a head is the right product anyway

From doc 10 §1.3, and it is the most expensive lesson this project learned:

> **The mistake that cost this project the most time: sizing the device to a 1.7 m body when a conversation is a face.**

Every video call ever made frames a head and shoulders. A head at conversational distance subtends **12.6°**. Presence is an angle, not a volume. A floating life-size head at the correct scale, with correct gaze, is a stronger presence signal than a shrunken full body — and it is the thing a 35 cm cube can actually deliver.

---

## 4. Three things that do NOT rescue a body-sized image

Each was tested and each fails for a stated reason. They are recorded so nobody re-runs them.

### 4.1 Portal mode does not work the way this repo claimed

`W = D·(b/a)` is **correct similar-triangles geometry** — and it is a **visibility bound, not a mechanism.** It bounds the width of the region *behind* the device that an eye can see through the aperture. It is the shadow the aperture casts.

> **A bound on where an image *may* appear is not a mechanism that *puts* one there.** Every L2 table in this repo tabulates permission and reads it as capability. That substitution is the whole error. [DERIVED]

**The closing theorem:** any ray-crossing upstream of the aperture lies *inside* the enclosure (≤ 30 cm). Therefore **any apparent image more than ~30 cm behind the front face is necessarily a virtual image** — matter at the image point excepted (Smalley's sole exception, already closed on power). A virtual image seen through a 20–30 cm hole is optically **a window**. It is not a person in your room. [DERIVED]

**Repo edits required:** `docs/01` §4.3b/§4.3c and `docs/10` §2.2 must be corrected to distinguish *permission* from *capability*.

### 4.2 Magnifying AIRR exists — and it moves the wall rather than removing it

**This is a genuine repo correction.** `docs/09` §3 and `docs/10` §4 assert unit magnification as a flat property of AIRR. `docs/02` §10 item 8 named "journal access showing a magnifying AIRR variant" as the specific thing that would falsify the AIRR bound. **That falsification condition is now MET.** The variants postdate the 2017 review this repo read.

| Variant | Source | What it does |
|---|---|---|
| **Fresnel-AIRR** | *Optical Review* (2023), `10.1007/s10043-023-00845-5` | Uses a Fresnel lens's virtual image as the AIRR source. Panel-to-beamsplitter distance **halved**; floating images formed at **3.4 m and 4.6 m**, naked-eye visible. **Breaks the float = setback 1:1 rule** [PUBLISHED — abstract read verbatim, full text paywalled] |
| **LeAIRR** | Fukuda et al., *J. SID*, `10.1002/jsid.70050` | *"the magnifying lens optically enlarges the virtual light-field display plane without increasing the physical panel size, thereby enabling simultaneous scaling of the aerial-image size and depth."* Longitudinal magnification ≈ (lateral)² [PUBLISHED — abstract read verbatim] |
| High-res LeAIRR | Takiyama et al., *J. SID* (2025), `10.1002/jsid.2056`; SPIE 13389 | Lens makes aerial image and retroreflector optically conjugate; CTF 2.5× better than conventional AIRR |

**Why it does not rescue the cube — two independent reasons:**

**(a) The constraint relocates from panel to lens.** The system stops being AIRR-limited and becomes **aperture-limited with the lens as the aperture**. An 80 cm in-front image needs a ≥80 cm exit optic; 170 cm needs ≥170 cm. Neither fits a 30 cm box. Law 1 is unmoved — it now applies to the Fresnel instead of the panel. [DERIVED]

**(b) Étendue charges for every bit of it.** By the sine condition, magnifying by M shrinks the angular cone by M:

| Magnification | Viewing cone | Loss vs. 170° |
|---|---|---|
| M = 1 | **170°** | — |
| M = 4 (upper body) | **±14.4° → 29°** | 5.9× |
| M = 8.5 (standing body) | **±6.7° → 13.5°** | 12.6× |

[DERIVED, sine condition: sin(85°) = 0.9962; M=4 → sin u′ = 0.2490; M=8.5 → sin u′ = 0.1172]

So even the magnified version trades away the single best property AIRR has. A 13.5° cone is a sweet spot one person must sit still inside — not a thing you walk around.

### 4.3 Curvature, float, and folding buy nothing

- **A curved retroreflector cannot magnify.** *"Aerial image position is not affected by the curvature of the retro-reflector."* [PUBLISHED + MEASURED, Yamamoto 2017 Fig. 5 caption, verbatim — demonstrated with a curved plate and with draped fabric]
- **Float does not buy size.** M = 1 holds at every float distance. There is no size/float trade — pushing the image out costs depth and never gains width. [DERIVED]
- **Plane folds do not buy size.** Mirrors preserve magnification *and* transverse extent. Folding buys optical path length, never étendue and never image size. [DERIVED]

---

## 5. Build ladder for the cube

| Rung | What | Cost | Proves |
|---|---|---|---|
| **C0** | Retroreflector sheet + acrylic half-mirror + your phone as the panel, taped to cardboard. No enclosure. | **< $100** | **That an image floats at all**, and the single largest open number in the project: `η_RR`, the retroreflector return efficiency, which **is stated in no paper we have found** |
| **C1** | Same optics, 12.9″ panel, measured with a spot luminance meter | + meter | `L_image / L_source` as an absolute number. Converts every brightness figure in doc 10 §4 from [DERIVED] to [MEASURED] |
| **C2** | Build it twice — OLED vs. LCD + retarder | + $50 | The p-AIRR gain. Predicted ~4× for LCD; **untested and the highest-value cheap measurement in the project** |
| **C3** | 350 mm enclosure, real panel, real retroreflector, static image | | The cube exists |
| **C4** | Live head from a phone over the network | | TAYF |

**Do C0 first, this weekend.** Every number in §2 rests on `η_RR`, and `η_RR` is unmeasured. If it comes back low the cube needs a much brighter panel and the thermal budget in doc 10 §7 reopens. **One afternoon settles it.**

---

## 6. Open items this document does not close

1. **`η_RR` is unmeasured.** Every brightness figure in §2 assumes the good case. This is the largest open number in the project. [UNVERIFIED]
2. **The LeAIRR full texts are paywalled.** Only abstracts were read. Highest-value follow-up: get the Fresnel lens *diameter* versus the aerial image size. Prediction is `D_lens ≳ W_image`. **If a published system shows an in-front image materially exceeding its largest optic, §4.2(a) is wrong and this whole verdict must be reopened.**
3. **One quote is UNVERIFIED**: *"the viewing angle and size of the proposed optical system are limited by the size of the convex lens"* — held only from two secondary paraphrases, never a primary source. Per methodology rule 2 it must not be cited as fact. **The physics stands without it.**
4. **The exact panel/beamsplitter/retroreflector packing in a 350 mm cube is not a completed optical design.** §2.3 is a layout sketch that closes geometrically; it is not a tolerance-analysed mechanical design.
5. **Two of four verification angles did not run** (étendue and empirical-reality agents hit the session limit). The two that completed both returned **NO** at high confidence and did not contradict each other, and the AIRR angle read the primary source in the original Japanese. The étendue numbers in §4.2(b) came from the AIRR angle rather than the dedicated étendue agent, and would benefit from independent recomputation.

---

## 7. Tagging corrections this document makes to the rest of the repo

| Location | Current | Should be |
|---|---|---|
| `docs/10` §4 magnification row | `unity \| [MEASURED] \| Fig. 2b` | `[PUBLISHED: plane symmetry] → [DERIVED: M=1]` — Yamamoto never states a magnification figure; unity follows by geometry. **This strengthens the claim** — an isometry argument beats any measurement |
| `docs/09` §3, `docs/10` §4 | "Unit magnification. Image size = source size, exactly" | Add: **"for CONVENTIONAL AIRR"**; cite LeAIRR / Fresnel-AIRR |
| `docs/02` §10 item 8 | falsification condition open | **MET** — with the note that the bound survives anyway because the constraint moves from panel to lens |
| `docs/10` §5.2 | "float distance = source setback, exactly and only" | Add **"for conventional AIRR"** — the Fresnel variant breaks precisely this |
| `docs/01` §4.3b/c, `docs/10` §2.2 | L2 tables read as capability | Mark as **visibility bounds (permission), not mechanisms (capability)** |
