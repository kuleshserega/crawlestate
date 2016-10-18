from math import ceil

import psycopg2

from flask_settings import DB_NAME, DB_USER, DB_PASSWD, DB_HOST


def pagination(page, total_count, per_page):
    pagination = {}
    pagination['previous_page'] = page - 1
    if not pagination['previous_page']:
        pagination['previous_page'] = None

    pagination['current_page'] = page

    pagination['next_page'] = None

    pages_count = ceil(float(total_count)/per_page)

    if pages_count > page:
        pagination['next_page'] = page + 1
        pagination['pages_count'] = pages_count

    return pagination


def get_proxy_from_db(proxy_status=None):
    PROXY_LIST = {}
    sql_request = "SELECT * FROM proxy"
    if proxy_status:
        sql_request += " WHERE status = '%s'" % proxy_status
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute(sql_request)
    results = cursor.fetchall()
    for row in results:
        PROXY_LIST[row[0]] = '%s://%s:%s' % (row[1], row[2], row[3])
    conn.close()

    return PROXY_LIST


def set_proxy_status(id, status):
    sql_request = "UPDATE proxy SET status = '%s' WHERE id = %d" % (status, id)
    try:
        conn = get_connect()
        cursor = conn.cursor()
        cursor.execute(sql_request)
        conn.commit()
    except Exception, e:
        print e
    conn.close()


def get_connect():
    conn = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWD,
        host=DB_HOST)
    return conn
