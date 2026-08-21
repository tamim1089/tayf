# TAYF (طيف)

**A person, sent across the world as a few hundred numbers a second, and rebuilt as light standing in the air at the other end.** No screen carrying the image, no headset, no glasses, nothing worn.

![The aperture law](models/png/09_aperture_law_front.png)

*Devices at true scale. Each plate is exactly as tall as the figure in front of it. That is the law the whole project runs on.*

---

## Start here

**→ [`docs/00_INDEX.md`](docs/00_INDEX.md)** — which of the twenty-odd documents to believe, and what supersedes what.

Then, in order:

1. **[`docs/13_THE_ROOM.md`](docs/13_THE_ROOM.md)** — the product.
2. **[`docs/15_THE_ACCOMMODATION_BUDGET.md`](docs/15_THE_ACCOMMODATION_BUDGET.md)** — why it is a *small* room, and the correction that deleted its most expensive part.
3. **[`docs/16_BUSINESS_LEGAL_AND_LOGISTICS.md`](docs/16_BUSINESS_LEGAL_AND_LOGISTICS.md)** — money, entity, IP, certification, logistics.
4. **[`experiments/perceptual-quality/BENCH.md`](experiments/perceptual-quality/BENCH.md)** — the **~$215** experiment that decides whether any of it is worth building.

[`docs/10_TAYF_UNIVERSAL_ENGINEERING.md`](docs/10_TAYF_UNIVERSAL_ENGINEERING.md) is the deep derivation — 3,650 lines, first principles to part numbers, every claim tiered by how much it is actually trusted. It is **partly superseded** by documents 11–16; read its banner first.

---

## The two products

They are different machines, both kept, and the difference is which of [`thedream.md`](thedream.md)'s ten rules each obeys.

| | **TAYF-C35** — [`docs/11`](docs/11_THE_CUBE.md) | **THE ROOM** — [`docs/13`](docs/13_THE_ROOM.md) |
|---|---|---|
| Form | 350 mm cube on a desk | 3.5–4 m room, viewers at 1.3–1.8 m |
| Shows | life-size head **and neck**, floating ~45 mm out | a life-size person, 360°, walk-around |
| Engine | AIRR — three static sheets, no moving parts | 15–19 fixed-focus DMD engines around an HOE band |
| Rules | **9 of 10 pass.** Only "ten centimetres" fails | rules 4, 6, 8 **deliberately suspended** |
| Status | specified, unbuilt | specified, gated on the PQ-1 bench |

> **A retraction, kept on the front page.** An earlier version of this README claimed a **20 × 20 cm** desk slab shows *"upper body at 1.2 m"*. **That is false** — an upper body is 80 cm, and a 20 cm aperture yields ~20 cm. The error is **4× linear, 16× in area**, and it is recorded in [`docs/11` §1.3](docs/11_THE_CUBE.md) rather than quietly deleted.

## The four laws

Every dimension falls out of geometry. These are not technology limits; they are statements about where light can go.

1. **Clipping** — an image *in your space* cannot exceed the aperture. `W ≤ D`. A 10 cm device floats a 10 cm object. *(Smalley et al., Nature **553**, 486 — matter at the image point is the sole exception, quoted verbatim in [`docs/01`](docs/01_SYSTEM_MASTER_SPEC.md) §4.3g.)*
2. **Visibility, not capability** — for an image *beyond* the device, `W = D·(b/a)` is a **permission, not a mechanism**: it says where such an image may be *seen from*, never that a device can *make* one. The operative law is the minimum viewing distance `a_min = D·p/(D−W)`, and **it has no solution once `W ≥ D`.** *(Corrected in [`docs/11`](docs/11_THE_CUBE.md) §4.2a — the original wording is kept there.)*
3. **Presence is an angle** — the device must subtend the same angle as the subject. A face at 1 m is only **12.6°**, which is why small devices are not useless.
4. **Tiling** — to be seen from 360°, apertures must tile the circle at the image: **`N = 2πz/D`**. This is why the room is small: **19 engines at z = 1.5 m**, 88 at 3.5 m. And viewers stand *inside* the ring, so **z > R** — which is what fixes z at 1.5 m once the design point R ≈ 1.3 m is set. *([`docs/13`](docs/13_THE_ROOM.md) §1, three independent derivations agreeing.)*

