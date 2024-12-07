import streamlit as st
import pandas as pd
from datetime import datetime

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

def format_data():
    # Load data
    file_path = 'data/workout - log.csv'
    df = pd.load_data(file_path)
    

    # Create a dictionary mapping muscles to exercises
    muscle_to_exercises = df.groupby('Muscle')['Exercise'].unique().to_dict()

    return muscle_to_exercises

    
def get_muscle():
    
    pass

def form2():
    st.title("📝 Log a Workout")
    
    # Input form
    with st.form("workout_form"):
        date = st.date_input("Date", value=datetime.now())
        exercise = st.selectbox("Exercise")
        muscle = st.s("Muscle Group", options=muscle_list, key="muscle_group")
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

    
    
def form():
    st.title("📝 Log a Workout")
    
    # Load data
    file_path = 'data/workout - log.csv'
    df = load_data(file_path)
    
    # Create dictionary mapping muscles to exercises
    muscle_to_exercises = df.groupby('Muscle')['Exercise'].unique().apply(list).to_dict()
    unique_muscles = df['Muscle'].unique().tolist()

    # Step 1: Select Muscle Group
    muscle_group = st.selectbox("Select Muscle Group", options=unique_muscles, key="muscle_group")

    # Step 2: Select Exercise
    exercises = muscle_to_exercises.get(muscle_group, [])
    exercise = st.selectbox("Select Exercise", options=exercises, key="exercise")
    
    # Step 3: Specify Number of Sets
    sets = st.number_input("Number of Sets", min_value=1, step=1, value=1, key="sets")

    # Step 4: Create a table for dynamic input of sets details
    set_data = []
    
    # edited_df = st.experimental_data_editor(set_data)

    # Create the table with placeholders for reps, weight, duration, and note for each set
    for i in range(sets):
        st.markdown(f"### Set {i+1} Details")
        cols = st.columns(5)

        reps = cols[0].number_input(f"Reps for Set {i+1}", min_value=1, step=1, key=f"reps_{i+1}")
        weight = cols[1].number_input(f"Weight for Set {i+1} (lbs/kg)", min_value=0.0, step=0.1, key=f"weight_{i+1}")
        duration = cols[2].number_input(f"Duration for Set {i+1} (minutes)", min_value=0, step=1, key=f"duration_{i+1}")
        note = cols[3].text_area(f"Notes for Set {i+1} (optional)", key=f"note_{i+1}")
        
        set_data.append({
            "Set": i+1, 
            "Reps": reps, 
            "Weight": weight, 
            "Duration": duration, 
            "Note": note
        })

    # Submit the data
    if st.button("Submit"):
        # Create a DataFrame for the new entry
        new_entry = pd.DataFrame({
            "Date": [datetime.now().strftime("%Y-%m-%d")] * sets,
            "Muscle": [muscle_group] * sets,
            "Exercise": [exercise] * sets,
            "Set": [data["Set"] for data in set_data],
            "Reps": [data["Reps"] for data in set_data],
            "Weight": [data["Weight"] for data in set_data],
            "Duration": [data["Duration"] for data in set_data],
            "Note": [data["Note"] for data in set_data]
        })

        # Save to CSV
        try:
            old_data = pd.read_csv("data/workouts.csv")
            df = pd.concat([old_data, new_entry], ignore_index=True)
        except FileNotFoundError:
            df = new_entry

        df.to_csv("data/workouts.csv", index=False)
        st.success("Workout logged successfully!")
        st.dataframe(new_entry)  # Show the logged workout data

if __name__ == "__main__":
    form()