# Idea Capture Template — Draft

Due Aug 23, 2026 (GSMA MENA Ignite Hackathon, Idea Phase close). This draft uses the honest two-track framing from `docs/roadmap.md` as the core narrative — a working, measured 90% plus a scoped, physics-literate 10% R&D roadmap — deliberately not an oversold "hologram cube" claim that collapses under a judge's first technical question.

## The idea, one sentence

Two identical ~10cm cubes capture their local users and exchange compact dynamic human representations — 215 numbers a second, not video — so each cube can reconstruct the remote person locally instead of streaming their image.

## What's actually novel and working today

The capture→avatar→compression→transport pipeline (`docs/architecture.md`) is not speculative: the closest published reference architecture (Mon3tr, arXiv 2601.07518) measures <0.2 Mbps bandwidth and ~80ms end-to-end latency for exactly this kind of parametric telepresence stream, over 1000x less bandwidth than volumetric/point-cloud streaming approaches. TAYF's contribution is packaging this into a dedicated capture+display appliance rather than a headset-bound software stack, and pairing it with CAMARA's network APIs so the stream gets a guaranteed-latency path instead of best-effort routing.

## The CAMARA / agentic layer

`agent/README.md`'s loop uses Nokia Network-as-Code's Congestion Insights to predict network conditions 15 minutes ahead and proactively request a QoD session or network slice before call quality degrades — genuinely forward-looking behavior, not a reactive QoS config with an "agent" label on it.

## The honest open problem

Reconstructing the remote person as literal free-space light (not on a screen) is an open research question, not a solved engineering task — the best published compact result (JSID 2025 fist-sized laser-plasma display) reaches sparse, iconic-density output, not photoreal video. The hackathon prototype terminates the pipeline in a compact light-field/retroreflective panel instead (`hardware/optical-engine.md`), and the pitch says so directly: this is the acknowledged next research target, with the physics already scoped, not a hidden gap.

## Theme fit

[Carries over from earlier: Theme 7, Open Innovation — separated families / migrant workers use case. Needs revisiting/confirming against the actual submission categories before Aug 23.]

## Open items before submission

1. Confirm theme/category selection is still current.
2. Fill in the team/solo-builder section per the hackathon's actual template fields (not yet transcribed here — need the original template document).
3. Tighten to whatever word/field limits the real template imposes — this draft is content, not final formatting.
