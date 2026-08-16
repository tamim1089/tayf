# Figure Index — read the originals alongside this project

A pointer table, not a copy. Every row is a real figure in a real paper, with a direct link, so you can open the source and read the figure **with its caption and surrounding text** — which is what actually makes a figure useful.

Nothing here is reproduced into this repository. The diagrams in `models/svg/` are original drawings of the same physics, carrying this project's numbers rather than the papers'.

**Verification status:** identifiers below were resolved during the document audit. Anything marked ⚠ was cited but not independently opened — treat it as a lead, not a source.

---

## The optical mechanism — read these first

| Source | Look at | Why it matters here |
|---|---|---|
| **Yamamoto, *J. Imaging Soc. Japan* 56(4) 341–351 (2017)**<br>`10.11370/isj.56.341` · **open access, J-Stage** | Optical layout figures and the viewing-angle measurement | **The single most important source in the project.** Defines the AIRR geometry we build on, measures **170° viewing angle** and **>2.2× polarised gain**, and shows image position is independent of retroreflector shape and placement. This is where our `airr_ray_path` diagram comes from |
| **Smalley et al., *Nature* 553, 486 (2018)**<br>[`10.1038/nature25176`](https://doi.org/10.1038/nature25176) | The optical-trap display figures, and the clipping discussion | States **"clipping"** as a general theorem: an image cannot appear outside the aperture cone, with matter at the image point as the sole exception. Law 1 of this project. Also the reference photophoretic display |
| **MDPI *J. Imaging* 11(5) 150 (2025)**<br>[`10.3390/jimaging11050150`](https://doi.org/10.3390/jimaging11050150) | ASKA3D plate specs and the comparison table | The **~40°** viewing figure belongs here, to MMAP micro-mirror plates — *not* to AIRR. This repo conflated the two for days. Read it next to Yamamoto to see the difference |
| **MDPI *J. Imaging* 11(3) 75 (2025)**<br>[`10.3390/jimaging11030075`](https://doi.org/10.3390/jimaging11030075) | Aerial-imaging optical comparisons | Adjacent aerial-display engineering |
| *Optical Review* (2026)<br>`10.1007/s10043-026-01034-w` ⚠ · `10.1007/s10043-026-01038-6` ⚠ | Thickness/magnification and resolution engineering | Cited in the AIRR line; **content not independently opened** |

## Rejected mechanisms — the figures that show why

| Source | Look at | Why it matters here |
|---|---|---|
| **Hirayama et al., *Nature* 575, 320 (2019)**<br>[`10.1038/s41586-019-1739-5`](https://doi.org/10.1038/s41586-019-1739-5) | The MATD apparatus, the six-particle demonstration, the POV traces | The acoustic route, evaluated in depth and rejected. The six-bead ceiling and the array-brackets-the-volume geometry are both visible in the figures |
| **SPIE 11310 (2020)**<br>[`10.1117/12.2569328`](https://doi.org/10.1117/12.2569328) | Display volume and frame-rate figures | The 10×10×10 cm³ MATD workspace, 12.5 Hz visual / 10 Hz with audio |
| **arXiv 2512.09401** | The volumetric-display subsection | Photophoretic trapping review; confirms no new experimental result since 2018 |
| **arXiv 2601.00630** | The holographic-telepresence system diagram | 28 fps wavefront replay — but on 4 datacentre GPUs and an optical bench |

## Capture, avatar and transport

| Source | Look at | Why it matters here |
|---|---|---|
| **arXiv 2601.07518** (Mon3tr) | System architecture, the latency breakdown table, the bandwidth comparison | **The closest full-stack reference to TAYF's solved half.** 215 floats/frame, <0.2 Mbps, ~80 ms, ~60 fps. Most of §5 and §6 traces here |
| **arXiv 2605.02086** (GETA-3DGS) | The rate–distortion curves | ~5× avatar compression |
| **arXiv 2510.10492** | The canonical/driving split diagram | <0.26 Mbps at 25 fps for canonical + driving |
| **arXiv 2503.20308** | The A/B study results | The 82.6% preference for *expressive* over *precisely-timed* motion — drives our perceptual allocation policy |
| **arXiv 2510.03874** (DHQA-4D) | The per-distortion MOS ranking | Which distortions viewers actually notice: geometry/texture matter, temporal jitter and UV compression do not |
| **arXiv 2405.14866** (Tele-Aloha) | Capture rig and display setup | Panel-bound telepresence, useful as contrast |

## Prior art / freedom to operate

| Patent | Relevance |
|---|---|
| [`US11474597B2`](https://patents.google.com/patent/US11474597B2) (Google) | **Observer-estimate-driven angular view selection.** Directly reads on the eye-tracked architecture. In force to 2040 |
| [`US10327014B2`](https://patents.google.com/patent/US10327014B2) (Google) | Symmetric capture-and-3D-display telepresence terminals. To 2037 |
| [`US11683448B2`](https://patents.google.com/patent/US11683448B2) (Duelight) | Model-once plus per-frame nodal points — the parametric-transport thesis. To 2038 |
| [`US11425363B2`](https://patents.google.com/patent/US11425363B2) (Looking Glass) | Neural gap-filling between sparse views |
| [`US11340475B2`](https://patents.google.com/patent/US11340475B2) (Utsunomiya) | **Aerial imaging — the highest FTO exposure on our critical path.** To 2038 |
| [`US11947139B2`](https://patents.google.com/patent/US11947139B2) (Toppan) | Aerial display. To 2041 |
| [`US10228653B2`](https://patents.google.com/patent/US10228653B2) · [`US10129517B2`](https://patents.google.com/patent/US10129517B2) | Volumetric/aerial display prior art |

---

## How to use this while reading

The four diagrams in the universal document are **originals**, not reproductions:

| Our diagram | Read alongside |
|---|---|
| `airr_ray_path.svg` | Yamamoto 2017 optical layout |
| `aperture_modes.svg` | Smalley 2018, the clipping discussion |
| `angular_presence.svg` | *(no source — derived here from foveal acuity)* |
| `efficiency_cascade.svg` | Yamamoto 2017 §gain; the η_RR term is unmeasured anywhere |

**η_RR — the retroreflector return efficiency — is stated in none of these papers.** If you find a figure that gives aerial-image luminance per unit source luminance, that closes the largest open number in the project. It is worth watching for while you read.
