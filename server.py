from math import ceil

from flask import Flask, render_template, url_for, redirect, \
    session, request, jsonify

from settings import SQLALCHEMY_DATABASE_URI

from models import db
from models import Property, Spider


app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'c0derunner'

app.config.update({
    'SQLALCHEMY_DATABASE_URI': SQLALCHEMY_DATABASE_URI,
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
})
db.init_app(app)

COUNT_PER_PAGE = 10


@app.route('/results/', defaults={'page': 1})
@app.route('/results/<int:page>')
def index(page):
    plist = []
    total_count = Property.query.count()
    pagination = {}
    pagination['previous_page'] = page - 1
    if not pagination['previous_page']:
        pagination['previous_page'] = None

    pagination['current_page'] = page

    pagination['next_page'] = None
    print total_count
    pages_count = ceil(float(total_count)/COUNT_PER_PAGE)
    print 'pages_count', pages_count
    if pages_count > page:
        pagination['next_page'] = page + 1

    results = Property.query.paginate(page, COUNT_PER_PAGE, False).items
    if results:
        for result in results:
            plist.append({
                'id': result.id,
                'spider_name': result.spider.name,
                'location': result.location,
                'unit_floor': result.unit_floor,
                'building_age': result.building_age,
                'number_of_units': result.number_of_units,
                'building_type': result.building_type,
                'gross_price': result.gross_price,
                'net_price': result.net_price,

                'date': result.date,
                'buildling': result.buildling,
                'size': result.size,
                'ft_price': result.ft_price,
                'op_type': result.op_type,
                'price': result.price,
                'data_source': result.data_source,

                'image_url': result.image_url,
                'about_the_flatshare': result.about_the_flatshare,
                'who_lives_there': result.who_lives_there,
                'ideal_flatmates': result.ideal_flatmates,
                'description': result.description,
            })

    return render_template('index.html', data=plist, pagination=pagination)


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
        app.run(host='0.0.0.0', port=8002)
