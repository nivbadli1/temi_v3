import sys
sys.path.append("/home/naya/TEMI_PROJECT/src/backend/classes")

from sqlalchemy import Column, Time
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
import configparser
from sqlalchemy import create_engine
import pandas as pd
import utils as U
from datetime import datetime as dt

# Define env
config = configparser.ConfigParser()
config.read('/home/naya/TEMI_PROJECT/src/config.ini')

# Create engine
e = "mysql+pymysql://{}:{}@{}:3306/{}".format( \
    config['MYSQL']['user'], config['MYSQL']['password'], config['MYSQL']['server'], config['MYSQL']['database'])
engine = create_engine(e)


Base = declarative_base()
metadata = Base.metadata

class Deprtment(Base):
    __tablename__ = 'departments'

    num = Column(INTEGER(11), primary_key=True, nullable=False)
    _from = Column('from', Time, primary_key=True, nullable=False)
    to = Column(Time, primary_key=True, nullable=False)
    day = Column(INTEGER(11), primary_key=True, nullable=False)

    # Get nun of dept
    def __init__(self, num):

        self.num = num
        self._NEXT_DAYS_NUM = 7
        self._CALL_FREQ = 15
        self.patients = None
        self.contacts = None
        self.events = None
        self.free_time_slots = None
        self.all_time_slots = None
        self.next_events = None
        self.set_dept_attrs()

    def set_dept_attrs(self):
        self.set_patients()
        self.set_contacts()
        self.set_events()
        self.set_next_events_dept()

    # Add time interval
    def set_events(self):
        df = pd.read_sql_table('events', engine)
        # df = df[df.start_time >= dt.now()]
        self.events =  df.merge(self.patients,left_on="patient_id",right_index=True)

    def set_patients(self):
        df = pd.read_sql_table('patients', engine)
        self.patients = df[df.department == self.num]

    def set_contacts(self):
        df = pd.read_sql_table('contacts', engine)
        self.patients = self.patients.merge(df, left_on='patient_id', right_on='patient_id')

    def get_dept_times(self):
        """
        the function return df of dept number
        :return:
        """
        df = pd.read_sql_table(self.__tablename__, engine)
        return df[df.num == self.num]

    def set_next_events_dept(self):
        self.next_events = self.events[self.events.start_time >= dt.now()]

    def get_next_pending_events(self):
        return self.next_events[self.next_events.status ==0]

    def get_dept_free_time_slots(self):
        self.get_dept_all_time_slots()
        self.free_time_slots.merge(self.next_events)

    def get_dept_all_time_slots(self):
        """The function return time_slots of the department"""
        # Read dept table from db
        df = self.get_dept_times()
        df = U.transform_time_df_to_datetime_df(df,self._NEXT_DAYS_NUM)
        df = U.get_df_time_slots(df, self._CALL_FREQ + 5)
        self.all_time_slots = df
        return df

    def get_contact_free_time(self,contact):
        df = pd.read_sql_table('contacts_time', engine).merge(self.contacts).\
            loc[:,["contact_id","day","from","to"]]
        self.contacts_times = df

    def get_slot(self):
        return self.free_time_slots.min()

    def get_contact_next_event(self,contact_id):
        return self.next_events.loc[self.next_events["contact_id"] == 1,["start_time"]].max()[0]

    def check_contact_hours(self,contact_id,event_time):
        for index, row in self.contacts_times.loc[self.contacts_times == contact_id].itertuples():
            if (row[0] <= event_time, row[1]):
                return True
        return False

    def generate_events(self):
        # Get dept optional times
        self.get_dept_free_time_slots()

        # Convert columns of day and time to datetime columns
        contacts_free_times = U.transform_time_df_to_datetime_df(self.contacts_times, 30)

        for patient_id, row in self.patients_df.iterrows():
            event = False
            free_slot = self.get_slot()
            contact_id = self.patients.loc[self.patients["patient_id"]==patient_id,["patient_id","contact_id"]]

            # For all time free slots or no event sched yet
            for index,row in self.free_time_slots or event:
                # If contact hour return true mean the time is availble contact hour create event, else itear until find time
                if(self.check_contact_hours(contact_id,free_slot)):
                    print("CREATE EVENT")
                    event = True
                else:
                    free_slot = self.get_slot()

            if(event==False):print("Contact have no optional meet time")