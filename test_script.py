import streamlit as st

# ✅ Define selected_employer at the very start
selected_employer = "No Employer Selected"

# 🔍 Debugging: Check if selected_employer is recognized
st.write("🔍 DEBUG 1: selected_employer =", selected_employer)

# ✅ Check if selected_employer exists in globals
if "selected_employer" in globals():
    st.success(f"✅ selected_employer exists in globals: {selected_employer}")
else:
    st.error("❌ selected_employer is NOT in globals! Something is wrong.")

# ✅ Now use selected_employer safely
st.markdown(f"""
    <h2 style='text-align: center;'>
        Historical Trend Data for {selected_employer}
    </h2>
""", unsafe_allow_html=True)
