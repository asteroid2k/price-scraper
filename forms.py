from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, InputRequired, NumberRange


class ScrapeForm(FlaskForm):
    item = StringField("item", validators=[
                       DataRequired(message="Enter product name")])
    site = SelectField("site", choices=["Kikuu", "Jumia"])
    page = IntegerField("page", validators=[DataRequired(
        message="Page Limit must be at least 1")])


class DataframeForm(FlaskForm):
    operator = SelectField(choices=["gte", "lte", "gt", "lt", "eq"])
    value = IntegerField(
        validators=[DataRequired(message="Provide a value")])
