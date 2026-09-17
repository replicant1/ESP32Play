# Blink an LED wired: GPIO5 -> resistor -> LED(+) ... LED(-) -> GND
from machine import Pin
from time import sleep

LED_PIN = 5
INTERVAL = 0.5  # seconds on, seconds off

led = Pin(LED_PIN, Pin.OUT)

try:
    while True:
        led.value(1)
        sleep(INTERVAL)
        led.value(0)
        sleep(INTERVAL)
except KeyboardInterrupt:
    # Ctrl-C at the REPL: leave the LED off rather than stuck on.
    led.value(0)
    print("stopped")
