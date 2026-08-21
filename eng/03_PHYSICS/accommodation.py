"""
TAYF accommodation budget - how much depth the human eye can actually resolve,
and therefore how many focal planes a free-space display must produce.

Exists because docs/13_THE_ROOM.md section 7 sized the depth planes GEOMETRICALLY
(a 1 m volume cut into 33 mm steps -> 24-32 planes -> a 2,700 Hz swept focus
element -> deformable mirrors at $10k-50k each). The eye does not resolve depth
in millimetres. It resolves depth in DIOPTERS, and one depth-of-field slab at
pod distance is over a metre thick. The correct plane count is 1-2. That single
correction deletes the highest-cost, highest-risk item in the whole design.

Discipline inherited from constants.py: every number carries a status label.
VERIFIED = measured in the cited primary source. DERIVED = computed here from
verified inputs, formula shown. ASSUMED = engineering baseline, explicitly
marked, to be swept. UNKNOWN = no basis yet; treated as risk driver.

The load-bearing number in this module is DOF_HALF and it is [ASSUMED]. The
entire product rests on it, so it is a swept parameter everywhere and never a
hardcoded truth. sweep_dof_half() exists specifically to show where the design
window goes when that assumption moves.

Ledger: corrects docs/13 section 7 and section 13 risk 1. Feeds
experiments/perceptual-quality/ and docs/15_THE_ACCOMMODATION_BUDGET.md.
"""
import math

# ---------------------------------------------------------------------------
# The one assumption everything rests on
# ---------------------------------------------------------------------------
# Half-width of the human eye's depth of field, in diopters. Literature-typical
# for a ~3 mm pupil in normal photopic conditions; commonly quoted as +/-0.3 D.
# [ASSUMED] Not verified against a primary source in this repository. Swept over
# 0.20-0.50 D in sweep_dof_half(); if the design window vanishes at the low end
# that is a finding about the product, not a bug in this file.
DOF_HALF = 0.30

# ---------------------------------------------------------------------------
# Subject depth extents, front-to-back, in metres
# ---------------------------------------------------------------------------
T_HEAD = 0.25            # [ASSUMED] head + neck, face to back of skull
T_BODY = 0.60            # [ASSUMED] torso incl. arms at rest, standing
T_SHOULDERS = 0.35       # [ASSUMED] head + shoulders, the bust framing

# ---------------------------------------------------------------------------
# Geometry defaults, from docs/13_THE_ROOM.md
# ---------------------------------------------------------------------------
D_APERTURE = 0.50        # [ASSUMED] per-engine aperture width, m (doc 13 s1.1)
WALL_MIN = 3.0           # [ASSUMED] nearest visible surface behind the image, m


def diopter_span(R, t):
    """Diopter extent of a subject of depth `t` whose centre is `R` metres away.

    Exact:  1/(R - t/2) - 1/(R + t/2)
    This is the quantity the eye actually sees. A subject is "flat" to the eye
    when this is smaller than one depth of field (2 * DOF_HALF), no matter how
    many millimetres thick it is.

    Raises ValueError if the subject would extend through the viewer.
    """
    if t <= 0:
        return 0.0
    if R <= t / 2:
        raise ValueError(f"viewer inside the subject: R={R} m, t={t} m")
    return 1.0 / (R - t / 2) - 1.0 / (R + t / 2)


def diopter_span_approx(R, t):
    """Fast path: span ~= t / R^2.

    [DERIVED] First-order expansion of diopter_span. Agrees to better than 4%
    for R >= 0.7 m at t = 0.25 m. Useful for reasoning out loud; the exact form
    is what the rest of this module uses.
    """
    return t / (R * R)


def dof_slab(R, dof_half=DOF_HALF):
    """Near bound, far bound, and thickness (m) of one depth-of-field slab
    centred on distance `R`.

    [DERIVED] near = 1/(1/R + dof_half), far = 1/(1/R - dof_half).
    Far bound is math.inf once 1/R <= dof_half, i.e. beyond R = 1/dof_half the
    eye cannot distinguish the image from infinity at all. At dof_half = 0.30
    that horizon is 3.33 m, which is why this display has to be a pod.
    """
    inv = 1.0 / R
    near = 1.0 / (inv + dof_half)
    far = math.inf if inv <= dof_half else 1.0 / (inv - dof_half)
    return near, far, (far - near)


