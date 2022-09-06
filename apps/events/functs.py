from __future__ import print_function

import datetime

import pytz
from gcsa.serializers.event_serializer import EventSerializer

from apps.authentication.models import Users, Patient, Contact, ContactTime, Event
from apps import db
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from collections import defaultdict

# import google.api.services.calendar.Calendar
# import google.api.services.calendar.model.Event
# import google.api.services.calendar.model.Events
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event as GoogleEvent
# from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.sql.expression import update


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

e = 'mysql+pymysql://naya:NayaPass1!@35.226.141.122/temi_v3'
engine = create_engine(e)
session = Session(engine)

# global session
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def printAllEvents():
    # """Shows basic usage of the Google Calendar API.
    #  Prints the start and name of the next 10 events on the user's calendar.
    #  """
    # creds = None
    # # The file token.json stores the user's access and refresh tokens, and is
    # # created automatically when the authorization flow completes for the first
    # # time.
    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.json', 'w') as token:
    #         token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


def addEvents():
    print("Generating events...")
    # Add events
    e1 = Event(5555, "www.google.com", "2022-09-04 14:00:00", 1, 3, 12)
    e2 = Event(6666, "www.google.com", "2022-09-05 16:00:00", 1, 4, 11)
    e3 = Event(7777, "www.google.com", "2022-09-05 17:00:00", 2, 6, 11)
    e4 = Event(8888, "www.google.com", "2022-09-05 20:00:00", 0, 5, 13)
    session.add_all([e1, e2, e3, e4])
    session.commit()
    print("Done generated events")


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


def getAllEventsToCalendar(eventJson=None):
    resultList = []
    resultDict = {}

    for event in session.query(Event).all():
        resultList.append(event.__dict__)
        # For QA:
        # print("ResultList: ", resultList)
        # print("Current Results: ", event.__dict__)

    resultDict = defaultdict(dict)
    # resultDict = dict

    for event in resultList:
        event.pop("_sa_instance_state")
        resultDict[event["event_id"]].update(event)

    return resultDict


def getAllEventsToCalendar_real():
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
    # Also remove useless columns for calender
    for event in resultList:
        event.pop("_sa_instance_state")
        event.pop("status")
        event.pop("row_created_time")
        resultDict[event["event_id"]].update(event)

    # Need to translate P_ID and C_ID to names
    return resultDict


def getAllEventsToCalendar_list():
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
    # Also remove useless columns for calender
    for event in resultList:
        event.pop("_sa_instance_state")
        event.pop("status")
        event.pop("row_created_time")
        resultDict[event["event_id"]].update(event)

    # Need to translate P_ID and C_ID to names
    return resultList


# Translate pationet to location
# contact ID get an email
#
# Get an EVENT ID (probably from UI function after selecting an event) and delete both from google calender and set status in event tables
def createNewCalanderEvent(patientID, contactID, startTime):
    # First, create an Event object:
    # Need: url? , start time, patient ID, Contact ID,
    interval = 20
    title = "Call Between " + patientID + " " + contactID
    event = GoogleEvent(title, start=startTime, end=startTime + datetime.timedelta(minutes=interval))
    print("The event is: {} ", event.__str__())
    print("Event ID before: ", event.event_id)
    google_real_event = gc.add_event(event)
    print("goocgle_real_event ID {}", )
    # print("Adding it to database: ")
    # google_real_event.
    #


# event_db object:
# self.url = url
# self.event_id = event_id
# self.start_time = start_time
# self.status = status
# self.patient_id = patient_id
# self.contact_id = contact_id

# Create a json template and
# TODO Hardcoded the timezone, need to adjust it in the future
def generate_json():
    event = {
        'summary': '',
        'location': '',
        'description': '',
        'start': {
            'dateTime': '2022-09-11T08:00:00+03:00',
        },
        'end': {
            'dateTime': '2022-09-11T11:00:00+03:00',
        },
        'attendees': [
            {'email': 'lpage@example.com'},
        ],
        "conferenceData": {
            "createRequest": {
                "conferenceSolutionKey": {
                    "type": "hangoutsMeet"
                },
                "requestId": "RandomString"
            }
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return event


def generated_json_test():
    fake_event = {
        "kind": "calendar#event",
        "etag": '"3324818981037000"',
        "id": "letg0hf7rl82ev6q6te1jn15eg",
        "status": "confirmed",
        "htmlLink": "https://www.google.com/calendar/event?eid=bGV0ZzBoZjdybDgyZXY2cTZ0ZTFqbjE1ZWcgbXRhdGVtaXByb2plY3RAbQ",
        "created": "2022-09-05T20:24:50.000Z",
        "updated": "2022-09-05T20:24:50.543Z",
        "creator": {"email": "mtatemiproject@gmail.com", "self": True},
        "organizer": {"email": "mtatemiproject@gmail.com", "self": True},
        "start": {"dateTime": "2022-09-17T09:00:00 03:00", "timeZone": "Asia/Jerusalem"},
        "end": {"dateTime": "2022-09-17T09:20:00 03:00", "timeZone": "Asia/Jerusalem"},
        "iCalUID": "letg0hf7rl82ev6q6te1jn15eg@google.com",
        "sequence": 0,
        "attendees": [
            {"email": "lpage@example.com", "responseStatus": "needsAction"},
        ],
        "hangoutLink": "https://meet.google.com/vac-bieu-pzm",
        "conferenceData": {
            "createRequest": {
                "requestId": "RandomString",
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
                "status": {"statusCode": "success"},
            },
            "entryPoints": [
                {
                    "entryPointType": "video",
                    "uri": "https://meet.google.com/vac-bieu-pzm",
                    "label": "meet.google.com/vac-bieu-pzm",
                }
            ],
            "conferenceSolution": {
                "key": {"type": "hangoutsMeet"},
                "name": "Google Meet",
                "iconUri": "https://fonts.gstatic.com/s/i/productlogos/meet_2020q4/v6/web-512dp/logo_meet_2020q4_color_2x_web_512dp.png",
            },
            "conferenceId": "vac-bieu-pzm",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 1440},
                {"method": "popup", "minutes": 10},
            ],
        },
        "eventType": "default",
    }
    return fake_event


