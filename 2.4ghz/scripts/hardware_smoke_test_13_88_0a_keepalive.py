"""
RK M75 2.4 GHz — experimental 13 88 0A + keepalive test.

Sequence:

    1. Send the recovered 13 88 0A RGB frame.
    2. Immediately retransmit the exact same transaction at 2 FPS.
    3. Maintain the connection for 10 seconds.
    4. Observe whether the RGB state remains stable.

The 13 88 08 path is not modified by this test.
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


KEEPALIVE_FPS = 2.0
DURATION_SECONDS = 10.0


def make_frame() -> Frame:
    """Build the exact 12-color frame recovered from the capture."""
    frame = Frame()

    for color, indices in zip(COLORS, TWELVE_GROUP_LAYOUT):
        for index in indices:
            frame.set_led(index, color)

    return frame


def main():
    print("=" * 78)
    print("RK M75 2.4 GHz — 13 88 0A + KEEPALIVE TEST")
    print("=" * 78)
    print()
    print("RGB transaction:     13 88 0A")
    print("Native stream:       129 bytes")
    print("Reports:             10 x 20 bytes")
    print("RGB groups:          12")
    print("LED entries:         81")
    print()
    print("Keepalive FPS:       2")
    print("Inter-report gap:    7 ms")
    print("Keepalive duration:  10 seconds")
    print()
    print(
        "The RGB frame is the exact 12-color pattern recovered "
        "from the official-software capture."
    )
    print()
    print(
        "The keepalive retransmits the exact same 10 HID reports."
    )
    print()

    frame = make_frame()

    with RKM75Wireless(gap_ms=7.0) as device:
        print("Windows HID handle opened.")
        print()

        input(
            "Press ENTER to send 13 88 0A and start the keepalive..."
        )

        print()
        print("-" * 78)
        print("SENDING 13 88 0A")
        print("-" * 78)

        tx_start = time.perf_counter()

        tx_ms = device.send_frame_twelve_groups(frame)

        tx_elapsed = time.perf_counter() - tx_start

        print(f"Transaction time:    {tx_ms:.3f} ms")
        print(f"Host elapsed:        {tx_elapsed * 1000.0:.3f} ms")
        print()

        print("-" * 78)
        print("STARTING 2 FPS KEEPALIVE")
        print("-" * 78)
        print()

        start = time.perf_counter()
        next_tick = start
        sent = 0

        while True:
            now = time.perf_counter()

            if now - start >= DURATION_SECONDS:
                break

            keepalive_start = time.perf_counter()

            device.send_keepalive()

            keepalive_ms = (
                time.perf_counter() - keepalive_start
            ) * 1000.0

            sent += 1

            print(
                f"Keepalive {sent:02d}: "
                f"{keepalive_ms:.3f} ms"
            )

            next_tick += 1.0 / KEEPALIVE_FPS

            remaining = next_tick - time.perf_counter()

            if remaining > 0:
                time.sleep(remaining)
            else:
                next_tick = time.perf_counter()

        elapsed = time.perf_counter() - start

        print()
        print("-" * 78)
        print("KEEPALIVE COMPLETE")
        print("-" * 78)
        print()
        print(f"Elapsed:             {elapsed:.3f} s")
        print(f"Keepalives sent:     {sent}")
        print(f"Average rate:        {sent / elapsed:.3f} FPS")
        print()
        print("VISUAL RESULT:")
        print("  A) 12-color pattern remained continuously visible")
        print("  B) pattern appeared, then firmware took over")
        print("  C) pattern remained but flashed/jumped")
        print("  D) colors were wrong")
        print("  E) nothing happened")
        print("  F) other")
        print()

        input(
            "Press ENTER to close the wireless HID connection..."
        )

    print()
    print("Windows HID handle closed.")


if __name__ == "__main__":
    main()