from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField, DateField, TelField, SelectField
from wtforms.validators import DataRequired


class ReservationForm(FlaskForm):

    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    phone = TelField("Phone Number", validators=[DataRequired()])
    message = TextAreaField("Message")
    date = DateField("Date", validators=[DataRequired()])
    time = StringField("Time", validators=[DataRequired()])
    people = SelectField("Number of People", choices=[x for x in range(1, 13)], validators=[DataRequired()])
    submit = SubmitField("Request a Reservation")







