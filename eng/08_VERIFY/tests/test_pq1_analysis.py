"""
Proves the PQ-1 analysis works, without collecting a trial.

The design is pre-registered, so the analysis cannot be adjusted once data
arrives. That makes it worth knowing NOW whether it behaves: does it control
false positives when nothing is there, does it find the effect when it is, and
does it route to the right decision either way.

Method: thousands of synthetic studies with ground truth we chose, run through
the identical pipeline the real data will go through, including the CSV round
trip. If these fail, the study would have burned 15.5 subject-hours and returned
a number nobody should believe.
"""
import math
import pathlib
import sys

import numpy as np
import pytest

_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_ROOT / "experiments" / "perceptual-quality"))
sys.path.insert(0, str(_ROOT / "eng" / "03_PHYSICS"))

from pq1_design import PRIMARY_CELL  # noqa: E402
from pq1_analyze import (  # noqa: E402
    ALPHA, CHANCE, EQUIVALENCE_MARGIN, analyse, decide, detection_test,
    equivalence_test, holm, load_trials, per_subject_binomial,
    subject_proportions,
)
from pq1_simulate import (  # noqa: E402
    BROKEN_RIG_WORLD, MODEL_WORLD, NULL_WORLD, PIVOT_WORLD, simulate_cell,
    simulate_study, to_csv,
)

N_STUDIES = 400          # Monte Carlo replications; SE ~ 0.011 at p=0.05
N_DETECTION_CELLS = 6    # 3 distances x 2 detection pairs


def _run(world, seed):
    return analyse(simulate_study(world, seed=seed), n_boot=0)


# ---------------------------------------------------------------------------
# Type-I error - the thing multiplicity correction exists for
# ---------------------------------------------------------------------------

def test_error_rates_match_what_the_design_intends():
    """Three families, three intended rates, all measured under the null:

      primary cell        - deliberately uncorrected, so ~alpha
      secondary detection - Holm across 5, so <= alpha for the whole family
      calibration         - Holm across 3, so <= alpha for the whole family

    The uncorrected rate across 6 detection cells would be 1-(1-.05)^6 = 0.265,
    so the secondary family must land far below that or Holm is not running.
    """
    prim = sec = cal = 0
    for s in range(N_STUDIES):
        results, _ = _run(NULL_WORLD, seed=1000 + s)
        det = results["detection"]
        prim += bool(det[PRIMARY_CELL]["significant"])
        sec += any(v["significant"] for k, v in det.items() if k != PRIMARY_CELL)
        cal += any(v["differs"] for v in results["equivalence"].values())
    prim, sec, cal = prim / N_STUDIES, sec / N_STUDIES, cal / N_STUDIES

    assert prim <= 0.09, f"primary false-positive {prim:.3f} exceeds alpha+slack"
    assert sec <= 0.09, f"secondary FWER {sec:.3f} not controlled"
    assert cal <= 0.09, f"calibration FWER {cal:.3f} not controlled"
    uncorrected = 1 - (1 - ALPHA) ** N_DETECTION_CELLS      # 0.265
    assert sec < uncorrected / 2, "Holm does not appear to be applied"


def test_a_good_rig_is_not_falsely_condemned():
    """Before the calibration family was Holm-corrected this fired on 15% of
    perfectly good rigs, which both wasted bench time and ate 15% of the
    study's power. Measured, not assumed."""
    false_alarms = sum(_run(MODEL_WORLD, seed=8000 + s)[1][0] == "FIX_RIG"
                       for s in range(N_STUDIES))
    assert false_alarms / N_STUDIES <= 0.09


def test_null_world_rarely_routes_to_go():
    n = 120
    gos = sum(_run(NULL_WORLD, seed=2000 + s)[1][0].startswith("GO")
              for s in range(n))
    assert gos / n <= 0.10, f"{gos}/{n} null studies reached GO"


# ---------------------------------------------------------------------------
# Power - can the study find the effect it was sized for
# ---------------------------------------------------------------------------

def test_power_meets_the_design_target_under_the_model():
    """If depth_cues.py is right, the study must reach GO at least 80% of the
    time. Below that, it is underpowered and would report 'inconclusive' after
    the money is spent."""
    gos = sum(_run(MODEL_WORLD, seed=3000 + s)[1][0].startswith("GO")
              for s in range(N_STUDIES))
    power = gos / N_STUDIES
    assert power >= 0.80, f"power {power:.3f} below the 0.80 target"


def test_broken_rig_is_caught_before_anything_else_is_believed():
    """A rig with visible artefacts must route to FIX_RIG even though its
    detection cells look excellent - that is the trap this ordering avoids."""
    caught = sum(_run(BROKEN_RIG_WORLD, seed=4000 + s)[1][0] == "FIX_RIG"
                 for s in range(120))
    assert caught / 120 >= 0.90


def test_pivot_world_routes_to_pivot_not_go():
    """Free space buying nothing over a same-place screen must not be rescued by
    the farscreen cell looking impressive.

    Tolerates the primary endpoint's own alpha: the primary cell is a true null
    here, so it will false-positive at ~5% by construction. Demanding 100% would
    be demanding a test with no type-I error, which does not exist."""
    n = N_STUDIES
    gos = sum(_run(PIVOT_WORLD, seed=5000 + s)[1][0].startswith("GO")
              for s in range(n))
    assert gos / n <= 0.09, f"{gos}/{n} pivot-world studies wrongly reached GO"


# ---------------------------------------------------------------------------
# TOST behaves as an equivalence test, not as a failed significance test
# ---------------------------------------------------------------------------

