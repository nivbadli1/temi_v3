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

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


def generate_events():
    event_list = []
    newEvent = Event("2022-09-09T09:00:00", "2022-09-09T10:00:00", "Is it working", allDay=False)
    event_list.append(newEvent)

    newEvent2 = Event("2022-09-10T09:00:00", "2022-09-10T10:00:00", "Is it working 2", allDay=False)
    event_list.append(newEvent2)

    for event in event_list:
        print("event is: ", event.title, event.start, event.end)
    return event_list


@blueprint.route('/<template>', methods=['GET', 'POST'])
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)
        # if segment == "tables.html":
        #     patients = patients.list()
        #     return render_template("home/" + template, segment=segment, patients=patients)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500
# Helper - Extract current page name from request


def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
