from apps.authentication.models import Users, Patient, Contact, ContactsTime, Event
from apps import db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

e = 'mysql+pymysql://naya:NayaPass1!@35.226.141.122/temi_v3'
engine = create_engine(e)

session = Session(engine)

def addEvents():
    print("Generating events...")
    # Add events
    e1 = Event(5555, "www.google.com", "2022-09-04 14:00:00", 1)
    e2 = Event(6666, "www.google.com", "2022-09-05 16:00:00", 1)
    e3 = Event(7777, "www.google.com", "2022-09-05 17:00:00", 2)
    e4 = Event(8888, "www.google.com", "2022-09-05 20:00:00", 0)
    session.add_all([e1, e2, e3, e4])
    session.commit()
    print("Done generated events")


if __name__ == '__main__':
    print("Lets start testing: ")
    addEvents()
    print("Done")



