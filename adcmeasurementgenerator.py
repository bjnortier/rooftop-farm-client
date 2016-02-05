import spidev
import time
import os

spi = spidev.SpiDev()
spi.open(0, 0)

CONFIG = {
    0: {
        'type': 'MOISTURE',
        'id': 'moist_a',
    }
}


def read_channel(channel):
    adc = spi.xfer2([1, (8+channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data/1013


def read_channels():
    result = {}
    for channel in range(8):
        if channel in CONFIG:
            config = CONFIG[channel]
            value = read_channel(channel)
            result[config['id']] = {
                'type': config['type'],
                'timestamp': time.time(),
                'value': value
            }
    return result

while True:
    result = read_channels()
    print(result)
    time.sleep(1)
