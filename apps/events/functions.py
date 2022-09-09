# Modules Imports:
from apps.authentication.models import Event

#  Google Calendar Imports:

from gcsa.google_calendar import GoogleCalendar
#  SQL Alchemy
from sqlalchemy.sql.expression import update
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


#  Global Configuration For Class:
e = 'mysql+pymysql://naya:NayaPass1!@35.226.141.122/temi_v3'
engine = create_engine(e)
session = Session(engine)


def set_event_as_deleted(event_id):
    stmt = update(Event).where(Event.event_id == event_id).values(status='2')
    engine.execute(stmt)
    print("Event marked as deleted (status = 2) in Event table")


def delete_calendar_event(event_id):
    gc = GoogleCalendar(credentials_path='apps/events/credentials.json')
    event_to_be_deleted = gc.get_event(event_id)
    gc.delete_event(event_to_be_deleted)
    print("Event deleted from calendar successfully")


def delete_event_func(event_id):
    # Get event from Google Calendar and delete it:
    delete_calendar_event(event_id)

    # Set Event in db to status = 2
    set_event_as_deleted(event_id)

    # Delete task from chrony

    print("Event deleted from whole system successfully")








