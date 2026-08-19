# RK M75 2.4 GHz Reverse-Engineering Findings

## Current status

The RK M75 2.4 GHz RGB protocol is **working but not completely reverse-engineered**.

We now have a validated full-keyboard RGB transport using the recovered six-group representation. The transport has been implemented as a reusable wireless backend and validated against the physical keyboard.

The remaining questions around maximum performance, exact field semantics, alternative groupings, arbitrary per-key RGB, official effect formats, and some transient visual behavior are still open.

This document preserves the research history and the reasoning behind the current implementation.

---

## 1. Initial receiver identification

The receiver was identified as:

- VID `0x258A`
- PID `0x0148`
- SINO WEALTH / Gaming KB
- relevant RGB HID collection `FF02/0002`
- report ID `0x13`

The receiver exposes multiple HID collections.

---

## 2. Passive HID monitoring

Passive monitoring of the relevant collection did not reveal useful RGB input traffic during ordinary keyboard use or hardware RGB changes.

This established that the useful RGB control path was not simply ordinary input-report traffic on that collection.

---

## 3. Official software RGB traffic

USBPcap/Wireshark captures showed that the official RK software controls the wireless RGB through HID `SET_REPORT` traffic.

Early captures established:

- 20-byte HID reports
- report ID `0x13`
- `13 88` header
- additive report checksum
- single-report per-key RGB traffic
- multi-report RGB traffic

These observations established the basis for the later transaction-family and native-stream investigations.

---

## 4. LED mapping

Individual wireless RGB captures for keys including ESC, A, W, M, SPACE, and ENTER matched the existing wired LED mapping.

This strongly supports a shared logical/native LED index space between wired and 2.4 GHz operation.

The mapping was subsequently used when reconstructing the full-keyboard native RGB representation.

This does **not** by itself prove that every wireless RGB representation uses exactly the same encoding or grouping.

---

## 5. `13 88 XX` discovery

The wireless RGB traffic was investigated as a common transaction family:

```text
13 88 XX
```

Later multi-report experiments established the working interpretation:

```text
XX = number of 20-byte HID reports in the transaction
```

This supersedes the earlier working terminology that treated the third byte simply as a command identifier.

Examples tested include:

```text
13 88 07
13 88 08
13 88 09
13 88 0A
```

These observations demonstrate that the third byte participates in the transaction/report-count structure.

They do **not** establish that every possible `XX` value is supported by the firmware.

---

## 6. Native full-keyboard stream reconstruction

The validated `13 88 08` path reconstructs a 105-byte native RGB stream.

The stream contains six RGB records:

```text
RGB + LED count + LED indices
```

with recovered group sizes:

```text
14, 15, 15, 14, 13, 10
```

The records contain 81 unique native LED indices.

The stream was packetized into eight 20-byte HID reports.

For every generated transaction we validate:

- 105-byte native stream
- 8 reports
- 20-byte report size
- sequence numbers
- payload lengths
- additive checksums
- exact stream reconstruction

The resulting transaction has been transmitted successfully to the physical keyboard and produces stable full-keyboard grouped RGB output.

### Important limitation

The six native records are currently treated as RGB control groups.

This means the recovered `13 88 08` representation provides full-keyboard coverage, but it does **not** yet provide arbitrary independent RGB control for every one of the 81 keys.

That distinction is important: **full-keyboard coverage is not the same as complete arbitrary per-key RGB support.**

---

## 7. Group-count experiments

The `13 88 08`, `13 88 09`, and `13 88 0A` paths were explored by changing the number and arrangement of RGB groups while preserving 81-key coverage.

These experiments demonstrated that larger transaction/report counts can carry larger native streams.

They did **not** establish that every possible grouping is semantically equivalent or visually optimal.

They also do not establish that a larger transaction is automatically better for every RGB effect.

The experiments therefore remain research evidence rather than production configuration.

---

## 8. Physical topology experiments

The native LED list was tested using physical row-band and column-oriented groupings.

Findings:

- some groupings were stable but produced visibly stepped or split transitions
- some groupings produced brief flashes
- group count alone did not guarantee smooth visual motion
- physical coherence matters to the visual result

This is one reason the current implementation preserves the recovered validated six-group native structure rather than dynamically inventing group topologies.

However, the current six-group structure should still be considered a validated representation, not a proven optimal representation.

---

## 9. Frame-rate experiments

The full-keyboard `13 88 08` path was tested at multiple frame rates.

The practical result was:

```text
14 FPS -> selected stable baseline
15 FPS -> generally stable in testing, but not selected
16-17 FPS -> increasingly frequent visible flashes
```

The exact maximum reliable frame rate has not been established.

Therefore 14 FPS is documented as:

> **highest currently selected stable baseline**

and not:

> **maximum supported FPS**

The existing hardware smoke test also confirms that the cleaned library implementation can sustain 14 FPS successfully on the physical keyboard.

---

## 10. Inter-report timing experiments

The inter-report gap was varied across multiple experiments.