def test_tost_concludes_equivalence_when_the_truth_is_equivalence():
    rng = np.random.default_rng(7)
    hits = 0
    for _ in range(N_STUDIES):
        cell = simulate_cell(0.50, n_subjects=26, n_trials=44,
                             sd_between=0.15, rng=rng)
        hits += equivalence_test(subject_proportions(cell),
                                 n_boot=0)["equivalent"]
    assert hits / N_STUDIES >= 0.80


def test_tost_refuses_equivalence_when_the_truth_sits_at_the_margin():
    """True rate exactly at the margin: concluding equivalence there is the
    type-I error of an equivalence test and must be rare."""
    rng = np.random.default_rng(11)
    hits = 0
    for _ in range(N_STUDIES):
        cell = simulate_cell(CHANCE + EQUIVALENCE_MARGIN, n_subjects=26,
                             n_trials=44, sd_between=0.15, rng=rng)
        hits += equivalence_test(subject_proportions(cell),
                                 n_boot=0)["equivalent"]
    assert hits / N_STUDIES <= 0.10


def test_a_large_real_difference_is_never_called_equivalent():
    rng = np.random.default_rng(13)
    for _ in range(50):
        cell = simulate_cell(0.85, 26, 44, 0.15, rng)
        assert not equivalence_test(subject_proportions(cell),
                                    n_boot=0)["equivalent"]


# ---------------------------------------------------------------------------
# Holm implementation
# ---------------------------------------------------------------------------

def test_holm_matches_a_worked_example():
    """Worked by hand, and the first version of this test got it wrong: 0.020 is
    LESS than 0.05/2 = 0.025, so it rejects. The implementation was right and
    the expectation was not - recorded because a test that encodes a mistake is
    worse than no test."""
    p = {"a": 0.001, "b": 0.013, "c": 0.020, "d": 0.90}
    r = holm(p, alpha=0.05)
    assert r["a"] is True          # 0.001 < 0.05/4 = 0.0125
    assert r["b"] is True          # 0.013 < 0.05/3 = 0.0167
    assert r["c"] is True          # 0.020 < 0.05/2 = 0.025
    assert r["d"] is False         # 0.900 > 0.05/1 -> retained


def test_holm_stops_when_a_threshold_is_actually_missed():
    """The step-down property: c has p = 0.031 < the naive 0.05, and is still
    retained, because b failed ahead of it.

    My first attempt at this example used {0.001, 0.030, 0.004} and expected c
    to be retained - but Holm SORTS, so 0.004 is tested second, not third, and
    rejects. Two bad hand-worked examples in this file; both kept as comments
    because the mistake is easier to make than to spot."""
    r = holm({"a": 0.001, "b": 0.030, "c": 0.031}, alpha=0.05)
    assert r["a"] is True          # rank 1, 0.001 < 0.05/3 = 0.0167
    assert r["b"] is False         # rank 2, 0.030 > 0.05/2 = 0.025 -> stop
    assert r["c"] is False         # rank 3, 0.031 < 0.05 but retained anyway


def test_holm_stops_at_the_first_failure():
    """Even a tiny p-value after a failure must be retained - that is what makes
    it step-down rather than per-test."""
    r = holm({"big": 0.40, "tiny": 0.0001}, alpha=0.05)
    assert r["tiny"] is True and r["big"] is False
    r2 = holm({"a": 0.03, "b": 0.031}, alpha=0.05)
    assert r2 == {"a": False, "b": False}      # 0.03 > 0.05/2


def test_nan_pvalues_do_not_reject():
    assert holm({"x": math.nan, "y": 0.001})["x"] is False


# ---------------------------------------------------------------------------
# Plumbing - the round trip the real data will actually take
# ---------------------------------------------------------------------------

def test_csv_round_trip_preserves_the_analysis(tmp_path):
    cells = simulate_study(MODEL_WORLD, seed=99)
    path = tmp_path / "trials.csv"
    to_csv(cells, path)
    reloaded = load_trials(path)
    assert set(reloaded) == set(cells)
    a = analyse(cells, n_boot=0)[1][0]
    b = analyse(reloaded, n_boot=0)[1][0]
    assert a == b


def test_calibration_cell_gets_more_trials_than_detection_cells():
    cells = simulate_study(MODEL_WORLD, seed=5)
    equiv = len(next(iter(cells[(1.3, "aerial_vs_real")].values())))
    det = len(next(iter(cells[(1.3, "aerial_vs_flat2d")].values())))
    assert equiv > det


def test_per_subject_binomial_reports_every_subject():
    cells = simulate_study(MODEL_WORLD, seed=6)
    out = per_subject_binomial(cells[(1.3, "aerial_vs_flat2d")])
    assert len(out) == 26
    assert all(0.0 <= v["p"] <= 1.0 for v in out.values())


def test_effect_size_and_ci_are_reported_even_for_a_null_cell():
    """Reporting only 'n.s.' throws away the difference between a tight null and
    a hopelessly noisy one."""
    rng = np.random.default_rng(3)
    cell = simulate_cell(0.50, 26, 44, 0.15, rng)
    r = detection_test(subject_proportions(cell))
    assert not math.isnan(r["d"])
    lo, hi = r["ci"]
    assert not math.isnan(lo) and lo < r["mean"] < hi


def test_too_few_subjects_degrades_safely_rather_than_crashing():
    tiny = {"S0": [1, 0, 1], "S1": [0, 1, 1]}
    r = detection_test(subject_proportions(tiny))
    assert r["significant"] is False and math.isnan(r["p"])
    assert equivalence_test(subject_proportions(tiny))["equivalent"] is False


def test_decide_reports_incomplete_when_the_key_cells_are_missing():
    verdict, _ = decide(detection={}, equivalence={})
    assert verdict == "INCOMPLETE"
