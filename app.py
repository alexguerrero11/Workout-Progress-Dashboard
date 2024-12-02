import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


# Load data from CSV
file_path = 'data/workout - log.csv'
df = pd.read_csv(file_path)

# Convert Date to datetime
df['Date'] = pd.to_datetime(df['Date'], format="%m/%d/%Y").dt.strftime("%Y-%m-%d")

# Ensure Exercise, Muscle, and Note are strings
df['Exercise'] = df['Exercise'].astype(str)
df['Muscle'] = df['Muscle'].astype(str)
df['Note'] = df['Note'].fillna("").astype(str)

# Convert Sets and Reps to float64
df['Sets'] = df['Sets'].fillna(0).astype(int)
df['Reps'] = df['Reps'].fillna(0).astype(int)

# Convert Weight to float64, keeping NaN for missing values
df['Weight'] = df['Weight'].astype(float)

# Convert Duration to object (string) with default value for missing data
df['Duration'] = df['Duration'].fillna("00:00:00").astype(str)

# Convert Total_volume to float64, keeping NaN for missing values
df['Total_volume'] = df['Reps'] * df['Weight'] 
df['Total_volume'] = df['Total_volume'].astype(float)


# Sort dataframe according to date, exercise, sets
df = df.sort_values(by=['Date','Exercise','Sets'])

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

# KPIs
count_per_week = len(df.query(" Date >= @start_of_week & Date <= @end_of_Week")['Date'].unique())
count_per_month = len(df.query(" Date >= @first_day_of_month & Date < @next_month_first_day")['Date'].unique())
count_total_records = len(df['Date'].unique())

# Latest Record
latest_record = df[df['Date'] == df['Date'].unique()[-1]]

# Sidebar for exercise selection
selected_muscle_group = st.sidebar.selectbox('Select Muscle Group:', df['Muscle'].unique())

# Filter data based on selected muscle group
filtered_data = df[df['Muscle'] == selected_muscle_group]

# Overview of all exercises according to muscle type
st.title('Workout Progress Dashboard')
st.sidebar.header('Filters')
st.sidebar.write(f'**Selected Muscle Group:** {selected_muscle_group}')

# Display main KPI's
st.markdown('### Main Metrics')
col1, col2, col3 = st.columns(3)
col1.metric(label='Count of Days in Current Week', value=f'{count_per_week}')
col2.metric(label='Count of Days in Current Month', value=f'{count_per_month}')
col3.metric(label='Total Number of Records', value=f'{count_total_records}')


# Display data table
st.subheader('Workout Data Overview')
st.dataframe(filtered_data)

# Highlight weights over time for the selected muscle group
st.subheader('Weights Over Time')

# Group data by Exercise and plot weight progression
for exercise, data in filtered_data.groupby('Exercise'):
    st.line_chart(data[['Date', 'Weight']].set_index('Date'), use_container_width=True)
    st.markdown(f"**Exercise:** {exercise}")

st.markdown('### Latest Record')
st.text(f"Recent muscle groups worked out: {latest_record['Muscle'].unique()}")
# st.dataframe(latest_record[['Muscle_group', 'Exercise']])
st.dataframe(latest_record)

# Show the app
st.sidebar.write('---')
st.sidebar.write('Created with Alex Guerrero')
