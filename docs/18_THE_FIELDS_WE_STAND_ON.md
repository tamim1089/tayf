# 18 — THE FIELDS WE STAND ON: every discipline this project draws from, and exactly what it takes from each

**Status:** living reference. Written 2026-08-22.
**Purpose:** TAYF is not an optics project with some human factors bolted on. It is a
problem that sits at the intersection of about thirty distinct scientific fields, several of
which the project has been using without naming, and a few of which it should be using and
is not. This document names all of them, states the specific relation or result taken from
each, points at where it enters, and marks what remains unverified.

**Audience:** another engineer or another model picking this up cold, who needs to know which
literature to read and which to ignore.

**Reading convention, inherited from `eng/03_PHYSICS/constants.py`.** Every claim carries a
tier. `[VERIFIED]` means measured in a primary source that has been read. `[DERIVED]` means
computed here from labelled inputs with the relation shown. `[ASSUMED]` means an engineering
baseline stated openly and swept where it matters. `[UNVERIFIED]` means recalled or inherited
and not checked in this repository — and the project has been burned by that category before,
so it is marked aggressively rather than sparingly.

**One structural note before the list.** The fields below are sorted by how load-bearing they
are, not by academic tidiness. Part II is the set without which there is no product at all.
Part III is what it takes to build one. Part IV is the human side, which decides whether
anyone wants it. Part V collects the genuinely obscure connections — the ones that were not
obvious and that each bought something concrete. Part VI records what we deliberately do not
use, because a project that claims every field claims none. Part VII notes where the standard
taxonomy has no box for something we need.

---

# Part I — The one-paragraph map

The product is a real image formed in open air and steered to tracked pupils. That single
sentence commits the project to **geometric and diffractive optics** for what the image can
be, to **radiometry and the conservation of étendue** for how much of it there can be, to
**visual optics and binocular vision** for whether any of it is perceptible, to
**mechanical and control engineering** for how the light gets aimed, to **psychophysics and
experimental statistics** for how we find out we are wrong, and to **architectural
acoustics, building services and regulation** for whether the result is a room anyone can
legally install and sit in. Everything else is downstream of those seven.

---

# Part II — Load-bearing fields

## II.1 Physics → Classical Physics → Optics → Geometric Optics

**What we take.** The clipping theorem and everything that follows from it. An image point
floating in free space radiates only into the solid angle its forming aperture occupies, so
an optic of width $D$ at distance $z$ from the image serves an angular wedge

$$\alpha \;\approx\; \frac{D\cos\varphi}{z}$$

with $\varphi$ the obliquity between the wall normal and the ray. Tiling the full circle
requires $\sum_i \alpha_i \ge 2\pi$, which for a continuous band of perimeter $C$ divided into
patches of width $D$ gives the governing count

$$N \;=\; \frac{C}{D}, \qquad\text{and for a circle of radius } z, \qquad N = \frac{2\pi z}{D}.$$

**We also take the elevation form**, derived in `docs/17` §1, which doc 13 never wrote down:
the band height serving an eye at $h_E$ looking at an image point at $h_P$ is

$$h_A \;=\; h_P + \left(h_P - h_E\right)\frac{d_{PA}}{d_{EP}},$$

and a negative $h_A$ is a hard visibility bound rather than a cost.

**Also from this field:** the composition of two plane reflections is a Euclidean isometry, so
a beamsplitter plus a retroreflective sheet has magnification exactly $M = 1$ — the result
that sizes the cube in `docs/11` and cannot be engineered around, because an isometry cannot
scale.

**Where it enters.** `eng/03_PHYSICS/accommodation.py:engines_needed()`,
`eng/03_PHYSICS/seated_room.py` in full, `docs/11`, `docs/13` §1, `docs/17` §1 and §5.
**Status.** `[DERIVED]` throughout, from `[VERIFIED]` first principles. This is the most
secure part of the whole project.

## II.2 Physics → Classical Physics → Optics → Physical Optics and Diffractive Optics

**What we take.** The grating equation sets the maximum angle any pixelated modulator can
deflect light through. For a modulator of pitch $p$ illuminated at wavelength $\lambda$, the
first diffraction order sits at

