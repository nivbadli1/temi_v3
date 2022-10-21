#!/usr/bin/env python3
import re

import pymysql
import pandas as pd
import pandas as pd
import numpy as np
import uuid
import sys
from datetime import datetime, timedelta, date as dt
from apps import config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, class_mapper
from run import app_config


def computed_operator(column, v):
    """
    The function get dict of columns and values and tranlsate dict to filter
    """
    if re.match(r"^!", v):
        """__ne__"""
        val = re.sub(r"!", "", v)
        return column.__ne__(val)
    if re.match(r">(?!=)", v):
        """__gt__"""
        val = re.sub(r">(?!=)", "", v)
        return column.__gt__(val)
    if re.match(r"<(?!=)", v):
        """__lt__"""
        val = re.sub(r"<(?!=)", "", v)
        return column.__lt__(val)
    if re.match(r">=", v):
        """__ge__"""
        val = re.sub(r">=", "", v)
        return column.__ge__(val)
    if re.match(r"<=", v):
        """__le__"""
        val = re.sub(r"<=", "", v)
        return column.__le__(val)
    if re.match(r"(\w*),(\w*)", v):
        """between"""
        a, b = re.split(r",", v)
        return column.between(a, b)
    """ default __eq__ """
    return column.__eq__(v)


def get_filter_statement(cls, filter_by=None):
    """
    The function get filter_by dict and return a filter statement
    """
    filters = []
    for k, v in filter_by.items():
        mapper = class_mapper(cls)
        if not hasattr(mapper.columns, k):
            continue
        filters.append(computed_operator(mapper.columns[k], "{}".format(v)))
    return filters


def get_df(cls, session, filter_by=None):
    """ The function get cls to query and can also get filter_dict with column and values to filter and return dataframe of the class"""
    # SQLAlCHEMY ORM QUERY TO FETCH ALL RECORDS
    sql = session.query(cls).statement
    if (filter_by):
        sql = session.query(cls).filter(*get_filter_statement(cls, filter_by)).statement
    df = pd.read_sql_query(
        sql=sql,
        con=session.bind,
        index_col=cls.__mapper__.primary_key[0].name
    )
    return df


def get_engine():
    """
    The function return engine of application
    """
    e = config.Config.SQLALCHEMY_DATABASE_URI
    return create_engine(e)


def get_session(engine):
    """
    The function get engine and return session
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# # The function get start end and freq and return pd_data range
def get_date_range(start, end, freq):
    return pd.date_range(start=start, end=end, freq=freq)


def transform_time_df(df, next_days_num):
    """
    The function get time_df to transform and return cls_time with next days dates
    """

    df = convert_time_cols_to_time_delta(df, ['from_hour', 'to_hour'])
    temp_df = get_next_days_dates(next_days_num)
    df = df.merge(temp_df, how='inner')
    df['from_date'] = df['from_hour'] + df['next_week_date']
    df['to_date'] = df['to_hour'] + df['next_week_date']
    df.drop(columns=["from_hour", "to_hour", "day", "next_week_date"], inplace=True)
    return df


def weeks_day_to_israeli_days(lst):
    """
    The function get lst and return the israeli days number for given
    """
    israeli_days = {"0": 1, "1": 2, "2": 3, "3": 4, "4": 5, "5": 6, "6": 7}
    return [israeli_days[str(i)] for i in lst]


def convert_time_cols_to_time_delta(df, cols):
    """
    :param df: df to convert cols
    :param cols: cols list names to convert
    :return: df with time_delta_cols
    """
    for col in cols:
        df[col] = pd.to_timedelta(df[col].astype(str))
    return df


# The function get days num and return  dataframe with num israeli day and the date for next days
def get_next_days_dates(next_days_num):
    """
    :param next_days: next days to get dates
    :return: df with next week date
    """
    df = pd.DataFrame()
    # Get next 7 forroword days as dates
    df["next_week_date"] = pd.date_range(start=dt.today(), periods=next_days_num)

    # Get next 7 days as week day
    df["next_week_day"] = pd.date_range(start=dt.today(), periods=next_days_num).strftime("%w")

    # Convert day as israeli days number
    df["day"] = weeks_day_to_israeli_days(df["next_week_day"])
    # print(df)
    return df.drop(columns=['next_week_day'])


def get_df_time_slots(df_time, freq=None, next_days_num=None):
    """
    :param df: df with from_dates and to_dates per cls
    :param freq: freq for slot return df
    :return: slote df from min datetime until max datetime with freq got
    """
    if (not freq): freq = 20
    if (not next_days_num): next_days_num = 5
    stg_df = transform_time_df(df_time, next_days_num)
    freq = str(freq) + "min"
    df = pd.concat([pd.DataFrame({ \
        'start_time': get_date_range(start=row['from_date'], end=row["to_date"], freq=freq)}) \
        for index, row in stg_df.iterrows()]).sort_values(by="start_time").reset_index(drop=True)
    return df
#
# def concact_time_cols_and_date(df,next_days_num):
#     """
#     :param df: df with time cols
#     :return: df with date cols
#     """
#     # Merge 7 next days dates with availble dates and hours
#     temp_df = get_next_days_dates(next_days_num)
#     df = df.merge(temp_df ,how='inner')
#     df['from_date'] = df['from_hour'] + df['next_week_date']
#     df['to_date'] = df['to_hour'] + df['next_week_date']
#     return df.drop(columns=["from_hour","to_hour","day","next_week_date"])
#

