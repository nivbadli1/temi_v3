# External Modules Imports:
import datetime
import logging
from crontab import CronTab
from flask import app, jsonify

# Internal Modules imports:
from apps.authentication.models import Event, Patient, Contact
from apps.events.functs import generate_json

# Google Calendar Imports:
from gcsa.google_calendar import GoogleCalendar

# SQL Alchemy
from sqlalchemy.sql.expression import update
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


#  Global Configuration For Class:
e = 'mysql+pymysql://naya:NayaPass1!@35.226.141.122/temi_v3'
engine = create_engine(e)
session = Session(engine)
DAYS_TO_SHOW_IN_EVENTS = 7
logger = logging.getLogger(__name__)


#### Add New Event Related Functions
### Utils:
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


#### Create New Event Related Functions ####
## Form UI Generator ##

# Generate a json patients names/ID to present in UI andhandle in backend
def generate_patiens_json():
    patients = Patient.query.with_entities(Patient.patient_id, Patient.f_name, Patient.l_name)
    patientsArray = []

    for patient in patients:
        patientObj = {'id': patient.patient_id, 'f_name': patient.f_name, 'l_name': patient.l_name}
        patientsArray.append(patientObj)

    # Return the relevant contact list as a json named contacts
    return jsonify({'patients': patientsArray})


# Generate X days from today list of days with key pair of timedate and Hebrew day:
def generate_days_list():
    from_date = datetime.datetime.today()
    today = from_date.date()
    following_week = []
    logger.info("IS it working ???")

    for i in range(DAYS_TO_SHOW_IN_EVENTS):
        new_date = today + datetime.timedelta(days=1 + i)
        print(new_date.isoformat(), replace_num_with_hebrew_day(new_date.weekday()))
        dayObj = {'date': new_date.isoformat(), 'hebrew_day': replace_num_with_hebrew_day(new_date.weekday())}
        following_week.append(dayObj)

    return jsonify({'weekdays': following_week})


# Get patient ID, return a json of contacts with ID and f_name
def get_relevant_contacts(patient_id):
    contacts = Contact.query.with_entities(Contact.contact_id, Contact.f_name, Contact.l_name, Contact.patient_id).filter_by(
        patient_id=patient_id)
    contactArray = []

    for contact in contacts:
        contactObj = {'id': contact.contact_id, 'f_name': contact.f_name, 'l_name': contact.l_name}
        contactArray.append(contactObj)

    # Return the relevant contact list as a json named contacts
    return jsonify({'contacts': contactArray})


# Get Date timestamp and and return TimeDate
def stamp_to_datetime(stamp):
    start_time = stamp + ' 08:00'
    time_format = '%Y-%m-%d %H:%M'
    day = datetime.datetime.strptime(start_time, time_format)
    return day


# Get a Date format YYYY-MM-DD and return the available days from 8 to 17
def get_available_slots(day):
    avail_slots = []
    slot = day
    # Generate a list of dictionaries with each free DF slot:
    while slot.hour <= 17:
        avail_slots.append(slot.strftime("%H:%M"))
        slot = slot + datetime.timedelta(minutes=20)
    return avail_slots


# Get a full slots list and remove occupied slots, return a list
def remove_occupied_slots(slots_list, day):
    # Create a set of the same day events
    gc = GoogleCalendar(credentials_path='apps/events/credentials.json')
    today_events_timestamps = []
    for event in gc.get_events(day, day + datetime.timedelta(days=1)):
        today_events_timestamps.append(event.start.strftime("%H:%M"))

    # Subtract the today_events_timestamps from the slots_list:
    return sorted(list(set(slots_list) - set(today_events_timestamps)))


## Related to create the actual event after we have patient, contact and full timestamp ##
# Step 1.0 - Create New event
# Step 1.1 - Generate Google Calendar new event
# Step 1.2 - Add new Event record to db
# Step 1.3 - TBD, add new event to crond job with location and URI

