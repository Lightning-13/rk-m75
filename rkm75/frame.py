from __future__ import annotations

from .protocol import LED_COUNT, RGB_SIZE


class Frame:
    def __init__(self):
        self._data = bytearray(LED_COUNT * RGB_SIZE)

    def fill(self, color):
        for i in range(LED_COUNT):
            self.set_led(i, color)

    def set_led(self, index, color):
        r, g, b = color

        offset = index * RGB_SIZE

        self._data[offset] = r
        self._data[offset + 1] = g
        self._data[offset + 2] = b

    @property
    def bytes(self):
        return bytes(self._data)