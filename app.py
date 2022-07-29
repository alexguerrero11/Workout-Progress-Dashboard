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
    
    name = 'Workout Progress Data - Main2.0.csv'
    workout_data_file = pd.read_csv(name)
    
    st.dataframe(workout_data_file)
    

with features:
    st.header('The features I created')
    