$$\sin\theta_{\max} \;=\; \frac{\lambda}{2p},$$

which is why a 4K phase modulator at 3.74 µm pitch delivers only about $\pm 4.2°$ and why the
passive relay band exists at all: the active element cannot cover the angle, so a large
passive optic does the angular work and a small active one does the modulation. This is the
single architectural decision that makes the engine count 19 rather than 275.

Holographic optical elements are volume gratings recorded by interference and read out by
Bragg-matched illumination; their angular and spectral selectivity is what permits **angular
multiplexing**, storing $K$ independent prescriptions in one film. That capability is what
lets $K$ remote participants share one band, and its limit — the photopolymer's dynamic
range, usually quoted as a total refractive-index modulation budget $\Delta n$ shared across
the multiplexed gratings — is the binding constraint on how many people a room can seat.
`[UNVERIFIED]` as a number for the specific film; identified as the open question in
`docs/17` §9.

**Where it enters.** `docs/02` §2–4, `docs/13` §2, `docs/17` §5.2.

## II.3 Physics → Thermodynamics → Statistical Thermodynamics, and Mathematics → Applied → Mathematical Physics (Hamiltonian mechanics)

**What we take: étendue, and the reason it is a conservation law rather than a rule of
thumb.** Étendue

$$G \;=\; n^2 \!\! \iint \!\! \mathrm{d}A\,\mathrm{d}\Omega \;\approx\; n^2 A\,\Omega$$

is conserved through any lossless optical system. The project uses it as a budget — `docs/13`
§3 calls it "the true currency" — but the deeper statement is worth naming because it tells
you the budget cannot be beaten by cleverness. **Étendue conservation is Liouville's theorem
applied to optical phase space.** Rays are points in a four-dimensional phase space of
position and direction; a lossless optical system is a canonical transformation; and
Liouville's theorem says the phase-space density $\rho(q,p)$ is invariant along the flow,

$$\frac{\mathrm{d}\rho}{\mathrm{d}t} \;=\; \frac{\partial\rho}{\partial t} + \{\rho, H\} \;=\; 0 .$$

Volume in phase space cannot be compressed. That is why you cannot take a small bright source
and make it a large bright image without paying somewhere, why brute-force broadcast to every
direction in a room is unaffordable, and why pupil steering is not an optimisation but the
only available move. The tracker is not a feature; it is the thing that keeps the design
inside a conservation law.

**Where it enters.** `docs/02` §2.3 and §4.3, `docs/13` §3.
**Status.** `[DERIVED]`. The identification of étendue with Liouville is standard in
Hamiltonian optics and is stated here because the repo uses the consequence without naming
the cause.

## II.4 Physics → Applied Physics → Optics, and Engineering → Colorimetry: Radiometry and Photometry

**What we take.** The luminous flux a Lambertian emitter of area $A$ at luminance $L$ must
produce, $\Phi = \pi L A$, and its consequence that optical power scales with the **square**
of the subject's linear size — a result `docs/10` §40 records as connecting the aperture law
directly to the thermal constraint. Also the additive-contrast relation that governs a
see-through image against a lit background,

$$C \;=\; \frac{L_\text{image} + L_\text{background}}{L_\text{background}},$$

which is why a free-space image can never reach infinite contrast, can never occlude, and
needs a dark backdrop rather than merely a bright projector.

**Status.** `[DERIVED]` from `[VERIFIED]` photometric definitions; the 55.7 cd/m² face-parity
anchor in `docs/02` §7.1 is `[DERIVED]`.

## II.5 Optometry and Vision Science → Visual Science → Visual Optics (accommodation and depth of field)

**What we take.** The eye resolves depth in **diopters**, not millimetres. A subject of
front-to-back depth $t$ whose centre is at distance $R$ spans

$$\Delta D \;=\; \frac{1}{R - t/2} - \frac{1}{R + t/2} \;\approx\; \frac{t}{R^2},$$

and it is optically flat whenever this is smaller than one depth of field. The number of
focal planes a display actually needs is therefore

