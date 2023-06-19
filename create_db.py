from ubergazelle import db, app
from ubergazelle.models import Regions
from ubergazelle.regions import region_list

with app.app_context():
    db.create_all()

for region_item in region_list:
    region = Regions(region_name=region_item)
    with app.app_context():
        db.session.add(region)
        db.session.commit()
