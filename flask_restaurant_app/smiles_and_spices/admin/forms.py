from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginAdminForm(FlaskForm):

    admin = StringField("Admin", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterAdminForm(FlaskForm):

    admin = StringField("Admin Name", validators=[DataRequired()])
    password = PasswordField("Admin Password", validators=[DataRequired()])
    key = PasswordField("Key", validators=[DataRequired()])
    submit = SubmitField("Register")