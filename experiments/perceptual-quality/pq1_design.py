"""
PQ-1 experimental design: sample size, power, and the analysis that will be run
on the data.

Exists because experiments/perceptual-quality/README.md originally specified
"n >= 12" and that number was a guess. A guessed sample size produces a study
that cannot distinguish "no effect" from "not enough subjects", which for a
go/no-go experiment is the worst possible outcome - it costs the money and
returns nothing.

This module computes the real numbers, and it does so BEFORE data collection so
the analysis is pre-registered rather than chosen after seeing the results.

Design: two-alternative forced choice (2AFC). On each trial the subject sees two
presentations of the same content, one in each of two conditions, in random
order, and answers a single question ("which one was physically there?" for the
realism task; "which felt more like a person was present?" for the presence
task). Chance is 0.5. A condition pair the subject cannot tell apart yields 0.5.

Two units of analysis, both reported:
  1. WITHIN-SUBJECT - each subject's trials against chance, exact binomial.
     Answers "can this person tell?"
  2. ACROSS-SUBJECT - each subject's proportion correct as one datum, tested
     against 0.5. Answers "can people tell?" This is the one that generalises
     and the one the go/no-go decision uses.

Multiplicity is real: 3 distances x 3 condition pairs = 9 tests. Holm-Bonferroni
is applied, and the sample size is computed against the CORRECTED alpha, not the
nominal one. Skipping that step is the single most common way a study like this
reports a false positive.

Two design flaws were found by running this file rather than by building the rig:
  - Six distances gave 173 min per subject. Cut to three.
  - The calibration cell wants a NULL, and a non-significant t-test is not
    evidence of a null. It needs TOST equivalence testing, which needs its own
    (larger) sample size. See subjects_for_equivalence().

Status discipline per eng/03_PHYSICS/constants.py.
Run: python3 experiments/perceptual-quality/pq1_design.py
"""
import math
import pathlib
import sys

from scipy import stats

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]
                       / "eng" / "03_PHYSICS"))

from depth_cues import (  # noqa: E402
    DISPLAY_CUES, RIG_QUALITY_COMPARISONS, accommodation_margin,
    cues_distinguishing, stereo_margin,
)
from accommodation import T_BODY, T_HEAD  # noqa: E402

# ---------------------------------------------------------------------------
# Design parameters
# ---------------------------------------------------------------------------
ALPHA = 0.05             # [ASSUMED] conventional
POWER = 0.80             # [ASSUMED] conventional
# Three distances, not six. The first draft swept six and the power analysis
# said 173 min per subject, which is infeasible and would have been discovered
# only after building the rig. Three points still test the model's trend claim:
# 0.7 = strongest cues, 1.3 = the design point, 2.5 = where accommodation is
# predicted to have died. [DERIVED from the timing budget in session_plan().]
DISTANCES = (0.7, 1.3, 2.5)   # m, viewer to image

# Seconds per trial, including switching between conditions. The rig MUST make
# the two conditions electronically switchable at the same apparent location -
# if a human has to move a screen between presentations, switching dominates
# and the study becomes infeasible. This is a hard requirement on the bench,
# discovered here rather than during the build. [ASSUMED] 12 s.
SECONDS_PER_TRIAL = 12.0
MAX_SESSION_MIN = 45.0        # [ASSUMED] fatigue confound past ~45 min

# The pairs actually run. "aerial" is the product in every one.
CONDITION_PAIRS = (
    ("aerial", "real"),            # calibration: how good is the rig?
    ("aerial", "flat2d"),          # what does free space buy over a 2D screen?
    ("aerial", "farscreen"),       # the HP Dimension / Beam baseline
)
N_TESTS = len(DISTANCES) * len(CONDITION_PAIRS)


def holm_alpha(n_tests=N_TESTS, alpha=ALPHA, rank=1):
    """Holm-Bonferroni threshold for the `rank`-th smallest p-value (1-indexed).

    [DERIVED] alpha / (n_tests - rank + 1). Sizing against rank=1 is the
    conservative choice: it is the threshold the most significant result must
    clear, and therefore the one that determines whether the study can detect
    anything at all.
    """
    return alpha / (n_tests - rank + 1)


