from email import header
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

# --------------------------------------------------
# import data and clean columns
workout_data = pd.read_csv("data/main.csv")
data_columns = ['Date', 'Exercise', 'Muscle_group', 'Sets', 'Reps', 'Weight', 'Duration', 'Note', 'Total_volume']
workout_data = workout_data[data_columns]
workout_data = workout_data.sort_values(by=['Date','Exercise','Sets'])
workout_data['Date'] = pd.to_datetime(workout_data['Date'], format="%m/%d/%Y")

# Date Parameters -- Calculations
today = date.today()
start_of_week = today - relativedelta(days=today.weekday())
end_of_Week = start_of_week + relativedelta(days=6)
first_day_of_month = today.replace(day=1)
next_month_first_day = today + relativedelta(months=1, day=1)

# Formatting into string
today = today.strftime('%m-%d-%Y')
start_of_week = start_of_week.strftime('%m-%d-%Y')
end_of_Week = end_of_Week.strftime('%m-%d-%Y')
first_day_of_month = first_day_of_month.strftime('%m-%d-%Y')
next_month_first_day = next_month_first_day.strftime('%m-%d-%Y')


count_per_week = len(workout_data.query(" Date >= @start_of_week & Date <= @end_of_Week")['Date'].unique())
count_per_month = len(workout_data.query(" Date >= @first_day_of_month & Date < @next_month_first_day")['Date'].unique())
count_total_records = len(workout_data['Date'].unique())

# --------------------------------------------------
# header
st.title('Welcome to Workout Dashboard!')
st.text('In this project I look into the progress of my workout and strength training.')
    
# KPIS
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric(label='Count of Days in current Week', value=f'{count_per_week}')
col2.metric(label='Count of Days in current Month', value=f'{count_per_month}')
col3.metric(label='Total Number of Records', value=f'{count_total_records}')



# --------------------------------------------------
# sidebar
st.sidebar.header("Please Filter Here:")

# date = st.sidebar.multiselect(
#     "Select a date:",
#     options= workout_data["Date"].unique(),
#     default= workout_data["Date"].unique()
# )

muscle_type = st.sidebar.multiselect(
    "Select a muscle type:",
    options= workout_data["Muscle_group"].unique(),
    default= workout_data["Muscle_group"].unique()
)

filter_selections = workout_data.query(
    # "Date == @date & Muscle_group == @muscle_type"
    "Muscle_group == @muscle_type"

)


# st.dataframe(filter_selections)
    
