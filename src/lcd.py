from machine import Pin, I2C
from machine_i2c_lcd import I2cLcd


class Lcd:

    def __init__(self, bus: int, sda: Pin, scl: Pin, freq: int, device: int):
        self.bus = bus
        self.sda = sda
        self.scl = scl
        self.freq = freq
        self.device = device
        self.i2c = I2C(self.bus, sda=self.sda, scl=self.scl, freq=self.freq)
        self.lcd = I2cLcd(self.i2c, self.get_i2c_bus_address(self.device), 2, 16)

    def get_i2c_bus_address(self, device: int):
        return self.i2c.scan()[device]