# Generate new Google Calendar Event (Step 1.1)
def add_new_google_calendar_event(start_time, patient_name, contact_name):
    gc = GoogleCalendar(credentials_path='apps/events/credentials.json')
    event_template = generate_json()
    # Format the Template JSON
    new_start_time = start_time.isoformat() + "+03:00"
    event_template['start']['dateTime'] = new_start_time
    new_end_time = start_time + datetime.timedelta(minutes=20)
    new_end_time = new_end_time.isoformat() + "+03:00"
    event_template['end']['dateTime'] = new_end_time

    event_template['summary'] = "פגישה בין " + patient_name + " ל" + contact_name

    print("event template new details are:", event_template)

    # Create a real Calendar event using the gc service
    event = gc.service.events().insert(calendarId='primary', body=event_template, conferenceDataVersion=1).execute()

    # gc.service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    print("Event is: ", type(event))
    print('Event created successfully: %s' % event)

    return event


# Add new event record to DB (Step 1.2)
def add_event_to_db(event, patient_id, contact_id):
    print("Adding event...")
    db_event = Event(url=event['hangoutLink'], event_id=event['id'], start_time=event['start']['dateTime'].split()[0],
                     status=0, patient_id=patient_id, contact_id=contact_id)
    session.add(db_event)
    session.commit()
    print("Event added to db successfully!")
    return True


def create_new_crond(location, time, uri, event_id):
    time = time.replace(second=0, microsecond=0)
    my_cron = CronTab(user=True)
    job = my_cron.new(command='echo hello_world_func', comment=event_id)
    job.minute.on(time.minute)
    job.hour.on(time.hour)
    job.day.on(time.day)
    job.month.on(time.month)
    my_cron.write()

# Main function, get the minimal 3 parameters and generate new Event (Steps 1.0)
def create_new_event(start, patient_id, contact_id):
    # Create a Google calendar event
    # should also take the p name and c name to do a beautiful title
    contact_name = session.query(Contact.f_name).filter(Contact.contact_id == contact_id).first()[0]
    patient_name = session.query(Patient.f_name).filter(Patient.patient_id == patient_id).first()[0]
    print("P: {} {}, C: {} {}", patient_name, patient_id, contact_name, contact_id)
    event = add_new_google_calendar_event(start, patient_name, contact_name)

    # Add new event ID to our database event table
    add_event_to_db(event, patient_id, contact_id)

    # Need to get the robot locations and translate patient bed to robot location.
    # patient_bed = session.query(Patient.bed).filter(patient_id == patient_id).first()[0]
    # Translate Bed to Robot Location:

    # event.url
    # start.isoformat
    location = "BED_12"
    # Add crony task:
    create_new_crond(location, start, event['hangoutLink'], event['id'])

    print("Im done!!! ")





#### Delete Event Related Functions ####
# Step 2.0 - Delete event flow
# Step 2.1 - Delete Event from Google Calendar
# Step 2.2 - Update Event in DB to status 2
# Step 2.3 - TBD, delete event task from crond

# Get Event ID and update record in DB to status 2 (Step 2.2)
def set_event_as_deleted(event_id):
    stmt = update(Event).where(Event.event_id == event_id).values(status='2')
    engine.execute(stmt)
    print("Event marked as deleted (status = 2) in Event table")


# Get Event ID and delete event from Google Calendar (Step 2.1)
def delete_calendar_event(event_id):
    gc = GoogleCalendar(credentials_path='apps/events/credentials.json')
    event_to_be_deleted = gc.get_event(event_id)
    gc.delete_event(event_to_be_deleted)
    print("Event deleted from calendar successfully")


def delete_job(event_id):
    cron = CronTab(user=True)
    cron.remove_all(comment=event_id)
    cron.write()


# Get Event ID from UI and run delete flow (Step 2.0)
def delete_event_func(event_id):
    # Get event from Google Calendar and delete it:
    delete_calendar_event(event_id)

    # Set Event in db to status = 2
    set_event_as_deleted(event_id)

    # Delete task from chrony
    delete_job(event_id)

    print("Event deleted from whole system successfully")
