# Experimental Program

Source: `research/notes.md` §24-28, §46-49. This is the physical/empirical validation ladder for `hardware/optical-engine.md` and `docs/theory.md`'s hypotheses — none of this has been run yet; it's the protocol, not results.

## Why this order

A human is a bad first optical test target — it compounds skin, hair, cloth, expression, identity, and occlusion into one experiment. The correct order isolates the optical problem first, then adds human-specific difficulty incrementally: **point → line → plane → 3D cube → rotating object → text/symbol → face → hand → head → upper body → full human.** Each stage answers "how much spatial and angular information is required before the observer perceives a stable three-dimensional object," at increasing difficulty. Do not skip ahead to "render a person" before the point/line/plane stages are measured — those measurements are what tell you whether the chosen optical engine can plausibly scale to a person at all.

## The 8 core experiments

| # | Name | Goal | Success metric |
|---|---|---|---|
| 1 | Free-Space Point | Create one stable visible point in free space | Stable voxel at a known 3D coordinate |
| 2 | Free-Space Geometry | Create a simple 3D object | Observer perceives a stable 3D object without a physical display surface |
| 3 | Rotation | Create a rotating 3D object | Angular consistency under rotation |
| 4 | Viewpoint Change | Move observer around the optical volume | Correct view-dependent image |
| 5 | Dynamic Human Primitive | Render a head or hand | Recognizable motion, stable depth |
| 6 | Avatar Transmission | Send a human representation through the network | Acceptable quality at <1 Mbps (already exceeded on paper by Mon3tr's <0.2Mbps — this experiment validates it on TAYF's actual `pipeline/`, not just cites the reference) |
| 7 | End-to-End Telepresence | Two remote nodes communicate | Human-to-human spatial conversation |
| 8 | Cube Miniaturization | Reduce optical system size | Maintain acceptable perceptual quality while approaching 10×10×10cm |

Experiments 1-4 belong to `hardware/optical-engine.md`'s track in isolation (no capture/network pipeline needed yet — see `experiments/voxel-display/` and `experiments/light-field/`). Experiments 5-8 require the full `pipeline/` stack to exist first.

## Research notebook — required fields per experiment run

Every experiment run gets logged with all of the following (per-branch READMEs below adapt this template to their specific metrics):

- **Hardware:** exact components, dimensions, optical geometry, optical power, power consumption, temperatures.
- **Software:** model, model version, weights, inference latency, GPU, CPU, memory.
- **Network:** bitrate, jitter, packet loss, RTT, end-to-end latency.
- **Optical:** viewing angle, spatial resolution, brightness, voxel size, optical efficiency, stability, apparent depth, ghosting, persistence.
- **Perception:** identity similarity, depth perception, 3D stability, motion quality, view consistency, human preference.

## Primary failure modes to specifically test for

Optical scaling (can the free-space volume become large enough), angular resolution (does the image break as the viewer moves), brightness (do enough photons reach the observer), safety (laser exposure), heat (does the optical engine fit its thermal envelope — `hardware/power-thermal.md`), temporal coherence (does the human flicker/"boil" during motion), hand/finger merging or disappearance, face convincingness (eyes, mouth), hair collapsing into an unnatural structure, and optical artifacts (ghost images, speckle, diffraction artifacts, chromatic artifacts, aliasing, view discontinuities).

## Branches (see each directory for a full protocol)

- `voxel-display/` — Branch A: laser-excited volumetric voxels.
- `light-field/` — Branch B: directional light-field / holographic reconstruction.
- `aerial-imaging/` — Branch C: aerial image optics.
- `angular-resolution/` — cross-branch: minimum physical view count question from `pipeline/view_synthesis/README.md`.
- `bandwidth/` — validates `pipeline/transport/README.md`'s target numbers on real hardware.
- `latency/` — validates the <150ms end-to-end budget (`docs/theory.md`, `pipeline/transport/README.md`) stage by stage.
- `perceptual-quality/` — Track D (`docs/theory.md`): how little optical information is actually needed for convincing presence.
