from pathlib import Path

src = Path("captures/report9.hex")
dst = Path("captures/report9.bin")

hex_bytes = []

for line in src.read_text().splitlines():
    line = line.strip()

    if not line:
        continue

    parts = line.split()

    # Skip the offset column (0000, 0010, ...)
    hex_bytes.extend(parts[1:])

data = bytes.fromhex("".join(hex_bytes))

print(f"Extracted {len(data)} bytes")

assert len(data) == 520, f"Expected 520 bytes, got {len(data)}"

dst.write_bytes(data)

print(f"Saved {dst}")