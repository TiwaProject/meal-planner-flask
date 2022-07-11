from apps import db


class Meals(db.Model):
    __tablename__ = 'Meals'

    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String(64), unique=False)
    meal_description = db.Column(db.String(64), unique=False)
    calories = db.Column(db.String(10), unique=False)
    created_by = db.Column(db.Integer, unique=False)
    meal = db.Column(db.String(15), unique=False)
    image = db.Column(db.String(64), unique=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            setattr(self, property, value)

    def __repr__(self):
        return str(self.meal_name)


class DailyMeals(db.Model):
    __tablename__ = 'DailyMeals'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64), unique=True)
    created_by = db.Column(db.Integer, unique=False)
    breakfast_meal_id = db.Column(db.Integer, unique=False)
    lunch_meal_id = db.Column(db.Integer, unique=False)
    dinner_meal_id = db.Column(db.Integer, unique=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            setattr(self, property, value)

    def __repr__(self):
        return str(self.date)
