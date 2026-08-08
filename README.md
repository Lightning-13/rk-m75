# RK M75

An open-source Python library for controlling the RGB lighting on the Royal Kludge RK M75 keyboard without the official Windows software.

> **Project Status:** Core reverse engineering complete. RGB control and the 81-key mapping have been validated on hardware. Streaming performance and additional device support are still being investigated.

---

## Features

- Discover the RK M75 RGB HID interface
- Communicate through USB HID Feature Reports
- Generate RGB Feature Reports entirely from Python
- Control the RGB framebuffer
- Address individual keyboard keys
- Complete validated 81-key RGB mapping
- Replay captured vendor Feature Reports
- Maintain RGB control through continuous Feature Report transmission
- Document the reverse-engineered protocol

---

## Goals

- Control RK M75 RGB lighting from Python
- Eliminate the need for the proprietary RK Windows software
- Document the USB HID lighting protocol
- Build a reusable open-source RGB control library
- Eventually support integration with projects such as OpenRGB and SignalRGB

Linux support is currently untested and is not an immediate development priority.

---

# Current Status

## Reverse Engineering

- [x] Identified USB transport
- [x] Located RGB Feature Report
- [x] Confirmed Report ID `9`
- [x] Identified Feature Report size (`520` bytes)
- [x] Identified vendor HID interface
- [x] Identified vendor HID collection (`MI_01`)
- [x] Identified Usage Page `0xFF02`
- [x] Identified lighting packet type (`0x08`)
- [x] Identified status packet type (`0x0B`)
- [x] Located RGB framebuffer
- [x] Confirmed framebuffer updates through controlled captures
- [x] Confirmed no checksum or sequence counter in lighting packets
- [x] Confirmed RGB Feature Report replay
- [x] Confirmed RGB Feature Report generation from Python
- [x] Located vendor keyboard layout configuration
- [x] Derived the 81-key RGB mapping from the vendor configuration
- [x] Validated all 81 RGB key positions on hardware
- [x] Confirmed firmware lighting takeover after external updates stop
- [x] Confirmed continuous RGB control at 10 Hz

## Implementation

- [x] HID device discovery
- [x] HID transport layer
- [x] Feature Report replay
- [x] Feature Report generation
- [x] RGB framebuffer abstraction
- [x] Individual key RGB control
- [x] 81-key RGB mapping
- [x] Continuous RGB keepalive
- [ ] Streaming API
- [ ] Animations
- [ ] Additional device support
- [ ] Linux support

---

# Important Firmware Behavior

The RK M75 does not permanently retain an externally supplied RGB framebuffer after receiving a single Feature Report.

With the official RK software closed:

Single Feature Report
        ↓
Requested RGB state
        ↓
~1 second
        ↓
Keyboard firmware reclaims lighting control.

Setting the official software's lighting mode to **Off** does not prevent this behavior. A single externally supplied RGB frame still disappears after approximately one second.

However, continuously transmitting the same Feature Report maintains external RGB control.

A test at 10 Hz successfully kept the keyboard red for more than one minute.

When transmission stopped, the keyboard reclaimed the lighting state after approximately one second.

The minimum required update frequency and maximum stable update rate have not yet been determined.

---

# Vendor Configuration and Key Mapping

The official RK Keyboard Software uses a shared configuration system for multiple Royal Kludge keyboard models.

The main configuration file contains a large list of supported VID/PID combinations. The RK M75 tested by this project is:

VID: 0x258A
PID: 0x0163
Device: RK-M75RGB New layout

The device-specific keyboard layout was found under the RK software's `Dev` directory.

Typical Windows installation path:

C:\Program Files (x86)\RK Keyboard Software\Dev\<PID>\

For the RK M75:

C:\Program Files (x86)\RK Keyboard Software\Dev\0163\

The device-specific configuration contains the keyboard layout and key definitions used by the official software.

The `[KEY]` section contains the physical keyboard layout and internal key indices. These indices correspond to the RGB framebuffer positions.

The complete 81-key mapping was extracted from this configuration and validated against the physical keyboard.

For example:

A     → LED 9
SPACE → LED 35

Both mappings were independently verified through hardware testing.

