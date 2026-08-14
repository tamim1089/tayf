# TAYF (طيف)

Engineering plan and research corpus for a compact spatial-telepresence device: parametric human-state capture and transport are solved, free-space optical reconstruction is the open problem.

## Concept

Two identical ~10×10×10cm cubes. Each captures its local human, computes a compact dynamic representation of them, streams it over an ordinary network connection, and reconstructs the remote human as free-space light at the other cube — no screen, wall, headset, or external projector as the primary output. The network carries a person's state, not their video.

## Implementability

~85% of the system — capture, human representation, compression, transport, and the telecom layer — is buildable today from published, license-clean methods, several already validated at real-time rates with measured bandwidth/latency numbers. The remaining ~15% — free-space optical emission of a photoreal, video-rate human from a 10cm enclosure — is not solved anywhere in the current literature. See [`FilesPlan.md`](./FilesPlan.md) for the full verdict and the two-track plan that follows from it.

## Repository layout

| Path | Contents |
|---|---|
| [`FilesPlan.md`](./FilesPlan.md) | Master engineering plan — start here |
| `docs/` | System architecture, theory, roadmap, spatial calibration |
| `hardware/` | BOM, camera rig, optical engine, power/thermal, enclosure |
| `firmware/` | Edge-SoC firmware scope |
| `pipeline/` | Capture → avatar → view-synthesis → transport software |
| `agent/` | CAMARA (Nokia Network-as-Code) agent layer |
| `app/` | Phone app scope (pairing, capture-boundary setting) |
| `design/` | Visual design principles and tokens |
| `experiments/` | The physical/empirical validation program |
| `patent/` | Patent strategy notes and prior-art seed list (draft, not legal advice) |
| `pitch/` | Hackathon submission drafts |
| `research/` | Annotated research corpus — 128 papers deep-read across four tracks, plus licensing and citation indexes |

## Status

Solo project, active research and planning phase. Nothing in `hardware/` has been ordered; nothing in `pipeline/` has been implemented yet. See `FilesPlan.md` §6 for the current blocking decisions.

## License

Not yet decided. See [`research/LICENSING.md`](./research/LICENSING.md) for the third-party dependency licensing table.
