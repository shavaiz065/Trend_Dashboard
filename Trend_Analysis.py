import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Streamlit Page Configuration
st.set_page_config(
    layout="wide",
    page_title="Data Trend",
    page_icon="📊",
)

# Custom CSS for Styling
st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #00bcd4, #212121); }
        h2 { text-align: center; color: #00bcd4; font-family: 'Roboto', sans-serif; }
        .stButton button { background-color: #00bcd4; color: white; border-radius: 12px; padding: 10px 20px; }
        .stButton button:hover { background-color: #4caf50; }
    </style>
""", unsafe_allow_html=True)

# Sidebar File Uploader
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, parse_dates=["Date"])  # Auto-parse dates
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # Drop NaN dates
    df = df.dropna(subset=["Date"])

    # Sidebar Filters
    selected_date = st.sidebar.date_input("Select a Date", pd.to_datetime("today"))
    selected_employer = st.sidebar.selectbox("Select Employer", df["Employer"].unique())

    # Filter Data
    selected_weekday = pd.to_datetime(selected_date).weekday()
    df_trend = df[
        (df["Employer"] == selected_employer) &
        ((df["Date"].dt.weekday == selected_weekday) | (df["Date"] == pd.to_datetime(selected_date)))
    ].sort_values("Date")

    # Dashboard Header
    st.markdown(f"<h2>Data Trend for {selected_employer}</h2>", unsafe_allow_html=True)

    # Columns Layout
    col1, col2 = st.columns(2)

    # Function to Plot Graphs
    def plot_graph(ax, x, y, title, xlabel, ylabel, color):
        ax.plot(x, y, marker="o", linestyle="-", color=color)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.set_xticklabels(x.dt.strftime('%Y-%m-%d'), rotation=45)

    with col1:
        fig, ax = plt.subplots(figsize=(10, 5))
        if df_trend.empty or "Enrolled Hours-Hourly" not in df_trend.columns:
            st.warning("No matching trend data found.")
        else:
            plot_graph(ax, df_trend["Date"], df_trend["Enrolled Hours-Hourly"], "Enrolled Hours Trend", "Date", "Enrolled Hours", "#00bcd4")
            st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(10, 5))
        if df_trend.empty or "HourlyEnrolledWorked" not in df_trend.columns:
            st.warning("No data found for Hourly Enrolled Worked.")
        else:
            plot_graph(ax, df_trend["Date"], df_trend["HourlyEnrolledWorked"], "Hourly Enrolled Worked Trend", "Date", "Hourly Enrolled Worked", "red")
            st.pyplot(fig)

    # Additional Graphs
    col3, col4 = st.columns(2)
    with col3:
        fig, ax = plt.subplots(figsize=(10, 5))
        if df_trend.empty or "Total Hours(Enrolled + Unenrolled)" not in df_trend.columns:
            st.warning("No data found for Total Hours.")
        else:
            plot_graph(ax, df_trend["Date"], df_trend["Total Hours(Enrolled + Unenrolled)"], "Total Hours Trend", "Date", "Total Hours", "green")
            st.pyplot(fig)

    with col4:
        fig, ax = plt.subplots(figsize=(10, 5))
        if df_trend.empty or "Employees in TA" not in df_trend.columns:
            st.warning("No data found for Employees in TA.")
        else:
            plot_graph(ax, df_trend["Date"], df_trend["Employees in TA"], "Employees in TA Trend", "Date", "Employees in TA", "purple")
            st.pyplot(fig)

    # Display Table
    if df_trend.empty:
        st.warning("No trend data found.")
    else:
        st.dataframe(df_trend)

else:
    st.info("Please upload a CSV file to start.")

# Debugging Information
print("Running from:", os.getcwd())
