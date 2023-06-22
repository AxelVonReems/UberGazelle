from ubergazelle_flask import db, app
from ubergazelle_flask.models import Regions
from ubergazelle_flask.regions import region_list

with app.app_context():
    db.create_all()

for region_item in region_list:
    region = Regions(region_name=region_item)
    with app.app_context():
        db.session.add(region)
        db.session.commit()
