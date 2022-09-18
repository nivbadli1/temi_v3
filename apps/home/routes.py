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
from apps.authentication.models import Patient,Users
from apps.home.forms import DepartmentTimesForm
from apps.authentication.models import UserTime
from apps import db
from flask import render_template, redirect, request, url_for, session, flash, jsonify


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
# Helper - Extract current page name from request

@blueprint.route('/new_profile.html', methods=['GET', 'POST'])
@login_required
def route_profile_page():
    department_form = DepartmentTimesForm()
    departments_times = UserTime.query.all()
    return render_template('home/new_profile.html', departments_times=departments_times, department_form=department_form)


@blueprint.route('/delete_department_time_id/<int:department_time_id>', methods=['GET', 'POST'])
@login_required
def delete_department_time(department_time_id):
    time_to_delete = UserTime.query.get(department_time_id)
    db.session.delete(time_to_delete)
    db.session.commit()

    return redirect(url_for('home_blueprint.route_profile_page'))


@blueprint.route('/add_department_time', methods=['GET', 'POST'])
@login_required
def add_department_time(department_time_id):
    department_form = DepartmentTimesForm()

    # Get form from UI and add new event
    if request.method == 'POST':
        time_format = '%Y-%m-%d %H:%M'
        # day_chosen = datetime.datetime.strptime(timestamp, time_format)
        # create_new_event()
        return redirect(url_for('home_blueprint.route_profile_page'))

    # Generate the New Department Time Form:
    # if request.method == 'Get':
    #     return redirect(url_for('home_blueprint.route_profile_page', department_form=department_form))


    return redirect(url_for('home_blueprint.route_profile_page'))




def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
