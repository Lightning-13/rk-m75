from __future__ import annotations

from .discovery import discover
from .transport import HidTransport


class RKM75:
    def __init__(self):
        self.device_info = discover()
        self.transport = HidTransport(self.device_info["path"])

    # Existing method (keep this)
    def send_feature_report(self, data: bytes) -> int:
        return self.transport.send_feature(data)

    # New method
    def send(self, frame):
        from .packet import Packet

        packet = Packet(frame)

        return self.transport.send_feature(
            packet.to_bytes()
        )

    def close(self):
        self.transport.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()