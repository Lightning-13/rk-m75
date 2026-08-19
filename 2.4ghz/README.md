# RK M75 2.4 GHz RGB

Reverse-engineering and implementation workspace for RGB control of the RK M75 over its 2.4 GHz wireless connection.

## Status

**Validated experimental transport — not complete protocol reverse engineering.**

The project has successfully reconstructed and transmitted a full-keyboard RGB transaction using:

```text
13 88 08
105-byte native stream
8 x 20-byte HID reports
81 native LED indices
```

The current validated implementation uses six native RGB groups covering 81 native LED indices.

This is **full-keyboard RGB coverage**, but it is **not yet a complete arbitrary per-key RGB implementation**. The current recovered representation assigns one RGB color to each native group.

## Validated operating baselines

The currently selected operating points are:

```text
Dynamic full-keyboard grouped RGB:
    14 FPS
    7 ms inter-report gap

Static RGB keepalive:
    5 FPS
    7 ms inter-report gap
```

These are validated stable engineering baselines, not proven hardware or protocol limits.

Testing at higher frame rates has shown increasingly frequent visible flashes, but the true maximum reliable wireless frame rate has not been established.

The current implementation also does not claim that 14 FPS is the fastest or smoothest rate the hardware can achieve.

## Important distinction

The current wireless path is **working and hardware-validated**, but the 2.4 GHz RGB protocol is not completely understood.

In particular, the following should not be treated as solved:

- arbitrary independent per-key RGB
- all valid `13 88 XX` transaction sizes
- complete semantics of every native stream field
- optimal native grouping
- complete decoding of official dynamic effects
- the true maximum reliable frame rate
- the exact cause of occasional transient flashes

The current implementation therefore intentionally exposes only the validated grouped RGB path.

## Current implementation

The reusable wireless backend lives in:

```text
rkm75/wireless/
```

It is kept as a separate wireless backend from the existing wired transport API.

The current path is:

```text
Frame
  ↓
six-group RGB representation
  ↓
105-byte native stream
  ↓
13 88 08 transaction
  ↓
8 × 20-byte HID reports
  ↓
RK M75 2.4 GHz receiver
```

The wireless backend has been validated against the physical keyboard using the 14 FPS / 7 ms baseline.

It is not yet exposed as a replacement for the existing wired API.

## Documentation

- `docs/protocol.md` — current protocol model and validated packet format
- `docs/findings.md` — reverse-engineering findings, experimental results, confidence boundaries, and open questions

## Research material

- `captures/` — raw wireless captures and supporting evidence
- `scripts/` — repeatable protocol validation and hardware tests

The captures provide the underlying evidence for the reverse-engineering work. The documentation distinguishes established observations from validated implementation behavior and unresolved questions.

## Validation

The repository contains automated tests for the wireless protocol, encoder, transport, device wrapper, and stream behavior.

The current hardware validation tools include:

```text
scripts/validate_native_13_88_08.py
scripts/hardware_smoke_test.py
scripts/hardware_keepalive_test.py
```

The offline validation script does not communicate with the keyboard.

The hardware smoke tests require the RK M75 2.4 GHz receiver and validate the actual wireless transport.

## Open questions

The protocol is not considered complete.

Still unresolved include:

- true maximum reliable wireless FPS
- whether smoother or higher-rate animation is possible
- whether a different scheduling or inter-report strategy improves smoothness
- complete native field semantics
- complete semantics of all valid `13 88 XX` transaction sizes
- whether another grouping is visually superior
- complete arbitrary per-key RGB support
- complete decoding of official dynamic-effect formats
- complete wireless initialization and state requirements
- the exact cause of occasional transient flashes