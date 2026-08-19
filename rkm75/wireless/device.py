from __future__ import annotations

from ..frame import Frame

from .discovery import discover
from .encoder import (
    encode_frame_six_groups,
    encode_frame_twelve_groups,
)
from .protocol import packetize
from .transport import WirelessHidTransport


class RKM75Wireless:
    """
    RK M75 2.4 GHz RGB device.

    Supported RGB paths currently under investigation:

        Frame
        -> recovered RGB group representation
        -> native RGB stream
        -> 13 88 XX transaction
        -> wireless HID reports

    The six-group 13 88 08 path is the currently validated baseline.

    The twelve-group 13 88 0A path has also been reproduced on
    hardware and is currently experimental.

    The most recently transmitted RGB transaction is retained so that
    the exact same HID reports can be retransmitted by send_keepalive().
    """

    def __init__(self, gap_ms: float = 7.0):
        if gap_ms < 0:
            raise ValueError("gap_ms must not be negative.")

        self.gap_ms = gap_ms
        self.device_info = None
        self.transport = None

        # Exact HID reports from the most recent RGB transaction.
        #
        # Keepalive retransmits these reports without re-encoding the
        # Frame or changing the transaction contents.
        self._last_reports = None

    def open(self):
        """Open the RK M75 wireless HID RGB interface."""
        if self.transport is not None:
            return

        self.device_info = discover()

        self.transport = WirelessHidTransport(
            self.device_info["path"],
            gap_ms=self.gap_ms,
        )

        self.transport.open()

    def _ensure_open(self):
        """Raise if the wireless device has not been opened."""
        if self.transport is None:
            raise RuntimeError(
                "RKM75Wireless is not open."
            )

    def send_frame(self, frame: Frame) -> float:
        """
        Encode and send one Frame using the validated six-group path.

        The resulting reports are retained for keepalive retransmission.

        Returns:
            Total HID transaction time in milliseconds.
        """
        self._ensure_open()

        stream = encode_frame_six_groups(frame)
        reports = packetize(stream)

        self._last_reports = reports

        return self.transport.send_reports(reports)

    def send_frame_twelve_groups(self, frame: Frame) -> float:
        """
        Encode and send one Frame using the experimental twelve-group
        13 88 0A path.

        The resulting ten reports are retained so the exact same
        transaction can subsequently be retransmitted by
        send_keepalive().

        Returns:
            Total HID transaction time in milliseconds.
        """
        self._ensure_open()

        stream = encode_frame_twelve_groups(frame)
        reports = packetize(stream)

        if len(reports) != 10:
            raise RuntimeError(
                f"Expected 10 reports for 13 88 0A, "
                f"got {len(reports)}."
            )

        self._last_reports = reports

        return self.transport.send_reports(reports)

    def send_keepalive(self) -> float:
        """
        Retransmit the exact most recently transmitted RGB transaction.

        The keepalive does not construct a new RGB packet and does not
        re-encode the Frame. It sends the exact same HID report sequence
        that was produced by the last send_frame() or
        send_frame_twelve_groups() call.

        Returns:
            Total HID transaction time in milliseconds.
        """
        self._ensure_open()

        if self._last_reports is None:
            raise RuntimeError(
                "Cannot send keepalive before an RGB transaction "
                "has been transmitted."
            )

        return self.transport.send_reports(self._last_reports)

    def close(self):
        """Close the wireless HID interface."""
        if self.transport is None:
            return

        self.transport.close()
        self.transport = None
        self.device_info = None
        self._last_reports = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()