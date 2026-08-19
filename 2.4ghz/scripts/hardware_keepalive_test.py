from __future__ import annotations

import time

from rkm75.frame import Frame
from rkm75.wireless.device import RKM75Wireless
from rkm75.wireless.stream import WirelessKeepalive


DURATION_SECONDS = 30.0
KEEPALIVE_FPS = 5.0
GAP_MS = 7.0


def main():
    print("=" * 78)
    print("RK-M75 2.4 GHz — CLEAN KEEPALIVE HARDWARE TEST")
    print("=" * 78)
    print()
    print(f"Keepalive FPS:       {KEEPALIVE_FPS:g}")
    print(f"Inter-report gap:    {GAP_MS:g} ms")
    print(f"Duration:            {DURATION_SECONDS:g} s")
    print("Protocol:            13 88 08")
    print("Transaction:         same RGB state repeated")
    print()

    device = RKM75Wireless(
        gap_ms=GAP_MS,
    )

    try:
        device.open()

        print("Windows HID handle opened.")
        print()

        # Deliberately use one static color.
        # This isolates keepalive behavior from animation timing.
        frame = Frame()
        frame.fill((255, 0, 0))

        print("Sending initial static red frame...")
        tx_ms = device.send_frame(frame)

        print(
            f"Initial transaction: {tx_ms:.3f} ms"
        )
        print()
        print(
            "The keyboard should now be solid red."
        )
        print()
        print(
            "Press ENTER to start the 30-second keepalive test..."
        )
        input()

        print()
        print("=" * 78)
        print("STARTING KEEPALIVE")
        print("=" * 78)

        start = time.perf_counter()

        keepalive = WirelessKeepalive(
            device,
            fps=KEEPALIVE_FPS,
        )

        sent = keepalive.run(
            duration=DURATION_SECONDS,
        )

        elapsed = time.perf_counter() - start

        print()
        print("=" * 78)
        print("KEEPALIVE TEST COMPLETE")
        print("=" * 78)
        print()
        print(f"Elapsed:              {elapsed:.3f} s")
        print(f"Keepalives sent:      {sent}")
        print(
            f"Average keepalive FPS: "
            f"{sent / elapsed:.3f}"
        )
        print()
        print("VISUAL RESULT:")
        print("  A) remained solid red")
        print("  B) went dark")
        print("  C) flashed")
        print("  D) changed color")
        print("  E) other")

    finally:
        device.close()
        print()
        print("Windows HID handle closed.")


if __name__ == "__main__":
    main()