$$n_\text{planes} \;=\; \max\left(1,\; \left\lceil \frac{\Delta D}{2\,\mathrm{DoF}_{1/2}} \right\rceil\right),$$

which at pod distances evaluates to 1, not the 24–32 that `docs/13` §7 originally specified.
That correction deleted the swept-focus element, the 2,700 Hz switching requirement and a
component priced between ten and fifty thousand dollars each — the single largest cost
removal in the project's history, and it came from reading the eye's specification instead of
the geometry's.

One depth-of-field slab has bounds $1/(1/R \pm \mathrm{DoF}_{1/2})$, and note the horizon: once
$1/R \le \mathrm{DoF}_{1/2}$ the far bound is infinite, so beyond $R = 1/\mathrm{DoF}_{1/2} = 3.33$ m
the eye cannot distinguish the image from infinity at all. **That is why this product is a pod
and not a hall,** and it is a fact about eyes rather than about budgets.

**Status.** The load-bearing constant $\mathrm{DoF}_{1/2} = 0.30$ D is `[PUBLISHED, secondary]`
and explicitly `[UNVERIFIED]` to the decimal: Campbell (1957), *Optica Acta* 4:157–164 and
Marcos, Moreno & Navarro (1999), *Vision Research* 39:2039–2049 are **identified but not
read** in this repository. The whole design rests on it, which is why
`accommodation.robust_window()` exists — it returns the viewer distance that satisfies the
design conditions for *every* value between 0.20 D and 0.50 D, so the geometry does not
depend on which figure turns out to be right.

## II.6 Optometry and Vision Science → Visual Science → Binocular Vision (stereopsis and vergence)

**What we take.** Binocular disparity across the same subject is

$$\delta \;=\; b\,\Delta D \;\approx\; \frac{b\,t}{R^2}$$

with $b$ the interocular distance. Both cues scale identically with subject depth and viewing
distance, so **their ratio cannot depend on either**:

$$\frac{\text{stereo margin}}{\text{accommodation margin}} \;=\; \frac{b \cdot 2\,\mathrm{DoF}_{1/2}}{\theta_\text{threshold}} \;=\; 268 \quad\text{at } b = 65\ \text{mm},\ 0.60\ \text{D},\ 30\ \text{arcsec}.$$

Stereopsis is between two and three orders of magnitude more sensitive to depth than
accommodation, everywhere, for every subject. This is the result that corrected `docs/13` §6,
that reduces vergence–accommodation conflict from a *depth* problem to a *comfort* problem,
that explains why headsets work at all, and that in `docs/17` §4.2 tells us a wrong focus
gradient on the nearest avatar is the cheapest error in the room.

**Status.** `[DERIVED]` in `eng/03_PHYSICS/depth_cues.py`, and it survives the full
stereoacuity sweep — $804\times$ at 10 arcsec, $134\times$ at the most generous 60 arcsec. The
threshold value is `[PUBLISHED, secondary]`; Howard & Rogers, *Perceiving in Depth*, is
identified and not read.

## II.7 Mathematics → Pure → Geometry → Convex Geometry

**What we take: the isoperimetric inequality.** Among all closed plane curves of given
enclosed area, the circle minimises perimeter, $C^2 \ge 4\pi A$. Since `docs/17` §5 shows the
engine count is $N = C/D$, this is not decoration — it is the exact statement of what a
non-circular room costs. For a rectangle of width $W$ and length $L$ enclosing the same
minimum clearance $W/2$,

$$\frac{N_\text{rect}}{N_\text{circ}} \;=\; \frac{2(W+L)}{\pi W}, \qquad \text{minimised at } L = W \text{ where it equals } \frac{4}{\pi} = 1.273 .$$

**A square room can never cost less than 27% more engines than a round one of the same
clearance, and no amount of engineering changes that, because it is a theorem.** A 3:4
rectangle costs 49% more. The marginal derivative $\mathrm{d}N/\mathrm{d}L = 2/D$ gives the
clean design rule: four engines, roughly ten thousand dollars, per extra metre of room in
either dimension.

