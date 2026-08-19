from __future__ import annotations

import time

from rkm75.frame import Frame
from rkm75.wireless.device import RKM75Wireless
from rkm75.wireless.encoder import SIX_GROUP_LAYOUT
from rkm75.wireless.protocol import (
    DYNAMIC_FPS,
    INTER_REPORT_GAP_MS,
    packetize,
    validate_transaction,
)


DURATION_SECONDS = 20.0
FPS = DYNAMIC_FPS
GAP_MS = INTER_REPORT_GAP_MS


def hsv_to_rgb(h: float, s: float = 1.0, v: float = 1.0):
    h %= 1.0

    i = int(h * 6.0)
    f = h * 6.0 - i

    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))

    i %= 6

    if i == 0:
        rgb = (v, t, p)
    elif i == 1:
        rgb = (q, v, p)
    elif i == 2:
        rgb = (p, v, t)
    elif i == 3:
        rgb = (p, q, v)
    elif i == 4:
        rgb = (t, p, v)
    else:
        rgb = (v, p, q)

    return tuple(round(x * 255) for x in rgb)


def make_frame(frame_number: int) -> Frame:
    frame = Frame()

    phase = frame_number / (FPS * 9.0)

    for group, indices in enumerate(SIX_GROUP_LAYOUT):
        color = hsv_to_rgb(
            phase + group / 6.0
        )

        for index in indices:
            frame.set_led(index, color)

    return frame


def validate_frame(frame: Frame):
    from rkm75.wireless.encoder import encode_frame_six_groups

    stream = encode_frame_six_groups(frame)
    reports = packetize(stream)

    validate_transaction(stream, reports)

    assert len(stream) == 105
    assert len(reports) == 8

    return stream, reports


def main():
    print("=" * 78)
    print("RK-M75 2.4 GHz — CLEAN LIBRARY HARDWARE SMOKE TEST")
    print("=" * 78)
    print()
    print(f"FPS:                 {FPS:g}")
    print(f"Inter-report gap:    {GAP_MS:g} ms")
    print(f"Duration:            {DURATION_SECONDS:g} s")
    print("Protocol:            13 88 08")
    print("Native stream:       105 bytes")
    print("Reports:             8 x 20 bytes")
    print()

    if FPS != DYNAMIC_FPS:
        raise RuntimeError(
            "Smoke test FPS does not match validated baseline."
        )

    if GAP_MS != INTER_REPORT_GAP_MS:
        raise RuntimeError(
            "Smoke test gap does not match validated baseline."
        )

    print("Building validation transaction...")

    frame = make_frame(0)
    stream, reports = validate_frame(frame)

    print("Native stream:       PASS")
    print("Reports:             PASS")
    print("Checksums:           PASS")
    print("Reconstruction:      PASS")
    print()

    print("Opening new wireless library transport...")

    device = RKM75Wireless(gap_ms=GAP_MS)

    try:
        device.open()

        print("Windows HID handle opened.")
        print()

        input(
            "Press ENTER to start the 20-second library test..."
        )

        print()
        print("=" * 78)
        print("STARTING")
        print("=" * 78)

        start = time.perf_counter()
        next_frame = start
        frame_number = 0
        transaction_times = []

        while True:
            now = time.perf_counter()

            if now - start >= DURATION_SECONDS:
                break

            frame = make_frame(frame_number)

            tx_ms = device.send_frame(frame)
            transaction_times.append(tx_ms)

            frame_number += 1
            next_frame += 1.0 / FPS

            remaining = next_frame - time.perf_counter()

            if remaining > 0:
                time.sleep(remaining)
            else:
                next_frame = time.perf_counter()

            if frame_number <= 5 or frame_number % 50 == 0:
                elapsed = time.perf_counter() - start

                print(
                    f"frame={frame_number:04d} "
                    f"elapsed={elapsed:7.2f}s "
                    f"tx={tx_ms:7.2f} ms"
                )

        elapsed = time.perf_counter() - start

        print()
        print("=" * 78)
        print("SMOKE TEST COMPLETE")
        print("=" * 78)

        print(f"Elapsed:              {elapsed:.3f} s")
        print(f"Frames sent:          {frame_number}")
        print(f"Average FPS:          {frame_number / elapsed:.3f}")

        if transaction_times:
            print(
                f"TX average:           "
                f"{sum(transaction_times) / len(transaction_times):.3f} ms"
            )
            print(
                f"TX minimum:           "
                f"{min(transaction_times):.3f} ms"
            )
            print(
                f"TX maximum:           "
                f"{max(transaction_times):.3f} ms"
            )

        print()
        print("VISUAL RESULT:")
        print("  A) same as known-good experiment")
        print("  B) smoother")
        print("  C) worse / jumping")
        print("  D) flashes")
        print("  E) wrong colors")
        print("  F) other")

    finally:
        device.close()
        print()
        print("Windows HID handle closed.")


if __name__ == "__main__":
    main()