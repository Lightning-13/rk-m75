import math
import time

from rkm75 import Frame, RKM75
from rkm75.keymap import KEYMAP


EXPECTED_VID = 0x258A
EXPECTED_PID = 0x0163

STREAM_FPS = 33
STREAM_DURATION = 10.0

KEEPALIVE_FPS = 10
KEEPALIVE_DURATION = 10.0
KEEPALIVE_INTERVAL = 1.0 / KEEPALIVE_FPS


def print_header():
    print()
    print("=" * 50)
    print("RK M75 Community Tester")
    print("=" * 50)
    print()
    print(f"Expected VID: 0x{EXPECTED_VID:04X}")
    print(f"Expected PID: 0x{EXPECTED_PID:04X}")
    print()


def device_test():
    print()
    print("[1] Device detection")
    print("-" * 30)

    try:
        with RKM75():
            pass
    except Exception as exc:
        print("FAIL")
        print()
        print("Could not open the RK M75 RGB HID interface.")
        print(f"Error: {exc}")
        return False

    print("PASS")
    print("RK M75 RGB HID interface detected.")
    return True


def static_rgb_test():
    print()
    print("[2] Static RGB")
    print("-" * 30)

    print("The keyboard should turn solid red.")
    print("Press Enter to send the test frame.")
    input("> ")

    frame = Frame()
    frame.fill((255, 0, 0))

    try:
        with RKM75() as kb:
            result = kb.send(frame)
    except Exception as exc:
        print("FAIL")
        print(f"Error: {exc}")
        return False

    print(f"send() returned: {result}")
    print()
    print("Did the keyboard turn solid red?")
    answer = input("[y/N]: ").strip().lower()

    if answer == "y":
        print("PASS")
        return True

    print("FAIL")
    return False


def keymap_test():
    print()
    print("[3] 81-key mapping")
    print("-" * 30)

    key_count = len(KEYMAP)

    print(f"This test will check {key_count} mapped keys.")
    print()
    print("Each key will be illuminated individually.")
    print("Check that the highlighted key is the correct physical key.")
    print()
    print("Press Enter to begin.")
    input("> ")

    frame = Frame()
    passed = 0

    try:
        with RKM75() as kb:
            for number, key in enumerate(KEYMAP, start=1):
                frame.fill((0, 0, 0))
                frame.set_key(key, (255, 0, 0))

                kb.send(frame)

                print(
                    f"[{number:02d}/{key_count}] "
                    f"{key:<16} -> LED {KEYMAP[key]}"
                )

                while True:
                    answer = input("Correct? [Y/n/q]: ").strip().lower()

                    if answer in ("y", "n", "q"):
                        break

                    print("Please enter y, n, or q.")

                if answer == "q":
                    print()
                    print("Keymap test cancelled.")
                    return None, passed

                if answer == "n":
                    print()
                    print(f"FAIL: {key}")
                    print(
                        "The highlighted key did not match "
                        "the expected key."
                    )
                    return False, passed

                passed += 1

    except KeyboardInterrupt:
        print()
        print("Cancelled.")
        return None, passed

    except Exception as exc:
        print("FAIL")
        print(f"Error: {exc}")
        return False, passed

    print()
    print("PASS")
    print(f"All {passed} mapped keys were confirmed.")

    return True, passed


def keepalive_test():
    print()
    print("[4] 10 Hz keepalive")
    print("-" * 30)

    print(
        "The keyboard will be held solid red for "
        f"{KEEPALIVE_DURATION:.0f} seconds using "
        f"{KEEPALIVE_FPS} Hz updates."
    )
    print()
    print("Press Enter to begin.")
    input("> ")

    frame = Frame()
    frame.fill((255, 0, 0))

    sent = 0
    start = time.perf_counter()

    try:
        with RKM75() as kb:
            while time.perf_counter() - start < KEEPALIVE_DURATION:
                kb.send(frame)
                sent += 1
                time.sleep(KEEPALIVE_INTERVAL)

    except KeyboardInterrupt:
        print()
        print("Cancelled.")
        return None, sent, 0.0

    except Exception as exc:
        print("FAIL")
        print(f"Error: {exc}")
        return False, sent, 0.0

    elapsed = time.perf_counter() - start

    print()
    print(f"Sent:     {sent}")
    print(f"Duration: {elapsed:.2f} seconds")
    print()
    print("Did the keyboard remain solid red for the entire test?")
    answer = input("[y/N]: ").strip().lower()

    if answer == "y":
        print("PASS")
        return True, sent, elapsed

    print("FAIL")
    return False, sent, elapsed