**Where it enters.** `eng/03_PHYSICS/seated_room.py:isoperimetric_penalty()`, `docs/17` §5.
This connection was not previously in the project and is the clearest example of a pure-maths
theorem setting a hardware budget.

## II.8 Mathematics → Applied → Analysis → Fourier Analysis and Numerical Analysis

**What we take.** Free-space propagation is a linear shift-invariant filter, so a field at one
plane determines the field at another by the angular spectrum method,

$$U(x,y,z) \;=\; \mathcal{F}^{-1}\!\left\{\mathcal{F}\{U_0\}\,e^{\,i k_z z}\right\}, \qquad k_z = \sqrt{k^2 - k_x^2 - k_y^2},$$

which is what makes computer-generated holography an FFT problem rather than a ray-tracing
one, and therefore what makes it a GPU problem with a known complexity of
$\mathcal{O}(n\log n)$ per plane per frame. Phase retrieval — finding the modulator pattern
that produces a wanted intensity — is the non-convex optimisation underneath, historically
Gerchberg–Saxton and now gradient-based.

**Status.** `[DERIVED]` from standard Fourier optics. The specific quality figures for
competing hologram algorithms quoted in the deck are `[PUBLISHED]` from an extracted figure
and are used only to argue that this half of the problem is public and competitive.

## II.9 Statistics → Mathematical Statistics → Hypothesis Testing, and Psychology → Psychophysics

**What we take.** PQ-1 is a two-alternative forced-choice psychophysical experiment analysed
under a pre-registered plan, and it uses three distinct statistical instruments.

*Signal detection theory* turns a proportion-correct into a sensitivity index
$d' = z(H) - z(F)$, separating what an observer can discriminate from how willing they are to
say so — the reason 2AFC is used rather than a rating scale.

*Two one-sided tests* (TOST) exist because the calibration cell of PQ-1 wants a **null**, and
a conventional test can never provide one. Equivalence within a margin $\Delta$ is concluded
only if both one-sided tests reject:

$$H_{01}: \mu \le -\Delta \quad\text{and}\quad H_{02}: \mu \ge +\Delta .$$

*Holm–Bonferroni* controls the family-wise error rate across the secondary comparisons by
requiring the $i$-th smallest $p$-value to satisfy $p_{(i)} \le \alpha/(m-i+1)$.

**Where it enters.** `eng/08_VERIFY/tests/test_pq1_design.py` and `test_pq1_analysis.py`. The
design was validated on four hundred simulated studies in each of four synthetic worlds
before any subject was proposed, which found four faults — including one that condemned 15%
of good rigs and silently ate the same fraction of the study's power.
**Status.** `[DERIVED]`, and the analysis is the most thoroughly checked artefact in the repo.

---

# Part III — Fields required to build it

## III.1 Physics → Modern → Condensed Matter → Semiconductor Physics

Digital micromirror devices are CMOS-substrate MEMS: roughly a million aluminium mirrors on
torsion hinges over SRAM cells, tilting $\pm 12°$ and switching in microseconds. What we take
is the switching rate and the mirror count as hard specifications, and the fact that the
device is sold only as part of a controller set through licensed design houses — which is a
market structure fact with more effect on the bill of materials than any physical property.
Laser and LED source physics enters through wall-plug efficiency, spectral width (which sets
HOE Bragg selectivity), and coherence length (which sets speckle).

## III.2 Physics → Classical → Continuum Mechanics → Elasticity and Fracture Mechanics

**Because the steering element is mechanical, the failure mode is fatigue.** A DMD hinge is a
thin aluminium-alloy torsion flexure cycled at the binary pattern rate. Cycles accumulate as

$$N_\text{cycles} \;=\; f_\text{binary} \times t_\text{operating}$$

which at 32,225 Hz for 8 hours a day, 250 days a year is $2.3\times10^{11}$ actuations per
device per year. Against an order-$10^{12}$ endurance figure — **`[UNVERIFIED]`**, recalled
from vendor reliability material and not read here — that is a roughly four-year replacement
interval across 34 devices, and it is an opex line that appears in no cost model this project
has written. Flagged in `docs/17` §6.

## III.3 Engineering → Electrical → Control Systems, and Mechanical → Dynamics → Vibration Analysis

