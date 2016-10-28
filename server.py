from flask import Flask, render_template, url_for, redirect, request, flash
from flask.ext.login import LoginManager, login_user, logout_user, \
    login_required
from flask.ext import excel

from flask_settings import SQLALCHEMY_DATABASE_URI, BASE_SCRAPYD_URL_AJAX, \
    BASE_SITE_URL

from models import db
from models import Property, Spider, Proxy, User

from helpers import pagination
from jinja_filters import message_alert_glyph, messages_alert_tags


app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'c0derunner'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.update({
    'SQLALCHEMY_DATABASE_URI': SQLALCHEMY_DATABASE_URI,
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
})
db.init_app(app)

app.jinja_env.filters['glyph_class'] = message_alert_glyph
app.jinja_env.filters['tag_class'] = messages_alert_tags

COUNT_PER_PAGE = 10

scrapyd_url = BASE_SCRAPYD_URL_AJAX


@app.route('/download/<int:spider_id>')
def download(spider_id=1):
    results = Property.query.filter_by(spider_id=spider_id)
    data = _get_csv_headers(spider_id)
    if results:
        for result in results:
            if spider_id == 1:
                data.append(
                    (result.id, result.spider.name, result.location.strip(),
                     result.unit_floor, result.building_age.strip(),
                     result.gross_price, result.gross_area,
                     result.gross_per_foot, result.net_price,
                     result.net_area, result.net_per_foot)
                )
            elif spider_id == 2:
                data.append(
                    (result.id, result.spider.name, result.location.strip(),
                     result.date, result.buildling, result.size,
                     result.ft_price, result.op_type, result.price,
                     result.data_source)
                )
            elif spider_id == 3:
                data.append(
                    (result.id, result.spider.name, result.location.strip(),
                     result.price, result.image_url,
                     result.about_the_flatshare, result.who_lives_there,
                     result.ideal_flatmates, result.description)
                )

    output = excel.make_response_from_array(data, 'csv')
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


def _get_csv_headers(spider_id=1):
    if spider_id == 1:
        return [
            ("ID", "Spider name", "Location", "Unit floor", "Building age",
             "Number of units", "Building type", "Gross price",
             "Gross area", "Gross p.f.", "Net price", "Net area",
             "Net p.f.")
        ]
    elif spider_id == 2:
        return [
            ("ID", "Spider name", "Location", "Date", "Building",
             "Size", "Price/ft", "Operation type", "Price", "Data source")
        ]
    elif spider_id == 3:
        return [
            ("ID", "Spider name", "Location", "Price/ft", "Image url",
             "About the flatshare", "Who lives there", "Ideal flatmates",
             "Description")
        ]


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']
    registered_user = User.query.filter_by(
        email=email, password=password).first()

    if registered_user is None:
        flash(u'Username or Password is invalid', 'error')
        return redirect(url_for('login'))

    login_user(registered_user)
    flash(u'Logged in successfully', 'success')

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/centadata/', defaults={'page': 1})
@app.route('/centadata/<int:page>')
@login_required
def centadata(page):
    plist = []
    total_count = Property.query.filter_by(spider_id=1).count()
    pagination_params = pagination(page, total_count, COUNT_PER_PAGE)

    results = Property.query.filter_by(spider_id=1).order_by(
        Property.id.desc()).paginate(page, COUNT_PER_PAGE, False).items
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
        'centadata.html', data=plist,
        pagination=pagination_params, scrapyd_url=scrapyd_url)


@app.route('/midlandici/', defaults={'page': 1})
@app.route('/midlandici/<int:page>')
@login_required
def midlandici(page):
    plist = []
    total_count = Property.query.filter_by(spider_id=2).count()
    pagination_params = pagination(page, total_count, COUNT_PER_PAGE)

    results = Property.query.filter_by(spider_id=2).order_by(
        Property.id.desc()).paginate(page, COUNT_PER_PAGE, False).items
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
        'midlandici.html', data=plist,
        pagination=pagination_params, scrapyd_url=scrapyd_url)


@app.route('/easyroommate/', defaults={'page': 1})
@app.route('/easyroommate/<int:page>')
@login_required
def easyroommate(page):
    plist = []
    total_count = Property.query.filter_by(spider_id=3).count()
    pagination_params = pagination(page, total_count, COUNT_PER_PAGE)

    results = Property.query.filter_by(spider_id=3).order_by(
        Property.id.desc()).paginate(page, COUNT_PER_PAGE, False).items
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
        'easyroommate.html', data=plist,
        pagination=pagination_params, scrapyd_url=scrapyd_url)


@app.route('/proxy', methods=['GET', 'POST'])
@app.route('/proxy/<operation>/<int:proxy_id>')
@login_required
def proxy(operation=None, proxy_id=None):
    if operation and proxy_id and operation == 'delete':
        try:
            rm_proxy = Proxy.query.get(proxy_id)
            db.session.delete(rm_proxy)
            db.session.commit()

            flash(u'Proxy removed', 'success')
        except Exception:
            flash(u'Proxy does not exist', 'error')

    if request.method == 'POST':
        proxy = Proxy(
            ptype=request.values.get('type', None),
            ip=request.values.get('ip', None),
            port=request.values.get('port', None))
        db.session.add(proxy)
        db.session.commit()

        flash(u'Proxy added', 'success')

    proxy_list = []
    results = Proxy.query.all()
    if results:
        for result in results:
            proxy_list.append({
                'id': result.id,
                'ptype': result.ptype,
                'ip': result.ip,
                'port': result.port,
                'status': result.status,
            })

    return render_template(
        'proxy.html', data=proxy_list,
        base_url=BASE_SITE_URL, scrapyd_url=scrapyd_url)


@app.route('/')
@login_required
def index():
    slist = []
    results = Spider.query.all()
    if results:
        for result in results:
            slist.append({
                'id': result.id,
                'spider_name': result.name,
            })

    return render_template('spiders.html', data=slist, scrapyd_url=scrapyd_url)


if __name__ == '__main__':
    import os
    os.environ['DEBUG'] = 'true'
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', port=8008)
