# RK M75

An open-source Python library for controlling the RGB lighting on the Royal Kludge RK M75 keyboard without the official Windows software.

> **Project Status:** The USB wired RGB control path is complete and validated on hardware. A separate 2.4 GHz wireless RGB path is also implemented, with the currently recovered transaction family validated on hardware. Wireless protocol reverse engineering remains ongoing.

---

## Features

### USB wired RGB

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
- Validate RGB frame and streaming inputs
- Provide explicit HID transport lifecycle handling

### 2.4 GHz wireless RGB

- Discover the RK M75 2.4 GHz RGB HID interface
- Communicate through the recovered wireless HID transport
- Encode the recovered six-group RGB representation
- Generate the validated 105-byte native RGB stream
- Packetize the native stream into `13 88 XX` HID reports
- Validate report checksums and stream reconstruction
- Stream changing RGB group states
- Maintain RGB control with wireless keepalive transmission
- Hardware-validated `13 88 08` full-keyboard RGB transactions
- Hardware-validated smooth 14 FPS wireless RGB animation

### Project tooling

- Automated API and protocol regression tests
- Reverse-engineering captures and documentation
- Hardware validation scripts
- Documented protocol and firmware behavior

---

## Goals

- Control RK M75 RGB lighting from Python
- Eliminate the need for the proprietary RK Windows software
- Document the USB HID lighting protocol
- Document the recovered 2.4 GHz wireless RGB protocol
- Build a reusable open-source RGB control library
- Provide reliable real-time RGB streaming interfaces
- Eventually support integration with projects such as OpenRGB and SignalRGB

Linux support is currently untested and is not an immediate development priority.

---

# Current Status

## USB Wired RGB

The original USB RGB control path is considered complete for the tested RK M75.

### Reverse Engineering

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

### Implementation

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
- [x] Public package API
- [x] RGB frame input validation
- [x] RGBStream input validation
- [x] HID transport lifecycle handling
- [x] Automated API regression tests
- [x] Hardware regression validation
- [ ] Additional device support
- [ ] OpenRGB integration
- [ ] SignalRGB integration
- [ ] Linux support

---

## 2.4 GHz Wireless RGB

The project also contains a separate wireless RGB implementation under:

```text
rkm75/wireless/
```

The reverse-engineering workspace and supporting documentation are kept under:

```text
2.4ghz/
```

The current wireless implementation deliberately covers only the recovered and hardware-validated RGB transaction path. It should not be considered a complete reverse engineering of the RK M75 wireless protocol.

### Current validated wireless path

The recovered RGB transaction family uses:

```text
13 88 XX
```

where `XX` identifies the number of 20-byte HID reports in the transaction.

The currently validated full-keyboard RGB transaction is:

```text
13 88 08
```

with:

```text
8 × 20-byte HID reports
105-byte native RGB stream
14 bytes of native data per report
additive report checksum
```

The native RGB stream contains six RGB group records covering the recovered 81 physical LED indices.

### Wireless implementation status

- [x] Identify the wireless RGB HID collection
- [x] Identify VID `0x258A`
- [x] Identify PID `0x0148`
- [x] Identify Usage Page `0xFF02`
- [x] Identify Usage `0x0002`
- [x] Recover the `13 88 XX` report family
- [x] Recover the 20-byte report structure
- [x] Recover report sequence numbering
- [x] Recover report payload length encoding
- [x] Recover additive report checksum
- [x] Recover the six native RGB groups
- [x] Recover 81 unique native LED indices
- [x] Recover the 105-byte full-keyboard native stream
- [x] Implement native stream encoding
- [x] Implement report packetization
- [x] Implement report validation and reconstruction
- [x] Implement wireless HID transport
- [x] Implement wireless device lifecycle
- [x] Implement wireless RGB streaming
- [x] Implement wireless keepalive
- [x] Validate the full `13 88 08` transaction on hardware
- [x] Validate smooth wireless RGB animation at 14 FPS
- [ ] Fully reverse engineer all `13 88 XX` transaction types
- [ ] Recover arbitrary per-key wireless RGB encoding
- [ ] Recover wireless lighting effects
- [ ] Determine the complete wireless protocol
- [ ] OpenRGB integration
- [ ] SignalRGB integration

