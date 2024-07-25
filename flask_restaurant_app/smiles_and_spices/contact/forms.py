from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, TelField
from wtforms.validators import DataRequired

class ContactForm(FlaskForm):

    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    phone = TelField("Phone", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")