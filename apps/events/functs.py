from __future__ import print_function

from apps.authentication.models import Users, Patient, Contact, ContactsTime, Event
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


if __name__ == '__main__':
    print("Lets start testing: ")
    gc = GoogleCalendar(credentials_path='./credentials.json')
    # Create internalEvent object to use across website
    for event in gc:
        print(event.id)
    print("Done")
