"""
Synthetic PQ-1 studies with known ground truth.

Purpose: prove the analysis in pq1_analyze.py behaves before spending 15.5
subject-hours on it. Feed it thousands of studies whose true effects you chose,
and check it recovers them - controls type-I error when nothing is there, finds
the effect when it is, and routes to the right decision either way.

This is the cheapest possible way to discover that a study design is broken.
The alternative is discovering it from real data, when the money is gone and
the answer is "inconclusive".

Subject model: each subject has a latent true rate drawn from a Beta with the
requested mean and between-subject SD, then trials are Binomial in that rate.
Beta rather than a clipped Gaussian because proportions live on [0,1] and a
clipped Gaussian piles mass at the boundaries, which would flatter the analysis
by making variance smaller than reality at the extremes.
"""
import pathlib
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from pq1_design import DISTANCES  # noqa: E402

CHANCE = 0.5


def _beta_params(mean, sd):
    """Beta(a, b) with the requested mean and SD, or None if infeasible.

    Max achievable SD for a given mean is sqrt(mean*(1-mean)); asking for more
    is a specification error, not something to silently clamp.
    """
    mean = min(max(mean, 1e-6), 1 - 1e-6)
    var_max = mean * (1 - mean)
    var = min(sd ** 2, var_max * 0.999)
    if var <= 0:
        return None
    k = var_max / var - 1
    return mean * k, (1 - mean) * k


def simulate_cell(true_rate, n_subjects, n_trials, sd_between, rng):
    """{subject: [0/1 trials]} for one cell."""
    ab = _beta_params(true_rate, sd_between)
    if ab is None:
        rates = np.full(n_subjects, true_rate)
    else:
        rates = rng.beta(ab[0], ab[1], size=n_subjects)
    cell = {}
    for i, r in enumerate(rates):
        cell[f"S{i:02d}"] = list(rng.binomial(1, r, size=n_trials))
    return cell


def simulate_study(true_rates, n_subjects=26, trials_ceiling=15,
                   trials_equiv=44, sd_between=0.15, seed=0,
                   distances=DISTANCES):
    """One synthetic study.

    `true_rates`: {pair_name: rate} or {(distance, pair_name): rate}. Pair names
    are the same "a_vs_b" strings the analysis expects.

    Trials per cell follow the design: the calibration cell gets more, because
    establishing equivalence is harder than detecting a large effect.
    """
    rng = np.random.default_rng(seed)
    cells = {}
    for R in distances:
        for key, rate in true_rates.items():
            pair = key[1] if isinstance(key, tuple) else key
            if isinstance(key, tuple) and key[0] != R:
                continue
            n_tr = trials_equiv if pair == "aerial_vs_real" else trials_ceiling
            cells[(R, pair)] = simulate_cell(rate, n_subjects, n_tr,
                                             sd_between, rng)
    return cells


def to_csv(cells, path):
    """Write in the exact shape pq1_analyze.load_trials() reads, so the round
    trip through disk is exercised rather than assumed."""
    with open(path, "w", newline="") as fh:
        fh.write("subject,distance,pair,trial,correct\n")
        for (R, pair), cell in sorted(cells.items()):
            for subj, trials in sorted(cell.items()):
                for i, c in enumerate(trials):
                    fh.write(f"{subj},{R},{pair},{i},{c}\n")


# Named scenarios the tests assert against.
NULL_WORLD = {                      # nothing is distinguishable from anything
    "aerial_vs_real": 0.50,
    "aerial_vs_flat2d": 0.50,
    "aerial_vs_farscreen": 0.50,
}
MODEL_WORLD = {                     # what depth_cues.py predicts
    "aerial_vs_real": 0.50,         # differs only in opacity -> near chance
    "aerial_vs_flat2d": 0.90,       # disparity 44-670x threshold -> ceiling
    "aerial_vs_farscreen": 0.90,
}
BROKEN_RIG_WORLD = {                # our optics have visible artefacts
    "aerial_vs_real": 0.80,
    "aerial_vs_flat2d": 0.90,
    "aerial_vs_farscreen": 0.90,
}
PIVOT_WORLD = {                     # free space buys nothing over a screen
    "aerial_vs_real": 0.50,
    "aerial_vs_flat2d": 0.50,
    "aerial_vs_farscreen": 0.90,    # only the far screen is distinguishable
}


if __name__ == "__main__":
    from pq1_analyze import analyse

    for name, world in (("NULL", NULL_WORLD), ("MODEL", MODEL_WORLD),
                        ("BROKEN_RIG", BROKEN_RIG_WORLD),
                        ("PIVOT", PIVOT_WORLD)):
        cells = simulate_study(world, seed=1)
        _, (verdict, why) = analyse(cells, n_boot=0)
        print(f"{name:>11} world -> {verdict}")
        print(f"              {why[:100]}")
