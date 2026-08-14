# Agent — Mandatory Hackathon AI Layer

**Read `agent/compliance.md` before writing any code in this directory.** The hackathon's mandatory AI Resource & Tooling Guide constrains what this layer is allowed to be built from, and it is easy to violate by default.

## What this layer does

Not part of the media pipeline (`pipeline/`). It watches network conditions and proactively manages the CAMARA network APIs so a TAYF call gets a guaranteed-latency path instead of best-effort routing — this is what makes it an *agent* rather than a fixed QoS config, per the hackathon's own framing.

## Loop

1. **Predict:** call `congestion_insights.query()` for the device — CAMARA's congestion prediction covers the *upcoming 15 minutes*, not just current state. This forward-looking property is the actual agentic behavior: the system acts before congestion hits, not after latency already degraded.
2. **Decide:** if predicted congestion is Medium/High for the call's device, or the `transport/` module reports a degrading-conditions signal, request a QoD session (or escalate to a network slice for a scheduled/predictable high-value session — e.g. a demo).
3. **Act:** `qod.create_session_v1(...)` for the call duration; `extend_session_v1(...)` if the call runs long; `delete_session_v1(...)` on hangup. See `agent/nac_client.py` for verified call patterns.
4. **Fallback:** if no QoD/slice is available (e.g. Wi-Fi-only demo environment), the call proceeds best-effort — the agent degrades gracefully rather than blocking the call.

## Why this satisfies the hackathon's CAMARA requirement

Uses Nokia Network-as-Code: QoD (`client.qod`), Congestion Insights (`client.congestion_insights`), and Network Slicing (`client.slice`) — all real CAMARA APIs, not simulated. Portal registration is still outstanding (project task #2) — required before any of this can run against real (or sandbox) endpoints.

## Open items

1. Portal registration (task #2) — blocks everything in this directory from running.
2. Decision logic thresholds (what congestion level triggers what action) are not tuned — first pass will be simple threshold rules, not learned.
