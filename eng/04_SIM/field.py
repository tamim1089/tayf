"""
Rayleigh-Sommerfeld field of the two opposed 16x16 arrays + twin-trap phase
law. Vectorized over transducers and evaluation points.

Model notes: eng/03_PHYSICS/model_notes.md, Sec 1-2. Ledger: C-01, C-02, C-05.
"""
import numpy as np
from scipy.special import j1

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "03_PHYSICS"))
from constants import (LAMBDA, ARRAY_N, ARRAY_PITCH, ARRAY_SEPARATION,
                       TRANSDUCER_RADIUS, TRANSDUCER_REF_PRESSURE, HALF_LAMBDA)


def element_positions(separation: float = ARRAY_SEPARATION) -> np.ndarray:
    """Returns (512, 3) transducer positions. Array 0 faces +z (bottom),
    Array 1 faces -z (top); grids on the x-y plane at z = +/-sep/2."""
    idx = np.arange(ARRAY_N)
    off = (ARRAY_N - 1) / 2.0
    xs = (idx - off) * ARRAY_PITCH
    X, Y = np.meshgrid(xs, xs)
    xy = np.stack([X.ravel(), Y.ravel()], axis=1)
    z0 = np.full((len(xy), 1), -separation / 2.0)
    z1 = np.full((len(xy), 1), +separation / 2.0)
    p0 = np.hstack([xy, z0])
    p1 = np.hstack([xy, z1])
    normals = np.zeros((len(p0) + len(p1), 3))
    normals[: len(p0), 2] = +1.0      # bottom array radiates +z
    normals[len(p0):, 2] = -1.0       # top array radiates -z
    return np.vstack([p0, p1]), normals


def twin_trap_phases(pts, normals, focus_a, focus_b, k):
    """Twin-trap phase law (Marzo-style): each element emits the sum of two
    foci at focus_a and focus_b with a pi offset, so the two focused fields
    cancel exactly at the midpoint -> pressure null (Gor'kov well) there.
    phi_n = arg( exp(-ik|r_n - a|) - exp(-ik|r_n - b|) )."""
    d_a = np.linalg.norm(pts - focus_a, axis=1)
    d_b = np.linalg.norm(pts - focus_b, axis=1)
    return np.angle(np.exp(-1j * k * d_a) - np.exp(-1j * k * d_b)) % (2 * np.pi)


def single_axis_phases(pts, focus, k):
    return (k * np.linalg.norm(pts - focus, axis=1)) % (2 * np.pi)


def directivity(theta: np.ndarray) -> np.ndarray:
    """Piston directivity D(theta) = 2*J1(ka sin t)/(ka sin t), D(0)=1."""
    x = LAMBDA / 2 / (TRANSDUCER_RADIUS * 2)  # not used; placeholder removed
    arg = 2 * np.pi * TRANSDUCER_RADIUS / LAMBDA * np.sin(theta)
    with np.errstate(divide="ignore", invalid="ignore"):
        d = np.where(np.abs(arg) > 1e-9, 2 * j1(arg) / np.where(arg == 0, 1, arg), 1.0)
    return d


def field_at(points, pts=None, normals=None, phases=None, amp=1.0):
    """Complex pressure at `points` (N,3) from 512 transducers with `phases`
    (512,) and amplitude scale `amp`. Returns (N,) complex."""
    if pts is None:
        pts, normals = element_positions()
    diff = points[:, None, :] - pts[None, :, :]       # (N,512,3)
    dist = np.linalg.norm(diff, axis=2)               # (N,512)
    cos_th = np.abs(np.sum(diff * normals[None, :, :], axis=2))  # (N,512)
    cos_th = np.abs(cos_th) / np.maximum(dist, 1e-12)
    th = np.arccos(np.clip(cos_th, 0.0, 1.0))
    k = 2 * np.pi / LAMBDA
    with np.errstate(divide="ignore"):
        amp_1m = TRANSDUCER_REF_PRESSURE / np.maximum(dist, 1e-9)
    phase = k * dist + phases[None, :]
    return (amp * amp_1m * directivity(th) * np.exp(1j * phase)).sum(axis=1)


def twin_trap_field(points, z_center=0.0, delta=None, sep=ARRAY_SEPARATION,
                    amp=1.0):
    """Field of a twin trap centered at (0,0,z_center), foci at
    z_center +- delta/2. Canonical delta = lambda/4 (ledger C-05)."""
    if delta is None:
        delta = LAMBDA / 4.0
    pts, normals = element_positions(sep)
    fa = np.array([0.0, 0.0, z_center + delta / 2.0])
    fb = np.array([0.0, 0.0, z_center - delta / 2.0])
    k = 2 * np.pi / LAMBDA
    ph = twin_trap_phases(pts, normals, fa, fb, k)
    return field_at(points, pts, normals, ph, amp)


def node_trap_field(points, focus, sep=ARRAY_SEPARATION, amp=1.0):
    """MATD display trap (PNAS 2018 HAT method, used by the MATD display):
    all elements focus on `focus`, then an extra pi phase delay is applied to
    the top array. The focus then becomes a pressure NODE of the standing
    wave between the two opposed arrays, where the bead traps. Localized
    3D well (axial from the standing wave, lateral from the focal envelope),
    unlike the planar-null twin trap."""
    pts, normals = element_positions(sep)
    k = 2 * np.pi / LAMBDA
    ph = (k * np.linalg.norm(pts - focus, axis=1)) % (2 * np.pi)
    top = normals[:, 2] < 0            # top array radiates -z
    ph[top] = (ph[top] + np.pi) % (2 * np.pi)
    return field_at(points, pts, normals, ph, amp)


def lattice_field(points, spacing=0.012, n=3, z_center=0.0, sep=ARRAY_SEPARATION,
                  amp=1.0, focus_center=(0.0, 0.0, 0.0)):
    """MATD display field: a grid of n x n x n node traps (pi-shifted foci)
    at lattice spacing `spacing` (1.4 lambda per PNAS 2018), centered at
    focus_center. The bead at the center rides in the well whose lateral
    walls are the neighboring traps' antinode rings. Per-element phase =
    argument of the complex sum of the per-trap phase laws."""
    pts, normals = element_positions(sep)
    k = 2 * np.pi / LAMBDA
    off = (n - 1) / 2.0
    idx = np.arange(n) - off
    cx, cy, cz = focus_center
    top = normals[:, 2] < 0
    S = np.zeros(len(pts), dtype=complex)
    n_tr = n ** 3
    for ix in idx:
        for iy in idx:
            for iz in idx:
                focus = np.array([cx + ix * spacing, cy + iy * spacing,
                                  cz + iz * spacing])
                d = np.linalg.norm(pts - focus, axis=1)
                ph = (k * d) % (2 * np.pi)
                ph[top] = (ph[top] + np.pi) % (2 * np.pi)
                S += np.exp(1j * ph) / np.sqrt(n_tr)
    phases = np.angle(S) % (2 * np.pi)
    return field_at(points, pts, normals, phases, amp)


def focused_field(points, focus, sep=ARRAY_SEPARATION, amp=1.0):
    """Single-focus field (all transducers to one focus)."""
    pts, normals = element_positions(sep)
    k = 2 * np.pi / LAMBDA
    ph = single_axis_phases(pts, focus, k)
    return field_at(points, pts, normals, ph, amp)
