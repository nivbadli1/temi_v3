import pandas as pd
from sqlalchemy.event import Events

from apps.authentication.models import Users,Patient,Contact,ContactTime,Event,UserTime
from apps import db
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime as dt
import utils as U

e = 'mysql+pymysql://naya:NayaPass1!@35.226.141.122/temi_v3'
engine = create_engine(e)


# p = session.query(Patient).filter_by(patient_id=200001).first()

Session = sessionmaker(bind=engine)
session = Session()

def get_df(cls,value=None):
    # SQLAlCHEMY ORM QUERY TO FETCH ALL RECORDS
    df = pd.read_sql_query(
        sql=session.query(cls).statement,
        con=engine,
        index_col=cls.__mapper__.primary_key[0].name
    )
    if(value):
        if('contact' in cls.__name__.lower()):
            return df[(df['contact_id'] == value)]
        elif('user' in cls.__name__.lower()):
            return df[(df['department_id'] == value)]
    return df



def get_next_events(cls,value,event_status=None):
    """
    The function return next evetns for cls (Patient,Contact,Dept)
    """
    events = get_df(Event)
    if(event_status):return events[(events[cls.__mapper__.primary_key[0].name] == value) & (events.status == event_status)]
    return events[(events[cls.__mapper__.primary_key[0].name] == value)]


def transform_time_df(cls,next_days_num):
    """
    The function get cls and return cls_time with next days dates
    """
    # Get cls Time table
    df = get_df(eval(cls.__name__ + 'Time'),13)
    df = U.convert_time_cols_to_time_delta(df, ['from_hour', 'to_hour'])
    temp_df = U.get_next_days_dates(next_days_num)
    df = df.merge(temp_df ,how='inner')
    df['from_date'] = df['from_hour'] + df['next_week_date']
    df['to_date'] = df['to_hour'] + df['next_week_date']
    df.drop(columns=["from_hour","to_hour","day","next_week_date"],inplace=True)
    return df

def get_df_time_slots(cls,freq=None,next_days_num=None):
    """
    :param df: df with from_dates and to_dates per cls
    :param freq: freq for slot return df
    :return: slote df from min datetime until max datetime with freq got
    """
    if(not freq):freq=20
    if(not next_days_num):next_days_num=30
    stg_df = transform_time_df(cls,next_days_num)
    freq = str(freq) + "min"
    df = pd.concat([pd.DataFrame({\
                'start_time': U.get_date_range(start=row['from_date'],end=row["to_date"],freq=freq)})\
                for index,row in stg_df.iterrows()]).sort_values(by="start_time").reset_index(drop=True)
    return df

def get_free_slots(cls,value):
    time_slots_df = get_df_time_slots(cls)
    next_event_df = get_next_events(cls,value)
    return time_slots_df.merge(next_event_df)

# df = get_df_time_slots(Contact,20,7)
df = get_free_slots(Contact,13)
print(df)
# def get_free_slots(cls_df:pd.DataFrame,events:pd.DataFrame,statusCode:int):
#     events_df = events.merge(cls_df, left_on=cls_df.index, right_index=True)
#     return events[(events.start_time >= dt.now()) & (events.status == 0)]



# patients = get_df(Patient)
# contacts = get_df(Contact)
# deprtments = get_df(Users)
# events = get_df(Event)
# df = get_free_slots(patients,events,0)
# print(df)



