from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ChoiceType

from vehicle_types import VEHICLE_TYPES
from regions import REGIONS

db = SQLAlchemy()


class Regions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Region ID {self.id}, region name {self.region_name}>'


class Drivers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_telegram_id = db.Column(db.Integer, unique=True, nullable=False)
    work_regions = db.Column(db.String, nullable=False)
    vehicle_type = db.Column(ChoiceType(VEHICLE_TYPES), nullable=False)

    def __repr__(self):
        return f'''
        <Driver {self.driver_telegram_id}, work regions {self.work_regions},
        vehicle type {self.vehicle_type}>
        '''


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_telegram_id = db.Column(db.Integer, unique=True, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    pickup_region = db.Column(
        ChoiceType(REGIONS), nullable=False, unique=True
    )
    pickup_address = db.Column(db.Text, nullable=False)
    delivery_region = db.Column(
        ChoiceType(REGIONS), nullable=False, unique=True
    )
    delivery_address = db.Column(db.Text, nullable=False)
    vehicle_type = db.Column(ChoiceType(VEHICLE_TYPES), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'''
        <Client {self.telegram_id}, pick-up region {self.pickup_region},
        pick-up address {self.pickup_address},
        delivery region {self.delivery_region}, delivery address
        {self.delivery_address}>
        '''
