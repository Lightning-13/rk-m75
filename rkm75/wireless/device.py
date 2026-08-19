from __future__ import annotations

from ..frame import Frame

from .discovery import discover
from .encoder import encode_frame_six_groups
from .protocol import packetize
from .transport import WirelessHidTransport


class RKM75Wireless:
    """
    RK M75 2.4 GHz wireless RGB device.

    Current supported RGB path:

        Frame
          ↓
        recovered six-group representation
          ↓
        105-byte native stream
          ↓
        13 88 08 transaction
          ↓
        wireless HID reports

    The current implementation represents the full keyboard using the
    recovered six native RGB groups. This is a validated implementation
    of the current known-good path, not a claim of complete wireless
    protocol reverse engineering.
    """

    def __init__(self, gap_ms: float = 7.0):
        if gap_ms < 0:
            raise ValueError(
                "gap_ms must not be negative."
            )

        self.gap_ms = float(gap_ms)

        self.device_info = None
        self.transport = None

        # Last complete wireless transaction.

        # Used by send_keepalive() to repeat the exact same RGB state
        # without re-encoding it.
        self._last_reports = None

    def open(self):
        """
        Discover and open the RK M75 2.4 GHz RGB HID interface.
        """
        if self.transport is not None:
            return

        self.device_info = discover()

        self.transport = WirelessHidTransport(
            self.device_info["path"],
            gap_ms=self.gap_ms,
        )

        try:
            self.transport.open()
        except Exception:
            self.transport = None
            self.device_info = None
            raise

    def _ensure_open(self):
        if self.transport is None:
            raise RuntimeError(
                "RKM75Wireless is not open."
            )

    def send_frame(self, frame: Frame) -> float:
        """
        Encode and send one RGB Frame.

        Returns:
            Total HID transaction time in milliseconds.
        """
        self._ensure_open()

        if not isinstance(frame, Frame):
            raise TypeError(
                "frame must be an rkm75.frame.Frame instance."
            )

        stream = encode_frame_six_groups(frame)
        reports = packetize(stream)

        # Keep the exact packetized transaction so it can be repeated
        # by send_keepalive().
        self._last_reports = reports

        return self.transport.send_reports(reports)

    def send_keepalive(self) -> float:
        """
        Repeat the most recently transmitted RGB transaction unchanged.

        This is the validated static RGB keepalive mechanism.

        A frame must have been transmitted first.
        """
        self._ensure_open()

        if self._last_reports is None:
            raise RuntimeError(
                "Cannot send keepalive before an RGB frame."
            )

        return self.transport.send_reports(
            self._last_reports
        )

    def close(self):
        """
        Close the wireless HID transport.
        """
        if self.transport is None:
            return

        try:
            self.transport.close()
        finally:
            self.transport = None
            self.device_info = None
            self._last_reports = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        self.close()