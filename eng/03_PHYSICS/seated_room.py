"""
TAYF seated meeting room - what changes when the remote people are on chairs,
and what a rectangular plan costs against a circular one.

Exists because docs/13_THE_ROOM.md models exactly one configuration: a single
standing person at the centre of a circular pod, viewed by standing people on a
1.3 m ring. A meeting is not that. A meeting is several people seated around a
table, some of them remote, in a rectangular room that fits a floor plan. This
module derives what that costs and what it buys.

Three results, none of which are in docs/13.

RESULT 1 - the aperture-below-the-floor bound. The governing law says an image
point is visible only from directions its aperture occupies. Run backwards that
means: for an eye at E to see image point P, there must be aperture on the ray
E->P EXTENDED PAST P until it meets the band. If the eye is high and the image
point is low, that ray plunges, and past a certain geometry it reaches the wall
below floor level - where no aperture can exist. A standing viewer close to a
low image point therefore loses the lower body, permanently, for a reason that
has nothing to do with engine count or brightness. Seating everyone is not a
concession to furniture; it is what closes this envelope.

RESULT 2 - engine count follows the PERIMETER, not the radius. N = 2*pi*z/D is
the circular special case of N = perimeter/D, because any closed band tiles the
full circle of azimuth at every interior point. A rectangle pays the
isoperimetric penalty: 4/pi = 1.27x for a square, more for a long room. It also
pays a second, subtler tax - the corner engines sit further away AND at
obliquity, so they deliver a much narrower wedge for the same hardware.

RESULT 3 - engine count does NOT scale with the number of remote seats. The
same closed band tiles 360 degrees around every interior point, so K seated
avatars need the same N engines as one. What K costs is multiplexing depth in
the film and frame budget in the modulator, not more engines.

Discipline inherited from constants.py: VERIFIED / DERIVED / ASSUMED / UNKNOWN.

Ledger: extends docs/13 section 1 (perimeter form of the tiling law) and
section 1.2 (vertical coverage); feeds docs/17_THE_MEETING_ROOM.md.
"""
import math

# ---------------------------------------------------------------------------
# Anthropometry, seated and standing
# ---------------------------------------------------------------------------
# Taken from models/build_models.py:Mesh.human(seated=True), which uses absolute
# seated dimensions rather than fractions of standing height. Eye height is
# placed at the head-box centre plus a small offset, consistent with that model.
# [ASSUMED] population-median adult; the 5th-95th spread is roughly +/-0.07 m
# seated and +/-0.15 m standing, and is swept in band_envelope().
H_EYE_SEATED = 1.20       # m, eye above floor, seated in a 0.45 m chair
H_EYE_STANDING = 1.60     # m, eye above floor, standing
H_SEAT_PAN = 0.45         # m
H_HEAD_TOP_SEATED = 1.29  # m, top of head seated
H_TABLE = 0.74            # m, standard table height  [VERIFIED] furniture standard

# Depth of a seated torso front-to-back, for the diopter budget. Shallower than
# the standing T_BODY = 0.60 m in accommodation.py because the arms are forward
# on the table and the legs are under it.
T_SEATED = 0.45           # m  [ASSUMED]

# ---------------------------------------------------------------------------
# Geometry defaults
# ---------------------------------------------------------------------------
D_APERTURE = 0.50         # m, per-engine aperture width  [ASSUMED] doc 13 s1.1
PER_SEAT_CHORD = 0.65     # m, table frontage per person  [ASSUMED] furniture std
CHAIR_SETBACK = 0.35      # m, seat centre behind the table edge  [ASSUMED]


# ---------------------------------------------------------------------------
# 1. The aperture envelope
# ---------------------------------------------------------------------------

def aperture_height(h_eye, h_img, d_eye_img, d_img_wall):
    """Height on the band at which aperture must exist for `h_eye` to see
    `h_img`.

    [DERIVED] The ray reaching the eye from image point P arrived from the band
    along the line through P, so the required band point A satisfies
    A = P + lambda (P - E). In elevation that is

        h_A = h_P + (h_P - h_E) * d_PA / d_EP

    A negative result means the aperture would have to be below floor level,
    where it cannot be built. That is a hard visibility bound, not a budget
    item.
    """
    if d_eye_img <= 0:
        raise ValueError("eye and image point coincide in plan")
    return h_img + (h_img - h_eye) * d_img_wall / d_eye_img


