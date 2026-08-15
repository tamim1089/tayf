"""
Avatar path builder (Phase 5): the canonical 14-joint / ~40-segment
wireframe avatar scaled into the 10x10x10 cm workspace, and the five motion
classes (PRD-08): standing, talking, head movement, waving, fast gesture.

Each class is a loop of joint trajectories; a frame is the wireframe at one
instant, partitioned into per-bead tours (time-multiplexed traps, C-19).
Feed: capacity_experiment.py. Ledger: C-33 (contested 37.5 cm claim),
PRD-08/09/13.
"""
import numpy as np

H = 0.09  # avatar height (m), fits 10 cm workspace with margin (PRD-06)

# 14 joints: pelvis, head, shoulders, elbows, wrists, hips, knees, ankles
JOINTS = dict(
    pelvis=np.array([0.0, 0.0, 0.050]),
    head=np.array([0.0, 0.0, 0.088]),
    shoulder_l=np.array([-0.012, 0.0, 0.060]),
    shoulder_r=np.array([0.012, 0.0, 0.060]),
    elbow_l=np.array([-0.016, 0.004, 0.046]),
    elbow_r=np.array([0.016, 0.004, 0.046]),
    wrist_l=np.array([-0.017, 0.008, 0.030]),
    wrist_r=np.array([0.017, 0.008, 0.030]),
    hip_l=np.array([-0.010, 0.0, 0.042]),
    hip_r=np.array([0.010, 0.0, 0.042]),
    knee_l=np.array([-0.010, 0.002, 0.026]),
    knee_r=np.array([0.010, 0.002, 0.026]),
    ankle_l=np.array([-0.009, 0.004, 0.010]),
    ankle_r=np.array([0.009, 0.004, 0.010]),
)


def _ring(center, radius, n, axis1="x", axis2="z"):
    a = np.array([0.0, 0.0, 0.0])
    if axis1 == "x":
        a[0], a[1] = 1.0, 0.0
    else:
        a[0], a[1] = 0.0, 1.0
    b = np.zeros(3)
    b[2 if axis2 == "z" else 1] = 1.0
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return center + radius * (np.cos(th)[:, None] * a + np.sin(th)[:, None] * b)


def _edge_points(a, b, n=24):
    return np.linspace(a, b, n)


def _split_at_crossings(segs, tol=2.0e-3):
    """Split segments at close-approach points (the wireframe's crossing
    joints, e.g. spine x shoulder bar) so the bead's tour can pass through
    the shared vertex without teleporting. Returns a new segment list."""
    out = [np.copy(s) for s in segs]
    for i in range(len(segs)):
        for j in range(i + 1, len(segs)):
            si, sj = segs[i], segs[j]
            d = np.linalg.norm(si[:, None, :] - sj[None, :, :], axis=2)
            di, dj = np.unravel_index(np.argmin(d), d.shape)
            if d[di, dj] < tol:
                pi, pj = si[di], sj[dj]
                # split segment i at pi, segment j at pj
                out[i] = _insert_point(out[i], pi)
                out[j] = _insert_point(out[j], pj)
    return out


def _insert_point(seg, p):
    """Insert p into the polyline seg at the nearest vertex position."""
    d = np.linalg.norm(seg - p, axis=1)
    k = int(np.argmin(d))
    return np.concatenate([seg[:k + 1], p[None], seg[k + 1:]], axis=0)


def wireframe(joints, head_n=10, ring_n=4, split=True):
    """Build the ~40-segment wireframe point cloud from joint positions.
    Returns list of polyline segment point arrays (split at crossings so
    tours stay connected)."""
    hc = joints["head"]
    segs = []
    segs.append(_edge_points(joints["pelvis"], joints["head"]))
    segs.append(_edge_points(joints["shoulder_l"], joints["shoulder_r"]))
    segs.append(_edge_points(joints["hip_l"], joints["hip_r"]))
    for side in ("l", "r"):
        segs.append(_edge_points(joints[f"shoulder_{side}"], joints[f"elbow_{side}"]))
        segs.append(_edge_points(joints[f"elbow_{side}"], joints[f"wrist_{side}"]))
        segs.append(_edge_points(joints[f"hip_{side}"], joints[f"knee_{side}"]))
        segs.append(_edge_points(joints[f"knee_{side}"], joints[f"ankle_{side}"]))
        # hands: two fingertips per wrist
        w = joints[f"wrist_{side}"]
        sign = -1.0 if side == "l" else 1.0
        segs.append(_edge_points(w, w + np.array([0.006 * sign, 0.003, -0.004])))
        segs.append(_edge_points(w, w + np.array([0.006 * sign, -0.003, -0.004])))
        # feet: two toe tips per ankle
        a = joints[f"ankle_{side}"]
        segs.append(_edge_points(a, a + np.array([0.004 * sign, 0.0, 0.003])))
        segs.append(_edge_points(a, a + np.array([0.004 * sign, 0.006, 0.003])))
    # head ring (in x-z plane), chest ring, pelvis ring
    hr = _ring(hc, 0.008, head_n)
    for i in range(head_n):
        segs.append(_edge_points(hr[i], hr[(i + 1) % head_n]))
    cr = _ring(0.5 * (joints["pelvis"] + joints["head"]) + np.array([0.0, 0.0, 0.002]),
               0.012, ring_n)
    for i in range(ring_n):
        segs.append(_edge_points(cr[i], cr[(i + 1) % ring_n]))
    pr = _ring(joints["pelvis"], 0.010, ring_n)
    for i in range(ring_n):
        segs.append(_edge_points(pr[i], pr[(i + 1) % ring_n]))
    if split:
        segs = _split_at_crossings(segs)
    return segs


