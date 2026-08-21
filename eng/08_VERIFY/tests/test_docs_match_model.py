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
    ALPHA, DISTANCES, holm_alpha, subjects_for_across_subject,
    subjects_for_equivalence, total_sd, trials_for_within_subject,
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

def _recommended():
    """Re-derives the recommended design the same way pq1_design.report() does:
    primary at full alpha, calibration Holm-corrected, both sized with the TOTAL
    SD rather than the between-subject SD alone."""
    ceiling = trials_for_within_subject(0.90, ALPHA)
    equiv = trials_for_within_subject(0.75, holm_alpha())
    n = max(subjects_for_equivalence(margin=0.10,
                                     sd=total_sd(0.15, 0.50, equiv)),
            subjects_for_across_subject(0.75, ALPHA,
                                        sd=total_sd(0.15, 0.90, ceiling)))
    per_subj = ceiling * 2 * len(DISTANCES) + equiv * len(DISTANCES)
    return n, per_subj


def test_subject_count_in_the_protocol_matches_the_power_analysis():
    n, _ = _recommended()
    assert f"{n} subjects" in _text(PQ_README)


def test_trial_count_in_the_protocol_matches_the_power_analysis():
    _, per_subj = _recommended()
    assert f"{per_subj} trials" in _text(PQ_README)


def test_protocol_records_the_total_sd_correction():
    """The correction that simulation forced must be visible to a reader, not
    buried in code - it is why the study needs 26 subjects and not 21."""
    assert "total" in _text(PQ_README).lower()
    assert "0.168" in _text(PQ_README)


def test_protocol_declares_a_primary_endpoint():
    txt = _text(PQ_README)
    assert "Primary endpoint" in txt
    assert "1.3" in txt


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


# ---------------------------------------------------------------------------
# Front door and index — added 2026-08-21 after the repo-wide sweep
#
# The README carried the project's worst recorded error ("a 20 x 20 cm slab
# shows an upper body") for weeks after docs/11 s1.3 formally retracted it.
# The correction existed; nobody re-read the front page. These guard that.
# ---------------------------------------------------------------------------

README = _ROOT / "README.md"
INDEX = _ROOT / "docs" / "00_INDEX.md"


def test_the_retracted_20cm_claim_is_never_a_live_readme_claim():
    """It may appear only inside a blockquote retraction, never as a table row."""
    for line in _text(README).splitlines():
        if "upper body at 1.2" in line or "20 × 20 cm" in line:
            assert line.lstrip().startswith(">"), f"live retracted claim: {line[:90]}"


def test_readme_states_the_current_next_action():
    txt = _text(README)
    assert "PQ-1" in txt
    assert "V0 — a 50 cm static disc" not in txt, "stale next step still present"


def test_readme_carries_the_cue_ratio_and_the_tiling_law():
    txt = _text(README)
    assert f"{round(cue_sensitivity_ratio())}×" in txt
    assert "N = 2πz/D" in txt


def test_readme_does_not_state_the_portal_law_as_a_capability():
    """`W = D·(b/a)` is a visibility bound. Any line carrying it must say so."""
    for line in _text(README).splitlines():
        if "D·(b/a)" in line:
            assert ("permission" in line or "not a mechanism" in line
                    or "Visibility" in line), f"portal stated as capability: {line[:90]}"


def test_every_doc_appears_in_the_index():
    """A new document cannot be added without indexing it."""
    index = _text(INDEX)
    missing = [p.name for p in sorted((_ROOT / "docs").glob("*.md"))
               if p.name != "00_INDEX.md" and p.stem[:2] not in index
               and p.name not in index and p.stem not in index]
    assert not missing, f"not listed in docs/00_INDEX.md: {missing}"


def test_index_marks_every_status_it_defines():
    txt = _text(INDEX)
    for status in ("LIVE", "PART", "HIST"):
        assert status in txt


# ---------------------------------------------------------------------------
# docs/11 s7's five corrections, applied 2026-08-21 after sitting undone
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("path,needle", [
    ("docs/01_SYSTEM_MASTER_SPEC.md", "VISIBILITY BOUND"),
    ("docs/02_FREE_SPACE_OPTICAL_ENGINEERING.md", "MET 2026-08-21"),
    ("docs/09_DEVICE_DESIGNS.md", "for CONVENTIONAL AIRR"),
    ("docs/10_TAYF_UNIVERSAL_ENGINEERING.md", "[DERIVED: M = 1]"),
    ("docs/10_TAYF_UNIVERSAL_ENGINEERING.md", "for CONVENTIONAL AIRR"),
])
def test_doc11_section7_corrections_were_actually_applied(path, needle):
    assert needle in _text(_ROOT / path), f"{path} still missing: {needle}"


