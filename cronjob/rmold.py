# -*- coding: utf-8 -*-
import os
import sys
import datetime

import psycopg2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_settings import DB_NAME, DB_USER, DB_PASSWD, DB_HOST


def remove_old_data():
    dt = (datetime.datetime.utcnow() - datetime.timedelta(hours=2)).strftime(
        '%Y-%m-%d %H:%M:%S')
    print 'DATE TIME:', dt
    sql_request = "DELETE FROM property where date_created < '%s'" % dt
    conn = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWD,
        host=DB_HOST)
    cursor = conn.cursor()
    cursor.execute(sql_request)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    remove_old_data()
