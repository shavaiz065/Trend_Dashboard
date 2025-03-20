import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'DejaVu Sans'  # Use a font available by default
import numpy as np
import datetime
from PIL import Image
import os
import matplotlib as mpl
import streamlit_analytics

# Start tracking analytics right after imports
streamlit_analytics.start_tracking()

# Set page config with a modern layout
st.set_page_config(
    layout="wide",
    page_title="Premium Trend Dashboard",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Enhanced custom CSS for a premium look
st.markdown("""
    <style>
        /* Main app styling */
        .stApp {
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            color: #e7e7e7;
        }

        /* Sidebar styling */
        .css-1d391kg, .css-1lcbmhc {
            background: linear-gradient(to bottom, #1a1a2e, #16213e);
        }

        /* Enhance card styling */
        div.stButton > button {
            background-color: #0f3460;
            color: white;
            border-radius: 8px;
            border: 1px solid #e94560;
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #e94560;
            border: 1px solid #0f3460;
            transform: scale(1.05);
        }

        /* Headers styling */
        # Replace the existing header styling in the CSS section with:

/* Headers styling */
h1, h2, h3 {
    color: #e94560 !important;
    font-family: 'DejaVu Sans', sans-serif;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
    text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.3) !important;
    margin-bottom: 20px !important;
}

h1 {
    font-size: 36px !important;
}

h2 {
    font-size: 30px !important;
    background: -webkit-linear-gradient(#e94560, #ff6b6b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h3 {
    font-size: 24px !important;
}

/* Add this for section headers */
.section-header {
    padding: 12px 20px;
    background: linear-gradient(90deg, #0f3460, #e94560);
    border-radius: 8px;
    margin: 30px 0 20px 0;
    color: white !important;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    -webkit-text-fill-color: white !important;
}

        /* Premium Card Styling */
.stAlert {
    background: linear-gradient(135deg, rgba(15, 52, 96, 0.9), rgba(233, 69, 96, 0.85));
    border-radius: 12px;
    border: 2px solid #e94560;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
    padding: 15px;
    color: white;
    font-size: 16px;
    font-weight: bold;
    text-align: center;
}


        /* Make dataframes more premium */
        .dataframe {
            border-radius: 10px !important;
            overflow: hidden !important;
            border: none !important;
        }
        .dataframe th {
            background-color: #0f3460 !important;
            color: white !important;
            text-align: center !important;
            font-weight: 600 !important;
        }
        .dataframe td {
            text-align: center !important;
            background-color: rgba(15, 52, 96, 0.5) !important;
            color: #e7e7e7 !important;
        }

        /* File uploader styling */
        .stFileUploader {
            padding: 10px;
            border-radius: 10px;
            background-color: rgba(15, 52, 96, 0.7);
            border: 1px solid #e94560;
        }

        /* Enhanced widgets */
        .stSelectbox, .stDateInput {
            background-color: rgba(15, 52, 96, 0.7);
            border-radius: 8px;
            padding: 5px;
            border: 1px solid #e94560;
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(15, 52, 96, 0.7);
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            border: 1px solid #e94560;
        }
        .stTabs [aria-selected="true"] {
            background-color: #e94560;
            color: white;
            font-weight: bold;
        }

        /* Animated elements */
        @keyframes glowing {
            0% { box-shadow: 0 0 5px #0f3460; }
            50% { box-shadow: 0 0 20px #e94560; }
            100% { box-shadow: 0 0 5px #0f3460; }
        }
        .premium-card {
            animation: glowing 3s infinite;
        }
    </style>
""", unsafe_allow_html=True)

# Add a password check in the sidebar for analytics access
with st.sidebar.expander("📊 Admin Analytics", expanded=False):
    analytics_password = st.text_input("Enter admin password to view analytics", type="password")
    show_analytics = st.checkbox("Show analytics dashboard", value=False)

    if analytics_password == "dmat-dashboard" and show_analytics:
        st.session_state.show_analytics = True
    else:
        st.session_state.show_analytics = False

# Configure matplotlib for a premium look
plt.style.use('dark_background')
mpl.rcParams['axes.facecolor'] = '#16213e'
mpl.rcParams['figure.facecolor'] = '#16213e'
mpl.rcParams['text.color'] = '#e7e7e7'
mpl.rcParams['axes.labelcolor'] = '#e7e7e7'
mpl.rcParams['xtick.color'] = '#e7e7e7'
mpl.rcParams['ytick.color'] = '#e7e7e7'
mpl.rcParams['grid.color'] = '#1a1a2e'
mpl.rcParams['axes.grid'] = True
mpl.rcParams['grid.alpha'] = 0.3
mpl.rcParams['axes.edgecolor'] = '#e94560'
mpl.rcParams['font.family'] = 'DejaVu Sans'
mpl.rcParams['font.weight'] = 'medium'

# Add a premium logo to the sidebar
st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 20px; padding: 10px; background: linear-gradient(90deg, #0f3460, #e94560); border-radius: 10px;">
        <h1 style="color: white; margin: 0; font-size: 24px;">DMAT<span style="color: #e94560">-</span>TREND</h1>
        <p style="color: white; margin: 0; font-size: 14px;">Premium Analytics Dashboard</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar file uploader with premium styling
st.sidebar.markdown("""
    <div style="padding: 10px; border-radius: 10px; background-color: rgba(15, 52, 96, 0.7); border: 1px solid #e94560; margin-bottom: 20px;">
        <h3 style="color: #e94560; margin-top: 0;">📊 Data Import</h3>
        <p style="color: #e7e7e7; margin-bottom: 10px;">Upload your CSV file to begin analysis</p>
    </div>
""", unsafe_allow_html=True)

# Show analytics dashboard if password is correct
if st.session_state.get('show_analytics', False):
    st.markdown("""
        <div style="
            background: linear-gradient(90deg, #0f3460, #e94560);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            text-align: center;
        ">
            <h2 style="color: white; margin: 0; font-size: 28px; font-weight: bold;">DMAT-Trend Visitor Analytics</h2>
        </div>
    """, unsafe_allow_html=True)

    # Show the analytics dashboard
    streamlit_analytics.stop_tracking(
        unsafe_password=None,  # No password needed as we've already authenticated
        hide_from_viewers=False,  # Show directly on the page
        dark_mode=True
    )

    # Stop execution to only show analytics
    st.stop()

uploaded_file = st.sidebar.file_uploader("", type=["csv"])

# Rest of your app code remains unchanged
# Show premium welcome screen only when no file is uploaded
if uploaded_file is None:
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px; padding: 40px; background: rgba(15, 52, 96, 0.7); border-radius: 20px; border: 2px solid #e94560;" class="premium-card">
            <h1 style="color: #e94560; font-size: 36px; margin-bottom: 20px;">📊 Welcome to DMAT-Trend Analytics Dashboard</h1>
            <p style="font-size: 20px; color: #e7e7e7; margin-bottom: 30px;">
                Upload a CSV file from the sidebar to generate comprehensive trend insights and visualizations.
            </p>
            <div style="width: 100px; height: 100px; background: linear-gradient(45deg, #0f3460, #e94560); margin: 0 auto; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 40px;">📈</span>
            </div>
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
        st.warning("Logo file not found. Using default styling.")

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

            # Add a subtle success message
            st.sidebar.markdown("""
                <div style="padding: 10px; border-radius: 10px; background-color: rgba(15, 52, 96, 0.7); border: 1px solid #4CAF50; margin-bottom: 20px;">
                    <p style="color: #4CAF50; margin: 0;"><span style="font-size: 18px;">✓</span> File uploaded successfully</p>
                </div>
            """, unsafe_allow_html=True)

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

    # Enhanced sidebar with premium styling
    st.sidebar.markdown("""
        <div style="
            padding: 15px; 
            border-radius: 12px; 
            background: linear-gradient(135deg, rgba(15, 52, 96, 0.85), rgba(233, 69, 96, 0.85)); 
            border: 2px solid #e94560; 
            margin-bottom: 20px;
            box-shadow: 2px 2px 10px rgba(233, 69, 96, 0.3);
            text-align: center;
        ">
            <h3 style="color: #fff; margin: 0; font-size: 22px; font-weight: bold;">🔍 Filters & Controls</h3>
        </div>
    """, unsafe_allow_html=True)

    # Date selection with premium styling
    selected_date = st.sidebar.date_input("Select Analysis Date", datetime.datetime.now())

    # Ensure there are employers to select from
    if "Employer" in df.columns and not df["Employer"].empty:
        selected_employer = st.sidebar.selectbox("Select Employer", df["Employer"].unique())
    else:
        st.error("No employer data found in the file")
        st.stop()

    # Add option for y-axis scaling with premium styling
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

    # Create a dataframe for the last 30 days data
    end_date_30 = pd.to_datetime(selected_date)
    start_date_30 = end_date_30 - pd.Timedelta(days=29)
    df_last_30_days = df[(df["Employer"] == selected_employer) &
                         (df["Date"] >= start_date_30) &
                         (df["Date"] <= end_date_30)].copy()
    df_last_30_days = df_last_30_days.sort_values(by="Date")

    # Add premium dashboard header
    st.markdown(f"""
        <div style="background: linear-gradient(90deg, #0f3460, #e94560); padding: 15px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">
            <h1 style="text-align: center; color: white; margin: 0; font-size: 32px;">Hours Trend Analysis</h1>
            <p style="text-align: center; color: white; margin: 5px 0 0 0; font-size: 18px;">{selected_employer} | {selected_date.strftime('%B %d, %Y')}</p>
        </div>
    """, unsafe_allow_html=True)


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
        ("HourlyEnrolledWorked", "Hourly Enrolled Users"),
        ("Total Hours(Enrolled + Unenrolled)", "Total Hours (Enrolled + Unenrolled)"),
        ("Employees in TA", "Employees in TA")
    ]

    metrics_results = {}
    for column_name, display_name in metrics_to_calculate:
        if column_name in df.columns:
            avg, reflected, difference = calculate_summary(column_name)
            metrics_results[display_name] = (avg, reflected, difference)

    # Summary Section - Premium design
    st.sidebar.markdown("<h3 style='text-align: center; color: #e94560;'>📊 Summary Overview</h3>",
                        unsafe_allow_html=True)

    with st.sidebar:
        def display_summary(title, avg, reflected, difference):
            color = "#e74c3c" if difference < 0 else "#2ecc71"
            diff_icon = "🔻" if difference < 0 else "▲"
            formatted_diff = f"<span style='color:{color}; font-weight:bold;'>{diff_icon} {difference:.2f}%</span>"

            return f"""
                <div style="padding: 12px; border-radius: 10px; background-color: rgba(15, 52, 96, 0.7); margin-bottom: 12px; border-left: 4px solid {color}; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                    <h5 style="margin: 0; color: #e7e7e7;">{title}</h5>
                    <p style="margin: 4px 0;"><b>Average:</b> <span style="color: #e7e7e7;">{avg:.2f}</span></p>
                    <p style="margin: 4px 0;"><b>Current:</b> <span style="color: #e7e7e7;">{reflected:.2f}</span></p>
                    <p style="margin: 4px 0;"><b>Difference:</b> {formatted_diff}</p>
                </div>
                """


        # Display summary for each metric
        for title, (avg, reflected, difference) in metrics_results.items():
            st.markdown(display_summary(title, avg, reflected, difference), unsafe_allow_html=True)

    # Create a premium centered title with proper styling
    st.markdown("""
        <div style="
            background: linear-gradient(90deg, #0f3460, #e94560);
            padding: 15px;
            border-radius: 10px;
            margin: 30px 0 20px 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            text-align: center;
        ">
            <h2 style="color: white; margin: 0; font-size: 28px; font-weight: bold;">Key Performance Indicators</h2>
        </div>
    """, unsafe_allow_html=True)

    # Create columns for displaying summary boxes
    cols = st.columns(4)


    def display_summary(col, title, avg, reflected, difference, icon="📊"):
        """
        Function to display a visually enhanced summary box with animations.
        """
        # Define colors and icons based on the difference value
        if difference < 0:
            bg_gradient = "linear-gradient(45deg, #ff7675, #d63031)"
            text_color = "#ffffff"
            icon_color = "#fab1a0"
            diff_icon = "📉"
        else:
            bg_gradient = "linear-gradient(45deg, #55efc4, #00b894)"
            text_color = "#ffffff"
            icon_color = "#c6f6d5"
            diff_icon = "📈"

        # Assign new icons for each summary box
        icon_dict = {
            "Enrolled Hours": "⏱️",
            "Hourly Enrolled Users": "👨‍💼",
            "Total Hours (Enrolled + Unenrolled)": "⏲️",
            "Employees in TA": "👥"
        }

        # Use the title to determine the icon, default to 📊 if title is not in dictionary
        icon = icon_dict.get(title, "📊")

        # Simplified HTML structure that will render properly in Streamlit
        html = f"""
            <div style="background: {bg_gradient}; border-radius: 12px; padding: 20px; 
                        text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.15); 
                        height: 100%; color: {text_color};">
                <div style="font-size: 2rem; margin-bottom: 10px; color: {icon_color};">{icon}</div>
                <h3 style="margin: 0; font-weight: bold;">{title}</h3>
                <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                    <div style="text-align: center; flex: 1;">
                        <p style="margin: 0; font-size: 1.2rem; opacity: 0.8;">Average</p>
                        <p style="margin: 5px 0; font-size: 1.5rem; font-weight: bold;">{avg:.1f}</p>
                    </div>
                    <div style="text-align: center; flex: 1;">
                        <p style="margin: 0; font-size: 1.2rem; opacity: 0.8;">Current</p>
                        <p style="margin: 5px 0; font-size: 2rem; font-weight: bold;">{reflected:.1f}</p>
                    </div>
                </div>
                <div style="background-color: rgba(255,255,255,0.2); border-radius: 30px; 
                            padding: 8px 15px; margin-top: 15px; display: inline-block; font-size: 1.5rem;">
                    <span style="font-weight: bold;">
                        {diff_icon} {abs(difference):.1f}%
                    </span>
                </div>
            </div>
        """

        # Render the HTML
        col.markdown(html, unsafe_allow_html=True)


    # Display summaries dynamically across columns
    for i, (title, (avg, reflected, difference)) in enumerate(metrics_results.items()):
        display_summary(cols[i % len(cols)], title, avg, reflected, difference)

    # Premium styled graphs section
    st.markdown(f"""
            <h2 style='text-align: center; color: #e94560; font-weight: bold; margin: 30px 0 20px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>
                Trend Analysis for {selected_employer}
            </h2>
        """, unsafe_allow_html=True)


    def plot_trend(ax, x, y, title, xlabel, ylabel, color, marker):
        # Premium color scheme
        background_color = '#16213e'
        grid_color = '#1a1a2e'
        title_color = '#e7e7e7'
        line_color = color

        # Set premium background
        ax.set_facecolor(background_color)
        fig = ax.figure
        fig.patch.set_facecolor(background_color)

        # Plot the main line with premium styling
        line = ax.plot(x, y, marker=marker, linestyle='-', color=line_color, linewidth=3,
                       markersize=9, markeredgewidth=2, markeredgecolor='#16213e', label="Data")

        # Add premium gradient fill under the curve
        ax.fill_between(x, y, y.min(), color=line_color, alpha=0.2)

        # Add a subtle 'glow' effect to the line
        for i in range(3):
            ax.plot(x, y, linewidth=4 + i * 2, alpha=0.03, color=line_color)

        # Premium styled axis labels and title
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold', color='#e7e7e7')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold', color='#e7e7e7')
        ax.set_title(title, fontsize=16, fontweight='bold', color=title_color, pad=15)

        # Premium grid styling
        ax.grid(True, linestyle='--', alpha=0.3, color=grid_color)

        # Set x-ticks with premium formatting
        ax.set_xticks(x)
        ax.set_xticklabels(x.dt.strftime('%Y-%m-%d'), rotation=45, ha='right', fontsize=10, color='#e7e7e7')

        # Premium tick parameters
        ax.tick_params(axis='both', colors='#e7e7e7', labelsize=10)

        # Premium styled spines with improved visibility
        for spine in ax.spines.values():
            spine.set_color('#e94560')
            spine.set_linewidth(2)  # Increased from 1 to 2
            spine.set_visible(True)

        # Adding premium data labels
        for i, txt in enumerate(y):
            ax.text(x.iloc[i], y.iloc[i] + (y.max() - y.min()) * 0.02,
                    f"{txt:.1f}", fontsize=10, ha='center',
                    va='bottom', color='#e7e7e7',
                    bbox=dict(boxstyle="round,pad=0.3", fc='#0f3460', ec=color, alpha=0.8, linewidth=1))

        # Premium styled legend
        legend = ax.legend(frameon=True, fontsize=11, loc='upper right')
        legend.get_frame().set_facecolor('#0f3460')
        legend.get_frame().set_edgecolor('#e94560')
        legend.get_frame().set_linewidth(1)
        for text in legend.get_texts():
            text.set_color('#e7e7e7')

        # Set y-axis based on selected option with premium padding
        if y_axis_option == "Start from Zero":
            ax.set_ylim(bottom=0, top=y.max() * 1.15)
        elif y_axis_option == "Auto":
            if len(y) >= 2:
                percent_change = abs((y.iloc[-1] - y.iloc[0]) / y.iloc[0] * 100) if y.iloc[0] != 0 else 0

                if percent_change < 10:
                    data_min = y.min() * 0.98
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

        # Calculate percentage change with premium display
        if len(y) >= 2 and y.iloc[0] != 0:
            percent_change = (y.iloc[-1] - y.iloc[0]) / y.iloc[0] * 100
            change_color = "#e74c3c" if percent_change < 0 else "#2ecc71"
            change_icon = "▼ " if percent_change < 0 else "▲ "

        # Premium layout spacing
        fig.tight_layout()


    # Create a 2x2 grid of premium charts only for metrics that exist in the dataframe
    chart_metrics = [
        ("Enrolled Hours-Hourly", "Enrolled Hours Trend", "#00bcd4", 'o'),
        ("HourlyEnrolledWorked", "Hourly Enrolled Users Trend", "#f39c12", 's'),
        ("Total Hours(Enrolled + Unenrolled)", "Total Hours Trend", "#3498db", 'd'),
        ("Employees in TA", "Employees in TA Trend", "#9b59b6", 'x')
    ]

    # Filter metrics that exist in the dataframe
    available_charts = [m for m in chart_metrics if m[0] in df.columns]

    # Create premium two-column layout
    col1, col2 = st.columns([2, 2])

    # Position to place charts
    positions = [col1, col2, col1, col2]

    for i, (metric, title, color, marker) in enumerate(available_charts):
        position = positions[i % len(positions)]

        with position:
            # Create a premium container for each chart
            st.markdown(f"""
                    <div style="padding: 10px; border-radius: 10px; background-color: rgba(15, 52, 96, 0.7); border: 1px solid {color}; margin-bottom: 20px;">
                        <h4 style="margin: 0 0 10px 0; color: {color}; text-align: center;">{title}</h4>
                    </div>
                """, unsafe_allow_html=True)

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
                        horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
                        color='#e7e7e7', fontsize=14)

            st.pyplot(fig)

    # And for the Time Period Analysis section:
    st.markdown(f"""
        <h2 class="section-header" style='text-align: center; font-weight: bold;'>
            Time Period Analysis for {selected_employer}
        </h2>
    """, unsafe_allow_html=True)

    # Premium styled tabs
    tab1, tab2 = st.tabs(["📊 Last 7 Days View", "📈 Last 30 Days View"])

    with tab1:
        # Last 7 Days View
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

    with tab2:
        # Last 30 Days View with Bar Charts
        if "Total Hours(Enrolled + Unenrolled)" in df.columns and not df_last_30_days.empty:
            col1, col2 = st.columns([1, 1])

            # Main 30-day bar chart for Total Hours
            with col1:
                fig, ax = plt.subplots(figsize=(12, 6))

                # Enhanced Bar chart for Total Hours with gradient
                bars = ax.bar(
                    df_last_30_days["Date"],
                    df_last_30_days["Total Hours(Enrolled + Unenrolled)"],
                    color="#3498db",  # Updated to a more premium blue
                    alpha=0.85,
                    width=0.7,
                    edgecolor='#2980b9',  # Adds subtle edge for depth
                    linewidth=1
                )

                # Improved data labels with better positioning and formatting
                for bar in bars:
                    height = bar.get_height()
                    ax.text(
                        bar.get_x() + bar.get_width() / 2.,
                        height + 0.5,  # Reduced distance from bar top
                        f'{height:.1f}',
                        ha='center',
                        va='bottom',
                        fontsize=9,
                        rotation=0,  # Changed to horizontal for better readability
                        fontweight='bold',
                        color='#34495e'
                    )

                # Enhanced chart styling
                ax.set_facecolor('#f8f9fa')  # Lighter background
                fig.patch.set_facecolor('#f8f9fa')
                ax.set_xlabel("Date", fontsize=11, fontweight='bold', color='#34495e')
                ax.set_ylabel("Total Hours", fontsize=13, fontweight='bold', color='black')

                ax.set_title(f"Total Hours (Last 30 Days) for {selected_employer}", fontsize=14, fontweight='bold',
                             color='#2c3e50', pad=15)
                ax.grid(True, linestyle='--', alpha=0.5, color='#34495e', axis='y')

                # Format x-axis dates with better spacing
                ax.set_xticks(df_last_30_days["Date"])
                ax.set_xticklabels(df_last_30_days["Date"].dt.strftime('%b %d'), rotation=45, ha='right', fontsize=11,
                                   color='black', fontweight='bold')

                # Enhanced spines with better visibility
                for spine in ax.spines.values():
                    spine.set_color('#34495e')  # Darker color for better visibility
                    spine.set_linewidth(1.5)  # Thicker line
                    spine.set_visible(True)  # Ensure they're visible
                    # Improve axis label visibility
                    ax.tick_params(axis='x', colors='black', labelsize=11)
                    ax.tick_params(axis='y', colors='black', labelsize=11)

                # Y-axis scaling options
                if y_axis_option == "Start from Zero":
                    ax.set_ylim(bottom=0, top=df_last_30_days["Total Hours(Enrolled + Unenrolled)"].max() * 1.15)
                elif y_axis_option == "Fixed Range":
                    global_min = df[df["Employer"] == selected_employer][
                                     "Total Hours(Enrolled + Unenrolled)"].min() * 0.93
                    global_max = df[df["Employer"] == selected_employer][
                                     "Total Hours(Enrolled + Unenrolled)"].max() * 1.07
                    ax.set_ylim(bottom=global_min, top=global_max)

                # Enhanced legend
                ax.legend(frameon=True, fancybox=True, framealpha=0.9, fontsize=10, loc='upper right',
                          edgecolor='#cccccc', shadow=True)

                fig.tight_layout()
                st.pyplot(fig)

            # Additional bar chart for 30-day Enrolled Hours
            with col2:
                if "Enrolled Hours-Hourly" in df.columns:
                    fig, ax = plt.subplots(figsize=(12, 6))

                    # Enhanced Bar chart for Enrolled Hours
                    bars = ax.bar(
                        df_last_30_days["Date"],
                        df_last_30_days["Enrolled Hours-Hourly"],
                        color="#27ae60",  # Updated premium green
                        alpha=0.85,
                        width=0.7,
                        edgecolor='#219653',  # Edge color for depth
                        linewidth=1
                    )

                    # Improved data labels
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(
                            bar.get_x() + bar.get_width() / 2.,
                            height + 0.5,
                            f'{height:.1f}',
                            ha='center',
                            va='bottom',
                            fontsize=9,
                            rotation=0,
                            fontweight='bold',
                            color='#34495e'
                        )

                    # Enhanced styling
                    ax.set_facecolor('#f8f9fa')
                    fig.patch.set_facecolor('#f8f9fa')
                    ax.set_xlabel("Date", fontsize=11, fontweight='bold', color='#34495e')
                    ax.set_ylabel("Enrolled Hours", fontsize=11, fontweight='bold', color='#34495e')
                    ax.set_title(f"Enrolled Hours (Last 30 Days) for {selected_employer}", fontsize=14,
                                 fontweight='bold', color='#2c3e50', pad=15)
                    ax.grid(True, linestyle='--', alpha=0.5, color='#dddddd', axis='y')

                    # Format x-axis dates with better labels
                    ax.set_xticks(df_last_30_days["Date"])
                    ax.set_xticklabels(df_last_30_days["Date"].dt.strftime('%b %d'), rotation=45, ha='right',
                                       fontsize=11, color='black', fontweight='bold')
                    # Improve axis label visibility
                    ax.tick_params(axis='x', colors='black', labelsize=11)
                    ax.tick_params(axis='y', colors='black', labelsize=11)

                    # Add subtle spines
                    for spine in ax.spines.values():
                        spine.set_color('#dddddd')
                        spine.set_linewidth(0.8)

                    # Y-axis scaling options
                    if y_axis_option == "Start from Zero":
                        ax.set_ylim(bottom=0, top=df_last_30_days["Enrolled Hours-Hourly"].max() * 1.15)
                    elif y_axis_option == "Fixed Range":
                        global_min = df[df["Employer"] == selected_employer]["Enrolled Hours-Hourly"].min() * 0.93
                        global_max = df[df["Employer"] == selected_employer]["Enrolled Hours-Hourly"].max() * 1.07
                        ax.set_ylim(bottom=global_min, top=global_max)

                    # Enhanced legend
                    ax.legend(frameon=True, fancybox=True, framealpha=0.9, fontsize=10, loc='upper right',
                              edgecolor='#cccccc', shadow=True)

                    fig.tight_layout()
                    st.pyplot(fig)
        else:
            st.warning("No enrolled hours data available for the last 30 days view.")

            # Enhanced monthly statistics summary with better UI
            if not df_last_30_days.empty:
                st.markdown("### 30-Day Statistics and Insights")

                # Calculate monthly statistics with additional metrics
                monthly_stats = {
                    "Total Hours": {
                        "Average": df_last_30_days["Total Hours(Enrolled + Unenrolled)"].mean(),
                        "Maximum": df_last_30_days["Total Hours(Enrolled + Unenrolled)"].max(),
                        "Minimum": df_last_30_days["Total Hours(Enrolled + Unenrolled)"].min(),
                        "Total": df_last_30_days["Total Hours(Enrolled + Unenrolled)"].sum(),
                    }
                }

                if "Enrolled Hours-Hourly" in df.columns:
                    # Calculate enrolled trend
                    x_enrolled = np.arange(len(df_last_30_days))
                    y_enrolled = df_last_30_days["Enrolled Hours-Hourly"].values
                    z_enrolled = np.polyfit(x_enrolled, y_enrolled, 1)

                    monthly_stats["Enrolled Hours"] = {
                        "Average": df_last_30_days["Enrolled Hours-Hourly"].mean(),
                        "Maximum": df_last_30_days["Enrolled Hours-Hourly"].max(),
                        "Minimum": df_last_30_days["Enrolled Hours-Hourly"].min(),
                        "Total": df_last_30_days["Enrolled Hours-Hourly"].sum(),
                    }

                # Display summary cards in a more streamlined way
                metric_cols = st.columns(len(monthly_stats))

                for i, (metric_name, stats) in enumerate(monthly_stats.items()):
                    with metric_cols[i]:
                        # Determine trend color and icon
                        trend_color = "#4CAF50" if stats["Trend"] == "+" else "#FF5252"
                        trend_icon = "↗" if stats["Trend"] == "+" else "↘"
                        trend_value = f"{abs(z_enrolled[0] * 100):.2f}%"

                        # Create premium-styled card with proper HTML escaping
                        st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #1e3a5f, #162d4a); 
                                border-radius: 12px; 
                                padding: 20px; 
                                color: white; 
                                margin-bottom: 15px;
                                box-shadow: 3px 3px 12px rgba(0, 0, 0, 0.3);
                            ">
                                <h3 style="text-align: center; color: #ff6b6b; font-weight: bold; margin-bottom: 12px;">{metric_name}</h3>

                                <div style="display: flex; justify-content: space-between; padding: 5px 10px;">
                                    <div style="text-align: left;">
                                        <p style="margin: 5px 0; font-weight: bold; color: #FFD700;">Average:</p>
                                        <p style="margin: 5px 0; font-weight: bold; color: #FFD700;">Maximum:</p>
                                    </div>
                                    <div style="text-align: right;">
                                        <p style="margin: 5px 0; font-weight: bold;">{stats["Average"]:.2f}</p>
                                        <p style="margin: 5px 0; font-weight: bold;">{stats["Maximum"]:.2f}</p>
                                    </div>
                                </div>

                                <div style="display: flex; justify-content: space-between; padding: 5px 10px;">
                                    <div style="text-align: left;">
                                        <p style="margin: 5px 0; font-weight: bold; color: #FFD700;">Minimum:</p>
                                        <p style="margin: 5px 0; font-weight: bold; color: #FFD700;">Total:</p>
                                    </div>
                                    <div style="text-align: right;">
                                        <p style="margin: 5px 0; font-weight: bold;">{stats["Minimum"]:.2f}</p>
                                        <p style="margin: 5px 0; font-weight: bold;">{stats["Total"]:.2f}</p>
                                    </div>
                                </div>

                                <div style="margin-top: 12px; text-align: center; padding: 8px; background: rgba(255, 255, 255, 0.1); border-radius: 8px;">
                                    <span style="color: {trend_color}; font-size: 1.3em; font-weight: bold;">{trend_icon} {trend_value}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                else:
                    st.warning("No data available for the last 30 days view.")
            else:
                st.info("Please upload a CSV file to start.")
