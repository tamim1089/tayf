#!/usr/bin/env python3
"""
build_fast.py — wide-net arXiv discovery for the TAYF (Compact Free-Space
Spatial Telepresence Node) research program, adapted from the HF-mirror
fast-metadata-snapshot pattern (see down4.py in a sibling project) instead
of the throttled arXiv API used by build_telepresence.py's `build` phase.

Downloads the full arXiv metadata snapshot ONCE from a HF dataset mirror
(seconds, not hours of paginated API calls), filters locally by category +
date range 2022-01..2026-08, then re-uses build_telepresence.py's keyword
CLUSTERS to score+select papers, merges into the existing corpus.jsonl /
ids.txt (dedup by id, additive — never removes existing entries), so the
already-fetched/documented papers stay valid.

Usage:
    pip install huggingface_hub --break-system-packages   # once
    python3 build_fast.py

Then continue with the existing fetch phase:
    python3 build_telepresence.py fetch --limit 800
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_telepresence import CLUSTERS, CATEGORY_TRACKS, CORPUS, IDS_FILE, TARGET  # noqa: E402

# =====================
# CONFIG
# =====================

YYMM_MIN = "2201"   # Jan 2022
YYMM_MAX = "2608"   # Aug 2026

HF_REPO = "jackkuo/arXiv-metadata-oai-snapshot"
HF_FILENAME = "arxiv-metadata-oai-snapshot.json"

# Categories beyond build_telepresence.py's original set — fills known gaps:
# laser-plasma/aerial-display physics, acoustics (acoustic levitation
# displays), and metasurface/photonic materials (tunable holographic optics).
EXTRA_CATEGORY_TRACKS = {
    "physics.acc-ph": ["OPTICS"],     # laser-plasma, ultrafast pulse physics
    "physics.class-ph": ["OPTICS"],   # acoustics, acoustic levitation
    "physics.flu-dyn": ["OPTICS"],    # acoustic streaming / particle trapping
    "cond-mat.mtrl-sci": ["OPTICS"],  # tunable metasurfaces, PCM materials
    "q-bio.NC": ["PERCEPTION"],       # neuroscience of presence/embodiment
}

# Keyword clusters missing from build_telepresence.py's OPTICS_CLUSTERS —
# these are the free-space-projection mechanisms the project's core premise
# depends on and that the first research pass under-covered.
EXTRA_OPTICS_CLUSTERS = [
    ["acoustic levitation", "acoustic hologram", "ultrasonic levitation", "acoustophoretic"],
    ["Pepper's ghost", "peppers ghost"],
    ["swept volume display", "swept-volume display", "rotating display volumetric"],
    ["aerial imaging plate", "retroreflector display", "AIP display"],
    ["photophoretic trap", "optical tweezer display", "acoustic trap display"],
    ["time-modulated metasurface", "reconfigurable metasurface", "phase change metasurface"],
    ["OAM multiplexing", "orbital angular momentum display"],
]

ALL_CATEGORY_TRACKS = {**CATEGORY_TRACKS, **EXTRA_CATEGORY_TRACKS}
ALL_CLUSTERS = {**CLUSTERS, "OPTICS": CLUSTERS["OPTICS"] + EXTRA_OPTICS_CLUSTERS}


def yymm_for_id(arxiv_id):
    if "/" in arxiv_id:
        return arxiv_id.split("/", 1)[1][:4]
    return arxiv_id[:4]


def in_range(arxiv_id):
    y = yymm_for_id(arxiv_id)
    return YYMM_MIN <= y <= YYMM_MAX


def load_existing():
    papers = {}
    if CORPUS.exists():
        with open(CORPUS) as f:
            for line in f:
                rec = json.loads(line)
                rec["matched"] = set(rec.get("matches", []))
                papers[rec["id"]] = rec
    return papers


def download_snapshot():
    from huggingface_hub import hf_hub_download
    print(f"[FAST] downloading metadata snapshot from {HF_REPO} ...", flush=True)
    t0 = time.time()
    path = hf_hub_download(repo_id=HF_REPO, filename=HF_FILENAME, repo_type="dataset")
    print(f"[FAST] downloaded in {time.time()-t0:.1f}s -> {path}", flush=True)
    return path


def build_text_matchers():
    # tag -> (category, track, cluster_terms, cluster_label)
    matchers = []
    for cat, tracks in ALL_CATEGORY_TRACKS.items():
        for track in tracks:
            for cluster in ALL_CLUSTERS[track]:
                matchers.append((cat, track, [t.lower() for t in cluster], cluster[0]))
    return matchers


def main():
    papers = load_existing()
    print(f"[FAST] loaded {len(papers)} existing papers from {CORPUS.name}", flush=True)

    snap_path = download_snapshot()
    matchers = build_text_matchers()
    wanted_cats = set(ALL_CATEGORY_TRACKS.keys())

    scanned = 0
    new_matches = 0
    t0 = time.time()
    with open(snap_path, "r") as f:
        for line in f:
            scanned += 1
            if scanned % 1_000_000 == 0:
                print(f"[FAST] scanned {scanned}, new_matches {new_matches}, "
                      f"{time.time()-t0:.0f}s elapsed", flush=True)
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            arxiv_id = rec.get("id", "")
            if not arxiv_id or not in_range(arxiv_id):
                continue
            cats = set(rec.get("categories", "").split())
            if not (cats & wanted_cats):
                continue

            title = (rec.get("title") or "").replace("\n", " ")
            abstract = (rec.get("abstract") or "").replace("\n", " ")
            blob = (title + " " + abstract).lower()

            hit_clusters = set()
            for cat, track, terms, label in matchers:
                if cat not in cats:
                    continue
                if any(t in blob for t in terms):
                    hit_clusters.add(f"{track}:{label}")

            if not hit_clusters:
                continue

            existing = papers.get(arxiv_id)
            if existing:
                before = len(existing["matched"])
                existing["matched"] |= hit_clusters
                if len(existing["matched"]) > before:
                    new_matches += 1
                continue

            primary = rec.get("categories", "").split()[0] if rec.get("categories") else ""
            papers[arxiv_id] = {
                "id": arxiv_id,
                "title": " ".join(title.split()),
                "abstract": " ".join(abstract.split()),
                "published": (rec.get("versions") or [{}])[0].get("created", ""),
                "categories": sorted(cats),
                "primary": primary,
                "authors": 0,
                "matched": hit_clusters,
            }
            new_matches += 1

    print(f"[FAST] scanned {scanned} total records, {len(papers)} unique matched papers "
          f"({new_matches} new/updated)", flush=True)

    rows = []
    for pid, p in papers.items():
        rows.append((len(p["matched"]), p.get("published", ""), pid, p))
    rows.sort(key=lambda r: (-r[0], r[1]))

    with open(CORPUS, "w") as f:
        for _, _, pid, p in rows:
            rec = {k: v for k, v in p.items() if k != "matched"}
            rec["score"] = len(p["matched"])
            rec["matches"] = sorted(p["matched"])
            f.write(json.dumps(rec) + "\n")

    selected = rows[:TARGET]
    optics_only = [r for r in rows if any("OPTICS" in m for m in r[3]["matched"])]
    for r in optics_only:
        if r not in selected:
            selected.append(r)

    with open(IDS_FILE, "w") as f:
        for _, _, pid, _ in sorted(selected, key=lambda r: r[2]):
            f.write(pid + "\n")

    print(f"[FAST] corpus={len(rows)} selected={len(selected)} -> {IDS_FILE.name}", flush=True)


if __name__ == "__main__":
    main()
