"""
Guards the documents against the models.

This project's failure mode is documented and recurring: a number is derived,
written into one file, then the derivation changes and the prose does not. It
happened with the 20 cm slab, with the 24-32 depth planes, and with doc 13's
moat claim that doc 05 had already refuted.

So the numbers that appear in prose are asserted here against the code that
produces them. If someone re-derives and the docs go stale, this fails.

These are text assertions, deliberately. They will break on a reformat, and that
is the point - a reformat of a load-bearing number should be a decision, not an
accident.
"""
import pathlib
import sys

import pytest

_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_ROOT / "eng" / "03_PHYSICS"))
sys.path.insert(0, str(_ROOT / "experiments" / "perceptual-quality"))

from accommodation import (  # noqa: E402
    T_BODY, engines_needed, planes_needed, robust_window,
)
from depth_cues import cue_sensitivity_ratio  # noqa: E402
from pq1_design import (  # noqa: E402
    DISTANCES, holm_alpha, subjects_for_equivalence,
    trials_for_within_subject,
)

DOC13 = _ROOT / "docs" / "13_THE_ROOM.md"
DOC15 = _ROOT / "docs" / "15_THE_ACCOMMODATION_BUDGET.md"
PQ_README = _ROOT / "experiments" / "perceptual-quality" / "README.md"
BENCH = _ROOT / "experiments" / "perceptual-quality" / "BENCH.md"


def _text(p):
    assert p.exists(), f"missing document: {p}"
    return p.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# The cue sensitivity ratio
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("doc", [DOC13, DOC15])
def test_sensitivity_ratio_in_prose_matches_the_model(doc):
    assert f"{round(cue_sensitivity_ratio())}×" in _text(doc)


# ---------------------------------------------------------------------------
# The design point
# ---------------------------------------------------------------------------

def test_robust_window_in_doc15_matches_the_model():
    lo, hi = robust_window(wall_offset=3.0)
    assert f"{lo:.2f} – {hi:.2f} m" in _text(DOC15)


def test_engine_count_in_doc13_matches_the_law():
    assert f"N = {round(engines_needed(1.2, 0.5))}" in _text(DOC13)


def test_doc13_no_longer_asserts_the_wrong_plane_count():
    """24-32 planes may appear only inside a struck-through or boxed correction,
    never as a live claim."""
    for line in _text(DOC13).splitlines():
        if "24–32" in line or "24-32" in line:
            assert line.lstrip().startswith(">") or "~~" in line, \
                f"live stale claim: {line[:90]}"


def test_doc15_plane_table_row_matches_the_model():
    """Checks the actual table cells rather than a guessed phrase: doc 15's
    plane-count row for the design point must equal what planes_needed()
    returns for head / shoulders / body."""
    from accommodation import T_HEAD, T_SHOULDERS
    want = [planes_needed(1.2, t) for t in (T_HEAD, T_SHOULDERS, T_BODY)]
    row = "| **1.20 m** | " + " | ".join(f"**{n}**" for n in want) + " |"
    assert row in _text(DOC15), f"expected row: {row}"


def test_doc15_records_the_superseded_figure():
    """The wrong number must still be visible, per METHODOLOGY rule 4 - a
    correction that erases what it corrected teaches nobody anything."""
    assert "24–32" in _text(DOC15)


# ---------------------------------------------------------------------------
# PQ-1 sizing
# ---------------------------------------------------------------------------

def test_subject_count_in_the_protocol_matches_the_power_analysis():
    n = subjects_for_equivalence(margin=0.10, sd=0.15)
    assert f"{n} subjects" in _text(PQ_README)


def test_trial_count_in_the_protocol_matches_the_power_analysis():
    a = holm_alpha()
    per_subj = (trials_for_within_subject(0.90, a) * 2 * len(DISTANCES)
                + trials_for_within_subject(0.75, a) * len(DISTANCES))
    assert f"{per_subj} trials" in _text(PQ_README)


def test_distances_in_the_protocol_match_the_design():
    txt = _text(PQ_README)
    assert " / ".join(f"{d}" for d in DISTANCES) in txt


# ---------------------------------------------------------------------------
# Bench document integrity
# ---------------------------------------------------------------------------

def test_bench_states_the_requirement_that_makes_or_breaks_the_experiment():
    """An AIRR relay images whatever it is fed. A flat source gives a flat
    aerial image, and the whole study becomes a null by construction."""
    txt = _text(BENCH)
    assert "must be a physical 3D object, not a screen" in txt


def test_bench_carries_the_viewing_cone_geometry():
    """The cone follows the same clipping law as doc 13 section 1; if the bench
    ever stops citing it, the two have diverged."""
    txt = _text(BENCH)
    assert "arctan((D/2) / d_BS)" in txt
    assert "21.8°" in txt          # the 200 mm beamsplitter at 250 mm


def test_bench_admits_what_it_cannot_answer():
    txt = _text(BENCH)
    for claim in ("Not the multi-viewer claim", "Not life-size", "Not the wedge"):
        assert claim in txt


def test_every_price_in_the_bench_is_marked_unverified():
    txt = _text(BENCH)
    assert "[UNVERIFIED]" in txt, "prices must carry a tier label (METHODOLOGY §2)"
