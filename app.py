from email import header
import streamlit as st
import pandas as pd

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()

with header:
    st.title('Welcome to Workout Dashboard project!')
    st.text('In this project I look into the progress of my workout and strength training.')
    
    
with dataset:
    st.header('My personal workout data.')
    st.text('I record my workouts daily and store them in a google sheet file.')
    
    # import file
    name = 'Workout Progress Data - master.csv'
    workout_data = pd.read_csv(name)
    
    # data cleaning
    #workout_data = workout_data.set_index(workout_data["Date"])
    workout_data = workout_data.sort_values(by=['Date','Exercise','Sets'])
    
    
    #  -- SIDEBAR -- 
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
    
    st.dataframe(filter_selections)

with features:
    st.header('The features I created')
    
