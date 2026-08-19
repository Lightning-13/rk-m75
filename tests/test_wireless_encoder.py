from rkm75.frame import Frame
from rkm75.wireless.encoder import (
    SIX_GROUP_LAYOUT,
    encode_frame_six_groups,
    frame_to_six_groups,
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