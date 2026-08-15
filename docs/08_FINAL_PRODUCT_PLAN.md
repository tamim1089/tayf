# 08 — Final Product Plan: TAYF with a Verified MATD Engine

**Reference date: 2026-08-15.** Supersedes the unresolved-engine framing of `docs/06` §1–§3 for the *emission* stage: the free-space engine is now a selected, verified technology (Track 5, MATD), not an open research question. What remains research is fidelity tier, not viability.

---

## 1. The decision, in one paragraph

TAYF ships as **two identical cubes exchanging a person-state vector stream (solved, ~215 floats/frame, 0.12–0.21 Mbps) and reconstructing the remote person as a free-space, true-3D wireframe figurine levitated inside a 10 × 10 × 10 cm³ workspace by opposed phased ultrasonic arrays** — the Multimodal Acoustic Trapping Display (MATD), whose display volume is *exactly* the 10 cm³ workspace this project has always specified. Every load-bearing claim in this decision is verified against primary sources (see §3). The fidelity tier is **wireframe figurine** (verified, buildable today); **photoreal full-body** is explicitly deferred to a research tier (§9) because no verified multi-particle POV display exists. The hackathon track (light-field panel) is unchanged and unblocked — MATD is the product engine, not the demo instrument.

**This kills the old cold start.** `docs/06` §1's critical path was `perceptual requirement → SBP → modulator → power → thermal → enclosure` — a chain whose only exit was a screen, because no verified free-space emitter existed. MATD short-circuits it: the engine is verified, low-power, eye-safe by construction (no laser), and its workspace is already the target size.

---

## 2. Why MATD won the engine selection (Track 5 vs. Tracks C1–C4)

| Engine | Status | Verdict |
|---|---|---|
| Laser-plasma voxel (`docs/02` §11.5) | 15× gap vs. requirement; two known-adverse scaling mechanisms (air depletion >10 kHz, brightness-vs-count) | **Killed on power.** Also eye-safety program required. |
| AIRR / aerial imaging | Unit magnification bound; journal-gated literature; not free space in the required sense | **Killed on magnification.** |
| 4f / CGH layout | f = 680 mm focal-length arithmetic; étendue-expander needed for broadcast | **Killed on focal length** (correct per `docs/02` §5 note). |
| Light-field panel (hackathon track) | Commercial, verified | **Instrument, not product.** Bound to a physical panel — violates H1. |
| **Track 5 — MATD (acoustic trapping)** | **Verified end-to-end: Nature 2019 + SPIE 2020 + Sci Adv 2022 + IEEE 2026 software** | **SELECTED.** |

MATD satisfies H1 (light scatters off a particle in free space — no screen, no wall, no headset), H2 (capture cube = display cube), H3 (input is state/vector stream, not pixels), H4 (POV display at 10–12.5 Hz; pipeline unchanged). It adds audio + localized haptics for free (§3.4) — no other engine candidate even attempts that.

**Spec change (honest, per `docs/01` A1's purpose):** the *workspace* stays 10³ cm³ (the MATD's demonstrated control volume), but the *device envelope* grows on the array axis: two opposed 16 × 16 arrays with ~23.4 cm separation ⇒ device ≈ 100 × 100 × 250 mm. This is `docs/06` §4's V2-class form factor — same philosophy as "the idea is not invalidated by the box being 150 mm." A1 is revised in §10.

---

## 3. Verified engineering facts (primary sources, fetched 2026-08-15)

