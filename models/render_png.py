#!/usr/bin/env python3
"""
render_png.py — render the TAYF designs straight to PNG.

Pure Python standard library. No numpy, no browser, no CDN, no GPU.
Software rasteriser with a z-buffer, writing PNGs by hand via zlib.

    python3 render_png.py           # all designs, 2 views each
    python3 render_png.py --wide    # bigger images
"""

import argparse
import math
import os
import struct
import zlib

from build_models import DESIGNS

# ----------------------------------------------------------------------
# PNG writer (stdlib only)
# ----------------------------------------------------------------------

def write_png(path, w, h, rgb):
    """rgb = bytearray of w*h*3."""
    raw = bytearray()
    for y in range(h):
        raw.append(0)                       # filter type 0
        raw += rgb[y * w * 3:(y + 1) * w * 3]

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)


# ----------------------------------------------------------------------
# Tiny 3D maths
# ----------------------------------------------------------------------

def norm(v):
    L = math.sqrt(sum(t * t for t in v)) or 1.0
    return (v[0] / L, v[1] / L, v[2] / L)

def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b): return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def look_at(eye, target, up=(0, 1, 0)):
    f = norm(sub(target, eye))
    s = norm(cross(f, up))
    u = cross(s, f)
    return (s, u, f)


def project(p, eye, basis, fov, w, h):
    """World point -> (screen x, screen y, view depth). None if behind camera."""
    s, u, f = basis
    d = sub(p, eye)
    x, y, z = dot(d, s), dot(d, u), dot(d, f)
    if z <= 0.02:
        return None
    scale = (h / 2) / math.tan(math.radians(fov) / 2)
    return (w / 2 + x * scale / z, h / 2 - y * scale / z, z)


# ----------------------------------------------------------------------
# Rasteriser
# ----------------------------------------------------------------------

BG = (11, 13, 16)

PALETTE = {          # base colour, alpha (1.0 = opaque)
    "device":   ((150, 160, 175), 1.0),
    "aperture": (( 79, 209, 232), 0.55),
    "image":    (( 37, 224, 168), 0.80),
    "scale":    (( 78,  90, 106), 1.0),
    "ground":   (( 26,  32,  40), 1.0),
}

def classify(name):
    n = name.lower()
    if "aperture" in n or "glass" in n: return "aperture"
    if "floating" in n: return "image"
    if any(k in n for k in ("scale", "viewer", "operator", "pedestrian")): return "scale"
    return "device"


class Frame:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.col = bytearray(BG * (w * h))
        self.z = [1e30] * (w * h)

    def tri(self, p0, p1, p2, colour, alpha, shade):
        w, h = self.w, self.h
        r, g, b = (int(c * shade) for c in colour)
        minx = max(0, int(min(p0[0], p1[0], p2[0])))
        maxx = min(w - 1, int(max(p0[0], p1[0], p2[0])) + 1)
        miny = max(0, int(min(p0[1], p1[1], p2[1])))
        maxy = min(h - 1, int(max(p0[1], p1[1], p2[1])) + 1)
        if minx > maxx or miny > maxy:
            return
        x0, y0 = p0[0], p0[1]
        d = ((p1[1]-p2[1])*(x0-p2[0]) + (p2[0]-p1[0])*(y0-p2[1]))
        if abs(d) < 1e-9:
            return
        for py in range(miny, maxy + 1):
            row = py * w
            for px in range(minx, maxx + 1):
                fx, fy = px + 0.5, py + 0.5
                l0 = ((p1[1]-p2[1])*(fx-p2[0]) + (p2[0]-p1[0])*(fy-p2[1])) / d
                if l0 < 0: continue
                l1 = ((p2[1]-p0[1])*(fx-p2[0]) + (p0[0]-p2[0])*(fy-p2[1])) / d
                if l1 < 0: continue
                l2 = 1.0 - l0 - l1
                if l2 < 0: continue
                zz = l0*p0[2] + l1*p1[2] + l2*p2[2]
                i = row + px
                if zz >= self.z[i]:
                    continue
                if alpha >= 0.999:
                    self.z[i] = zz
                j = i * 3
                if alpha >= 0.999:
                    self.col[j] = r; self.col[j+1] = g; self.col[j+2] = b
                else:
                    a = alpha
                    self.col[j]   = int(self.col[j]  *(1-a) + r*a)
                    self.col[j+1] = int(self.col[j+1]*(1-a) + g*a)
                    self.col[j+2] = int(self.col[j+2]*(1-a) + b*a)