#
# def transform_time_df_to_datetime_df(df,next_days_num):
#     """
#     :param df: df with time cols
#     :param next_days_num: how many days forrword to get dates
#     :return: df with next dates time
#     """
#     df = convert_time_cols_to_time_delta(df, ['from_hour', 'to_hour'])
#     df = concact_time_cols_and_date(df,next_days_num)
#     return df
#
# # The function get start end and freq and return pd_data range
# def get_df_date_range(start,end,freq):
#     """
#     :param start: start datetime
#     :param end: end datetime
#     :param freq: freq datetime
#     :return: df with date range
#     """
#     return pd.date_range(start=start,end=end,freq=freq)
#
# # The function get availble_hours df and return time period dataframe
# def get_df_time_slots(df,freq):
#     """
#     :param df: datetime dataframe with days and time from to
#     :param freq: freq for slot return df
#     :return: slote df from min datetime until max datetime with freq got
#     """
#     freq = str(freq) + "min"
#     df = pd.concat([pd.DataFrame({\
#                 'start_time': get_date_range(start=row['from_date'],end=row["to_date"],freq=freq)})\
#                 for index,row in df.iterrows()])
#     return df
#
#
# def get_all_deprtments(engine):
#     return list(pd.read_sql_table('Users',engine).num.unique())
#
# def read_table(table_name,engine):
#         return pd.read_sql('SELECT * FROM {}'.format(table_name),
#             engine
#             )
#
#
#
# # # The function get df and start time, create the event and reutrn url
# def create_event(df,start_time,contact_id,patient_id):
#     df.at[start_time,'event']=1
#     return df
#
# def check_if_date_between(date,start,end):
#     return start <= date <= end
#

#
# # The function get availble_hours df and return time period dataframe
# def get_availble_hours_df(availble_hours_df):
#     df = pd.concat([pd.DataFrame({\
#                 'start_time': get_date_range(start=row['from'],end=row["to"],freq='20min')})\
#                 for index,row in availble_hours_df.iterrows()])
#     df.set_index("start_time",inplace=True)
#     return df
#
# # The function get contacts data frame and patient id and return all contacts belong to the patient
# def get_all_contacts_of_patient(df,patient_id):
#     return df.loc[df.contact_patient == patient_id].index
#
# # The function get df and return df with all datetime columns
# def convert_columns_to_date_time(df):
#     for col in df:
#         df[col] = pd.to_datetime(df[col])
#     return df
#
# # The function iterate over all contacts hours of contact and return true if time availble
# def check_contact_hours(df,avaible_time,contact_id):
#     for index,row in df.loc[1,['availble_contact_hours']].itertuples():
#         if(row[0] <= avaible_time ,row[1]):
#             return True
#     return False
#
# # The function get df and return availble times if event is none
# def get_all_availble_times(df):
#     return df.loc[a_df_hours.event.isna()]
#
# # The function get df and return the minimum date availble
# def get_min_availble_time(df):
#     return df.loc[df.event.isna()].index.min()
#
#
#

#
# # The function return dataframe with num israeli day and the date for next 7 days
# def get_next_days_dates(next_days):
#     df = pd.DataFrame()
#     # Get next 7 forroword days as dates
#     df["next_week_date"] = pd.date_range(start=dt.today(),periods=next_days)
#
#     # Get next 7 days as week day
#     df["next_week_day"] = pd.date_range(start=dt.today(),periods=next_days).strftime("%w")
#
#     # Convert day as israeli days number
#     df["day"] = weeks_day_to_israeli_days(df["next_week_day"])
#     return df
#
#
# # The function get start end and freq and return pd_data range
# def get_date_range(start,end,freq):
#     return pd.date_range(start=start,end=end,freq=freq)
#
# # The function get availble_hours df and return time period dataframe
# # def get_availble_hours_df(availble_hours_df,freq):
# #     # The function concat each day availble hours
# #     df = pd.concat([pd.DataFrame({\
# #                 'start_time': get_date_range(start=row['from_date'],end=row["to_date"],freq=freq)})\
# #                 for index,row in availble_hours_df.iterrows()])
# #     df.set_index("start_time",inplace=True)
# #     return df
#
# # The function get dataframe with availble dates and freq and return time slots beteen
# def get_time_slots(dates_df,freq):
#     # The function concat each day availble hours
#     df = pd.concat([pd.DataFrame({\
#                 'start_time': get_date_range(start=row['from_date'],end=row["to_date"],freq=freq)})\
#                 for index,row in df_dates.iterrows()])
#     df.set_index("start_time",inplace=True)
#     return df
