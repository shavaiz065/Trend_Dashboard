import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from PIL import Image
import os

# Set page config with a modern layout
st.set_page_config(
    layout="wide",
    page_title="Trend Dashboard",
    page_icon=":bar_chart:",
)

# Custom CSS for styling
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #00bcd4, #212121);
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar file uploader
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

# Show welcome screen only when no file is uploaded
if uploaded_file is None:
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px;">
            <h1 style="color: #3498db;">📊 Welcome to the DMAT-Trend Analysis Dashboard! 📊</h1>
            <p style="font-size: 18px; color: #2c3e50;">
                Upload a CSV file from the sidebar to get started.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Get absolute path to logo file
    logo_path = os.path.join("assets", "logo.png")

    # Check if logo file exists
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)  # Open the image
        col1, col2, col3 = st.columns([1, 2, 1])  # Create columns to center the image
        with col2:
            st.image(logo, use_container_width=True)  # Center logo with full width
    else:
        st.error(f"⚠️ Logo not found at: {logo_path}. Please check the file path.")

# Now process the file if uploaded
if uploaded_file:
    # Your existing logic to process the file goes here
    pass

# Check if file is uploaded
if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)

        # Check if the uploaded file has the specified headers
        required_headers = [
            "businessSystemID", "employerName", "date", "enrolledHoursSum",
            "unEnrolledHoursSum", "enrolledSalariedSum", "unEnrolledSalariedSum",
            "enrolledUserCount", "unEnrolledUserCount", "totalHours",
            "employeesInTA", "lastTAFileProcessedDate", "receivingTime"
        ]

        # Check if the uploaded file contains all the required headers
        if all(header in df.columns for header in required_headers):
            # Create a mapping of original headers to expected dashboard headers
            column_mapping = {
                "businessSystemID": "BranchID",
                "employerName": "Employer",
                "date": "Date",
                "enrolledHoursSum": "Enrolled Hours-Hourly",
                "enrolledUserCount": "HourlyEnrolledWorked",
                "totalHours": "Total Hours(Enrolled + Unenrolled)",
                "employeesInTA": "Employees in TA"
            }

            # Rename columns according to the mapping
            df = df.rename(columns=column_mapping)

            # Removed the success message

        else:
            # If not all required headers are present, check if the expected dashboard headers already exist
            expected_headers = ["Employer", "Date", "Enrolled Hours-Hourly", "HourlyEnrolledWorked",
                                "Total Hours(Enrolled + Unenrolled)", "Employees in TA"]

            if not all(header in df.columns for header in expected_headers):
                st.warning(
                    "The uploaded file doesn't have the expected column structure. Please ensure it has the correct headers.")
                st.info(
                    "Expected headers: businessSystemID, employerName, date, enrolledHoursSum, enrolledUserCount, totalHours, employeesInTA, etc.")
    except Exception as e:
        st.error(f"Error reading the uploaded file: {e}")
        st.stop()

    # Convert date column to datetime
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df = df.dropna(subset=["Date"])

    # Sidebar date and employer selection
    selected_date = st.sidebar.date_input("Select a date", datetime.datetime.now())

    # Ensure there are employers to select from
    if "Employer" in df.columns and not df["Employer"].empty:
        selected_employer = st.sidebar.selectbox("Select Employer", df["Employer"].unique())
    else:
        st.error("No employer data found in the file")
        st.stop()

    # Add option for y-axis scaling
    y_axis_option = st.sidebar.radio(
        "Y-Axis Scaling",
        ["Auto", "Fixed Range", "Start from Zero"],
        index=0,
        help="Auto: Intelligently scale based on data variance. Fixed Range: Use a consistent range for better comparison. Start from Zero: Show full scale from zero."
    )

    # Filter data based on selection
    df_selected_date = df[(df["Employer"] == selected_employer) & (df["Date"] == pd.to_datetime(selected_date))]
    selected_weekday = pd.to_datetime(selected_date).weekday()
    df_trend = df[(df["Employer"] == selected_employer) & (df["Date"].dt.weekday == selected_weekday)].copy()
    df_trend = df_trend.sort_values(by="Date")

    # Create a dataframe for the last 7 days data
    end_date = pd.to_datetime(selected_date)
    start_date = end_date - pd.Timedelta(days=6)
    df_last_7_days = df[(df["Employer"] == selected_employer) &
                        (df["Date"] >= start_date) &
                        (df["Date"] <= end_date)].copy()
    df_last_7_days = df_last_7_days.sort_values(by="Date")


    # Summary Metrics Calculation
    def calculate_summary(metric):
        if metric not in df_trend.columns:
            return 0, 0, 0

        avg = df_trend[metric].mean() if not df_trend.empty else 0

        reflected = df_selected_date[metric].values[
            0] if metric in df_selected_date.columns and not df_selected_date.empty and len(
            df_selected_date[metric].values) > 0 else 0
        difference = ((reflected - avg) / avg * 100) if avg != 0 else 0
        return avg, reflected, difference


    # Calculate metrics only if they exist in the dataframe
    metrics_to_calculate = [
        ("Enrolled Hours-Hourly", "Enrolled Hours"),
        ("HourlyEnrolledWorked", "Hourly Enrolled Worked"),
        ("Total Hours(Enrolled + Unenrolled)", "Total Hours (Enrolled + Unenrolled)"),
        ("Employees in TA", "Employees in TA")
    ]

    metrics_results = {}
    for column_name, display_name in metrics_to_calculate:
        if column_name in df.columns:
            avg, reflected, difference = calculate_summary(column_name)
            metrics_results[display_name] = (avg, reflected, difference)

    # Summary Section
    st.sidebar.markdown("<h2 style='text-align: center;'>📊 Summary Overview</h2>", unsafe_allow_html=True)

    with st.sidebar:
        def display_summary(title, avg, reflected, difference):
            color = "red" if difference < 0 else "green"
            diff_icon = "🔻" if difference < 0 else "▲"
            formatted_diff = f"<span style='color:{color}; font-weight:bold;'>{diff_icon} {difference:.2f}%</span>"

            return f"""
            <div style="padding: 12px; border-radius: 8px; background-color: #f8f9fa; margin-bottom: 8px;">
                <h5 style="margin: 0; color: #333;">{title}</h5>
                <p style="margin: 4px 0;"><b>Average:</b> {avg:.2f}</p>
                <p style="margin: 4px 0;"><b>Reflected on ({selected_date}):</b> {reflected:.2f}</p>
                <p style="margin: 4px 0;"><b>Difference:</b> {formatted_diff}</p>
            </div>
            """


        # Display summary for each metric
        for title, (avg, reflected, difference) in metrics_results.items():
            st.markdown(display_summary(title, avg, reflected, difference), unsafe_allow_html=True)

    import streamlit as st

    # Create a centered title with better styling
    st.markdown("""
        <h2 style='text-align: center; color: #2C3E50; font-weight: bold;'>
            📊 Summary Overview
        </h2>
    """, unsafe_allow_html=True)

    # Create 4 columns for displaying summary boxes
    cols = st.columns(4)


    def display_summary(col, title, avg, reflected, difference):
        """
        Function to display a visually enhanced summary box.
        """
        # Define colors and icons based on the difference value
        if difference < 0:
            bg_color = "#FFE6E6"  # Light Red Background
            text_color = "#E74C3C"  # Red Text
            icon = "🔻"
        else:
            bg_color = "#E6F9E6"  # Light Green Background
            text_color = "#27AE60"  # Green Text
            icon = "▲"

        # Format difference with a visually appealing design
        formatted_diff = f"""
            <span style='color:{text_color}; font-size: 20px; font-weight: bold;'>
                {icon} {difference:.2f}%
            </span>
        """

        # Enhanced card-style summary box
        summary_html = f"""
            <div style="
                padding: 18px; 
                border-radius: 12px; 
                background: {bg_color}; 
                text-align: center; 
                box-shadow: 2px 4px 12px rgba(0,0,0,0.1);
                font-family: 'Arial', sans-serif;
                transition: transform 0.2s;
            " onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
                <h4 style="margin: 5px 0; color: #34495E; font-weight: bold;">{title}</h4>
                <p style="margin: 6px 0; font-size: 16px;"><b>Avg:</b> {avg:.2f}</p>
                <p style="margin: 6px 0; font-size: 16px;"><b>Reflected:</b> {reflected:.2f}</p>
                <p style="margin: 8px 0; font-size: 18px;">{formatted_diff}</p>
            </div>
        """

        col.markdown(summary_html, unsafe_allow_html=True)


    # Display summaries dynamically across columns
    for i, (title, (avg, reflected, difference)) in enumerate(metrics_results.items()):
        display_summary(cols[i % len(cols)], title, avg, reflected, difference)

    # Graphs Section
    st.markdown(f"<h2 style='text-align: center;'>Trend Data for {selected_employer}</h2>", unsafe_allow_html=True)


    def plot_trend(ax, x, y, title, xlabel, ylabel, color, marker):
        # Modern color scheme
        background_color = '#f9f9f9'
        grid_color = '#dddddd'
        title_color = '#2c3e50'

        # Set background color
        ax.set_facecolor(background_color)
        fig = ax.figure
        fig.patch.set_facecolor(background_color)

        # Plot the main line with improved styling
        ax.plot(x, y, marker=marker, linestyle='-', color=color, linewidth=2.5,
                markersize=8, markeredgewidth=1.5, markeredgecolor='white', label="Data")

        # Add gradient fill under the curve
        ax.fill_between(x, y, y.min(), color=color, alpha=0.2)

        # Improved axis labels and title with modern fonts
        ax.set_xlabel(xlabel, fontsize=11, fontweight='bold', color='#555555')
        ax.set_ylabel(ylabel, fontsize=11, fontweight='bold', color='#555555')
        ax.set_title(title, fontsize=14, fontweight='bold', color=title_color, pad=15)

        # Refined grid styling
        ax.grid(True, linestyle='--', alpha=0.7, color=grid_color)

        # Set x-ticks with better formatting and spacing
        ax.set_xticks(x)
        ax.set_xticklabels(x.dt.strftime('%Y-%m-%d'), rotation=45, ha='right', fontsize=9)

        # Customize tick parameters for a cleaner look
        ax.tick_params(axis='both', colors='#555555')

        # Clean up spines
        for spine in ax.spines.values():
            spine.set_color('#bbbbbb')
            spine.set_linewidth(0.8)

        # Adding data labels with enhanced styling
        for i, txt in enumerate(y):
            ax.text(x.iloc[i], y.iloc[i] + (y.max() - y.min()) * 0.02,
                    f"{txt:.1f}", fontsize=9, ha='center',
                    va='bottom', color='#333333',
                    bbox=dict(boxstyle="round,pad=0.2", fc='white', ec=color, alpha=0.7, linewidth=1))

        # Add trend line with improved styling if there are multiple data points
        if len(x) > 1:
            z = np.polyfit(x.index, y, 1)
            p = np.poly1d(z)
            ax.plot(x, p(x.index), "--", color="#ff7043", linewidth=2, alpha=0.8, label="Trend Line")

        ax.legend(frameon=False, fontsize=10)

        # Set y-axis based on selected option with improved padding
        if y_axis_option == "Start from Zero":
            ax.set_ylim(bottom=0, top=y.max() * 1.15)
        elif y_axis_option == "Auto":
            if len(y) >= 2:
                percent_change = abs((y.iloc[-1] - y.iloc[0]) / y.iloc[0] * 100) if y.iloc[0] != 0 else 0

                if percent_change < 10:
                    data_min = y.min() * 0.98  # Slightly improved padding
                    data_max = y.max() * 1.02
                    ax.set_ylim(bottom=data_min, top=data_max)
                else:
                    data_min = y.min() * 0.93
                    data_max = y.max() * 1.07
                    ax.set_ylim(bottom=data_min, top=data_max)
        elif y_axis_option == "Fixed Range":
            if not df.empty and y.name in df.columns:
                global_min = df[df["Employer"] == selected_employer][y.name].min() * 0.93
                global_max = df[df["Employer"] == selected_employer][y.name].max() * 1.07
                ax.set_ylim(bottom=global_min, top=global_max)

        # Calculate percentage change with enhanced display
        if len(y) >= 2 and y.iloc[0] != 0:
            percent_change = (y.iloc[-1] - y.iloc[0]) / y.iloc[0] * 100
            change_color = "#e74c3c" if percent_change < 0 else "#2ecc71"
            change_icon = "▼ " if percent_change < 0 else "▲ "

            # Add percentage change annotation with improved styling
            ax.annotate(f"{change_icon}{abs(percent_change):.1f}% change",
                        xy=(0.98, 0.05),
                        xycoords='axes fraction',
                        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=change_color, alpha=0.9, linewidth=1.5),
                        ha='right',
                        fontsize=10,
                        fontweight='bold',
                        color=change_color)

        # Add a subtle shadow effect to the chart
        ax.patch.set_alpha(0.7)

        # Enhanced legend styling
        legend = ax.legend(frameon=True, fancybox=True, framealpha=0.9,
                           fontsize=10, loc='upper right',
                           edgecolor='#cccccc')
        legend.get_frame().set_facecolor('white')

        # Adjust layout for better spacing
        fig.tight_layout()


    # Create a 2x2 grid of charts only for metrics that exist in the dataframe
    chart_metrics = [
        ("Enrolled Hours-Hourly", "Enrolled Hours Trend", "#00bcd4", 'o'),
        ("HourlyEnrolledWorked", "Hourly Enrolled Worked Trend", "red", 's'),
        ("Total Hours(Enrolled + Unenrolled)", "Total Hours Trend", "#0096FF", 'd'),
        ("Employees in TA", "Employees in TA Trend", "blue", 'x')
    ]

    # Filter metrics that exist in the dataframe
    available_charts = [m for m in chart_metrics if m[0] in df.columns]

    # Create three-column layout for better organization of charts
    col1, col2 = st.columns([2, 2])

    # Position to place charts
    positions = [col1, col2, col1, col2]

    for i, (metric, title, color, marker) in enumerate(available_charts):
        position = positions[i % len(positions)]

        with position:
            fig, ax = plt.subplots(figsize=(12, 6))
            if not df_trend.empty and metric in df_trend.columns:
                plot_trend(
                    ax,
                    df_trend["Date"],
                    df_trend[metric],
                    f"{title} for {selected_employer}",
                    "Date",
                    metric.replace("_", " "),
                    color,
                    marker
                )
            else:
                ax.text(0.5, 0.5, f"No data available for {metric}",
                        horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

            st.pyplot(fig)

    # Add the fifth graph - Total Hours for Last 7 Days
    st.markdown(f"<h2 style='text-align: center;'>Last 7 Days View for {selected_employer}</h2>",
                unsafe_allow_html=True)

    col1, col2 = st.columns([2, 2])

    with col1:
        if "Total Hours(Enrolled + Unenrolled)" in df.columns and not df_last_7_days.empty:
            fig, ax = plt.subplots(figsize=(12, 6))
            plot_trend(
                ax,
                df_last_7_days["Date"],
                df_last_7_days["Total Hours(Enrolled + Unenrolled)"],
                f"Total Hours (Last 7 Days) for {selected_employer}",
                "Date",
                "Total Hours",
                "#9C27B0",  # Purple color to differentiate from other charts
                '^'  # Triangle marker for distinction
            )
            st.pyplot(fig)
        else:
            st.warning("No data available for the last 7 days view.")

    if df_trend.empty:
        st.warning("No trend data found for previous same weekdays.")
    else:
        st.write(df_trend)

else:
    st.info("Please upload a CSV file to start.")