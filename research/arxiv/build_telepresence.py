#!/usr/bin/env python3
"""
build_telepresence.py — arXiv corpus builder + e-print source downloader
for the Compact Free-Space Spatial Telepresence research program.

Phase 1 (BUILD): query arXiv API per (category x keyword-cluster), save
                  title+abstract corpus, rank by #clusters matched, write ids.txt.
Phase 2 (FETCH):  async download e-print SOURCES (tex) from export.arxiv.org,
                  extract only text files (.tex/.bib/.bbl/.sty), fall back to
                  PDF->pdftotext when no source exists. Resume-safe.

Usage:
    python3 build_telepresence.py build
    python3 build_telepresence.py fetch --limit 500 --from-manifest queued
"""

import asyncio
import aiohttp
import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

# =====================
# CONFIG
# =====================

BASE = Path(__file__).resolve().parent.parent.parent
ARX = BASE / "research" / "arxiv"
CORPUS = ARX / "corpus.jsonl"
RAW_DIR = ARX / "raw"
IDS_FILE = ARX / "ids.txt"
MANIFEST = ARX / "manifest.csv"
TMP_DL = BASE / "research" / "papers" / "tmp" / "dl"
TMP_SRC = BASE / "research" / "papers" / "tmp" / "src"
TMP_TXT = BASE / "research" / "papers" / "tmp" / "txt"

DATE_LO = "202201010000"
DATE_HI = "202608312359"
SLEEP = 3.0
TARGET = 3000
API = "https://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

DOWNLOAD_CONCURRENCY = 64
TEXT_EXTS = {".tex", ".bib", ".bbl", ".sty", ".txt", ".aux", ".cls", ".def"}

# =====================
# TRACK KEYWORD CLUSTERS
# =====================

OPTICS_CLUSTERS = [
    ["light field display", "lightfield display"],
    ["holographic display"],
    ["aerial display", "aerial imaging", "aerial image", "image in air", "mid-air image"],
    ["volumetric display", "volumetric image"],
    ["femtosecond laser plasma", "laser-induced plasma", "laser plasma display", "optical plasma"],
    ["spatial light modulator", "SLM holograph"],
    ["autostereoscopic", "glasses-free 3D display"],
    ["metasurface holograph", "holographic metasurface"],
    ["computational display"],
    ["optical trap display", "trap display"],
    ["directional backlight", "directional light", "parallax barrier", "microlens array display"],
    ["free-space light field", "volumetric image projection"],
    ["plasma voxel", "plasma volume display", "super-resolution display"],
]

HUMAN_CLUSTERS = [
    ["gaussian splatting", "3D gaussian splat", "Gaussian Splatting"],
    ["neural avatar", "human avatar", "codec avatar"],
    ["neural radiance field", "NeRF"],
    ["view synthesis", "novel view synthesis", "new view synthesis"],
    ["human reconstruction", "3D human", "human digitization", "monocular human"],
    ["animatable avatar", "animatable human", "driven avatar"],
    ["telepresence", "holoportation"],
    ["SMPL", "SMPL-X", "parametric body"],
    ["hand pose", "hand tracking", "hand reconstruction", "hand avatar"],
    ["head avatar", "face reconstruction", "talking head", "facial animation", "head synthesis"],
    ["volumetric video", "dynamic scene reconstruction", "4D reconstruction"],
    ["human rendering", "human performance", "monocular avatar"],
    ["mesh registration", "avatar driving", "expression transfer", "motion retargeting"],
]

TRANSPORT_CLUSTERS = [
    ["point cloud compression", "V-PCC", "G-PCC", "dynamic point cloud"],
    ["neural compression", "learned compression", "rate-distortion", "neural codec"],
    ["low latency streaming", "low-latency video", "real-time streaming"],
    ["WebRTC", "real-time communication"],
    ["4D gaussian", "dynamic gaussian", "gaussian streaming"],
    ["immersive video", "volumetric streaming", "volumetric video transmission"],
    ["audio-driven facial", "audio-driven avatar", "speech-driven animation"],
    ["video conferencing", "remote collaboration", "mixed reality collaboration"],
    ["gaussian codec", "splat compression", "3DGS compression"],
    ["predictive coding", "temporal prediction video", "video compression neural"],
]

