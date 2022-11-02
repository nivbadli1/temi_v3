import sys
sys.path.append("/opt/gitshit/temi_v3/")
from apps.core import util as U
from apps.dashboards import dashboard_utils as SU
from apps.authentication.models import Event, Contact, Patient, Users
import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: ./static/assets/img/logo-ct-dark2.jpeg;
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "My Company Name";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

from PIL import Image
import streamlit as st

# You can always call this function where ever you want
st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="🤖 📲 ",
    layout="wide",
)
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path=r"C:\Users\User\PycharmProjects\temi_v3\apps\static\assets\img\logo-ct-dark2.jpeg", width=50, height=60)



_SESSION = U.get_session(engine=U.get_engine())


@st.experimental_memo
def get_tables():
    events = U.get_df(Event, _SESSION)
    patients = U.get_df(Patient, _SESSION)
    contacts = U.get_df(Contact, _SESSION)
    events = events.merge(patients, how='left', on='patient_id')
    events = events.merge(contacts, how='left', on='contact_id')
    return events

# Filter dataframe filtrerd by deprtment
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns
    Args:
        df (pd.DataFrame): Original dataframe
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    # modify = st.checkbox("לחץ כאן לסינון נתונים")
    #
    # if not modify:
    #     return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("סינון נתונים לפי", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"ערכים לסינון עמודה: {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"ערכים לסינון עמודה: {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"ערכים לסינון עמודה: {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df

df = get_tables()
# df.info()
# departments_df = U.get_df(Users, _SESSION)
st.image(my_logo)
# dashboard title
# st.title("אחיות מסך ניהול ומעקב")
st.markdown("<h1 style='text-align: center; color: grey;'>מסך ניהול אחיות</h1>", unsafe_allow_html=True)

def left_align(s, props='text-align: left;'):
    return props
# top-level filters
# dept_filter = st.selectbox("בחר מספר מחלקה", pd.unique(departments_df["username"]))

# creating a single-element container
placeholder = st.empty()


# dataframe filter for deprtment - main filter
# df = df[df["department_id_y"] == dept_filter]

display_df = SU.transform_events_df(df)


# Mertics section
# for seconds in range(200):
with placeholder.container():
    # create three columns
    # kpi1, kpi2, kpi3 = st.columns(3)
    kpi1,kpi2,kpi3,kpi4 = st.columns(4)
    # creating KPIs
    measures_dict = SU.get_measures()


    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label=" 📲 מספר השיחות שהתקיימו בשבוע האחרון ",
        value=int(measures_dict.get('last_week_events_done_count')),

    )

    kpi2.metric(
        label=" 📵 מספר השיחות שהתבטלו בשבוע האחרון",
        value=round(measures_dict.get('last_week_events_done_count')),

    )

    kpi3.metric(
        label=" 🔜 מספר השיחות שממתינות לביצוע בשבוע הבא",
        value=round(measures_dict.get('last_week_events_done_count')),

    )

    kpi4.metric(
        label="	👨‍👩‍👦 דיירים שאין להם אנשי קשר רשומים",
        value=round(measures_dict.get('last_week_events_done_count')),

    )
# st.markdown("###deprtment df")

    st.dataframe(filter_dataframe(display_df))

    df_xlsx = SU.to_excel(display_df)
    st.download_button(label='📥 להורדת התוצאות לאקסל',
                       data=df_xlsx,
                       file_name='events.xlsx')
