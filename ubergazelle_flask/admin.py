from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models import db, Client, Drivers, Regions
from views import DriversAdmin


app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
admin = Admin(app, name='Ubergazelle', template_mode='bootstrap4')
admin.add_view(ModelView(Client, db.session))
admin.add_view(DriversAdmin(Drivers, db.session))
admin.add_view(ModelView(Regions, db.session))

if __name__ == '__main__':
    app.run(debug=True)
