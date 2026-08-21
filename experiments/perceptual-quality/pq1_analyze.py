"""
PQ-1 pre-registered analysis.

Written BEFORE any data exists, which is the entire point. An analysis chosen
after seeing results is not an analysis, it is a search for a p-value, and this
study exists to make a go/no-go call on the whole optical programme.

Fixed here and not negotiable once collection starts:
  - which test is applied to which cell,
  - the multiplicity correction,
  - the equivalence margin,
  - the decision rule that maps results onto GO / PIVOT / FIX_RIG / STOP.

Two kinds of cell, and they are NOT tested the same way:

  DETECTION cells (aerial vs flat2d, aerial vs farscreen) ask "can people tell?"
  One-sided t-test against chance. The model predicts these sit at ceiling.

  EQUIVALENCE cell (aerial vs real) asks "are these the same?" A non-significant
  t-test would be absence of evidence, not evidence of absence, so it gets TOST
  against a pre-specified +/-0.10 margin. This is the calibration cell: it
  measures OUR rig's artefacts, and it caps how much any other cell can be
  trusted.

Validated by simulation in eng/08_VERIFY/tests/test_pq1_analysis.py, which runs
the whole pipeline over thousands of synthetic studies with known ground truth
and checks that type-I error is controlled and power is achieved. That is the
proof that this file works, obtained without collecting a single trial.

Usage:
    python3 pq1_analyze.py trials.csv
    # columns: subject,distance,pair,trial,correct
"""
import csv
import math
import pathlib
import sys
from collections import defaultdict

import numpy as np
from scipy import stats

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from pq1_design import (  # noqa: E402
    ALPHA, CONDITION_PAIRS, DISTANCES, POWER, PRIMARY_CELL,
)

EQUIVALENCE_MARGIN = 0.10        # [ASSUMED] fixed before collection. Do not tune.
EQUIVALENCE_PAIRS = {("aerial", "real")}
N_BOOTSTRAP = 10_000
CHANCE = 0.5


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_trials(path):
    """CSV -> {(distance, pair_str): {subject: [0/1, ...]}}."""
    cells = defaultdict(lambda: defaultdict(list))
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            key = (float(row["distance"]), row["pair"])
            cells[key][row["subject"]].append(int(row["correct"]))
    return cells


def subject_proportions(cell):
    """{subject: [trials]} -> np.array of per-subject proportion correct."""
    return np.array([np.mean(v) for v in cell.values() if len(v)])


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def detection_test(props, alpha=ALPHA, n_boot=N_BOOTSTRAP):
    """One-sided one-sample t-test that the mean proportion exceeds chance.

    Returns dict with mean, p, Cohen's d, and a bootstrap 95% CI. The CI is
    reported for every cell including nulls - a null with a CI spanning
    [0.48, 0.55] is a very different result from one spanning [0.35, 0.68] and
    reporting only "n.s." throws that distinction away.
    """
    n = len(props)
    if n < 3:
        return dict(n=n, mean=float(np.mean(props)) if n else math.nan,
                    p=math.nan, d=math.nan, ci=(math.nan, math.nan),
                    significant=False)
    t, p_two = stats.ttest_1samp(props, CHANCE)
    p = p_two / 2 if t > 0 else 1 - p_two / 2         # one-sided, upper
    sd = props.std(ddof=1)
    d = (props.mean() - CHANCE) / sd if sd > 0 else math.inf
    return dict(n=n, mean=float(props.mean()), p=float(p), d=float(d),
                ci=_bootstrap_ci(props, n_boot=n_boot), significant=None)


