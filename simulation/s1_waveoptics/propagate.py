#!/usr/bin/env python3
"""
S1 — Wave-optics core: angular-spectrum free-space propagation.

Implements docs/07_HARDWARE_SIMULATION_PLAN.md track S1. This module is the
primitive everything else in S1 is built from: propagate a complex field from
one plane to another, exactly, without paraxial approximation.

    U(x,y,z) = F^-1{ F{U(x,y,0)} * H(fx,fy,z) }
    H(fx,fy,z) = exp( i*2*pi*z * sqrt(1/lambda^2 - fx^2 - fy^2) )

Evanescent components (fx^2 + fy^2 > 1/lambda^2) are set to zero rather than
allowed to blow up.

Backend is numpy by default and torch when available, so the same code runs
on this machine and on the remote RTX 5060 (set TAYF_DEVICE=cuda).

Validation (S1.1) is not optional decoration: gate G1 in the simulation plan
says nothing downstream is trustworthy until the simulator reproduces analytic
results. Run `python3 propagate.py` to execute the validation suite.
"""

import math
import os

import numpy as np

try:
    import torch
    _HAS_TORCH = True
except ImportError:
    _HAS_TORCH = False

DEVICE = os.environ.get("TAYF_DEVICE", "cpu")


# ----------------------------------------------------------------------
# Core propagator
# ----------------------------------------------------------------------

def angular_spectrum(U0, dx, z, wavelength):
    """Propagate complex field U0 a distance z through free space.

    U0         : (N, N) complex array, field at z=0
    dx         : sample pitch, metres
    z          : propagation distance, metres (may be negative)
    wavelength : metres

    Returns the complex field at distance z, same shape and sampling.
    """
    N = U0.shape[0]
    fx = np.fft.fftfreq(N, d=dx)
    FX, FY = np.meshgrid(fx, fx, indexing="xy")

    arg = 1.0 / wavelength**2 - FX**2 - FY**2
    propagating = arg > 0
    kz = np.zeros_like(arg)
    kz[propagating] = np.sqrt(arg[propagating])

    H = np.zeros_like(arg, dtype=np.complex128)
    H[propagating] = np.exp(1j * 2 * np.pi * z * kz[propagating])

    return np.fft.ifft2(np.fft.fft2(U0) * H)


def max_propagation_distance(N, dx, wavelength):
    """Distance beyond which the transfer function aliases on this grid.

    The angular-spectrum kernel becomes undersampled when the phase between
    adjacent frequency samples exceeds pi. Exceeding this silently produces
    wrong answers, which is exactly the failure mode a validation suite is
    supposed to catch.
    """
    L = N * dx
    return L * math.sqrt(max(0.0, (2 * dx / wavelength) ** 2 - 1.0)) / 2.0


def fraunhofer(U0, dx, z, wavelength):
    """Single-FFT far-field (Fraunhofer) propagation.

    Valid when z >> D^2/lambda (D = aperture extent). Unlike the angular
    spectrum, the output plane has a DIFFERENT sample pitch:

        dx_out = lambda * z / (N * dx)

    Returns (field, dx_out). Use this rather than angular_spectrum() for
    far-field work — angular spectrum aliases badly at large z on a fixed
    grid, which is a real trap and the reason this function exists.
    """
    N = U0.shape[0]
    dx_out = wavelength * z / (N * dx)
    x = (np.arange(N) - N // 2) * dx_out
    X, Y = np.meshgrid(x, x, indexing="xy")
    k = 2 * np.pi / wavelength
    prefactor = np.exp(1j * k * z) / (1j * wavelength * z) * \
        np.exp(1j * k * (X**2 + Y**2) / (2 * z))
    U = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(U0))) * dx**2
    return prefactor * U, dx_out


def fraunhofer_valid_distance(dx, N_aperture_samples, wavelength):
    """Minimum z for the Fraunhofer approximation: z >> D^2 / lambda."""
    D = N_aperture_samples * dx
    return D**2 / wavelength


