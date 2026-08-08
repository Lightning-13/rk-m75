import hid

VID = 0x258A
PID = 0x0148


def main():
    print(f"Looking for receiver VID=0x{VID:04X} PID=0x{PID:04X}")
    print()

    devices = hid.enumerate(VID, PID)

    if not devices:
        print("No receiver found.")
        return

    print(f"Found {len(devices)} HID device entries.\n")

    for i, d in enumerate(devices, 1):
        print(f"--- Device {i} ---")

        for key in (
            "path",
            "vendor_id",
            "product_id",
            "serial_number",
            "manufacturer_string",
            "product_string",
            "release_number",
            "interface_number",
            "usage_page",
            "usage",
        ):
            print(f"{key:22}: {d.get(key)!r}")

        print()


if __name__ == "__main__":
    main()