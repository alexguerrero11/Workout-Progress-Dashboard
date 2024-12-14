import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import plotly.express as px
import plotly.graph_objects as go

def load_data(file_path: str):
    """
    Load workout data from a CSV file and preprocess it.
    """
    try:
        df = pd.read_csv(file_path)
        # reformat columns
        df['Date'] = pd.to_datetime(df['Date'])
        # df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")
        df['Exercise'] = df['Exercise'].astype(str)
        df['Muscle'] = df['Muscle'].astype(str)
        df['Note'] = df['Note'].fillna("").astype(str)
        df['Sets'] = df['Sets'].fillna(0).astype(int)
        df['Reps'] = df['Reps'].fillna(0).astype(int)
        df['Weight'] = df['Weight'].fillna(0).astype(float)
        df['Duration'] = df['Duration'].fillna("00:00:00").astype(str)     
        df['Total_volume'] = df['Reps'] * df['Weight'] 
        df['Total_volume'] = df['Total_volume'].astype(float)
        # Sort dataframe according to date, exercise, sets
        df = df.sort_values(by=['Date','Exercise','Sets'])
        return df
    except FileNotFoundError:
        st.error("File not found. Please check the file path.")
    except Exception as e:
        st.error(f"Error loading data: {e}")
    return None


def display_kpis(df):
    """
    Display key performance indicators (KPIs).
    """
    today = date.today()
    start_of_week = today - relativedelta(days=today.weekday())
    start_of_last_week = start_of_week - relativedelta(weeks=1)
    end_of_last_week = start_of_week - relativedelta(days=1)

    # KPIs
    total_workouts = df['Date'].nunique()
    weekly_workouts = len(df.query("Date >= @start_of_week")['Date'].unique())
    last_week_workouts = len(df.query("Date >= @start_of_last_week & Date <= @end_of_last_week")['Date'].unique())

    st.markdown("### Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("Workouts This Week", weekly_workouts)
    col2.metric("Workouts Last Week", last_week_workouts)
    col3.metric("Total Workout Days", total_workouts)


def filter_data(df):
    """
    Add sidebar filters and return filtered data.
    """
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
    """
    Generate advanced visualizations using Plotly.
    """
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


def analytics():
    """
    Main analytics function for the Streamlit app.
    """
    st.title("📊 Workout Analytics")

    # Load data
    file_path = 'data/workout - log.csv'
    df = load_data(file_path)

    if df is None or df.empty:
        st.warning("No data available.")
        return

    # Display KPIs
    display_kpis(df)

    # Filter data
    filtered_df = filter_data(df)

    # Display filtered data
    with st.expander("Filtered Workout Data"):
        st.dataframe(filtered_df.tail())
        
    # Plot data
    plot_data(filtered_df)


if __name__ == "__main__":
    analytics()
