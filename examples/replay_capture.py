from pathlib import Path

from rkm75 import RKM75


def main():
    packet = Path("captures/report9.bin").read_bytes()

    print(f"Loaded {len(packet)} bytes")

    with RKM75() as kb:
        print("Sending Feature Report...")

        written = kb.send_feature_report(packet)

        print(f"send_feature_report() returned: {written}")


if __name__ == "__main__":
    main()