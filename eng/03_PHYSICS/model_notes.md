# MATD Physics Model — First-Principles Derivations

Every equation in this document is either (i) textbook/standard and marked as
such, or (ii) derived here with the steps shown. Numbers computed inline use
`eng/03_PHYSICS/constants.py` values. All results feed the simulator in
`eng/04_SIM/`. Status labels per `02_CLAIMS/CLAIM_LEDGER.md`.

---

## 1. The array field (Rayleigh–Sommerfeld, piston sources)

Each of the two arrays is a 16×16 grid of piston transducers at 10 mm pitch
(160 mm aperture, CLAIM C-01). A piston of radius `a_T` at position `x_n`
radiating amplitude `P_ref` at 1 m contributes (standard result, [1]):

    p_n(x) = P_ref · (1/|x − x_n|) · D(θ_n) · exp(i(k|x − x_n| + φ_n))
    D(θ)   = 2·J₁(k·a_T·sin θ) / (k·a_T·sin θ)        (piston directivity)
    θ_n    = angle between (x − x_n) and the transducer normal

Superposition over all N transducers of both arrays:

    p(x) = Σ_n p_n(x)            (with φ_n per the phase law, §2)

**Usage in this package:** the full field is computed only at validation time
(Phase 4 ladder) and at calibration points. The trajectory feasibility oracle
(Phase 5) uses the **local harmonic-trap model** (§5) whose parameters are
derived from this field — this is what makes Monte Carlo over millions of
trajectory seconds affordable while keeping the physics anchored.

**UNKNOWN parameter:** `P_ref` normalization (the absolute pressure at 1 m).
The published sources do not state it. The simulator instead calibrates the
trap-region amplitude `P_0` (§6) against the published kinematics
(141 m/s², 8.75/3.75 m/s, 0.75 m/s corners) — the honest way to stay
"experimentally grounded" without inventing a value. Ledger rows C-31, C-32,
C-70–72 depend on this calibration.

## 2. Standing-wave node-trap phase law (the MATD's operating principle, [2])

**Correction 2026-08-15 (Phase 4):** the MATD display trap is a standing-wave
**node trap**, not a bare twin trap. In a node trap all elements focus on a
single target with the array split by planes: elements on the top half receive
+π, the bottom half 0 (or equivalent phase split), producing a pressure node
at the focus:

    φ_n = k|F − x_n| + π·H(z_n > 0)      (HAT, PNAS 2018; MATD, Nature 2019)

A 3D display volume is a **lattice of such node traps** at the minimum
independent spacing 1.4λ = 12 mm (PNAS 2018); adjacent traps are ~1.4λ apart,
each a local pressure node (the phase-law superposition is computed by
arg of the sum of complex element contributions, `field.lattice_field`).

The bare **twin trap** (two foci ±π apart) is a different device: it creates
a planar pressure **null sheet** between two cylindrical fingers, is ~30×
weaker axially, and cannot levitate (PNAS 2018; Nature Communications
ncomms9661). It is retained in `field.twin_trap_field` only as a reference;
it is NOT the display trap model.

## 3. Gor'kov potential and force [standard, [3]]

For a sphere of radius `a` much smaller than λ in a field (p, v):

    U = 2πa³ρ_air·c² [ f₁·|p|² / (3·ρ_air²·c⁴) − f₂·|v|² / (2·c²) ]

    f₁ = 1 − ρ_air·c²/(ρ_b·c_b²)              (compressibility term)
    f₂ = 2(ρ_b − ρ_air)/(2·ρ_b + ρ_air)       (density term)

    F = −∇U

**EPS bead (a = 1 mm, ρ_b = 30 kg/m³, c_b ≈ 1000 m/s ASSUMED):**

    f₁ = 1 − 1.204·343²/(30·10⁶) = 0.995     [DERIVED, C-16-based]
    f₂ = 2·(30−1.204)/(60+1.204) = 0.941      [DERIVED]

Note (fix 2026-08-15): the velocity term divides by c² (the prefactor
2πa³ρc² already carries the c²); an earlier draft divided by c⁴ and
underestimated the lateral well by a factor c² = 1.18e5.

