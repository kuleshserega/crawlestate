from math import ceil


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


def get_proxy_from_db():
    import psycopg2

    from flask_settings import DB_NAME, DB_USER, DB_PASSWD, DB_HOST

    PROXY_LIST = []

    sql_request = "SELECT * FROM proxy WHERE status = 'Works'"
    conn = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWD,
        host=DB_HOST)
    cursor = conn.cursor()
    cursor.execute(sql_request)
    results = cursor.fetchall()
    for row in results:
        PROXY_LIST.append(
            '%s://%s:%s' % (row[1], row[2], row[3]))
    conn.close()

    return PROXY_LIST
