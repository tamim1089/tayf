#!/usr/bin/env python3
"""
ready.py — list papers whose sources are downloaded, chunk into agent batches.

Usage:
    python3 ready.py --n 10        # write up to 10 batch files (20 papers each)
    python3 ready.py --status      # counts only
"""
import argparse
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
ARX = BASE / "research" / "arxiv"
RAW_DIR = ARX / "raw"
TMP_SRC = BASE / "research" / "papers" / "tmp" / "src"
TMP_TXT = BASE / "research" / "papers" / "tmp" / "txt"
BATCH_DIR = ARX / "batches"
ASSIGNED = ARX / "assigned.txt"
BATCH_SIZE = 20
TRACK_PRIORITY = ["OPTICS", "HUMAN", "TRANSPORT", "PERCEPTION"]


def track_of(matches):
    for t in TRACK_PRIORITY:
        if any(m.startswith(t + ":") for m in matches):
            return TRACK_PRIORITY.index(t) + 1
    return 2


def meta():
    out = {}
    for rf in sorted(RAW_DIR.glob("raw_*.jsonl")):
        with open(rf) as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                m = out.setdefault(rec["id"], {"title": rec["title"], "matches": set()})
                m["matches"].add(rec["cluster"])
    return out


def ready_ids(meta_map):
    assigned = set()
    if ASSIGNED.exists():
        assigned = set(ASSIGNED.read_text().split())
    ready = []
    for pid in sorted(meta_map):
        if pid in assigned:
            continue
        src = TMP_SRC / pid
        if src.exists() and any(src.iterdir()):
            ready.append(pid)
        else:
            txt = TMP_TXT / f"{pid.replace('/', '_')}.txt"
            if txt.exists() and txt.stat().st_size > 500:
                ready.append(pid)
    return ready, assigned


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--size", type=int, default=BATCH_SIZE)
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    meta_map = meta()
    ready, assigned = ready_ids(meta_map)
    print(f"corpus_ids={len(meta_map)} assigned={len(assigned)} ready={len(ready)}")

    if args.status:
        return

    BATCH_DIR.mkdir(exist_ok=True)
    batches = [ready[i:i + args.size] for i in range(0, len(ready), args.size)][:args.n]
    written = 0
    for bi, batch in enumerate(batches):
        bf = BATCH_DIR / f"batch_{bi:02d}.tsv"
        if bf.exists():
            continue
        with open(bf, "w") as f:
            for pid in batch:
                m = meta_map[pid]
                src = TMP_SRC / pid
                if src.exists() and any(src.iterdir()):
                    path = str(src)
                    kind = "tex"
                else:
                    path = str(TMP_TXT / f"{pid.replace('/', '_')}.txt")
                    kind = "pdf"
                f.write(f"{pid}\t{kind}\t{path}\t{track_of(m['matches'])}\t{m['title']}\n")
        with open(ASSIGNED, "a") as f:
            f.write("\n".join(batch) + "\n")
        written += 1
        print(f"batch_{bi:02d} -> {len(batch)} papers")
    print(f"wrote {written} batch files")


if __name__ == "__main__":
    main()