| # | Fact | Source | Status |
|---|---|---|---|
| F1 | Two opposed 16 × 16 (256 each) 40 kHz phased arrays levitate a ~1 mm EPS bead; speeds 8.75 m/s vertical, 3.75 m/s horizontal; accelerations to 141 m/s²; corner speed ≤ 0.75 m/s | Nature 575:320–323, 10.1038/s41586-019-1739-5; SPIE 10.1117/12.2569328 | **Verified** |
| F2 | Display update volume is **10 × 10 × 10 cm³**; frame rate 12.5 Hz (visual) / 10 Hz (visual+audio); RGB color 24 bpp; 0.1 s POV window | SPIE 2020 (10.1117/12.2569328) | **Verified** |
| F3 | Wavelength 8.5 mm ⇒ minimum trap separation 4.25 mm (λ/2); phase updates capped near ~17k/s (40 kHz ÷ stabilization cycles) | Nature 2019; `matd_plan.md` verified pass | **Verified** |
| F4 | Time-multiplexed secondary trap (75/25 duty) delivers localized **tactile** feedback; amplitude demodulation delivers **audible sound** from the same array | Nature 2019 | **Verified** |
| F5 | Six beads stably levitated by time-multiplexed traps (liquid transfer demo) — the verified multi-particle ceiling | Nature 2019 | **Verified** |
| F6 | Hands do NOT crash the trap (finger-click gesture demo in the original system) | Nature 2019 | **Verified** (contradicts earlier draft claims) |
| F7 | Real-time BEM scattering (E = F + GH, H precomputed, GPU F/G) at >10,000 updates/s, 256 transducers, 3,000–6,000 mesh elements — volumetric POV images with **static** scattering objects | Sci Adv 8(24):eabn7614, 10.1126/sciadv.abn7614 | **Verified** (static only; moving-hand = future work) |
| F8 | Electrostatic "mermaid potential" separates levitated particles (silver-coated 250–300 µm spheres, 51 kHz, 3.4 mm gap) — but: **static self-assembly only; expanded states fragile n≥6; no POV display** | PNAS 122(50):e2516865122, 10.1073/pnas.2516865122 | **Verified, NOT a display** |
| F9 | Low-cost build reference: 60 transducers (2 × 30), 1.5 mm EPS bead, 4×5×8 cm³ volume, 10 fps, FPGA (ALTERA CoreEp4CE6, π/64 phase, 1.5 Mbaud UART) | Fushimi et al., APL 115(6):064101, 10.1063/1.5113467 | **Verified** |
| F10 | 512-channel modular FPGA system (40 kHz, 2 mm particles): 225 cm² control area (15 × 15 cm), 14.2 cm Z-height, 2.1 mm step — exceeds the 10 cm³ workspace at 40 kHz, ≈ 1M KRW (~$750) | IEIE journal 2025 (auric.kr RD_R/454644) | **Verified** |
| F11 | OptiTrap trajectory optimization renders shapes up to 563% larger / 150% faster, corner-aware, feasibility ≥9/10 attempts | ACM TOG 41(5), 10.1145/3517746 | **Verified** |
| F12 | AcousTools: MIT-licensed, PyTorch/GPU, Setup→Propagators→Solvers→Analysis→Hardware, drives OpenMPD 16 × 16 arrays | arXiv:2511.07336; IEEE T-UFFC 73(2):99–111, 10.1109/TUSON.2026.3659798 | **Verified, MIT, usable** |
| F13 | Transport is solved in-house: Mon3tr-class 215 floats/frame, <0.2 Mbps, ~80 ms end-to-end; TAYF stack measured 0.12–0.21 Mbps | `docs/03`, arXiv 2601.07518 | **Verified (own work)** |
| F14 | MATD control data (x, y, z, R, G, B per voxel) is a vector stream — matches H3 and the existing pipeline schema byte-for-byte in spirit | Nature 2019; SPIE 2020 | **Verified** |

---

## 4. Product architecture (unchanged from `docs/architecture.md`, emission stage swapped)

```
Cube A (sender)                           Cube B (receiver = MATD)
┌─────────────────────────┐               ┌─────────────────────────────┐
│ 3–4× global-shutter cams │  WebRTC      │ FPGA: twin-trap phase solver │
│ → pose/face/hand 215 floats│  state ch.  │  17k updates/s, 2×256 ch     │
│ → H3 vector frame         │──0.12–0.21──▶│ → two opposed 16×16 arrays   │
│ (solved: docs/03, pipeline/)│  Mbps       │ → 1 mm bead scans 10³ cm³    │
└─────────────────────────┘               │ RGB LED illumination (24 bpp) │
   capture+enrollment offloaded           │ secondary trap: audio+haptics │
                                          └─────────────────────────────┘
```

- **No display pixels on the wire.** The 215-float frame drives the figurine's skeleton→wireframe mapping locally (H3's "state, not pixels" holds at both ends).
- **Capture side is unchanged and shipping** (`docs/03`; avatar license decision M-A1 is the only blocker).
- **Latency:** pipeline 76–177 ms (`docs/01` §9) already meets H4's 150 ms one-way; the MATD adds no network latency — only its 10–12.5 Hz POV refresh, which is a rendering property, not a transport cost.

---

## 5. The one math that matters: can a wireframe figurine fit the POV budget?

POV path budget (verified numbers, conservative horizontal case):

