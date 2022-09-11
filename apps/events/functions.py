# Modules Imports:
import datetime

from flask import app, jsonify

from apps.authentication.models import Event, Patient, Contact

#  Google Calendar Imports:

from gcsa.google_calendar import GoogleCalendar
#  SQL Alchemy
from sqlalchemy.sql.expression import update
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from apps.patients.utils import get_days_list


#  Global Configuration For Class:
e = 'mysql+pymysql://naya:NayaPass1!@35.226.141.122/temi_v3'
engine = create_engine(e)
session = Session(engine)
DAYS_TO_SHOW_IN_EVENTS = 7

# Add New Event Related Functions
# Utils:
def replace_num_with_hebrew_day(day):
    d = dict({
        6: "ראשון",
        0: "שני",
        1: "שלישי",
        2: "רביעי",
        3: "חמישי",
        4: "שישי",
        5: "שבת",
    })
    return d[day]

# Generate X days from today list of days with key pair of timedate and Hebrew day:
def generate_days_list():
    from_date = datetime.datetime.today()
    today = from_date.date()
    following_week = []

    for i in range(DAYS_TO_SHOW_IN_EVENTS):
        new_date = today + datetime.timedelta(days=1+i)
        print(new_date.isoformat(), replace_num_with_hebrew_day(new_date.weekday()))
        dayObj = {'date': new_date.isoformat(), 'hebrew_day': replace_num_with_hebrew_day(new_date.weekday())}
        following_week.append(dayObj)

    return jsonify({'weekdays': following_week})

def get_relevant_contacts(patient_id):
    contacts = Contact.query.with_entities(Contact.contact_id, Contact.f_name, Contact.patient_id).filter_by(
        patient_id=patient_id)
    contactArray = []

    for contact in contacts:
        contactObj = {'id': contact.contact_id, 'f_name': contact.f_name}
        contactArray.append(contactObj)

    # Return the relevant contact list as a json named contacts
    return jsonify({'contacts': contactArray})

def get_available_slots(stamp):
    start_time = stamp + ' 08:00'
    time_format = '%Y-%m-%d %H:%M'
    day_chosen = datetime.datetime.strptime(start_time, time_format)
    avail_slots = []
    slot = day_chosen
    # Generate a list of dictionaries with each free DF slot:
    while slot.hour <= 17:
        avail_slots.append(slot.strftime("%H:%M"))
        slot = slot + datetime.timedelta(minutes=20)

    return avail_slots


if __name__ == '__main__':
    get_available_slots("2022-09-18")

# Delete Event Related Functions

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






