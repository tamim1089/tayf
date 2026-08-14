# Enclosure — Physical Layout

Ties the block diagram in `docs/architecture.md` to physical component placement inside the 10×10×10cm volume. Apple-minimalist industrial design direction lives in `design/README.md`; this doc is the engineering constraint layer underneath it.

## Component volume competition

The cube's six faces and interior volume are claimed by, in rough priority order:

1. **Optical engine** (hackathon-track light-field/AIP panel) — needs at least one full face as its emissive/display surface, likely the face oriented toward the other participant/chair.
2. **Camera array** — 3-4 modules per `hardware/camera-rig.md`, tiled across the front face and one adjacent face; competes for face real estate with the optical engine if both want the same-facing surface (the display face and the "look at the room" capture face are not necessarily the same face — needs resolving once the panel's viewing-angle spec is known).
3. **Edge SoC + thermal solution** — interior volume, needs airflow path per `hardware/power-thermal.md` once that's populated.
4. **Radio module + antenna** — interior, with antenna placement sensitive to enclosure material (metal Apple-style unibody vs a radio-transparent window/insert — open item, see `design/README.md`).
5. **Power input** (USB-PD) — one exposed port, minimal per the Apple-minimalist brief.

## Open items

1. Resolve display-face vs capture-face conflict once the optical engine vendor/viewing-angle spec is known (`hardware/optical-engine.md`).
2. Antenna placement vs enclosure material — needs a decision on enclosure material (metal vs radio-transparent composite) that doesn't exist yet.
3. Serviceability/assembly approach (does the cube open, and how) — not addressed yet, deliberately deferred until the above are settled since it constrains everything else.