PERCEPTION_CLUSTERS = [
    ["perceptual quality", "perceptual metric", "quality assessment"],
    ["visual comfort", "visual fatigue", "stereoscopic perception"],
    ["3D display perception", "depth perception display", "motion parallax"],
    ["motion-to-photon", "end-to-end latency"],
    ["sense of presence", "social presence", "co-presence"],
    ["latency perception", "delay perception", "interaction latency"],
    ["light field perception", "holographic perception"],
    ["perceptual rendering", "saliency", "foveated"],
]

CATEGORY_TRACKS = {
    "physics.optics": ["OPTICS"],
    "physics.app-ph": ["OPTICS"],
    "eess.IV": ["OPTICS", "TRANSPORT"],
    "eess.SP": ["TRANSPORT"],
    "cs.GR": ["OPTICS", "HUMAN"],
    "cs.CV": ["HUMAN", "TRANSPORT", "PERCEPTION", "OPTICS"],
    "cs.LG": ["HUMAN"],
    "cs.AI": ["HUMAN"],
    "stat.ML": ["HUMAN"],
    "cs.NI": ["TRANSPORT"],
    "cs.MM": ["TRANSPORT"],
    "cs.IT": ["TRANSPORT"],
    "cs.HC": ["PERCEPTION", "TRANSPORT"],
    "cs.SD": ["TRANSPORT"],
}

CLUSTERS = {
    "OPTICS": OPTICS_CLUSTERS,
    "HUMAN": HUMAN_CLUSTERS,
    "TRANSPORT": TRANSPORT_CLUSTERS,
    "PERCEPTION": PERCEPTION_CLUSTERS,
}

# =====================
# PHASE 1: BUILD CORPUS
# =====================


