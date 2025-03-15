import streamlit as st
import pandas as pd

def show_dashboard(df):
    st.title("🏋️ Your Workout History")

    if df.empty:
        st.warning("No workout data found. Add your first workout!")
    else:
        st.dataframe(df)


def show_dashboard2(conn):
    st.title("🏋️ Your Workout History")

    # fetch data from db
    df = pd.read_sql("SELECT * FROM workouts", conn)

    if df.empty:
        st.warning("No workout data found. Add your first workout!")
    else:
        st.dataframe(df)
