from rkm75.device import RKM75

def main():
    kb = RKM75()

    print("✓ Opened RGB HID interface")
    print(f"Path: {kb.info['path'].decode()}")

    kb.close()

if __name__ == "__main__":
    main()