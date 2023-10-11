import time

from machine import Pin
from _thread import allocate_lock, start_new_thread
from sys import exit
from e10_433 import E10_433

mode_2 = Pin(6, Pin.OUT)
mode_3 = Pin(4, Pin.OUT)
cs = Pin(13, Pin.OUT)

rf1 = E10_433(spi_id=1, mode2=mode_2, mode3=mode_3, chip_select=cs,
              baudrate=100_000,
              polarity=0,
              phase=0,
              sck=Pin(14, Pin.OUT),
              mosi=Pin(15, Pin.OUT),
              miso=Pin(12, Pin.IN))

buf = b'\xde\xad\xbe\xef'
print(buf)

led = Pin(25, Pin.OUT)
led.low()

spLock = allocate_lock()


def thread1():
    while True:
        if spLock.locked():
            exit()

        print('core 1')
        time.sleep(1)


def thread0():
    while True:
        try:
            print('core 0')
            time.sleep(1)
        except KeyboardInterrupt as e:
            spLock.acquire()
            raise e


start_new_thread(thread1, ())
thread0()

while True:
    rf1.write(buf)
    print(buf)

    led.high()
    time.sleep(0.5)
    led.low()
    time.sleep(0.5)