### Important wireless limitation

The current wireless encoder represents the keyboard using six native RGB groups.

It does **not** yet provide a proven arbitrary per-key wireless RGB encoder equivalent to the wired `Frame` API.

The current implementation therefore focuses on the recovered six-group representation and the validated full-keyboard `13 88 08` transaction.

More detailed wireless findings are documented in:

```text
2.4ghz/docs/findings.md
2.4ghz/docs/protocol.md
```

---

# Important Firmware Behavior

The RK M75 does not permanently retain an externally supplied RGB framebuffer after receiving a single USB Feature Report.

With the official RK software closed:

```text
Single Feature Report
        |
        v
Requested RGB state
        |
        v
     ~1 second
        |
        v
Keyboard firmware reclaims lighting control
```

Setting the official software's lighting mode to **Off** does not prevent this behavior. A single externally supplied RGB frame still disappears after approximately one second.

However, continuously transmitting the same Feature Report maintains external RGB control.

A test at 10 Hz successfully kept the keyboard red for more than one minute.

When transmission stopped, the keyboard reclaimed the lighting state after approximately one second.

---

# Wired Streaming Behavior

Continuous Feature Report transmission can be used to maintain control of the RGB framebuffer and produce live RGB animations.

The tested RK M75 successfully sustained:

```text
10 Hz   -> stable
20 Hz   -> stable
30 Hz   -> stable
31 Hz   -> stable
32 Hz   -> stable
33 Hz   -> stable
```

At 33 Hz, continuously changing RGB frames produced a smooth visual animation on the keyboard.

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

An unrestricted stress test, with no FPS limiter, also settled at approximately 15 FPS.

A changing-frame stress test produced the same behavior, showing that the slowdown is not caused by repeatedly transmitting an unchanged RGB frame.

The current evidence therefore shows:

> **33 Hz is the highest update rate currently validated as stable on the tested RK M75 under Windows. At 34 Hz, `send_feature_report()` enters a significantly slower blocking behavior and observed throughput drops to approximately 15 Hz.**

This should not currently be interpreted as a proven absolute hardware maximum. The exact layer responsible for the behavior has not yet been isolated.

For this reason, the current wired `RGBStream` implementation limits the configured streaming rate to a maximum of 33 Hz.

---

# Wireless Streaming Behavior

The currently validated wireless dynamic RGB path uses:

```text
FPS:                 14
Inter-report gap:    7 ms
Transaction:         13 88 08
Native stream:       105 bytes
Reports:             8 × 20 bytes
```

A 20-second hardware validation produced:

```text
Duration:            20.000 s
Frames sent:         280
Average FPS:         14.000
TX average:          ~56.5 ms
TX minimum:          ~55.0 ms
TX maximum:          ~58.0 ms
```

The keyboard remained visually smooth throughout the test with:

```text
No flashing
No jumping
No incorrect colors
```

The wireless stream is therefore considered **hardware validated at 14 FPS with a 7 ms inter-report gap**.

This is a validated operating point, not a claimed maximum wireless update rate.

---

# Wired Streaming API

The library provides an `RGBStream` interface for continuous wired RGB transmission.

## Basic RGB control

```python
from rkm75 import Frame, RKM75

frame = Frame()
frame.set_key("A", (255, 0, 0))

with RKM75() as kb:
    kb.send(frame)
```

## Continuous RGB streaming

```python
from rkm75 import Frame, RKM75

frame = Frame()

with RKM75() as kb:
    with kb.stream(fps=33) as stream:
        while True:
            frame.fill((255, 0, 0))
            stream.send(frame)
```

The streaming layer handles the update timing while the caller remains responsible for generating or modifying the `Frame`.

---

# Wireless API

The wireless implementation is exposed separately from the wired API.

The current wireless device API works with the recovered six-group representation rather than arbitrary per-key `Frame` objects.

A simplified wireless usage pattern is:

```python
from rkm75.wireless import RKM75Wireless

colors = (
    (255, 0, 0),
    (255, 128, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 128, 255),
    (180, 0, 255),
)

with RKM75Wireless() as keyboard:
    keyboard.send_frame(colors)
```

