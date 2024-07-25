from flask import render_template, Blueprint

core = Blueprint("core", __name__)

########################
### Render Home Page ###
########################

@core.route("/")
def home():

    return render_template("home.html")

