import re

import pandas as pd
from pandas import DataFrame
from sqlalchemy.event import Events

from apps.authentication.models import Users, Patient, Contact, ContactTime, Event, UserTime
from apps import db
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, class_mapper
from datetime import datetime as dt
import utils as U
from run import app_config
from apps.events import functions as E

class Department:
    _FREQ = 20
    _NEXT_DAYS_NUM = 30

    def __init__(self, department_id, session=None):
        # Create session if not get_session
        if not session:
            self.engine = U.get_engine()
            self.session = U.get_session(self.engine)

        # Set department_id
        self.department_id = department_id

        # Set patients of department with their contacts
        self.patients = self.get_patients_for_dept()

        # Set events of depertments
        self.next_department_events = self.get_next_events(filter_by={'department_id': self.department_id, 'status': 2})

        # Set free slots of department
        try:
            self.department_free_slots_df = self.get_free_slots(Users, filter_by={'department_id': self.department_id})
        except Exception as e:
            raise Exception(e)



        self.department_free_slots_list = None

    def get_next_events(self, filter_by=None, event_status=None):
        """
        The function return next events for cls (Patient,Contact,Dept)
        """
        events = U.get_df(Event, self.session, filter_by)
        return events

    def get_patients_for_dept(self):
        """
        The function get all the patients of the department and their contacts
        """
        patients = U.get_df(Patient, self.session, filter_by={"department_id": self.department_id}).reset_index()
        contacts = U.get_df(Contact, self.session).reset_index()
        patients = patients.merge(contacts, on='patient_id', how='left')
        return patients

    def get_free_slots(self, cls, contact_id=None, filter_by=None):
        """
        The function get cls and filter by and return free slots of cls
        """
        if ('users' in cls.__name__.lower()):
            df = U.get_df(eval(cls.__name__[:-1] + 'Time'), self.session, filter_by={'user_id': self.department_id})
        elif ('contact' in cls.__name__.lower()):
            df = U.get_df(eval(cls.__name__ + 'Time'), self.session, filter_by={'contact_id': contact_id})

        # If df is not empty
        if (not df.shape): raise Exception("No free slots at db for cls", format(cls.__name__))

        time_slots_df = U.get_df_time_slots(df, freq=self._FREQ, next_days_num=self._NEXT_DAYS_NUM)
        next_events_df = self.get_next_events(filter_by)
        df = time_slots_df.merge(next_events_df, how='left', indicator=True)
        df['start_time'] = df['start_time'].mask(df.pop('_merge').eq('both'))
        return df[df['start_time'].notnull()].loc[:, ['start_time']]

    def set_department_free_slots_list(self):
        self.department_free_slots_list = self.department_free_slots_df['start_time'].tolist()

    def get_contact_availability(self, contact_id):
        """
        The function get contact_id and return available time for contact_id
        """
        try:
            contact_free_slots = self.get_free_slots(Contact, contact_id)
        except Exception as e:
            return False

        contact_free_slots = contact_free_slots['start_time'].tolist()
        # department_free_slots_list = self.department_free_slots['start_time'].tolist()
        # time_slot = self.department_free_slots_list[0]
        for contact_time in contact_free_slots:
            if (contact_time in self.department_free_slots_list):
                return contact_time
        return False

    def generate_events(self):
        self.set_department_free_slots_list()
        patients = self.patients
        """
        The function get department and return events for the next 7 days for each contact of patients in department
        """
        for patient_id, row in patients.iterrows():

            contact_id = patients.loc[patient_id, ["contact_id"]][0]
            time = self.get_contact_availability(contact_id)

            if (time):
                print("Patient id: ", row['patient_id'], " contact_id: ", contact_id, "time:", time)
                self.department_free_slots_list.remove(time)
                try:
                    E.create_new_event(time, row['patient_id'], contact_id)
                except Exception as e:
                    # raise Exception("Error in create_event", e)
                    pass
            else:
                print("Contact have no optional meet time")


class SchedulerEvents():
    def __init__(self,session=None):
        if not session:
            self.engine = U.get_engine()
            self.session = U.get_session(self.engine)
        pass

    def run(self):
        departments = U.get_df(Users, self.session)
        for dept_num in departments.index.tolist():
            print(dept_num)
            try:
                d = Department(dept_num)
                d.generate_events()
            except Exception as e:
                print("Error in generate_events for department:{}".format(dept_num), e)
            continue