def fetch(query, start=0, n=2000):
    params = urllib.parse.urlencode({
        "search_query": query, "start": start, "max_results": n,
        "sortBy": "submittedDate", "sortOrder": "descending"})
    url = f"{API}?{params}"
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "arxiv-telepresence-pipeline"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 or attempt < 5:
                wait = 10 * (attempt + 1)
                print(f"  retry in {wait}s ({e.code})", flush=True)
                time.sleep(wait)
            else:
                raise
        except Exception:
            wait = 10 * (attempt + 1)
            print(f"  retry in {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError("fetch failed after retries")


def parse_feed(xml_bytes):
    root = ET.fromstring(xml_bytes)
    out = []
    for e in root.findall("atom:entry", NS):
        raw_id = e.find("atom:id", NS).text
        arxiv_id = re.sub(r"v\d+$", "", raw_id.rsplit("/", 1)[-1])
        primary = e.find("arxiv:primary_category", NS)
        out.append({
            "id": arxiv_id,
            "title": re.sub(r"\s+", " ", (e.findtext("atom:title", "", NS) or "")).strip(),
            "abstract": re.sub(r"\s+", " ", (e.findtext("atom:summary", "", NS) or "")).strip(),
            "published": e.findtext("atom:published", "", NS) or "",
            "categories": [c.get("term") for c in e.findall("atom:category", NS)],
            "primary": primary.get("term") if primary is not None else "",
            "authors": len(e.findall("atom:author", NS)),
        })
    return out


def build_corpus():
    if CORPUS.exists() and IDS_FILE.exists():
        print(f"[BUILD] {CORPUS.name} and {IDS_FILE.name} exist, skipping. Delete to rebuild.", flush=True)
        return

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_files = sorted(RAW_DIR.glob("raw_*.jsonl"))

    papers = {}  # id -> {meta, matched:set}
    loaded_queries = set()
    for rf in raw_files:
        tag = rf.name[4:-6]
        loaded_queries.add(tag)
        with open(rf) as f:
            for line in f:
                rec = json.loads(line)
                p = papers.setdefault(rec["id"], {**rec, "matched": set()})
                p["matched"].add(rec["cluster"])

    total_queries = 0
    new_rows = 0

    for cat, tracks in CATEGORY_TRACKS.items():
        for track in tracks:
            for cluster in CLUSTERS[track]:
                tag = f"{cat}|{track}|{cluster[0]}"
                total_queries += 1
                if tag in loaded_queries:
                    continue
                term = " OR ".join(f'all:"{t}"' for t in cluster)
                query = f'({term}) AND cat:{cat} AND submittedDate:[{DATE_LO} TO {DATE_HI}]'
                start = 0
                got = 0
                while True:
                    try:
                        data = fetch(query, start=start)
                    except Exception as e:
                        print(f"[BUILD ERROR] {cat}/{cluster[0]}: {e}", flush=True)
                        break
                    entries = parse_feed(data)
                    if not entries:
                        break
                    with open(RAW_DIR / f"raw_{tag.replace('/', '_')}.jsonl", "a") as f:
                        for en in entries:
                            f.write(json.dumps({**en, "cluster": f"{track}:{cluster[0]}"}) + "\n")
                            new_rows += 1
                            p = papers.setdefault(en["id"], {**en, "matched": set()})
                            p["matched"].add(f"{track}:{cluster[0]}")
                    got += len(entries)
                    start += 2000
                    time.sleep(SLEEP)
                    if len(entries) < 2000:
                        break
                print(f"[BUILD] {cat:16s} {track:9s} {cluster[0][:34]:34s} -> {got}", flush=True)
                time.sleep(SLEEP)

    print(f"[BUILD] {total_queries} queries, {len(papers)} unique papers", flush=True)

    rows = []
    for pid, p in papers.items():
        rows.append((len(p["matched"]), p["published"], pid, p))
    rows.sort(key=lambda r: (-r[0], r[1]), reverse=False)

    with open(CORPUS, "w") as f:
        for _, _, pid, p in rows:
            rec = {k: v for k, v in p.items() if k != "matched"}
            rec["score"] = len(p["matched"])
            rec["matches"] = sorted(p["matched"])
            f.write(json.dumps(rec) + "\n")

    selected = rows[:TARGET]
    optics_only = [r for r in rows if any("OPTICS" in m for _, _, _, p in [r] for m in p["matched"])]
    for r in optics_only:
        if r not in selected:
            selected.append(r)

    with open(IDS_FILE, "w") as f:
        for _, _, pid, _ in sorted(selected, key=lambda r: r[2]):
            f.write(pid + "\n")

    print(f"[BUILD] corpus={len(rows)} selected={len(selected)} -> {IDS_FILE.name}", flush=True)


# =====================
# PHASE 2: FETCH E-PRINT SOURCES
# =====================

csv_lock = asyncio.Lock()
done = 0
errors = 0


async def write_manifest(row):
    new = not MANIFEST.exists()
    async with csv_lock:
        with open(MANIFEST, "a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["id", "status", "kind", "path"])
            w.writerow(row)


def load_manifest():
    status = {}
    if MANIFEST.exists():
        with open(MANIFEST) as f:
            for row in csv.DictReader(f):
                status[row["id"]] = row
    return status


def extract_sources(arxiv_id, blob):
    """Extract text files from e-print tarball/tex blob. Returns (outdir, ok)."""
    outdir = TMP_SRC / arxiv_id
    outdir.mkdir(parents=True, exist_ok=True)
    if blob[:2] == b"\x1f\x8b":
        import gzip
        try:
            raw = gzip.decompress(blob)
        except Exception:
            raw = blob
        if raw.lstrip().startswith(b"\\documentclass") or raw.lstrip().startswith(b"%") or raw.lstrip().startswith(b"\\input"):
            (outdir / "main.tex").write_bytes(raw)
            return outdir, True
        blob = raw
    if blob[:4] == b"%PDF":
        return None, False
    try:
        tf = tarfile.open(fileobj=__import__("io").BytesIO(blob))
    except Exception:
        return None, False
    n = 0
    for m in tf.getmembers():
        if not m.isfile():
            continue
        name = m.name.lower()
        if not any(name.endswith(ext) for ext in TEXT_EXTS):
            continue
        base = Path(m.name).name
        try:
            data = tf.extractfile(m).read()
        except Exception:
            continue
        if len(data) < 20:
            continue
        (outdir / base).write_bytes(data[:4_000_000])
        n += 1
    tf.close()
    return (outdir, True) if n else (None, False)


def pdf_to_text(arxiv_id):
    pdf = TMP_DL / f"{arxiv_id.replace('/', '_')}.pdf"
    txt = TMP_TXT / f"{arxiv_id.replace('/', '_')}.txt"
    txt.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], capture_output=True)
    return txt if r.returncode == 0 and txt.stat().st_size > 500 else None