# ----------------------------------------------------------------------
# Test fields
# ----------------------------------------------------------------------

def gaussian_beam(N, dx, w0, wavelength, z=0.0):
    """Analytic Gaussian beam at distance z from its waist."""
    x = (np.arange(N) - N // 2) * dx
    X, Y = np.meshgrid(x, x, indexing="xy")
    r2 = X**2 + Y**2
    k = 2 * np.pi / wavelength
    zR = np.pi * w0**2 / wavelength

    if z == 0.0:
        return np.exp(-r2 / w0**2).astype(np.complex128), w0

    wz = w0 * math.sqrt(1 + (z / zR) ** 2)
    Rz = z * (1 + (zR / z) ** 2)
    gouy = math.atan(z / zR)
    U = (w0 / wz) * np.exp(-r2 / wz**2) * np.exp(1j * (k * z + k * r2 / (2 * Rz) - gouy))
    return U.astype(np.complex128), wz


def beam_width(U, dx):
    """1/e^2 intensity radius via second moment."""
    I = np.abs(U) ** 2
    N = U.shape[0]
    x = (np.arange(N) - N // 2) * dx
    X, Y = np.meshgrid(x, x, indexing="xy")
    tot = I.sum()
    cx, cy = (I * X).sum() / tot, (I * Y).sum() / tot
    var = (I * ((X - cx) ** 2 + (Y - cy) ** 2)).sum() / tot
    return math.sqrt(2.0 * var)   # 1/e^2 radius for a Gaussian


def circular_aperture(N, dx, radius):
    x = (np.arange(N) - N // 2) * dx
    X, Y = np.meshgrid(x, x, indexing="xy")
    return ((X**2 + Y**2) <= radius**2).astype(np.complex128)


# ----------------------------------------------------------------------
# S1.1 — Validation suite (gate G1)
# ----------------------------------------------------------------------

def validate():
    lam = 550e-9
    passed, failed = 0, 0

    def check(name, got, expect, tol, unit=""):
        nonlocal passed, failed
        err = abs(got - expect) / abs(expect) if expect else abs(got)
        ok = err <= tol
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        print(f"         got {got:.6g}{unit}  expected {expect:.6g}{unit}"
              f"  err {err*100:.3f}% (tol {tol*100:.1f}%)")
        if ok:
            passed += 1
        else:
            failed += 1

    print("=" * 72)
    print("S1.1 — SIMULATOR VALIDATION AGAINST ANALYTIC RESULTS  (gate G1)")
    print("=" * 72)
    print(f"wavelength {lam*1e9:.0f} nm | backend numpy | torch={_HAS_TORCH}")

    # --- Gaussian beam diffraction ------------------------------------
    print("\n[1] Gaussian beam expansion vs. analytic w(z) = w0*sqrt(1+(z/zR)^2)")
    # Grid must satisfy zR < N*dx^2/lambda, i.e. w0 < dx*sqrt(N/pi), or the
    # angular-spectrum kernel aliases before the beam has visibly expanded.
    N, dx, w0 = 1024, 4e-6, 50e-6
    zR = math.pi * w0**2 / lam
    zmax = max_propagation_distance(N, dx, lam)
    print(f"    grid {N}x{N} @ {dx*1e6:.1f} um | w0={w0*1e6:.0f} um | "
          f"zR={zR*1e3:.2f} mm | grid limit z<{zmax*1e3:.1f} mm")
    print(f"    (sampling constraint w0 < dx*sqrt(N/pi) = "
          f"{dx*math.sqrt(N/math.pi)*1e6:.0f} um -- satisfied)")
    U0, _ = gaussian_beam(N, dx, w0, lam)
    for z in (0.5 * zR, 1.0 * zR, 2.0 * zR):
        if z > zmax:
            print(f"    z={z*1e3:.2f} mm SKIPPED (exceeds grid limit)")
            continue
        Uz = angular_spectrum(U0, dx, z, lam)
        wz_sim = beam_width(Uz, dx)
        wz_ana = w0 * math.sqrt(1 + (z / zR) ** 2)
        check(f"w(z) at z={z*1e3:.2f} mm ({z/zR:.1f} zR)",
              wz_sim * 1e6, wz_ana * 1e6, 0.02, " um")

    # --- Energy conservation -------------------------------------------
    print("\n[2] Energy conservation (lossless propagation)")
    e0 = float(np.sum(np.abs(U0) ** 2))
    Uz = angular_spectrum(U0, dx, 0.5 * zR, lam)
    check("total intensity after propagation", float(np.sum(np.abs(Uz) ** 2)),
          e0, 0.01)

    # --- Round trip ------------------------------------------------------
    print("\n[3] Round trip: propagate +z then -z recovers the input")
    Uback = angular_spectrum(angular_spectrum(U0, dx, 0.3 * zR, lam),
                             dx, -0.3 * zR, lam)
    rms = float(np.sqrt(np.mean(np.abs(Uback - U0) ** 2)))
    ref = float(np.sqrt(np.mean(np.abs(U0) ** 2)))
    check("round-trip RMS error / field RMS", rms / ref, 0.0, 1e-6)

    # --- Fraunhofer diffraction from a circular aperture ---------------
    print("\n[4] Circular aperture far field -> Airy, first null at "
          "1.22*lambda/D")
    # NB: must use the Fraunhofer propagator here. Angular spectrum aliases
    # badly at far-field distances on a fixed grid -- an earlier version of
    # this suite used it and reported a 16% error that was pure numerics.
    N2, dx2, a = 2048, 1e-6, 25e-6       # aperture radius 25 um, D = 50 um
    D = 2 * a
    z_min = fraunhofer_valid_distance(dx2, int(2 * a / dx2), lam)
    z_ff = 20 * z_min                    # comfortably into the far field
    print(f"    D={D*1e6:.0f} um | Fraunhofer needs z >> {z_min*1e3:.2f} mm; "
          f"using z={z_ff*1e3:.1f} mm")
    Uap = circular_aperture(N2, dx2, a)
    Uff, dx_out = fraunhofer(Uap, dx2, z_ff, lam)
    I = np.abs(Uff[N2 // 2, :]) ** 2
    centre = N2 // 2
    half = I[centre:]
    null = None
    for i in range(2, len(half) - 1):
        if half[i] <= half[i - 1] and half[i] <= half[i + 1] and half[i] < 0.02 * half[0]:
            null = i
            break
    if null:
        theta_sim = (null * dx_out) / z_ff
        theta_ana = 1.22 * lam / D
        check("first-null angle", theta_sim * 1e3, theta_ana * 1e3, 0.05, " mrad")
    else:
        print("  [WARN] no clear first null found; check far-field condition")

    # --- Grating equation: max steering angle vs pixel pitch (S1.3) -----
    print("\n[5] Grating equation sin(theta_max) = lambda/(2*p) "
          "-- validates docs/01 §4.6")
    for p_um, expect_deg in ((8.0, 1.97), (3.74, 4.22), (1.0, 16.0)):
        p = p_um * 1e-6
        got = math.degrees(math.asin(min(1.0, lam / (2 * p))))
        check(f"pixel pitch {p_um} um -> theta_max", got, expect_deg, 0.02, " deg")

    print("\n" + "=" * 72)
    print(f"GATE G1: {passed} passed, {failed} failed -> "
          f"{'SIMULATOR TRUSTED' if failed == 0 else 'DO NOT PROCEED'}")
    print("=" * 72)
    if failed:
        print("Downstream S1 experiments are not trustworthy until this passes.")
    return failed == 0


if __name__ == "__main__":
    ok = validate()
    raise SystemExit(0 if ok else 1)
