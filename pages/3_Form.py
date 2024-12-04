import streamlit as st
import pandas as pd
from datetime import datetime

def form():
    st.title("📝 Log a Workout")

    # Input form
    with st.form("workout_form"):
        date = st.date_input("Date", value=datetime.now())
        exercise = st.text_input("Exercise", placeholder="e.g., Bench Press")
        muscle = st.text_input("Muscle Group", placeholder="e.g., Chest")
        sets = st.number_input("Sets", min_value=0, step=1)
        reps = st.number_input("Reps", min_value=0, step=1)
        weight = st.number_input("Weight (lbs/kg)", min_value=0.0, step=0.1)
        duration = st.number_input("Duration (minutes)", min_value=0)
        note = st.text_area("Notes (optional)")

        submitted = st.form_submit_button("Submit")

        if submitted:
            # Save to CSV
            new_entry = pd.DataFrame({
                "Date": [date],
                "Exercise": [exercise],
                "Muscle": [muscle],
                "Sets": [sets],
                "Reps": [reps],
                "Weight": [weight],
                "Duration": [duration],
                "Note": [note]
            })

            try:
                old_data = pd.read_csv("data/workouts.csv")
                df = pd.concat([old_data, new_entry], ignore_index=True)
            except FileNotFoundError:
                df = new_entry

            df.to_csv("data/workouts.csv", index=False)
            st.success("Workout logged successfully!")

form()