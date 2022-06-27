from fileinput import filename
import pandas as pd
import streamlit as st
import plotly as px
from PIL import Image

st.set_page_config(page_title='Workout Data')
st.header('Welcome back, ready to check your progress!')
st.subheader('Check this out:')

### Data
name = 'Workout Progress Data - Main2.0.csv'

data_file = pd.read_csv(name)

name = 'Exercise_list.csv'
exercise_file = pd.read_csv(name)


st.dataframe(data_file)

st.dataframe(exercise_file)