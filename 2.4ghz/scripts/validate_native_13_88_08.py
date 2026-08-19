"""
Offline validation of the validated RK M75 2.4 GHz RGB path.

Run from the repository root:

    python 2.4ghz/scripts/validate_native_13_88_08.py

This does not touch the keyboard.
"""

from __future__ import annotations

import sys
from pathlib import Path


# Make the repository root importable when this script is run directly.
HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[2]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from rkm75.frame import Frame  # noqa: E402
from rkm75.wireless.encoder import (  # noqa: E402
    SIX_GROUP_LAYOUT,
    encode_frame_six_groups,
    frame_to_six_groups,
)
from rkm75.wireless.protocol import (  # noqa: E402
    NATIVE_PAYLOAD_SIZE,
    REPORT_SIZE,
    packetize,
    reconstruct,
    report_count_for_stream,
    validate_transaction,
)


EXPECTED_LED_COUNT = 81
EXPECTED_GROUP_COUNT = 6
EXPECTED_NATIVE_STREAM_SIZE = 105
EXPECTED_REPORT_COUNT = 8


def main() -> None:
    # Validate the recovered six-group topology.
    assert len(SIX_GROUP_LAYOUT) == EXPECTED_GROUP_COUNT

    flattened = [
        index
        for group in SIX_GROUP_LAYOUT
        for index in group
    ]

    assert len(flattened) == EXPECTED_LED_COUNT
    assert len(set(flattened)) == EXPECTED_LED_COUNT
    assert min(flattened) >= 0
    assert max(flattened) <= 0xFF

    # Build a Frame whose six native groups each have one uniform color.
    colors = (
        (255, 0, 0),
        (255, 128, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 128, 255),
        (180, 0, 255),
    )

    frame = Frame()

    for group_color, led_indices in zip(colors, SIX_GROUP_LAYOUT):
        for led_index in led_indices:
            frame.set_led(led_index, group_color)

    groups = frame_to_six_groups(frame)

    assert len(groups) == EXPECTED_GROUP_COUNT

    # Encode the actual application-level Frame through the real library.
    stream = encode_frame_six_groups(frame)

    assert len(stream) == EXPECTED_NATIVE_STREAM_SIZE

    # The recovered native stream should packetize into eight reports.
    reports = packetize(stream)

    assert report_count_for_stream(stream) == EXPECTED_REPORT_COUNT
    assert len(reports) == EXPECTED_REPORT_COUNT
    assert all(len(report) == REPORT_SIZE for report in reports)

    # Validate the complete transaction and exact reconstruction.
    validate_transaction(stream, reports)

    assert reconstruct(reports) == stream

    # Verify the expected native payload capacity.
    assert NATIVE_PAYLOAD_SIZE == 14

    print("RK-M75 2.4 GHz 13 88 08 validation")
    print("----------------------------------")
    print(f"Groups:          {len(groups)} PASS")
    print(f"LED entries:     {len(flattened)} PASS")
    print(f"Native stream:   {len(stream)} bytes PASS")
    print(
        f"Reports:         "
        f"{len(reports)} x {REPORT_SIZE} bytes PASS"
    )
    print("Checksums:       PASS")
    print("Reconstruction:  PASS")


if __name__ == "__main__":
    main()