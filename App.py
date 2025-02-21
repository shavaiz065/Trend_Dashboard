import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config with a modern layout and dark theme
st.set_page_config(
    layout="wide",  # Use the wide layout to maximize space
    page_title="Trend Dashboard",
    page_icon=":bar_chart:",  # Add an icon for your app
)

# Custom CSS for futuristic styling
st.markdown("""
    <style>
        /* Background color for the page */
        .main {
            background-color: #121212;
            color: white;
        }

        /* Sidebar styles */
        .sidebar .sidebar-content {
            background-color: #1e1e1e;
            color: white;
        }

        .css-1d391kg {
            background-color: #333;
        }

        /* Heading styles */
        h1, h2, h3 {
            font-family: 'Roboto', sans-serif;
            font-weight: bold;
            color: #00bcd4;  /* Futuristic blue color */
        }

        /* Add a gradient background to the page */
        .stApp {
            background: linear-gradient(135deg, #00bcd4, #212121);
        }

        /* Styling the button */
        .stButton button {
            background-color: #00bcd4;
            color: white;
            border-radius: 12px;
            border: 2px solid #00bcd4;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
        }

        .stButton button:hover {
            background-color: #4caf50;
            border: 2px solid #4caf50;
        }

        /* Style the table */
        .dataframe {
            border: 1px solid #00bcd4;
            border-radius: 10px;
            padding: 10px;
            background-color: #1e1e1e;
            color: white;
        }

        /* Styling for the plot grid and labels */
        .matplotlib-plot .plotly-graph-div {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar file uploader
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

# Check if file is uploaded
if uploaded_file is not None:
    # Read CSV file
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading the uploaded file: {e}")
        st.stop()

    # Convert Date column to datetime format
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df = df.dropna(subset=["Date"])  # Drop invalid dates

    # Sidebar inputs
    selected_date = st.sidebar.date_input("Select a date", pd.to_datetime("today"))
    selected_employer = st.sidebar.selectbox("Select Employer", df["Employer"].unique())

    # Filter data for selected date
    df_selected_date = df[(df["Employer"] == selected_employer) & (df["Date"] == pd.to_datetime(selected_date))]

    # Find previous same weekday data
    selected_weekday = pd.to_datetime(selected_date).weekday()
    df_trend = df[(df["Employer"] == selected_employer) & (df["Date"].dt.weekday == selected_weekday)].copy()

    # Sort data by date (oldest to newest)
    df_trend = df_trend.sort_values(by="Date")

    # Add a centered heading above the graphs
    st.markdown(f"<h2 style='text-align: center;'>Trend Data for {selected_employer}</h2>", unsafe_allow_html=True)

    # Create a two-row layout for the graphs (use full width of the page)
    col1, col2 = st.columns([2, 2])  # Adjust column width (2:2 ratio for side-by-side)

    with col1:
        fig, ax = plt.subplots(figsize=(12, 6))  # Adjust the size of the graph

        if df_trend.empty:
            st.warning("No matching trend data found.")
            ax.set_title("No Data Available")
        else:
            ax.plot(df_trend["Date"], df_trend["Enrolled Hours-Hourly"], marker='o', linestyle='-', color='#00bcd4')
            ax.set_xlabel("Date")
            ax.set_ylabel("Enrolled Hours")
            ax.set_title(f"Enrolled Hours Trend for {selected_employer}")
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.set_xticks(df_trend["Date"])
            ax.set_xticklabels(df_trend["Date"].dt.strftime('%Y-%m-%d'), rotation=45)

        st.pyplot(fig)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(12, 6))  # Adjust the size of the graph

        if df_trend.empty or "HourlyEnrolledWorked" not in df_trend.columns:
            st.warning("No matching trend data found for Hourly Enrolled Worked.")
            ax2.set_title("No Data Available")
        else:
            ax2.plot(df_trend["Date"], df_trend["HourlyEnrolledWorked"], marker='s', linestyle='-', color='red')
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Hourly Enrolled Worked")
            ax2.set_title(f"Hourly Enrolled Worked Trend for {selected_employer}")
            ax2.grid(True, linestyle='--', alpha=0.5)
            ax2.set_xticks(df_trend["Date"])
            ax2.set_xticklabels(df_trend["Date"].dt.strftime('%Y-%m-%d'), rotation=45)

        st.pyplot(fig2)

    # Create another row for the next two graphs (Total Hours and Employees in TA)
    col3, col4 = st.columns([2, 2])  # Adjust column width (2:2 ratio for side-by-side)

    with col3:
        fig3, ax3 = plt.subplots(figsize=(12, 6))  # Adjust the size of the graph

        if df_trend.empty or "Total Hours(Enrolled + Unenrolled)" not in df_trend.columns:
            st.warning("No matching trend data found for Total Hours (Enrolled + Unenrolled).")
            ax3.set_title("No Data Available")
        else:
            ax3.plot(df_trend["Date"], df_trend["Total Hours(Enrolled + Unenrolled)"], marker='d', linestyle='-',
                     color='#00bcd4')
            ax3.set_xlabel("Date")
            ax3.set_ylabel("Total Hours (Enrolled + Unenrolled)")
            ax3.set_title(f"Total Hours (Enrolled + Unenrolled) Trend for {selected_employer}")
            ax3.grid(True, linestyle='--', alpha=0.5)
            ax3.set_xticks(df_trend["Date"])
            ax3.set_xticklabels(df_trend["Date"].dt.strftime('%Y-%m-%d'), rotation=45)

        st.pyplot(fig3)

    with col4:
        fig4, ax4 = plt.subplots(figsize=(12, 6))  # Adjust the size of the graph

        if df_trend.empty or "Employees in TA" not in df_trend.columns:
            st.warning("No matching trend data found for Employees in TA.")
            ax4.set_title("No Data Available")
        else:
            ax4.plot(df_trend["Date"], df_trend["Employees in TA"], marker='x', linestyle='-', color='blue')
            ax4.set_xlabel("Date")
            ax4.set_ylabel("Employees in TA")
            ax4.set_title(f"Employees in TA Trend for {selected_employer}")
            ax4.grid(True, linestyle='--', alpha=0.5)
            ax4.set_xticks(df_trend["Date"])
            ax4.set_xticklabels(df_trend["Date"].dt.strftime('%Y-%m-%d'), rotation=45)

        st.pyplot(fig4)

    # Show previous trend data in table (All Columns)
    if df_trend.empty:
        st.warning("No trend data found for previous same weekdays.")
    else:
        st.write(df_trend)  # ✅ Saare columns show karega

else:
    st.info("Please upload a CSV file to start.")
