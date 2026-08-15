# Digital Engineering Proof Package — Status Board

**Mission:** answer, with numeric evidence and no hand-waving:
> Can a single MATD particle, under experimentally grounded constraints, render
> our chosen miniature human wireframe continuously enough for a two-way
> telepresence call?

**Verdict protocol (locked):**
- **A** — all 5 motion classes sustain ≥ 10 Hz with ≥ 20 % refresh margin at
  Monte Carlo p95, and one-way latency p95 ≤ 150 ms.
- **B** — 0–20 % margin, or one class fails, or a named parameter cannot be
  bounded; unresolved-experiment list is the deliverable.
- **C** — any class below 10 Hz at nominal point → redesigned display brief.

**Frozen choices (2026-08-15):** analytic Rayleigh–Sommerfeld field with
standing-wave **node-trap** phase law (all elements focus on the target,
top array +π → pressure node; lattice at 1.4λ = 12 mm spacing — PNAS 2018 /
Nature 2019; the bare twin-trap law was ruled out in Phase 4: planar null,
30× weak axially, cannot levitate); k-Wave 2D spot-checks only (credibility).
Canonical avatar: 14 joints / ~40 segments. Latency metric: p95 ≤ 150 ms.

| Phase | Deliverable | Status |
|---|---|---|
| 0 | Skeleton, deps, constants.py | DONE |
| 1 | PRD freeze + V&V matrix | DONE |
| 2 | Claim ledger | DONE |
| 3 | Physics model notes | DONE |
| 4 | Simulator + validation ladder | DONE (8/8 rungs green) |
| 5 | Avatar + capacity experiment | PENDING |
| 6 | Network/capture model | PENDING |
| 7 | Architecture + FPGA datapath | PENDING |
| 8 | Verification suite | PENDING |
| 9 | Failure analysis + risk register | PENDING |
| 10 | Verdict + PDF dossier | PENDING |

**Master rule:** no number enters a later phase without a label
(VERIFIED / DERIVED / ASSUMED / UNKNOWN) traceable to `02_CLAIMS/CLAIM_LEDGER.md`.
