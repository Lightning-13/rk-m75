"""
Offline validation of the cleaned 13 88 08 implementation.

Run from the repository root:

    python 2.4ghz/scripts/validate_native_13_88_08.py

This does not touch the keyboard.
"""

from pathlib import Path
import sys

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))

from rkm75_wireless.protocol import (  # noqa: E402
    GROUP_COUNT,
    LED_COUNT,
    NATIVE_STREAM_SIZE,
    REPORT_COUNT,
    REPORT_SIZE,
    encode_groups,
    packetize,
    validate_led_groups,
    validate_transaction,
)


def main():
    validate_led_groups()

    colors = (
        (255, 0, 0),
        (255, 128, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 128, 255),
        (180, 0, 255),
    )

    stream = encode_groups(colors)
    reports = packetize(stream)
    validate_transaction(stream, reports)

    assert len(stream) == NATIVE_STREAM_SIZE
    assert len(reports) == REPORT_COUNT
    assert all(len(report) == REPORT_SIZE for report in reports)

    print("RK-M75 2.4 GHz 13 88 08 validation")
    print("----------------------------------")
    print(f"Groups:          {GROUP_COUNT} PASS")
    print(f"LED entries:     {LED_COUNT} PASS")
    print(f"Native stream:   {len(stream)} bytes PASS")
    print(f"Reports:         {len(reports)} x {REPORT_SIZE} bytes PASS")
    print("Checksums:       PASS")
    print("Reconstruction:  PASS")


if __name__ == "__main__":
    main()
