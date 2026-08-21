# 16 — Business, Legal, Logistics and the Full Cost Stack

**Reference date: 2026-08-21.** Everything that is not engineering. Companion to
`docs/13_THE_ROOM.md` (the product), `docs/15_THE_ACCOMMODATION_BUDGET.md` (why it is a small
room), and `docs/14_TELEHUMAN_AND_THE_PATENT_GAP.md` (why the moat is smaller than it looked).

> **This is not legal, tax, or financial advice.** It is an engineering-grade map of what has to
> be decided, what it costs, and which items genuinely need a professional. Every item marked
> **[LAWYER]**, **[ACCOUNTANT]** or **[ASSESSOR]** must not be actioned off this document.

---

## 0. ⏰ Time-critical, today

**Hub71 Cohort 20 applications close 21 August 2026 — the date this document was written.**
`[VERIFIED — hub71.com programme page, read 2026-08-21]` Programme starts February 2027.

The package is **up to AED 750,000**: AED 250k in-kind support services, AED 250k cash for
equity via an **ADGM-jurisdiction SAFE** on founder-friendly terms that converts only at the next
priced round, and up to a further AED 250k top-up after the one-year Company Building Programme,
for further equity. `[VERIFIED — Hub71 press release + programme page]`

At ≈ **USD 204k**, that is roughly a year of solo runway plus a lab. If the deadline is missed
today, the next cohort is the fallback — check the cycle rather than assuming annual.

---

## 1. What the business actually is

`docs/15` moved the product from "pod" to **small room**, and that changes the pitch more than it
changes the hardware.

| | Value |
|---|---|
| **Form** | 3.5–4 m diameter room, viewers standing at **1.3–1.8 m** from centre |
| **Engines** | 15–19 (`N = 2πz/D`) |
| **Sold as** | **Pairs.** A call needs two ends. |
| **The one claim no competitor can match** | **Multi-viewer.** HP Dimension is one-on-one *by construction*; every viewer in a TAYF room sees the remote person correctly from their own angle. |
| **What it is not** | A better-looking screen. Say "several people in a room" or say nothing. |

Everything else — no headset, no substrate, walk-around, no vergence-accommodation fatigue — is
supporting, not leading. **Accommodation is 268× weaker than disparity** as a depth cue
(`eng/03_PHYSICS/depth_cues.py`) and must never lead a pitch again.

---

## 2. Company formation

### 2.1 Jurisdiction — the actual decision

| Option | Fit | Notes |
|---|---|---|
| **ADGM (Abu Dhabi)** | **Best if taking Hub71** | Hub71's SAFE is ADGM-drafted. Common-law courts, English-language, investor-familiar. Taking Hub71 money effectively picks this for you. |
| **DIFC (Dubai)** | Good | Common law, strong IP and data regime, higher cost. Innovation Licence ~USD 1,500/yr `[UNVERIFIED — inherited from research/2026-08-21_external_feasibility_review.md]` |
| **in5 / DTEC (Dubai free zones)** | Best if self-funding | in5 licence ~AED 1,000/yr, DTEC ~AED 9,500 join fee and **permits a workshop/lab** — which you need. `[UNVERIFIED, same source]` |
| **Mainland LLC** | Only if selling to UAE government directly | More admin; some public tenders require it. |

**Recommendation:** apply to Hub71 today and let ADGM follow. If Hub71 declines, **DTEC** — it is
the cheapest route that legally permits a physical lab, which the bench in
`experiments/perceptual-quality/BENCH.md` requires.

### 2.2 Founder items

- **Golden Visa**, specialised-talent (engineering/AI) route — no monetary investment required.
  `[UNVERIFIED, inherited]` Worth applying early; it decouples your residency from any employer
  or free zone.
- **Student status.** You are an undergraduate. Check whether ADU claims any interest in IP
  created by students, especially if you use university lab time or equipment. **[LAWYER]** — this
  is the single cheapest legal question to answer and the most expensive to get wrong. Ask before
  you borrow a luminance meter from a university lab, not after.
