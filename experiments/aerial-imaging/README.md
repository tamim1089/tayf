# Branch C — Aerial Imaging Optics

Corresponds to the retroreflective/AIP half of `hardware/optical-engine.md`'s hackathon-track option, and to the north-star question of transforming a small optical source into a larger apparent aerial volume.

## Research questions

1. Can small optics (Fresnel, catadioptric, retroreflective corner-cube arrays) produce a large apparent volume from a source that fits the 10cm constraint?
2. How much magnification is achievable, and what does it cost in brightness (inverse relationship expected — needs measurement, not assumption)?
3. What happens to spatial resolution under magnification — does the apparent image stay sharp enough for face/hand detail at the perceptual-quality thresholds `experiments/perceptual-quality/README.md` is establishing?

## Protocol

Same experiment-1-through-4 ladder as `experiments/light-field/README.md`, run against whichever aerial-imaging optical path is chosen if the AIP variant of the hackathon-track decision (task #9) is selected over a light-field panel. If the light-field panel is chosen instead, this branch stays a north-star-track alternative rather than the primary path — `hardware/optical-engine.md` treats these as two candidates under one hackathon-track slot, not two parallel required tracks.

## Literature check, Aug 2026: wrong venue searched, not "nothing exists"

A 467-paper triage of every "aerial"-tagged corpus entry, plus a full-corpus keyword sweep for retroreflective/catadioptric/Fresnel/AIRR/corner-cube terminology, found **zero genuine papers on arXiv** — all 467 were drone/satellite/remote-sensing false positives (same failure mode as "plasma" matching particle-accelerator physics elsewhere in this project). This does **not** mean the mechanism has no real research behind it: external search confirms **Aerial Imaging by Retro-Reflection (AIRR)** — Yamamoto/Suyama et al., Utsunomiya University, commercialized as **ASKA3D** — is a real, decade-plus, active research program, published in Optics Express / OSA Continuum / Optical Review, none of which arXiv mirrors. Titles found are almost verbatim this branch's two open questions: "Reducing thickness of long-distance aerial display system in AIRR using Fresnel lens" (Optical Review, 2023) and "Improved resolution for aerial imaging by retro-reflection with two transparent spheres" (Optical Review, 2022). Full text could not be obtained (JS-gated / login-walled / 403s) — no magnification, brightness, or resolution numbers are verified; one search-engine-paraphrased brightness figure (~25% of source) is explicitly flagged unverified and must not be cited as fact.

**Known scale caveat even before real numbers arrive:** AIRR's demonstrated form factor (floating LED signage, retroreflector plates tens of centimeters across, arm's-length-plus viewing distances) targets kiosk/signage scale — even a favorable published number would leave "does the retroreflector + beam-splitter path fold into a 10cm sealed enclosure with the source also inside it" completely open.

**Next step for whoever picks this branch up:** get institutional or document-delivery access to Optics Express, OSA Continuum, and Optical Review specifically for the Yamamoto/Suyama AIRR line. Another arXiv sweep, however the search terms are refined, will keep returning zero — this is a venue problem, not a search-quality problem.

## Status

Not started — contingent on task #9's outcome. Search target for the eventual literature deep-dive is now specific: AIRR/ASKA3D, not a generic "aerial imaging" arXiv search.