The project observed that more aggressive timing can increase the probability of transient visual errors.

A 7 ms gap was selected as the conservative baseline.

The exact mechanism behind the timing sensitivity has not been isolated.

Therefore 7 ms should be treated as a validated operating point rather than a proven firmware requirement.

---

## 11. Frame duplication experiment

Each generated RGB state was transmitted twice:

```text
A A
B B
C C
...
```

This did not improve the perceived smoothness.

The experiment is retained as negative evidence and is not part of the implementation.

---

## 12. Frame-to-frame timing diagnostic

A dedicated 14 FPS timing diagnostic measured:

- complete HID transaction time
- actual frame-to-frame interval
- scheduler sleep time

The frame period remained close to the 71.429 ms target with no detected large timing anomalies in the diagnostic output.

Brief flashes could still occur without a corresponding scheduler anomaly.

This indicates that at least some observed flashes cannot be explained solely by a large host-side frame timing spike.

The underlying cause remains unresolved.

---

## 13. Keepalive experiments

Stopping RGB transmission allows the keyboard's own RGB behavior to reclaim control.

Static keepalive rates were tested.

Observed practical behavior:

```text
5 FPS -> very stable
2 FPS -> very stable
1 FPS -> RGB takeover/off
```

The selected implementation baseline is therefore:

```text
5 FPS static keepalive
7 ms inter-report gap
```

The keepalive retransmits the same RGB state rather than generating a new animation frame.

The 5 FPS value is therefore a selected reliability margin, not a proven minimum firmware requirement.

---

## 14. Animation / keepalive transitions

Longer animation-to-keepalive-to-animation testing showed occasional very brief flashes around some cycle boundaries.

These were not reproducibly explained by a large host-side timing anomaly.

No speculative transition workaround was accepted into the implementation.

The behavior remains an open research question.

---

## 15. Official Dynamic Breathing capture

The official software also provided a captured seven-report RGB effect using `13 88 07`.

Dynamic Breathing is a single-color effect: the keyboard displays one overall color at a time.

The capture is therefore useful as protocol evidence, but it should not be used to infer that `13 88 07` is a better representation for our multicolor full-keyboard wave.

The official capture is retained for future protocol analysis.

---

## 16. Current validated implementation

The current reusable wireless backend is:

```text
rkm75/wireless/
```

The validated RGB path is:

```text
Frame
  ↓
six-group RGB representation
  ↓
105-byte native stream
  ↓
13 88 08 transaction
  ↓
8 x 20-byte HID reports
  ↓
RK M75 2.4 GHz receiver
```

The current operating baseline is:

```text
13 88 08
105-byte native stream
8 x 20-byte HID reports
81 native LED indices
7 ms inter-report gap
14 FPS dynamic baseline
5 FPS static keepalive
```

The implementation has been validated on the physical keyboard and produces smooth, stable output at the selected 14 FPS baseline.

The transport and effect generation are kept separate so future work can experiment with other RGB representations without rewriting the HID packetization layer.

---

## 17. Confidence boundaries

The current state should be understood in three categories.

### Validated

The following are directly implemented, tested, and successfully exercised on the physical keyboard:

- receiver identification
- relevant HID collection
- 20-byte report structure
- `13 88 08` full-keyboard grouped transaction
- 105-byte native stream
- six native RGB records
- 81 unique native LED indices
- report sequence numbering
- payload-length field
- additive checksum
- exact report reconstruction
- 14 FPS / 7 ms dynamic operating baseline
- 5 FPS / 7 ms static keepalive baseline

### Strongly supported but not complete

The following have substantial experimental support but should not be treated as completely decoded:

- `13 88 XX` as a report-count transaction family
- relationship between the native group representation and physical keyboard topology
- behavior of other transaction sizes
- relationship between grouped RGB traffic and official effect formats
- the precise firmware behavior responsible for timing sensitivity

### Unknown / unresolved

The following remain open:

- true maximum reliable wireless FPS
- whether 15 FPS can be made consistently better with another scheduler
- whether a different inter-report strategy improves smoothness
- whether the occasional flashes are caused by firmware, receiver, USB/HID, or host scheduling behavior
- complete semantics of all native stream fields
- complete semantics of every possible `XX`
- whether the six-group representation is optimal
- complete support for arbitrary per-key RGB input
- complete decoding of official dynamic effects
- complete wireless initialization/state requirements

---

## Current conclusion

The 2.4 GHz RGB path is no longer merely a capture-analysis exercise.

We have a **validated working full-keyboard grouped RGB transport**.

The cleaned implementation is now part of the repository under `rkm75/wireless/`, and its protocol, encoder, transport, device, and stream behavior are covered by automated tests.

However, the protocol is **not considered completely reverse-engineered**.

The current 14 FPS / 7 ms configuration should be treated as a stable engineering baseline rather than a proven performance ceiling, and the current six-group representation should not be treated as the final solution for arbitrary per-key RGB or all wireless effects.
