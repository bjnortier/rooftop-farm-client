#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import sqlite3 as lite
import json
import requests

try:
    con = lite.connect('measurements.db')
    cur = con.cursor()

    while True:
        cur.execute('SELECT id, type, timestamp, data FROM measurements LIMIT 50')
        rows = cur.fetchall()

        payload = list(map(lambda x: {
            'type': x[1],
            'timestamp': x[2],
            'data': x[3],
        }, rows))
        print(payload)
        r = requests.post('http://localhost:3000/api/measurements', json=payload)
        print(r)

        ids = list(map(lambda x: str(x[0]), rows))
        print(ids)
        cur.execute('DELETE FROM measurements WHERE id in (' + ','.join(ids) + ')');
        con.commit()

        time.sleep(5)

except lite.Error as e:
    print("Error %s:" % e.args[0])
    sys.exit(1)
finally:
    if con:
        con.close()