- **Founder vesting.** Even solo. If you never add a co-founder it costs nothing; if you do, its
  absence is the most common way early companies break. **[LAWYER]**

---

## 3. Legal — ranked by how much damage it can do

### 3.1 ⚠ Avatar and likeness data — the biggest and least obvious exposure

A photoreal, live-driven likeness of a real person is **biometric data**.

- **UAE PDPL (Federal Decree-Law No. 45 of 2021)**, in force since **2 January 2022**, treats
  biometric data as **sensitive personal data**: explicit consent, enhanced security, withdrawal
  at any time, enforced by the **UAE Data Office**. `[VERIFIED — multiple independent secondary
  sources read 2026-08-21; primary text not read. **[LAWYER]** before relying on specifics.]`
- **GDPR Art. 9** special category applies to any EU data subject — i.e. the moment one end of a
  call is in Europe.
- **Right of publicity / personality rights** — you are manufacturing a controllable likeness.
- **Deepfake exposure.** The enrolment pipeline that produces a legitimate avatar produces an
  illegitimate one with no modification. This is not hypothetical risk; it is the same artefact.

**What this forces into the architecture, not the paperwork:**

1. **Enrolment consent** that is specific, informed, revocable, and logged.
2. **Deletion that actually deletes** — every derived model, not just the source scan.
3. **Authenticity binding** — a session must be cryptographically bound to a live, consenting
   person, so an avatar cannot be driven without them. Design it in now; retrofitting is
   expensive and, after an incident, worthless.
4. **Data residency** — decide where avatars live before a government customer asks.

This is also a **sales asset**. Sovereign and enterprise buyers will ask, and "we built consent
and revocation into the protocol" is a far better answer than a policy PDF.

### 3.2 IP — file less than you think

From `docs/14` §5, already established:

| Item | Status |
|---|---|
| Pupil-steering scheduling | **Anticipated** — Google **US11474597B2**, active to 2040. Do not file. |
| Avatar enrolment pipeline | **Anticipated** — Mon3tr (arXiv 2601.07518). Do not file. |
| Ring-of-emitters architecture | **Published prior art** — TeleHuman 2, CHI 2018, unpatented by anyone. Free to use, impossible to own. |
| **HOE band mapping N engines to 360° of aperture** | **Survives.** File here. |
| **Multi-engine geometric calibration** | **Survives, narrowed.** File here. |

**Sequence:** file **nothing** until PQ-1 returns. A provisional is cheap (~USD 150 US
micro-entity government fee `[UNVERIFIED]`) but a provisional on the wrong claim starts a
12-month clock you cannot afford to waste. Keep specifics as trade secrets until then.

**Open and unresolved:** whether US11474597B2's angular-pixel-array limitation excludes a ring of
steered projectors. Anticipation blocks *owning* it; whether it blocks *using* it is a
claim-construction question. **[LAWYER]** — and get this answered before Stage 2 spend, not
before Stage 5.

### 3.3 Eye safety and product liability

The device puts controlled light toward people's eyes for the length of a meeting.

- **Use LEDs, not lasers.** LEDs fall under **IEC 62471** photobiological safety (Risk Groups
  RG0–RG3) rather than **IEC 60825-1** laser classification. `[VERIFIED at secondary level —
  inherited from the external review, corroborated as standard practice; **[ASSESSOR]** must
  confirm per design.]` `docs/13` §4 shows ~1,000× light headroom, so spending it on the easier
  regulatory path is free.
- **Fail-dark.** Loss of tracker lock must kill emission. This is a safety argument *and* a
  liability argument.
- **Product liability insurance** before the first unit leaves the building. Quote it early — an
  optical device aimed at faces may attract questions a generic policy will not answer.
- **Flicker.** Depth-plane or refresh structure must be checked against photosensitive-epilepsy
  guidance. `[UNVERIFIED — standard not identified]` **[ASSESSOR]**

### 3.4 Export control and import

- High-end SLMs, certain lasers, and some precision optics carry **dual-use / EAR** flags. Check
  the **ECCN per line item** before ordering. `[UNVERIFIED, inherited]` `docs/15` deleting the
  swept-focus element **materially reduces this exposure** — DMDs and LEDs are ordinary commerce;
  phase SLMs and pulsed lasers are not.
