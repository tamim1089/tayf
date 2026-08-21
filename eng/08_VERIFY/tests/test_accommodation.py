"""
Pins the accommodation budget that docs/13's section 7 correction rests on.

If these fail, docs/13_THE_ROOM.md section 7, docs/15_THE_ACCOMMODATION_BUDGET.md,
and the Phase 3 bench geometry in experiments/perceptual-quality/ are all wrong
together. They are not independent - that is the point of pinning them here.
"""
import math
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "03_PHYSICS"))

from accommodation import (  # noqa: E402
    DOF_HALF, T_BODY, T_HEAD, T_SHOULDERS,
    background_cue, design_window, diopter_span, diopter_span_approx,
    dof_slab, engines_needed, planes_needed, robust_window, sweep_dof_half,
)


# ---------------------------------------------------------------------------
# The load-bearing claim: a person is FLAT to the eye at pod distance
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("R,t,expected", [
    (1.20, T_HEAD, 0.176),      # head at 1.2 m
    (0.70, T_HEAD, 0.527),
    (2.50, T_HEAD, 0.040),
    (1.20, T_BODY, 0.444),      # whole body at 1.2 m, still under one DoF
    (0.70, T_BODY, 1.500),
    (1.00, T_BODY, 0.659),
])
def test_diopter_span_pinned(R, t, expected):
    assert diopter_span(R, t) == pytest.approx(expected, abs=5e-4)


def test_body_fits_one_slab_at_pod_distance():
    """The correction that deletes the swept-focus element and its BOM line."""
    assert diopter_span(1.20, T_BODY) < 2 * DOF_HALF
    assert planes_needed(1.20, T_BODY) == 1
    assert planes_needed(1.20, T_HEAD) == 1


@pytest.mark.parametrize("R,t,n", [
    (0.70, T_BODY, 3),          # too close: subject spans 1.5 D
    (0.70, T_SHOULDERS, 2),
    (1.00, T_BODY, 2),
    (1.20, T_BODY, 1),          # the window opens here
    (2.50, T_BODY, 1),
    (0.70, T_HEAD, 1),
])
def test_planes_needed_pinned(R, t, n):
    assert planes_needed(R, t) == n


def test_doc13_was_wrong_by_more_than_an_order_of_magnitude():
    """doc 13 section 7 specified 24-32 planes. Nothing in the usable range
    needs more than 3, and the design point needs 1."""
    worst = max(planes_needed(R, T_BODY)
                for R in (0.7, 1.0, 1.2, 1.5, 2.0, 2.5))
    assert worst == 3
    assert planes_needed(1.3, T_BODY) == 1


# ---------------------------------------------------------------------------
# Depth of field
# ---------------------------------------------------------------------------

def test_dof_slab_is_metres_thick_not_millimetres():
    near, far, thick = dof_slab(1.0)
    assert near == pytest.approx(0.769, abs=1e-3)
    assert far == pytest.approx(1.429, abs=1e-3)
    assert thick * 1000 == pytest.approx(659, abs=1.0)


def test_beyond_the_horizon_far_bound_is_infinite():
    """Past R = 1/DOF_HALF the eye cannot separate the image from infinity.
    At 0.30 D that horizon is 3.33 m - the reason this must be a pod."""
    horizon = 1.0 / DOF_HALF
    _, far, _ = dof_slab(horizon + 0.5)
    assert far == math.inf
    _, far_inside, _ = dof_slab(horizon - 0.5)
    assert math.isfinite(far_inside)


# ---------------------------------------------------------------------------
# The cue that actually differentiates free space from a screen
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("R,wall,expected,perceptible", [
    (0.70, 3.10, 1.106, True),
    (1.00, 3.40, 0.706, True),
    (1.20, 3.60, 0.556, True),
    (1.50, 3.90, 0.410, True),
    (2.50, 4.90, 0.196, False),     # differentiator is physically absent here
])
def test_background_cue_pinned(R, wall, expected, perceptible):
    cue = background_cue(R, wall)
    assert cue == pytest.approx(expected, abs=5e-4)
    assert (cue >= DOF_HALF) is perceptible


def test_the_wedge_must_not_be_tested_at_2_5_m():
    """Phase 5's explicit warning, pinned: at 2.5 m the cue is below threshold,
    so a wedge tested there returns a false negative on its own differentiator."""
    assert background_cue(2.5, 4.9) < DOF_HALF
    assert background_cue(1.3, 4.3) >= DOF_HALF


# ---------------------------------------------------------------------------
# The design window, and its independence from the one ASSUMED number
# ---------------------------------------------------------------------------

def test_design_window_matches_the_plan():
    lo, hi, rows = design_window(t=T_BODY, wall_offset=2 * 1.2)
    assert lo == pytest.approx(1.05, abs=0.03)
    assert hi == pytest.approx(1.85, abs=0.03)
    assert any(r["passes"] for r in rows)


def test_window_never_closes_across_the_plausible_dof_range():
    """DOF_HALF is [ASSUMED]. If the window vanished at the pessimistic end the
    product would depend on an unverified number. It does not."""
    for dof, (lo, hi) in sweep_dof_half(t=T_BODY, wall_offset=3.0).items():
        assert lo is not None, f"window closed at DOF_HALF={dof}"
        assert hi > lo


def test_robust_window_exists_and_contains_the_design_point():
    """The result that makes the geometry safe: one R works for every plausible
    depth-of-field figure, so the bench cannot invalidate the pod dimensions -
    only the size of the effect."""
    lo, hi = robust_window(t=T_BODY, wall_offset=3.0)
    assert lo is not None, "no single R survives all DOF_HALF values"
    assert lo <= 1.32 <= hi
    assert lo == pytest.approx(1.30, abs=0.03)
    assert hi == pytest.approx(1.35, abs=0.03)


# ---------------------------------------------------------------------------
# Cross-check against doc 13's geometric law
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("z,d,n", [
    (1.2, 0.50, 15),
    (1.5, 0.50, 19),
    (2.5, 0.50, 31),
    (1.2, 0.40, 19),
])
def test_engines_needed_pinned(z, d, n):
    assert round(engines_needed(z, d)) == n


def test_approximation_agrees_with_exact_form():
    """span ~= t/R^2 is quoted in docs/15 as the reasoning shortcut. Hold it to
    the 4% claim over the range it is quoted for."""
    for R in (0.7, 1.0, 1.2, 1.5, 2.0, 2.5):
        exact = diopter_span(R, T_HEAD)
        assert abs(diopter_span_approx(R, T_HEAD) - exact) / exact < 0.04


def test_viewer_inside_the_subject_is_an_error_not_a_silent_wrong_answer():
    with pytest.raises(ValueError):
        diopter_span(0.10, T_BODY)
