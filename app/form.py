import streamlit as st
import pandas as pd
from datetime import datetime


def display_form(df):
    st.title("📝 Log a Workout")

    # Load data


    # Create dictionary mapping muscles to exercises
    muscle_to_exercises = df.groupby('Muscle')['Exercise'].unique().apply(list).to_dict()
    unique_muscles = df['Muscle'].unique().tolist()

    # Select Muscle Group
    muscle_group = st.selectbox("Select Muscle Group", options=unique_muscles, key="muscle_group")

    # Select Exercise
    exercises = muscle_to_exercises.get(muscle_group, [])
    exercise = st.selectbox("Select Exercise", options=exercises, key="exercise")

    # Specify Number of Sets
    sets = st.number_input("Number of Sets", min_value=1, step=1, value=1, key="sets")

    set_data = []

    st.markdown("### Enter Set Details:")

    # Dynamically generate input fields for each set
    for i in range(sets):
        st.markdown(f"#### Set {i+1}")
        cols = st.columns(4)
        reps = cols[0].number_input(f"Reps (Set {i+1})", min_value=0, step=1, key=f"reps_{i}")
        weight = cols[1].number_input(f"Weight (lbs) (Set {i+1})", min_value=0, step=1, key=f"weight_{i}")
        duration = cols[2].number_input(f"Duration (seconds) (Set {i+1})", min_value=0, step=1, key=f"duration_{i}")
        note = cols[3].text_input(f"Note (Set {i+1})", key=f"note_{i}")
        set_data.append({"Set": i+1, "Reps": reps, "Weight": weight, "Duration": duration, "Note": note})

    # Submit the data
    if st.button("Submit"):
        # Convert set data into a DataFrame
        new_entry = pd.DataFrame(set_data)
        new_entry["Date"] = datetime.now().strftime("%Y-%m-%d")
        new_entry["Muscle"] = muscle_group
        new_entry["Exercise"] = exercise

        # Save to CSV
        try:
            old_data = pd.read_csv("data/workouts.csv")
            df = pd.concat([old_data, new_entry], ignore_index=True)
        except FileNotFoundError:
            df = new_entry

        df.to_csv("data/workouts.csv", index=False)
        st.success("Workout logged successfully!")
        st.dataframe(new_entry)  # Show the logged workout data
        
