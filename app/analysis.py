import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from datetime import date
from dateutil.relativedelta import relativedelta
import plotly.express as px
import plotly.graph_objects as go

def show_analysis_2(conn):
    st.title("📊 Workout Trends")

    df = pd.read_sql("SELECT * FROM workouts", conn)

    if df.empty:
        st.warning("No data available for analysis.")
        return

    st.write("### Workout Frequency")
    st.bar_chart(df["exercise"].value_counts())

    st.write("### Weight Progress Over Time")
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=df["date"], y=df["weight"], hue=df["exercise"])
    plt.xticks(rotation=45)
    st.pyplot(plt)

def show_analysis(df):
    st.title("📊 Workout Trends")
    
    if df.empty:
        st.warning("No data available for analysis.")
        return

    st.write("### Workout Frequency")
    st.bar_chart(df["Exercise"].value_counts())

    st.write("### Weight Progress Over Time")
    
    # plt.figure(figsize=(10, 5))
    # sns.lineplot(x=df["Date"], y=df["Weight"], hue=df["Exercise"])
    # plt.xticks(rotation=45)
    # st.pyplot(plt)
    
