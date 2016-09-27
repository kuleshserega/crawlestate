from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spider_id = db.Column(db.ForeignKey('spider.id'))
    spider = db.relationship('Spider')
    # common fields
    location = db.Column(db.String(40))
    # info related to Centdata spider
    year_duration = db.Column(db.String(40))
    unit_floor = db.Column(db.String(40))
    building_age = db.Column(db.Integer)
    number_of_units = db.Column(db.Integer)
    building_type = db.Column(db.String(40))
    gross_price = db.Column(db.String(40))
    net_price = db.Column(db.String(40))
    # info related to Midlandici spider
    date = db.Column(db.DateTime)
    district = db.Column(db.String(100))
    buildling = db.Column(db.String(255))
    size = db.Column(db.String(40))
    ft_price = db.Column(db.String(40))
    op_type = db.Column(db.String(40))
    price = db.Column(db.String(40))
    data_source = db.Column(db.String(40))
    # info related to Easyroommate spider
    price = db.Column(db.String(20))
    image_url = db.Column(db.Text)
    about_the_flatshare = db.Column(db.Text)
    who_lives_there = db.Column(db.String(255))
    ideal_flatmates = db.Column(db.String(255))
    description = db.Column(db.Text)


class Spider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
