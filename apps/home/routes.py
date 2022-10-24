# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime
from typing import Any

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import json
from apps.authentication.models import Patient, Users
from apps.home.forms import DepartmentTimesForm
from apps.authentication.models import UserTime
from apps import db
from flask import render_template, redirect, request, url_for, session, flash, jsonify
from sqlalchemy import desc


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>', methods=['GET', 'POST'])
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)
        # if segment == "patients_list.html":
        #     patients = patients.list()
        #     return render_template("home/" + template, segment=segment, patients=patients)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

@blueprint.route('/new_profile.html', methods=['GET', 'POST'])
@login_required
def route_profile_page():
    department_form = DepartmentTimesForm()
    # todo: Need to add filter for the current logged in user id?
    departments_times = UserTime.query.order_by(UserTime.day.asc()).all()
    d = dict({
        1: "ראשון",
        2: "שני",
        3: "שלישי",
        4: "רביעי",
        5: "חמישי",
        6: "שישי",
        7: "שבת"
    })
    departments_times_lists = []
    for element in departments_times:
        departments_times_lists.append([d[element.day], element.from_hour.strftime("%H:%M"), element.to_hour.strftime("%H:%M"), element.id])

    from flask_login import current_user, login_user
    print("current user is: ", current_user.email, current_user.id, current_user.username)

    return render_template('home/new_profile.html', departments_times=departments_times,
                           department_form=department_form, departments_times_lists=departments_times_lists, current_username=current_user.username)


@blueprint.route('/delete_department_time_id/<int:department_time_id>', methods=['GET', 'POST'])
@login_required
def delete_department_time(department_time_id):
    time_to_delete = UserTime.query.get(department_time_id)
    db.session.delete(time_to_delete)
    db.session.commit()

    return redirect(url_for('home_blueprint.route_profile_page'))


@blueprint.route('/add_department_time', methods=['GET', 'POST'])
@login_required
def add_department_time(department_time_id=1):
    department_form = DepartmentTimesForm()

    # Get form from UI and add new event
    if request.method == 'POST':
        # if POST, we got a new department time
        newUserTime = UserTime(from_hour=department_form.from_hour.data, to_hour=department_form.to_hour.data, day=department_form.day.data, user_id=department_time_id)
        db.session.add(newUserTime)
        db.session.commit()

        return redirect(url_for('home_blueprint.route_profile_page'))

    # Generate the New Department Time Form:
    # if request.method == 'Get':
    #     return redirect(url_for('home_blueprint.route_profile_page', department_form=department_form))
    # DepartmentTimesForm

    return redirect(url_for('home_blueprint.route_profile_page'))


def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