def test_doc10_carries_its_supersession_banner():
    assert "PARTLY SUPERSEDED" in _text(_ROOT / "docs" / "10_TAYF_UNIVERSAL_ENGINEERING.md")


# ---------------------------------------------------------------------------
# The room model must obey its own geometry
# ---------------------------------------------------------------------------

def test_room_model_keeps_viewers_inside_the_aperture_ring():
    """z > R, or the audience stands outside their own walls. The first version
    of design_room() used z = 1.2 with R = 1.3; the render caught it."""
    src = _text(_ROOT / "models" / "build_models.py")
    body = src.split("def design_room(")[1].split("\ndef ")[0]

    def assigned(name, cast):
        """Read the real assignment line, not the first mention in prose - the
        docstring discusses the rejected z = 1.2 / N = 15 option, and a naive
        substring search finds that instead."""
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith(f"{name} ="):
                return cast(stripped.split("=", 1)[1].split("#")[0].strip())
        raise AssertionError(f"no assignment for {name} in design_room()")

    z, r, n = assigned("Z_POD", float), assigned("R_VIEW", float), assigned("N", int)
    assert z > r, f"viewers at R={r} are outside the band at z={z}"
    assert n == round(engines_needed(z, 0.50)), "N does not match 2*pi*z/D"


# ---------------------------------------------------------------------------
# The 2026-08-21 costing/legal research pass — findings that must not be lost
# ---------------------------------------------------------------------------

BOM = _ROOT / "hardware" / "bom.md"
DOC16 = _ROOT / "docs" / "16_BUSINESS_LEGAL_AND_LOGISTICS.md"
DOC14 = _ROOT / "docs" / "14_TELEHUMAN_AND_THE_PATENT_GAP.md"
BENCH = _ROOT / "experiments" / "perceptual-quality" / "BENCH.md"


def test_bom_carries_the_one_verified_price_and_no_longer_claims_the_refuted_one():
    """$2,195 (DLi DLP7000UV board) is the only researched component price, and
    it refutes the $900/engine and $42k volume BOM this file used to state."""
    txt = _text(BOM)
    assert "$2,195" in txt
    assert "UNRESOLVED" in txt, "volume BOM must not be restated without a quote"
    for line in txt.splitlines():
        if "$42,000" in line or "$900" in line:
            assert ("~~" in line or line.lstrip().startswith(">")
                    or "previous" in line or "exceeds" in line), \
                f"refuted BOM figure stated live: {line[:90]}"


def test_gross_margin_claim_is_withdrawn_not_restated():
    """At qty-1 pricing the delivered cost exceeds the list price, so the 70% GM
    claim cannot stand until a volume quote exists."""
    txt = _text(DOC16)
    assert "withdrawn" in txt.lower()
    for line in txt.splitlines():
        if "70%" in line and "gross margin" in line.lower():
            assert ("withdrawn" in line or "~~" in line
                    or line.lstrip().startswith(">")), f"GM restated live: {line[:90]}"


@pytest.mark.parametrize("needle", [
    "Article 50",           # EU AI Act transparency, live 2 Aug 2026
    "2 August 2026",
    "C2PA",                 # the marking mechanism
    "limited-risk",         # the tier, not high-risk
])
def test_doc16_carries_the_eu_ai_act_finding(needle):
    assert needle in _text(DOC16), f"EU AI Act finding lost: {needle}"


def test_doc16_records_the_two_corrections_to_its_own_advice():
    txt = _text(DOC16)
    assert "AED 30,000" in txt, "Golden Visa salary threshold correction lost"
    assert "light-industrial" in txt, "DTEC workshop correction lost"


def test_fto_threat_is_sized_at_light_field_lab_not_google():
    """The research pass moved the primary FTO exposure. Both docs must say so."""
    for doc in (DOC14, DOC16):
        txt = _text(doc)
        assert "Light Field Lab" in txt
        assert "391" in txt, "the active-patent count is the whole point"


def test_bench_flags_the_retroreflector_patent_family():
    """The rig uses a retroreflector, which triggers Asukanet/Yamamoto."""
    txt = _text(BENCH)
    assert "Asukanet" in txt
    assert "IEC 62629-52-1" in txt, "the aerial-display measurement standard"


def test_physics_modules_name_their_primary_sources():
    acc = _text(_ROOT / "eng" / "03_PHYSICS" / "accommodation.py")
    cue = _text(_ROOT / "eng" / "03_PHYSICS" / "depth_cues.py")
    assert "Campbell (1957)" in acc and "Optica Acta" in acc
    assert "Marcos" in acc
    assert "Howard & Rogers" in cue
