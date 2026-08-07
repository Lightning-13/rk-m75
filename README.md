# RK M75

An open-source Python library for controlling the RGB lighting on the Royal Kludge RK M75 keyboard without the official Windows software.

> **Project Status:** Reverse engineering complete. Implementation in progress.

---

## Goals

- Control RK M75 RGB lighting from Python
- Support Windows and Linux
- Eliminate the need for the RK proprietary software
- Document the USB HID lighting protocol
- Build a reusable open-source library

---

## Current Status

### Reverse Engineering

- [x] Identified USB transport
- [x] Located RGB Feature Report
- [x] Confirmed Report ID 9
- [x] Identified vendor HID interface
- [x] Determined Feature Report size (520 bytes)
- [x] Identified lighting packet type (`0x08`)
- [x] Identified status packet type (`0x0B`)
- [x] Located RGB framebuffer
- [x] Confirmed framebuffer updates via controlled captures
- [x] Confirmed no checksum or sequence counter in lighting packets
- [x] Confirmed vendor HID collection (`MI_01`, `Usage Page 0xFF02`)

### Implementation

- [x] HID device discovery
- [x] Transport layer
- [ ] Feature report replay
- [ ] Packet builder
- [ ] Framebuffer abstraction
- [ ] Key mapping
- [ ] Animations
- [ ] Linux support

---

# Repository Layout

```
captures/       Wireshark captures used during reverse engineering
docs/           Protocol documentation (work in progress)
examples/       Example programs
json/           Exported Wireshark JSON captures
reports/        Generated analysis output (ignored by Git)
rkm75/          Python library
tests/          Unit tests
tools/          Reverse-engineering utilities
```

---

# Project Architecture

```
                +------------------+
                |    Application   |
                +------------------+
                         |
                         v
                +------------------+
                |      RKM75       |
                +------------------+
                         |
                         v
                +------------------+
                |   Packet Builder |
                +------------------+
                         |
                         v
                +------------------+
                |    Transport     |
                +------------------+
                         |
                         v
                +------------------+
                | HID Feature Report|
                +------------------+
```

---

# Development Roadmap

## Milestone 1

- [x] Discover RGB HID interface
- [x] Open transport

## Milestone 2

- [ ] Replay captured Feature Report

## Milestone 3

- [ ] Generate Feature Reports from Python

## Milestone 4

- [ ] Control individual keys

## Milestone 5

- [ ] Complete key map

## Milestone 6

- [ ] Linux support

---

# Protocol Summary

| Property | Value |
|----------|------|
| Transport | USB HID Feature Report |
| Report ID | 9 |
| Report Size | 520 bytes |
| Interface | MI_01 |
| Usage Page | 0xFF02 |

More detailed protocol documentation will be added under `docs/` once the implementation has been validated by the hardware.

---

# Current Progress

The project can currently:

- Discover the vendor HID interface
- Open the RGB HID collection
- Prepare the transport layer for Feature Report communication

The next milestone is replaying a captured RGB packet to the keyboard.

---

# Contributing

Contributions are welcome once the protocol implementation stabilizes.

Until then, expect rapid changes to the internal API.

---

# License

MIT