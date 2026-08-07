# RK M75 USB HID Protocol

This document describes the USB HID protocol used by the Royal Kludge RK M75 for RGB lighting control.

---

# Device Information

| Property | Value |
|----------|-------|
| Vendor ID | `0x258A` |
| Product ID | `0x0163` |
| Manufacturer | SINO WEALTH |
| Product | Gaming KB |
| Interface | `MI_01` |
| Usage Page | `0xFF02` |
| Usage | `0x0001` |

The RGB interface is exposed as a vendor-defined HID collection.

---

# Transport

Lighting updates are sent using USB HID Feature Reports.

| Property | Value |
|----------|-------|
| Request | SET_REPORT |
| Report Type | Feature Report |
| Report ID | `0x09` |
| Report Size | 520 bytes |

No interrupt OUT endpoint is used.

---

# Feature Report Layout

```
+--------+----------------------+-------------+
| Header | RGB Framebuffer      | Padding     |
+--------+----------------------+-------------+
| 8 B    | 378 B                | 134 B       |
+--------+----------------------+-------------+
```

Total report size:

```
520 bytes
```

---

# Header

The first eight bytes are constant for lighting packets.

```
09 08 00 00 01 00 7A 01
```

| Offset | Value | Description |
|--------|------|-------------|
| 0 | `0x09` | Report ID |
| 1 | `0x08` | Lighting packet |
| 2-3 | `0x0000` | Reserved |
| 4 | `0x01` | Constant |
| 5 | `0x00` | Reserved |
| 6-7 | `0x017A` | Payload length (378 bytes) |

---

# RGB Framebuffer

The framebuffer begins immediately after the header.

Offset:

```
8
```

Length:

```
378 bytes
```

Entries:

```
126 RGB slots
```

Each entry consists of three bytes.

```
R G B
```

Example:

```
FF 00 00
```

represents red.

---

# Packet Types

## 0x08

Lighting update.

Contains the RGB framebuffer.

---

## 0x0B

Status packet.

Observed periodically while the official software is running.

The purpose of the payload has not yet been determined.

---

# Padding

The remaining bytes after the framebuffer are zero.

They are ignored by the keyboard.

---

# Validation

The protocol has been validated by:

- Replaying captured Feature Reports.
- Generating Feature Reports entirely from Python.
- Successfully controlling keyboard lighting on hardware.

---

# Current Limitations

The protocol described here currently applies only to the Royal Kludge RK M75.

Compatibility with other Royal Kludge keyboards has not yet been investigated.