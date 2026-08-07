from __future__ import annotations

from .protocol import HEADER
from .protocol import PADDING_SIZE


class Packet:

    def __init__(self, frame):

        self.frame = frame

    def to_bytes(self):

        return (

            HEADER

            + self.frame.bytes

            + bytes(PADDING_SIZE)

        )

    def save(self, filename):
        from pathlib import Path

        Path(filename).write_bytes(
            self.to_bytes()
        )