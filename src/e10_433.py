from machine import SPI, Pin


class E10_433:
    def __init__(self, spi_id: int, mode2: Pin, mode3: Pin, chip_select: Pin, **kwargs):
        self.spi = SPI(spi_id, **kwargs)
        self._mode = None
        self.mode2 = mode2
        self.mode3 = mode3
        self.cs = chip_select

    def set_mode(self, is_tx: bool = True):
        # crystal gpio
        #      2 3
        # tx - 0 1
        # rx - 1 0

        if self._mode == is_tx:
            return

        if is_tx:
            self.mode2.low()
            self.mode3.high()
        else:
            self.mode2.high()
            self.mode3.low()

        self._mode = is_tx

    def mode(self) -> bool:
        """
        :return: True if TX  False if RX
        """
        return self._mode

    def write(self, buf) -> int | None:
        """
        :param buf:  AnyReadableBuf
        :return: None
        """
        self.set_mode(True)

        self.cs.low()
        res = self.spi.write(buf)
        self.cs.high()
        return res

    def read(self, nbytes: int, write: int = 0x00) -> bytes:
        self.set_mode(False)

        self.cs.low()
        data = self.spi.read(nbytes, write)
        self.cs.high()
        return data
