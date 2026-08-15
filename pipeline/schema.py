"""
TAYF driving-parameter wire format.

Grounded in Mon3tr (arXiv 2601.07518), the closest published reference
architecture: body pose (75) + facial expression (50) + hand pose (90)
= 215 floats/frame, measured end-to-end at <0.2 Mbps / ~80ms over WebRTC.

This is the packet shared between pipeline/capture (producer) and
pipeline/avatar (consumer on the receiving cube). Both sides must import
this module rather than redefine the packet shape independently.
"""

from dataclasses import dataclass, field, fields
import struct

BODY_POSE_DIM = 75      # SMPL-family joint rotation parameters
FACE_EXPRESSION_DIM = 50  # blendshape/expression coefficients
HAND_POSE_DIM = 90      # 45 per hand (MANO-style), both hands
TOTAL_DIM = BODY_POSE_DIM + FACE_EXPRESSION_DIM + HAND_POSE_DIM  # 215

_PACK_FMT = f"<{TOTAL_DIM}f d"  # 215 float32 + 1 float64 timestamp


@dataclass
class DrivingState:
    """One frame of driving parameters for a TAYF avatar."""

    body_pose: tuple = field(default_factory=lambda: (0.0,) * BODY_POSE_DIM)
    face_expression: tuple = field(default_factory=lambda: (0.0,) * FACE_EXPRESSION_DIM)
    hand_pose: tuple = field(default_factory=lambda: (0.0,) * HAND_POSE_DIM)
    timestamp: float = 0.0

    def __post_init__(self):
        if len(self.body_pose) != BODY_POSE_DIM:
            raise ValueError(f"body_pose must have {BODY_POSE_DIM} values, got {len(self.body_pose)}")
        if len(self.face_expression) != FACE_EXPRESSION_DIM:
            raise ValueError(f"face_expression must have {FACE_EXPRESSION_DIM} values, got {len(self.face_expression)}")
        if len(self.hand_pose) != HAND_POSE_DIM:
            raise ValueError(f"hand_pose must have {HAND_POSE_DIM} values, got {len(self.hand_pose)}")

    def pack(self) -> bytes:
        """Serialize to a fixed-size binary frame (pre-FP16/LZ4 compression, see pipeline/transport)."""
        values = (*self.body_pose, *self.face_expression, *self.hand_pose, self.timestamp)
        return struct.pack(_PACK_FMT, *values)

    @classmethod
    def unpack(cls, data: bytes) -> "DrivingState":
        values = struct.unpack(_PACK_FMT, data)
        *floats, timestamp = values
        return cls(
            body_pose=tuple(floats[:BODY_POSE_DIM]),
            face_expression=tuple(floats[BODY_POSE_DIM:BODY_POSE_DIM + FACE_EXPRESSION_DIM]),
            hand_pose=tuple(floats[BODY_POSE_DIM + FACE_EXPRESSION_DIM:]),
            timestamp=timestamp,
        )


PACKED_SIZE_BYTES = struct.calcsize(_PACK_FMT)  # 215*4 + 8 = 868 bytes/frame


# ----------------------------------------------------------------------
# Wire encoding — MEASURED, see docs/10_TAYF_UNIVERSAL_ENGINEERING.md §3.4
# ----------------------------------------------------------------------
#
# The original spec was fp16 + LZ4, assuming a 0.6x compression ratio.
# That assumption was tested and is WRONG: packed pose floats are high
# entropy, so a general-purpose compressor finds nothing to exploit and
# *expands* the payload by ~2.6%.
#
#     fp16 absolute      430 B/frame   0.206 Mbps @60fps
#     fp16 + zlib        441 B/frame   0.212 Mbps   <- worse than raw
#     delta + int8       215 B/frame   0.104 Mbps   <- USE THIS
#     delta + int8 + zlib 226 B/frame  0.109 Mbps   <- compressor hurts again
#
# Quantisation error is DELTA_RANGE/254 rad (half a step). At the 0.35 rad
# bound below that is 1.4 mrad = 284 arcsec = 0.079 deg, which displaces the
# end of a 0.5 m limb by 0.7 mm -- invisible. Tightening DELTA_RANGE to the
# measured motion envelope reduces it proportionally.
#
# Delta chains break on packet loss, so send an absolute keyframe
# periodically; at 1 Hz the amortised cost is negligible (~0.105 Mbps all-in).

DELTA_SCALE = 1.0 / 127.0      # int8 quantisation step, in units of DELTA_RANGE
DELTA_RANGE = 0.35             # rad; max per-frame joint change at 60 fps [ESTIMATE]
KEYFRAME_INTERVAL_S = 1.0      # absolute frame cadence for loss recovery


def encode_delta(cur: "DrivingState", ref: "DrivingState") -> bytes:
    """Quantise (cur - ref) to one signed byte per parameter. 215 bytes."""
    a = (*cur.body_pose, *cur.face_expression, *cur.hand_pose)
    b = (*ref.body_pose, *ref.face_expression, *ref.hand_pose)
    step = DELTA_RANGE * DELTA_SCALE
    return bytes(
        max(-127, min(127, int(round((x - y) / step)))) + 128
        for x, y in zip(a, b)
    )


def decode_delta(payload: bytes, ref: "DrivingState", timestamp: float) -> "DrivingState":
    """Reconstruct from a delta payload. Caller must track `ref` identically."""
    if len(payload) != TOTAL_DIM:
        raise ValueError(f"delta payload must be {TOTAL_DIM} bytes, got {len(payload)}")
    step = DELTA_RANGE * DELTA_SCALE
    b = (*ref.body_pose, *ref.face_expression, *ref.hand_pose)
    vals = [y + (p - 128) * step for p, y in zip(payload, b)]
    return DrivingState(
        body_pose=tuple(vals[:BODY_POSE_DIM]),
        face_expression=tuple(vals[BODY_POSE_DIM:BODY_POSE_DIM + FACE_EXPRESSION_DIM]),
        hand_pose=tuple(vals[BODY_POSE_DIM + FACE_EXPRESSION_DIM:]),
        timestamp=timestamp,
    )


DELTA_SIZE_BYTES = TOTAL_DIM   # 215 bytes/frame
