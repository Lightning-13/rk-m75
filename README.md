# RK M75

An open-source Python library for controlling the RGB lighting on the Royal Kludge RK M75 keyboard without the official Windows software.

> **Status:** Reverse engineered and capable of replaying RGB Feature Reports. Native packet generation is currently under development.

---

## Goals

- Control RK M75 RGB lighting from Python
- Support Windows and Linux
- Eliminate the need for the official RK software
- Document the USB HID lighting protocol
- Build a reusable open-source library

---

## Current Capabilities

The current implementation has been validated against a real RK M75 keyboard.

The library can currently:

- Discover the vendor RGB HID interface
- Open the correct HID collection
- Replay captured RGB Feature Reports
- Successfully change keyboard lighting from Python

The next milestone is generating RGB Feature Reports directly from Python without relying on captured packets.

---

## Current Status

### Reverse Engineering

- [x] Identified USB transport
- [x] Located RGB Feature Report
- [x] Confirmed Report ID `0x09`
- [x] Identified vendor HID interface
- [x] Determined Feature Report size (520 bytes)
- [x] Identified lighting packet type (`0x08`)
- [x] Identified status packet type (`0x0B`)
- [x] Located RGB framebuffer
- [x] Confirmed framebuffer updates using controlled captures
- [x] Confirmed no checksum or sequence counter in lighting packets
- [x] Confirmed vendor HID collection (`MI_01`, Usage Page `0xFF02`)
- [x] Successfully replayed a captured RGB Feature Report to the keyboard

### Implementation

- [x] HID device discovery
- [x] HID transport layer
- [x] Feature Report replay
- [x] Native packet generation
- [x] Frame abstraction
- [x] Packet builder
- [ ] Key mapping
- [ ] Animation framework
- [ ] Linux support

---

# Repository Layout

```
captures/       Wireshark captures used during reverse engineering
docs/           Protocol documentation
examples/       Example programs
reports/        Generated analysis output (ignored by Git)
rkm75/          Python library
tests/          Unit tests
tools/          Reverse-engineering utilities
```

---

# Project Architecture

```
                +----------------------+
                |     Application      |
                +----------------------+
                           |
                           v
                +----------------------+
                |        RKM75         |
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
```

---

# Development Roadmap

## Milestone 1

- [x] Discover RGB HID interface
- [x] Open HID transport

## Milestone 2

- [x] Replay captured RGB Feature Report

## Milestone 3

- [ ] Generate RGB Feature Reports directly from Python

## Milestone 4

- [ ] Control individual keys

## Milestone 5

- [ ] Complete key map
- [ ] Animation support

## Milestone 6

- [ ] Linux support
- [ ] Public API stabilization

---

# Protocol Summary

| Property | Value |
|----------|-------|
| Transport | USB HID Feature Report |
| Report ID | `0x09` |
| Feature Report Size | 520 bytes |
| Interface | `MI_01` |
| Usage Page | `0xFF02` |
| Lighting Packet | `0x08` |
| Status Packet | `0x0B` |

Detailed protocol documentation will be published under `docs/` as implementation progresses.

---

# Current Progress

The project can currently:

- Discover the correct RGB HID interface
- Open the vendor HID collection
- Send HID Feature Reports
- Replay captured RGB packets
- Successfully control keyboard lighting from Python

Current development is focused on replacing captured packets with packets generated entirely by the library.

---

# Supported Hardware

| Keyboard | Status |
|----------|--------|
| Royal Kludge RK M75 | ✅ Verified |

Support for additional Royal Kludge keyboards may be added in the future if their protocols are compatible.

---

# Contributing

Contributions are welcome.

The protocol has been reverse engineered, but the public API is still evolving. Expect internal interfaces to change until packet generation and key mapping are complete.

If you discover protocol differences on another RK keyboard, please open an issue.

---

# License

MIT