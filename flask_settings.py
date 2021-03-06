import os


DB_NAME = os.environ.get('DB_NAME', 'db')
DB_USER = os.environ.get('DB_USER', 'db_user')
DB_PASSWD = os.environ.get('DB_PASSWD', 'dbpswrd')
DB_HOST = os.environ.get('DB_HOST', '172.17.42.1')

BASE_SCRAPYD_URL = 'http://localhost:6800/%s'
BASE_SCRAPYD_URL_AJAX = 'http://localhost:6800/'
RUN_SPIDER = 'schedule.json'

BASE_SITE_URL = 'http://localhost:8008/'

SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s' % (
    DB_USER,
    DB_PASSWD,
    DB_HOST,
    DB_NAME
)

from settings_local import *
