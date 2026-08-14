# Real-Time Volumetric Human Capture & Rendering — SOTA, August 2026

> Research thread 1 of 6. ~45 web searches + ~90 direct source fetches (arXiv full HTML, GitHub repos + LICENSE files, vendor pages, MPEG/IETF trackers).
> Every number is attributed. "No published number found" means exactly that — no estimates were substituted.

---

## 0. The five things that matter

1. **Three architectures, ~3 orders of magnitude apart in bandwidth.**
   - (a) *Stream the volume* — point clouds / 4D Gaussians: **20–300 Mbps**
   - (b) *Reconstruct per-frame from sparse views, stream result* — Tele-Aloha class: **~100 Mbps**
   - (c) *Pre-build avatar offline, stream only driving parameters* — Apple Personas **0.7 Mbps measured**, Mon3tr **<0.2 Mbps**

   **Class (c) wins on every practical axis and is what every shipping product actually does.** Class (a) is what volumetric hackathon demos attempt, and it is the wrong choice.

2. **Exactly one production "true" volumetric telepresence system exists**: HP Dimension with Google Beam, **$24,999 + undisclosed license**, still limited-early-access ~9 months post-launch. Microsoft has fully exited. Meta has shipped nothing photorealistic; next headset slipped to 2027+.

3. **Gaussian splatting won the representation war** — confirmed in Apple Personas, Meta Codec Avatars, Evercoast, Canon's CES 2026 prototype, ~100% of 2026 academic work.

4. **Feed-forward (no per-person training) sparse-view reconstruction is real but not real-time at good resolution.** Best 2026 uncalibrated 4-view 2K method (HiReFF) runs **3.01 fps on an RTX 4090**. The real-time ones (GPS-Gaussian, 25 fps @ 2K) need calibrated, rigidly-mounted, hardware-synced cameras.

