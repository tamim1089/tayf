# Invention Disclosure — Draft

**Draft for attorney review, not a filing.** Source: `research/notes.md` §42. Four candidate inventive concepts, each a specific combination rather than the general "holographic telepresence" idea (see `patent/PATENT_NOTES.md` for why the general idea is unpatentable prior art).

## Concept A — Compact self-contained symmetric telepresence node

A device that, within a single ~10cm enclosure (`hardware/enclosure.md`), (1) captures a human, (2) generates a compact dynamic representation of them (`pipeline/schema.py`'s 215-float driving state, built on a persistent enrolled avatar per `pipeline/avatar/README.md`), (3) transmits the representation, (4) reconstructs the human at a remote, functionally identical node, and (5) produces a free-space (not screen-bound) optical representation of them — with both endpoints symmetric (`docs/architecture.md`). The specific combination of "single enclosure contains sensing+compute+network+optical output, and both endpoints are identical" is the candidate novelty, not any one subsystem alone.

## Concept B — Neural-gap-filled sparse optical engine

A miniature optical engine where a neural renderer (`pipeline/view_synthesis/README.md`) determines which angular/spatial optical information is actually required (`docs/theory.md`'s light-field formalism `L(x,y,z,θ,φ,t)`), physical optical channels generate only that selected subset, and neural view synthesis fills the remaining angular gaps — rather than a display attempting uniform physical coverage. The candidate novelty is coupling the *selection* of what to physically emit to a live perceptual/observer-position estimate (`docs/calibration.md`), not neural view synthesis alone (which has extensive prior art on its own).

## Concept C — Jointly optimized spatial-optical telepresence state

A telepresence node where the human representation, the local spatial coordinate system, the optical coordinate system, the current viewing direction, and the temporal state (`docs/calibration.md`) are jointly optimized as one system rather than treated as independent pipeline stages — e.g. the representation's fidelity allocation (`docs/theory.md`'s perceptual allocation) is driven by the current observer viewing angle, not fixed in advance.

## Concept D — Hybrid sparse-emission + compact-representation + neural-synthesis cooperation

A system where sparse optical emission, a compact learned human representation, and neural view synthesis cooperate specifically to produce a perceptually complete 3D remote person from less physical optical hardware than any one of the three alone would require — the claimed novelty being the cooperative/joint design (each component's design parameters chosen with the others in mind), not any single component.

## Status

These are research-direction sketches per `research/notes.md`, not claims. Actual claim scope, if any exists after a real prior-art search (`patent/prior-art.md`), must come from a patent attorney — see `patent/claim-map.md` for how these concepts might map onto the system architecture, and `patent/PATENT_NOTES.md` for the disclosure-timing constraint this file itself is subject to.
