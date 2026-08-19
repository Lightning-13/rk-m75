from rkm75.frame import Frame
import pytest
from rkm75.wireless.encoder import (
    SIX_GROUP_LAYOUT,
    encode_frame_six_groups,
    frame_to_six_groups,
)
from rkm75.wireless.encoder import (
    TWELVE_GROUP_LAYOUT,
    encode_frame_twelve_groups,
    frame_to_twelve_groups,
)
from rkm75.wireless.protocol import packetize, reconstruct

def test_six_group_layout_has_81_unique_leds():
    indices = [
        index
        for group in SIX_GROUP_LAYOUT
        for index in group
    ]

    assert len(indices) == 81
    assert len(set(indices)) == 81


def test_frame_to_six_groups_preserves_group_colors():
    frame = Frame()

    colors = (
        (255, 0, 0),
        (255, 128, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 128, 255),
        (128, 0, 255),
    )

    for color, indices in zip(colors, SIX_GROUP_LAYOUT):
        for index in indices:
            frame.set_led(index, color)

    groups = frame_to_six_groups(frame)

    assert len(groups) == 6

    for expected_color, expected_indices, group in zip(
        colors,
        SIX_GROUP_LAYOUT,
        groups,
    ):
        assert group.color == expected_color
        assert group.led_indices == expected_indices


def test_frame_six_group_encoding_is_105_bytes():
    frame = Frame()

    colors = (
        (255, 0, 0),
        (255, 128, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 128, 255),
        (128, 0, 255),
    )

    for color, indices in zip(colors, SIX_GROUP_LAYOUT):
        for index in indices:
            frame.set_led(index, color)

    stream = encode_frame_six_groups(frame)

    assert len(stream) == 105


def test_frame_six_group_rejects_mixed_group_colors():
    frame = Frame()

    first_group = SIX_GROUP_LAYOUT[0]

    frame.set_led(first_group[0], (255, 0, 0))
    frame.set_led(first_group[1], (0, 255, 0))

    for index in first_group[2:]:
        frame.set_led(index, (255, 0, 0))

    for group in SIX_GROUP_LAYOUT[1:]:
        for index in group:
            frame.set_led(index, (0, 0, 255))

    try:
        frame_to_six_groups(frame)
    except ValueError as exc:
        assert "without losing per-LED RGB information" in str(exc)
    else:
        raise AssertionError(
            "Mixed native-group colors should be rejected."
        )

def test_frame_to_wireless_reports_end_to_end():
    frame = Frame()

    colors = (
        (255, 0, 0),
        (255, 128, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 128, 255),
        (128, 0, 255),
    )

    for color, indices in zip(colors, SIX_GROUP_LAYOUT):
        for index in indices:
            frame.set_led(index, color)

    stream = encode_frame_six_groups(frame)
    reports = packetize(stream)

    assert len(stream) == 105
    assert len(reports) == 8
    assert all(
        report[:3] == bytes.fromhex("13 88 08")
        for report in reports
    )

    assert reconstruct(reports) == stream

def test_twelve_group_layout_has_81_unique_leds():
    flattened = [
        index
        for group in TWELVE_GROUP_LAYOUT
        for index in group
    ]

    assert len(TWELVE_GROUP_LAYOUT) == 12
    assert tuple(len(group) for group in TWELVE_GROUP_LAYOUT) == (
        7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6
    )
    assert len(flattened) == 81
    assert len(set(flattened)) == 81


def test_frame_to_twelve_groups_preserves_group_colors():
    colors = (
        (255, 0, 0),
        (255, 64, 0),
        (255, 128, 0),
        (255, 255, 0),
        (128, 255, 0),
        (0, 255, 0),
        (0, 255, 128),
        (0, 255, 255),
        (0, 128, 255),
        (0, 0, 255),
        (128, 0, 255),
        (255, 0, 255),
    )

    frame = Frame()

    for color, indices in zip(colors, TWELVE_GROUP_LAYOUT):
        for index in indices:
            frame.set_led(index, color)

    groups = frame_to_twelve_groups(frame)

    assert len(groups) == 12

    for group, expected_color, expected_indices in zip(
        groups,
        colors,
        TWELVE_GROUP_LAYOUT,
    ):
        assert group.color == expected_color
        assert group.led_indices == expected_indices


def test_frame_twelve_group_encoding_is_129_bytes():
    colors = (
        (255, 0, 0),
        (255, 64, 0),
        (255, 128, 0),
        (255, 255, 0),
        (128, 255, 0),
        (0, 255, 0),
        (0, 255, 128),
        (0, 255, 255),
        (0, 128, 255),
        (0, 0, 255),
        (128, 0, 255),
        (255, 0, 255),
    )

    frame = Frame()

    for color, indices in zip(colors, TWELVE_GROUP_LAYOUT):
        for index in indices:
            frame.set_led(index, color)

    stream = encode_frame_twelve_groups(frame)

    assert len(stream) == 129


def test_frame_twelve_group_encoding_matches_captured_stream():
    colors = (
        (255, 0, 0),
        (255, 64, 0),
        (255, 128, 0),
        (255, 255, 0),
        (128, 255, 0),
        (0, 255, 0),
        (0, 255, 128),
        (0, 255, 255),
        (0, 128, 255),
        (0, 0, 255),
        (128, 0, 255),
        (255, 0, 255),
    )

    frame = Frame()

    for color, indices in zip(colors, TWELVE_GROUP_LAYOUT):
        for index in indices:
            frame.set_led(index, color)

    expected = bytes.fromhex(
        """
        ff 00 00 07 00 4e 3d 2c 1b 10 0b
        ff 40 00 07 0c 54 43 32 21 16 11
        ff 80 00 07 12 01 49 38 27 1c 23
        ff ff 00 07 18 07 4f 3e 2d 22 35
        80 ff 00 07 1e 0d 5b 44 33 28 3b
        00 ff 00 07 24 13 02 4a 39 2e 41
        00 ff 80 07 2a 19 08 50 3f 34 53
        00 ff ff 07 30 1f 0e 5c 45 3a 59
        00 80 ff 07 36 25 14 03 51 40 5f
        00 00 ff 06 3c 2b 1a 09 52 5d
        80 00 ff 06 42 31 20 0f 04 58
        ff 00 ff 06 48 37 26 15 0a 05
        """
    )

    assert encode_frame_twelve_groups(frame) == expected


def test_frame_twelve_group_encoding_rejects_mixed_group_colors():
    frame = Frame()

    indices = TWELVE_GROUP_LAYOUT[0]

    for index in indices[:-1]:
        frame.set_led(index, (255, 0, 0))

    frame.set_led(indices[-1], (0, 255, 0))

    with pytest.raises(ValueError):
        encode_frame_twelve_groups(frame)