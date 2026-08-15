#!/usr/bin/env python3
"""
S3 — Thermal envelope of a sealed TAYF enclosure.

Implements docs/07_HARDWARE_SIMULATION_PLAN.md tracks S3.1 (reproduce the
lumped model in docs/01_SYSTEM_MASTER_SPEC.md §5) and S3.3 (sweep edge length
to find the size that actually closes the budget).

Thermal is the binding constraint on the TAYF form factor: a sealed 100 mm
cube rejects only ~12.4 W at a 40 C surface, and a Jetson-class SoC alone
draws 7-15 W. This script answers: what edge length does a real component
set require?

Model: steady-state lumped network, sealed enclosure, still air.

    Q_total = Q_convection + Q_radiation
    Q_convection = h * A * dT
    Q_radiation  = eps * sigma * A * (T_s^4 - T_amb^4)

Natural-convection h for a vertical/horizontal plate in still air is
5-10 W/m^2K; 8.0 is used as the nominal and swept in sensitivity(). This is
a first-order model deliberately: it is meant to size the problem and force
an early design decision, not to replace CFD. Escalate to Elmer/OpenFOAM
only if the answer comes out marginal.

Usage:
    python3 thermal_sweep.py              # full report
    python3 thermal_sweep.py --json       # machine-readable
"""

import argparse
import json
import math

SIGMA = 5.670374419e-8   # Stefan-Boltzmann, W/m^2K^4
T_AMB_C = 25.0           # ambient, C
EMISSIVITY = 0.90        # anodized/painted enclosure
H_CONV_NOMINAL = 8.0     # natural convection, W/m^2K (still air, 5-10 typical)

# Surface temperature limits. Above ~45 C a handheld object reads as "hot";
# 50 C is the practical ceiling for a device a person sits next to, and
# IEC 60950-style touch-temperature guidance for metal is stricter still.
DT_COMFORTABLE = 15.0    # 40 C surface
DT_ACCEPTABLE = 25.0     # 50 C surface
DT_LIMIT = 35.0          # 60 C surface - too hot to hold

# Candidate component power draws (W). Every number here is a datasheet-class
# figure and is marked with its confidence; see hardware/bom.md, where all
# vendor/pricing lines remain UNVERIFIED pending a real sourcing pass.
COMPONENTS = {
    # name:                (typ_W, max_W, confidence)
    "Jetson Orin Nano":    (7.0,  15.0, "datasheet power modes 7W/15W"),
    "Jetson Orin NX":      (10.0, 25.0, "datasheet power modes 10W/25W"),
    "Cameras 4x GS":       (1.2,   2.0, "~0.3-0.5W per MIPI module, ESTIMATE"),
    "5G modem":            (2.0,   5.0, "bursty; ESTIMATE"),
    "LCoS SLM + driver":   (3.0,   6.0, "ESTIMATE - highly device dependent"),
    "Illumination/laser":  (2.0,  10.0, "ESTIMATE - depends on mechanism"),
    "Misc (PMIC, sensors)":(1.0,   2.0, "ESTIMATE"),
}

CONFIGS = {
    "hackathon-panel": ["Jetson Orin Nano", "Cameras 4x GS", "5G modem",
                        "Misc (PMIC, sensors)"],
    "holographic-nano": ["Jetson Orin Nano", "Cameras 4x GS", "5G modem",
                         "LCoS SLM + driver", "Illumination/laser",
                         "Misc (PMIC, sensors)"],
    "holographic-nx":  ["Jetson Orin NX", "Cameras 4x GS", "5G modem",
                        "LCoS SLM + driver", "Illumination/laser",
                        "Misc (PMIC, sensors)"],
}


def dissipation(edge_m, dT, h=H_CONV_NOMINAL, emis=EMISSIVITY, t_amb_c=T_AMB_C):
    """Steady-state heat a sealed cube of given edge length can reject."""
    area = 6.0 * edge_m ** 2
    t_amb_k = t_amb_c + 273.15
    t_s_k = t_amb_k + dT
    q_conv = h * area * dT
    q_rad = emis * SIGMA * area * (t_s_k ** 4 - t_amb_k ** 4)
    return {"area_m2": area, "q_conv_W": q_conv, "q_rad_W": q_rad,
            "q_total_W": q_conv + q_rad, "surface_C": t_amb_c + dT}


def required_edge(power_W, dT, h=H_CONV_NOMINAL, emis=EMISSIVITY):
    """Smallest edge length that rejects power_W at the given rise.

    Q scales as edge^2 for both terms, so solve directly rather than iterate.
    """
    unit = dissipation(1.0, dT, h, emis)["q_total_W"]   # W at edge = 1 m
    return math.sqrt(power_W / unit)


