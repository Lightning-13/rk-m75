# Capture Set

This directory contains the USB captures used during reverse engineering of the Royal Kludge RK M75 RGB protocol.

## Capture Method

All captures were recorded while interacting with the official RK software.

USB traffic was captured using Wireshark.

The objective was to isolate the USB HID Feature Reports responsible for RGB lighting updates.

---

## Capture List

| File | Description |
|------|-------------|
| `00_idle.pcapng` | Keyboard idle with no lighting changes |
| `01_all_red.pcapng` | Entire keyboard set to red |
| `02_all_green.pcapng` | Entire keyboard set to green |
| `03_all_blue.pcapng` | Entire keyboard set to blue |
| `04_all_white.pcapng` | Entire keyboard set to white |
| `05_all_off.pcapng` | All LEDs turned off |
| `06_esc_red_to_green.pcapng` | Entire keyboard red, then only **Esc** changed to green |
| `07_a_red_to_green.pcapng` | Entire keyboard red, then only **A** changed to green |
| `08_space_red_to_green.pcapng` | Entire keyboard red, then only **Space** changed to green |

---

## Capture Strategy

All captures were recorded using the same lighting mode inside the RK software.

Only the RGB values were changed between captures.

This minimizes unrelated protocol changes and makes packet comparison reliable.

The single-key captures were designed to identify the mapping between RGB buffer indices and physical keys.

---

## Purpose

These captures serve as the ground truth for protocol reverse engineering and are intentionally kept unmodified.

All protocol documentation and implementation in this repository should be reproducible from these captures.