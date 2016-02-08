import sys
import zmq
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
                'sensor_id': config['id'],
                'type': config['type'],
                'timestamp': time.time() * 1000,  # 1970 ms
                'data': {
                    'value': value,
                }
            }
    return result


def connect_and_push():
    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:%s" % port)
    while True:
        socket.send_json(read_channels())
        msg = socket.recv()
        print('.', end='')
        sys.stdout.flush()
        time.sleep(1)

while True:
    time.sleep(1)
    connect_and_push()
