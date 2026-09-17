# ESP32Play

MicroPython experiments on an ESP32. A learning scratchpad, not a library —
small self-contained scripts, no package structure.

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

## Hardware

One LED on **GPIO5**: `GPIO5 -> ~220-330R resistor -> LED(+)`, `LED(-) -> GND`.

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
