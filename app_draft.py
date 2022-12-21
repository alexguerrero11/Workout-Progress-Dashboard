import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Workout Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")

# -- IMPORT CSV FILE --
workout_data = pd.read_csv("Workout Progress Data - master.csv")

# # -- DISPLAYING DATAFRAME --
# st.dataframe(workout_data)

# -- WORKING WITH DF
workout_data = workout_data.sort_values(by=['Date','Exercise','Sets'])

# -- SIDEBAR -- 
st.sidebar.header("Please Filter Here:")
    
date = st.sidebar.multiselect(
    "Select a date:",
    options= workout_data["Date"].unique(),
    default= workout_data["Date"].unique()
)

muscle_type = st.sidebar.multiselect(
    "Select a muscle type:",
    options= workout_data["Muscle_group"].unique(),
    default= workout_data["Muscle_group"].unique()
)

filter_selections = workout_data.query(
    "Date == @date & Muscle_group == @muscle_type"
)

# -- DISPLAYING FILTERED DATAFRAME --
st.dataframe(filter_selections)

# -- MAINPAGE -- 
st.title(":bar_chart: Workout Dashboard")
st.markdown("##")

# TOP KPI's
total_volume = workout_data