from pathlib import Path

hex_dump = Path("captures/report9.hex").read_text()

hex_bytes = []

for line in hex_dump.splitlines():

    if not line.strip():
        continue

    parts = line.split()

    # Skip offset
    hex_bytes.extend(parts[1:])

data = bytes.fromhex("".join(hex_bytes))

print("Length:", len(data))

assert len(data) == 520

Path("captures/report9.bin").write_bytes(data)

print("Saved report9.bin")