import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField, SelectField, DateField
from wtforms.validators import Email, DataRequired, ValidationError, InputRequired


# add meal form

def validate_meal(field):
    if field.data == "":
        raise ValidationError("Sorry, you haven't chosen a meal")


class CreateMealForm(FlaskForm):
    meal_name = StringField('Meal Name', id='meal_name_create', validators=[DataRequired()])
    calories = StringField('Calories', id='calories_create', validators=[DataRequired()])
    meal_description = TextAreaField('Description', id='meal_description_create', validators=[DataRequired()])
    meal = SelectField('meal', choices=[('default', 'Select the meal'), ('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'),
                                        ('Dinner', 'Dinner')], id='meal_create',
                       validators=[validate_meal, DataRequired(), InputRequired()])
    image = FileField('Image', id='meal_image_create', validators=[DataRequired()])


class DateForm(FlaskForm):
    day = datetime.date.today()
    date = DateField('Date', id='date_select', default=day, validators=[DataRequired()])
