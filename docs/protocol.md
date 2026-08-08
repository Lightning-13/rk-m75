# RK M75 RGB Protocol

This document describes the currently reverse-engineered RGB communication
protocol for the RK M75.

The protocol has been experimentally validated on the following device:

```text
VID:     0x258A
PID:     0x0163
Device:  RK-M75RGB New layout
```

Other RK keyboard models are not currently considered validated.

---

## USB / HID

The RGB interface is exposed through the vendor HID collection.

```text
Interface:   1
MI:          MI_01
Usage Page:  0xFF02
Usage:       0x01
```

Communication is performed using HID Feature Reports.

The RGB interface was identified through controlled USB/HID captures and
interaction with the official RK Keyboard Software.

---

## Feature Report

The RGB lighting report has:

```text
Report ID: 0x09
Size:      520 bytes
```

The report can be sent using HID Feature Report communication.

The report was successfully replayed from a captured packet and later
generated entirely from Python.

The generated report produces the expected RGB state on the physical
keyboard.

---

## Lighting Packet

The RGB lighting packet contains packet type:

```text
0x08
```

A separate status packet type was identified:

```text
0x0B
```

The lighting packet contains the RGB framebuffer used to control the
keyboard lighting.

The exact semantics of every packet field have not yet been established.

---

## RGB Framebuffer

The Feature Report contains the RGB framebuffer used by the keyboard.

The library represents the framebuffer using a logical `Frame` object.

The library converts the logical RGB representation into the vendor's
520-byte Feature Report format.

The framebuffer can be generated entirely from Python.

Individual keyboard keys can be assigned RGB values through the validated
key mapping.

No checksum has been identified in the lighting packet.

No sequence counter has been identified in the lighting packet.

---

## Key Mapping

The logical key → framebuffer index mapping was derived from the official
RK software's device-specific configuration for PID `0x0163`.

The configuration is located under:

```text
C:\Program Files (x86)\RK Keyboard Software\Dev\0163\
```

The `[KEY]` section contains the physical keyboard layout and internal
key indices.

Examples:

```text
A      → LED 9
SPACE  → LED 35
```

The complete 81-key mapping was validated on the physical RK M75.

The vendor configuration reports:

```text
LayoutKeyNum=84
```

but the current library maps the 81 main RGB keyboard keys.

The remaining three logical positions, potentially associated with the
rotary encoder or other controls, have not been experimentally mapped.

---

## Firmware Takeover

The keyboard firmware continues to manage its onboard lighting state after
an external RGB Feature Report is received.

A single RGB report is therefore transient.

Observed behavior:

```text
Send report
    ↓
RGB state changes
    ↓
~1 second
    ↓
Firmware reasserts its lighting state
```

This behavior was observed with the official RK software closed.

Therefore, sending a single Feature Report is not sufficient for permanent
external RGB control.

---

## Lighting-Off Behavior

Setting the official RK software's lighting mode to Off does not disable
the firmware takeover mechanism.

With the official software closed:

```text
Lighting Off
     ↓
Send single RGB report
     ↓
RGB state appears
     ↓
~1 second
     ↓
Keyboard returns to black
```

Therefore, an external application cannot currently rely on the official
software's Off state to permanently release RGB control.

Continuous Feature Report transmission is the standalone method currently
used to maintain external RGB control.

---

## Continuous Updates

Repeatedly sending the same Feature Report maintains external RGB control.

A 10 Hz test was performed:

```text
Interval:  100 ms
Frequency: 10 Hz
Duration:  More than 60 seconds
```

The requested RGB state remained active for the entire test.

When transmission stopped, the keyboard reclaimed control after
approximately one second.

Therefore:

```text
10 Hz continuous Feature Reports
        =
validated persistent external RGB control
```

10 Hz is sufficient for a static RGB keepalive.

It should not be interpreted as the minimum supported frequency.

---

## Streaming

Continuous RGB streaming has been experimentally validated at rates up to
33 Hz on the tested RK M75 under Windows.

The following scheduled rates were successfully sustained:

```text
10 Hz  → 10.00 FPS
20 Hz  → 20.00 FPS
30 Hz  → 30.00 FPS
31 Hz  → 31.00 FPS
32 Hz  → 32.00 FPS
33 Hz  → 33.00 FPS
```

At 33 Hz, continuously changing RGB frames produced smooth visual
transitions on the physical keyboard.

A 30-second animation test produced:

