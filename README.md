# RK M75

An open-source Python library for controlling the RGB lighting on the Royal Kludge RK M75 keyboard without the official Windows software.

> **Project Status:** Core reverse engineering complete. RGB control, the 81-key mapping, continuous RGB control, and 33 Hz live RGB streaming have been validated on hardware. The streaming API is now implemented. Additional device support and OpenRGB/SignalRGB integration remain future work.

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
- Stream continuously changing RGB frames
- Validated smooth RGB animation at 33 Hz
- Provide a reusable `RGBStream` API
- Document the reverse-engineered protocol and firmware behavior

---

## Goals

- Control RK M75 RGB lighting from Python
- Eliminate the need for the proprietary RK Windows software
- Document the USB HID lighting protocol
- Build a reusable open-source RGB control library
- Provide a reliable real-time RGB streaming interface
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
- [x] Characterized Feature Report streaming behavior
- [x] Validated continuous RGB streaming at 33 Hz
- [x] Validated smooth changing-frame RGB animation at 33 Hz
- [x] Validated 5-minute continuous RGB streaming

## Implementation

- [x] HID device discovery
- [x] HID transport layer
- [x] Feature Report replay
- [x] Feature Report generation
- [x] RGB framebuffer abstraction
- [x] Individual key RGB control
- [x] 81-key RGB mapping
- [x] Continuous RGB keepalive
- [x] RGB streaming API
- [x] 33 Hz streaming validation
- [x] RGB animation validation
- [ ] Additional device support
- [ ] OpenRGB integration
- [ ] SignalRGB integration
- [ ] Linux support

---

# Important Firmware Behavior

The RK M75 does not permanently retain an externally supplied RGB
framebuffer after receiving a single Feature Report.

With the official RK software closed:

````text
Single Feature Report
        ↓
Requested RGB state
        ↓
~1 second
        ↓
Keyboard firmware reclaims lighting control
````

Setting the official software's lighting mode to **Off** does not prevent
this behavior. A single externally supplied RGB frame still disappears
after approximately one second.

However, continuously transmitting the same Feature Report maintains
external RGB control.

A test at 10 Hz successfully kept the keyboard red for more than one
minute.

When transmission stopped, the keyboard reclaimed the lighting state
after approximately one second.

---

# Streaming Behavior

Continuous Feature Report transmission can be used to maintain control
of the RGB framebuffer and produce live RGB animations.

The tested RK M75 successfully sustained:

```text
10 Hz   → stable
20 Hz   → stable
30 Hz   → stable
31 Hz   → stable
32 Hz   → stable
33 Hz   → stable
```

At 33 Hz, continuously changing RGB frames produced a smooth visual
animation on the keyboard.

A 5-minute continuous animation test produced:

```text
Duration:    300 seconds
Sent:        9900
Errors:      0
Actual FPS:  33.00
```

The keyboard remained visually stable throughout the test.

## Behavior Above 33 Hz

34 Hz produced a significantly different transport behavior:

```text
Target FPS: 34
Actual FPS: ~15.76

Average send time: ~63 ms
Median send time:  ~83 ms
```

Additional tests at 35 Hz and 40 Hz produced approximately 15 FPS.

An unrestricted stress test, with no FPS limiter, also settled at
approximately 15 FPS.

A changing-frame stress test produced the same behavior, showing that
the slowdown is not caused by repeatedly transmitting an unchanged RGB
frame.

The current evidence therefore shows:

> **33 Hz is the highest update rate currently validated as stable on the
> tested RK M75 under Windows. At 34 Hz, `send_feature_report()` enters a
> significantly slower blocking behavior and observed throughput drops
> to approximately 15 Hz.**

This should not currently be interpreted as a proven absolute hardware
maximum. The exact layer responsible for the behavior has not yet been
isolated.

For this reason, the current `RGBStream` implementation limits the
configured streaming rate to a maximum of 33 Hz.

---

# Streaming API

The library provides an `RGBStream` interface for continuous RGB
transmission.

Example:

```python
from rkm75 import Frame, RKM75

frame = Frame()

with RKM75() as kb:
    with kb.stream(fps=33) as stream:
        while True:
            frame.fill((255, 0, 0))
            stream.send(frame)
```

The streaming layer handles the update timing while the caller remains
responsible for generating or modifying the `Frame`.

This separation allows future applications to provide RGB frames from
external sources without needing to implement the HID timing logic
themselves.

The current implementation accepts streaming rates up to 33 Hz.

---

# Vendor Configuration and Key Mapping

The official RK Keyboard Software uses a shared configuration system for
multiple Royal Kludge keyboard models.

The main configuration file contains a large list of supported VID/PID
combinations. The RK M75 tested by this project is:

```text
VID: 0x258A
PID: 0x0163
Device: RK-M75RGB New layout
```

The device-specific keyboard layout was found under the RK software's
`Dev` directory.

Typical Windows installation path:

```text
C:\Program Files (x86)\RK Keyboard Software\Dev\<PID>\
```

For the RK M75:

```text
C:\Program Files (x86)\RK Keyboard Software\Dev\0163\
```

