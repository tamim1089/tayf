> **⚠ RESOLVED 2026-08-16 — read the top of this file with that in mind.** The AIRR primary literature described below as paywalled is not: Yamamoto, *J. Imaging Soc. Japan* **56**(4) 341–351 (2017), DOI `10.11370/isj.56.341`, is **open access on J-Stage** and has now been read in full. It measures **170° viewing angle** and **>2.2× polarised-AIRR gain**. The unit-magnification bound below still stands. What remains unmeasured anywhere is the retroreflector return efficiency η_RR.

# Branch C — Aerial Imaging Optics

Corresponds to the retroreflective/AIP half of `hardware/optical-engine.md`'s hackathon-track option, and to the north-star question of transforming a small optical source into a larger apparent aerial volume.

## Research questions

1. Can small optics (Fresnel, catadioptric, retroreflective corner-cube arrays) produce a large apparent volume from a source that fits the 10cm constraint?
2. How much magnification is achievable, and what does it cost in brightness (inverse relationship expected — needs measurement, not assumption)?
3. What happens to spatial resolution under magnification — does the apparent image stay sharp enough for face/hand detail at the perceptual-quality thresholds `experiments/perceptual-quality/README.md` is establishing?

## Protocol

Same experiment-1-through-4 ladder as `experiments/light-field/README.md`, run against whichever aerial-imaging optical path is chosen if the AIP variant of the hackathon-track decision (task #9) is selected over a light-field panel. If the light-field panel is chosen instead, this branch stays a north-star-track alternative rather than the primary path — `hardware/optical-engine.md` treats these as two candidates under one hackathon-track slot, not two parallel required tracks.

## Literature check, Aug 2026: wrong venue searched, not "nothing exists"

A 467-paper triage of every "aerial"-tagged corpus entry, plus a full-corpus keyword sweep for retroreflective/catadioptric/Fresnel/AIRR/corner-cube terminology, found **zero genuine papers on arXiv** — all 467 were drone/satellite/remote-sensing false positives (same failure mode as "plasma" matching particle-accelerator physics elsewhere in this project). This does **not** mean the mechanism has no real research behind it: external search confirms **Aerial Imaging by Retro-Reflection (AIRR)** — Yamamoto/Suyama et al., Utsunomiya University, commercialized as **ASKA3D** — is a real, decade-plus, active research program, published in Optics Express / OSA Continuum / Optical Review, none of which arXiv mirrors. Titles found are almost verbatim this branch's two open questions: "Reducing thickness of long-distance aerial display system in AIRR using Fresnel lens" (Optical Review, 2023) and "Improved resolution for aerial imaging by retro-reflection with two transparent spheres" (Optical Review, 2022). Full text was not obtained *at the time* — **but see the banner at the top of this file: the key paper was open access all along and has since been read.** The lesson stands and is recorded in `research/METHODOLOGY.md`: the sweep failed on venue coverage and search vocabulary, not on the literature's existence.

**Known scale caveat even before real numbers arrive:** AIRR's demonstrated form factor (floating LED signage, retroreflector plates tens of centimeters across, arm's-length-plus viewing distances) targets kiosk/signage scale — even a favorable published number would leave "does the retroreflector + beam-splitter path fold into a 10cm sealed enclosure with the source also inside it" completely open.

**Next step for whoever picks this branch up:** measure **η_RR**, the retroreflector return efficiency (aerial-image cd/m² per source cd/m²). The literature question is closed; this one is not, it is stated nowhere, and every brightness and panel-power figure in the project depends on it. One afternoon with a spot luminance meter at V0.

> **Scheduled 2026-08-21.** η_RR now gets measured on the **same bench** as experiment PQ-1 in
> `experiments/perceptual-quality/README.md`, which needs a static free-space real image anyway.
> Build once, take both numbers. Two instrument paths: a borrowed spot luminance meter gives
> `[MEASURED]`; a phone camera in full manual mode calibrated against a known-luminance source
> gives `[INDICATIVE]` — record which was used. This closes an open item that `docs/13` §4
> currently papers over with an assumed 5% end-to-end efficiency.
>
> Note the unit-magnification bound below does **not** block this use: PQ-1 needs a free-space
> real image at a controlled distance, not a magnified one, and a 50–80 mm test object at M = 1
> is exactly what AIRR delivers well.

> **Methodological note:** the two "zero papers found" sweeps that preceded this section were keyword searches, and they were wrong in a specific and instructive way — see `research/METHODOLOGY.md` §1. The real AIRR literature existed the whole time, in journals the keyword never reached.

## Bounded on first principles (2026-08-15), without needing the paywalled literature

`docs/02_FREE_SPACE_OPTICAL_ENGINEERING.md` settles the branch's central question analytically, which the arXiv sweeps could not: **AIRR is unit-magnification by construction.** A retroreflective aerial-imaging plate forms a real image that is the same size as the source, mirrored about the plate — it relays, it does not magnify. That is a geometric property of the mechanism, not a limitation of any particular implementation, so no amount of primary-literature access changes it.

Consequences for TAYF:
- **The apparent image can be no larger than the internal source**, so a life-size head requires a life-size internal display — impossible inside a 100 mm enclosure.
- Bounded at **≤60 mm image with ~40 mm float distance** for a cube-scale device, and the beamsplitter geometry stops fitting beyond roughly that.
- This makes AIRR viable for a small floating object — a face at doll scale, an icon, a status indicator — and **not viable for a life-size remote human**.

The Optical Review papers named below remain worth reading for the thickness/magnification and resolution-recovery engineering, but they cannot change the unit-magnification bound. **Branch C is therefore no longer "unassessed" — it is bounded, and it does not reach TAYF's stated apparent-size requirement (`docs/01_SYSTEM_MASTER_SPEC.md` §8).**

## Status

Bounded, not pursued for the life-size target. Still a candidate for a small-object or reduced-scale variant if parameter A4 (apparent subject) is ever relaxed that far. Search target for any future literature dive remains specific: AIRR/ASKA3D, not a generic "aerial imaging" arXiv search.
