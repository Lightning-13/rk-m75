from rkm75 import Frame, RKM75

frame = Frame()

frame.fill((255, 0, 0))

frame.set_key("A", (0, 255, 0))

with RKM75() as kb:
    print("Sending packet...")

    result = kb.send(frame)

    print(result)