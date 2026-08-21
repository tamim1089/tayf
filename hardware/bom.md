# Bill of Materials

> **⚠ REWRITTEN 2026-08-21.** The previous version costed a **10 cm cube** — Jetson Orin, a
> synchronised camera array, a 5G modem, an undecided optical engine. That is the wrong
> architecture, not merely stale pricing. The product is now **THE ROOM** (`docs/13`), and the
> cube variant is TAYF-C35 (`docs/11`). The old capture/compute lines survive in
> `docs/04_CUBE_HARDWARE_AND_PROTOTYPE_ENGINEERING.md`.

**Status: one price is `[VERIFIED]`; every other is `[UNVERIFIED]`.** The pricing pass ran and
its results are in `research/2026-08-21_costing_and_legal_research.md`. It returned exactly one
primary-source component price — and that price **broke this file's engine line by ~3×** (§2).
Everything else was correctly refused rather than estimated. **Order nothing from this file.**

---

## 1. What changed the BOM most

`docs/15_THE_ACCOMMODATION_BUDGET.md` showed a person fits inside a **single depth-of-field
slab** at pod distance, so the display needs **1–2 focal planes, not 24–32**. That deleted:

- the swept-focus element,
- the 2,700 Hz plane-switch requirement,
- deformable mirrors at $10–50k each,
- and the TAG-lens / PB-FLC-stack investigation entirely.

**The engines are fixed focus.** The line did not shrink — it disappeared.

`N` is **19**, not the 15 an earlier revision used: viewers stand *inside* the aperture ring, so
`z > R` is forced, and with the design point at `R = 1.3 m` that puts the band at `z = 1.5 m` →
`N = 2πz/D = 19` at `D = 0.5 m` (`docs/13` §1.1).

## 2. Per-room BOM — THE ROOM, N = 19

> ### ⚠ CORRECTED 2026-08-21 by a researched price. The engine line was wrong by ~3×.
> The previous version costed the display engine at **$900**. The one primary-source price now
> in hand is **$2,195** — Digital Light Innovations' DLP7000UV DMD Remote Board Assembly, in
> stock `[VERIFIED, vendor page — see research/2026-08-21_costing_and_legal_research.md §1]`.
> TI sells the DMD only as part of a chipset through authorised design houses, so a board
> assembly is the real unit of purchase.
>
> **At that price, 19 DMD boards alone cost $41,705 — which by itself exceeds the $42,000
> *volume* BOM this file previously claimed.** Two caveats, both real: the verified board is the
> **UV** variant and the visible-light part may be cheaper `[UNVERIFIED]`, and ViALUX publishes
> no prices at all. Neither rescues the old number.

| Item | Spec | Qty | Unit | Total |
|---|---|---|---|---|
| **Display engine** | DLP7000-class DMD board + LED + **fixed-focus relay** + driver | 19 | **$2,595** | **$49,305** |
| HOE / relay band | angularly-multiplexed vHOE, ~6.6 m² | 1 | $2,000/m² est. | $13,200 |
| Render node | 2× RTX 6000 Ada / RTX PRO 6000-class + host | 1 | — | $18,000 |
| Tracking | 6× global-shutter NIR camera + illuminators + host | 1 | — | $6,000 |
| Structure | room shell, blackout, acoustics, power, thermal | 1 | — | $25,000 |
| Integration | calibration rig, cabling, labour | 1 | — | $30,000 |
| **Prototype BOM (qty 1)** | | | | **≈ $141,500** |
| **Volume BOM (100 u)** | | | | **UNRESOLVED** |

**The volume BOM is no longer stated.** It previously read $42,000, which the verified board
price refutes at qty 1 and which no volume quote supports. It is recoverable only with written
ViALUX / Digital Light Innovations pricing at qty 100 — **`[UNVERIFIED]`, and the single most
load-bearing unknown in the cost model.**

**Consequence for the business case:** `docs/16` §5's $180,000 list at ~70% gross margin
**depends entirely on that unobtained volume quote.** At qty-1 pricing the delivered cost exceeds
the list price. This is stated plainly rather than smoothed over — it is the number most likely
to be wrong in front of an investor.

**Power: ≈ 1.6 kW** — 19 engines × ~40 W + GPUs ~600 W + tracking/host ~200 W. Still one 20 A
circuit; thermal inside a small enclosed room remains the real constraint.

## 3. Component notes

- **DMD.** Not the *technical* bottleneck — DLP7000 (0.7″ XGA) reaches 32,225 Hz binary with the
  DLPC410 controller; DLP9500 (1080p) 23,148 Hz — but it **is** the cost bottleneck. TI sells the
  DMD only as part of a chipset via authorised design houses: **Digital Light Innovations**
  (DLP7000UV board assembly **$2,195**, `[VERIFIED]`), **ViALUX** (V-Modules and complete STAR-07
  optical modules with LED, optics and active cooling — **no published prices, quote required**),
  In-Vision, TI EVMs. ViALUX modules are industrial build-to-order; **assume >8 week lead times
  and confirm in writing.**
- **Sources: LEDs, not lasers.** `docs/13` §4 shows ~1,000× light headroom (pupil-steered
  delivery needs ~14 lm of source), so spend it on the easier regulatory path — LEDs fall under
  **IEC 62471** rather than IEC 60825-1 laser classification. This also removed phase SLMs and
  pulsed lasers from the BOM, which **cuts export-control exposure** (`docs/16` §3.4).
- **HOE band — the single-source risk, the only real moat, and probably beyond the supplier.**
  Covestro **Bayfol HX** is a real mass-produced self-developing RGB photopolymer (HX105/120/200,
  recordable 440–680 nm, no wet processing) `[VERIFIED]`. **Ceres Holographics** is the only
  independent firm doing digital mastering plus roll-to-roll replication of large-format vHOEs on
  it `[VERIFIED]`. But the specification does not fit their demonstrated capability:

  | Our need | Ceres, demonstrated |
  |---|---|
  | ~6.6 m² band, angularly multiplexed | finished films **up to 1400 mm wide**; per-HOE automotive parts **up to 400 × 300 mm** |
  | bespoke one-off for a pre-revenue startup | **automotive OEM focus**, "almost unmovable design cycles" |
  | — | digital master printer maxes at **A2 (420 × 594 mm)** at 16 px/mm² |

  Replication machines cost "several million dollars each" (CEO Andy Travers). **Whether they
  will quote at all is `[UNVERIFIED]` and must be asked directly.** Named fallbacks for
  large-area vHOE: **De Montfort University** holography group, **University of Arizona Wyant
  College** (published Bayfol HX characterisation), **MIT Media Lab**, **TU Delft**, and
  commercially **Luminit LLC** (holographic diffusers) and **Wasatch Photonics** (volume
  gratings). Small quantities of raw film are resold by **Geola** (Lithuania). Order the long
  pole first.
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

1. **ViALUX / Digital Light Innovations volume pricing at qty 100.** The whole gross-margin
   thesis rests on it and nothing else in this file matters until it exists.
2. **Will Ceres quote a 6.6 m² angularly-multiplexed band at all?** Probably not as specified —
   see §3. If not, the named fallbacks are De Montfort University's holography group, University
   of Arizona's Wyant College, MIT Media Lab, TU Delft, Luminit LLC and Wasatch Photonics.
3. ECCN classification per optical line item (`docs/16` §3.4).
4. IEC 62471 risk-group determination for the chosen LED and optic (`docs/16` §4).
