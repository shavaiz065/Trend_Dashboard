import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set Streamlit layout to wide before anything else
st.set_page_config(layout="wide")

# File upload option in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    # Convert Date column to datetime format
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df = df.dropna(subset=["Date"])  # Drop invalid dates

    # Sidebar inputs
    selected_date = st.sidebar.date_input("Select a date", pd.to_datetime("today"))
    selected_employer = st.sidebar.selectbox("Select Employer", df["Employer"].unique())

    # Set title based on selected employer
    st.title(f"Data Trend ({selected_employer})")

    # Get the selected weekday
    selected_weekday = pd.to_datetime(selected_date).weekday()

    # Filter data for the selected date and the same weekday in previous weeks
    df_selected_date = df[(df["Employer"] == selected_employer) & (df["Date"] == pd.to_datetime(selected_date))]

    # Get all data for the selected employer and the same weekday from previous weeks
    df_trend = df[(df["Employer"] == selected_employer) & (df["Date"].dt.weekday == selected_weekday)].copy()

    # Combine the data for the selected date and previous same weekdays
    df_combined = pd.concat([df_trend, df_selected_date]).drop_duplicates().sort_values(by="Date")

    # Create subplots for 4 graphs (2 rows and 2 columns)
    fig, ax = plt.subplots(2, 2, figsize=(20, 12))  # 2 rows, 2 columns

    if df_combined.empty:
        st.warning("No matching trend data found.")
        for i in range(2):
            for j in range(2):
                ax[i, j].set_title("No Data Available")
    else:
        # First graph for Enrolled Hours
        ax[0, 0].plot(df_combined["Date"], df_combined["Enrolled Hours-Hourly"], marker='o', linestyle='-')
        ax[0, 0].set_xlabel("Date")
        ax[0, 0].set_ylabel("Enrolled Hours")
        ax[0, 0].set_title(f"Enrolled Hours Trend for {selected_employer}")
        ax[0, 0].grid(True)
        ax[0, 0].set_xticks(df_combined["Date"])
        ax[0, 0].set_xticklabels(df_combined["Date"].dt.strftime('%Y-%m-%d'), rotation=45)

        # Second graph for Hourly Enrolled Worked
        ax[0, 1].plot(df_combined["Date"], df_combined["HourlyEnrolledWorked"], marker='o', linestyle='-',
                      color='orange')
        ax[0, 1].set_xlabel("Date")
        ax[0, 1].set_ylabel("Hourly Enrolled Worked")
        ax[0, 1].set_title(f"Hourly Enrolled Worked Trend for {selected_employer}")
        ax[0, 1].grid(True)
        ax[0, 1].set_xticks(df_combined["Date"])
        ax[0, 1].set_xticklabels(df_combined["Date"].dt.strftime('%Y-%m-%d'), rotation=45)

        # Third graph for Total Hours (Enrolled + Unenrolled)
        if "Total Hours(Enrolled + Unenrolled)" in df_combined.columns:
            ax[1, 0].plot(df_combined["Date"], df_combined["Total Hours(Enrolled + Unenrolled)"], marker='o',
                          linestyle='-', color='green')
            ax[1, 0].set_xlabel("Date")
            ax[1, 0].set_ylabel("Total Hours (Enrolled + Unenrolled)")
            ax[1, 0].set_title(f"Total Hours (Enrolled + Unenrolled) Trend for {selected_employer}")
            ax[1, 0].grid(True)
            ax[1, 0].set_xticks(df_combined["Date"])
            ax[1, 0].set_xticklabels(df_combined["Date"].dt.strftime('%Y-%m-%d'), rotation=45)
        else:
            ax[1, 0].set_title("Total Hours (Enrolled + Unenrolled) Column Not Found")

        # Fourth graph for Employees in TA (assuming it's a column in the dataset)
        if "Employees in TA" in df_combined.columns:
            ax[1, 1].plot(df_combined["Date"], df_combined["Employees in TA"], marker='o', linestyle='-', color='red')
            ax[1, 1].set_xlabel("Date")
            ax[1, 1].set_ylabel("Employees in TA")
            ax[1, 1].set_title(f"Employees in TA Trend for {selected_employer}")
            ax[1, 1].grid(True)
            ax[1, 1].set_xticks(df_combined["Date"])
            ax[1, 1].set_xticklabels(df_combined["Date"].dt.strftime('%Y-%m-%d'), rotation=45)
        else:
            ax[1, 1].set_title("Employees in TA Column Not Found")

    # Display the plot
    st.pyplot(fig)

    # Show trend data for the selected date and same weekday data from previous weeks
    st.subheader(f"Trend Data for {selected_employer}")
    if df_combined.empty:
        st.warning("No trend data found for selected date and same weekdays.")
    else:
        st.write(df_combined)

else:
    st.info("Please upload a CSV file to begin.")
