# 17 — THE MEETING ROOM: seated people, a rectangular plan, and mechanical steering

**Status:** active design brief. Written 2026-08-22.
**Derivations:** `eng/03_PHYSICS/seated_room.py`. Every number below is printed by
`python3 seated_room.py`; nothing here is typed twice.
**Relationship to `docs/13_THE_ROOM.md`:** doc 13 models exactly one configuration — a
single standing person at the centre of a circular pod, watched by standing people on a
1.3 m ring. A meeting is not that. This document derives what changes when the people sit
down, when the plan is rectangular, and when the steering element has to be a moving part.

Three results here contradict or extend doc 13, and one of them kills a framing the project
had been assuming without stating.

---

## 1. The relation that governs everything below

Doc 13 §1 gives the azimuthal law. What it does not give is the **elevation** law, and in a
seated meeting the elevation law is what binds.

An image point $P$ formed by converging light is visible from an eye at $E$ only if the ray
$E \to P$, **extended past $P$**, meets the aperture. The light that reaches the eye came
from the band on the far side of the image and carried straight on through the focus. So for
every viewer–image pair there is one and only one band location that can serve it, and its
height follows from similar triangles:

$$h_A \;=\; h_P + \left(h_P - h_E\right)\,\frac{d_{PA}}{d_{EP}}$$

where $h_E$ and $h_P$ are the eye and image heights above the floor, $d_{EP}$ is the
horizontal distance from eye to image, and $d_{PA}$ the horizontal distance from image on to
the wall. Write the **lever ratio**

$$r \;\equiv\; \frac{d_{PA}}{d_{EP}}$$

and the relation becomes a statement about error amplification:

$$h_A - h_P \;=\; r\,\left(h_P - h_E\right)$$

**The band's vertical excursion away from the image height is the eye-height mismatch
multiplied by $r$.** This is the single most useful thing in this document, and it is
counter-intuitive in a specific way: the band height requirement is set by the **nearest**
viewer, not the farthest. A viewer close to an image that has a distant wall behind it gives
a large $r$, and a centimetre of eye-height difference becomes several centimetres of band.

Two consequences fall straight out, and neither is in doc 13.

**A negative $h_A$ is unbuildable, not expensive.** There is no aperture below the floor, so
any viewer–image pair whose required band height comes out negative simply cannot be served.
This is a visibility bound of the same character as the clipping theorem itself, and no
amount of engine count, brightness or modulator bandwidth touches it.

**Layout is an optical parameter.** Where the chairs go changes $r$, and $r$ multiplies the
band. Furniture arrangement is not an interior-design decision downstream of the optics; it
is one of the optics variables.

---

## 2. The standing configuration is worse than doc 13 implies

Evaluating the relation for the doc 13 geometry, with a standing viewer whose eye is at
1.60 m, 1.30 m from a standing image, and the band 1.50 m beyond:

| what is being looked at | $h_P$ | required $h_A$ |
|---|---|---|
| the image's chest | 1.20 m | 0.74 m |
| the image's knee | 0.50 m | **−0.77 m** |

The knee needs aperture 77 cm below the floor. So a standing, full-body, free-space person
watched from conversational distance **loses everything below roughly mid-thigh**, and loses
it to geometry rather than to budget. Doc 13's band, which runs from 0.55 m to 2.30 m, was
sized for $\pm 20^\circ$ of vertical parallax about the band centre; it was never checked
against this relation. The renders in `models/png/01_the_room_*` show a whole standing
figure, and the lower third of that figure is not deliverable to the viewers drawn beside it.

This is the same class of error as the `z > R` mistake recorded in doc 13 §1.1 — a table that
did not catch what the geometry does — and it is recorded here rather than quietly fixed.

---

## 3. Seating everyone fixes the wrong half of the problem

The obvious response is to sit everybody down: seated eyes drop to about 1.20 m, the rays
flatten, and the plunge should stop. It half works.

