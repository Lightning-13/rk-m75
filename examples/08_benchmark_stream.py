import argparse
import statistics
import time

from rkm75 import Frame, RKM75


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark RK M75 RGB Feature Report streaming."
    )

    parser.add_argument(
        "--fps",
        type=float,
        default=10.0,
        help="Target update rate in frames per second.",
    )

    parser.add_argument(
        "--duration",
        type=float,
        default=30.0,
        help="Benchmark duration in seconds.",
    )

    args = parser.parse_args()

    if args.fps <= 0:
        raise ValueError("FPS must be greater than 0.")

    if args.duration <= 0:
        raise ValueError("Duration must be greater than 0.")

    interval = 1.0 / args.fps

    frame = Frame()
    frame.fill((255, 0, 0))

    sent = 0
    errors = 0
    send_times = []

    print("RK M75 RGB streaming benchmark")
    print(f"Target FPS: {args.fps:g}")
    print(f"Duration:   {args.duration:g} seconds")
    print()

    with RKM75() as kb:
        start = time.perf_counter()
        next_send = start

        while True:
            now = time.perf_counter()

            if now - start >= args.duration:
                break

            if now < next_send:
                time.sleep(next_send - now)
                continue

            send_start = time.perf_counter()

            try:
                kb.send(frame)
                sent += 1

                send_time = time.perf_counter() - send_start
                send_times.append(send_time)

            except Exception as exc:
                errors += 1
                print(f"Send failed: {exc}")

            next_send += interval

    elapsed = time.perf_counter() - start
    actual_fps = sent / elapsed if elapsed > 0 else 0.0

    print()
    print("Benchmark complete")
    print(f"Elapsed:    {elapsed:.3f} seconds")
    print(f"Sent:       {sent}")
    print(f"Errors:     {errors}")
    print(f"Actual FPS: {actual_fps:.2f}")

    if send_times:
        send_ms = [value * 1000 for value in send_times]

        print()
        print("send_feature_report() timing")
        print(f"Average:    {statistics.mean(send_ms):.3f} ms")
        print(f"Minimum:    {min(send_ms):.3f} ms")
        print(f"Maximum:    {max(send_ms):.3f} ms")
        print(f"Median:     {statistics.median(send_ms):.3f} ms")


if __name__ == "__main__":
    main()