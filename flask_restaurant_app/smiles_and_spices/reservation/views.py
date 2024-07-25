from flask import render_template, redirect, url_for, Blueprint, request, abort
from flask_login import current_user
from smiles_and_spices.reservation.forms import ReservationForm
from smiles_and_spices.models import Reservation, Admin
from smiles_and_spices import db
from datetime import datetime

reservation_bp = Blueprint("reservation_bp", __name__)

###############################
### Render Reservation Page ###
###############################

@reservation_bp.route("/reservation", methods=["GET", "POST"])
def reservation():

    form = ReservationForm()
    hour = f"{datetime.today().hour + 1}:00"

    if request.method == "POST":
        hour = request.form.get("action")

    if form.validate_on_submit():
        reserv = Reservation(name=form.name.data,
                             email=form.email.data,
                             phone=form.phone.data,
                             date=form.date.data,
                             time=form.time.data,
                             people=form.people.data,
                             message=form.message.data)
        db.session.add(reserv)
        db.session.commit()
        return redirect(url_for("menu_bp.menu"))

    return render_template("reservation.html", form=form, time=datetime.today(), hour=hour)

#####################################
### Reservation View - Admin Page ###
#####################################

@reservation_bp.route("/admin/reservation-view")
def reservation_view():

    admins = Admin.query.all()
    if current_user not in admins:
        abort(403)

    reservations = Reservation.query.all()

    return render_template("reservation_view.html", reservations=reservations)

##########################
### Delete Reservation ###
##########################

@reservation_bp.route("/reservation-view/<int:reservation_id>", methods=["GET", "POST"])
def delete_reservation(reservation_id):

    admins = Admin.query.all()
    if current_user not in admins:
        abort(403)

    reservation = Reservation.query.get(reservation_id)
    db.session.delete(reservation)
    db.session.commit()

    return redirect(url_for("reservation_bp.reservation_view"))