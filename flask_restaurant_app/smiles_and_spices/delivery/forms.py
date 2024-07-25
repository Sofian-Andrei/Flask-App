from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, RadioField, TelField, EmailField, BooleanField
from wtforms.validators import DataRequired


class UpdateCartForm(FlaskForm):
    quantity = IntegerField("Quantity", validators=[DataRequired()], default=1)
    submit = SubmitField("Update Cart")


class CheckoutHomeForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    district = StringField("District", validators=[DataRequired()])
    street = StringField("Street and Nr.", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    landmark = StringField("Landmark")
    phone = TelField("Phone", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    payment = RadioField("Payment on Delivery", validators=[DataRequired()], choices=[("Card", "Payment with Card"),
                                                                                      ("Cash", "Payment with Cash")],
                         default="Card")
    text = TextAreaField("Order Note(Optional)")
    submit = SubmitField("Place the Order")


class CheckoutPickupForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    phone = TelField("Phone", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    text = TextAreaField("Order Note(Optional)")
    submit = SubmitField("Place the Order")


class CheckoutChoseForm(FlaskForm):
    home_pickup = RadioField("Home_Pickup", choices=[("for_home", "for_home"), ("for_pickup", "for_pickup")],
                             default="for_home")


class CheckForm(FlaskForm):
    check = BooleanField("Check Order")
