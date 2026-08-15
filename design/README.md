# Design Principles — Apple-Minimalist, Non-Skitchy

Source directive (verbatim intent, not softened): follow Apple's minimalist glassmorphism philosophy, skip unnecessary decoration, don't over-design. This applies to the phone app (`app/`) now and the cube's physical industrial design (`hardware/enclosure.md`) later.

## Rules, stated as restraint, not ornamentation

1. **One material language.** Translucent/blurred surfaces (glassmorphism) as the *only* surface treatment — no competing skeuomorphic textures, gradients-as-decoration, or drop-shadow stacking. See `design/tokens.md` for the concrete blur/corner-radius values.
2. **Type carries hierarchy, not color.** Weight and size differentiate importance; color is reserved for state (active call, capture-boundary edit mode) not decoration.
3. **No chrome that isn't function.** Every visible control does something specific to the two jobs in `app/README.md` (pair, set boundary). If a screen has a control that isn't pairing, boundary-setting, enrollment, or call start/end, it doesn't belong in the hackathon build.
4. **Motion is confirmation, not entertainment.** Transitions communicate state change (boundary saved, call connecting) — no motion added purely for polish.
5. **The physical cube inherits the same restraint** — per `hardware/enclosure.md`, one visible port (power), no visible fasteners/vents unless `hardware/power-thermal.md`'s cooling solution requires them, in which case they get designed in, not bolted on as an afterthought.

## Constraint conflict: surface finish is a thermal decision

Simulation (`simulation/s3_thermal/thermal_sweep.py`, summarized in `docs/01_SYSTEM_MASTER_SPEC.md` §5.2) found that enclosure emissivity moves the entire thermal budget by 69%: a matte dark shell (ε≈0.9) rejects 21.2 W at 100 mm/50 °C, while polished bare metal (ε≈0.05) rejects only 12.5 W. Since the whole device has to fit inside roughly 12–21 W, **more than half the thermal budget is decided by the finish.**

A polished aluminium unibody — the most obvious reading of the Apple-minimalist brief — is therefore not a free aesthetic choice. Rule 5 above ("the physical cube inherits the same restraint") stands, but is now qualified: **the shell must be a high-emissivity finish** (matte, anodized, or dark), and any brief-conforming design must achieve its minimalism through form, proportion, and absence of ornament rather than through a mirror-polished metal surface. If a polished finish is ever required for product reasons, the enclosure must grow or gain active cooling to pay for it — that tradeoff belongs to `hardware/power-thermal.md`, not to this document.

## Non-goals

Not building a full brand system (logo variations, marketing site, etc.) for the hackathon — that's scope the solo timeline (`docs/roadmap.md`) doesn't support and the pitch (`pitch/`) doesn't need.