def trials_for_within_subject(p_true, alpha, power=POWER, max_n=4000):
    """Trials one subject must complete for an exact one-sided binomial test to
    detect a true rate `p_true` against chance, at `alpha` and `power`.

    Exact, not the normal approximation - at these n the approximation is
    optimistic by enough to matter.
    """
    if p_true <= 0.5:
        return math.inf
    for n in range(4, max_n + 1):
        # smallest k whose upper-tail p-value under H0 clears alpha
        k = stats.binom.isf(alpha, n, 0.5) + 1
        if k > n:
            continue
        achieved = stats.binom.sf(k - 1, n, p_true)   # P(X >= k | p_true)
        if achieved >= power:
            return n
    return math.inf


def subjects_for_across_subject(p_true, alpha, power=POWER, sd=0.15,
                                max_n=1000):
    """Subjects needed to detect a mean proportion-correct of `p_true` against
    0.5, one-sided one-sample t-test.

    `sd` is the between-subject standard deviation of the proportion.
    [ASSUMED] sd = 0.15. Between-subject spread in psychophysical proportion-
    correct is commonly 0.10-0.20; 0.15 is the middle and is swept in report().
    """
    if p_true <= 0.5:
        return math.inf
    d = (p_true - 0.5) / sd                     # Cohen's d
    for n in range(3, max_n + 1):
        df = n - 1
        crit = stats.t.isf(alpha, df)
        ncp = d * math.sqrt(n)
        if stats.nct.sf(crit, df, ncp) >= power:
            return n
    return math.inf


def predicted_direction(a, b, R, t=T_BODY):
    """What the physics model predicts for this comparison at this distance.

    Not a predicted p-value - the psychometric function is unknown and inventing
    one would be false precision. This returns the qualitative prediction plus
    the cue margins that justify it, so the study is falsifiable: a result
    contradicting these is informative about the model, not just about subjects.
    """
    diff = cues_distinguishing(a, b)
    am, sm = accommodation_margin(R, t), stereo_margin(R, t)
    if (a, b) in RIG_QUALITY_COMPARISONS:
        return ("near chance if the rig is good; any discrimination measures "
                "OUR artefacts (ghosting, luminance, aberration)", diff, am, sm)
    if "disparity" in diff and sm >= 1.0:
        return (f"strong discrimination: disparity is {sm:.0f}x threshold", diff, am, sm)
    if diff and am >= 1.0:
        return (f"moderate: accommodation {am:.1f}x threshold", diff, am, sm)
    if diff:
        return ("weak - only substrate/opacity cues remain", diff, am, sm)
    return ("chance: null by construction", diff, am, sm)


def subjects_for_equivalence(margin, alpha=ALPHA, power=POWER, sd=0.15,
                             true_diff=0.0, max_n=1000):
    """Subjects needed for a TOST equivalence test: to conclude the true rate is
    within +/- `margin` of chance.

    You cannot prove a null with a significance test - failing to reject H0 is
    not evidence of equivalence, it is absence of evidence. The calibration cell
    (aerial vs real) WANTS a null, so it needs TOST, with the equivalence margin
    fixed in advance.

    [DERIVED] Two one-sided t-tests; power is the probability BOTH reject.
    """
    for n in range(3, max_n + 1):
        df, se = n - 1, sd / math.sqrt(n)
        crit = stats.t.isf(alpha, df)
        # both one-sided tests must reject; for true_diff=0 this is symmetric
        ncp_lo = (true_diff + margin) / se
        ncp_hi = (true_diff - margin) / se
        pw = stats.nct.sf(crit, df, ncp_lo) - stats.nct.sf(-crit, df, ncp_hi)
        if pw >= power:
            return n
    return math.inf


def session_plan(trials_per_cell, n_cells, secs=SECONDS_PER_TRIAL,
                 max_min=MAX_SESSION_MIN):
    """Total trials, minutes, and how many sittings that forces."""
    total = trials_per_cell * n_cells
    minutes = total * secs / 60.0
    return total, minutes, max(1, math.ceil(minutes / max_min))


