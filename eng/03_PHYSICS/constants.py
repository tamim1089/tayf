"""
TAYF Digital Engineering Proof Package - physical constants and baseline
parameters. Single source of truth for every simulation in eng/.

Discipline: every number here carries a status label. VERIFIED = measured
in the cited primary source. DERIVED = computed here from verified inputs,
formula shown. ASSUMED = engineering baseline, explicitly marked, to be
swept in Monte Carlo. UNKNOWN = no basis yet; treated as risk driver.

Environment: air at 20 C, 1 atm.
"""
from dataclasses import dataclass, field
import math

# ---------------------------------------------------------------------------
# Constants of the medium (20 C, 1 atm) - standard values, treat as exact
# ---------------------------------------------------------------------------
C_AIR = 343.0            # m/s, speed of sound
RHO_AIR = 1.204          # kg/m^3
ETA_AIR = 1.825e-5       # Pa.s dynamic viscosity
G = 9.81                 # m/s^2

# ---------------------------------------------------------------------------
# Drive parameters
# ---------------------------------------------------------------------------
F_DRIVE = 40e3           # Hz  [VERIFIED] MATD/APL transducers
LAMBDA = C_AIR / F_DRIVE  # 8.575 mm [DERIVED] lambda = c/f
HALF_LAMBDA = LAMBDA / 2.0  # 4.287 mm - minimum trap separation [DERIVED]

# Phase update rate: field recomputed at 40 kHz / N_cycles_per_update.
# [ASSUMED] N=2.5 -> 16 kHz; SPIE: position updates limited by transducer
# frequency; "17k steps/s" quoted in matd_plan.md. Sweep in Monte Carlo.
CYCLES_PER_UPDATE = 2.5
PHASE_UPDATE_RATE = F_DRIVE / CYCLES_PER_UPDATE  # 16 kHz nominal

# ---------------------------------------------------------------------------
# Array geometry (MATD reference: two opposed 16x16 arrays, 10 mm pitch)
# ---------------------------------------------------------------------------
ARRAY_N = 16             # transducers per side
ARRAY_PITCH = 10e-3      # m  [VERIFIED] 10 mm pitch, 160 mm aperture
TRANSDUCER_RADIUS = 4.5e-3  # m  [ASSUMED] MA40S4S-class piston radius
TRANSDUCER_REF_PRESSURE = 1.0  # Pa at 1 m - [UNKNOWN] normalization;
#                              # calibrated later against published trap depth
ARRAY_SEPARATION = 0.234  # m [VERIFIED] 23.4 cm between array faces
WORKSPACE_CUBE = 0.100    # m [VERIFIED] 10 x 10 x 10 cm control volume

# ---------------------------------------------------------------------------
# Particle (display bead)
# ---------------------------------------------------------------------------
BEAD_RADIUS = 1.0e-3      # m [VERIFIED] 1 mm radius EPS bead (ledger C-15)
RHO_BEAD = 30.0           # kg/m^3 [ASSUMED] EPS 20-50 kg/m^3; sweep 10-60

BEAD_MASS = 4.0 / 3.0 * math.pi * BEAD_RADIUS**3 * RHO_BEAD  # kg [DERIVED]
DRAG_COEF = 6.0 * math.pi * ETA_AIR * BEAD_RADIUS            # [DERIVED]
TAU_FREE_DECAY = BEAD_MASS / DRAG_COEF   # s [DERIVED] ~365 ms at r=1mm rho=30

# ---------------------------------------------------------------------------
# Physics reference numbers from the literature (validation targets)
# ---------------------------------------------------------------------------
REF_V_MAX_VERT = 8.75     # m/s [VERIFIED] Nature 2019
REF_V_MAX_HORZ = 3.75     # m/s [VERIFIED] SPIE 2020
REF_A_MAX = 141.0         # m/s^2 [VERIFIED] SPIE 2020 highest accel (visual only)
REF_V_CORNER = 0.75       # m/s [VERIFIED] SPIE 2020 corner speed (visual only)
REF_FRAME_RATE = 12.5     # Hz [VERIFIED] SPIE 2020 max image frame rate
REF_POV_WINDOW = 0.1      # s [VERIFIED] persistence-of-vision integration window

# ---------------------------------------------------------------------------
# Derived display-side quantities (labels; values computed at import)
# ---------------------------------------------------------------------------
DISPLAY_RATE_MIN = 10.0   # Hz [REQUIREMENT] PRD-08
DISPLAY_RATE_TARGET = 12.5  # Hz [VERIFIED-capable] PRD-08


@dataclass
class SimBudget:
    """Baseline Monte Carlo nominal point (all ASSUMED unless VERIFIED)."""
    array_n: int = ARRAY_N
    pitch: float = ARRAY_PITCH
    separation: float = ARRAY_SEPARATION
    bead_radius: float = BEAD_RADIUS
    rho_bead: float = RHO_BEAD
    pressure_gain_db: float = 0.0      # +-3 dB sweep
    phase_rate: float = PHASE_UPDATE_RATE
    disturbance_mps: float = 0.0       # uniform air velocity bias
    timing_jitter_s: float = 0.0       # command timestamp jitter
    workspace: float = WORKSPACE_CUBE


def bead_mass(radius: float, rho: float) -> float:
    return 4.0 / 3.0 * math.pi * radius**3 * rho


def drag_coefficient(radius: float) -> float:
    return 6.0 * math.pi * ETA_AIR * radius
