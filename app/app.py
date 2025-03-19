import streamlit as st
import pandas as pd
import db
import dashboard
import form
import analysis
import homepage

st.sidebar.title("Workout Dashboard")
menu = st.sidebar.radio("Menu", ["Homepage", "Add Workout", "Analysis"])

# Connect to DB
#conn = db.get_db_connection()
FILE_PATH = '../data/workout - log.csv'

def load_data():
    """Load workout data from the CSV file."""
    try:
        df = pd.read_csv(FILE_PATH)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Total_volume"] = df["Reps"] * df["Weight"]
        return df
    except FileNotFoundError:
        st.error(f"File not found at {FILE_PATH}")
        return None

df = load_data()

# menu 
if menu == "Homepage":
    homepage.homepage(df)
elif menu == "Add Workout":
    form.display_form(df)
elif menu == "Analysis":
    analysis.analytics(df)

#conn.close()
