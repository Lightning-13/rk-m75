from rkm75 import Frame, RKM75
from rkm75.keymap import KEYMAP

# Each physical row gets a different color.
ROWS = {
    "function": {
        "keys": [
            "ESC", "F1", "F2", "F3", "F4", "F5", "F6",
            "F7", "F8", "F9", "F10", "F11", "F12",
            "DELETE",
        ],
        "color": (255, 0, 0),       # Red
    },

    "number": {
        "keys": [
            "GRAVE", "1", "2", "3", "4", "5", "6",
            "7", "8", "9", "0", "MINUS", "EQUAL",
            "BACKSPACE", "HOME",
        ],
        "color": (0, 255, 0),       # Green
    },

    "qwerty": {
        "keys": [
            "TAB", "Q", "W", "E", "R", "T", "Y",
            "U", "I", "O", "P", "LEFT_BRACKET",
            "RIGHT_BRACKET", "BACKSLASH", "PAGE_UP",
        ],
        "color": (0, 0, 255),       # Blue
    },

    "home": {
        "keys": [
            "CAPS_LOCK", "A", "S", "D", "F", "G", "H",
            "J", "K", "L", "SEMICOLON", "APOSTROPHE",
            "ENTER",
        ],
        "color": (255, 255, 0),     # Yellow
    },

    "bottom": {
        "keys": [
            "LEFT_SHIFT", "Z", "X", "C", "V", "B", "N",
            "M", "COMMA", "PERIOD", "SLASH", "RIGHT_SHIFT",
            "UP",
        ],
        "color": (255, 0, 255),     # Magenta
    },

    "space": {
        "keys": [
            "LEFT_CTRL", "LEFT_WIN", "LEFT_ALT", "SPACE",
            "RIGHT_ALT", "FN", "RIGHT_CTRL",
            "LEFT", "DOWN", "RIGHT", "PAGE_DOWN",
        ],
        "color": (0, 255, 255),     # Cyan
    },
}


frame = Frame()

tested = set()

for row in ROWS.values():
    for key in row["keys"]:
        if key not in KEYMAP:
            raise KeyError(f"{key!r} is missing from KEYMAP")

        frame.set_key(key, row["color"])
        tested.add(key)

print(f"Testing {len(tested)} mapped keys across {len(ROWS)} rows")

with RKM75() as kb:
    print("Sending row test...")
    result = kb.send(frame)
    print("send() returned:", result)

input("Press Enter to exit...")