#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import sqlite3 as lite
import json
import requests


def post_payload(payload):
    try:
        r = requests.post(
            os.environ['POST_API_URL'] + '/measurements',
            json=payload)
        print(r)
        if r.status_code == 201:
            delete_ids(ids)
    except requests.exceptions.ConnectionError as e:
        print('!!! connection error')


def delete_ids(ids):
    print("deleting: %s rows" % len(ids))
    cur.execute('DELETE FROM measurements WHERE id in (' + ','.join(ids) + ')')
    con.commit()

try:
    con = lite.connect('measurements.db')
    cur = con.cursor()

    while True:
        cur.execute("""
            SELECT id,
                   sensor_id,
                   type,
                   timestamp,
                   data
            FROM measurements
            LIMIT 50
            """)
        rows = cur.fetchall()

        ids = list(map(lambda x: str(x[0]), rows))
        payload = list(map(lambda x: {
            'sensor_id': x[1],
            'type': x[2],
            'timestamp': x[3],
            'data': x[4],
        }, rows))
        if len(payload) > 0:
            post_payload(payload)
        time.sleep(5)

except lite.Error as e:
    print("Error %s:" % e.args[0])
    sys.exit(1)
finally:
    if con:
        con.close()
