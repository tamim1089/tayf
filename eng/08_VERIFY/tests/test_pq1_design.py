"""
Pins the PQ-1 statistical design.

These are not decorative. The go/no-go decision for the whole optical programme
is made from this study, and an underpowered study returns "we don't know" while
costing the same as a good one. If these tests fail, the sample sizes written
into experiments/perceptual-quality/README.md are wrong.
"""
import math
import pathlib
import sys

import pytest

_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_ROOT / "experiments" / "perceptual-quality"))
sys.path.insert(0, str(_ROOT / "eng" / "03_PHYSICS"))

from scipy import stats  # noqa: E402

from pq1_design import (  # noqa: E402
    ALPHA, CONDITION_PAIRS, DISTANCES, MAX_SESSION_MIN, N_TESTS, POWER,
    SECONDS_PER_TRIAL, holm_alpha, predicted_direction, session_plan,
    subjects_for_across_subject, subjects_for_equivalence,
    trials_for_within_subject,
)


# ---------------------------------------------------------------------------
# Multiplicity
# ---------------------------------------------------------------------------

def test_n_tests_matches_the_design():
    assert N_TESTS == len(DISTANCES) * len(CONDITION_PAIRS) == 9


def test_holm_alpha_is_bonferroni_at_rank_1_and_relaxes_after():
    assert holm_alpha(rank=1) == pytest.approx(ALPHA / N_TESTS)
    assert holm_alpha(rank=N_TESTS) == pytest.approx(ALPHA)
    prev = 0
    for r in range(1, N_TESTS + 1):
        a = holm_alpha(rank=r)
        assert a > prev
        prev = a


def test_correction_actually_costs_something():
    """If correcting for multiplicity did not change the sample size, the
    correction would not be doing anything and something would be wrong."""
    assert (trials_for_within_subject(0.75, holm_alpha())
            > trials_for_within_subject(0.75, ALPHA))


# ---------------------------------------------------------------------------
# Within-subject binomial sizing
# ---------------------------------------------------------------------------

def test_trials_decrease_as_the_effect_grows():
    ns = [trials_for_within_subject(p, ALPHA)
          for p in (0.60, 0.65, 0.75, 0.90)]
    assert ns == sorted(ns, reverse=True)


def test_chance_level_effect_is_undetectable():
    assert trials_for_within_subject(0.50, ALPHA) == math.inf
    assert trials_for_within_subject(0.40, ALPHA) == math.inf


@pytest.mark.parametrize("p,alpha_kind,expected", [
    (0.90, "nominal", 8), (0.75, "nominal", 23),
    (0.90, "holm", 15), (0.75, "holm", 44),
])
def test_trials_pinned(p, alpha_kind, expected):
    a = ALPHA if alpha_kind == "nominal" else holm_alpha()
    assert trials_for_within_subject(p, a) == expected


def test_returned_n_really_achieves_the_stated_power():
    """Independent re-derivation: recompute power at the returned n and confirm
    it clears POWER. Guards against an off-by-one in the critical value."""
    for p in (0.65, 0.75, 0.90):
        n = trials_for_within_subject(p, ALPHA)
        k = stats.binom.isf(ALPHA, n, 0.5) + 1
        assert stats.binom.sf(k - 1, n, p) >= POWER
        assert stats.binom.sf(k - 1, n, 0.5) <= ALPHA     # type-I control


# ---------------------------------------------------------------------------
# Across-subject sizing and equivalence
# ---------------------------------------------------------------------------

def test_more_between_subject_variance_needs_more_subjects():
    a = holm_alpha()
    ns = [subjects_for_across_subject(0.65, a, sd=s) for s in (0.10, 0.15, 0.20)]
    assert ns == sorted(ns)


def test_equivalence_needs_more_subjects_than_a_wider_margin():
    assert (subjects_for_equivalence(margin=0.05)
            > subjects_for_equivalence(margin=0.10)
            > subjects_for_equivalence(margin=0.20))


def test_equivalence_sizing_is_near_the_normal_approximation():
    """Sanity check against n ~= (z_a + z_b)^2 * sd^2 / margin^2."""
    sd, margin = 0.15, 0.10
    approx = ((stats.norm.isf(ALPHA) + stats.norm.isf(1 - POWER)) ** 2
              * sd ** 2 / margin ** 2)
    n = subjects_for_equivalence(margin=margin, sd=sd)
    assert approx * 0.7 <= n <= approx * 2.0


def test_calibration_cell_is_sized_for_equivalence_not_significance():
    """The aerial-vs-real cell wants a null. It must be the most demanding cell
    in the study - if it were cheaper than the others, the design would be
    letting itself off the hook on the one result it most wants to believe."""
    equiv = subjects_for_equivalence(margin=0.10, sd=0.15)
    detect = subjects_for_across_subject(0.75, holm_alpha(), sd=0.15)
    assert equiv > detect


# ---------------------------------------------------------------------------
# Feasibility - the constraint that reshaped the design
# ---------------------------------------------------------------------------

def test_the_recommended_session_fits_in_one_sitting():
    ceiling = trials_for_within_subject(0.90, holm_alpha())
    equiv = trials_for_within_subject(0.75, holm_alpha())
    per_subj = ceiling * 2 * len(DISTANCES) + equiv * len(DISTANCES)
    minutes = per_subj * SECONDS_PER_TRIAL / 60.0
    assert minutes <= MAX_SESSION_MIN, f"{minutes:.0f} min exceeds the fatigue limit"


def test_the_six_distance_design_really_was_infeasible():
    """Records why DISTANCES was cut to three - so nobody 'improves' it back."""
    _, minutes, sittings = session_plan(
        trials_for_within_subject(0.75, ALPHA / 18), n_cells=18)
    assert minutes > 120
    assert sittings >= 3


def test_session_plan_arithmetic():
    total, minutes, sittings = session_plan(10, 9, secs=12.0, max_min=45.0)
    assert total == 90
    assert minutes == pytest.approx(18.0)
    assert sittings == 1


# ---------------------------------------------------------------------------
# Predictions are falsifiable
# ---------------------------------------------------------------------------

def test_calibration_pair_is_flagged_as_rig_quality():
    msg, _, _, _ = predicted_direction("aerial", "real", 1.3)
    assert "artefact" in msg.lower()


def test_flat2d_predicted_strong_at_every_distance():
    for R in DISTANCES:
        msg, diff, _, sm = predicted_direction("aerial", "flat2d", R)
        assert "strong" in msg
        assert "disparity" in diff
        assert sm > 40


def test_every_planned_cell_has_a_prediction():
    for a, b in CONDITION_PAIRS:
        for R in DISTANCES:
            msg, diff, am, sm = predicted_direction(a, b, R)
            assert msg and isinstance(msg, str)
            assert am > 0 and sm > 0
