# RK M75 2.4 GHz Reverse-Engineering Findings

## 2026-08-08 — Initial receiver identification

USBTreeView identified the RK M75 2.4 GHz receiver as:

- VID: `0x258A`
- PID: `0x0148`
- Manufacturer: SINO WEALTH
- Product: Gaming KB

The receiver exposes multiple HID collections.

HIDAPI enumeration confirmed 10 HID device entries for the receiver,
including multiple vendor-defined collections.

## 2026-08-08 — Passive HID monitoring

The `FF02/0002` collection was monitored using HIDAPI.

No input traffic was observed during:

- idle operation
- normal key presses
- RGB changes using keyboard hardware controls

This established that RGB control traffic was not appearing as ordinary
input reports on that collection.

The `FF02/0001` collection was also monitored without observing useful
RGB-related input traffic.

## 2026-08-08 — Official software control confirmed

The official RK software successfully controlled RGB while the keyboard
was connected through 2.4 GHz.

This established that the wireless RGB path is software-controllable.

USBPcap/Wireshark capture was then used to observe the software's USB
traffic to the receiver.

## 2026-08-08 — Command 0x07 discovered

Official software RGB traffic was found to use HID `SET_REPORT` transfers
with report ID `0x13`.

Command `0x07` is transmitted as a seven-report sequence with sequence
values `00` through `06`.

The first report contains the selected RGB color.

The sequence is repeatedly refreshed by the official software.

## 2026-08-08 — Command 0x01 discovered

Additional captures of per-key RGB changes revealed command `0x01`.

The packet contains:

- RGB color
- LED index
- additive checksum

The command is a single 20-byte report.

## 2026-08-08 — Wireless LED mapping confirmed

Individual RGB captures were performed for:

- A
- W
- M
- ESC
- SPACE
- ENTER

The wireless LED indices matched the existing wired mapping exactly:

| Key | Wireless | Wired |
|---|---:|---:|
| ESC | 0 | 0 |
| A | 9 | 9 |
| W | 14 | 14 |
| M | 46 | 46 |
| SPACE | 35 | 35 |
| ENTER | 81 | 81 |

This provides strong evidence that wired and 2.4 GHz RGB control share
the same logical LED index space.

## Current Status

The per-key RGB command is sufficiently understood to describe its
structure, but no experimental packets have yet been transmitted by
this project.

Command `0x07` remains the primary reverse-engineering target.

No wireless implementation has been added to the stable `rkm75/`
package.