import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# Check if file is uploaded
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading the uploaded file: {e}")
        st.stop()

    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df = df.dropna(subset=["Date"])

    selected_date = st.sidebar.date_input("Select a date", pd.to_datetime("today"))
    selected_employer = st.sidebar.selectbox("Select Employer", df["Employer"].unique())

    # Filter data based on selection
    df_selected_date = df[(df["Employer"] == selected_employer) & (df["Date"] == pd.to_datetime(selected_date))]
    selected_weekday = pd.to_datetime(selected_date).weekday()
    df_trend = df[(df["Employer"] == selected_employer) & (df["Date"].dt.weekday == selected_weekday)].copy()
    df_trend = df_trend.sort_values(by="Date")

    # Summary Metrics Calculation
    def calculate_summary(metric):
        avg = df_trend[metric].mean() if metric in df_trend.columns else 0
        reflected = df_selected_date[metric].values[0] if metric in df_selected_date.columns and not df_selected_date.empty else 0
        difference = ((reflected - avg) / avg * 100) if avg != 0 else 0
        return avg, reflected, difference

    avg_enrolled_hours, reflected_hours, difference_enrolled = calculate_summary("Enrolled Hours-Hourly")
    avg_hourly_enrolled_worked, reflected_hourly_enrolled_worked, difference_hourly_enrolled_worked = calculate_summary("HourlyEnrolledWorked")
    avg_total_hours, reflected_total_hours, difference_total_hours = calculate_summary("Total Hours(Enrolled + Unenrolled)")
    avg_employees_in_ta, reflected_employees_in_ta, difference_employees_in_ta = calculate_summary("Employees in TA")

    # Summary Section
    st.sidebar.markdown("<h2 style='text-align: center;'>📊 Summary Overview</h2>", unsafe_allow_html=True)

    with st.sidebar:
        def display_summary(title, avg, reflected, difference):
            color = "red" if difference < 0 else "green"
            diff_icon = "🔻" if difference < 0 else "🔺"
            formatted_diff = f"<span style='color:{color}; font-weight:bold;'>{diff_icon} {difference:.2f}%</span>"

            return f"""
            <div style="padding: 12px; border-radius: 8px; background-color: #f8f9fa; margin-bottom: 8px;">
                <h5 style="margin: 0; color: #333;">{title}</h5>
                <p style="margin: 4px 0;"><b>Average:</b> {avg:.2f}</p>
                <p style="margin: 4px 0;"><b>Reflected on ({selected_date}):</b> {reflected:.2f}</p>
                <p style="margin: 4px 0;"><b>Difference:</b> {formatted_diff}</p>
            </div>
            """

        st.markdown(display_summary("Enrolled Hours", avg_enrolled_hours, reflected_hours, difference_enrolled), unsafe_allow_html=True)
        st.markdown(display_summary("Hourly Enrolled Worked", avg_hourly_enrolled_worked, reflected_hourly_enrolled_worked, difference_hourly_enrolled_worked), unsafe_allow_html=True)
        st.markdown(display_summary("Total Hours (Enrolled + Unenrolled)", avg_total_hours, reflected_total_hours, difference_total_hours), unsafe_allow_html=True)
        st.markdown(display_summary("Employees in TA", avg_employees_in_ta, reflected_employees_in_ta, difference_employees_in_ta), unsafe_allow_html=True)

    # Graphs Section
    st.markdown(f"<h2 style='text-align: center;'>Trend Data for {selected_employer}</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 2])

    def plot_trend(ax, x, y, title, xlabel, ylabel, color, marker):
        ax.plot(x, y, marker=marker, linestyle='-', color=color, label="Data")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(x.dt.strftime('%Y-%m-%d'), rotation=45)

        # Adding data labels in black
        for i, txt in enumerate(y):
            ax.text(x.iloc[i], y.iloc[i], f"{txt:.2f}", fontsize=10, ha='center', va='bottom', color='black')

        if len(x) > 1:
            z = np.polyfit(x.index, y, 1)
            p = np.poly1d(z)
            ax.plot(x, p(x.index), "--", color="orange", label="Trend Line")

        ax.legend()

    with col1:
        fig, ax = plt.subplots(figsize=(12, 6))
        if not df_trend.empty:
            plot_trend(ax, df_trend["Date"], df_trend["Enrolled Hours-Hourly"],
                       f"Enrolled Hours Trend for {selected_employer}", "Date", "Enrolled Hours", "#00bcd4", 'o')
        st.pyplot(fig)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        if not df_trend.empty and "HourlyEnrolledWorked" in df_trend.columns:
            plot_trend(ax2, df_trend["Date"], df_trend["HourlyEnrolledWorked"],
                       f"Hourly Enrolled Worked Trend for {selected_employer}", "Date", "Hourly Enrolled Worked", "red", 's')
        st.pyplot(fig2)

    col3, col4 = st.columns([2, 2])

    with col3:
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        if not df_trend.empty and "Total Hours(Enrolled + Unenrolled)" in df_trend.columns:
            plot_trend(ax3, df_trend["Date"], df_trend["Total Hours(Enrolled + Unenrolled)"],
                       f"Total Hours (Enrolled + Unenrolled) Trend for {selected_employer}", "Date", "Total Hours", "#00bcd4", 'd')
        st.pyplot(fig3)

    with col4:
        fig4, ax4 = plt.subplots(figsize=(12, 6))
        if not df_trend.empty and "Employees in TA" in df_trend.columns:
            plot_trend(ax4, df_trend["Date"], df_trend["Employees in TA"],
                       f"Employees in TA Trend for {selected_employer}", "Date", "Employees in TA", "blue", 'x')
        st.pyplot(fig4)

    if df_trend.empty:
        st.warning("No trend data found for previous same weekdays.")
    else:
        st.write(df_trend)

else:
    st.info("Please upload a CSV file to start.")
