from __future__ import annotations

from .protocol import LED_COUNT, RGB_SIZE
from .keymap import KEYMAP


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

    def set_key(self, key: str, color):
        key = key.upper()

        try:
            index = KEYMAP[key]
        except KeyError:
            raise KeyError(f"Unknown key '{key}'")

        self.set_led(index, color)

    @property
    def bytes(self):
        return bytes(self._data)