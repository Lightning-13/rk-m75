from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence

from ..frame import Frame


RGB = tuple[int, int, int]


# Exact 81-LED partition recovered from the wireless captures.
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


def frame_to_six_groups(frame: Frame) -> tuple[NativeGroup, ...]:
    """
    Convert a Frame to the recovered six-group representation.

    Every LED in a native group must currently have the same RGB value.
    This deliberately rejects arbitrary per-key RGB that cannot be
    represented by the six-group native format without information loss.
    """
    if not isinstance(frame, Frame):
        raise TypeError(
            "frame must be an rkm75.frame.Frame instance."
        )

    data = frame.bytes
    groups = []

    for led_indices in SIX_GROUP_LAYOUT:
        colors = {
            tuple(
                data[index * 3:index * 3 + 3]
            )
            for index in led_indices
        }

        if len(colors) != 1:
            raise ValueError(
                "Frame cannot be represented by the six-group "
                "wireless layout without losing per-LED RGB information."
            )

        groups.append(
            NativeGroup(
                color=next(iter(colors)),
                led_indices=led_indices,
            )
        )

    return tuple(groups)


def encode_frame_six_groups(frame: Frame) -> bytes:
    """
    Encode a Frame using the currently recovered six-group format.
    """
    return encode_native_groups(
        frame_to_six_groups(frame)
    )