import os


DB_NAME = os.environ.get('DB_NAME', 'db')
DB_USER = os.environ.get('DB_USER', 'db_user')
DB_PASSWD = os.environ.get('DB_PASSWD', 'dbpswrd')
DB_HOST = os.environ.get('DB_HOST', '172.17.42.1')


from settings_local import *
