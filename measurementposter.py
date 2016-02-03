#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import sqlite3 as lite
import json

try:
    con = lite.connect('measurements.db')
    cur = con.cursor()

    while True:
        cur.execute('SELECT * FROM measurements LIMIT 50')
        rows = cur.fetchall()
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
