# ESP32Play

MicroPython experiments on an **ESP32-C3** — a couple of small scripts for
driving an LED, kept as a scratchpad for learning the board.

## Hardware

Both scripts assume one LED on **GPIO5**, wired:

```
GPIO5 -> resistor (~220-330R) -> LED anode (+)
LED cathode (-) -> GND
```

Change `LED_PIN` at the top of either script to use a different pin. On the
C3, keep to GPIO0-21 and avoid GPIO2, GPIO8 and GPIO9 — those are strapping
pins sampled at boot, and driving them can stop the board starting.

## Scripts

| Script | What it does |
| --- | --- |
| `blink.py` | Blinks the LED on and off at a fixed interval. |
| `fade.py` | Fades the LED in and out with PWM, using a gamma-corrected ramp so the sweep looks linear to the eye. |

Both exit cleanly on Ctrl-C at the REPL, leaving the LED off.

## Setup

Host-side tooling (`esptool`, `mpremote`) lives in a virtualenv:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install esptool mpremote
```

A virtualenv hardcodes its own path, so it breaks if the project directory is
renamed or moved. Delete `.venv` and repeat the above if that happens — it is
gitignored precisely because it isn't portable.

## Flashing MicroPython

Only needed once, or when upgrading. Download the **`ESP32_GENERIC_C3`** build
from [micropython.org](https://micropython.org/download/ESP32_GENERIC_C3/) —
the plain `ESP32_GENERIC` build targets the dual-core Xtensa ESP32 and will
not boot on a C3.

The C3 has native USB, so it appears as `/dev/cu.usbmodem*` rather than the
`/dev/cu.usbserial-*` you get from a CP210x or CH340 bridge:

```sh
ls /dev/cu.usbmodem*                      # find the port
esptool --chip esp32c3 --port <port> erase-flash
esptool --chip esp32c3 --port <port> --baud 460800 \
    write-flash 0x0 ESP32_GENERIC_C3-<version>.bin
```

Note the `0x0` offset — the original ESP32 flashes at `0x1000`, the C3 at `0x0`.

## Running

Run a script on the board without writing it to flash:

```sh
mpremote run blink.py
```

Or copy it over so it starts on every boot:

```sh
mpremote cp fade.py :main.py
```

`mpremote repl` drops into the REPL; Ctrl-] exits.
