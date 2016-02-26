import sys
import spidev
import time
import os

spi = spidev.SpiDev()
spi.open(0, 0)


def read_channel(channel):
    adc = spi.xfer2([1, (8+channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return round(data/1023, 3)


while True:
    values = list(map(lambda x: read_channel(x), range(8)))
    print(values)
    time.sleep(1)
