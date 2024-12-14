import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Workout App",
    page_icon="👋",
)


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
    

def plot_data(df):
    """
    Generate advanced visualizations using Plotly.
    """
    st.markdown("### Visualizations")
    
    # Exercise Frequency
    if not df.empty:
        st.subheader("Exercise Frequency")
        exercise_counts = df['Exercise'].value_counts().reset_index()
        exercise_counts.columns = ['Exercise', 'Count']
        fig = px.bar(exercise_counts, x='Count', y='Exercise', orientation='h',
                     title="Frequency of Exercises", color='Count', text='Count')
        st.plotly_chart(fig, use_container_width=True)
    
    # Weight Progression
    st.subheader("Weight Progression Over Time")
    if not df.empty:
        weight_trend = df.groupby('Date')['Weight'].sum().reset_index()
        fig = px.line(weight_trend, x='Date', y='Weight', title="Weight Progression Over Time",
                      markers=True, line_shape="spline")
        st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap of Workouts
    st.subheader("Workout Frequency Heatmap")
    df['Weekday'] = df['Date'].dt.day_name()
    df['Week'] = df['Date'].dt.strftime('%U')
    heatmap_data = df.groupby(['Weekday', 'Week']).size().unstack(fill_value=0)
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale="Viridis"
    ))
    fig.update_layout(title="Workout Frequency Heatmap", xaxis_title="Week", yaxis_title="Day of Week")
    st.plotly_chart(fig, use_container_width=True)



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
    

def homepage():
    
    """
    Main analytics function for the Streamlit app.
    """

    st.title("🏋️ Workout Dashboard - Home")
    st.sidebar.success("Select a page above.")
    
    # Load data
    file_path = 'data/workout - log.csv'
    df = load_data(file_path)

    if df is None:
        return

    # Display KPIs
    display_kpis(df)

    # Display workout data
    with st.expander("Data Preview"):
        st.dataframe(df.head())

    # Plot data
    plot_data(df)

if __name__ == "__main__":
    homepage()