def report():
    a_corr = holm_alpha()
    print("PQ-1 design\n")
    print(f"{N_TESTS} planned tests ({len(DISTANCES)} distances x "
          f"{len(CONDITION_PAIRS)} pairs)")
    print(f"nominal alpha {ALPHA}, power {POWER}")
    print(f"Holm-corrected alpha for the most significant result: "
          f"{a_corr:.5f}\n")

    print("1. Trials per subject (exact binomial, within-subject)")
    print(f"{'true rate':>10} {'alpha=.05':>11} {'Holm alpha':>12}")
    for p in (0.60, 0.65, 0.75, 0.90):
        n1 = trials_for_within_subject(p, ALPHA)
        n2 = trials_for_within_subject(p, a_corr)
        print(f"{p:>10.2f} {n1:>11} {n2:>12}")

    print("\n2. Subjects (one-sample t vs 0.5, across-subject)")
    print(f"{'true rate':>10} {'sd=0.10':>9} {'sd=0.15':>9} {'sd=0.20':>9}")
    for p in (0.60, 0.65, 0.75, 0.90):
        row = [subjects_for_across_subject(p, a_corr, sd=s)
               for s in (0.10, 0.15, 0.20)]
        print(f"{p:>10.2f} " + " ".join(f"{v:>9}" for v in row))

    print("\n3. Predicted outcome per cell (body, t=0.60 m)")
    print(f"{'R':>5} {'pair':>22} {'accom':>7} {'stereo':>8}  prediction")
    for a, b in CONDITION_PAIRS:
        for R in DISTANCES:
            msg, diff, am, sm = predicted_direction(a, b, R)
            print(f"{R:>5.1f} {a + ' vs ' + b:>22} {am:>6.2f}x "
                  f"{sm:>7.0f}x  {msg}")

    # --- the recommendation, sized PER CELL by its predicted effect ---
    print("\n4. RECOMMENDED DESIGN, sized per cell")
    print("   Sizing every cell for a weak effect is wasteful: the model")
    print("   predicts the flat2d/farscreen cells sit at ceiling (disparity is")
    print("   44-670x threshold) and only the calibration cell sits at chance.\n")

    ceiling_trials = trials_for_within_subject(0.90, a_corr)
    ceiling_subj = subjects_for_across_subject(0.75, a_corr, sd=0.15)
    equiv_subj = subjects_for_equivalence(margin=0.10, sd=0.15)
    equiv_trials = trials_for_within_subject(0.75, a_corr)

    print(f"   aerial vs flat2d / farscreen (predicted ceiling):")
    print(f"      {ceiling_trials} trials/subject/cell, {ceiling_subj} subjects")
    print(f"   aerial vs real (calibration, wants a NULL -> TOST +/-0.10):")
    print(f"      {equiv_trials} trials/subject, {equiv_subj} subjects")

    n_subj = max(ceiling_subj, equiv_subj)
    per_subj = ceiling_trials * 2 * len(DISTANCES) + equiv_trials * len(DISTANCES)
    minutes = per_subj * SECONDS_PER_TRIAL / 60.0
    sittings = max(1, math.ceil(minutes / MAX_SESSION_MIN))
    print(f"\n   => {n_subj} subjects x {per_subj} trials = "
          f"{n_subj * per_subj} trials total")
    print(f"      {minutes:.0f} min per subject -> {sittings} sitting(s)")
    print(f"      {n_subj * minutes / 60:.1f} subject-hours to run the whole study")

    print("\n   HARD RIG REQUIREMENT discovered by this analysis:")
    print("   the two conditions must be switchable ELECTRONICALLY at the same")
    print("   apparent location. If a person has to move a screen between")
    print("   presentations, switching dominates the trial and the study")
    print("   stops being feasible. Design the bench for this from the start.")

    print("\n5. PRE-REGISTERED ANALYSIS (fix before collecting)")
    print("   - Primary: across-subject one-sided t vs 0.5, per cell, Holm.")
    print("   - Secondary: per-subject exact binomial, reported individually.")
    print("   - Report effect sizes and CIs for every cell including nulls.")
    print("   - aerial-vs-real is CALIBRATION and is tested for EQUIVALENCE")
    print("     (TOST, margin +/-0.10), not for significance. A non-significant")
    print("     t-test there would be absence of evidence, not evidence of")
    print("     absence, and must not be reported as 'indistinguishable'.")
    print("   - Stopping rule: fixed n. No peeking, no adding subjects after")
    print("     looking - that is what turns a null into a false positive.")


if __name__ == "__main__":
    report()
