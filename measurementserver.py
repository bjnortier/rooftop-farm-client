#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
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
        `sensor_id` VARCHAR(255),
        `type` VARCHAR(255),
        `timestamp` DATETIME NOT NULL,
        `data` VARCHAR(2048) NOT NULL)
    """)
    data = cur.fetchone()

    while True:
        msg = socket.recv_json()
        for sensor_id in msg:
            m1 = msg[sensor_id]
            m2 = (
                sensor_id, m1['timestamp'], m1['type'], json.dumps(m1['data'])
            )
            print(m2)
            cur.execute("""
                INSERT INTO `measurements`
                (`id`, `sensor_id`, `timestamp`, `type`, `data`)
                VALUES
                (NULL, ?, ?, ?, ?)
            """, m2)
            con.commit()
        socket.send_string('ACK')

except lite.Error as e:
    print("Error %s:" % e.args[0])
    sys.exit(1)
finally:
    if con:
        con.close()
