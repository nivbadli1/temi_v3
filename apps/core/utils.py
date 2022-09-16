#!/usr/bin/env python3
import pymysql
import pandas as pd
import pandas as pd
import numpy as np
import uuid
import sys
from datetime import datetime,timedelta,date as dt

def get_free_slots(days:int,object):



def convert_time_cols_to_time_delta(df,cols):
    """
    :param df: df to convert cols
    :param cols: cols list names to convert
    :return: df with time_delta_cols
    """
    for col in cols:
        df[col] = pd.to_timedelta(df[col].astype(str))
    return  df

def concact_time_cols_and_date(df,next_days_num):
    """
    :param df: df with time cols
    :return: df with date cols
    """
    # Merge 7 next days dates with availble dates and hours
    temp_df = get_next_days_dates(next_days_num)
    df = df.merge(temp_df ,how='inner')
    df['from_date'] = df['from'] + df['next_week_date']
    df['to_date'] = df['to'] + df['next_week_date']
    return df.drop(columns=["from","to","day","next_week_date"])

# The function get days num and return  dataframe with num israeli day and the date for next days
def get_next_days_dates(next_days_num):
    """
    :param next_days: next days to get dates
    :return: df with next week date
    """
    df = pd.DataFrame()
    # Get next 7 forroword days as dates
    df["next_week_date"] = pd.date_range(start=dt.today().date(),periods=next_days_num)

    # Get next 7 days as week day
    df["next_week_day"] = pd.date_range(start=dt.today(),periods=next_days_num).strftime("%w")

    # Convert day as israeli days number
    df["day"] = weeks_day_to_israeli_days(df["next_week_day"])
    print(df)
    return df.drop(columns=['next_week_day'])

def transform_time_df_to_datetime_df(df,next_days_num):
    """
    :param df: df with time cols
    :param next_days_num: how many days forrword to get dates
    :return: df with next dates time
    """
    df = convert_time_cols_to_time_delta(df, ['from', 'to'])
    df = concact_time_cols_and_date(df,next_days_num)
    return df

# The function get start end and freq and return pd_data range
def get_df_date_range(start,end,freq):
    """
    :param start: start datetime
    :param end: end datetime
    :param freq: freq datetime
    :return: df with date range
    """
    return pd.date_range(start=start,end=end,freq=freq)

# The function get availble_hours df and return time period dataframe
def get_df_time_slots(df,freq):
    """
    :param df: datetime dataframe with days and time from to
    :param freq: freq for slot return df
    :return: slote df from min datetime until max datetime with freq got
    """
    freq = str(freq) + "min"
    df = pd.concat([pd.DataFrame({\
                'start_time': get_date_range(start=row['from_date'],end=row["to_date"],freq=freq)})\
                for index,row in df.iterrows()])
    return df


def get_all_deprtments(engine):
    return list(pd.read_sql_table('departments',engine).num.unique())

def read_table(table_name,engine):
        return pd.read_sql('SELECT * FROM {}'.format(table_name),
            engine
            )



# # The function get df and start time, create the event and reutrn url
def create_event(df,start_time,contact_id,patient_id):
    df.at[start_time,'event']=1
    return df

def check_if_date_between(date,start,end):
    return start <= date <= end

# The function get start end and freq and return pd_data range
def get_date_range(start,end,freq):
    return pd.date_range(start=start,end=end,freq=freq)

# The function get availble_hours df and return time period dataframe
def get_availble_hours_df(availble_hours_df):
    df = pd.concat([pd.DataFrame({\
                'start_time': get_date_range(start=row['from'],end=row["to"],freq='20min')})\
                for index,row in availble_hours_df.iterrows()])
    df.set_index("start_time",inplace=True)
    return df

# The function get contacts data frame and patient id and return all contacts belong to the patient
def get_all_contacts_of_patient(df,patient_id):
    return df.loc[df.contact_patient == patient_id].index

# The function get df and return df with all datetime columns
def convert_columns_to_date_time(df):
    for col in df:
        df[col] = pd.to_datetime(df[col])
    return df

# The function iterate over all contacts hours of contact and return true if time availble
def check_contact_hours(df,avaible_time,contact_id):
    for index,row in df.loc[1,['availble_contact_hours']].itertuples():
        if(row[0] <= avaible_time ,row[1]):
            return True
    return False

# The function get df and return availble times if event is none
def get_all_availble_times(df):
    return df.loc[a_df_hours.event.isna()]

# The function get df and return the minimum date availble
def get_min_availble_time(df):
    return df.loc[df.event.isna()].index.min()



def weeks_day_to_israeli_days(lst):
    israeli_days = {"0":1,"1":2,"2":3,"3":4,"4":5,"5":6,"6":7}
    return [israeli_days[str(i)] for i in lst]

# The function return dataframe with num israeli day and the date for next 7 days
def get_next_days_dates(next_days):
    df = pd.DataFrame()
    # Get next 7 forroword days as dates
    df["next_week_date"] = pd.date_range(start=dt.today(),periods=next_days)

    # Get next 7 days as week day
    df["next_week_day"] = pd.date_range(start=dt.today(),periods=next_days).strftime("%w")

    # Convert day as israeli days number
    df["day"] = weeks_day_to_israeli_days(df["next_week_day"])
    return df


# The function get start end and freq and return pd_data range
def get_date_range(start,end,freq):
    return pd.date_range(start=start,end=end,freq=freq)

# The function get availble_hours df and return time period dataframe
# def get_availble_hours_df(availble_hours_df,freq):
#     # The function concat each day availble hours
#     df = pd.concat([pd.DataFrame({\
#                 'start_time': get_date_range(start=row['from_date'],end=row["to_date"],freq=freq)})\
#                 for index,row in availble_hours_df.iterrows()])
#     df.set_index("start_time",inplace=True)
#     return df

# The function get dataframe with availble dates and freq and return time slots beteen
def get_time_slots(dates_df,freq):
    # The function concat each day availble hours
    df = pd.concat([pd.DataFrame({\
                'start_time': get_date_range(start=row['from_date'],end=row["to_date"],freq=freq)})\
                for index,row in df_dates.iterrows()])
    df.set_index("start_time",inplace=True)
    return df