# Cross-Branch — Angular Resolution / Minimum Physical View Count

Directly targets `pipeline/view_synthesis/README.md`'s open research question: what is the minimum number of physical optical channels required when neural view synthesis fills the angular gaps?

## Protocol

1. Start with the optical engine chosen in `hardware/optical-engine.md` (task #9) at its native physical view count N.
2. Progressively mask/disable physical views and rely on `pipeline/view_synthesis/README.md`'s interpolation to fill the gap, measuring perceptual quality degradation (via `experiments/perceptual-quality/README.md`'s methodology) as N decreases.
3. Identify the knee point — where quality degrades sharply rather than gracefully — as the practical minimum channel count for this class of optical engine.
4. Repeat across static geometry, rotating geometry, and (once available) real avatar output, since interpolation difficulty likely differs between rigid test objects and a deforming human.

## Why this matters beyond curiosity

If the minimum viable channel count is meaningfully lower than the sourced panel's native count, that's a real cost/power/size lever for a future hardware revision — it turns "the panel is what it is" into "we know exactly how much of the panel's capability we actually need."

## Status

Not started — blocked on `hardware/optical-engine.md` panel sourcing (task #9) and `pipeline/view_synthesis/README.md`'s implementation.
