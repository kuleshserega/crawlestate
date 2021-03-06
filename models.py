from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, index=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password = db.Column(db.String(10))

    def __unicode__(self):
        return self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spider_id = db.Column(db.ForeignKey('spider.id'))
    spider = db.relationship('Spider')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # common fields
    location = db.Column(db.String(255))
    # info related to Centdata spider
    unit_floor = db.Column(db.String(255))
    building_age = db.Column(db.String(40))
    number_of_units = db.Column(db.String(40))
    building_type = db.Column(db.String(40))
    net_price = db.Column(db.String(40))
    net_area = db.Column(db.String(40))
    net_per_foot = db.Column(db.String(40))
    gross_price = db.Column(db.String(40))
    gross_area = db.Column(db.String(40))
    gross_per_foot = db.Column(db.String(40))
    # info related to Midlandici spider
    date = db.Column(db.Date)
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


class Proxy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ptype = db.Column(db.String(7))
    ip = db.Column(db.String(20))
    port = db.Column(db.String(7))
    status = db.Column(db.String(20), default='Works')
