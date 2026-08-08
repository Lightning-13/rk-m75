\# RK M75 2.4 GHz Reverse Engineering



Experimental reverse-engineering workspace for investigating RGB control

of the RK M75 over its 2.4 GHz wireless connection.



\## Status



Experimental. Nothing in this directory is part of the stable RK M75

library yet.



The stable wired RGB implementation remains in `rkm75/`.



\## Goals



\- Identify the RK M75 2.4 GHz receiver interface.

\- Enumerate its HID interfaces and report descriptors.

\- Determine how the official software communicates with the receiver.

\- Capture and analyze RGB traffic.

\- Determine whether the wireless RGB protocol differs from the wired protocol.

\- Determine whether the existing 81-key RGB mapping applies.

\- Determine update-rate and keepalive requirements.

\- Build a minimal experimental implementation only after the protocol is understood.



\## Rules



\- Do not modify the stable `rkm75/` implementation during initial investigation.

\- Do not assume the wired RGB protocol applies to 2.4 GHz.

\- Record observations and captures before drawing conclusions.

\- Keep experimental scripts isolated under `2.4ghz/`.

\- Do not merge experimental code into `main` until it has been validated.



\## Directory Layout



\- `captures/` — raw captures and extracted reports

\- `scripts/` — investigation and enumeration utilities

\- `experiments/` — temporary protocol experiments

\- `reports/` — generated analysis

\- `docs/` — findings and protocol notes