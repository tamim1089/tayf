# Component Licensing Table

Per `research/notes.md` §41: "MIT repository" does not mean "commercially safe system" — dependencies can carry separate restrictions on weights, datasets, or transitively-included code. This table must be kept current and independently re-verified before any commercialization step, not trusted from memory.

| Component | Purpose | License (as researched) | Commercial status | Used in |
|---|---|---|---|---|
| gsplat | Gaussian-splat rendering | Apache-2.0 | Promising | `pipeline/requirements.txt` |
| Brush | WebGPU Gaussian rendering | Apache-2.0 | Promising | candidate, not yet wired into `pipeline/` |
| Anny (NAVER) | Parametric human body model | Apache-2.0 | Promising — **recommended avatar model**, see `pipeline/avatar/README.md` | `pipeline/requirements.txt` |
| MHR (Meta Momentum Human Rig) | Human rig | Permissive direction | Verify exact terms before use | alternative to Anny, not yet chosen between |
| BiRefNet | Matting/segmentation | MIT | Promising | `pipeline/capture/README.md`, `pipeline/requirements.txt` |
| SAM 3 / SAM 3D Body | Body estimation / segmentation | Custom | Verify before use | candidate, not yet wired in |
| LAM | Large avatar model (canonical-avatar enrollment) | Apache-2.0 | Promising | `pipeline/avatar/README.md`, `pipeline/requirements.txt` |
| SMPL / SMPL-X | Parametric body model | Non-commercial | **Excluded** — do not use | explicitly rejected, see `pipeline/avatar/README.md` |
| aiortc | WebRTC in Python | BSD | Promising | `pipeline/requirements.txt` |
| network-as-code (Nokia NaC SDK) | CAMARA API client | Vendor SDK — verify redistribution terms if TAYF ships the client, not just uses it | Verify | `agent/nac_client.py` |

## Policy

1. Every new dependency added to `pipeline/requirements.txt` or vendored elsewhere gets a row here before it's used in anything beyond a local experiment.
2. "Apache-2.0 repository" is not sufficient — check the actual model *weights* license separately from the code license (this is exactly the trap notes.md warns about: a permissively-licensed training/inference codebase can still ship non-commercial pretrained weights).
3. Re-verify this whole table before any step toward commercialization or public release — licenses change, and "verified once" is not "verified now."

## Why SMPL-X is excluded despite being the research-literature default

Most papers catalogued in `research/deepseek_research.md`'s Human-Representation track use SMPL-X because it's the academic standard, not because it's the right production choice. TAYF standardizes on Anny (or MHR, pending the "verify exact terms" item above) specifically so the capture/avatar pipeline is never built against a dependency that has to be ripped out before shipping.
