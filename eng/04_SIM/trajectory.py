"""
Trajectory command generation: parameterize an arbitrary 3D path and assign
time via an S-curve (jerk-limited) speed profile clamped to class
velocity/acceleration limits (OptiTrap-class timing, model notes Sec 7).
Output: trap_cmd_fn(t) usable by particle.simulate.

S-curve profile: triangular-jerk acceleration phases (0 -> a_max -> 0)
followed by constant acceleration, then cruise; symmetric deceleration.
This suppresses the undamped (zeta ~ 3e-5) bead ringing that fixed-accel
ramps excite (validation ladder R3/R4 finding, 2026-08-15).

Ledger: C-10 (corner cap 0.75 m/s), C-08, C-09, C-33 (contested 37.5 cm).
"""
import math
import numpy as np


class MotionLimits:
    """Per-motion-class kinematic limits. Visual-only mode per SPIE 2020:
    v_max 3.75 m/s horizontal (C-08), a_max 141 m/s^2 (C-09),
    corner v_max 0.75 m/s (C-10). Vertical can reach 8.75 m/s (C-07)."""

    def __init__(self, v_max=3.75, a_max=141.0, corner_v=0.75, j_max=None):
        self.v_max = v_max
        self.a_max = a_max
        self.corner_v = corner_v
        self.j_max = j_max if j_max else a_max / 0.05  # reach a_max in 50 ms

    def speed_limit(self, curvature: np.ndarray, v_max=None):
        """Speed limit along the path from curvature (centripetal bound):
        v_centr = sqrt(a_max / curvature). Blended with the corner cap at
        high-curvature points."""
        lim = v_max if v_max else self.v_max
        centr = np.sqrt(self.a_max / np.maximum(curvature, 1e-9))
        cap = np.where(curvature > 0, centr, lim)
        return np.minimum(cap, lim)


def curvature_of(points):
    """Curvature of a polyline via Menger curvature at interior vertices."""
    n = len(points)
    k = np.zeros(n)
    for i in range(1, n - 1):
        a = points[i - 1]; b = points[i]; c = points[i + 1]
        ab = b - a; bc = c - b
        area = np.linalg.norm(np.cross(ab, bc)) / 2.0
        denom = np.linalg.norm(ab) * np.linalg.norm(bc) * np.linalg.norm(c - a)
        k[i] = 4.0 * area / max(denom, 1e-12) if denom > 0 else 0.0
    return k


def arc_lengths(points):
    d = np.linalg.norm(np.diff(points, axis=0), axis=1)
    return d, np.concatenate([[0.0], np.cumsum(d)])


# ---------------------------------------------------------------------------
# S-curve primitives (speed change dv >= 0 with jerk limit j)
# ---------------------------------------------------------------------------
def s_curve_td(dv, a_max, j_max):
    """Time and distance for an S-curve speed change of dv (>=0)."""
    if dv <= 0:
        return 0.0, 0.0
    Tj = a_max / j_max
    dv1 = a_max * Tj            # speed gained by the two jerk phases
    if dv <= dv1:
        T = math.sqrt(dv / j_max)
        return 2.0 * T, dv * T
    T2 = (dv - dv1) / a_max
    t = 2.0 * Tj + T2
    s = dv1 * (Tj + T2) + 0.5 * a_max * T2 ** 2
    return t, s


def s_curve_dv_from_dist(s, a_max, j_max):
    """Largest speed change achievable within distance s (inverse of td)."""
    if s <= 0:
        return 0.0
    Tj = a_max / j_max
    dv1 = a_max * Tj
    s_j = dv1 * Tj              # distance for the pure-jerk profile
    if s <= s_j:
        # dv*T(dv) = s with T = sqrt(dv/j) -> dv = (s*sqrt(j))^(2/3)
        return (s * math.sqrt(j_max)) ** (2.0 / 3.0)
    # const-accel phase: s = dv1*(Tj+T2) + a*T2^2/2, dv = dv1 + a*T2
    b = dv1 + a_max * Tj
    # s = dv1*Tj + dv1*T2 + a*T2^2/2  ->  solve quadratic for T2
    c = dv1 * Tj - s
    T2 = (-dv1 + math.sqrt(max(dv1 ** 2 - 2 * a_max * c, 0.0))) / a_max
    return dv1 + a_max * T2


