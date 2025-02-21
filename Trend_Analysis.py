import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Streamlit Page Configuration
st.set_page_config(layout="wide", page_title="Data Trend", page_icon="📊")

# Custom CSS for Styling
st.markdown(
    """
    <style>
        .stApp { background: linear-gradient(135deg, #00bcd4, #212121); }
        h2 { text-align: center; color: #00bcd4; font-family: 'Roboto', sans-serif; }
        .stButton button { background-color: #00bcd4; color: white; border-radius: 12px; padding: 10px 20px; }
        .stButton button:hover { background-color: #4caf50; }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar File Uploader
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Ensure necessary columns exist
        required_columns = {"Employer", "Date"}
        if not required_columns.issubset(df.columns):
            st.error(f"Uploaded file must contain columns: {', '.join(required_columns)}")
            st.stop()

        # Convert "Date" column to datetime
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])  # Remove rows where Date is NaT

        # Add Weekday column
        df["Weekday"] = df["Date"].dt.weekday

    except Exception as e:
        st.error(f"Error processing file: {e}")
        st.stop()

    # Sidebar Filters
    selected_date = st.sidebar.date_input("Select a Date", pd.to_datetime("today"))
    selected_employer = st.sidebar.selectbox("Select Employer", df["Employer"].unique())

    # Filter Data
    selected_weekday = pd.to_datetime(selected_date).weekday()
    df_trend = df[(df["Employer"] == selected_employer) & (df["Weekday"] == selected_weekday)].sort_values("Date")

    # Dashboard Header
    st.markdown("<h2>Data Trend</h2>", unsafe_allow_html=True)

    # Layout Columns
    col1, col2 = st.columns(2)

    # Function to Plot Graphs
    def plot_graph(ax, x, y, title, xlabel, ylabel, color):
        ax.plot(x, y, marker="o", linestyle="-", color=color)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.set_xticks(range(len(x)))
        ax.set_xticklabels(x.dt.strftime('%Y-%m-%d'), rotation=45)


    with col1:
        if "Enrolled Hours-Hourly" in df_trend.columns:
            fig, ax = plt.subplots(figsize=(10, 5))
            plot_graph(ax, df_trend["Date"], df_trend["Enrolled Hours-Hourly"],
                       "Enrolled Hours Trend", "Date", "Enrolled Hours", "#00bcd4")
            st.pyplot(fig)
        else:
            st.warning("No data available for 'Enrolled Hours-Hourly'.")

    with col2:
        if "HourlyEnrolledWorked" in df_trend.columns:
            fig, ax = plt.subplots(figsize=(10, 5))
            plot_graph(ax, df_trend["Date"], df_trend["HourlyEnrolledWorked"],
                       "Hourly Enrolled Worked Trend", "Date", "Hourly Enrolled Worked", "red")
            st.pyplot(fig)
        else:
            st.warning("No data available for 'Hourly Enrolled Worked'.")

    # Display Table
    if df_trend.empty:
        st.warning("No trend data found.")
    else:
        st.dataframe(df_trend)

else:
    st.info("Please upload a CSV file to start.")

# Debugging Information
st.sidebar.text(f"Running from: {os.getcwd()}")