def wall_distance(px, py, ux, uy, half_w, half_l):
    """Distance from interior point (px,py) along unit direction (ux,uy) to the
    wall of a rectangle [-half_w, half_w] x [-half_l, half_l].

    [DERIVED] Standard slab test, smallest positive root.
    """
    ts = []
    if abs(ux) > 1e-12:
        ts.append(((half_w if ux > 0 else -half_w) - px) / ux)
    if abs(uy) > 1e-12:
        ts.append(((half_l if uy > 0 else -half_l) - py) / uy)
    ts = [t for t in ts if t > 1e-9]
    if not ts:
        raise ValueError("degenerate direction")
    return min(ts)


def band_envelope(seats, half_w, half_l, h_eyes, img_heights,
                  occluded_below=None):
    """Lowest and highest band heights the room actually needs.

    Sweeps every (viewing seat, image seat) ordered pair and every image height,
    and returns the extremes of aperture_height() together with the worst
    offender. `occluded_below` drops image points the tabletop hides, which is
    the one place real matter does the display a favour: an additive image
    cannot occlude, but a physical table in front of it can.

    Returns dict with lo, hi, and the (viewer, target, h_img, h_eye) that set
    each bound.
    """
    lo, hi = math.inf, -math.inf
    lo_case = hi_case = None
    for i, (ex, ey) in enumerate(seats):
        for j, (px, py) in enumerate(seats):
            if i == j:
                continue
            dx, dy = px - ex, py - ey
            d_ep = math.hypot(dx, dy)
            ux, uy = dx / d_ep, dy / d_ep
            d_pa = wall_distance(px, py, ux, uy, half_w, half_l)
            for h_e in h_eyes:
                for h_i in img_heights:
                    if occluded_below is not None and h_i < occluded_below(d_ep, h_e):
                        continue
                    h_a = aperture_height(h_e, h_i, d_ep, d_pa)
                    if h_a < lo:
                        lo, lo_case = h_a, (i, j, h_i, h_e, d_ep, d_pa)
                    if h_a > hi:
                        hi, hi_case = h_a, (i, j, h_i, h_e, d_ep, d_pa)
    return dict(lo=lo, hi=hi, lo_case=lo_case, hi_case=hi_case)


def visible_floor(h_band_bottom, h_eye, d_eye_img, d_img_wall):
    """Lowest point of an image that a band starting at `h_band_bottom` can
    actually deliver to an eye at `h_eye`.

    [DERIVED] Inverting aperture_height() for h_P with r = d_PA / d_EP:

        h_P = (h_band + h_E * r) / (1 + r)

    This is the useful engineering form. aperture_height() asks "what band do I
    need"; this asks "given the band I can build, where does the person get cut
    off". The answer is the design constraint, because the band bottom is fixed
    by the floor at 0 m and by furniture in practice.
    """
    r = d_img_wall / d_eye_img
    return (h_band_bottom + h_eye * r) / (1.0 + r)


def table_occlusion_floor(table_radius, seat_radius, h_table=H_TABLE):
    """Return a function giving the lowest image height still visible over the
    tabletop, for a viewer at `d_ep` from the image with eye at `h_e`.

    [DERIVED] The binding ray grazes the FAR edge of the tabletop. With the eye
    at horizontal 0 and the far table edge at d_far = seat_radius + table_radius,
    the grazing slope is (h_table - h_e)/d_far, so at the image the ray sits at

        h_min = h_e + (h_table - h_e) * d_ep / d_far

    Anything below that is hidden by the table, which means the display never
    has to form it and no aperture is needed for it.
    """
    d_far = seat_radius + table_radius

    def floor_at(d_ep, h_e):
        return h_e + (h_table - h_e) * d_ep / d_far

    return floor_at


# ---------------------------------------------------------------------------
# 2. Engine count: the perimeter form of the tiling law
# ---------------------------------------------------------------------------

