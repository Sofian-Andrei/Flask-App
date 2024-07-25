from flask import render_template, redirect, url_for, Blueprint, flash, request, session, abort
from flask_login import current_user
from smiles_and_spices import db, app
from smiles_and_spices.models import Food, Admin
from smiles_and_spices.menu.forms import AddFoodForm, AddCartForm, StarsForm
from smiles_and_spices.menu.pic_handler import add_pictures


menu_bp = Blueprint("menu_bp", __name__)

########################
### Render Menu Page ###
########################

@menu_bp.route("/menu/", methods=["GET", "POST"])
def menu():

    foods = Food.query.all()
    #session.clear()

    return render_template("menu.html", foods=foods)

############################################
### Add Product to Database - Admin Page ###
############################################

@menu_bp.route("/admin/add_menu", methods=["GET", "POST"])
def add_menu():

    admins = Admin.query.all()
    if current_user not in admins:
        abort(403)

    form = AddFoodForm()
    food_menu = Food.query.order_by(Food.name)

    if form.validate_on_submit():
        pic = add_pictures(form.pictures.data, form.name.data)
        food = Food(name=form.name.data,
                    category=form.category.data,
                    description=form.description.data,
                    pictures=pic,
                    price=form.price.data,
                    weight=form.weight.data)
        db.session.add(food)
        db.session.commit()
        pictures = url_for("static", filename="assets/" + pic)
        return redirect(url_for("menu_bp.add_menu", pictures=pictures))

    return render_template("add_menu.html", form=form, food_menu=food_menu)

####################################
### Delete Product from Database ###
####################################

@menu_bp.route("/<int:food_id>/delete", methods=["POST", "GET"])
def delete(food_id):

    admins = Admin.query.all()
    if current_user not in admins:
        abort(403)

    food = Food.query.get(food_id)
    db.session.delete(food)
    db.session.commit()

    return redirect(url_for("menu_bp.add_menu"))

####################################
### Modify Product from Database ###
####################################

@menu_bp.route("/<int:food_id>/update", methods=["POST", "GET"])
def update(food_id):

    admins = Admin.query.all()
    if current_user not in admins:
        abort(403)

    food = Food.query.get(food_id)
    food_menu = Food.query.all()
    form = AddFoodForm()

    if form.validate_on_submit():
        if form.pictures.data is None:
            pic = food.pictures
        else:
            pic = add_pictures(form.pictures.data, form.name.data)
        food.name = form.name.data
        food.category = form.category.data
        food.description = form.description.data
        food.price = form.price.data
        food.pictures = pic
        food.weight = form.weight.data
        db.session.commit()
        pictures = url_for("static", filename="assets/" + pic)
        return redirect(url_for("menu_bp.add_menu", food_id=food.id, pictures=pictures))

    elif request.method == "GET":
        form.name.data = food.name
        form.category.data = food.category
        form.description.data = food.description
        form.price.data = food.price
        form.pictures.data = food.pictures
        form.weight.data = food.weight

    return render_template("add_menu.html", form=form, food_menu=food_menu)

################################
### Filter Starters Category ###
################################

@menu_bp.route("/menu/starters")
def starters():

    foods = Food.query.filter((Food.category == "Starter") | (Food.category == "Soup"))

    return render_template("menu.html", foods=foods)

############################
### Filter Main Category ###
############################

@menu_bp.route("/menu/main")
def main():

    foods = Food.query.filter((Food.category == "Salads") | (Food.category == "Pastas") |
                             (Food.category == "Wraps") | (Food.category == "Burgers") |
                             (Food.category == "Fish") | (Food.category == "Seafood"))

    return render_template("menu.html", foods=foods)

####################################
### Filter Specialities Category ###
####################################

@menu_bp.route("/menu/specialities")
def specialities():

    foods = Food.query.filter(Food.category == "Specialities")

    return render_template("menu.html", foods=foods)

#############################
### Filter Sides Category ###
#############################

@menu_bp.route("/menu/sides")
def sides():

    foods = Food.query.filter((Food.category == "Side Dishes") | (Food.category == "Side Salads") |
                              (Food.category == "Souse Dips"))

    return render_template("menu.html", foods=foods)

