# Firmware — Scope

**No firmware code exists yet, deliberately.** Nothing here is buildable until `hardware/camera-rig.md` and `hardware/bom.md` settle on real silicon — writing driver/boot code against unconfirmed hardware would be fake progress. This doc defines scope so implementation can start the moment hardware is confirmed.

## What runs at the firmware layer (below the pipeline in `pipeline/`)

1. **Boot flow** — edge SoC (Jetson Orin Nano Super-class, per `hardware/bom.md`) bring-up: bootloader → minimal OS → pipeline runtime start. Standard for the platform once chosen; not a custom bootloader project.
2. **Camera hardware-trigger sync** — the shared trigger line described in `hardware/camera-rig.md` needs a small driver/timing layer to fire all 3-4 sensors in lockstep and tag frames with a shared timestamp before they reach the capture module in `pipeline/capture/README.md`.
3. **Sensor drivers** — standard MIPI-CSI driver stack for whichever sensor `hardware/bom.md` confirms; expect to reuse vendor/kernel drivers rather than write new ones.
4. **Radio management** — 5G modem bring-up and handoff to the CAMARA-aware agent layer (`agent/README.md`) for QoD session state.
5. **Optical-engine driver** — panel-specific control interface once `hardware/optical-engine.md`'s hackathon-track panel is sourced; entirely vendor-dependent, cannot be scoped further until then.

## Explicit non-goals for the hackathon track

- No custom laser/scanner firmware — the north-star optical engine track (`hardware/optical-engine.md`) is out of scope for any near-term firmware work, and no laser-adjacent firmware gets written before the eye-safety analysis referenced there exists.
- No battery-management firmware unless `hardware/power-thermal.md` lands on battery-powered rather than USB-PD-tethered operation.

## Open items

Blocked entirely on hardware selection. Revisit once `hardware/bom.md`'s vendor pass is rerun and `hardware/camera-rig.md`/`hardware/optical-engine.md` have committed choices.
