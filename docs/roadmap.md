# TAYF Roadmap — Three Tracks

> ### ⚠ SUPERSEDED IN PART — read [`docs/10_TAYF_UNIVERSAL_ENGINEERING.md`](10_TAYF_UNIVERSAL_ENGINEERING.md) first
>
> This document predates the current design and is kept as a **detail source and historical record**, not as a specification. Where it disagrees with document 10, document 10 wins. Specifically superseded:
> - **The device is not a 10 cm cube.** It is a family of flat apertures (20 cm slab → A4 folio → 50 cm disc → chair → mirror), sized by the aperture law. Depth is dead weight; every form is a slab.
> - **The engine is static AIRR optics**, selected. Free-space plasma, acoustic and photophoretic routes were all evaluated and ruled out with quantitative reasons (doc 10 §9).
> - **The "~85% / ~15%" framing is retired.** It described a problem that no longer exists in that shape.
> - **Viewing angle is 170°**, measured (Yamamoto 2017, `10.11370/isj.56.341`) — not the ±20–30° stated in earlier revisions, which belongs to a different mechanism.
> - **Transport is delta + int8 at 0.104 Mbps**, measured — not fp16 + LZ4, whose assumed 0.6× ratio was tested and found to *expand* the payload.


Source: `FilesPlan.md` §3.2, §7; superseded on the north-star engine by `docs/08_FINAL_PRODUCT_PLAN.md` (2026-08-15).

## Why three tracks

The capture→representation→transport stack is solved (cited, working prior art, real measured numbers). Free-space photoreal optical emission at 10cm is not solved anywhere in the published literature — but free-space *wireframe* emission now is: the MATD (Multimodal Acoustic Trapping Display) is verified end-to-end (Nature 2019; SPIE 2020: 10×10×10 cm³ display volume; Sci Adv 2022 BEM; IEEE 2026 AcousTools, MIT) and becomes the product engine. Splitting tracks is the honest engineering move, not a downgrade.

## Track Hackathon-Prototype (buildable solo, Aug 14 → Sep 13)

Everything in `docs/architecture.md`'s pipeline, terminated in a compact light-field or retroreflective aerial-imaging panel instead of true free-space plasma (`hardware/optical-engine.md` §Hackathon-track). Goal: one working end-to-end cube-to-cube demo, a real body reconstructed from 215 numbers a second, over a real CAMARA QoD-guaranteed link, in well under 150ms.

- **Aug 14 → Aug 23:** finalize the pitch narrative, pick the hackathon-track optical engine, rerun the killed hardware/vendor research pass, submit Idea Capture Template + pitch deck.
- **Aug 23 → Sep 13:** build the pipeline for real, integrate the sourced optical panel, get one working demo with a live CAMARA QoD session.

## Track MATD-Product (the verified free-space engine, post-hackathon)

The actual product: two cubes exchanging the solved 215-float/frame vector stream, reconstructing the remote person as a glowing wireframe figurine levitated in a 10×10×10 cm³ workspace by opposed 40 kHz phased arrays — with localized audio and haptics from the same arrays. All claims verified (`docs/08` §3). Prototype ladder E0→E3, ~$250–400 in commodity parts to reach E1. Device envelope ~100×100×250 mm (arrays separated 23.4 cm); the 10 cm³ workspace survives.

## Track North-Star (multi-year, the research tier)

Photoreal emission — the E4 tier in `docs/08`: multi-particle POV displays (mermaid/electrostatic separation, StableLev/AAC-class trajectory repair) that do not exist yet in verified literature, or an optical engine that surpasses MATD's wireframe tier. This is a publishable/patentable research program. It does not appear on the hackathon timeline.

## Hard gates

- **Aug 23, 2026** — Idea Capture Template + pitch deck (GSMA MENA Ignite Hackathon, Idea Phase close).
- **Sep 13, 2026** — Prototype Phase / Live Demo.
- **Nov 2026** — MWC Doha showcase, contingent on advancing past the prototype phase.
- **Q4 2026** — E2 two-cube MATD loop (per `docs/08` §8 M-E4).
