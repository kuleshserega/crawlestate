# -*- coding: utf-8 -*-
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import flask_settings
import models


engine = create_engine(flask_settings.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()


class CrawlestatePipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'centadata':
            prop = models.Property(
                spider_id=1,
                location=item['location'],
                unit_floor=item['unit_floor'],
                building_age=int(item['building_age']),
                number_of_units=int(item['number_of_units']),
                building_type=item['building_type'],
                gross_price=item['gross_price'],
                net_price=item['net_price'],
            )
        elif spider.name == 'midlandici':
            prop = models.Property(
                spider_id=2,
                location=item['location'],
                date=item['date'],
                buildling=item['buildling'],
                size=item['size'],
                ft_price=item['ft_price'],
                op_type=item['op_type'],
                price=item['price'],
                data_source=item['data_source'],
            )
        elif spider.name == 'easyroommate':
            prop = models.Property(
                spider_id=3,
                location=item['location'],
                price=item['price'],
                image_url=item['image_url'],
                about_the_flatshare=item['about_the_flatshare'],
                who_lives_there=item['who_lives_there'],
                ideal_flatmates=item['ideal_flatmates'],
                description=item['description'],
            )

        session.add(prop)
        session.commit()
        return item