With six people around a round table at seat radius 0.65 m and the room 3.6 m by 4.8 m, the
band required to render a **full seated body** runs from **−0.67 m to 1.84 m**. Still below
the floor. Asking the buildable question instead — given a band starting at floor level,
where does the far person get cut off — gives this, where "table hides below" is the height
under which the real tabletop occludes the avatar anyway and the display is off the hook:

| band bottom | body visible above | table hides below | unrenderable gap |
|---|---|---|---|
| 0.00 m | 0.69 m | 0.57 m | 0.12 m |
| 0.30 m | 0.82 m | 0.57 m | 0.25 m |
| 0.55 m | 0.92 m | 0.57 m | 0.35 m |

There is a band of torso, between a tenth and a third of a metre tall, that the tabletop does
not hide and no buildable aperture can reach. It appears as a horizontal cut across the
avatar's chest. Widening the table until its occlusion floor rises to meet the reachable
region requires a table radius of about 1.9 m — a table 3.8 m across for six people — which
is not furniture.

**The seated full-body avatar is not a buildable framing at a real table.** Recorded as a
finding, not a bug.

---

## 4. The bust framing, and why the layout decides the band

Render only what a video call already shows: head, neck and shoulders, floating at the height
a real head would be, roughly 1.00 m to 1.35 m above the floor. All image points now sit
close to eye height, the term $\left(h_P - h_E\right)$ collapses, and the relation stops
amplifying. Doc 11 §1 already argues the perceptual case for this framing — head alone reads
as a severed head, head plus neck reads as a person leaning in — so the optics and the
perception want the same thing.

The layout then decides the rest:

| layout | worst $d_{EP}$ | worst $d_{PA}$ | lever $r$ | band envelope | band height |
|---|---|---|---|---|---|
| round table, six seats | 0.65 m | 2.08 m | 3.2 | 0.14 – 2.05 m | 1.92 m |
| two rows facing at 1.20 m | 1.20 m | 1.20 m | 1.0 | **0.73 – 1.57 m** | **0.84 m** |
| doc 13 standing pod | — | — | — | 0.55 – 2.30 m | 1.75 m |

A round table forces adjacent pairs, where the viewer sits 0.65 m from the avatar while the
wall is 2.1 m behind it. That is $r = 3.2$, and it triples the band. Two rows facing across a
narrow table put viewer and wall at comparable distances, $r \approx 1$, and the band shrinks
to little more than the spread of adult eye heights.

**Facing rows cut band area by 52% against the standing pod at equal perimeter.** The band is
the holographic optical element, which `docs/16` names simultaneously as the only defensible
moat and the single-source supply risk, whose vendor tops out at 1400 mm web width and an A2
master. Halving its area is the largest cost and risk reduction available anywhere in this
design, and it comes from moving chairs.

### 4.1 The window moves too, in the right direction

Doc 13 and doc 15 computed the viewer-distance window for a **standing body**, $t = 0.60$ m
of front-to-back depth, and got the robust band $R = 1.30$ to $1.35$ m — the interval that
survives every depth-of-field figure between 0.20 D and 0.50 D. A seated bust is shallower,
$t \approx 0.35$ m, and sits about 2 m in front of the wall behind it. Re-running
`accommodation.robust_window()` on those parameters:

| subject | robust $R$ | nominal $R$ at $\mathrm{DoF}_{1/2} = 0.30$ D |
|---|---|---|
| standing body, pod | 1.30 – 1.35 m | 1.05 – 2.00 m |
| seated bust, meeting room | **1.00 – 1.20 m** | 0.80 – 1.75 m |