def config_power(name):
    typ = sum(COMPONENTS[c][0] for c in CONFIGS[name])
    mx = sum(COMPONENTS[c][1] for c in CONFIGS[name])
    return typ, mx


def report():
    out = {}
    print("=" * 74)
    print("S3 — TAYF THERMAL ENVELOPE")
    print("=" * 74)
    print(f"ambient {T_AMB_C:.0f} C | emissivity {EMISSIVITY} | "
          f"h {H_CONV_NOMINAL} W/m2K (still air)")

    # ---- S3.1: reproduce the master-spec table -------------------------
    print("\n[S3.1] Dissipation of a sealed 100 mm cube "
          "(reproduces docs/01 §5)")
    print(f"  {'dT':>4} {'surface':>9} {'conv':>8} {'rad':>8} {'TOTAL':>9}")
    s31 = []
    for dT in (DT_COMFORTABLE, DT_ACCEPTABLE, DT_LIMIT):
        d = dissipation(0.100, dT)
        print(f"  {dT:4.0f}K {d['surface_C']:8.0f}C {d['q_conv_W']:7.2f}W "
              f"{d['q_rad_W']:7.2f}W {d['q_total_W']:8.2f}W")
        s31.append({"dT_K": dT, **d})
    out["s3_1_100mm"] = s31

    # ---- component budgets ---------------------------------------------
    print("\n[S3.2] Candidate configuration power draw")
    cfgs = {}
    for name in CONFIGS:
        typ, mx = config_power(name)
        cfgs[name] = {"typ_W": typ, "max_W": mx}
        print(f"  {name:20s} typ {typ:5.1f} W   max {mx:5.1f} W")
    print("  NOTE: every non-SoC figure is an ESTIMATE. See hardware/bom.md —")
    print("        no component enters the BOM without a measured power number.")
    out["s3_2_configs"] = cfgs

    # ---- S3.3: the sweep that decides the industrial design ------------
    print("\n[S3.3] Can a given edge length reject a given configuration?")
    edges_mm = [100, 125, 150, 175, 200, 250, 300]
    for dT, label in ((DT_COMFORTABLE, "40 C surface — comfortable"),
                      (DT_ACCEPTABLE, "50 C surface — acceptable ceiling")):
        print(f"\n  --- dT = {dT:.0f} K ({label}) ---")
        header = "  edge   budget  " + "  ".join(f"{n[:14]:>14s}" for n in CONFIGS)
        print(header)
        for mm in edges_mm:
            d = dissipation(mm / 1000.0, dT)
            cells = []
            for name in CONFIGS:
                typ, _ = config_power(name)
                margin = d["q_total_W"] - typ
                mark = "OK " if margin >= 0 else "NO "
                cells.append(f"{mark}{margin:+9.1f}W".rjust(14))
            print(f"  {mm:3d}mm {d['q_total_W']:6.1f}W  " + "  ".join(cells))

    # ---- required sizes -------------------------------------------------
    print("\n[S3.3b] Minimum edge length required (typical draw)")
    req = {}
    for name in CONFIGS:
        typ, mx = config_power(name)
        row = {}
        for dT, lbl in ((DT_COMFORTABLE, "40C"), (DT_ACCEPTABLE, "50C")):
            e_typ = required_edge(typ, dT) * 1000
            e_max = required_edge(mx, dT) * 1000
            row[lbl] = {"typ_mm": e_typ, "max_mm": e_max}
            print(f"  {name:20s} @{lbl}: {e_typ:6.0f} mm (typ) | "
                  f"{e_max:6.0f} mm (peak {mx:.0f}W)")
        req[name] = row
    out["s3_3_required_edge"] = req

    # ---- sensitivity ----------------------------------------------------
    print("\n[S3.4] Sensitivity of the 100 mm budget to model assumptions "
          f"(dT={DT_ACCEPTABLE:.0f}K)")
    print("  convection coefficient h (still air 5-10; forced air 25-100):")
    for h in (5.0, 8.0, 10.0, 25.0, 50.0):
        d = dissipation(0.100, DT_ACCEPTABLE, h=h)
        tag = "  <- forced air" if h >= 25 else ""
        print(f"    h={h:5.1f} W/m2K -> {d['q_total_W']:6.2f} W{tag}")
    print("  emissivity (0.05 bare polished metal .. 0.95 matte black):")
    for e in (0.05, 0.5, 0.9, 0.95):
        d = dissipation(0.100, DT_ACCEPTABLE, emis=e)
        print(f"    eps={e:4.2f}      -> {d['q_total_W']:6.2f} W")

    # ---- verdict --------------------------------------------------------
    print("\n" + "=" * 74)
    print("VERDICT")
    print("=" * 74)
    d100_40 = dissipation(0.100, DT_COMFORTABLE)["q_total_W"]
    d100_50 = dissipation(0.100, DT_ACCEPTABLE)["q_total_W"]
    print(f"  A sealed 100 mm cube rejects {d100_40:.1f} W at 40 C surface, "
          f"{d100_50:.1f} W at 50 C.")
    print()
    print("  Does 100 mm close?  (typ = sustained draw, peak = all rails maxed)")
    print(f"  {'config':22s} {'40C typ':>9} {'40C peak':>9} "
          f"{'50C typ':>9} {'50C peak':>9}")
    verdicts = {}
    for name in CONFIGS:
        typ, mx = config_power(name)
        cells, vs = [], {}
        for dT, lbl in ((DT_COMFORTABLE, "40C"), (DT_ACCEPTABLE, "50C")):
            budget = dissipation(0.100, dT)["q_total_W"]
            for p, plbl in ((typ, "typ"), (mx, "peak")):
                ok = budget >= p
                cells.append(("PASS" if ok else "FAIL").rjust(9))
                vs[f"{lbl}_{plbl}"] = ok
        verdicts[name] = vs
        print(f"  {name:22s} " + " ".join(cells))

    print()
    print("  READ THIS CAREFULLY — the answer is marginal, not binary:")
    print("   * 100 mm PASSES for every config at sustained/typical draw IF a")
    print("     50 C surface is acceptable. That is hot to the touch but legal")
    print("     for a device you don't hold.")
    print("   * 100 mm FAILS at peak draw in every config, and fails for both")
    print("     holographic configs even at typical draw if the surface must")
    print("     stay at a comfortable 40 C.")
    print()
    print("  => 10 cm is not killed by thermal. It is CORNERED by it: it")
    print("     survives only with a hot shell AND active peak management.")
    print("     Design consequences (docs/01 §5, in preference order):")
    print(f"       1. Grow to ~150 mm and the problem disappears entirely")
    print(f"          (150 mm rejects {dissipation(0.150, DT_COMFORTABLE)['q_total_W']:.0f} W "
          f"at a comfortable 40 C) — parameter A1 exists for this")
    print( "       2. Cut compute — the tracked architecture already removes 58x")
    print( "          of hologram synthesis load (docs/01 §4.4). This is a")
    print( "          THERMAL result as much as an optical one.")
    print(f"       3. Forced air: h=25 raises the 100 mm/50 C budget to "
          f"{dissipation(0.100, DT_ACCEPTABLE, h=25.0)['q_total_W']:.0f} W,")
    print( "          at the cost of fan noise beside a conversation")
    print( "       4. Duty-cycle peak power — calls are bursty; peak != sustained")
    print()
    print( "   * Emissivity is nearly free performance: matte dark finish (0.9)")
    print(f"     gives {dissipation(0.100, DT_ACCEPTABLE)['q_total_W']:.1f} W vs "
          f"{dissipation(0.100, DT_ACCEPTABLE, emis=0.05)['q_total_W']:.1f} W for polished bare")
    print( "     metal — a 69% swing on finish alone. An Apple-style polished")
    print( "     aluminium shell is a THERMAL DECISION, not just an aesthetic one.")
    print()
    print("  First-order lumped model — sufficient to force the size decision")
    print("  now. Escalate to FEA/CFD before committing to 100 mm, precisely")
    print("  because that call is marginal rather than comfortable.")
    out["verdict"] = {
        "budget_100mm_40C_W": d100_40,
        "budget_100mm_50C_W": d100_50,
        "passes_at_100mm": verdicts,
        "required_mm": {n: {"40C_typ": required_edge(config_power(n)[0], DT_COMFORTABLE) * 1000,
                            "50C_typ": required_edge(config_power(n)[0], DT_ACCEPTABLE) * 1000,
                            "40C_peak": required_edge(config_power(n)[1], DT_COMFORTABLE) * 1000,
                            "50C_peak": required_edge(config_power(n)[1], DT_ACCEPTABLE) * 1000}
                        for n in CONFIGS},
    }
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true",
                    help="emit machine-readable results")
    args = ap.parse_args()
    results = report()
    if args.json:
        print("\n" + json.dumps(results, indent=2))