**What we take.** Two requirements on the steering element, derived in `docs/17` §6. Pointing
accuracy to land a beam inside a pupil of diameter $d$ at range $L$ with margin $k$:

$$\sigma_\theta \;\le\; \frac{d}{k\,L} \;=\; 0.40\ \text{mrad optical},$$

halved again for a mirror. And the settling budget, which is the one that actually decides the
architecture — an engine serving $N_p$ pupils at frame rate $f$ with optical duty $\eta$ must
slew and settle within

$$t_\text{settle} \;\le\; \frac{1-\eta}{f\,N_p} \;=\; 278\ \mu\text{s at } N_p = 12,\ f = 60\ \text{Hz},\ \eta = 0.8 .$$

Closed-loop galvanometers are millisecond-class for multi-degree steps, so a separate
mechanical steering stage would spend half the frame in transit. The resolution is that the
DMD is itself the mechanical steering element and the direction is encoded in the pattern, so
steering costs one frame slot and no settling transient.

**Vibration** enters through pointing stability: holding 0.4 mrad while the building moves.
Office floor vibration is specified on the ISO/VC curves, and a rigid ceiling-mounted ring
translating rather than tilting is the geometry that survives it; a floor-mounted ring
couples footfall from people walking inside the room directly into pointing. That is a
one-line design rule with a civil-engineering origin, and it is the reason the ring hangs.

## III.4 Materials Science → Thin Films and Coatings, and Polymer Science

The relay band is a photopolymer film — Bayfol HX class — in which volume gratings are
recorded by interference. What we take is the recording chemistry's dynamic range, its
angular and spectral selectivity, its shrinkage on cure (which shifts the Bragg condition and
therefore the aim), and its environmental stability over a decade on a wall. The supplier's
demonstrated capability tops out at 1400 mm web and an A2 master, against a requirement of
several square metres, and `docs/16` names this component as simultaneously the only
defensible moat and the single-source supply risk. `docs/17` §5.1 adds a second problem the
rectangle creates: a circular band is one master repeated $N$ times, while a rectangular band
needs about nine distinct prescriptions.

## III.5 Computer Science → AI → Computer Vision, and Systems → Real-time Systems

Head and pupil tracking is a pose-estimation problem under hard real-time constraint. The
tracker must deliver pupil positions at $\ge 120$ Hz with end-to-end latency under about 5 ms,
because the total motion-to-photon budget is set by ITU-T G.114's 150 ms for conversational
interaction and the optical engine is currently unbudgeted within it. Two properties matter
more than accuracy: the estimator must **fail dark rather than bright**, since a tracker that
loses lock and keeps emitting is pointing light at faces with nothing watching where it goes;
and its latency distribution matters more than its mean, because a tail event is a beam
landing on a cheek.

Avatar capture uses 3D reconstruction and Gaussian-splat representations, and `docs/18` §VI
records the deliberate conclusion that this half is **not** defensible intellectual property —
the splat-to-hologram bridge is public, competitive and improving annually.

## III.6 Computer Science → Systems → Parallel Computing → GPU Computing, and Operations Research → Scheduling Theory

Hologram computation is FFT-bound and belongs on a GPU. But there is a second, less obvious
computational problem: **which engine serves which pupil this frame.** With $N$ engines each
able to cover a wedge and $M$ pupils moving through the room, the per-frame allocation is a
bipartite assignment problem,

$$\min \sum_{i,j} c_{ij}\,x_{ij} \quad \text{s.t.} \quad \sum_j x_{ij} \le 1,\ \sum_i x_{ij} \ge 1,$$

with $c_{ij}$ the cost of engine $i$ serving pupil $j$ — infinite if $j$ lies outside $i$'s
wedge. It is solvable exactly in polynomial time by the Hungarian algorithm, but it has to be
re-solved every frame with hysteresis, because an assignment that flickers between engines
produces a visible luminance flicker on a viewer's retina. This is a scheduling problem with
deadlines wearing an optics costume, and the project has not written it down anywhere else.

## III.7 Engineering → Mechanical → Heat Transfer and HVAC, and Physics → Acoustics → Room Acoustics