A shallower subject spans fewer diopters, stays inside one focal plane much closer in, and
the window opens toward the viewer. This matters practically: 1.30 to 1.35 m is not a
distance ordinary conference furniture produces, whereas 1.00 to 1.20 m is exactly a narrow
table with people facing across it. A table 0.50 m wide with 0.35 m chair setback each side
puts facing participants at 1.20 m, the top of the robust window. A conventional 0.90 m table
puts them at 1.60 m — inside the nominal window, outside the robust one, which means the
focus discriminator there is riding on the depth-of-field figure being at the optimistic end
of Campbell's range rather than the conservative end this project assumes.

### 4.2 The neighbour is too close, and it does not matter

At the seated bust depth, `accommodation.planes_needed()` returns:

| position | distance | diopter span | focal planes |
|---|---|---|---|
| adjacent seat | 0.65 m | 0.893 D | 2 |
| one seat away | 1.13 m | 0.283 D | 1 |
| opposite seat | 1.30 m | 0.211 D | 1 |

Whoever sits immediately beside an avatar is inside the single-plane limit and will see a
focus gradient across its face that is wrong by about one depth of field. The honest reading
is that this is the cheapest error available: `depth_cues.cue_sensitivity_ratio()` puts
stereopsis at $268\times$ the sensitivity of accommodation, independent of subject size and
viewing distance, so a wrong focus gradient on the nearest avatar costs almost nothing
perceptually while a wrong disparity would be fatal. The engines stay fixed-focus.

---

## 5. What the rectangle costs

Doc 13 states the tiling law as $N = 2\pi z / D$. That is the circular special case. The
general form is

$$N \;=\; \frac{\text{perimeter of the band}}{D}$$

because any closed curve surrounding an interior point subtends exactly $2\pi$ of azimuth at
that point, whatever its shape. The requirement is that the band be **continuous**, and the
engine count is set by how much band one engine can drive. Substituting a circle of radius
$z$ recovers doc 13's form exactly.

A rectangle therefore pays the isoperimetric penalty, since the circle minimises perimeter
for a given clearance:

| plan | perimeter | engines at $D = 0.5$ m | vs. circle |
|---|---|---|---|
| circular pod, $z = 1.5$ m | 9.4 m | 19 | 1.00 |
| square, 3.6 × 3.6 m | 14.4 m | 29 | 1.27 |
| rectangle, 3.6 × 4.4 m | 16.0 m | 32 | 1.41 |
| rectangle, 3.6 × 4.8 m | 16.8 m | 34 | 1.49 |
| rectangle, 3.6 × 6.0 m | 19.2 m | 38 | 1.70 |

The square's $4/\pi = 1.273$ is exact and is the best any rectangle can do. Differentiating,
$\mathrm{d}N/\mathrm{d}L = 2/D = 4$ engines per extra metre in either dimension, which at the
researched $\$2{,}595$ per engine is about **$\$10{,}400$ per linear metre of room.**

### 5.1 The corner tax

There is a second penalty that the perimeter count hides. One engine's aperture patch
subtends, at the image point,

$$\alpha \;=\; \frac{D\cos\varphi}{z}$$

where $\varphi$ is the angle between the wall normal and the ray. In a circle every engine is
at the same $z$ with $\varphi = 0$ and every engine delivers the same wedge. In a rectangle
the corner engines are both further away and oblique:

| plan | best engine | corner engine | ratio |
|---|---|---|---|
| 3.6 × 3.6 m | 15.9° at $z = 1.80$ m | 8.0° at $z = 2.55$ m | 2.00× |
| 3.6 × 4.8 m | 15.9° at $z = 1.80$ m | 5.7° at $z = 3.00$ m | 2.78× |

Identical hardware, up to $2.8\times$ less azimuth. If gaps in coverage are ever acceptable
they belong at the corners, which is also where nobody stands. Full 360° means buying them.

A second, non-obvious cost: in a circle the band has continuous rotational symmetry, so it is
**one HOE master repeated $N$ times**. A rectangle has only the order-4 mirror group, so it
needs roughly $N/4 \approx 9$ distinct master prescriptions. That multiplies the count of the
exact component `docs/16` flags as the single-source risk.

### 5.2 The number of remote seats is free

