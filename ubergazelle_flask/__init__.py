from flask import Flask

from ubergazelle_flask.models import db


app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
