import time
from machine import Pin



led = Pin(25, Pin.OUT)
led.low()

while True:
    led.high()
    time.sleep(0.25)
    led.low()
    time.sleep(0.25)