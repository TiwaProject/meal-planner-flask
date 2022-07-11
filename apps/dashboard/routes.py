import base64
import random
from apps import db
from apps.dashboard import blueprint
from flask import render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

from apps.dashboard.forms import CreateMealForm, DateForm
from apps.dashboard.models import Meals, DailyMeals


@blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    uid = current_user.id
    meals_query = Meals.query.filter(Meals.created_by.in_((1, uid)))
    users_daily_meal_query = DailyMeals.query.filter_by(created_by=uid)
    breakfast_list = meals_query.filter_by(meal="Breakfast").all()
    lunch_list = meals_query.filter_by(meal="Lunch").all()
    dinner_list = meals_query.filter_by(meal="Dinner").all()

    create_meal_form = CreateMealForm(request.form)
    print("current user : " + str(uid))

    if uid == 1:
        if 'create_meal' in request.form:
            return save_meal()
        return render_template("dashboard/dashboard-admin.html", breakfast=breakfast_list, lunch=lunch_list,
                               dinner=dinner_list,
                               form=create_meal_form)
    else:
        date_form = DateForm(request.form)
        if 'create_meal' in request.form:
            return save_meal()
        elif 'select_date' in request.form:
            date = request.form['date']
            session['date'] = date
            breakfast = random.choice(breakfast_list)
            lunch = random.choice(lunch_list)
            dinner = random.choice(dinner_list)
            new_meal_plan = DailyMeals(created_by=uid, breakfast_meal_id=breakfast.id, lunch_meal_id=lunch.id,
                                       dinner_meal_id=dinner.id)
            db.session.add(new_meal_plan)
            db.session.commit()
            return render_template("dashboard/dashboard.html", breakfast=breakfast_list, lunch=lunch_list,
                                   dinner=dinner_list,
                                   form=create_meal_form, meal_form=date_form, meals=[breakfast, lunch, dinner])

        return render_template("dashboard/dashboard.html", breakfast=breakfast_list, lunch=lunch_list,
                               dinner=dinner_list,
                               form=create_meal_form, meal_form=date_form)


@blueprint.route('/success')
@login_required
def success():
    return render_template("dashboard/success.html")


def save_meal():
    uid = current_user.id
    meal_name = request.form['meal_name']
    meal_description = request.form['meal_description']
    meal = request.form['meal']
    calories = request.form['calories']
    image = request.files['image']
    data = image.read()
    render_file = render_picture(data)
    new_meal = Meals(meal_name=meal_name,
                     meal_description=meal_description,
                     image=render_file,
                     meal=meal,
                     created_by=uid,
                     calories=calories)
    db.session.add(new_meal)
    db.session.commit()
    return redirect(url_for('dashboard_blueprint.success'))


def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/dashboard/FILE.html
        return render_template("dashboard/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('dashboard/page-404.html'), 404

    except:
        return render_template('dashboard/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
