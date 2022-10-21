# @Email:  contact@pythonandvba.com
# @Website:  https://pythonandvba.com
# @YouTube:  https://youtube.com/c/CodingIsFun
# @Project:  Sales Dashboard w/ Streamlit


import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
# from apps.core import util as U
# from apps.authentication.models import Event




# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

# df = U.get_df(Event, session)

df = pd.read_sql_table('events', 'mysql+pymysql://naya:NayaPass1!@35.193.190.203/temi_v3')
# print(df.columns)
# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
department_id = st.sidebar.multiselect(
    "Select the City:",
    options=df["department_id"].unique(),
    default=df["department_id"].unique()
)

patient_id = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["patient_id"].unique(),
    default=df["patient_id"].unique(),
)

# gender = st.sidebar.multiselect(
#     "Select the Gender:",
#     options=df["Gender"].unique(),
#     default=df["Gender"].unique()
# )

df_selection = df.query(
    "department_id == @department_id & patient_id ==@patient_id"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_meets = df[df['status'] ==2].count().shape[0]
total_meets2 = df[df['status'] ==2].count().shape[0]
total_meets3 = df[df['status'] ==2].count().shape[0]
# average_rating = round(df_selection["Rating"].mean(), 1)
# star_rating = ":star:" * int(round(average_rating, 0))
# average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
# left_column= st.columns(1)
with left_column:
    st.subheader("סהכ שיחות שבועיות")
    st.subheader(f"{total_meets:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{total_meets2} {total_meets2}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {total_meets3}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
meets_by_patient = (
    # df_selection.groupby(by=["patient_id"]).sum()[["Total"]].sort_values(by="Total")
    df_selection.groupby(by=["patient_id"]).size().to_frame('data')['data']
)
fig_product_sales = px.bar(
    meets_by_patient,
    x="data",
    y=meets_by_patient.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * total_meets2,
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
#
# # SALES BY HOUR [BAR CHART]
# sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
# fig_hourly_sales = px.bar(
#     sales_by_hour,
#     x=sales_by_hour.index,
#     y="Total",
#     title="<b>Sales by hour</b>",
#     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
#     template="plotly_white",
# )
# fig_hourly_sales.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )
#
#
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)