def engines_perimeter(perimeter, d_aperture=D_APERTURE):
    """N = perimeter / D.

    [DERIVED] The generalisation of docs/13's N = 2*pi*z/D. Any closed curve
    around an interior point subtends exactly 2*pi of azimuth at that point, so
    the requirement is that the band be continuous, and the engine count is set
    by how much band one engine can drive. For a circle of radius z the
    perimeter is 2*pi*z and the doc's form is recovered exactly.
    """
    return perimeter / d_aperture


def engines_rect(width, length, d_aperture=D_APERTURE):
    """[DERIVED] N for a rectangular band on the walls."""
    return engines_perimeter(2.0 * (width + length), d_aperture)


def engines_circle(z, d_aperture=D_APERTURE):
    """[DERIVED] N for a circular band of radius z. Identical to
    accommodation.engines_needed()."""
    return engines_perimeter(2.0 * math.pi * z, d_aperture)


def isoperimetric_penalty(width, length):
    """How many times more band a rectangle needs than the circle inscribed in
    its short dimension.

    [DERIVED] 2(W+L) / (pi * W / 2 * 2) = 2(W+L)/(pi*W... ) -- written out:
    circle of radius a = W/2 has perimeter pi*W; rectangle has 2(W+L); ratio is
    2(W+L)/(pi*W). Equals 4/pi = 1.273 when L = W.
    """
    return 2.0 * (width + length) / (math.pi * width)


def engine_wedge(z, obliquity_cos=1.0, d_aperture=D_APERTURE):
    """Azimuth, in radians, that one engine's aperture serves at distance z.

    [DERIVED] The patch's projected width as seen from the image point is
    D*cos(phi), subtending D*cos(phi)/z. In a circle every engine gets the same
    wedge; in a rectangle the corner engines are further AND oblique, so they
    deliver far less azimuth for identical hardware.
    """
    return d_aperture * obliquity_cos / z


def rect_wedges(width, length, d_aperture=D_APERTURE):
    """Wedge served by the best and worst placed engine in a rectangular room,
    with the image at the centre.

    [DERIVED] Best is the mid-point of the short wall: normal incidence at
    z = W/2. Worst is a corner: z = sqrt((W/2)^2 + (L/2)^2) with obliquity
    cos(phi) = (W/2)/z for the long wall meeting that corner.
    """
    a, b = width / 2.0, length / 2.0
    z_corner = math.hypot(a, b)
    best = engine_wedge(a, 1.0, d_aperture)
    worst = engine_wedge(z_corner, a / z_corner, d_aperture)
    return best, worst, z_corner


# ---------------------------------------------------------------------------
# 3. Seating geometry
# ---------------------------------------------------------------------------

def round_table(n_seats, per_seat=PER_SEAT_CHORD, setback=CHAIR_SETBACK):
    """Seat radius, table radius, and the adjacent / opposite viewing distances
    for `n_seats` evenly spaced around a round table.

    [DERIVED] Adjacent chord = 2 R sin(pi/n) must be at least `per_seat`, so
    R = per_seat / (2 sin(pi/n)). Opposite distance is 2R for even n, and
    2R cos(pi/(2n)) for odd n.
    """
    r_seat = per_seat / (2.0 * math.sin(math.pi / n_seats))
    r_table = max(0.25, r_seat - setback)
    adjacent = 2.0 * r_seat * math.sin(math.pi / n_seats)
    if n_seats % 2 == 0:
        opposite = 2.0 * r_seat
    else:
        opposite = 2.0 * r_seat * math.cos(math.pi / (2.0 * n_seats))
    return dict(n=n_seats, r_seat=r_seat, r_table=r_table,
                adjacent=adjacent, opposite=opposite)


def seat_positions(n_seats, r_seat, phase=0.0):
    """[DERIVED] Plan coordinates of n evenly spaced seats."""
    return [(r_seat * math.sin(2 * math.pi * i / n_seats + phase),
             r_seat * math.cos(2 * math.pi * i / n_seats + phase))
            for i in range(n_seats)]


