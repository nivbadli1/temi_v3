# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for, session, flash, jsonify
from flask_login import login_required

# from apps.patients import blueprint
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event as GoogleEvent

from apps.events import blueprint
from apps.authentication.models import Users, Patient, Contact, ContactTime, Event
from apps import db
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from flask import Flask, render_template, request, redirect, url_for, flash

from apps.events.forms import EventForm

e = 'mysql+pymysql://naya:NayaPass1!@35.226.141.122/temi_v3'
engine = create_engine(e)
session = Session(engine)

current_event_id = ""


@blueprint.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    eventForm = EventForm()
    gc = GoogleCalendar(credentials_path='apps/events/credentials.json')
    return render_template('events/calendar.html', gc=gc, form=eventForm)


# Get the minial vars need to create a google event. gets IU and later save it in db
# def createCalendarEvent():


# Get an EVENT ID (probably from UI function after selecting an event) and delete both from google calender and set status in event tables
# def deleteCalanderEvent(patientID, contactID, startTime):
#     # First, create an Event object:
#     event = GoogleEvent('Call between {} and {}', patientID, contactID, start=startTime, end=startTime + 20)
#     print("The event is: {} ", event.__str__())
#

# 2022-09-03 22:42:06

# current_event_id = 0


@blueprint.route('/calendar/delete_event/', methods=['GET', 'POST'])
@login_required
def delete_event(current_event_id):
    # global current_event_id
    if request.method == "POST":
        try:
            variable = str(request.form.get("current_event_id"))
            stmt = update(Event).where(Event.event_id == variable).values(status='2')
            engine.execute(stmt)
        except:
            flash("Invalid type for variable")

    return redirect(url_for('events_blueprint.calendar'))

# def get_segment(request):
#     try:
#         segment = request.path.split('/')[-1]
#         if segment == '':
#             segment = 'index'
#         return segment
#
#     except:
#         return None
