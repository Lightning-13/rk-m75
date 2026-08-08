import time

from rkm75 import Frame, RKM75

frame = Frame()
frame.fill((255, 0, 0))

with RKM75() as kb:
    print("Starting RGB keepalive...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            kb.send(frame)
            time.sleep(0.1)  # 10 FPS
    except KeyboardInterrupt:
        print("\nStopped.")