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
| **in5 / DTEC (Dubai free zones)** | Cheapest, **but see the warning below** | DTEC setup ~**AED 16,715–18,375** incl. flexi-desk + 2 visa quota; service licence ~AED 5,000/yr for 5 years then AED 8,000. in5 is an incubator you apply to, not a licence you buy. `[SECONDARY, 2026 setup advisors]` |
| **Mainland LLC** | Only if selling to UAE government directly | More admin; some public tenders require it. |

> ### ⚠ CORRECTED 2026-08-21 — the workshop claim was wrong, and it was the reason for the recommendation
> This section previously said DTEC *"permits a workshop/lab — which you need."* **That is
> unverified and probably false.** DTEC and in5 are co-working and office environments; a
> flexi-desk almost certainly does **not** permit a mains-powered optics workshop. Building the
> PQ-1 bench likely needs a **light-industrial licence and a physical unit** — Dubai Silicon Oasis
> proper, Dubai Industrial City, SRTIP (Sharjah), or a KIZAD / Masdar City unit in Abu Dhabi.
>
> **Action: ask the DTEC/DSOA licensing desk in writing** whether "scientific/technical R&D +
> prototype assembly" is permitted in your leased space. `[UNVERIFIED — CRITICAL]` Do this before
> paying for any licence, because it is the licence's whole purpose.

**Recommendation:** apply to Hub71 and let ADGM follow. Otherwise pick the jurisdiction *after*
resolving the workshop question above — the cheapest licence that forbids the bench is worthless.

**Tax:** free zones give 100% foreign ownership and 0% corporate tax on qualifying income (QFZP);
9% above AED 375k on non-qualifying income. **[ACCOUNTANT]**

### 2.2 Founder items

- **Golden Visa — corrected 2026-08-21.** The earlier "no monetary investment required" was
  wrong for the ordinary route. The skilled-professional path requires MoHRE Level 1/2, an
  attested bachelor's degree, and **AED 30,000/month *basic* salary** — and per **Fragomen
  (January 2026) allowances no longer count toward it**, sustained over the preceding two years,
  reversing an August 2024 relaxation. `[VERIFIED — ADDED/ADRO + Fragomen]`
  **You will not meet that test as an undergraduate.** The realistic paths are the
  **specialised-talent nomination route** — where a formal nomination or endorsement by a UAE
  authority *waives the salary threshold*, processed via GDRFA — or the **outstanding-student**
  route (GPA ≈ 3.75+). A granted patent strengthens the nomination case, which is another reason
  the IP sequence in §3.2 matters. Government fees ~AED 4,695–10,140.
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

#### ⚠ EU AI Act Article 50 — resolved 2026-08-21, and it changes the roadmap

I flagged this as an unexamined hole. It is now answered `[VERIFIED — EC primary + law-firm
analyses]`:

- **Transparency obligations are in force from 2 August 2026.** They are live now.
- A live-driven photoreal avatar of a real person **is a "deepfake" under Art. 50**: the deployer
  must disclose it is AI-generated or manipulated, and the **provider must mark the output
  machine-readably.** Marking has a grace period to **2 December 2026** (AI Omnibus, in force
  27 July 2026).
- **Tier: limited-risk / transparency — NOT high-risk.** The system is not an Annex III use case
  and is not biometric identification. **Keep it that way:** adding biometric *identification* or
  *emotion recognition* would risk jumping to high-risk or to prohibited under Art. 5.
- **Fines** up to €15M or 3% of worldwide turnover — but **Art. 99(6) applies the lower figure to
  SMEs and startups**, which caps a small company's exposure near five figures. Materially less
  frightening than the headline.

**Roadmap consequence: machine-readable marking and a disclosure UX must exist in the render
pipeline before any EU shipment.** The good news is that requirement 3 below — cryptographic
session binding, which was already planned for anti-deepfake provenance — **is** the compliance
mechanism. Pair it with **C2PA content-provenance signing** and one control satisfies both.

#### The UAE pairing that makes consent legally load-bearing

