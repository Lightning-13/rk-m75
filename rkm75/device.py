from __future__ import annotations

from .discovery import discover
from .transport import HidTransport


class RKM75:
    def __init__(self):
        self.device_info = discover()
        self.transport = HidTransport(self.device_info["path"])

    def send_feature_report(self, data: bytes) -> int:
        return self.transport.send_feature(data)

    def close(self):
        self.transport.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()