def equivalence_test(props, margin=EQUIVALENCE_MARGIN, alpha=ALPHA,
                     n_boot=N_BOOTSTRAP):
    """TOST: conclude |mean - chance| < margin.

    Both one-sided tests must reject. Returns the larger of the two p-values,
    which is the TOST p-value.
    """
    n = len(props)
    if n < 3:
        return dict(n=n, mean=float(np.mean(props)) if n else math.nan,
                    p=math.nan, ci=(math.nan, math.nan), equivalent=False)
    lo, hi = CHANCE - margin, CHANCE + margin
    t_lo, p_lo = stats.ttest_1samp(props, lo)        # want mean > lo
    t_hi, p_hi = stats.ttest_1samp(props, hi)        # want mean < hi
    p_lo = p_lo / 2 if t_lo > 0 else 1 - p_lo / 2
    p_hi = p_hi / 2 if t_hi < 0 else 1 - p_hi / 2
    p = max(p_lo, p_hi)
    # Also run a plain detection test on this cell. "Failed to establish
    # equivalence" and "established a difference" are different claims, and
    # only the second one means the rig is broken. The first can just mean this
    # cell was underpowered, which must not block the study.
    t_d, p_two = stats.ttest_1samp(props, CHANCE)
    p_diff = p_two / 2 if t_d > 0 else 1 - p_two / 2
    return dict(n=n, mean=float(props.mean()), p=float(p),
                p_difference=float(p_diff),
                differs=bool(p_diff < alpha),
                ci=_bootstrap_ci(props, n_boot=n_boot), equivalent=bool(p < alpha))


def per_subject_binomial(cell, alpha=ALPHA):
    """Exact one-sided binomial per subject. Secondary analysis, reported
    individually - a group mean hides a bimodal 'half of them can, half can't',
    which for a product decision is a different fact entirely.
    """
    out = {}
    for subj, trials in cell.items():
        k, n = int(sum(trials)), len(trials)
        p = stats.binom.sf(k - 1, n, CHANCE) if n else math.nan
        out[subj] = dict(k=k, n=n, p=float(p), significant=bool(p < alpha))
    return out


def _bootstrap_ci(props, level=0.95, n_boot=N_BOOTSTRAP, seed=0):
    if not n_boot:                       # simulation path skips this
        return (math.nan, math.nan)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(props), size=(n_boot, len(props)))
    means = props[idx].mean(axis=1)
    lo, hi = np.quantile(means, [(1 - level) / 2, 1 - (1 - level) / 2])
    return (float(lo), float(hi))


def holm(pvalues, alpha=ALPHA):
    """Holm-Bonferroni step-down. Returns {key: reject}.

    Step-down, not plain Bonferroni: uniformly more powerful at the same
    family-wise error rate, and once a hypothesis fails to reject, every less
    significant one is retained too.
    """
    items = sorted(pvalues.items(), key=lambda kv: (math.inf if math.isnan(kv[1])
                                                    else kv[1]))
    m, out, still = len(items), {}, True
    for i, (key, p) in enumerate(items):
        thresh = alpha / (m - i)
        if still and not math.isnan(p) and p < thresh:
            out[key] = True
        else:
            still = False
            out[key] = False
    return out


# ---------------------------------------------------------------------------
# The pipeline and the decision rule
# ---------------------------------------------------------------------------

def analyse(cells, alpha=ALPHA, margin=EQUIVALENCE_MARGIN,
            n_boot=N_BOOTSTRAP):
    """Run the pre-registered analysis. Returns (results, decision)."""
    detection, equivalence = {}, {}
    for key, cell in cells.items():
        props = subject_proportions(cell)
        pair = tuple(key[1].split("_vs_"))
        if pair in EQUIVALENCE_PAIRS:
            equivalence[key] = equivalence_test(props, margin, alpha, n_boot)
        else:
            detection[key] = detection_test(props, alpha, n_boot)

    # The primary endpoint is tested at full alpha and excluded from the
    # correction; secondaries are Holm-corrected among themselves. Correcting
    # the primary against its own supporting analyses would penalise the study
    # for asking additional questions.
    # The calibration cells' DIFFERENCE tests are their own family of three.
    # Left uncorrected they false-alarmed on ~15% of perfectly good rigs, which
    # both wastes bench time and silently eats 15% of the study's power. Holm
    # across the family brings that back to ~5%. Measured, not assumed.
    cal_rejects = holm({k: v["p_difference"] for k, v in equivalence.items()},
                       alpha)
    for k, v in equivalence.items():
        v["differs"] = bool(cal_rejects.get(k, False))

    secondary = {k: v["p"] for k, v in detection.items() if k != PRIMARY_CELL}
    rejects = holm(secondary, alpha)
    for k, v in detection.items():
        if k == PRIMARY_CELL:
            v["significant"] = bool(not math.isnan(v["p"]) and v["p"] < alpha)
            v["primary"] = True
        else:
            v["significant"] = rejects.get(k, False)
            v["primary"] = False

    return dict(detection=detection, equivalence=equivalence), decide(
        detection, equivalence)


