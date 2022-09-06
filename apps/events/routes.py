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
from apps.authentication.models import Users, Patient, Contact, ContactTime
from apps import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from collections import defaultdict

# e = 'mysql+pymysql://naya:NayaPass1!@35.226.141.122/temi_v3'
# engine = create_engine(e)
# session = Session(engine)


@blueprint.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    gc = GoogleCalendar(credentials_path='apps/events/credentials.json')
    return render_template('events/calendar.html', gc=gc)

# Get the minial vars need to create a google event. gets IU and later save it in db
# def createCalendarEvent():


# Get an EVENT ID (probably from UI function after selecting an event) and delete both from google calender and set status in event tables
def deleteCalanderEvent(patientID, contactID, startTime):
# First, create an Event object:
    event = GoogleEvent('Call between {} and {}', patientID, contactID, start=startTime, end=startTime+20)
    print("The event is: {} " , event.__str__())

# 2022-09-03 22:42:06


# TODO Te be deleted
@blueprint.route('/calendar_page')
@login_required
def calender_page():
    return render_template('events/calendar_events.html')

# TODO To Be Deleted
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

