# Branch A — Laser-Excited Volumetric Voxels

Corresponds to `hardware/optical-engine.md`'s north-star track. Not a hackathon-timeline experiment (`docs/roadmap.md`) — this protocol exists so the north-star track has a real starting experiment queued, not just a citation to JSID 2025.

## Research questions

1. How large can the voxel volume become within a 10cm-scale optical housing?
2. How fast can voxels be generated (voxels/s), and how does that scale against JSID 2025's ~10k voxels/s baseline?
3. How safe is the laser system at the pulse energies required for reliable air ionization? (See `hardware/optical-engine.md` §safety — this question cannot be answered experimentally before the eye-safety analysis exists on paper.)
4. How many voxels are actually required to represent a recognizable human feature (face, hand) at useful perceptual density — cross-references `experiments/perceptual-quality/README.md`.
5. Can *selectively* placed voxels (perceptual allocation, `docs/theory.md`) approximate a human better than uniformly-distributed voxels at the same total count?

## Protocol (experiments 1-4 from `experiments/README.md`, this branch's version)

1. Single stable point in air — measure achievable voxel size, position stability, brightness, and required laser/scan parameters at minimum viable pulse energy.
2. Simple 3D geometry (line, plane, cube) — measure spatial resolution and volume achieved at this housing scale.
3. Rotating object — measure angular consistency and any motion-induced artifacts (voxel "boiling," positional drift).
4. Fixed-position observer moved around the volume — since a physical voxel is inherently omnidirectional (unlike a light-field engine), this experiment instead measures whether apparent brightness/visibility holds up across viewing angles.

## Added research questions (Aug 2026 literature sweep, see `hardware/optical-engine.md`'s literature-update section)

6. **Does cumulative air-density depletion destabilize voxel position/brightness above ~10kHz repetition rate?** arXiv 2501.10198 measures that below ~10kHz, heat from each femtosecond filament fully diffuses before the next pulse; above ~10kHz, a permanent density-depletion well forms and every subsequent pulse ionizes already-perturbed air (measured: density stays depleted to ~92% between pulses at 100kHz). JSID 2025's ~10k voxels/s baseline sits right at this crossover — naively raising repetition rate to hit the north-star track's 10^5-10^6 points/s target may not scale linearly for this reason alone, independent of laser power or eye safety. Not yet tested experimentally in this project; flagged from the physics literature, not from a TAYF measurement.
7. **Watch-list scanning mechanism:** arXiv 2601.08906 (a Stanford "Re-Imaging Phased Array" SLM) demonstrates >10 million effective frames/second arbitrary 2D beam addressing — 2-3 orders of magnitude faster than any scanning mechanism considered so far. It is a neutral-atom-quantum-computing/microscopy tool, not a display device: demonstrated spot count is single-digit-to-tens (not millions), it has no depth/z mechanism, and the optical path is multi-meter with active piezo stabilization. Not usable as-is, but worth re-checking as the technology matures — a genuinely faster 2D addressing front-end paired with a separate depth mechanism (e.g. plasma ionization) is a real, if distant, hybrid option for Branch E.

## Literature check, second pass (Aug 2026): still no positive scaling result

A follow-up search (81 plasma/filament/voxel/trap-keyword candidates filtered from the OPTICS corpus, plus a full-corpus phrase sweep for filament-array/multi-beam/reduced-pressure/voxel-rate terms, plus targeted web search for 2026 H2 results outside arXiv) found **nothing that beats or approaches JSID 2025's ~10k voxels/s baseline.** Two new pieces of information, neither positive:

- **A second physical reason scaling is hard**, alongside question 6's air-density-depletion effect: patent-literature background confirms naive multi-spot parallelism (splitting one laser's energy across N simultaneous spots via CGH multiplexing) trades brightness for voxel count rather than multiplying effective throughput — spatial parallelism doesn't cheaply buy higher voxel budgets either.
- **One unverified, non-arXiv lead**: Tsai, Kumagai, Quan, Luo, Hayasaki, "Emission enhancement of femtosecond-laser-excited voxels using adaptive pulse shaping for volumetric display," *Applied Optics* 65, G69–G74 (2026) — reportedly 1.82× per-voxel brightness enhancement via genetic-algorithm-optimized pulse shaping. Same lab as the SIGGRAPH 2026 dual-path system already cited in `hardware/optical-engine.md`. Journal-only, not on arXiv — this project's arXiv-only corpus methodology structurally misses this group's other work, worth a manual check against the Applied Optics issue directly if this track becomes a real priority. It's a brightness fix, not a rate fix, and doesn't bear on the air-density-depletion caution either way.

A candidate 6th display mechanism surfaced incidentally (not laser-plasma, but adjacent): **photophoretic optical trap display** (Smalley et al., Nature 2018 — single mechanically-scanned particle, sub-10µm voxels, near-360° viewing), confirmed by a 2025 review (2512.09401) to have no new experimental result since 2018, with multi-particle scaling only aspirational (citing an undemonstrated 2016 proposal). Now listed in `hardware/optical-engine.md`'s ranked-mechanisms table as historical prior art, not a pursued candidate.

## Prerequisites before this branch can start

- Eye-safety analysis (`hardware/optical-engine.md` §safety) — not started, not optional, blocks any powered test near a person.
- Femtosecond laser + scanning optics hardware — not sourced (`hardware/bom.md` explicitly scopes this out of the hackathon BOM).

## Status

Not started. Documented here so the north-star track (`docs/roadmap.md`) has a concrete first experiment queued rather than remaining an abstract citation.
