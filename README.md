# ESP32Play

MicroPython experiments on an ESP32 — a couple of small scripts for driving an
LED, kept as a scratchpad for learning the board.

## Hardware

Both scripts assume one LED on **GPIO5**, wired:

```
GPIO5 -> resistor (~220-330R) -> LED anode (+)
LED cathode (-) -> GND
```

Change `LED_PIN` at the top of either script if yours is on a different pin.

## Scripts

| Script | What it does |
| --- | --- |
| `blink.py` | Blinks the LED on and off at a fixed interval. |
| `fade.py` | Fades the LED in and out with PWM, using a gamma-corrected ramp so the sweep looks linear to the eye. |

Both exit cleanly on Ctrl-C at the REPL, leaving the LED off.

## Running

The board needs [MicroPython](https://micropython.org/download/) flashed first.
Host-side tooling (`esptool`, `mpremote`) lives in a virtualenv:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install esptool mpremote
```

Then run a script on the board without copying it to flash:

```sh
mpremote run blink.py
```

Or copy it over and have it start at boot:

```sh
mpremote cp fade.py :main.py
```
