# Phone App — Scope

## Purpose

Two jobs only, per the original concept: (1) pair with a TAYF cube, (2) set the capture boundary (the box the local cube should treat as "the subject," per `pipeline/capture/README.md`). Deliberately not a full companion app — Apple-minimalist means doing less, not adding a dashboard.

## Platform recommendation: SwiftUI, iOS-first

Reasoning, stated as a recommendation the user can override, not a silent decision:

- The design brief (`design/README.md`) is explicitly Apple-minimalist glassmorphism — SwiftUI's native materials (`.ultraThinMaterial` etc.) get this for close to free; cross-platform frameworks would mean rebuilding Apple's own visual language by hand.
- Solo builder, hackathon timeline (`docs/roadmap.md`) — one platform, one codebase, no cross-platform abstraction tax.
- A hackathon demo only needs to work on the builder's own phone, not ship broadly — Android support is a real product concern for later, not a Sep 13 concern.

## Flow

1. **Pair** — discover and connect to a cube (local network or a short-range pairing step; mechanism TBD once radio/firmware specifics are settled in `hardware/bom.md`/`firmware/README.md`).
2. **Set boundary** — live camera preview from the cube (or a simple on-device AR box) lets the user draw/adjust the capture volume described in `hardware/camera-rig.md`.
3. **Enroll** (first use only) — kick off the ~1-2 min avatar enrollment capture described in `pipeline/avatar/README.md`.
4. **Start/end call** — thin control surface; the actual call happens cube-to-cube, not through the phone.

## Body-region selection (fidelity/bandwidth tradeoff)

Per `research/notes.md` §37-38: the phone is a controller, not required hardware during a call — but at session setup it can expose a fidelity/cost tradeoff by letting the user pick which body regions get high-fidelity treatment:

- **Full body** — default, no region prioritization.
- **High-fidelity mode** — face, eyes, mouth, hands, fingers prioritized; lower-saliency regions (clothing, hidden geometry) get reduced fidelity. This maps directly to `docs/theory.md`'s perceptual-allocation principle and to `pipeline/avatar/README.md`'s representation budget — the app isn't rendering anything itself, it's setting a priority weighting the capture/representation pipeline already needs to support.
- **Custom region** (head / hands / upper body / torso) — narrows the capture boundary itself (the same box-drawing flow as step 2 above), trading full-body presence for guaranteed quality on a smaller region, useful in a constrained-bandwidth or constrained-compute demo scenario.

This setting is transmitted once at call setup, not renegotiated per-frame — it configures `pipeline/capture/README.md` and `pipeline/avatar/README.md`'s fidelity budget for the session.

## Open items

1. Pairing mechanism not decided — depends on radio hardware choice.
2. No UI has been built — this is a scope doc, not a design file (see `design/tokens.md` for the visual system once UI work starts).
3. Body-region selection's actual effect on `pipeline/schema.py`'s fixed 215-float schema is unresolved — the schema is currently fixed-size; a true fidelity tradeoff might mean varying which sub-estimators run (`pipeline/capture/README.md`) rather than changing the wire format itself. Needs resolving before this feature is implemented, not just specified.
