from flask import Flask, render_template, url_for, redirect, \
    session, request, jsonify

from settings import SQLALCHEMY_DATABASE_URI

from models import db
from models import Property, Spider

from helpers import pagination


app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'c0derunner'

app.config.update({
    'SQLALCHEMY_DATABASE_URI': SQLALCHEMY_DATABASE_URI,
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
})
db.init_app(app)

COUNT_PER_PAGE = 10


@app.route('/centadata/', defaults={'page': 1})
@app.route('/centadata/<int:page>')
def centadata(page):
    plist = []
    total_count = Property.query.filter_by(spider_id=1).count()
    pagination_params = pagination(page, total_count, COUNT_PER_PAGE)

    results = Property.query.filter_by(spider_id=1).paginate(
        page, COUNT_PER_PAGE, False).items
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
                'gross_area': result.gross_area,
                'gross_per_foot': result.gross_per_foot,
                'net_price': result.net_price,
                'net_area': result.net_area,
                'net_per_foot': result.net_per_foot,
            })

    return render_template(
        'centadata.html', data=plist, pagination=pagination_params)


@app.route('/midlandici/', defaults={'page': 1})
@app.route('/midlandici/<int:page>')
def midlandici(page):
    plist = []
    total_count = Property.query.filter_by(spider_id=2).count()
    pagination_params = pagination(page, total_count, COUNT_PER_PAGE)

    results = Property.query.filter_by(spider_id=2).paginate(
        page, COUNT_PER_PAGE, False).items
    if results:
        for result in results:
            plist.append({
                'id': result.id,
                'spider_name': result.spider.name,
                'location': result.location,
                'date': result.date,
                'buildling': result.buildling,
                'size': result.size,
                'ft_price': result.ft_price,
                'op_type': result.op_type,
                'price': result.price,
                'data_source': result.data_source,
            })

    return render_template(
        'midlandici.html', data=plist, pagination=pagination_params)


@app.route('/easyroommate/', defaults={'page': 1})
@app.route('/easyroommate/<int:page>')
def easyroommate(page):
    plist = []
    total_count = Property.query.filter_by(spider_id=3).count()
    pagination_params = pagination(page, total_count, COUNT_PER_PAGE)

    results = Property.query.filter_by(spider_id=3).paginate(
        page, COUNT_PER_PAGE, False).items
    if results:
        for result in results:
            plist.append({
                'id': result.id,
                'spider_name': result.spider.name,
                'location': result.location,
                'price': result.price,
                'image_url': result.image_url,
                'about_the_flatshare': result.about_the_flatshare,
                'who_lives_there': result.who_lives_there,
                'ideal_flatmates': result.ideal_flatmates,
                'description': result.description,
            })

    return render_template(
        'easyroommate.html', data=plist, pagination=pagination_params)


@app.route('/')
def index():
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
