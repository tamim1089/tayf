#!/usr/bin/env python3
"""
make_diagrams.py — original technical diagrams for the universal document.

Hand-written SVG, no dependencies. These are drawn from the physics rather
than copied from any paper: the geometry is ours, the numbers are ours, and
the repository is public, so reproducing published figures would be a
copyright problem as well as a worse diagram.

    python3 make_diagrams.py     -> models/svg/*.svg
"""

import os

W, H = 860, 470
BG, INK, MUTE = "#ffffff", "#12161c", "#6b7684"
BEAM, IMG, RR = "#c9a227", "#12a37a", "#3b7dd8"

HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        'width="{w}" height="{h}" font-family="ui-sans-serif,system-ui,sans-serif">'
        '<rect width="{w}" height="{h}" fill="{bg}"/>'
        '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="{beam}"/></marker>'
        '<marker id="b" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="{ink}"/></marker></defs>')


def svg(body, w=W, h=H):
    return HEAD.format(w=w, h=h, bg=BG, beam=BEAM, ink=INK) + body + "</svg>"


def txt(x, y, s, size=13, fill=INK, anchor="start", weight="400", style=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" '
            f'font-style="{style or "normal"}">{s}</text>')


def line(x1, y1, x2, y2, c=INK, w=2, dash=None, arrow=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    a = f' marker-end="url(#{arrow})"' if arrow else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" '
            f'stroke-width="{w}"{d}{a}/>')


def rect(x, y, w, h, fill="none", stroke=INK, sw=2, rx=2, op=1.0):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
            f'fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}"/>')


# ----------------------------------------------------------------------
# 1. AIRR ray path — the mechanism
# ----------------------------------------------------------------------

def airr():
    b = [txt(30, 34, "AIRR — how a real image forms in open air", 17, INK, weight="600"),
         txt(30, 56, "Light leaves the source, reflects off the beamsplitter to the retroreflector, "
                     "returns along its own path, passes through the beamsplitter, and converges in mid-air.",
             12.5, MUTE)]

    bsx1, bsy1, bsx2, bsy2 = 300, 150, 470, 320   # 45° beamsplitter
    b.append(f'<line x1="{bsx1}" y1="{bsy1}" x2="{bsx2}" y2="{bsy2}" stroke="{MUTE}" '
             f'stroke-width="7" stroke-linecap="round" opacity="0.30"/>')
    b.append(line(bsx1, bsy1, bsx2, bsy2, MUTE, 2))
    b.append(txt(478, 322, "beamsplitter 45°", 12, MUTE))

    # source panel, bottom, emitting up
    b.append(rect(315, 392, 150, 16, "#e9edf2", INK, 2))
    b.append(txt(390, 428, "source panel (LCD/OLED)", 12, INK, "middle", "600"))

    # retroreflector, right, facing left
    b.append(rect(596, 172, 16, 150, "#e6efff", RR, 2))
    for i in range(7):
        y = 180 + i * 22
        b.append(f'<path d="M596 {y} l16 11 l-16 11" fill="none" stroke="{RR}" stroke-width="1.4"/>')
    b.append(txt(622, 190, "retroreflector", 12, RR, "start", "600"))
    b.append(txt(622, 208, "returns light along", 11, MUTE))
    b.append(txt(622, 223, "its incoming path", 11, MUTE))

    # rays: up from source -> BS -> right to RR -> back left -> through BS -> up-left to image
    for dx in (-40, 40):
        sx = 390 + dx
        hy = 150 + (sx - bsx1)            # y where the ray meets the 45° line
        b.append(line(sx, 392, sx, hy + 6, BEAM, 2.2, arrow="a"))          # up
        b.append(line(sx, hy, 604, hy, BEAM, 2.2, arrow="a"))              # right to RR
        b.append(line(600, hy + 7, sx, hy + 7, BEAM, 2.2, arrow="a"))      # back left
        b.append(line(sx, hy + 7, 196, 236, BEAM, 2.2, dash="5 4", arrow="a"))  # converge

    # the aerial image
    b.append(f'<ellipse cx="188" cy="236" rx="30" ry="44" fill="{IMG}" fill-opacity="0.16" '
             f'stroke="{IMG}" stroke-width="2.4"/>')
    b.append(txt(188, 178, "REAL IMAGE", 12.5, IMG, "middle", "700"))
    b.append(txt(188, 300, "floats in open air", 12, IMG, "middle", "600"))
    b.append(txt(188, 317, "nothing is at this point", 11, MUTE, "middle"))

    b.append(line(315, 372, 465, 372, MUTE, 1.4, arrow="b"))
    b.append(line(465, 372, 315, 372, MUTE, 1.4, arrow="b"))
    b.append(txt(390, 366, "d", 12, MUTE, "middle", "600", "italic"))
    b.append(txt(30, 352, "the image sits as far from the", 11, MUTE))
    b.append(txt(30, 366, "beamsplitter as the source does", 11, MUTE))
    b.append(txt(30, 456, "Unit magnification: image size = source size, exactly. "
                          "Viewing angle 170° measured (Yamamoto 2017, 10.11370/isj.56.341).",
                11.5, MUTE))
    return svg("".join(b))