Both are covered quantitatively in `docs/17` §7. The heat load of 34 engines, eight people and
a render node is 2,644 W in a 46.7 m³ room, raising unventilated air temperature at

$$\frac{\mathrm{d}T}{\mathrm{d}t} \;=\; \frac{Q}{\rho V c_p} \;\approx\; 2.8\ \text{K per minute},$$

roughly three times a normal small meeting room's provision, in a room whose walls cannot
carry grilles. The acoustic problem is that the optical band removes the surface a meeting
room normally treats, pushing the entire absorption budget onto the ceiling the engines want,
with Sabine's $T_{60} = 0.161\,V/\sum S_i \alpha_i$ giving 0.38 s with an absorptive ceiling
and an unusable 0.87 s without. And the field supplies an argument for the rectangle that the
optics do not: **a cylindrical room focuses sound on its own axis**, exactly where the image
and the speaker are, which is a known defect of circular rooms in architectural acoustics.

## III.8 Medical Sciences → Radiation Science → Non-ionizing Radiation, and Ophthalmology

Every steered beam is aimed at a pupil by design, so the eye-safety case is not incidental to
this architecture — it *is* the architecture. IEC 62471 photobiological risk grouping and IEC
60825 laser classification apply, and the binding quantity for a small apparent source viewed
directly is retinal radiance rather than total power. Two design rules follow and both are
already in the project: the tracker must fail dark, and the safety case and the cost case are
the same argument, because the thing that makes 19 engines sufficient instead of 275 is also
the thing that concentrates light on eyes.

---

# Part IV — Human, social and commercial fields

## IV.1 Psychology → Cognitive → Perception, and Communication Sciences → Nonverbal Communication

**Gaze.** On a flat screen every viewer sees the same rendered face, so everybody believes
they are being addressed and nobody can tell who actually is — the Mona Lisa effect. A real
image in free space is seen from each seat's own angle, so an avatar turning to address one
person is seen to turn, correctly and simultaneously, by everyone. Round-table gaze awareness
is a documented failure of video conferencing and it is the meeting-specific thing this
architecture wins. `docs/17` §8 records that it is untested and is not currently among PQ-1's
conditions, and that it should be.

## IV.2 Anthropology → Cultural, and Social Psychology: Proxemics

**The niche result.** Hall's proxemic zones place personal distance at roughly 0.45–1.2 m and
social distance at 1.2–3.6 m, with the boundary between them at about 1.2 m — the distance at
which a Western adult stops treating an encounter as intimate and starts treating it as
social. `eng/03_PHYSICS/seated_room.py` returns a robust optical window for a seated bust of
**1.00–1.20 m**, and the standing-body window is 1.30–1.35 m. **The optical window and the
social boundary coincide to within a few centimetres, for entirely unrelated reasons** — one
is the eye's depth of field against a background, the other is a cultural convention about
personal space. That is a coincidence rather than a mechanism, but it is a useful one: the
distance the physics wants is the distance a meeting naturally adopts, so the design does not
have to fight furniture or fight people. `[UNVERIFIED]` as to Hall's exact figures, which are
recalled and not read here, and culture-dependent in any case.

## IV.3 Cognitive and Computer Science Interfaces → HCI → Computer-mediated Communication

Co-presence and social presence are measured constructs with published instruments, not
opinions. The result the project takes most seriously is the one that argues *against* it: a
post-hoc Nemenyi test in the literature returns $p = 0.900$ between flat video and a video
grid on co-presence, and a correctly placed two-dimensional cutout scored 5.2 of 7 against a
full three-dimensional avatar's 5.3 — statistically indistinguishable — while the flat cutout
*won* on rated fidelity, 5.1 to 3.7. A second study finds that a well-timed physical cue
moves impermeability scores far more than an extra visual dimension does. These are the
strongest published arguments that the product may not be perceptible, and they are the
reason PQ-1 exists.

## IV.4 Sports Science → Ergonomics, and Biomedical Engineering → Biomechanics: Anthropometry

