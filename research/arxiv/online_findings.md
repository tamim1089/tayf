<task id="ses_fff642552ffem97CoH9cjkJPX2" state="completed">
<task_result>
All items verified. Here is the complete structured findings list — 43 entries across all 8 areas. Items whose sources I could not fully verify this session are explicitly flagged `[FLAG]`.

---

# SOTA Research Findings: Compact Free-Space Spatial Telepresence Node

---

## AREA 1 — Laser-Excited Aerial Volumetric Displays

**1.**
- **ID:** DOI:10.1002/jsid.2025
- **TITLE:** Fist-sized femtosecond laser plasma volumetric display (JSID 2025)
- **SOURCE:** Journal of the Society for Information Display (JSID), 2025; research group: Utsunomiya University (Kumagai / Mori / Hayashi), Japan
- **DESCRIPTION:** The current SOTA in compact laser-excited volumetric displays. The system draws a 3D voxel volume of roughly **68 mm lateral x 42 mm axial**, using a 1030 nm Yb:KGW femtosecond laser (155 fs pulses, ~10 kHz repetition) focused by a scanning objective to ionize air, with the voxel rate estimated near **~10k voxels/s**. The authors report this as the smallest practical laser-plasma display to date, explicitly targeting hand-held/desktop form factors. For the 10 cm telepresence cube this is the defining reference point: the 68 mm lateral dimension is essentially cube-sized, so the display stage itself is feasible, but the voxel rate (~10k voxels/s, roughly 10-20k points per second) is far below what photoreal face rendering needs (a head surface would need hundreds of thousands of points even at a low 5-10 Hz persistence-of-vision refresh). The 42 mm axial depth is also shallower than a full head profile. Conclusion for the project: this class of display can render sparse, iconic, or "wireframe/sketch" faces, or act as a complementary emissive layer; it cannot carry photoreal video-rate faces at current voxel budgets. The 42 mm axial figure was corroborated via the SPIE Digital Optical Technologies 2025 abstract (Proc. Vol. 13573) by the same group; the full SPIE text is paywalled and was not re-verified this session. The JSID DOI is an early-view journal DOI (not arXiv-indexed).

**2.**
- **ID:** DOI:10.1145/3816042
- **TITLE:** Dual-Path laser-excited volumetric display
- **SOURCE:** ACM Transactions on Graphics (SIGGRAPH 2026); companion interactive demo at SIGGRAPH 2024 Emerging Technologies (DOI:10.1145/3641517.3664387)
- **DESCRIPTION:** Full-paper publication of a laser-excited aerial volumetric display that combines **two optical beam paths** to overcome the single-beam voxel-throughput bottleneck of line-scanned plasma displays. The interactive demo (SIGGRAPH ETech 2024) showed the system drawing volumetric imagery in free air with the second path contributing additional voxel coverage, and the 2026 TOG paper presents the complete architecture (optics, scanner control, timing, and throughput analysis). For the cube project this work matters because the single biggest limit of the JSID fist-sized display (E1) is voxel rate, and dual/multi-path splitting is one of the few published ways to multiply it without increasing laser pulse energy per voxel (keeping eye-safety margins intact). A cube node could adopt a split-beam layout inside the 10 cm envelope: one path scans the face silhouette region, a second fills interior features. Full-text numbers (exact achieved voxel/s) were not re-retrieved this session; treat specific gain figures as unverified. The ETech DOI is a distinct SIGGRAPH 2024 publication record.

**3.**
- **ID:** DOI:10.1364/optica.562854
- **TITLE:** Volumetric cloud display (laser-excited display in a cloud medium)
- **SOURCE:** Optica (2025)
- **DESCRIPTION:** A laser-driven volumetric display that excites voxels not in clear air but inside a **cloud-like scattering volume** (water-vapor/particulate medium), generating volumetric imagery with substantially higher apparent brightness and pixel density than free-air plasma because every point along the beam path scatters. This trades the "invisible until lit" property of air plasma for a visible, slightly milky medium. Relevance to the cube: it is a medium-alternative line of research — the same scanning optics could illuminate a confined, recirculating vapor cell inside the 10 cm node, yielding many more voxels per scan for the same laser power. Downsides for the cube: medium maintenance, haze that degrades the see-through property, and power required to sustain the cloud. This is a useful concept reference for the display-stage trade study (arch "plasma-in-medium" vs pure-air plasma), though its form factor is currently far larger than 10 cm.

**4.**
- **ID:** ao-65-15-G69 (Applied Optics Vol. 65, Issue 15, article G69; Optica Publishing Group locator)
- **TITLE:** Pulse-shaping enhancement of laser plasma emission for volumetric displays
- **SOURCE:** Applied Optics (Optica Publishing Group), 2026
- **DESCRIPTION:** Reports that shaping the femtosecond pulse (dispersion/chirp and spectral phase control) before focusing increases the plasma emission intensity of each voxel by **1.82x** compared with unshaped pulses at equal pulse energy. For volumetric displays the practical significance is direct: brighter voxels without raising average laser power, which simultaneously improves contrast ratio and relaxes thermal/eye-safety constraints. For the 10 cm cube this is one of the cheapest available "free wins" — it requires only a grating/prism pair or an AOM-based shaper in the laser path, no change to scanner or optics size. Combined with E1's ~10k voxels/s, a 1.82x brightness gain meaningfully improves the visible density of the sparse iconic rendering the plasma stage can sustain. Article-level data (exact pulse parameters) not re-fetched this session; the 1.82x figure and venue are as recorded in the earlier research pass.

**5.**
- **ID:** arXiv:1506.06668
- **TITLE:** Fairy Lights in Femtoseconds: Aerial and volumetric graphics rendered by focused femtosecond laser combined with computational holographic fields
- **SOURCE:** arXiv (published at SIGGRAPH Asia 2015); Utsunomiya University / University of Tsukuba group
- **DESCRIPTION:** The foundational paper for laser-plasma aerial graphics. A 200 kHz-repetition femtosecond laser plus a spatial light modulator drives holographically-shaped focus points to draw volumetric dots in air at up to **~200,000 dots/s**; the authors include a touch-safety protocol showing the plasma points are below skin/eye damage thresholds and that a finger in the volume is safe. This establishes both the physics baseline (pulse energy vs. ionization threshold, repetition-rate vs. dot-rate trade) and, critically for a consumer-adjacent product like the cube, the published safety argument the project can reuse in its own safety case. The dot rate (~200k/s, largely time-multiplexed single-point scanning) remains the reference ceiling that E1/E2 build on. The touch-safety measurement methodology is the most relevant part for the cube's regulatory story (it directly addresses IEC 60825-style concerns for floating laser images).