# Add a premium section header for the trend data table with more spacing
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)  # Add space before the section

# Check if a file has been uploaded before trying to use selected_employer
if uploaded_file is not None:
    st.markdown(f"""
        <h2 class="section-header" style='text-align: center; font-weight: bold;'>
            Historical Trend Data for {selected_employer}
        </h2>
    """, unsafe_allow_html=True)

    # Display trend data with enhanced styling and download option
    if df_trend.empty:
        st.warning("No trend data found for previous same weekdays.")
    else:
        # Create a container for better spacing and organization
        with st.container():

            with col1:
                st.markdown("""
                <h3 style="margin-top: 10px; margin-bottom: 5px; color: #e94560;">Complete Trend Analysis Dataset</h3>
            """, unsafe_allow_html=True)

        with col2:
            # Generate CSV download button with improved styling
            csv = df_trend.to_csv(index=False)
            st.markdown("""
                <style>
                /* Custom styling for the download button */
                div[data-testid="stDownloadButton"] button {
                    background-color: #0a2040 !important;
                    color: #FFFF00 !important; /* Bright yellow text for maximum contrast */
                    border: 2px solid #e94560 !important;
                    padding: 10px !important;
                    font-weight: 800 !important;
                    font-size: 16px !important;
                    border-radius: 8px !important;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4) !important;
                    text-shadow: 1px 1px 2px #000000 !important;
                    transition: all 0.3s ease !important;
                    width: 100% !important;
                    margin-top: 10px !important;
                }
                div[data-testid="stDownloadButton"] button:hover {
                    background-color: #e94560 !important;
                    color: #FFFFFF !important;
                    border-color: #0a2040 !important;
                    transform: translateY(-2px) !important;
                    box-shadow: 0 6px 15px rgba(233, 69, 96, 0.4) !important;
                }
                div[data-testid="stDownloadButton"] svg {
                    margin-right: 5px !important;
                    fill: #FFFF00 !important; /* Match the text color */
                }
                div[data-testid="stDownloadButton"] p {
                    color: #FFFF00 !important; /* Also style any text within the button */
                }
                </style>
            """, unsafe_allow_html=True)

            st.download_button(
                label="📥 Download Data",
                data=csv,
                file_name=f"{selected_employer}_trend_data.csv",
                mime="text/csv",
                key="download-csv",
                help="Download the complete trend dataset as CSV",
                use_container_width=True,
            )

        # Add premium styling for the table
        st.markdown("""
            <style>
            .trend-table {
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 0.9em;
                font-family: 'DejaVu Sans', sans-serif;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
                border-radius: 12px;
                overflow: hidden;
                width: 100%;
            }
            .trend-table thead tr {
                background: linear-gradient(90deg, #0f3460, #e94560);
                color: #fff;
                text-align: center;
                font-weight: bold;
            }
            .trend-table th, .trend-table td {
                padding: 12px 15px;
                text-align: center;
            }
            .trend-table tbody tr {
                border-bottom: 1px solid rgba(15, 52, 96, 0.1);
                background-color: rgba(15, 52, 96, 0.05);
            }
            .trend-table tbody tr:nth-of-type(even) {
                background-color: rgba(15, 52, 96, 0.1);
            }
            .trend-table tbody tr:hover {
                background-color: rgba(233, 69, 96, 0.1);
                transition: all 0.3s ease;
            }
            .trend-table tbody tr:last-of-type {
                border-bottom: 3px solid #e94560;
            }
            </style>
        """, unsafe_allow_html=True)

        # Convert the DataFrame to an HTML table with custom styling
        html_table = df_trend.to_html(classes="trend-table", escape=False, index=False)
        st.markdown(html_table, unsafe_allow_html=True)

        # Add info card below the table
        st.markdown("""
            <div style="
                padding: 15px; 
                border-radius: 12px; 
                background: linear-gradient(135deg, rgba(15, 52, 96, 0.85), rgba(233, 69, 96, 0.85)); 
                border: 2px solid #e94560; 
                margin-top: 20px;
                margin-bottom: 30px;
                box-shadow: 2px 2px 10px rgba(233, 69, 96, 0.3);
                text-align: center;
            ">
                <p style="color: white; margin: 0; font-size: 16px;">
                    <span style="font-size: 20px;">ℹ️</span> 
                    This table displays historical data for the same weekday, providing context for trend analysis
                </p>
            </div>
        """, unsafe_allow_html=True)

# Continue tracking analytics until the end of your app
# The stop_tracking is now inside our if statement above to show the dashboard when needed