- **UAE import duty** is commonly 5% on goods entering the mainland; free-zone import for
  re-export is typically duty-suspended. **[ACCOUNTANT]**

### 3.5 Contracts you will need before the first sale

Purchase/lease agreement with acceptance criteria, SLA (uptime, response time, calibration
drift), data-processing agreement, NDA for site access, and an installation/site-readiness
schedule specifying power, floor loading, ceiling height and blackout. **[LAWYER]**

---

## 4. Regulatory and certification path

Not glamorous, and it will gate shipping.

| Item | Applies | When |
|---|---|---|
| **IEC 62471** photobiological safety | Yes, LED sources | Before any customer demo with the public |
| **CE / UKCA** | If selling into EU/UK | Before first EU shipment |
| **UL / NRTL** | If selling into US | Before first US shipment |
| **EMC** (emissions/immunity) | Yes | With CE/UL |
| **RoHS / WEEE** | EU | With CE |
| **TDRA type approval** | Any radio in the product (Wi-Fi/5G) | Before UAE sale |
| **Civil defence / fire** | An enclosed room installed in a building | Per venue, per emirate |

**Budget 3–6 months and USD 15–40k for a first certification pass** `[UNVERIFIED — no quotes
obtained]`. Start conversations with a test house at Stage 2, not Stage 5.

---

## 5. The full cost stack

Built up from `docs/13` §10 as corrected by `docs/15` (fixed-focus engines, N = 15).

### 5.1 Per unit

| Line | Prototype | Volume (100 u) |
|---|---|---|
| BOM | $101,000 | $42,000 |
| Freight + duty (~5%) | — | $2,500 |
| Assembly + test (~40 h) | — | $1,200 |
| Calibration (skilled, ~8 h) | — | $500 |
| Packaging / crating | — | $800 |
| Warranty reserve (~8% BOM) | — | $3,400 |
| **Factory cost** | | **≈ $50,400** |
| Installation (2 people, 2 days, travel) | — | $4,000 |
| **Delivered cost** | | **≈ $54,400** |

At a **$180,000** list price the gross margin is **~70%**, and the product sells in **pairs**:
**~$360,000 per customer relationship.** `[DERIVED from UNVERIFIED BOM inputs — every figure
above inherits `hardware/bom.md`'s unresolved pricing.]`

### 5.2 Recurring

$2,000–4,000 per room per month: avatar enrolment, calibration-drift correction, updates,
support. Recurring revenue is what makes the company fundable; the hardware is the wedge.

### 5.3 Getting to a decision — what you actually spend next

| Stage | Cost | Gate |
|---|---|---|
| **PQ-1 bench** | **$215** | `BENCH.md` |
| Certification conversations | $0 | Stage 2 |
| Wedge | $4,000–15,000 | PQ-1 returns GO |
| HOE test tile (Ceres/Covestro/university) | $100k–400k | wedge passes |
| First full room | several $M | — |

**The next decision costs $215.** Everything below it is gated behind an experiment whose
analysis is already pre-registered and validated (`experiments/perceptual-quality/pq1_analyze.py`).

### 5.4 Solo burn

Free-zone licence, incubator desk, frugal living in Abu Dhabi or Dubai: order **USD 3–5k/month**,
so **$40–60k for year one** `[ASSUMED — not costed against real quotes]`. Hub71's AED 250k cash
(≈ USD 68k) covers roughly that year. **[ACCOUNTANT]**

---

## 6. Logistics

- **Long-lead items:** custom HOE film is a *fabrication programme*, not a purchase — assume
  months and a contract partner (Ceres Holographics / Covestro / a university holography lab).
  DMD dev kits and optics are weeks. Order the long pole first.
- **Single-source risk:** the HOE band has no second supplier today. That is a company-level
  dependency, not a purchasing detail.