###############################
### Filter Deserts Category ###
###############################

@menu_bp.route("/menu/deserts")
def deserts():

    foods = Food.query.filter(Food.category == "Deserts")

    return render_template("menu.html", foods=foods)

##############################
### Filter Drinks Category ###
##############################

@menu_bp.route("/menu/drinks")
def drinks():

    foods = Food.query.filter((Food.category == "Coffee") | (Food.category == "Special Drinks") |
                              (Food.category == "Soft Drinks") | (Food.category == "Beers & Ciders"))

    return render_template("menu.html", foods=foods)

###############################
### Filter Products in Menu ###
###############################

@menu_bp.route("/menu/<category_name>")
def sub_menu(category_name):

    foods = Food.query.filter_by(category=category_name)

    return render_template("menu.html", foods=foods)

###########################
### Render Product Page ###
###########################

@menu_bp.route("/menu/product/<name>", methods=["POST", "GET"])
def product(name):

    foods = Food.query.filter_by(name=name)
    form = AddCartForm()
    stars = StarsForm()

    for food in foods:
        if form.validate_on_submit():
            if form.submit.data:
                flash("Your item has been added to the cart")
                if "cart" in session:
                    if not any(food.name in list(d[0].keys()) for d in session["cart"]):
                        session["cart"].append([{food.name: form.quantity.data}, {food.pictures: food.price}])
                        session["total_price"] = str(int(session["total_price"]) + (food.price * form.quantity.data))
                    elif any(food.name in list(d[0].keys()) for d in session["cart"]):
                        for d in session["cart"]:
                            d[0].update((k, (form.quantity.data + v)) for k, v in d[0].items() if k == food.name)
                        session["total_price"] = str(int(session["total_price"]) + (food.price * form.quantity.data))
                else:
                    session["cart"] = [[{food.name: form.quantity.data}, {food.pictures: food.price}]]
                    session["total_price"] = str(food.price * form.quantity.data)
                return redirect(url_for("menu_bp.product", f=food, form=form, name=name))

        if stars.validate():
            if "rating" in session:
                if food.name not in session["rating"]:
                    session["rating"] = session["rating"] + food.name
                    if food.rate is None:
                        food.rate = str(food.rate)
                        food.rate = stars.stars.data
                    else:
                        food.rate += stars.stars.data
                    db.session.commit()
            else:
                session["rating"] = food.name

            return render_template("product.html", f=food, form=form, stars=stars)

        return render_template("product.html", f=food, form=form, stars=stars)

#############################################
### Add Product to Cart from Product Page ###
#############################################

@menu_bp.route("/add-cart/<name>", methods=["POST", "GET"])
def add_cart_menu(name):

    foods = Food.query.filter_by(name=name)

    for food in foods:
        if "cart" in session:
            if not any(food.name in list(d[0].keys()) for d in session["cart"]):
                session["cart"].append([{food.name: 1}, {food.pictures: food.price}])
                session["total_price"] = str(int(session["total_price"]) + (food.price * 1))
            elif any(food.name in list(d[0].keys()) for d in session["cart"]):
                for d in session["cart"]:
                    d[0].update((k, (1 + v)) for k, v in d[0].items() if k == food.name)
                session["total_price"] = str(int(session["total_price"]) + (food.price * 1))
        else:
            session["cart"] = [[{food.name: 1}, {food.pictures: food.price}]]
            session["total_price"] = str(food.price * ([x[food.name] for y in session["cart"] for x in y if food.name in x][0]))

        return redirect(request.referrer)

################################
### Delete Product from Cart ###
################################

@menu_bp.route("/delete-cart/<name>", methods=["POST", "GET"])
def delete_cart(name):

    foods = Food.query.filter_by(name=name)

    for food in foods:
        try:
            session["total_price"] = str(int(session["total_price"]) - (food.price * [x[food.name] for y in session["cart"] for x in y if food.name in x][0]))
        except IndexError:
            pass
        session["cart"] = [x for x in session["cart"] if x != [{food.name: y for y in x[0].values()}, {food.pictures: food.price}]]
        return redirect(request.referrer)