def planes_needed(R, t, dof_half=DOF_HALF):
    """How many focal planes are actually required to render a subject of depth
    `t` at distance `R`, with a floor of 1.

    [DERIVED] ceil(diopter_span / (2 * dof_half)). Plane spacing of one full
    depth of field is consistent with the multifocal-display literature, which
    typically uses 0.6-0.9 D spacing with depth blending between planes.
    """
    return max(1, math.ceil(diopter_span(R, t) / (2.0 * dof_half)))


def background_cue(R, wall=WALL_MIN):
    """Diopter difference between a free-space image at `R` and the nearest
    visible surface behind it at `wall`.

    [DERIVED] 1/R - 1/wall.

    This - NOT the subject's own depth extent - is the cue that differentiates a
    free-space image from a flat screen hung on that far wall. Once the subject
    fits inside one focal slab (which it does at every pod distance), the
    within-subject focus cue is gone and this is the only accommodation
    signal left. It must exceed the perceptibility threshold or the free-space
    advantage is physically absent, not merely subtle.
    """
    return 1.0 / R - 1.0 / wall


def engines_needed(z, d_aperture=D_APERTURE):
    """Number of engines to tile 360 degrees of aperture at image-to-aperture
    distance `z`.

    [DERIVED] N = 2*pi*z / d_aperture, the governing law of docs/13 section 1.
    Lives here so that the geometric constraint and the perceptual constraint
    can be evaluated against each other in one place - they pull on the same
    variable and are only jointly satisfiable in a narrow band.

    Note z (image-to-aperture) is NOT R (image-to-viewer). In a pod the viewer
    stands inside the aperture ring, so R < z.
    """
    return 2.0 * math.pi * z / d_aperture


def design_window(t=T_BODY, dof_half=DOF_HALF, wall_offset=None,
                  r_min=0.5, r_max=3.0, step=0.05, max_planes=1):
    """Sweep viewer distance R and return the band where the display is both
    cheap and differentiated:

        planes_needed(R, t) <= max_planes   AND   background_cue(R) >= dof_half

    The two conditions pull opposite ways. Close in, the subject spans many
    diopters and needs several planes. Far out, the background cue drops below
    threshold and the free-space advantage disappears. The product only exists
    in the overlap.

    `wall_offset`: if given, the far wall is taken as R + wall_offset (a pod
    that moves with the viewer). If None, the fixed WALL_MIN is used.

    Returns (r_lo, r_hi, rows) where rows is every sampled R with its numbers.
    r_lo/r_hi are None if the window is empty - which is a finding.
    """
    rows, ok = [], []
    n = int(round((r_max - r_min) / step)) + 1
    for i in range(n):
        R = r_min + i * step
        try:
            span = diopter_span(R, t)
        except ValueError:
            continue
        wall = (R + wall_offset) if wall_offset is not None else WALL_MIN
        if wall <= R:
            continue
        p = planes_needed(R, t, dof_half)
        cue = background_cue(R, wall)
        passes = (p <= max_planes) and (cue >= dof_half)
        rows.append(dict(R=R, span=span, planes=p, wall=wall,
                         cue=cue, passes=passes))
        if passes:
            ok.append(R)
    if not ok:
        return None, None, rows
    return min(ok), max(ok), rows


def sweep_dof_half(t=T_BODY, values=(0.20, 0.25, 0.30, 0.35, 0.40, 0.50),
                   **kw):
    """Where does the design window go as the one [ASSUMED] number moves?

    Returns {dof_half: (r_lo, r_hi)}. A window that closes at the low end tells
    you the product depends on an eye being more tolerant than the pessimistic
    reading of the literature - which is exactly the thing the Phase 3 bench is
    built to measure rather than assume.
    """
    out = {}
    for d in values:
        lo, hi, _ = design_window(t=t, dof_half=d, **kw)
        out[d] = (lo, hi)
    return out


def robust_window(t=T_BODY, values=(0.20, 0.25, 0.30, 0.35, 0.40, 0.50), **kw):
    """The band of R that satisfies the design conditions for EVERY value of
    DOF_HALF in `values` - i.e. the design point that does not depend on which
    depth-of-field figure turns out to be right.

    This is the answer to the [ASSUMED] problem. Rather than betting the product
    on DOF_HALF = 0.30, pick an R inside the intersection of all the windows and
    the geometry holds whatever the bench measures.

    Returns (lo, hi) or (None, None) if no single R works for all values.
    """
    los, his = [], []
    for lo, hi in sweep_dof_half(t=t, values=values, **kw).values():
        if lo is None:
            return None, None
        los.append(lo)
        his.append(hi)
    lo, hi = max(los), min(his)
    return (lo, hi) if lo <= hi else (None, None)


