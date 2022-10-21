# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for, session, flash, jsonify
from flask_login import login_required

import datetime

# GCSA
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event as GoogleEvent

# Internal classes imports:
from apps.events import blueprint
from apps.authentication.models import Users, Patient, Contact, ContactTime, Event
from apps import db
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from flask import Flask, render_template, request, redirect, url_for, flash
from apps.events import functions
from apps.events.forms import EventForm, AddNewEventForm

from apps.events.functions import generate_days_list, replace_num_with_hebrew_day, get_available_slots, \
    get_relevant_contacts, create_new_event, generate_patiens_json, stamp_to_datetime, remove_occupied_slots


@blueprint.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    eventForm = EventForm()
    add_new_event_form = AddNewEventForm()
    gc = GoogleCalendar(credentials_path='apps/events/credentials.json')

    return render_template('events/calendar.html', gc=gc, eventForm=eventForm, add_new_event_form=add_new_event_form)


@blueprint.route("/events/patients_list")
@login_required
def generate_json_patients():
    p_json = generate_patiens_json()
    return p_json


@blueprint.route("/add_new_event", methods=['GET', 'POST'])
@login_required
def add_new_event_popup():
    add_new_event_form = AddNewEventForm()
    time_format = '%Y-%m-%d %H:%M'

    send_to_robot = None
    # Get form from UI and add new event
    if request.method == 'POST':
        if 'event_for_now' in request.form:
            day_chosen = datetime.datetime.strptime(datetime.datetime.now().strftime(time_format), time_format)
            send_to_robot=True
        else:
            timestamp = add_new_event_form.data['day'] + ' ' + add_new_event_form.data['time']
            day_chosen = datetime.datetime.strptime(timestamp, time_format)

        create_new_event(patient_id=add_new_event_form.data['patient'], contact_id=add_new_event_form.data['contact'],
                         start=day_chosen,send_to_robot=send_to_robot)
        return redirect(url_for('events_blueprint.calendar'))

    # Generate the New Event Form:
    if request.method == 'Get':
        return redirect(url_for('events_blueprint.calendar', add_new_event_form=add_new_event_form))

    return render_template('events/calendar.html', add_new_event_form=add_new_event_form)


@blueprint.route('/delete_event', methods=['GET', 'POST'])
@login_required
def delete_event():
    form = EventForm()
    if request.method == "POST":
        try:
            # Both work, keep as option
            eventID = form.eventID.data
            # variable = request.form.get("eventID")

            # Add delete logic here:
            # delete_event_real(eventID)
            functions.delete_event_func(eventID)
        except:
            flash("Invalid type for variable")

    return redirect(url_for('events_blueprint.calendar'))


@blueprint.route('/events/<patient_id>')
@login_required
def all_contacts(patient_id):
    contact_json = get_relevant_contacts(patient_id)
    return contact_json


# Get a date such as 2022-03-30 and return the available time slot list
@blueprint.route('/events/generate_events_slots/<event_date>')
@login_required
def generate_available_events_slot(event_date):
    day = stamp_to_datetime(event_date)
    slots_list = get_available_slots(day)
    available_list = remove_occupied_slots(slots_list, day)
    return jsonify({'slots': available_list})


@blueprint.route('/events/days_list')
@login_required
def get_weekdays_list():
    from_date = datetime.datetime.today()
    today = from_date.date()
    following_week = []

    for i in range(7):
        new_date = today + datetime.timedelta(days=1 + i)
        print(new_date.isoformat(), replace_num_with_hebrew_day(new_date.weekday()))
        dayObj = {'date': new_date.isoformat(), 'hebrew_day': replace_num_with_hebrew_day(new_date.weekday())}
        following_week.append(dayObj)

    return jsonify({'weekdays': following_week})

# def get_segment(request):
#     try:
#         segment = request.path.split('/')[-1]
#         if segment == '':
#             segment = 'index'
#         return segment
#
#     except:
#         return None
