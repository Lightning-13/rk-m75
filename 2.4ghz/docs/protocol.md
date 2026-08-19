# RK M75 2.4 GHz RGB Protocol

## Scope and confidence

This document describes the **currently validated** RK M75 2.4 GHz RGB transport. It is not a complete reverse-engineering of the receiver protocol.

The terminology below distinguishes:

- **Confirmed** — directly observed or mechanically validated.
- **Validated** — transmitted by this project and verified on the keyboard.
- **Experimental** — tested, but not selected as the implementation baseline.
- **Unknown** — not established well enough to document as protocol fact.

The current implementation is deliberately conservative.

---

## Receiver

Validated device:

- VID: `0x258A`
- PID: `0x0148`
- Relevant HID collection: `FF02/0002`
- HID report ID: `0x13`
- Windows HID output path

The project currently targets the tested RK M75 2.4 GHz receiver.

---

## `13 88 XX` RGB transaction family

The observed RGB transactions use:

```text
13 88 XX ...
```

The current interpretation, supported by the multi-report experiments, is:

```text
13 88 XX
      └── number of 20-byte HID reports in this RGB transaction
```

Examples observed/tested include:

```text
13 88 07 -> 7 reports
13 88 08 -> 8 reports
13 88 09 -> 9 reports
13 88 0A -> 10 reports
```

This should not be interpreted as proof that every possible `XX` value is supported by firmware.

The implementation currently supports the validated `13 88 08` path.

Other transaction sizes remain experimental unless separately validated.

---

## HID report structure

For the validated `13 88 08` path, every HID report is 20 bytes:

```text
offset  size  meaning
------  ----  -------
0       3     13 88 08
3       1     sequence number, 0..7
4       1     0x10 + meaningful native-data length
5       14    native-data bytes, zero-padded when shorter
19      1     additive checksum
```

Checksum:

```text
checksum = sum(report[0:19]) & 0xFF
```

The reports are reconstructed in sequence order `0..7`.

The 14-byte value above is the maximum native-data payload carried by one 20-byte report in the validated packet structure.

This accounting is important when reasoning about shorter native streams: the transaction header, sequence byte, payload-length byte, and checksum are not available for native RGB data.

---

## Validated `13 88 08` native RGB stream

The currently validated full-keyboard implementation uses:

- 105 native stream bytes
- 6 RGB records
- 81 native LED indices
- 8 HID reports
- 14 native-data bytes per report maximum

Each native record is:

```text
RGB(3) + LED_COUNT(1) + LED_INDICES(N)
```

The recovered group sizes are:

```text
14, 15, 15, 14, 13, 10
```

The six groups together contain 81 unique native LED indices.

The current implementation treats these six groups as the unit of RGB control.

Therefore the validated path provides **full-keyboard grouped RGB coverage**, but it does not claim complete arbitrary per-key RGB control.

In particular, the current representation cannot be treated as proof that every possible 81-key RGB frame can be encoded independently through the same six records.

---

## Packetization

The 105-byte native stream is split into 14-byte chunks:

```text
105 / 14 -> 8 reports
```

The first seven reports carry 14 native-data bytes.

The final report carries the remaining 7 native-data bytes and is padded to 20 bytes.

The encoder validates:

1. stream length
2. report count
3. report size
4. `13 88 08` header
5. sequence numbers
6. payload-length field
7. checksum
8. reconstructed native stream

---

## Timing

### Dynamic RGB baseline

The selected operating point is:

```text
14 FPS
7 ms inter-report gap
```

This is the **highest currently selected stable baseline**, not a proven hardware maximum.

Testing found higher frame-rate points increasingly prone to visible flashes. The exact layer responsible for the limit has not been isolated.

The current implementation therefore does not enforce 14 FPS because the protocol has been proven incapable of running faster. It uses 14 FPS as the current conservative engineering baseline.

### Static RGB keepalive

The selected keepalive baseline is:

```text
5 FPS
7 ms inter-report gap
```

The same RGB transaction is retransmitted unchanged.

This is required because stopping external RGB traffic allows the keyboard's firmware RGB behavior to reclaim the lighting state.

Observed keepalive characterization:

```text
14 FPS   dynamic RGB workload
10 FPS   static keepalive tested
5 FPS    stable
2 FPS    stable
1 FPS    RGB takeover/off observed
```

5 FPS is therefore the selected static keepalive margin, not a proven minimum required by the firmware.

---

## Transition behavior

Long transition testing observed occasional very brief off/on flashes around animation/keepalive or cycle boundaries.

The cause has **not** been conclusively identified.

No transition workaround is part of the current transport implementation.

---

## Other observed RGB paths

Earlier capture work established additional wireless RGB traffic, including:

- single-report per-key updates
- multi-report RGB transactions
- a seven-report `13 88 07` structure
- other observed transaction sizes including `13 88 09` and `13 88 0A`

These observations remain part of the reverse-engineering history.

They are not required by the current validated full-frame `13 88 08` implementation and should not be silently treated as fully decoded.

In particular, the existence of smaller transactions does **not** by itself establish which transaction size should be used for a particular effect or number of changed LEDs.

Future experiments should determine the relationship between native stream length, transaction report count, and the actual semantics of the native data rather than assuming a fixed command for every RGB operation.

---

## Implementation boundary

The cleaned wireless implementation lives in:

```text
rkm75/wireless/
```

It is intentionally kept as a separate wireless backend from the existing wired transport API.

The current backend has been validated against the physical keyboard using the 14 FPS / 7 ms `13 88 08` full-keyboard grouped RGB path.

The current implementation includes:

- wireless discovery
- native RGB encoding
- HID report packetization
- Windows HID transport
- device wrapper
- dynamic RGB stream timing
- static RGB keepalive timing

Integration of arbitrary per-key wireless RGB, additional native transaction formats, and official dynamic-effect decoding remains future work.

---

## What is not established

The following remain open:

- true maximum reliable wireless FPS
- whether a different scheduling strategy can improve smoothness
- whether 14 FPS is a firmware/receiver ceiling
- complete semantics of every native stream byte
- complete semantics of every possible `XX`
- which smaller transaction sizes are appropriate for specific RGB operations
- whether a different valid grouping provides better visual output
- complete relationship between all official RGB effect formats and the full-frame grouped path
- whether the current grouped representation is optimal for arbitrary per-key RGB input
- complete wireless initialization/state requirements

Therefore:

> **14 FPS / 7 ms is a validated operating point, not a claim that the protocol cannot run faster or smoother.**
