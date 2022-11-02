import sys
sys.path.append("/opt/gitshit/temi_v3/")
import datetime as dt
import pandas as pd
# from apps.dashboards import dashboard_app as D
import pandas as pd
from io import BytesIO

from apps.core import util as U
from apps.authentication.models import Event, Contact, Patient


def get_filtered_days_df(df, date_column, method, value):
    """
    The function get date column and df and return df with excpeted dates
    """
    if method == 'last':
        return df[df[date_column].between(dt.datetime.now() - dt.timedelta(days=7), dt.datetime.now())]
    elif method == "first":
        return df[df[date_column].between(dt.datetime.now(), dt.datetime.now() + dt.timedelta(days=7))]


def get_calls_by_status(df, status):
    return df[df['status'] == status]


def get_non_assignment_patients(patients_df, contacts_df):
    try:
        # Convert contacts_patient_id to int
        contacts_df['patient_id'] = contacts_df['patient_id'].astype('Int64')
    except Exception as e:
        pass
    p = patients_df.merge(contacts_df, left_index=True, right_on='patient_id', how='left').reset_index()
    # Return id of patient has no assigment
    return p[p['index'].isnull() == True]

def get_events_status(event_status):
    return ('שיחה בוצעה' if event_status == 0 else 'שיחה בוטלה' if event_status == 1 else 'שיחה ממתינה לביצוע')

def transform_events_df(df):
    df['status'] = df['status'].apply(get_events_status)
    # Transform dataframe for website
    df= df[['start_time','f_name_x','l_name_x','f_name_y','l_name_y','max_calls','status','mail','phone']]
    df.columns = ['תאריך תחילת שיחה','שם פרטי דייר','שם משפחה דייר','שם פרטי איש קשר','שם משפחה איש קשר','מספר שיחות שבועיות','סטטוס שיחה','מייל','מספר טלפון']

    return df

def get_tables():
    session = U.get_session(engine=U.get_engine())
    events = U.get_df(Event, session)
    patients = U.get_df(Patient, session)
    contacts = U.get_df(Contact, session)
    events = events.merge(patients, how='left', on='patient_id')
    events = events.merge(contacts, how='left', on='contact_id')
    return events

def get_measures(session=None):
    """
    The function return measures for the dashboard by key and value
    """
    if not session:
        # Get session
        session = U.get_session(engine=U.get_engine())
    # Get df
    patients = U.get_df(Patient, session)
    contacts = U.get_df(Contact, session)

    # Get events table
    events = get_tables()

    # Get events for last week
    last_week_events = get_filtered_days_df(events, 'start_time', 'last', '1W')

    # Get events for next week
    next_week_events = get_filtered_days_df(events, 'start_time', 'first', '1W')

    # TOP KPI's
    last_week_events_done_count = get_calls_by_status(last_week_events, 2).shape[0]
    last_week_events_cancel_count = get_calls_by_status(last_week_events, 1).shape[0]
    next_week_events_pending_count = get_calls_by_status(next_week_events, 0).shape[0]
    patients_with_no_assignments = get_non_assignment_patients(patients, contacts).shape[0]
    return dict(last_week_events_done_count=last_week_events_done_count,
                last_week_events_cancel_count=last_week_events_cancel_count,
                next_week_events_pending_count=next_week_events_pending_count,
                patients_with_no_assignments=patients_with_no_assignments)


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


