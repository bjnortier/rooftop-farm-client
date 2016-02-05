#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
import sys
import time


def connect_and_push():
    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:%s" % port)
    while True:
        socket.send_json({
            'type': 'moisture',
            'timestamp': time.time(),
            'data': '{"value": 78.0}"'
        })
        msg = socket.recv()
        print('.', end='')
        sys.stdout.flush()
        time.sleep(1)

while True:
    try:
        time.sleep(1)
        connect_and_push()
    except zmq.error.ZMQError as e:
        print(e)
