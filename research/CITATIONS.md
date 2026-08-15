# Research Index

Pointer index across every research artifact in this repo — read this first to find where a given claim is sourced, rather than searching each file independently.

| File | Contents | Scope |
|---|---|---|
| `research/METHODOLOGY.md` | **Read first.** Research rules earned from actual wrong conclusions on this project — chiefly: never survey literature by keyword search, and always name the architecture a constraint was evaluated in. | All tracks |
| `research/notes.md` | The original architecture/vision brainstorm — four research tracks, optical architecture candidates, patent framing, experimental program. Source document for `docs/theory.md`, `experiments/`, `patent/`. | Conceptual/architectural |
| `research/01-volumetric-capture-sota.md` | Volumetric capture/rendering SOTA: Gaussian splatting, parametric avatars, codecs, licenses, bandwidth figures. Source for `research/LICENSING.md` and `pipeline/`'s dependency choices. | Human representation + transport |
| `research/deepseek_research.md` | Annotated bibliography — 128 papers deep-read across four tracks (Optics, Human, Transport, Perception), each with a long paragraph on method + relevance to TAYF. The single largest primary-source corpus in this repo. | All four research tracks |
| `research/arxiv/online_findings.md` | Free-space display physics findings from web research (laser-plasma, cloud-medium displays, pulse-shaping) — some entries flagged `[FLAG]` as not independently re-verified. Source for `hardware/optical-engine.md`'s physics table. | Free-space optics |
| `research/arxiv/corpus.jsonl`, `ids.txt`, `manifest.csv` | Raw discovery/fetch pipeline state — ~15,800 candidate papers, ~4,000 fetched sources, 128 documented. Not meant to be read directly; see `deepseek_research.md` for the readable output. | Pipeline state |

## Highest-value single findings (worth knowing without re-reading everything)

- **Mon3tr (arXiv 2601.07518)** — the closest published full-stack reference architecture for TAYF's capture→representation→transport chain: <0.2 Mbps, ~80ms end-to-end, 215-float driving-parameter stream. Underpins `pipeline/schema.py` directly.
- **JSID 2025 fist-sized laser-plasma display** — the closest published free-space optical result at cube scale (68×42mm, ~10k voxels/s). Underpins `hardware/optical-engine.md`'s north-star track and its "not photoreal-capable for years" verdict.
- **GETA-3DGS (arXiv 2605.02086)** and **arXiv 2510.10492** — avatar/Gaussian compression numbers underpinning `pipeline/avatar/README.md`'s compression claims.

## Status of unverified claims

Every `[FLAG]` in `research/arxiv/online_findings.md` remains unresolved — the fact-check pass tasked with resolving them was killed mid-run before writing anything (see project task list). Treat those specific citations as unverified until that pass is rerun, not as confirmed.

## What's still missing

Per `docs/theory.md`'s Track D (Perception), the psychophysics/perceptual-threshold literature is the thinnest-covered track in `deepseek_research.md` relative to its importance — see `experiments/perceptual-quality/README.md` for what needs to be run rather than just read.