Seated eye height about 1.20 m, standing about 1.60 m, seat pan 0.45 m, table 0.74 m, top of a
seated head 1.29 m, interocular distance 65 mm with a population range of roughly 55–72 mm.
These are not trivia: `docs/17` §1 shows the band envelope is the eye-height *spread*
multiplied by the lever ratio, so the 5th-to-95th-percentile spread propagates directly into
square metres of the most expensive component in the room. `[ASSUMED]`, from
`models/build_models.py`, and worth replacing with a real anthropometric standard.

## IV.5 Political Science → Public Policy, and Science and Technology Studies → Technology Regulation

A live-driven photorealistic avatar of a real person is a deepfake under EU AI Act Article 50,
which has been in force since 2 August 2026, and carries transparency obligations. This is a
product-defining constraint rather than a compliance footnote, because the obligation attaches
to the thing the product *is*. Recorded in `docs/16`.

## IV.6 Economics → Microeconomics → Producer Theory, and Industrial Organization

Unit economics: one researched price of $\$2{,}595$ per display engine against an assumed
$\$900$ broke the bill of materials by a factor of three and withdrew a 70% margin claim,
which stays withdrawn until a written quote exists. Market structure matters as much as
price: the modulator is available only through licensed design houses, which is a
distribution fact that no engineering decision can route around.

---

# Part V — The niche fields, and what each one actually bought

These are the connections that were not obvious. Each is listed with the concrete thing it
produced, because a field that buys nothing does not belong on this list.

**Convex geometry → the isoperimetric inequality.** Bought the exact price of a rectangular
room: $4/\pi = 1.273$ minimum, 1.49 for the 3.6 × 4.8 m plan, and the rule that a metre of
room length costs four engines. A theorem, so it cannot be engineered away.

**Hamiltonian mechanics → Liouville's theorem.** Bought the reason étendue is a conservation
law and not a rule of thumb, and therefore the reason pupil steering is forced rather than
chosen.

**Combinatorial optimisation and graph theory → bipartite matching.** Bought the recognition
that engine-to-pupil allocation is a per-frame assignment problem needing hysteresis, which
nothing in the repo currently implements and which will produce visible flicker if it is
written naively.

**Architectural acoustics → concave focusing.** Bought an argument for the rectangle that has
nothing to do with optics: a cylindrical pod focuses sound on the axis where the image and
the speaker stand. Also bought the finding that the optical band and the acoustic absorber
compete for the same ceiling.

**Estimation theory → the Cramér–Rao bound.** Any unbiased pupil-position estimator has
variance floored by the inverse Fisher information, $\sigma^2_{\hat\theta} \ge 1/I(\theta)$,
which for a photon-limited centroid scales as the inverse of collected photons. That converts
"the tracker must be accurate" into "the tracker's illuminator power, exposure and pupil
contrast set a hard precision floor," and it is the right way to specify it. Not yet used.

**Fracture mechanics and fatigue → hinge endurance.** Bought a four-year scheduled replacement
interval across 34 devices that no cost model contains.

**Structural dynamics → floor vibration.** Bought the rule that the engine ring hangs from the
ceiling rather than standing on the floor, because footfall inside the room would otherwise
couple straight into pointing.

**Tribology → flexures over bearings.** If any macroscopic steering stage survives into the
design, a bearing wears and a flexure does not, and for a device expected to run eight hours a
day for a decade that decides the mechanism. Recorded as a rule, not yet a decision.

**Metrology → co-registration.** Thirty-four engines must agree on where the image point is to
much better than a pupil diameter. That is a calibration problem with an established
discipline behind it — bundle adjustment, traceable artefacts, drift budgets — and
`docs/calibration.md` is where it belongs.

**Scheduling theory → time-slicing.** $K$ remote seats share one modulator, and the frame
budget divides $K$ ways with deadlines. The DMD's roughly sixty-fold headroom covers $K = 4$;
the film's dynamic range is what actually binds.

**Colorimetry → additive gamut against a visible background.** A see-through image adds its
light to whatever is behind it, so the achievable gamut is a function of the backdrop, not a
property of the source. Colour management for an additive display against a non-black
background is a real sub-field and the project has not touched it.

