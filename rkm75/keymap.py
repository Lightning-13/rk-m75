"""RK M75 logical key -> RGB LED index mapping."""

KEYMAP = {
    # Function / navigation row
    "ESC": 0,
    "F1": 12,
    "F2": 18,
    "F3": 24,
    "F4": 30,
    "F5": 36,
    "F6": 42,
    "F7": 48,
    "F8": 54,
    "F9": 60,
    "F10": 66,
    "F11": 72,
    "F12": 78,
    "DELETE": 84,

    # Number row
    "GRAVE": 1,
    "1": 7,
    "2": 13,
    "3": 19,
    "4": 25,
    "5": 31,
    "6": 37,
    "7": 43,
    "8": 49,
    "9": 55,
    "0": 61,
    "MINUS": 67,
    "EQUAL": 73,
    "BACKSPACE": 79,
    "HOME": 91,

    # QWERTY row
    "TAB": 2,
    "Q": 8,
    "W": 14,
    "E": 20,
    "R": 26,
    "T": 32,
    "Y": 38,
    "U": 44,
    "I": 50,
    "O": 56,
    "P": 62,
    "LEFT_BRACKET": 68,
    "RIGHT_BRACKET": 74,
    "BACKSLASH": 80,
    "PAGE_UP": 92,

    # Home row
    "CAPS_LOCK": 3,
    "A": 9,
    "S": 15,
    "D": 21,
    "F": 27,
    "G": 33,
    "H": 39,
    "J": 45,
    "K": 51,
    "L": 57,
    "SEMICOLON": 63,
    "APOSTROPHE": 69,
    "ENTER": 81,

    # Bottom letter row
    "LEFT_SHIFT": 4,
    "Z": 10,
    "X": 16,
    "C": 22,
    "V": 28,
    "B": 34,
    "N": 40,
    "M": 46,
    "COMMA": 52,
    "PERIOD": 58,
    "SLASH": 64,
    "RIGHT_SHIFT": 82,
    "UP": 88,

    # Bottom row
    "LEFT_CTRL": 5,
    "LEFT_WIN": 11,
    "LEFT_ALT": 17,
    "SPACE": 35,
    "RIGHT_ALT": 53,
    "FN": 59,
    "RIGHT_CTRL": 65,
    "LEFT": 83,
    "DOWN": 89,
    "RIGHT": 95,
    "PAGE_DOWN": 93,
}


def get_led_index(key: str) -> int:
    """Return the RGB LED index for a logical key name."""
    try:
        return KEYMAP[key.upper()]
    except KeyError:
        raise KeyError(f"Unknown key: {key!r}") from None