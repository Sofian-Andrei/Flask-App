from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed
from smiles_and_spices import app

app.config.from_object(__name__)


class AddFoodForm(FlaskForm):

    name = StringField("Food Name", validators=[DataRequired()])
    category = SelectField("Food Type", choices=["Starter", "Soup", "Salads", "Pastas", "Wraps", "Burgers", "Fish",
                                                 "Seafood", "Specialities", "Side Dishes", "Side Salads", "Souse Dips",
                                                 "Deserts", "Coffee", "Special Drinks", "Soft Drinks", "Beer & Ciders"],
                           validators=[DataRequired()])
    description = TextAreaField("Food Description", validators=[DataRequired()])
    pictures = FileField("Add Food Pictures", validators=[FileAllowed(["jpg", "png"])])
    price = IntegerField("Food Price", validators=[DataRequired()])
    weight = IntegerField("Weight(g)")
    submit = SubmitField("Add/Update")


class AddCartForm(FlaskForm):

    quantity = IntegerField("Quantity", validators=[DataRequired()], default=1)
    submit = SubmitField("Add to Cart")


class StarsForm(FlaskForm):

    stars = RadioField("Stars", choices=[(5, "star5"), (4, "star4"), (3, "star3"), (2, "star2"), (1, "star1")])

