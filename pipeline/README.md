# Pipeline — Module Map

Software implementing the sender/receiver halves of `docs/architecture.md`'s pipeline diagram. This is the part of TAYF with the least open research risk — every stage here is backed by cited, measured prior art (`research/deepseek_research.md`).

## Modules

- **`capture/`** — camera ingestion + pose/face/hand estimation. See `capture/README.md`.
- **`avatar/`** — canonical avatar enrollment + Gaussian-attribute rig. See `avatar/README.md`.
- **`schema.py`** — the driving-parameter wire format shared between sender and receiver. Import this, don't redefine the packet shape elsewhere.
- **`transport/`** — packing, compression, and the WebRTC/CAMARA QoD data path. See `transport/README.md`.
- **`requirements.txt`** — pinned, license-clean dependency list.

## Data flow

```
capture/ (3-4 cam streams)
    -> pose/face/hand estimators (parallel)
    -> schema.py DrivingState (215 floats)
    -> transport/ (FP16 + LZ4, WebRTC data channel over CAMARA QoD slice)
    -> [network] ->
    -> transport/ (decompress, decode)
    -> avatar/ (LBS + Gaussian-attribute animation against the enrolled canonical avatar)
    -> hardware/optical-engine.md driver
```

## License posture

Every dependency in `requirements.txt` is Apache-2.0 or MIT. SMPL-X and its derivatives are deliberately excluded (non-commercial license) — see `pipeline/avatar/README.md` and project task "Commit to license-clean avatar model."

## Target numbers (from Mon3tr, arXiv 2601.07518 — the closest published reference architecture)

- Bandwidth: <0.2 Mbps sustained
- End-to-end latency: ~80ms
- Frame rate: ~60fps target (measured on Quest3-class receiver SoC; unvalidated on the Jetson-class edge SoC TAYF actually targets — see `hardware/bom.md`)
