import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import plotly.express as px


def filter_data(df):
    st.sidebar.header("Filters")
    
    # Date Range Picker
    start_date, end_date = st.sidebar.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])
    filtered_df = df[(df['Date'] >= pd.Timestamp(start_date)) & (df['Date'] <= pd.Timestamp(end_date))]
    
    # Muscle Group
    unique_muscles = df['Muscle'].unique()
    selected_muscle = st.sidebar.selectbox("Select Muscle Group", options=unique_muscles)
    filtered_df = filtered_df[filtered_df['Muscle'] == selected_muscle]

    # Exercises
    unique_exercises = filtered_df['Exercise'].unique()
    selected_exercises = st.sidebar.multiselect("Select Exercises", unique_exercises, default=unique_exercises)
    filtered_df = filtered_df[filtered_df['Exercise'].isin(selected_exercises)]

    return filtered_df


def plot_data(df):
    st.markdown("### Visualizations")

    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    # Exercise Frequency
    st.subheader("Exercise Frequency")
    exercise_counts = df['Exercise'].value_counts().reset_index()
    exercise_counts.columns = ['Exercise', 'Count']
    fig = px.bar(exercise_counts, x='Count', y='Exercise', orientation='h', title="Frequency of Exercises", color='Count', text='Count')
    st.plotly_chart(fig, use_container_width=True)

    # Weight vs. Reps (Scatter Plot)
    st.subheader("Weight vs. Reps")
    fig = px.scatter(df, x='Reps', y='Weight', color='Exercise', size='Total_volume', hover_data=['Date'], title="Weight vs. Reps")
    st.plotly_chart(fig, use_container_width=True)

    # Total Volume Over Time
    st.subheader("Total Volume Over Time")
    volume_trend = df.groupby('Date')['Total_volume'].sum().reset_index()
    fig = px.line(volume_trend, x='Date', y='Total_volume', title="Total Volume Progression", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # Distribution of Reps
    st.subheader("Distribution of Reps")
    fig = px.histogram(df, x='Reps', nbins=20, color='Muscle', title="Reps Distribution")
    st.plotly_chart(fig, use_container_width=True)


def analytics(df):
    st.title("📊 Workout Analytics")

    # Filter data
    filtered_df = filter_data(df)

    # Display filtered data
    with st.expander("Filtered Workout Data"):
        st.dataframe(filtered_df.tail())
        
    # Plot data
    plot_data(filtered_df)
