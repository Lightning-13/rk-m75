# RK M75 Community Tester

This directory contains a small hardware-testing utility for validating
RGB functionality on the RK M75.

The tester is intended for community members who want to help validate the
reverse-engineered RGB implementation on additional RK M75 keyboards.

## Supported Device

The tester currently targets:

```text
Vendor ID:  0x258A
Product ID: 0x0163
Device:     RK-M75RGB New layout
````

Other RK keyboard models are not supported by this tester.

The presence of another RK keyboard PID in the official RK software does
not mean that the device is compatible with this project.

## Requirements

* Windows
* Python 3.10 or newer
* An RK M75 connected by USB
* The RGB HID interface must be accessible

The tester uses the existing `rkm75` library from this repository.

## Running the Tester

From the repository root:

```powershell
python tester\run_tests.py
```

The tester provides:

```text
1. Device detection
2. Static RGB
3. 81-key mapping
4. 10 Hz keepalive
5. 33 Hz streaming
A. Run all tests
Q. Quit
```

## Tests

### 1. Device Detection

Checks that the RK M75 RGB HID interface can be discovered and opened.

No RGB changes are made.

Expected result:

```text
PASS
RK M75 RGB HID interface detected.
```

### 2. Static RGB

Sends a generated RGB frame that should turn the keyboard solid red.

The tester asks the user to visually confirm the result.

Expected result:

```text
PASS
```

### 3. 81-Key Mapping

Tests the logical RGB mapping used by the library.

Each mapped key is illuminated individually.

The tester displays:

```text
[01/81] ESC -> LED 0
[02/81] F1  -> LED 12
...
```

For every key, confirm that the highlighted physical key matches the
displayed logical key.

Enter:

```text
y
```

if the key is correct.

Enter:

```text
n
```

if the key is incorrect.

Enter:

```text
q
```

to cancel the test.

A successful test should finish with:

```text
PASS
All 81 mapped keys were confirmed.
```

### 4. 10 Hz Keepalive

Repeatedly sends the same RGB frame at 10 Hz for approximately 10 seconds.

The keyboard should remain solid red throughout the test.

This validates that continuous Feature Report transmission can maintain
external RGB control on the tested device.

### 5. 33 Hz Streaming

Runs a continuously changing RGB animation at the validated 33 Hz
streaming rate.

The test runs for approximately 10 seconds.

The tester reports:

```text
Target FPS
Duration
Sent frames
Actual FPS
```

The animation should appear smooth and should not produce visible errors.

33 Hz is the highest streaming rate currently validated as stable for the
RK M75 implementation.

The tester intentionally does not test rates above 33 Hz.

## Safety

This tester:

* Does not update keyboard firmware
* Does not modify keyboard configuration
* Does not write persistent device settings
* Only sends RGB HID Feature Reports through the existing library
* Can be stopped with `Ctrl+C`

The tests may temporarily change the keyboard's RGB lighting.

When external RGB transmission stops, the keyboard firmware may reclaim
lighting control after approximately one second.

## Reporting Results

After completing a test, copy the displayed test result.

For a complete test run, the tester produces a report similar to:

```text
==================================================
RK M75 Community Test Report
==================================================

VID: 0x258A
PID: 0x0163

Device detection: PASS
Static RGB:       PASS
81-key mapping:   PASS (81/81)
10 Hz keepalive:  PASS
33 Hz streaming:  PASS (32.63 FPS)

Copy the report above when reporting results.
```

When reporting results, please include:

* The complete test report
* Whether the keyboard is an RK M75
* Any visible RGB problems
* Any keymap mismatch
* Any errors printed by the tester
* Any unusual behavior

Do not report another RK keyboard as an RK M75 result.

## Known Limitations

This tester is currently designed for the validated RK M75 RGB device:

```text
VID: 0x258A
PID: 0x0163
```

It does not establish compatibility with other RK keyboards.

The 33 Hz limit is a validated implementation limit, not a claim that the
keyboard's physical RGB hardware cannot operate above 33 Hz.

## Project

The tester is part of the RK M75 reverse-engineering project.

The main project documentation is located in:

```text
README.md
docs/findings.md
docs/protocol.md
```