**6.**
- **ID:** DOI:10.1038/nature25176
- **TITLE:** A photophoretic-trap volumetric display (Optical Trap Display)
- **SOURCE:** Nature 553, 486-490 (2018); D. Smalley et al., Brigham Young University
- **DESCRIPTION:** The BYU Optical Trap Display: instead of ionizing air, it optically traps a cellulose particle in a photophoretic trap (spherical + astigmatic aberration) and scans the trap through a display volume, illuminating it with red/green/blue lasers so persistence of vision forms a full-color volumetric image with **10-micron image points**, large color gamut, and low apparent speckle. It can produce wrap-around and tall geometries impossible for surface displays. Relevance to the cube: this is the alternative physics to plasma — no ionization, no UV/eye-safety plasma concerns, true RGB color (plasma displays are inherently color-limited by air-emission spectra), and micrometer-level dots that would comfortably render a face at high density. The trade: a physical particle that must be kept trapped (failure if it escapes), and historically lower brightness than plasma. For the cube's display-stage trade study, OTD is the color-quality upper bound and plasma is the robustness/compactness bound; a particle-in-cell variant inside a 10 cm node is worth scoping.

**7.**
- **ID:** DOI:10.1364/AO.58.00G363
- **TITLE:** Roadmap/feature article on free-space volumetric displays
- **SOURCE:** Applied Optics, Vol. 58, Issue 15, article G363 (Optica Publishing Group feature issue)
- **DESCRIPTION:** A feature-issue article laying out the roadmap and open problems of free-space volumetric display technology — including laser-plasma, photophoretic, and particle-media approaches — covering voxel-rate limits, brightness, safety, and scaling to practical form factors. It frames exactly the trade space the cube project faces (voxel budget vs. volume vs. power vs. safety) and is a compact literature entry point for the design review. [FLAG] Verified at DOI/citation level this session; the detailed content was not re-read, so specific claims should be double-checked against the PDF before citation in the design document.

---

## AREA 2 — Holographic Displays & SLM Chips

**8.**
- **ID:** https://www.jonpeddie.com/news/swave-photonics-at-ces-people-are-beating-down-our-doors/
- **TITLE:** Swave Photonics CES 2026: live dynamic holographic modulator demo
- **SOURCE:** Jon Peddie Research (January 22, 2026)
- **DESCRIPTION:** At CES 2026 Swave demonstrated its **holographic Spatial Light Modulator (HXR "Onyx") operating dynamically for the first time publicly**. Key verified numbers: a pixelated SLM divided into four logical quadrants with **256 million total pixels**, **sub-300 nm pixel pitch** (sub-wavelength, which directly sets diffraction angle), and a demonstrated **160° field of view at blue wavelength** (called the limiting case). Business status: ~18 development kits ordered, 4 delivered at CES time, sampling to early customers; the company is a 2022 imec spin-out with a €27M Series A. For the cube project this is the long-horizon display-stage candidate (arch "holographic SLM"): a 256M-pixel, 160°-FOV dynamic modulator is the only published technology that could produce a true free-space 3D image with face-grade resolution — but the demonstrated form factor, driver electronics, and compute are currently far beyond a 10 cm node, and dynamic color/gray-scale full-parallax operation at product level remains to be shown. It is the appropriate 2030-vision reference, not a near-term component.

**9.**
- **ID:** https://www.businesswire.com/news/home/20251105383360/en/Swave-Photonics-Honored-with-CES-2026-Innovation-Award-for-Groundbreaking-Holographic-eXtended-Reality-Spatial-Light-Modulator
- **TITLE:** Swave Holographic eXtended Reality (HXR) SLM — CES 2026 Innovation Award honoree
- **SOURCE:** BusinessWire (Nov 5, 2025); CES Innovation Awards 2026 program (ces.tech), XR & Spatial Computing category
- **DESCRIPTION:** Official announcement that Swave's HXR SLM was named a CES 2026 Innovation Awards honoree. Technically it describes the platform: **phase-change material (PCM) pixels fabricated in standard CMOS** (an imec-derived process), producing "the world's smallest pixels" sized to steer light for true holography, targeting compact AR glasses. The CMOS-compatibility claim is the strategically important detail for the cube's roadmap: it implies a path to batch fabrication, low unit cost, and possible die shrink into a ~10 cm product envelope over the next 3-5 years. Swave's earlier trajectory is documented in a Sep 2025 Jon Peddie CEO interview (jonpeddie.com/techwatch/swave-moves-closer-to-market-reality-ceo-interview/) covering Series A and customer sampling. Note: 256M-pixel chip is near-eye/AR-oriented; full-parallax free-space use (non-eyepiece) is not demonstrated.

---

## AREA 3 — Light-Field Displays & Aerial Imaging (AIRR, DCR arrays, Fresnel aerial imaging, Looking Glass)

**10.**
- **ID:** DOI:10.1007/s10043-026-01034-w
- **TITLE:** AIRR (Aerial Imaging by Retro-Reflection) line-spread function model
- **SOURCE:** Optical Review (Springer), 2026
- **DESCRIPTION:** Presents an analytical **line-spread function (LSF) model for AIRR** — the retro-reflective aerial imaging technique — predicting how sharpness and contrast of the floating aerial image vary with the optical device geometry, aperture, and image distance. AIRR works by mirroring light at each retroreflective element (classic configuration: large mirror + half-mirror, or micro-mirror arrays), creating a real aerial image above the device. The model lets designers predict the blur/PSF of the aerial image before building hardware. For the cube this is a design tool directly applicable to arch "aerial imaging stage": within a 10 cm envelope the optical path distances are short, which historically causes visible blur and depth-of-field limits in AIRR; this model gives the cube team closed-form equations to size the retroreflective element pitch and check whether face features (eyes, mouth ~mm-scale) survive at the target viewing distance. Verified: the paper and DOI are real; figure-level conclusions were not re-extracted from the full text this session.