The device-specific configuration contains the keyboard layout and key
definitions used by the official software.

The `[KEY]` section contains the physical keyboard layout and internal
key indices. These indices correspond to the RGB framebuffer positions.

The complete 81-key mapping was extracted from this configuration and
validated against the physical keyboard.

For example:

```text
A     → LED 9
SPACE → LED 35
```

Both mappings were independently verified through hardware testing.

The complete 81-key mapping was then tested by illuminating every mapped
key, followed by a row-based color test. All mapped keys illuminated in
their expected physical positions.

The configuration reports `LayoutKeyNum=84`, but only the 81 main RGB
keyboard keys are currently mapped by the library. Additional controls,
such as the encoder, are outside the current keymap scope.

---

# Compatibility With Other RK Keyboards

The official RK configuration contains many other Royal Kludge keyboard
PIDs.

This suggests that the shared RK software and its device-specific
configuration system support a wide range of RK keyboards.

However:

> **Presence of a PID in the official configuration does not mean that
> this project supports that keyboard.**

The protocol, packet layout, framebuffer layout, key mapping, firmware
behavior, and streaming behavior have only been validated on:

```text
VID 0x258A
PID 0x0163
RK-M75RGB New layout
```

Other RK keyboards should be considered **unverified** and must be
tested independently.

The same RK software driver/configuration system may work with other
devices listed in the vendor configuration, but compatibility is not
guaranteed.

---

# Repository Layout

```text
captures/       Wireshark captures used during reverse engineering
docs/           Protocol documentation and findings
examples/       Example programs and hardware tests
json/           Exported Wireshark JSON captures
reports/        Generated analysis output
rkm75/          Python library
tests/          Unit tests
tools/          Reverse-engineering utilities
```

---

# Project Architecture

```text
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
                |    RGBStream     |
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
                +-------------------+
                | HID Feature Report|
                +-------------------+
                         |
                         v
                +------------------+
                |     RK M75       |
                +------------------+
```

`RGBStream` provides the timing layer for continuous transmission while
the existing packet and transport layers remain responsible for turning
the framebuffer into USB HID Feature Reports.

---

# Examples

Examples are numbered roughly in the order they were developed during
reverse engineering.

```text
examples/
    01_open_device.py
    02_replay_capture.py
    03_all_red.py
    04_a_green.py
    05_test_keymap.py
    06_test_keymap_rows.py
    07_keepalive.py
    08_benchmark_stream.py
    09_stress_stream.py
    10_stress_changing_frames.py
    11_animation_33hz.py
    12_stream.py
```

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

### Benchmark RGB streaming

```bash
python examples/08_benchmark_stream.py --fps 33 --duration 30
```

This measures scheduled Feature Report streaming performance.

### Stress-test the HID transport

```bash
python examples/09_stress_stream.py --duration 10
```

This removes the FPS limiter and measures the behavior of the HID
Feature Report transport when pushed continuously.

### Stress-test changing RGB frames

```bash
python examples/10_stress_changing_frames.py --duration 10
```

This continuously changes the RGB framebuffer while measuring transport
throughput.

### Test smooth 33 Hz RGB animation

```bash
python examples/11_animation_33hz.py
```

This performs a continuously changing full-frame RGB animation.

The validation version of this test runs for five minutes.

### Use the streaming API

```bash
python examples/12_stream.py
```

This demonstrates the library's `RGBStream` interface.

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

* [x] Characterize stable streaming rates
* [x] Characterize Feature Report behavior above 33 Hz
* [x] Measure effective FPS
* [x] Validate long-duration stability
* [x] Build streaming API
* [x] Validate smooth RGB animations
* [ ] Further investigate the 33/34 Hz transport boundary
* [ ] Optimize streaming implementation if possible
* [ ] Validate per-key changing-frame animations

## Future

* [ ] Additional RK keyboard models
* [ ] OpenRGB integration
* [ ] SignalRGB integration
* [ ] Linux support

---

# Protocol Summary

| Property              | Value                  |
| --------------------- | ---------------------- |
| Transport             | USB HID Feature Report |
| Vendor ID             | `0x258A`               |
| Product ID            | `0x0163`               |
| Device                | RK-M75RGB New layout   |
| Report ID             | `9`                    |
| Report Size           | `520 bytes`            |
| Interface             | `MI_01` / Interface 1  |
| Usage Page            | `0xFF02`               |
| Lighting packet type  | `0x08`                 |
| Status packet type    | `0x0B`                 |
| Validated stream rate | `33 Hz`                |

More detailed protocol information is available in:

```text
docs/protocol.md
```

Reverse-engineering observations are documented in:

```text
docs/findings.md
```

---

# Contributing

Contributions are welcome.

The core RGB control and streaming path has been validated on the RK M75,
but the internal API may continue to evolve as the streaming and device
abstraction layers are expanded.

Hardware testing is currently focused on the RK M75 with:

```text
VID 0x258A
PID 0x0163
```

Contributions involving other RK devices should include hardware and
protocol validation where possible.

---

# License

MIT

````