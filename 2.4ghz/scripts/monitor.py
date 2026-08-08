import argparse
import hid
import time


VID = 0x258A
PID = 0x0148


def find_interface(usage_page, usage):
    for device in hid.enumerate(VID, PID):
        if (
            device.get("usage_page") == usage_page
            and device.get("usage") == usage
        ):
            return device

    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--usage-page", type=lambda x: int(x, 0), required=True)
    parser.add_argument("--usage", type=lambda x: int(x, 0), required=True)
    args = parser.parse_args()

    target = find_interface(args.usage_page, args.usage)

    if target is None:
        print(
            f"Could not find "
            f"usage page 0x{args.usage_page:04X}, "
            f"usage 0x{args.usage:04X}."
        )
        return

    print("Opening:")
    print(target["path"])
    print()
    print("Listening for input reports...")
    print("Press Ctrl+C to stop.")
    print()

    dev = hid.device()
    dev.open_path(target["path"])
    dev.set_nonblocking(1)

    try:
        while True:
            data = dev.read(64)

            if data:
                print(
                    f"{time.strftime('%H:%M:%S')}  "
                    f"{len(data):2d} bytes  "
                    + " ".join(f"{b:02X}" for b in data)
                )

            time.sleep(0.001)

    except KeyboardInterrupt:
        print("\nStopped.")

    finally:
        dev.close()


if __name__ == "__main__":
    main()