- Per frame window t = 0.1 s at v_max = 3.75 m/s ⇒ **37.5 cm of line per frame** (vertical axis gives 87.5 cm; corners capped at 0.75 m/s ⇒ design to OptiTrap-style timing).
- A 7–8 cm figurine (head + shoulders + torso + arms, low-poly line-art, ~60–100 points): wireframe total length ≈ **25–45 cm** ⇒ fits 10–12.5 Hz with margin **when trajectories are OptiTrap-optimized** (F11) rather than naive constant-speed tracing.
- Working rule for content: line budget ≤ 30 cm/frame at 10 Hz, ≤ 25 cm at 12.5 Hz; express as a **character-budget constraint in the renderer** (the same role Ψ plays for the optical chain — `pipeline/` gets a `voxel_budget` parameter, defaulting to these numbers, measured on the real rig).
- Multi-particle does NOT rescue the photoreal tier today (F8: fragile n≥6, static only; F5: 6 beads ceiling in verified literature). **Photoreal = research tier**, gated on future multi-bead POV results (StableLev CHI'24, AAC CHI'26 remain the only real progress and they fight instability, not solve it).

---

## 6. MATD prototype ladder (replaces `docs/06` §4's emission rungs for Track 5)

| Stage | Build | Proves | Go/no-go |
|---|---|---|---|
| **E0** | 72-transducer TinyLev-class levitator (~$90 kit or $30 of MA40S4S), static single bead | We can levitate and hold a 1 mm bead stably in air; basic trap math reproduced (AcousTools solvers) | Bead held >60 s at 5 mm position error |
| **E1** | 2 × 30–60 channel FPGA-driven arrays (F9 reference), twin-trap phase control, RGB LED, 10³ cm³ workspace | Single-bead POV: a point → line → 2D shapes → 3D cube/torus at ≥10 Hz, colored | Stable free-space 3D object with no display surface (matches old V0 gate) |
| **E2** | Two-cube integration: existing pipeline (F13) → E1 display, both directions | Full H1–H4 product loop with a live person as a wireframe figurine | Two-way session, <150 ms, recognizable silhouette, ≤30 cm/frame line budget |
| **E3** | Production engineering: 512-ch FPGA (F10), BEM static-scattering tolerance (F7), enclosure, thermal measurement, audio+haptics modes (F4) | Ship-grade device; 30-min sustained calls | All of E2 sustained; thermal closed; spec A1 revised value |
| **E4 (research tier)** | Multi-particle mermaid/electrostatic POV (F8 → unproven display application), AAC/StableLev-style trajectory repair | Photoreal or high-detail tier | No earlier stage depends on it |

`docs/06` V0/V1 gates transfer: **E2 = the Sep 13-class milestone for the product engine** (parallel to, not replacing, the hackathon panel demo).

---

## 7. Bill of materials outline (verified suppliers/components, prices where published)

| Item | Choice | Reference | Est. cost |
|---|---|---|---|
| Transducers (40 kHz, 10 mm) | Murata MA40S4S or Aexit/Manorshi equivalents | F9 (Fushimi rig), TinyLev heritage | ~$0.3–1 each; 512 ≈ $150–500 |
| Driver | FPGA board, ≥60–512 channels, π/64 phase resolution, 1.5 Mbaud+ link | F9 (ALTERA CoreEp4CE6), F10 (modular master-slave FPGA) | $50–750 |
| Software stack | AcousTools (MIT) for Setup/Propagators/Solvers/Analysis; OpenMPD board drivers for 16×16 arrays | F12 | $0 |
| Particle | 1 mm EPS bead (display), 1.5 mm EPS (F9 reference); spares pack | F1, F9 | ~$10 |
| Illumination | RGB LED array; ≥1 per face for 360° visibility (SPIE: single side-LED limits viewing) | F1 (SPIE §illumination) | $20–60 |
| Compute | Jetson-class edge (existing decision, `docs/04`) | `docs/04`, M-A5 | existing |
| Enclosure | 100 × 100 × 250 mm (array axis), open optical path, bead-access door | A1 revision (§10) | — |

Hobbyist tier today (~$250–400 total): TinyLev kit + F9 electronics + existing compute — validates E0/E1 before any custom PCB.

---

## 8. Milestones (new Track E, integrated with `docs/06` §5 tracks)

- **M-E1** E0 levitation achieved, AcousTools solver validated on our array layout *(depends: none — parts are commodity)*
- **M-E2** E1 single-bead POV display: point→line→plane→cube ladder in the 10³ workspace *(depends: M-E1)*
- **M-E3** Phase solver ported to FPGA at ≥10 kHz update rate (F9 reference: 60 ch; target 256+ per array) *(depends: M-E1)*
- **M-E4** E2 two-cube loop: pipeline (M-A3, M-N4) → MATD *(depends: M-E2, M-A3, M-N4)*
- **M-E5** Audio + haptic modes verified on the real rig (F4: 75/25 time-multiplexing, amplitude demodulation) *(depends: M-E2)*
- **M-E6** BEM static-scattering tolerance (F7) integrated; enclosure + thermal measured, A1 revision committed *(depends: M-E4)*
- **M-E7** E3 production freeze; E4 research tier scoped separately *(depends: M-E6)*

