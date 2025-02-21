import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Load Data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")  # Convert to datetime
    return df


st.title("Data Trend Analysis")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
if uploaded_file is not None:
    df = load_data(uploaded_file)

    employers = df["Employer"].unique()
    selected_employer = st.selectbox("Select Employer", employers)

    selected_date = st.date_input("Select Date")
    selected_date = pd.to_datetime(selected_date)
    selected_weekday = selected_date.weekday()

    df_trend = df.query("Employer == @selected_employer and Date.dt.weekday == @selected_weekday").sort_values("Date")

    # Ensure selected date is included
    df_selected = df[(df["Employer"] == selected_employer) & (df["Date"] == selected_date)]
    df_trend = pd.concat([df_trend, df_selected]).drop_duplicates().sort_values("Date")

    st.write("### Trend Data")
    st.dataframe(df_trend)

    # Plot Graph
    fig, ax = plt.subplots()
    ax.plot(df_trend["Date"], df_trend["Enrolled Hours"], marker="o", linestyle="-")
    ax.set_xlabel("Date")
    ax.set_ylabel("Enrolled Hours")
    ax.set_title(f"Trend for {selected_employer}")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
