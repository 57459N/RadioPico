import time

from machine import Pin
from _thread import allocate_lock, start_new_thread
from sys import exit
from e10_433 import E10_433


led = Pin(25, Pin.OUT)
led.low()

spLock = allocate_lock()


def thread1():
    rf_rx = E10_433(spi_id=0,
                    mode2=Pin(20, Pin.OUT),
                    mode3=Pin(21, Pin.OUT),
                    chip_select=Pin(5, Pin.OUT),
                    baudrate=100_000,
                    polarity=0,
                    phase=0,
                    sck=Pin(2, Pin.OUT),
                    mosi=Pin(7, Pin.OUT),
                    miso=Pin(16, Pin.IN))

    packet_len = 16
    while True:
        try:
            if spLock.locked():
                exit()

            data = rf_rx.read(packet_len)
            print(data)
            time.sleep(0.1)
        except KeyboardInterrupt:
            exit()


def thread0():
    rf_tx = E10_433(spi_id=1,
                    mode2=Pin(6, Pin.OUT),
                    mode3=Pin(4, Pin.OUT),
                    chip_select=Pin(13, Pin.OUT),
                    baudrate=100_000,
                    polarity=0,
                    phase=0,
                    sck=Pin(14, Pin.OUT),
                    mosi=Pin(15, Pin.OUT),
                    miso=Pin(12, Pin.IN))

    buf = b'\xde\xad\xbe\xef'
    print(buf)

    while True:
        try:
            rf_tx.write(buf)

        except KeyboardInterrupt as e:
            spLock.acquire()
            raise e


start_new_thread(thread1, ())
thread0()
