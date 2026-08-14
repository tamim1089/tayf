#!/usr/bin/env python3
"""
assemble.py — merges per-batch reading entries into research/deepseek_research.md.

Entry file format (one per paper, separated by blank lines):
---
ID: 2506.12345
TITLE: ...
TRACK: 1   (1=Optics 2=Human 3=Transport 4=Perception; omitted -> auto-classify)
DESCRIPTION: ... (may span many lines)

Usage:
    python3 assemble.py add <entryfile>     # parse entries, insert into sections
    python3 assemble.py classify <id>       # print track+title for an id
    python3 assemble.py init                # create skeleton doc if missing
"""

import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
DOC = BASE / "research" / "deepseek_research.md"
CORPUS = BASE / "research" / "arxiv" / "corpus.jsonl"

SECTIONS = {
    1: "## Track 1 — Free-Space Optical Engine (volumetric / holographic / light-field / aerial)",
    2: "## Track 2 — Human Representation & Capture (avatars, gaussian splatting, view synthesis)",
    3: "## Track 3 — Compression, Transport & Latency (codecs, streaming, WebRTC)",
    4: "## Track 4 — Perception & Presence (thresholds, quality, psychophysics)",
}
MARKERS = {k: f"<!-- SECTION{k}-END -->" for k in SECTIONS}

TRACK_PRIORITY = ["OPTICS", "HUMAN", "TRANSPORT", "PERCEPTION"]

_corpus = None


def corpus():
    global _corpus
    if _corpus is None:
        _corpus = {}
        if CORPUS.exists():
            with open(CORPUS) as f:
                for line in f:
                    try:
                        r = json.loads(line)
                    except Exception:
                        continue
                    _corpus[r["id"]] = r
    return _corpus


def classify(pid):
    rec = corpus().get(pid, {})
    matches = rec.get("matches", [])
    track = None
    for t in TRACK_PRIORITY:
        if any(m.startswith(t + ":") for m in matches):
            track = TRACK_PRIORITY.index(t) + 1
            break
    return track, rec.get("title", "")


def parse_entries(text):
    entries = []
    blocks = re.split(r"\n(?=---\nID:)", text)
    for b in blocks:
        m = re.match(r"---\s*\nID:\s*(\S+)\s*\nTITLE:\s*(.*?)\s*\n(?:TRACK:\s*(\d)\s*\n)?DESCRIPTION:\s*\n?(.*?)\s*$", b, re.S)
        if not m:
            continue
        pid, title, track, desc = m.group(1), m.group(2).strip(), m.group(3), m.group(4).strip()
        if not track:
            track, ctitle = classify(pid)
            if not title:
                title = ctitle
        if not title:
            title = corpus().get(pid, {}).get("title", "unknown")
        desc = desc.replace("\n", "\n")
        entries.append((pid, title, int(track) if track else 1, desc))
    return entries


def ensure_doc():
    if DOC.exists() and DOC.stat().st_size > 1000:
        return
    header = """# DeepSeek Brainstorming — Research Corpus for the Compact Free-Space Spatial Telepresence Node

> Working concept: two identical ~10 cm × 10 cm × 10 cm autonomous cubes capture their local humans,
> compute compact dynamic representations, transmit them over a low-latency network, and reconstruct
> the remote human directly into free space (no wall, screen, headset, or external projector).
>
> Pipeline: capture → compact dynamic human representation → network transport → reconstruction →
> free-space optical emission. Three frontiers: computational representation, network/temporal
> transport, free-space optical engine (volumetric, holographic, light-field, aerial-imaging, or hybrid).
>
> Central hypothesis: *a remote human can be perceptually reconstructed in free space using a
> physically compact optical engine if the human is represented by a sufficiently efficient dynamic
> neural representation and the optical system generates only perceptually necessary spatial and
> angular information.*

## Method

- Corpus: arXiv 2022-01 → 2026-08, built by `research/arxiv/build_telepresence.py` (per-category
  keyword-cluster queries across 14 categories: physics.optics, physics.app-ph, eess.IV, eess.SP,
  cs.GR, cs.CV, cs.LG, cs.AI, stat.ML, cs.NI, cs.MM, cs.IT, cs.HC, cs.SD).
- Each paper was read from its arXiv e-print source (LaTeX) or PDF text in full, then documented
  here with ID, title, and a long paragraph: what the paper does (methods, math, results) and how
  it can serve this project. Sources are deleted from disk immediately after documentation.
- Section 5 contains Agent 1's independent web research (vendors, patents, standards, non-arXiv works).

"""
    with open(DOC, "w") as f:
        f.write(header)
        for k, title in SECTIONS.items():
            f.write(f"\n{title}\n\n")
            f.write(f"<!-- SECTION{k}-END -->\n")
        f.write("\n## Section 5 — Online Research Findings (Agent 1)\n\n")
        f.write("<!-- SECTION5-END -->\n")


def add_entries(entryfile):
    ensure_doc()
    text = Path(entryfile).read_text()
    entries = parse_entries(text)
    if not entries:
        print(f"no entries parsed from {entryfile}")
        return
    doc = DOC.read_text()
    by_track = {k: [] for k in SECTIONS}
    for pid, title, track, desc in entries:
        by_track.setdefault(track, []).append((pid, title, desc))
    for track, items in by_track.items():
        if not items:
            continue
        marker = MARKERS[track]
        if marker not in doc:
            print(f"WARN: marker {marker} missing")
            continue
        body = "".join(
            f"### {pid} — {title}\n\n{desc}\n\n" for pid, title, desc in items
        )
        doc = doc.replace(marker, body + marker)
    DOC.write_text(doc)
    print(f"added {len(entries)} entries from {entryfile}")


def classify_cmd(pid):
    track, title = classify(pid)
    print(f"TRACK {track} | {title}")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "add":
        add_entries(sys.argv[2])
    elif len(sys.argv) >= 3 and sys.argv[1] == "classify":
        classify_cmd(sys.argv[2])
    elif len(sys.argv) == 2 and sys.argv[1] == "init":
        ensure_doc()
        print("doc initialized")
    else:
        print(__doc__)