async def fetch_one(session, sem, arxiv_id):
    global done, errors
    async with sem:
        src_dir = TMP_SRC / arxiv_id
        if src_dir.exists() and any(src_dir.iterdir()):
            done += 1
            await write_manifest([arxiv_id, "done", "tex", str(src_dir)])
            return
        txt_path = TMP_TXT / f"{arxiv_id.replace('/', '_')}.txt"
        if txt_path.exists() and txt_path.stat().st_size > 500:
            done += 1
            await write_manifest([arxiv_id, "done", "pdf", str(txt_path)])
            return

        url = f"https://export.arxiv.org/e-print/{arxiv_id}"
        blob = None
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=120)) as resp:
                if resp.status == 200:
                    blob = await resp.read()
        except Exception:
            blob = None

        if blob:
            outdir, ok = extract_sources(arxiv_id, blob)
            if ok:
                done += 1
                await write_manifest([arxiv_id, "done", "tex", str(outdir)])
                return

        pdf_url = f"https://export.arxiv.org/pdf/{arxiv_id}"
        data = None
        try:
            async with session.get(pdf_url, timeout=aiohttp.ClientTimeout(total=120)) as resp:
                if resp.status == 200:
                    data = await resp.read()
        except Exception:
            data = None
        if data and len(data) > 1000:
            pdf = TMP_DL / f"{arxiv_id.replace('/', '_')}.pdf"
            pdf.parent.mkdir(parents=True, exist_ok=True)
            pdf.write_bytes(data)
            txt = pdf_to_text(arxiv_id)
            if txt:
                pdf.unlink(missing_ok=True)
                done += 1
                await write_manifest([arxiv_id, "done", "pdf", str(txt)])
                return
            pdf.unlink(missing_ok=True)

        errors += 1
        await write_manifest([arxiv_id, "error", "", ""])
        print(f"[ERROR] {arxiv_id}", flush=True)


async def run_fetch(limit):
    with open(IDS_FILE) as f:
        ids = [x.strip() for x in f if x.strip()]
    status = load_manifest()
    ids = [i for i in ids if status.get(i, {}).get("status") != "done"]
    if limit:
        ids = ids[:limit]
    print(f"[FETCH] {len(ids)} ids to fetch", flush=True)
    sem = asyncio.Semaphore(DOWNLOAD_CONCURRENCY)
    connector = aiohttp.TCPConnector(limit=100, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=connector,
                                     headers={"User-Agent": "arxiv-telepresence-pipeline"}) as session:
        await asyncio.gather(*[fetch_one(session, sem, i) for i in ids])
    print(f"[FETCH] done={done} errors={errors}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    b = sub.add_parser("build")
    b.set_defaults(cmd="build")
    f = sub.add_parser("fetch")
    f.add_argument("--limit", type=int, default=0)
    f.set_defaults(cmd="fetch")
    args = ap.parse_args()

    for d in (TMP_DL, TMP_SRC, TMP_TXT):
        d.mkdir(parents=True, exist_ok=True)

    if args.cmd == "build":
        build_corpus()
        asyncio.run(run_fetch(0))
    elif args.cmd == "fetch":
        asyncio.run(run_fetch(args.limit))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
