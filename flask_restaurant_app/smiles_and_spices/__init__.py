import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_googlemaps import GoogleMaps

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join("static", "assets")

app.config["SECRET_KEY"] = "mykey"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
GoogleMaps(app, key="AIzaSyBWJomvDS5aX_0BN2z8oQLmy_piKgJIJX8")
login_manager = LoginManager()
login_manager.init_app(app)

#########################
### Blueprints config ###
#########################

from smiles_and_spices.core.views import core
from smiles_and_spices.delivery.views import delivery_bp
from smiles_and_spices.menu.views import menu_bp
from smiles_and_spices.reservation.views import reservation_bp
from smiles_and_spices.admin.views import admin_bp
from smiles_and_spices.contact.views import contact_bp
from smiles_and_spices.error_pages.errors import error_pages

app.register_blueprint(core)
app.register_blueprint(delivery_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(error_pages)
