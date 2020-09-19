from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, InputRequired, NumberRange


class ScrapeForm(FlaskForm):
    item = StringField(validators=[DataRequired(message="Enter Product name")])
    site = SelectField(choices=["Kikuu", "Jumia"], validators=[DataRequired()])
    page_limit = IntegerField(validators=[NumberRange(
        min=1, message="Page Limit must be at least 1")])
