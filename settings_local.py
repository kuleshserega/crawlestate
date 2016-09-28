import os


DB_NAME = os.environ.get('DB_NAME', 'estate_db')
DB_USER = os.environ.get('DB_USER', 'estate_user')
DB_PASSWD = os.environ.get('DB_PASSWD', 'estatepswrd')
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')


SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s' % (
    DB_USER,
    DB_PASSWD,
    DB_HOST,
    DB_NAME
)
