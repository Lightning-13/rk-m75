import argparse
import statistics
import time

from rkm75 import Frame, RKM75


def main():
    parser = argparse.ArgumentParser(
        description="Stress-test RK M75 RGB Feature Report throughput."
    )

    parser.add_argument(
        "--duration",
        type=float,
        default=10.0,
        help="Test duration in seconds.",
    )

    args = parser.parse_args()

    if args.duration <= 0:
        raise ValueError("Duration must be greater than 0.")

    frame = Frame()
    frame.fill((255, 0, 0))

    sent = 0
    errors = 0
    send_times = []

    print("RK M75 RGB Feature Report stress test")
    print(f"Duration: {args.duration:g} seconds")
    print("Sending continuously with no FPS limiter...")
    print()

    with RKM75() as kb:
        start = time.perf_counter()

        while True:
            elapsed = time.perf_counter() - start

            if elapsed >= args.duration:
                break

            send_start = time.perf_counter()

            try:
                kb.send(frame)
                sent += 1

                send_times.append(
                    time.perf_counter() - send_start
                )

            except Exception as exc:
                errors += 1
                print(f"Send failed: {exc}")

    elapsed = time.perf_counter() - start
    actual_fps = sent / elapsed if elapsed > 0 else 0.0

    print()
    print("Stress test complete")
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