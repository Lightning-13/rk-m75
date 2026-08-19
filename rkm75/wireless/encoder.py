from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence

from ..frame import Frame


RGB = tuple[int, int, int]


# Exact 81-LED partition recovered from the validated 13 88 08 captures.
#
# These are native LED-map indices, not physical key names.
SIX_GROUP_LAYOUT = (
    (
        0x00, 0x0C, 0x12, 0x18, 0x1E, 0x24, 0x2A,
        0x30, 0x36, 0x3C, 0x42, 0x48, 0x4E, 0x54,
    ),
    (
        0x01, 0x07, 0x0D, 0x13, 0x19, 0x1F, 0x25,
        0x2B, 0x31, 0x37, 0x3D, 0x43, 0x49, 0x4F, 0x5B,
    ),
    (
        0x02, 0x08, 0x0E, 0x14, 0x1A, 0x20, 0x26,
        0x2C, 0x32, 0x38, 0x3E, 0x44, 0x4A, 0x50, 0x5C,
    ),
    (
        0x03, 0x09, 0x0F, 0x15, 0x1B, 0x21, 0x27,
        0x2D, 0x33, 0x39, 0x3F, 0x45, 0x51, 0x5D,
    ),
    (
        0x04, 0x0A, 0x10, 0x16, 0x1C, 0x22, 0x28,
        0x2E, 0x34, 0x3A, 0x40, 0x52, 0x58,
    ),
    (
        0x05, 0x0B, 0x11, 0x23, 0x35, 0x3B, 0x41,
        0x53, 0x59, 0x5F,
    ),
)


# Exact 81-LED partition recovered from the captured 13 88 0A transaction.
#
# These are native LED-map indices, not physical key names.
#
# The grouping was recovered by assigning a deterministic 12-color pattern
# through the official software and reconstructing the resulting 129-byte
# native stream.
TWELVE_GROUP_LAYOUT = (
    (
        0x00, 0x4E, 0x3D, 0x2C, 0x1B, 0x10, 0x0B,
    ),
    (
        0x0C, 0x54, 0x43, 0x32, 0x21, 0x16, 0x11,
    ),
    (
        0x12, 0x01, 0x49, 0x38, 0x27, 0x1C, 0x23,
    ),
    (
        0x18, 0x07, 0x4F, 0x3E, 0x2D, 0x22, 0x35,
    ),
    (
        0x1E, 0x0D, 0x5B, 0x44, 0x33, 0x28, 0x3B,
    ),
    (
        0x24, 0x13, 0x02, 0x4A, 0x39, 0x2E, 0x41,
    ),
    (
        0x2A, 0x19, 0x08, 0x50, 0x3F, 0x34, 0x53,
    ),
    (
        0x30, 0x1F, 0x0E, 0x5C, 0x45, 0x3A, 0x59,
    ),
    (
        0x36, 0x25, 0x14, 0x03, 0x51, 0x40, 0x5F,
    ),
    (
        0x3C, 0x2B, 0x1A, 0x09, 0x52, 0x5D,
    ),
    (
        0x42, 0x31, 0x20, 0x0F, 0x04, 0x58,
    ),
    (
        0x48, 0x37, 0x26, 0x15, 0x0A, 0x05,
    ),
)


@dataclass(frozen=True)
class NativeGroup:
    """One RGB + LED-index record in the recovered wireless format."""

    color: RGB
    led_indices: tuple[int, ...]

    def __post_init__(self):
        if len(self.color) != 3:
            raise ValueError(
                "RGB color must contain exactly 3 values."
            )

        if any(
            isinstance(value, bool) or not isinstance(value, int)
            for value in self.color
        ):
            raise ValueError("RGB values must be integers.")

        if not all(0 <= value <= 255 for value in self.color):
            raise ValueError(
                "RGB values must be between 0 and 255."
            )

        if not self.led_indices:
            raise ValueError(
                "Native group must contain at least one LED."
            )

        for index in self.led_indices:
            if isinstance(index, bool) or not isinstance(index, int):
                raise ValueError(
                    "LED indices must be integers."
                )

            if not 0 <= index <= 255:
                raise ValueError(
                    "LED indices must fit in one byte."
                )


def encode_native_groups(
    groups: Sequence[NativeGroup],
) -> bytes:
    """
    Encode native RGB groups into the wireless native byte stream.

    Each group is:

        RGB       3 bytes
        LED count 1 byte
        LED indices N bytes
    """
    if not groups:
        raise ValueError(
            "At least one native group is required."
        )

    stream = bytearray()

    for group in groups:
        if not isinstance(group, NativeGroup):
            raise TypeError(
                "groups must contain NativeGroup instances."
            )

        if len(group.led_indices) > 255:
            raise ValueError(
                "A native group cannot contain more than 255 LEDs."
            )

        stream.extend(group.color)
        stream.append(len(group.led_indices))
        stream.extend(group.led_indices)

    return bytes(stream)


def _frame_to_groups(
    frame: Frame,
    layout,
    layout_name: str,
) -> tuple[NativeGroup, ...]:
    if not isinstance(frame, Frame):
        raise TypeError(
            "frame must be an rkm75.frame.Frame instance."
        )

    data = frame.bytes
    groups = []

    for led_indices in layout:
        colors = {
            tuple(
                data[index * 3:index * 3 + 3]
            )
            for index in led_indices
        }

        if len(colors) != 1:
            raise ValueError(
                f"Frame cannot be represented by the {layout_name} "
                "wireless layout without losing per-LED RGB information."
            )

        groups.append(
            NativeGroup(
                color=next(iter(colors)),
                led_indices=led_indices,
            )
        )

    return tuple(groups)


def frame_to_six_groups(
    frame: Frame,
) -> tuple[NativeGroup, ...]:
    """
    Convert a Frame to the recovered six-group representation.

    Every LED in a native group must currently have the same RGB value.
    """
    return _frame_to_groups(
        frame,
        SIX_GROUP_LAYOUT,
        "six-group",
    )


def encode_frame_six_groups(frame: Frame) -> bytes:
    """
    Encode a Frame using the currently hardware-validated
    six-group 13 88 08 format.
    """
    return encode_native_groups(
        frame_to_six_groups(frame)
    )


def frame_to_twelve_groups(
    frame: Frame,
) -> tuple[NativeGroup, ...]:
    """
    Convert a Frame to the recovered twelve-group 13 88 0A
    representation.

    This is currently experimental. Each recovered native group must
    have one uniform RGB color.
    """
    return _frame_to_groups(
        frame,
        TWELVE_GROUP_LAYOUT,
        "twelve-group",
    )


def encode_frame_twelve_groups(frame: Frame) -> bytes:
    """
    Encode a Frame using the captured 13 88 0A twelve-group format.

    The resulting 129-byte stream packetizes automatically into
    ten 20-byte reports because each report carries at most 14
    native-data bytes.
    """
    stream = encode_native_groups(
        frame_to_twelve_groups(frame)
    )

    if len(stream) != 129:
        raise ValueError(
            f"Expected 129-byte 13 88 0A stream, got {len(stream)}."
        )

    return stream