The wireless API and exact implementation details should be treated as experimental while wireless reverse engineering continues.

---

# Vendor Configuration and Key Mapping

The official RK Keyboard Software uses a shared configuration system for multiple Royal Kludge keyboard models.

The main configuration file contains a large list of supported VID/PID combinations. The RK M75 tested by this project is:

```text
VID: 0x258A
PID: 0x0163
Device: RK-M75RGB New layout
```

The device-specific keyboard layout was found under the RK software's `Dev` directory.

Typical Windows installation path:

```text
C:\Program Files (x86)\RK Keyboard Software\Dev\<PID>\
```

For the RK M75:

```text
C:\Program Files (x86)\RK Keyboard Software\Dev\0163\
```

The device-specific configuration contains the keyboard layout and key definitions used by the official software.

The `[KEY]` section contains the physical keyboard layout and internal key indices. These indices correspond to the RGB framebuffer positions.

The complete 81-key mapping was extracted from this configuration and validated against the physical keyboard.

For example:

```text
A      -> LED 9
SPACE  -> LED 35
```

Both mappings were independently verified through hardware testing.

The complete 81-key mapping was then tested by illuminating every mapped key, followed by a row-based color test. All mapped keys illuminated in their expected physical positions.

The RGB framebuffer contains 126 RGB entries, while the library currently exposes 81 mapped physical keyboard keys.

The configuration reports `LayoutKeyNum=84`, but only the 81 main RGB keyboard keys are currently mapped by the library. Additional controls, such as the encoder, are outside the current keymap scope.

---

# Compatibility With Other RK Keyboards

The official RK configuration contains many other Royal Kludge keyboard PIDs.

This suggests that the shared RK software and its device-specific configuration system support a wide range of RK keyboards.

However:

> **Presence of a PID in the official configuration does not mean that this project supports that keyboard.**

The wired protocol, packet layout, framebuffer layout, key mapping, firmware behavior, and streaming behavior have only been validated on:

```text
VID 0x258A
PID 0x0163
RK-M75RGB New layout
```

The current wireless RGB implementation has been validated separately on:

```text
VID 0x258A
PID 0x0148
RK M75 wireless RGB HID interface
```

Other RK keyboards should be considered **unverified** and must be tested independently.

The same RK software driver/configuration system may work with other devices listed in the vendor configuration, but compatibility is not guaranteed.

---

# Repository Layout

```text
2.4ghz/
    README.md
    captures/
    docs/
        findings.md
        protocol.md
    scripts/
        hardware_keepalive_test.py
        hardware_smoke_test.py
        validate_native_13_88_08.py

captures/
    USB wired Wireshark captures

docs/
    USB wired protocol documentation and findings

examples/
    Wired library examples and hardware tests

reports/
    Generated analysis output

rkm75/
    Core Python library
    wireless/
        Wireless RGB implementation

tests/
    Wired and wireless automated regression tests

tools/
    Reverse-engineering utilities
```

The `2.4ghz/` directory contains research material and documentation for the wireless protocol.

The production-facing Python implementation lives under:

```text
rkm75/wireless/
```

The repository intentionally does not retain the large collection of historical experimental scripts used during wireless reverse engineering. Their relevant conclusions have been consolidated into the wireless documentation.

---

# Project Architecture

## Wired

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
                     +---------+
                     | RK M75  |
                     +---------+
```

## Wireless

```text
                 +------------------+
                 |    Application   |
                 +------------------+
                          |
                          v
                 +------------------+
                 | RKM75Wireless    |
                 +------------------+
                          |
                          v
                 +------------------+
                 | Wireless Encoder |
                 +------------------+
                          |
                          v
                 +------------------+
                 | Native RGB Stream|
                 +------------------+
                          |
                          v
                 +------------------+
                 |   Packetization  |
                 +------------------+
                          |
                          v
                 +------------------+
                 |   13 88 XX HID   |
                 |      Reports     |
                 +------------------+
                          |
                          v
                 +------------------+
                 | Wireless HID     |
                 | Transport        |
                 +------------------+
                          |
                          v
                     +---------+
                     | RK M75  |
                     +---------+
