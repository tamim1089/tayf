#!/usr/bin/env python3
"""
build_models.py — 3D models of the five TAYF display designs, to real scale.

Pure Python, zero dependencies. Emits .obj (universal) and .stl (CAD/print).

Every dimension traces to docs/01_SYSTEM_MASTER_SPEC.md §4.3b: an image in the
viewer's own space cannot exceed the aperture that emits it, so each design's
panel is sized to the person it must show. The translucent figure in each scene
is the floating image; the solid grey figure is a real human for scale.

    python3 build_models.py          # writes obj/ and stl/
    python3 build_models.py --list   # just print the dimension table
"""

import argparse
import math
import os
import struct

# ----------------------------------------------------------------------
# Minimal mesh kernel
# ----------------------------------------------------------------------

class Mesh:
    def __init__(self):
        self.v = []          # vertices
        self.f = []          # faces as (i,j,k) 0-based
        self.groups = []     # (name, first_face_index)

    def group(self, name):
        self.groups.append((name, len(self.f)))

    def add(self, verts, faces):
        o = len(self.v)
        self.v.extend(verts)
        self.f.extend([(a + o, b + o, c + o) for a, b, c in faces])

    # ---- primitives ----
    def box(self, cx, cy, cz, w, h, d):
        """Axis-aligned box centred at (cx,cy,cz). w=X h=Y d=Z."""
        x0, x1 = cx - w / 2, cx + w / 2
        y0, y1 = cy - h / 2, cy + h / 2
        z0, z1 = cz - d / 2, cz + d / 2
        verts = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                 (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        faces = [(0, 2, 1), (0, 3, 2),      # back
                 (4, 5, 6), (4, 6, 7),      # front
                 (0, 1, 5), (0, 5, 4),      # bottom
                 (3, 7, 6), (3, 6, 2),      # top
                 (0, 4, 7), (0, 7, 3),      # left
                 (1, 2, 6), (1, 6, 5)]      # right
        self.add(verts, faces)

    def cyl(self, cx, cy, cz, r, h, axis="y", seg=28):
        """Cylinder centred at (cx,cy,cz), length h along `axis`."""
        verts, faces = [], []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            c, s = math.cos(a) * r, math.sin(a) * r
            if axis == "y":
                verts.append((cx + c, cy - h / 2, cz + s))
                verts.append((cx + c, cy + h / 2, cz + s))
            elif axis == "z":
                verts.append((cx + c, cy + s, cz - h / 2))
                verts.append((cx + c, cy + s, cz + h / 2))
            else:  # x
                verts.append((cx - h / 2, cy + c, cz + s))
                verts.append((cx + h / 2, cy + c, cz + s))
        for i in range(seg):
            a0, a1 = 2 * i, 2 * ((i + 1) % seg)
            faces += [(a0, a1, a1 + 1), (a0, a1 + 1, a0 + 1)]
        # caps
        n = len(verts)
        if axis == "y":
            verts += [(cx, cy - h / 2, cz), (cx, cy + h / 2, cz)]
        elif axis == "z":
            verts += [(cx, cy, cz - h / 2), (cx, cy, cz + h / 2)]
        else:
            verts += [(cx - h / 2, cy, cz), (cx + h / 2, cy, cz)]
        for i in range(seg):
            a0, a1 = 2 * i, 2 * ((i + 1) % seg)
            faces += [(n, a1, a0), (n + 1, a0 + 1, a1 + 1)]
        self.add(verts, faces)

    def quad(self, p0, p1, p2, p3):
        """Flat four-corner panel (two triangles, no thickness)."""
        self.add([p0, p1, p2, p3], [(0, 1, 2), (0, 2, 3)])

    def human(self, cx, cz, height=1.70, facing=1.0, seated=False):
        """Blocky human proxy standing on y=0, facing +Z if facing=1."""
        H = height
        if seated:
            # Seated anthropometry (absolute, not scaled by standing height):
            # seat pan 0.45 m, shoulders 1.00 m, top of head 1.28 m.
            k = H / 1.72
            seat = 0.45 * k
            sh = 1.00 * k
            self.box(cx, (seat + sh) / 2, cz, 0.40 * k, sh - seat, 0.24 * k)  # torso
            self.cyl(cx, sh + 0.05 * k, cz, 0.055 * k, 0.10 * k)              # neck
            self.box(cx, sh + 0.18 * k, cz, 0.16 * k, 0.22 * k, 0.20 * k)     # head
            for s_ in (-1, 1):
                self.box(cx + s_ * 0.175 * k, (seat + sh) / 2 + 0.04 * k, cz,
                         0.09 * k, 0.36 * k, 0.10 * k)                        # arms
                self.box(cx + s_ * 0.10 * k, seat - 0.05 * k,
                         cz + facing * 0.20 * k,
                         0.13 * k, 0.11 * k, 0.42 * k)                        # thighs
                self.box(cx + s_ * 0.10 * k, seat / 2 - 0.03 * k,
                         cz + facing * 0.40 * k,
                         0.11 * k, seat - 0.06 * k, 0.11 * k)                 # shins
        else:
            # Anthropometric: shoulder span ~0.27H (46cm at 1.70m), so the
            # figure fits inside a 0.50 m aperture as the geometry requires.
            self.box(cx, 0.72 * H, cz, 0.24 * H, 0.30 * H, 0.14 * H)         # torso
            self.cyl(cx, 0.90 * H, cz, 0.05 * H, 0.07 * H)                   # neck
            self.box(cx, 0.94 * H, cz, 0.12 * H, 0.16 * H, 0.14 * H)         # head
            for s in (-1, 1):
                self.box(cx + s * 0.105 * H, 0.70 * H, cz,
                         0.065 * H, 0.34 * H, 0.065 * H)                      # arms
                self.box(cx + s * 0.062 * H, 0.28 * H, cz,
                         0.095 * H, 0.56 * H, 0.10 * H)                       # legs

    def bust(self, cx, cy, cz, height=0.50):
        """Head + shoulders, vertically centred at cy."""
        H = height
        self.box(cx, cy - 0.30 * H, cz, 1.00 * H, 0.36 * H, 0.42 * H)  # shoulders
        self.cyl(cx, cy - 0.02 * H, cz, 0.13 * H, 0.20 * H)            # neck
        self.box(cx, cy + 0.26 * H, cz, 0.34 * H, 0.42 * H, 0.38 * H)  # head

    # ---- export ----
    def write_obj(self, path, name):
        with open(path, "w") as fh:
            fh.write(f"# TAYF design: {name}\n# units: metres\n")
            for x, y, z in self.v:
                fh.write(f"v {x:.5f} {y:.5f} {z:.5f}\n")
            bounds = self.groups + [("", len(self.f))]
            for gi in range(len(self.groups)):
                gname, start = bounds[gi]
                end = bounds[gi + 1][1]
                fh.write(f"g {gname}\no {gname}\n")
                for a, b, c in self.f[start:end]:
                    fh.write(f"f {a+1} {b+1} {c+1}\n")

    def write_stl(self, path, name):
        tris = []
        for a, b, c in self.f:
            p, q, r = self.v[a], self.v[b], self.v[c]
            u = (q[0] - p[0], q[1] - p[1], q[2] - p[2])
            w = (r[0] - p[0], r[1] - p[1], r[2] - p[2])
            n = (u[1] * w[2] - u[2] * w[1],
                 u[2] * w[0] - u[0] * w[2],
                 u[0] * w[1] - u[1] * w[0])
            L = math.sqrt(sum(t * t for t in n)) or 1.0
            tris.append(((n[0] / L, n[1] / L, n[2] / L), p, q, r))
        with open(path, "wb") as fh:
            fh.write(f"TAYF {name}".ljust(80)[:80].encode())
            fh.write(struct.pack("<I", len(tris)))
            for n, p, q, r in tris:
                fh.write(struct.pack("<12fH", *n, *p, *q, *r, 0))


# ----------------------------------------------------------------------
# The five designs — all dimensions in metres, real scale
# ----------------------------------------------------------------------

def design_mirror():
    """CONSUMER: full-length mirror, life-size standing person floats in front."""
    m = Mesh()
    AW, AH, DEPTH = 0.55, 1.75, 0.20      # aperture 50x170cm, 20cm deep
    FLOAT = 0.20                           # image floats 20cm in front

    m.group("device_frame")
    for sx in (-1, 1):                                        # side rails
        m.box(sx * (AW / 2 + 0.03), AH / 2, 0, 0.06, AH + 0.06, DEPTH)
    for sy in (0, 1):                                         # top / bottom rails
        m.box(0, AH * sy + (0.03 if sy else -0.03), 0, AW, 0.06, DEPTH)
    m.box(0, AH / 2, -DEPTH / 2 + 0.01, AW, AH, 0.02)         # source panel (rear)

    m.group("aperture_plate")
    m.box(0, AH / 2, DEPTH / 2 - 0.005, AW, AH, 0.01)         # AIRR plate (front)

    m.group("floating_image")
    m.human(0, FLOAT + 0.12, height=1.70)                     # the person, life-size

    m.group("viewer_for_scale")
    m.human(1.60, 0.95, height=1.70)
    return m, "01_mirror_fullbody", dict(
        aperture="0.50 x 1.70 m", depth="0.20 m",
        shows="life-size standing person", note="off-state is a mirror")


def design_doorway():
    """CONSUMER/OFFICE: door-frame unit, person stands in the doorway."""
    m = Mesh()
    AW, AH, T = 0.80, 2.00, 0.14
    m.group("door_frame")
    for sx in (-1, 1):
        m.box(sx * (AW / 2 + 0.06), AH / 2, 0, 0.12, AH, T)
    m.box(0, AH + 0.06, 0, AW + 0.24, 0.12, T)
    m.group("aperture_plate")
    m.box(0, AH / 2, T / 2 - 0.005, AW, AH, 0.01)
    m.group("floating_image")
    m.human(0, 0.30, height=1.70)
    m.group("viewer_for_scale")
    m.human(1.85, 1.10, height=1.70)
    return m, "02_doorway", dict(
        aperture="0.80 x 2.00 m", depth="0.14 m",
        shows="life-size person standing in the doorway",
        note="frame is pre-existing architecture")


def design_disc():
    """CONSUMER: 50cm disc on a stand, life-size bust floats in front."""
    m = Mesh()
    R, DEPTH, STAND = 0.25, 0.12, 0.95
    m.group("stand")
    m.cyl(0, 0.015, 0, 0.16, 0.03)                    # base
    m.cyl(0, STAND / 2, 0, 0.022, STAND)              # column
    m.group("device_body")
    m.cyl(0, STAND + R, 0, R, DEPTH, axis="z")        # disc housing
    m.group("aperture_plate")
    m.cyl(0, STAND + R, DEPTH / 2 + 0.004, R * 0.97, 0.008, axis="z")
    m.group("floating_image")
    m.bust(0, STAND + R, DEPTH / 2 + 0.22, height=0.50)
    m.group("viewer_for_scale")
    m.human(1.35, 0.55, height=1.70)
    return m, "03_disc_bust", dict(
        aperture="0.50 m dia", depth="0.12 m",
        shows="life-size head + shoulders", note="cheapest entry point")


def design_shopwindow():
    """ADS: shop-window retrofit, person appears on the sidewalk side."""
    m = Mesh()
    GW, GH = 2.40, 2.20
    m.group("shop_structure")
    m.box(0, GH / 2, -0.60, 3.20, 0.12, 0.12)             # header
    for sx in (-1, 1):
        m.box(sx * 1.60, GH / 2, -0.30, 0.14, GH, 0.60)   # piers
    m.box(0, -0.05, -0.30, 3.20, 0.10, 0.60)              # cill
    m.group("window_glass")
    m.box(0, GH / 2, 0, GW, GH, 0.012)                    # the shop window itself
    m.group("hidden_source_backstage")
    m.box(0, 1.10, -0.55, 1.60, 1.00, 0.08)               # panel inside the shop
    m.group("floating_image")
    m.human(0, 0.55, height=1.75)                          # person on the pavement
    m.group("pedestrians_for_scale")
    m.human(-1.55, 1.95, height=1.68)
    m.human(1.65, 2.05, height=1.72)
    return m, "04_shop_window", dict(
        aperture="2.40 x 2.20 m (existing glass)", depth="0.60 m backstage",
        shows="life-size person on the pavement",
        note="Pepper's ghost; uses infrastructure that already exists")


def design_c2table():
    """DEFENCE: horizontal command table — the geometry inversion."""
    m = Mesh()
    W, D, TOP = 1.50, 1.50, 0.95
    m.group("table")
    m.box(0, TOP - 0.05, 0, W, 0.10, D)                  # body
    for sx in (-1, 1):
        for sz in (-1, 1):
            m.box(sx * 0.62, (TOP - 0.10) / 2, sz * 0.62,
                  0.07, TOP - 0.10, 0.07)                # legs
    m.group("aperture_plate_horizontal")
    m.box(0, TOP + 0.005, 0, W * 0.92, 0.01, D * 0.92)   # faces UP at the operators
    m.group("floating_volume")                            # terrain / battlespace
    for i in range(7):
        for j in range(7):
            x = (i - 3) * 0.17
            z = (j - 3) * 0.17
            hgt = 0.05 + 0.22 * math.exp(-((x * 1.7) ** 2 + (z * 1.7) ** 2))
            m.box(x, TOP + 0.05 + hgt / 2, z, 0.14, hgt, 0.14)
    m.group("operators_for_scale")
    for ang in (0, 90, 200, 290):
        a = math.radians(ang)
        m.human(1.15 * math.cos(a), 1.15 * math.sin(a), height=1.72)
    return m, "05_c2_table", dict(
        aperture="1.50 x 1.50 m, HORIZONTAL", depth="0.35 m",
        shows="terrain / battlespace above the surface",
        note="works because operators look DOWN — the inversion")


def design_folio():
    """PORTABLE: A4 folding unit, life-size human head floats above the base.

    Closed it is a hardback book (30 x 21 x 7 cm, 4.4 L) that goes in any
    laptop bag. Opened, a 45-degree plate stands up and a life-size head
    floats above the base. An A4 aperture is 29.7 x 21 cm; an adult head is
    25 x 16 cm -- so A4 is the smallest bag-friendly size that still shows a
    face at true scale.
    """
    m = Mesh()
    DESK = 0.74                       # sits on a normal desk
    L, D, T = 0.30, 0.21, 0.035       # base footprint

    m.group("desk")
    m.box(0, DESK - 0.02, 0, 1.30, 0.04, 0.65)
    for sx in (-1, 1):
        for sz in (-1, 1):
            m.box(sx * 0.60, (DESK - 0.04) / 2, sz * 0.28,
                  0.05, DESK - 0.04, 0.05)

    m.group("device_base")
    m.box(0, DESK + T / 2, 0, L, T, D)
    m.box(0, DESK + T + 0.004, 0.015, L - 0.03, 0.006, D - 0.05)   # source panel

    m.group("aperture_plate")                                       # 45 deg fold
    y0, y1 = DESK + T, DESK + T + D
    m.quad((-L/2, y0, -D/2), (L/2, y0, -D/2),
           ( L/2, y1,  D/2), (-L/2, y1,  D/2))

    m.group("floating_image")                                       # life-size head
    hy = DESK + T + 0.155
    m.box(0, hy + 0.055, 0.055, 0.165, 0.215, 0.185)                # head
    m.cyl(0, hy - 0.075, 0.055, 0.048, 0.075)                       # neck
    m.box(0, hy - 0.135, 0.055, 0.30, 0.055, 0.16)                  # collar

    m.group("seated_person_for_scale")
    m.human(0.0, 0.80, height=1.72, facing=-1.0, seated=True)
    return m, "06_folio_portable", dict(
        aperture="0.30 x 0.21 m (A4)", depth="0.07 m closed",
        shows="life-size human head",
        note="4.4 L closed - a hardback book, fits any laptop bag")



def design_table_scene():
    """PRODUCT SCENE: 20x20x10 cm slab on a desk. PORTAL MODE.

    Viewer 0.30 m from the slab; upper body appears 1.20 m from the viewer,
    i.e. 0.90 m BEYOND the device. b>a so the image legitimately exceeds the
    aperture (docs/01 4.3b). You look past the slab at them.
    """
    m = Mesh()
    DESK = 0.74
    m.group("desk")
    m.box(0, DESK-0.02, 0.45, 1.40, 0.04, 0.70)
    for sx in (-1,1):
        for sz in (0.16, 0.74):
            m.box(sx*0.64, (DESK-0.04)/2, sz, 0.05, DESK-0.04, 0.05)

    m.group("device_body")                       # 20 x 20 x 10 cm slab
    m.box(0, DESK+0.10, 0.30, 0.20, 0.20, 0.10)
    m.group("aperture_plate")
    m.box(0, DESK+0.10, 0.246, 0.19, 0.19, 0.008)

    m.group("floating_image")                    # upper body, 0.90 m beyond
    zi, base = 1.20, 0.62
    m.box(0, base+0.30, zi, 0.42, 0.52, 0.24)                 # torso
    m.cyl(0, base+0.60, zi, 0.055, 0.10)                       # neck
    m.box(0, base+0.74, zi, 0.17, 0.23, 0.21)                  # head
    for sx in (-1,1):
        m.box(sx*0.185, base+0.32, zi+0.02, 0.10, 0.38, 0.11)  # arms

    m.group("viewer_for_scale")
    m.human(0.0, -0.30, height=1.72, facing=1.0, seated=True)
    return m, "07_scene_table", dict(
        aperture="0.20 x 0.20 m slab", depth="0.10 m",
        shows="life-size upper body, 0.9 m beyond the device",
        note="PORTAL mode (b>a): you look past the slab at them")


def design_chair_scene():
    """PRODUCT SCENE: aperture built into a chair back. IMAGE-IN-FRONT MODE.

    Rule 4 strict: the image floats in FRONT of the aperture, in the room,
    so image <= aperture. An 0.80 m chair back therefore shows a seated
    upper body at true scale, sitting in the chair.
    """
    m = Mesh()
    SEAT, BACK_TOP = 0.45, 1.25
    m.group("chair")
    m.box(0, SEAT, -0.02, 0.55, 0.06, 0.50)                    # seat pan
    for sx in (-1,1):
        for sz in (-1,1):
            m.box(sx*0.24, SEAT/2, sz*0.21, 0.05, SEAT, 0.05)  # legs
    for sx in (-1,1):                                           # back frame
        m.box(sx*0.29, (SEAT+BACK_TOP)/2, -0.26, 0.05, BACK_TOP-SEAT, 0.09)
    m.box(0, BACK_TOP+0.025, -0.26, 0.63, 0.05, 0.09)

    m.group("aperture_plate")                                   # 0.55 x 0.80 m
    m.box(0, (SEAT+BACK_TOP)/2, -0.222, 0.55, BACK_TOP-SEAT, 0.012)

    m.group("floating_image")                                   # seated, in the chair
    m.human(0.0, 0.02, height=1.72, facing=1.0, seated=True)

    m.group("viewer_for_scale")
    m.human(0.0, 1.95, height=1.72, facing=-1.0, seated=True)
    return m, "08_scene_chair", dict(
        aperture="0.55 x 0.80 m (chair back)", depth="0.09 m",
        shows="life-size seated upper body, in the chair",
        note="IMAGE-IN-FRONT mode: rule 4 strict, image <= aperture")



def design_family():
    """THE APERTURE LAW, VISUALISED: aperture size == subject size (in-front mode).

    Four devices side by side at true relative scale, each with the largest
    subject it can show as a real image in the viewer's own space (W <= D).
    The point of the picture is that each cyan plate is exactly as tall as the
    green figure standing in front of it. That is the law, drawn.
    """
    m = Mesh()
    slots = [   # (x, aperture_w, aperture_h, subject)
        (-1.55, 0.25, 0.28, "head"),
        (-0.75, 0.55, 0.55, "bust"),
        ( 0.25, 0.60, 0.85, "seated"),
        ( 1.55, 0.55, 1.75, "standing"),
    ]
    m.group("device_frame")
    for x, aw, ah, _ in slots:
        base = 0.35 if ah < 1.0 else 0.0
        m.box(x, base + ah/2, -0.10, aw + 0.05, ah + 0.05, 0.07)
        if base > 0:                                  # stand for the small ones
            m.cyl(x, base/2, -0.10, 0.02, base)
            m.cyl(x, 0.01, -0.10, 0.10, 0.02)

    m.group("aperture_plate")
    for x, aw, ah, _ in slots:
        base = 0.35 if ah < 1.0 else 0.0
        m.box(x, base + ah/2, -0.062, aw, ah, 0.008)

    m.group("floating_image")
    for x, aw, ah, kind in slots:
        base = 0.35 if ah < 1.0 else 0.0
        if kind == "head":
            cy = base + ah/2
            m.box(x, cy + 0.02, 0.02, 0.17, 0.22, 0.20)
            m.cyl(x, cy - 0.135, 0.02, 0.05, 0.09)
        elif kind == "bust":
            m.bust(x, base + ah/2, 0.02, height=0.50)
        elif kind == "seated":
            cy = base
            m.box(x, cy + 0.28, 0.02, 0.40, 0.52, 0.22)
            m.cyl(x, cy + 0.59, 0.02, 0.055, 0.10)
            m.box(x, cy + 0.73, 0.02, 0.17, 0.23, 0.20)
            for sx in (-1, 1):
                m.box(x + sx*0.18, cy + 0.30, 0.03, 0.09, 0.38, 0.10)
        else:
            m.human(x, 0.02, height=1.72)
    return m, "09_aperture_law", dict(
        aperture="0.25 / 0.55 / 0.60 / 0.55 m",
        depth="n/a", shows="head / bust / seated upper body / standing",
        note="each plate is exactly as tall as the figure it shows: W <= D")


DESIGNS = [design_family, design_table_scene, design_chair_scene, design_folio, design_mirror, design_doorway, design_disc,
           design_shopwindow, design_c2table]


# ----------------------------------------------------------------------
# Self-contained browser viewer (geometry embedded, no server needed)
# ----------------------------------------------------------------------

VIEWER_HTML = """<!doctype html>
<html><head><meta charset="utf-8"><title>TAYF — display designs</title>
<style>
 *{box-sizing:border-box;margin:0;padding:0}
 body{background:#0b0d10;color:#e6e9ef;font:14px/1.5 ui-sans-serif,system-ui,sans-serif;
      height:100vh;display:flex;overflow:hidden}
 #side{width:290px;flex:none;border-right:1px solid #1e242c;padding:22px 20px;
       overflow-y:auto;background:#0e1116}
 h1{font-size:15px;font-weight:600;letter-spacing:.02em;margin-bottom:4px}
 .sub{font-size:12px;color:#7d8794;margin-bottom:22px}
 .item{padding:11px 13px;border:1px solid #1e242c;border-radius:9px;margin-bottom:8px;
       cursor:pointer;transition:.15s}
 .item:hover{border-color:#2f3945;background:#131820}
 .item.on{border-color:#3ba9c7;background:#10222a}
 .item .n{font-weight:600;font-size:13px}
 .item .d{font-size:11px;color:#8b95a3;margin-top:3px}
 #meta{margin-top:22px;padding-top:18px;border-top:1px solid #1e242c;font-size:12px}
 #meta div{margin-bottom:9px}
 #meta .k{color:#7d8794;font-size:11px;text-transform:uppercase;letter-spacing:.05em}
 #meta .v{color:#e6e9ef}
 .note{color:#3ba9c7;font-style:italic;line-height:1.45}
 #key{margin-top:20px;padding-top:16px;border-top:1px solid #1e242c;font-size:11px}
 .kr{display:flex;align-items:center;gap:9px;margin-bottom:6px;color:#8b95a3}
 .sw{width:11px;height:11px;border-radius:3px;flex:none}
 #main{flex:1;position:relative}
 canvas{display:block}
 #hint{position:absolute;bottom:16px;left:50%;transform:translateX(-50%);
       font-size:11px;color:#5d6773;pointer-events:none}
</style></head><body>
<div id="side">
  <h1>TAYF — free-space display designs</h1>
  <div class="sub">Real scale, metres. Aperture spans the image it emits.</div>
  <div id="list"></div>
  <div id="meta"></div>
  <div id="key">
    <div class="kr"><span class="sw" style="background:#6b7684"></span>device body</div>
    <div class="kr"><span class="sw" style="background:#4fd1e8"></span>aperture plate</div>
    <div class="kr"><span class="sw" style="background:#25e0a8"></span>floating image</div>
    <div class="kr"><span class="sw" style="background:#39424f"></span>real human (scale)</div>
  </div>
</div>
<div id="main"><div id="hint">drag to orbit · scroll to zoom · right-drag to pan</div></div>
<script type="module">
import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';
import {OrbitControls} from 'https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js';

const DATA = __DATA__;

const main = document.getElementById('main');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b0d10);
scene.fog = new THREE.Fog(0x0b0d10, 8, 26);

const cam = new THREE.PerspectiveCamera(42, 1, 0.05, 100);
const rend = new THREE.WebGLRenderer({antialias:true});
rend.setPixelRatio(devicePixelRatio);
main.appendChild(rend.domElement);

const ctrl = new OrbitControls(cam, rend.domElement);
ctrl.enableDamping = true; ctrl.dampingFactor = 0.08;

scene.add(new THREE.HemisphereLight(0x9fb4cc, 0x0b0d10, 1.5));
const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(3,6,4); scene.add(key);
const rim = new THREE.DirectionalLight(0x4fd1e8, 0.7); rim.position.set(-4,2,-3); scene.add(rim);

const grid = new THREE.GridHelper(12, 24, 0x243040, 0x161c24);
scene.add(grid);

const MAT = {
  device:  new THREE.MeshStandardMaterial({color:0x6b7684, roughness:.55, metalness:.35}),
  aperture:new THREE.MeshStandardMaterial({color:0x4fd1e8, roughness:.1, metalness:.2,
            transparent:true, opacity:.42, side:THREE.DoubleSide}),
  image:   new THREE.MeshStandardMaterial({color:0x25e0a8, emissive:0x0e6b52,
            transparent:true, opacity:.62, roughness:.4}),
  scale:   new THREE.MeshStandardMaterial({color:0x39424f, roughness:.9}),
};
function matFor(name){
  if(name.includes('aperture')||name.includes('glass')) return MAT.aperture;
  if(name.includes('floating')) return MAT.image;
  if(name.includes('scale')||name.includes('viewer')||name.includes('operators')
     ||name.includes('pedestrian')) return MAT.scale;
  return MAT.device;
}

let group = null;
function show(i){
  if(group) scene.remove(group);
  group = new THREE.Group();
  const d = DATA[i];
  for(const g of d.groups){
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(g.pos, 3));
    geo.computeVertexNormals();
    group.add(new THREE.Mesh(geo, matFor(g.name)));
  }
  scene.add(group);

  const box = new THREE.Box3().setFromObject(group);
  const c = box.getCenter(new THREE.Vector3());
  const r = box.getSize(new THREE.Vector3()).length()/2;
  ctrl.target.copy(c);
  cam.position.set(c.x + r*1.35, c.y + r*0.55, c.z + r*1.5);
  cam.near = r/80; cam.far = r*30; cam.updateProjectionMatrix();

  document.querySelectorAll('.item').forEach((e,j)=>e.classList.toggle('on', i===j));
  document.getElementById('meta').innerHTML =
    `<div><div class="k">aperture</div><div class="v">${d.aperture}</div></div>
     <div><div class="k">depth</div><div class="v">${d.depth}</div></div>
     <div><div class="k">shows</div><div class="v">${d.shows}</div></div>
     <div class="note">${d.note}</div>`;
}

const list = document.getElementById('list');
DATA.forEach((d,i)=>{
  const el = document.createElement('div');
  el.className='item';
  el.innerHTML = `<div class="n">${d.title}</div><div class="d">${d.aperture}</div>`;
  el.onclick = ()=>show(i);
  list.appendChild(el);
});

function resize(){
  const w = main.clientWidth, h = main.clientHeight;
  cam.aspect = w/h; cam.updateProjectionMatrix(); rend.setSize(w,h);
}
addEventListener('resize', resize); resize();
show(0);
(function loop(){requestAnimationFrame(loop); ctrl.update(); rend.render(scene,cam);})();
</script></body></html>
"""


def write_viewer(path, built):
    """built = list of (mesh, name, meta). Embeds geometry so file:// works."""
    import json
    payload = []
    for mesh, name, meta in built:
        bounds = mesh.groups + [("", len(mesh.f))]
        groups = []
        for gi in range(len(mesh.groups)):
            gname, start = bounds[gi]
            end = bounds[gi + 1][1]
            pos = []
            for a, b, c in mesh.f[start:end]:
                for idx in (a, b, c):
                    pos.extend(round(t, 4) for t in mesh.v[idx])
            if pos:
                groups.append({"name": gname, "pos": pos})
        title = name.split("_", 1)[1].replace("_", " ")
        payload.append({"title": title, "groups": groups, **meta})
    with open(path, "w") as fh:
        fh.write(VIEWER_HTML.replace("__DATA__", json.dumps(payload)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    obj_dir, stl_dir = os.path.join(here, "obj"), os.path.join(here, "stl")
    if not args.list:
        os.makedirs(obj_dir, exist_ok=True)
        os.makedirs(stl_dir, exist_ok=True)

    print(f"{'design':22s} {'aperture':>26} {'depth':>9} {'shows'}")
    print("-" * 100)
    built = []
    for fn in DESIGNS:
        mesh, name, meta = fn()
        built.append((mesh, name, meta))
        print(f"{name:22s} {meta['aperture']:>26} {meta['depth']:>9} "
              f"{meta['shows']}")
        print(f"{'':22s} {'':>26} {'':>9} -> {meta['note']}")
        if not args.list:
            mesh.write_obj(os.path.join(obj_dir, name + ".obj"), name)
            mesh.write_stl(os.path.join(stl_dir, name + ".stl"), name)

    if not args.list:
        viewer = os.path.join(here, "viewer.html")
        write_viewer(viewer, built)
        print(f"\nwrote {len(DESIGNS)} .obj -> {obj_dir}")
        print(f"wrote {len(DESIGNS)} .stl -> {stl_dir}")
        print(f"wrote viewer      -> {viewer}")
        print(f"\n  xdg-open {viewer}")


if __name__ == "__main__":
    main()