**Plane standing wave sanity check (derived here).** Take p(z) = P_0·cos(kz)
(velocity v(z) = P_0/(ρ_air·c)·sin(kz), [standard]): writing u = kz − π/2
(pressure node at u = 0),

    U(u) = A·[ f₁·sin²(u)/3 − f₂·cos²(u)/2 ],   A = 2πa³·P_0²/(ρ_air·c²)

- Node is a minimum: U(0) = −A·f₂/2 < 0, while the antinode is a maximum.
  Dense compressible particles trap at pressure nodes. ✓ (matches MATD)
- Axial stiffness at the node:

    k_ax = U″(0) = 2A·k²·(f₁/3 + f₂/2)
         = 4πa³·P_0²·k²·(f₁/3 + f₂/2)/(ρ_air·c²)

  Numerically (a = 1e−3 m, k = 2π/λ = 732.8 m⁻¹, f₁/3 + f₂/2 = 0.802):

    k_ax = 4.77e−9 · P_0²   [N/m]     [DERIVED — ledger C-70]

- Well depth between adjacent nodes:

    U_well = A·(f₁/3 + f₂/2) = 4.45e−15 · P_0²   [J]     [DERIVED — C-71]

- The potential is sinusoidal along z (period λ/2) ⇒ the axial well edge is
  the adjacent node at **Δp_esc_ax = λ/4 = 2.14 mm** (force stops growing at
  the λ/8 inflection, but the bead leaves only when it crosses the barrier).
  The **lateral** well edge is the lattice half-period **Δp_esc_lat =
  6 mm** (12 mm spacing / 2). Per-axis escape distances `ESC_AX` = (6, 6,
  2.14) mm; the spring saturates at k_i·ESC_AX_i per axis.

    F = min(|F_harmonic_i|, k_i·ESC_AX_i)   per axis   (particle.py)

