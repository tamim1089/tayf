# Optical Engine — Two-Track Spec

Source: `FilesPlan.md` §3, `research/arxiv/online_findings.md`. This is the single most consequential hardware decision in the project — nothing else in the display stage can proceed until the hackathon-track choice below is made.

## The physics constraint (why this is hard)

Free space has no scattering medium. Making a volume of ordinary air emit or redirect light without a physical surface requires one of: emitting light directly from points in the volume (plasma, particles, an emissive medium), or redirecting light so a viewer's eyes reconstruct depth (a coherent wavefront/SLM, angular multiplexing, a light-field panel). There is no way to make air glow directly from a phone-driven display. This rules out the literal "the phone blows the 3D shape into the air" framing as a plug-and-play mechanism and narrows the real design space to the five mechanisms below.

## Ranked mechanisms

| Mechanism | Cube-scale evidence | Fidelity ceiling | Verdict |
|---|---|---|---|
| Laser-plasma ionization (aerial voxels) | JSID 2025: 68×42mm, ~10k voxels/s. Dual-path scaling exists (SIGGRAPH 2026, DOI 10.1145/3816042) | Sparse/wireframe, not photoreal | North-star track |
| Acoustic levitation / ultrasonic particle display | MATD (Nature 2019) — room-scale, single/few particles, very low refresh | Cannot render a moving human at any published scale | Ruled out |
| Volumetric cloud/medium display | Optica 2025 — denser than air-plasma, but current form factor far exceeds 10cm; medium maintenance inside a sealed cube is unsolved | Better voxel density, unproven at this scale | Not the prototype |
| Holographic SLM / CGH | Real, mature field. Multiplane CGH (arXiv 2205.07030): 57s/frame on RTX 3070 non-real-time; narrow viewing angle (a few degrees at useful resolution, arXiv 2203.06784) | Coherent speckle, narrow angle, not real-time yet | Not the prototype |
| **Light-field / retroreflective panel** (Looking Glass-class, AIP) | Commercial products exist today | Not free space — bound to a physical panel — but real depth cues, works today | **Hackathon track** |

## Hackathon track (buildable now)

Compact light-field or retroreflective aerial-imaging panel, driven by the renderer in `pipeline/transport/README.md`'s receiver stage. Not literal free space; presented on stage honestly as the buildable interim output stage while the display track described below is the acknowledged open R&D item. Vendor/part selection is an open item — first task for the rerun of `hardware/bom.md`'s research pass.

## The engine must stay pluggable

Per `research/notes.md` §10: do not lock the invention to one optical mechanism. `pipeline/`'s renderer targets an abstract optical-engine interface (input: `L(x,y,z,θ,φ,t)` samples per `docs/theory.md`; output: whatever the physical engine needs — panel frames, scan-pattern commands, hologram phase maps), so swapping the hackathon-track panel for a different candidate, or eventually swapping in a north-star engine, does not require touching `pipeline/avatar/` or `pipeline/capture/`.

```mermaid
flowchart TB
    X["Compact Free-Space Optical Engine\n(abstract interface)"]
    X --> A["Laser Volumetric Engine\n(voxel-display/)"]
    X --> B["Light-Field Engine\n(light-field/)"]
    X --> C["Holographic SLM Engine"]
    X --> D["Aerial Imaging Engine\n(aerial-imaging/)"]
    X --> E["Hybrid Optical Engine"]
```

## Research variables per candidate (what each branch actually measures — see `experiments/`)

- **Laser-plasma (Branch A):** voxel size, voxel density, drawing volume, laser energy, scan speed, repetition rate, axial resolution, lateral resolution, safety margin, optical efficiency, temporal stability. Protocol: `experiments/voxel-display/README.md`.
- **Directional light-field / holographic (Branch B):** number of views needed for convincing 3D, achievable emitter compactness, neural-interpolation compatibility for missing angles. Protocol: `experiments/light-field/README.md`, `pipeline/view_synthesis/README.md`.
- **360° directional light field:** a light-field variant using multiple compact optical channels (candidate: 8+ views) combined with neural interpolation between physical channels — same underlying research question as Branch B at a wider angular target. Not separately branched in `experiments/`; treated as a light-field configuration, not a distinct mechanism.
- **Aerial imaging (Branch C):** achievable magnification vs. brightness/resolution tradeoff for transforming a small source into a larger apparent volume (Fresnel optics, catadioptric systems, retroreflective corner-cube arrays). Protocol: `experiments/aerial-imaging/README.md`.
- **Holographic SLM (Branch D):** achievable field of view, required hologram resolution, required laser power, whether the optical path fits inside 10cm at all. Not separately branched in `experiments/` yet — folded into north-star track pending resource priority after Branch A/B.
- **Hybrid (Branch E):** combinations such as light-field + aerial optics + neural rendering, or laser voxels + directional light field, or holographic SLM + aerial imaging. Explicitly not attempted before the individual branches produce real measurements — combining unmeasured mechanisms compounds unknowns rather than resolving them.

## North-star track (not a hackathon deliverable)

Laser-plasma or hybrid plasma-in-medium aerial display, scaled from the JSID 2025 baseline toward 10^5-10^6 points/s. This is a multi-year program, not a four-week one — see `docs/roadmap.md`.

### Laser eye safety — not started, not optional

Femtosecond laser-plasma ionization is a Class 4 laser hazard by nature of the mechanism (it has to be intense enough to ionize air at focus). A device meant to sit near a person's face has no margin for skipping this. Before any north-star optical hardware is powered on near a person:

1. Full exposure/pulse-energy analysis against applicable laser safety limits (not yet started).
2. Engineering controls to consider: physical exclusion zone around the focal volume, gaze/proximity-triggered pulse gating, interlocks.
3. This section stays a placeholder — not a checklist to skip — until real analysis exists. No demo, however informal, proceeds without it.
