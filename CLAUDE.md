# ESP32Play

MicroPython experiments on an **ESP32-C3**. A learning scratchpad, not a
library — small self-contained scripts, no package structure.

## This is MicroPython, not CPython

The `.py` files in the repo root run **on the board**, not on this machine.
That constrains things in ways worth stating up front:

- `machine`, `time.sleep_ms`, etc. only exist on the device. These scripts
  cannot be run or imported on the host — don't try to execute them here to
  "check" them, and don't write host-side unit tests against them.
- The board has no `pip` and only a subset of the stdlib. Never add an import
  without confirming MicroPython ships it.
- `.venv/` is **host-side tooling only** (`esptool`, `mpremote`). Nothing in it
  is available to code running on the board. It's gitignored.

## Board: ESP32-C3

Single-core RISC-V, not the dual-core Xtensa of the original ESP32. Most of
what's written for "ESP32" applies, but these differ and have bitten before:

- **Firmware is `ESP32_GENERIC_C3`**, not `ESP32_GENERIC`. The Xtensa build
  will not boot on this chip. Flash with `esptool --chip esp32c3 ...`.
- **GPIO0-21 only.** Pin numbers above 21 in a tutorial mean it was written
  for a different chip; translate, don't copy.
- **Avoid GPIO2, GPIO8, GPIO9** for output — they're strapping pins read at
  boot, and driving them can stop the board coming up. GPIO9 is usually the
  BOOT button. On many C3 boards GPIO8 also has an onboard RGB LED.
- **PWM: 6 LEDC channels, low-speed only** (the original ESP32 has 16 across
  two speed modes). Fine for one LED; a constraint if this grows. MicroPython
  still presents 16-bit duty via `duty_u16` and scales internally.
- **Native USB Serial/JTAG on GPIO18/19** — no CP210x or CH340 bridge, so the
  board enumerates as `/dev/cu.usbmodem*`, not `/dev/cu.usbserial-*`. Don't
  conclude nothing is plugged in from the absence of a `usbserial` device.

## Hardware

One LED on **GPIO5**: `GPIO5 -> ~220-330R resistor -> LED(+)`, `LED(-) -> GND`.
GPIO5 is a plain GPIO on the C3 — not strapping, safe to drive at boot.

Scripts define `LED_PIN` as a constant at the top rather than inlining the pin
number, so a rewiring is a one-line change.

## Deploying

```sh
source .venv/bin/activate
mpremote run blink.py      # run once, nothing written to flash
mpremote cp fade.py :main.py   # persist; runs on every boot
```

`mpremote run` is the default for iterating. Only write `main.py` when the
intent is for the board to do something standalone on power-up.

## Conventions

- Scripts handle `KeyboardInterrupt` and leave hardware in a safe idle state on
  exit — LED off, PWM deinitialized. A script that leaves a pin driving after
  Ctrl-C is a bug.
- Tunables (pin, frequency, timing, gamma) are named constants at the top.
- Comments explain *why* a value or approach was chosen — e.g. gamma correction
  in `fade.py` — not what the line does.

## Repo

Public at https://github.com/replicant1/ESP32Play under the `replicant1`
account. `.venv/` is excluded; the README covers recreating it.