Because any closed band tiles $2\pi$ at *every* interior point, $K$ seated avatars need the
same $N$ engines as one. What $K$ costs is elsewhere: $K$ superimposed gratings per band
patch, spending the photopolymer's dynamic range, and a frame budget divided $K$ ways in the
modulator. Doc 13 §7's DMD headroom — 32,225 binary frames per second against roughly 540
plane-switches required — covers $K = 4$ comfortably on time. The film's dynamic range is
what actually binds, and it is unquoted.

---

## 6. Mechanical steering: what a moving part has to achieve

The engines must land light on tracked pupils rather than broadcast it everywhere; that
factor is the whole difference between 19 engines and TeleHuman 2's 275. Taking the constraint
that the steering element is **mechanical**, two requirements fall out and they pull opposite
ways.

**Pointing accuracy.** A pupil in a dim room is about 4 mm across. At a 2.5 m throw it
subtends $4\times10^{-3}/2.5 = 1.6$ mrad. Landing inside it with a factor-of-four margin
requires

$$\sigma_\theta \;\le\; \frac{d_\text{pupil}}{k\,L} \;=\; \frac{0.004}{4 \times 2.5} \;=\; 0.40\ \text{mrad optical}$$

and a steering mirror doubles the angle it turns through, so the mechanical requirement is
**0.20 mrad, about 41 arcsec.** This is not the hard part. Closed-loop galvanometer scanners
routinely hold an order of magnitude better.

**Settling time.** This is the hard part. An engine serving $N_p$ pupils must visit each one
every frame. If a fraction $\eta$ of the frame has to be spent actually emitting light, the
mechanics get the remainder:

$$N_p\,t_\text{settle} \;\le\; (1-\eta)\,T_\text{frame}
\qquad\Longrightarrow\qquad
t_\text{settle} \;\le\; \frac{1-\eta}{f\,N_p}$$

At 60 Hz and 80% optical duty:

| pupils per engine | maximum slew-and-settle |
|---|---|
| 4 | 833 µs |
| 8 | 417 µs |
| 12 | **278 µs** |
| 16 | 208 µs |

A room with six local people has twelve pupils. **The steering element must slew across its
whole assigned wedge — up to 16° optical — and settle inside about 280 microseconds.** A
closed-loop galvanometer with an aperture large enough to matter does not do that for
large-angle steps; it is a millisecond-class device for multi-degree moves. Adding a galvo as
a separate steering stage therefore spends roughly half the frame budget on mechanical
transit.

**The resolution is that the mechanism is already in the design.** A digital micromirror
device is a mechanical steering element: roughly a million hinged mirrors flipping through
$\pm 12°$, switching in microseconds. If the direction is encoded in the binary pattern
written to the DMD rather than in the orientation of a mirror downstream of it, the steering
happens at the pattern rate with no settling transient at system level, and random access to
any pupil costs one frame slot. The steering *is* the modulation. This is the strongest
argument for the DMD architecture and it is separate from the brightness and bandwidth
arguments doc 13 §7 already makes.

That choice buys the frame budget and hands back a wear problem. At 32,225 binary frames per
second, 8 hours a day, 250 days a year, each device accumulates

$$32{,}225 \times 8 \times 3600 \times 250 \;=\; 2.3 \times 10^{11}\ \text{hinge actuations per year.}$$

If the published hinge endurance is of order $10^{12}$ cycles — **`[UNVERIFIED]`**, recalled
from vendor reliability material and not read in this repository — that is reached in about
**4.3 years**, across 34 devices, as a scheduled replacement rather than a failure. Nobody has
costed that line. It belongs in `docs/16`'s opex stack and it is not there.

**What is not being used, and why it is worth naming.** Acousto-optic deflectors give
microsecond random access with no moving part at all, which would dissolve the settling
problem outright; they are ruled out here by angular range of a few degrees, diffraction
efficiency, and chromatic dispersion across a colour image, not by the mechanical
constraint. Liquid-crystal and optical-phased-array steering are slower than the galvo they
would replace. The mechanical constraint costs the design nothing it would otherwise have
had.