```

The wired and wireless paths are intentionally separate because they use different HID interfaces, transport mechanisms, and RGB representations.

---

# Examples

The wired examples are numbered roughly in the order they were developed during reverse engineering.

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

### Benchmark RGB streaming

```bash
python examples/08_benchmark_stream.py --fps 33 --duration 30
```

### Stress-test the HID transport

```bash
python examples/09_stress_stream.py --duration 10
```

### Stress-test changing RGB frames

```bash
python examples/10_stress_changing_frames.py --duration 10
```

### Test smooth 33 Hz RGB animation

```bash
python examples/11_animation_33hz.py
```

### Use the wired streaming API

```bash
python examples/12_stream.py
```

---

# Wireless Hardware Validation

The wireless implementation includes dedicated hardware validation scripts.

### Offline protocol validation

This does not communicate with the keyboard:

```bash
python 2.4ghz/scripts/validate_native_13_88_08.py
```

### Wireless RGB smoke test

```bash
python 2.4ghz/scripts/hardware_smoke_test.py
```

The current validated baseline is:

```text
14 FPS
7 ms inter-report gap
20 second hardware test
13 88 08 transaction
8 × 20-byte HID reports
105-byte native stream
```

### Wireless keepalive validation

```bash
python 2.4ghz/scripts/hardware_keepalive_test.py
```

These scripts require the RK M75 wireless receiver and are intended for hardware testing rather than automated CI.

---

# Automated Tests

The project includes a hardware-independent regression test suite covering the wired and wireless public APIs and protocol layers.

Current test modules include:

```text
tests/
    test_device.py
    test_frame.py
    test_keymap.py
    test_packet.py
    test_stream.py
    test_transport.py
    test_wireless_device.py
    test_wireless_encoder.py
    test_wireless_protocol.py
    test_wireless_stream.py
    test_wireless_transport.py
