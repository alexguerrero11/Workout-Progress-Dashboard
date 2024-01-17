import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV
file_path = 'data/workout-data - main.csv'
df = pd.read_csv(file_path)

# Sidebar for exercise selection
selected_muscle_group = st.sidebar.selectbox('Select Muscle Group:', df['Muscle_group'].unique())

# Filter data based on selected muscle group
filtered_data = df[df['Muscle_group'] == selected_muscle_group]

# Overview of all exercises according to muscle type
st.title('Workout Progress Dashboard')
st.sidebar.header('Filters')
st.sidebar.write(f'**Selected Muscle Group:** {selected_muscle_group}')

# Display data table
st.subheader('Workout Data Overview')
st.dataframe(filtered_data)

# Highlight weights over time for the selected muscle group
st.subheader('Weights Over Time')

# Group data by Exercise and plot weight progression
for exercise, data in filtered_data.groupby('Exercise'):
    st.line_chart(data[['Date', 'Weight']].set_index('Date'), use_container_width=True)
    st.markdown(f"**Exercise:** {exercise}")

# Show the app
st.sidebar.write('---')
st.sidebar.write('Created with ❤️ by Your Name')
