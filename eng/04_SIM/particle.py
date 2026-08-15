"""
Particle dynamics: RK4 integration of the trap-particle system with Stokes
drag, gravity, ambient disturbance, force saturation and zero-order-held
trap commands (phase-update discretization).

Model notes Sec 4-6. Ledger C-17, C-18, C-30..C-34, C-60.
"""
import numpy as np

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "03_PHYSICS"))
from constants import (BEAD_RADIUS, RHO_BEAD, ETA_AIR, G, LAMBDA, PHASE_UPDATE_RATE,
                       bead_mass, drag_coefficient)

M_BEAD = bead_mass(BEAD_RADIUS, RHO_BEAD)
GAMMA = drag_coefficient(BEAD_RADIUS)
DELTA_P_ESC = LAMBDA / 8.0          # 1.072 mm - model notes Sec 3
# Per-axis escape distances: axial = node-to-barrier (lambda/4 = 2.14 mm),
# lateral = lattice half-period (12 mm spacing / 2 = 6 mm, PNAS 2018 1.4
# lambda min trap separation). The bead leaves the well when it crosses
# these; the spring saturates at k*esc on each axis.
ESC_AX = np.array([0.012 / 2.0, 0.012 / 2.0, LAMBDA / 4.0])


class TrapSpring:
    """Local harmonic trap with per-axis saturation; parameters from gorkov
    characterization + calibration. Force model (model notes Sec 5):
        F_i = -k_i*dx_i capped at k_i*ESC_AX_i (well edge)."""

    def __init__(self, k_ax=2.2e-3, k_lat_ratio=0.5):
        self.k_ax = k_ax
        self.k_lat = k_ax * k_lat_ratio
        self.k = np.array([self.k_lat, self.k_lat, self.k_ax])
        self.f_max = self.k * ESC_AX
        self.k_lat_ratio = k_lat_ratio

    def force(self, x, x_trap):
        dx = np.asarray(x) - np.asarray(x_trap)
        f = -self.k * dx
        # per-axis saturation at the well edge
        over = np.abs(f) > self.f_max
        f[over] = np.sign(f[over]) * self.f_max[over]
        return f


def step_rk4(state, trap_cmd_fn, t, dt, spring: TrapSpring, u_dist=(0.0, 0.0, 0.0),
             gravity=True):
    """One RK4 step of x'' = (F_trap + F_drag + F_g)/m. state = [x, v].
    trap_cmd_fn(t) -> trap position, or None when the slot is off (no trap
    force; time-multiplexed slots)."""
    x, v = state

    def acc(x_, v_, t_):
        xt = trap_cmd_fn(t_)
        a = np.zeros(3)
        if xt is not None:
            xt = np.asarray(xt)
            a = spring.force(x_, xt) / M_BEAD
        a -= GAMMA * (v_ - np.asarray(u_dist)) / M_BEAD
        if gravity:
            a = a + np.array([0.0, 0.0, -G])
        return a

    k1 = acc(x, v, t)
    x2 = x + 0.5 * dt * v
    v2 = v + 0.5 * dt * k1
    k2 = acc(x2, v2, t + 0.5 * dt)
    x3 = x + 0.5 * dt * v2
    v3 = v + 0.5 * dt * k2
    k3 = acc(x3, v3, t + 0.5 * dt)
    x4 = x + dt * v3
    v4 = v + dt * k3
    k4 = acc(x4, v4, t + dt)
    v_new = v + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    x_new = x + (dt / 6.0) * (v + 2 * v2 + 2 * v3 + v4)
    return np.array([x_new, v_new])


def simulate(trap_cmd_fn, t_end, dt=1.0 / PHASE_UPDATE_RATE,
             spring: TrapSpring = None, x0=None, v0=None,
             u_dist=(0.0, 0.0, 0.0), gravity=True, track_every=1):
    """Integrate the bead under a ZOH-sampled trap command. Returns dict:
    t, x (N,3), v (N,3), err (N,), loss_count, loss_times, max_a, max_v."""
    if spring is None:
        spring = TrapSpring()
    if x0 is None:
        x0 = np.array([0.0, 0.0, 0.0])
    if v0 is None:
        v0 = np.array([0.0, 0.0, 0.0])
    n = int(t_end / dt)
    ts = np.arange(n) * dt
    xs = np.empty((n, 3)); vs = np.empty((n, 3))
    state = np.array([x0, v0])
    loss_count = 0
    loss_times = []
    max_a = 0.0
    max_v = 0.0
    # ZOH: sample trap command at update instants
    for i, t in enumerate(ts):
        xt_cmd = trap_cmd_fn(t)
        if xt_cmd is not None:
            xt = np.asarray(xt_cmd)
            dx = np.abs(state[0] - xt)
            if np.any(dx >= ESC_AX):
                loss_count += 1
                if len(loss_times) < 20:
                    loss_times.append(t)
            a = spring.force(state[0], xt) / M_BEAD
        else:
            a = np.zeros(3)
        a -= GAMMA * (state[1] - np.asarray(u_dist)) / M_BEAD
        if gravity:
            a = a + np.array([0.0, 0.0, -G])
        max_a = max(max_a, np.linalg.norm(a))
        max_v = max(max_v, np.linalg.norm(state[1]))
        xs[i] = state[0]; vs[i] = state[1]
        state = step_rk4(state, trap_cmd_fn, t, dt, spring, u_dist, gravity)
    errs = np.full(n, np.nan)
    for i, t in enumerate(ts):
        xt_cmd = trap_cmd_fn(t)
        if xt_cmd is not None:
            errs[i] = np.linalg.norm(xs[i] - np.asarray(xt_cmd))
    return dict(t=ts, x=xs, v=vs, err=errs, loss_count=loss_count,
                loss_times=loss_times, max_a=max_a, max_v=max_v)


def calibrate_pressure(k_ax_target, k_ax_measured):
    """Field amplitude scale g such that measured stiffness hits the target
    (stiffness scales quadratically with field amplitude)."""
    return np.sqrt(k_ax_target / max(k_ax_measured, 1e-30))