**UAE PDPL (Decree-Law 45/2021)** `[VERIFIED — primary decree text]` defines Biometric Data as
data allowing or confirming unique identification *"such as facial images"*, and classes it as
Sensitive Personal Data. Requirements: consent unless a listed lawful basis (Arts. 4–6), a DPO
where large-scale sensitive processing occurs (Art. 10), a **DPIA for high-risk or new technology
(Art. 21)**, breach notification to the UAE Data Office, and cross-border transfer only to
adequate jurisdictions or with safeguards.

> **Open:** whether a *rendered* likeness is itself biometric data turns on whether it "allows
> unique identification" and is **genuinely arguable**. The *capture* scan clearly is. **Safe
> design assumption: treat both as sensitive personal data.** Also unresolved — the **Executive
> Regulations status is reported inconsistently** (some sources say issued 2023, others pending).
> `[UNVERIFIED — confirm with counsel, do not assume final.]` Federal enforcement to date is
> limited; DIFC and ADGM run separate, more active regimes.

**GDPR Art. 9** is narrower than I implied: biometric data is special-category **only when
processed "for the purpose of uniquely identifying a natural person."** Both readings live — a
telepresence avatar arguably *represents* rather than *identifies*, but enrolment processes facial
geometry and any matching step brings Art. 9 in. EDPB Guidelines 05/2022 and 3/2019 make the
purpose test decisive. **No settled CJEU case law on live photoreal avatars.**

**UAE Decree-Law 34/2021 (Cybercrimes)** `[VERIFIED — primary]` criminalises fabricating or
processing recordings and images with intent to defame or harm: Art. 44 (recording/sharing without
consent — imprisonment plus AED 150k–500k), Arts. 52/54 (fabricated content, AED 100k–1M). The
Cybersecurity Council issued a deepfake warning in 2025 and ~10 arrests followed in March 2026
`[SECONDARY]`. **Your enrolment pipeline produces exactly the artefact this law criminalises when
misused** — which is why the consent and provenance controls below are legal architecture, not
policy.

**What this forces into the architecture, not the paperwork** — all four validated by the research
pass, two strengthened:

1. **Enrolment consent** that is specific, informed, revocable, and logged. **Extend:**
   tamper-evident, per-session.
2. **Deletion that actually deletes** — every derived model, not just the source scan.
   **The single most important control**, and it must be *contractual*, because the law does not
   yet clearly compel deletion of a trained model on revocation.
3. **Authenticity binding** — a session cryptographically bound to a live, consenting person.
   **Strengthened:** it proves liveness under the anti-deepfake laws *and* is the EU AI Act Art. 50
   marking mechanism. **Pair with C2PA signing.**
4. **Data residency** — offer UAE-resident and EU-resident processing, and **default to
   on-premise/in-room processing** to minimise transfer exposure entirely.

**Licence drafting note:** a valid likeness licence needs named grantor, defined uses, duration,
territory, sublicensing, revocation, and **explicit consent to create AND retain a trained model**.
Revocation must contractually trigger derived-model deletion. **[LAWYER]**

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

#### ⚠ The FTO threat was mis-sized — corrected 2026-08-21

I told you to get US11474597B2 answered before Stage 2. That was the right instinct pointed at
the wrong patent.

**US11474597B2 is probably designable-around.** `[VERIFIED — USPTO full text + assignment
history]` It is **Google LLC, originating at Raxium Inc.** (inventors → Raxium 2021-07-08 →
Google 2022-08-25), priority 2019-11-01, granted 2022-10-18, active to **2040-11-02**. Claim 1 is
tied to two things a steered-projector ring plausibly practises neither of:

1. *"an array of angular pixels"* that **emit** light — an emissive panel of angularly-varying
   pixels (Raxium's microLED heritage), not discrete projectors throwing converging wavefronts
   onto an HOE; and
2. a specific **hierarchical** viewer → head → eye tracking sequence.

Their side would argue doctrine of equivalents — a steered projector as "one angularly-varying
pixel". **The hierarchical-tracking limitation is your strongest distinguishing feature.** A
prosecution-history estoppel check still needs an attorney pulling the file wrapper (pre-grant
publication US20210132693A1), asking specifically whether *"array of angular pixels"* was narrowed
to overcome prior art.

**The real exposure is Light Field Lab.** ~471 patents, **~391 active**, several 2017–2020 filings
running to **2037–2040**, with claims over converging wavefronts, phase-guide/energy-relay
structures and 4D-plenoptic rendering (e.g. US11624934). **Their claim vocabulary overlaps ours
directly** — "converging wavefronts forming a real image" is our own language. This is where a
genuine blocking claim is most likely to surface and it needs a **paid claim-by-claim opinion
before shipping.** `[count SECONDARY]`

**And a new one that touches the bench:** the **Asukanet / Utsunomiya (Yamamoto) AIRR family** —
Asukanet micro-mirror-array plates (US8702252) and multiple Yamamoto retroreflection patents
(US11340475, US11300810, US12196977). **If any retroreflective element is used, these must be
cleared.** An HOE band is a meaningful design-around; a retroreflector is not. See the note now in
`experiments/perceptual-quality/BENCH.md`.

**Good news:** the **USC ICT 360° family** (US8432436B2, priority 2007) is **expired or
near-expired**. Low FTO risk, and it works *for* you as prior art.

**Also corrected:** the "InterDigital/PCMS family claiming eye-tracking-to-reduce-views" I asked
about does not exist as I described it — that concept is in the Google/Raxium 597's own
specification. A distinct InterDigital family does exist in multi-view telepresence
(**US10701318B2**, PCMS Holdings → InterDigital VC Holdings 2023-03-07). I half-remembered two
patents as one.

**Revised sequence: an FTO opinion centred on Light Field Lab's active claims, plus the
AIRR/Asukanet family if any retroreflector survives into the product. [LAWYER]** — budget for it;
this is the item most likely to surface a genuine blocker.

### 3.3 Eye safety and product liability

The device puts controlled light toward people's eyes for the length of a meeting.

- **Use LEDs, not lasers.** LEDs fall under **IEC 62471** photobiological safety (Risk Groups
  RG0–RG3) rather than **IEC 60825-1** laser classification. `[VERIFIED at secondary level —
  inherited from the external review, corroborated as standard practice; **[ASSESSOR]** must
  confirm per design.]` `docs/13` §4 shows ~1,000× light headroom, so spending it on the easier
  regulatory path is free.
- **Fail-dark.** Loss of tracker lock must kill emission. This is a safety argument *and* a
  liability argument.
- **Product liability insurance** before the first unit leaves the building. **Resolve IEC 62471
  first** — the research pass found the RG classification is likely a *rating factor* and a
  completed photobiological report likely a *condition of cover*, so the certification gates the
  insurance, not the other way round. UAE carriers/brokers to approach: **GIG Gulf (AXA Gulf),
  Sukoon (Oman Insurance), Orient Insurance**, and internationally **Marsh, Aon, WTW**. Ask
  explicitly whether *"optical radiation to the eye"* is an exclusion that must be bought back.
  `[UNVERIFIED — no quote obtained]` Quote it early — an
  optical device aimed at faces may attract questions a generic policy will not answer.
- **Flicker — standards identified 2026-08-21.** The governing references are **IEEE Std
  1789-2015** (LED current-modulation flicker) and, for seizure-provoking content, **ITU-R BT.1702**
  plus the WCAG "three flashes" threshold. **There is no dedicated standard for
  temporally-multiplexed volumetric displays** — a genuine gap, which means an assessor's judgement
  rather than a checkbox. Ask the test house's photobiology lab *and* an ophthalmic human-factors
  expert, specifically about depth-plane-switching temporal artefacts. **[ASSESSOR]**

### 3.4 Export control and import

**Researched 2026-08-21** `[VERIFIED framework — BIS / Federal Register]`:

- **DMDs.** Standard *visible* DLP7000/9500 parts are widely commercially available; the
  controlled cases (CCL Cat. 3, 3A001) are largely UV and specialised. A visible DMD is **very
  likely EAR99 or low-control** — but get the ECCN in writing from TI or the design house per part.
- **IR tracking cameras.** ECCN **6A003.b.4** controls imaging cameras by frame rate and detector
  count, and the heavily controlled items are **thermal (LWIR)**. A global-shutter **near-IR
  silicon** tracking camera sits well below the thresholds and is typically EAR99 or lightly
  NS-controlled. Confirm per model.
- **Precision relay optics.** Mostly EAR99.
- **The claim that deleting the swept-focus element cut this exposure is CONFIRMED**
  `[VERIFIED]`: pulsed lasers (6A005) and some SLMs carry heavier controls, and a
  DMD + LED + NIR-silicon-camera design is a materially lower-control profile. `docs/15` bought a
  regulatory saving as well as a cost one.
- The UAE is not comprehensively embargoed, but **end-use/end-user screening (BIS Consolidated
  Screening List) still applies.** Get a written ECCN classification per part before first import.
- **UAE import duty** is commonly 5% on goods entering the mainland; free-zone import for
  re-export is typically duty-suspended. **[ACCOUNTANT]**

### 3.5 Contracts you will need before the first sale

What enterprise/installed-AV buyers actually expect `[VERIFIED — market-standard shape]`:

- **Purchase or lease agreement with acceptance testing** — milestone criteria (image quality,
  multi-viewer angular coverage, uptime), sign-off gating final payment, warranty. Use
  **IEC 62629-52-1 (2024)** as the objective measurement basis.
- **SLA with calibration-drift terms** — uptime %, response and resolution times, recalibration
  cadence, convergence-error thresholds that trigger a service visit, remedies and credits.
- **Data Processing Agreement** — GDPR Art. 28 / UAE PDPL processor terms for avatar data:
  sub-processors, security, breach notification, and **deletion on termination**, which ties
  directly to §3.1 requirement 2.
- **Site-readiness schedule** — room dimensions (3.5–4 m), mains load, HVAC and thermal, ambient
  light control, floor loading, network. A standard AV site-survey annex.
- **Reciprocity clause.** Sold in pairs, so **both endpoints must meet spec** or the multi-viewer
  experience does not exist. Model it on Google Beam's both-ends-licensed requirement.

Named resources: an AV-integration lawyer, and **AVIXA (InfoComm)** contract frameworks.
**[LAWYER]**

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

**Named test houses reachable from the UAE:** Intertek, TÜV Rheinland, Nemko, Bureau Veritas,
SGS. `[VERIFIED]` **Cost and calendar remain `[UNVERIFIED]`** — priced per light source, so get
quotes early; the insurer in §3.3 will require the report.

**IEC 62471 detail** `[VERIFIED — primary IEC]`: governs optical radiation 200–3000 nm and
classifies **RG0** (unlimited exposure) / **RG1** (≤10,000 s) / **RG2** (≤100 s) / **RG3**
(≤0.25 s) by maximum permissible exposure at a viewing distance. For a face-aimed device this is
*the* critical test, and **landing at RG1 or below carries the entire safety case.**

**UAE TDRA type approval** `[VERIFIED — primary TDRA]`: mandatory for any device containing a
radio (Wi-Fi, Bluetooth, GNSS). Three tiers by risk — **Level 1 = 1 working day, Level 2 = 5,
Level 3 = 10**; certificate valid **3 years**; requires a UAE-registered supplier/dealer and
ILAC-accredited test reports (CE reports generally accepted, local sample testing occasionally
required). Telecom licensing application fee **AED 10,000, non-refundable** `[SECONDARY]`.
**If the room carries no intentional radio, TDRA may not apply at all** — but any Wi-Fi control
link triggers it, which is a genuine architecture lever. Separately, **ECAS/MOIAT** conformity
applies to regulated electricals via notified bodies `[SECONDARY]`.

**Acceptance-testing standard:** **IEC 62629-52-1 (2024), "3D displays — fundamental measurements
of aerial display"** exists `[VERIFIED]` and is the natural objective basis for customer
acceptance criteria — and for PQ-1's own measurement methodology.

## 5. The full cost stack

Built up from `docs/13` §10 as corrected by `docs/15` (fixed-focus engines, N = 15).

### 5.1 Per unit

> ### ⚠ CORRECTED 2026-08-21. The gross-margin thesis is now unproven.
> The pricing pass returned **one** primary-source component price and it broke the engine line
> by ~3×: **$2,195** for a Digital Light Innovations DLP7000UV DMD board assembly `[VERIFIED]`,
> against the **$900** assumed here. TI sells the DMD only as part of a chipset through
> authorised design houses, so a board is the real purchasing unit.
>
> **19 DMD boards at qty 1 = $41,705, which alone exceeds the $42,000 volume BOM claimed below.**

| Line | Prototype (qty 1) | Volume (100 u) |
|---|---|---|
| BOM | ~~$101,000~~ **$141,500** | ~~$42,000~~ **UNRESOLVED** |
| Freight + duty (~5%) | — | — |
| Assembly, test, calibration | — | — |
| Packaging, warranty reserve | — | — |
| **Factory cost** | | **not computable** |
| Installation | — | — |
| **Delivered cost** | | **not computable** |

**The $180,000 list at ~70% gross margin is withdrawn until a volume quote exists.** At qty-1
pricing the delivered cost exceeds the list price. The arithmetic was internally consistent; its
inputs were not researched. Recovering it needs written **ViALUX / Digital Light Innovations**
pricing at qty 100 — the single most load-bearing unknown in the model, and the number most
likely to be wrong in front of an investor.

**Threshold that changes the plan:** if the HOE band exceeds **~$15k/unit** at low volume, or
carries a **>6-month lead time**, the pricing thesis breaks and the product must be re-priced or
re-architected.

### 5.2 Recurring

$2,000–4,000 per room per month: avatar enrolment, calibration-drift correction, updates,
support. Recurring revenue is what makes the company fundable; the hardware is the wedge. **This
is now the more defensible half of the model**, because it does not depend on the unresolved BOM.

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
| **FTO opinion centred on Light Field Lab's ~391 active claims**, plus AIRR/Asukanet if any retroreflector survives | **[LAWYER]** — the item most likely to surface a real blocker |
| US11474597B2 file-wrapper estoppel: was "array of angular pixels" narrowed to overcome prior art? | **[LAWYER]** — lower priority than it looked |
| PDPL **Executive Regulations** status — issued or pending? Sources conflict | **[LAWYER]** |
| Whether DTEC/in5 permits a **mains-powered optics workshop** | **licensing desk, in writing — do this first** |
| PDPL / GDPR avatar-consent architecture | **[LAWYER]** |
| Entity choice and the Hub71 SAFE terms | **[LAWYER]** + **[ACCOUNTANT]** |
| IEC 62471 risk group, flicker, AEL | **[ASSESSOR]** |
| ECCN per optical line item | **[LAWYER]** / freight forwarder |
| Duty, VAT, free-zone treatment | **[ACCOUNTANT]** |

**The pricing pass ran** (`research/2026-08-21_costing_and_legal_research.md`) and returned
exactly **one** primary-source component price — which broke the engine line by ~3× and withdrew
the gross-margin claim (§5.1). Everything else was correctly refused rather than estimated.
**Treat the cost stack as a structure that is sound and a set of numbers that are still mostly
unresolved**, with the ViALUX/DLi volume quote and the Ceres HOE quote as the two that decide
whether the business case exists at all.

---

## 10. The three findings that most change the plan

1. **The HOE band is unpriceable today and probably exceeds the supplier's demonstrated
   capability** — Ceres tops out at 1400 mm film width and an A2 master area, against a 6.6 m²
   angularly-multiplexed band, and their entire focus is automotive OEMs. It is simultaneously the
   moat and the single-source risk. Until a written $/m² + MOQ + NRE + lead-time quote exists, the
   cost model and the margin claim are unproven.
2. **EU AI Act Art. 50 is live now (2 August 2026)** and needs machine-readable marking plus a
   disclosure UX in the render pipeline before EU shipment — but it lands in the **limited-risk**
   tier, not high-risk, and SME fine caps limit the downside. The cryptographic session binding
   already planned **is** the compliance mechanism; pair it with C2PA.
3. **The patent to fear is not the one I named.** Google/Raxium's 597 has a strong literal
   non-infringement argument. **Light Field Lab's ~391 active patents**, several in force past
   2035, use the same "converging wavefront" vocabulary as this design. That is where a blocking
   claim would come from, and it needs a paid opinion.