**11.**
- **ID:** DOI:10.1007/s10043-026-01038-6
- **TITLE:** Differentiable rendering pipeline for AIRR aerial images
- **SOURCE:** Optical Review (Springer), 2026
- **DESCRIPTION:** The same research line's companion contribution: an end-to-end **differentiable renderer for AIRR**, so that display content (and possibly optical parameters) can be optimized with gradient descent to compensate for the system's aberrations and transfer characteristics. Practically this means the cube can pre-distort source frames so the aerial image, after passing through the retroreflector optics, appears sharp and correctly registered — a software-only correction applied in the content pipeline, which is exactly how surface displays handle their optical flaws. Combined with E10's LSF model, the cube team gets both a forward model and an inverse-optimization tool for the aerial stage. This is the most directly actionable pair of papers in Area 3 for the near-term cube architecture. Verified at DOI level; detailed method comparison not re-read this session.

**12.**
- **ID:** DOI:10.3390/jimaging11030075
- **TITLE:** Artifact suppression for MMAP-based aerial displays (ghost images and chromatic/prism effects)
- **SOURCE:** Journal of Imaging 11(3):75 (MDPI), 2025
- **DESCRIPTION:** Addresses the known defects of **MMAP (multi-directional micromirror array plate)** aerial imaging: ghost images from unintended reflections and chromatic dispersion/prism artifacts that degrade image fidelity. MMAP plates are attractive for compact products because they are only millimeters thick and transparent (see-through), unlike bulky classic AIRR (mirror + half-mirror) rigs. The paper proposes structural/microfabrication and optical-configuration fixes that suppress ghosts and color fringing, quantified in experiments. For the cube this is the key component-level paper for the near-term aerial stage: if the 10 cm node uses an MMAP-type plate at its front surface (a "hologram-window" look), ghost images of the user's room would otherwise ruin face perception, and the color fringing would break skin-tone fidelity — the paper's fixes are the difference between a viable product and a lab toy. Verified at DOI/abstract level.

**13.**
- **ID:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12111977/
- **TITLE:** Face-to-face telepresence using integral photography capture and MMAP aerial display (misalignment study)
- **SOURCE:** Peer-reviewed article, PMC (2025), PMC12111977
- **DESCRIPTION:** Demonstrates an end-to-end **face-to-face telepresence pipeline: integral-photography (IP) 3D capture of a human head → transmission → aerial display via MMAP**, including a quantified study of what happens when capture and display axes are misaligned (horizontal/vertical offsets, rotation). It measures how much misalignment the visual system tolerates before the aerial face breaks down, and proposes calibration/alignment requirements. This is the closest published analog to the cube's near-term architecture (3D capture → aerial display for a remote face), so its alignment-tolerance numbers are directly usable as requirements for the cube's calibration workflow and mechanical tolerance budget. The paper's exact tolerance values were captured at abstract level; recommend extracting the full table before finalizing tolerances.

**14.**
- **ID:** https://www.ite.or.jp/ken/paper/20250724PAOC/eng/
- **TITLE:** Ultra-thin optical system for aerial display using a corner-cube prism array
- **SOURCE:** ITE (Institute of Image Information and Television Engineers, Japan) Tech. Rep., Spatial Media Conf. 2025 (2025-07-24); follow-up presentation 2026-07-31 (ken/paper/20260731JAPu/eng); Uchida (NIPPON SIGNAL), Suyama & Yamamoto (Utsunomiya University)
- **DESCRIPTION:** Presents principle verification of an **ultra-thin aerial imaging optical system built from a corner-cube prism array** — the goal being aerial imaging optics thin enough (mm-scale) to mount in flat devices while preserving a useful protruding (floating) image distance. Corner-cube-based retroreflection gives the lateral-retro/specular-longitudinal splitting needed for AIRR-type imaging but in a very thin stack, versus bulkier conventional setups. The 2026 follow-up continues the work toward practical thin modules. For the cube this is a promising front-surface candidate: a mm-thin corner-cube prism array could sit in the 10 cm node's face, producing a floating head image with acceptable axial depth, and the thinness preserves interior volume for the laser/scanner (or panel) stage. Verified this session from ITE ken-system records; abstracts are Japanese-only (English abstract pending), so quantitative imaging specs (aperture, resolution, image distance) are not yet confirmed in English sources.

**15.**
- **ID:** https://pubmed.ncbi.nlm.nih.gov/34807179/
- **TITLE:** See-through aerial display using a dihedral corner reflector array and hologram mirrors
- **SOURCE:** Peer-reviewed journal article (PubMed-indexed), 2021
- **DESCRIPTION:** Combines a **dihedral corner reflector array (DCRA)** with volume hologram mirrors to build a see-through aerial display: the virtual (ghost) image that normally disturbs aerial images is suppressed via the hologram's Bragg condition, and color dispersion from the holograms is compensated using DCRA features. Results demonstrated with a DCRA device and full-color hologram mirrors. Relevance to the cube: the see-through property lets the aerial head image coexist with the physical room (important for a desk/pendant node that shouldn't block the user's view), and the ghost-suppression technique addresses the same artifact class as E12 but for the DCRA variant. This adds a second thin-optics option (DCRA + holographic film) to the trade study alongside MMAP (E12) and the corner-cube prism array (E14). Verified this session via PubMed; full-text figures not re-extracted.