# ----------------------------------------------------------------------
# 2. The two aperture modes
# ----------------------------------------------------------------------

def modes():
    b = [txt(30, 34, "The two aperture modes — name which one you mean", 17, INK, weight="600"),
         txt(30, 56, "Conflating these is the easiest technical error in this project.",
             12.5, MUTE)]

    def panel(ox, title, sub, mode):
        p = [txt(ox + 190, 96, title, 14.5, INK, "middle", "700"),
             txt(ox + 190, 116, sub, 12, MUTE, "middle")]
        eye_x, eye_y = ox + 40, 250
        p.append(f'<circle cx="{eye_x}" cy="{eye_y}" r="11" fill="none" stroke="{INK}" stroke-width="2"/>')
        p.append(f'<circle cx="{eye_x}" cy="{eye_y}" r="4" fill="{INK}"/>')
        p.append(txt(eye_x, eye_y + 32, "eye", 11.5, MUTE, "middle"))

        if mode == "front":
            ap_x, ap_h, im_x, im_h = ox + 300, 150, ox + 175, 62
        else:
            ap_x, ap_h, im_x, im_h = ox + 175, 62, ox + 322, 150

        p.append(rect(ap_x - 5, 250 - ap_h / 2, 10, ap_h, "#dfe6ee", INK, 2))
        p.append(txt(ap_x, 250 - ap_h / 2 - 12, "aperture D", 11.5, INK, "middle", "600"))

        p.append(f'<rect x="{im_x-16}" y="{250-im_h/2}" width="32" height="{im_h}" '
                 f'fill="{IMG}" fill-opacity="0.18" stroke="{IMG}" stroke-width="2.2" rx="4"/>')
        p.append(txt(im_x, 250 + im_h / 2 + 20, "image W", 11.5, IMG, "middle", "600"))

        far = max(ap_x, im_x) + 40
        for s in (-1, 1):
            p.append(line(eye_x + 11, eye_y, far, 250 + s * (ap_h / 2) *
                          (far - eye_x) / (ap_x - eye_x), BEAM, 1.8, dash="4 4"))
        return "".join(p)

    b.append(panel(30, "IN-FRONT  (Law 1)", "image nearer you than the device", "front"))
    b.append(txt(220, 388, "W &#60;= D", 20, INK, "middle", "700"))
    b.append(txt(220, 412, "a 20 cm device shows a 20 cm head", 12, MUTE, "middle"))
    b.append(txt(220, 434, "in your own space — rule 4 strict", 11.5, MUTE, "middle"))

    b.append(f'<line x1="440" y1="80" x2="440" y2="440" stroke="{MUTE}" stroke-width="1" '
             f'stroke-dasharray="4 5"/>')

    b.append(panel(460, "PORTAL  (Law 2)", "image beyond the device", "portal"))
    b.append(txt(650, 388, "W = D · (b / a)", 20, INK, "middle", "700"))
    b.append(txt(650, 412, "a 20 cm device shows a standing person at 2.55 m", 12, MUTE, "middle"))
    b.append(txt(650, 434, "unbounded — but you look through a frame", 11.5, MUTE, "middle"))
    return svg("".join(b))


# ----------------------------------------------------------------------
# 3. Presence is an angle
# ----------------------------------------------------------------------

