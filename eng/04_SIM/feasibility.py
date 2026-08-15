"""
Feasibility oracle: given a path + motion limits + trap model, decide whether
the bead can follow it without loss of trap, and at what refresh rate.

Feeds the capacity experiment (05_AVATAR/capacity_experiment.py).
Ledger: C-33 (the contested 37.5 cm usable-path claim), PRD-08/09/12.
"""
import numpy as np

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "04_SIM"))
from particle import simulate, DELTA_P_ESC, ESC_AX, TrapSpring
from trajectory import timing_law, piecewise_linear_interp, MotionLimits


def run_feasibility(path, limits: MotionLimits, spring: TrapSpring,
                    t_loop=None, dt=1.0 / 16000.0, u_dist=(0.0, 0.0, 0.0),
                    scale=1.0, seed=0, a_ellipsoid=None):
    """Simulate one loop traversal of `path` (N,3). If t_loop is given, the
    path is re-timed to fit exactly in t_loop (constant-speed per vertex
    rescaled); otherwise the physics-limited timing law is used.
    Returns dict: feasible, refresh_hz, loop_time, follow_err_max,
    err_p95, loss_count, max_a, max_v, margin (per-axis escape)."""
    path = np.asarray(path, dtype=float) * scale
    if t_loop is not None:
        # fit path into the loop: uniform rescale of vertex times
        d, s = arc_lengths(path)
        n = len(path)
        # speed chosen so that total time == t_loop
        seg_time = d / max(d.sum(), 1e-12) * t_loop
        vt = np.concatenate([[0.0], np.cumsum(seg_time)])
        v_eff = d / np.maximum(seg_time, 1e-12)
        trap_fn = piecewise_linear_interp(path, vt)
    else:
        v, vt, ttot = timing_law(path, limits, a_ellipsoid=a_ellipsoid)
        trap_fn = piecewise_linear_interp(path, vt)
        t_loop = ttot

    sim = simulate(trap_fn, t_loop, dt=dt, spring=spring, u_dist=u_dist)
    refresh = 1.0 / t_loop
    # per-axis margin: worst axis of (p95 err / escape distance)
    xs = sim["x"]
    xt = np.array([np.asarray(trap_fn(t)) for t in sim["t"]])
    err_ax = np.abs(xs - xt)
    frac = err_ax / ESC_AX
    margin = 1.0 - np.percentile(np.max(frac, axis=1), 95)
    return dict(
        feasible=sim["loss_count"] == 0 and margin > 0,
        refresh_hz=refresh, loop_time=t_loop,
        follow_err_max=float(np.nanmax(sim["err"])),
        follow_err_p95=float(np.nanpercentile(sim["err"], 95)),
        loss_count=sim["loss_count"],
        max_a=sim["max_a"], max_v=sim["max_v"],
        margin=float(margin),
    )


def arc_lengths(points):
    d = np.linalg.norm(np.diff(points, axis=0), axis=1)
    return d, np.concatenate([[0.0], np.cumsum(d)])


def max_refresh_for_path(path, limits: MotionLimits, spring: TrapSpring,
                         min_refresh=1.0, max_refresh=20.0, dt=1.0 / 16000.0,
                         tol=0.1, u_dist=(0.0, 0.0, 0.0)):
    """Bisect over loop time: find the fastest loop that keeps the bead in
    the trap (loss_count == 0 and margin > tol). Returns (max_refresh_hz,
    result_dict at that loop, full scan)."""
    lo, hi = 1.0 / max_refresh, 1.0 / min_refresh   # loop times
    best = None
    for _ in range(24):
        tmid = np.sqrt(lo * hi)
        r = run_feasibility(path, limits, spring, t_loop=tmid, dt=dt,
                            u_dist=u_dist)
        if r["feasible"]:
            best = r
            hi = tmid  # try faster
        else:
            lo = tmid
    if best is None:
        best = run_feasibility(path, limits, spring, t_loop=lo, dt=dt, u_dist=u_dist)
    return best["refresh_hz"], best