**And one perceptual result that corrected the pitch.** Both depth cues scale as `t/R²`, so their ratio is constant at every distance and subject size: **stereopsis is 268× more sensitive to depth than accommodation.** Vergence–accommodation conflict is a *comfort* problem, not a *depth* problem. Lead with **multi-viewer** — a room full of people each seeing the remote person correctly from their own angle, which no tracked screen can do — not with focus. *([`eng/03_PHYSICS/depth_cues.py`](eng/03_PHYSICS/depth_cues.py), 20 tests.)*

## What is solved, and what is not

**Solved and measured:** capture, avatar representation, compression, transport, and the CAMARA network layer. Wire rate **0.104 Mbps** measured; latency **126 ms** against a 150 ms conversational threshold; AIRR viewing angle **170°** measured *(Yamamoto 2017, `10.11370/isj.56.341`)*.

**Derived and unit-tested, not yet measured:** the aperture law, the depth-cue budget, the accommodation budget, the design point. 132 tests in [`eng/08_VERIFY/tests/`](eng/08_VERIFY/), including one that fails the build if prose drifts from the code that produced it.

**Unmeasured, and blocking:** **η_RR**, the retroreflector return efficiency. No published source states it, every brightness figure in the project rests on it, and one afternoon on the PQ-1 bench closes it.

**Unresolved, and expensive:** the **HOE relay band**. It is simultaneously the only defensible
moat and a single-source risk — and the supplier's demonstrated capability (1400 mm film width,
A2 master area, automotive-only focus) does not obviously reach a 6.6 m² angularly-multiplexed
band. Until a written quote exists, the cost model is unproven. See `hardware/bom.md` §3.

**Unresolved, and the real risk:** whether anyone can *tell*. Once a person fits inside one depth-of-field slab, a free-space image is not obviously better than a screen at the same place — and a published study found a flat 2D cutout scoring co-presence indistinguishably from a full 3D avatar. That is an **existence risk**, not a build risk, and it is what PQ-1 exists to settle. See [`docs/15`](docs/15_THE_ACCOMMODATION_BUDGET.md) §4.

**Not buildable by anyone:** a 10 cm cube putting a whole standing person in your chair. Six independent physical laws forbid it — clipping, nitrogen's spin selection rule, the plasma power wall, numerical aperture, Bjerknes collapse, and pulmonary toxicology. Each was tested rather than assumed; each is written up in `docs/10` §9 so nobody re-treads them.

## Repository

| Path | Contents |
|---|---|
| [`docs/00_INDEX.md`](docs/00_INDEX.md) | **Which documents to believe — start here** |
| `docs/11`–`16` | The live set: the cube, prior art, the room, patents, accommodation, business |
| `docs/01`–`10`, `docs/sections/` | Deep derivations and detail specs, partly superseded |
| `eng/` | Physics models and the 132-test verification suite |
| `experiments/` | Physical validation programme. **PQ-1 is the next action.** |
| `models/` | True-scale 3D models, renderer, viewer. Pure standard library. |
| `simulation/` | Wave-optics propagator (9/9 against analytic results), thermal model |
| `pipeline/` | Capture → avatar → view synthesis → transport, incl. `schema.py` |
| `agent/` | Nokia Network-as-Code / CAMARA layer and its compliance constraints |
| `hardware/` · `firmware/` · `app/` · `design/` | Subsystem specs |
| `patent/` | Prior-art and IP notes *(draft — not legal advice)* |
| `research/` | **175 papers** across four tracks, plus licensing, citations, and `METHODOLOGY.md` |

**[`research/METHODOLOGY.md`](research/METHODOLOGY.md) is worth reading on its own.** It records the research rules this project earned by breaking them — chief among them that surveying literature by keyword returns confident false negatives about exactly the ideas you failed to anticipate. A keyword sweep here returned 467 drone photographs for "aerial" while the decade-long research programme the project actually needed sat in an open-access journal the search never reached.

The same habit applies to the engineering. The corrections are indexed in [`docs/00_INDEX.md`](docs/00_INDEX.md) and are the most useful thing in the repository.

## Status

Solo project. Nothing ordered, nothing fabricated.

**Next action: build the PQ-1 bench (~$215) and run it.** Beamsplitter, retroreflector, two identical figurines, a stepper. It measures η_RR and answers whether a free-space image is perceptibly better than a screen at the same location — the question that gates every other spend. Protocol, confounds and parts list in [`experiments/perceptual-quality/BENCH.md`](experiments/perceptual-quality/BENCH.md); the analysis is pre-registered and validated against synthetic studies before any data exists.

## Licence

Undecided. See [`research/LICENSING.md`](research/LICENSING.md) for the third-party dependency table — SMPL-X and its derivatives are excluded as non-commercial, and several estimator licences remain unverified.
