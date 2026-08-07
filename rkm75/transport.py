from __future__ import annotations

import hid


class HidTransport:
    def __init__(self, path: bytes):
        self.device = hid.device()
        self.device.open_path(path)

    def send_feature(self, report: bytes) -> int:
        if len(report) != 520:
            raise ValueError(
                f"Expected a 520-byte Feature Report, got {len(report)} bytes."
            )

        return self.device.send_feature_report(report)

    def get_feature(self, report_id: int, length: int) -> bytes:
        return bytes(
            self.device.get_feature_report(report_id, length)
        )

    def close(self):
        self.device.close()