```text
Duration:    30.000 seconds
Sent:        990
Errors:      0
Actual FPS:  33.00
```

A five-minute stability test produced:

```text
Duration:    300.000 seconds
Sent:        9900
Errors:      0
Actual FPS:  33.00
```

The keyboard remained visually stable for the complete five-minute test.

This establishes 33 Hz as the highest update rate currently validated as
stable for this implementation.

---

## Streaming Behavior Above 33 Hz

The first tested rate above 33 Hz was 34 Hz.

Observed behavior:

```text
Target FPS: 34
Actual FPS: approximately 15.76
```

The underlying `send_feature_report()` call also became significantly
slower:

```text
Average: approximately 63 ms
Median:  approximately 83 ms
Minimum: approximately 23 ms
Maximum: approximately 89 ms
```

Further tests showed similar behavior:

```text
35 Hz → approximately 15.20 FPS
40 Hz → approximately 14.98 FPS
```

An unrestricted stress test with no FPS limiter also settled at
approximately 15 FPS.

A changing-frame stress test produced approximately 15 FPS as well,
demonstrating that the slowdown is not caused by repeatedly sending an
unchanged framebuffer.

All of these tests completed without reported Feature Report send errors.

The exact layer responsible for this behavior has not yet been isolated.
Possible factors include the Windows HID path, HID library/backend,
USB scheduling, or device-side flow control.

Therefore:

> 33 Hz is the highest update rate currently validated as stable on the
> tested RK M75 under Windows.

This is not currently claimed to be an absolute hardware maximum.

The current `RGBStream` implementation therefore limits the configured
streaming rate to 33 Hz.

---

## RGB Streaming API

The experimentally validated streaming behavior has been implemented as a
library-level `RGBStream` interface.

The preferred API is:

```python
from rkm75 import Frame, RKM75

frame = Frame()

with RKM75() as kb:
    with kb.stream(fps=33) as stream:
        while True:
            frame.fill((255, 0, 0))
            stream.send(frame)
```

The streaming layer handles update timing and Feature Report transmission.

The application remains responsible for generating or modifying the
`Frame`.

This separation allows future applications to provide RGB frames without
implementing the HID timing loop themselves.

The API rejects configured rates above 33 Hz because the transport behavior
above that rate has not been validated as stable.

For example:

```python
kb.stream(fps=33)  # supported
kb.stream(fps=34)  # rejected
```

---

## Streaming Architecture

The current RGB control path can be represented as:

```text
Application
     ↓
Frame
     ↓
RGBStream
     ↓
RKM75
     ↓
Packet Builder
     ↓
RGB Framebuffer
     ↓
HID Transport
     ↓
520-byte Feature Report
     ↓
RK M75
```

`RGBStream` is responsible for continuous transmission timing.

`RKM75` provides device communication.

The packet layer converts the logical framebuffer into the vendor Feature
Report format.

This separation is intended to make the streaming layer reusable by future
RGB integrations.

---

## Compatibility

The official RK software contains configuration entries for many RK
keyboard PIDs.

This does not establish compatibility with this protocol implementation.

The protocol described here has only been experimentally validated on:

```text
VID:    0x258A
PID:    0x0163
Device: RK-M75RGB New layout
```

Other RK keyboards require independent validation.

The presence of another PID in the official RK configuration may indicate
that the same vendor software infrastructure supports that device, but it
does not guarantee that the same RGB protocol, framebuffer layout,
key mapping, or streaming behavior will work.

---

## Known Unknowns

The following areas remain incomplete:

- Exact semantics of all packet fields
- Complete status packet documentation
- Encoder RGB/control mapping
- Minimum keepalive frequency
- Exact cause of the 33/34 Hz transport boundary
- Maximum theoretical streaming rate
- Protocol differences between other RK keyboard models
- Per-key changing-frame streaming validation
- Additional device support

---

## Current Protocol Summary

```text
USB Vendor ID:       0x258A
USB Product ID:      0x0163
Device:              RK-M75RGB New layout

HID Interface:       1
HID Collection:      MI_01
Usage Page:          0xFF02
Usage:               0x01

Feature Report ID:   0x09
Feature Report Size: 520 bytes

Lighting Packet:     0x08
Status Packet:       0x0B

Validated Keymap:    81 keys
Keepalive:           10 Hz validated
Streaming:           33 Hz validated
Long-duration test:  5 minutes / 9900 frames
```