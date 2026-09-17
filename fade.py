# Fade an LED in and out, wired: GPIO5 -> resistor -> LED(+) ... LED(-) -> GND
from machine import Pin, PWM
from time import sleep_ms

LED_PIN = 5
FREQ = 1000      # Hz; well above the eye's flicker threshold
STEPS = 256      # brightness levels per sweep
STEP_MS = 8      # ~2s per sweep, ~4s for a full in-and-out cycle
GAMMA = 2.2

led = PWM(Pin(LED_PIN), freq=FREQ, duty_u16=0)

# The eye responds to brightness logarithmically, so a linear duty sweep looks
# like it snaps bright then stalls. Pre-computing a gamma-corrected ramp once
# keeps the loop to a table lookup.
ramp = [int(65535 * (i / (STEPS - 1)) ** GAMMA) for i in range(STEPS)]

try:
    while True:
        for duty in ramp:
            led.duty_u16(duty)
            sleep_ms(STEP_MS)
        for duty in reversed(ramp):
            led.duty_u16(duty)
            sleep_ms(STEP_MS)
except KeyboardInterrupt:
    # Release the PWM peripheral, or it keeps driving the pin after we exit.
    led.duty_u16(0)
    led.deinit()
    Pin(LED_PIN, Pin.OUT).value(0)
    print("stopped")
