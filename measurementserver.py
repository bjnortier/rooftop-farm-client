#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
import random
import sys
import time
import sqlite3 as lite
import json

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

try:
    con = lite.connect('measurements.db')
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS `measurements` (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `timestamp` DATETIME NOT NULL,
        `type` VARCHAR(255),
        `data` VARCHAR(2048) NOT NULL)
    """)
    data = cur.fetchone()

    while True:
        msg = socket.recv_json()
        print(msg)
        measurement = (msg['timestamp'], msg['type'], msg['data'])
        cur.execute("""
            INSERT INTO `measurements`
            (`id`, `timestamp`, `type`, `data`)
            VALUES
            (NULL, ?, ?, ?)
        """, measurement)
        con.commit()
        socket.send_string('ACK')

except lite.Error as e:
    print("Error %s:" % e.args[0])
    sys.exit(1)
finally:
    if con:
        con.close()
