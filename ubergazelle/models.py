from flask_sqlalchemy import SQLAlchemy

from .regions import Regions
from .vehicle_types import VehicleTypes

db = SQLAlchemy()


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_telegram_id = db.Column(db.Integer, unique=True)
    weight = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    pickup_region = db.Column(db.Enum(Regions), nullable=False)
    pickup_address = db.Column(db.Text, nullable=False)
    delivery_region = db.Column(db.Enum(Regions), nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    vehicle_type = db.Column(db.Enum(VehicleTypes), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'''
        <Client {self.telegram_id}, pick-up region {self.pickup_region},
        pick-up address {self.pickup_address},
        delivery region {self.delivery_region}, delivery address
        {self.delivery_address}>
        '''


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_telegram_id = db.Column(db.Integer, unique=True)
    work_regions = db.Column(db.Enum(Regions), nullable=False)
    vehicle_type = db.Column(db.Enum(VehicleTypes), nullable=False)

    def __repr__(self):
        return f'''
        <Driver {self.driver_telegram_id}, work regions {self.work_regions},
        vehicle type {self.vehicle_type}>
        '''
