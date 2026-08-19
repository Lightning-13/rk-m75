"""
RK M75 2.4 GHz RGB protocol primitives.

This module describes the currently validated 13 88 XX transaction family.

The application-level RGB representation remains rkm75.Frame.
This module only handles wireless-native byte streams and HID report
packetization.
"""

from __future__ import annotations

from collections.abc import Sequence

VID = 0x258A
PID = 0x0148

USAGE_PAGE = 0xFF02
USAGE = 0x0002

REPORT_ID = 0x13
REPORT_SIZE = 20
NATIVE_PAYLOAD_SIZE = 14

TRANSACTION_PREFIX = bytes.fromhex("13 88")

# Current validated operating baseline.
DYNAMIC_FPS = 14.0
INTER_REPORT_GAP_MS = 7.0

# Current selected static keepalive baseline.
KEEPALIVE_FPS = 5.0


def report_count_for_stream(stream: bytes) -> int:
    """
    Return the number of 20-byte HID reports required for a native stream.

    Each report carries at most 14 meaningful native-data bytes.
    """
    if not isinstance(stream, bytes):
        raise TypeError("stream must be bytes.")

    if not stream:
        raise ValueError("native stream must not be empty.")

    return (
        len(stream) + NATIVE_PAYLOAD_SIZE - 1
    ) // NATIVE_PAYLOAD_SIZE


def transaction_header(report_count: int) -> bytes:
    """
    Return the 13 88 XX transaction header.

    XX is the number of reports in the transaction.
    """
    if isinstance(report_count, bool) or not isinstance(report_count, int):
        raise TypeError("report_count must be an integer.")

    if report_count <= 0:
        raise ValueError("report_count must be greater than zero.")

    if report_count > 0xFF:
        raise ValueError("report_count must fit in one byte.")

    return TRANSACTION_PREFIX + bytes((report_count,))


def checksum(report: bytes | bytearray) -> int:
    """
    Calculate the validated additive report checksum.
    """
    if len(report) != REPORT_SIZE:
        raise ValueError(
            f"Expected {REPORT_SIZE}-byte report."
        )

    return sum(report[:19]) & 0xFF


def packetize(stream: bytes) -> tuple[bytes, ...]:
    """
    Convert a native RGB byte stream into 20-byte HID reports.

    The report count is selected from the native stream length:

        ceil(len(stream) / 14)

    Each report contains:

        0..2   13 88 XX
        3      sequence number
        4      0x10 + meaningful native-data length
        5..18  native-data payload
        19     additive checksum
    """
    if not isinstance(stream, bytes):
        raise TypeError("stream must be bytes.")

    if not stream:
        raise ValueError("native stream must not be empty.")

    report_count = report_count_for_stream(stream)
    header = transaction_header(report_count)

    reports: list[bytes] = []

    for sequence in range(report_count):
        start = sequence * NATIVE_PAYLOAD_SIZE
        payload = stream[start:start + NATIVE_PAYLOAD_SIZE]

        report = bytearray(REPORT_SIZE)

        report[0:3] = header
        report[3] = sequence
        report[4] = 0x10 + len(payload)

        report[5:5 + len(payload)] = payload

        report[19] = checksum(report)

        reports.append(bytes(report))

    return tuple(reports)


def reconstruct(reports: Sequence[bytes]) -> bytes:
    """
    Reconstruct the native stream from a transaction's HID reports.
    """
    if not reports:
        raise ValueError("reports must not be empty.")

    report_count = len(reports)

    expected_header = transaction_header(report_count)

    reconstructed = bytearray()

    for sequence, report in enumerate(reports):
        if len(report) != REPORT_SIZE:
            raise ValueError(
                f"Report {sequence}: expected {REPORT_SIZE} bytes."
            )

        if report[0:3] != expected_header:
            raise ValueError(
                f"Report {sequence}: invalid transaction header."
            )

        if report[3] != sequence:
            raise ValueError(
                f"Report {sequence}: invalid sequence number."
            )

        meaningful_length = report[4] - 0x10

        if not 1 <= meaningful_length <= NATIVE_PAYLOAD_SIZE:
            raise ValueError(
                f"Report {sequence}: invalid payload length."
            )

        expected_checksum = checksum(report)

        if report[19] != expected_checksum:
            raise ValueError(
                f"Report {sequence}: checksum mismatch."
            )

        reconstructed.extend(
            report[5:5 + meaningful_length]
        )

    return bytes(reconstructed)


def validate_transaction(
    stream: bytes,
    reports: Sequence[bytes],
) -> None:
    """
    Validate packetization and exact stream reconstruction.
    """
    expected_count = report_count_for_stream(stream)

    if len(reports) != expected_count:
        raise ValueError(
            f"Expected {expected_count} reports, got {len(reports)}."
        )

    reconstructed = reconstruct(reports)

    if reconstructed != stream:
        raise ValueError(
            "Reports do not reconstruct the original native stream."
        )