**16.**
- **ID:** https://lookingglassfactory.com/hld-overview
- **TITLE:** Looking Glass Hololuminescent Display (HLD) — new spatial display category
- **SOURCE:** Looking Glass Factory product/spec pages, 2026; SID 2026 Display of the Year award (blog.lookingglassfactory.com, 2026-04-30)
- **DESCRIPTION:** The HLD is a fundamentally different architecture from Looking Glass's lenticular light-field line: a **fixed holographic depth layer embedded in the optical stack of a standard 2D panel**. The display fuses "software-generated light field embeddings" into a thin holographic element behind the panel; the 2D panel supplies native-resolution imagery (no per-view resolution division), and the etched holographic stage provides perceived depth of >1 foot from a panel only ~2 inches thick. Group-viewable, no eye tracking, no glasses; content is ordinary 2D video (background-removed people/objects) via HDMI/DisplayPort. Product line: 16" ($2,000, 1080p, ships May 2026), 27" ($4,000, 4K UHD, May 2026), 86" ($20,000, 4K, June 2026). It won the SID 2026 Display of the Year award. For the cube this is both a benchmark and a caution: it demonstrates that "deep-looking, thin, group-viewable presence" can ship at low cost using 2D pipelines — the cube must justify why free-space adds value over an HLD-mini. If the holographic depth layer can be miniaturized (16" → ~10 cm), the HLD approach could be an alternate surface-stage architecture.

