# Bill of Materials

> **⚠ REWRITTEN 2026-08-21.** The previous version costed a **10 cm cube** — Jetson Orin, a
> synchronised camera array, a 5G modem, an undecided optical engine. That is the wrong
> architecture, not merely stale pricing. The product is now **THE ROOM** (`docs/13`), and the
> cube variant is TAYF-C35 (`docs/11`). The old capture/compute lines survive in
> `docs/04_CUBE_HARDWARE_AND_PROTOTYPE_ENGINEERING.md`.

**Status: every price below is `[UNVERIFIED]`.** No vendor quote has been obtained for any line.
The pricing pass is specified and handed off — see `research/2026-08-21_external_feasibility_review.md`
and the follow-up brief. **Order nothing from this file.**

---

## 1. What changed the BOM most

`docs/15_THE_ACCOMMODATION_BUDGET.md` showed a person fits inside a **single depth-of-field
slab** at pod distance, so the display needs **1–2 focal planes, not 24–32**. That deleted:

- the swept-focus element,
- the 2,700 Hz plane-switch requirement,
- deformable mirrors at $10–50k each,
- and the TAG-lens / PB-FLC-stack investigation entirely.

**The engines are fixed focus.** The line did not shrink — it disappeared. `N` also fell from 24
to **15** at the design point (`z = 1.2 m`, `D = 0.5 m`, `N = 2πz/D`).

## 2. Per-room BOM — THE ROOM, N = 15

| Item | Spec | Qty | Unit | Total |
|---|---|---|---|---|
| Display engine | DLP7000/DLP9500-class DMD + high-CRI LED + **fixed-focus relay** + driver | 15 | $900 | $13,500 |
| HOE / relay band | angularly-multiplexed vHOE, ~6.6 m² | 1 | $2,000/m² proto | $13,200 |
| Render node | 2× workstation GPU + host; 8 eye-views of a splat avatar at 90 Hz | 1 | — | $18,000 |
| Tracking | 6× global-shutter IR camera + illuminators + host | 1 | — | $6,000 |
| Structure | room shell, blackout, acoustics, power, thermal | 1 | — | $25,000 |
| Integration | calibration rig, cabling, labour | 1 | — | $30,000 |
| **Prototype BOM** | | | | **≈ $101,000** |
| **Volume BOM** (100 u; HOE $300/m², engine $450) | | | | **≈ $42,000** |

Full delivered-cost stack, margin and pricing: `docs/16_BUSINESS_LEGAL_AND_LOGISTICS.md` §5
(volume BOM $42,000 → factory $50,400 → delivered $54,400).

**Power: ≈ 1.4 kW** — 15 engines × ~40 W + GPUs ~600 W + tracking/host ~200 W. One 20 A circuit.
Thermal is the real constraint: 1.4 kW inside a small enclosed room needs quiet active cooling,
and a telepresence room that roars is unsellable.

## 3. Component notes

- **DMD.** Not the bottleneck and off-the-shelf: DLP7000 (0.7″ XGA) reaches 32,225 Hz binary with
  the DLPC410 controller; DLP9500 (1080p) 23,148 Hz. Dev kits from ViALUX, Digital Light
  Innovations, In-Vision, TI. `[UNVERIFIED — inherited from the external review, no quote]`
- **Sources: LEDs, not lasers.** `docs/13` §4 shows ~1,000× light headroom (pupil-steered
  delivery needs ~14 lm of source), so spend it on the easier regulatory path — LEDs fall under
  **IEC 62471** rather than IEC 60825-1 laser classification. This also removed phase SLMs and
  pulsed lasers from the BOM, which **cuts export-control exposure** (`docs/16` §3.4).
- **HOE band — the single-source risk and the only real moat.** Covestro **Bayfol HX** photopolymer
  with **Ceres Holographics** roll-to-roll replication is the candidate fabrication spine. This is
  a *fabrication programme*, not a purchase: NRE for mastering, MOQ and lead time all unknown.
  No second supplier exists today. Order the long pole first.
- **Explicitly rejected: scanned-beam engines.** A galvo/MEMS scanner draws 10⁶–10⁷ points/s
  against a requirement of 7.2×10⁸. Loses by two orders of magnitude. Do not revisit (`docs/13` §7).

## 4. What actually gets bought next

Not this. **The PQ-1 bench, ≈ $215** — beamsplitter, retroreflective sheeting, two identical
figurines, a small panel, a stepper carousel, blackout. Parts list and build order in
`experiments/perceptual-quality/BENCH.md`. It measures **η_RR** — never measured by anyone, and
the number every brightness figure above quietly depends on — and answers whether a free-space
image is perceptibly better than a screen at the same location.

Everything in §2 is gated behind that result.

## 5. Blocking before any order

1. Real vendor quotes for every §2 line at qty 1 and qty 100 — **handed off, not done**.
2. Will Ceres/Covestro quote a bespoke 6.6 m² angularly-multiplexed band to a pre-revenue
   startup? If not, who does?
3. ECCN classification per optical line item (`docs/16` §3.4).
4. IEC 62471 risk-group determination for the chosen LED and optic (`docs/16` §4).
