"""
TAYF depth-cue budget - which depth cue actually carries the signal, and by
how much.

Written 2026-08-21 after docs/15_THE_ACCOMMODATION_BUDGET.md established that a
person fits inside one accommodation slab at pod distance. That result deleted
the swept-focus element, but it also raised a question doc 15 did not answer:
if accommodation is null, what does a free-space image have that a screen at
the same distance does not?

The answer turns out to be provable rather than empirical, and it corrects
docs/13_THE_ROOM.md section 6, which named accommodation as "the one thing this
beats every screen and headset at."

THE RESULT. Both depth cues scale identically with subject depth t and viewing
distance R:

    accommodation span   =        t / R^2     diopters
    disparity span       =  b *   t / R^2     radians       (b = interocular)

so the ratio of their suprathreshold margins is INDEPENDENT of both t and R:

    stereo_margin / accom_margin  =  b * 2 * DOF_HALF / theta_threshold
                                  =  268x   at b=65 mm, DoF 0.6 D, 30 arcsec

Stereopsis is two to three orders of magnitude more sensitive to depth than
accommodation, at every distance and for every subject size. Accommodation is
the weakest depth cue the eye has. A display that gets disparity right and focus
wrong is far closer to correct than one that does the reverse - which is why
headsets work at all despite vergence-accommodation conflict, and why VAC is
correctly described as a *comfort* problem, not a *depth* problem.

Consequence for TAYF: the free-space advantage over a 2D screen is real and
large, but it is STEREOPSIS, not focus. The advantage over a stereo screen
serving one tracked viewer is neither - it is multi-viewer geometry, walk-around
beyond the screen's cone, absence of a substrate, and no eyewear.

Status discipline per eng/03_PHYSICS/constants.py.
Ledger: corrects docs/13 section 6; extends docs/15 section 4. Sets the
condition set for experiment PQ-1 in experiments/perceptual-quality/.
"""
import math

from accommodation import DOF_HALF, T_BODY, T_HEAD, T_SHOULDERS, diopter_span

RAD2ARCSEC = 206264.806            # exact, definitional

# ---------------------------------------------------------------------------
# Binocular parameters
# ---------------------------------------------------------------------------
# Interocular distance. [ASSUMED] 65 mm is the conventional adult mean; the
# population runs roughly 55-72 mm. Enters every result linearly.
IPD = 0.065

# Stereoacuity threshold, arcsec - the smallest depth-disparity a viewer can
# reliably detect.
# [PUBLISHED, secondary] Literature read at review/abstract level, not from the
# primary papers: normal stereopsis is conventionally defined as <= 60 arcsec;
# typical normal observers measure <= 30 arcsec; a 100 ms forced-choice study
# reports a mean of ~37 arcsec for observers under 60; trained observers reach
# < 5 arcsec. 30 arcsec is used as the working value and 10/30/60 are swept.
# NOT verified against primary sources in this repository.
STEREO_THRESHOLD_ARCSEC = 30.0


def disparity_span(R, t, ipd=IPD):
    """Binocular disparity range across a subject of depth `t` at distance `R`,
    in arcsec.

    [DERIVED] ipd/(R - t/2) - ipd/(R + t/2), small-angle, converted to arcsec.
    Note this is exactly `ipd` times diopter_span() - the two cues differ by a
    constant factor, not by a functional form.
    """
    if t <= 0:
        return 0.0
    if R <= t / 2:
        raise ValueError(f"viewer inside the subject: R={R} m, t={t} m")
    return ipd * diopter_span(R, t) * RAD2ARCSEC


def accommodation_margin(R, t, dof_half=DOF_HALF):
    """How many times over the accommodation threshold a subject's own depth is.

    [DERIVED] < 1.0 means the subject is optically flat to focus - the eye
    cannot use accommodation to resolve its depth at all.
    """
    return diopter_span(R, t) / (2.0 * dof_half)


def stereo_margin(R, t, ipd=IPD, threshold_arcsec=STEREO_THRESHOLD_ARCSEC):
    """How many times over the stereoacuity threshold the same subject is."""
    return disparity_span(R, t, ipd) / threshold_arcsec


def cue_sensitivity_ratio(ipd=IPD, dof_half=DOF_HALF,
                          threshold_arcsec=STEREO_THRESHOLD_ARCSEC):
    """How much more sensitive stereopsis is than accommodation, as a pure number.

    [DERIVED] ipd * 2 * dof_half / (threshold in radians).

    Independent of subject size and viewing distance - both cancel. This single
    number is why docs/13 section 6's accommodation-led pitch was wrong.
    """
    return ipd * 2.0 * dof_half / (threshold_arcsec / RAD2ARCSEC)