def facing_rows(n_per_side, separation, pitch):
    """Two rows facing each other across a long table: locals on one side,
    remote avatars on the other.

    [DERIVED] Returns (local_seats, remote_seats) in plan. The point of this
    layout is the LEVER RATIO r = d_PA / d_EP in aperture_height(). A round
    table forces adjacent pairs, where the viewer is 0.65 m from the image and
    the wall is 2.4 m behind it, so r ~ 3.7 and every centimetre of eye-height
    mismatch becomes four centimetres of band. Two rows facing put the viewer
    and the wall at comparable distances, r ~ 1, and the band collapses to
    little more than the spread of eye heights.
    """
    x = separation / 2.0
    ys = [(i - (n_per_side - 1) / 2.0) * pitch for i in range(n_per_side)]
    return ([(-x, y) for y in ys], [(x, y) for y in ys])


def cross_envelope(viewers, targets, half_w, half_l, h_eyes, img_heights):
    """Band envelope for viewers on one side looking at images on the other.

    [DERIVED] Same relation as band_envelope(), but only across-table pairs are
    evaluated, because same-side pairs are two real people looking at each
    other and involve no display at all.
    """
    lo, hi, lo_case, hi_case = math.inf, -math.inf, None, None
    for (ex, ey) in viewers:
        for (px, py) in targets:
            dx, dy = px - ex, py - ey
            d_ep = math.hypot(dx, dy)
            ux, uy = dx / d_ep, dy / d_ep
            d_pa = wall_distance(px, py, ux, uy, half_w, half_l)
            for h_e in h_eyes:
                for h_i in img_heights:
                    h_a = aperture_height(h_e, h_i, d_ep, d_pa)
                    if h_a < lo:
                        lo, lo_case = h_a, (d_ep, d_pa, h_i, h_e)
                    if h_a > hi:
                        hi, hi_case = h_a, (d_ep, d_pa, h_i, h_e)
    return dict(lo=lo, hi=hi, lo_case=lo_case, hi_case=hi_case)


# ---------------------------------------------------------------------------
# 4. Steering: what "mechanical" has to achieve
# ---------------------------------------------------------------------------

def pointing_requirement(pupil_d=0.004, throw=2.5, margin=4.0):
    """Angular pointing accuracy the steering element must hold, in radians.

    [DERIVED] The beam must land inside a pupil of diameter `pupil_d` at range
    `throw`, with `margin` times headroom against the pupil's angular size. A
    steering MIRROR doubles angle, so its mechanical requirement is half this.
    """
    optical = pupil_d / (margin * throw)
    return optical, optical / 2.0


def settle_requirement(n_pupils, frame_hz=60.0, duty=0.80):
    """Longest slew-and-settle time the steering element may take, in seconds.

    [DERIVED] An engine serving `n_pupils` must visit each every frame. If a
    fraction `duty` of the frame has to be spent actually emitting light, the
    remainder is all the mechanics get:

        n * t_settle <= (1 - duty) * T_frame

    This is the number that decides whether a mechanical steerer can be a
    separate element or has to be the modulator itself.
    """
    return (1.0 - duty) / (frame_hz * n_pupils)


def hinge_cycles(binary_hz, hours_per_day, days_per_year, years):
    """[DERIVED] Micromirror hinge actuations accumulated over a service life.

    A DMD is a mechanical device: roughly a million hinges flexing at the binary
    pattern rate. Run continuously it is the fastest-wearing part in the room
    and the only one with no field-serviceable subcomponent.
    """
    return binary_hz * hours_per_day * 3600.0 * days_per_year * years


# ---------------------------------------------------------------------------
# 5. The room as a building: heat and sound
# ---------------------------------------------------------------------------

def sensible_heat(n_people, n_engines, w_per_engine, w_render,
                  w_per_person=100.0):
    """[DERIVED] Total sensible heat dumped into the room, in watts."""
    return n_people * w_per_person + n_engines * w_per_engine + w_render


def air_temperature_rate(watts, volume, rho=1.204, cp=1005.0):
    """[DERIVED] K/s rise of unventilated room air under a given heat load."""
    return watts / (rho * volume * cp)