```

The current suite contains:

```text
73 tests
```

The complete suite currently passes on the development environment:

```text
73 passed
```

The tests cover:

- Public `RKM75` API behavior
- Device discovery delegation
- Device lifecycle and context management
- RGB framebuffer creation
- RGB input validation
- LED index validation
- Logical key mapping
- 81-key mapping integrity
- Wired packet structure and size
- Feature Report padding
- Packet file output
- Wired RGBStream FPS validation
- Wired RGBStream lifecycle
- Wired RGBStream timing behavior
- HID transport validation
- HID transport lifecycle
- Closed-transport behavior
- Wireless transaction structure
- Wireless report count and payload capacity
- Wireless native stream reconstruction
- Wireless six-group LED layout
- Wireless group color encoding
- Wireless report packetization
- Wireless HID transport validation
- Wireless wireless-device lifecycle
- Wireless RGB streaming
- Wireless keepalive behavior

The automated tests do not require a physical RK M75.

Hardware validation is performed separately using the dedicated examples and wireless scripts.

---

# Development Roadmap

## Milestone 1 — HID Discovery

- [x] Discover wired RGB HID interface
- [x] Discover wireless RGB HID interface
- [x] Open wired transport
- [x] Open wireless transport

## Milestone 2 — Wired Feature Report Replay

- [x] Capture vendor RGB Feature Report
- [x] Extract report
- [x] Replay report successfully

## Milestone 3 — Wired Packet Generation

- [x] Reconstruct Feature Report structure
- [x] Generate RGB Feature Reports from Python
- [x] Send generated RGB frames successfully

## Milestone 4 — Wired Key Mapping

- [x] Locate vendor keyboard layout
- [x] Derive 81-key RGB mapping
- [x] Implement logical key API
- [x] Validate all 81 RGB positions
- [x] Document firmware takeover behavior
- [x] Validate 10 Hz continuous control

## Milestone 5 — Wired Live Streaming

- [x] Characterize stable streaming rates
- [x] Characterize Feature Report behavior above 33 Hz
- [x] Measure effective FPS
- [x] Validate long-duration stability
- [x] Build streaming API
- [x] Validate smooth RGB animations

## Milestone 6 — Wireless Protocol Recovery

- [x] Identify wireless RGB HID interface
- [x] Recover `13 88 XX` transaction family
- [x] Recover 20-byte report structure
- [x] Recover report sequence field
- [x] Recover payload length field
- [x] Recover additive checksum
- [x] Recover six native RGB groups
- [x] Recover 81 unique native LED indices
- [x] Recover 105-byte full-keyboard native stream
- [x] Validate `13 88 08` on hardware
- [x] Validate smooth 14 FPS wireless animation
- [ ] Fully characterize shorter `13 88 XX` transactions
- [ ] Recover arbitrary per-key wireless RGB encoding
- [ ] Recover wireless effects
- [ ] Determine complete wireless protocol

## Milestone 7 — API Hardening & Reliability

- [x] Define public package API
- [x] Validate RGB frame inputs
- [x] Validate LED indices
- [x] Validate RGBStream FPS inputs
- [x] Harden HID transport lifecycle
- [x] Add device unit tests
- [x] Add frame unit tests
- [x] Add packet unit tests
- [x] Add stream unit tests
- [x] Add transport unit tests
- [x] Add keymap regression tests
- [x] Add wireless protocol tests
- [x] Add wireless encoder tests
- [x] Add wireless transport tests
- [x] Add wireless device tests
- [x] Add wireless stream tests
- [x] Validate hardened implementation on hardware
- [x] Revalidate 33 Hz wired streaming stability
- [x] Revalidate 81-key wired RGB mapping
- [x] Revalidate continuous wired RGB control
- [x] Validate wireless `13 88 08` transaction
- [x] Confirm 73 automated tests pass

## Future

- [ ] Community testing on additional RK M75 systems
- [ ] Complete 2.4 GHz protocol reverse engineering
- [ ] Arbitrary per-key wireless RGB control
- [ ] Wireless lighting effects
- [ ] OpenRGB integration
- [ ] SignalRGB integration
- [ ] Additional RK keyboard models
- [ ] Linux support

---

# Protocol Summary

## USB Wired

| Property | Value |
| --- | --- |
| Transport | USB HID Feature Report |
| Vendor ID | `0x258A` |
| Product ID | `0x0163` |
| Device | RK-M75RGB New layout |
| Report ID | `9` |
| Report Size | `520 bytes` |
| Interface | `MI_01` / Interface 1 |
| Usage Page | `0xFF02` |
| Lighting packet type | `0x08` |
| Status packet type | `0x0B` |
| RGB framebuffer | `126 RGB entries` |
| Mapped physical keys | `81` |
| Validated stream rate | `33 Hz` |

## 2.4 GHz Wireless

| Property | Value |
| --- | --- |
| Transport | Wireless HID |
| Vendor ID | `0x258A` |
| Product ID | `0x0148` |
| Usage Page | `0xFF02` |
| Usage | `0x0002` |
| Transaction family | `13 88 XX` |
| Validated transaction | `13 88 08` |
| Report size | `20 bytes` |
| Report count | `8` |
| Native stream size | `105 bytes` |
| Native RGB groups | `6` |
| Native LED entries | `81` |
| Inter-report gap | `7 ms` |
| Validated dynamic rate | `14 FPS` |

More detailed wired protocol information is available in:

```text
docs/protocol.md
```

Wired reverse-engineering observations are documented in:

```text
docs/findings.md
```

Wireless protocol documentation is available in:

```text
2.4ghz/docs/protocol.md
2.4ghz/docs/findings.md
```

---

# Contributing

Contributions are welcome.

The wired RGB control and streaming API has been validated on the RK M75 and covered by automated regression tests.

The 2.4 GHz wireless RGB path is also hardware validated at its current supported operating point, but the wireless protocol is still under active reverse engineering.

Hardware testing is currently focused on the RK M75 with:

```text
Wired:
VID 0x258A
PID 0x0163

Wireless:
VID 0x258A
PID 0x0148
```

Community testing of additional RK M75 units is especially welcome before OpenRGB and SignalRGB integration work begins.

Contributions involving other RK devices should include hardware and protocol validation where possible.

---

# License

MIT