from rkm75 import Frame, RKM75

frame = Frame()
frame.fill((255, 0, 0))

with RKM75() as kb:
    print("Sending generated packet...")
    result = kb.send(frame)
    print("send() returned:", result)