# TAYF Digital Engineering Proof Package — Product Requirements Document (Frozen)

**Version:** 1.0 (frozen 2026-08-15). Changes require a delta record and re-run
of affected verification rows.
**Object:** the exact shipped thing is **two identical cubes**, each of which
(1) captures the local person, (2) transmits person-state (not pixels), and
(3) reconstructs the remote person as a **free-space wireframe figurine**
levitated by opposed 40 kHz phased ultrasonic arrays (MATD engine) inside a
10×10×10 cm³ optical workspace.

Requirement IDs: `PRD-xx`. Every row is falsifiable: pass criterion given, and
the test that decides it is named in `VV_MATRIX.md`.

---

## 1. System-level

| ID | Requirement | Pass criterion | Test method |
|---|---|---|---|
| PRD-01 | Output is free-space: no screen, wall, projector surface, or headset at either end. | Ray from particle to observer travels ≥ 95 % in air; no reflective surface in the H1 optical path. | Ray-trace of geometry (ART-01) + dimensional drawing audit |
| PRD-02 | Endpoints are symmetric: Cube A = Cube B (capture + display in one box). | Same hardware/software manifest both ends. | Architecture audit (ART-02) |
| PRD-03 | Transmission carries person-state, never pixels or mesh geometry. | Wire format == `DrivingState` (215 floats) per `pipeline/schema.py`; no image payload in data channel. | Code inspection + network model (NET-01) |
| PRD-04 | One-way latency p95 ≤ 150 ms end-to-end (ITU-T G.114). | Latency distribution model: p95 ≤ 150 ms under worst-case network class. | NET-02 |
| PRD-05 | Two-way telepresence session sustained ≥ 30 min without loss of trap. | Capacity experiment: no trap-loss in ≥ 99.9 % of simulated seconds at nominal point. | SIM-03 |

## 2. Display / physical

| ID | Requirement | Pass criterion | Test method |
|---|---|---|---|
| PRD-06 | Optical workspace 10×10×10 cm³. | All avatar path vertices inside workspace with ≥ 5 mm margin. | GEOM-01 |
| PRD-07 | Device envelope 100×100×250 mm (array axis), ± 10 %. | Dimensional drawing closure; array faces at 23.4 cm separation. | ART-03 (CAD-level drawing) |
| PRD-08 | Visual refresh 10 Hz minimum, 12.5 Hz target. | Simulated render rate ≥ 10 Hz for all 5 motion classes at p95 Monte Carlo; ≥ 20 % margin gate for outcome A. | SIM-01 (capacity experiment) |
| PRD-09 | Acceptable flicker: POV window 100 ms; each path loop ≤ 100 ms. | Per-loop draw time ≤ 100 ms in feasibility oracle. | SIM-01 |
| PRD-10 | Viewing: 360° azimuth visibility (by physics); illumination must support ≥ 180°. | ≥ 3 RGB illumination directions modeled; intensity coverage ≥ 180° azimuth. | ART-04 (illumination analysis) |
| PRD-11 | Recognizability: the wireframe must be identifiable as a human silhouette. | Silhouette IoU ≥ 0.6 vs template across all motion classes (perceptual proxy metric). | SIM-02 |
| PRD-12 | Trap safety: no loss of trap during nominal operation. | Loss-of-trap events = 0 at nominal point over ≥ 10⁴ simulated seconds; ≤ 1 per 10³ s at p95. | SIM-03 |
| PRD-13 | Minimum feature separation ≥ 4.3 mm (λ/2) — content is constrained by physics. | No path segment shorter than 0.9·λ/2 at corner vertices. | GEOM-02 |

## 3. Audio / haptics

| ID | Requirement | Pass criterion | Test method |
|---|---|---|---|
| PRD-14 | Localized audio from the display array (amplitude demodulation). | Feasibility: 25 % duty secondary modulation preserves ≥ 10 Hz visual refresh. | SIM-01 (audio-on mode) |
| PRD-15 | Haptics: stretch goal, not a gate. Secondary trap at user-specified point. | Not verified in this package; explicitly out of scope for the verdict. | — |

