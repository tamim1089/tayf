#!/usr/bin/env python3
"""
S3 — Thermal envelope of a sealed TAYF enclosure.

Implements docs/07_HARDWARE_SIMULATION_PLAN.md tracks S3.1 (reproduce the
lumped model in docs/01_SYSTEM_MASTER_SPEC.md §5) and S3.3 (sweep edge length
to find the size that actually closes the budget).

Thermal is the binding constraint on the TAYF form factor. A sealed 100 mm
cube rejects only ~10.4 W at a comfortable 40 C shell and ~16.2 W at the
48 C IEC metal touch limit (5 participating faces), while a Jetson-class SoC
alone draws 7-15 W. This script answers: what edge length does a real
component set actually require?

The limit is HUMAN SKIN, not silicon: junction temperature is comfortable at
25 W, but the shell is a safety violation well before that.

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

# Surface temperature limits.
#
# CORRECTED 2026-08-15 per docs/04_CUBE_HARDWARE_AND_PROTOTYPE_ENGINEERING.md:
# a hot metal shell is a SAFETY violation, not a comfort complaint. IEC
# touch-temperature guidance caps continuously-touchable METAL at ~48 C
# (plastic is allowed higher because it conducts heat into skin more slowly).
# The 50 C and 60 C cases below therefore describe devices that cannot ship;
# they are retained ONLY for sensitivity analysis and are labelled as such.
DT_COMFORTABLE = 15.0    # 40 C surface - comfortable, design target
DT_TOUCH_LIMIT = 23.0    # 48 C surface - IEC metal touch limit, HARD CEILING
DT_ACCEPTABLE = 25.0     # 50 C - ABOVE the metal limit, sensitivity only
DT_LIMIT = 35.0          # 60 C - safety violation, sensitivity only

# Not all six faces reject heat: one is occupied by the base/mounting and the
# optical exit aperture is not a radiator. doc 04 uses ~5 participating faces.
PARTICIPATING_FACES = 5.0

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


def dissipation(edge_m, dT, h=H_CONV_NOMINAL, emis=EMISSIVITY, t_amb_c=T_AMB_C,
                faces=PARTICIPATING_FACES):
    """Steady-state heat a sealed cube of given edge length can reject.

    `faces` defaults to 5, not 6: the base/mounting face and the optical exit
    aperture do not radiate usefully. Pass faces=6.0 to reproduce the earlier
    (optimistic) figures in docs/01 §5's first table.
    """
    area = faces * edge_m ** 2
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
    for dT in (DT_COMFORTABLE, DT_TOUCH_LIMIT, DT_ACCEPTABLE, DT_LIMIT):
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
    for dT, label in ((DT_COMFORTABLE, "40 C — comfortable design target"),
                      (DT_TOUCH_LIMIT, "48 C — IEC metal touch limit, HARD CEILING")):
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
        for dT, lbl in ((DT_COMFORTABLE, "40C"), (DT_TOUCH_LIMIT, "48C")):
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
    d100_50 = dissipation(0.100, DT_TOUCH_LIMIT)["q_total_W"]
    print(f"  A sealed 100 mm cube rejects {d100_40:.1f} W at 40 C surface, "
          f"{d100_50:.1f} W at the 48 C metal touch limit.")
    print()
    print("  Does 100 mm close?  (typ = sustained draw, peak = all rails maxed)")
    print(f"  {'config':22s} {'40C typ':>9} {'40C peak':>9} "
          f"{'48C typ':>9} {'48C peak':>9}")
    verdicts = {}
    for name in CONFIGS:
        typ, mx = config_power(name)
        cells, vs = [], {}
        for dT, lbl in ((DT_COMFORTABLE, "40C"), (DT_TOUCH_LIMIT, "48C")):
            budget = dissipation(0.100, dT)["q_total_W"]
            for p, plbl in ((typ, "typ"), (mx, "peak")):
                ok = budget >= p
                cells.append(("PASS" if ok else "FAIL").rjust(9))
                vs[f"{lbl}_{plbl}"] = ok
        verdicts[name] = vs
        print(f"  {name:22s} " + " ".join(cells))

    print()
    print("  THE ANSWER (5 participating faces, 48 C metal touch limit):")
    print("   * Only the hackathon-panel config passes at 100 mm, and only at")
    print("     sustained draw against the 48 C HARD CEILING - i.e. with zero")
    print("     comfort margin and no headroom for peaks.")
    print("   * BOTH holographic configs FAIL at 100 mm at every temperature")
    print("     and every load. The optical engine's power is what breaks it.")
    print("   * NO config survives peak draw at 100 mm.")
    print()
    print("  => 10 cm does NOT close for the full-capability device. This is")
    print("     the binding constraint on the form factor - not the optics,")
    print("     which have 145x aperture headroom (docs/01 §4.5).")
    print("     Relaxations, in order of preference (docs/01 §5.3):")
    e_need = required_edge(config_power("holographic-nano")[0], DT_COMFORTABLE) * 1000
    print(f"       1. Grow to ~{math.ceil(e_need/10)*10:.0f} mm: the holographic config then closes")
    print(f"          at a comfortable 40 C. doc 04 independently lands on 130 mm.")
    print( "       2. Cut compute. The tracked architecture already removes 58x")
    print( "          of hologram synthesis load (docs/01 §4.4) - a THERMAL")
    print( "          result as much as an optical one. A 7 W SoC profile or a")
    print( "          discrete NPU is the highest-value untested hardware")
    print( "          question in the project.")
    print( "       3. Duty-cycle. Thermal mass buys ~8-11 min at full capability")
    print( "          - the length of a phone call. This reframes TAYF as a CALL")
    print( "          device rather than an always-on one (doc 04).")
    print( "       4. Forced air is NOT available: doc 04 excludes it on volume")
    print( "          (~90 cm3 into a ~93%-packed interior), dust (vents plus")
    print( "          ~20 optical surfaces in a folded coherent path), and")
    print( "          acoustics (~25 dBA beside a conversation).")
    print()
    pol = dissipation(0.100, DT_TOUCH_LIMIT, emis=0.05)["q_total_W"]
    ano = dissipation(0.100, DT_TOUCH_LIMIT, emis=0.90)["q_total_W"]
    print(f"   * Emissivity is first-order, not a finish detail: anodised/matte")
    print(f"     {ano:.1f} W vs polished bare metal {pol:.1f} W at 100 mm/48 C")
    print(f"     - a {(ano-pol)/ano*100:.0f}% swing. An Apple-style polished unibody has a")
    print(f"     THERMAL VETO over the industrial design (design/README.md).")
    print()
    print("  First-order lumped model. experiments/thermal/ exists to measure")
    print("  this on real hardware; where they disagree, the measurement wins.")
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
