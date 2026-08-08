import math
import time

from rkm75 import Frame, RKM75


FPS = 33
DURATION = 30.0


def main():
    frame = Frame()

    sent = 0
    start = time.perf_counter()

    with RKM75() as kb:
     with kb.stream(fps=FPS) as stream:
            while time.perf_counter() - start < DURATION:
                elapsed = time.perf_counter() - start
                phase = (elapsed / 3.0) * 2.0 * math.pi

                red = int((math.sin(phase) + 1.0) * 127.5)
                green = int(
                    (math.sin(phase + 2.0 * math.pi / 3.0) + 1.0) * 127.5
                )
                blue = int(
                    (math.sin(phase + 4.0 * math.pi / 3.0) + 1.0) * 127.5
                )

                frame.fill((red, green, blue))
                stream.send(frame)

                sent += 1

    elapsed = time.perf_counter() - start
    actual_fps = sent / elapsed if elapsed > 0 else 0.0

    print("RK M75 RGBStream test")
    print(f"Target FPS: {FPS}")
    print(f"Duration:   {elapsed:.3f} seconds")
    print(f"Sent:       {sent}")
    print(f"Actual FPS: {actual_fps:.2f}")


if __name__ == "__main__":
    main()