The complete 81-key mapping was then tested by illuminating every mapped key, followed by a row-based color test. All mapped keys illuminated in their expected physical positions.

The configuration reports `LayoutKeyNum=84`, but only the 81 main RGB keyboard keys are currently mapped by the library. Additional controls, such as the encoder, are outside the current keymap scope.

---

# Compatibility With Other RK Keyboards

The official RK configuration contains many other Royal Kludge keyboard PIDs.

This suggests that the shared RK software and its device-specific configuration system support a wide range of RK keyboards.

However:

> **Presence of a PID in the official configuration does not mean that this project supports that keyboard.**

The protocol, packet layout, framebuffer layout, key mapping, and firmware behavior have only been validated on:

VID 0x258A
PID 0x0163
RK-M75RGB New layout

Other RK keyboards should be considered **unverified** and must be tested independently.

---

# Repository Layout

captures/       Wireshark captures used during reverse engineering
docs/           Protocol documentation and findings
examples/       Example programs and hardware tests
json/           Exported Wireshark JSON captures
reports/        Generated analysis output
rkm75/          Python library
tests/          Unit tests
tools/          Reverse-engineering utilities

---

# Project Architecture

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
                |    Framebuffer   |
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
                         |
                         v
                +------------------+
                |     RK M75       |
                +------------------+

---

# Examples

Examples are numbered roughly in the order they were developed during reverse engineering.

examples/
    01_open_device.py
    02_replay_capture.py
    03_all_red.py
    04_a_green.py
    05_test_keymap.py
    06_test_keymap_rows.py
    07_keepalive.py

### Open the device

```bash
python examples/01_open_device.py
```

### Replay a captured report

```bash
python examples/02_replay_capture.py
```

### Generate an all-red frame

```bash
python examples/03_all_red.py
```

### Control an individual key

```bash
python examples/04_a_green.py
```

### Validate the complete keymap

```bash
python examples/05_test_keymap.py
```

### Validate key positions by row

```bash
python examples/06_test_keymap_rows.py
```

### Maintain continuous RGB control

```bash
python examples/07_keepalive.py
```

The keepalive example currently transmits at 10 Hz.

---

# Development Roadmap

## Milestone 1 — HID Discovery

* [x] Discover RGB HID interface
* [x] Open transport

## Milestone 2 — Feature Report Replay

* [x] Capture vendor RGB Feature Report
* [x] Extract report
* [x] Replay report successfully

## Milestone 3 — Packet Generation

* [x] Reconstruct Feature Report structure
* [x] Generate RGB Feature Reports from Python
* [x] Send generated RGB frames successfully

## Milestone 4 — Key Mapping

* [x] Locate vendor keyboard layout
* [x] Derive 81-key RGB mapping
* [x] Implement logical key API
* [x] Validate all 81 RGB positions
* [x] Document firmware takeover behavior
* [x] Validate 10 Hz continuous control

## Milestone 5 — Live Streaming

* [ ] Determine minimum stable update rate
* [ ] Determine maximum stable update rate
* [ ] Measure effective FPS
* [ ] Measure long-duration stability
* [ ] Build streaming API
* [ ] Develop RGB animations

## Future

* [ ] Additional RK keyboard models
* [ ] OpenRGB integration
* [ ] SignalRGB integration
* [ ] Linux support

---

# Protocol Summary

| Property             | Value                  |
| -------------------- | ---------------------- |
| Transport            | USB HID Feature Report |
| Vendor ID            | `0x258A`               |
| Product ID           | `0x0163`               |
| Device               | RK-M75RGB New layout   |
| Report ID            | `9`                    |
| Report Size          | `520 bytes`            |
| Interface            | `MI_01` / Interface 1  |
| Usage Page           | `0xFF02`               |
| Lighting packet type | `0x08`                 |
| Status packet type   | `0x0B`                 |

More detailed protocol information is available in:

`docs/protocol.md`

Reverse-engineering observations are documented in:

`docs/findings.md`

---

# Contributing

Contributions are welcome.

The internal API is still evolving while the streaming and device abstraction layers are being developed.

Hardware testing is currently focused on the RK M75 with:

VID 0x258A
PID 0x0163

Contributions involving other RK devices should include hardware and protocol validation where possible.

---

# License

MIT