# ---------------------------------------------------------------------------
# Motion classes: joint trajectories over a loop period, sampled at t in [0,T)
# ---------------------------------------------------------------------------
def _rigid_sway(joints, t, T, amp_x=0.004, amp_z=0.002):
    j = {k: np.copy(v) for k, v in joints.items()}
    dx = amp_x * np.sin(2 * np.pi * t / T)
    dz = amp_z * np.sin(4 * np.pi * t / T)
    for k in j:
        j[k][0] += dx
        j[k][2] += dz
    return j


def _head_nod(joints, t, T, amp_deg=15.0):
    j = {k: np.copy(v) for k, v in joints.items()}
    th = np.radians(amp_deg) * np.sin(2 * np.pi * t / T)
    hc = j["head"]
    for k in j:
        if k in ("head",):  # rotate the head point about the neck (fixed)
            continue
    # nod: rotate head ring points about the x-axis through the neck
    neck = np.array([0.0, 0.0, 0.066])
    j["head"] = neck + _rot_x(hc - neck, th)
    return j


def _head_turn(joints, t, T, amp_deg=30.0):
    j = {k: np.copy(v) for k, v in joints.items()}
    th = np.radians(amp_deg) * np.sin(2 * np.pi * t / T)
    neck = np.array([0.0, 0.0, 0.066])
    j["head"] = neck + _rot_y(joints["head"] - neck, th)
    return j


def _wave(joints, t, T, radius=0.020, freq=1.5):
    j = {k: np.copy(v) for k, v in joints.items()}
    ph = 2 * np.pi * freq * t
    w = joints["wrist_r"]
    j["wrist_r"] = w + np.array([0.0, radius * np.cos(ph), radius * np.sin(ph)])
    # elbow follows half-way toward the wrist (soft IK)
    j["elbow_r"] = joints["elbow_r"] + 0.35 * (j["wrist_r"] - w)
    return j


def _fast_gesture(joints, t, T, amp=0.040, freq=2.0):
    j = {k: np.copy(v) for k, v in joints.items()}
    ph = 2 * np.pi * freq * t
    w = joints["wrist_r"]
    j["wrist_r"] = w + np.array([amp * np.sin(ph), 0.0, 0.008 * np.cos(2 * ph)])
    j["elbow_r"] = joints["elbow_r"] + 0.35 * (j["wrist_r"] - w)
    return j


def _rot_x(v, th):
    c, s = np.cos(th), np.sin(th)
    return np.array([v[0], c * v[1] - s * v[2], s * v[1] + c * v[2]])


def _rot_y(v, th):
    c, s = np.cos(th), np.sin(th)
    return np.array([c * v[0] + s * v[2], v[1], -s * v[0] + c * v[2]])


# class -> (loop period T, trajectory function, motion limits)
CLASSES = {
    "standing": dict(T=0.6, fn=lambda t: _rigid_sway(JOINTS, t, 0.6),
                     v_max=3.75, note="idle sway +/-4 mm lateral"),
    "talking": dict(T=0.5, fn=lambda t: _head_nod(JOINTS, t, 0.5),
                    v_max=3.75, note="head nod 15 deg"),
    "head_movement": dict(T=0.4, fn=lambda t: _head_turn(JOINTS, t, 0.4),
                          v_max=3.75, note="head turn 30 deg"),
    "waving": dict(T=0.66, fn=lambda t: _wave(JOINTS, t, 0.66),
                   v_max=3.75, note="right-hand circle 2 cm at 1.5 Hz"),
    "fast_gesture": dict(T=0.5, fn=lambda t: _fast_gesture(JOINTS, t, 0.5),
                         v_max=3.75, note="right-arm sweep 4 cm at 2 Hz"),
}


def frame_segments(class_name, t):
    """Wireframe segments at time t for a class."""
    c = CLASSES[class_name]
    return wireframe(c["fn"](t))


def bead_tours(segments, n_beads=6):
    """Partition wireframe segments into n_beads balanced tours (greedy:
    longest-first into the shortest tour). Segments are ordered by nearest
    endpoint so the bead's path stays physically connected (no teleports -
    a jump beyond the escape distance would lose the trap). Returns list of
    concatenated polyline paths (each (M,3)) and the per-tour lengths."""
    lens = [np.linalg.norm(np.diff(s, axis=0), axis=1).sum() for s in segments]
    order = np.argsort(lens)[::-1]
    tours = [[] for _ in range(n_beads)]
    tour_len = [0.0] * n_beads
    for i in order:
        b = int(np.argmin(tour_len))
        tours[b].append(segments[i])
        tour_len[b] += lens[i]
    # order each tour's segments by nearest endpoint (continuous walk)
    paths = []
    for t in tours:
        chain = [t[0]]
        rest = t[1:]
        while rest:
            tip = chain[-1][-1]
            d = [min(np.linalg.norm(s[0] - tip), np.linalg.norm(s[-1] - tip))
                 for s in rest]
            k = int(np.argmin(d))
            s = rest.pop(k)
            if np.linalg.norm(s[0] - tip) <= np.linalg.norm(s[-1] - tip):
                chain.append(s)
            else:
                chain.append(s[::-1])
        paths.append(np.concatenate(chain, axis=0))
    return paths, tour_len