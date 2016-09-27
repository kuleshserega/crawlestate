from flask import Flask, render_template, url_for, redirect, \
    session, request, jsonify

from settings import DB_NAME, DB_USER, DB_PASSWD, DB_HOST

from models import db
from models import Property, Spider


app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'c0derunner'

app.config.update({
    'SQLALCHEMY_DATABASE_URI': 'postgresql://%s:%s@%s/%s' % (
        DB_USER,
        DB_PASSWD,
        DB_HOST,
        DB_NAME
    ),
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
})
db.init_app(app)


@app.route('/')
def index():
    plist = []
    results = Property.query.all()
    if results:
        for result in results:
            plist.append({
                'id': result.id,
                'spider_name': result.spider.name,
                'location': result.location,
                'year_duration': result.year_duration,
                'unit_floor': result.unit_floor,
                'building_age': result.building_age,
                'number_of_units': result.number_of_units,
                'building_type': result.building_type,
                'gross_price': result.gross_price,
                'net_price': result.net_price,
            })

    return render_template('index.html', data=plist)


@app.route('/spiders')
def spiders():
    slist = []
    results = Spider.query.all()
    if results:
        for result in results:
            slist.append({
                'id': result.id,
                'spider_name': result.name,
            })

    return render_template('spiders.html', data=slist)


if __name__ == '__main__':
    import os
    os.environ['DEBUG'] = 'true'
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', port=8001)
