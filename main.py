import time
from machine import Pin, SPI

spi = SPI(1, baudrate=100_000, polarity=0, phase=0, sck=Pin(14, Pin.OUT), mosi=Pin(15, Pin.OUT), miso=Pin(12, Pin.IN))

# crystal gpio
#      2 3
# tx - 0 1
# rx - 1 0
mode_2 = Pin(6, Pin.OUT)
mode_3 = Pin(4, Pin.OUT)


def set_tx_mode():
    mode_2.low()
    mode_3.high()


def set_rx_mode():
    mode_2.high()
    mode_3.low()


set_tx_mode()

buf = b'\xde\xad\xbe\xed'
print(buf)

led = Pin(25, Pin.OUT)
led.low()

while True:
    # spi.write()

    led.high()
    time.sleep(0.5)
    led.low()
    time.sleep(0.5)
