"""
RK M75 2.4 GHz — experimental 13 88 0A hardware test.

Sends the exact 12-group color pattern recovered from the
19_per_key_unique_colors.pcapng capture.

This test deliberately keeps the HID connection open after each
transaction so that the keyboard has time to react.

The 13 88 08 path remains the currently validated production path.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[2]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from rkm75 import Frame  # noqa: E402
from rkm75.wireless import (  # noqa: E402
    RKM75Wireless,
    TWELVE_GROUP_LAYOUT,
)


COLORS = (
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


def make_frame() -> Frame:
    """Build the exact 12-color frame used by the capture experiment."""
    frame = Frame()

    for color, indices in zip(COLORS, TWELVE_GROUP_LAYOUT):
        for index in indices:
            frame.set_led(index, color)

    return frame


def send_and_report(device: RKM75Wireless, frame: Frame, label: str):
    print()
    print("-" * 78)
    print(label)
    print("-" * 78)

    started = time.perf_counter()

    tx_ms = device.send_frame_twelve_groups(frame)

    elapsed_ms = (time.perf_counter() - started) * 1000.0

    print(f"Transaction time:    {tx_ms:.3f} ms")
    print(f"Host elapsed:        {elapsed_ms:.3f} ms")
    print("Connection remains open.")
    print()


def main():
    print("=" * 78)
    print("RK M75 2.4 GHz — EXPERIMENTAL 13 88 0A OBSERVATION TEST")
    print("=" * 78)
    print()
    print("Native stream:       129 bytes")
    print("Reports:             10 x 20 bytes")
    print("Groups:              12")
    print("LED entries:         81")
    print("Inter-report gap:    7 ms")
    print()
    print(
        "Pattern: exact 12-color pattern recovered from "
        "19_per_key_unique_colors.pcapng."
    )
    print()
    print("This test intentionally keeps the HID connection open.")
    print("It sends the frame twice with a 5-second observation window.")
    print()
    print("Do not close the keyboard software while this test is running.")
    print()

    frame = make_frame()

    with RKM75Wireless(gap_ms=7.0) as device:
        print("Windows HID handle opened.")
        print()

        input(
            "Press ENTER to send the first 13 88 0A transaction..."
        )

        send_and_report(
            device,
            frame,
            "FIRST TRANSACTION",
        )

        print("Observe the keyboard for 5 seconds.")
        print("Do not press anything.")
        time.sleep(5.0)

        input(
            "Press ENTER to send the second 13 88 0A transaction..."
        )

        send_and_report(
            device,
            frame,
            "SECOND TRANSACTION",
        )

        print("Observe the keyboard for another 5 seconds.")
        time.sleep(5.0)

        print()
        print("=" * 78)
        print("OBSERVATION COMPLETE")
        print("=" * 78)
        print()
        print("VISUAL RESULT:")
        print("  A) exact / full keyboard")
        print("  B) partial keyboard")
        print("  C) wrong colors")
        print("  D) flashes / takeover")
        print("  E) nothing")
        print("  F) other")
        print()

        input(
            "Press ENTER to close the wireless HID connection..."
        )

    print()
    print("Windows HID handle closed.")


if __name__ == "__main__":
    main()