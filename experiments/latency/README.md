# Latency Validation

Validates the <150ms end-to-end budget (`docs/theory.md`, `pipeline/transport/README.md`) stage by stage — the <150ms figure is ITU-T G.114's one-way conversational threshold, a design target, not yet a measured result on TAYF hardware.

## Stage breakdown to instrument

```
Capture -> Processing -> Encoding -> Network -> Decoding -> Rendering -> Optical Output
```

Each stage gets its own timestamp; the budget is not "150ms total, allocate however" but a per-stage accounting so a regression can be traced to its actual source rather than treated as one opaque number.

## Reference point

Mon3tr measures ~80ms end-to-end on PC-class sender + Quest3-class receiver hardware — with a real breakdown (13.78ms worker execution, 2.13ms sync, 1.27ms smoothing for the capture-side estimators alone). TAYF's equivalent breakdown is unmeasured on the actual target hardware (Jetson-class edge SoC, per `hardware/bom.md`) — this is explicitly flagged as unvalidated risk in `pipeline/README.md` and `pipeline/capture/README.md`.

## Protocol

1. Instrument every stage boundary in `pipeline/` once implemented.
2. Run on the actual target edge SoC, not the remote RTX 5060 (dev/training only per `hardware/bom.md`) — a PC-class benchmark here would repeat Mon3tr's own limitation rather than answer TAYF's real question.
3. Identify which stage consumes the largest share of the budget on embedded hardware specifically — expected candidate: the parallel pose/face/hand estimators (`pipeline/capture/README.md`), since Mon3tr's own numbers show that stage dominating even on non-embedded hardware.
4. Add the optical-engine driver's own latency (frame-to-photon time) once `hardware/optical-engine.md`'s panel is sourced — this stage has no reference number yet at all.

## Status

Not started — blocked on `pipeline/` implementation and hardware arrival.
