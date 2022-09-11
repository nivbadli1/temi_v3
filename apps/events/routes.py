# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for, session, flash, jsonify
from flask_login import login_required

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

# e = 'mysql+pymysql://naya:NayaPass1!@35.226.141.122/temi_v3'
# engine = create_engine(e)
# session = Session(engine)


@blueprint.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    eventForm = EventForm()
    add_new_event_form = AddNewEventForm()

    add_new_event_form.patient_list.choices = Patient.query.with_entities(Patient.patient_id, Patient.f_name)
    add_new_event_form.contact_list.choices = Contact.query.with_entities(Contact.contact_id, Contact.f_name)
    gc = GoogleCalendar(credentials_path='apps/events/credentials.json')
    return render_template('events/calendar.html', gc=gc, eventForm=eventForm, add_new_event_form=add_new_event_form)


@blueprint.route("/add_new_event", methods=['GET', 'POST'])
@login_required
def add_new_event_popup():
    add_new_event_form = AddNewEventForm()

    # If request.method == 'POST' update patient information
    # if request.method == 'POST':
    #     p = Patient(
    #         patient_id=form.patient_id.data,
    #         f_name=form.f_name.data,
    #         l_name=form.l_name.data,
    #         bed=form.bed.data,
    #         department=current_user.id,
    #         max_calls=form.max_calls.data
    #     )
    #     db.session.add(p)
    #     db.session.commit()
    if request.method == 'Get':
        # add_new_event_form.patient_list.choices = Patient.query.all()
        return redirect(url_for('events_blueprint.calendar', add_new_event_form=add_new_event_form))
        # return redirect(url_for('patients_blueprint.patient_info', patient_id=p.patient_id))
        # flash("מטופל {} עודכן בהצלחה".format(p.f_name))

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

# def get_segment(request):
#     try:
#         segment = request.path.split('/')[-1]
#         if segment == '':
#             segment = 'index'
#         return segment
#
#     except:
#         return None
