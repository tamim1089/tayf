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


PACKED_SIZE_BYTES = struct.calcsize(_PACK_FMT)  # 215*4 + 8 = 868 bytes/frame, pre-compression