5. **Licensing is the most likely thing to kill a product built from this research.** INRIA 3DGS rasterizer is non-commercial. SMPL/SMPL-X are non-commercial *and forbid training networks for commercial use*. Meshcapade (sole commercial SMPL licensor) **was acquired by Epic Games and shut its platforms 18 April 2026**. Clean escapes appeared only Nov 2025 (Anny, Apache-2.0; Meta's MHR rig).

---

## 1. SOTA: photorealistic humans from 2–8 cameras

### 1.1 The four families

| Family | Needs | Time to first frame | Runtime cost | Examples |
|---|---|---|---|---|
| **A.** Per-subject optimized avatar | Monocular or dense rig; minutes→days training | Minutes to 2 days | Cheap (50–500 fps) | Animatable Gaussians, 3DGS-Avatar, GauHuman, ExAvatar |
| **B.** Feed-forward generalizable, per-frame novel view | 2–8 calibrated views, no training | 0 | Expensive per frame | GPS-Gaussian(+), EVA-Gaussian, HiReFF |
| **C.** Feed-forward animatable avatar (one pass → riggable) | 1 image to 4 views | <1 s to seconds | Cheap after | LAM, LIFe-GoM, HumanGS, FiCA, LCA |
| **D.** Parametric avatar + parameter streaming | Offline enrollment, monocular driving | 33 s–1 h enrollment | Very cheap | Mon3tr, Apple Personas, Meta Codec Avatars |

**For 2–8 cameras: family B is the cool demo, family C/D is what actually works in a call.**

### 1.2 Family A — per-subject optimized (quality ceiling, worst ergonomics)

| Method | Venue | Input | Train | Render | License | Notes |
|---|---|---|---|---|---|---|
| GauHuman | CVPR 2024 · [2312.02973](https://arxiv.org/abs/2312.02973) | ZJU-MoCap | **1–2 min** | **up to 189 fps** | see repo | ~13k Gaussians |
| 3DGS-Avatar | CVPR 2024 · [2312.09228](https://arxiv.org/abs/2312.09228) · [repo](https://github.com/mikeqzy/3dgs-avatar-release) | monocular | **~30 min** | **50+ fps** | **MIT** + SMPL dep | 400× faster train vs prior SOTA |
| GaussianAvatar | CVPR 2024 · [repo](https://github.com/huliangxiao/GaussianAvatar) | monocular | not published | not published | **MIT** + SMPL/SMPL-X | needs INRIA rasterizer |
| Animatable Gaussians | CVPR 2024 · [2311.16096](https://arxiv.org/html/2311.16096v3) | **16–47 views** | **~2 days on RTX 4090** | **10 fps** @1024² | **Tsinghua NON-COMMERCIAL** | Highest fidelity; brutal cost |
| ExAvatar | ECCV 2024 · [2407.21686](https://arxiv.org/abs/2407.21686) | short monocular | not published | not published | **MIT** + SMPL-X (non-comm) | Whole body + face + hands |
| SplattingAvatar | CVPR 2024 | — | — | **>300 fps desktop / 30 fps mobile** | — | Gaussians on triangle mesh |

> **Reality check:** Animatable Gaussians needs 16–47 cameras and two days of RTX 4090 time for *one* avatar, rendering at 10 fps. It is the method people screenshot. It is not deployable.

### 1.3 Family B — feed-forward per-frame from sparse views

Closest match to "2–8 cameras → photorealistic body, no per-person training."

| Method | Venue | Views | Res | Speed | Hardware | License |
|---|---|---|---|---|---|---|
| GPS-Gaussian | CVPR 2024 Highlight | sparse stereo pairs | **2K** | **25 fps** | **single RTX 3090** | — |
| GPS-Gaussian+ | T-PAMI 2025 · [2411.11363](https://arxiv.org/abs/2411.11363) · [repo](https://github.com/YaourtB/GPS_plus) | 2 adjacent | high-res | no explicit fps published | — | **MIT repo, requires INRIA rasterizer (non-comm)** |
| EVA-Gaussian | [2410.01425](https://arxiv.org/abs/2410.01425) | sparse multi-view | high-res | "real-time", no fps | — | — |
| **HiReFF** | Jun 2026 · [2606.29333](https://arxiv.org/html/2606.29333v1) | **4 views, 90° apart, UNCALIBRATED** | **2K (2072²), 360°** | **3.01 fps** | **RTX 4090** | release not stated |

Baselines beaten by GPS-Gaussian: FloRen 15 fps, ENeRF 5 fps.
HiReFF quality: PSNR **26.51** (vs AnySplat 25.59), SSIM 0.9164, LPIPS 0.1277.

> **The trade-off, plainly:** GPS-Gaussian gets 25 fps because cameras are calibrated and fixed. HiReFF removes calibration and drops to 3 fps. **You do not get both in 2026.**

### 1.4 Family C — feed-forward animatable avatar (the 2025–26 frontier)

| Method | Date | Input | Build | Render | License |
|---|---|---|---|---|---|
| **LAM** | SIGGRAPH 2025 · [2502.17796](https://arxiv.org/abs/2502.17796) · [repo](https://github.com/aigc3d/LAM) | **1 image** (head) | **1.4 s on A100** | **562.9 fps A100 / 110+ fps Xiaomi 14** | **Apache-2.0** ← best-licensed serious option |
| LIFe-GoM | ICLR 2025 · [2502.09617](https://arxiv.org/abs/2502.09617) | sparse views | **<1 s** | **95.1 fps @1024²** | — |
| HumanGS | Apr 2026 · [2604.10259](https://arxiv.org/abs/2604.10259) | multi-view + SMPL-X | >15× faster than transformer baselines | real-time | not stated |
| FiCA (Meta) | Jun 2026 · [2606.24232](https://arxiv.org/abs/2606.24232) | **1 portrait** | **<5 s** | "real-time" | not stated |
| Instant Expressive Gaussian Head Avatars (NVIDIA) | Dec 2025 · [2512.16893](https://arxiv.org/abs/2512.16893) | 1 image | feed-forward | **107.31 fps** | CC-BY-4.0 paper |
| AGORA | [2512.06438](https://arxiv.org/abs/2512.06438) | — | — | **560 fps GPU / 60 fps mobile** | — |
| One-Shot 360° UV-Gaussian | ECCV 2026 · [2601.12770](https://arxiv.org/abs/2601.12770) | 1 image | feed-forward | **246 fps** | — |
| **LCA (Meta)** | CVPR 2026 · [2604.02320](https://arxiv.org/abs/2604.02320) | **phone capture at test time** | — | **no numbers published** | undisclosed |

> **LCA is the most important 2026 result for this problem.** Meta pretrained on **1M in-the-wild videos**, then post-trained on studio multi-view, producing full-body avatars with **finger-level articulation** from unconstrained phone capture — with *emergent* relightability and loose-garment support. It collapses the "you need a 100-camera dome" requirement. Meta publishes **no inference numbers and no release.**

### 1.5 On-device / mobile rendering (genuinely solved)

| Method | fps | Device |
|---|---|---|
| HRM²Avatar (Alibaba, SIGGRAPH Asia 2025) · [2510.13587](https://arxiv.org/abs/2510.13587) | **120 fps mobile / 90 fps standalone VR** | phones, HMDs |
| TaoAvatar (Alibaba, CVPR 2025) · [2503.17032](https://arxiv.org/abs/2503.17032) | **90 fps** | Apple Vision Pro |
| SqueezeMe (Meta, SIGGRAPH 2025) · [2412.15171](https://arxiv.org/abs/2412.15171) | **72 fps for 3 full-body avatars** | Quest 3 |
| Pruned Local Blendshapes (CVPR 2026) · [2605.01854](https://arxiv.org/abs/2605.01854) | **120 fps @2K** | mobile, **WebGPU** |
| LAM | **110+ fps** | Xiaomi 14 |

> Meta's caveat on SqueezeMe: source avatars still come from a **100+ camera rig**, and mobile versions have **flat lighting, no dynamic relighting**.

### 1.6 End-to-end systems with real latency numbers

| System | Cameras | Res/fps | Latency | Bandwidth | GPU |
|---|---|---|---|---|---|
| **Tele-Aloha** (SIGGRAPH 2024) · [2405.14866](https://arxiv.org/html/2405.14866v1) | **4× FLIR BFS-U3-123S6C-C, 4096×3000, 30 Hz global shutter** (two stereo pairs) | 2048² @ 30 fps | **<150 ms same-LAN**; compute **23.5 ms** (disparity 4.7 / encode 6.1 / decode+refine 9.3 / blend 1.4 / **3DGS raster 1.0**) | **100 Mbit/s** | **1× RTX 4090** |
| **Mon3tr** (HKUST, Jan 2026) · [2601.07518](https://arxiv.org/html/2601.07518) | **1 webcam (<$20)** online; 32× 12MP offline enrollment | ~60 fps Quest 3, >124 fps PC | **~80 ms e2e** | **<0.2 Mbps** (>1000× less than point cloud) | RTX 5090 D sender |
| GS-SCNet (Apr 2026) · [2604.25330](https://arxiv.org/html/2604.25330v1) | **2 (stereo)** | 19.2 fps | encode 52 ms + decode 31 ms | −75.18% BD-Rate vs MV-HEVC+GPS-Gaussian | A100 |
| LentiAvatar (Jun 2026) · [2606.10550](https://arxiv.org/abs/2606.10550) | monocular | 10.65 fps live / 38.49 distilled | — | — | not published |
| **CaptureStudio** (CVMP 2025) · [repo](https://github.com/irc-hslu/capturestudio) | arbitrary RGB-D (Orbbec) | 5–10 fps live preview | — | — | distributed |

Tele-Aloha: system cost ~$15,000. PSNR 26.54 / SSIM 0.928 / LPIPS 0.095. **No code release found.**
Mon3tr: enrollment 1–2 min capture → **~33 s** reconstruct. PSNR 32.4 train / >28 novel pose. VRAM 3.9 GB (vs MonoPort 11.2 GB). Streams **SMPL/FLAME/MANO params over WebRTC**. **Code not stated as public.**
CaptureStudio outputs **PLY, MPEG V-PCC, SPLAT** — open source, rare and useful.

---

## 2. Production systems

### 2.1 Google Beam (ex-Project Starline)

- **Product:** HP Dimension with Google Beam, announced InfoComm 11 Jun 2025. **MSRP $24,999; Beam license sold separately, price undisclosed.**
- **Availability:** select enterprise from late 2025 (US/CA/UK/FR/DE/JP). As of May 2026 update, **still "limited early access."** No GA. HP's page is a demo-request form with no price.
- **Display:** **65-inch 8K light-field (autostereoscopic)**.
- **Cameras: UNRESOLVED CONFLICT.** Google/9to5Google/pocket-lint say **six**; HP's own page and SVC Online say **seven**. HP's spec PDF fails TLS and is unfetchable.
- Beam generation is **RGB-camera-only + AI** — no dedicated depth sensor mentioned, unlike original Starline.
- **Audio:** 12-mic beamforming array, 4 speakers, spatial audio. Adaptive LED lighting for skin-tone correction.
- **Model:** "state-of-the-art AI volumetric video model." **No model name, params, architecture, or inference hardware published.** No Beam-era paper.
- **Bandwidth/latency: NO PUBLIC NUMBER FOR BEAM.** Only figures are from the **2021 Starline research prototype**: **30–100 Mbps**, **105.8 ms average e2e**, ~100× compression from multi-Gbps raw, **4 GPUs per endpoint** (2× Quadro RTX 6000 + 2× Titan RTX), 65" 8K, **33.1 M full-color px at 60 Hz** ([paper](https://hhoppe.com/starline.pdf)). **Beam is a different, cheaper architecture — do not assume these carry over.**
- **Interop:** 3D one-to-one on Google Meet and Zoom only; **2D-only** with Teams and Webex.
- **Customers:** Deloitte, Salesforce, Citadel, NEC, Duolingo, Recruit, Bain, Hackensack Meridian Health, Huntington Bank, Schwarz Digits, USO pilot.
- **Google I/O 2026 (20 May): 3D group meetings.** Claimed +50% sense of social connection, +21% ability to contribute. **No sample size, methodology, or CIs published.** Google labels it "a new experiment."
- **Beam does not appear in Google's own "100 things we announced at I/O 2026" post.** A hands-on at HP Imagine 2026 notes "video quality itself still has room to improve."
- All Google efficacy stats (39% more non-verbals, 37% more turn-taking, 28% recall, 14% focus) are internal research, no published methodology.

### 2.2 Meta Codec Avatars

**As of August 2026, Meta has shipped zero photorealistic Codec Avatars to consumers.** Consumer Meta Avatars remain stylized cartoons. There is **no official "Codec Avatars 1/2/3/4" numbering** — community shorthand mapped onto papers.

**Hard blocker: sensors.** Quest 3/3S have **no eye tracking, no face tracking**; Quest Pro discontinued. Dec 2025 reporting: Meta **cancelled Pismo Low/High** (2026 Quest 4 candidates); **Quest 4 now H2 2027+**, Orion-class AR glasses **not before 2028**. **No Meta MR headset launches in 2026.**

Research trail:
- Quest 2-era decoder: 1 avatar @ 72 fps, 3 @ ~63, 5 @ ~43
- Relightable Gaussian Codec Avatars (CVPR 2024) · [2312.03704](https://arxiv.org/abs/2312.03704) — sub-mm detail, hair strands, pores
- URAvatar (SIGGRAPH Asia 2024) — relightable head from **phone scan under unknown illumination**
- Relightable Full-Body GCA (Jan 2025) · [2501.14726](https://arxiv.org/abs/2501.14726)
- SqueezeMe (SIGGRAPH 2025) — 3 avatars @ 72 fps Quest 3
- HairCUP (Jul 2025) — head/hair decomposition
- Gaussian Pixel Codec Avatars (Dec 2025) · [2512.15711](https://arxiv.org/abs/2512.15711)
- **Audio Driven Real-Time Facial Animation** (SIGGRAPH Asia 2025) · [2510.01176](https://arxiv.org/abs/2510.01176) — **<15 ms GPU time**, single-step distilled diffusion, **100–1000× faster** than offline baselines. *This is the plausible path to shipping on trackerless Quest 3: drive the face from the microphone.*
- FiCA (Jun 2026) — single portrait → codec avatar in **<5 s**
- LCA (CVPR 2026) — 1M-video pretraining, phone-conditioned full body

Compute: phone-scan → head avatar is **~1 hour of server GPU**; highest-quality relightable still needs desktop GPUs.

### 2.3 Apple Personas / Spatial Personas

- **Enrollment:** Vision Pro's front sensor array — **eight external cameras** incl. color, near-IR, **TrueDepth**, **LiDAR**. Apple doesn't publish which subset.
- **On-device, confirmed.** Apple: Personas "are still created on device in a matter of seconds." Hands-on: **under 10 seconds on M5**.
- **Gaussian splatting: CONFIRMED, not rumored.** Apple's Scott Norris told CNET Persona tech **uses Gaussian splatting**. Apple also ships **SHARP** (photo → 3DGS in seconds).
- **visionOS 26** (15 Sep 2025) was the big quality jump — full side-profile, accurate hair/lashes/complexion, face+body scanned together, 1,000+ eyeglass variations.
- **visionOS 27** (WWDC Jun 2026): no announced Persona/FaceTime changes, but **RealityKit gains native Gaussian-splat rendering**.
- **The only rigorously measured public numbers in this entire landscape** — *A First Look at Immersive Telepresence on Apple Vision Pro* · [2405.10422](https://arxiv.org/html/2405.10422v2) (measured on visionOS 1.x, treat as lower bound):
  - **FaceTime Spatial Persona: ~0.7 Mbps mean throughput** (lowest of all apps tested). 2D Persona ~2 Mbps; Zoom ~1.5; Webex >4
  - Render target **90 fps → 11.1 ms per-frame deadline**. GPU frame time **5.65 ± 0.69 ms** (2 users) → **7.62 ± 1.29 ms** (5 users)
  - Spatial Persona mesh **78,030 triangles** at 0.5 m; viewport adaptation + foveation → **21,036 triangles, −39% GPU time**
  - **Visibility optimizations do not reduce bandwidth**
  - Network RTT **>80 ms** US coast-to-coast
- **Hardware:** M5 Vision Pro launched 22 Oct 2025 at $3,499, **raised to $3,699 Jun 2026**. Apr 2026 report says Apple **shelved further Vision Pro development after M5 underperformed**, redirecting to smart glasses (reporting, not Apple-confirmed).

> **The architectural lesson: Apple does spatial telepresence at ~0.7 Mbps — 40–140× less than the Starline prototype — because the avatar is a parametrically-driven on-device model, not a transmitted volumetric stream.**

### 2.4 Microsoft — comprehensively exited

- Holoportation (MSR 2016) never became a product
- Mixed Reality Capture Studios: SF studio had **106 cameras, 10 GB/s**. Microsoft **laid off the MRCS team January 2023** with no notice to partner studios, transferred stage tech to Arcturus 17 Aug 2023
- Mesh Toolkit retired 24 Jun 2025; Mesh apps and **Teams Immersive Space (3D) retired 1 Dec 2025**. Replacement caps at **16 participants** vs Mesh's 330
- HoloLens hardware discontinued; HoloLens 2 support ends **31 Dec 2027**. **Windows Mixed Reality support ends 1 Nov 2026**

**Verdict: dead.**

### 2.5 Asia

**No Asian production volumetric telepresence product with published specs comparable to Beam was found.**

- **Canon** — volumetric studio in Kawasaki as a *service* (no specs/pricing). At **CES 2026** demoed a **prototype portable volumetric + mocap rig using Gaussian splatting**. Prototype only.
- **NTT "Another Me"** — **not volumetric telepresence**; AI digital-alter-ego research, no commercial launch
- **NEC** — appears only as a Beam *customer*
- **SK Telecom Jump Studio** — Asia's first MRCS licensee, **106 cameras**, since Apr 2020. Post-Microsoft-exit status **unconfirmed for 2025–26**
- **Samsung Display** showed a glasses-free light field *panel* at AWE USA — a panel, not a system
- **China: no credible primary source found** for a ByteDance/Tencent/Alibaba/Huawei production system. *However*, Alibaba is the strongest player in **mobile Gaussian avatars** academically (TaoAvatar, HRM²Avatar, LAM/aigc3d)

### 2.6 Startups — alive/dead ledger

| Company | Truly volumetric? | Status Aug 2026 | Funding | Price |
|---|---|---|---|---|
| **Matsuko** (SK) | Yes — single phone camera → hologram | **Alive**, pivoted to holographic training + AI | not public | not disclosed |
| **Proto Hologram** (US) | Partly — 2D-ish holographic box | **Alive**, flagship Proto Luma 86" | ~**$25M** / 5 rounds | quote-only; earlier **$29k–$65k** |
| **ARHT Media** (CA) | Display/streaming | **DEAD** — filed under Canada's BIA **4 Oct 2024** | — | — |
| **Holoconnects** (NL) | **No** — 2D-in-a-box | Alive, **unfunded** | — | **€4,500** (22" Mini) → **€29,500–30,000** (86"); wall from **€60,000** |
| **Looking Glass** (US) | Display only | Alive, won **SID 2026 Display of the Year** | **$30.1M** | **musubi $149** (Jul 2026); **HLD 16"/27" $2,000–$4,000**; **HLD 86" $20,000** |
| **Light Field Lab** (US) | SolidLight display | **Alive, nothing shipped commercially**; still "pilot production line" | **$50M B + $28M A** | **no price published** |
| **Brelyon** (US) | **No** — monocular depth monitor | Alive, shipping; CES 2026 Ultra Reality Mini | **$16.6M** | no absolute price |
| **Swave Photonics** (BE) | Holographic SLM **chip** | Alive; CES 2026 Innovation Award (HXR Onyx) | **€27M A + €6M** | component |
| **Arcturus** (US) | Yes — inherited MS MRCS tech | Alive | not public | not public |
| **Evercoast** (US) | Yes — **4D Gaussian splatting** | Alive, repositioned to physical-AI; **acquired Depthkit Jun 2024** | not public | not public |
| **Volograms** (IE) | Yes — phone→volumetric | Alive | €1.5M seed | not public |
| **8i** (NZ/US) | Yes | **Likely moribund** — site says "© 2023" | — | — |
| **Metastage** (US) | Yes — MRCS-derived | Alive, independent | — | project-based |

Matsuko's "75% retention vs 10% for lectures" claim is a rehash of the discredited learning pyramid — **unverified marketing.**

---

## 3. Codecs and transport

### 3.1 MPEG standards status (Aug 2026)

| Standard | ISO/IEC | Status |
|---|---|---|
| V3C + V-PCC | 23090-5 | Published IS (2021, 2023 2nd ed) |
| G-PCC | 23090-9 | Published IS (2023) |
| MIV | 23090-12 | Published; TMIV 15.1.1 |
| V-DMC (dynamic mesh) | 23090-29 | In development |
| L3C2 (low-latency LiDAR) | 23090-30 | FDIS at MPEG 151 |
| E-G-PCC (temporal prediction) | 23090-38 | Finalization targeted early 2026 |

**Gaussian Splat Coding (GSC) — real, active, years away.** Two tracks: V-PCC path at **CDAM (MPEG 153)**, G-PCC path at **Working Draft**. MPEG 155 (Geneva 2026) approved **29 use cases** incl. dynamic splat tracks over HTTP adaptive streaming. **Call for dynamic test material: WG 5 N 422, deadline 15 October 2026** — format **I-3DGS** (per-frame INRIA-format, **constant point count and ordering across frames**, 25–30 fps, ≥5 s, 1–100 M splats, COLMAP calibration mandatory). **A coding CfP is only "being prepared" — no published date, no target IS date.**

MPEG's own consensus: *"single-frame compression is essentially solved"* — the work is temporal.

> **Practical implication: anything shipping before ~2029 must use a proprietary or de-facto format.**

**Encoders:** MPEG reference codecs (`mpeg-pcc-tmc2`, `tmc13`) are **not real-time**. The only claimed real-time V-PCC encoder is **KDDI Research's** (2022): ~400× faster than reference, ≥30 fps, ~0.8M pts/frame, pure software — hardware and latency undisclosed.

> **V-PCC's structural advantage:** geometry/attribute/occupancy planes are ordinary HEVC/VVC video, so hardware decoders apply. **G-PCC has no hardware decoder.**

### 3.2 Gaussian splat compression

**Static** — from [2502.19457](https://arxiv.org/html/2502.19457v1); 3DGS-30k baseline = **734 MB** on Mip-NeRF360:

| Method | Size | PSNR | Ratio |
|---|---|---|---|
| Scaffold-GS | 102 MB | 28.84 | 7× |
| LightGaussian | 42 MB | 27.28 | 18× |
| **c3dgs** (CVPR'24) | **28.8 MB** | 26.98 | **26–31×**, +**up to 4× render fps**, **MIT** · [repo](https://github.com/KeKsBoTer/c3dgs) |
| RDO-Gaussian | 23.5 MB | 27.05 | 31× |
| HAC-lowrate | 15.3 MB | 27.53 | 48× |
| ContextGS-lowrate | 12.7 MB | 27.62 | 58× |

Most aggressive configs reach **83–113×**. HAC++ (TPAMI 2025) claims **>100× vs vanilla**; no fps published.

**SOG / `.sog` — the de-facto transport format.** Maps Gaussian attributes into 2D images sorted by spatial locality (PLAS sort), compressed with **WebP**. Spec at v2.
- **~15–20× smaller than PLY**, 2–3× better than "compressed PLY"
- Real scenes: 4M-splat church **1 GB → 55 MB**; 4M-Gaussian skate park **1 GB → 42 MB (~95%)**
- Open-sourced 17 Sep 2025; Morton-ordered, GPU-ready, no load-time processing; compressor moved CUDA→**WebGPU**
- ⚠️ **Tooling caveat:** [playcanvas/sogs](https://github.com/playcanvas/sogs) is **archived** — use **[playcanvas/splat-transform](https://github.com/playcanvas/splat-transform)**. SOG spec license not stated.

**Dynamic / 4D:**

| Method | Train/frame | Size/frame | Render | Implied bitrate @30fps |
|---|---|---|---|---|
| 3DGStream (CVPR'24 HL) | ~12 s | 8,294 KB | 200–215 fps | ~2 Gbps |
| QUEEN (NeurIPS'24) | **<5 s** | ~0.7 MB | **350 fps** | **~168 Mbps** |
| 4DGC | — | 511 KB / 430 KB | 168–213 fps | ~123 Mbps |
| **4D-MoDe** (Sep 2025) | **0.68 min** | **93.5 KB** @31.56 dB; **71.7 KB** @28.01; **"as low as 11.4 KB"** foreground-only | 172–210 fps | **~22 / ~17 / ~2.7 Mbps** |
| 4DGCPro (Sep 2025) | 4.3 min | 1.31 MB @29.47 dB → 0.33 MB @27.69 | iPhone A15 34–43 ms | **79–314 Mbps** |
| ComGS (NeurIPS'25) | — | **159× < 3DGStream, 14× < QUEEN** | competitive | ~12 Mbps equiv |
| **V3** · [2409.13648](https://arxiv.org/abs/2409.13648) | — | — | — | **Compresses attributes as 2D video → hardware codecs apply. Architecturally the most shippable.** |

> ⚠️ **Critical caveat:** 4D-MoDe's 0.68 min/frame and 4DGCPro's 4.3 min/frame are **offline per-frame optimization**. These are not live encoders. **Nobody has published a real-time 4DGS encoder.**

### 3.3 Bitrate for a talking human — the honest answer

**No published apples-to-apples measurement of a talking human at good quality, volumetric vs 2D, exists.** Anchors:

- **Raw:** 8i Voxelized Full Bodies — 42 cameras, 30 fps, 1024³, ~800k–1M pts/frame ≈ **1.0 Gbps uncompressed**
- **V-PCC on that:** KDDI reports 1/40 reduction → **~25 Mbps**
- **Research V-PCC operating points:** 0.01502–0.01866 bpp → **~0.45–0.56 Mbps** at 1M pts × 30 fps — but that's the visibly-degraded end of the RD curve
- **MIV (6DoF multi-view+depth):** **~15–30 Mbps** at HEVC Level 5.2
- **4DGS:** QUEEN **168 Mbps**; 4D-MoDe foreground-only **~2.7 Mbps** (best case, not validated on conversational capture)
- **2D reference:** 1080p30 talking head ~1–3 Mbps *(industry common knowledge, not sourced to a citable measurement)*
- **Parametric avatar:** Apple Spatial Persona **0.7 Mbps measured**; Mon3tr **<0.2 Mbps**

> **Bottom line: volumetric human at good quality is ~10–25 Mbps (V-PCC/MIV class) vs ~1–3 Mbps for 2D — about 10×. Parametric avatars are ~0.2–0.7 Mbps, i.e. cheaper than 2D video.**

### 3.4 Latency budgets

| Budget | Value | Source |
|---|---|---|
| Mouth-to-ear one-way, "essentially transparent" | **≤150 ms** | ITU-T G.114 |
| One-way, unacceptable | **>400 ms** | ITU-T G.114 |
| VR motion-to-photon | **<15–20 ms** | [MTP consensus](https://arxiv.org/pdf/1801.07587) |
| VR conferencing fluency | degrades 100→1500 ms; **sharp drop at 300 ms under cognitive load** | [2603.09261](https://arxiv.org/pdf/2603.09261) (2026, most recent empirical study) |
| Interactive telepresence target in 2026 lit | **<100 ms e2e** | Mon3tr et al |

> **These are two different clocks.** MTP (<20 ms) is satisfied *locally* by reprojecting an already-received frame. The 150 ms G.114 budget governs the remote path: capture → matting → reconstruct/encode → network → decode → render. Tele-Aloha's 23.5 ms of compute fits inside a <150 ms **LAN** budget — add WAN RTT (Apple measured **>80 ms US coast-to-coast**) and headroom vanishes.

### 3.5 Transport

- **WebRTC remains the only shipping option for <150 ms conversational media.** Mon3tr uses it.
- **ReVo** · [2604.27441](https://arxiv.org/abs/2604.27441) (Apr 2026) — cross-layer volumetric videoconferencing on WebRTC, modality-aware RGB/depth separation, network-layer FEC on critical content, post-decode neural reconstruction: **up to +32% SSIM (RGB), +13% (depth), −95.7% video freezes**. No Mbps/fps published.
- **Media over QUIC (MoQT):** `draft-ietf-moq-transport-19`, **6 July 2026, still pre-RFC**. Cloudflare relays in 330+ cities; claims **"sub-second"** — a *broadcast* target, ~5× above the conversational budget. **Use MoQ for one-to-many volumetric replay, not for calls.**

---

## 4. Segmentation, matting, and 3D tracking

### 4.1 Matting

- **RobustVideoMatting** — still the throughput champion: **RTX 3090 FP16 — 172 fps HD / 154 fps 4K**; 2060 Super 134/108; GTX 1080 Ti FP32 104/74. Exports TorchScript/ONNX/TF.js/CoreML. **License: GPL-3.0 — hard blocker for closed source.** No successor from the same authors.
- **MatAnyone** (CVPR 2025) / **MatAnyone 2** (CVPR 2026 Highlight) · [2512.11782](https://arxiv.org/abs/2512.11782) — current SOTA line. Both **NTU S-Lab License 1.0 (non-commercial)**. **Neither publishes an fps number.** Both need a first-frame mask.
- **BiRefNet** — best-licensed high-quality option: **MIT**, **17 fps @1024² FP16, 3.45 GB VRAM, RTX 4090**; DIS5K S=0.911. Variants for 2K/HR/matting. 2025–26: SDPA attention; `refine_foreground` accelerated **8× to ~80 ms on RTX 5090**.
- **MODNet** — **Apache-2.0**, trimap-free, "real-time up to 2K", 7 MB demo model, **no fps table**.
- **SAM 3 → SAM 3.1.** SAM 3 released 19 Nov 2025 (848M params); SAM 3.1 on 27 Mar 2026. **~30 ms/image with >100 objects on H200**; SAM 3.1 hits **32 fps on a single H100** (2× SAM 3). Object Multiplex tracks up to 16 objects/forward pass. **License: custom SAM License.** ⚠️ **SAM 3 is detection/tracking, not matting — no alpha.** Pair with BiRefNet-matting or MatAnyone 2.

### 4.2 3D body / hand / face tracking

**The 2026 headline: SAM 3D Body** · [2602.15989](https://arxiv.org/abs/2602.15989) (CVPR 2026) · [repo](https://github.com/facebookresearch/sam-3d-body) — promptable single-image full-body HMR accepting 2D-keypoint and mask prompts. Introduces **MHR (Momentum Human Rig)**, decoupling skeleton from surface shape — **a Meta-authored SMPL-X replacement free of Max Planck's non-commercial license.** 3DPW 54.8 MPJPE, EMDB 61.7, RICH 60.3 PVE. **No fps published.**
**Fast SAM 3D Body** · [2603.15603](https://arxiv.org/abs/2603.15603) reports **up to 10.9× e2e speedup**, SMPL conversion **>10,000×** — but **no absolute fps, GPU, or code availability stated.**

| Model | fps / latency | Hardware | License |
|---|---|---|---|
| Multi-HMR (ECCV'24, NAVER) | ViT-S **29 ms (~34 fps)** / ViT-B 43 / ViT-L 74 @672² | **V100-32GB** | Custom NAVER |
| SMPLest-X (TPAMI'25) | **8.36 fps** (third-party) | Huge ckpt **8.2 GB** | **MIT** code |
| NLF (NeurIPS'24) | no fps published | — | **MIT code, NON-COMMERCIAL weights** ← easy trap |
| HMR2.0 / 4D-Humans | no fps published | 8×A100 training | MIT + **SMPL non-comm** |
| MediaPipe Pose Landmarker | **per-device latency removed from current docs** | CPU/GPU/mobile | Apache-2.0 |
| MediaPipe Holistic (legacy) | **0.89 fps CPU / 3.15 fps GPU** in a 2026 sign-language pipeline benchmark · [2604.24609](https://arxiv.org/pdf/2604.24609) — *pipeline-level, not model-level; treat with caution* | — | Apache-2.0 |
| WiLoR (hands) | **>130 fps (medium), 175 fps (small)** | CUDA 11.7 | **CC-BY-NC-ND + AGPL + MANO — triple encumbrance** |
| Video Depth Anything | **Small 7.5 ms / 6.8 GB; Large 14 ms / 23.6 GB** A100 FP16 | A100 | **Small Apache-2.0; Base/Large CC-BY-NC-4.0**. Streaming mode degrades ScanNet δ1 0.926 → 0.836 |

> **Two clean license escapes appeared within weeks of each other in Nov 2025:**
> - **Anny** (NAVER Labs Europe, 6 Nov 2025) · [repo](https://github.com/naver/anny) — **Apache-2.0**, no registration, no gated download. Parametric human built from anthropometric + WHO calibration data (**no 3D scans → no biometric-privacy exposure**), positioned as a **drop-in SMPL-X replacement for HMR**. Ships Anny-One (800k+ synthetic images).
> - **MHR** (Meta) — permissive rig under SAM 3D Body.

---

## 5. Component table — the commercially-safe stack

| Component | Repo | License | Hardware | Speed |
|---|---|---|---|---|
| **gsplat** | [nerfstudio-project/gsplat](https://github.com/nerfstudio-project/gsplat) | **Apache-2.0** | CUDA only | **4× less VRAM, 15% less time** than INRIA, identical PSNR |
| INRIA 3DGS | [graphdeco-inria/gaussian-splatting](https://github.com/graphdeco-inria/gaussian-splatting) | **NON-COMMERCIAL** | CUDA | baseline — **most human-avatar repos depend on this even when they say MIT** |
| **Brush** | [ArthurBrussee/brush](https://github.com/ArthurBrussee/brush) | **Apache-2.0** | **WebGPU — no CUDA**, runs macOS/Win/Linux/Android/browser, AMD/Intel/NVIDIA | "generally faster than gsplat" |
| SuperSplat | [playcanvas/supersplat](https://github.com/playcanvas/supersplat) | **MIT** | Browser | — |
| c3dgs | [KeKsBoTer/c3dgs](https://github.com/KeKsBoTer/c3dgs) | **MIT** | CUDA 12 | 31× compression, **up to 4× render fps** |
| **LAM** | [aigc3d/LAM](https://github.com/aigc3d/LAM) | **Apache-2.0** | A100 → phones | **1.4 s build; 562.9 fps A100 / 110+ fps Xiaomi 14** |
| GPS-Gaussian+ | [YaourtB/GPS_plus](https://github.com/YaourtB/GPS_plus) | **MIT repo, requires INRIA rasterizer** | CUDA | 25 fps @2K (v1) |
| CaptureStudio | [irc-hslu/capturestudio](https://github.com/irc-hslu/capturestudio) | LICENSE present, type unconfirmed | multi-Orbbec RGB-D | 5–10 fps preview; outputs **PLY/V-PCC/SPLAT** |
| **BiRefNet** | [ZhengPeng7/BiRefNet](https://github.com/ZhengPeng7/BiRefNet) | **MIT** | RTX 4090 FP16, 3.45 GB | **17 fps @1024²** |
| RobustVideoMatting | [PeterL1n/RobustVideoMatting](https://github.com/PeterL1n/RobustVideoMatting) | **GPL-3.0** | RTX 3090 FP16 | **172 fps HD** |
| MODNet | [ZHKKKe/MODNet](https://github.com/ZHKKKe/MODNet) | **Apache-2.0** | PC/mobile | "real-time up to 2K" |
| SAM 3D Body | [facebookresearch/sam-3d-body](https://github.com/facebookresearch/sam-3d-body) | **SAM License** | — | **MHR rig — SMPL-X-free** |
| **Anny** | [naver/anny](https://github.com/naver/anny) | **Apache-2.0** | — | **SMPL-X replacement, commercially usable** |
| Orbbec Femto Bolt (HW) | [orbbec.com](https://www.orbbec.com/products/tof-camera/femto-bolt/) | — | — | depth 1024²@15 / 640×576@30; RGB 4K@30; **8-pin daisy-chain sync**. The Azure Kinect successor |

---

## 6. What is genuinely hard

### The seven things that kill volumetric telepresence projects

**1. Calibration and synchronization eat your first two days.**
The 25 fps GPS-Gaussian number assumes *calibrated, rigidly mounted, hardware-synchronized* cameras. Remove calibration and 2026's best method drops to **3.01 fps on an RTX 4090**. Webcams have no sync pin, rolling shutter, and independent auto-exposure/auto-white-balance — three things that will actively fight you. Tele-Aloha used **global-shutter FLIR machine-vision cameras** for a reason. Femto Bolt's 8-pin daisy chain is the cheap path to sync; consumer webcams are not.

**2. Hands and faces are where photorealism dies, and they're the whole point.**
Every method reports body-level PSNR. The information a conversation carries is in micro-expressions, gaze, and finger articulation — exactly the regions with the fewest pixels and fastest motion. Meta needed a *separate research line* for each (HairCUP for hair, Relightable Full-Body for hands+face, LCA for fingers) and a 100+ camera dome. **A 4-camera rig will produce a smeared mouth interior, fused fingers, and hair that reads as a helmet.**

**3. Lighting mismatch destroys the illusion even when geometry is perfect.**
Splats bake in capture lighting. Put a person captured under office fluorescents into a warm-lit room and the brain flags it instantly. Relighting needs light-stage capture or per-frame PBR decomposition. **Meta explicitly notes SqueezeMe's mobile avatars have flat lighting with no dynamic relighting** — Meta shipped the compromise; you will too. Google Beam works around this with **adaptive LED lighting on the capture side** — a hardware answer, not a software one.

**4. Temporal flicker is the failure mode nobody demos.**
Per-frame feed-forward reconstruction has no temporal consistency term. Still frames look great; motion boils. This is why MPEG's dynamic-splat test-material call demands **constant point count and ordering across frames** — temporal coherence is the unsolved part, and MPEG says so directly.

**5. Bandwidth: the naive architecture is 100× over budget.**
Streaming 4D Gaussians at good quality is **~120–314 Mbps**. Best foreground-only research number is **~2.7 Mbps**, and **every one of those methods needs 0.7–4.3 minutes of offline optimization per frame.** There is no real-time 4DGS encoder in the literature. Apple ships spatial telepresence at **0.7 Mbps** by not streaming geometry at all.

**6. Latency: you have ~150 ms and the network takes half.**
Apple measured **>80 ms RTT US coast-to-coast**. Tele-Aloha's 23.5 ms of compute fits only because it was measured **on the same LAN**. And it isn't just "feels laggy" — the 2026 study shows fluency degrades gradually from 100 ms but **collapses at 300 ms under cognitive load**. A demo that feels fine while people chat fails the moment they try to work together.

**7. Licensing will quietly make your work unshippable.**
The pattern: **a repo with an MIT badge whose actual dependencies are non-commercial.** GPS-Gaussian+ is MIT but requires the INRIA rasterizer. 3DGS-Avatar / GaussianAvatar / ExAvatar are MIT but require SMPL/SMPL-X — whose license bans commercial use *and bans training networks for commercial use*, tainting anything you fine-tune. NLF's code is MIT but its **weights** are non-commercial. WiLoR carries **three** incompatible obligations. And the commercial escape hatch just closed: **Meshcapade, the exclusive commercial SMPL licensor, was acquired by Epic Games and shut its platforms 18 April 2026.**

> **Safe stack:** gsplat (Apache-2.0) + Anny (Apache-2.0) or MHR + BiRefNet (MIT) + LAM (Apache-2.0). **Audit every transitive dependency.**

### Additional traps

- **Datasets are research-only and enormous.** DNA-Rendering: 60 synchronous cameras, 4096×3000, 500 subjects, access by email request. You cannot train a generalizable model at a hackathon — you must use pretrained weights, which pulls their license with them.
- **"Real-time" in abstracts usually means rendering, not the pipeline.** Animatable Gaussians is "real-time" (10 fps) after **two days** of training. LAM's 562.9 fps is on an A100 and excludes tracking, matting, and transport.
- **Enrollment friction is a product feature.** Mon3tr: 32× 12MP cameras, 1–2 min, then 33 s — but only *once*. Apple: ~10 s on-device. Meta: ~1 hour server GPU. **The one you can ship is the one with the shortest enrollment.**
- **Segmentation errors are more visible in 3D than 2D.** A matting error in 2D is a fringe; in 3D it becomes floating geometry that persists across viewpoints and flickers with motion.
- **Privacy is now a research topic** — see InViStream · [2608.11645](https://arxiv.org/abs/2608.11645) (UCLA/Nokia Bell Labs, Aug 2026): sanitize *before* raw multi-view data leaves the cameras, because a fused point cloud reveals the whole room.

### What to actually build

Follow **Mon3tr's architecture** — the only one with a plausible latency/bandwidth story:

1. **Offline (once per person, ~1–2 min):** capture → build a personal Gaussian avatar. **LAM (Apache-2.0, 1.4 s, head-only)** for instant, or a short per-subject fit for a body.
2. **Online:** single RGB camera → **BiRefNet (MIT)** matting → **SAM 3D Body / Multi-HMR + Anny** for pose+hands → stream **only parameters over WebRTC (<0.2 Mbps)** → drive and render the pre-built avatar on the receiver with **gsplat or Brush (Apache-2.0)**.
3. **Drive the face from audio**, not face tracking — Meta's own path around missing sensors, **<15 ms GPU time**.
4. Render to a browser (SuperSplat/PlayCanvas, SOG) or Quest 3.

**Budget your demo risk on enrollment quality and hands, not on frame rate.**

---

## 7. Numbers that do not exist (stated explicitly)

- Google Beam / HP Dimension bandwidth and latency — **none published by either company**
- Google Beam camera count — **unresolved conflict: 6 vs 7**
- Google Beam license price — undisclosed
- Meta LCA — no params, inference time, GPU, or release status
- SAM 3D Body / Fast SAM 3D Body — no absolute fps
- MatAnyone, MatAnyone 2, HAC++, MODNet, NLF, HMR2.0, NVIDIA Maxine — no published fps
- MediaPipe per-device latency — **removed from current Google docs**
- SOG spec license — not stated
- **A talking-human volumetric-vs-2D bitrate comparison at matched quality — does not exist in the literature. This is a real, publishable gap.**
- Chinese production volumetric telepresence systems — no credible primary source found
- MPEG GSC CfP date and target IS date — not published