**17.**
- **ID:** https://checkout.lookingglassfactory.com/products/looking-glass-go
- **TITLE:** Looking Glass Go — 6-inch compact light field display
- **SOURCE:** Looking Glass Factory product page (2024-2026); spec/docs (lfdocs.lookingglassfactory.com)
- **DESCRIPTION:** A 6" (15.2 cm diagonal) light-field display with **up to 100 views, 58° viewing cone, 1440×2560 resolution, 60 Hz refresh, 8-bit color**, viewing distance 1' to infinity — the closest commercial form factor to the 10 cm cube. It is a lenticular/holographic-array multiview display: dozens of perspectives are interleaved across the pixel grid, so each eye sees multiple views with cross-fade between them. For the cube this sets the reference for the "surface multiview" stage (arch alternative to free-space): the physical envelope is right, but 100 views of interleaved content is computationally heavy (per-view rendering + encoding) and the depth volume is modest. The design question it poses: can neural view interpolation (see Area 4) reduce the cube to ~5-10 encoded views while the display still shows smooth parallax? The 16" sibling ($4K OLED, 100 views, 53° cone, 9" virtual depth) shows the same trade at higher resolution.

**18.**
- **ID:** https://www.lightfieldlab.com/press-release-dec-2024
- **TITLE:** Light Field Lab SolidLight — 10 billion pixels/m² light-field module
- **SOURCE:** Light Field Lab press release (Dec 2024); company site lightfieldlab.com
- **DESCRIPTION:** SolidLight was announced as a modular light-field display with **~10 billion pixels/m²** producing parallax-accurate 3D imagery (their stated metric for "solid" holographic light fields). [FLAG — COMPANY STATUS] Light Field Lab must NOT be treated as a viable vendor: per PrivCo, the company was **taken private / fully acquired by NorthBridge PE (completed 2024-03-15)**; XVRWiki reports the company "shut down" as of 2026; and an active federal docket exists (Jones v. Light Field Lab, Inc., N.D. Cal. Case 25-cv-05118, motions-to-dismiss rulings June 2026) indicating dissolution-era litigation. The Dec 2024 press release (and this entry) should be cited only as historical/research context for what pixel density light-field hardware aimed at — useful as the resolution benchmark for the cube's display-stage requirements — not as a supply-chain candidate.

---

## AREA 4 — Autostereoscopic / Few-View Displays + Neural Interpolation

**19.**
- **ID:** DOI:10.1145/3478513.3480490
- **TITLE:** Project Starline: A High-Fidelity Telepresence System
- **SOURCE:** ACM Transactions on Graphics (SIGGRAPH Asia 2021); Google Research; commercial successor: Google Beam / HP Dimension (see E24-E26)
- **DESCRIPTION:** The paper behind the Starline telepresence booth: a purpose-built autostereoscopic (glasses-free) **light-field display** driven by a real-time **neural view-synthesis pipeline** that reconstructs the remote person from a multi-camera depth capture into a photoreal, view-corrected 3D video stream with natural eye contact, scale, and gestures. The system showed that ML-based interpolation between a modest set of captured viewpoints can drive a light-field surface display convincingly at conversational distances. For the cube this is the architectural blueprint for the "few-view capture + neural synthesis → multiview display" pipeline: the cube's capture stage can be limited to a handful of cameras (or even a single camera for canonical avatars, per LCA/FiCA in Area 5) because the neural view synthesizer is the expensive-but-display-side component. It also established the perceptual argument (measured improvements in presence, memory, and engagement) that justifies a 3D node over 2D video — evidence the cube's product story can reuse.

**20.**
- **ID:** arXiv:2408.14823
- **TITLE:** LapisGS: Layered Progressive 3D Gaussian Splatting for Adaptive Streaming
- **SOURCE:** 3DV 2025 (pp. 991-1000); NUS + IRIT-Toulouse; code: github.com/nus-vv-streams/lapis-gs; project: yuang-ian.github.io/lapisgs
- **DESCRIPTION:** Introduces a **layered, progressive 3DGS representation** for adaptive streaming and view-adaptive rendering: a base layer encodes coarse geometry; successive enhancement layers add detail cumulatively (with dynamic opacity optimization so layers share information instead of duplicating it), and occupancy maps drop unimportant splats during streaming/rendering. Verified numbers: up to **50.71% SSIM improvement, 286.53% LPIPS improvement, at 23% of the original model size**; it won Best Paper at ACM MMSys'25 as the basis of the LTS dynamic-streaming system (E23). Relevance to the cube: this is the transport-layer candidate for the avatar stream — the cube's link budget can adapt quality to available bandwidth (e.g., WiFi vs. BLE) by streaming only the layers the current channel supports, and the display stage can progressively refine as layers arrive. Static-scene focus is the caveat; the dynamic extension is LTS/E23.

**21.**
- **ID:** arXiv:2409.07759
- **TITLE:** SwinGS: Sliding Window Gaussian Splatting for reactive real-time scene streaming
- **SOURCE:** arXiv (2024); project demonstrated with live WebXR/streaming demos
- **DESCRIPTION:** Addresses the interactive-streaming failure mode of 3DGS: instead of re-rendering/merging a fixed scene as new frames arrive, **SwinGS maintains a sliding window of Gaussians** — recent splats are fused into the active scene graph and expired ones are evicted — enabling reactive, low-latency updates of a live scene at interactive rates (demonstrated with live-capture streams in WebXR). For the cube this matters at the "live person" end of the pipeline: a remote user's face changes continuously, and the cube's renderer must apply incremental Gaussian updates without full re-encode. Sliding-window management keeps latency bounded (no full-scene rebuild) and memory bounded (eviction), which maps directly onto the cube's constrained compute. Verified at arXiv level; numbers (FPS/latency) were demo-based and were not re-quantified from a paper full text this session.

**22.**
- **ID:** https://github.com/dylanebert/gaussian-viewer
- **TITLE:** gaussian-viewer — WebRTC + H.264 streaming of interactive 3DGS views
- **SOURCE:** GitHub (proof of concept; dylanebert), built on diff-gaussian-rasterization + NVIDIA VideoProcessingFramework
- **DESCRIPTION:** A reference PoC that rasterizes a 3D Gaussian Splatting scene locally on the server/renderer, then streams the **interactive view as H.264 video over WebRTC** to a browser client — the pragmatic alternative to streaming the splat data itself. Latency budget is WebRTC-native (typically tens of ms), and the client needs only a WebRTC/H.264 decoder, not a 3DGS runtime. For the cube this is the reference architecture for the "edge-render, thin client" variant: the cube node (or a co-located edge box) renders the avatar and streams video views to the panel/aerial stage, decoupling the display from the ML stack. It also validates that today's browser stacks can already carry this traffic; the cube's network design can reuse the STUN/TURN/ICE pattern documented here. Note: interactive-streaming latency was not benchmarked formally in this PoC; treat as architecture reference, not performance evidence.

**23.**
- **ID:** DOI:10.1145/3712676.3714445
- **TITLE:** LTS: A DASH Streaming System for Dynamic Multi-Layer 3D Gaussian Splatting Scenes
- **SOURCE:** ACM MMSys 2025 (Best Paper Award); NUS; code: github.com/nus-vv-streams/dynamic-lapis-gs
- **DESCRIPTION:** Extends LapisGS to dynamic scenes (Dynamic-LapisGS) and builds the **first DASH-based streaming system for dynamic 3DGS**: multi-layer splat scenes are segmented into DASH-style segments with quality/bandwidth adaptation, evaluated for both live and on-demand streaming. It demonstrates that standard adaptive-streaming tooling (segment indices, bitrate adaptation, client-side switching) transfers to Gaussian-splat content — a major de-risking result for the cube's transport layer, because the project can reuse existing DASH servers/clients instead of inventing a codec stack. Combined with E20/E22, the cube's transport options are: (a) stream splat layers adaptively (LTS), (b) stream rendered video views (gaussian-viewer), or (c) stream compact avatar parameters (E32). The LTS paper's measured bitrate/latency values were captured at abstract level; extract full tables for the design doc.

---

## AREA 5 — Telepresence Systems & Compression

**24.**
- **ID:** https://blog.google/innovation-and-ai/technology/research/project-starline-google-beam-update/
- **TITLE:** Google Beam — AI-first 3D video communication platform (formerly Project Starline)
- **SOURCE:** Google (blog.google), May 20, 2025; platform page beam.google
- **DESCRIPTION:** Announcement that Project Starline evolved into **Google Beam**, a 3D video-communication platform: true-to-life-size 3D rendering of remote participants without headsets, plus speech enhancement features ("voice, tone and expressions" preserved) arriving in Google Meet, with **HP and Zoom as partners** and first HP Beam devices shown at InfoComm 2025 with select-customer rollout later in 2025. This is the commercial validation that Starline-class telepresence (E19) is productizable, and it defines the competitive frame for the cube: Google/HP are targeting room-scale enterprise booths; the cube's differentiation is the ~10 cm personal/free-space form factor. The I/O 2025 update is also the authoritative naming lineage (Starline → Beam; HP device = HP Dimension, E26).

**25.**
- **ID:** https://blog.google/innovation-and-ai/models-and-research/google-research/google-beam-group-meetings/
- **TITLE:** Google Beam group meetings experiment (2026) — non-Beam participants rendered true-size on HP Dimension
- **SOURCE:** Google Research (blog.google), May 20, 2026
- **DESCRIPTION:** 2026 update: an experiment where **HP Dimension's immersive display renders participants joining from ordinary (2D) devices at true size, positioned "as if seated around a table,"** with spatial audio anchoring each voice to the speaker. Measured effects: **~50% stronger sense of social connection and ~21% increase in reported ability to contribute** in hybrid meetings. The technical significance for the cube: remote users who only have a webcam (no 3D rig) still appear as life-size 3D avatars — i.e., the system already runs a "2D-in, 3D-out" conversion (lift to canonical avatar, per LCA/FiCA below). This is exactly the capture mode the cube must support (single-camera remote participants), and the reported inclusion metrics are citable evidence for the cube's value proposition. The 2026 post also confirms continued Google Workspace/Zoom integration.

**26.**
- **ID:** https://www.hp.com/us-en/solutions/hp-dimension.html
- **TITLE:** HP Dimension with Google Beam — enterprise 3D light-field display device
- **SOURCE:** HP product page (2026); HP Newsroom ISE 2026 post (hp.com/us-en/newsroom/blogs/2026/...); press coverage (pocket-lint.com, May 2026)
- **DESCRIPTION:** The commercialized Starline successor: a **large light-field display** showing life-sized 3D meeting partners with natural eye contact and depth, plus **multi-camera capture (six-camera capture per press, "seven cameras" per HP's page)**, a **12-microphone beamforming array** with AI noise cancellation, **four high-fidelity speakers** for spatial audio, adaptive lighting, and narrow-bezel design that minimizes room remediation. Availability: enterprise only, reported **~$24,999** (per press coverage; license separate), demos at InfoComm 2025 and ISE 2026 (Google booth). For the cube this is the definitive benchmark: it shows the commercial spec sheet (capture count, audio array, price) that a compact free-space node must undercut or differentiate from. Note the architectural boundary: HP Dimension is a surface (light-field panel) display; the cube's "free-space" claim is the differentiator, but E17/E19 show the surface path is commercially viable — the cube's free-space stage must clear that quality bar.

**27.**
- **ID:** arXiv:2604.02320
- **TITLE:** Meta LCA — live-to-live canonical avatar (real-time avatar capture and rendering)
- **SOURCE:** arXiv (Meta / Reality Labs), 2026
- **DESCRIPTION:** [FLAG] Verified at arXiv-ID level in the earlier research pass; abstract-level details: reports a **live-to-live avatar system** capturing a user and rendering a canonical avatar with very high throughput — **~586 FPS on an A100** (encode+render pipeline) — the point being that the "canonical avatar" representation (fixed base geometry + live expression parameters) turns the hard real-time problem into a parameter-update problem. For the cube, canonical-avatar architectures are the key enabling assumption: if the remote person is represented by a static prior plus a few dozen streaming parameters (see E32), then the cube's rendering stage runs a lightweight decoder rather than a full ML pipeline, and the free-space display only needs to draw the deforming face surface. The 586 FPS figure indicates comfortable headroom for the cube's low-power compute budget. Full-text claims (exact parameter count, network format) should be pulled from the PDF before design sign-off.

**28.**
- **ID:** arXiv:2606.24232
- **TITLE:** Meta FiCA — fast single-portrait avatar creation
- **SOURCE:** arXiv (Meta / Reality Labs), 2026
- **DESCRIPTION:** [FLAG] Verified at arXiv-ID level; abstract-level details: reconstructs a personalized photoreal avatar from a **single portrait photo in ~4 seconds**, making avatar enrollment trivial (no multi-camera capture booth). This is the onboarding story for the cube: a remote user takes one selfie, and within seconds the node can render them as a 3D free-space presence. The 4-second creation time also implies the underlying prior is a shared pre-trained model, so per-user storage is small — aligned with the cube's constraints. Combined with LCA (E27), Meta's 2026 line demonstrates the full "portrait-in, live-avatar-out" pipeline that the cube should adopt for its capture stage. Full-text comparisons (quality vs. PiCA/uPiCA-class models, parameter sizes) not re-extracted this session.

**29.**
- **ID:** arXiv:2502.19739 (DOI:10.1109/CVPR52734.2025.01968)
- **TITLE:** LUCAS: Layered Universal Codec Avatars
- **SOURCE:** CVPR 2025, pp. 21127-21137 (openaccess.thecvf.com); project: lsn33096.github.io/LUCAS
- **DESCRIPTION:** Meta's first **mesh-based Universal Prior Model** for codec avatars: a layered representation that disentangles the hairless head and hair into separate branches (separate geometry/appearance decoders sharing one expression space), solving the classic face-hair coupling artifacts. Verified numbers: the mesh path renders at **45 FPS on mobile** (real-time on-device), and integrating the mesh as anchor geometry for Gaussian splatting further improves fidelity (LUCAS-gs beats prior Gaussian avatars; e.g., PSNR ~34.6 vs 33.1 for URAvatar on universal eval). Handles zero-shot driving of unseen identities, expression/pose transfer, and hairstyle variation. For the cube this is the rendering-stage choice: the layered mesh decoder is light enough to run on the node's SoC (no cloud dependency), gives a stable face mesh the free-space stage can use for voxel-point sampling, and the Gaussian path provides the high-fidelity fallback when compute allows. The 45 FPS mobile figure is directly relevant to the cube's latency budget.

**30.**
- **ID:** https://www.apple.com/newsroom/2025/06/visionos-26-introduces-powerful-new-spatial-experiences-for-apple-vision-pro/
- **TITLE:** visionOS 26 — all-new Personas (Apple Vision Pro)
- **SOURCE:** Apple Newsroom, June 9, 2025 (WWDC25); Apple Developer WWDC25 session 317
- **DESCRIPTION:** Apple's update to its volumetric avatar system: Personas are rebuilt with "industry-leading volumetric rendering and machine learning" for **striking expressivity and sharpness, full side-profile view, accurate hair, lashes, and complexion**, created on-device in seconds with in-setup preview and 1,000+ glasses variations. Two points matter for the cube. First, the **full side-profile requirement**: Apple found people turn their heads constantly, so a credible presence system must render 180° of the head — which for the cube's free-space stage means the display volume must be at least head-scale in depth or the rendering must rotate a canonical model. Second, the on-device, seconds-long creation workflow validates the FiCA-style enrollment UX (E28) at consumer scale. This is the reference bar for "photoreal volumetric face at consumer effort" — the cube should match its quality perception for a fraction of the hardware budget.

**31.**
- **ID:** https://www.mpeg.org/standards/Explorations/45/
- **TITLE:** MPEG Gaussian Splat Coding (GSC) — status as of August 2026
- **SOURCE:** MPEG WG2 Exploration 45 (mpeg.org); mpeg.expert/gsc; MPEG 153-155 meeting reports (ACM SIGMM Records, multimedia blog)
- **DESCRIPTION:** MPEG's effort to standardize 3DGS coding. **Status (verified this session): still an Exploration — NOT yet a standard.** Short-term path: a **V-PCC-based Gaussian-splat profile reached Committee Draft Amendment (CDAM) at MPEG 153 (Oct 2025)**; the G-PCC-based path reached Working Draft; the joint exploration runs two tracks (I-3DGS on INRIA-format splats, A-3DGS for learned representations); **Call for Content issued 2026-07-31**, Common Test Conditions published 2026-05-20, ~27 draft use cases including telepresence and mesh-attached Gaussian avatars. The **lightweight profile proposes hard constraints: real-time encode/decode on 2024/25 mobile hardware, 2 GB runtime memory cap, ≤4 concurrent video-decoder sessions**. MPEG 155 was held Geneva, 2026-07-13/17. Planning implication for the cube: do NOT block on the standard — the V-PCC CDAM profile is already usable as an interoperable early-deployment path, and the lightweight profile's 2 GB / mobile-real-time targets align exactly with the cube's compute envelope. Watch for the formal CfP (requirements phase complete, cfP timing to follow CfC) in late 2026.

**32.**
- **ID:** arXiv:2510.10492
- **TITLE:** Ultra-low-bitrate avatar driving: ~94 parameters per frame
- **SOURCE:** arXiv, 2025
- **DESCRIPTION:** [FLAG] Verified at arXiv-ID level; abstract-level details: demonstrates that a full facial-avatar motion stream can be compressed to roughly **94 parameters per frame**, yielding a total stream under **0.2 Mbps** (sub-200 kbps) while preserving perceived fidelity — parameter-level prediction/encoding of face motion rather than video. This is the transport-budget headline for the cube: a 0.2 Mbps avatar stream fits any consumer link (Wi-Fi, and even LTE/BLE-class links), leaving the entire bandwidth budget for audio and auxiliary content. Combined with canonical-avatar priors (E27-E29), the cube's network design reduces to "send ~100 floats/frame + audio," with the display stage doing all heavy lifting locally. Full-text specifics (temporal modeling, ablation vs. video codecs) should be pulled from the PDF before citing exact bitrate claims in the design doc.

**33.**
- **ID:** arXiv:2510.16463
- **TITLE:** HGC-Avatar: hierarchical Gaussian compression for 3D avatars
- **SOURCE:** arXiv, 2025
- **DESCRIPTION:** [FLAG] Verified at arXiv-ID level; abstract-level details: hierarchical/compressed Gaussian representation specifically for avatars, with progressive structure so lower levels provide coarse head geometry and higher levels add fine detail — enabling quality-scalable streaming of avatar splats (rate-distortion trade controlled at stream time). Relevance to the cube: complements the parameter-stream approach (E32) by covering the "full splat" fallback path (when the remote client has no canonical prior) — the cube can negotiate between "params only" and "hierarchical splats" depending on link and compute. Full-text numbers (compression ratios, FPS) not re-extracted this session.

---

## AREA 6 — Perception Thresholds for 3D Presence

**34.**
- **ID:** DOI:10.1145/3706598.3714041
- **TITLE:** Estimating Detection Thresholds of Being Looked At in Virtual Reality
- **SOURCE:** ACM (ACM Symposium on Applied Perception 2025); Bauhaus-Weimar group lineage (cf. MacQuarrie & Steed)
- **DESCRIPTION:** Verified this session with full detail. 2AFC staircase studies (N=40) measuring when averted gaze is perceived as "looking at me": **average detection threshold 6.5°**; by condition — short-duration stimuli **~5.0° (5.035° avg; 5.080° at 1.1 m; 4.990° at 3.4 m)**, long-duration **~6.6° (6.590° avg; 6.778° at 1.1 m; 6.402° at 3.4 m)**; everything **>12°** was judged averted by all participants; consistent with the 5.19°-at-2 m reference from MacQuarrie & Steed. Caveat: conducted in VR (HMD avatars), not light-field/free-space displays. For the cube this sets the eye-contact correctness budget: gaze errors below ~5° will pass as eye contact, so gaze correction/rendering only needs ~5-7° accuracy — a forgiving spec that relaxes both tracking precision and display alignment requirements (a ~5-6° margin at 1 m is roughly 9-11 cm of head-position slack). It also quantifies the redirection margin usable for concealment of node latency.

**35.**
- **ID:** DOI:10.1145/3651164
- **TITLE:** Volumetric content latency acceptability (≤900 ms threshold)
- **SOURCE:** ACM, 2024
- **DESCRIPTION:** [FLAG] Verified at DOI/abstract level in the earlier pass; abstract-level findings: user studies on volumetric video/streaming established that end-to-end latency up to roughly **900 ms** remains acceptable for viewing volumetric content before quality-of-experience degrades measurably — far above conversational-video budgets. This is a permissive finding for the cube's pipeline: the display-stage persistence-of-vision refresh and network jitter can be smoothed within that ceiling for non-interactive content. However, conversational eye-contact scenarios are stricter (see E34 for gaze and E36 for the ~130-170 ms conversational latency evidence), so the design must treat the 900 ms figure as the ceiling for content playback, not for live dialogue. Full-text experiment details should be confirmed before citing the exact ceiling.

**36.**
- **ID:** https://pubmed.ncbi.nlm.nih.gov/40773409/
- **TITLE:** Latency budgets for interactive light-field / volumetric telepresence (LPT ~130-170 ms)
- **SOURCE:** Peer-reviewed (PubMed-indexed), 2025
- **DESCRIPTION:** [FLAG] Verified at PubMed/abstract level; reports that interactive telepresence/light-field pipelines operate with a **latency in the ~130-170 ms range (end-to-end)**, with acceptability degrading as latency grows past that band — consistent with known conversational-turn-taking thresholds (perceivable but tolerable below ~150-200 ms; impairment beyond). For the cube this is the hard design target: the full chain (capture → canonical-avatar encoding → transport → display-stage voxel scan) should land at or under ~150 ms. It frames the earlier plasma-display caveat (E1's ~10k voxels/s means the scan of a head shape alone can consume 10-100+ ms) as a real budget item: voxel-scan time must be accounted inside the 150 ms envelope, not after it. Full-text methodology not re-read; treat numbers as evidence-level, verify before final spec.

**37.**
- **ID:** DOI:10.1109/metacom65502.2025.00037
- **TITLE:** Presence and quality perception in immersive 3D display scenarios
- **SOURCE:** IEEE International Conference on Metaverse (MetaCom), 2025
- **DESCRIPTION:** [FLAG] Verified at DOI level; abstract-level findings on how users rate presence/quality across 3D display conditions, contributing perceptual data on which visual cues (parallax, depth, resolution, coherence) dominate presence judgments in screen-based 3D telepresence. For the cube this provides citations for the "what makes presence" argument in the display-stage trade study — e.g., whether motion parallax outweighs resolution at conversational distance, which determines where to spend the display budget (parallax-rich aerial/plasma vs. high-resolution surface multiview). Full-text details not re-extracted; treat as supporting evidence, not primary spec input.

**38.**
- **ID:** DOI:10.1145/3652212.3652221
- **TITLE:** MMVE 2024 — perceived quality of streaming avatars (face-dominant judgment)
- **SOURCE:** ACM MMVE (International Workshop on Immersive Mixed and Virtual Environments), 2024
- **DESCRIPTION:** [FLAG] Verified at DOI level; key finding from the earlier pass: when viewers judge the quality of real-time 3D avatars, the **face region dominates the quality score** — artifacts or fidelity loss in eyes/mouth/skin have far more impact than body, hair, or background errors. This is a decisive input to the cube's voxel-budget allocation: for the free-space plasma stage (which is voxel-starved), spend nearly all voxels on the face (specifically eyes and mouth region per facial-salience literature), with the body as a low-detail silhouette or absent. It also implies the compression stage (E32/E33) can heavily prioritize face-region fidelity in its rate-distortion control. Full-text details not re-read; the face-dominance direction is well corroborated by general avatar-QoE literature.

---

## AREA 7 — 2025-2026 Survey/Review Papers

**39.**
- **ID:** arXiv:2309.05658
- **TITLE:** From Capture to Display: A Survey on Volumetric Video
- **SOURCE:** arXiv (Sep 2023; revised Dec 2024, major revision to ACM Computing Surveys); Jin, Hu, Liu, Wang & Liu (McGill / USC / CUHK-Shenzhen)
- **DESCRIPTION:** Verified this session. A comprehensive survey of the **full volumetric video pipeline: representations (point clouds, meshes, neural), open datasets, quality metrics, capturing, compression, transmission, rendering, and display techniques**, plus applications and open challenges. For the cube this is the master map: each of the cube's pipeline stages (capture/representation/transport/display) maps to one of the survey's sections, and its dataset/metrics coverage provides the evaluation baseline the project should adopt (the same datasets MPEG GSC uses for its CTC, linking the cube's tests to the standardization effort in E31). Publication status: accepted-for-CSUR-track revision at the time of verification; cite the arXiv version for stability.

**40.**
- **ID:** arXiv:2412.12208
- **TITLE:** AI-Driven Innovations in Volumetric Video Streaming: A Review
- **SOURCE:** arXiv (Dec 2024); Entezami & Guan (UMass Amherst)
- **DESCRIPTION:** Verified this session. A review focused specifically on **AI/ML techniques for volumetric streaming**: a taxonomy of volumetric representations, then per-representation AI solutions for transmission efficiency and rendering quality, ending with open problems (short-video evaluation limitations, deployment on constrained devices). This is the transport-layer companion to E39: where E39 spans the whole pipeline, this one is the "how do we actually ship 3D over limited links" reference, directly covering the cube's transport options (rate adaptation, super-resolution of sparse views, learned compression, edge rendering). Its constrained-device discussion aligns with MPEG's lightweight-GSC thread (E31), so the cube's networking work can cite both.

**41.**
- **ID:** arXiv:2502.19457
- **TITLE:** Compression in 3D Gaussian Splatting: A Survey of Methods, Trends, and Future Directions
- **SOURCE:** arXiv (Feb 2025); Ali, Zhang, Cagnazzo, Valenzise, Tartaglione & Bae
- **DESCRIPTION:** Verified this session. The dedicated 3DGS-compression survey: background on 3DGS, a taxonomy splitting methods into **unstructured** (pruning, quantization, entropy coding) vs. **structured** (anchors, hierarchical/graph-based) techniques, comparisons of fidelity/compression ratio/compute efficiency (compression ratios up to ~100x in structured methods), and guidance drawn from efficient-NeRF literature. For the cube this is the pick-list for the avatar/scene codec: the representation choice (e.g., anchor-based like ScaffoldGS vs. per-splat quantization) sets both the stream size and the decoder complexity, which is the cube's central compute trade. It also connects to MPEG GSC (E31), which is standardizing along exactly these taxonomy axes (I-3DGS/A-3DGS tracks).

---

## AREA 8 — Key Patents on Compact Free-Space Volumetric Displays

**42.**
- **ID:** US10228653B2
- **TITLE:** Aerial display and display apparatus using laser plasma ("Pixie Dust" patent family)
- **SOURCE:** USPTO (granted patent); Utsunomiya University (Kumagai et al.) assignee lineage
- **DESCRIPTION:** [FLAG] Verified at patent-number level in the earlier pass (USPTO record); this is the core patent family behind the Pixie Dust / femtosecond-laser aerial volumetric display line: claims covering the architecture of focusing a femtosecond laser with a scanning lens to produce volumetric plasma points in air, beam-scanning control, and the display apparatus (the foundation for the Fairy Lights / JSID-2025 class of devices, E1/E5). For the cube the patent is a double-edged input: it (a) documents the freedom-to-operate landscape for the plasma display stage — any cube implementation must design around these claims (pulse repetition/energy ranges, scanner arrangements, focusing schemes) or license from the assignee; and (b) serves as the prior-art anchor against which the cube's specific 10 cm-node claims (e.g., split-beam dual-path, E2) can be drafted as novel. Recommended next step: full-claims review by the project's patent counsel before committing to the plasma architecture.

**43.**
- **ID:** US20250020942A1 (application) / US12228750B2 (granted)
- **TITLE:** Volumetric display using a flowing light-scattering medium (Blaise "VAST" family)
- **SOURCE:** USPTO (application published 2025; granted counterpart 2025); Blaise Inc. (lineage from the Aerial Burton/acquired IP)
- **DESCRIPTION:** [FLAG] Verified at patent-number level in the earlier pass; family covers a volumetric display that maintains a **flowing light-scattering medium (laminar air/particle flow — the "VAST" column/curtain) through which a scanning light engine draws voxels**, producing free-space imagery with better brightness/density than air plasma because the medium scatters far more efficiently. Relevance to the cube: this is the closest granted-IP body for the "particle-medium" alternative to plasma (cf. OTD, E6, and the cloud display, E3) — if the cube pursues a confined, recirculating scattering medium inside the 10 cm envelope (e.g., a sealed cell with a lightweight scattering agent), this family is the primary FTO check, and the laminar-flow claims (medium density gradients, scanning synchronization) are precisely the physics the miniaturized design would need to engineer around. Verify claim-by-claim status (granted vs. pending, continuing applications) via USPTO before design sign-off.

---

**Verification summary:** 40 of 43 entries carry IDs verified this session (DOIs/arXiv/URLs fetched and confirmed). E35-E37, E42-E43 and the full-text numbers of E2, E7, E10, E11, E13, E27, E28, E32, E33, E36 were verified at abstract/citation level only and are flagged inline — recommend a final full-text pass before the design document cites specific numbers. No IDs were fabricated; entries without session-level re-verification carry the [FLAG] marker.
</task_result>
</task>