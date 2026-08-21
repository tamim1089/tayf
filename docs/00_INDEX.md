# 00 — Index: which of these documents to believe

**Maintained 2026-08-21.** Twenty-plus documents accumulated over a project that changed shape
several times. This page says which are current, which are history, and what supersedes what.

`research/METHODOLOGY.md` rule 4 means **superseded documents are kept, not deleted** — the
corrections are the record. That only works if you can tell them apart. That is this page.

| Status | Meaning |
|---|---|
| **LIVE** | Current. Build from this. |
| **PART** | Superseded in part. Correct where it agrees with the LIVE set, historical where it doesn't. Banner at the top says which. |
| **HIST** | Historical. Kept for the reasoning and the error record. **Do not build from it.** |

---

## Start here

1. **`13_THE_ROOM.md`** — the product.
2. **`15_THE_ACCOMMODATION_BUDGET.md`** — why it is a *small* room, and the correction that
   deleted its most expensive component.
3. **`16_BUSINESS_LEGAL_AND_LOGISTICS.md`** — money, entity, IP, certification, logistics.
4. **`experiments/perceptual-quality/BENCH.md`** — the ~$215 experiment that decides whether any
   of it is worth building.

---

## The live set

| Doc | Status | What it is |
|---|---|---|
| **`13_THE_ROOM.md`** | **LIVE** | The product: 360° free-space telepresence room, `N = 2πz/D`, 15–19 engines, viewers at 1.3–1.8 m. `thedream.md` rules 4/6/8 deliberately suspended. Carries three boxed corrections (§6, §7, §11) — read them, they are the useful part. |
| **`15_THE_ACCOMMODATION_BUDGET.md`** | **LIVE** | A person fits in one depth-of-field slab at pod distance, so the plane count is 1–2 and not 24–32. Deletes the swept-focus element. Fixes the design point at R ≈ 1.3 m, robust across every plausible depth-of-field figure. |
| **`16_BUSINESS_LEGAL_AND_LOGISTICS.md`** | **LIVE** | Entity, funding, the biometric/likeness exposure, certification path, full cost stack, logistics, go-to-market. |
| **`14_TELEHUMAN_AND_THE_PATENT_GAP.md`** | **LIVE** | TeleHuman 2 (CHI 2018) built the broadcast version of this architecture and never commercialised it. Vertegaal's 16-patent estate contains nothing on it. Corrects doc 13's moat claim. |
| **`12_THE_FORGOTTEN_PRIOR_ART.md`** | **LIVE** | US 4,881,068 — a 1988 sealed rubidium cube that did what `thedream.md` asks, and why it still fails rule 4. |
| **`11_THE_CUBE.md`** | **LIVE** | TAYF-C35, the **rules-compliant** design: 350 mm cube, life-size head + neck, 9 of 10 rules passed. A *different product* from doc 13, deliberately kept. §1.3 records this project's worst error. §7 lists corrections to the older docs. |
| **`05_RESEARCH_PRIOR_ART_AND_PATENT_ARCHITECTURE.md`** | **PART** | The prior-art and FTO ledger. §3.4 is the most consequential section in the repository. Still the authority on patents; predates docs 14/16. |

## Partly superseded — correct in places, historical in others

| Doc | Status | Read it for | Superseded on |
|---|---|---|---|
| `10_TAYF_UNIVERSAL_ENGINEERING.md` | **PART** | The deep derivation — 3,650 lines, first principles to part numbers, every claim tiered. Several derivations exist nowhere else. | Plane count, focus element, the accommodation pitch, the device family, the product form. See its banner. |
| `01_SYSTEM_MASTER_SPEC.md` | **PART** | The clipping theorem with the verbatim Smalley quotation, §4.3 | L2 tables read as capability — they are visibility bounds |
| `02_FREE_SPACE_OPTICAL_ENGINEERING.md` | **PART** | Layouts A–F, the plasma and photophoretic eliminations | §10 item 8 falsification now MET |
| `09_DEVICE_DESIGNS.md` | **PART** | The aperture law applied to viewing geometries | The six-form family; "unit magnification" needs the *conventional AIRR* qualifier |
| `03_...CAPTURE...md`, `04_CUBE_HARDWARE...md` | **PART** | Capture, avatar, transport — largely unaffected by the optical corrections | Anything about the 10 cm cube enclosure |
| `roadmap.md`, `architecture.md`, `theory.md`, `calibration.md` | **PART** | Design reasoning | Timeline, device form, next step |

## Historical — do not build from these

| Doc | Why kept |
|---|---|
| `FilesPlan.md` | The first plan. The 10 cm cube, the 85/15 split, the plasma north star. The reasoning is worth reading; every specific is superseded. |
| `06_MASTER_RESEARCH_AND_BUILD_PLAN.md`, `07_HARDWARE_SIMULATION_PLAN.md`, `08_FINAL_PRODUCT_PLAN.md` | Superseded plans, kept for the decision trail. |
| `matd_plan.md` | Acoustic trapping (MATD). Evaluated and ruled out with quantitative reasons. |
| `docs/sections/` | Section sources that `docs/10` was assembled from. Inherit doc 10's status. |

---

## Outside `docs/`

| Path | Status | What |
|---|---|---|
| `thedream.md` | **LIVE** | The ten rules. The authority on what the product is *supposed* to be. Doc 11 obeys them; doc 13 suspends 4, 6 and 8 deliberately and says so. |
| `research/METHODOLOGY.md` | **LIVE** | Five rules earned by breaking them. Read before any research pass. |
| `eng/03_PHYSICS/` | **LIVE** | `accommodation.py`, `depth_cues.py` — the models the docs are checked against. |
| `eng/08_VERIFY/tests/` | **LIVE** | 132 tests, including `test_docs_match_model.py`, which fails the build if prose drifts from the code that produced it. |
| `experiments/perceptual-quality/` | **LIVE** | PQ-1: protocol, bench spec, pre-registered analysis, and the simulation that validated it. **The next physical action.** |
| `experiments/aerial-imaging/` | **LIVE** | Branch C, bounded. Holds the η_RR measurement — never measured by anyone, scheduled on the PQ-1 bench. |
| `hardware/` | **PART** | Being brought onto the doc 13 architecture; check each file's banner. |
| `models/` | **LIVE** | True-scale 3D models and renderer. Pure standard library. |
| `research/` | **LIVE** | 175 papers across four tracks, plus citations, licensing, and two external research passes. |
| `research/2026-08-21_costing_and_legal_research.md` | **LIVE** | The pricing and legal pass. Returned one verified component price that broke the BOM by ~3×, resolved the EU AI Act question, and re-sized the FTO threat from Google to Light Field Lab. |
| `patent/` | **PART** | Draft IP notes. Superseded on strategy by doc 14 §5 and doc 16 §3.2. **Not legal advice.** |

---

## The corrections worth reading on their own

This project's habit of recording its own errors in place is the most useful thing in it:

- **`11` §1.3** — the 20 cm slab. Told its own author a 20 cm aperture shows an upper body. It
  shows 20 cm. 4× linear, 16× in area.
- **`13` §6** — led the pitch with accommodation, which is **268× weaker** than stereopsis as a
  depth cue.
- **`13` §7** — sized depth planes geometrically instead of perceptually, inventing a 2,700 Hz
  requirement and a $10–50k component that were never needed.
- **`13` §11** — claimed a moat that `docs/05` §3.4 had already refuted, in this same repository.
- **`15` §6** — flagged a component for deletion in the wrong architecture, then retracted it.
- **`experiments/perceptual-quality/README.md` §PQ-1.1** — four statistical design faults caught
  by simulation before any subject was run.
