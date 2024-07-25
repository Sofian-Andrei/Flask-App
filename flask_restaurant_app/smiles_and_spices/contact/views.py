from flask import render_template, Blueprint
from smiles_and_spices.contact.forms import ContactForm


contact_bp = Blueprint("contact_bp", __name__)

###########################
### Render Contact Page ###
###########################

@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():

    form = ContactForm()

    return render_template("contact.html", form=form)