## 4. Capture / representation / transport

| ID | Requirement | Pass criterion | Test method |
|---|---|---|---|
| PRD-16 | Capture chain: cameras → pose/face/hand landmarks → `DrivingState` @ ≥ 30 fps capture rate. | Model: stage latencies sum within budget (see PRD-04). | NET-03 |
| PRD-17 | Bandwidth: total data-channel bit rate ≤ 0.2 Mbps at display rate (12.5 Hz). | Numeric proof including all protocol overheads; margin ≥ 2× under worst-case loss with retransmit. | NET-01 |
| PRD-18 | Late-frame policy: frames arriving after the render deadline are dropped, not queued. | State machine: deadline-based skip; maximum staleness ≤ 1 frame period. | NET-04, ART-05 |
| PRD-19 | Loss resilience: 0–10 % packet loss handled without freeze > 1 frame. | Network stress test: interpolation error bounded, no trap command gaps. | NET-05 |

## 5. Environment / safety

| ID | Requirement | Pass criterion | Test method |
|---|---|---|---|
| PRD-20 | Indoor still air, 20 °C, 1 atm; air disturbance ≤ 0.3 m/s steady bias. | Feasibility maintained at 0.3 m/s disturbance in worst-case test. | SIM-04 |
| PRD-21 | No laser emission of any class. | Engine contains no coherent source. | ART-06 (safety audit) |
| PRD-22 | Acoustic exposure: human-accessible SPL within IEC-recommended limits for continuous exposure. | Model SPL at 30 cm from array ≤ 100 dB(A) [ASSUMED limit — see CLAIM-41]; verified by measurement later. | ART-06 |
| PRD-23 | Bead containment: particle cannot escape the enclosure in normal operation. | Enclosure envelope + interlock in dimensional drawing. | ART-03 |

## 6. Non-goals (explicit)

| ID | Statement |
|---|---|
| PRD-NG1 | Photorealism, solid surfaces, texture, faces with detail — not in this product tier. |
| PRD-NG2 | Multi-particle rendering (mermaid/electrostatic POV) — research tier, no dependency. |
| PRD-NG3 | 80–100 kHz MUT arrays — unverified; not required at 40 kHz. |
| PRD-NG4 | Battery operation — tethered USB-PD only. |
| PRD-NG5 | Multi-observer adaptive tracking — single observer assumption only. |
| PRD-NG6 | High-fidelity hand/finger detail — hands collapse to wrist-level wireframe. |
| PRD-NG7 | Telepresence "personality" features (identity from enrollment) — recognizability = silhouette only (PRD-11). |

---

## 7. Environmental & content assumptions (must be stated, not hidden)

1. Content is the 14-joint / ~40-segment canonical avatar (frozen with this PRD).
2. Motion classes: standing, talking, head movement, waving, fast gesture —
   kinematics sourced from public mocap statistics (no capture hardware).
3. Observer is at ≥ 30 cm from the workspace; single observer.
4. Network path: residential-class broadband; QoD optional (best-effort assumed
   in the verdict; QoD modeled as bonus headroom only).
5. Gravity vector fixed (arrays vertical, workspace axis vertical).

## 8. Outcome gates (from `00_PLAN/PLAN.md`)

| Outcome | Condition |
|---|---|
| **A** | All 5 classes ≥ 10 Hz at ≥ 20 % refresh margin, Monte Carlo p95; PRD-04 p95 ≤ 150 ms; PRD-12 at nominal. |
| **B** | 0–20 % margin, or one class fails, or a named parameter unbounded; deliver unresolved-experiment list. |
| **C** | Any class < 10 Hz at nominal point → redesigned display brief (deliverable 09/redesign_brief.md). |
