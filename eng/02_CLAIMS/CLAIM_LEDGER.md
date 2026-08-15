# Claim Ledger — every number, labeled

Discipline: **VERIFIED** = measured/confirmed in a primary source fetched by
this project. **DERIVED** = computed here or in the source from verified
inputs; formula/chain given. **ASSUMED** = engineering baseline chosen here;
must be swept or measured; promotion path stated. **UNKNOWN** = no basis;
risk driver. Nothing unlabeled may enter a later phase.

Source keys: N19 = Nature 575:320–323 (2019), DOI 10.1038/s41586-019-1739-5 ·
S20 = SPIE 10.1117/12.2569328 (2020) · F19 = APL 10.1063/1.5113467 (2019) ·
SA22 = Sci Adv 8(24):eabn7614 · PNAS25 = PNAS 122(50):e2516865122 ·
D01 = docs/01 · D03 = docs/03 · D08 = docs/08 · SCH = pipeline/schema.py ·
TR = pipeline/transport/README.md

## A. Display physics (engine)

| # | Claim | Value | Label | Chain / promotion |
|---|---|---|---|---|
| C-01 | Array format | 2 × 16×16, 10 mm pitch | **VERIFIED** N19/S20 | — |
| C-02 | Array separation | 23.4 cm | **VERIFIED** N19 | — |
| C-03 | Display control volume | 10×10×10 cm³ | **VERIFIED** S20 | — |
| C-04 | Drive frequency | 40 kHz | **VERIFIED** N19 | — |
| C-05 | Wavelength in air | 8.5 mm | **DERIVED** 343/40e3 = 8.575 mm | c verified standard |
| C-06 | Min trap separation | 4.25 mm (λ/2) | **DERIVED** | from C-05 |
| C-07 | Max vertical particle speed | 8.75 m/s | **VERIFIED** N19/S20 | — |
| C-08 | Max horizontal speed | 3.75 m/s | **VERIFIED** S20 | — |
| C-09 | Max acceleration | 141 m/s² (visual only) | **VERIFIED** S20 | — |
| C-10 | Corner speed cap | 0.75 m/s (visual only) | **VERIFIED** S20 | — |
| C-11 | Max image frame rate | 12.5 Hz (visual) / 10 Hz (+audio) | **VERIFIED** S20 | — |
| C-12 | POV integration window | 0.1 s | **VERIFIED** N19/S20 | — |
| C-13 | Color depth | 24 bpp RGB | **VERIFIED** S20 | — |
| C-14 | Phase update rate | ~17 kHz | **DERIVED** 40 kHz ÷ ~2.5 cycles; `CYCLES_PER_UPDATE` ASSUMED | promote: measure solver/FPGA loop |
| C-15 | Bead | 1 mm EPS (1 mm radius per S20 = 1 mm-r bead) | **VERIFIED** S20 (radius 1 mm) | D08 said 1 mm diameter — **correction: radius** |
| C-16 | Bead density (EPS) | 30 kg/m³ | **ASSUMED** range 10–60 | sweep MC; promote: datasheet |
| C-17 | Bead mass | 1.26e-7 kg @ C-16 | **DERIVED** 4/3πr³ρ | from C-15, C-16 |
| C-18 | Free-decay drag time constant | ~365 ms | **DERIVED** τ=m/6πηr | from C-17; kill risk resolved in Phase 4: spring-dominated response (ω_trap ≈ 375 rad/s ≫ 1/τ); near-undamped ring ζ≈0.016 → ring-limited operating accel (C-35) |
| C-19 | Six beads stably levitated (time-mux) | qualitative | **VERIFIED** N19 | multi-particle ceiling |
| C-20 | "50 particles / 5000 % voxel budget" | — | **FALSE** removed from matd_plan.md | PNAS25: no display claim |
| C-21 | Mermaid/electrostatic multi-particle POV | none demonstrated | **VERIFIED (absence)** PNAS25 | static assembly, fragile n≥6 |

## B. Dynamics / trap