def sabine_rt60(volume, surfaces):
    """[DERIVED] Sabine reverberation time. `surfaces` is [(area, alpha), ...].

    T60 = 0.161 V / sum(S_i alpha_i). Included because the walls of this room
    are optical film - hard, specular, and acoustically live - which removes the
    surface a meeting room normally treats and pushes the entire absorption
    budget onto the ceiling, where the engines also want to live.
    """
    a = sum(s * al for s, al in surfaces)
    return 0.161 * volume / a if a > 0 else math.inf


# ---------------------------------------------------------------------------
def report():
    print("TAYF seated meeting room\n" + "=" * 62)

    print("\n1. ROUND TABLES AND WHERE THE PERCEPTUAL WINDOW FALLS")
    print("   accommodation.robust_window() gives R = 1.30-1.35 m as the only")
    print("   viewing distance that survives every depth-of-field figure.")
    print(f"{'seats':>6} {'seat R':>8} {'table R':>9} {'adjacent':>10} "
          f"{'opposite':>10}  robust?")
    for n in (4, 5, 6, 8, 10):
        t = round_table(n)
        ok = "yes" if 1.30 <= t["opposite"] <= 1.35 else "no"
        print(f"{n:>6} {t['r_seat']:>8.2f} {t['r_table']:>9.2f} "
              f"{t['adjacent']:>10.2f} {t['opposite']:>10.2f}  {ok}")

    print("\n1b. THE WINDOW MOVES WHEN THE SUBJECT IS A SEATED BUST")
    import sys as _s
    _s.path.insert(0, __file__.rsplit("/", 1)[0])
    from accommodation import robust_window, design_window
    print("   docs/13 and docs/15 computed the window for a STANDING BODY,")
    print("   t = 0.60 m, and got R = 1.30-1.35 m. A meeting shows a seated")
    print("   bust, t = 0.35 m, against a wall about 2 m behind it.")
    for label, t, off in (("standing body, pod", 0.60, 3.0),
                          ("seated bust, meeting room", 0.35, 2.0)):
        lo, hi = robust_window(t=t, wall_offset=off)
        nlo, nhi, _ = design_window(t=t, wall_offset=off)
        print(f"   {label:>26}: robust R = {lo:.2f}-{hi:.2f} m, "
              f"nominal R = {nlo:.2f}-{nhi:.2f} m")
    print("   a shallower subject spans fewer diopters, so it stays inside one")
    print("   focal plane much closer in, and the window opens toward the")
    print("   viewer. 1.00-1.20 m is ordinary table furniture; 1.30-1.35 m is not.")

    print("\n2. THE APERTURE-BELOW-THE-FLOOR BOUND")
    print("   Required band height for one eye to see one image point,")
    print("   h_A = h_P + (h_P - h_E) d_PA / d_EP. Negative is unbuildable.")
    print(f"{'case':>34} {'h_eye':>7} {'h_img':>7} {'d_EP':>6} {'d_PA':>6} "
          f"{'h_band':>8}")
    cases = [
        ("standing sees standing knee", H_EYE_STANDING, 0.50, 1.30, 1.50),
        ("standing sees standing chest", H_EYE_STANDING, 1.20, 1.30, 1.50),
        ("standing sees seated chest, close", H_EYE_STANDING, 1.00, 1.00, 1.80),
        ("standing sees seated head", H_EYE_STANDING, 1.29, 1.00, 1.80),
        ("seated sees seated lap", H_EYE_SEATED, 0.60, 1.40, 1.50),
        ("seated sees seated chest", H_EYE_SEATED, 1.00, 1.40, 1.50),
        ("seated sees seated head", H_EYE_SEATED, 1.29, 1.40, 1.50),
    ]
    for name, he, hi, dep, dpa in cases:
        ha = aperture_height(he, hi, dep, dpa)
        flag = "   <-- BELOW FLOOR" if ha < 0 else ""
        print(f"{name:>34} {he:>7.2f} {hi:>7.2f} {dep:>6.2f} {dpa:>6.2f} "
              f"{ha:>8.2f}{flag}")

    print("\n3. THE SEATED FULL-BODY AVATAR DOES NOT CLOSE")
    t6 = round_table(6)
    seats = seat_positions(6, t6["r_seat"])
    W, L = 3.6, 4.8
    occl = table_occlusion_floor(t6["r_table"], t6["r_seat"])
    img_h = [H_SEAT_PAN + 0.05 * k for k in range(18)]   # 0.45 .. 1.30 m
    eyes_seated = [1.13, 1.20, 1.27]
    env = band_envelope(seats, W / 2, L / 2, eyes_seated, img_h,
                        occluded_below=occl)
    print(f"   room {W} x {L} m, six seats at R = {t6['r_seat']:.2f} m,"
          f" table R = {t6['r_table']:.2f} m")
    print(f"   band needed to render a full seated body: {env['lo']:.2f} m to "
          f"{env['hi']:.2f} m  -- the lower bound is BELOW THE FLOOR")
    print("   so ask the buildable question instead: given a band that starts")
    print("   at the floor, where does a seated body get cut off?")
    d_opp = t6["opposite"]
    d_pa = wall_distance(0.0, t6["r_seat"], 0.0, 1.0, W / 2, L / 2)
    for h_b in (0.00, 0.30, 0.55):
        cut = visible_floor(h_b, H_EYE_SEATED, d_opp, d_pa)
        hides = occl(d_opp, H_EYE_SEATED)
        gap = cut - hides
        print(f"   band bottom {h_b:.2f} m -> body visible above "
              f"{cut:.2f} m; table hides below {hides:.2f} m; "
              f"unrenderable gap {gap:.2f} m")
    print("   a 0.3-0.4 m band of torso is neither hidden by the table nor")
    print("   reachable by any band above the floor. The seated FULL BODY is")
    print("   not a buildable framing at a table this size.")

    print("\n3b. THE BUST FRAMING, AND WHY THE LAYOUT DECIDES THE BAND")
    bust_h = [1.00 + 0.05 * k for k in range(8)]        # 1.00 .. 1.35 m
    print(f"   image = head, neck and shoulders at real head height, "
          f"{bust_h[0]:.2f} - {bust_h[-1]:.2f} m")
    envb = band_envelope(seats, W / 2, L / 2, eyes_seated, bust_h)
    print(f"   round table, six seats: band {envb['lo']:.2f} to "
          f"{envb['hi']:.2f} m  ({envb['hi'] - envb['lo']:.2f} m tall)")
    _, _, _, _, d_ep, d_pa = envb["lo_case"]
    print(f"      worst pair d_EP = {d_ep:.2f} m, d_PA = {d_pa:.2f} m, "
          f"lever r = {d_pa/d_ep:.1f}  -- the ADJACENT seat sets it")

    loc, rem = facing_rows(3, separation=1.20, pitch=0.80)
    envf = cross_envelope(loc, rem, W / 2, L / 2, eyes_seated, bust_h)
    d_ep, d_pa, _, _ = envf["lo_case"]
    print(f"   two rows facing at 1.20 m: band {envf['lo']:.2f} to "
          f"{envf['hi']:.2f} m  ({envf['hi'] - envf['lo']:.2f} m tall)")
    print(f"      worst pair d_EP = {d_ep:.2f} m, d_PA = {d_pa:.2f} m, "
          f"lever r = {d_pa/d_ep:.1f}")
    print(f"   docs/13 standing pod band: 0.55 to 2.30 m  (1.75 m tall)")
    print(f"   facing rows save {100*(1 - (envf['hi']-envf['lo'])/1.75):.0f}% "
          f"of band AREA at equal perimeter -- and the band is the HOE, which")
    print(f"   docs/16 names as both the only moat and the single-source risk.")

    print("\n3c. THE NEIGHBOUR IS TOO CLOSE FOR ONE FOCAL PLANE")
    print("   accommodation.planes_needed() at the seated bust depth "
          f"t = {T_SEATED - 0.10:.2f} m")
    import sys as _sys
    _sys.path.insert(0, __file__.rsplit("/", 1)[0])
    from accommodation import planes_needed, diopter_span
    for label, d in (("adjacent seat", t6["adjacent"]),
                     ("one seat away", 2 * t6["r_seat"] * math.sin(2 * math.pi / 6)),
                     ("opposite seat", t6["opposite"])):
        t = T_SEATED - 0.10
        print(f"   {label:>15} at {d:.2f} m: span "
              f"{diopter_span(d, t):.3f} D -> "
              f"{planes_needed(d, t)} focal plane(s)")
    print("   the neighbour needs two, and the honest reading is that it does")
    print("   not matter: depth_cues.cue_sensitivity_ratio() says stereopsis is")
    print("   268x more sensitive than accommodation, so a wrong focus gradient")
    print("   on the nearest avatar is the cheapest error in the room.")

    print("\n4. ENGINE COUNT: PERIMETER, NOT RADIUS")
    print(f"{'plan':>28} {'perimeter':>11} {'engines':>9} {'vs circle':>11}")
    circ = engines_circle(1.5)
    print(f"{'circular pod, z = 1.5 m':>28} {2*math.pi*1.5:>11.1f} "
          f"{circ:>9.1f} {1.0:>11.2f}")
    for W, L in ((3.6, 3.6), (3.6, 4.4), (3.6, 4.8), (3.6, 6.0)):
        n = engines_rect(W, L)
        print(f"{f'rectangle {W} x {L} m':>28} {2*(W+L):>11.1f} {n:>9.1f} "
              f"{isoperimetric_penalty(W, L):>11.2f}")
    print(f"   marginal cost of length: {2.0 / D_APERTURE:.0f} engines "
          f"per extra metre, in either dimension")

    print("\n5. THE CORNER TAX")
    for W, L in ((3.6, 3.6), (3.6, 4.8)):
        best, worst, zc = rect_wedges(W, L)
        print(f"   {W} x {L} m: best engine {math.degrees(best):.1f} deg, "
              f"corner engine {math.degrees(worst):.1f} deg "
              f"(z_corner = {zc:.2f} m), ratio {best/worst:.2f}x")

    print("\n6. STEERING: WHAT MECHANICAL HAS TO ACHIEVE")
    opt, mech = pointing_requirement()
    print(f"   pointing accuracy: {opt*1e3:.2f} mrad optical, "
          f"{mech*1e3:.2f} mrad mechanical ({math.degrees(mech)*3600:.0f} arcsec)")
    for npx in (4, 8, 12, 16):
        ts = settle_requirement(npx)
        print(f"   {npx:>2} pupils per engine at 60 Hz, 80% duty -> "
              f"settle in {ts*1e6:.0f} us")
    cyc = hinge_cycles(32_225, 8, 250, 1)
    print(f"   DMD hinge actuations: {cyc:.2e} per year at 32,225 Hz, "
          f"8 h/day, 250 d/yr")
    print(f"   a 1e12-cycle rating would then be reached in "
          f"{1e12/cyc:.1f} years  [rating UNVERIFIED]")

    print("\n7. THE ROOM AS A BUILDING")
    W, L, H = 3.6, 4.8, 2.7
    V = W * L * H
    n_eng = engines_rect(W, L)
    q = sensible_heat(8, n_eng, 40.0, 500.0)
    print(f"   volume {V:.1f} m3, {n_eng:.0f} engines at 40 W, 8 people, "
          f"render node 500 W")
    print(f"   sensible load {q:.0f} W -> unventilated air rise "
          f"{air_temperature_rate(q, V)*60:.1f} K/min")
    band_h = 1.30
    band_area = 2 * (W + L) * band_h
    wall_rest = 2 * (W + L) * H - band_area
    floor = ceil = W * L
    for label, a_ceil in (("absorptive ceiling", 0.70), ("hard ceiling", 0.05)):
        rt = sabine_rt60(V, [(floor, 0.25), (ceil, a_ceil),
                             (band_area, 0.05), (wall_rest, 0.10)])
        print(f"   RT60, {label:>18}: {rt:.2f} s   "
              f"(speech target 0.4-0.6 s)")
    print("   the band is hard specular film, so the walls cannot carry the")
    print("   absorption, and the ceiling has to - where the engines also go.")


if __name__ == "__main__":
    report()
