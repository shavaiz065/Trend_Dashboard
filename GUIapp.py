import streamlit as st
import pandas as pd

# Load Data
df = pd.read_csv("TAReport - UKG.csv")

# App Title
st.title("Employer Data Trend")

# Dropdown for Employer Selection
employer_list = df["Employer"].unique()
selected_employer = st.selectbox("Select Employer", employer_list)

# Show Data for Selected Employer
filtered_df = df[df["Employer"] == selected_employer]
st.dataframe(filtered_df)
