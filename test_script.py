import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from streamlit_extras.stray import stray

# Initialize tracking
stray(tracking_id="YOUR_STRAY_ID", page_name="Dashboard")

# App title
st.title("Sales Dashboard")
st.markdown("A simple dashboard with Stray analytics integration")

# Sample data
data = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'Sales': [100, 150, 130, 190, 210]
})

# Display data
st.subheader("Sales Data")
st.dataframe(data)

# Chart
st.subheader("Sales Chart")
st.line_chart(data.set_index('Month'))

# Interactive element
if st.button("Generate Report"):
    # Track custom event
    components.html(
        """
        <script>
        if (typeof stray !== 'undefined') {
            stray.track('report_generated');
        }
        </script>
        """,
        height=0
    )
    st.success("Report generated successfully!")