**Do not start before gate:** E0 is safe, but no FPGA channel count above 60 should be committed to a PCB until E1 proves the POV path on bench electronics — the verified trap math is the risk-free part; the bead-dynamics-vs-content match is the unknown that E1 measures.

---

## 9. Honest limits and residual risks

1. **Photoreal tier is not assured.** The "50 particles / 5000% voxel budget" claim was removed as fabricated (`matd_plan.md` corrected 2026-08-15). Verified multi-particle research is static-assembly (PNAS) or stability-challenged displays (StableLev, AAC). E4 is a research program, not a roadmap promise.
2. **Enclosure grows to ~250 mm on the array axis** (23.4 cm array separation). The 10 cm³ *workspace* survives; the device does not. A1 revised; `docs/06` F2's logic ("form factor wrong ≠ idea wrong") applies verbatim.
3. **Air currents and dust** move the bead; MATD-class systems are sensitive (F9 documents distortion with speed). E2 must include the environmental-fragility protocol (`experiments/`).
4. **Thermal is unmeasured for 256–512 channels.** Low per-channel drive (~0.03–0.1 W) suggests a 10–40 W envelope, but this is a measured quantity, not a claim — E3 measures it; `docs/01` §5's enclosure math governs the passive cooling design.
5. **Licensing (actions, all cheap):** MATD demo code is CC-BY-NC-SA ⇒ reimplement from the published math (the physics is not encumbered; the code is). AcousTools is MIT (usable). PNAS paper is CC-BY-NC-ND (read-only reference). **Patent FTO: WO2023227890A1** (UCL, MATD trap-control) is already in `docs/05` prior-art table — listed **ceased at WO stage, national status unconfirmed**: confirm national phase status before E2 hardware freeze. Optical prior-art set (`docs/05`) is unaffected; Track 5 adds an acoustic-holography claim class to the claim map.
6. **H4's 150 ms budget** is unchanged but the display refresh is 10–12.5 Hz: verify conversational acceptability of figurine-rate motion in the S5 perceptual battery (a new S5.8 item).

---

## 10. Spec changes (single table)

| Parameter | Old | New | Why |
|---|---|---|---|
| A1 (enclosure edge) | 100 mm | **250 mm on array axis, 100 mm on others** | MATD geometry: opposed arrays, 23.4 cm separation |
| Workspace (display volume) | implied ≤100³ | **10 × 10 × 10 cm³ — now a verified engine spec** | F2 (SPIE 2020) |
| Emission mechanism | unselected (Tracks C1–C4) | **Track 5 MATD, verified** | §2, §3 |
| Fidelity tier (north-star) | photoreal (unstated mechanism) | **wireframe figurine shipped; photoreal = research tier E4** | F8 reality |
| Optical gap headline (`docs/02` §4.4) | 1.3–1.7× broadcast | **N/A for Track 5** (no SBP chain; vector stream → trap positions) | engine replacement |

---

## 11. Immediate next actions

1. **Order E0 parts** (TinyLev kit or 72 × MA40S4S + bench driver, ~$100) — no gating research question remains.
2. **Close M-A1 (avatar license) and M-N1 (Nokia portal)** — still the only blockers for the hackathon track and for E2's pipeline side.
3. **Confirm WO2023227890A1 national-phase status** (patent action, `docs/05` §3.4#18).
4. **Add S5.8** (figurine-rate acceptability) and the E-track items to `simulation/` + `experiments/` READMEs.
5. **Update `pipeline/` schema** with the `voxel_budget` parameter (default ≤30 cm/frame @ 10 Hz) and a wireframe-of-the-215-float-avatar export mode for E1/E2.
6. **Pitch refresh:** the two-track story becomes a three-tier story — hackathon panel demo (Aug 23/Sep 13), verified MATD product engine (E2 by Q4), photoreal research tier (E4). The "solved engine" claim is now defensible under questioning because every number in §3 traces to a fetched primary source.

*Companion documents: `matd_plan.md` (corrected 2026-08-15), `docs/01` (spec; A1 revision above), `docs/02` (Track 5 decision vs. C1–C4), `docs/03` (capture/transport, unchanged), `docs/05` (patent table incl. WO2023227890A1), `docs/06` (build plan; E-track adds), `docs/07` (simulation tracks).*