def _fmt(x, nd=3, inf="inf"):
    return inf if x == math.inf else f"{x:.{nd}f}"


def report():
    """Print the tables that docs/15 and docs/13's correction are built on."""
    print("TAYF accommodation budget")
    print(f"DOF_HALF = {DOF_HALF} D  [ASSUMED]   "
          f"one full depth of field = {2*DOF_HALF} D\n")

    print("1. Subject depth extent in diopters (span = 1/(R-t/2) - 1/(R+t/2))")
    print(f"{'R (m)':>7} {'head':>9} {'shoulders':>11} {'body':>9}   "
          f"one DoF = {2*DOF_HALF:.2f} D")
    for R in (0.5, 0.7, 1.0, 1.2, 1.5, 2.0, 2.5, 3.5):
        try:
            h, s, b = (diopter_span(R, T_HEAD), diopter_span(R, T_SHOULDERS),
                       diopter_span(R, T_BODY))
        except ValueError:
            continue
        print(f"{R:>7.2f} {h:>9.3f} {s:>11.3f} {b:>9.3f}")

    print("\n2. One depth-of-field slab is this thick")
    print(f"{'R (m)':>7} {'near':>8} {'far':>8} {'thickness':>12}")
    for R in (0.7, 1.0, 1.2, 1.5, 2.0, 2.5):
        near, far, thick = dof_slab(R)
        t_mm = "inf" if thick == math.inf else f"{thick*1000:.0f} mm"
        print(f"{R:>7.2f} {near:>8.2f} {_fmt(far,2):>8} {t_mm:>12}")

    print("\n3. Focal planes actually needed  (doc 13 s7 said 24-32)")
    print(f"{'R (m)':>7} {'head':>7} {'shoulders':>11} {'body':>7}")
    for R in (0.7, 1.0, 1.2, 1.5, 2.0, 2.5):
        print(f"{R:>7.2f} {planes_needed(R,T_HEAD):>7} "
              f"{planes_needed(R,T_SHOULDERS):>11} "
              f"{planes_needed(R,T_BODY):>7}")

    print("\n4. Design window for a full body, pod wall 2*z behind the image")
    for zp in (1.2, 1.5):
        lo, hi, _ = design_window(t=T_BODY, wall_offset=2 * zp)
        if lo is None:
            print(f"   pod radius {zp} m: NO WINDOW - product does not exist "
                  f"at this geometry")
        else:
            print(f"   pod radius {zp} m: R = {lo:.2f} to {hi:.2f} m"
                  f"   -> N = {engines_needed(zp):.0f} engines")

    print("\n5. Sensitivity of the window to DOF_HALF (body, pod radius 1.5 m)")
    print(f"{'DOF_HALF':>9} {'R window (m)':>22}")
    for d, (lo, hi) in sweep_dof_half(t=T_BODY, wall_offset=3.0).items():
        w = "EMPTY" if lo is None else f"{lo:.2f} - {hi:.2f}"
        print(f"{d:>9.2f} {w:>22}")

    lo, hi = robust_window(t=T_BODY, wall_offset=3.0)
    if lo is None:
        print("\n   NO ROBUST WINDOW - the design point depends on which "
              "DOF_HALF is correct, so the bench must settle it first.")
    else:
        print(f"\n   ROBUST WINDOW: R = {lo:.2f} to {hi:.2f} m works for EVERY "
              f"DOF_HALF above.\n   The geometry does not depend on which "
              f"depth-of-field figure is right.")

    print("\n6. Engines to tile 360 degrees, N = 2*pi*z / D_aperture")
    print(f"{'z (m)':>7} {'D=0.40':>9} {'D=0.50':>9}")
    for z in (1.2, 1.5, 2.0, 2.5, 3.5):
        print(f"{z:>7.2f} {engines_needed(z,0.40):>9.0f} "
              f"{engines_needed(z,0.50):>9.0f}")


if __name__ == "__main__":
    report()