def decide(detection, equivalence):
    """Map results onto the decision fixed in docs/15 section 4.1.

    Order matters: the rig is checked FIRST. A rig that fails calibration makes
    every other cell uninterpretable, and reading a favourable flat2d result off
    a broken rig is exactly how a project talks itself into building the wrong
    thing.
    """
    # Gate on DEMONSTRATED difference, not on failure to demonstrate
    # equivalence. Requiring all three calibration cells to reach equivalence
    # was a conjunction of three ~80%-power tests, i.e. ~51% joint - it failed
    # good rigs about half the time. Simulation caught it.
    broken = [k for k, v in equivalence.items() if v.get("differs")]
    if broken:
        where = ", ".join(f"R={k[0]}" for k in sorted(broken))
        return ("FIX_RIG", f"aerial is measurably distinguishable from a real "
                f"object at {where} - our optics have artefacts (ghosting, "
                f"luminance mismatch, aberration). Every other cell is "
                f"uninterpretable until this is fixed.")

    primary = detection.get(PRIMARY_CELL)
    if primary is None:
        return ("INCOMPLETE", f"the primary cell {PRIMARY_CELL} is missing")

    others = [v for k, v in detection.items()
              if k != PRIMARY_CELL and k[1].endswith("flat2d")]
    n_sig = sum(bool(v["significant"]) for v in others)

    if not primary["significant"]:
        return ("PIVOT", "at the design point R = 1.3 m, free space is not "
                "distinguishable from a 2D screen at the same location. The "
                "model predicted 168x threshold discrimination there, so either "
                "the model is wrong or the advantage is not perceptual. Do not "
                "build the wedge; a much cheaper product does the same job.")
    if n_sig == len(others):
        return ("GO", "free space beats a flat screen at the design point and "
                "at every other distance, and the rig is calibrated. Build the "
                "wedge at R = 1.3 m.")
    return ("GO_NARROW", f"free space wins at the design point but at only "
            f"{n_sig} of {len(others)} other distances. Build the wedge, and "
            "treat the losing distances as the product's actual working limit.")


def report(cells, alpha=ALPHA):
    results, (verdict, why) = analyse(cells, alpha)
    print("PQ-1 results (pre-registered analysis)\n")

    print("EQUIVALENCE cells - calibration, TOST margin "
          f"+/-{EQUIVALENCE_MARGIN}")
    print(f"{'R':>5} {'pair':>20} {'n':>3} {'mean':>7} {'95% CI':>16} "
          f"{'p':>8}  verdict")
    for (R, pair), v in sorted(results["equivalence"].items()):
        ci = f"[{v['ci'][0]:.2f},{v['ci'][1]:.2f}]"
        print(f"{R:>5.1f} {pair:>20} {v['n']:>3} {v['mean']:>7.3f} {ci:>16} "
              f"{v['p']:>8.4f}  {'EQUIVALENT' if v['equivalent'] else 'NOT SHOWN'}")

    print("\nDETECTION cells - one-sided t vs 0.5, Holm-corrected")
    print(f"{'R':>5} {'pair':>20} {'n':>3} {'mean':>7} {'95% CI':>16} "
          f"{'p':>8} {'d':>6}  sig")
    for (R, pair), v in sorted(results["detection"].items()):
        ci = f"[{v['ci'][0]:.2f},{v['ci'][1]:.2f}]"
        print(f"{R:>5.1f} {pair:>20} {v['n']:>3} {v['mean']:>7.3f} {ci:>16} "
              f"{v['p']:>8.4f} {v['d']:>6.2f}  {'YES' if v['significant'] else 'no'}")

    print(f"\nDECISION: {verdict}\n  {why}")
    return results, verdict


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    report(load_trials(sys.argv[1]))
