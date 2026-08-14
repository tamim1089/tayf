# Bandwidth Validation

Validates `pipeline/transport/README.md`'s target numbers (<0.2 Mbps, per Mon3tr) against TAYF's actual implementation — the reference numbers are citations from someone else's system, not yet measured on this one.

## Protocol

1. Instrument `pipeline/schema.py`'s pack/compress path end-to-end: raw 868 bytes/frame → FP16 → LZ4 → wire bytes actually sent.
2. Measure sustained Mbps across a representative conversational session (talking, moving, gesturing) — not just a static-pose best case, since compressibility likely varies with motion (temporal-delta-style gains, if `pipeline/transport/README.md` adds delta encoding, would show up here).
3. Compare against Mon3tr's <0.2Mbps reference — flag any material gap and investigate whether it's the compression stage or TAYF's specific 215-float schema layout.
4. Repeat over the CAMARA QoD-guaranteed path (`agent/README.md`) and best-effort Wi-Fi, since the agent layer's value proposition is partly about consistency under a guaranteed slice, not just raw throughput.

## Success metric

Sustained bandwidth within the same order of magnitude as Mon3tr's reference number, measured on TAYF's actual `pipeline/`, not assumed from the citation.

## Status

Not started — blocked on `pipeline/transport/README.md`'s implementation (currently a spec doc, no code).