def presence():
    """All four subjects at the SAME 1 m distance, nested, so the differing
    angular size is the only variable — which is the point of the law."""
    import math
    Wp, Hp = 900, 520
    b = [txt(30, 34, "Law 3 — presence is an angle, not a size", 17, INK, weight="600"),
         txt(30, 56, "All four subjects at the same 1 m distance. Only the angle differs, "
                     "and the device must match it.", 12.5, MUTE)]
    eye = (72, 292)
    px_per_m = 200                     # 1 m of distance
    sx = eye[0] + px_per_m             # subject plane

    b.append(f'<line x1="{sx}" y1="80" x2="{sx}" y2="500" stroke="{MUTE}" '
             f'stroke-width="1" stroke-dasharray="3 4"/>')
    b.append(txt(sx, 74, "all at 1 m", 11.5, MUTE, "middle"))

    rows = [(1.70, "standing body", 80.7), (0.80, "seated upper body", 43.6),
            (0.50, "head + shoulders", 28.1), (0.22, "face", 12.6)]
    for i, (h_m, name, ang) in enumerate(rows):
        h = h_m * px_per_m
        top, bot = eye[1] - h / 2, eye[1] + h / 2
        b.append(line(eye[0] + 12, eye[1], sx + 26, top, BEAM, 1.5, dash="4 4"))
        b.append(line(eye[0] + 12, eye[1], sx + 26, bot, BEAM, 1.5, dash="4 4"))
        b.append(f'<rect x="{sx-13}" y="{top}" width="26" height="{h}" fill="{IMG}" '
                 f'fill-opacity="0.10" stroke="{IMG}" stroke-width="2" rx="3"/>')
        lx = sx + 46 + i * 0
        b.append(txt(lx, top + 15, f"{ang:.1f}°", 13, INK, "start", "700"))
        b.append(txt(lx + 46, top + 15, name, 11.5, MUTE))
        b.append(txt(lx + 200, top + 15, f"{h_m:.2f} m", 11.5, MUTE))

    b.append(f'<circle cx="{eye[0]}" cy="{eye[1]}" r="13" fill="none" stroke="{INK}" stroke-width="2.2"/>')
    b.append(f'<circle cx="{eye[0]}" cy="{eye[1]}" r="5" fill="{INK}"/>')
    b.append(txt(eye[0], eye[1] + 34, "eye", 11.5, MUTE, "middle"))

    b.append(txt(30, 494, "A 10 cm device reaches 12.6° — a life-size face — at 45 cm, "
                          "where a phone already sits. FaceTime at 40 cm subtends 19.9°; "
                          "a real person at 1.2 m, 10.5°.", 11.5, MUTE))
    return svg("".join(b), Wp, Hp)


# ----------------------------------------------------------------------
# 4. Where the light goes
# ----------------------------------------------------------------------

def efficiency():
    b = [txt(30, 34, "Optical efficiency cascade — where 75% of the light goes",
             17, INK, weight="600"),
         txt(30, 56, "The beamsplitter is crossed twice, costing ~50% each time. "
                     "This sets the source-panel luminance.", 12.5, MUTE)]
    stages = [("source panel", 100, "assumed"),
              ("beamsplitter, pass 1", 50, "reflect toward retroreflector"),
              ("retroreflector return", 50, "eta_RR UNMEASURED - assumed 1.0"),
              ("beamsplitter, pass 2", 25, "transmit toward viewer"),
              ("aerial image", 25, "~250 cd/m2")]
    y = 110
    for i, (name, pct, note) in enumerate(stages):
        w = 5.1 * pct
        col = IMG if i == len(stages) - 1 else (BEAM if i else "#dfe6ee")
        b.append(rect(250, y, w, 40, col, INK, 1.8, 4, 0.5 if i else 1))
        b.append(txt(240, y + 25, name, 12.5, INK, "end", "600"))
        b.append(txt(258, y + 25, f"{pct}%", 13, INK, "start", "700"))
        b.append(txt(262 + w, y + 25, note, 11.5, MUTE))
        y += 62
    b.append(txt(30, 430, "Indoor viewing needs roughly 100–300 cd/m² at the image, so a "
                          "1000 cd/m² panel closes it — IF eta_RR ~ 1.", 12, INK))
    b.append(txt(30, 450, "eta_RR is stated nowhere in the literature and is the single "
                          "highest-value measurement this project can make.", 12, MUTE))
    return svg("".join(b))


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")
    os.makedirs(out, exist_ok=True)
    for name, fn in (("airr_ray_path", airr), ("aperture_modes", modes),
                     ("angular_presence", presence), ("efficiency_cascade", efficiency)):
        p = os.path.join(out, name + ".svg")
        open(p, "w").write(fn())
        print(f"  {name}.svg  ({os.path.getsize(p)} B)")
    print(f"\nwrote -> {out}")


if __name__ == "__main__":
    main()
