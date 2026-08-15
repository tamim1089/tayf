"""
Gor'kov potential, force and trap characterization on top of the array field.

Model notes Sec 3. Ledger C-30..C-32, C-70..C-72.
"""
import numpy as np

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "03_PHYSICS"))
from constants import (C_AIR, RHO_AIR, ETA_AIR, BEAD_RADIUS, RHO_BEAD,
                       LAMBDA, HALF_LAMBDA)

C_BEAD = 1000.0   # m/s, EPS speed of sound (ASSUMED, ledger C-16 note)

F1 = 1.0 - RHO_AIR * C_AIR**2 / (RHO_BEAD * C_BEAD**2)
F2 = 2.0 * (RHO_BEAD - RHO_AIR) / (2.0 * RHO_BEAD + RHO_AIR)


def velocity_from_pressure(p, grad_p):
    """Acoustic particle velocity from pressure and its gradient:
    rho_air * dv/dt = -grad p  =>  v = i*grad(p) / (rho_air * omega)."""
    omega = 2 * np.pi * 40e3
    return 1j * grad_p / (RHO_AIR * omega)


def gorkov_potential(p, grad_p):
    """Gor'kov potential U at points given complex pressure p (N,) and
    complex gradient grad_p (N,d). Returns (N,) in J.
    U = 2*pi*r^3*rho*c^2 * (f1*p^2/(3*rho^2*c^4) - f2*v^2/(2*c^2)) with
    v^2 = |grad p|^2/(rho*omega)^2. (Fix 2026-08-15: velocity term had an
    erroneous extra c^2 factor; lateral well was underestimated by c^2.)"""
    v2 = np.einsum("ni,ni->n", grad_p, grad_p.conj()).real / (RHO_AIR * 2 * np.pi * 40e3) ** 2
    p2 = np.abs(p) ** 2
    c2 = C_AIR**2
    pref = 2 * np.pi * BEAD_RADIUS**3 * RHO_AIR * c2
    return pref * (F1 * p2 / (3 * RHO_AIR**2 * c2**2)
                   - F2 * v2 / (2 * c2))


def complex_gradient(f, h=0.1e-3):
    """Central-difference gradient of a scalar complex field sampled on a
    regular grid with spacing h along every axis; works for 2D and 3D grids
    (field[i0,i1] or field[i0,i1,i2]). Edge cells use one-sided differences
    via replicated edges."""
    fp = np.pad(f, 1, mode="edge")
    g = np.empty(f.shape + (f.ndim,), dtype=complex)
    for ax in range(f.ndim):
        sl_hi = [slice(1, -1)] * f.ndim
        sl_lo = [slice(1, -1)] * f.ndim
        sl_hi[ax] = slice(2, None)
        sl_lo[ax] = slice(None, -2)
        g[..., ax] = (fp[tuple(sl_hi)] - fp[tuple(sl_lo)]) / (2 * h)
    return g


def trap_properties_from_field(field_fn, center=(0.0, 0.0, 0.0), extent=1.2e-3,
                               steps=21, delta=0.012, amp=1.0, sep=0.234):
    """Characterize the trap at `center`: grid U on [center-extent, center+extent],
    find the U minimum (trap center), then axial (z) and lateral (x) stiffness
    via quadratic fit, and the well depth to the adjacent saddle.
    Returns dict with k_ax, k_lat, U_depth, center_shift_m, and the U profile."""
    axis = np.linspace(-extent, extent, steps)
    Z, Y, X = np.meshgrid(axis, axis, axis, indexing="ij")
    pts = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1) + np.array(center)
    p = field_fn(pts)
    p3 = p.reshape(steps, steps, steps)
    U3 = gorkov_potential(p.ravel(), complex_gradient(p3, h=axis[1] - axis[0]).reshape(-1, 3))
    U = U3.reshape(steps, steps, steps)
    i_min = np.unravel_index(np.argmin(U), U.shape)
    cmin = (np.array([axis[i_min[0]], axis[i_min[1]], axis[i_min[2]]]) + np.asarray(center)).tolist()

    # quadratic fits along the three principal axes through the min
    iz, iy, ix = i_min
    k = {}
    for name, ax_idx in (("z", iz), ("y", iy), ("x", ix)):
        prof = U[iz, iy, ix]  # placeholder to keep shape logic uniform
        # extract the line along the axis through the min
        if name == "z":
            line = U[:, iy, ix] - U[iz, iy, ix]
        elif name == "y":
            line = U[iz, :, ix] - U[iz, iy, ix]
        else:
            line = U[iz, iy, :] - U[iz, iy, ix]
        A = np.polyfit(axis - axis[ax_idx], line, 2)[0]
        k[name] = 2.0 * A  # U = A*dx^2 -> k = 2A
    k_ax, k_lat = k["z"], max(k["x"], k["y"])
    # well depth: min(U) to min over the cell edges along z (adjacent node)
    depth = (U[iz, iy, ix] - np.min(U[[0, -1], iy, ix]) if iz > 0 and iz < steps - 1
             else U[iz, iy, ix] - np.min(U))
    return dict(k_ax=k_ax, k_lat=k_lat, U_depth=abs(depth),
                center_shift=tuple(cmin), min_idx=(iz, iy, ix),
                U_grid=U, axis=axis)
