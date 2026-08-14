# Power / Thermal Budget — Worksheet

**Status: structure only, real numbers not yet filled in.** This is blocking for `hardware/enclosure.md` and for finalizing `hardware/bom.md`'s edge-SoC choice.

## Why this matters more than it looks

A sealed ~1000cm³ enclosure running continuous edge-AI inference (multiple parallel pose/face/hand estimators, per `pipeline/capture/README.md`) has very little surface area to reject heat passively. This is the real engineering bottleneck of the "10cm cube" constraint — not the algorithms, which are already proven at real-time rates on non-thermally-constrained hardware (Mon3tr's PC-class sender).

## Worksheet (fill in once BOM is confirmed)

| Component | Power draw (TDP, W) | Duty cycle | Heat to reject (W) |
|---|---|---|---|
| Edge SoC (Jetson Orin Nano Super-class) | TBD once `hardware/bom.md` confirms exact module | continuous | TBD |
| Cameras (×3-4) | TBD | continuous | TBD |
| 5G modem | TBD | bursty | TBD |
| Optical engine (hackathon-track panel) | TBD | continuous while displaying | TBD |
| **Total** | | | **TBD** |

## Cooling options to evaluate against the total above

- Passive (heat spreader to enclosure shell) — likely insufficient for continuous edge-SoC inference at Jetson Orin Nano-class TDP; include only if total is very low.
- Forced-air (small fan) — adds noise and an ingress/moving-part reliability concern inside a consumer device, but is the most likely candidate given expected SoC TDP.
- Vapor chamber — better performance/volume tradeoff than forced-air but adds cost and lead time; consider only if forced-air proves acoustically unacceptable for a device meant to sit next to a conversation.

## Open items

1. Cannot proceed past "TBD" until `hardware/bom.md`'s edge-SoC and camera line items are confirmed with real datasheet TDP figures.
2. Once populated, this worksheet drives the enclosure's physical layout in `hardware/enclosure.md` (vent placement, component spacing for airflow).
3. Battery vs USB-PD-tethered operation is not yet decided — affects whether "power draw" needs a battery-capacity/runtime column too.