def streaming_test():
    print()
    print("[5] 33 Hz RGB streaming")
    print("-" * 30)

    print(
        "The keyboard will display a continuously changing "
        f"RGB animation at {STREAM_FPS} Hz."
    )
    print(f"Test duration: {STREAM_DURATION:.0f} seconds")
    print()
    print("Press Enter to begin.")
    input("> ")

    frame = Frame()
    sent = 0
    start = time.perf_counter()

    try:
        with RKM75() as kb:
            with kb.stream(fps=STREAM_FPS) as stream:
                while time.perf_counter() - start < STREAM_DURATION:
                    elapsed = time.perf_counter() - start
                    phase = (elapsed / 3.0) * 2.0 * math.pi

                    red = int(
                        (math.sin(phase) + 1.0) * 127.5
                    )

                    green = int(
                        (
                            math.sin(
                                phase + 2.0 * math.pi / 3.0
                            )
                            + 1.0
                        )
                        * 127.5
                    )

                    blue = int(
                        (
                            math.sin(
                                phase + 4.0 * math.pi / 3.0
                            )
                            + 1.0
                        )
                        * 127.5
                    )

                    frame.fill((red, green, blue))
                    stream.send(frame)
                    sent += 1

    except KeyboardInterrupt:
        print()
        print("Cancelled.")
        return None, sent, 0.0, 0.0

    except Exception as exc:
        print("FAIL")
        print(f"Error: {exc}")
        return False, sent, 0.0, 0.0

    elapsed = time.perf_counter() - start
    actual_fps = sent / elapsed if elapsed > 0 else 0.0

    print()
    print(f"Target FPS: {STREAM_FPS}")
    print(f"Duration:   {elapsed:.3f} seconds")
    print(f"Sent:       {sent}")
    print(f"Actual FPS: {actual_fps:.2f}")
    print()

    print("Was the animation smooth and free of visible errors?")
    answer = input("[y/N]: ").strip().lower()

    if answer == "y":
        print("PASS")
        return True, sent, elapsed, actual_fps

    print("FAIL")
    return False, sent, elapsed, actual_fps


def run_all():
    results = {}

    results["Device detection"] = device_test()

    if results["Device detection"] is not True:
        print()
        print("Device detection failed.")
        print("The remaining tests cannot be run.")
        return results

    results["Static RGB"] = static_rgb_test()

    keymap_result, keymap_passed = keymap_test()
    results["81-key mapping"] = keymap_result
    results["81-key mapping count"] = keymap_passed

    keepalive_result, keepalive_sent, keepalive_elapsed = (
        keepalive_test()
    )
    results["10 Hz keepalive"] = keepalive_result
    results["10 Hz keepalive sent"] = keepalive_sent
    results["10 Hz keepalive duration"] = keepalive_elapsed

    stream_result, stream_sent, stream_elapsed, stream_fps = (
        streaming_test()
    )
    results["33 Hz streaming"] = stream_result
    results["33 Hz streaming sent"] = stream_sent
    results["33 Hz streaming duration"] = stream_elapsed
    results["33 Hz streaming actual FPS"] = stream_fps

    return results


def status_text(result):
    if result is True:
        return "PASS"

    if result is False:
        return "FAIL"

    return "SKIPPED"


def print_summary(results):
    print()
    print("=" * 50)
    print("RK M75 Community Test Report")
    print("=" * 50)
    print()

    print(f"VID: 0x{EXPECTED_VID:04X}")
    print(f"PID: 0x{EXPECTED_PID:04X}")
    print()

    print(
        f"Device detection: "
        f"{status_text(results.get('Device detection'))}"
    )

    print(
        f"Static RGB:       "
        f"{status_text(results.get('Static RGB'))}"
    )

    keymap_status = status_text(results.get("81-key mapping"))
    keymap_count = results.get("81-key mapping count", 0)

    print(
        f"81-key mapping:   {keymap_status} "
        f"({keymap_count}/{len(KEYMAP)})"
    )

    keepalive_status = status_text(
        results.get("10 Hz keepalive")
    )

    print(
        f"10 Hz keepalive:  {keepalive_status}"
    )

    stream_status = status_text(
        results.get("33 Hz streaming")
    )

    stream_sent = results.get(
        "33 Hz streaming sent",
        0,
    )

    actual_fps = results.get(
        "33 Hz streaming actual FPS",
        0.0,
    )

    if stream_status == "PASS":
        print(
            f"33 Hz streaming:  PASS "
            f"({stream_sent} frames, {actual_fps:.2f} FPS)"
        )
    else:
        print(
            f"33 Hz streaming:  {stream_status}"
        )

    print()
    print("Copy the report above when reporting results.")
    print()


def run_single(name, function):
    result = function()

    if isinstance(result, tuple):
        if name == "81-key mapping":
            value, passed = result
            results = {
                name: value,
                "81-key mapping count": passed,
            }

        elif name == "10 Hz keepalive":
            value, sent, elapsed = result
            results = {
                name: value,
                "10 Hz keepalive sent": sent,
                "10 Hz keepalive duration": elapsed,
            }

        elif name == "33 Hz streaming":
            value, sent, elapsed, actual_fps = result
            results = {
                name: value,
                "33 Hz streaming sent": sent,
                "33 Hz streaming duration": elapsed,
                "33 Hz streaming actual FPS": actual_fps,
            }

        else:
            results = {name: result}

    else:
        results = {name: result}

    print_summary(results)


def main():
    print_header()

    try:
        while True:
            print("Choose a test:")
            print()
            print("1. Device detection")
            print("2. Static RGB")
            print("3. 81-key mapping")
            print("4. 10 Hz keepalive")
            print("5. 33 Hz streaming")
            print("A. Run all tests")
            print("Q. Quit")
            print()

            choice = input("> ").strip().lower()

            if choice == "q":
                print()
                print("Goodbye.")
                return

            if choice == "a":
                results = run_all()
                print_summary(results)
                return

            tests = {
                "1": ("Device detection", device_test),
                "2": ("Static RGB", static_rgb_test),
                "3": ("81-key mapping", keymap_test),
                "4": ("10 Hz keepalive", keepalive_test),
                "5": ("33 Hz streaming", streaming_test),
            }

            if choice not in tests:
                print()
                print("Invalid selection.")
                print()
                continue

            name, function = tests[choice]

            try:
                run_single(name, function)
            except KeyboardInterrupt:
                print()
                print()
                print("Test cancelled.")
                print()

    except KeyboardInterrupt:
        print()
        print()
        print("Tester stopped.")
        print()


if __name__ == "__main__":
    main()