def s_curve_time_for_segment(v0, v1, seg_len, a_max, j_max):
    """Time to traverse a segment of length seg_len with endpoint speeds
    (v0, v1) under jerk-limited acceleration."""
    if seg_len <= 0:
        return 0.0
    v0 = max(v0, 0.0); v1 = max(v1, 0.0)
    d_acc = s_curve_td(v1 - v0, a_max, j_max)[1]
    if seg_len >= d_acc:
        t = s_curve_td(v1 - v0, a_max, j_max)[0]
        return t + (seg_len - d_acc) / max(v1, 1e-6)
    # short segment: peak speed v_p < v1 with d(v0,v_p) + d(v_p,v1) = seg_len
    lo, hi = 0.0, max(v0, v1)
    for _ in range(40):
        vp = 0.5 * (lo + hi)
        d1 = s_curve_td(vp - v0, a_max, j_max)[1]
        d2 = s_curve_td(v1 - vp, a_max, j_max)[1]
        if d1 + d2 < seg_len:
            lo = vp
        else:
            hi = vp
    vp = 0.5 * (lo + hi)
    return (s_curve_td(vp - v0, a_max, j_max)[0]
            + s_curve_td(v1 - vp, a_max, j_max)[0])


def timing_law(points, limits: MotionLimits, v_profile=None, dt=1e-4,
               a_ellipsoid=None):
    """Jerk-limited timing: integrate speed along the path with
    v = min(v_max, centripetal limit, v_profile), acceleration built up at
    the jerk limit (continuous accel profile - per-segment S-curve restarts
    caused accel jumps that rang the nearly-undamped bead, ladder R5/R7
    finding 2026-08-15). Two passes: forward (accel-limited), backward
    (brake-limited). a_ellipsoid (3,) -> per-segment a_max from the
    acceleration budget ellipsoid sum((a_i/a_op_i)^2) <= 1. Returns
    (v, t, total_t)."""
    d, s = arc_lengths(points)
    curv = curvature_of(points)
    v_lim = limits.speed_limit(curv)
    if v_profile is not None:
        v_lim = np.minimum(v_lim, v_profile)
    n = len(points)
    j = limits.j_max
    # per-segment acceleration limit (direction-resolved budget)
    if a_ellipsoid is None:
        a_seg = np.full(n, limits.a_max)
    else:
        a_ellipsoid = np.asarray(a_ellipsoid, dtype=float)
        u = np.diff(points, axis=0)
        ln = np.linalg.norm(u, axis=1)
        dirn = u / np.maximum(ln[:, None], 1e-12)
        w = (dirn / a_ellipsoid) ** 2
        a_seg = np.concatenate(
            [[limits.a_max], 1.0 / np.sqrt(np.maximum(w.sum(axis=1), 1e-30))])
    # forward pass: jerk-limited acceleration build-up
    v = np.zeros(n)
    a = np.zeros(n)
    for i in range(1, n):
        ds = d[i - 1]
        if ds <= 0:
            v[i] = v[i - 1]
            a[i] = a[i - 1]
            continue
        vmax = min(v_lim[i], math.sqrt(v[i - 1] ** 2
                   + 2 * min(a_seg[i], a_seg[i - 1]) * ds))
        a_target = max((vmax ** 2 - v[i - 1] ** 2) / (2 * ds), 0.0)
        a[i] = min(a_target, a[i - 1] + j * ds / max(v[i - 1], 1e-3))
        a[i] = max(a[i], 0.0)
        v[i] = math.sqrt(max(v[i - 1] ** 2 + 2 * a[i] * ds, 0.0))
    # backward pass: jerk-limited braking
    for i in range(n - 2, -1, -1):
        ds = d[i]
        if ds <= 0:
            v[i] = min(v[i], v[i + 1])
            continue
        vmax = min(v[i], math.sqrt(v[i + 1] ** 2
                   + 2 * min(a_seg[i], a_seg[i + 1]) * ds))
        a_req = (v[i + 1] ** 2 - vmax ** 2) / (2 * ds)
        a_brake = max(a_req, -j * ds / max(v[i + 1], 1e-3))
        v[i] = min(vmax, math.sqrt(max(v[i + 1] ** 2 + 2 * a_brake * ds, 0.0)))
    # rebuild time from segment mean speeds
    t = np.zeros(n)
    for i in range(1, n):
        if d[i - 1] > 0:
            vmean = max(0.5 * (v[i - 1] + v[i]), 1e-3)
            t[i] = t[i - 1] + d[i - 1] / vmean
        else:
            t[i] = t[i - 1]
    return v, t, t[-1]


def piecewise_linear_interp(vertices, vertex_t):
    """Build trap_cmd_fn(t) = linear interpolation of vertices at vertex_t.
    ZOH is applied by the simulator's sampling; here continuous command."""
    def fn(t):
        i = np.searchsorted(vertex_t, t, side="right") - 1
        i = np.clip(i, 0, len(vertices) - 2)
        t0, t1 = vertex_t[i], vertex_t[i + 1]
        if t1 <= t0:
            return vertices[i]
        f = (t - t0) / (t1 - t0)
        return vertices[i] + f * (vertices[i + 1] - vertices[i])
    return fn


def path_capacity(path_len, loop_time):
    """Refresh rate for a loop of given length and loop time."""
    return 1.0 / loop_time