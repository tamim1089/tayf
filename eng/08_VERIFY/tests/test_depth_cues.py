"""
Pins the depth-cue budget that corrects docs/13 section 6.

The central claim under test: stereopsis is two to three orders of magnitude
more sensitive to depth than accommodation, at EVERY distance and for EVERY
subject size, because both cues scale as t/R^2 and therefore their ratio is
constant. If test_ratio_is_independent_of_distance_and_size fails, the whole
argument for correcting doc 13 section 6 fails with it.
"""
import math
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "03_PHYSICS"))

from accommodation import T_BODY, T_HEAD, diopter_span  # noqa: E402
from depth_cues import (  # noqa: E402
    CUE_NAMES, DISPLAY_CUES, IPD, RAD2ARCSEC, RIG_QUALITY_COMPARISONS,
    STEREO_THRESHOLD_ARCSEC, accommodation_margin, cue_sensitivity_ratio,
    cue_table, cues_distinguishing, disparity_span, stereo_margin,
)


# ---------------------------------------------------------------------------
# The load-bearing result
# ---------------------------------------------------------------------------

def test_ratio_is_independent_of_distance_and_size():
    """Both cues go as t/R^2, so stereo_margin/accom_margin must be the same
    number for every (R, t). This is the proof, not an approximation."""
    ref = None
    for R in (0.7, 1.0, 1.3, 1.5, 2.0, 2.5, 3.5):
        for t in (0.05, 0.25, 0.35, 0.60):
            r = stereo_margin(R, t) / accommodation_margin(R, t)
            if ref is None:
                ref = r
            assert r == pytest.approx(ref, rel=1e-9), f"varies at R={R}, t={t}"


def test_sensitivity_ratio_pinned():
    assert cue_sensitivity_ratio() == pytest.approx(268, abs=1.0)


@pytest.mark.parametrize("thr,expected", [(10.0, 804), (30.0, 268), (60.0, 134)])
def test_sensitivity_ratio_across_threshold_assumption(thr, expected):
    """Even at the most generous stereoacuity assumption (60 arcsec), stereopsis
    still beats accommodation by >100x. The conclusion does not depend on which
    threshold figure is right."""
    r = cue_sensitivity_ratio(threshold_arcsec=thr)
    assert r == pytest.approx(expected, abs=1.0)
    assert r > 100


def test_closed_form_matches_definition():
    """ratio == ipd * 2 * DOF_HALF / threshold_in_radians."""
    from accommodation import DOF_HALF
    expected = IPD * 2 * DOF_HALF / (STEREO_THRESHOLD_ARCSEC / RAD2ARCSEC)
    assert cue_sensitivity_ratio() == pytest.approx(expected, rel=1e-12)


# ---------------------------------------------------------------------------
# Disparity magnitudes
# ---------------------------------------------------------------------------

def test_disparity_is_exactly_ipd_times_diopter_span():
    for R, t in ((1.3, 0.6), (0.7, 0.25), (2.5, 0.35)):
        assert disparity_span(R, t) == pytest.approx(
            IPD * diopter_span(R, t) * RAD2ARCSEC, rel=1e-12)


@pytest.mark.parametrize("R,t,arcsec", [
    (1.3, T_BODY, 5028),
    (1.3, T_HEAD, 2002),
    (2.5, T_BODY, 1306),
    (0.7, T_BODY, 20111),
])
def test_disparity_span_pinned(R, t, arcsec):
    assert disparity_span(R, t) == pytest.approx(arcsec, rel=1e-3)


def test_the_regime_that_makes_the_product_interesting():
    """At the design point a body is FLAT to accommodation but hugely
    suprathreshold to stereopsis. That combination is the whole reason the
    swept-focus element could be deleted without losing depth."""
    assert accommodation_margin(1.3, T_BODY) < 1.0
    assert stereo_margin(1.3, T_BODY) > 100


def test_stereopsis_never_dies_in_the_usable_range():
    """Accommodation falls below threshold past ~1.0 m; stereopsis does not fall
    below threshold anywhere we care about. Any claim that depth 'disappears' at
    2.5 m is about focus only."""
    for R in (0.7, 1.0, 1.3, 1.5, 2.0, 2.5):
        assert stereo_margin(R, T_BODY) > 40
    assert accommodation_margin(2.5, T_BODY) < 0.2


def test_viewer_inside_subject_raises():
    with pytest.raises(ValueError):
        disparity_span(0.1, T_BODY)


def test_zero_depth_subject_has_no_disparity():
    assert disparity_span(1.3, 0.0) == 0.0


# ---------------------------------------------------------------------------
# The display truth table that sets PQ-1's conditions
# ---------------------------------------------------------------------------

def test_truth_table_is_well_formed():
    for name, row in DISPLAY_CUES.items():
        assert len(row) == len(CUE_NAMES), f"{name} has wrong arity"
        assert all(isinstance(v, bool) for v in row)


def test_aerial_differs_from_real_only_in_opacity():
    """The honest limit: an aerial image is additive and cannot occlude. If this
    ever returns an empty tuple, the model has been flattered - see the comment
    above DISPLAY_CUES."""
    assert cues_distinguishing("aerial", "real") == ("opaque",)
    assert ("aerial", "real") in RIG_QUALITY_COMPARISONS


def test_free_space_beats_a_2d_screen_on_disparity_not_focus():
    diff = cues_distinguishing("aerial", "flat2d")
    assert "disparity" in diff
    assert "accommodation" not in diff      # both are AT R, so focus matches


def test_a_tracked_stereo_screen_is_the_real_competitor():
    """It matches on disparity and parallax. What it cannot do is serve more
    than one viewer - which is therefore the irreducible claim."""
    diff = cues_distinguishing("aerial", "stereo_tracked")
    assert "disparity" not in diff
    assert "motion_parallax" not in diff
    assert "multiviewer" in diff


def test_cue_table_covers_every_distance_and_subject():
    rows = cue_table()
    assert len(rows) == 6 * 3
    assert all(len(r) == 7 for r in rows)