**Proxemics → the 1.0–1.2 m coincidence.** Covered in §IV.2.

---

# Part VI — Fields we are deliberately not using

A project that claims every field claims none. These were considered and set aside, each for a
stated reason.

**Quantum optics and quantum information.** Coherence matters to this design classically —
speckle, Bragg selectivity, interference recording — but no quantum property does. There is no
entanglement, no squeezing and no single-photon regime anywhere in the architecture.

**Nonlinear optics.** No frequency conversion, no self-focusing, no parametric process. The
power densities are far too low and there is no need.

**Acousto-optics.** Genuinely evaluated as a steering mechanism, because microsecond random
access would dissolve the settling problem in §III.3. Rejected on angular range of a few
degrees, diffraction efficiency, and chromatic dispersion across a colour image — not on the
mechanical constraint.

**Adaptive optics and deformable mirrors.** Deleted by `docs/15`'s finding that one focal
plane suffices. This was the highest-cost, highest-risk component in the design and it is
gone.

**Acoustic levitation and optical trapping.** A live branch of the project — `constants.py`
holds the 40 kHz MATD parameters — but a *separate* one. It is the single published exception
to the aperture bound, since matter at the image point needs no aperture, and it does not
scale past one particle in a cubic centimetre.

**Plasma physics and ionised-air displays.** Investigated in `docs/12` and killed on
arithmetic: excited room air converts about $7\times10^{-5}$ of deposited energy into photons
at 300–430 nm, giving roughly $5\times10^{-6}$ lumens per watt, so a dim floating head needs
of order $10^5$–$10^6$ watts dumped continuously into the room.

**Deep learning for the optical path.** Used for avatar capture and pose estimation only.
Nothing in the light path is learned, and nothing should be — a display whose geometry is a
network's opinion cannot be verified against the clipping theorem.

---

# Part VII — Where the standard taxonomy has no box for what we need

Recorded because the absence caused real difficulty in writing this document.

**Computer graphics is entirely missing** from the field list this document was mapped
against — no rendering, no rasterisation, no light transport, no real-time graphics — despite
being a mature discipline that this project uses continuously. It has been filed under
Computer Science → AI, which is wrong.

**Psychophysics has no entry.** It appears only implicitly under Cognitive Psychology →
Perception Research, despite being a distinct methodological tradition with its own
instruments, and it is the discipline PQ-1 is written in.

**Photobiology has no entry.** Optical radiation hazard to the retina sits between Radiation
Science and Ophthalmology in the taxonomy and is fully in neither, despite being the field
that governs whether this device is legal to switch on.

**Optical engineering is scattered.** Geometric optics, diffractive optics, radiometry,
illumination design and tolerancing appear in four separate places under Physics and
Engineering, with no single heading. For a project whose entire risk sits there, that is the
most inconvenient gap of the four.

**Law and intellectual property are absent altogether** from a taxonomy that includes Forensic
Science and Actuarial Science, despite `docs/05` being an entire document on patent
architecture.

---

## Cross-reference

| Field | Primary document | Code |
|---|---|---|
| Geometric optics, tiling law | `docs/13` §1, `docs/17` §1, §5 | `accommodation.py`, `seated_room.py` |
| Diffractive optics, HOE | `docs/02` §2–4, `docs/13` §2 | — |
| Étendue, Liouville | `docs/02` §4.3, `docs/13` §3 | — |
| Accommodation, depth of field | `docs/15`, `docs/17` §4.1 | `accommodation.py` |
| Stereopsis, binocular vision | `docs/13` §6 corrected | `depth_cues.py` |
| Convex geometry, isoperimetric | `docs/17` §5 | `seated_room.py` |
| Psychophysics, TOST, Holm | `experiments/perceptual-quality/` | `test_pq1_*.py` |
| Control, actuation, fatigue | `docs/17` §6 | `seated_room.py` |
| Acoustics, HVAC | `docs/17` §7 | `seated_room.py` |
| Proxemics, anthropometry | `docs/17` §4 | `seated_room.py`, `build_models.py` |
| Regulation, unit economics | `docs/16` | — |