def render(mesh, eye, target, w, h, fov=40):
    fr = Frame(w, h)
    basis = look_at(eye, target)
    light = norm((0.45, 0.8, 0.5))

    # ground grid, drawn first
    tris = []
    for gx in range(-7, 8):
        for gz in range(-7, 8):
            a = (gx*0.5, 0, gz*0.5); b = ((gx+1)*0.5, 0, gz*0.5)
            c = ((gx+1)*0.5, 0, (gz+1)*0.5); d2 = (gx*0.5, 0, (gz+1)*0.5)
            if (gx + gz) % 2:
                tris.append((a, b, c, "ground")); tris.append((a, c, d2, "ground"))

    bounds = mesh.groups + [("", len(mesh.f))]
    for gi in range(len(mesh.groups)):
        gname, start = bounds[gi]
        end = bounds[gi + 1][1]
        kind = classify(gname)
        for a, b, c in mesh.f[start:end]:
            tris.append((mesh.v[a], mesh.v[b], mesh.v[c], kind))

    # painter's order for the translucent passes: farthest first
    def depth(t):
        cx = (t[0][0]+t[1][0]+t[2][0])/3
        cy = (t[0][1]+t[1][1]+t[2][1])/3
        cz = (t[0][2]+t[1][2]+t[2][2])/3
        return -math.dist((cx, cy, cz), eye)
    opaque = [t for t in tris if PALETTE[t[3]][1] >= 0.999]
    trans  = sorted((t for t in tris if PALETTE[t[3]][1] < 0.999), key=depth)

    for p, q, r, kind in opaque + trans:
        sp = project(p, eye, basis, fov, w, h)
        sq = project(q, eye, basis, fov, w, h)
        sr = project(r, eye, basis, fov, w, h)
        if not (sp and sq and sr):
            continue
        n = norm(cross(sub(q, p), sub(r, p)))
        shade = 0.32 + 0.68 * max(0.0, abs(dot(n, light)))
        colour, alpha = PALETTE[kind]
        fr.tri(sp, sq, sr, colour, alpha, shade)
    return fr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wide", action="store_true")
    args = ap.parse_args()
    W, H = (1600, 1100) if args.wide else (1100, 780)

    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "png")
    os.makedirs(out, exist_ok=True)

    for fn in DESIGNS:
        mesh, name, meta = fn()
        xs = [v[0] for v in mesh.v]; ys = [v[1] for v in mesh.v]; zs = [v[2] for v in mesh.v]
        cx, cy, cz = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2, (min(zs)+max(zs))/2
        target = (cx, cy, cz)
        # fit: half-diagonal of the bounding box, then back off so it fills frame
        ex, ey, ez = max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs)
        radius = 0.5*math.sqrt(ex*ex + ey*ey + ez*ez)
        fov = 40
        dist = radius / math.tan(math.radians(fov)/2) * 1.02

        def orbit(az_deg, el_deg, d=dist):
            az, el = math.radians(az_deg), math.radians(el_deg)
            return (cx + d*math.cos(el)*math.sin(az),
                    cy + d*math.sin(el),
                    cz + d*math.cos(el)*math.cos(az))

        views = {
            "3q":   orbit(52, 16),    # three-quarter: shows depth separation
            "front":orbit(8,  10),    # near head-on: shows aperture spanning image
            "top":  orbit(35, 55),    # elevated: best for the horizontal C2 table
        }
        for vname, eye in views.items():
            fr = render(mesh, eye, target, W, H, fov=fov)
            p = os.path.join(out, f"{name}_{vname}.png")
            write_png(p, W, H, fr.col)
        print(f"  {name:22s} {meta['aperture']:>30}   3 views")

    print(f"\nwrote PNGs -> {out}")


if __name__ == "__main__":
    main()
