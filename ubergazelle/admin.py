from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models import db, Client, Driver


app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
admin = Admin(app, name='Ubergazelle', template_mode='bootstrap3')
admin.add_view(ModelView(Client, db.session))
admin.add_view(ModelView(Driver, db.session))
app.run(debug=True)
