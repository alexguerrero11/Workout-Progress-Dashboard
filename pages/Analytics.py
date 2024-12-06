import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


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
    Display key performance indicators.
    """
    
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
    weekly_count = len(df.query(" Date >= @start_of_week & Date <= @end_of_Week")['Date'].unique())
    monthly_count = len(df.query(" Date >= @first_day_of_month & Date < @next_month_first_day")['Date'].unique())
    total_records = len(df['Date'].unique())

    st.markdown("### Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("Workouts This Week", weekly_count)
    col2.metric("Workouts This Month", monthly_count)
    col3.metric("Total Workout Days", total_records)


def filter_data(df):
    """
    Add sidebar filters and return filtered data.
    """
    st.sidebar.header("Filters")
    # Filter by year
    unique_years = list(sorted(df['Date'].dt.year.unique()))
    selected_year = st.sidebar.selectbox("Select Year", unique_years,index=unique_years.index(2024))

    # Filter by muscle group
    unique_muscles = list(df['Muscle'].unique())
    selected_muscle = st.sidebar.selectbox("Select Muscle Group", unique_muscles)

    # Filter by exercises
    filtered_df = df[(df['Date'].dt.year == selected_year) & (df['Muscle'] == selected_muscle)]
    
    selected_exercises = st.sidebar.multiselect("Select Exercises", filtered_df['Exercise'].unique(),
                                                default=filtered_df['Exercise'].unique())
    
    return filtered_df[filtered_df['Exercise'].isin(selected_exercises)]


def plot_data(df):
    """
    Generate visualizations.
    """
    st.markdown("### Visualizations")

    # Exercise Frequency
    st.subheader("Exercise Frequency")
    fig, ax = plt.subplots()
    sns.countplot(data=df, y="Exercise", order=df['Exercise'].value_counts().index, ax=ax)
    ax.set_title("Frequency of Exercises")
    st.pyplot(fig)

    # Weight Progression
    st.subheader("Weight Progression Over Time")
    if not df.empty:
        weight_trend = df.groupby('Date')['Weight'].mean()
        st.bar_chart(weight_trend)

    # Total Volume by Exercise
    st.subheader("Total Volume by Exercise")
    if 'Total_volume' in df.columns:
        volume_by_exercise = df.groupby('Exercise')['Total_volume'].sum().sort_values()
        st.bar_chart(volume_by_exercise)


def analytics():
    """
    Main analytics function for the Streamlit app.
    """
    st.title("📊 Workout Analytics")

    # Load data
    file_path = 'data/workout - log.csv'
    df = load_data(file_path)

    if df is None:
        return

    # Display KPIs
    display_kpis(df)

    # Filter data
    filtered_data = filter_data(df)

    # Display filtered data
    st.markdown("### Filtered Workout Data")
    st.dataframe(filtered_data)

    # Plot data
    plot_data(filtered_data)


if __name__ == "__main__":
    analytics()
