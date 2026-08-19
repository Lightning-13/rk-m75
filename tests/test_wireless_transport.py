from rkm75.wireless.protocol import REPORT_SIZE
from rkm75.wireless.transport import WirelessHidTransport


def test_wireless_transport_requires_open():
    transport = WirelessHidTransport(
        path=b"dummy",
        gap_ms=7.0,
    )

    try:
        transport.send_report(bytes(REPORT_SIZE))
    except RuntimeError as exc:
        assert "closed" in str(exc).lower()
    else:
        raise AssertionError(
            "Closed transport should reject sends."
        )


def test_wireless_transport_rejects_wrong_report_size():
    transport = WirelessHidTransport(
        path=b"dummy",
        gap_ms=7.0,
    )

    # We only need to get past the open-state check for this
    # validation test. No actual HID call should occur because
    # report-size validation happens first.
    transport._closed = False
    transport._handle = object()

    try:
        transport.send_report(bytes(REPORT_SIZE - 1))
    except ValueError as exc:
        assert "20-byte" in str(exc)
    else:
        raise AssertionError(
            "Invalid report size should be rejected."
        )

    transport._handle = None
    transport._closed = True