- **Shipping a 4 m room:** it must break into crates that fit a standard container and a service
  lift, and reassemble to sub-millimetre optical alignment. **Design for disassembly from the
  first drawing** — this constraint kills more installed-hardware companies than physics does.
- **Site requirements** become a contract schedule: floor loading, ceiling height, power (~1.4 kW
  after the `docs/15` correction, one 20 A circuit), **HVAC** (1.4 kW inside a small enclosed
  room is a real thermal problem and a noisy pod is unsellable), blackout, and network.
- **Service model:** 15–19 engines in a sealed room, calibrated to sub-millimetre. Remote
  diagnostics and field-swappable engine modules, or every fault becomes a flight.

---

## 7. Go-to-market, and the two-ended problem

`docs/13` §13 risk 7, promoted by the external review to **risk 1**: a room is worthless alone.
Cisco sold TelePresence rooms and wrote them down when good-enough video went free; ARHT Media's
equity collapsed to roughly C$0.02. `[UNVERIFIED, inherited]`

**Three structures, in order of preference for a solo founder:**

1. **Sell through a carrier.** e&, du, STC, Zain, Ooredoo want an anchor use case for 5G SA and
   edge compute — which a TAYF room genuinely needs. They bring colo, the QoS slice, and the
   enterprise relationship; you bring hardware and software and take a revenue share. Far easier
   than selling $180k boxes direct, and it is the pitch GSMA judges are primed for.
2. **Own both ends: hub network, sell sessions.** Kills the chicken-and-egg by construction —
   nobody buys a cinema, they buy a ticket. But location-based immersive capex is brutal
   (Sandbox VR venues $250k–1.9M, >60% utilisation to protect margin; The VOID failed)
   `[UNVERIFIED, inherited]`, and a minimum viable network is **two paired hubs**, e.g. a
   Dubai–London corridor. **This is a second, capital-hungry company. Not v1.**
3. **Direct sale in pairs.** Only into buyers who already have two sites and a reason.

**Beachhead:** luxury retail and flagship brand activations — marketing budget, fast decisions,
buys on wow, and tolerant of a controlled-lighting room. **Highest willingness to pay:**
sovereign and diplomatic. **Cleanest ROI story:** energy and heavy industry remote expert, where
you compare against travel cost and downtime hours.

---

## 8. Timeline

| When | What |
|---|---|
| **Today, 21 Aug 2026** | Hub71 Cohort 20 deadline |
| Aug–Sep | Order PQ-1 parts, build bench, measure η_RR |
| Sep–Oct | Run PQ-1: 26 subjects, 180 trials, ~36 min each |
| Oct | **Go / pivot / stop.** Everything below is gated here. |
| Oct–Dec | Wedge, if GO. Certification conversations. **[LAWYER]** on ADU IP and on US11474597B2 |
| 2027 | HOE tile programme, raise on the wedge video |

The **GSMA Prototype Phase (13 Sep 2026)** falls mid-PQ-1. You will have a working bench, real
measured η_RR, a governing equation, and a pre-registered study — not a floating head. Pitch the
*method*: "here is the equation, here is the experiment that decides it, here is the number
nobody has ever measured." For a judging panel that has seen ten rendered mock-ups, that is a
stronger position than it feels like.

---

## 9. What must not be actioned from this document

| Item | Who |
|---|---|
| ADU's claim on student-created IP | **[LAWYER]** — ask first |
| Whether US11474597B2 blocks *use* | **[LAWYER]** — before Stage 2 spend |
| PDPL / GDPR avatar-consent architecture | **[LAWYER]** |
| Entity choice and the Hub71 SAFE terms | **[LAWYER]** + **[ACCOUNTANT]** |
| IEC 62471 risk group, flicker, AEL | **[ASSESSOR]** |
| ECCN per optical line item | **[LAWYER]** / freight forwarder |
| Duty, VAT, free-zone treatment | **[ACCOUNTANT]** |

**Every price in §5 inherits `hardware/bom.md`, where all pricing is `[UNVERIFIED]` and blocked
on a research pass that was killed mid-run.** Treat the cost stack as a *structure* that is
correct and a set of *numbers* that are not yet real.