**Calibration (step-pinned, Phase 4):** the field's absolute pressure is
UNKNOWN (the array model's amplitude is abstract); the stiffness is pinned to
the published 141 m/s² step response (C-09) by k = m·a/dx = M_BEAD·141/1 mm:

    K_TARGET = 1.77e−2 N/m   (gain 1.235)   [DERIVED — C-31]
    K_LAT = 9.66e−4 N/m, ratio 0.055        [DERIVED — C-31]
    gravity sag = mg/k = 70 µm ≪ Δp_esc     [DERIVED]
    drag limits: v_vert = k_ax·Δp_esc_ax/γ = 110 m/s, v_horz = 16.9 m/s

## 4. Particle dynamics

    m·ẍ = F_trap(x, t) − 6πη_air·r·(ẋ − u_dist) + m·g

with m = 4/3·πa³·ρ_b = 1.26e−7 kg [DERIVED C-17], drag coefficient
γ = 6πη_air·r = 3.44e−7 N·s/m [DERIVED], u_dist = ambient air velocity
(PRD-20: ≤ 0.3 m/s).

**Free-decay drag time constant:**

    τ = m/γ = 1.26e−7 / 3.44e−7 ≈ 365 ms        [DERIVED — C-18]

τ ≫ 10 ms frame period — but this does **not** mean the bead cannot follow:
in a spring trap the response is spring-dominated. The trap angular
frequency is ω_trap = √(k_ax/m) ≈ 375 rad/s ≫ 1/τ, so the bead rides the
trap; the damping ratio is ζ = γ/(2√(km)) ≈ 0.016 (nearly undamped).

**Ring-limited operating acceleration (Phase 4 finding, C-35):** because
ζ ≈ 0.016, any acceleration change makes the bead's error swing to ~2× the
static lag (2·m·a/k at t = π/ω). The sustained operating acceleration on an
axis is therefore

    a_op = 0.9 · k_i · Δp_esc_i / (2·m)

(lateral 20.7 m/s², vertical ≥ 100 m/s² with the axial stiffness). Timing
laws must respect a_op; the old P_0 = 680 Pa / k = 4.77e−9·P_0² calibration
was 14× too weak (gravity sag 19.5 mm ≫ well) and is superseded by the
step-pinned calibration (§3).

**Sustained-speed ceilings (Phase 4 R3/R4):** vertical ≥ 30 m/s,
horizontal 6.7 m/s (drag limits 110 / 16.9 m/s) — the published C-07
8.75 and C-08 3.75 m/s are reproduced with headroom.

## 5. Feasibility oracle (fast model used for avatar capacity)

For trajectory feasibility the full field is replaced by a local
spring-with-saturation model, parameters taken from the calibrated field:

    ẍ = [F_harmonic + F_sat_cap − γ·(ẋ − u_dist) + m·g] / m
    F_harmonic_i = −k_i·(x_i − x_trap_i), capped at |F_i| = k_i·ESC_AX_i

with anisotropy: k_lat = r_lat·k_ax (r_lat DERIVED from the array field:
ratio 0.055 in Phase 4; sweeps cover r_lat ∈ [0.05, 1.0]). Escape distances
per axis: ESC_AX = (6, 6, 2.14) mm (lateral = lattice half-period,
axial = node-to-barrier). Trap command `x_trap(t)` is the trajectory output
(§7), updated at the phase-update rate (16 kHz).

**Metrics per simulated trajectory:**
- follow-error ε(t) = |x − x_trap|
- stability margin m(t) = 1 − ε(t)/Δp_esc
- loss-of-trap event when ε ≥ Δp_esc (count + timestamp)
- max |a|, max |v|, jerk at update instants (timing-jitter axis)

## 6. Phase-update coupling and discretization

Field updates arrive every Δt_u = 1/PHASE_UPDATE_RATE = 62.5 µs (nominal
16 kHz, C-14). Between updates the field is constant ⇒ the trap command is a
zero-order hold. Effects captured in the simulator:
- the bead integrates under a *piecewise-constant* force (exact physical
  discretization of a ZOH-driven trap);
- timing jitter (σ_tj) on update instants injects force-direction error,
  swept in Monte Carlo;
- jerk spikes at update instants scale with |ẋ_trap| — quantified in SIM-01.

## 7. Trap command generation (trajectory → phases)

Given a desired particle path q(s), the trajectory module (`trajectory.py`)
computes trap positions u(t) = q(τ(t)) with a **jerk-limited speed profile**
of OptiTrap class [4]: speed clamped to (v_max_class, a_max_class), the
acceleration built up at the jerk limit over the whole path (per-segment
S-curve restarts rang the nearly-undamped bead — ladder R5 finding), with
the ring-limited operating acceleration a_op (§4, C-35) replacing the raw
force budget. u(t) is then a continuous signal sampled at the phase rate.

## 8. What remains UNKNOWN after this model (honest list)

| Quantity | Status | Promotion path |
|---|---|---|
| Absolute field amplitude | abstract (unitless); stiffness pinned to 141 m/s² step (C-09) | in-situ pressure measurement |
| Lateral stiffness ratio r_lat | derived from lattice geometry: 0.055; corner-implied ~1; swept 0.05–1.0 | near-field scan / stroboscopy |
| Trap damping beyond Stokes (streaming) | ignored — swept as disturbance | flow visualization |
| Transducer harmonic/creep response | ignored | transducer datasheet + bench |
| EPS acoustic impedance (c_b) | assumed 1000 m/s, swept ρ_b | supplier datasheet |
| Corner geometry of published rig | unknown (Phase 4: 0.75 m/s tracked at 43 mm radius @ ratio 0.055) | paper figures / reproduction |

## References

[1] Rayleigh–Sommerfeld piston radiation — standard acoustics (e.g., Blackstock,
    *Fundamentals of Physical Acoustics*).
[2] Standing-wave node traps: Marzo & Drinkwater, PNAS 115(36) (2018) —
    HAT; Hirayama et al., Nature 575:320–323 (2019) — MATD. Twin-trap
    reference (planar null, not levitation): Nature Communications 7:12564
    (2016), ncomms9661.
[3] Gor'kov, L.P., *Sov. Phys. Dokl.* 6:773 (1962) — standard derivation.
[4] OptiTrap, ACM TOG 41(5) (2022), DOI 10.1145/3517746 — trajectory timing.
