# Reverse Engineering Findings

This document records experimentally verified observations made during reverse engineering.

Only findings confirmed through packet captures or hardware testing are included.

---

# USB Transport

## Confirmed

- RGB communication uses USB HID Feature Reports.
- Lighting updates use Report ID `0x09`.
- Reports are sent through the vendor HID interface (`MI_01`).
- Usage Page is `0xFF02`.

---

# Packet Structure

## Confirmed

- Feature Report size is exactly 520 bytes.
- Lighting packets begin with an 8-byte header.
- RGB framebuffer begins at byte offset 8.
- Framebuffer size is 378 bytes.
- Framebuffer contains 126 RGB entries.
- Remaining bytes are zero padding.

---

# Packet Types

## Lighting Packet

Subtype:

```
0x08
```

Contains RGB framebuffer data.

---

## Status Packet

Subtype:

```
0x0B
```

Observed periodically while the official software is running.

Purpose currently unknown.

---

# RGB Encoding

Each LED entry consists of three bytes.

```
Red
Green
Blue
```

Example:

```
FF 00 00
```

Red.

---

# Validation

## Replay

Captured Feature Reports can be replayed successfully.

The keyboard immediately updates its lighting.

---

## Native Packet Generation

Packets generated entirely from Python are accepted by the keyboard.

No captured packets are required.

---

# Checksum

No checksum has been observed.

No sequence counter has been observed.

Only RGB bytes change between lighting updates.

---

# Keep-Alive Behaviour

The official software continuously broadcasts the current lighting state.

Repeated packets are not required for successful updates.

A single lighting packet is sufficient.

---

# Verified Key Mapping

| Key | LED Index |
|------|----------:|
| A | 9 |
| Space | 35 |

Only experimentally verified mappings are listed.

---

# Remaining Work

- Complete key mapping.
- Decode the `0x0B` status packet.
- Investigate compatibility with additional Royal Kludge keyboards.