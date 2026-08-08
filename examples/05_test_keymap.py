from rkm75 import Frame, RKM75
from rkm75.keymap import KEYMAP

frame = Frame()

for key in KEYMAP:
    frame.set_key(key, (255, 0, 0))

print(f"Testing {len(KEYMAP)} mapped keys")

with RKM75() as kb:
    kb.send(frame)

input("Press Enter to exit...")