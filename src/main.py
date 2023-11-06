import uasyncio
from device_controller.slot_controller import SlotController
from radio_driver.radio_controller import RadioController
from can_driver.can.can_controller import CANController
from radio_driver.SI4463 import SI4463
from machine import Pin
from device_controller.device_config import DeviceConfig
import gc
import time



def start_led_opening():
    led = Pin("LED", Pin.OUT)
    for i in range(3):
        led.value(1)
        time.sleep(0.5)
        led.value(0)
        time.sleep(0.5)


async def main():
    print('started main')
    slot_controller = SlotController()
    slot_controller.initialize()

    # VAR 2
    radio_controller = RadioController()
    radio_controller.initialize()
    radio_controller.start_rx()


#     can_controller = CANController()
#     can_controller.initialize()

    start_led_opening()
    watchdog_refresh_counter = 0

    while True:
        await uasyncio.sleep_ms(2000)
        watchdog_refresh_counter += 1
        if watchdog_refresh_counter % 5 == 0:
            print("Free RAM memory : {}".format(gc.mem_free()))


if __name__ == "__main__":
    uasyncio.run(main())