---

## 7. The room is a building, and the building fights back

Two constraints appear only once this is a real meeting room rather than a geometry, and
neither is in any prior document.

**Heat.** A 3.6 × 4.8 × 2.7 m room is 46.7 m³. Thirty-four engines at 40 W, eight people at
100 W metabolic, and a 500 W render node is **2,644 W of sensible load**. Unventilated, that
raises the air temperature at

$$\frac{\mathrm{d}T}{\mathrm{d}t} \;=\; \frac{Q}{\rho\,V\,c_p} \;=\; \frac{2644}{1.204 \times 46.7 \times 1005} \;\approx\; 2.8\ \text{K per minute.}$$

A typical small meeting room is provisioned for around 1 kW of cooling. This one needs closer
to 3 kW, in a room whose walls are covered in optical film and therefore cannot carry
diffusers or grilles. Supply and return have to come through the floor or through the same
ceiling zone the engines occupy.

**Sound.** The band is hard, specular film. It removes the surface a meeting room normally
treats, and pushes the whole absorption budget onto the ceiling — which is also where the
engines live. Sabine's relation $T_{60} = 0.161\,V/\sum S_i\alpha_i$ gives:

| ceiling | $T_{60}$ | verdict against a 0.4–0.6 s speech target |
|---|---|---|
| absorptive tile, $\alpha = 0.70$ | 0.38 s | acceptable, slightly dry |
| hard, $\alpha = 0.05$ | 0.87 s | unusable for speech |

The engine coffer and the acoustic absorber compete for the same ceiling area, and the
competition has to be resolved in favour of the absorber or the room fails as a meeting room
regardless of how good the image is.

This also supplies an argument for the rectangle that has nothing to do with optics. A
circular pod is a cylinder of hard concave surfaces, and concave surfaces focus. The
focus of a cylindrical room is its axis — precisely where the image and the person speaking
to it stand. Circular rooms are a known defect in architectural acoustics for exactly this
reason. **The rectangle is acoustically the safer plan, and it buys that at the isoperimetric
premium computed in §5.** The optics prefer the circle; the room prefers the rectangle; §5
prices the disagreement at 27% to 70% more engines.

---

## 8. The meeting-specific thing this actually wins

Worth stating plainly because the deck does not: in a meeting, the product's advantage is
**gaze**. On a flat screen every viewer sees the same rendered face, so everyone believes
they are being looked at and nobody can tell who is being addressed. A real image in free
space is looked at from each seat's own angle, so an avatar turning to address one person is
seen to turn by everyone, correctly, simultaneously. Round-table gaze awareness — knowing who
is looking at whom — is a documented failure mode of video conferencing, and it is the one
thing this architecture fixes that a bigger, sharper, cheaper screen cannot.

That is a claim about perception, it is untested, and it is exactly the kind of claim PQ-1
exists to settle. It is not currently among PQ-1's conditions. It should be.

---

## 9. What this document changes, and what it leaves open

**Changed.** The tiling law is stated in its perimeter form. The elevation relation and the
aperture-below-the-floor bound are new and they invalidate the full-body standing framing at
conversational distance. The bust framing and facing-row layout are new, and together they
halve band area. The seated-bust viewing window is 1.00–1.20 m robust, not 1.30–1.35 m.

**Open.** The photopolymer's dynamic range under $K$-fold angular multiplexing is unquoted
and it is the binding constraint on how many remote seats a room can hold. The DMD hinge
endurance figure is unverified and it sets a replacement interval nobody has costed. Whether
a floating bust at table height reads as a colleague or as a talking head in a jar is a
perceptual question with no data behind it, and doc 11 §1's own note on the difference
between a head and a head-with-neck is the only evidence either way.
