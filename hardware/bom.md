# Bill of Materials — Candidate Components

**Status: UNVERIFIED pricing/availability.** The online research pass tasked with confirming real vendor part numbers and current pricing was killed mid-run before writing anything (see project task list). Nothing below should be ordered until that pass is rerun. What follows is engineering-judgment candidate selection — the *class* of part is a defensible choice, the specific SKU/price is not confirmed.

## Cameras (per cube)

- **Candidate class:** 3-4× synchronized global-shutter sensor modules, MIPI-CSI, hardware-triggered sync.
- **Candidate sensors:** Sony IMX296 / IMX568 class (global shutter, machine-vision grade).
- **Why global shutter, not rolling:** the capture volume includes fast hand/face motion; rolling shutter skew would corrupt the pose estimators' input.
- **Open item:** exact count/placement — see `hardware/camera-rig.md`.

## Edge compute

- **Candidate:** NVIDIA Jetson Orin Nano Super-class module.
- **Why:** the only realistic candidate that runs the pose/face/hand estimators plus avatar-animation inference inside a passively-or-lightly-cooled 10cm enclosure. Mon3tr's published numbers (arXiv 2601.07518) assume a PC-class sender GPU and a Quest3-class (Snapdragon XR2) receiver SoC — neither has been validated at Jetson-class embedded compute. This is real risk, not a solved substitution (see `docs/roadmap.md` open items).
- **Explicitly not this:** the remote RTX 5060 is dev/training/enrollment only, never the deployed runtime.

## Radio

- **Candidate:** 5G modem module with carrier-side CAMARA QoD support; Wi-Fi fallback for indoor demo reliability independent of live 5G coverage.

## Optical engine

- **Hackathon track:** compact light-field or retroreflective aerial-imaging panel. No vendor/part search done yet — this is the first item for the rerun research pass. **Software feasibility is no longer a question mark**: arXiv 2506.08064 is an already-working open-source webcam-to-Looking-Glass-Portrait pipeline naming video conferencing as its use case (see `experiments/light-field/README.md`) — this narrows the remaining hackathon-track risk down to actual panel sourcing/pricing, not "can this even be driven in real time."
- **North-star track:** femtosecond fiber laser + galvo/MEMS scanner. Explicitly out of scope for hardware ordering until `hardware/optical-engine.md`'s eye-safety section is resolved.

## Power / thermal

- USB-PD input. Cooling solution (forced-air vs vapor chamber) depends on the thermal budget calculation in `hardware/power-thermal.md`, not yet done.

## Blocking items before any order is placed

1. Rerun the killed online-research pass for real part numbers and pricing.
2. Finish `hardware/camera-rig.md` FOV math to fix the camera count.
3. Finish `hardware/power-thermal.md` to size the cooling solution.
4. Decide the hackathon-track optical engine (`hardware/optical-engine.md`).
