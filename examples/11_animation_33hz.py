import math
import time

from rkm75 import Frame, RKM75


FPS = 33
DURATION = 300.0


def main():
    frame = Frame()

    sent = 0
    errors = 0

    interval = 1.0 / FPS

    print("RK M75 33 Hz RGB animation test")
    print(f"Duration: {DURATION:g} seconds")
    print(f"Target FPS: {FPS}")
    print()

    with RKM75() as kb:
        start = time.perf_counter()
        next_send = start

        while True:
            now = time.perf_counter()

            if now - start >= DURATION:
                break

            if now < next_send:
                time.sleep(next_send - now)
                continue

            # Smooth hue cycle.
            elapsed = now - start
            phase = (elapsed / 3.0) * 2.0 * math.pi

            red = int((math.sin(phase) + 1.0) * 127.5)
            green = int(
                (math.sin(phase + 2.0 * math.pi / 3.0) + 1.0) * 127.5
            )
            blue = int(
                (math.sin(phase + 4.0 * math.pi / 3.0) + 1.0) * 127.5
            )

            frame.fill((red, green, blue))

            try:
                kb.send(frame)
                sent += 1
            except Exception as exc:
                errors += 1
                print(f"Send failed: {exc}")

            next_send += interval

    elapsed = time.perf_counter() - start
    actual_fps = sent / elapsed if elapsed > 0 else 0.0

    print()
    print("Animation test complete")
    print(f"Elapsed:    {elapsed:.3f} seconds")
    print(f"Sent:       {sent}")
    print(f"Errors:     {errors}")
    print(f"Actual FPS: {actual_fps:.2f}")


if __name__ == "__main__":
    main()