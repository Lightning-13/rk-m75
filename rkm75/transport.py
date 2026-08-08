from __future__ import annotations

import hid


class HidTransport:
    def __init__(self, path: bytes):
        self.device = hid.device()
        self.device.open_path(path)
        self._closed = False

    def _ensure_open(self):
        if self._closed:
            raise RuntimeError("HID transport is closed.")

    def send_feature(self, report: bytes) -> int:
        self._ensure_open()

        if len(report) != 520:
            raise ValueError(
                f"Expected a 520-byte Feature Report, got {len(report)} bytes."
            )

        return self.device.send_feature_report(report)

    def get_feature(self, report_id: int, length: int) -> bytes:
        self._ensure_open()

        return bytes(
            self.device.get_feature_report(report_id, length)
        )

    def close(self):
        if self._closed:
            return

        self.device.close()
        self._closed = True