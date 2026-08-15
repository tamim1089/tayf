# Thermal Branch

Created 2026-08-15. `docs/04_CUBE_HARDWARE_AND_PROTOTYPE_ENGINEERING.md` flagged that this branch was missing entirely despite heat being the binding constraint on the whole form factor — an experiments programme with no thermal branch was measuring everything except the thing most likely to force a redesign.

## Why this branch exists

The optical budget closes (`docs/01_SYSTEM_MASTER_SPEC.md` §4 — the SBP gap is 1.3–1.7× broadcast, a surplus when tracked). The thermal budget does not. **≈16 W is the realistic ceiling** for a sealed 100 mm metal enclosure held to the ~48 °C IEC touch limit across ~5 participating faces, and a full-capability configuration draws ~27.3 W → a 63 °C shell, a 1.9× overshoot.

The binding limit is **human skin, not silicon.** Junction temperature is comfortable at 25 W; the shell is a safety violation well before that. This inverts the usual embedded-design intuition and is the single most important thing to keep in mind here.

## Research questions

1. **What is the real ceiling?** The 16 W figure comes from a first-order model with an assumed convection coefficient and participating-face count. Measure it on a real enclosure mock-up with resistive heaters standing in for components.
2. **Does thermal mass genuinely buy a call?** Modelling says 8–11 minutes at full capability before the shell reaches the touch limit — roughly the length of a phone call. If real, it **reframes TAYF as a call device rather than an always-on one**, which is a product decision disguised as a thermal one. This is the highest-value question in the branch.
3. **How much does emissivity actually move it?** Modelling says a polished Apple-style unibody costs ~40% of total heat rejection versus anodized. Measure it, because it gives the industrial-design brief a thermal veto (`design/README.md` is already updated).
4. **What does a 7 W compute profile cost in capability?** Named in doc 04 as *the highest-value untested hardware question in the project* — a lower-power SoC profile or a discrete NPU may close the gap outright without changing the enclosure.
5. **Is forced air genuinely excluded?** Doc 04 rules it out on three independent grounds — volume (~90 cm³ in an interior already ~93% packed), dust ingress (vents plus ~20 optical surfaces in a folded coherent path), and acoustics (~25 dBA beside a conversation). Confirm at least the acoustic and dust arguments empirically before accepting a permanent architectural exclusion.
6. **Where do the hotspots actually sit?** Lumped models say nothing about whether the SoC cooks the camera modules feeding capture, or the SLM.

## Protocol

1. **T1 — Instrumented mock-up.** Machined/printed enclosure at 100, 130, 150 mm with resistive heaters at component positions; thermocouples on shell faces and at each heater; sweep input power; record steady-state shell temperature and time-to-limit.
2. **T2 — Finish comparison.** Identical mock-up, different surface finishes (bare polished, anodized, matte dark). Isolates the emissivity term.
3. **T3 — Transient / duty cycle.** Power profile matching a real call (bursty, not steady). Measures question 2 directly.
4. **T4 — Real component thermal map.** Once V1 hardware exists, thermal camera under real workload rather than resistive stand-ins.
5. **T5 — Acoustic measurement** of any candidate active cooling, at conversational distance, in a quiet room.

## Required instrumentation

Thermocouples or RTDs plus a multi-channel logger, bench PSU with power measurement, thermal camera, sound level meter (for T5), and an ambient-temperature-controlled space — an uncontrolled room invalidates every measurement here.

## Relationship to simulation

`simulation/s3_thermal/thermal_sweep.py` is the first-order model this branch tests. Its `DT_ACCEPTABLE = 25 K` case (50 °C shell) is **above the metal touch limit** and is retained only for sensitivity analysis — it is not a design point. Any disagreement between T1 and the model is resolved in favour of T1, and the model is corrected.

## Status

Not started. Blocked on nothing but time and a mock-up — this branch needs no optical components, no avatar pipeline, and no network. **It is the cheapest branch to start and the most likely to force a design change**, which is a strong argument for starting it before anything optical is ordered.