| # | Claim | Value | Label | Chain / promotion |
|---|---|---|---|---|
| C-30 | Trap model | standing-wave node trap: all elements focus on the target, top array +π phase → pressure node (PNAS 2018 HAT; Nature 2019 MATD); display = lattice of node traps @ 1.4λ = 12 mm spacing | **VERIFIED** PNAS18/N19 + Phase 4 R0 | NOT the bare twin trap (planar null, 30× weak axially, cannot levitate — PNAS18/Nature Comms ncomms9661) |
| C-31 | Trap stiffness k | k_ax = 1.77e-2 N/m, k_lat = 9.66e-4 N/m (ratio 0.055) @ gain 1.235 | **DERIVED** Phase 4: Gor'kov field + step-pinned calibration k = m·141/1mm | k_lat/k_ax = 0.055 vs corner-implied ~1 → **UNKNOWN**, swept 0.05–1.0 |
| C-32 | Escape displacement Δp_esc | axial 2.14 mm (λ/4 node-to-barrier), lateral 6 mm (12 mm half-period) | **DERIVED** Phase 4 well geometry | old λ/8 = 1.07 mm was axial inflection only |
| C-33 | "3.75 m/s × 0.1 s = 37.5 cm usable path" | 37.5 cm | **ASSUMED → contested** | capacity experiment replaces; corners/accel bound it |
| C-34 | Corner traversal feasible at 0.75 m/s | — | **VERIFIED** S20 | timing must respect C-10; Phase 4: model tracks 0.75 at 43 mm radius (k_lat ratio 0.055); published ~4 mm needs k_lat ≈ k_ax — UNKNOWN gap |
| C-35 | Ring-limited operating acceleration | a_op = 0.9·k·ESC/(2m): lateral 20.7, vertical ≥100 m/s² | **DERIVED** Phase 4 R3–R5 | near-undamped bead (ζ≈0.016) rings to ~2× static lag after accel changes |
| C-36 | Sustained-speed ceilings (ring-limited) | vertical ≥ 30 m/s, horizontal 6.7 m/s (drag limits 110 / 16.9) | **DERIVED** Phase 4 R3/R4 | C-07 8.75 and C-08 3.75 reproduced with headroom |

## C. Pipeline / transport

| # | Claim | Value | Label | Chain / promotion |
|---|---|---|---|---|
| C-40 | DrivingState dims | 75+50+90 = 215 floats | **VERIFIED** SCH (code) | — |
| C-41 | Raw frame size | 868 B | **DERIVED** 215·4+8 | from C-40, struct fmt |
| C-42 | fp32 @ 60 fps | 0.413 Mbps | **DERIVED** | 868·8·60 |
| C-43 | fp16 @ 60 fps | 0.206 Mbps | **DERIVED** | 434·8·60 |
| C-44 | fp16+LZ4 wire rate | ≈ 0.16 Mbps | **ASSUMED** D03/TR — unmeasured | Phase 6 derives from real byte streams |
| C-45 | < 0.2 Mbps sustained | target | **UNVALIDATED** TR states so | Phase 6 numeric proof |
| C-46 | End-to-end latency 76–177 ms | range | **DERIVED** D01 §6 stage table | upper end violates H4; distribution UNKNOWN |
| C-47 | Mon3tr reference | ~80 ms / < 0.2 Mbps | **VERIFIED** D01/D03 cite arXiv 2601.07518 | on PC-class hardware, not ours |
| C-48 | Stage budgets (capture 8–16, pose 20–30, enc 2–5, net 20–60, dec 2–5, anim 8–15, track 5–10, synth 10–20, emit 1–16) | ms | **ASSUMED** D01 §6 | unvalidated on Jetson; Phase 6 models |
| C-49 | Display-rate downselect bitrate | ≈ 43 kbps fp16 @ 12.5 Hz | **DERIVED** | from C-43 × 12.5/60; Phase 6 confirms |
| C-50 | Refresh period vs H4 | 80–100 ms period vs 150 ms budget | **DERIVED** | jitter buffer ≤ 1 frame (Phase 6/7) |

## D. Environment / safety / power

| # | Claim | Value | Label | Chain / promotion |
|---|---|---|---|---|
| C-60 | Air disturbance | ≤ 0.3 m/s | **ASSUMED** indoor spec | promote: measurement |
| C-61 | Transducer drive power | 0.03–0.1 W/ch | **ASSUMED ESTIMATE** | promote: bench measurement |
| C-62 | Array electrical envelope | 15–50 W (512 ch) | **DERIVED ESTIMATE** from C-61 | mark ESTIMATE in dossier |
| C-63 | SPL at 30 cm | ≤ 100 dB(A) | **ASSUMED** exposure limit | promote: measurement; IEC doc in dossier |
| C-64 | No laser | — | **VERIFIED** design constraint D08 | — |

## E. Verdict-relevant derived quantities (Phase 3/4 outputs, will fill)

| # | Claim | Status |
|---|---|---|
| C-70 | Trap stiffness k_ax, k_lat from Gor'kov + field | **UNKNOWN → DERIVED in Phase 3** |
| C-71 | Trap depth / escape energy | **UNKNOWN → DERIVED in Phase 3** |
| C-72 | Follow-error at 10–12.5 Hz loop | **UNKNOWN → SIM-01 output** |
| C-73 | Effective drawable path capacity per class | **UNKNOWN → SIM-01 output** |

## F. Corrections issued by this ledger

- C-15: D08 "1 mm diameter" → S20 states 1 mm-radius bead. Ledger defers to S20.
- C-20/21: matd_plan.md corrected 2026-08-15 (fabricated voxel-budget claim removed).
- C-33: the 37.5 cm usable-path figure is ASSUMED and contested; SIM-01 decides.
- C-46: D01's own note "upper end violates H4" is honored; PRD-04 tests p95.
