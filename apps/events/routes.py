# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for, session, flash, jsonify
from flask_login import login_required

# from apps.patients import blueprint
from gcsa.google_calendar import GoogleCalendar

from apps.events import blueprint
from apps.authentication.models import Users, Patient, Contact, ContactsTime
from apps import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from collections import defaultdict

e = 'mysql+pymysql://naya:NayaPass1!@35.226.141.122/temi_v3'
engine = create_engine(e)
session = Session(engine)


@blueprint.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    # events_list = generate_events()
    # events_list = getAllEventsToCalendar()
    # return render_template('events/calendar.html', segment=segment, events_list=events_list)
    gc = GoogleCalendar(credentials_path='apps/events/credentials.json')

    return render_template('events/calendar.html', gc=gc)


@blueprint.route('/calendar_page')
@login_required
def calender_page():
    return render_template('events/calendar_events.html')

@blueprint.route('/calendar-events')
@login_required
def calendar_events():
    conn = None
    cursor = None
    try:
        # conn = mysql.connect() cursor = conn.cursor(pymysql.cursors.DictCursor) cursor.execute( "SELECT id, title,
        # url, class, UNIX_TIMESTAMP(start_date)*1000 as start, UNIX_TIMESTAMP(end_date)*1000 as " "end FROM event")
        # rows = cursor.fetchall()
        from apps.events.functs import getAllEventsToCalendar_list
        resp = jsonify(getAllEventsToCalendar_list())
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)

        # return render_template('events/calendar_events.html', events_list=events_list)


def getAllEventsToCalendar():
    resultList = []
    resultDict = {}
    # Iterate and get all events to a temp list:
    for event in session.query(Event).all():
        resultList.append(event.__dict__)
        # For QA:
        # print("ResultList: ", resultList)
        # print("Current Results: ", event.__dict__)
    # Define Default Dict:
    resultDict = defaultdict(dict)
    # For each event, remove useless column and add to resultDict with event_ID as main tag:
    # Also remove useless columns for calander
    for event in resultList:
        event.pop("_sa_instance_state", "status", "row_created_time")
        resultDict[event["event_id"]].update(event)

    return resultDict


# def get_segment(request):
#     try:
#         segment = request.path.split('/')[-1]
#         if segment == '':
#             segment = 'index'
#         return segment
#
#     except:
#         return None


def generate_events():
    event_list = []
    newEvent = Event("2022-09-09T09:00:00", "2022-09-09T10:00:00", "Is it working", allDay=False, resourceEditable=True)
    event_list.append(newEvent)

    newEvent2 = Event("2022-09-10T09:00:00", "2022-09-10T10:00:00", "Is it working 2", allDay=False,
                      resourceEditable=True)
    event_list.append(newEvent2)

    for event in event_list:
        print("event is: ", event.title, event.start, event.end)
    return event_list


class Event:
    def __init__(self, title, start, end, allDay, resourceEditable):
        self.title = title
        self.start = start
        self.end = end
        self.backgroundColor = "#f56954"
        self.borderColor = "#f56954"
        self.allDay = allDay
        self.resourceEditable = resourceEditable

    def __repr__(self):
        return "{title:'%s', start='%s', end='%s', allDay='%s', backgroundColor='%s', borderColor='%s', resourceEditable: '%s'}" % (
            self.title, self.start, self.end, self.allDay, self.backgroundColor, self.borderColor,
            self.resourceEditable)

# @blueprint.route("/<int:patient_id>/patient_info", methods=['GET', 'POST'])
# @login_required
# def update(patient_id):
#     form = PatientForm()
#     # Get all attributes of the patient
#     p = Patient.query.filter_by(patient_id=patient_id).first_or_404()
#
#     # If request.method == 'POST' update patient information
#     if form.validate_on_submit():
#         p.patient_id = form.patient_id.data
#         p.f_name = form.f_name.data
#         p.l_name = form.l_name.data
#         p.bed = form.bed.data
#         p.department = form.department.data
#         p.max_calls = form.max_calls.data
#         db.session.commit()
#         # flash("מטופל {} עודכן בהצלחה".format(p.f_name))
#         return redirect(url_for('patients.list',patient_id=p.patient_id))
#     # If request.method == 'GET' get patient information
#     elif request.method == 'GET':
#         form.patient_id.data = p.patient_id
#         form.f_name.data = p.f_name
#         form.l_name.data = p.l_name
#         form.bed.data = p.bed
#         form.department.data = p.department
#         form.max_calls.data = p.max_calls
#
#     return render_template('patients/patient_info.html',form=form, patient_id=patient_id)
#

# @blueprint.route("/add", methods=['GET', 'POST'])
# @login_required
# def add():
#     form = PatientForm()
#     # # Get all attributes of the patient
#     # p = Patient.query.filter_by(patient_id=patient_id).first_or_404()
#
#     # If request.method == 'POST' update patient information
#     if request.method == 'POST':
#         p = Patient(
#             patient_id=form.patient_id.data,
#             f_name=form.f_name.data,
#             l_name=form.l_name.data,
#             bed=form.bed.data,
#             department=form.department.data,
#             max_calls=form.max_calls.data
#         )
#         db.session.add(p)
#         db.session.commit()
#         return redirect(url_for('patients_blueprint.tables'))
#         # return redirect(url_for('patients_blueprint.patient_info', patient_id=p.patient_id))
#         # flash("מטופל {} עודכן בהצלחה".format(p.f_name))
#     return render_template('patients/add_patient.html',form=form)


# return render_template('patients/patient_info.html',form=form, patient_id=patient_id)

# @blueprint.route("/<int:patient_id>/patient_info", methods=['GET', 'POST'])
# @login_required
# def patient_info(patient_id):
#     form = PatientForm()
#     # Get all attributes of the patient
#     p = Patient.query.filter_by(patient_id=patient_id).first_or_404()
#     if request.method == 'GET':
#         form.patient_id.data = p.patient_id
#         form.f_name.data = p.f_name
#         form.l_name.data = p.l_name
#         form.bed.data = p.bed
#         form.department.data = p.department
#         form.max_calls.data = p.max_calls
#         contacts = p.contacts
#     return render_template('patients/patient_info.html',form=form, patient_id=patient_id,contacts=contacts)

# @blueprint.route("/<int:patient_id>/delete", methods=['GET', 'POST'])
# @login_required
# def delete(patient_id):
#     try:
#         patient_id = Patient.query.get(patient_id)
#         db.session.delete(patient_id)
#         db.session.commit()
#     except:
#         print("Error")
#         # flash("מטופל לא קיים")
#     return redirect(url_for('patients_blueprint.tables'))
