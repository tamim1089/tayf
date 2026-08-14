# TAYF Roadmap — Two Tracks

Source: `FilesPlan.md` §3.2, §7.

## Why two tracks

The capture→representation→transport stack is solved (cited, working prior art, real measured numbers). Free-space photoreal optical emission at 10cm is not solved anywhere in the published literature. Pretending otherwise produces a pitch that collapses under the first technical question a judge asks. Splitting it into two explicit tracks is the honest engineering move, not a downgrade.

## Track Hackathon-Prototype (buildable solo, Aug 14 → Sep 13)

Everything in `docs/architecture.md`'s pipeline, terminated in a compact light-field or retroreflective aerial-imaging panel instead of true free-space plasma (`hardware/optical-engine.md` §Hackathon-track). Goal: one working end-to-end cube-to-cube demo, a real body reconstructed from 215 numbers a second, over a real CAMARA QoD-guaranteed link, in well under 150ms.

- **Aug 14 → Aug 23:** finalize the two-track pitch narrative, pick the hackathon-track optical engine, rerun the killed hardware/vendor research pass, submit Idea Capture Template + pitch deck.
- **Aug 23 → Sep 13:** build the pipeline for real, integrate the sourced optical panel, get one working demo with a live CAMARA QoD session.

## Track North-Star (multi-year, the actual invention)

Laser-plasma or hybrid plasma-in-medium aerial display, scaled from the JSID 2025 baseline (~10k voxels/s, 68×42mm) toward the 10^5-10^6 points/s a recognizable moving face needs, with eye-safety engineering designed in from the start (pulse energy limits, exposure budgets, possibly gaze-tracked pulse gating) rather than retrofitted. This is a publishable/patentable research program. It does not appear on the hackathon timeline, and no laser hardware should be brought near a demo audience before a real eye-safety analysis exists (`hardware/optical-engine.md` §North-star-track / safety).

## Hard gates

- **Aug 23, 2026** — Idea Capture Template + pitch deck (GSMA MENA Ignite Hackathon, Idea Phase close).
- **Sep 13, 2026** — Prototype Phase / Live Demo.
- **Nov 2026** — MWC Doha showcase, contingent on advancing past the prototype phase.
