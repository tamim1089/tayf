# Prior Art — Seed List

**Not a completed search.** This is what's already surfaced incidentally during technical research (`research/deepseek_research.md`, `research/arxiv/online_findings.md`) — a real prior-art search for `patent/invention-disclosure.md` needs a professional pass, not just this list.

## Free-space/volumetric display prior art

- JSID 2025 fist-sized femtosecond laser-plasma display (68×42mm, ~10k voxels/s) — the closest existing art to `hardware/optical-engine.md`'s north-star track.
- Dual-path laser-excited volumetric display, SIGGRAPH 2026 / ETech 2024 (DOI 10.1145/3816042, 10.1145/3641517.3664387).
- Optica 2025 volumetric cloud display (laser-excited, scattering medium).
- Fairy Lights in Femtoseconds (arXiv 1506.06668, SIGGRAPH Asia 2015) — foundational femtosecond-laser aerial-graphics prior art.
- Acoustic levitation displays — MATD (Nature 2019).
- Photophoretic optical trap displays — Smalley et al. (Nature 2018).
- Voxon swept-volume displays (VX1/VX2/VX2-XL) — commercial product prior art.
- Looking Glass Factory, Sony ELF-SR2 — commercial light-field/glasses-free 3D display prior art.
- Wide-FOV dynamic metasurface-hybrid holographic projector, 159°×159° FOV (arXiv 2511.22639) — closest prior art to any future claim involving metasurface-extended SLM viewing angle.
- HoloTile RGB real-time speckle-free full-color CGH (arXiv 2409.11049) and Ellipsography joint phase-polarization speckle suppression (arXiv 2604.16237) — prior art against any future claim involving real-time or speckle-suppressed holographic display specifically.
- Video-rate holographic telepresence via single-shot wavefront measurement (arXiv 2601.00630) — closest prior art to any future claim combining holography with a telepresence/communication use case specifically.
- altiro3D open-source webcam-to-light-field-panel pipeline naming video conferencing as a use case (arXiv 2506.08064) — direct prior art against any future claim over the hackathon-track's capture→view-synthesis→panel pipeline concept; TAYF's differentiation there, if any, would need to be in the free-space/cube-integration angle, not the pipeline concept itself.
- **Aerial Imaging by Retro-Reflection (AIRR)** — Yamamoto, Tomiyama, Suyama et al., Utsunomiya University, "Floating aerial LED signage based on aerial imaging by retro-reflection," Optics Express 22(22):26919 (2014), plus a decade-plus follow-on line in OSA Continuum and Optical Review; commercialized as **ASKA3D**, with related patents on corner-cube-array retroreflector fabrication and floating-display devices held by Asukanet/related assignees. This is the closest real, commercialized prior art to `hardware/optical-engine.md`'s Branch C (aerial imaging) — direct prior art against any future claim over retroreflective/Fresnel-based aerial magnification specifically. Full-text figures not yet independently verified (see `experiments/aerial-imaging/README.md`) but the program's existence and patent coverage are confirmed.
- Gaussian Wave Splatting / Random-phase Wave Splatting (arXiv 2505.06582, 2508.17480, Stanford) — a closed-form Gaussian-splat-to-hologram transform for near-eye CGH. Closest prior art to Concept B/D (`patent/invention-disclosure.md`) if TAYF's optical-engine pipeline ever combines a Gaussian avatar representation directly with holographic rendering — this group has not applied it to human content or free-space output, but the transform itself is prior art for that combination regardless.

## Telepresence system prior art

- Proto Hologram, Holoconnects — commercial Pepper's-ghost-based "hologram" telepresence products, directly relevant to why "a hologram cube" (`patent/PATENT_NOTES.md`) is unpatentable as a general concept.
- Google Beam / Project Starline — light-field telepresence booths.
- Mon3tr (arXiv 2601.07518) — monocular 3D telepresence with pre-built Gaussian avatars; closest prior art to Concept A/D's representation+transmission coupling.
- Holoportation, VirtualCube, MetaStream, MagicStream, TeleAloha — comparison systems Mon3tr itself benchmarks against (per `research/deepseek_research.md`'s entry on it) — worth pulling that comparison table directly into a real search.

## Explicitly not yet searched

- Patent databases themselves (USPTO, EPO, WIPO) — everything above comes from academic/commercial-product research, not a patent-literature search. This is the biggest gap before `patent/invention-disclosure.md` can be evaluated seriously.
- Any existing patent specifically describing a small cube-shaped free-space-capture-and-display device — the online research pass tasked with checking this (project task #8) was killed before producing anything. This remains unresolved, not "checked and clear."

## Status

Seed list only. `patent/PATENT_NOTES.md`'s recommended process treats this as step 3 of 6 — currently incomplete.
