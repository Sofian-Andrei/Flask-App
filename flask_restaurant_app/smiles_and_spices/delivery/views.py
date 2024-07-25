import time
from flask_login import current_user
from smiles_and_spices import db
from flask import render_template, redirect, Blueprint, session, request, abort
from smiles_and_spices.models import Food, Admin
from smiles_and_spices.delivery.forms import CheckoutHomeForm, CheckoutChoseForm, CheckoutPickupForm, CheckForm
from smiles_and_spices.models import Checkout_home, Checkout_pickup
from datetime import datetime


delivery_bp = Blueprint("delivery_bp", __name__)

########################
### Render Cart Page ###
########################

@delivery_bp.route("/delivery", methods=["GET", "POST"])
def delivery():

    return render_template("delivery.html")

###########################################
### Increase Product Quantity from Cart ###
###########################################

@delivery_bp.route("/delivery/update_up/<name>", methods=["GET", "POST"])
def delivery_update_up(name):

    foods = Food.query.filter_by(name=name)
    new_session = []

    for x in session["cart"]:
        x[0].update((k, ([x[name] for y in session["cart"] for x in y if name in x][0] + 1)) for k, v in x[0].items()
                    if k == name)
        new_session.append(x)

    for food in foods:
        session["total_price"] = str(int(session["total_price"]) + food.price)

    session["cart"] = new_session
    return redirect(request.referrer)

###########################################
### Decrease Product Quantity from Cart ###
###########################################

@delivery_bp.route("/delivery/update_down/<name>", methods=["GET", "POST"])
def delivery_update_down(name):

    foods = Food.query.filter_by(name=name)
    new_session = []

    if [x[name] for y in session["cart"] for x in y if name in x][0] > 1:
        for x in session["cart"]:
            x[0].update((k, ([x[name] for y in session["cart"] for x in y if name in x][0] - 1)) for k, v in x[0].items()
                        if k == name)
            new_session.append(x)
        for food in foods:
            session["total_price"] = str(int(session["total_price"]) - food.price)
    else:
        for x in session["cart"]:
            x[0].update((k, ([x[name] for y in session["cart"] for x in y if name in x][0])) for k, v in x[0].items() if
                        k == name)
            new_session.append(x)

    session["cart"] = new_session
    return redirect(request.referrer)

############################
### Render Checkout Page ###
############################

@delivery_bp.route("/delivery/checkout", methods=["POST", "GET"])
def checkout():

    form_home = CheckoutHomeForm()
    form_pickup = CheckoutPickupForm()
    chose_form = CheckoutChoseForm()

    if chose_form.home_pickup.data == "for_home":
        result = "for_home"
    else:
        result = "for_pickup"
    if form_home.validate_on_submit():
        order = Checkout_home(first_name=form_home.first_name.data,
                              last_name=form_home.last_name.data,
                              city=form_home.city.data,
                              district=form_home.district.data,
                              street=form_home.street.data,
                              address=form_home.address.data,
                              phone=form_home.phone.data,
                              email=form_home.email.data,
                              text=form_home.text.data,
                              date=str(datetime.now())[:19],
                              payment=form_home.payment.data,
                              order=[{"".join(dic[0].keys()): [*dic[1].values(), *dic[0].values(), int(session["total_price"])]}
                                     for dic in session["cart"]])
        db.session.add(order)
        db.session.commit()
        [session.pop(key) for key in list(session.keys()) if key == "cart" or key == "total_price"]
        return render_template("thanks_page.html")

    if form_pickup.validate_on_submit():
        order = Checkout_pickup(first_name=form_pickup.first_name.data,
                                last_name=form_pickup.last_name.data,
                                phone=form_pickup.phone.data,
                                email=form_pickup.email.data,
                                text=form_pickup.text.data,
                                date=str(datetime.now())[:19],
                                order=[{"".join(dic[0].keys()): [*dic[1].values(), *dic[0].values(), int(session["total_price"])]}
                                       for dic in session["cart"]])
        db.session.add(order)
        db.session.commit()
        [session.pop(key) for key in list(session.keys()) if key == "cart" or key == "total_price"]
        return render_template("thanks_page.html")

    time.sleep(0.4)
    return render_template("checkout.html", form_home=form_home, form_pickup=form_pickup,
                           chose_form=chose_form, result=result)

################################
### Orders View - Admin Page ###
################################

@delivery_bp.route("/admin/orders", methods=["POST", "GET"])
def orders():

    admins = Admin.query.all()
    if current_user not in admins:
        abort(403)

    page_home = request.args.get("page", 1, type=int)
    orders_home = Checkout_home.query.order_by(Checkout_home.id.desc()).paginate(page=page_home, per_page=6)
    page_pickup = request.args.get("page_p", 1, type=int)
    orders_pickup = Checkout_pickup.query.order_by(Checkout_pickup.id.desc()).paginate(page=page_pickup, per_page=6)

    return render_template("order.html", orders_home=orders_home, orders_pickup=orders_pickup)

################################
### Check New Order for Home ###
################################

@delivery_bp.route("/admin/orders/<int:id>")
def check_order_home(id):

    admins = Admin.query.all()
    if current_user not in admins:
        abort(403)

    order = Checkout_home.query.get(id)
    order.checked = True
    db.session.commit()

    return redirect(request.referrer)

#############################
### Delete Order for Home ###
#############################

@delivery_bp.route("/admin/orders/delete/<int:id>")
def delete_order_home(id):

    admins = Admin.query.all()
    if current_user not in admins:
        abort(403)

    order = Checkout_home.query.get(id)
    db.session.delete(order)
    db.session.commit()

    return redirect(request.referrer)

##################################
### Check New Order for Pickup ###
##################################

@delivery_bp.route("/admin/orders/p<int:id>")
def check_order_pickup(id):

    admins = Admin.query.all()
    if current_user not in admins:
        abort(403)

    order = Checkout_pickup.query.get(id)
    order.checked = True
    db.session.commit()

    return redirect(request.referrer)

##############################
### Delete Order for Pickup###
##############################

@delivery_bp.route("/admin/orders/p<int:id>")
def delete_order_pickup(id):

    admins = Admin.query.all()
    if current_user not in admins:
        abort(403)

    order = Checkout_pickup.query.get(id)
    db.session.delete(order)
    db.session.commit()

    return redirect(request.referrer)
