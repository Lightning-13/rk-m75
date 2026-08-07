from __future__ import annotations

from .discovery import discover
from .transport import HidTransport


class RKM75:

    def __init__(self):

        self.device_info = discover()

        self.transport = HidTransport(

            self.device_info["path"]

        )

    def close(self):

        self.transport.close()

    def __enter__(self):

        return self

    def __exit__(

        self,

        exc_type,

        exc,

        tb,

    ):

        self.close()