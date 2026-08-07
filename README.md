# RK M75

An open-source Python library for controlling the RGB lighting on the Royal Kludge RK M75 keyboard over USB HID without the official Windows software.

> **Status:** Reverse engineered and capable of generating RGB Feature Reports entirely from Python. Logical per-key lighting support is now under active development.

---

# Goals

- Control RK M75 RGB lighting from Python
- Support Windows and Linux
- Eliminate the need for the official RK software
- Document the USB HID lighting protocol
- Build a reusable open-source library

---

# Current Capabilities

The implementation has been validated against a real Royal Kludge RK M75 keyboard.

The library can currently:

- Discover the vendor RGB HID interface
- Open the correct HID collection
- Generate RGB Feature Reports entirely from Python
- Control keyboard lighting without the official software
- Control verified individual keys through a logical API

Current development focuses on expanding the verified key map and building higher-level lighting features.

---

# Example

```python
from rkm75 import Frame, RKM75

frame = Frame()

frame.fill((255, 0, 0))
frame.set_key("A", (0, 255, 0))

with RKM75() as keyboard:
    keyboard.send(frame)
```

---

# Current Status

## Reverse Engineering

- [x] Identified USB transport
- [x] Located RGB Feature Report
- [x] Confirmed Report ID `0x09`
- [x] Identified vendor HID interface
- [x] Determined Feature Report size (520 bytes)
- [x] Identified lighting packet type (`0x08`)
- [x] Identified status packet type (`0x0B`)
- [x] Located RGB framebuffer
- [x] Confirmed framebuffer updates using controlled captures
- [x] Confirmed no checksum or sequence counter
- [x] Confirmed vendor HID collection (`MI_01`, Usage Page `0xFF02`)
- [x] Successfully replayed captured Feature Reports
- [x] Successfully generated Feature Reports entirely from Python
- [x] Verified logical key mappings (`A`, `Space`)

## Implementation

- [x] HID device discovery
- [x] HID transport layer
- [x] Feature Report replay
- [x] Native packet generation
- [x] Frame abstraction
- [x] Packet builder
- [x] Logical key API
- [ ] Complete key map
- [ ] Animation framework
- [ ] Linux support
- [ ] Public API stabilization

---

# Repository Layout

```
captures/       Wireshark captures used during reverse engineering
docs/           Protocol documentation and findings
examples/       Example programs
reports/        Generated analysis output (ignored by Git)
rkm75/          Python library
tests/          Unit tests
tools/          Reverse-engineering utilities
```

---

# Architecture

```
                +----------------------+
                |     Application      |
                +----------------------+
                           |
                           v
                +----------------------+
                |        Frame         |
                +----------------------+
                           |
                           v
                +----------------------+
                |    Packet Builder    |
                +----------------------+
                           |
                           v
                +----------------------+
                |      Transport       |
                +----------------------+
                           |
                           v
                +----------------------+
                | USB HID Feature Report|
                +----------------------+
                           |
                           v
                +----------------------+
                |       RK M75         |
                +----------------------+
```

---

# Development Roadmap

## Milestone 1

- [x] Discover RGB HID interface
- [x] Open HID transport

## Milestone 2

- [x] Replay captured RGB Feature Reports

## Milestone 3

- [x] Generate RGB Feature Reports directly from Python

## Milestone 4

- [x] Introduce logical key API
- [ ] Expand verified key map

## Milestone 5

- [ ] Animation framework

## Milestone 6

- [ ] Linux support
- [ ] Stable public API

---

# Protocol Summary

| Property | Value |
|----------|-------|
| Transport | USB HID Feature Report |
| Report ID | `0x09` |
| Report Size | 520 bytes |
| Interface | `MI_01` |
| Usage Page | `0xFF02` |
| Lighting Packet | `0x08` |
| Status Packet | `0x0B` |

Detailed protocol documentation is available under the `docs/` directory.

---

# Current Progress

The project can currently:

- Discover the RGB HID interface
- Open the vendor HID collection
- Generate valid RGB Feature Reports
- Control keyboard lighting entirely from Python
- Control verified individual keys using logical key names

Current development focuses on completing the verified key map and implementing animation support.

---

# Supported Hardware

| Keyboard | Status |
|----------|--------|
| Royal Kludge RK M75 | ✅ Verified |

Support for additional Royal Kludge keyboards may be added if compatible protocols are identified.

---

# Reverse Engineering Status

The USB HID lighting protocol has been successfully reverse engineered and validated against real hardware.

Current development is focused on improving the public API rather than discovering additional protocol details.

---

# Contributing

Contributions are welcome.

The protocol is understood, but the public API is still evolving. If you discover protocol differences on another Royal Kludge keyboard or improve the implementation, feel free to open an issue or submit a pull request.

---

# License

MIT