def cue_table(distances=(0.7, 1.0, 1.3, 1.5, 2.0, 2.5),
              subjects=(("head", T_HEAD), ("shoulders", T_SHOULDERS),
                        ("body", T_BODY))):
    """Rows of (R, label, t, diopters, accom_margin, arcsec, stereo_margin)."""
    rows = []
    for R in distances:
        for label, t in subjects:
            try:
                rows.append((R, label, t, diopter_span(R, t),
                             accommodation_margin(R, t),
                             disparity_span(R, t), stereo_margin(R, t)))
            except ValueError:
                continue
    return rows


# ---------------------------------------------------------------------------
# What each candidate display actually delivers
# ---------------------------------------------------------------------------
# Truth table behind experiment PQ-1's condition set. Each entry says whether
# that display reproduces the cue CORRECTLY for the viewer(s) named.
#   real      - a physical object at the location (the ceiling condition)
#   aerial    - free-space real image at the location (the product)
#   flat2d    - 2D screen physically at the same location
#   farscreen - 2D screen at the far wall, angularly matched (the Beam baseline)
# `opaque` is included because leaving it out made the model claim that an
# aerial image and a real object are indistinguishable. They are not: an aerial
# image is additive, so it cannot occlude what is behind it (docs/13 section 5,
# the permanent ghost limit). Omitting a cue the mechanism genuinely lacks is
# how a model flatters its own architecture.
DISPLAY_CUES = {
    #                    accom  disparity  parallax  multiview  substrate_free  opaque
    "real":             (True,  True,      True,     True,      True,           True),
    "aerial":           (True,  True,      True,     True,      True,           False),
    "flat2d":           (True,  False,     False,    True,      False,          True),
    "farscreen":        (False, False,     False,    True,      False,          True),
    "stereo_tracked":   (False, True,      True,     False,     False,          True),
}
CUE_NAMES = ("accommodation", "disparity", "motion_parallax",
             "multiviewer", "substrate_free", "opaque")

# Comparisons whose purpose is to characterise the RIG rather than the concept.
# The model predicts aerial and real differ only in opacity, so any *other*
# difference subjects report against a real object is an artefact of our optics
# - ghosting, luminance mismatch, aberration, or cone clipping. That makes this
# the calibration condition, not a null.
RIG_QUALITY_COMPARISONS = {("aerial", "real")}


def cues_distinguishing(a, b):
    """Which cues differ between two displays - i.e. what an A-vs-B comparison
    can possibly be detecting. An empty result means the comparison is a null by
    construction and must not be run as if it were informative.
    """
    ca, cb = DISPLAY_CUES[a], DISPLAY_CUES[b]
    return tuple(n for n, x, y in zip(CUE_NAMES, ca, cb) if x != y)


def report():
    print("TAYF depth-cue budget\n")
    ratio = cue_sensitivity_ratio()
    print(f"Stereopsis is {ratio:.0f}x more sensitive to depth than "
          f"accommodation.")
    print("Independent of subject size and viewing distance - both cancel.\n")

    print("Sensitivity ratio vs the stereoacuity assumption:")
    for thr in (10.0, 30.0, 60.0):
        print(f"   threshold {thr:>4.0f} arcsec -> "
              f"{cue_sensitivity_ratio(threshold_arcsec=thr):>6.0f}x")

    print(f"\nPer-subject margins (accommodation DoF = {2*DOF_HALF} D, "
          f"stereo threshold = {STEREO_THRESHOLD_ARCSEC:.0f} arcsec)")
    print(f"{'R':>5} {'subject':>10} {'accom D':>9} {'x thr':>8} "
          f"{'stereo \"':>10} {'x thr':>8}  verdict")
    for R, label, t, d, am, s, sm in cue_table():
        v = ("both visible" if am >= 1 else
             "FLAT to focus, sharp to stereo" if sm >= 1 else "invisible to both")
        print(f"{R:>5.1f} {label:>10} {d:>9.3f} {am:>7.2f}x "
              f"{s:>10.0f} {sm:>7.0f}x  {v}")

    print("\nWhat an A-vs-B comparison can detect")
    for a, b in (("aerial", "real"), ("aerial", "flat2d"),
                 ("aerial", "farscreen"), ("aerial", "stereo_tracked")):
        diff = cues_distinguishing(a, b)
        tag = "  [RIG QUALITY]" if (a, b) in RIG_QUALITY_COMPARISONS else ""
        print(f"   {a:>8} vs {b:<15} -> "
              f"{', '.join(diff) if diff else 'NOTHING - null by construction'}{tag}")
    print("\n   aerial vs real is the calibration condition: the model says they")
    print("   differ only in opacity, so anything else subjects report is our")
    print("   rig's fault, not the concept's.")


if __name__ == "__main__":
    report()
