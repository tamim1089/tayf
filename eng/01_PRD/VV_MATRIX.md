# Verification & Validation Matrix

Every PRD row maps to test(s). Each test maps to a runnable artifact in
`eng/08_VERIFY/`. A row is CLOSED only when the artifact exists, runs, and its
numeric output is recorded in `eng/09_DOSSIER/`.

Legend — method: U=unit, S=simulation, N=network model, A=analytic, I=inspection/audit.

| PRD | V&V id | Method | Test (artifact) | Pass criterion | Status |
|---|---|---|---|---|---|
| PRD-01 | VV-01 | A/I | ART-01 ray-audit of workspace geometry; no surface in beam path | ≥ 95 % air path | OPEN |
| PRD-02 | VV-02 | I | ART-02 manifest symmetry audit | identical manifest both ends | OPEN |
| PRD-03 | VV-03 | U/N | NET-01 wire-format check + bandwidth proof | payload == DrivingState; no pixels | OPEN |
| PRD-04 | VV-04 | N | NET-02 latency distribution model | p95 ≤ 150 ms worst-case | OPEN |
| PRD-05 | VV-05 | S | SIM-03 sustained-session stability sim | no trap loss ≥ 99.9 % sim-seconds | OPEN |
| PRD-06 | VV-06 | U/S | GEOM-01 workspace containment check | ≥ 5 mm margin all vertices | OPEN |
| PRD-07 | VV-07 | A/I | ART-03 dimensional drawing closure | 100×100×250 ± 10 %; 23.4 cm array gap | OPEN |
| PRD-08 | VV-08 | S | SIM-01 capacity experiment | ≥ 10 Hz all classes @ p95; ≥ 20 % margin | OPEN |
| PRD-09 | VV-09 | S | SIM-01 loop-time check | every loop ≤ 100 ms | OPEN |
| PRD-10 | VV-10 | A | ART-04 illumination coverage | ≥ 180° azimuth covered | OPEN |
| PRD-11 | VV-11 | S | SIM-02 silhouette IoU | ≥ 0.6 vs template | OPEN |
| PRD-12 | VV-12 | S | SIM-03 trap-loss counter | 0 @ nominal / ≤ 1e-3 s⁻¹ @ p95 | OPEN |
| PRD-13 | VV-13 | U | GEOM-02 feature-spacing check | no segment < 0.9·λ/2 | OPEN |
| PRD-14 | VV-14 | S | SIM-01 audio-on mode | ≥ 10 Hz preserved at 25 % duty | OPEN |
| PRD-16 | VV-16 | N | NET-03 capture-chain stage model | stage sums within budget | OPEN |
| PRD-17 | VV-17 | N | NET-01 bandwidth proof | ≤ 0.2 Mbps, ≥ 2× margin w/ retransmit | OPEN |
| PRD-18 | VV-18 | S/I | NET-04 + ART-05 deadline state machine | max staleness ≤ 1 frame | OPEN |
| PRD-19 | VV-19 | N/S | NET-05 loss stress | no command gap > 1 frame at 10 % loss | OPEN |
| PRD-20 | VV-20 | S | SIM-04 disturbance worst-case | feasible at 0.3 m/s | OPEN |
| PRD-21 | VV-21 | I | ART-06 safety audit: no coherent source | PASS | OPEN |
| PRD-22 | VV-22 | A/I | ART-06 SPL model at 30 cm | ≤ 100 dB(A) [ASSUMED limit] | OPEN |
| PRD-23 | VV-23 | A/I | ART-03 containment check | enclosure closes | OPEN |
| PRD-08/12 | VV-24 | S | VAL-01 validation ladder vs published data | within ± 10 % (accel), qualitative (6-bead) | OPEN |

**Traceability rule:** no test may reference a number that lacks a label in
`02_CLAIMS/CLAIM_LEDGER.md`. Violations block the phase.
