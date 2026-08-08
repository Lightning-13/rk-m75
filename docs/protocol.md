# RK M75 RGB Protocol

This document describes the currently reverse-engineered RGB communication
protocol for the RK M75.

Tested device:

VID:     0x258A
PID:     0x0163
Device:  RK-M75RGB New layout

---

## USB / HID

The RGB interface is exposed through the vendor HID collection.

Interface:   1
MI:          MI_01
Usage Page:  0xFF02
Usage:       0x01

Communication is performed using HID Feature Reports.

---

## Feature Report

The RGB lighting report has:

Report ID: 0x09
Size:      520 bytes

The report can be sent using HID Feature Report communication.

The report was successfully replayed from a captured packet and later
generated entirely from Python.

---

## Lighting Packet

The RGB lighting packet contains packet type:

0x08

A separate status packet type was identified:

0x0B

The packet contains the RGB framebuffer used to control the keyboard
lighting.

---

## RGB Framebuffer

The framebuffer contains RGB values for the keyboard's RGB positions.

The library represents the framebuffer using a logical `Frame` object.

The library converts the logical key representation into the vendor's
520-byte Feature Report format.

No checksum has been identified in the lighting packet.

No sequence counter has been identified in the lighting packet.

---

## Key Mapping

The logical key → framebuffer index mapping was derived from the official
RK software's device-specific configuration for PID `0x0163`.

The configuration is located under:

C:\Program Files (x86)\RK Keyboard Software\Dev\0163\

The `[KEY]` section contains the physical keyboard layout and internal
key indices.

Examples:

A      → LED 9
SPACE  → LED 35

The complete 81-key mapping was validated on the physical RK M75.

---

## Firmware Takeover

The keyboard firmware continues to manage its onboard lighting state after
an external RGB Feature Report is received.

A single RGB report is therefore transient.

Observed behavior:

Send report
    ↓
RGB state changes
    ↓
~1 second
    ↓
Firmware reasserts its lighting state

This behavior was observed with the official RK software closed.

---

## Lighting-Off Behavior

Setting the official RK software's lighting mode to Off does not disable
the firmware takeover mechanism.

With the official software closed:

Lighting Off
     ↓
Send single RGB report
     ↓
RGB state appears
     ↓
~1 second
     ↓
Keyboard returns to black

Therefore, an external application cannot currently rely on the official
software's Off state to permanently release RGB control.

---

## Continuous Updates

Repeatedly sending the same Feature Report maintains external RGB control.

A 10 Hz test was performed:

Interval:  100 ms
Frequency: 10 Hz
Duration:  More than 60 seconds

The requested RGB state remained active for the entire test.

When transmission stopped, the keyboard reclaimed control after
approximately one second.

Therefore:

10 Hz continuous Feature Reports
        =
validated persistent external RGB control

This should currently be considered the **known-good update rate**, rather
than the minimum or maximum supported rate.

---

## Streaming

Continuous RGB streaming is proven to work at 10 Hz.

The maximum stable update rate has not yet been determined.

Future tests will characterize:

* Minimum stable update rate
* Maximum stable update rate
* Frame latency
* Long-duration stability
* Behavior at higher transmission rates
* Actual visible frame rate

The streaming implementation will be developed separately from the
current key-mapping implementation.

---

## Compatibility

The official RK software contains configuration entries for many RK
keyboard PIDs.

This does not establish compatibility with this protocol implementation.

The protocol described here has only been experimentally validated on:

VID:    0x258A
PID:    0x0163
Device: RK-M75RGB New layout

Other RK keyboards require independent validation.

---

## Known Unknowns

The following areas remain incomplete:

* Exact semantics of all packet fields
* Complete status packet documentation
* Encoder RGB/control mapping
* Minimum keepalive frequency
* Maximum stable streaming rate
* Maximum practical animation rate
* Protocol differences between other RK keyboard models