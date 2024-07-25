from smiles_and_spices import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(user_id)

class Food(db.Model):

    __tablename__ = "foods"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, index=True, unique=True)
    category = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(200))
    pictures = db.Column(db.String(200), nullable=False, default="default.png")
    price = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=True, default=datetime.now)
    rate = db.Column(db.String)

    def __int__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price

    def __repr__(self):
        return f"{self.name} from {self.category} with price {self.price}"


class Admin(db.Model, UserMixin):

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    password_hash = db.Column(db.String(30), nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Admin name: {self.name}"

class Reservation(db.Model):

    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String, nullable=False)
    people = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text(500))

    def __init__(self, name, email, phone, date, time, people, message):
        self.name = name
        self.email = email
        self.phone = phone
        self.date = date
        self.time = time
        self.people = people
        self.message = message


    def __repr__(self):
        return f"A reservation for {self.name}, for {self.people} people at {self.time} on date {self.date}.\nContact:\nEmail {self.email}\nPhone {self.phone}"

class Checkout_home(db.Model):

    __tablename__ = "checkout_home"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    district = db.Column(db.String(30), nullable=False)
    street = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text(500))
    payment = db.Column(db.String, nullable=False)
    order = db.Column(db.PickleType, nullable=False)
    date = db.Column(db.String, nullable=True, default=str(datetime.now())[:19])
    checked = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, city, district, street, address, phone, email, payment, text, order, date):
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.district = district
        self.street = street
        self.address = address
        self.phone = phone
        self.email = email
        self.payment = payment
        self.text = text
        self.order = order
        self.date = date

    def __repr__(self):
        return (f"An order for delivery with {self.payment} for {self.first_name} {self.last_name} from {self.city}, {self.district} with address on "
                f"{self.street}, {self.address}. Contact {self.phone}, {self.email}")

class Checkout_pickup(db.Model):

    __tablename__ = "checkout_pickup"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text(500))
    order = db.Column(db.PickleType, nullable=False)
    date = db.Column(db.String, nullable=True, default=str(datetime.now())[:19])
    checked = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, phone, email, text, order, date):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.text = text
        self.order = order
        self.date = date

    def __repr__(self):
        return f"An order with pickup for {self.first_name} {self.last_name}. Contact {self.phone}, {self.email}"


