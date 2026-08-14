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
| Holographic SLM / CGH | Real, mature field. **Updated Aug 2026 (see §"Literature update" below): angle, speed, and speckle each now have independent real point-solutions** — 159°×159° dynamic FOV (2511.22639), 60Hz full-color speckle-free video (2409.11049), 30dB speckle suppression (2604.16237) | No paper combines angle+speed+speckle; none evaluated at 10cm-cube scale, power/safety budget, or on a moving photoreal human face rather than test patterns | Individually de-risked sub-problems; the combined, human-face, cube-scale system remains unbuilt |
| **Light-field / retroreflective panel** (Looking Glass-class, AIP) | Commercial products exist today. **Software side now de-risked** — three real-time many-view rendering papers plus an already-working open-source webcam-to-panel pipeline (see literature update below) | Not free space — bound to a physical panel — but real depth cues, works today | **Hackathon track** |

## Literature update, Aug 2026 sweep (research task: "reduce the 15% gap")

A dedicated pass through ~742 previously-fetched, unread OPTICS-track papers (full write-ups in `research/deepseek_research.md` Track 1) was run specifically to try to narrow the free-space-display gap. Verdict, stated as plainly as the research pass itself stated it: **nothing found closes or comes close to closing the gap. The ~85%/15% split in `FilesPlan.md` stands.** What did change is more nuanced than "still exactly as unsolved":

- **CGH's narrow-viewing-angle problem is now measurably outdated.** 2511.22639 (a static metasurface pixel-interpolating a conventional LCoS SLM) demonstrates a real, hardware-validated 159.4°×159.2° dynamic hologram FOV at 60Hz — a ~7×7 area improvement over the ~few-degree figure previously cited (was sourced to arXiv 2203.06784). Monochromatic, small benchtop scale (95mm image at 8.4mm), precomputed-frame playback (not live generation) — but angle itself is no longer the blocking constraint it was.
- **Generic real-time CGH is achievable today**, just not of a human face: 2601.00630 (28fps holographic replay of real physical objects, measured not rendered, but needs 4×datacenter GPUs and an optical bench), 2409.11049 (HoloTile RGB — 60Hz full-color speckle-free video on a commodity SLM, >100× faster than conventional CGH), and 2205.02367 (exploits an existing 1440Hz commercial MEMS phase SLM). None has been run on a moving photoreal face — the closest content is three dice and a swimming dolphin.
- **Speckle has a strong but slow fix.** 2604.16237 (Ellipsography — joint phase+polarization modulation) gets ~30dB PSNR, 10dB better than the prior best real-display speckle-suppression technique, but runs at ~2.2s/frame and needs non-standard optics — it trades the speckle problem for no improvement on the speed problem.
- **The laser-plasma north-star track gets a caution, not a scaling win.** 2501.10198 shows a real physical reason (cumulative air-density depletion above ~10kHz pulse repetition rate — JSID 2025's baseline sits right at this crossover) why naively raising rep rate to scale voxels/s likely isn't linear. 2601.08906 (a >10 million-effective-fps arbitrary 2D beam-addressing SLM) is a genuinely remarkable physics result but is a neutral-atom-quantum-computing tool with single-digit-to-tens demonstrated spot count, no depth/z mechanism, and a multi-meter optical path — a "watch this," not evidence voxel counts can jump orders of magnitude. Both added as research questions to `experiments/voxel-display/README.md`.
- **Aerial-imaging magnification (Branch C) turned up nothing** in this pass — exactly as unaddressed as before.
- **Track D (perceptual threshold) could not be assessed** — psychophysics/presence papers are tagged PERCEPTION not OPTICS in the corpus, so this sweep (scoped to unread OPTICS papers) had no material to check. `docs/theory.md`'s engineering hypothesis remains exactly as unverified as `experiments/perceptual-quality/README.md` already states.
- **The hackathon-track light-field panel choice got a real, unrelated-to-the-gap win**: three independent papers (2605.04509 CoherentRaster, 2601.19901 LFDPR, 2508.18540 — all real-time many-view rendering from Gaussian/voxel content, one at 228fps on an actual commercial Looking-Glass-class panel) plus 2506.08064 — an already-working, open-source, single-webcam-to-Looking-Glass-Portrait live pipeline that explicitly names video conferencing as a use case — show the hackathon track's *entire* capture→view-synthesis→panel pipeline is buildable today on commodity hardware. See `pipeline/view_synthesis/README.md` and `experiments/light-field/README.md`.

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