# Working perfect
def add_new_google_calendar_event(start_time, patient_name, contact_name):
    gc = GoogleCalendar(credentials_path='./credentials.json')
    event_template = generate_json()
    # Format the Template JSON
    new_start_time = start_time.isoformat() + "+03:00"
    event_template['start']['dateTime'] = new_start_time
    new_end_time = start_time + datetime.timedelta(minutes=20)
    new_end_time = new_end_time.isoformat() + "+03:00"
    event_template['end']['dateTime'] = new_end_time

    event_template['summary'] = "פגישה בין " + str(patient_name) + " ל" + str(contact_name)

    print("event template new details are:", event_template)

    # Create a real Calendar event using the gc service
    event = gc.service.events().insert(calendarId='primary', body=event_template, conferenceDataVersion=1).execute()

    # gc.service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    print("Event is: ", type(event))
    print('Event created successfully: %s' % event)

    return event


def add_event_to_db(event, patient_id, contact_id):
    print("Adding event...")
    db_event = Event(url=event['hangoutLink'], event_id=event['id'], start_time=event['start']['dateTime'].split()[0],
                     status=0, patient_id=patient_id, contact_id=contact_id)
    session.add(db_event)
    session.commit()
    print("Event added to db successfully!")
    return True


def create_new_event(start, patient_id, contact_id):
    # Create a Google calendar event
    # should also take the p name and c name to do a beautiful title
    contact_name = session.query(Contact.f_name).filter(contact_id == contact_id).first()[0]
    patient_name = session.query(Patient.f_name).filter(patient_id == patient_id).first()[0]
    event = add_new_google_calendar_event(start, patient_name, contact_name)

    # Add new event ID to our database event table
    add_event_to_db(event, patient_id, contact_id)

    # Add new event job in crony
    # Need to get the robot locations and translate patient bed to robot location.
    patient_bed = session.query(Patient.bed).filter(patient_id == patient_id).first()[0]
    # Translate Bed to Robot Location:
    # Add crony task:

    print("Im done!!! ")


def delete_event(event_id):
    # Get event from Google Calendar and delete it:
    delete_calendar_event(event_id)

    # Set Event in db to status = 2
    stmt = update(Event).where(Event.event_id == event_id).values(status='2')
    engine.execute(stmt)
    print("Event marked as deleted (status = 2) in Event table")

    # Delete task from chrony

    print("Event deleted from whole system successfully")


def delete_calendar_event(event_id):
    gc = GoogleCalendar(credentials_path='./credentials.json')
    event_to_be_deleted = gc.get_event(event_id)
    gc.delete_event(event_to_be_deleted)
    print("Event deleted from calendar successfully")


def tests():
    print("   tests   ")
    # gc = GoogleCalendar(credentials_path='./credentials.json')
    patient_id = 56
    # patient_name = session.query(Patient.f_name).filter_by(patient_id=patient_id).one()
    # patient_name = session.query(Patient.f_name).filter(patient_id == patient_id).first()[0]

    # temp_json = generate_json_test()
    # add_event_to_db(temp_json, 7, 29)


if __name__ == '__main__':
    print("~~~ Let main run ~~~")
    # tests()
    delete_event("qbdsapqc3fdlp87numfb2lbfgo")
    # gc = GoogleCalendar(credentials_path='./credentials.json')
    # for event in gc:
    #     print(EventSerializer.to_json(event))
    # # Format: Year Month Day Hour Minute Second
    # # Add new event example:
    # start = datetime.datetime(2022, 9, 18, 11, 0, 0)
    # patient_id = 12
    # contact_id = 13
    # create_new_event(start, patient_id, contact_id)

    # add_new_google_calendar_event(start)

    # tz_string = datetime.datetime.now().astimezone().tzname()
    # if tz_string == "IDT":
    #     timezone = "+03:00"
    # else:
    #     timezone = "+02:00"

    # Print all events from Calendar:

    print("Done")
