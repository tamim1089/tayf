# Patent Strategy Notes

Source: `research/notes.md` §42-44. **This file is notes toward a strategy, not legal advice.** A professional prior-art search and a patent attorney must determine actual novelty and claim scope before any filing — nothing here substitutes for that.

## What not to attempt to patent

- "A hologram cube." Extensive prior art (Proto Hologram, Holoconnects, decades of Pepper's-ghost and volumetric-display work — see `patent/prior-art.md`).
- "Displaying a person holographically." Same problem — far too broad, far too anticipated.

## Where the actual novelty might be

Novelty, if it exists, is in specific *combinations*, not in the general concept of holographic telepresence. See `patent/invention-disclosure.md` for the four candidate inventive concepts drafted from `research/notes.md` §42.

## Timing warning — do not publicly disclose before filing

Public disclosure (GitHub included) can create patent complications depending on jurisdiction (most non-US jurisdictions have no grace period at all; US grace period is one year but should not be relied on as a strategy). This repo is currently public-repo-shaped (research files, architecture docs) — before pushing any of `patent/` or the more specific engineering detail in `hardware/optical-engine.md`/`pipeline/` to a public remote, resolve:

1. Whether any of `patent/invention-disclosure.md`'s four concepts are worth protecting.
2. If so, run a real prior-art search (`patent/prior-art.md` is a seed list, not a completed search) and get provisional-filing advice **before** further public disclosure.
3. Until that's resolved, treat this repository's remote-hosting status as an open question, not a default "push it to GitHub" assumption.

## Recommended process (per notes.md, adapted)

1. Maintain private invention records (this directory).
2. Document experiments (`experiments/`).
3. Run a real prior-art search (`patent/prior-art.md`).
4. Prepare an invention disclosure (`patent/invention-disclosure.md` — draft exists, needs attorney review).
5. Consider provisional/patent filing strategy with actual counsel.
6. Only then publish the corresponding technical material publicly.
