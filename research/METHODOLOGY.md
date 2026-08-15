# Research Methodology — rules earned the hard way

Every rule here exists because breaking it produced a wrong conclusion on this project. They are not style preferences.

---

## 1. Do not survey literature by keyword search

**The rule:** never use grep/keyword matching to decide whether prior work exists, whether a research area is empty, or whether a solution has been found. Keyword search can only return terms you already thought of, so it produces confident-looking negatives about exactly the ideas you failed to anticipate — which are the ones worth finding.

**What it cost us:**

- **The aerial-imaging false negative.** A keyword sweep for "aerial" returned 467 papers in this corpus, *all* of them drone/satellite imagery, and zero display-optics hits. Two independent passes concluded "no aerial-imaging research exists." It does: Aerial Imaging by Retro-Reflection (AIRR / ASKA3D, Yamamoto & Suyama, Utsunomiya University) is a decade-plus active program — published in Optics Express, OSA Continuum and Optical Review, venues arXiv does not mirror, using vocabulary the keyword never touched.
- **The plasma false positives.** "Plasma" surfaced particle-accelerator and THz-generation physics, repeatedly, across multiple passes, wasting reading budget on papers with no display relevance.
- **Propagated blind spots.** The corpus-building pipeline (`build_telepresence.py`, `build_fast.py`) is itself keyword-cluster-based, so its vocabulary gaps silently became every downstream "we found nothing" conclusion. A negative result from this corpus is evidence about the corpus, not about the world.

**What to do instead:** read broadly and semantically. Follow citation graphs from the few papers you know are relevant. Ask "what physical mechanism would solve this?" and search for the mechanism's *physics*, not its name. Check whether the relevant literature even lives in the corpus you are searching — venue coverage is a real, large gap. When you must report a negative, write *"did not find in corpus X using approach Y"*, never *"does not exist."*

---

## 2. Verify or mark UNVERIFIED — never assert

Early in this project an AI tool supplied three holography citations that were misattributed: a DOI prefix that resolved to SIGGRAPH 2024 rather than the claimed April 2026 paper, and an arXiv ID that was a January 2024 optical-tweezers paper rather than display holography. Building on those would have wasted weeks.

Cite only IDs confirmed present in `deepseek_research.md` or fetched directly. Tag vendor pricing, part numbers and non-arXiv figures explicitly (`[U-PRICE]`, `[U-PN]`, `[U-SPEC]`). When a number is computed rather than sourced, show the formula and inputs so it can be checked independently.

---

## 3. State which architecture a constraint applies to

**The most expensive error on this project so far.** The Lagrange invariant `N_x = 4·y·u/λ` was computed for a broadcast display filling ±20° simultaneously, yielding "a 4K panel is 82× short" — and that conclusion was reported as a fundamental physical wall. It is correct arithmetic for an architecture this project had already explicitly rejected. Under the eye-tracked architecture actually specified, the same formula gives 2,727 pixels against 3,840 available: a 1.41× *surplus*. The two answers differ by 116×, exactly the view count.

A constraint is not a property of the physics alone; it is a property of physics *plus* the configuration you evaluate it in. Always name the configuration.

---

## 4. Report your own errors in the same document that contained them

Corrections are appended in place with a dated caveat rather than silently overwritten, so anyone re-reading a conclusion sees what it used to say and why it changed. Instances so far: the thermal ceiling (6-face/50 °C → 5-face/48 °C, and a 60 °C shell reclassified as a safety violation), the tracked-vs-broadcast Lagrange correction above, and the S1.5 quality metric (PSNR measured Gerchberg–Saxton speckle rather than resolution, reported as a metric failure rather than searching for a metric that agreed with the hypothesis).

---

## 5. A negative result is a decision, not a failure

The most valuable outputs of this project's research have been exclusions: laser-plasma ruled out on power (25–250× outside the thermal envelope, which no efficiency improvement closes), AIRR bounded by unit magnification, the 4f layout killed on f = 680 mm arithmetic, and the aperture constraint `W = D·(b/a)` that bounds where an image may appear. Each removed a branch that would otherwise have consumed months. Record them as prominently as positive findings.
