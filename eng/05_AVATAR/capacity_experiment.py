"""
Phase 5 capacity experiment (VV-08 / SIM-01): for each motion class, build
the wireframe frame, partition into per-bead tours (6 time-multiplexed
traps, C-19), time each tour with the ring-limited trajectory law, and
report the refresh rate 1/max(tour_time). Then Monte Carlo over the
uncertain parameters (k_lat ratio, bead density, disturbance, gain) and
report the p95 margin vs the PRD-08 gate (10 Hz min, 12.5 Hz target,
>= 20 % margin for verdict A).

Run:  python3 eng/05_AVATAR/capacity_experiment.py [--sweep N] [--quick]
Ledger: C-33 (37.5 cm contested claim resolved here), PRD-08/09/13.
"""
import sys, pathlib, argparse
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "04_SIM"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "03_PHYSICS"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[0] / "05_AVATAR"))

import numpy as np
from path_builder import CLASSES, frame_segments, bead_tours
from particle import simulate, TrapSpring, ESC_AX, M_BEAD, GAMMA
from trajectory import MotionLimits, timing_law, piecewise_linear_interp

N_BEADS = 6
TARGET_HZ = 12.5
MIN_HZ = 10.0
MARGIN_GATE = 0.20


def a_op_ellipsoid(k_ax, k_lat, m):
    """Ring-limited operating accelerations per axis (model notes Sec 4):
    a_op = 0.9 * k*ESC/(2*m), vertical capped at 100 m/s^2."""
    return np.array([min(100.0, 0.9 * k_lat * ESC_AX[0] / (2.0 * m)),
                     min(100.0, 0.9 * k_lat * ESC_AX[1] / (2.0 * m)),
                     min(100.0, 0.9 * k_ax * ESC_AX[2] / (2.0 * m))])


def class_refresh(class_name, k_ax, k_lat, m, n_beads=N_BEADS,
                  u_dist=(0.0, 0.0, 0.0), dt=1.0 / 16000.0):
    """Frame timing for one class at model parameters: worst tour time,
    plus a verification sim of the worst tour. Returns dict."""
    c = CLASSES[class_name]
    # worst-case frame: sample the loop densely, take the longest tour time
    spring = TrapSpring(k_ax=k_ax, k_lat_ratio=max(k_lat / k_ax, 0.02))
    ell = a_op_ellipsoid(k_ax, k_lat, m)
    worst = dict(loop=0.0, refresh=0.0)
    ts = np.linspace(0, c["T"], 21)
    worst_tour_time = 0.0
    worst_tour = None
    for t in ts:
        segs = frame_segments(class_name, t)
        paths, _ = bead_tours(segs, n_beads)
        limits = MotionLimits(v_max=c["v_max"])
        for p in paths:
            vp, vt, ttot = timing_law(p, limits, a_ellipsoid=ell)
            if ttot > worst_tour_time:
                worst_tour_time = ttot
                worst_tour = p
    # verify the worst tour with the full particle sim
    limits = MotionLimits(v_max=c["v_max"])
    vp, vt, ttot = timing_law(worst_tour, limits, a_ellipsoid=ell)
    fn = piecewise_linear_interp(worst_tour, vt)
    sim = simulate(fn, ttot, dt=dt, spring=spring, u_dist=u_dist,
                   x0=worst_tour[0], v0=np.zeros(3))
    refresh = 1.0 / worst_tour_time
    return dict(refresh_hz=refresh, loop_time=worst_tour_time,
                loss_count=sim["loss_count"], margin=sim["loss_count"] == 0,
                tour_len=float(np.linalg.norm(np.diff(worst_tour, axis=0), axis=1).sum()),
                worst_tour_time_sim=ttot)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", type=int, default=0,
                    help="Monte Carlo samples per class (0 = nominal only)")
    ap.add_argument("--quick", action="store_true", help="coarse sweep")
    args = ap.parse_args()

    # nominal point (Phase 4 calibration): EPS 1 mm bead
    m0 = M_BEAD
    k_ax0 = 0.01772
    r_lat0 = 9.664e-4 / 0.01772
    print(f"nominal: k_ax={k_ax0:.4f} N/m  k_lat/k_ax={r_lat0:.3f}  "
          f"m={m0:.2e} kg  n_beads={N_BEADS}")
    results = {}
    for name in CLASSES:
        r = class_refresh(name, k_ax0, k_ax0 * r_lat0, m0)
        results[name] = r
        print(f"  {name:14s} refresh={r['refresh_hz']:6.2f} Hz  "
              f"loop={r['loop_time']*1e3:6.1f} ms  tour={r['tour_len']*1e3:5.1f} mm  "
              f"loss={r['loss_count']}")

    # verdict framing at nominal
    ok_all = all(r["refresh_hz"] >= TARGET_HZ * (1 + MARGIN_GATE)
                 for r in results.values())
    print(f"\nnominal verdict frame: all classes >= {TARGET_HZ*1.2:.1f} Hz "
          f"(12.5*1.2)? {'YES' if ok_all else 'NO'}")

    if args.sweep:
        # Monte Carlo: k_lat ratio [0.05, 1.0] log, gain [-3, +3] dB,
        # bead density [10, 60], disturbance |u| <= 0.3 m/s, jitter 0-1 update
        rng = np.random.default_rng(7)
        n = args.sweep
        per_class = {name: [] for name in CLASSES}
        if args.quick:
            rng = np.random.default_rng(3)
            n = max(8, n // 3)
        for _ in range(n):
            r_lat = 10 ** rng.uniform(np.log10(0.05), 0.0)
            gain_db = rng.uniform(-3.0, 3.0)
            rho = rng.uniform(10.0, 60.0)
            m = 4 / 3 * np.pi * (1e-3) ** 3 * rho
            k_ax = k_ax0 * 10 ** (gain_db / 10.0)
            u = rng.uniform(0, 0.3) * (rng.random(3) - 0.5) * 2
            for name in CLASSES:
                r = class_refresh(name, k_ax, k_ax * r_lat, m, u_dist=u)
                per_class[name].append(r["refresh_hz"])
        print(f"\nMonte Carlo p95 (n={n}):")
        for name in CLASSES:
            arr = np.array(per_class[name])
            print(f"  {name:14s} p95={np.percentile(arr, 95):6.2f} Hz  "
                  f"p05={np.percentile(arr, 5):6.2f} Hz  "
                  f"median={np.median(arr):6.2f} Hz")

    return results


if __name__ == "__main__":
    main()