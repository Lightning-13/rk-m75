from __future__ import annotations

from .protocol import LED_COUNT, RGB_SIZE
from .keymap import KEYMAP


class Frame:
    def __init__(self):
        self._data = bytearray(LED_COUNT * RGB_SIZE)

    @staticmethod
    def _validate_color(color):
        try:
            values = tuple(color)
        except TypeError:
            raise ValueError("RGB color must contain exactly 3 values.")

        if len(values) != 3:
            raise ValueError("RGB color must contain exactly 3 values.")

        if any(isinstance(value, bool) or not isinstance(value, int)
            for value in values):
            raise ValueError("RGB values must be integers.")

        if not all(0 <= value <= 255 for value in values):
            raise ValueError("RGB values must be between 0 and 255.")

        return values

    @staticmethod
    def _validate_index(index):
        if not isinstance(index, int):
            raise TypeError("LED index must be an integer.")

        if not 0 <= index < LED_COUNT:
            raise IndexError(
                f"LED index must be between 0 and {LED_COUNT - 1}."
            )

    def fill(self, color):
        color = self._validate_color(color)

        for i in range(LED_COUNT):
            self.set_led(i, color)

    def set_led(self, index, color):
        self._validate_index(index)
        r, g, b = self._validate_color(color)

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