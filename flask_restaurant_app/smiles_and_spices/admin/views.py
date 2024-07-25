from flask import render_template, redirect, url_for, Blueprint, flash
from flask_login import login_user, logout_user
from smiles_and_spices import db
from smiles_and_spices.models import Admin
from smiles_and_spices.admin.forms import LoginAdminForm, RegisterAdminForm

admin_bp = Blueprint("admin_bp", __name__)

########################
### Admin Login Page ###
########################

@admin_bp.route("/admin-login", methods=["GET", "POST"])
def login_admin():

    form = LoginAdminForm()

    if form.validate_on_submit():
        admin = Admin.query.filter_by(name=form.admin.data).first()
        if admin.check_password(form.password.data) and admin is not None:
            login_user(admin)
            return redirect(url_for("menu_bp.add_menu"))

    return render_template("login_admin.html", form=form)

###########################
### Register Admin Page ###
###########################

@admin_bp.route("/register", methods=["GET", "POST"])
def register_admin():

    form = RegisterAdminForm()

    if form.validate_on_submit():
        if form.key.data == "12345":
            admin = Admin(name=form.admin.data, password=form.password.data)
            db.session.add(admin)
            db.session.commit()
            return redirect(url_for("admin_bp.login_admin"))
        else:
            flash("Wrong Key")
            return redirect(url_for("admin_bp.register_admin"))

    return render_template("register.html", form=form)

####################
### Admin Logout ###
####################

@admin_bp.route("/logout")
def logout():

    logout_user()

    return redirect(url_for('admin_bp.login_admin'))


